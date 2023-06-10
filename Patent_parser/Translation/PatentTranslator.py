from deep_translator import GoogleTranslator
from typing import List
import time


class PatentTranslator:
    def __init__(self) -> None:
        self._translator = GoogleTranslator(source='en', target='ru')

    def create_chunks(self, corpus: str, max_chunk_size: int) -> List[str]:
        """
        Разбить строку большого объема на фрагменты для перевода
        :param corpus: полный текст
        :param max_chunk_size: максимальный размер фрагмента
        :return список с фрагментами текста для дальнейшего перевода
        """
        chunks = [corpus[i:i + max_chunk_size] for i in range(0, len(corpus), max_chunk_size)]
        return chunks

    def translate_text(self, field: str, max_chunk_size: int) -> str:
        """
        Перевод текстового поля на английский язык
        :param field: текстовое поле
        :param max_chunk_size: максимальный размер фрагмента
        :return переведенное текстовое поле
        """
        # Проверка на длину текстового поля
        if len(field) > max_chunk_size:
            results_list = []   # Список переведенных фрагментов текста
            concatenated_result = ""   # Соединенные фрагменты теста

            # Перевод текста по частям
            original_chunks = self.create_chunks(field, max_chunk_size)
            for i in original_chunks:
                r = self._translator.translate(text=i)
                time.sleep(10)
                results_list.append(r)

            # Соединение переведенных фрагментов
            for i in results_list:
                concatenated_result += i

            return concatenated_result
        else:
            # Перевод небольшого текстового поля
            res = self._translator.translate(text=field)
            time.sleep(10)
            return res

