import time

from Classes.WebDriver import WebDriver


class YandexWebDriver(WebDriver):
    def __init__(self) -> None:
        super().__init__()

    def get_patent_html(self, link: str) -> str:
        self._driver.get(link)
        time.sleep(5)
        return self._driver.page_source

    def get_search_patents(self, link) -> str:
        self._driver.get(link)
        time.sleep(5)
        return self._driver.page_source
