import time
from Database.ClickhouseDB import ClickhouseDB
from Parse_Methods.google_parser_struct import GoogleParser
from Parse_Methods.google_webdriver import GoogleWebDriver
from Classes.Patent import Patent
from settings import CLICKHOUSE_HOST, CLICKHOUSE_USERNAME, CLICKHOUSE_PASSWORD
import pandas as pd


def main():
    # Объявление объекта класса БД
    db_client = ClickhouseDB(CLICKHOUSE_HOST, CLICKHOUSE_USERNAME, CLICKHOUSE_PASSWORD)
    google_driver = GoogleWebDriver()  # Объявление объекта класса драйвера
    google_parser = GoogleParser(google_driver)  # Объявление объекта класса парсера

    # Колонки таблицы для заполнения
    table_columns = ['Id', 'Title', 'Abstract', 'Index', 'Asignee', 'Authors', 'IPC',
                     'Date_of_publication', 'Description', 'Claims', 'Similar_docs']

    # Идентификатор сохраняемой записи
    Id = 1

    # Список с ссылками на страницы с патентами
    patent_links = []

    # Получаем список ссылок на патентные документы
    data = pd.read_csv('../Data/IPC_patents.csv')['result link'].tolist()
    for link in data:
        if 'RU' in str(link):
            link = link.replace("/en", "/ru")
        patent_links.append(str(link))

    for patent_link in patent_links:
        patent = Patent(patent_link, google_parser)

        # Получаем аннотацию патента
        abstract = patent.get_abstract()
        print('Аннотация:\n', abstract)

        # Получаем название патента
        title = patent.get_title()
        print('Название:\n', title)

        # Получаем дату публикации патента
        date_of_publication = patent.get_date_of_publication()
        print('Дата публикации:\n', date_of_publication)

        # Получаем правопреемника
        asignee = patent.get_assignee()
        print('Правопреемник:\n', asignee)

        # Получаем авторов
        authors = patent.get_authors()

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
        row = [Id, title, abstract, index, asignee, authors, ipc, date_of_publication,
               description, claims, sim_docs]
        data = [row]
        db_client.insert_into_db(data, table_columns, db_client.database, db_client.db_ipc_patents)

        print(f'Патент №{Id} сохранен в БД')

        Id += 1


        # Задержка, чтобы избежать бана в сервисе
        time.sleep(10)


if __name__ == '__main__':
    main()
