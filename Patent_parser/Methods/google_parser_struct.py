from bs4 import BeautifulSoup
from Classes.WebDriver import WebDriver
from Classes.Parser import Parser


class GoogleParser(Parser):
    def __init__(self, google_web_driver: WebDriver) -> None:
        self.__soup: BeautifulSoup = None
        self.__google_web_driver = google_web_driver

    def get_patent_link(self, link: str) -> None:
        page = self.__google_web_driver.get_patent_html(link)
        self.__soup = BeautifulSoup(page, 'html.parser')

    def get_organisation_links(self, link: str) -> None:
        """
        Получить ссылки на патенты организации
        """
        raise NotImplementedError

    def get_title(self) -> str:
        return self.__soup.find('h1', {'id': 'title'}).text

    def get_assignee(self) -> str:
        return self.__soup.select_one('[data-assignee]')['data-assignee']

    def get_authors(self) -> str:
        inventors = ""
        for data_inventor in self.__soup.select('[data-inventor]'):
            inventors = data_inventor['data-inventor'] + "\n"

        return inventors

    def get_index(self) -> str:
        index = self.__soup.find('h2', attrs={'id': 'pubnum'})
        if index:
            index_text = index.text
        else:
            index_text = ""

        return index_text

    def get_date_of_publication(self) -> str:
        return  self.__soup.find('div', attrs={'class':'publication style-scope application-timeline'}).text

    def get_abstract(self) -> str:
        return self.__soup.find('patent-text', {'name': 'abstract'}).text

    def get_description(self) -> str:
        return self.__soup.find('patent-text', {'name': 'description'}).text

    def get_claims(self) -> str:
        return self.__soup.find('patent-text', {'name': 'claims'}).text

    def get_ipc(self) -> str:
        mpk_string = ""
        for ipc in self.__soup.find_all('div', {'class': 'classification-tree', 'hidden': False})[3::4]:
            mpk = ipc.find_all('a', {'id': 'link'})[-1].text
            mpk_string += mpk + "\n"

        return mpk_string

    def get_similar_patents(self) -> str:
        docs_string = ""
        docs = self.__soup.find_all("div", {"class": "tbody style-scope patent-result"})
        table = docs[1].find_all("state-modifier", {"class": "style-scope patent-result"})
        for doc in table:
            link = doc["data-result"]
            similar_link = f"https://patents.google.com/{link}"
            docs_string += similar_link + "\n"

        return docs_string

