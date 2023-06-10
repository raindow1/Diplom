from abc import ABC, abstractmethod

from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class WebDriver(ABC):
    def __init__(self) -> None:
        """
        Создать вебдрайвер
        """
        chrome_options = Options()
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.headless = True  # use background mode
        self._driver = webdriver.Chrome("chromedriver.exe", chrome_options=chrome_options)

    @abstractmethod
    def get_patent_html(self, patent_link: str) -> str:
        """
        Получить html-верстку страницы патента
        return: html-верстка с сайта
        """
        pass

    def quit(self):
        self._driver.quit()
