
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

try:
    file_name = str(sys.argv[1])
except:
    print('enter file name')
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

# list to store all stockcodes.
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

        # start date should always be before than end date
        if storeStart>storeEnd:
            startDate, endDate = endDate, startDate
            storeStart, storeEnd = storeEnd, storeStart

        # SortedDates only contain list of dates in sorted manner
        # in order to get the index of buyDate and endDate
        # we can use the binary search over this list.
        # this would decrease the time complexity of code 
        sortedDates = []
        for i in range(1,len(rows)):
            try:
                date = rows[i][1]
                date = list(date.split('-'))
                if date[1][0].isalpha():
                    dummy = ''
                    for k in range(3):
                        if k==0:
                            dummy+=date[1][k].upper()
                        else:
                            dummy+=date[1][k].lower()
                    m = month[dummy]
                else:
                    m = date[1]
                formatdate = datetime(int(date[0]),int(m),int(date[2]))
                sortedDates.append(formatdate.date())

                rows[i][1] = formatdate.strftime('%Y-%b-%d') 
            except:
                continue
        
        # Sorting the entire data(list of list) with respect to date
        data = sorted(rows, key=lambda row: row[1]) # sorting data according to date.
        # Taking data of unqiue dates
        data = list(unique_items(data))
        # Similar for sortedDate list
        sortedDates = list(set(sortedDates))

        sortedDates = sorted(sortedDates)
        # x stores the index of startdate and if not found taking previous date.
        x = bisect.bisect_left(sortedDates, storeStart)
        if storeStart in sortedDates:
                x = x
        else:
            if x!=0:
                x-=1
        # y stores the index of enDate and if not found taking previous date.
        y = bisect.bisect_left(sortedDates, storeEnd)
        if storeEnd not in sortedDates:
            if y!=0:
                y-=1
        sum1 = 0
        sd = []
        if x>y:
            x,y = y,x

        # taking of stocks price in the range of given dates
        for i in range(x,y+1):
            if data[i][0]==stockName:
                sum1+=float(data[i][2])
                sd.append(float(data[i][2]))
    
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
        # the default value od them can be obtained using the date on the range range they 
        # appear for the first time
        for i in range(x,y+1):
            if stockName == data[i][0]:
                buyDate, sellDate = sortedDates[i], sortedDates[i]
                break
        # calculating buyDate and sellDate in the given range
        # of dates in order to get maximum profit.
        for i in range(x, y+1):
            if stockName == data[i][0]:
                # Ensure buydate is less than sell date.
                if float(data[i][2])<min1 and sortedDates[i]<=sellDate:
                    min1 = float(data[i][2])
                    buyDate = sortedDates[i]
                if float(data[i][2])>max1 and sortedDates[i]>=buyDate:
                    max1 = float(data[i][2])
                    sellDate = sortedDates[i]
        print()
        print()
        if sum1 == 0.0:
            buyDate = None
            sellDate = None
            profit = None
        else:
            profit = max1-min1

        print('Here is your result:- Mean-{}, std- {}, Buy date-{},Sell date-{}, profit-{}'.format(mean,deviation,buyDate,sellDate,profit))

        ch = input('Do you want to continue? y or n:')
        if ch.lower()=='n':
            break
    except:
        print('Something went wrong')
        exit()
    finally:
        print('The program has been executed successfully. Closing the file')
        file.close()







