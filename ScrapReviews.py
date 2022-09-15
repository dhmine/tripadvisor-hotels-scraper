#import requests
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup as bs
import pandas as pd
from pandas import DataFrame
import time
import re
import argparse
import logging
import requests
import pickle
from functools import wraps
import csv
import pandas as pd
import time
from selenium.webdriver.common.action_chains import ActionChains
# default path to file to store data
from selenium.webdriver.common.by import By
from review_test import get_reviews
import openpyxl



df = pd.read_excel('TripAdvisor_Nice_Links.xlsx') 
for i in df.url.unique() :
    get_reviews("scrap/Datas/", i)