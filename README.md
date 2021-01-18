# GGLConsole

GGLConsole provides you the command line interface for websearch by Google / Bing.

[🇯🇵日本語のREADMEはこちら](https://github.com/uezo/gglconsole/blob/master/README.ja.md)

![Web search on console](https://github.com/uezo/gglconsole/blob/main/gglconsole/resources/gglconsole.png)

# Installation

```bash
$ pip install gglconsole
```

# Browser mode

Input the keywords you want to search as arguments of `ggl` command. The result will be shown in browser.

```bash
$ ggl python line bot
```

If you want to search by Bing or Qiita, use `bing` or `qiita` command.

```bash
$ bing python line bot
$ qiita python line bot
```

# Console mode

To enable console mode, configure API credentials by calling with `--console`.

```bash
$ ggl --console
Google API key: [YOUR API KEY]
```

Replace `ggl` to `bing` or `qiita` to configure other services.
Use `--browser` if you want to switch back to browser mode.

After configuration, input keywords as same as browser mode.

```bash
$ ggl python line bot
```

- 10 results will be shown on console.
- Input enter if you want to retrieve more results.
- Input index number(s) to show the website on browser. You can input multiple indexes devided by space.

## How to get API keys

- Google: Enable Custom Search API on Cloud Console or visit https://developers.google.com/custom-search/v1/introduction and press `Get a Key` button to get a free trial API Key(limited 100 requests/day). If you want to use your own search engine visit https://cse.google.com/cse/all to create and get `cx`, and set it as the value of `google_cx` in configuration file. (Optional)
- Bing: Create Bing Search V7 on Azure Portal https://portal.azure.com/#create/Microsoft.BingSearch Level `S6` is suitable for this use case.
- Qiita: Create personal access token at https://qiita.com/settings/applications

# Configuration

Use `--config` to show the path to configuration file. Open this file with your text editor to change configuration.

```bash
$ ggl --config
```

- search_engine_class: Name of default search engine (GoogleEngine)
- prompt: Prompt message to input keywords (何について調べますか？🐬)
- show_banner: Show banner or not (true)
- config_command: Option to show the path to configuration file (--config)
- exit_on_end: Exit after process 1 query (false)
- exit_on_ctrlc: Exit by Ctrl+C (true)
- exit_commands: Commands to exit ([exit, quit, \q])
- index_delimiter: Delimiter of index numbers (" ")
- count: Numbers of results to show by 1 query. (10)
- browser_target: The window to show the website. 0:default | 1:new window | 2:new tab (0)
- use_api: False for browser mode, True for console mode. (false)
- title_style: rich styles for title of search result. (bold bright_white)
- link_style: rich styles for link of search result. (blue underline)
- snippet_style: rich styles for snippet of search result. (white)
