from Potential_partners.ProblemComparison import ProblemComparison
from Database.ClickhouseDB import ClickhouseDB
from settings import CLICKHOUSE_HOST, CLICKHOUSE_USERNAME, CLICKHOUSE_PASSWORD


def patent_filter() -> tuple:
    """
    Отфильтровать патенты по языку
    :return списки с Id русских и иностранных патентов
    """
    # Создание объекта класса БД
    db_client = ClickhouseDB(CLICKHOUSE_HOST, CLICKHOUSE_USERNAME, CLICKHOUSE_PASSWORD)
    # Получение данных о количестве патентов
    patent_count = db_client.count_data(db_client.database,db_client.db_ipc_patents)
    # Объявление списков
    rus_patents = []
    in_patents = []
    # Фильрация патентов
    for i in range(1, patent_count):
        patent_index = db_client.select_from_db(db_client.database,
                                                db_client.db_ipc_patents, ['Index'], i).result_rows[0][0]
        if 'RU' in patent_index:
            rus_patents.append(i)
        else:
            in_patents.append(i)

    return rus_patents, in_patents


def main():

    # Объявление необходимых переменных
    temp_Id = 980  # Id временной записи
    Id = 1  # Id записи
    count = 0

    ru_res_root = []  # Список с найденным сказуемым
    ru_res_nmod = []  # Список с найденными зависимыми словами второго уровня
    ru_third_nmod = []  # Список с найденными зависимыми словами третьего уровня
    rus_patents = patent_filter()[0]  # Список с Id русскоязычных патентов
    in_patents = patent_filter()[1]  # Список с Id англоязычных патентов
    db_client = ClickhouseDB(CLICKHOUSE_HOST, CLICKHOUSE_USERNAME, CLICKHOUSE_PASSWORD)  # Объект класса БД

    second_level_count = 0  # Количество найденных зависимых слов второго уровня
    third_level_count = 0  # Количество найденных зависимых слов третьего уровня
    first_level_k = 1  # Коэффициент сравнения первого уровня
    second_level_k = 1  # Коэффициент сравнения второго уровня
    third_level_k = 0  # Коэффициент сравнения третьего уровня
    final_k = 0  # Итоговый коэффициент сравнения

    table_columns = ['Id', 'Problem']  # Колонки таблицы

    tech_vacuum = []  # Временный массив тех. вакуума
    final_tech_vacuum = []  # Массив тех. вакуума

    # Получение данных о количестве записей
    ipc_patent_count = db_client.count_data(db_client.database, db_client.db_ipc_structure)

    # Выбор записи проблемы РФ с которой начнется сравнение
    ru_row_selection = int(
        input('Выберите запись проблемы предприятия ВО, с которой начнется сравнение:\n'
              '->: '))

    if ru_row_selection < 1 or ru_row_selection > ipc_patent_count:
        print('Ошибка: Некорректный id записи')
        exit(1)

    # Выбор записи иностранной проблемы с которой начнется сравнение
    en_row_selection = int(
        input('Выберите запись проблемы предприятий РФ и друж. стран, с которой начнется сравнение:\n'
              '->: '))

    if en_row_selection < 1 or en_row_selection > ipc_patent_count:
        print('Ошибка: Некорректный id записи')
        exit(1)

    # Создание объекта класса сравнения проблем
    problems = ProblemComparison()

    for i in range(ru_row_selection, ipc_patent_count):
        # Проверка на русскоязычный патент
        if i in rus_patents:
            # Получение предложения с проблемой
            ru_result = db_client.select_from_db(db_client.database, db_client.db_ipc_structure, ["Problem"], i)
            ru_problem = ru_result.result_rows[0][0]
            # Получение слов для сравнения
            ru_res_root = problems.get_structure(ru_problem)[0]
            ru_res_nmod = problems.get_structure(ru_problem)[1]
            ru_third_nmod = problems.get_structure(ru_problem)[2]

            # print(VO_res_root)
            # print(VO_res_nmod)
            # print(VO_third_nmod)

        for c in range(en_row_selection, ipc_patent_count):
            # Проверка на англоязычный патент
            if c in in_patents:
                # Получение предложения с проблемой
                en_result = db_client.select_from_db(db_client.database, db_client.db_ipc_structure, ["Problem"], c)
                en_problem = en_result.result_rows[0][0]
                # Получение слов для сравнения
                en_res_root = problems.get_structure(en_problem)[0]
                en_res_nmod = problems.get_structure(en_problem)[1]
                en_third_nmod = problems.get_structure(en_problem)[2]
                # Получение временного тех. вакуума
                result_probs = db_client.select_all_from_db(db_client.database, db_client.db_temp_tech_vacuum, ["Problem"])
                for k in range(1, len(result_probs.result_rows)):
                    tech_vacuum.append(result_probs.result_rows[k][0])

                # print(IPC_res_root)
                # print(IPC_res_nmod)
                # print(IPC_third_nmod)

                # Сравнение слов по уровням
                # Сравнение сказуемых
                for root_key in ru_res_root:
                    if root_key in en_res_root:
                        # Повышение коэффициента при успешном сходстве
                        first_level_k *= 3
                if first_level_k == 3:
                    # Сравнение зависимых слов второго уровня
                    for nmod_key in ru_res_nmod:
                        if nmod_key in en_res_nmod:
                            second_level_count += 1
                    if second_level_count > 0:
                        # Повышение коэффициента при успешном сходстве
                        first_level_k *= 2
                        # Сравнение зависимых слов третьего уровня
                        for third_nmod_key in ru_third_nmod:
                            if third_nmod_key in en_third_nmod:
                                third_level_count += 1
                        match third_level_count:
                            case 1:
                                # Повышение коэффициента при успешном сходстве одного слова
                                third_level_k *= 0.5
                            case 2:
                                # Повышение коэффициента при успешном сходстве двух слов
                                third_level_k *= 0.75
                            case 3:
                                # Повышение коэффициента при успешном сходстве трех слов
                                third_level_k = 1

                # Расчет итогового коэффиента по формуле
                final_k = (first_level_k + second_level_k + third_level_k) / 6

                # Проверка на отсутствие сходства
                if final_k < 0.9:
                    if len(en_problem) != 0:
                        # Проверка на отсутствие в тех. вакууме
                        if en_problem[0] not in tech_vacuum:
                            # Запись во временный тех. вакуум
                            tech_vacuum.append(en_problem[0])
                            row = [temp_Id, en_problem[0]]
                            data = [row]
                            db_client.insert_into_db(data, table_columns, db_client.database, db_client.db_temp_tech_vacuum)
                            temp_Id += 1
                elif len(en_problem) != 0:
                    # Проверка на наличие в тех. вакууме
                    if en_problem[0] in tech_vacuum:
                        # Удаление из тех. вакуума
                        db_client.client.command("SET allow_experimental_lightweight_delete = true")
                        db_client.delete_from_db(db_client.database, db_client.db_temp_tech_vacuum, c)

                # Обнуление необходимых счетчиков и переменных
                second_level_count = 0
                third_level_count = 0
                first_level_k = 1
                second_level_k = 1
                third_level_k = 0
                final_k = 0
                tech_vacuum.clear()

                print(f'analyzed patent #{i}')
                print(f'analyzed patent #{c}')

    # Формирование итогового тех. вакуума
    final_result_probs = db_client.select_all_from_db(db_client.database, db_client.db_temp_tech_vacuum, ["Problem"])
    for f in range(1, len(final_result_probs.result_rows)):
        final_tech_vacuum.append(final_result_probs.result_rows[f][0])

    for problem in final_tech_vacuum:
        row = [Id, problem]
        data = [row]
        db_client.insert_into_db(data, table_columns, db_client.database, db_client.db_tech_vacuum)
        Id += 1


#26 patent




if __name__ == "__main__":
    main()

