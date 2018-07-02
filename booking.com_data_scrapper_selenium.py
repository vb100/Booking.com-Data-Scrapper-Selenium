"""This app. will collect the data about Mowbray Court Hotel  from Booking.com
Prepared by Vytautas Bielinskas at Ekistics Property Advisors LLP"""

from selenium import webdriver
options = webdriver.chrome.options.Options()
options.add_argument("--disable-extensions")

chrome_path = r"C:\Users\user\Desktop\Python\JSscrapping\chromedriver.exe"
driver = webdriver.Chrome(chrome_path)

# Import basic libraries
import pandas as pd
import os

# Get the list of reservation days for the next year
def getPeriod():
    from datetime import date, timedelta
    
    d1 = date(2017,12,15)
    d2 = date(2018,1,10)
    
    dd = [d1 + timedelta(days = x) for x in range((d2 - d1).days + 1)]
        
    dateStr = []
    for x in range(0, len(dd), 1):
        dateStr.append(str(dd[x]))
        print(dateStr)
        
    return dateStr

days = getPeriod()

# Prepare URLs list
urls = []
url_full = 'https://www.booking.com/hotel/gb/the-mowbray-court.en-gb.html?label=gen173nr-1FCAEoggJCAlhYSDNiBW5vcmVmaIgBiAEBmAEuwgEKd2luZG93cyAxMMgBDNgBAegBAfgBC5ICAXmoAgM;sid=b936752e86136715926a341ad92c5f93;all_sr_blocks=183707102_91687460_2_41_0;checkin=2018-01-10;checkout=2018-01-11;dest_id=-2601889;dest_type=city;dist=0;group_adults=2;hapos=1;highlighted_blocks=183707102_91687460_2_41_0;hpos=1;room1=A%2CA;sb_price_type=total;srepoch=1507188269;srfid=432e588605f8385de45b06ab319925e007d99be3X1;srpvid=db6134168cf40284;type=total;ucfs=1&#hotelTmpl'

def getURLs(urls, endday, url_full):
    urls = []
    for i in range(0, endday, 1):
        url_divided = url_full.split("checkin=")
        url_first_part = url_divided[0] + "checkin=" + days[i]
        url_second_part = ";checkout=" + days[i+1] + ((url_divided[1].split("checkout="))[1])[10:]
        url_full = url_first_part + url_second_part
        print(url_full)
        urls.append(url_full)
    return urls

url_list = getURLs(urls, len(days)-1, url_full)

# Crawling the Booking.com pages
for i in range(0, len(days)-1, 1):
    allowing = True;    
    driver.get(url_list[i])
               
    #Preparing free space for new data
    d = {}
    l = []
    
    #Get reservation date
    reservation_date = driver.find_element_by_class_name("sb-date-field__display").text
    d["(Reservation date)"] = reservation_date
    
    #Scanners
    rooms = driver.find_elements_by_class_name("js-track-hp-rt-room-name")
    prices = driver.find_elements_by_class_name("rooms-table-room-price")
    
    #Scanning
    def scanner(rooms, prices, df, allowing):
        if len(rooms) * 2 == len(prices):
            i_price = 0
            for item in range(0, len(rooms), 1):
                #print(rooms[item].text)
                for pricer in range(0, 2, 1):
                    if i_price % 2 == 0:  
                        d[rooms[item].text + " 1"] = float(prices[i_price].text.partition(' ')[2])
                        i_price = i_price + 1
                        continue
                    elif i_price % 2 == 1:
                        d[rooms[item].text + " 2"] = float(prices[i_price].text.partition(' ')[2])
                        i_price = i_price + 1
                        continue
        else:
            print("Need change criterions inside the code!")
            allowing = False
            
        l.append(d)
        return d, allowing
    
    scanner(rooms, prices, d, allowing)

    #It is time to take Panda to the job and appen the existed database
    if allowing == True and l != []:
        df = pd.DataFrame(l)
    
    def writeToFile(df):
        #--> If file does not exist write header
        if not os.path.isfile('Hotel_Price_Data.csv'):
            df.to_csv('Hotel_Price_Data.csv')
        else: # --> Otherwise append data to existing database file
            df.to_csv('Hotel_Price_Data.csv', mode = 'a', header = False)
        return(True)
        
    if allowing == True and l != []:
        writeToFile(df)
    
print("Finished")