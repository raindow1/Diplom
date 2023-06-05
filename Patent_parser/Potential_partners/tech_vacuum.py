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
    table_columns = ['Id', 'Problem']
    second_level_count = 0
    third_level_count = 0
    first_level_k = 1
    second_level_k = 1
    third_level_k = 1
    final_k = 0
    tech_vacuum = []

    VO_patent_count = db_client.count_data(db_client.database, db_client.db_yandex_structure)
    IPC_patent_count = db_client.count_data(db_client.database, db_client.db_ipc_structure)
    vo_problems = ProblemComparison()

    for i in range(1, IPC_patent_count):
        if i in rus_patents:
            VO_result = db_client.select_from_db(db_client.database, db_client.db_ipc_structure, ["Problem"], i)
            VO_problem = VO_result.result_rows[0][0]
            VO_res_root = vo_problems.get_structure(VO_problem)[0]
            VO_res_nmod = vo_problems.get_structure(VO_problem)[1]
            VO_third_nmod = vo_problems.get_structure(VO_problem)[2]

            # print(VO_res_root)
            # print(VO_res_nmod)
            # print(VO_third_nmod)

        for c in range(29, IPC_patent_count):

            if c in in_patents:
                IPC_result = db_client.select_from_db(db_client.database, db_client.db_ipc_structure, ["Problem"], c)
                IPC_problem = IPC_result.result_rows[0][0]
                IPC_res_root = vo_problems.get_structure(IPC_problem)[0]
                IPC_res_nmod = vo_problems.get_structure(IPC_problem)[1]
                IPC_third_nmod = vo_problems.get_structure(IPC_problem)[2]

                # print(IPC_res_root)
                # print(IPC_res_nmod)
                # print(IPC_third_nmod)

                for root_key in VO_res_root:
                    if root_key in IPC_res_root:
                        first_level_k *= 3
                if first_level_k == 3:
                    for nmod_key in VO_res_nmod:
                        if nmod_key in IPC_res_nmod:
                            second_level_count += 1
                    if second_level_count > 0:
                        first_level_k *= 2
                        for third_nmod_key in VO_third_nmod:
                            if third_nmod_key in IPC_third_nmod:
                                third_level_count += 1
                        match third_level_count:
                            case 1:
                                third_level_k *= 0.5
                            case 2:
                                third_level_k *= 0.75
                            case 3:
                                third_level_k = 1

                final_k = (first_level_k + second_level_k + third_level_k) / 6

                if final_k < 0.9:
                    if len(IPC_problem) != 0:
                        if IPC_problem[0] not in tech_vacuum:
                            tech_vacuum.append(IPC_problem[0])

            print(f'analyzed patent #{i}')
            print(f'analyzed patent #{c}')

    for problem in tech_vacuum:
        row = [Id, problem]
        data = [row]
        db_client.insert_into_db(data, table_columns, db_client.database, db_client.db_tech_vacuum)
        Id += 1







if __name__ == "__main__":
    main()

