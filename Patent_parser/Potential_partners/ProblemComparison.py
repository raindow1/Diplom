from typing import List
import csv
from Potential_partners.Problems import Problems


class ProblemComparison(Problems):
    def __init__(self) -> None:
        super().__init__()

    def get_key_words(self) -> List[str]:
        """
        Получить ключевые слова из файлов для выделения структур проблем
        :return: ключевые слова
        """
        # Объявление необходимых переменных
        tmp = dict()  # временный словарь
        word_list = []  # список искмых ключевых слов
        deletion_mas = []  # список со словами для удаления

        # Выделение ключевых слов из первого тестового датасета
        with open('../Data/dataset.csv', 'r') as csv_file:
            reader = csv.reader(csv_file)
            for row in reader:
                tmp_list = row[1].split(";")
                for word in tmp_list:
                    if word != '':
                        word = word.split(" ")
                        if word[0] not in word_list:
                            word_list.append(word[0])

        # Выделение ключевых слов из второго тестового датасета
        with open('../Data/dataset_1.csv', 'r') as csv_file:
            reader = csv.reader(csv_file)
            for row in reader:
                tmp_list = row[1].split(";")
                for word in tmp_list:
                    if word != '':
                        word = word.split(" ")
                        if word[0] not in word_list:
                            word_list.append(word[0])


        # Выделение ключевых слов из третьего тестового датасета
        file = open("../Data/sentences.txt")
        for line in file:
            sent = line.split(",")
            for s in sent:
                tmp_list = row[1].split(";")
                for word in tmp_list:
                    if word != '':
                        word = word.split(" ")
                        if word[0] not in word_list:
                            word_list.append(word[0])

        # Нахождение лишних слов с помощью поиска частей речи
        for f in word_list:
            doc = self._nlp(f)
            for sent in doc.sentences:
                for word in sent.words:
                    tmp[word.text] = {"upos": word.upos, "lemma": word.lemma}
                    f = tmp[word.text]["lemma"]
        for k in tmp.keys():
            if (tmp[k]["upos"] in ["ADJ", "ADV", "PUNCT"]):
                deletion_mas.append(k)


        # Удаление нкоторых слов вручную
        deletion_mas.remove(",")
        word_list.remove("автоматизированное")
        word_list.remove("сбор,")
        word_list.remove("обеспеченин")
        word_list.remove("полученин")
        word_list.remove('')

        # Удаление найденных лишних слов
        for del_word in deletion_mas:
            word_list.remove(del_word)

        return word_list

    def get_structure(self, problem: str) -> tuple:
        """
        Выделить главные слова в проблеме для анализа на сходство
        :param: строка с проблемой изобретения
        :return: списки с выделенными словами из синтаксической конструкции предложения
        """

        # Объявление необходимых переменных
        tmp = dict()  # Временный словарь
        word_count = 0  # Количество найденных ключевых слов в предложении
        res_root = dict()  # Словарь с начальной формой найденного сказуемого
        res_nmod = dict()  # Словарь с начальными формами найденных зависимых от сказуемого слов (второй уровень)
        third_nmod = dict()  # Словарь с начальными формами найденных зависимых слов от слов второго уровня
        root_result_mas = []  # Список с найденным сказуемым
        nmod_result_mas = []  # Список с найденными зависимыми словами второго уровня и их гиперонимами
        third_nmod_result_mas = []  # Список с найденными зависимыми словами третьего уровня и их гиперонимами
        root_id = 0  # Позиция в предложении сказуемого
        second_nmod_id = 0  # Позиция в предложении второго зависимого слова
        third_nmod_id = 0  # Позиция в предложении третьего зависимого слова

        list = self.get_key_words()

        # Проверка на наличие предложения с проблемой во входной переменной
        if problem:
            for word in list:
                # Выделение основной части предложения
                if word in problem[0]:
                    word_count += 1
                    index = problem[0].find(word)
                    splitted_string = problem[0][index:]
                    anl_string = splitted_string.split(',')[0]
                    # Построение дерева зависимости найденной части
                    doc = self._nlp(anl_string)
                    # Поиск и сохранение в словари сказуемых и зависимых слов
                    for sent in doc.sentences:
                        for a in sent.words:
                            tmp[a.text] = {"deprel": a.deprel, "lemma": a.lemma, "id": a.id, "head": a.head}
                    for k in tmp.keys():
                        if tmp[k]["deprel"] in ["root"]:
                            res_root[k] = {"lemma": tmp[k]["lemma"], "id": tmp[k]["id"]}
                            root_id = res_root[k]["id"]
                        if tmp[k]["deprel"] in ["nmod","amod", "obj"] and tmp[k]["head"] == root_id:
                            res_nmod[k] = {"lemma": tmp[k]["lemma"]}
                            second_nmod_id = tmp[k]["id"]
                        if tmp[k]["deprel"] in ["nmod","amod", "obj"] and tmp[k]["head"] == second_nmod_id:
                            third_nmod[k] = {"lemma": tmp[k]["lemma"]}
                            third_nmod_id = tmp[k]["id"]
                        if tmp[k]["deprel"] in ["nmod","amod", "obj"] and tmp[k]["head"] == third_nmod_id:
                            third_nmod[k] = {"lemma": tmp[k]["lemma"]}

                    # Сохранение в результирующий список сказуемого
                    for key_root in res_root.keys():
                        root_result_mas.append(res_root[key_root]["lemma"])

                    # Сохранение в результирующий список зависимых слов второго уровня, а также их гиперонимов при наличии
                    for key_nmod in res_nmod.keys():
                        try:
                            nmod_synsets = self._wn.get_senses(res_nmod[key_nmod]["lemma"])[0].synset.hypernyms
                            nmod_result_mas = nmod_synsets[0].title.split(",")
                        except (KeyError, IndexError):
                            nmod_synsets = ""
                        nmod_result_mas.append(res_nmod[key_nmod]["lemma"])

                    # Сохранение в результирующий список зависимых слов третьего уровня, а также их гиперонимов при наличии
                    for key_third_nmod in third_nmod.keys():
                        try:
                            third_synsets = self._wn.get_senses(res_nmod[key_third_nmod]["lemma"])[0].synset.hypernyms
                            third_nmod_result_mas = third_synsets[0].title.split(",")
                        except (KeyError, IndexError):
                            third_synsets = ""
                        third_nmod_result_mas.append(third_nmod[key_third_nmod]["lemma"])
                if word_count > 0:
                    break

        return root_result_mas, nmod_result_mas, third_nmod_result_mas
