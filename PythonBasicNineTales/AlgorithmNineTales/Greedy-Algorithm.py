#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2019/9/21 10:22 
# @Author : Nine-Tales
# @Desc: 贪心算法各种示例;

import sys
import os

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)

"""
# 找零钱问题:
# 假设只有 1 分、 2 分、五分、 1 角、二角、 五角、 1元的硬币。
# 在超市结账 时，如果 需要找零钱， 收银员希望将最少的硬币数找给顾客。
# 那么，给定 需要找的零钱数目，如何求得最少的硬币数呢？
def main():
    # 存储每种硬币面值;
    d = [0.01, 0.02, 0.05, 0.1, 0.2, 0.5, 1.0]
    # 存储每种硬币的数量;
    d_num = []
    s = 0
    # 拥有的零钱总和;
    temp = input("请输入每种零钱的数量:")
    d_num0 = temp.split(" ")

    for i in range(0, len(d_num0)):
        d_num.append(int(d_num0[i]))
        # 计算出收银员拥有多少钱;
        s += d[i] * d_num[i]

    sum = float(input("请输入需要找的零钱:"))

    if sum > s:
        # 当输入的总金额比收银员的总金额多时, 无法进行找零;
        print("数据有误")
        return 0
    s = s - sum

    # 要想用的钱币数量最少, 那么需要利用所有面值大的钱币, 因此从数组
    # 的面值大的元素开始遍历;
    i = 6
    while i >= 0:
        if sum >= d[i]:
            n = int(sum/ d[i])
            if n >= d_num[i]:
                # 更新n
                n = d_num[i]
            # 贪心算法的关键步骤, 令sum动态的改变;
            sum -= n * d[i]
            print("用了%d个%f元硬币" %(n, d[i]))
        i -= 1
"""

"""
# 求最大子数组之和的问题: 给定一个整数数组(数组元素有负有正),
# 求其连续子数组之和的最大值;
def main():
    s = [12, -4, 32, -36, 12, 6, -6]
    print("定义的数组为:", s)
    s_max, s_sum = 0, 0
    for i in range(len(s)):
        s_sum += s[i]
        if s_sum >= s_max:
            # 不断更新迭代s_max的值, 尽可能的令其最大;
            s_max = s_sum
        elif s_sum < 0:
            s_sum = 0
    print("最大子数组和为:", s_max)
"""

"""
#一辆汽车加满油后可行驶n公里。旅途中有若干个加油站。
# 设计一个有效算法，指出应在哪些加油站停靠加油，使沿途加油次数最少。
# 对于给定的n(n <= 5000)和k(k <= 1000)个加油站位置，编程计算最少加油次数。
# 设汽车加满油后可行驶N公里, 且旅途中有k个加油站
def greedy():
    n = 100
    k = 5
    d = [50, 80, 39, 60, 40, 32]
    # 表示加油站之间的距离
    num = 0
    # 表示加油次数
    for i in range(k):
        if d[i] > n:
            print("no solution, 无法解决")
            return

    i, s = 0, 0
    # 利用s进行迭代
    while i <= k:
        s += d[i]
        if s >= n:
            # 当局部和大于n时则局部和更新为当前距离;
            s = d[i]
            # 贪心意在令每一次加满油之后跑尽可能多的距离
            num += 1
        i += 1
    print(num)
"""


# 假设你办了个广播节目，要让全美50个州的听众都收听得到，为此，
# 你需要决定在哪些广播台播出，出于预算，你要力图在尽可能少的
# 广播台播出，现在广播台名单和其覆盖位置如下：
# {'KONE': ID,NV,UT}{'KTWO': WA,ID,MT},{KTHREE : OR,NV,CA}
# {KFOUR : NV,UT},{KFIVE : CA, AZ}

# 要覆盖的州
def main():
    states_needed = set(["mt", "wa", "or", "id", "nv", "ut", "ca", "az"])

    # 广播台清单
    stations = dict()
    stations['KONE'] = set(['id', 'nv', 'ut'])
    stations['KTWO'] = set(['wa', 'id', 'mt'])
    stations['KTHREE'] = set(['or', 'nv', 'ca'])
    stations['KFOUR'] = set(['nv', 'ut'])
    stations['KFIVE'] = set(['ca', 'az'])

    # 最终使用的广播台
    final_stations = set()

    while states_needed:  # 当还有需要的州未覆盖的时候循环
        best_station = None  # 覆盖了最多未覆盖的州的广播台
        states_covered = set()  # 已经覆盖了的州的集合
        # 遍历所有广播台，找出最佳广播台并且将他的覆盖州加入已覆盖的州的集合
        for station, states_for_station in stations.items():
            # 计算需要覆盖的州和每个广播台覆盖的州的交集
            covered = states_needed & states_for_station
            # 如果交集的州数量比已经覆盖的州的数量多
            if len(covered) > len(states_covered):
                best_station = station  # 最佳广播台更新为这个广播台
                states_covered = covered  # 已覆盖的州更新为交集
        states_needed -= states_covered  # 更新为覆盖的州
        final_stations.add(best_station)  # 更新最终结果

    print(final_stations)


if __name__ == '__main__':
    main()
    # greedy()