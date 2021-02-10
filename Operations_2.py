import pandas as pd
from pandas_datareader import data
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime, date
import pytz

from bs4 import BeautifulSoup
import requests
from selenium import webdriver
#from selenium.webdriver.common.keys import Keys
from pyvirtualdisplay import Display



import re
import os


catDict={ 'Hotel':['Hotel_Tracking', 'Hotel_Tracking_2' ]                       
        }

colDict_1={'Date':1,
        'Price':2,
        'UpdateTime':3,
        'minPrice':4,
        'minDate':5
        }


class Scraping_Price(object):
    def __init__(self):
        self.url='https://www.agoda.com/hotel-labaris-khao-yai/hotel/khao-yai-th.html?selectedproperty=5944987&los=2&rooms=1&adults=2&childs=0&languageId=1&userId=17a9f591-583f-4e1b-9e77-deeefbbe2b15&sessionId=rrrwwx4pyjxcikw43livcajf&pageTypeId=1&origin=TH&locale=en-US&cid=-1&aid=130243&currencyCode=THB&htmlLanguage=en-us&cultureInfoName=en-US&ckuid=17a9f591-583f-4e1b-9e77-deeefbbe2b15&prid=0&children=0&priceCur=THB&textToSearch=Hotel%20Labaris%20Khao%20Yai&productType=-1&travellerType=1&familyMode=off&checkin=2021-02-15'
        self.url_2='https://www.agoda.com/oakwood-hotel-residence-sri-racha/hotel/chonburi-th.html?finalPriceView=1&isShowMobileAppPrice=false&cid=-1&numberOfBedrooms=&familyMode=false&adults=2&children=0&rooms=1&maxRooms=0&checkIn=2021-02-15&isCalendarCallout=false&childAges=&numberOfGuest=0&missingChildAges=false&travellerType=1&showReviewSubmissionEntry=false&currencyCode=THB&isFreeOccSearch=false&tspTypes=5&los=2&searchrequestid=4197d3ee-ae2c-482b-b9b4-ddf0b7a9b5f3'

    def ScrapingOperation(self):
        #display=Display(visible=0, size=(1024,768))
        #display.start()

        option=webdriver.ChromeOptions()
        option.add_argument("--incognito")
        driver = webdriver.Chrome(chrome_options=option)
        #driver=webdriver.Chrome('/usr/local/bin/chromedriver',options=option)
        driver.implicitly_wait(30)
        driver.get(self.url)

        elements_p= driver.find_elements_by_xpath('.//span[@class = "pd-price"]') 
        elements_i= driver.find_elements_by_xpath('.//div[@class = "ChildRoomsList-room-featurebucket ChildRoomsList-room-featurebucket-Benefits"]')

        indexList=[]
        count=0
        for title in elements_i:
            try:
                output=title.text
            except:
                output='error'
            result = output.find('Breakfast') 
            #print(' :: ',result)
            if(result>0):
                #print(output, ' == ',type(output),' ::  ',count)
                indexList.append(count)
            count+=1

        #print(indexList)
        priceIndex=[]
        for title in elements_p:
            try:
                output=title.text
            except:
                output='error'
            priceIndex.append(output)       

        #print(priceIndex)
        #print(' result :: ',priceIndex[indexList[0]]) 
        
        #driver.quit()
        #display.stop()
        return  priceIndex[indexList[0]]
        
    def ScrapingOperation_2(self):
        #display=Display(visible=0, size=(1024,768))
        #display.start()

        option=webdriver.ChromeOptions()
        option.add_argument("--incognito")
        driver = webdriver.Chrome(chrome_options=option)
        #driver=webdriver.Chrome('/usr/local/bin/chromedriver',options=option)
        driver.implicitly_wait(30)
        driver.get(self.url_2)

        elements_p= driver.find_elements_by_xpath('.//span[@class = "pd-price"]') 
        elements_i= driver.find_elements_by_xpath('.//div[@class = "ChildRoomsList-room-featurebucket ChildRoomsList-room-featurebucket-Benefits"]')

        indexList=[]
        count=0
        for title in elements_i:
            try:
                output=title.text
            except:
                output='error'
            result = output.find('Breakfast') 
            #print(' :: ',result)
            if(result>0):
                #print(output, ' == ',type(output),' ::  ',count)
                indexList.append(count)
            count+=1

        #print(indexList)
        priceIndex=[]
        
        for title in elements_p:            
            try:
                output=title.text
            except:
                output='error'
            priceIndex.append(output)
        
        #print(priceIndex)
        #print(' result :: ',priceIndex[indexList[0]]) 
        
        #driver.quit()
        #display.stop()
        return  priceIndex[indexList[0]]

class ReadSheet(object):
    def __init__(self):
        self.secret_path_1=r'c:/users/70018928/Quantra_Learning/CheckInOutReminder-e2ff28c53e80.json'
        #self.secret_path_1=r'/home/pi/Project/Webscraping/CheckInOutReminder-e2ff28c53e80.json'
        self.secret_path_2=r'./CheckInOutReminder-e2ff28c53e80.json'
        self.scope= ['https://spreadsheets.google.com/feeds',
                              'https://www.googleapis.com/auth/drive']
    
    def Authorization_Hotel(self):
        try:
            creds = ServiceAccountCredentials.from_json_keyfile_name(self.secret_path_1, self.scope)
        except:
            creds = ServiceAccountCredentials.from_json_keyfile_name(self.secret_path_2, self.scope)
        client = gspread.authorize(creds) 
        sheetHList=[]
        cList=catDict['Hotel']
        for n in cList:
            sheetHList.append(client.open("DataScraping_Hotel").worksheet(n))
        return sheetHList

    def StrToDate(self,strIn):
        return datetime.strptime(strIn, '%Y-%m-%d')

    def Date2TString(self, dateIn):
        return dateIn.strftime("%Y-%m-%d")

    def GetDateTime(self):
        todayUTC=datetime.today()
        nowUTC=datetime.now()
        # dd/mm/YY H:M:S
        to_zone = pytz.timezone('Asia/Bangkok')

        today=todayUTC.astimezone(to_zone)
        now=nowUTC.astimezone(to_zone)

        todayStr=today.strftime("%Y-%m-%d")
        nowDate = now.strftime("%Y-%m-%d")
        nowTime = now.strftime("%H:%M:%S")

        #print(' today : ',todayStr)
        #print(nowDate, ' ==> ', nowTime)
        return todayStr, nowDate, nowTime

    def InsertNewValue_1(self,todayStr, nowDate, nowTime, sheet, dateIn, priceIn, minPrice, minDate):
        lenRecords=len(sheet.get_all_values())
        list_of_hashes=sheet.get_all_records()
        lenHash=len(list_of_hashes)
        print(" len : ",lenRecords)
        lastDate=sheet.cell(lenRecords,1).value
        print(' lastDate : ',lastDate)
        lenDate=len(list_of_hashes[lenHash-1]['Date'])
        if(dateIn == lastDate):
            todayRow=lenRecords
            row_index=todayRow
            col_index=colDict_1['Price']
            message=priceIn
            sheet.update_cell(row_index, col_index,message)
            col_index=colDict_1['UpdateTime']
            message=nowTime
            sheet.update_cell(row_index, col_index,message)
            col_index=colDict_1['minPrice']
            message=minPrice
            sheet.update_cell(row_index, col_index,message)
            col_index=colDict_1['minDate']
            message=minDate
            sheet.update_cell(row_index, col_index,message)
            print('Updated at ', nowTime)
        else:
            todayRow=lenRecords+1
            row_index=todayRow
            col_index=colDict_1['Date']
            message=todayStr
            sheet.update_cell(row_index, col_index,message)
            col_index=colDict_1['Price']
            message=priceIn
            sheet.update_cell(row_index, col_index,message)
            col_index=colDict_1['UpdateTime']
            message=nowTime
            sheet.update_cell(row_index, col_index,message)
            col_index=colDict_1['minPrice']
            message=minPrice
            sheet.update_cell(row_index, col_index,message)
            col_index=colDict_1['minDate']
            message=minDate
            sheet.update_cell(row_index, col_index,message)
            print('Updated on ', todayStr, ' :: ', nowTime)

    def GetPreviousValue(self, todayStr, nowDate, nowTime, sheet):
        lenRecords=len(sheet.get_all_values())
        list_of_hashes=sheet.get_all_records()
        lenHash=len(list_of_hashes)
        print(" len : ",lenRecords)
        lastDate=sheet.cell(lenRecords,1).value
        print(' lastDate : ',lastDate)
        #lenDate=len(list_of_hashes[lenHash-1]['Date'])
        #previousDate=sheet.cell(lenRecords-1,1).value
        minPrice=sheet.cell(lenRecords-1,4).value
        minDate=sheet.cell(lenRecords-1,5).value
        
        return lastDate, minDate, minPrice
    
    def LoadSheet(self,sheet):
        listSheet=sheet.get_all_values()
        listHash=sheet.get_all_records()
        dfSet=pd.DataFrame()
        lenList=len(listHash)
        colList=listSheet[0]
        dateList=[]
        priceList=[]
        updateList=[]
        for n in range(0,lenList):
            dateList.append(self.StrToDate(listHash[n][colList[0]]))
            priceList.append(listHash[n][colList[1]])
            updateList.append(listHash[n][colList[2]])
        
        dfSet=pd.concat([pd.DataFrame(dateList),pd.DataFrame(priceList),pd.DataFrame(updateList)],axis=1)
        dfSet.columns=['Date','Price','Update']
        
        return dfSet
                                                    
        
        

