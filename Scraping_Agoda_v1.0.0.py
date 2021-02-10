from Operations_2 import *

#Declare class
scrapingPrice=Scraping_Price()
readSheet=ReadSheet()

# Declare function
sheetHList=readSheet.Authorization_Hotel()


updatedPrice_1=scrapingPrice.ScrapingOperation()
print(updatedPrice_1)
updatedPrice_2=scrapingPrice.ScrapingOperation_2()
print(updatedPrice_2)



todayStr, nowDate, nowTime=readSheet.GetDateTime()
updatedPrice=0

count=1
for n in sheetHList:
    print(' n :',n,' :: ',count)
    lastDate, minDate, minPrice= readSheet.GetPreviousValue(todayStr, nowDate, nowTime, n)
    print(' :: ',lastDate, ' :: ',minDate,'  ::  ',minPrice)
    if(count==1):
        updatedPrice=updatedPrice_1
    else:
        updatedPrice=updatedPrice_2
        
    if(updatedPrice<minPrice):
        print(' updated ')
        minPrice=updatedPrice
        minDate=nowDate
    readSheet.InsertNewValue_1(todayStr, nowDate, nowTime, n ,nowDate, updatedPrice, minPrice, minDate)
    print(' Complete ')
    count+=1