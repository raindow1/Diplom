from Database.ClickhouseDB import ClickhouseDB
from Problem_Solution.ProblemSolutionExtractor import ProblemSolutionExtractor
from settings import CLICKHOUSE_HOST, CLICKHOUSE_USERNAME, CLICKHOUSE_PASSWORD


def main():

    # Объявление необходимых переменных
    Id = 1  # Идентификатор записи
    # Объявление объекта класса БД
    db_client = ClickhouseDB(CLICKHOUSE_HOST, CLICKHOUSE_USERNAME, CLICKHOUSE_PASSWORD)
    table_columns = ['Id', 'Problem', 'Solution', 'Patent_id']  # колонки таблицы
    patent_limit = 0  # Ограничение анализируемых записей

    # Выбор таблицы для проведения анализа проблем
    service_selection = int(
        input('Выберите таблицу, анализ патентов которой будет производится:\n'
              '\t1. Яндекс Патенты(Предприятия ВО);\n'
              '\t2. Google Patents(Предприятия ВО);\n'
              '\t3. Google Patents(Предприятия РФ и дружественных стран).\n'
              '->: '))

    # Получение данных о количестве записей
    if service_selection == 1:
        patent_count = db_client.count_data(db_client.database, db_client.db_yandex_patents)
    elif service_selection == 2:
        patent_count = db_client.count_data(db_client.database, db_client.db_google_patents)
    elif service_selection == 3:
        patent_count = db_client.count_data(db_client.database, db_client.db_transd_patents)
    else:
        print('Входные данные некорректны.')
        exit(1)

    # Выбор записи патента, с которой начнется анализ
    start_selection = int(
        input('Выберите запись патента, с которой начнется анализ:\n'
              '->: '))

    if start_selection < 1 or start_selection > patent_count:
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
        patent_limit = start_selection + data_limit
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

    # Выделение структуры "Проблема-Решение"
    for i in range(start_selection, patent_limit):
        # Получение необходимых текстовых полей
        if service_selection == 1:
            result = db_client.select_from_db(db_client.database, db_client.db_yandex_patents,
                                              ['Description', 'Abstract'], i)
            solution = db_client.select_from_db(db_client.database, db_client.db_yandex_patents,
                                              ['Title'], i).result_rows[0][0]
            description = result.result_rows[0][0]
            abstract = result.result_rows[0][1]
        elif service_selection == 2:
            result = db_client.select_from_db(db_client.database, db_client.db_google_patents,
                                              ['Description', 'Abstract'], i)
            solution = db_client.select_from_db(db_client.database, db_client.db_google_patents,
                                                ['Title'], i).result_rows[0][0]
            description = result.result_rows[0][0]
            abstract = result.result_rows[0][1]
        else:
            result = db_client.select_from_db(db_client.database, db_client.db_transd_patents,
                                              ['Description', 'Abstract'], i)
            solution = db_client.select_from_db(db_client.database, db_client.db_transd_patents,
                                                ['Solution'], i).result_rows[0][0]
            description = result.result_rows[0][0]
            abstract = result.result_rows[0][1]

        # Объявление объекта класса ProblemSolutionExtractor
        structure = ProblemSolutionExtractor()
        # Нахождение предложения с проблемой
        problems = structure.get_problem(description, abstract)

        # Запись найденной структуры в БД
        if db_check == 1:
            row = [Id, problems[0], solution, i]
            data = [row]
            if service_selection == 1:
                db_client.insert_into_db(data, table_columns, db_client.database, db_client.db_yandex_structure)
            elif service_selection == 2:
                db_client.insert_into_db(data, table_columns, db_client.database, db_client.db_google_structure)
            else:
                db_client.insert_into_db(data, table_columns, db_client.database, db_client.db_ipc_structure)

        print(f'Патент №{i}')
        print('Проблема:\n', problems)
        print('Решение:\n', solution)

        Id += 1



if __name__ == "__main__":
    main()