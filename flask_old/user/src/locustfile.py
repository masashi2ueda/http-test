from locust import HttpUser, task

class HelloWorldUser(HttpUser):
    @task
    def hello_world(self):
        self.client.get("")

# from multiprocessing import Process
# import os
# import time

# # flaskが起きるまで待つ
# time.sleep(3)

# def print_each(process_name):
#     start = time.time()
#     for i in range(5):
#         print(process_name, i, os.system('curl flask:5901/sleep1sec'))
#         print(process_name, f"{(time.time() - start):.2f}秒経過")


# # プロセスを作成します
# p1 = Process(target=print_each, args=("PA",))
# p2 = Process(target=print_each, args=("PB",))

# # プロセスを開始します
# p1.start()
# p2.start()

# # 各プロセスの終了を待ちます
# p1.join()
# p2.join()

# print("Done!")