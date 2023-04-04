import requests
import re
import csv
import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from database import client


# configure web driver
chrome_options = Options()
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--no-sandbox")
chrome_options.headless = True     # use background mode
driver = webdriver.Chrome("chromedriver.exe", chrome_options=chrome_options)

Id = 1

with open("organisations.csv", encoding='UTF8') as f:
    organisations = [row.replace("\n","") for row in f]
    organisations.pop(0)



parse_link = "https://patents.google.com/patent/DK3180198T3/en?q=(B42)&num=100"

url = parse_link
driver.get(url)
time.sleep(15)
page = driver.page_source
soup = BeautifulSoup(page, 'html.parser')

#MPK
mpk_string= ""
mpk_tree = soup.find_all('div', {"class" : "style-scope classification-tree"})
mpk = soup.find_all("state-modifier", {"class":"code style-scope classification-tree"})
for mpk_part in mpk:
    #mpk_text = mpk_part.text
    print(mpk_part)
   # mpk_string +=mpk_text[0] + "\n"
