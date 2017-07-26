from __future__ import print_function
from collections import defaultdict
import doupo_trade


class Account:
    def __init__(self, available=0, units=10):
        # assume no margin and service fee
        self.available = available
        self.units = units
        self.futures = defaultdict(list)  # {due-price : [settlement price, amount]}
        self.options = defaultdict(list)  # {option_name : [settlement price, amount]}

    def addavailable(self, money):
        self.available += money

    def setunits(self, newunits):
        self.units = newunits

    def takenewfuture(self, due, price, amount):
        futurename = str(due) + '-' + str(price)
        if futurename not in self.futures:
            self.futures[futurename] = [price, amount]  # + means buy(long), - means sell(short)
        else:
            self.futures[futurename][1] += amount

    def hedgefuture(self, oldfuture, newprice):
        if oldfuture not in self.futures:
            raise Exception("oldfuture " + oldfuture + " not exist")

        # assume close this future at all
        [oldprice, oldamount] = self.futures[oldfuture]

        profit = (newprice - oldprice) * oldamount * self.units
        self.available += profit

        self.futures.pop(oldfuture)

    def takenewoption(self, optionname, price, amount):
        settlementprice = int(optionname.split('-')[2])
        if optionname not in self.options:
            self.options[optionname] = [settlementprice, amount]  # + means buy(long), - means sell(short)
        else:
            self.options[optionname][1] += amount

        premium = price * amount * self.units  # + means pay, - means get
        self.available -= premium

    def hedgeoption(self, optionname, newprice):
        if optionname not in self.options:
            raise Exception("optionname " + optionname + " not exist")

        # assume close this option at all
        oldamount = self.options[optionname][1]

        premium = newprice * oldamount * self.units
        self.available += premium

        self.options.pop(optionname)

    def printaccount(self):
        print("the available asset is: ", end='')
        print(self.available)
        print("the futures are: ", end='')
        print(self.futures)
        print("the options are: ", end='')
        print(self.options)

    def gettotalfutureasset(self, date):
        totalfutureasset = 0
        for futurename in self.futures:
            [due, oldprice] = futurename.split('-')
            amount = self.futures[futurename][1]
            newprice = doupo_trade.get_closing_price(date, due, 1)
            value = (newprice - int(oldprice)) * amount * self.units
            totalfutureasset += value
        return totalfutureasset

    def gettotaloptionasset(self, date):
        totaloptionasset = 0
        for optionname in self.options:
            amount = self.options[optionname][1]
            newprice = doupo_trade.get_closing_price(date, optionname, 0)
            value = newprice * amount * self.units
            totaloptionasset += value
        return totaloptionasset

    def gettotalasset(self, date):
        totalfutureasset = self.gettotalfutureasset(date)
        totaloptionasset = self.gettotaloptionasset(date)

        total = self.available + totalfutureasset + totaloptionasset
        return total
