import requests
import re
import csv
import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

# configure web driver
chrome_options = Options()
chrome_options.headless = True     # use background mode
driver = webdriver.Chrome("chromedriver.exe", chrome_options=chrome_options)

with open("organisations.csv", encoding='UTF8') as f:
    organisations = [row.replace("\n","") for row in f]
    organisations.pop(0)

org_links = {}

for organisation in organisations:
    url = f"https://patents.google.com/?q={organisation}&oq={organisation}"
    driver.get(url)
    time.sleep(5)
    page = driver.page_source
    soup = BeautifulSoup(page, 'html.parser')
    root = soup.find_all("state-modifier", {"class" : "result-title style-scope search-result-item"})
    links = []
    for each_tag in root:
        link = each_tag["data-result"]
        links.append(link)
    org_links[organisation] = links
    print(org_links)

with open("org_links.json", "w") as outfile:
    json.dump(org_links, outfile, indent = 4, ensure_ascii=False)
driver.quit()
