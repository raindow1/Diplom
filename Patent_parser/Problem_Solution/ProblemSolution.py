from abc import ABC, abstractmethod
from typing import List, Dict, Union
from dicts_and_rules import ORGANIZATION, ORGANIZATION1
from yargy import Parser, rule, and_, not_


class ProblemSolution(ABC):

    def __init__(self) -> None:
        """
        Инициализировать yargy-парсер
        """
        self._orgparser_main = Parser(ORGANIZATION)
        self._orgparser_add = Parser(ORGANIZATION1)
    @abstractmethod
    def get_problem(self, patent_id: int) -> List[str]:
        """
        Получить проблему(цель) изобретения
        """
        raise NotImplementedError

    def get_solution(self, patent_id: int) -> str:
        """
        Получить название патента
        """
        raise NotImplementedError