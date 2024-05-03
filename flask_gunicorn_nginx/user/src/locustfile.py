from locust import HttpUser, TaskSet, task, between

# タスクセットクラス
class UserBehavior(TaskSet):

    @task(5)
    def get_users(self):
        self.client.get("/")

    @task(4)
    def get_users_urlparam(self):
        self.client.get("/", params={"age": 30})

    @task(3)
    def post_user(self):
        self.client.post("/", json={"user_id": "5", "name": "test", "age": 30})

    @task(2)
    def put_user(self):
        self.client.put("/1", json={"name": "updated", "age": 22})

    @task(1)
    def delete_user(self):
        self.client.delete("/3")

# ユーザークラス
class WebsiteUser(HttpUser):
    # hostを指定（コマンドラインから実行時に使用）
    host = "http://flask:5901"

    tasks = [UserBehavior]

    # 5秒から15秒の間隔を置いて実行
    wait_time = between(5, 15)