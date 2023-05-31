from typing import List
import csv
from Potential_partners.Problems import Problems


class ProblemComparison(Problems):
    def __init__(self) -> None:
        super().__init__()

    def get_key_words(self) -> List[str]:
        tmp = dict()
        word_list = []
        deletion_mas = []
        with open('dataset.csv', 'r') as csv_file:
            reader = csv.reader(csv_file)
            for row in reader:
                tmp_list = row[1].split(";")
                for word in tmp_list:
                    if word != '':
                        word = word.split(" ")
                        if word[0] not in word_list:
                            word_list.append(word[0])

        with open('dataset_1.csv', 'r') as csv_file:
            reader = csv.reader(csv_file)
            for row in reader:
                tmp_list = row[1].split(";")
                for word in tmp_list:
                    if word != '':
                        word = word.split(" ")
                        if word[0] not in word_list:
                            word_list.append(word[0])

        file = open("sentences.txt")
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

        # Удаление лишних слов из списка
        # Удаление вручную
        deletion_mas.remove(",")
        word_list.remove("автоматизированное")
        word_list.remove("сбор,")
        word_list.remove("обеспеченин")
        word_list.remove("полученин")
        word_list.remove('')
        # Удаление найденных слов через анализ части речи
        for del_word in deletion_mas:
            word_list.remove(del_word)

        return word_list

    def get_structure(self, problem: str) -> tuple:
        tmp = dict()
        word_count = 0
        res_root = dict()
        res_nmod = dict()
        third_nmod = dict()
        root_hyponyms = []
        nmod_hyponyms = []
        third_hyponyms = []
        root_id = 0
        second_nmod_id = 0

        list = self.get_key_words()


        if problem:
            for word in list:
                if word in problem[0]:
                    word_count += 1
                    index = problem[0].find(word)
                    splitted_string = problem[0][index:]
                    anl_string = splitted_string.split(',')[0]
                    doc = self._nlp(anl_string)
                    for sent in doc.sentences:
                        for a in sent.words:
                            tmp[a.text] = {"deprel": a.deprel, "lemma": a.lemma, "id": a.id, "head": a.head}
                    for k in tmp.keys():
                        if tmp[k]["deprel"] in ["root"]:
                            res_root[k] = {"lemma": tmp[k]["lemma"], "id": tmp[k]["id"]}
                            root_id = res_root[k]["id"]
                        if tmp[k]["deprel"] in ["nmod"] and tmp[k]["head"] == root_id:
                            res_nmod[k] = {"lemma": tmp[k]["lemma"]}
                            second_nmod_id = tmp[k]["id"]
                        if tmp[k]["deprel"] in ["nmod"] and tmp[k]["head"] == second_nmod_id:
                            third_nmod[k] = {"lemma": tmp[k]["lemma"]}


                    for key_root in res_root.keys():
                        root_hyponyms.append(res_root[key_root]["lemma"])

                    for key_nmod in res_nmod.keys():
                        try:
                            nmod_synsets = self._wn.get_senses(res_nmod[key_nmod]["lemma"])[0].synset.hypernyms
                            nmod_hyponyms = nmod_synsets[0].title.split(",")
                        except (KeyError, IndexError):
                            nmod_synsets = ""
                        nmod_hyponyms.append(res_nmod[key_nmod]["lemma"])

                    for key_third_nmod in third_nmod.keys():
                        try:
                            third_synsets = self._wn.get_senses(res_nmod[key_third_nmod]["lemma"])[0].synset.hypernyms
                            third_hyponyms = third_synsets[0].title.split(",")
                        except (KeyError, IndexError):
                            third_synsets = ""
                        third_hyponyms.append(third_nmod[key_third_nmod]["lemma"])
                if word_count > 0:
                    break

        return root_hyponyms, nmod_hyponyms, third_hyponyms
