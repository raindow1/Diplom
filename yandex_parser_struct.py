from typing import List, Dict, Union

from bs4 import BeautifulSoup

from Classes.WebDriver import WebDriver
from Classes.Parser import Parser


class YandexParser(Parser):
    def __init__(self, yandex_web_driver: WebDriver) -> None:
        self.__soup: BeautifulSoup = None
        self.__yandex_web_driver = yandex_web_driver

    def get_patent_link(self, link: str) -> None:
        page = self.__yandex_web_driver.get_patent_html(link)
        self.__soup = BeautifulSoup(page, 'html.parser')

    def get_title(self) -> str:
        return self.__soup.find('div', {"class" : "document-title document-title__desktop"}).text

    def get_assignee(self) -> str:
        return self.__soup.find_all(lambda tag: 'Патентообладатели:' in tag.text).pop().next_sibling.text

    def get_authors(self) -> str:
        return self.__soup.find_all(lambda tag: 'Авторы:' in tag.text).pop().next_sibling.text

    def get_date_of_publication(self) -> str:
        date = self.__soup.find_all('span', {"class": "doc-summary-item__value"})
        date_text = date[3].text

        return date_text

    def get_abstract(self) -> str:
        abstract_text = ""
        abstract = self.__soup.find('div', {"id": "doc-abstract"})
        if abstract:
            abstract_text = abstract.find_next_sibling('div').text

        return abstract_text

    def get_description(self) -> str:
        description_text = ""
        description = self.__soup.find('div', {"id": "doc-description"})
        if description:
            description_text = description.find_next_sibling('div').text

        return description_text

    def get_claims(self) -> str:
        claim_text = ""
        claim = self.__soup.find('div', {"id": "doc-claims"})
        if claim:
            claim_text = claim.find_next_sibling('div').text

        return claim_text

    def get_ipc(self) -> str:
        mpk_string = ""
        mpk = self.__soup.find_all('div', {"class": "header-mpk-item"})
        for mpk_part in mpk:
            if mpk_part.text != "МПК":
                mpk_text = mpk_part.text.split("(")
                mpk_string += mpk_text[0] + "\n"

        return mpk_string

    def get_similar_patents(self) -> str:
        docs_string = ""
        sim_patents = self.__soup.find_all('div', {"class": "doctable_rows"})
        if sim_patents:
            sim_patents1 = sim_patents[len(sim_patents) - 1].find_all('div',
                                                                      {"class": "doctable_row doctable_row_click"})
            for patent in sim_patents1:
                sim_patents_text = patent.find_all('span', {"class": "doctable_cell"})
                pat_index = sim_patents_text[0].text
                pat_date = sim_patents_text[1].text.replace('.', '')
                similar_link = f"https://yandex.ru/patents/doc/{pat_index}_{pat_date}"
                docs_string += similar_link + "\n"
        else:
            docs_string = ""

        return docs_string

