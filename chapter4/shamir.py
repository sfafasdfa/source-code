import random
from math import ceil
from decimal import Decimal

FIELD_SIZE = 10 ** 2
MOD = 9999999987


def coeff(t, secret):
    """
    生成最高次为t - 1次的多项式，其中常数项是secret
    """
    # 保证第一项不为0
    coeff = [random.randrange(1, FIELD_SIZE)]
    # 后面t - 2系数项可为0
    if t > 3:
        coeff += [random.randrange(0, FIELD_SIZE) for _ in range(t - 2)]
    # 加入常数项
    coeff.append(secret)
    return coeff


def polynom(x, coefficients):
    """
    获取f(x)的值
    """
    point = 0
    # coeff从左到右是高次到低次的(使用enumerate表示指数)
    for coefficient_index, coefficient_value in enumerate(coefficients[::-1]):
        point += x ** coefficient_index * coefficient_value
    return point


def generate_shares(n, m, secret):
    """
    将秘密分成n份，只需要m份就可以复原（也就是阈值，函数的最高次数 + 1）
    """
    coefficient = coeff(m, secret)
    shares = []
    xs = random.sample(range(0, FIELD_SIZE), n)

    for i in range(1, n + 1):
        x = xs[i - 1]
        shares.append((x, polynom(x, coefficient)))

    return shares


def reconstruct_secret(shares):
    """
    利用拉格朗日插值法（已知m个秘密)还原并得到secret(f(0))
    """
    sums = 0

    for j, share_j in enumerate(shares):
        xj, yj = share_j
        prod = Decimal(1)

        for i, share_i in enumerate(shares):
            xi, _ = share_i
            if i != j:
                #print(Decimal(Decimal(xi) / (xi - xj)))
                prod *= Decimal(Decimal(xi) / (xi - xj))
        #print(yj)
        prod *= yj
        sums += Decimal(prod)
    print(sums)

    return int(round(Decimal(sums), 0))


# Driver code
if __name__ == '__main__':
    # (3,5) sharing scheme
    t, n = 50, 100
    secret = 1234
    print(f'Original Secret: {secret}')

    # Phase I: Generation of shares
    shares = generate_shares(n, t, secret)
    print(f'Shares: {", ".join(str(share) for share in shares)}')

    # Phase II: Secret Reconstruction
    # Picking t shares randomly for
    # reconstruction
    pool = random.sample(shares, t)
    print(f'Combining shares: {", ".join(str(share) for share in pool)}')
    print(f'Reconstructed secret: {reconstruct_secret(pool)}')
