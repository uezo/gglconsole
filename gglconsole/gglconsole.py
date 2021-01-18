import os
import sys
import traceback
from abc import ABCMeta, abstractmethod
import readline
import webbrowser
import urllib.parse
import json
import requests
from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel


class SearchResult:
    def __init__(self, title, url, snippet):
        self.title = title
        self.url = url
        self.snippet = snippet


class SearchResponse:
    def __init__(self, results, total_count_display, web_search_url, error_json=None):
        self.results = results
        self.total_count_display = total_count_display
        self.web_search_url = web_search_url
        self.error_json = error_json


class SearchEngineBase(metaclass=ABCMeta):
    @abstractmethod
    def configure(self, config):
        pass

    @abstractmethod
    def get_search_url(self, q):
        pass

    @abstractmethod
    def search(self, q, start, count):
        pass


class GoogleEngine(SearchEngineBase):
    def __init__(self, config):
        self.api_key = config.get("google_api_key")
        self.cx = config.get("google_cx") or "253ce3c27ae6de09f"

    def configure(self, config):
        updated = False

        while not self.api_key:
            self.api_key = input("Google API key: ")
            config["google_api_key"] = self.api_key
            updated = True

        return updated

    def get_search_url(self, q):
        return f"https://www.google.com/search?ie=UTF-8&oe=UTF-8&q={urllib.parse.quote(q)}"

    def search(self, q, start, count):
        url = f"https://customsearch.googleapis.com/customsearch/v1?key={self.api_key}&cx={self.cx}&start={start}&num={count}&q={urllib.parse.quote(q)}"
        resp = requests.get(url, timeout=10).json()
        if "items" in resp:
            results = [SearchResult(title=r["title"], url=r["link"], snippet=r.get("snippet") or "") for r in resp["items"]]
            return SearchResponse(
                results,
                resp["searchInformation"]["formattedTotalResults"],
                self.get_search_url(q))
        else:
            return SearchResponse([], "", "", resp)


class BingEngine(SearchEngineBase):
    def __init__(self, config):
        self.api_key = config.get("bing_api_key")

    def configure(self, config):
        updated = False

        while not self.api_key:
            self.api_key = input("Bing API key: ")
            config["bing_api_key"] = self.api_key
            updated = True

        return updated

    def get_search_url(self, q):
        return f"https://www.bing.com/search?q={urllib.parse.quote(q)}"

    def search(self, q, start, count):
        headers = {"Ocp-Apim-Subscription-Key": self.api_key}
        url = f"https://api.bing.microsoft.com/v7.0/search?offset={start - 1}&count={count}&q={urllib.parse.quote(q)}"
        resp = requests.get(url, headers=headers, timeout=10).json()
        if "webPages" in resp and "value" in resp["webPages"]:
            results = [SearchResult(title=r["name"], url=r["url"], snippet=r.get("snippet") or "") for r in resp["webPages"]["value"]]
            return SearchResponse(
                results,
                str(resp["webPages"]["totalEstimatedMatches"]),
                resp["webPages"]["webSearchUrl"])

        else:
            return SearchResponse([], "", "", resp)


class QiitaEngine(SearchEngineBase):
    def __init__(self, config):
        self.api_key = config.get("qiita_api_key")

    def configure(self, config):
        updated = False

        while not self.api_key:
            self.api_key = input("Qiita API key: ")
            config["qiita_api_key"] = self.api_key
            updated = True

        return updated

    def get_search_url(self, q):
        return f"https://qiita.com/search?q={urllib.parse.quote(q)}"

    def search(self, q, start, count):
        page = int((start - 1) / count) + 1
        headers = {"Authorization": "Bearer " + self.api_key}
        url = f"https://qiita.com/api/v2/items?page={page}&per_page={count}&query={urllib.parse.quote(q)}"
        resp = requests.get(url, headers=headers, timeout=10).json()
        if resp:
            results = [SearchResult(
                title=r["title"],
                url=r["url"],
                snippet=f'LGTM: {str(r["likes_count"])} | Update: {r["updated_at"][:10]}') for r in resp]

            return SearchResponse(
                results,
                "-",
                self.get_search_url(q))

        else:
            return SearchResponse([], "", "", resp)


class GGLConsole:
    def __init__(self, config_path=None, search_engine_class=None):
        self.console = Console(highlight=False)

        self.config_path = config_path \
            or os.path.join(os.path.expanduser("~"), ".gglconsole/gglconsole.json")
        config = self.get_config()

        self.prompt = config.get("prompt")
        self.show_banner = config.get("show_banner")
        self.config_command = config.get("config_command")
        self.exit_on_end = config.get("exit_on_end")
        self.exit_on_ctrlc = config.get("exit_on_ctrlc")
        self.exit_commands = config.get("exit_commands")
        self.index_delimiter = config.get("index_delimiter")
        self.count = config.get("count")
        self.browser_target = config.get("browser_target")
        self.use_api = config.get("use_api")

        self.title_style = config.get("title_style")
        self.link_style = config.get("link_style")
        self.snippet_style = config.get("snippet_style")

        search_engine_class = search_engine_class\
            or globals()[config.get("search_engine_class")]
        self.search_engine = search_engine_class(config=config)

    @staticmethod
    def escape_rich(text):
        if not text:
            return ""
        return text.replace("[", "\[").replace("\n", "")

    @staticmethod
    def parse_int(text):
        try:
            return int(text)
        except Exception:
            return None

    def get_config(self):
        if not os.path.isfile(self.config_path):
            config = {}
        else:
            with open(self.config_path, "r") as f:
                config = json.load(f)

        # apply default values
        config["search_engine_class"] =\
            config.get("search_engine_class") or "GoogleEngine"
        config["prompt"] = config.get("prompt") or "何について調べますか？🐬"
        config["show_banner"] = True\
            if config.get("show_banner") is not False else False
        config["config_command"] = config.get("config_command") or "--config"
        config["exit_on_end"] = False\
            if config.get("exit_on_end") is not True else True
        config["exit_on_ctrlc"] = config.get("exit_on_ctrlc") or True
        config["exit_commands"] = ["exit", "quit", "\q"]\
            if config.get("exit_commands") is None\
            else config.get("exit_commands")
        config["index_delimiter"] = config.get("index_delimiter") or " "
        config["count"] = config.get("count") or 10
        config["browser_target"] = config.get("browser_target") or 0
        config["use_api"] = False\
            if config.get("use_api") is not True else True
        config["title_style"] = config.get("title_style") or "bold bright_white"
        config["link_style"] = config.get("link_style") or "blue underline"
        config["snippet_style"] = config.get("snippet_style") or "white"

        # save configurations to apply default values
        os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
        with open(self.config_path, "w") as f:
            json.dump(config, f, indent=4, ensure_ascii=False)

        return config

    def configure(self):
        self.get_config()
        self.console.print(f"Open '{self.config_path}' manually and configure it.")

    def enable_api(self, use_api):
        config = self.get_config()
        config["use_api"] = use_api
        if use_api:
            self.search_engine.configure(config)
        with open(self.config_path, "w") as f:
            json.dump(config, f, indent=4, ensure_ascii=False)

    def help(self):
        self.console.print("Usage: ggl|bing [italic]\[keyword1] \[keyword2] \[keyword3] ...[/italic]")
        self.console.print("Help: GGLConsole provides you the CLI for websearch by Google / Bing. `ggl --config` to change configurations.")

    def get_indexes(self, text):
        if self.index_delimiter in text:
            ret = []
            for idx_str in text.split(self.index_delimiter):
                if not idx_str:
                    continue
                idx = self.parse_int(idx_str)
                if idx is not None:
                    ret.append(idx)
                else:
                    return []
            return ret
        else:
            idx = self.parse_int(text)
            if idx is not None:
                return [idx]
            else:
                return []

    def show_browser(self, url):
        webbrowser.open(url, new=self.browser_target)

    def is_exit_requested(self, text):
        if text in self.exit_commands:
            return True
        else:
            return False

    def print_results(self, current_search_results, retrieved_count):
        for i, item in enumerate(reversed(current_search_results)):
            self.console.rule()
            self.console.print(f"[{retrieved_count - i}] {self.escape_rich(item.title)}", style=self.title_style)
            self.console.print(self.escape_rich(item.url), style=self.link_style)
            self.console.print(self.escape_rich(item.snippet), style=self.snippet_style)

    def print_search_info(self, search_word, total_count_display, web_search_url):
        self.console.rule()
        self.console.print(f'Keyword: [bold]{search_word}[/bold] | Total: [bold]{total_count_display}[/bold] | [blue underline]{web_search_url}[/blue underline]')

    def start(self, keyword=None):
        search_word = ""
        search_results = []
        page = 1

        # show banner
        if self.show_banner:
            self.console.print(Panel("🔍[bold]GGLConsole[/bold] by (c)2021 uezo [blue underline]https://twitter.com/uezochan[/blue underline] | " + ", ".join(self.exit_commands) + " to exit"))

        while True:
            try:
                if keyword:
                    user_input = keyword
                    keyword = None
                else:
                    user_input = Prompt.ask(self.prompt)
                user_input = user_input.strip().lower().replace("　", " ")

                # exit when exit_command is input
                if self.is_exit_requested(user_input):
                    break

                # open browser directly if use_api is False
                if not self.use_api:
                    self.show_browser(self.search_engine.get_search_url(user_input))
                    continue

                # show url in browser when index number is input
                input_numbers = self.get_indexes(user_input)
                if search_results and input_numbers:
                    for input_number in input_numbers:
                        if input_number < 1 or input_number > len(search_results):
                            print(f"Invalid index: {input_number} (1 ~ {len(search_results)})")
                        else:
                            self.show_browser(search_results[input_number - 1].url)
                    continue

                if user_input:
                    # get new search results when keyword is input
                    search_word = user_input
                    search_results = []
                    page = 1

                    search_response = self.search_engine.search(search_word, start=1, count=self.count)

                else:
                    if not search_results:
                        continue

                    # get more results when nothing is input
                    page += 1
                    search_response = self.search_engine.search(search_word, start=self.count * (page - 1) + 1, count=self.count)

                    if not search_response.results:
                        page -= 1
                        print("No more result to show")
                        continue

                # show results
                if search_response.results:
                    search_results.extend(search_response.results)
                    self.print_results(
                        search_response.results, len(search_results))
                    if page == 1:
                        self.print_search_info(
                            search_word,
                            search_response.total_count_display,
                            search_response.web_search_url)

                elif search_response.error_json:
                    self.console.print(
                        "[red]ERROR[/red]\n"
                        + json.dumps(
                            search_response.error_json,
                            indent=4, ensure_ascii=False))

                else:
                    print(f"No results for '{user_input}'")

                if self.exit_on_end:
                    break

            except KeyboardInterrupt:
                if self.exit_on_ctrlc:
                    break
                else:
                    print("")

            except Exception as ex:
                self.console.print(
                    f"[red]ERROR: {str(ex)}[/red]\n"
                    + traceback.format_exc())
                raise ex


def main():
    if sys.argv[0].endswith("/bing"):
        # set bing engine if called as bing
        gglconsole = GGLConsole(search_engine_class=BingEngine)
    elif sys.argv[0].endswith("/qiita"):
        # set qiita engine if called as qiita
        gglconsole = GGLConsole(search_engine_class=QiitaEngine)
    else:
        gglconsole = GGLConsole()

    if len(sys.argv) == 2 and sys.argv[1].startswith("--"):
        if sys.argv[1] == gglconsole.config_command:
            gglconsole.configure()
        elif sys.argv[1] == "--console":
            gglconsole.enable_api(True)
        elif sys.argv[1] == "--browser":
            gglconsole.enable_api(False)
        else:
            gglconsole.help()

    elif len(sys.argv) > 1:
        gglconsole.start(" ".join(sys.argv[1:]))

    else:
        gglconsole.start()


if __name__ == "__main__":
    main()
