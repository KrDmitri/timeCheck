import numpy as np
from datetime import date
import time

start = time.time()

n = 1000
r = 0.005
vol = 0.2646

n0 = date.toordinal(date(2021, 9, 17))
n1 = date.toordinal(date(2022, 3, 14))
n2 = date.toordinal(date(2022, 9, 13))
n3 = date.toordinal(date(2023, 3, 14))
n4 = date.toordinal(date(2023, 9, 12))
n5 = date.toordinal(date(2024, 3, 12))
n6 = date.toordinal(date(2024, 9, 13))

check_day = np.array([n1 - n0, n2 - n0, n3 - n0, n4 - n0, n5 - n0, n6 - n0])
oneyear = 365
tot_date = n6 - n0
dt = 1 / oneyear
S = np.zeros([tot_date + 1, 1])
S[0] = 100.0
strike_price = np.array([0.95, 0.90, 0.80, 0.80, 0.80, 0.75]) * S[0]

repay_n = len(strike_price)
coupon_rate = np.array([0.021, 0.042, 0.063, 0.084, 0.105, 0.126])

payment = np.zeros([repay_n, 1])             # 각 평가일에 지불할 금액
facevalue = 10 ** 4
tot_payoff = np.zeros([repay_n, 1])          # 총 수익
payoff = np.zeros([repay_n, 1])              # 개별 수익
discount_payoff = np.zeros([repay_n, 1])     # 할인된 수익
kib = 0.55 * S[0]
dummy = 0.132                                # 추가 쿠폰 금리라는데 이 정보는 어디서 보는거지?

for j in range(repay_n):
    payment[j] = facevalue * (1 + coupon_rate[j])

for i in range(n):
    z = np.random.normal(0, 1, size=[tot_date, 1])
    for j in range(tot_date):
        S[j + 1] = S[j] * np.exp((r - 0.5 * vol ** 2) * dt + vol * np.sqrt(dt) * z[j])
    S_checkday = S[check_day]
    payoff = np.zeros([repay_n, 1])
    repay_event = 0
    for j in range(repay_n):
        if S_checkday[j] >= strike_price[j]:
            payoff[j] = payment[j]
            repay_event = 1
            break
    if repay_event == 0:
        if min(S) > kib:
            payoff[-1] = facevalue * (1 + dummy)
        else:
            payoff[-1] = facevalue * (S[-1] / S[0])
    tot_payoff += payoff

mean_payoff = tot_payoff / n

for j in range(repay_n):
    discount_payoff[j] = mean_payoff[j] * np.exp(-r * check_day[j] / oneyear)
price = np.sum(discount_payoff)
print(price)

end = time.time()

