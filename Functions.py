# -*- coding: utf-8 -*-
"""
Created on 20-07-2022
@author: DHMINE Mohamed
"""
from bs4 import BeautifulSoup
from selenium import webdriver
import requests
import time
import csv
import re
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

# Library provides the way to automatically manage drivers for chrome
from webdriver_manager.chrome import ChromeDriverManager

def get_infromation_hotel(target_url):
    """""
    This function scrape every hotel link declared to give all features of it
    Input :
    -----
            targuet url for the hotel
    Output :
    -----
            Adress : adress of the hotel
            Amenities : All of ameneties of the hotel
            Hotel_experience : hotel review feedback
    """""
    driver = webdriver.Chrome(ChromeDriverManager().install())
    # get driver
    driver.get(target_url)
    time.sleep(1)

    # library bs for scraping
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    name = driver.find_element(by='xpath', value="//h1[@class='QdLfr b d Pn']").text
    # print(driver.find_element(by='xpath', value="//span[@class='fHvkI PTrfg']").text)
    try:
        address = soup.find('span', {"class": "fHvkI PTrfg"}).text
    except:
        address = 'None'
    # address = driver.find_element(by='xpath', value="//span[contains(@class, 'fHvkI PTrfg')]").text.strip()
    try :
        hotel_experience = driver.find_element(by='xpath', value="//div[@class='Ysobf']").text
    except:
        hotel_experience = 'None'
    try :
        # price = driver.find_element(by='xpath', value="//div[@class='WXMFC b']").text
        price = soup.find('div', {"class": "WXMFC b"})
    except:
        price = 'None'
    try:
        rating = driver.find_element(by='xpath', value="//span[@class='IHSLZ P']").text
    except:
        rating = 'None'
    try :
        review = driver.find_element(by='xpath', value="//span[@class='HWBrU q Wi z Wc']").text
    except :
        review = 'None'
    try :
        rank = driver.find_element(by='xpath', value="//span[@class='Ci _R S4 H3 MD']").text
    except :
        rank = 'None'
    amentities = []
    for a in soup.findAll('div', {"class": "yplav f ME H3 _c"}):
        try :
            amentities.append(a.text.strip())
        except :
            amentities = 'None'
    # print(driver.find_element(by='xpath', value="//div[@class='Ysobf']").text)
    # Create a dictionary and transform it to dataframe
    d1 = {'name': name, 'address': address,
          'hotel_experience': hotel_experience,
          'Price': price, 'review': review, 'rating':rating,
          'amenities': [amentities], 'rank': rank}
    df = pd.DataFrame.from_dict(d1)
    print(df)
    return df

