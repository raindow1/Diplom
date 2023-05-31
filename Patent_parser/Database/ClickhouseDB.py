from typing import List
import clickhouse_connect


class ClickhouseDB:
    def __init__(self) -> None:
        self._client = clickhouse_connect.get_client(host='localhost', username='raindow', password='1988')
        self.database = "db_patents"
        self.db_yandex_patents = "yandex_patents"
        self.db_google_patents = "google_patents"
        self.db_ipc_patents = "IPC_google_patents"
        self.db_yandex_structure = "yandex_problem_solution"
        self.db_google_structure = "google_problem_solution"
        self.db_potential_partners = "Potential_partners"
        self.db_tech_vacuum = "tech_vacuum"
        self.db_transd_patents = "translated_IPC_patents"
        self.db_ipc_structure = "IPC_problem_solution"

    def insert_into_db(self, data: List, table_columns: List, db_name: str, db_table: str) -> None:
        return self._client.insert(db_table, data,
                      column_names=table_columns,
                      database=db_name)

    def count_data(self, db_name: str, db_table: str) -> int:
        return self._client.query(f'SELECT count() FROM {db_name}.{db_table}').result_rows[0][0]

    def delete_from_db(self, db_name: str, db_table: str, row_id: int) -> None:
        return self._client.query(f'DELETE FROM {db_name}.{db_table} WHERE Id =={row_id}')

    def delete_all_from_db(self, db_name: str, db_table: str) -> None:
        return self._client.query(f'DELETE FROM {db_name}.{db_table}')

    def select_from_db(self, db_name: str, db_table: str, db_columns: List, row_id: int):
        column_string = ""
        if len(db_columns) > 1:
            for column in db_columns[:-1]:
                column_string += column + ","
            column_string += db_columns[len(db_columns)-1]
        else:
            column_string = db_columns[0]

        return self._client.query(f'SELECT {column_string} FROM {db_name}.{db_table} WHERE Id = {row_id}')

