from Database.database import client
from Potential_partners.ProblemComparison import ProblemComparison


def main():

    Id = 20
    second_level_count = 0
    third_level_count = 0
    VO_res_root = []
    VO_res_nmod = []
    VO_third_nmod = []
    first_level_k = 1
    second_level_k = 1
    third_level_k = 0
    final_k = 0
    partners = []


    VO_patent_count = client.query('SELECT count() FROM db_patents.yandex_problem_solution').result_rows[0][0]
    IPC_patent_count = client.query('SELECT count() FROM db_patents.IPC_problem_solution').result_rows[0][0]
    vo_problems = ProblemComparison()

    for i in range(6, VO_patent_count):
        VO_result = client.query(f'SELECT Problem FROM db_patents.yandex_problem_solution WHERE Id = {i}')
        VO_problem = VO_result.result_rows[0][0]
        VO_res_root = vo_problems.get_structure(VO_problem)[0]
        VO_res_nmod = vo_problems.get_structure(VO_problem)[1]
        VO_third_nmod = vo_problems.get_structure(VO_problem)[2]

        print(VO_res_root)
        print(VO_res_nmod)
        print(VO_third_nmod)
#i = 11 c = 50 - test data
        for c in range(1, IPC_patent_count):

            IPC_result = client.query(f'SELECT Problem FROM db_patents.IPC_problem_solution WHERE Id = {c}')
            IPC_asignee = client.query(f'SELECT Asignee FROM db_patents.IPC_google_patents WHERE Id = {c}').result_rows[0][0]
            IPC_problem = IPC_result.result_rows[0][0]
            IPC_res_root = vo_problems.get_structure(IPC_problem)[0]
            IPC_res_nmod = vo_problems.get_structure(IPC_problem)[1]
            IPC_third_nmod = vo_problems.get_structure(IPC_problem)[2]
            third_nmod_len = len(IPC_third_nmod)

            print(IPC_res_root)
            print(IPC_res_nmod)
            print(IPC_third_nmod)

            for root_key in VO_res_root:
                if root_key in IPC_res_root:
                    first_level_k *= 3
            if first_level_k == 3:
                for nmod_key in VO_res_nmod:
                    if nmod_key in IPC_res_nmod:
                        second_level_count += 1
                if second_level_count > 0:
                    second_level_k *= 2
                    for third_nmod_key in VO_third_nmod:
                        if third_nmod_key in IPC_third_nmod:
                            third_level_count += 1
                    match third_level_count:
                        case 1:
                            third_level_k = 0.5
                        case 2:
                            third_level_k = 0.75
                        case 3:
                            third_level_k = 1

            final_k = (first_level_k + second_level_k + third_level_k) / 6

            if final_k > 0.9 and IPC_asignee not in partners:
                partners.append(IPC_asignee)
                row = [Id, IPC_asignee, IPC_problem, c, final_k]
                data = [row]
                client.insert('potential_partners', data,
                              column_names=['Id', 'Organisation_name', 'IProblems', 'IPC_patent_id', "Match_ratio"],
                              database="db_patents")
                Id += 1

            second_level_count = 0
            third_level_count = 0
            first_level_k = 1
            second_level_k = 1
            third_level_k = 0
            final_k = 0

            print(f'analyzed patent #{i}')
            print(f'analyzed patent #{c}')







if __name__ == "__main__":
    main()

