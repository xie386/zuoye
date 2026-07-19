

---

### Python代码基本功面试题

#### 第1题：变量与数据类型
**题目：**
请简要说明Python中 `list` 和 `tuple` 的区别，并分别写出一个它们适用的典型场景。

**答案要点：**
1.  `list`（列表）是可变的数据类型，创建后可以对其元素进行增、删、改操作；`tuple`（元组）是不可变的数据类型，创建后其内容不可更改。
2.  **适用场景**：
    *   **`list`**：适用于需要动态变化的元素集合，例如存储一个角色的所有Buff列表，可以随时添加或移除Buff。
    *   **`tuple`**：适用于固定不变的数据集合，例如函数返回多个值时，本质上是返回一个元组；或者用于字典的键（因为其可哈希）。

---

#### 第2题：函数参数与返回值
**题目：**
阅读以下代码，分析其输出结果，并解释 `*args` 和 `**kwargs` 在函数定义中的作用。

```python
def process_data(base, *args, **kwargs):
    print(f"基础值: {base}")
    print(f"额外数值: {args}")
    print(f"额外属性: {kwargs}")
    return base + sum(args)

result = process_data(10, 1, 2, 3, power=5, agile=3)
print(f"最终结果: {result}")
```

**答案要点：**
1.  **输出结果**：
    ```
    基础值: 10
    额外数值: (1, 2, 3)
    额外属性: {'power': 5, 'agile': 3}
    最终结果: 16
    ```
2.  **`*args`**：用于接收任意数量的**位置参数**，并将它们打包成一个**元组**。在示例中，`1, 2, 3` 被 `args` 接收。
3.  **`**kwargs`**：用于接收任意数量的**关键字参数**，并将它们打包成一个**字典**。在示例中，`power=5, agile=3` 被 `kwargs` 接收。

---

#### 第3题：列表推导式
**题目：**
请使用**一行列表推导式**，生成一个包含1到20之间所有偶数的平方的列表。请写出代码。

**答案：**
```python
even_squares = [x**2 for x in range(1, 21) if x % 2 == 0]
print(even_squares)
# 输出: [4, 16, 36, 64, 100, 144, 196, 256, 324, 400]
```

---

#### 第4题：类与继承
**题目：**
现有以下代码，请指出其中的错误并修正，使得 `Dog` 类的实例能正确打印出其 `name` 属性。

```python
class Animal:
    def __init__(self, name):
        self.name = name

class Dog(Animal):
    def __init__(self, breed):
        self.breed = breed

my_dog = Dog("Buddy", "Golden Retriever")
print(my_dog.name)
```

**答案要点：**
1.  **错误**：`Dog` 类重写了 `__init__` 方法，但没有调用父类 `Animal` 的 `__init__` 方法，导致 `self.name` 属性从未被初始化。此外，`Dog("Buddy", "Golden Retriever")` 传入了两个参数，但定义只接收一个。
2.  **修正**：
    ```python
    class Animal:
        def __init__(self, name):
            self.name = name
    
    class Dog(Animal):
        def __init__(self, name, breed):
            super().__init__(name)  # 调用父类构造方法
            self.breed = breed
    
    my_dog = Dog("Buddy", "Golden Retriever")
    print(my_dog.name)  # 输出: Buddy
    ```

---

#### 第5题：多线程与线程安全
**题目：**
在多线程环境中，为什么修改全局变量时通常需要加锁？请简述如果不加锁可能导致的后果。

**答案要点：**
1.  **原因**：多线程并发执行时，多个线程可能同时读取和修改同一个全局变量，导致数据竞争（Race Condition）。由于线程调度是随机的，操作的执行顺序无法保证，最终结果会依赖于线程执行的先后顺序，产生不可预知的错误。
2.  **后果**：例如，一个计数器 `count` 初始为0，两个线程同时执行 `count += 1`。这个操作在底层并非原子操作（读-加-写），可能出现两个线程都读取到 `0`，然后各自加1并写回，最终 `count` 为1而不是2，导致数据不一致。

---

#### 第6题：生成器 (Generator)
**题目：**
请解释 `yield` 关键字的作用，并说明生成器相比于普通列表的优势。

**答案要点：**
1.  **`yield` 的作用**：`yield` 用于定义一个生成器函数。当函数执行到 `yield` 时，会返回一个值并暂停函数的执行，保留当前所有的状态。当再次调用生成器的 `next()` 方法时，函数会从暂停处继续执行。
2.  **优势**：**节省内存**。普通列表会一次性将所有元素加载到内存中；而生成器是惰性求值的（Lazy Evaluation），它一次只生成一个元素，对于需要处理大量数据（例如读取超大日志文件）的场景，可以极大降低内存占用。

---

#### 第7题：装饰器 (Decorator)
**题目：**
请编写一个名为 `timer` 的装饰器，用于测量一个函数执行所花费的时间，并打印出耗时。

**答案：**
```python
import time

def timer(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"函数 {func.__name__} 执行耗时: {end - start:.4f}秒")
        return result
    return wrapper

@timer
def slow_function():
    time.sleep(1)
    return "Done"

slow_function()
# 输出类似: 函数 slow_function 执行耗时: 1.0002秒
```

---

#### 第8题：文件操作与上下文管理器
**题目：**
`with` 语句在文件操作中有什么好处？请将以下传统代码改写为使用 `with` 语句的版本。

```python
f = open("data.txt", "w")
f.write("Hello, World!")
f.close()
```

**答案要点：**
1.  **好处**：`with` 语句是一个上下文管理器，它能确保在代码块执行完毕后，文件会被自动正确地关闭，即使代码块内部发生了异常。这有效防止了资源泄露，使代码更简洁、安全。
2.  **改写**：
    ```python
    with open("data.txt", "w") as f:
        f.write("Hello, World!")
    ```

---

#### 第9题：异常处理
**题目：**
请编写一个包含 `try...except...finally` 的代码块，用于处理可能发生的 `ZeroDivisionError`，并在 `finally` 块中打印 "计算结束"。

**答案：**
```python
try:
    num = 10 / 0
except ZeroDivisionError:
    print("错误：除数不能为0！")
finally:
    print("计算结束")
```

---

#### 第10题：Git与团队协作
**题目：**
请简述在企业多人协作开发中，为什么禁止直接在 `main` 分支上进行开发并推送？标准的协作流程是什么？

**答案要点：**
1.  **原因**：`main`（或 `master`）分支是项目的稳定、可发布版本。如果所有人都直接在 `main` 上开发并推送，会导致代码混乱、冲突频繁，极不稳定，甚至可能包含未测试的代码，无法作为可靠的发布基准。
2.  **标准流程**：
    1.  开发前，先从远程 `main` 分支拉取最新代码 `git pull origin main`。
    2.  基于 `main` 分支，创建一个新的功能分支 `git checkout -b feature/your-feature-name`。
    3.  在自己的功能分支上进行开发和本地提交。
    4.  开发完成后，再次拉取最新的 `main` 分支，并在本地解决冲突 `git pull origin main`。
    5.  将功能分支推送到远程仓库 `git push origin feature/your-feature-name`。
    6.  在Git平台（如GitHub/GitLab）上发起一个Pull Request (PR) 或 Merge Request (MR)，请求将你的功能分支合并到 `main` 分支。
    7.  团队其他成员或管理员进行代码审查（Code Review），通过后合并到 `main` 分支。