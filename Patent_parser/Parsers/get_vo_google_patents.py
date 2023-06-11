from Database.ClickhouseDB import ClickhouseDB
from bs4 import BeautifulSoup
from Parse_Methods.google_parser_struct import GoogleParser
from Parse_Methods.google_webdriver import GoogleWebDriver
from settings import CLICKHOUSE_HOST, CLICKHOUSE_USERNAME, CLICKHOUSE_PASSWORD
from Classes.Patent import Patent
import time


def main():
    db_client = ClickhouseDB(CLICKHOUSE_HOST, CLICKHOUSE_USERNAME, CLICKHOUSE_PASSWORD)  # Обяъвление объекта класса БД
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
            print('Аннотация:\n', abstract)

            # Получаем название патента
            title = patent.get_title()
            print('Название:\n', title)

            # Получаем дату публикации патента
            date_of_publication = patent.get_date_of_publication()
            print('Дата публикации:\n', date_of_publication)

            # Получаем авторов
            authors = patent.get_authors()
            print('Авторы:\n', authors)

            # Получаем индекс
            index = patent.get_index()

            # Получаем описание
            description = patent.get_description()

            # Получаем класс МПК
            ipc = patent.get_ipc()

            # Получаем формулу изобретения
            claims = patent.get_claims()

            # Получаем похожие документы
            sim_docs = patent.get_similar_patents()

            # Сохраняем запись в БД
            row = [Id, title, abstract, index, ipc, date_of_publication, authors,
                   description, claims, sim_docs]
            data = [row]
            db_client.insert_into_db(data, table_columns, db_client.database, db_client.db_google_patents)

            print(f'Патент №{Id} сохранен в БД')

            Id += 1

            # Задержка, чтобы избежать бана в сервисе
            time.sleep(10)

if __name__ == '__main__':
    main()
