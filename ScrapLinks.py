# -*- coding: utf-8 -*-
from typing import List
import time
from bs4 import BeautifulSoup
from selenium import webdriver

from selenium.webdriver.common.keys import Keys
import csv
import re
import pandas as pd
hotel = []
url = []
url1 = "https://www.tripadvisor.fr/Hotels-g187234-oa"
url2 = "-Nice_French_Riviera_Cote_d_Azur_Provence_Alpes_Cote_d_Azur-Hotels.html#BODYCON"
domain = 'https://www.tripadvisor.fr'

target_urls = [(url1 + str(i) + url2) for i in list(map(lambda x: 30 * x, range(1, 15)))]
target_url = "https://www.tripadvisor.com/Hotels-g187234-Nice_French_Riviera_Cote_d_Azur_Provence_Alpes_Cote_d_Azur-Hotels.html"
target_urls.insert(1, target_url)

# Library provides the way to automatically manage drivers for chrome
from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(ChromeDriverManager().install())
time.sleep(1)
# url to scrap
# get driver
for l in target_urls:
    driver.get(l)
    time.sleep(1)
    # library bs for scraping
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    hotel_blocks = soup.find_all('div', {"class": "prw_rup prw_meta_hsx_responsive_listing ui_section listItem"})
    for element in hotel_blocks:
        #extarct links of hotels
        urls = domain+element.find('div', {"class": "listing_title"}).find('a').get('href')
        url.append(urls)
        hotel.append(element.text.strip())

#Create a dictionary and transform it to dataframe
d1 = {'Hotel': hotel, "url" : url }
df = pd.DataFrame.from_dict(d1)
print(df)
#data to excel
df.to_excel('TripAdvisor_Nice_Links.xlsx')


