from Problem_Solution.ProblemSolution import ProblemSolution
from database import client
from typing import List, Dict, Union
from razdel import sentenize


class YandexProblemSolution(ProblemSolution):
    def __init__(self) -> None:
        super().__init__()

    def get_problem(self, patent_id: int) -> List[str]:
        problems = []
        result = client.query(f'SELECT Description, Abstract FROM db_patents.yandex_patents WHERE Id = {patent_id}')

        description = result.result_rows[0][0]
        abstract = result.result_rows[0][1]

        description_sentences = list(sentenize(description))
        abstract_sentences = list(sentenize(abstract))

        for desc_sentence in description_sentences:
            matches = list(self._orgparser_main.findall(desc_sentence.text))
            if matches and not problems:
                problems.append(desc_sentence.text)
            else:
                matches = list(self._orgparser_add.findall(desc_sentence.text))
                if matches and not problems:
                    problems.append(desc_sentence.text)

        for abstr_sentence in abstract_sentences:
            matches = list(self._orgparser_main.findall(abstr_sentence.text))
            if matches and not problems:
                problems.append(abstr_sentence.text)
            else:
                matches = list(self._orgparser_add.findall(abstr_sentence.text))
                if matches and not problems:
                    problems.append(abstr_sentence.text)

        return problems

    def get_solution(self, patent_id: int) -> str:
        return client.query(f'SELECT Title FROM db_patents.yandex_patents WHERE Id = {patent_id}').result_rows[0][0]
