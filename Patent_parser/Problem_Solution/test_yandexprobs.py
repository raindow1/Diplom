from database import client
from Problem_Solution.YandexProblemSolution import YandexProblemSolution


def main():

    patent_count = client.query('SELECT count() FROM db_patents.yandex_patents').result_rows[0][0]

    for i in range(1, patent_count):
        yandex_probs = YandexProblemSolution()
        solution = yandex_probs.get_solution(i)
        problems = yandex_probs.get_problem(i)

        print(problems)
        print(solution)

if __name__ == "__main__":
    main()