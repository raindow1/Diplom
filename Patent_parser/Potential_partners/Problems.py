from abc import ABC, abstractmethod
from typing import List, Dict
import stanza
from ruwordnet import RuWordNet


class Problems(ABC):

    def __init__(self) -> None:
        self._wn = RuWordNet()
        self._nlp = stanza.Pipeline(lang='ru', processors='tokenize,pos,lemma,ner,depparse')

    @abstractmethod
    def get_key_words(self) -> List[str]:
        """
        Получить ключевые слова из файлов для выделения структур проблем
        :return: ключевые слова
        """
        raise NotImplementedError

    @abstractmethod
    def get_structure(self, problem: str) -> Dict:
        """
        Выделить главные слова в проблеме для анализа на сходство
        :param: строка с проблемой изобретения
        :return: словари с выделенными словами из синтаксической конструкции предложения
        """
        raise NotImplementedError
