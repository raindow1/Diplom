from Problem_Solution.ProblemSolution import ProblemSolution
from Database.database import client
from typing import List
from razdel import sentenize


class ProblemSolutionExtractor(ProblemSolution):
    def __init__(self) -> None:
        super().__init__()

    def get_problem(self, description: str, abstract: str) -> List[str]:
        """
        Получить проблему(цель) изобретения
        :param description: текст описания изобретения
        :param abstract: текст анотации изобретения
        :return список проблем
        """

        # Обявление списка с найденными предложениями
        problems = []

        # Сегментация текстовых полей на предложения
        description_sentences = list(sentenize(description))
        abstract_sentences = list(sentenize(abstract))

        # Анализ каждого предложения текста описания изобретения с учетом сформулированных правил
        for desc_sentence in description_sentences:
            matches = list(self._orgparser_main.findall(desc_sentence.text))
            if matches and not problems:
                problems.append(desc_sentence.text)
            else:
                matches = list(self._orgparser_add.findall(desc_sentence.text))
                if matches and not problems:
                    problems.append(desc_sentence.text)

        # Анализ каждого предложения текста аннотации изобретения с учетом сформулированных правил
        for abstr_sentence in abstract_sentences:
            matches = list(self._orgparser_main.findall(abstr_sentence.text))
            if matches and not problems:
                problems.append(abstr_sentence.text)
            else:
                matches = list(self._orgparser_add.findall(abstr_sentence.text))
                if matches and not problems:
                    problems.append(abstr_sentence.text)

        return problems

