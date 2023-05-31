from Database.database import client
from Potential_partners.ProblemComparison import ProblemComparison
from Database.ClickhouseDB import ClickhouseDB


def patent_filter():
    patent_count = client.query('SELECT count() FROM db_patents.IPC_google_patents').result_rows[0][0]
    rus_patents = []
    in_patents = []
    for i in range(1, patent_count):
        patent_index = client.query(f'SELECT Index FROM db_patents.IPC_google_patents WHERE Id = {i}').result_rows[0][0]
        if 'RU' in patent_index:
            rus_patents.append(i)
        else:
            in_patents.append(i)

    return rus_patents, in_patents


def main():

    Id = 1
    count = 0
    VO_res_root = []
    VO_res_nmod = []
    VO_third_nmod = []
    rus_patents = patent_filter()[0]
    in_patents = patent_filter()[1]
    db_client = ClickhouseDB()
    database = "db_patents"
    VO_db = "yandex_problem_solution"
    IPC_db = "IPC_problem_solution"
    vacuum_db = "tech_vacuum"
    table_columns = ['Id', 'Problem']

    VO_patent_count = db_client.count_data(database, VO_db)
    IPC_patent_count = db_client.count_data(database, IPC_db)
    vo_problems = ProblemComparison()

    for i in range(1, IPC_patent_count):
        if i in rus_patents:
            VO_result = db_client.select_from_db(database, IPC_db, ["Problem"], i)
            VO_problem = VO_result.result_rows[0][0]
            VO_res_root = vo_problems.get_structure(VO_problem)[0]
            VO_res_nmod = vo_problems.get_structure(VO_problem)[1]
            VO_third_nmod = vo_problems.get_structure(VO_problem)[2]

            # print(VO_res_root)
            # print(VO_res_nmod)
            # print(VO_third_nmod)

        for c in range(1, IPC_patent_count):

            if c in in_patents:
                IPC_result = db_client.select_from_db(database, IPC_db, ["Problem"], c)
                IPC_problem = IPC_result.result_rows[0][0]
                IPC_res_root = vo_problems.get_structure(IPC_problem)[0]
                IPC_res_nmod = vo_problems.get_structure(IPC_problem)[1]
                IPC_third_nmod = vo_problems.get_structure(IPC_problem)[2]

                # print(IPC_res_root)
                # print(IPC_res_nmod)
                # print(IPC_third_nmod)

                for root_key in VO_res_root:
                    if root_key in IPC_res_root:
                        count += 1
                for nmod_key in VO_res_nmod:
                    if nmod_key in IPC_res_nmod:
                        count += 1
                for third_nmod_key in VO_third_nmod:
                    if third_nmod_key in IPC_third_nmod:
                        count += 1

                if count < 3 and IPC_problem[0]:
                    row = [Id, IPC_problem[0]]
                    data = [row]
                    db_client.insert_into_db(data, table_columns, database, vacuum_db)
                    Id += 1


            print(f'analyzed patent #{c}')







if __name__ == "__main__":
    main()

