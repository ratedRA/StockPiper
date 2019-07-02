#!/usr/bin/env python
# coding: utf-8

# In[3]:


import csv

from datetime import datetime
import sys
import bisect
from statistics import stdev
from collections import defaultdict
import calendar
import difflib

# sorting of list acording to date was yielding lots of duplicates. so unique_items returns
# list containing only one record for a specific date.

def unique_items(L):
    found = set()
    for item in L:
        if item[1] not in found:
            yield item
            found.add(item[1])



month = {v: k for k,v in enumerate(calendar.month_abbr)} #maps month name to its number.

file_name = str(sys.argv[1])
#print(file_name)
try:
    with open(file_name, 'r') as file:
        my_reader = csv.reader(file, delimiter=',')
        rows = []
        for row in my_reader:
            rows.append(row)
except:
    print('No such file. exiting...')
    exit()

stockCodes = []

for i in range(1, len(rows)):
    stockCodes.append(rows[i][0])

while 1:
    try:
        stockName = input('"Welcome Agent! Which stock you need to process?":-')

        try:
            if stockName not in stockCodes:
                matches = difflib.get_close_matches(stockName, stockCodes) # get the closest stock code.
                stockName = matches[0]
                choice = input('"Oops! Do you mean {}? y or n":'.format(stockName))
                if choice.lower()=='n':
                    print('exiting...')
                    exit()
        except:
            print('stock code not found. exiting...')
            exit()

        startDate = list(input('"From which date you want to start (dd-mm-yyyy)":-').split('-'))

        # making compatible with type of month (either number or first three letter of month)
        if startDate[1].isalpha():
            dummy = ''
            for i in range(3):
                if i == 0:
                    dummy += startDate[1][i].upper()
                else:
                    dummy += startDate[1][i].lower()
            m = int(month[dummy])
        else:
            m = int(startDate[1])

        startDate = datetime(int(startDate[2]),m,int(startDate[0]))
        storeStart = startDate.date()
        startDate = startDate.strftime('%Y-%b-%d')

        endDate = list(input('Till which date you want to analyze (dd-mm-yyyy)').split('-'))
        if endDate[1].isalpha():
            dummy = ''
            for i in range(3):
                if i == 0:
                    dummy += endDate[1][i].upper()
                else:
                    dummy += endDate[1][i].lower()
            m = int(month[dummy])
        else:
            m = int(endDate[1])
        endDate = datetime(int(endDate[2]),m,int(endDate[0]))
        storeEnd = endDate.date()
        endDate = endDate.strftime('%Y-%b-%d')

        if storeStart>storeEnd:
            startDate, endDate = endDate, startDate
            storeStart, storeEnd = storeEnd, storeStart

        #print(storeStart, storeEnd)
            
        buy_date = sys.maxsize
        sortedDates = []
        for i in range(1,len(rows)):
            try:
                date = rows[i][1]
                date = list(date.split('-'))
                if date[1][0].isalpha():
                    dummy = ''
                    for k in range(3):
                        if k==0:
                            dummy+=date[1][i].upper()
                        else:
                            dummy+=date[1][i].lower()
                    m = month[dummy]
                else:
                    m = date[1]
                formatdate = datetime(int(date[0]),int(m),int(date[2])).date()
                sortedDates.append(formatdate)

                rows[i][0] = formatdate.sprftime('%Y-%b-%d') 
            except:
                continue
        #print(rows[1:100])

        data = sorted(rows[1:], key=lambda row: row[1]) # sorting data according to date.
        #print(data[0:30])
        data = list(unique_items(data))
        print(data[0:20])
        sortedDates = list(set(sortedDates))

        sortedDates = sorted(sortedDates)

        # for getting the index of startdate and if not found taking previous date.
        x = bisect.bisect_left(sortedDates, storeStart)
        if storeStart in sortedDates:
                x = x
        else:
            if x!=0:
                x-=1
        y = bisect.bisect_left(sortedDates, storeEnd)
        if storeEnd not in sortedDates:
            if y!=0:
                y-=1
        sum1 = 0
        sd = []
        if x>y:
            x,y = y,x
        print(x,y)
        for i in range(x,y+1):
            if data[i][0]==stockName:
                sum1+=float(data[i][2])
                sd.append(float(data[i][2]))
                #print(sum1)
        mean = sum1/(abs(y-x)+1) #calculating mean of of the stock price.
        err = 0
        deviation = 0
        try:
            deviation = stdev(sd)
        except:
            err=1
            print('Something went wrong while calculating Standard Deviation')

        max1 = -(sys.maxsize)
        min1 = sys.maxsize

        #finding buying and selling date of the stock in the given range of date to get max profit.

        for i in range(x,y+1):
            if stockName == data[i][0]:
                buyDate, sellDate = sortedDates[i], sortedDates[i]
                break

        for i in range(x, y+1):
            #print(data[i][6])
            if stockName == data[i][0]:
                # Ensure buydate is less than sell date.
                #print(data[i][1])
                if float(data[i][2])<min1 and sortedDates[i]<=sellDate:
                    min1 = float(data[i][2])
                    buyDate = sortedDates[i]
                    #print(min1)
                if float(data[i][2])>max1 and sortedDates[i]>=buyDate:
                    max1 = float(data[i][2])
                    sellDate = sortedDates[i]
        print()
        print()

        print('Here is your result:- Mean-{}, std- {}, Buy date-{},Sell date-{}, profit-{}'.format(mean,deviation,buyDate,sellDate,max1-min1))

        # print(max1,min1)

        # print(buyDate, sellDate, max1-min1)

        # print(mean)
        # if err==0:
        #     print(deviation)
        ch = input('Do you want to continue? y or n:')
        if ch.lower()=='n':
            break
    except:
        print('Something went wrong')
        exit()



# In[ ]:




