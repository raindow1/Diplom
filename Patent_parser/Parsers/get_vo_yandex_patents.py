from Database.ClickhouseDB import ClickhouseDB
from bs4 import BeautifulSoup
from Methods.yandex_parser_struct import YandexParser
from Methods.yandex_webdriver import YandexWebDriver
from Classes.Patent import Patent
import time


def main():
    client = ClickhouseDB()  # Обяъвление объекта класса БД
    yandex_driver = YandexWebDriver()  # Обяъвление объекта класса драйвера
    yandex_parser = YandexParser(yandex_driver)  # Обяъвление объекта класса парсера

    # Колонки таблицы для заполнения
    table_columns = ['Id', 'Title', 'Abstract', 'Index', 'IPC', 'Contributor'
                     'Date_of_publication', 'Description', 'Claims', 'Similar_docs']

    # Идентификатор сохраняемой записи
    Id = 1


    # Получаем список ссылок на патентные документы
    with open("../Data/organisations.csv", encoding='UTF8') as f:
        organisations = [row.replace("\n", "") for row in f]
        organisations.pop(0)

    for organisation in organisations:

        url = f"https://yandex.ru/patents?dco=RU&dco=SU&dl=ru&dt=0&dty=1&dty=2&s=0&sp=0&spp=50&st=0&text={organisation}"
        page = yandex_driver.get_patent_html(url)
        soup = BeautifulSoup(page, 'html.parser')

        pages = soup.find('div', {"class": "leaf-button leaf-button--last"})
        if pages:
            page = int(pages.text)
        else:
            page = 1

        for i in range(page - 1):
            url = f"https://yandex.ru/patents?dco=RU&dl=ru&dt=0&dty=1&dty=2&s=0&sp={i}&spp=50&st=0&text={organisation}"
            page = yandex_driver.get_patent_html(url)
            soup = BeautifulSoup(page, 'html.parser')

            # Links
            links = soup.find_all('a', {"class": "snippet-title"})

            for link in links:
                parse_link = "https://yandex.ru" + link['href']
                patent = Patent(parse_link, yandex_parser)

                # Получаем аннотацию патента
                abstract = patent.get_abstract()
                print(abstract)

                # Получаем название патента
                title = patent.get_title()
                print(title)

                # Получаем дату публикации патента
                date_of_publication = patent.get_date_of_publication()
                print(date_of_publication)

                # Получаем авторов
                authors = patent.get_authors()
                print(authors)

                # Получаем индекс
                index = patent.get_index()
                print(index)

                # Получаем описание
                description = patent.get_description()
                print(description)

                # Получаем класс МПК
                ipc = patent.get_ipc()
                print(ipc)

                # Получаем формулу изобретения
                claims = patent.get_claims()
                print(claims)

                # Получаем похожие документы
                sim_docs = patent.get_similar_patents()
                print(sim_docs)

                # Сохраняем запись в БД
                row = [Id, title, abstract, index, ipc, date_of_publication, authors,
                       description, claims, sim_docs]
                data = [row]
                client.insert_into_db(data, table_columns, client.database, client.db_yandex_patents)
                Id += 1

                # Задержка, чтобы избежать бана в сервисе
                time.sleep(10)

if __name__ == '__main__':
    main()
