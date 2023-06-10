import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from Database.database import client
import pandas as pd




# configure web driver
chrome_options = Options()
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--no-sandbox")
chrome_options.headless = True     # use background mode
driver = webdriver.Chrome("chromedriver.exe", chrome_options=chrome_options)

Id = 1

with open("../Data/organisations.csv", encoding='UTF8') as f:
    organisations = [row.replace("\n","") for row in f]
    organisations.pop(0)

patent_links = []
data = pd.read_csv('../Data/IPC_patents.csv')['result link'].tolist()
for link in data:
    if 'RU' in str(link):
        link = link.replace("/en","/ru")
    patent_links.append(str(link))


for patent_link in patent_links:
    url = patent_link
    driver.get(url)
    time.sleep(5)
    page = driver.page_source
    soup = BeautifulSoup(page, 'html.parser')



    #Abstact
    abstract = soup.find('meta', attrs={'name':'description'})
    if abstract:
        abstract_text = abstract["content"]
    else:
        abstract_text = ""

    #Title
    title = soup.find('meta', attrs={'name':'DC.title'})
    title_text = title["content"]



    #Asignee
    asignee = soup.select_one('[data-assignee]')['data-assignee']


    #Authors
    authors_list = []
    for data_inventor in soup.select('[data-inventor]'):
        authors = data_inventor['data-inventor']
        authors_list.append(authors)

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
    docs_list = []
    docs = soup.find_all("div", {"class":"tbody style-scope patent-result"})
    table = docs[1].find_all("state-modifier", {"class" : "style-scope patent-result"})
    for doc in table:
        link = doc["data-result"]
        similar_link = f"https://patents.google.com/{link}"
        docs_list.append(similar_link)


    row = [Id, title_text, abstract_text, index_text,asignee,authors_list, mpk_string, date_text, description_string, claim_string, docs_list]
    data = [row]
    client.insert('IPC_google_patents', data, column_names=['Id','Title', 'Abstract', 'Index', 'Asignee', 'Authors', 'IPC', 'Date_of_publication', 'Description', 'Claims','Similar_docs'], database = "db_patents")
    Id += 1


driver.quit()
