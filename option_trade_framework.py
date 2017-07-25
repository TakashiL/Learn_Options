from __future__ import print_function
from collections import defaultdict
import doupo_trade


class Account:
    def __init__(self, asset=0):
        self.availableAsset = asset
        self.margins = defaultdict(int)
        self.positions = defaultdict(int)

    def addavailableasset(self, money):
        self.availableAsset += money

    def addmargins(self, name, money):
        self.availableAsset -= money
        self.margins[name] += money

    def releasemargins(self, name):
        self.availableAsset += self.margins[name]
        self.margins.pop(name)

    def changepositions(self, name, amount, price, margin=0):
        # + means buy, - means sell
        self.positions[name] += amount

        self.availableAsset -= price * amount

        if margin != 0:
            self.addmargins(name, margin)

        # if position == 0, delete this item, release margin
        if self.positions[name] == 0:
            self.positions.pop(name)
            if name in self.margins:
                self.releasemargins(name)

    def printaccount(self):
        print("the available asset is: ", end='')
        print(self.availableAsset)
        print("the margin asset is: ", end='')
        print(self.margins)
        print("the positions are: ", end='')
        print(self.positions)

    def gettotalmargin(self):
        totalmargin = 0
        for key in self.margins:
            totalmargin += self.margins[key]
        return totalmargin

    def gettotalpositionasset(self, date):
        totalpositionasset = 0
        for key in self.positions:
            if 'm' in key:
                isfuture = 0
            else:
                isfuture = 1
            price = doupo_trade.get_closing_price(date, key, isfuture)
            totalpositionasset += price * self.positions[key] * 10
        return totalpositionasset

    def gettotalasset(self, date):
        totalmargin = self.gettotalmargin()
        totalpositionasset = self.gettotalpositionasset(date)

        total = self.availableAsset + totalmargin + totalpositionasset
        return total
