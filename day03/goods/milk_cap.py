import sys
import os
# 添加项目根目录到路径，使直接运行此文件时能找到 shop_tools
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from goods.base_drink import BaseDrink

# goods/milk_cap.py - 奶盖茶类
class MilkCapTea(BaseDrink):
    def __init__(self, name: str, price: float):
        super().__init__(name, price)
        self.type = "奶盖茶"
# 实例属性，__milk_cap_cost 
        self.__milk_cap_cost = price*self.shop_discount
# 继承BaseDrink，实现奶盖茶专属优惠：购买2杯及以上立减3元
    def get_final_price(self, buy_num: int) -> float:
        """计算奶盖的最终价格"""
        origin = self.price*self.shop_discount * buy_num
        if buy_num < 2:
            final = origin
        else:
            final = origin - 3
        print("=====")
        return round(final, 2)

    def get_milk_cap_cost(self) -> float:
        """获取奶盖的单杯价格"""
        return self.__milk_cap_cost 
    def print_ticket(self, buy_num: int):
        """
        打印订单票
        :param buy_num: 购买数量
        :param final_price: 最终价格
        """
        if buy_num >= 2:
            total = self.get_final_price(buy_num)
            print(f"本店奶盖茶专属优惠：购买2杯及以上立减3元\n饮品：{self.name},数量：{buy_num}, 总价：{total}")
        else:
            total = self.get_final_price(buy_num)
            print(f"饮品：{self.name},数量：{buy_num}, 总价：{total}")
#测试代码
if __name__ == "__main__":
    milk_cap = MilkCapTea("奶盖四季春", 15)
    print(milk_cap.get_milk_cap_cost())
    milk_cap.print_ticket(1)
    milk_cap.print_ticket(2)
    milk_cap.print_ticket(3)
    milk_cap.set_shop_discount(0.8)
    print(milk_cap.get_milk_cap_cost())
    milk_cap.print_ticket(1)
    milk_cap.print_ticket(2)
    milk_cap.print_ticket(3)