from abc import ABC, abstractmethod
from deep_translator import GoogleTranslator
from typing import List, Dict, Union


class Translator(ABC):
    def __init__(self) -> None:
        """
        Инициализировать переводчик
        """
        self._translator = GoogleTranslator(source='en', target='ru')

    @abstractmethod
    def create_chunks(self, corpus: str, max_chunk_size: int) -> List[str]:
        """
        Разбить текст на части
        """
        raise NotImplementedError

    @abstractmethod
    def translate_text(self, field: str, max_chunk_size: int) -> str:
        """
        Перевести текст на русский язык
        """
        raise NotImplementedError