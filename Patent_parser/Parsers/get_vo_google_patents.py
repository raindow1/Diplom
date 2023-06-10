from Database.ClickhouseDB import ClickhouseDB
from bs4 import BeautifulSoup
from Methods.google_parser_struct import GoogleParser
from Methods.google_webdriver import GoogleWebDriver
from Classes.Patent import Patent
import time


def main():
    client = ClickhouseDB()  # Обяъвление объекта класса БД
    google_driver = GoogleWebDriver()  # Обяъвление объекта класса драйвера
    google_parser = GoogleParser(google_driver)  # Обяъвление объекта класса парсера

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
        url = f"https://patents.google.com/?assignee={organisation}&language=RUSSIAN&num=100"
        page = google_driver.get_patent_html(url)
        org = BeautifulSoup(page, 'html.parser')

        root = org.find_all("state-modifier", {"class": "result-title style-scope search-result-item"})
        for each_tag in root:
            link = each_tag["data-result"]
            parse_link = 'https://patents.google.com/' + link
            patent = Patent(parse_link, google_parser)

            # Получаем аннотацию патента
            abstract = patent.get_abstract()
            print(abstract)

            # Получаем название патента
            title = patent.get_title()
            print(title)

            # Получаем дату публикации патента
            date_of_publication = patent.get_date_of_publication()
            print(date_of_publication)

            # Получаем правопреемника
            asignee = patent.get_assignee()
            print(asignee)

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
            client.insert_into_db(data, table_columns, client.database, client.db_google_patents)
            Id += 1

            # Задержка, чтобы избежать бана в сервисе
            time.sleep(10)

if __name__ == '__main__':
    main()
