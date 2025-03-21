"""
Скрипт для обработки теста эмоционального интеллекта
"""
import pandas as pd
import os

class BadOrderEI(Exception):
    """
    Исключение для обработки случая когда колонки не совпадают
    """
    pass


class BadValueEI(Exception):
    """
    Исключение для неправильных значений в вариантах ответов
    """
    pass

class BadCountColumnsEI(Exception):
    """
    Исключение для обработки случая если количество колонок не равно 46
    """
    pass


def calc_union_value_ei(row):
    """
    Функция для подсчета значения Общий уровень эмоционального интеллекта
    :param row: строка с ответами
    :return: число
    """
    value_forward = 0 # счетчик депрессии прямых ответов
    value_reverse = 0 # счетчик депрессии обратных ответов
    lst_forward = [1, 3, 4, 7, 9, 11, 13, 14, 15, 17, 19, 20, 21, 23, 24, 25, 26, 27, 28, 29, 32, 34, 36, 37]  # список ответов которые нужно считать простым сложением
    lst_reverse = [2, 5, 6, 8, 10, 12, 16, 18, 22, 30, 31, 33, 35, 38, 39, 40, 41, 42, 43, 44, 45, 46] # обратный подсчет

    for idx, value in enumerate(row):
        if idx + 1 in lst_forward:
            # print(f'Прямой подсчет {idx +1}') # Для проверки корректности
            value_forward += value
        elif idx +1 in lst_reverse:
            # print(f'Обратный подсчет {idx +1}')# Для проверки корректности
            if value == 0:
                value_reverse += 3
            elif value == 1:
                value_reverse += 2
            elif value == 2:
                value_reverse += 1
            elif value == 3:
                value_reverse += 0

    return value_forward + value_reverse



def calc_level_union_ei(value):
    """
    Функция для подсчета уровня общего эмоционального интеллекта
    :param value:
    :return:
    """
    if 0 <= value <= 71:
        return 'Очень низкое значение'
    elif 72 <= value <= 78:
        return 'Низкое значение'
    elif 79 <= value <= 92:
        return 'Среднее значение'
    elif 93 <= value <= 104:
        return 'Высокое значение'
    else:
        return 'Очень высокое значение'



def calc_sub_value_mp(row):
    """
    Функция для подсчета значения субшкалы МП
    :param row: строка с ответами
    :return: число
    """
    lst_mp = [1, 3, 11, 13, 20, 27, 29, 32, 34,38, 42, 46]

    value_forward = 0 # счетчик депрессии прямых ответов
    value_reverse = 0 # счетчик депрессии обратных ответов
    lst_forward = [1, 3, 4, 7, 9, 11, 13, 14, 15, 17, 19, 20, 21, 23, 24, 25, 26, 27, 28, 29, 32, 34, 36, 37]  # список ответов которые нужно считать простым сложением
    lst_reverse = [2, 5, 6, 8, 10, 12, 16, 18, 22, 30, 31, 33, 35, 38, 39, 40, 41, 42, 43, 44, 45, 46] # обратный подсчет

    for idx, value in enumerate(row):
        if idx +1 in lst_mp:
            if idx + 1 in lst_forward:
                # print(f'Прямой подсчет {idx +1}') # Для проверки корректности
                value_forward += value
            elif idx +1 in lst_reverse:
                # print(f'Обратный подсчет {idx +1}')# Для проверки корректности
                if value == 0:
                    value_reverse += 3
                elif value == 1:
                    value_reverse += 2
                elif value == 2:
                    value_reverse += 1
                elif value == 3:
                    value_reverse += 0

    return value_forward + value_reverse

def calc_level_sub_mp(value):
    """
    Функция для подсчета уровня субшкалы МП
    :param value:
    :return:
    """
    if 0 <= value <= 19:
        return 'Очень низкое значение'
    elif 20 <= value <= 22:
        return 'Низкое значение'
    elif 23 <= value <= 26:
        return 'Среднее значение'
    elif 27 <= value <= 30:
        return 'Высокое значение'
    else:
        return 'Очень высокое значение'


def calc_sub_value_mu(row):
    """
    Функция для подсчета значения субшкалы МУ
    :param row: строка с ответами
    :return: число
    """
    lst_check = [9, 15, 17, 24, 36, 2, 5, 30, 40, 44]

    value_forward = 0 # счетчик депрессии прямых ответов
    value_reverse = 0 # счетчик депрессии обратных ответов
    lst_forward = [1, 3, 4, 7, 9, 11, 13, 14, 15, 17, 19, 20, 21, 23, 24, 25, 26, 27, 28, 29, 32, 34, 36, 37]  # список ответов которые нужно считать простым сложением
    lst_reverse = [2, 5, 6, 8, 10, 12, 16, 18, 22, 30, 31, 33, 35, 38, 39, 40, 41, 42, 43, 44, 45, 46] # обратный подсчет

    for idx, value in enumerate(row):
        if idx +1 in lst_check:
            if idx + 1 in lst_forward:
                # print(f'Прямой подсчет {idx +1}') # Для проверки корректности
                value_forward += value
            elif idx +1 in lst_reverse:
                # print(f'Обратный подсчет {idx +1}')# Для проверки корректности
                if value == 0:
                    value_reverse += 3
                elif value == 1:
                    value_reverse += 2
                elif value == 2:
                    value_reverse += 1
                elif value == 3:
                    value_reverse += 0

    return value_forward + value_reverse

def calc_level_sub_mu(value):
    """
    Функция для подсчета уровня субшкалы МУ
    :param value:
    :return:
    """
    if 0 <= value <= 14:
        return 'Очень низкое значение'
    elif 15 <= value <= 17:
        return 'Низкое значение'
    elif 18 <= value <= 21:
        return 'Среднее значение'
    elif 22 <= value <= 24:
        return 'Высокое значение'
    else:
        return 'Очень высокое значение'


def calc_sub_value_vp(row):
    """
    Функция для подсчета значения субшкалы ВП
    :param row: строка с ответами
    :return: число
    """
    lst_check = [7, 14, 26, 8, 18, 22, 31, 35, 41, 45]

    value_forward = 0 # счетчик депрессии прямых ответов
    value_reverse = 0 # счетчик депрессии обратных ответов
    lst_forward = [1, 3, 4, 7, 9, 11, 13, 14, 15, 17, 19, 20, 21, 23, 24, 25, 26, 27, 28, 29, 32, 34, 36, 37]  # список ответов которые нужно считать простым сложением
    lst_reverse = [2, 5, 6, 8, 10, 12, 16, 18, 22, 30, 31, 33, 35, 38, 39, 40, 41, 42, 43, 44, 45, 46] # обратный подсчет

    for idx, value in enumerate(row):
        if idx +1 in lst_check:
            if idx + 1 in lst_forward:
                # print(f'Прямой подсчет {idx +1}') # Для проверки корректности
                value_forward += value
            elif idx +1 in lst_reverse:
                # print(f'Обратный подсчет {idx +1}')# Для проверки корректности
                if value == 0:
                    value_reverse += 3
                elif value == 1:
                    value_reverse += 2
                elif value == 2:
                    value_reverse += 1
                elif value == 3:
                    value_reverse += 0

    return value_forward + value_reverse

def calc_level_sub_vp(value):
    """
    Функция для подсчета уровня субшкалы ВП
    :param value:
    :return:
    """
    if 0 <= value <= 13:
        return 'Очень низкое значение'
    elif 14 <= value <= 16:
        return 'Низкое значение'
    elif 17 <= value <= 21:
        return 'Среднее значение'
    elif 22 <= value <= 25:
        return 'Высокое значение'
    else:
        return 'Очень высокое значение'

def calc_sub_value_vu(row):
    """
    Функция для подсчета значения субшкалы ВУ
    :param row: строка с ответами
    :return: число
    """
    lst_check = [4, 25, 28, 37,12, 33, 43]

    value_forward = 0 # счетчик депрессии прямых ответов
    value_reverse = 0 # счетчик депрессии обратных ответов
    lst_forward = [1, 3, 4, 7, 9, 11, 13, 14, 15, 17, 19, 20, 21, 23, 24, 25, 26, 27, 28, 29, 32, 34, 36, 37]  # список ответов которые нужно считать простым сложением
    lst_reverse = [2, 5, 6, 8, 10, 12, 16, 18, 22, 30, 31, 33, 35, 38, 39, 40, 41, 42, 43, 44, 45, 46] # обратный подсчет

    for idx, value in enumerate(row):
        if idx +1 in lst_check:
            if idx + 1 in lst_forward:
                # print(f'Прямой подсчет {idx +1}') # Для проверки корректности
                value_forward += value
            elif idx +1 in lst_reverse:
                # print(f'Обратный подсчет {idx +1}')# Для проверки корректности
                if value == 0:
                    value_reverse += 3
                elif value == 1:
                    value_reverse += 2
                elif value == 2:
                    value_reverse += 1
                elif value == 3:
                    value_reverse += 0

    return value_forward + value_reverse

def calc_level_sub_vu(value):
    """
    Функция для подсчета уровня субшкалы ВУ
    :param value:
    :return:
    """
    if 0 <= value <= 9:
        return 'Очень низкое значение'
    elif 10 <= value <= 12:
        return 'Низкое значение'
    elif 13 <= value <= 15:
        return 'Среднее значение'
    elif 16 <= value <= 17:
        return 'Высокое значение'
    else:
        return 'Очень высокое значение'


def calc_sub_value_va(row):
    """
    Функция для подсчета значения субшкалы ВЭ
    :param row: строка с ответами
    :return: число
    """
    lst_check = [19, 21, 23, 6, 10, 16, 39]

    value_forward = 0 # счетчик депрессии прямых ответов
    value_reverse = 0 # счетчик депрессии обратных ответов
    lst_forward = [1, 3, 4, 7, 9, 11, 13, 14, 15, 17, 19, 20, 21, 23, 24, 25, 26, 27, 28, 29, 32, 34, 36, 37]  # список ответов которые нужно считать простым сложением
    lst_reverse = [2, 5, 6, 8, 10, 12, 16, 18, 22, 30, 31, 33, 35, 38, 39, 40, 41, 42, 43, 44, 45, 46] # обратный подсчет

    for idx, value in enumerate(row):
        if idx +1 in lst_check:
            if idx + 1 in lst_forward:
                # print(f'Прямой подсчет {idx +1}') # Для проверки корректности
                value_forward += value
            elif idx +1 in lst_reverse:
                # print(f'Обратный подсчет {idx +1}')# Для проверки корректности
                if value == 0:
                    value_reverse += 3
                elif value == 1:
                    value_reverse += 2
                elif value == 2:
                    value_reverse += 1
                elif value == 3:
                    value_reverse += 0

    return value_forward + value_reverse

def calc_level_sub_va(value):
    """
    Функция для подсчета уровня субшкалы ВЭ
    :param value:
    :return:
    """
    if 0 <= value <= 6:
        return 'Очень низкое значение'
    elif 7 <= value <= 9:
        return 'Низкое значение'
    elif 10 <= value <= 12:
        return 'Среднее значение'
    elif 13 <= value <= 15:
        return 'Высокое значение'
    else:
        return 'Очень высокое значение'


def calc_level_mei(value):
    """
    Функция для подсчета уровня шкалы МЭИ
    :param value:
    :return:
    """
    if 0 <= value <= 34:
        return 'Очень низкое значение'
    elif 35 <= value <= 39:
        return 'Низкое значение'
    elif 40 <= value <= 46:
        return 'Среднее значение'
    elif 47 <= value <= 52:
        return 'Высокое значение'
    else:
        return 'Очень высокое значение'

def calc_level_vei(value):
    """
    Функция для подсчета уровня шкалы ВЭИ
    :param value:
    :return:
    """
    if 0 <= value <= 33:
        return 'Очень низкое значение'
    elif 34 <= value <= 38:
        return 'Низкое значение'
    elif 39 <= value <= 47:
        return 'Среднее значение'
    elif 48 <= value <= 53:
        return 'Высокое значение'
    else:
        return 'Очень высокое значение'


def calc_level_pa(value):
    """
    Функция для подсчета уровня шкалы ПЭ
    :param value:
    :return:
    """
    if 0 <= value <= 34:
        return 'Очень низкое значение'
    elif 35 <= value <= 39:
        return 'Низкое значение'
    elif 40 <= value <= 47:
        return 'Среднее значение'
    elif 48 <= value <= 53:
        return 'Высокое значение'
    else:
        return 'Очень высокое значение'


def calc_level_ua(value):
    """
    Функция для подсчета уровня шкалы УЭ
    :param value:
    :return:
    """
    if 0 <= value <= 33:
        return 'Очень низкое значение'
    elif 34 <= value <= 39:
        return 'Низкое значение'
    elif 40 <= value <= 47:
        return 'Среднее значение'
    elif 48 <= value <= 53:
        return 'Высокое значение'
    else:
        return 'Очень высокое значение'


def calc_stenain_mei(value):
    """
    Функция для подсчета стенайна шкаллы МЭИ
    :return:
    """
    if value <= 31:
        return 1
    elif 32 <= value <= 34:
        return 2
    elif 35 <= value <= 37:
        return 3
    elif 38 <= value <= 40:
        return 4
    elif 41 <= value <= 44:
        return 5
    elif 45 <= value <= 47:
        return 6
    elif 48 <= value <= 51:
        return 7
    elif 52 <= value <= 55:
        return 8
    else:
        return 9


def calc_stenain_vei(value):
    """
    Функция для подсчета стенайна шкаллы ВЭИ
    :param value:
    :return:
    """
    if value <= 28:
        return 1
    elif 29 <= value <= 32:
        return 2
    elif 33 <= value <= 36:
        return 3
    elif 37 <= value <= 40:
        return 4
    elif 41 <= value <= 44:
        return 5
    elif 45 <= value <= 48:
        return 6
    elif 49 <= value <= 53:
        return 7
    elif 54 <= value <= 57:
        return 8
    else:
        return 9


def calc_stenain_pa(value):
    """
    Функция для подсчета стенайна шкаллы ПЭ
    :param value:
    :return:
    """
    if value <= 31:
        return 1
    elif 32 <= value <= 34:
        return 2
    elif 35 <= value <= 37:
        return 3
    elif 38 <= value <= 40:
        return 4
    elif 41 <= value <= 44:
        return 5
    elif 45 <= value <= 47:
        return 6
    elif 48 <= value <= 51:
        return 7
    elif 52 <= value <= 56:
        return 8
    else:
        return 9

def calc_stenain_ua(value):
    """
    Функция для подсчета стенайна шкаллы ПЭ
    :param value:
    :return:
    """
    if value <= 29:
        return 1
    elif 30 <= value <= 32:
        return 2
    elif 33 <= value <= 36:
        return 3
    elif 37 <= value <= 40:
        return 4
    elif 41 <= value <= 44:
        return 5
    elif 45 <= value <= 47:
        return 6
    elif 48 <= value <= 51:
        return 7
    elif 52 <= value <= 56:
        return 8
    else:
        return 9






def processing_ei(base_df: pd.DataFrame, answers_df: pd.DataFrame):
    """
    Функция для обработки
    :param base_df: часть датафрейма с описательными колонками
    :param answers_df: часть датафрейма с ответами
    :param size: количество колонок которое должно быть в answers_df
    :param name_test: название теста
    :param threshold_base: количество колонок
    :param end_folder: конечная папка для сохранения
    """
    out_answer_df = base_df.copy()  # делаем копию для последующего соединения с сырыми ответами
    if len(answers_df.columns) != 46:  # проверяем количество колонок с вопросами
        raise BadCountColumnsEI

    # Словарь с проверочными данными
    lst_check_cols = ['Я замечаю, когда близкий человек переживает, даже если он (она) пытается это скрыть',
                      'Если человек на меня обижается, я не знаю, как восстановить с ним хорошие отношения',
                      'Мне легко догадаться о чувствах человека по выражению его лица',
                      'Я хорошо знаю, чем заняться, чтобы улучшить себе настроение',
                      'У меня обычно не получается повлиять на эмоциональное состояние своего собеседника',
                      'Когда я раздражаюсь, то не могу сдержаться, и говорю всё, что думаю',
                      'Я хорошо понимаю, почему мне нравятся или не нравятся те или иные люди',
                      'Я не сразу замечаю, когда начинаю злиться',
                      'Я умею улучшить настроение окружающих',
                      'Если я увлекаюсь разговором, то говорю слишком громко и активно жестикулирую',
                      'Я понимаю душевное состояние некоторых людей без слов',
                      'В экстремальной ситуации я не могу усилием воли взять себя в руки',
                      'Я легко понимаю мимику и жесты других людей',
                      'Когда я злюсь, я знаю, почему',
                      'Я знаю, как ободрить человека, находящегося в тяжелой ситуации',
                      'Окружающие считают меня слишком эмоциональным человеком',
                      'Я способен успокоить близких, когда они находятся в напряжённом состоянии',
                      'Мне бывает трудно описать, что я чувствую по отношению к другим',
                      'Если я смущаюсь при общении с незнакомыми людьми, то могу это скрыть',
                      'Глядя на человека, я легко могу понять его эмоциональное состояние',
                      'Я контролирую выражение чувств на своем лице',
                      'Бывает, что я не понимаю, почему испытываю то или иное чувство',
                      'В критических ситуациях я умею контролировать выражение своих эмоций',
                      'Если надо, я могу разозлить человека',
                      'Когда я испытываю положительные эмоции, я знаю, как поддержать это состояние',
                      'Как правило, я понимаю, какую эмоцию испытываю',
                      'Если собеседник пытается скрыть свои эмоции, я сразу чувствую это',
                      'Я знаю, как успокоиться, если я разозлился',
                      'Можно определить, что чувствует человек, просто прислушиваясь к звучанию его голоса',
                      'Я не умею управлять эмоциями других людей',
                      'Мне трудно отличить чувство вины от чувства стыда',
                      'Я умею точно угадывать, что чувствуют мои знакомые',
                      'Мне трудно справляться с плохим настроением',
                      'Если внимательно следить за выражением лица человека, то можно понять, какие эмоции он скрывает',
                      'Я не нахожу слов, чтобы описать свои чувства друзьям',
                      'Мне удаётся поддержать людей, которые делятся со мной своими переживаниями',
                      'Я умею контролировать свои эмоции',
                      'Если мой собеседник начинает раздражаться, я подчас замечаю это слишком поздно',
                      'По интонациям моего голоса легко догадаться о том, что я чувствую',
                      'Если близкий человек плачет, я теряюсь',
                      'Мне бывает весело или грустно без всякой причины',
                      'Мне трудно предвидеть смену настроения у окружающих меня людей',
                      'Я не умею преодолевать страх',
                      'Бывает, что я хочу поддержать человека, а он этого не чувствует, не понимает',
                      'У меня бывают чувства, которые я не могу точно определить',
                      'Я не понимаю, почему некоторые люди на меня обижаются',
                      ]
    # Проверяем порядок колонок
    order_main_columns = lst_check_cols  # порядок колонок и названий как должно быть
    order_temp_df_columns = list(answers_df.columns)  # порядок колонок проверяемого файла
    error_order_lst = []  # список для несовпадающих пар
    # Сравниваем попарно колонки
    for main, temp in zip(order_main_columns, order_temp_df_columns):
        if main != temp:
            error_order_lst.append(f'На месте колонки {main} находится колонка {temp}')
            error_order_message = ';'.join(error_order_lst)
    if len(error_order_lst) != 0:
        raise BadOrderEI

    # словарь для замены слов на числа
    dct_replace_value = {'совсем не согласен': 0,
                         'скорее не согласен': 1,
                         'скорее согласен': 2,
                         'полностью согласен': 3}

    valid_values = [0, 1, 2, 3]
    answers_df.replace(dct_replace_value, inplace=True)  # заменяем слова на цифры для подсчетов

    # Проверяем, есть ли значения, отличающиеся от указанных в списке
    mask = ~answers_df.isin(valid_values)

    # Получаем строки с отличающимися значениями
    result_check = answers_df[mask.any(axis=1)]
    if len(result_check) != 0:
        error_row = list(map(lambda x: x + 2, result_check.index))
        error_row = list(map(str, error_row))
        error_message = ';'.join(error_row)
        raise BadValueEI

    # Проводим подсчет
    # Общий уровень эмоционального интеллекта ОЭИ
    base_df['Значение_общего_ЭИ'] = answers_df.apply(calc_union_value_ei, axis=1)
    base_df['Значение_нормы_общего_ЭИ'] = '72-104 баллов'
    base_df['Уровень_общего_ЭИ'] = base_df['Значение_общего_ЭИ'].apply(calc_level_union_ei)

    # Субшкала МП Понимание чужих эмоций
    base_df['Значение_субшкалы_МП'] = answers_df.apply(calc_sub_value_mp, axis=1)
    base_df['Значение_нормы_МП'] = '20-30 баллов'
    base_df['Уровень_субшкалы_МП'] = base_df['Значение_субшкалы_МП'].apply(calc_level_sub_mp)

    # Субшкала МУ Управление чужими эмоциями
    base_df['Значение_субшкалы_МУ'] = answers_df.apply(calc_sub_value_mu, axis=1)
    base_df['Значение_нормы_МУ'] = '15-24 баллов'
    base_df['Уровень_субшкалы_МУ'] = base_df['Значение_субшкалы_МУ'].apply(calc_level_sub_mu)

    # Субшкала ВП Понимание своих эмоций
    base_df['Значение_субшкалы_ВП'] = answers_df.apply(calc_sub_value_vp, axis=1)
    base_df['Значение_нормы_ВП'] = '14-25 баллов'
    base_df['Уровень_субшкалы_ВП'] = base_df['Значение_субшкалы_ВП'].apply(calc_level_sub_vp)

    # Субшкала ВУ Управление своими эмоциями
    base_df['Значение_субшкалы_ВУ'] = answers_df.apply(calc_sub_value_vu, axis=1)
    base_df['Значение_нормы_ВУ'] = '10-17 баллов'
    base_df['Уровень_субшкалы_ВУ'] = base_df['Значение_субшкалы_ВУ'].apply(calc_level_sub_vu)

    # Субшкала ВЭ Контроль экспрессии
    base_df['Значение_субшкалы_ВЭ'] = answers_df.apply(calc_sub_value_va, axis=1)
    base_df['Значение_нормы_ВЭ'] = '7-15 баллов'
    base_df['Уровень_субшкалы_ВЭ'] = base_df['Значение_субшкалы_ВЭ'].apply(calc_level_sub_va)

    # Шкала МЭИ Межличностный эмоциональный интеллект
    base_df['Значение_шкалы_МЭИ'] = base_df['Значение_субшкалы_МП'] + base_df['Значение_субшкалы_МУ']
    base_df['Значение_нормы_МЭИ'] = '35-52 баллов'
    base_df['Уровень_шкалы_МЭИ'] = base_df['Значение_шкалы_МЭИ'].apply(calc_level_mei)
    base_df['Стенайн_шкалы_МЭИ'] = base_df['Значение_шкалы_МЭИ'].apply(calc_stenain_mei)


    # Шкала ВЭИ Внутриличностный эмоциональный интеллект
    base_df['Значение_шкалы_ВЭИ'] = base_df['Значение_субшкалы_ВП'] + base_df['Значение_субшкалы_ВУ'] + base_df['Значение_субшкалы_ВЭ']
    base_df['Значение_нормы_ВЭИ'] = '34-54 баллов'
    base_df['Уровень_шкалы_ВЭИ'] = base_df['Значение_шкалы_ВЭИ'].apply(calc_level_vei)
    base_df['Стенайн_шкалы_ВЭИ'] = base_df['Значение_шкалы_ВЭИ'].apply(calc_stenain_vei)

    # Шкала ПЭ Понимание эмоций
    base_df['Значение_шкалы_ПЭ'] = base_df['Значение_субшкалы_МП'] + base_df['Значение_субшкалы_ВП']
    base_df['Значение_нормы_ПЭ'] = '34-54 баллов'
    base_df['Уровень_шкалы_ПЭ'] = base_df['Значение_шкалы_ПЭ'].apply(calc_level_pa)
    base_df['Стенайн_шкалы_ПЭ'] = base_df['Значение_шкалы_ПЭ'].apply(calc_stenain_pa)

    # Шкала УЭ Управление эмоциями
    base_df['Значение_шкалы_УЭ'] =  base_df['Значение_субшкалы_МУ'] + base_df['Значение_субшкалы_ВУ'] + base_df['Значение_субшкалы_ВЭ']
    base_df['Значение_нормы_УЭ'] = '34-53 баллов'
    base_df['Уровень_шкалы_УЭ'] = base_df['Значение_шкалы_УЭ'].apply(calc_level_ua)
    base_df['Стенайн_шкалы_УЭ'] = base_df['Значение_шкалы_ПЭ'].apply(calc_stenain_ua)










    base_df.to_excel('dffds.xlsx')
    raise ZeroDivisionError
