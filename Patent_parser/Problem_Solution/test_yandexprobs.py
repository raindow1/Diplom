from Database.ClickhouseDB import ClickhouseDB
from Problem_Solution.YandexProblemSolution import YandexProblemSolution


def main():

    db_client = ClickhouseDB()
    patent_count = db_client.count_data(db_client.database, db_client.db_yandex_patents)

    for i in range(1, patent_count):
        yandex_probs = YandexProblemSolution()
        solution = yandex_probs.get_solution(i)
        problems = yandex_probs.get_problem(i)

        print(problems)
        print(solution)

if __name__ == "__main__":
    main()