from typing import List
import clickhouse_connect


class ClickhouseDB:
    def __init__(self, host: str, username: str, password: str) -> None:
        self._client = clickhouse_connect.get_client(host=host,
                                                     username=username,
                                                     password=password)
        self.database = "db_patents"
        self.db_yandex_patents = "yandex_patents"
        self.db_google_patents = "google_patents"
        self.db_ipc_patents = "IPC_google_patents"
        self.db_yandex_structure = "yandex_problem_solution"
        self.db_google_structure = "google_problem_solution"
        self.db_potential_partners = "Potential_partners"
        self.db_tech_vacuum = "tech_vacuum"
        self.db_temp_tech_vacuum = "temp_tech_vacuum"
        self.db_transd_patents = "translated_IPC_patents"
        self.db_ipc_structure = "IPC_problem_solution"

    def insert_into_db(self, data: List, table_columns: List, db_name: str, db_table: str) -> None:
        """
        Добавить запись в таблицу БД
        :param data: данные для сохранения
        :param table_columns: кололнки таблицы
        :param db_name: наименование БД
        :param db_table: наименование таблицы в БД
        :return запрос INSERT в БД
        """
        return self._client.insert(db_table, data,
                      column_names=table_columns,
                      database=db_name)

    def count_data(self, db_name: str, db_table: str) -> int:
        """
        Посчитать количество записей в таблице БД
        :param db_name: наименование БД
        :param db_table: наименование таблицы в БД
        :return запрос SELECT count() в БД
        """
        return self._client.query(f'SELECT'
                                  f' count() '
                                  f'FROM '
                                  f'{db_name}.{db_table}').result_rows[0][0]

    def delete_from_db(self, db_name: str, db_table: str, row_id: int) -> None:
        """
        Удалить запись по определенному Id из таблицы БД
        :param db_name: наименование БД
        :param db_table: наименование таблицы в БД
        :param row_id: Id записи
        :return запрос DELETE в БД
        """
        return self._client.query(f'DELETE '
                                  f'FROM '
                                  f'{db_name}.{db_table} '
                                  f'WHERE '
                                  f'Id ={row_id}')

    def delete_all_from_db(self, db_name: str, db_table: str) -> None:
        """
        Удалить все записи из таблицы БД
        :param db_name: наименование БД
        :param db_table: наименование таблицы в БД
        :return запрос DELETE в БД
        """
        return self._client.query(f'DELETE'
                                  f' FROM '
                                  f'{db_name}.{db_table}')

    def select_from_db(self, db_name: str, db_table: str, db_columns: List, row_id: int):
        """
        Выборка записей из БД
        :param db_name: наименование БД
        :param db_table: наименование таблицы в БД
        :param db_columns: колонки таблицы
        :param row_id: Id записи
        :return запрос SELECT в БД
        """
        column_string = ""
        if len(db_columns) > 1:
            for column in db_columns[:-1]:
                column_string += column + ","
            column_string += db_columns[len(db_columns)-1]
        else:
            column_string = db_columns[0]

        return self._client.query(f'SELECT'
                                  f' {column_string} '
                                  f'FROM '
                                  f'{db_name}.{db_table}'
                                  f' WHERE '
                                  f'Id = {row_id}')

    def select_all_from_db(self, db_name: str, db_table: str, db_columns: List):
        """
        Выборка всех записей из БД
        :param db_name: наименование БД
        :param db_table: наименование таблицы в БД
        :param db_columns: колонки таблицы
        :return запрос SELECT в БД
        """
        column_string = ""
        if len(db_columns) > 1:
            for column in db_columns[:-1]:
                column_string += column + ","
            column_string += db_columns[len(db_columns) - 1]
        else:
            column_string = db_columns[0]

        return self._client.query(f'SELECT '
                                  f'{column_string} '
                                  f'FROM '
                                  f'{db_name}.{db_table}')

    @property
    def client(self):
        return self._client

