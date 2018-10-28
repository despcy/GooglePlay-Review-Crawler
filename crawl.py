
from selenium import webdriver
from bs4 import BeautifulSoup
from pdb import set_trace as bp ##for testing
import re
import time
import csv
outputFileName='result'
link = "https://play.google.com/store/apps/details?id=io.fusetech.stackademia&hl=en_US&showAllReviews=true"
driver = webdriver.Chrome("./chromedriver")
driver.get(link)
title = driver.find_element_by_xpath('//*[@id="fcxH9b"]/div[4]/c-wiz/div/div[3]/meta[2]').get_attribute('content')

print(title)
flag=0
while 1:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    try:
        loadMore=driver.find_element_by_xpath("//*[contains(@class,'U26fgb O0WRkf oG5Srb C0oVfc n9lfJ')]").click()
    except:
        time.sleep(1)
        flag=flag+1
        if flag >= 10:
            break
    else:
        flag=0




reviews=driver.find_elements_by_xpath("//*[@jsname='fk8dgd']//div[@class='d15Mdf bAhLNe']")
print("There are "+str(len(reviews))+" reviews avaliable")
print("Writing the data...")


with open(outputFileName+'.csv', mode='w') as file:
    writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    writer.writerow(["name","ratings","date","helpful vote","comment"])
    for review in reviews:
        try:
            soup=BeautifulSoup(review.get_attribute("innerHTML"),"lxml")
            name=soup.find(class_="X43Kjb").text
            ratings=soup.find('div',role='img').get('aria-label').strip("Rated ")[0]
            date=soup.find(class_="p2TkOb").text
            helpful=soup.find(class_="jUL89d y92BAb").text
            if not helpful:
                helpful=0;
                comment=soup.find('span',jsname='fbQN7e').text
                if not comment:#expand the comment button
                comment=soup.find('span',jsname='bN97Pc').text
                writer.writerow([name.encode('utf-8'),ratings,date,helpful,comment.encode('utf-8')])
        except:
            print("error")
