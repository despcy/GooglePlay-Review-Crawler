
from selenium import webdriver
import re
import time
import csv

driver = webdriver.Chrome("./chromedriver")
link = "https://play.google.com/store/apps/details?id=com.naturalcycles.cordova&hl=en_US&showAllReviews=true"
#link = "https://play.google.com/store/apps/details?id=com.avaamo.android&hl=en_US&showAllReviews=true"
driver.get(link)
#driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
title = driver.find_element_by_xpath('//*[@id="fcxH9b"]/div[4]/c-wiz/div/div[3]/meta[2]').get_attribute('content')

print(title)
flag=0
while 1:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    try:
        loadMore=driver.find_element_by_xpath("//*[contains(@class,'U26fgb O0WRkf oG5Srb C0oVfc n9lfJ')]").click()
    except:
        time.sleep(3)
        flag=flag+1
        if flag >= 20:
            break
    else:
        flag=0


print("Writing the data...")
reviews=driver.find_elements_by_xpath("//*[@jsname='fk8dgd']//div[@class='d15Mdf bAhLNe']")
with open(title+'.csv', mode='w') as file:
    writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    writer.writerow(["name","ratings","date","helpful vote","comment"])
    for review in reviews:
        name=review.find_element_by_class_name('X43Kjb').text
        ratings=re.findall(r'\d+',review.find_element_by_css_selector("[role=img]").get_attribute('aria-label'))[0]
        date=review.find_element_by_class_name('p2TkOb').text
        helpful=review.find_element_by_css_selector("[class='jUL89d y92BAb']").text
        if not helpful:
            helpful=0;
        comment=review.find_element_by_css_selector("[jsname='fbQN7e']").get_attribute("textContent")
        if not comment:#expand the comment button
            continue;
            comment=review.find_element_by_css_selector("[jsname='bN97Pc']").get_attribute("textContent")
        writer.writerow([name.encode('utf-8'),ratings,date,helpful,comment.encode('utf-8')])
