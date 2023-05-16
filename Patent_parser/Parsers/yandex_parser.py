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

for organisation in organisations:

    url = f"https://yandex.ru/patents?dco=RU&dco=SU&dl=ru&dt=0&dty=1&dty=2&s=0&sp=0&spp=50&st=0&text={organisation}"
    driver.get(url)
    time.sleep(5)
    page = driver.page_source
    soup = BeautifulSoup(page, 'html.parser')

    pages = soup.find('div', {"class" : "leaf-button leaf-button--last"})
    if pages:
        page = int(pages.text)
    else:
        page = 1

    for i in range(page-1):
        url = f"https://yandex.ru/patents?dco=RU&dl=ru&dt=0&dty=1&dty=2&s=0&sp={i}&spp=50&st=0&text={organisation}"
        driver.get(url)
        time.sleep(5)
        page = driver.page_source
        soup = BeautifulSoup(page, 'html.parser')

        #Links
        links = soup.find_all('a', {"class" : "snippet-title"})

        for link in links:
            parse_link = "https://yandex.ru" + link['href']

            url = parse_link
            driver.get(url)
            time.sleep(15)
            page = driver.page_source
            soup = BeautifulSoup(page, 'html.parser')

            #Title
            title = soup.find('div', {"class" : "document-title document-title__desktop"})
            if title:
                title_text = title.text
            else:
                title_text = ""

            abstract_check = soup.find_all('div', {"id": "doc-abstract"})
            claims_check = soup.find_all('div', {"id": "doc-claims"})
            description_check = soup.find_all('div', {"id": "doc-description"})

            abstract_text = ""
            claim_string = ""
            description_string = ""

            #Abstract
            abstract = soup.find('div', {"id" : "doc-abstract"})
            if abstract:
                abstract_text = abstract.find_next_sibling('div').text
            else:
                abstract_text = ""


            #Claims
            claims = soup.find('div', {"id" : "doc-claims"})
            if claims:
                claim_string = claims.find_next_sibling('div').text
            else:
                claim_string = ""



            #Description
            description = soup.find('div', {"id" : "doc-description"})
            if description:
                description_string = description.find_next_sibling('div').text
            else:
                description_string = ""


            #Index
            index = soup.find('div', {"class" : "doc-summary-url"})
            if index:
                index_text = index.text
            else:
                index_text = ""


            #MPK
            mpk_string = ""
            mpk = soup.find_all('div', {"class" : "header-mpk-item"})
            for mpk_part in mpk:
                if mpk_part.text != "МПК":
                    mpk_text = mpk_part.text.split("(")
                    mpk_string += mpk_text[0] + "\n"


            #Contributor
            contributor = soup.find('span', {"class" : "doc-summary-item__value"})
            contributor_string = contributor.text


            #Publicaton date
            date = soup.find_all('span', {"class" : "doc-summary-item__value"})
            date_text = date[3].text


            #Authors
            authors = soup.find_all('div', {"class" : "header-content-item"})
            authors_text = authors[2].text


            #Similar patents
            docs_string = ""
            sim_patents = soup.find_all('div', {"class" : "doctable_rows"})
            if sim_patents:
                sim_patents1 = sim_patents[len(sim_patents)-1].find_all('div', {"class" : "doctable_row doctable_row_click"})
                for patent in sim_patents1:
                    sim_patents_text = patent.find_all('span', {"class" : "doctable_cell"})
                    pat_index = sim_patents_text[0].text
                    pat_date = sim_patents_text[1].text.replace('.', '')
                    similar_link = f"https://yandex.ru/patents/doc/{pat_index}_{pat_date}"
                    docs_string += similar_link + "\n"
            else:
                docs_string = ""

            row = [Id, title_text, abstract_text, index_text, mpk_string, date_text, contributor_string, description_string,
                   claim_string, docs_string]
            data = [row]
            client.insert('yandex_patents', data,
                          column_names=['Id', 'Title', 'Abstract', 'Index', 'IPC', 'Date_of_publication', 'Contributor',
                                        'Description', 'Claims', 'Similar_docs'], database="db_patents")
            Id += 1

