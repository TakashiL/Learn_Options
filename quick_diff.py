from math import exp
'''
if (C - P) > F*exp(-r*Tf) - K*exp(-r*To):
    buy a combo
'''

r = 0.02
# future = 228; option = 254  # 1801
future = 145; option = 173  # 1709


def calcu(callprice, putprice, futureprice, optionprice, date):
    futuretime = 1.0 * (future - date) / 252
    optiontime = 1.0 * (future - date) / 252
    middle = callprice - putprice
    upper = 1.0 * futureprice * exp(-r * futuretime) - 1.0 * optionprice * exp(-r * optiontime)

    print middle
    print upper
    print middle - upper

calcu(121.5, 58, 2840, 2800, 140)
