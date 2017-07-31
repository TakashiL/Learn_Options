# coding: utf-8
import pandas as pd
import os
from collections import defaultdict

# parameter
futureslip = 2
optionslip = 1
futureservicefee = 3
optionservicefee = 1


def gettradingdaydict():
    tradingday = defaultdict(int)
    count = 59
    for f in os.listdir("doupo_option_data"):
        date = f.split('.')[0]
        tradingday[date] = count
        count += 1
    return tradingday


# retrun type: dataframe
# description: option data of a specific day
def option_onedaydata(filename):
    # 商品名称， 合约名称， 开盘价， 最高价， 最低价， 收盘价， 前结算价， 结算价， 涨跌， 涨跌1， Delta， 成交量， 持仓量， 持仓量变化， 成交额， 行权量
    columnnames = ['spmc', 'hymc', 'kpj', 'zgj', 'zdj', 'spj', 'qjsj', 'jsj', 'zd', 'zd1', 'delta', 'cjl', 'ccl', 'ccjbh', 'cje', 'xql']
    temparray = []

    fileaddress = r"doupo_option_data\\" + filename
    f = open(fileaddress)
    f.readline()  # remove first line

    datalines = f.readlines()
    for line in datalines:
        line = line.replace(',', '')  # e.g. 1,487 -> 1487
        line = line.split()
        if len(line) != 16:  # stop when meets the total line
            break
        temparray.append(line)

    df = pd.DataFrame(temparray)
    # set column names
    df.columns = columnnames
    # change numbers from string to numeric  i.e. third column to 15th column
    for i in range(2, 16):
        df.iloc[:, i] = pd.to_numeric(df.iloc[:, i])

    return df


def dominant_calloptions(date, dominant):
    options = []
    df = option_onedaydata(date + '.txt')
    for option in df['hymc']:
        month = option.split('-')[0]
        type = option.split('-')[1]
        if dominant in month and type == 'C':
            options.append(option)
    return options


# retrun type: defaultdict
# description: all days all option data, e.g. {'0331.txt': df, '0405.txt': df}
def option_alldata():
    data = defaultdict(pd.DataFrame)
    for f in os.listdir("doupo_option_data"):
        data[f] = option_onedaydata(f)
    return data


# retrun type: dataframe
# description: future data of a specific day
def future_onedaydata(filename):
    # 商品名称， 交割月份， 开盘价， 最高价， 最低价， 收盘价， 前结算价， 结算价， 涨跌， 涨跌1， 成交量， 持仓量， 持仓量变化， 成交额
    columnnames = ['spmc', 'jgyf', 'kpj', 'zgj', 'zdj', 'spj', 'qjsj', 'jsj', 'zd', 'zd1', 'cjl', 'ccl', 'ccjbh', 'cje']
    temparray = []

    fileaddress = r"doupo_future_data\\" + filename
    f = open(fileaddress)
    f.readline()  # remove first line

    datalines = f.readlines()
    for line in datalines:
        line = line.replace(',', '')
        line = line.split()
        if len(line) != 14:
            break
        temparray.append(line)

    df = pd.DataFrame(temparray)
    # set column names
    df.columns = columnnames
    # change numbers from string to numeric  i.e. third column to 15th column
    for i in range(2, 14):
        df.iloc[:, i] = pd.to_numeric(df.iloc[:, i])

    return df


# retrun type: defaultdict
# description: all days all future data, e.g. {'0331.txt': df, '0405.txt': df}
def future_alldata():
    data = defaultdict(pd.DataFrame)
    for f in os.listdir("doupo_future_data"):
        data[f] = future_onedaydata(f)

    return data


# retrun type: defaultdict
# description: all dominant contract, e.g. {'0301.txt': '1705', '0405.txt': '1709'}
def dominantcontract():
    dominant = defaultdict(str)
    data = future_alldata()
    for key in data:
        df = data[key]
        dominant[key] = df.iloc[df['cjl'].idxmax(), 1]

    return dominant


# retrun type: defaultdict
# description: all days dominant option data, e.g. {'0331.txt': df, '0405.txt': df}
def option_dominantdata():
    alldata = option_alldata()
    dominant = dominantcontract()
    for key in dominant:
        if key not in alldata:  # if no option data for this date, skip
            continue
        dcontract = dominant[key]
        tempdf = alldata[key]
        tempdf = tempdf[tempdf['hymc'].str.contains(dcontract)]
        alldata[key] = tempdf

    return alldata


def get_closing_price(date, name, isfuture):
    if isfuture == 0:
        df = option_onedaydata(date + '.txt')
        price = df[df['hymc'].str.contains(name)]['spj']
    elif isfuture == 1:
        df = future_onedaydata(date + '.txt')
        price = df[df['jgyf'].str.contains(name)]['spj']
    else:
        print "error in argument option " + date + " - " + name
        exit(0)
    return price.iloc[0]


def take_option(account, date, name, amount):
    price = get_closing_price(date, name, 0)
    account.available -= optionservicefee
    account.takenewoption(name, price, amount)
    print 'Trade record: Option:' + name + ' date:' + date + ' amount:' + str(amount) + ' price:' + str(price)


def buy_option(account, date, name, amount):
    take_option(account, date, name, amount)


def sell_option(account, date, name, amount):
    # calculate margin if has any
    take_option(account, date, name, -amount)


def hedge_option(account, date, name):
    # assume close this option at all
    price = get_closing_price(date, name, 0)
    amount = account.options[name][1]
    account.available -= optionservicefee
    account.available -= optionslip * account.units
    account.hedgeoption(name, price)
    print 'Hedge record: Option:' + name + ' date:' + date + ' amount:' + str(amount) + ' new price:' + str(price)


def take_future(account, date, name, amount):
    price = get_closing_price(date, name, 1)
    account.available -= futureservicefee
    account.takenewfuture(name, price, amount)
    print 'Trade record: Future:' + name + ' date:' + date + ' amount:' + str(amount) + ' price:' + str(price)


def buy_future(account, date, name, amount):
    # calculate margin if has any
    take_future(account, date, name, amount)


def sell_future(account, date, name, amount):
    # calculate margin if has any
    take_future(account, date, name, -amount)


def hedge_future(account, date, futurename):
    due = futurename.split('-')[0]
    # assume close this future at all
    price = get_closing_price(date, due, 1)
    amount = account.futures[futurename][1]
    account.available -= futureservicefee
    account.available -= futureslip * account.units
    account.hedgefuture(futurename, price)
    print 'Hedge record: Future:' + futurename + ' date:' + date + ' amount:' + str(amount) + ' new price:' + str(price)

