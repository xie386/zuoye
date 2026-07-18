import asyncio
import time
list1 = []
async def greet(name, delay):
    await asyncio.sleep(delay)
    print(f"Hello, {name}!")
    return name
async def main():
    global list1
    start_time = time.time()
    list1 = await asyncio.gather(
        greet("Alice", 1),
        greet("Bob", 2),
        greet("Carol", 3),
    )
    print("All done!")
    print(f"耗时{time.time() - start_time}秒")
asyncio.run(main())
print(list1)


