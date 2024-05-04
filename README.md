# http-test
## 概要
- ①flaskのdevelopment serverをそのまま使った場合、②gunicornを通した場合、③nginxからgunicornを通した場合のそれぞれの動作を確認した

- 結果は以下のようになった
    - gunicornを使うと処理が早くなる
        - →プロセス数が増えるため
    - gunicorn+nginxにするとgunicornより遅くなる
        - →gunicornとnginxとの通信が発生するため？

| 構成 | Average Response Time(ミリ秒)	 |
| ---- | ---- |
| ①flask dev server | 80.44 |
| ②flask dev server + gunicorn | 47.30 |
| ③flask dev server + gunicorn + nginx | 75.52 |


## 再現方法
1. docker composeを使える環境にする
1. 各フォルダ{①:./flask, ②:./flask_gunicorn, ③:./flask_gunicorn_nginx}に入り、docker composeを起動する.以下①flaskの例
    ```sh
    cd flask
    docker compose up
    ```
1. flask/user/src/output_stats.csvに結果が保存される

## メモ
### 各構成
- ①flask
    - webコンテナでflaskを起動
    - userコンテナからflaskにアクセスして、apiの性能テストを行う
- ②flask+gunicorn
    - webコンテナでgunicornを起動＋flaskと通信
    - userコンテナからgunicornにアクセスして、apiの性能テストを行う
- ③flask+gunicorn+nginx
    - webコンテナでgunicornを起動＋flaskと通信
    - nginxコンテナでgunicronと通信
    - userコンテナからnginxにアクセスして、apiの性能テストを行う

### オプション
- gunicornの起動
    - gunicorn -w 4
- apiの性能テスト(locust)
    -  -u 1000 -r 100 --run-time 10s

### ファイルの権限
- docker内で作成したファイルをhostで編集しようとすると権限エラーが出る→hostのユーザとUID、GIDを合わせると問題が起きなくなる
1. まずdocker-compose.yamlで下記を設定(hostのUID: 1000, GID: 1000とする)
    ```
    ...
    services:
        service_name:
            args:
                - UID=1000
                - GID=1000
                - USERNAME=user
                - GROUPNAME=user
    ....
    ```
1. Dockerfileでユーザを作成＋選択
    ```
    ...
    ARG UID
    ARG GID
    ARG USERNAME
    ARG GROUPNAME
    RUN groupadd -g ${GID} ${GROUPNAME} -f && \
        useradd -m -s /bin/bash -u ${UID} -g ${GID} ${USERNAME}

    ...(aptのupdate, installなど)...

    USER ${USERNAME}
    ```


### nginxの設定
- 下記をnginx.confに記載→コンテナにコピーする
```
...(ここから上の部分もないと動かない)...
http {
    server {
        # ここは待ち受けるポートを指定
        listen  80;
        # ここは例にならった
        server_name localhost;

        # ここで飛ばしたい場所を指定
        location / {
            # docker composeではサービス名でコンテナ間の通信が可能(gunicornは5901ポートを開いてある)
            proxy_pass http://web:5901;
        }
    }
}
```


### locustの実行
- docker-compose.yamlのcommandで下記のようにすると、うまくいかない
    ```
    ...
    command: locust -f locustfile.py --headless -u 1000 -r 100 --run-time 10s --csv=output
    ...
    ```
- 下記のようにフルパスを入れるとうまくいった
    ```
    ...
    command: /home/user/.local/bin/locust -f locustfile.py --headless -u 1000 -r 100 --run-time 10s --csv=output
    ...
    ```

### その他メモ
- docker-compose.yamlではコンテナ間のみの通信なら、exposeでok。portsとするとコンテナの外にポートが開いてしまう。

## お勉強パート

### 背景
いつも簡単なPoC用web appをflaskとvueで作っている。  
バックエンドはflaskのdev serverを使っているが、本当はよくないらしい。  
gunicornやnginxを通すとよいとよく聞くが、何がなんだかわからないので、調べる+使ってみる。  

### gunicornとは何か？
- Gunicorn（Green Unicorn）はPythonのWebアプリケーションサーバー
- WSGI（Web Server Gateway Interface）準拠のWebアプリケーションフレームワークと連携して動作
- WSGIとは？
    - WebサーバとWebアプリケーション間の汎用的なインターフェースを定義する
    - WSGIを利用することで、WebサーバとWebアプリケーションの実装を切り離すことができ、WebサーバとWebアプリケーションフレームワークの組み合わせを柔軟に選択可能
        - flaskはWebアプリケーションフレームワーク
        - nginxはwebサーバ
        - WSGIはnginxとflaskをつないでくれる
- 複数のプロセスを同時に実行し、複数のリクエストを同時に処理可能
    - Webアプリケーションのパフォーマンスが向上し、ユーザーに迅速かつ効率的なレスポンスを提供することが可能

### nginxとは何か？
- Webサーバーソフトの1つ
- webサーバとは？
    - Webサーバーとは、ユーザーからのリクエストを受けて処理を実行し、ユーザーにレスポンスを返すためのコンピューター
- 特徴は「オープンソース」「高性能な処理」「幅広い機能」
- リバースプロキシやロードバランサとしても使える
    - リバースプロキシとは？
        - (リバースプロキシの前に)プロキシ(フォワードプロキシ)とは？
            - ネットワーク内のpcの代理でwebサーバにリクエストを送ってくれる
            - メリット
                - キャッシュ：再度アクセス時に高速にアクセス可能
                - ユーザ認証：ネットワーク内の特定のpcのみwebにアクセスできる制限をかけられる
                - フィルタリング：見てはいけないサイトを禁止できる
                - ウィルス対策：受信コンテンツのウィルスチェックができる
                - 匿名性の確保：ネットワーク外のwebサーバにはプロキシサーバがアクセスするので、ネットワーク内のIPアドレスなどを隠せる
        - リバースプロキシとは？
            - ネットワーク外からネットワーク内へのアクセスを中継する
            - メリット
                - リクエストに応じたサーバ選択：外から見たら一つだけど、中で処理するサーバを分けられる
                - 負荷分散：同じ処理を行う複数のサーバを置いておけば、大量アクセスを分散できる
                - キャッシュ：同じ情報を保存しておいて、高速に返せる
                - SSL高速化：内部のwebサーバで複合化しなくてよくなり、リバースプロキシで高速に行える
                - セキュリティ向上：ネットワーク外から内部のサーバのIPなどを隠せる
    - ロードバランサとは？
        - いったんサーバーへのアクセスを集約し、リソースに余裕があるサーバーを接続先として選択する
        - 事前に決めた順序でリクエストを各サーバーに振り分ける「静的分散」、サーバーの状態をリアルタイムに測定して、リクエストをサーバーに振り分ける「動的分散」の2つがある

## 参考にさせていただいたサイト様
- [Gunicornってなに？](https://asameshicode.com/what-is-gunicorn/#google_vignette)
- [WSGIの概要](https://gihyo.jp/dev/feature/01/wsgi/0001)
- [NGINX(エンジンエックス)とは？その特徴やメリットについて徹底解説！！](https://cn.teldevice.co.jp/column/38275/)
- [リバースプロキシとプロキシの違いとは？それぞれのサーバーの仕組みは？](https://eset-info.canon-its.jp/malware_info/special/detail/201021.html)
- [ロードバランサー（Load Balancer）とは](https://www.ntt.com/bizon/glossary/j-r/load-balancer.html)
- [APIの性能テストにLocustを使ってみた](https://note.shiftinc.jp/n/n77be58376523)
- [【Docker × Flask】Locustでflask製のREST APIに負荷をかけてみる](https://scrawledtechblog.com/docker-flask-locust/)
