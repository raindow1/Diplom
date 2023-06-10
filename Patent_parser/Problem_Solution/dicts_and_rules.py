from yargy.pipelines import morph_pipeline, caseless_pipeline
from yargy.interpretation import fact
from yargy import Parser, rule, and_, not_

Problem = fact(
    'Problem',
    ['target', 'add_word', 'second_word']
)

# Первый словарь ключевых слов для извлечения проблемы
TARGET = morph_pipeline([
    "цель",
    "способ",
    "изобретение",
    "задача",
    "модель",
    "использование"
    ])

# Словарь опциональных ключевых слов
ADD_WORD = caseless_pipeline([
    "предлагаеого",
    "настоящего",
    "данного",
    "решаемая"
    ])

# Второй словарь ключевых слов для извлечения проблемы
SECOND_WORD = morph_pipeline([
    "изобретения",
    "предназначено",
    "решения",
    "устройства"
    ])

# Второй словарь ключевых слов для извлечения проблемы по второму правилу
SECOND_WORD_ADD = morph_pipeline([
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

#Первое правило для извлечения проблемы из текста
ORGANIZATION = rule(TARGET.interpretation(Problem.target),
                    ADD_WORD.interpretation(Problem.add_word).optional(),
                    SECOND_WORD.interpretation(Problem.second_word))

#Второе правило для извлечения проблемы из текста
ORGANIZATION1 = rule(TARGET.interpretation(Problem.target),
                    ADD_WORD.interpretation(Problem.add_word).optional(),
                    SECOND_WORD_ADD.interpretation(Problem.second_word))