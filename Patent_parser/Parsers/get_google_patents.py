import requests
import time
from bs4 import BeautifulSoup
from database import client
from Methods.google_parser_struct import GoogleParser
from Methods.yandex_parser_struct import YandexParser
from Methods.google_webdriver import GoogleWebDriver
from Methods.yandex_webdriver import YandexWebDriver
from Classes.Patent import Patent
import os




def main():
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
    google_driver = GoogleWebDriver()
    google_parser = GoogleParser(google_driver)

    Id = 1

    with open("organisations.csv", encoding='UTF8') as f:
        organisations = [row.replace("\n", "") for row in f]
        organisations.pop(0)

    for organisation in organisations:
        url = f"https://patents.google.com/?assignee={organisation}&language=RUSSIAN&num=100"
        page = google_driver.get_patent_html(url)
        org = BeautifulSoup(page, 'html.parser')

        root = org.find_all("state-modifier", {"class": "result-title style-scope search-result-item"})
        for each_tag in root:
            link = each_tag["data-result"]
            parse_link = 'https://patents.google.com/' + link


            patent = Patent(parse_link, google_parser)

            #Abstract
            abstract = patent.get_abstract()

            #Title
            title = patent.get_title()

            #Date of publication
            date_of_publication = patent.get_date_of_publication()

            #Asignee
            asignee = patent.get_assignee()

            #Authors
            authors = patent.get_authors()

            #Description
            description = patent.get_description()

            #IPC
            ipc = patent.get_ipc()

            #Claims
            claims = patent.get_claims()

            #Similar_docs
            sim_docs = patent.get_similar_patents()

            row = [Id, title, abstract, asignee, authors, ipc, date_of_publication,
                   description, claims, sim_docs]
            data = [row]
            client.insert('IPC_google_patents', data,
                          column_names=['Id', 'Title', 'Abstract', 'Index', 'Asignee', 'Authors', 'IPC',
                                        'Date_of_publication', 'Description', 'Claims', 'Similar_docs'],
                          database="db_patents")
            Id += 1


if __name__ == '__main__':
    main()
