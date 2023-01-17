# -*- coding: utf-8 -*-
"""
Created on 20-07-2022
@author: DHMINE Mohamed
"""
from bs4 import BeautifulSoup as bs
import time
import csv
import re
import pandas as pd
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import argparse
import logging
import requests
import pickle
from functools import wraps
from selenium.webdriver.common.action_chains import ActionChains
# default path to file to store data
from selenium.webdriver.common.by import By

# Library provides the way to automatically manage drivers for chrome
from webdriver_manager.chrome import ChromeDriverManager


def get_information_hotel(target_url):
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
    driver = webdriver.Firefox(executable_path="C:/Users/Mohamed/Documents/SmartROI/geckodriver.exe")
    driver.maximize_window()
    # get driver
    driver.get(target_url)
    time.sleep(3)

    # acceptation cookies
    try :
        element = driver.find_element(by="xpath", value="//button[@id='onetrust-accept-btn-handler']")
        ActionChains(driver).move_to_element(element).click().perform()
    # library bs for scraping
    except :
        pass
    soup = bs(driver.page_source, 'html.parser')
    name = driver.find_element(by='xpath', value="//h1[@class='QdLfr b d Pn']").text
    # print(driver.find_element(by='xpath', value="//span[@class='fHvkI PTrfg']").text)
    data = []
    try:
        address = soup.find('span', {"class": "fHvkI PTrfg"}).text
    except:
        address = 'None'
    # address = driver.find_element(by='xpath', value="//span[contains(@class, 'fHvkI PTrfg')]").text.strip()
    try:
        hotel_experience = driver.find_element(by='xpath', value="//div[@class='Ysobf']").text
    except:
        hotel_experience = 'None'
    try:
        # price = driver.find_element(by='xpath', value="//div[@class='WXMFC b']").text
        price = soup.find('div', {"class": "WXMFC b"})
    except:
        price = 'None'
    try:
        rating = driver.find_element(by='xpath', value="//span[@class='IHSLZ P']").text
    except:
        rating = 'None'
    try:
        review = driver.find_element(by='xpath', value="//span[@class='HWBrU q Wi z Wc']").text
    except:
        review = 'None'
    try:
        rank = driver.find_element(by='xpath', value="//span[@class='Ci _R S4 H3 MD']").text
    except:
        rank = 'None'
    amentities = []
    for a in soup.findAll('div', {"class": "yplav f ME H3 _c"}):
        try:
            amentities.append(a.text.strip())
        except:
            amentities = 'None'

    try:
        # Desc = soup.findAll('div', {"class": "fIrGe _T"}).text.strip()
        Description = driver.find_element(by='xpath', value="//div[@class='fIrGe _T']").text
    except:
        Description = 'None'
    try:
        Grade_walkers = driver.find_element(by='xpath', value="//div[@class='oOsXK WtgYg _S H3 q']").text.split(':')[1]
    except:
        Grade_walkers = 'None'
    try:
        N_Restaurants = driver.find_element(by='xpath', value="//span[@class='iVKnd Bznmz']").text
    except:
        N_Restaurants = 'None'
    try:
        N_Attractions = driver.find_element(by='xpath', value="//span[@class='iVKnd rYxbA']").text
    except:
        N_Attractions = 'None'

    try:

        num = driver.find_element(by='xpath',
                                  value="//a[@class='NFFeO _S ITocq NjUDn']").get_attribute('href').split(':')[1]
    except:

        num = 'None'

    rating_dict = {'Note_Location': None, 'Note_Cleanliness': None,
                   'Note_Service': None, 'Note_Value': None}
    for i, col in enumerate(rating_dict):
        try:
            tmp = soup.findAll('span', {'class': 'LzfAd'})[i].text
            rating_dict[col] = tmp
        except:
            rating_dict[col] = None

    # print(driver.find_element(by='xpath', value="//div[@class='Ysobf']").text)
    # Create a dictionary and transform it to dataframe
    d1 = {'name': name, 'address': address, 'number': num,
          'hotel_experience': hotel_experience,
          'Price': price, 'review': review, 'rating': rating,
          'amenities': [amentities], 'rank': rank,
          'Description': Description,
          'Grade_walkers': Grade_walkers,
          'N_nearRestaurants': N_Restaurants,
          'N_nearAttractions': N_Attractions,
          'Note_Location': rating_dict["Note_Location"],
          'Note_Cleanliness': rating_dict["Note_Cleanliness"],
          'Note_Service': rating_dict["Note_Service"],
          'Note_Value': rating_dict["Note_Value"]
          }
    df = pd.DataFrame.from_dict(d1)
    print(df)
    df.to_excel('data_f.xlsx')
    driver.quit()
    return df


def get_reviews(path_to_file, url):
    """""
    This function scrape every hotel link declared to give all reviews of every user
    Input :
    -----
            path_to_file = path to save the file 
            url =  targuet url for the hotel
    Output :
    -----
            df with all reviews
    """""

    # default path to file to store data
    path_to_file = path_to_file

    # default number of scraped pages
    num_page = 51

    driver = webdriver.Firefox(executable_path="C:/Users/Mohamed/Documents/SmartROI/geckodriver.exe")
    driver.maximize_window()
    driver.get(url)
    time.sleep(3)

    # acceptation cookies
    element = driver.find_element(by="xpath", value="//button[@id='onetrust-accept-btn-handler']")
    ActionChains(driver).move_to_element(element).click().perform()

    reviews = []
    # change the value inside the range to save more or less pages of reviews
    for i in range(1, num_page):
        try:
            # expand the review
            time.sleep(3)
            driver.find_element('xpath', ".//div[contains(@data-test-target, 'expand-review')]").click()
            container = driver.find_elements("xpath", "//div[@data-reviewid]")
            soup = bs(driver.page_source, 'html.parser')
            cont = soup.find_all('div', class_='YibKl MC R2 Gi z Z BB pBbQr')
            # name of the hotel
            name = soup.find('div', class_='jvqAy').text.strip()
            # change the page by clicking on next button
            driver.find_element(by="xpath", value=".//a[@class='ui_button nav next primary ']").click()
            for idx, rev in enumerate(cont):
                hotel = name
                review_inner = rev.find('div', class_='WAllg _T')
                id_review = review_inner['data-reviewid']
                user_and_date = rev.find('div', class_='cRVSd').text
                date = re.search('(.)*(wrote\sa\sreview)\s((.)*)', user_and_date).group(3)
                try:
                    date_of_stay = rev.find("span", class_="teHYY _R Me S4 H3").text.split(':')[1]
                except:
                    date_of_stay = 'none'
                try:
                    user_name = rev.find("a", class_="ui_header_link uyyBf").text
                    user_link = rev.find("a", class_="ui_header_link uyyBf")['href']
                except:
                    user_name = 'none'
                location = rev.find('span', class_='default LXUOn small')
                if location is not None:
                    location = location.text
                try:
                    rating = review_inner.find('span', {"class": re.compile("ui_bubble_rating\sbubble_..")})['class'][
                                 1][-2:]
                    rating_review = float(rating[0] + '.' + rating[1])
                except:
                    rating = 'none'
                try:
                    title = review_inner.find('a', class_='Qwuub').text
                    review_text = review_inner.find('q', class_='QewHA H4 _a').text.replace("\n", " ")
                except:
                    tilte = 'none'
                values = rev.find_all('span', class_='yRNgz')
                n_reviews = int(values[0].text.replace(',', '').replace('.', ''))

                if len(values) > 1:
                    votes = int(values[1].text.replace(',', '').replace('.', ''))
                else:
                    votes = 0

                d1 = {'hotel_name': hotel, 'id_review': id_review, 'title': title,
                      'date': date, 'location': location,
                      'user_name': user_name, 'user_link': user_link, 'date_of_stay': date_of_stay,
                      'rating': rating, 'review': review_text, 'rating_review': rating_review,
                      'n_review_user': n_reviews, 'n_votes_review': votes}

                reviews.append(d1)
        except:
            d1 = 'none'

    df = pd.DataFrame.from_dict(reviews)
    df.to_csv(path_to_file + 'Data_hotels/reviews_{}.csv'.format(name))
    return df
