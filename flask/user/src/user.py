import os
import time

# flaskが起きるまで待つ
time.sleep(3)

start = time.time()
for i in range(5):
    print(i, os.system('curl flask:5901/sleep1sec'))
    print(f"{(time.time() - start):.2f}秒経過")