from database import client
from yargy import Parser, rule, and_, not_
from yargy.interpretation import fact
from yargy.predicates import gram
from yargy.relations import gnc_relation
from yargy.pipelines import morph_pipeline, caseless_pipeline
from razdel import sentenize

Id = 1

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

SECOND_WORD1 = morph_pipeline([
    "позволяет",
    "достигается",
    "результат",
    "решает",
    "направлено",
    "модели",
    "способа",
    ])

KEY_WORDS = morph_pipeline([
    'целью изобретения',
    'цель изобретения',
    'изобретение предназаначено',
    "способ предназначен",
    "способ позволяет",
    "целью решения",
    "целью предлагаемого решения",
    "задачей способа",
    "задачей изобретения",
    "задача изобретения",
    "задача достигается",
    "задачей предлагаемого изобретения",
    "задачей настоящего изобретения",
    "задачей данного изобретения",
    "задачей решения",
    "задачей предлагаемого решения",
    "изобретение позволяет",
    "модель позволяет",
    "изобретение решает",
    "целью способа",
    "решаемая изобретением",
    "результатом изобретения",
    "техническая задача"
])

ORGANIZATION = rule(TARGET.interpretation(Problem.target),
                    ADD_WORD.interpretation(Problem.add_word).optional(),
                    SECOND_WORD.interpretation(Problem.second_word))

ORGANIZATION1 = rule(TARGET.interpretation(Problem.target),
                    ADD_WORD.interpretation(Problem.add_word).optional(),
                    SECOND_WORD1.interpretation(Problem.second_word))

orgparser = Parser(ORGANIZATION)
orgparser1 = Parser(ORGANIZATION1)

problems = []

patent_count = client.query('SELECT count() FROM db_patents.google_patents').result_rows[0][0]

for i in range(1, patent_count):
    result = client.query(f'SELECT Description, Abstract FROM db_patents.google_patents WHERE Id = {i}')
    solution = client.query(f'SELECT Title FROM db_patents.google_patents WHERE Id = {i}').result_rows[0][0]
    description = result.result_rows[0][0]
    abstract = result.result_rows[0][1]

    description_sentences = list(sentenize(description))
    abstract_sentences = list(sentenize(abstract))

    for desc_sentence in description_sentences:
        matches = list(orgparser.findall(desc_sentence.text))
        if matches and not problems:
            problems.append(desc_sentence.text)
        else:
            matches = list(orgparser1.findall(desc_sentence.text))
            if matches and not problems:
                problems.append(desc_sentence.text)


    for abstr_sentence in abstract_sentences:
        matches = list(orgparser.findall(abstr_sentence.text))
        if matches and not problems:
            problems.append(abstr_sentence.text)
        else:
            matches = list(orgparser1.findall(abstr_sentence.text))
            if matches and not problems:
                problems.append(abstr_sentence.text)


    row = [Id, problems, solution, i]
    data = [row]
    client.insert('google_problem_solution', data,
                  column_names=['Id', 'Problem', 'Solution', 'Patent_id'], database="db_patents")
    Id += 1
    problems.clear()

