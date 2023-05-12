from abc import ABC, abstractmethod
from typing import List, Dict, Union


class Parser(ABC):
    @abstractmethod
    def get_patent_link(self, link: str) -> None:
        """
        Получить ссылку на патент
        """
        raise NotImplementedError

    def get_title(self) -> str:
        """
        Получить название патента
        """
        raise NotImplementedError

    def get_assignee(self) -> str:
        """
        Получить правопреемника
        """
        raise NotImplementedError

    def get_authors(self) -> str:
        """
        Получить авторов
        """
        raise NotImplementedError

    @abstractmethod
    def get_date_of_publication(self) -> str:
        """
        Получить дату публикации патента
        """
        raise NotImplementedError

    @abstractmethod
    def get_abstract(self) -> str:
        """
        Получить аннотацию
        """
        raise NotImplementedError

    @abstractmethod
    def get_description(self) -> str:
        """
        Получить описание патента
        """
        raise NotImplementedError

    @abstractmethod
    def get_claims(self) -> str:
        """
        Получить формулу изобретения
        """
        raise NotImplementedError

    @abstractmethod
    def get_ipc(self) -> str:
        """
        Получить классы МПК
        """
        raise NotImplementedError

    @abstractmethod
    def get_similar_patents(self) -> str:
        """
        Получить список похожих патентов
        """
        raise NotImplementedError


