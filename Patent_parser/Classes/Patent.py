from Classes.Parser import Parser


class Patent:
    def __init__(self, link: str, parser: Parser) -> None:
        self.__link = link
        self.__parser = parser
        self.link = self.__link

    @property
    def link(self) -> str:
        return self.__link

    @link.setter
    def link(self, link: str) -> None:
        self.__link = link
        self.__parser.get_patent_link(link)

    @property
    def parser(self) -> Parser:
        return self.__parser

    @parser.setter
    def parser(self, parser: Parser) -> None:
        self.__parser = parser
        self.__parser.get_patent_link(self.__link)


    def get_title(self) -> str:
        """
        Получить название патента
        :return: название патента
        """
        return self.__parser.get_title()

    def get_assignee(self) -> str:
        """
        Получить правопреемника
        :return: правопреемник
        """
        return self.__parser.get_assignee()

    def get_authors(self) -> str:
        """
        Получить авторов
        :return: авторы патента
        """
        return self.__parser.get_authors()

    def get_index(self) -> str:
        """
        Получить индекс патента
        :return: индекс патента
        """
        return self.__parser.get_index()

    def get_date_of_publication(self) -> str:
        """
        Получить дату публикации патента
        :return: дата публикации патента
        """
        return self.__parser.get_date_of_publication()

    def get_abstract(self) -> str:
        """
        Получить аннотацию
        :return: текстовое поле аннотации патента
        """
        return self.__parser.get_abstract()

    def get_description(self) -> str:
        """
        Получить описание
        :return: текстовое поле описания патента
        """
        return self.__parser.get_description()

    def get_claims(self) -> str:
        """
        Получить формулу изобретения
        :return: текстовое поле формулы изобретения
        """
        return self.__parser.get_claims()

    def get_ipc(self) -> str:
        """
        Получить классы МПК
        :return:список классов МПК
        """
        return self.__parser.get_ipc()

    def get_similar_patents(self) -> str:
        """
        Получить похожие патенты
        :return: список похожих патентов
        """
        return self.__parser.get_similar_patents()
