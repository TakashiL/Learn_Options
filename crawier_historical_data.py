import urllib2
import csv
import codecs
import time

'''
option:
url example: "http://www.dce.com.cn/publicweb/quotesdata/exportDayQuotesChData.html?dayQuotes.variety=all&dayQuotes.trade_type=1&year=2017&month=6&day=12&exportFlag=txt"

future
url example: "http://www.dce.com.cn/publicweb/quotesdata/exportDayQuotesChData.html?dayQuotes.variety=m&dayQuotes.trade_type=0&year=2017&month=6&day=12&exportFlag=txt"

dayQuotes.variety: m - doupo
dayQuotes.trade_type: 0 - futures, 1 - options
year: 2017 - 2017 year
month: 0 - January, 1 - February, ..., 11 - December
day: 1 - 1st, 2 - 2nd, ..., 31 - 31th
exportFlag: txt - txt, excel - csv
'''

# parameter
baseurl = "http://www.dce.com.cn/publicweb/quotesdata/exportDayQuotesChData.html?dayQuotes.variety=all&dayQuotes.trade_type=1&year=2017"
future_baseurl = "http://www.dce.com.cn/publicweb/quotesdata/exportDayQuotesChData.html?dayQuotes.variety=m&dayQuotes.trade_type=0&year=2017"
endurl = "&exportFlag=txt"
months = [2, 3, 4, 5, 6]  # 2 - March, 3 - April, 4 - May, 5 - June, 6 - July
days = range(1, 32)

for month in months:
    for day in days:
        url = future_baseurl + "&month=" + str(month) + "&day=" + str(day) + endurl

        response = urllib2.urlopen(url)
        data = response.read()

        if day < 10:
            day_str = '0' + str(day)
        else:
            day_str = str(day)
        month_str = '0' + str(month+1)

        txtPath = r"doupo_future_data\\" + month_str + day_str + ".txt"

        # write into txt file
        f = file(txtPath, "w+")
        f.write(data)
        f.close()

        '''
        csvPath = r"doupo_option_data\\" + month_str + day_str + ".csv"
        
        # create csv writer
        csvFile = file(csvPath, "wb")
        csvFile.write(codecs.BOM_UTF8)  # handle chinese coding bug
        writer = csv.writer(csvFile)

        # read txt file and convert to csv
        f = open(txtPath, "r")
        lines = f.readlines()
        for line in lines:
            line = line.split()
            writer.writerow(line)

        # close file
        f.close()
        csvFile.close()
        '''

        print month_str + "-" + day_str

        time.sleep(1)







