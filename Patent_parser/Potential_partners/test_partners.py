from database import client
from Potential_partners.ProblemComparison import ProblemComparison


def main():

    Id = 1
    count = 0
    VO_res_root = []
    VO_res_nmod = []
    VO_third_nmod = []


    VO_patent_count = client.query('SELECT count() FROM db_patents.yandex_problem_solution').result_rows[0][0]
    IPC_patent_count = client.query('SELECT count() FROM db_patents.IPC_problem_solution').result_rows[0][0]
    vo_problems = ProblemComparison()

    for i in range(1, VO_patent_count):
        VO_result = client.query(f'SELECT Problem FROM db_patents.yandex_problem_solution WHERE Id = {i}')
        VO_problem = VO_result.result_rows[0][0]
        VO_res_root = vo_problems.get_structure(VO_problem)[0]
        VO_res_nmod = vo_problems.get_structure(VO_problem)[1]
        VO_third_nmod = vo_problems.get_structure(VO_problem)[2]

        # print(VO_res_root)
        # print(VO_res_nmod)
        # print(VO_third_nmod)

        for c in range(1, IPC_patent_count):

            IPC_result = client.query(f'SELECT Problem FROM db_patents.IPC_problem_solution WHERE Id = {c}')
            IPC_asignee = client.query(f'SELECT Asignee FROM db_patents.IPC_google_patents WHERE Id = {c}').result_rows[0][0]
            IPC_problem = IPC_result.result_rows[0][0]
            IPC_res_root = vo_problems.get_structure(IPC_problem)[0]
            IPC_res_nmod = vo_problems.get_structure(IPC_problem)[1]
            IPC_third_nmod = vo_problems.get_structure(IPC_problem)[2]

            print(IPC_res_root)
            print(IPC_res_nmod)
            print(IPC_third_nmod)

            for root_key in VO_res_root:
                if root_key in IPC_res_root:
                    count += 1
            for nmod_key in VO_res_nmod:
                if nmod_key in IPC_res_nmod:
                    count += 1
            for third_nmod_key in VO_third_nmod:
                if third_nmod_key in IPC_third_nmod:
                    count += 1

            if count >= 3:
                sim_probs = ['fff', 'ddd']
                row = [Id, IPC_asignee, IPC_problem[0], sim_probs]
                data = [row]
                client.insert('Potential_partners', data,
                              column_names=['Id', 'Organisation_name', 'Problems', 'Similar_problems'],
                              database="db_patents")
                Id += 1


            print(f'analyzed patent #{c}')







if __name__ == "__main__":
    main()

