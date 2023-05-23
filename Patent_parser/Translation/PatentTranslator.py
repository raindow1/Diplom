from Translation.Translator import Translator
from typing import List, Dict, Union
import time


class PatentTranslator(Translator):
    def __init__(self) -> None:
        super().__init__()

    def create_chunks(self, corpus: str, max_chunk_size: int) -> List[str]:
        chunks = [corpus[i:i + max_chunk_size] for i in range(0, len(corpus), max_chunk_size)]
        return chunks

    def translate_text(self, field: str, max_chunk_size: int) -> str:
        if len(field) > max_chunk_size:
            results_list = []
            concatenated_result = ""

            original_chunks = self.create_chunks(field, max_chunk_size)
            for i in original_chunks:
                r = self._translator.translate(text=i)
                time.sleep(10)
                results_list.append(r)

            for i in results_list:
                concatenated_result += i

            return concatenated_result
        else:
            res = self._translator.translate(text=field)
            time.sleep(10)
            return res

