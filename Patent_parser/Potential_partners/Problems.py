from abc import ABC, abstractmethod
from typing import List, Dict, Union
import stanza
from ruwordnet import RuWordNet


class Problems(ABC):

    def __init__(self) -> None:
        """
        Инициализировать WordNet и Stanza
        """
        self._wn = RuWordNet()
        self._nlp = stanza.Pipeline(lang='ru', processors='tokenize,pos,lemma,ner,depparse')

    @abstractmethod
    def get_key_words(self) -> List[str]:
        """
        Получить ключевые слова из файлов для выделения структур проблем
        """
        raise NotImplementedError

    @abstractmethod
    def get_structure(self, problem: str) -> Dict:
        """
        Выделить главные слова в проблеме для анализа на сходство
        """
        raise NotImplementedError
