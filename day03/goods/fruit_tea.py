import sys
import os
# 添加项目根目录到路径，使直接运行此文件时能找到 shop_tools
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from goods.base_drink import BaseDrink
# goods/fruit_tea.py - 果茶子类
# 继承BaseDrink，实现果茶专属优惠：全场折扣基础上额外95折

#重写打印小票方法：显示果茶专属优惠信息


class FruitTea(BaseDrink):
    def __init__(self, name: str, price: float):
        super().__init__(name, price)
        self.type = "果茶"

    def get_final_price(self, buy_num: int) -> float:
        """计算果茶的最终价格"""
        origin = self.price * buy_num
        final = origin * self.shop_discount * 0.95
        print("=====")
        return round(final, 2)

    def print_ticket(self, buy_num: int):
        """
        打印订单票
        :param buy_num: 购买数量
        :param final_price: 最终价格
        """
        total = self.get_final_price(buy_num)
        print(f"本店果茶专属优惠：全场折扣基础上额外95折\n饮品：{self.name},数量：{buy_num}, 总价：{total}")
#测试代码
if __name__ == "__main__":
    fruit_tea = FruitTea("棒打今日橙", 10)
    fruit_tea.print_ticket(2)
    fruit_tea.set_shop_discount(0.8)
    fruit_tea.print_ticket(2)
