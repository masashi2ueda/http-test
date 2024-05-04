# 概要
- flaskのdev serverのスペックをチェックする

# 実行
1. composeを起動
    ```sh
    docker compose up
    ```
    - webとuserコンテナが立ち上がる
1. userコンテナで計測が走る
1. 結果がホストの
1. flaskの起動確認→ホストのブラウザでhttp://127.0.0.1:5901/goodにアクセスして、Goodとでればok
1. userコンテナに入る
1. flaskのdev serverのスペックをuserコンテナの中の以下コマンドで測る
    ```sh
    cd /src
    locust -f locustfile.py --headless -u 1000 -r 100 --run-time 10s --csv=output
    ```
    - -fはLocustのテストスクリプトのパスを指定
    - --headlessはGUIなしで実行することを指定
    - -uはシミュレートするユーザーの数を指定
    - -rはユーザーの発生率（秒あたり）を指定
    - --run-timeはテストの実行時間を指定
1. 結果は/srcの中のcsvを確認(ホストの./user/srcにマウントされているので、そこからでも確認できる)

# 参考
- [【Docker × Flask】Locustでflask製のREST APIに負荷をかけてみる](https://scrawledtechblog.com/docker-flask-locust/)
