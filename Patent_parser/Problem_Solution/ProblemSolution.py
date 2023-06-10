from abc import ABC, abstractmethod
from typing import List, Dict, Union
from dicts_and_rules import ORGANIZATION, ORGANIZATION1
from yargy import Parser, rule, and_, not_


class ProblemSolution(ABC):

    def __init__(self) -> None:
        self._orgparser_main = Parser(ORGANIZATION)
        self._orgparser_add = Parser(ORGANIZATION1)
    @abstractmethod
    def get_problem(self, description: str, abstract: str) -> List[str]:
        """
        Получить проблему(цель) изобретения
        :param description: текст описания изобретения
        :param abstract: текст анотации изобретения
        :return список проблем
        """
        raise NotImplementedError

