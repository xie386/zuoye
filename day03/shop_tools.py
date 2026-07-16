# shop_tools.py - 通用工具模块
# 包含：数字校验、价格计算、文件读写、线程锁库存管理等功能

import threading


def check_positive(num: float) -> bool:
    """
    校验数字是否大于0
    :param num: 价格、库存、数量等数字
    :return: 合法大于数返回True，否则返回False
    :raises TypeError: 输入非数字类型时抛出异常
    """
    if not isinstance(num, (int, float)):
        raise TypeError("参数必须传入数字（int/float）")
    return num > 0


def calc_total_price(price: float, num: int) -> float:
    """
    计算饮品总价
    :param price: 单品单价
    :param num: 购买数量
    :return: 应付金额，保留两位小数
    :raises ValueError: 价格或数量小于等于0时抛出异常
    """
    if not check_positive(price) or not check_positive(num):
        raise ValueError("价格、购买数量必须大于0")
    return round(price * num, 2)


# ==================== 文件操作工具 ====================

def save_order_with_with(order_info: str):
    """
    使用with语法保存订单到order.txt文件
    with上下文管理器会自动关闭文件，杜绝资源泄漏
    :param order_info: 订单信息字符串
    """
    with open("order.txt", "a", encoding="utf-8") as f:
        f.write(order_info + "\n")
    print("订单保存完成，文件已自动关闭")


def read_all_orders():
    """
    使用with读取全部历史订单
    :return: 订单文件全部内容字符串
    """
    with open("order.txt", "r", encoding="utf-8") as f:
        content = f.read()
    return content


def clear_order_file():
    """使用with w模式清空订单文件"""
    with open("order.txt", "w", encoding="utf-8") as f:
        pass
    print("订单文件已清空")


# ==================== 列表推导式工具 ====================

def get_cheap_drinks(drink_dict: dict, limit: float) -> list:
    """
    使用列表推导式筛选低于指定价格的饮品
    :param drink_dict: 饮品名称-价格字典
    :param limit: 价格上限
    :return: 低于限价的饮品名称列表
    """
    if not isinstance(drink_dict, dict):
        raise TypeError("参数必须是饮品名称-价格字典")
    cheap_data = {name: p for name, p in drink_dict.items() if p < limit}
    return list(cheap_data.keys())


# ==================== 生成器工具 ====================

def order_record_generator(order_list: list):
    """
    订单生成器：按需生成订单记录，节省内存
    :param order_list: 订单列表，每项为(饮品名, 数量, 总价)元组
    :yield: 格式化订单记录字符串
    """
    for order in order_list:
        yield f"饮品：{order[0]}，数量：{order[1]}，总价：{order[2]}"


# ==================== 多线程库存管理 ====================

# 全局共享库存字典（所有线程共用，必须提前定义）
global_stock = {"珍珠奶茶": 50, "杨枝甘露": 30, "芝士葡萄": 40, "美式咖啡": 60}
# 创建互斥锁对象，保证多线程安全
stock_lock = threading.Lock()


def sell_drink_thread_safe(drink_name: str, sell_num: int):
    """
    使用with线程锁安全扣减库存，防止多线程超卖
    with lock 会自动执行 acquire() 和 release()，避免死锁
    :param drink_name: 饮品名称
    :param sell_num: 售卖数量
    :return: 售卖成功返回True，失败返回False
    """
    with stock_lock:
        if global_stock[drink_name] < sell_num:
            print(f"{drink_name}库存不足，售卖失败")
            return False
        global_stock[drink_name] -= sell_num
        info = f"{drink_name} 售出{sell_num}杯，剩余库存{global_stock[drink_name]}"
        save_order_with_with(info)
        print(info)
        return True


def restock_drink(key: str, num: int):
    """
    进货函数：增加全局库存中指定商品的存货量
    :param key: 商品在global_stock中的键名
    :param num: 进货增加量，必须为正整数
    :raises KeyError: 商品不存在于库存中
    :raises ValueError: 增加量不是正整数
    """
    if key not in global_stock:
        raise KeyError(f"商品'{key}'不存在于库存中")
    if not isinstance(num, int) or num <= 0:
        raise ValueError("进货增加量必须为正整数")
    with stock_lock:
        global_stock[key] += num
        print(f"{key} 进货{num}件，当前库存{global_stock[key]}")


def multi_thread_sell():
    """多线程并发售卖测试函数"""
    t1 = threading.Thread(target=sell_drink_thread_safe, args=("珍珠奶茶", 5))
    t2 = threading.Thread(target=sell_drink_thread_safe, args=("珍珠奶茶", 3))
    t1.start()
    t2.start()
    t1.join()
    t2.join()


# ==================== 模块测试代码 ====================
# 以下代码仅在直接运行 shop_tools.py 时执行（python shop_tools.py）
# 被其他文件导入时不会执行
if __name__ == "__main__":
    print("===== shop_tools.py 模块自测 =====\n")

    # 1. 测试 check_positive 校验函数
    print("--- 测试1：数字校验 ---")
    print(f"check_positive(5) = {check_positive(5)}")  # 应返回 True
    print(f"check_positive(0) = {check_positive(0)}")  # 应返回 False
    print(f"check_positive(-3) = {check_positive(-3)}")  # 应返回 False
    try:
        check_positive("abc")  # 应抛 TypeError
    except TypeError as e:
        print(f"check_positive('abc') 抛出异常：{e}")

    # 2. 测试 calc_total_price 价格计算
    print("\n--- 测试2：价格计算 ---")
    print(f"calc_total_price(12, 3) = {calc_total_price(12, 3)}元")  # 36.0
    print(f"calc_total_price(15.5, 2) = {calc_total_price(15.5, 2)}元")  # 31.0
    try:
        calc_total_price(-10, 2)  # 应抛 ValueError
    except ValueError as e:
        print(f"calc_total_price(-10, 2) 抛出异常：{e}")

    # 3. 测试文件操作（写入+读取+清空）
    print("\n--- 测试3：文件操作 ---")
    clear_order_file()  # 先清空
    save_order_with_with("测试订单1")
    save_order_with_with("测试订单2")
    print("读取订单内容：")
    print(read_all_orders())

    # 4. 测试列表推导式筛选
    print("--- 测试4：低价饮品筛选 ---")
    menu = {"珍珠奶茶": 12, "杨枝甘露": 16, "芝士葡萄": 15, "美式咖啡": 10}
    cheap = get_cheap_drinks(menu, 14)
    print(f"低于14元的饮品：{cheap}")  # ['珍珠奶茶', '美式咖啡']

    # 5. 测试生成器
    print("\n--- 测试5：订单生成器 ---")
    orders = [("珍珠奶茶", 2, 24), ("杨枝甘露", 1, 16)]
    for record in order_record_generator(orders):
        print(record)

    # 6. 测试线程锁
    print("\n--- 测试6：多线程安全售卖 ---")
    print(f"售卖前珍珠奶茶库存：{global_stock['珍珠奶茶']}")
    multi_thread_sell()
    print(f"售卖后珍珠奶茶库存：{global_stock['珍珠奶茶']}")

    print("\n===== 全部测试完成 =====")
