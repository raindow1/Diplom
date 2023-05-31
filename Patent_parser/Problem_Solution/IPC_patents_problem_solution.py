from Database.database import client
from yargy import Parser
from razdel import sentenize
from dicts_and_rules import ORGANIZATION, ORGANIZATION1


def main():

    Id = 1285

    orgparser_main = Parser(ORGANIZATION)
    orgparser_add = Parser(ORGANIZATION1)

    problems = []

    patent_count = client.query('SELECT count() FROM db_patents.translated_IPC_patents').result_rows[0][0]

    for i in range(1285, patent_count):
        result = client.query(f'SELECT Description, Abstract FROM db_patents.translated_IPC_patents WHERE Id = {i}')
        solution = client.query(f'SELECT Solution FROM db_patents.translated_IPC_patents WHERE Id = {i}').result_rows[0][0]
        description = result.result_rows[0][0]
        abstract = result.result_rows[0][1]

        description_sentences = list(sentenize(description))
        abstract_sentences = list(sentenize(abstract))

        for desc_sentence in description_sentences:
            matches = list(orgparser_main.findall(desc_sentence.text))
            if matches and not problems:
                problems.append(desc_sentence.text)
            else:
                matches = list(orgparser_add.findall(desc_sentence.text))
                if matches and not problems:
                    problems.append(desc_sentence.text)


        for abstr_sentence in abstract_sentences:
            matches = list(orgparser_main.findall(abstr_sentence.text))
            if matches and not problems:
                problems.append(abstr_sentence.text)
            else:
                matches = list(orgparser_add.findall(abstr_sentence.text))
                if matches and not problems:
                    problems.append(abstr_sentence.text)


        row = [Id, problems, solution, i]
        data = [row]
        client.insert('IPC_problem_solution', data,
                      column_names=['Id', 'Problem', 'Solution', 'Patent_id'], database="db_patents")
        Id += 1
        problems.clear()


if __name__ == "__main__":
    main()
