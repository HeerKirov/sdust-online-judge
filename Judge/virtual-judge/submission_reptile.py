from functions import hdu
import time

# 根据数据库完成度不断对提交进行查询。为那些不能直接查询runid的oj提供查询服务

reptile_functions = [
    hdu.reptile_submit
]


def run(interval):
    while True:
        for delegate in reptile_functions:
            delegate()
        time.sleep(interval)

run(2)
