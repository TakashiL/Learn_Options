from option_trade_framework import Account
import doupo_trade

account = Account(100000, 10)
doupo_trade.buy_future(account, '0609', '1709', 1)
doupo_trade.buy_option(account, '0609', 'm1709-P-2650', 1)
doupo_trade.sell_option(account, '0609', 'm1709-C-2650', 1)

account.printaccount()
print '----------------------------'
print account.gettotalfutureasset('0609')
print account.gettotaloptionasset('0609')
print account.gettotalasset('0609')
print '----------------------------'
print account.gettotalfutureasset('0612')
print account.gettotaloptionasset('0612')
print account.gettotalasset('0612')
print '----------------------------'

doupo_trade.hedge_future(account, '0612', '1709-2686')
doupo_trade.hedge_option(account, '0612', 'm1709-P-2650')
doupo_trade.hedge_option(account, '0612', 'm1709-C-2650')

account.printaccount()
print '----------------------------'
print account.available
print account.gettotalfutureasset('0612')
print account.gettotaloptionasset('0612')
print account.gettotalasset('0612')

