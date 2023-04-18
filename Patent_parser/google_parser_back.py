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

with open("Parsers/organisations.csv", encoding='UTF8') as f:
    organisations = [row.replace("\n","") for row in f]
    organisations.pop(0)


for organisation in organisations:
    url = f"https://patents.google.com/?assignee={organisation}&language=RUSSIAN&num=100"
    driver.get(url)
    time.sleep(5)
    page = driver.page_source
    org = BeautifulSoup(page, 'html.parser')

    root = org.find_all("state-modifier", {"class": "result-title style-scope search-result-item"})
    for each_tag in root:
        link = each_tag["data-result"]
        parse_link = 'https://patents.google.com/' + link
        driver.get(parse_link)
        time.sleep(15)
        link_page = driver.page_source
        soup = BeautifulSoup(link_page, 'html.parser')


        #Abstact
        abstract = soup.find('meta', attrs={'name':'description'})
        if abstract:
            abstract_text = abstract["content"]
        else:
            abstract_text = ""

        #Title
        title = soup.find('meta', attrs={'name':'DC.title'})
        title_text = title["content"]


        #Index
        index = soup.find('h2', attrs={'id':'pubnum'})
        if index:
            index_text = index.text
        else:
            index_text = ""


        #Date of publication
        date_text = ""
        date = soup.find('div', attrs={'class':'publication style-scope application-timeline'})
        if date:
            date_text = date.text
        else:
            date = ""



        #Contributor -- problem
        contributor = soup.find_all('meta', attrs={'name':'DC.contributor'})
        contributor_string = ""
        for cont in contributor:
            contributor_text = cont["content"]
            contributor_string += contributor_text + "\n"
        #print(contributor_text)

        #MPK
        mpk_string = ""
        for ipc in soup.find_all('div', {'class': 'classification-tree', 'hidden': False})[3::4]:
            mpk = ipc.find_all('a', {'id': 'link'})[-1].text
            mpk_string += mpk + "\n"

        #Description
        description_string = ""
        description = soup.find_all("div", {"class" : "description-paragraph style-scope patent-text"})
        if description:
            for des in description:
                description_text = des.text
                description_string += description_text + "\n"
        else:
            description_string = ""
        #print(description_string)

        #Claims
        claim_string = ""
        claims = soup.find_all("div", {"class" : "claim-text style-scope patent-text"})
        if claims:
            for claim in claims:
                claim_text = claim.text
                claim_string += claim_text + "\n"
        else:
            claim_string = ""
        #print(claim_string)

        #Similar documents
        docs_string = ""
        docs = soup.find_all("div", {"class":"tbody style-scope patent-result"})
        table = docs[1].find_all("state-modifier", {"class" : "style-scope patent-result"})
        for doc in table:
            link = doc["data-result"]
            similar_link = f"https://patents.google.com/{link}"
            docs_string += similar_link + "\n"
        #print(docs_string)

        row = [Id, title_text, abstract_text, index_text, mpk_string, date_text, contributor_string, description_string, claim_string, docs_string]
        data = [row]
        client.insert('google_patents', data, column_names=['Id','Title', 'Abstract', 'Index', 'IPC', 'Date_of_publication','Contributor', 'Description', 'Claims','Similar_docs'], database = "db_patents")
        Id += 1


driver.quit()
