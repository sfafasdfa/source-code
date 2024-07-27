import random
import math


def moni(a, b):  # 用扩展的欧几里得算法计算模逆
    f = 0  # 判断a是否大于b的标志位
    if a < b:
        f = 1
        t = a
        a = b
        b = t
    x1, x2, x3 = 1, 0, a
    y1, y2, y3 = 0, 1, b
    while y3 != 0:
        q = x3 // y3
        t1 = x1 - q * y1
        t2 = x2 - q * y2
        t3 = x3 - q * y3
        x1, x2, x3 = y1, y2, y3
        y1, y2, y3 = t1, t2, t3
    if f != 1:
        return x1
    else:
        return x2


def ChineseRemainderTheorem(kj, dj):  # 中国剩余定理，参数为任选的t个或其他个数的子秘密
    l = len(kj) # 计算子秘密的个数
    M = 1
    for i in range(l):
        M *= dj[i]
    Mi = []
    for i in range(l):
        Mi.append(M // dj[i])
    Mini = []
    for i in range(l):
        Mini.append(moni(Mi[i], dj[i]))
    sum = 0
    for i in range(l):
        sum += kj[i] * Mi[i] * Mini[i]
    return sum % M

if __name__ == '__main__':
    t = int(input("请输入参数t："))
    n = int(input("请输入参数n："))
    with open("D:\secret2.txt") as file:
        data = file.readline()
    k = int(data)
    print("从文件中读取的秘密k的值为:")
    print(k)

    # 生成n位d值放入列表
    d = []
    temp = random.randint(pow(10, (math.floor(math.log(k, 10)) + 1) // t + 1),
                        pow(10, (math.floor(math.log(k, 10)) + 1) // (t - 1)))
    d.append(temp)
    while len(d) < n:
        temp = random.randint(pow(10, (math.floor(math.log(k, 10)) + 1) // t + 1),
                            pow(10, (math.floor(math.log(k, 10)) + 1) // (t - 1)))
        if len(d) == 1:
            if math.gcd(d[0], temp) == 1:
                d.append(temp)
        else:
            d.append(temp)
            flag = 1  # 检查各d值是否两两互素的标志
            for i in range(len(d) - 1):
                for j in range(i + 1, len(d)):
                    if math.gcd(d[i], d[j]) != 1:
                        flag = 0    # 不满足两两互素，将temp从列表中删去
                        d.pop()
                        break
                if flag == 0:
                    break

    print(n, "个d值分别为:", sep='')
    for i in range(n):
        print(d[i])
    N = 1
    M = 1
    for i in range(t):
        N = N * d[i]
    for i in range(n - t + 1, n):
        M = M * d[i]
    print("N值为：", N)
    print("M值为：", M)
    ki = []
    for i in range(n):
        ki.append(k % d[i])

    # 任选t组子秘密来恢复秘密k
    kn = random.sample(range(n), t)  # 从n位任选t位，把下标存入kn列表
    k1 = []
    d1 = []
    for i in range(t):
        k1.append(ki[kn[i]])
        d1.append(d[kn[i]])
    recoverk = ChineseRemainderTheorem(k1, d1)
    print("用t个子秘密恢复的秘密为:")
    print(recoverk)
    if recoverk == k:
        print("用t个子秘密恢复的秘密与原秘密相同，恢复正确！")
    else:
        print("用t个子秘密恢复的秘密与原秘密不同，恢复错误！")

    # 任选t-1组子秘密来恢复秘密
    kn2 = random.sample(range(n), t - 1)  # 从n位任选t-1位，把下标存入kn2列表
    k2 = []
    d2 = []
    for i in range(t - 1):
        k2.append(ki[kn2[i]])
        d2.append(d[kn2[i]])
    recoverk = ChineseRemainderTheorem(k2, d2)
    print("用t-1个子秘密恢复的秘密为:")
    print(recoverk)
    if recoverk == k:
        print("用t-1个子秘密恢复的秘密与原秘密相同，恢复正确！")
    else:
        print("用t-1个子秘密恢复的秘密与原秘密不同，恢复错误！")
