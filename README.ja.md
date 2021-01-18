# GGLConsole

GGLConsoleはコマンドライン上でGoogle / Bing検索するためのツールです。

[🇬🇧README in English is here](https://github.com/uezo/gglconsole/blob/master/README.ja.md)

![Web search on console](https://github.com/uezo/gglconsole/blob/main/gglconsole/resources/gglconsole.png)

# インストール

```bash
$ pip install gglconsole
```

# ブラウザーモード

`ggl`コマンドに続けて検索キーワードを入力してください。検索結果がブラウザーで表示されます。

```bash
$ ggl python line bot
```

BingまたはQiitaで検索したい場合は`bing`、`qiita`コマンドを使用します。

```bash
$ bing python line bot
$ qiita python line bot
```

# コンソールモード

検索結果の表示まで含めてコンソールで完結するには、まずはコンソールモードを有効にする必要があります。`--console`を使用してAPIキー（Googleの場合はCXも）を入力してください。

```bash
$ ggl --console
Google API key: [YOUR API KEY]
CX: [YOUR CX]
```

他のサービスのコンソールモードを有効にするには、`ggl`ではなく`bing`や`qiita`を使用します。
ブラウザーモードに戻す場合は`--browser`を使用してください。

設定が完了したらブラウザーモードの時と同じようにコマンドに続けて検索キーワードを入力します。

```bash
$ ggl python line bot
```

- 検索結果は一度に10件ずつ表示されます。
- さらに結果を表示するには何も入力せずにエンターキーを押下してください。
- 検索結果のタイトルに付されているインデックス番号を入力すると当該ページがブラウザーで表示されます。半角スペース区切りで複数のインデックスを入力することも可能です。


## APIキーの入手方法

- Google: Cloud ConsoleでCustom Search APIを有効にするか、 https://developers.google.com/custom-search/v1/introduction で`Get a Key`ボタンを押して無償評価用のキーを入手してください（100クエリ/日まで）。任意設定項目として、自身の管理するカスタム検索エンジンを利用するには https://cse.google.com/cse/all で検索エンジンを作成の上`cx`を取得し、これを設定ファイルに `google_cx` というキーで追加してください。
- Bing: Azure PortalにてBing Search V7を作成 https://portal.azure.com/#create/Microsoft.BingSearch します。Level `S6`がこのツールのユースケースには向いていると思います。
- Qiita: 管理画面から個人用アクセストークンを取得してください。 https://qiita.com/settings/applications


# 設定

設定ファイルのパスを表示するには`--config`を使用します。お好みのテキストエディタで開いて内容を修正してください。

```bash
$ ggl --config
```

- search_engine_class: デフォルトのサーチエンジンのクラス名 (GoogleEngine)
- prompt: 検索キーワード入力待ちのプロンプト (何について調べますか？🐬)
- show_banner: 起動時にバナーを表示するかどうか (true)
- config_command: 設定ファイルのパス表示のためのオプション (--config)
- exit_on_end: クエリーを処理後にコマンド入力待機を終了するかどうか (false)
- exit_on_ctrlc: Ctrl+Cでコマンド入力待機を終了するかどうか (true)
- exit_commands: プログラム終了のためのコマンド ([exit, quit, \q])
- index_delimiter: Webページを複数開く時のためのインデックス番号の区切り文字 (" ")
- count: 1クエリーで表示する検索結果の数 (10)
- browser_target: ブラウザの開き方 0:default | 1:new window | 2:new tab (0)
- use_api: コンソールモードにするには`True`、ブラウザーモードにするには`False`をセット (false)
- title_style: 検索結果のタイトルのスタイル (bold bright_white)
- link_style: 検索結果のリンクのスタイル (blue underline)
- snippet_style: 検索結果のスニペットのスタイル (white)
