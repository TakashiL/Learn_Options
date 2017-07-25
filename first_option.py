from option_trade_framework import Account
import doupo_trade

account = Account(100000)
doupo_trade.buy_future(account, '0609', '1709', 1, 30000)
doupo_trade.buy_option(account, '0609', 'm1709-P-2650', 1)
doupo_trade.sell_option(account, '0609', 'm1709-C-2650', 1, 13000)

account.printaccount()
print '----------------------------'
print account.availableAsset
print account.gettotalmargin()
print account.gettotalpositionasset('0609')
print account.gettotalasset('0609')
print '----------------------------'
print account.availableAsset
print account.gettotalmargin()
print account.gettotalpositionasset('0612')
print account.gettotalasset('0612')

doupo_trade.sell_future(account, '0612', '1709', 1)
doupo_trade.sell_option(account, '0612', 'm1709-P-2650', 1, 20000)
doupo_trade.buy_option(account, '0612', 'm1709-C-2650', 1)

print '----------------------------'
account.printaccount()
print '----------------------------'
print account.availableAsset
print account.gettotalmargin()
print account.gettotalpositionasset('0612')
print account.gettotalasset('0612')