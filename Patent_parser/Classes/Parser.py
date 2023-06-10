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
        :return:название патента
        """
        raise NotImplementedError

    def get_assignee(self) -> str:
        """
        Получить правопреемника
        :return:правопреемник
        """
        raise NotImplementedError

    def get_authors(self) -> str:
        """
        Получить авторов
        :return: авторы патента
        """
        raise NotImplementedError

    def get_index(self) -> str:
        """
        Получить индекс патента
        :return: индекс патента
        """
        raise NotImplementedError

    @abstractmethod
    def get_date_of_publication(self) -> str:
        """
        Получить дату публикации патента
        :return: дата публикации патента
        """
        raise NotImplementedError

    @abstractmethod
    def get_abstract(self) -> str:
        """
        Получить аннотацию патента
        :return: текстовое поле аннотации патента
        """
        raise NotImplementedError

    @abstractmethod
    def get_description(self) -> str:
        """
        Получить описание патента
        :return: текстовое поле описания патента
        """
        raise NotImplementedError

    @abstractmethod
    def get_claims(self) -> str:
        """
        Получить формулу изобретения
        :return: текстовое поле формулы изобретения
        """
        raise NotImplementedError

    @abstractmethod
    def get_ipc(self) -> str:
        """
        Получить классы МПК
        :return: список классов МПК
        """
        raise NotImplementedError

    @abstractmethod
    def get_similar_patents(self) -> str:
        """
        Получить список похожих патентов
        :return: список похожих патентов
        """
        raise NotImplementedError


