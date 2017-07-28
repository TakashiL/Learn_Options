from math import exp
import os
import matplotlib.pyplot as plt
from option_trade_framework import Account
import doupo_trade


class Combo:
    def __init__(self, futuredue, futureprice, settleprice, putoptionprice, calloptionprice, amount):
        self.futuredue = futuredue
        self.futureprice = futureprice
        self.settleprice = settleprice
        self.putoption = 'm' + futuredue + '-P-' + str(settleprice)
        self.putoptionprice = putoptionprice
        self.calloption = 'm' + futuredue + '-C-' + str(settleprice)
        self.calloptionname = calloptionprice
        self.amount = amount


def doupo_takeposition(account, date, combo):
    doupo_trade.buy_future(account, date, combo.futuredue, combo.amount)
    doupo_trade.buy_option(account, date, combo.putoption, combo.amount)
    doupo_trade.sell_option(account, date, combo.calloption, combo.amount)


def doupo_hedgeposition(account, date, combo):
    futurename = combo.futuredue + '-' + str(combo.futureprice)
    doupo_trade.hedge_future(account, date, futurename)
    doupo_trade.hedge_option(account, date, combo.putoption)
    doupo_trade.hedge_option(account, date, combo.calloption)

myaccount = Account(0, 10)
combos = []  # [Combo1, Combo2]
asset = []
days = []
daycount = 0
maxmargin = 0
tradecount = 0
tempasset = 0

# file
trade_record = open('trade_record.txt', 'w')

# parameter

dominant = '1709'
optiontradingday = 145
futuretradingday = 173
# datefiles = ['0609.txt', '0612.txt', '0613.txt']
datefiles = os.listdir("doupo_option_data")
tradingday = doupo_trade.gettradingdaydict()
r = 0.02

'''
first sign
if (C - P) > F*exp(-r*Tf) - K*exp(-r*To):
    buy a combo
    
second sign
if (C - P) < F*exp(-r*Tf) - K:
    sell a combo
'''
# strategy starts
for f in datefiles:
    date = f.split('.')[0]
    futureprice = doupo_trade.get_closing_price(date, dominant, 1)
    futuretime = 1.0 * (futuretradingday - tradingday[date]) / 252
    optiontime = 1.0 * (optiontradingday - tradingday[date]) / 252
    myaccount.printaccount(date)

    totalasset = myaccount.gettotalasset(date)
    asset.append(totalasset)
    days.append(daycount)
    daycount += 1

    if len(combos) == 0:  # no position, try to buy a combo
        maxdiff = 0
        maxK = 0
        maxput = 0
        maxcall = 0

        calloptions = doupo_trade.dominant_calloptions(date, dominant)
        for calloption in calloptions:
            K = int(calloption.split('-')[2])
            putoption = calloption.replace('C', 'P')
            calloptionprice = doupo_trade.get_closing_price(date, calloption, 0)
            putoptionprice = doupo_trade.get_closing_price(date, putoption, 0)

            middle = calloptionprice - putoptionprice
            upper = futureprice * exp(-r*futuretime) - K * exp(-r*optiontime)
            diff = middle - upper

            if diff > maxdiff:
                maxdiff = diff
                maxK = K
                maxput = putoptionprice
                maxcall = calloptionprice

        if maxdiff > 10:
            tmpcombo = Combo(dominant, futureprice, maxK, maxput, maxcall, 1)
            tempasset = myaccount.gettotalasset(date)
            doupo_takeposition(myaccount, date, tmpcombo)
            combos.append(tmpcombo)
            
            calloptionmargin1 = maxcall * 10 + futureprice - 0.5 * max(0, maxK-futureprice) * 10
            calloptionmargin2 = maxcall * 10 + 0.5 * futureprice
            calloptionmargin = max(calloptionmargin1, calloptionmargin2)
            margin = futureprice + calloptionmargin
            if margin > maxmargin:
                maxmargin = margin
            trade_record.write(date + ' buy a combo, margin: ' + str(maxmargin) + ', current asset: ' + str(tempasset) + '\n')

    else:  # own position, try to hedge position
        mycombo = combos[0]
        todaycallprice = doupo_trade.get_closing_price(date, mycombo.calloption, 0)
        todayputprice = doupo_trade.get_closing_price(date, mycombo.putoption, 0)
        todayK = mycombo.settleprice

        middle = todaycallprice - todayputprice
        upper = futureprice * exp(-r*futuretime) - todayK * exp(-r*optiontime)
        if middle - upper < 7:
            doupo_hedgeposition(myaccount, date, mycombo)
            combos.pop(0)
            profit_onetime = myaccount.gettotalasset(date) - tempasset

            tradecount += 1
            trade_record.write(date + ' hedge a combo, tradecount: ' + str(tradecount) + ', profit: ' + str(profit_onetime) + '\n')

print "---------------------------------"
print "max margin: " + str(maxmargin)
print "final profit: " + str(myaccount.gettotalasset('0726'))
print "total trade times: " + str(tradecount)

trade_record.close()

for i in range(len(asset)):
    asset[i] += maxmargin

# plot
plt.figure(figsize=(8,8))
plt.plot(days, asset, color='red', linewidth=2, marker='o')
plt.xlabel("days(d)")
plt.ylabel("asset")
plt.show()
