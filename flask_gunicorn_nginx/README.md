# 概要
- flask+gunicornのスペックをチェックする

# 実行
1. composeを起動
    ```sh
    docker compose up -d
    ```
    - flask+gunicornとuserコンテナが立ち上がる
1. flask+gunicornの起動確認→ホストでhttp://127.0.0.1:5901/goodにアクセスして、Goodとでればok
1. userコンテナに入る
1. flask+gunicornのスペックをuserコンテナの中の/srcで以下コマンドで測る
    ```sh
    locust -f locustfile.py --headless -u 1000 -r 100 --run-time 10s --csv=output
    ```
    - -fはLocustのテストスクリプトのパスを指定
    - --headlessはGUIなしで実行することを指定
    - -uはシミュレートするユーザーの数を指定
    - -rはユーザーの発生率（秒あたり）を指定
    - --run-timeはテストの実行時間を指定
1. 結果は./flask/user/srcのcsvを確認

# お勉強
- /etc/nginx/nginx.conf: メイン設定ファイル
- /etc/nginx/conf.d/default.conf: デフォルトサーバーの設定ファイル
- /etc/nginx/conf.d/ssl/conf: SSLの設定ファイル
- /etc/nginx/conf.d/virtual.conf: バーチャルホストの設定ファイル
- 80番port
    - HTTPは標準では80番ポートを用いるよう規定されているが、プロキシサーバやキャッシュサーバ、組織の内部向けサーバなど特殊な用途のHTTP通信や、サーバのシステム管理者以外の一般ユーザーがWebサーバを起動する場合などにTCPの8080番が使用される。

# 参考
- [【Docker × Flask】Locustでflask製のREST APIに負荷をかけてみる](https://scrawledtechblog.com/docker-flask-locust/)
- [Nginx について纏めてみる](https://qiita.com/leomaro7/items/98d6af85a4e155449aed)
- [8080番ポート 【port 8080】 代替HTTPポート](https://e-words.jp/w/8080%E7%95%AA%E3%83%9D%E3%83%BC%E3%83%88.html#:~:text=HTTP%E3%81%AF%E6%A8%99%E6%BA%96%E3%81%A7%E3%81%AF80,%E7%95%AA%E3%81%8C%E4%BD%BF%E7%94%A8%E3%81%95%E3%82%8C%E3%82%8B%E3%80%82)
