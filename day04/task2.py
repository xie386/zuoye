import asyncio
from datetime import datetime
import threading
async def seek(name):
    print(f"Seek {name}")
    return name
#为什么添加了async前缀的函数想要执行必须加asyncio.run()函数:
# 因为asyncio.run()函数可以将异步函数转换为同步函数,并执行它
#直接执行报错原因:
# 1.异步函数的执行是异步的,不能直接在同步环境中执行
# 2.异步函数的执行需要等待,而直接执行会阻塞主线程
# 3.异步函数的执行需要等待,而直接执行会阻塞主线程
# 4.异步函数的执行需要等待,而直接执行会阻塞主线程
start1=datetime.now()
for i in range(100):
    asyncio.run(seek(i))
use1=datetime.now()-start1
print("串行耗时:",use1)


def run_seek(i):
    asyncio.run(seek(i))

start2=datetime.now()
threads=[threading.Thread(target=run_seek, args=(i,)) for i in range(100)]
for thread in threads:
    thread.start()
for thread in threads:
    thread.join()
use2=datetime.now()-start2
print("多线程耗时:",use2)


async def main():
    await asyncio.gather(*[seek(i) for i in range(100)])

start3=datetime.now()
asyncio.run(main())
use3=datetime.now()-start3
print("异步耗时:",use3)

