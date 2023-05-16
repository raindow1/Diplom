import time
from database import client
from yargy import Parser, rule, and_, not_
from yargy.pipelines import morph_pipeline, caseless_pipeline
from razdel import sentenize
from yargy.interpretation import fact


def get_struct(Id):
    Problem = fact(
        'Problem',
        ['target', 'add_word', 'second_word']
    )

    TARGET = morph_pipeline([
        "цель",
        "способ",
        "изобретение",
        "задача",
        "модель",
        "использование"
    ])

    ADD_WORD = caseless_pipeline([
        "предлагаеого",
        "настоящего",
        "данного",
        "решаемая"
    ])

    SECOND_WORD = morph_pipeline([
        "изобретения",
        "предназначено",
        "решения",
        "устройства"
    ])

    SECOND_WORD_ADD = morph_pipeline([
        "позволяет",
        "достигается",
        "результат",
        "решает",
        "направлено",
        "модели",
        "способа",
    ])


    # Rules for problem extraction
    ORGANIZATION = rule(TARGET.interpretation(Problem.target),
                        ADD_WORD.interpretation(Problem.add_word).optional(),
                        SECOND_WORD.interpretation(Problem.second_word))

    ORGANIZATION1 = rule(TARGET.interpretation(Problem.target),
                         ADD_WORD.interpretation(Problem.add_word).optional(),
                         SECOND_WORD_ADD.interpretation(Problem.second_word))

    orgparser_main = Parser(ORGANIZATION)
    orgparser_add = Parser(ORGANIZATION1)

    problems = []

    patent_count = client.query('SELECT count() FROM db_patents.google_patents').result_rows[0][0]


    result = client.query(f'SELECT Description, Abstract FROM db_patents.google_patents WHERE Id = {Id}')
    solution = client.query(f'SELECT Title FROM db_patents.google_patents WHERE Id = {Id}').result_rows[0][0]
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


    return problems


def main():
    problems = get_struct(12)
    print(problems)


if __name__ == "__main__":
    main()