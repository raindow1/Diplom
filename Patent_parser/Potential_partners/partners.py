from Potential_partners.ProblemComparison import ProblemComparison
from Database.ClickhouseDB import ClickhouseDB
from settings import CLICKHOUSE_HOST, CLICKHOUSE_USERNAME, CLICKHOUSE_PASSWORD


def main():

    # Объявление необходимых переменных
    Id = 1  # Идентификатор записи
    vo_patent_limit = 0  # Ограничение записей предприятий ВО
    ipc_patent_limit = 0  # Ограничение записей предприятий РФ и друж. стран

    db_client = ClickhouseDB(CLICKHOUSE_HOST, CLICKHOUSE_USERNAME, CLICKHOUSE_PASSWORD)  # Объект класса БД

    second_level_count = 0  # Количество найденных зависимых слов второго уровня
    third_level_count = 0  # Количество найденных зависимых слов третьего уровня
    vo_res_root = []  # Список с найденным сказуемым
    vo_res_nmod = []  # Список с найденными зависимыми словами второго уровня
    vo_third_nmod = []  # Список с найденными зависимыми словами третьего уровня
    first_level_k = 1  # Коэффициент сравнения первого уровня
    second_level_k = 1  # Коэффициент сравнения второго уровня
    third_level_k = 0  # Коэффициент сравнения третьего уровня
    final_k = 0  # Итоговый коэффициент сравнения

    partners = []  # Список найденных технологических партнеров

    # Колонки таблицы
    table_columns = ['Id', 'Organisation_name', 'IProblems', 'IPC_patent_id', "Match_ratio"]


    # Запрос данных о количестве записей
    vo_patent_count = db_client.count_data(db_client.database, db_client.db_yandex_structure)
    ipc_patent_count = db_client.count_data(db_client.database, db_client.db_ipc_structure)

    # Выбор записи ВО с которой начнется сравнение
    vo_row_selection = int(
        input('Выберите запись проблемы предприятия ВО, с которой начнется сравнение:\n'
              '->: '))

    if vo_row_selection < 1 or vo_row_selection > vo_patent_count:
        print('Ошибка: Некорректный id записи')
        exit(1)

    # Выбор записи патентов РФ и друж. стран с которой начнется сравнение
    ipc_row_selection = int(
        input('Выберите запись проблемы предприятий РФ и друж. стран, с которой начнется сравнение:\n'
              '->: '))

    if ipc_row_selection < 1 or ipc_row_selection > ipc_patent_count:
        print('Ошибка: Некорректный id записи')
        exit(1)

    # Необходимость ограничения
    limit_selection = int(
        input('Установить ограничение в кол-ве обрабатываемых записей?\n'
              '\t1. Нет;\n'
              '\t2. Да.\n'
              '->: '))

    if limit_selection == 1:
        vo_patent_limit = vo_patent_count
        ipc_patent_limit = ipc_patent_count
    elif limit_selection == 2:
        vo_data_limit = int(
            input('Установите ограничение проблем предприятий ВО:\n'
                  '->: '))
        vo_patent_limit = vo_row_selection + vo_data_limit
        ipc_data_limit = int(
            input('Установите ограничение проблем предприятий РФ и друж. стран:\n'
                  '->: '))
        ipc_patent_limit = ipc_row_selection + ipc_data_limit
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

    # Создание объекта класса сравнения проблем
    problems = ProblemComparison()

    # Процесс сравнения проблем
    for i in range(vo_row_selection, vo_patent_limit):
        # Получение предложения с проблемой
        vo_result = db_client.select_from_db(db_client.database, db_client.db_yandex_structure, ['Problem'], i)
        vo_problem = vo_result.result_rows[0][0]

        # Получение слов для сравнения
        vo_res_root = problems.get_structure(vo_problem)[0]
        vo_res_nmod = problems.get_structure(vo_problem)[1]
        vo_third_nmod = problems.get_structure(vo_problem)[2]

#i = 11 c = 50 - test data
        for c in range(ipc_row_selection, ipc_patent_limit):
            # Получение предложения с проблемой
            ipc_result = db_client.select_from_db(db_client.database, db_client.db_ipc_structure, ['Problem'], c)
            # Получение правопреемника
            ipc_asignee = db_client.select_from_db(db_client.database, db_client.db_ipc_patents,
                                                   ['Asignee'], c).result_rows[0][0]
            ipc_problem = ipc_result.result_rows[0][0]
            # Получение слов для сравнения
            ipc_res_root = problems.get_structure(ipc_problem)[0]
            ipc_res_nmod = problems.get_structure(ipc_problem)[1]
            ipc_third_nmod = problems.get_structure(ipc_problem)[2]

            # Сравнение слов по уровням
            # Сравнение сказуемых
            for root_key in vo_res_root:
                if root_key in ipc_res_root:
                    # Повышение коэффициента при успешном сходстве
                    first_level_k *= 3
            if first_level_k == 3:
                # Сравнение зависимых слов второго уровня
                for nmod_key in vo_res_nmod:
                    if nmod_key in ipc_res_nmod:
                        second_level_count += 1
                if second_level_count > 0:
                    # Повышение коэффициента при успешном сходстве
                    second_level_k *= 2
                    # Сравнение зависимых слов третьего уровня
                    for third_nmod_key in vo_third_nmod:
                        if third_nmod_key in ipc_third_nmod:
                            third_level_count += 1
                    match third_level_count:
                        case 1:
                            # Повышение коэффициента при успешном сходстве одного слова
                            third_level_k = 0.5
                        case 2:
                            # Повышение коэффициента при успешном сходстве двух слов
                            third_level_k = 0.75
                        case 3:
                            # Повышение коэффициента при успешном сходстве трех слов
                            third_level_k = 1

            # Расчет итогового коэффиента по формуле
            final_k = (first_level_k + second_level_k + third_level_k) / 6

            # Запись предприятия в партнеры при нужном значении итогового коэффициента сравнения
            if final_k > 0.9 and ipc_asignee not in partners:
                partners.append(ipc_asignee)
                print('Решаемая проблема предприятия ВО:\n', vo_problem[0])
                print('Найденная организация-партнер:\n', ipc_asignee)
                print('Решаемая проблема организации-партнера:\n', ipc_problem[0])
                print(f'Id патента:{c}\n')
                if db_check == 1:
                    row = [Id, ipc_asignee, ipc_problem, c, final_k]
                    data = [row]
                    db_client.insert_into_db(data, table_columns, db_client.database, db_client.db_potential_partners)
                    Id += 1

            # Обнуление необходимых счетчиков
            second_level_count = 0
            third_level_count = 0
            first_level_k = 1
            second_level_k = 1
            third_level_k = 0
            final_k = 0








if __name__ == "__main__":
    main()

