from Database.ClickhouseDB import ClickhouseDB
from Translation.PatentTranslator import PatentTranslator
from settings import CLICKHOUSE_HOST,CLICKHOUSE_PASSWORD,CLICKHOUSE_USERNAME

def main():

    # Объявление необходимых переменных
    max_chunk_size = 4000  # Максимальный размер фрагментов текста (символы)
    trans = PatentTranslator()  # Объявление объекта класса переводчика
    db_client = ClickhouseDB(CLICKHOUSE_HOST, CLICKHOUSE_USERNAME, CLICKHOUSE_PASSWORD)  # Объявление объекта класса БД
    table_columns = ['Id', 'Abstract', 'Description', 'Patent_id', 'Solution']  # колонки таблицы
    patent_limit = 0  # Ограничение записей

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

    # Необходимость ограничения
    limit_selection = int(
        input('Установить ограничение в кол-ве обрабатываемых записей?\n'
              '\t1. Нет;\n'
              '\t2. Да.\n'
              '->: '))

    if limit_selection == 1:
        patent_limit = patent_count
    elif limit_selection == 2:
        data_limit = int(
            input('Установите ограничение:\n'
                  '->: '))
        patent_limit = row_selection + data_limit
    else:
        print('Некорректные входные данные')

    # Необходимость записи в БД
    db_save_selection = int(
        input('Производить запись в БД?\n'
              '\t1. Нет;\n'
              '\t2. Да.\n'
              '->: '))

    if db_save_selection == 1:
        db_check = 0
    elif db_save_selection == 2:
        db_check = 1
    else:
        print('Некорректные входные данные')
        exit(1)

    # Перевод текстовых полей
    for i in range(row_selection, patent_limit):
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
            if db_check == 1:
                row = [Id, translated_abstract, translated_description, i, translated_solution]
                data = [row]
                db_client.insert_into_db(data, table_columns, db_client.database, db_client.db_transd_patents)

            print(f'Патент #{i} успешно переведен')

        else:
            # Сохранение текстовых полей на русском языке без изменений
            if db_check == 1:
                row = [Id, abstract, description, i, solution]
                data = [row]
                db_client.insert_into_db(data, table_columns, db_client.database, db_client.db_transd_patents)

        Id += 1


if __name__ == "__main__":
    main()
