from bs4 import BeautifulSoup
from selenium import webdriver
import requests
import time
import csv
import re
from Functions import get_infromation_hotel
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

# Library provides the way to automatically manage drivers for chrome
from webdriver_manager.chrome import ChromeDriverManager


driver = webdriver.Chrome(ChromeDriverManager().install())
time.sleep(1)
domain = 'https://www.tripadvisor.fr'

# import hotels' urls
df = pd.read_excel('TripAdvisor_Nice_Links.xlsx')
df = df.drop_duplicates(subset='url')
print(df.url)

# Use function get_information_hotel from Functions.py file to do the loop to extract hotels'features
df1 = pd.DataFrame()
df2 = pd.DataFrame()
for i in df['url']:
    print(i)
    df2 = get_infromation_hotel(i)
    df1 = df1.append(df2)
print(df1)
print(df1.info())

# save data to an excel file
df1.to_excel('T_data_hotels.xlsx')

# %%
