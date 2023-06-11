from Database.ClickhouseDB import ClickhouseDB
from Translation.PatentTranslator import PatentTranslator
from settings import CLICKHOUSE_HOST,CLICKHOUSE_PASSWORD,CLICKHOUSE_USERNAME

def main():

    # Объявление необходимых переменных
    max_chunk_size = 4000  # Максимальный размер фрагментов текста (символы)
    trans = PatentTranslator()  # Объявление объекта класса переводчика
    db_client = ClickhouseDB(CLICKHOUSE_HOST, CLICKHOUSE_USERNAME, CLICKHOUSE_PASSWORD)  # Объявление объекта класса БД
    table_columns = ['Id', 'Abstract', 'Description', 'Patent_id', 'Solution']  # колонки таблицы

    # Получение данных о количестве записей
    patent_count = db_client.count_data(db_client.database, db_client.db_ipc_patents)

    # Выбор записи с которой начнется перевод
    row_selection = int(
        input('Выберите запись, с которой начнется перевод:\n'
              '->: '))

    Id = row_selection

    if row_selection < 1 or row_selection > patent_count:
        print('Ошибка: Некорректный id записи')
        exit(1)

    # Перевод текстовых полей
    for i in range(row_selection, patent_count):
        # Получение необходимых данных
        index = db_client.select_from_db(db_client.database, db_client.db_ipc_patents, ["Index"], Id).result_rows[0][0]
        result = db_client.select_from_db(db_client.database, db_client.db_ipc_patents, ["Description", "Abstract"], Id)
        solution = db_client.select_from_db(db_client.database, db_client.db_ipc_patents, ["Title"], Id).result_rows[0][0]
        description = result.result_rows[0][0]
        abstract = result.result_rows[0][1]
        # Проверка на англоязычный патент
        if 'RU' not in index:
            # Перевод текстовых полей
            translated_solution = trans.translate_text(solution, max_chunk_size)
            print('Название:\n', translated_solution)
            translated_description = trans.translate_text(description, max_chunk_size)
            print('Описание:\n', translated_description)
            translated_abstract = trans.translate_text(abstract, max_chunk_size)
            print('Аннотация:\n', translated_abstract)

            # Сохранение текстовых полей в БД
            row = [Id, translated_abstract, translated_description, i, translated_solution]
            data = [row]
            db_client.insert_into_db(data, table_columns, db_client.database, db_client.db_transd_patents)

            print(f'Патент #{i} успешно переведен')

        else:
            # Сохранение текстовых полей на русском языке без изменений
            row = [Id, abstract, description, i, solution]
            data = [row]
            db_client.insert_into_db(data, table_columns, db_client.database, db_client.db_transd_patents)

        Id += 1


if __name__ == "__main__":
    main()
