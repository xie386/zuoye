import json
import random
import itertools

# 1.
with open("role_json.json", "r", encoding="utf-8") as f:
    player = json.load(f)
legal_add_list = [x for x in range(0, 11)]


def add_attr(power, add_num):
    if add_num in legal_add_list:
        return power + add_num
    else:
        print("加点大于10或者小于0,非法")
        return power


#  数值展示
def show(player):
    return f"力量: {player["power"]}, 生命: {player["HP"]}, 敏捷: {player["agile"]}"


def buff_get():
    buffs = ["力量+20", "迅捷+20", "生命+30"]
    for buff in buffs:
        yield buff


buff_cycle = itertools.cycle(buff_get())


# 2.暴击
def maybe_square(func):
    def wrapper(*args, **kwargs):
        res = func(*args, **kwargs)  # 基础伤害
        if random.random() < 0.4:  # 40% 暴击
            buff = next(buff_cycle)
            print(f"触发暴击！获得 Buff：{buff}")
            if buff == "力量5":
                res += 20
                print("力量额外 +5")
            elif buff == "迅捷5":
                res += 20
                print("迅捷额外 +5")
            elif buff == "生命恢复3":
                player["HP"] += 30
                print(f"  生命恢复 3 点，当前 HP：{player['HP']}")
            # 暴击：伤害平方
            res = res ** 2
            print(f"  暴击后伤害：{res}")
            return res
        else:
            return res

    return wrapper


@maybe_square
def _pia_(p): return p


use_pa = lambda p, a: 0.5 * p + 0.5 * a


def main():
    print(f"玩家当前属性{player}")
    while True:
        print("1. 增加力量")
        print("2. 增加生命")
        print("3. 增加敏捷")
        print("4. 查看输出伤害")
        print("5. 对战")
        print("6. 恢复最初状态")
        print("0. 退出加点并显示最终结果")
        choice = input("请选择操作")
        if choice == '0':
            print("加点结束,你的最终属性是", show(player))
            break
        elif choice == '1':
            try:
                add_num = int(input("请输入要增加的数值"))
                player["power"] = add_attr(player["power"], add_num)
                print("完成加点,当前属性:", show(player))
            except Exception as e:
                print(f"输入数据不合法,加点失败返回菜单:{e}")
        elif choice == '2':
            try:
                add_num = int(input("请输入要增加的数值"))
                player["HP"] += add_num
                print("完成加点,当前属性:", show(player))
            except Exception as e:
                print(f"输入数据不合法,加点失败返回菜单:{e}")
        elif choice == '3':
            try:
                add_num = int(input("请输入要增加的数值"))
                player["agile"] = add_attr(player["agile"], add_num)
                print("完成加点,当前属性:", show(player))
            except Exception as e:
                print(f"输入数据不合法,加点失败返回菜单:{e}")
        elif choice == '4':
            print("输出伤害:", _pia_(use_pa(player["power"], player["agile"])))
            gen = buff_get()
            print("触发buff:", next(gen))
        elif choice == '5':
            # 创建怪物
            HP_temp = player["HP"]
            monster = {"power": 10, "HP": 1000, "agile": 10}
            round_num = 1
            print("\n=== 战斗开始 ===")
            print(f"怪物属性：力量 {monster['power']}, 生命 {monster['HP']}, 敏捷 {monster['agile']}")
            print(f"你的属性：{show(player)}\n")

            while True:
                print(f"----- 第 {round_num} 回合 -----")
                # 玩家攻击
                player_damage = _pia_(use_pa(player["power"], player["agile"]))
                monster["HP"] -= player_damage
                print(f"你对怪物造成 {player_damage} 点伤害，怪物剩余 HP：{monster['HP']}")
                if monster["HP"] <= 0:
                    print("你击败了怪物！胜利！")
                    break

                # 怪物攻击（不触发暴击）
                monster_damage = use_pa(monster["power"], monster["agile"])
                player["HP"] -= monster_damage
                print(f"怪物对你造成 {monster_damage} 点伤害，你剩余 HP：{player['HP']}")
                if player["HP"] <= 0:
                    print("你被怪物击败了…… 失败！")
                    break

                # 怪物属性每回合增加10
                monster["power"] += 10
                monster["agile"] += 10
                print(f"怪物力量提升至 {monster['power']}，敏捷提升至 {monster['agile']}")
                round_num += 1
                input("按 Enter 继续下一回合...")
            player["HP"] = HP_temp
            print("战斗结束,返回菜单")

        elif choice == '6':
            player["power"] = 10
            player["HP"] = 100
            player["agile"] = 10
            print("已恢复初始状态")
        else:
            print("无效输入")
            continue

    with open("role_json.json", "w", encoding="utf-8") as f:
        json.dump(player, f, ensure_ascii=False)


if __name__ == "__main__":
    main()