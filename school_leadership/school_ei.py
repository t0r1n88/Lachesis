"""
Скрипт для обработки теста эмоционального интеллекта
"""
import pandas as pd
from tkinter import messagebox
from lachesis_support_functions import round_mean,sort_name_class
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

def count_all_scale(df:pd.DataFrame, lst_cols:list,lst_index:list):
    """
    Функция для подсчета уровней по всем шкалам
    :param df: датарфейм
    :param lst_cols: список колонок по которым нужно вести обработку
    :param lst_index: список индексов
    :return:датафрейм
    """
    base_df = pd.DataFrame(index=lst_index) # базовый датафрейм с индексами
    for scale in lst_cols:
        if scale == 'ЭИ':
            scale_df = pd.pivot_table(df, index=f'Уровень_общего_ЭИ',
                                      values=f'Значение_общего_ЭИ',
                                      aggfunc='count')

            scale_df[f'Общий ЭИ % от общего'] = round(
                scale_df[f'Значение_общего_ЭИ'] / scale_df[f'Значение_общего_ЭИ'].sum(), 3) * 100
            scale_df.rename(columns={f'Значение_общего_ЭИ': f'Количество_ЭИ'}, inplace=True)

            # # Создаем суммирующую строку
            scale_df.loc['Итого'] = scale_df.sum()
        else:
            scale_df = pd.pivot_table(df, index=f'Уровень_шкалы_{scale}',
                                                      values=f'Значение_шкалы_{scale}',
                                                      aggfunc='count')

            scale_df[f'{scale} % от общего'] = round(
                scale_df[f'Значение_шкалы_{scale}'] / scale_df[f'Значение_шкалы_{scale}'].sum(),3) * 100
            scale_df.rename(columns={f'Значение_шкалы_{scale}':f'Количество_{scale}'},inplace=True)

            # # Создаем суммирующую строку
            scale_df.loc['Итого'] = scale_df.sum()


        base_df = base_df.join(scale_df)

    base_df = base_df.reset_index()
    base_df.rename(columns={'index':'Уровень эмоционального интеллекта'},inplace=True)
    return base_df







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
    """
    try:
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
        lst_error_answers = [] # список для хранения строк где найдены неправильные ответы

        for i in range(46):
            mask = ~answers_df.iloc[:,i].isin(valid_values) # проверяем на допустимые значения
            result_check = answers_df.iloc[:,i][mask]
            if len(result_check) != 0:
                error_row = list(map(lambda x: x + 2, result_check.index))
                error_row = list(map(str, error_row))
                error_row_lst = [f'В {i+1} вопросной колонке на строке {value}' for value in error_row]
                error_in_column = ','.join(error_row_lst)
                lst_error_answers.append(error_in_column)

        if len(lst_error_answers) !=0:
            error_message = ';'.join(lst_error_answers)
            raise BadValueEI

        # Проводим подсчет
        # Общий уровень эмоционального интеллекта ОЭИ
        base_df['Значение_общего_ЭИ'] = answers_df.apply(calc_union_value_ei, axis=1)
        base_df['Норма_общего_ЭИ'] = '72-104 баллов'
        base_df['Уровень_общего_ЭИ'] = base_df['Значение_общего_ЭИ'].apply(calc_level_union_ei)

        # Субшкала МП Понимание чужих эмоций
        base_df['Значение_субшкалы_МП'] = answers_df.apply(calc_sub_value_mp, axis=1)
        base_df['Норма_МП'] = '20-30 баллов'
        base_df['Уровень_субшкалы_МП'] = base_df['Значение_субшкалы_МП'].apply(calc_level_sub_mp)

        # Субшкала МУ Управление чужими эмоциями
        base_df['Значение_субшкалы_МУ'] = answers_df.apply(calc_sub_value_mu, axis=1)
        base_df['Норма_МУ'] = '15-24 баллов'
        base_df['Уровень_субшкалы_МУ'] = base_df['Значение_субшкалы_МУ'].apply(calc_level_sub_mu)

        # Субшкала ВП Понимание своих эмоций
        base_df['Значение_субшкалы_ВП'] = answers_df.apply(calc_sub_value_vp, axis=1)
        base_df['Норма_ВП'] = '14-25 баллов'
        base_df['Уровень_субшкалы_ВП'] = base_df['Значение_субшкалы_ВП'].apply(calc_level_sub_vp)

        # Субшкала ВУ Управление своими эмоциями
        base_df['Значение_субшкалы_ВУ'] = answers_df.apply(calc_sub_value_vu, axis=1)
        base_df['Норма_ВУ'] = '10-17 баллов'
        base_df['Уровень_субшкалы_ВУ'] = base_df['Значение_субшкалы_ВУ'].apply(calc_level_sub_vu)

        # Субшкала ВЭ Контроль экспрессии
        base_df['Значение_субшкалы_ВЭ'] = answers_df.apply(calc_sub_value_va, axis=1)
        base_df['Норма_ВЭ'] = '7-15 баллов'
        base_df['Уровень_субшкалы_ВЭ'] = base_df['Значение_субшкалы_ВЭ'].apply(calc_level_sub_va)

        # Шкала МЭИ Межличностный эмоциональный интеллект
        base_df['Значение_шкалы_МЭИ'] = base_df['Значение_субшкалы_МП'] + base_df['Значение_субшкалы_МУ']
        base_df['Норма_МЭИ'] = '35-52 баллов'
        base_df['Уровень_шкалы_МЭИ'] = base_df['Значение_шкалы_МЭИ'].apply(calc_level_mei)
        base_df['Стенайн_шкалы_МЭИ'] = base_df['Значение_шкалы_МЭИ'].apply(calc_stenain_mei)


        # Шкала ВЭИ Внутриличностный эмоциональный интеллект
        base_df['Значение_шкалы_ВЭИ'] = base_df['Значение_субшкалы_ВП'] + base_df['Значение_субшкалы_ВУ'] + base_df['Значение_субшкалы_ВЭ']
        base_df['Норма_ВЭИ'] = '34-54 баллов'
        base_df['Уровень_шкалы_ВЭИ'] = base_df['Значение_шкалы_ВЭИ'].apply(calc_level_vei)
        base_df['Стенайн_шкалы_ВЭИ'] = base_df['Значение_шкалы_ВЭИ'].apply(calc_stenain_vei)

        # Шкала ПЭ Понимание эмоций
        base_df['Значение_шкалы_ПЭ'] = base_df['Значение_субшкалы_МП'] + base_df['Значение_субшкалы_ВП']
        base_df['Норма_ПЭ'] = '34-54 баллов'
        base_df['Уровень_шкалы_ПЭ'] = base_df['Значение_шкалы_ПЭ'].apply(calc_level_pa)
        base_df['Стенайн_шкалы_ПЭ'] = base_df['Значение_шкалы_ПЭ'].apply(calc_stenain_pa)

        # Шкала УЭ Управление эмоциями
        base_df['Значение_шкалы_УЭ'] =  base_df['Значение_субшкалы_МУ'] + base_df['Значение_субшкалы_ВУ'] + base_df['Значение_субшкалы_ВЭ']
        base_df['Норма_УЭ'] = '34-53 баллов'
        base_df['Уровень_шкалы_УЭ'] = base_df['Значение_шкалы_УЭ'].apply(calc_level_ua)
        base_df['Стенайн_шкалы_УЭ'] = base_df['Значение_шкалы_ПЭ'].apply(calc_stenain_ua)

        # Создаем датафрейм для создания части в общий датафрейм
        part_df = pd.DataFrame(columns=['Значение_шкалы_ОЭИ','Уровень_шкалы_ОЭИ','Значение_шкалы_МЭИ','Уровень_шкалы_МЭИ','Значение_шкалы_ВЭИ','Уровень_шкалы_ВЭИ','Значение_шкалы_ПЭ','Уровень_шкалы_ПЭ','Значение_шкалы_УЭ','Уровень_шкалы_УЭ'])

        part_df['Значение_шкалы_ОЭИ'] = base_df['Значение_общего_ЭИ']
        part_df['Уровень_шкалы_ОЭИ'] = base_df['Уровень_общего_ЭИ']


        part_df['Значение_шкалы_МЭИ'] = base_df['Значение_шкалы_МЭИ']
        part_df['Уровень_шкалы_МЭИ'] = base_df['Уровень_шкалы_МЭИ']

        part_df['Значение_шкалы_ВЭИ'] = base_df['Значение_шкалы_ВЭИ']
        part_df['Уровень_шкалы_ВЭИ'] = base_df['Уровень_шкалы_ВЭИ']

        part_df['Значение_шкалы_ПЭ'] = base_df['Значение_шкалы_ПЭ']
        part_df['Уровень_шкалы_ПЭ'] = base_df['Уровень_шкалы_ПЭ']

        part_df['Значение_шкалы_УЭ'] = base_df['Значение_шкалы_УЭ']
        part_df['Уровень_шкалы_УЭ'] = base_df['Уровень_шкалы_УЭ']



        base_df.sort_values(by='Значение_общего_ЭИ', ascending=False, inplace=True)  # сортируем

        # Делаем сводную таблицу по курсу
        mean_course_oei_df = pd.pivot_table(base_df, index=['Номер_класса'],
                                            values=['Значение_общего_ЭИ'],
                                            aggfunc=round_mean)
        mean_course_oei_df.reset_index(inplace=True)
        mean_course_oei_df['Уровень_общего_ЭИ'] = mean_course_oei_df['Значение_общего_ЭИ'].apply(
            calc_level_union_ei)  # считаем уровень

        # делаем сводную по курсу и ОЭИ
        count_course_oei_df = pd.pivot_table(base_df, index=['Номер_класса'],
                                                  columns='Уровень_общего_ЭИ',
                                                  values='Значение_общего_ЭИ',
                                                  aggfunc='count', margins=True, margins_name='Итого')
        count_course_oei_df.reset_index(inplace=True)
        count_course_oei_df = count_course_oei_df.reindex(
            columns=['Номер_класса', 'Очень низкое значение', 'Низкое значение', 'Среднее значение',
                     'Высокое значение', 'Очень высокое значение', 'Итого'])

        count_course_oei_df['% Очень низкое значение от общего'] = round(
            count_course_oei_df['Очень низкое значение'] / count_course_oei_df['Итого'], 2) * 100

        count_course_oei_df['% Низкое значение от общего'] = round(
            count_course_oei_df['Низкое значение'] /
            count_course_oei_df['Итого'], 2) * 100

        count_course_oei_df['% Среднее значение от общего'] = round(
            count_course_oei_df['Среднее значение'] /
            count_course_oei_df['Итого'], 2) * 100

        count_course_oei_df['% Высокое значение от общего'] = round(
            count_course_oei_df['Высокое значение'] / count_course_oei_df['Итого'], 2) * 100

        count_course_oei_df['% Очень высокое значение от общего'] = round(
            count_course_oei_df['Очень высокое значение'] / count_course_oei_df['Итого'], 2) * 100



        # Делаем сводную таблицу по курсу МЭИ
        mean_course_mei_df = pd.pivot_table(base_df, index=['Номер_класса'],
                                            values=['Значение_шкалы_МЭИ'],
                                            aggfunc=round_mean)
        mean_course_mei_df.reset_index(inplace=True)
        mean_course_mei_df['Уровень_шкалы_МЭИ'] = mean_course_mei_df['Значение_шкалы_МЭИ'].apply(
            calc_level_mei)  # считаем уровень

        # делаем сводную по курсу
        count_course_mei_df = pd.pivot_table(base_df, index=['Номер_класса'],
                                                  columns='Уровень_шкалы_МЭИ',
                                                  values='Значение_шкалы_МЭИ',
                                                  aggfunc='count', margins=True, margins_name='Итого')
        count_course_mei_df.reset_index(inplace=True)
        count_course_mei_df = count_course_mei_df.reindex(
            columns=['Номер_класса', 'Очень низкое значение', 'Низкое значение', 'Среднее значение',
                     'Высокое значение', 'Очень высокое значение', 'Итого'])

        count_course_mei_df['% Очень низкое значение  от общего'] = round(
            count_course_mei_df['Очень низкое значение'] / count_course_mei_df['Итого'], 2) * 100

        count_course_mei_df['% Низкое значение от общего'] = round(
            count_course_mei_df['Низкое значение'] /
            count_course_mei_df['Итого'], 2) * 100

        count_course_mei_df['% Среднее значение от общего'] = round(
            count_course_mei_df['Среднее значение'] /
            count_course_mei_df['Итого'], 2) * 100

        count_course_mei_df['% Высокое значение от общего'] = round(
            count_course_mei_df['Высокое значение'] / count_course_mei_df['Итого'], 2) * 100
        count_course_mei_df['% Очень высокое значение от общего'] = round(
            count_course_mei_df['Очень высокое значение'] / count_course_mei_df['Итого'], 2) * 100


        # ВЭИ
        mean_course_vei_df = pd.pivot_table(base_df, index=['Номер_класса'],
                                            values=['Значение_шкалы_ВЭИ'],
                                            aggfunc=round_mean)
        mean_course_vei_df.reset_index(inplace=True)
        mean_course_vei_df['Уровень_шкалы_ВЭИ'] = mean_course_vei_df['Значение_шкалы_ВЭИ'].apply(
            calc_level_vei)  # считаем уровень

        # делаем сводную по курсу
        count_course_vei_df = pd.pivot_table(base_df, index=['Номер_класса'],
                                                  columns='Уровень_шкалы_ВЭИ',
                                                  values='Значение_шкалы_ВЭИ',
                                                  aggfunc='count', margins=True, margins_name='Итого')
        count_course_vei_df.reset_index(inplace=True)
        count_course_vei_df = count_course_vei_df.reindex(
            columns=['Номер_класса', 'Очень низкое значение', 'Низкое значение', 'Среднее значение',
                     'Высокое значение', 'Очень высокое значение', 'Итого'])

        count_course_vei_df['% Очень низкое значение  от общего'] = round(
            count_course_vei_df['Очень низкое значение'] / count_course_vei_df['Итого'], 2) * 100

        count_course_vei_df['% Низкое значение от общего'] = round(
            count_course_vei_df['Низкое значение'] /
            count_course_vei_df['Итого'], 2) * 100

        count_course_vei_df['% Среднее значение от общего'] = round(
            count_course_vei_df['Среднее значение'] /
            count_course_vei_df['Итого'], 2) * 100

        count_course_vei_df['% Высокое значение от общего'] = round(
            count_course_vei_df['Высокое значение'] / count_course_vei_df['Итого'], 2) * 100
        count_course_vei_df['% Очень высокое значение от общего'] = round(
            count_course_vei_df['Очень высокое значение'] / count_course_vei_df['Итого'], 2) * 100



        # Делаем сводную таблицу по курсу среднее ПЭ
        mean_course_pa_df = pd.pivot_table(base_df, index=['Номер_класса'],
                                           values=['Значение_шкалы_ПЭ'],
                                           aggfunc=round_mean)
        mean_course_pa_df.reset_index(inplace=True)
        mean_course_pa_df['Уровень_шкалы_ПЭ'] = mean_course_pa_df['Значение_шкалы_ПЭ'].apply(
            calc_level_pa)  # считаем уровень

        # делаем сводную по курсу и количеству ПЭ
        count_course_pa_df = pd.pivot_table(base_df, index=['Номер_класса'],
                                            columns='Уровень_шкалы_ПЭ',
                                            values='Значение_шкалы_ПЭ',
                                            aggfunc='count', margins=True, margins_name='Итого')
        count_course_pa_df.reset_index(inplace=True)
        count_course_pa_df = count_course_pa_df.reindex(
            columns=['Номер_класса', 'Очень низкое значение', 'Низкое значение', 'Среднее значение',
                     'Высокое значение', 'Очень высокое значение', 'Итого'])

        count_course_pa_df['% Очень низкое значение  от общего'] = round(
            count_course_pa_df['Очень низкое значение'] / count_course_pa_df['Итого'], 2) * 100

        count_course_pa_df['% Низкое значение от общего'] = round(
            count_course_pa_df['Низкое значение'] /
            count_course_pa_df['Итого'], 2) * 100

        count_course_pa_df['% Среднее значение от общего'] = round(
            count_course_pa_df['Среднее значение'] /
            count_course_pa_df['Итого'], 2) * 100

        count_course_pa_df['% Высокое значение от общего'] = round(
            count_course_pa_df['Высокое значение'] / count_course_pa_df['Итого'], 2) * 100
        count_course_pa_df['% Очень высокое значение от общего'] = round(
            count_course_pa_df['Очень высокое значение'] / count_course_pa_df['Итого'], 2) * 100




        # Делаем сводную таблицу по курсу среднее УЭ
        mean_course_ua_df = pd.pivot_table(base_df, index=['Номер_класса'],
                                           values=['Значение_шкалы_УЭ'],
                                           aggfunc=round_mean)
        mean_course_ua_df.reset_index(inplace=True)
        mean_course_ua_df['Уровень_шкалы_УЭ'] = mean_course_ua_df['Значение_шкалы_УЭ'].apply(
            calc_level_ua)  # считаем уровень

        # делаем сводную по курсу и количеству ПЭ
        count_course_ua_df = pd.pivot_table(base_df, index=['Номер_класса'],
                                            columns='Уровень_шкалы_УЭ',
                                            values='Значение_шкалы_УЭ',
                                            aggfunc='count', margins=True, margins_name='Итого')
        count_course_ua_df.reset_index(inplace=True)
        count_course_ua_df = count_course_ua_df.reindex(
            columns=['Номер_класса', 'Очень низкое значение', 'Низкое значение', 'Среднее значение',
                     'Высокое значение', 'Очень высокое значение', 'Итого'])

        count_course_ua_df['% Очень низкое значение  от общего'] = round(
            count_course_ua_df['Очень низкое значение'] / count_course_ua_df['Итого'], 2) * 100

        count_course_ua_df['% Низкое значение от общего'] = round(
            count_course_ua_df['Низкое значение'] /
            count_course_ua_df['Итого'], 2) * 100

        count_course_ua_df['% Среднее значение от общего'] = round(
            count_course_ua_df['Среднее значение'] /
            count_course_ua_df['Итого'], 2) * 100

        count_course_ua_df['% Высокое значение от общего'] = round(
            count_course_ua_df['Высокое значение'] / count_course_ua_df['Итого'], 2) * 100
        count_course_ua_df['% Очень высокое значение от общего'] = round(
            count_course_ua_df['Очень высокое значение'] / count_course_ua_df['Итого'], 2) * 100

        """
        Своды  по курсу и полу
        """
        # ОЭИ
        mean_course_sex_oei_df = pd.pivot_table(base_df, index=['Номер_класса', 'Пол'],
                                                values=['Значение_общего_ЭИ'],
                                                aggfunc=round_mean)
        mean_course_sex_oei_df.reset_index(inplace=True)
        mean_course_sex_oei_df['Уровень_общего_ЭИ'] = mean_course_sex_oei_df['Значение_общего_ЭИ'].apply(
            calc_level_union_ei)  # считаем уровень

        # делаем сводную по курсу и количеству ПЭ
        count_course_sex_oei_df = pd.pivot_table(base_df, index=['Номер_класса', 'Пол'],
                                                 columns='Уровень_общего_ЭИ',
                                                 values='Значение_общего_ЭИ',
                                                 aggfunc='count', margins=True, margins_name='Итого')
        count_course_sex_oei_df.reset_index(inplace=True)
        count_course_sex_oei_df = count_course_sex_oei_df.reindex(
            columns=['Номер_класса', 'Пол', 'Очень низкое значение', 'Низкое значение', 'Среднее значение',
                     'Высокое значение', 'Очень высокое значение', 'Итого'])

        count_course_sex_oei_df['% Очень низкое значение  от общего'] = round(
            count_course_sex_oei_df['Очень низкое значение'] / count_course_sex_oei_df['Итого'], 2) * 100

        count_course_sex_oei_df['% Низкое значение от общего'] = round(
            count_course_sex_oei_df['Низкое значение'] /
            count_course_sex_oei_df['Итого'], 2) * 100

        count_course_sex_oei_df['% Среднее значение от общего'] = round(
            count_course_sex_oei_df['Среднее значение'] /
            count_course_sex_oei_df['Итого'], 2) * 100

        count_course_sex_oei_df['% Высокое значение от общего'] = round(
            count_course_sex_oei_df['Высокое значение'] / count_course_sex_oei_df['Итого'], 2) * 100
        count_course_sex_oei_df['% Очень высокое значение от общего'] = round(
            count_course_sex_oei_df['Очень высокое значение'] / count_course_sex_oei_df['Итого'], 2) * 100

        # МЭИ
        mean_course_sex_mei_df = pd.pivot_table(base_df, index=['Номер_класса', 'Пол'],
                                                values=['Значение_шкалы_МЭИ'],
                                                aggfunc=round_mean)
        mean_course_sex_mei_df.reset_index(inplace=True)
        mean_course_sex_mei_df['Уровень_шкалы_МЭИ'] = mean_course_sex_mei_df['Значение_шкалы_МЭИ'].apply(
            calc_level_union_ei)  # считаем уровень

        # делаем сводную по курсу и количеству ПЭ
        count_course_sex_mei_df = pd.pivot_table(base_df, index=['Номер_класса', 'Пол'],
                                                 columns='Уровень_шкалы_МЭИ',
                                                 values='Значение_шкалы_МЭИ',
                                                 aggfunc='count', margins=True, margins_name='Итого')
        count_course_sex_mei_df.reset_index(inplace=True)
        count_course_sex_mei_df = count_course_sex_mei_df.reindex(
            columns=['Номер_класса', 'Пол', 'Очень низкое значение', 'Низкое значение', 'Среднее значение',
                     'Высокое значение', 'Очень высокое значение', 'Итого'])

        count_course_sex_mei_df['% Очень низкое значение  от общего'] = round(
            count_course_sex_mei_df['Очень низкое значение'] / count_course_sex_mei_df['Итого'], 2) * 100

        count_course_sex_mei_df['% Низкое значение от общего'] = round(
            count_course_sex_mei_df['Низкое значение'] /
            count_course_sex_mei_df['Итого'], 2) * 100

        count_course_sex_mei_df['% Среднее значение от общего'] = round(
            count_course_sex_mei_df['Среднее значение'] /
            count_course_sex_mei_df['Итого'], 2) * 100

        count_course_sex_mei_df['% Высокое значение от общего'] = round(
            count_course_sex_mei_df['Высокое значение'] / count_course_sex_mei_df['Итого'], 2) * 100
        count_course_sex_mei_df['% Очень высокое значение от общего'] = round(
            count_course_sex_mei_df['Очень высокое значение'] / count_course_sex_mei_df['Итого'], 2) * 100

        # ВЭИ
        mean_course_sex_vei_df = pd.pivot_table(base_df, index=['Номер_класса', 'Пол'],
                                                values=['Значение_шкалы_ВЭИ'],
                                                aggfunc=round_mean)
        mean_course_sex_vei_df.reset_index(inplace=True)
        mean_course_sex_vei_df['Уровень_шкалы_ВЭИ'] = mean_course_sex_vei_df['Значение_шкалы_ВЭИ'].apply(
            calc_level_union_ei)  # считаем уровень

        # делаем сводную по курсу и количеству ПЭ
        count_course_sex_vei_df = pd.pivot_table(base_df, index=['Номер_класса', 'Пол'],
                                                 columns='Уровень_шкалы_ВЭИ',
                                                 values='Значение_шкалы_ВЭИ',
                                                 aggfunc='count', margins=True, margins_name='Итого')
        count_course_sex_vei_df.reset_index(inplace=True)
        count_course_sex_vei_df = count_course_sex_vei_df.reindex(
            columns=['Номер_класса', 'Пол', 'Очень низкое значение', 'Низкое значение', 'Среднее значение',
                     'Высокое значение', 'Очень высокое значение', 'Итого'])

        count_course_sex_vei_df['% Очень низкое значение  от общего'] = round(
            count_course_sex_vei_df['Очень низкое значение'] / count_course_sex_vei_df['Итого'], 2) * 100

        count_course_sex_vei_df['% Низкое значение от общего'] = round(
            count_course_sex_vei_df['Низкое значение'] /
            count_course_sex_vei_df['Итого'], 2) * 100

        count_course_sex_vei_df['% Среднее значение от общего'] = round(
            count_course_sex_vei_df['Среднее значение'] /
            count_course_sex_vei_df['Итого'], 2) * 100

        count_course_sex_vei_df['% Высокое значение от общего'] = round(
            count_course_sex_vei_df['Высокое значение'] / count_course_sex_vei_df['Итого'], 2) * 100
        count_course_sex_vei_df['% Очень высокое значение от общего'] = round(
            count_course_sex_vei_df['Очень высокое значение'] / count_course_sex_vei_df['Итого'], 2) * 100


        # ПЭ
        mean_course_sex_pa_df = pd.pivot_table(base_df, index=['Номер_класса', 'Пол'],
                                                values=['Значение_шкалы_ПЭ'],
                                                aggfunc=round_mean)
        mean_course_sex_pa_df.reset_index(inplace=True)
        mean_course_sex_pa_df['Уровень_шкалы_ПЭ'] = mean_course_sex_pa_df['Значение_шкалы_ПЭ'].apply(
            calc_level_union_ei)  # считаем уровень

        # делаем сводную по курсу и количеству ПЭ
        count_course_sex_pa_df = pd.pivot_table(base_df, index=['Номер_класса', 'Пол'],
                                                 columns='Уровень_шкалы_ПЭ',
                                                 values='Значение_шкалы_ПЭ',
                                                 aggfunc='count', margins=True, margins_name='Итого')
        count_course_sex_pa_df.reset_index(inplace=True)
        count_course_sex_pa_df = count_course_sex_pa_df.reindex(
            columns=['Номер_класса', 'Пол', 'Очень низкое значение', 'Низкое значение', 'Среднее значение',
                     'Высокое значение', 'Очень высокое значение', 'Итого'])

        count_course_sex_pa_df['% Очень низкое значение  от общего'] = round(
            count_course_sex_pa_df['Очень низкое значение'] / count_course_sex_pa_df['Итого'], 2) * 100

        count_course_sex_pa_df['% Низкое значение от общего'] = round(
            count_course_sex_pa_df['Низкое значение'] /
            count_course_sex_pa_df['Итого'], 2) * 100

        count_course_sex_pa_df['% Среднее значение от общего'] = round(
            count_course_sex_pa_df['Среднее значение'] /
            count_course_sex_pa_df['Итого'], 2) * 100

        count_course_sex_pa_df['% Высокое значение от общего'] = round(
            count_course_sex_pa_df['Высокое значение'] / count_course_sex_pa_df['Итого'], 2) * 100
        count_course_sex_pa_df['% Очень высокое значение от общего'] = round(
            count_course_sex_pa_df['Очень высокое значение'] / count_course_sex_pa_df['Итого'], 2) * 100

        # УЭ
        mean_course_sex_ua_df = pd.pivot_table(base_df, index=['Номер_класса', 'Пол'],
                                                values=['Значение_шкалы_УЭ'],
                                                aggfunc=round_mean)
        mean_course_sex_ua_df.reset_index(inplace=True)
        mean_course_sex_ua_df['Уровень_шкалы_УЭ'] = mean_course_sex_ua_df['Значение_шкалы_УЭ'].apply(
            calc_level_union_ei)  # считаем уровень

        # делаем сводную по курсу и количеству ПЭ
        count_course_sex_ua_df = pd.pivot_table(base_df, index=['Номер_класса', 'Пол'],
                                                 columns='Уровень_шкалы_УЭ',
                                                 values='Значение_шкалы_УЭ',
                                                 aggfunc='count', margins=True, margins_name='Итого')
        count_course_sex_ua_df.reset_index(inplace=True)
        count_course_sex_ua_df = count_course_sex_ua_df.reindex(
            columns=['Номер_класса', 'Пол', 'Очень низкое значение', 'Низкое значение', 'Среднее значение',
                     'Высокое значение', 'Очень высокое значение', 'Итого'])

        count_course_sex_ua_df['% Очень низкое значение  от общего'] = round(
            count_course_sex_ua_df['Очень низкое значение'] / count_course_sex_ua_df['Итого'], 2) * 100

        count_course_sex_ua_df['% Низкое значение от общего'] = round(
            count_course_sex_ua_df['Низкое значение'] /
            count_course_sex_ua_df['Итого'], 2) * 100

        count_course_sex_ua_df['% Среднее значение от общего'] = round(
            count_course_sex_ua_df['Среднее значение'] /
            count_course_sex_ua_df['Итого'], 2) * 100

        count_course_sex_ua_df['% Высокое значение от общего'] = round(
            count_course_sex_ua_df['Высокое значение'] / count_course_sex_ua_df['Итого'], 2) * 100
        count_course_sex_ua_df['% Очень высокое значение от общего'] = round(
            count_course_sex_ua_df['Очень высокое значение'] / count_course_sex_ua_df['Итого'], 2) * 100

        """
        Делаем своды по группам
        """
        # Делаем сводную таблицу по Группе
        mean_group_oei_df = pd.pivot_table(base_df, index=['Класс'],
                                            values=['Значение_общего_ЭИ'],
                                            aggfunc=round_mean)
        mean_group_oei_df.reset_index(inplace=True)
        mean_group_oei_df['Уровень_общего_ЭИ'] = mean_group_oei_df['Значение_общего_ЭИ'].apply(
            calc_level_union_ei)  # считаем уровень
        mean_group_oei_df.sort_values(by='Класс', key=lambda x: x.map(sort_name_class), inplace=True)  # сортируем

        # делаем сводную по Групе и ОЭИ
        count_group_oei_df = pd.pivot_table(base_df, index=['Класс'],
                                                  columns='Уровень_общего_ЭИ',
                                                  values='Значение_общего_ЭИ',
                                                  aggfunc='count', margins=True, margins_name='Итого')
        count_group_oei_df.reset_index(inplace=True)
        count_group_oei_df = count_group_oei_df.reindex(
            columns=['Класс', 'Очень низкое значение', 'Низкое значение', 'Среднее значение',
                     'Высокое значение', 'Очень высокое значение', 'Итого'])

        count_group_oei_df['% Очень низкое значение от общего'] = round(
            count_group_oei_df['Очень низкое значение'] / count_group_oei_df['Итого'], 2) * 100

        count_group_oei_df['% Низкое значение от общего'] = round(
            count_group_oei_df['Низкое значение'] /
            count_group_oei_df['Итого'], 2) * 100

        count_group_oei_df['% Среднее значение от общего'] = round(
            count_group_oei_df['Среднее значение'] /
            count_group_oei_df['Итого'], 2) * 100

        count_group_oei_df['% Высокое значение от общего'] = round(
            count_group_oei_df['Высокое значение'] / count_group_oei_df['Итого'], 2) * 100

        count_group_oei_df['% Очень высокое значение от общего'] = round(
            count_group_oei_df['Очень высокое значение'] / count_group_oei_df['Итого'], 2) * 100

        part_svod_df = count_group_oei_df.iloc[:-1:]
        part_svod_df.sort_values(by='Класс', key=lambda x: x.map(sort_name_class), inplace=True)  # сортируем
        itog_svod_df = count_group_oei_df.iloc[-1:]
        count_group_oei_df = pd.concat([part_svod_df, itog_svod_df])



        # Делаем сводную таблицу по Классу МЭИ
        mean_group_mei_df = pd.pivot_table(base_df, index=['Класс'],
                                            values=['Значение_шкалы_МЭИ'],
                                            aggfunc=round_mean)
        mean_group_mei_df.reset_index(inplace=True)
        mean_group_mei_df['Уровень_шкалы_МЭИ'] = mean_group_mei_df['Значение_шкалы_МЭИ'].apply(
            calc_level_mei)  # считаем уровень
        mean_group_mei_df.sort_values(by='Класс', key=lambda x: x.map(sort_name_class), inplace=True)  # сортируем

        # делаем сводную по Группе
        count_group_mei_df = pd.pivot_table(base_df, index=['Класс'],
                                                  columns='Уровень_шкалы_МЭИ',
                                                  values='Значение_шкалы_МЭИ',
                                                  aggfunc='count', margins=True, margins_name='Итого')
        count_group_mei_df.reset_index(inplace=True)
        count_group_mei_df = count_group_mei_df.reindex(
            columns=['Класс', 'Очень низкое значение', 'Низкое значение', 'Среднее значение',
                     'Высокое значение', 'Очень высокое значение', 'Итого'])

        count_group_mei_df['% Очень низкое значение  от общего'] = round(
            count_group_mei_df['Очень низкое значение'] / count_group_mei_df['Итого'], 2) * 100

        count_group_mei_df['% Низкое значение от общего'] = round(
            count_group_mei_df['Низкое значение'] /
            count_group_mei_df['Итого'], 2) * 100

        count_group_mei_df['% Среднее значение от общего'] = round(
            count_group_mei_df['Среднее значение'] /
            count_group_mei_df['Итого'], 2) * 100

        count_group_mei_df['% Высокое значение от общего'] = round(
            count_group_mei_df['Высокое значение'] / count_group_mei_df['Итого'], 2) * 100
        count_group_mei_df['% Очень высокое значение от общего'] = round(
            count_group_mei_df['Очень высокое значение'] / count_group_mei_df['Итого'], 2) * 100

        part_svod_df = count_group_mei_df.iloc[:-1:]
        part_svod_df.sort_values(by='Класс', key=lambda x: x.map(sort_name_class), inplace=True)  # сортируем
        itog_svod_df = count_group_mei_df.iloc[-1:]
        count_group_mei_df = pd.concat([part_svod_df, itog_svod_df])


        # ВЭИ
        mean_group_vei_df = pd.pivot_table(base_df, index=['Класс'],
                                            values=['Значение_шкалы_ВЭИ'],
                                            aggfunc=round_mean)
        mean_group_vei_df.reset_index(inplace=True)
        mean_group_vei_df['Уровень_шкалы_ВЭИ'] = mean_group_vei_df['Значение_шкалы_ВЭИ'].apply(
            calc_level_vei)  # считаем уровень
        mean_group_vei_df.sort_values(by='Класс', key=lambda x: x.map(sort_name_class), inplace=True)  # сортируем

        # делаем сводную по Группе
        count_group_vei_df = pd.pivot_table(base_df, index=['Класс'],
                                                  columns='Уровень_шкалы_ВЭИ',
                                                  values='Значение_шкалы_ВЭИ',
                                                  aggfunc='count', margins=True, margins_name='Итого')
        count_group_vei_df.reset_index(inplace=True)
        count_group_vei_df = count_group_vei_df.reindex(
            columns=['Класс', 'Очень низкое значение', 'Низкое значение', 'Среднее значение',
                     'Высокое значение', 'Очень высокое значение', 'Итого'])

        count_group_vei_df['% Очень низкое значение  от общего'] = round(
            count_group_vei_df['Очень низкое значение'] / count_group_vei_df['Итого'], 2) * 100

        count_group_vei_df['% Низкое значение от общего'] = round(
            count_group_vei_df['Низкое значение'] /
            count_group_vei_df['Итого'], 2) * 100

        count_group_vei_df['% Среднее значение от общего'] = round(
            count_group_vei_df['Среднее значение'] /
            count_group_vei_df['Итого'], 2) * 100

        count_group_vei_df['% Высокое значение от общего'] = round(
            count_group_vei_df['Высокое значение'] / count_group_vei_df['Итого'], 2) * 100
        count_group_vei_df['% Очень высокое значение от общего'] = round(
            count_group_vei_df['Очень высокое значение'] / count_group_vei_df['Итого'], 2) * 100

        part_svod_df = count_group_vei_df.iloc[:-1:]
        part_svod_df.sort_values(by='Класс', key=lambda x: x.map(sort_name_class), inplace=True)  # сортируем
        itog_svod_df = count_group_vei_df.iloc[-1:]
        count_group_vei_df = pd.concat([part_svod_df, itog_svod_df])



        # Делаем сводную таблицу по Группе среднее ПЭ
        mean_group_pa_df = pd.pivot_table(base_df, index=['Класс'],
                                           values=['Значение_шкалы_ПЭ'],
                                           aggfunc=round_mean)
        mean_group_pa_df.reset_index(inplace=True)
        mean_group_pa_df['Уровень_шкалы_ПЭ'] = mean_group_pa_df['Значение_шкалы_ПЭ'].apply(
            calc_level_pa)  # считаем уровень
        mean_group_pa_df.sort_values(by='Класс', key=lambda x: x.map(sort_name_class), inplace=True)  # сортируем

        # делаем сводную по Группе и количеству ПЭ
        count_group_pa_df = pd.pivot_table(base_df, index=['Класс'],
                                            columns='Уровень_шкалы_ПЭ',
                                            values='Значение_шкалы_ПЭ',
                                            aggfunc='count', margins=True, margins_name='Итого')
        count_group_pa_df.reset_index(inplace=True)
        count_group_pa_df = count_group_pa_df.reindex(
            columns=['Класс', 'Очень низкое значение', 'Низкое значение', 'Среднее значение',
                     'Высокое значение', 'Очень высокое значение', 'Итого'])

        count_group_pa_df['% Очень низкое значение  от общего'] = round(
            count_group_pa_df['Очень низкое значение'] / count_group_pa_df['Итого'], 2) * 100

        count_group_pa_df['% Низкое значение от общего'] = round(
            count_group_pa_df['Низкое значение'] /
            count_group_pa_df['Итого'], 2) * 100

        count_group_pa_df['% Среднее значение от общего'] = round(
            count_group_pa_df['Среднее значение'] /
            count_group_pa_df['Итого'], 2) * 100

        count_group_pa_df['% Высокое значение от общего'] = round(
            count_group_pa_df['Высокое значение'] / count_group_pa_df['Итого'], 2) * 100
        count_group_pa_df['% Очень высокое значение от общего'] = round(
            count_group_pa_df['Очень высокое значение'] / count_group_pa_df['Итого'], 2) * 100

        part_svod_df = count_group_pa_df.iloc[:-1:]
        part_svod_df.sort_values(by='Класс', key=lambda x: x.map(sort_name_class), inplace=True)  # сортируем
        itog_svod_df = count_group_pa_df.iloc[-1:]
        count_group_pa_df = pd.concat([part_svod_df, itog_svod_df])




        # Делаем сводную таблицу по Группе среднее УЭ
        mean_group_ua_df = pd.pivot_table(base_df, index=['Класс'],
                                           values=['Значение_шкалы_УЭ'],
                                           aggfunc=round_mean)
        mean_group_ua_df.reset_index(inplace=True)
        mean_group_ua_df['Уровень_шкалы_УЭ'] = mean_group_ua_df['Значение_шкалы_УЭ'].apply(
            calc_level_ua)  # считаем уровень
        mean_group_ua_df.sort_values(by='Класс', key=lambda x: x.map(sort_name_class), inplace=True)  # сортируем

        # делаем сводную по Классу и количеству ПЭ
        count_group_ua_df = pd.pivot_table(base_df, index=['Класс'],
                                            columns='Уровень_шкалы_УЭ',
                                            values='Значение_шкалы_УЭ',
                                            aggfunc='count', margins=True, margins_name='Итого')
        count_group_ua_df.reset_index(inplace=True)
        count_group_ua_df = count_group_ua_df.reindex(
            columns=['Класс', 'Очень низкое значение', 'Низкое значение', 'Среднее значение',
                     'Высокое значение', 'Очень высокое значение', 'Итого'])

        count_group_ua_df['% Очень низкое значение  от общего'] = round(
            count_group_ua_df['Очень низкое значение'] / count_group_ua_df['Итого'], 2) * 100

        count_group_ua_df['% Низкое значение от общего'] = round(
            count_group_ua_df['Низкое значение'] /
            count_group_ua_df['Итого'], 2) * 100

        count_group_ua_df['% Среднее значение от общего'] = round(
            count_group_ua_df['Среднее значение'] /
            count_group_ua_df['Итого'], 2) * 100

        count_group_ua_df['% Высокое значение от общего'] = round(
            count_group_ua_df['Высокое значение'] / count_group_ua_df['Итого'], 2) * 100
        count_group_ua_df['% Очень высокое значение от общего'] = round(
            count_group_ua_df['Очень высокое значение'] / count_group_ua_df['Итого'], 2) * 100

        part_svod_df = count_group_ua_df.iloc[:-1:]
        part_svod_df.sort_values(by='Класс', key=lambda x: x.map(sort_name_class), inplace=True)  # сортируем
        itog_svod_df = count_group_ua_df.iloc[-1:]
        count_group_ua_df = pd.concat([part_svod_df, itog_svod_df])

        """
        Своды  по Группе и полу
        """
        # ОЭИ
        mean_group_sex_oei_df = pd.pivot_table(base_df, index=['Класс', 'Пол'],
                                                values=['Значение_общего_ЭИ'],
                                                aggfunc=round_mean)
        mean_group_sex_oei_df.reset_index(inplace=True)
        mean_group_sex_oei_df['Уровень_общего_ЭИ'] = mean_group_sex_oei_df['Значение_общего_ЭИ'].apply(
            calc_level_union_ei)  # считаем уровень
        mean_group_sex_oei_df.sort_values(by='Класс', key=lambda x: x.map(sort_name_class), inplace=True)  # сортируем

        # делаем сводную по Группе и количеству ПЭ
        count_group_sex_oei_df = pd.pivot_table(base_df, index=['Класс', 'Пол'],
                                                 columns='Уровень_общего_ЭИ',
                                                 values='Значение_общего_ЭИ',
                                                 aggfunc='count', margins=True, margins_name='Итого')
        count_group_sex_oei_df.reset_index(inplace=True)
        count_group_sex_oei_df = count_group_sex_oei_df.reindex(
            columns=['Класс', 'Пол', 'Очень низкое значение', 'Низкое значение', 'Среднее значение',
                     'Высокое значение', 'Очень высокое значение', 'Итого'])

        count_group_sex_oei_df['% Очень низкое значение  от общего'] = round(
            count_group_sex_oei_df['Очень низкое значение'] / count_group_sex_oei_df['Итого'], 2) * 100

        count_group_sex_oei_df['% Низкое значение от общего'] = round(
            count_group_sex_oei_df['Низкое значение'] /
            count_group_sex_oei_df['Итого'], 2) * 100

        count_group_sex_oei_df['% Среднее значение от общего'] = round(
            count_group_sex_oei_df['Среднее значение'] /
            count_group_sex_oei_df['Итого'], 2) * 100

        count_group_sex_oei_df['% Высокое значение от общего'] = round(
            count_group_sex_oei_df['Высокое значение'] / count_group_sex_oei_df['Итого'], 2) * 100
        count_group_sex_oei_df['% Очень высокое значение от общего'] = round(
            count_group_sex_oei_df['Очень высокое значение'] / count_group_sex_oei_df['Итого'], 2) * 100

        part_svod_df = count_group_sex_oei_df.iloc[:-1:]
        part_svod_df.sort_values(by='Класс', key=lambda x: x.map(sort_name_class), inplace=True)  # сортируем
        itog_svod_df = count_group_sex_oei_df.iloc[-1:]
        count_group_sex_oei_df = pd.concat([part_svod_df, itog_svod_df])

        # МЭИ
        mean_group_sex_mei_df = pd.pivot_table(base_df, index=['Класс', 'Пол'],
                                                values=['Значение_шкалы_МЭИ'],
                                                aggfunc=round_mean)
        mean_group_sex_mei_df.reset_index(inplace=True)
        mean_group_sex_mei_df['Уровень_шкалы_МЭИ'] = mean_group_sex_mei_df['Значение_шкалы_МЭИ'].apply(
            calc_level_union_ei)  # считаем уровень
        mean_group_sex_mei_df.sort_values(by='Класс', key=lambda x: x.map(sort_name_class), inplace=True)  # сортируем


        # делаем сводную по Группе и количеству ПЭ
        count_group_sex_mei_df = pd.pivot_table(base_df, index=['Класс', 'Пол'],
                                                 columns='Уровень_шкалы_МЭИ',
                                                 values='Значение_шкалы_МЭИ',
                                                 aggfunc='count', margins=True, margins_name='Итого')
        count_group_sex_mei_df.reset_index(inplace=True)
        count_group_sex_mei_df = count_group_sex_mei_df.reindex(
            columns=['Класс', 'Пол', 'Очень низкое значение', 'Низкое значение', 'Среднее значение',
                     'Высокое значение', 'Очень высокое значение', 'Итого'])

        count_group_sex_mei_df['% Очень низкое значение  от общего'] = round(
            count_group_sex_mei_df['Очень низкое значение'] / count_group_sex_mei_df['Итого'], 2) * 100

        count_group_sex_mei_df['% Низкое значение от общего'] = round(
            count_group_sex_mei_df['Низкое значение'] /
            count_group_sex_mei_df['Итого'], 2) * 100

        count_group_sex_mei_df['% Среднее значение от общего'] = round(
            count_group_sex_mei_df['Среднее значение'] /
            count_group_sex_mei_df['Итого'], 2) * 100

        count_group_sex_mei_df['% Высокое значение от общего'] = round(
            count_group_sex_mei_df['Высокое значение'] / count_group_sex_mei_df['Итого'], 2) * 100
        count_group_sex_mei_df['% Очень высокое значение от общего'] = round(
            count_group_sex_mei_df['Очень высокое значение'] / count_group_sex_mei_df['Итого'], 2) * 100

        part_svod_df = count_group_sex_mei_df.iloc[:-1:]
        part_svod_df.sort_values(by='Класс', key=lambda x: x.map(sort_name_class), inplace=True)  # сортируем
        itog_svod_df = count_group_sex_mei_df.iloc[-1:]
        count_group_sex_mei_df = pd.concat([part_svod_df, itog_svod_df])

        # ВЭИ
        mean_group_sex_vei_df = pd.pivot_table(base_df, index=['Класс', 'Пол'],
                                                values=['Значение_шкалы_ВЭИ'],
                                                aggfunc=round_mean)
        mean_group_sex_vei_df.reset_index(inplace=True)
        mean_group_sex_vei_df['Уровень_шкалы_ВЭИ'] = mean_group_sex_vei_df['Значение_шкалы_ВЭИ'].apply(
            calc_level_union_ei)  # считаем уровень
        mean_group_sex_vei_df.sort_values(by='Класс', key=lambda x: x.map(sort_name_class), inplace=True)  # сортируем

        # делаем сводную по Группе и количеству ПЭ
        count_group_sex_vei_df = pd.pivot_table(base_df, index=['Класс', 'Пол'],
                                                 columns='Уровень_шкалы_ВЭИ',
                                                 values='Значение_шкалы_ВЭИ',
                                                 aggfunc='count', margins=True, margins_name='Итого')
        count_group_sex_vei_df.reset_index(inplace=True)
        count_group_sex_vei_df = count_group_sex_vei_df.reindex(
            columns=['Класс', 'Пол', 'Очень низкое значение', 'Низкое значение', 'Среднее значение',
                     'Высокое значение', 'Очень высокое значение', 'Итого'])

        count_group_sex_vei_df['% Очень низкое значение  от общего'] = round(
            count_group_sex_vei_df['Очень низкое значение'] / count_group_sex_vei_df['Итого'], 2) * 100

        count_group_sex_vei_df['% Низкое значение от общего'] = round(
            count_group_sex_vei_df['Низкое значение'] /
            count_group_sex_vei_df['Итого'], 2) * 100

        count_group_sex_vei_df['% Среднее значение от общего'] = round(
            count_group_sex_vei_df['Среднее значение'] /
            count_group_sex_vei_df['Итого'], 2) * 100

        count_group_sex_vei_df['% Высокое значение от общего'] = round(
            count_group_sex_vei_df['Высокое значение'] / count_group_sex_vei_df['Итого'], 2) * 100
        count_group_sex_vei_df['% Очень высокое значение от общего'] = round(
            count_group_sex_vei_df['Очень высокое значение'] / count_group_sex_vei_df['Итого'], 2) * 100

        part_svod_df = count_group_sex_vei_df.iloc[:-1:]
        part_svod_df.sort_values(by='Класс', key=lambda x: x.map(sort_name_class), inplace=True)  # сортируем
        itog_svod_df = count_group_sex_vei_df.iloc[-1:]
        count_group_sex_vei_df = pd.concat([part_svod_df, itog_svod_df])


        # ПЭ
        mean_group_sex_pa_df = pd.pivot_table(base_df, index=['Класс', 'Пол'],
                                                values=['Значение_шкалы_ПЭ'],
                                                aggfunc=round_mean)
        mean_group_sex_pa_df.reset_index(inplace=True)
        mean_group_sex_pa_df['Уровень_шкалы_ПЭ'] = mean_group_sex_pa_df['Значение_шкалы_ПЭ'].apply(
            calc_level_union_ei)  # считаем уровень
        mean_group_sex_pa_df.sort_values(by='Класс', key=lambda x: x.map(sort_name_class), inplace=True)  # сортируем

        # делаем сводную по Группе и количеству ПЭ
        count_group_sex_pa_df = pd.pivot_table(base_df, index=['Класс', 'Пол'],
                                                 columns='Уровень_шкалы_ПЭ',
                                                 values='Значение_шкалы_ПЭ',
                                                 aggfunc='count', margins=True, margins_name='Итого')
        count_group_sex_pa_df.reset_index(inplace=True)
        count_group_sex_pa_df = count_group_sex_pa_df.reindex(
            columns=['Класс', 'Пол', 'Очень низкое значение', 'Низкое значение', 'Среднее значение',
                     'Высокое значение', 'Очень высокое значение', 'Итого'])

        count_group_sex_pa_df['% Очень низкое значение  от общего'] = round(
            count_group_sex_pa_df['Очень низкое значение'] / count_group_sex_pa_df['Итого'], 2) * 100

        count_group_sex_pa_df['% Низкое значение от общего'] = round(
            count_group_sex_pa_df['Низкое значение'] /
            count_group_sex_pa_df['Итого'], 2) * 100

        count_group_sex_pa_df['% Среднее значение от общего'] = round(
            count_group_sex_pa_df['Среднее значение'] /
            count_group_sex_pa_df['Итого'], 2) * 100

        count_group_sex_pa_df['% Высокое значение от общего'] = round(
            count_group_sex_pa_df['Высокое значение'] / count_group_sex_pa_df['Итого'], 2) * 100
        count_group_sex_pa_df['% Очень высокое значение от общего'] = round(
            count_group_sex_pa_df['Очень высокое значение'] / count_group_sex_pa_df['Итого'], 2) * 100
        part_svod_df = count_group_sex_pa_df.iloc[:-1:]
        part_svod_df.sort_values(by='Класс', key=lambda x: x.map(sort_name_class), inplace=True)  # сортируем
        itog_svod_df = count_group_sex_pa_df.iloc[-1:]
        count_group_sex_pa_df = pd.concat([part_svod_df, itog_svod_df])

        # УЭ
        mean_group_sex_ua_df = pd.pivot_table(base_df, index=['Класс', 'Пол'],
                                                values=['Значение_шкалы_УЭ'],
                                                aggfunc=round_mean)
        mean_group_sex_ua_df.reset_index(inplace=True)
        mean_group_sex_ua_df['Уровень_шкалы_УЭ'] = mean_group_sex_ua_df['Значение_шкалы_УЭ'].apply(
            calc_level_union_ei)  # считаем уровень
        mean_group_sex_ua_df.sort_values(by='Класс', key=lambda x: x.map(sort_name_class), inplace=True)  # сортируем

        # делаем сводную по Группе и количеству ПЭ
        count_group_sex_ua_df = pd.pivot_table(base_df, index=['Класс', 'Пол'],
                                                 columns='Уровень_шкалы_УЭ',
                                                 values='Значение_шкалы_УЭ',
                                                 aggfunc='count', margins=True, margins_name='Итого')
        count_group_sex_ua_df.reset_index(inplace=True)
        count_group_sex_ua_df = count_group_sex_ua_df.reindex(
            columns=['Класс', 'Пол', 'Очень низкое значение', 'Низкое значение', 'Среднее значение',
                     'Высокое значение', 'Очень высокое значение', 'Итого'])

        count_group_sex_ua_df['% Очень низкое значение  от общего'] = round(
            count_group_sex_ua_df['Очень низкое значение'] / count_group_sex_ua_df['Итого'], 2) * 100

        count_group_sex_ua_df['% Низкое значение от общего'] = round(
            count_group_sex_ua_df['Низкое значение'] /
            count_group_sex_ua_df['Итого'], 2) * 100

        count_group_sex_ua_df['% Среднее значение от общего'] = round(
            count_group_sex_ua_df['Среднее значение'] /
            count_group_sex_ua_df['Итого'], 2) * 100

        count_group_sex_ua_df['% Высокое значение от общего'] = round(
            count_group_sex_ua_df['Высокое значение'] / count_group_sex_ua_df['Итого'], 2) * 100
        count_group_sex_ua_df['% Очень высокое значение от общего'] = round(
            count_group_sex_ua_df['Очень высокое значение'] / count_group_sex_ua_df['Итого'], 2) * 100

        part_svod_df = count_group_sex_ua_df.iloc[:-1:]
        part_svod_df.sort_values(by='Класс', key=lambda x: x.map(sort_name_class), inplace=True)  # сортируем
        itog_svod_df = count_group_sex_ua_df.iloc[-1:]
        count_group_sex_ua_df = pd.concat([part_svod_df, itog_svod_df])


        # Датафрейм для проверки

        out_answer_df = pd.concat([out_answer_df, answers_df], axis=1)

        # Общий свод сколько склонностей всего в процентном соотношении
        svod_all_df = count_all_scale(base_df, ['ЭИ', 'МЭИ', 'ВЭИ', 'ПЭ', 'УЭ'],
                                      ['Очень низкое значение',
                                       'Низкое значение',
                                       'Среднее значение',
                                       'Высокое значение',
                                       'Очень высокое значение',
                                        'Итого'])





        # формируем словарь
        out_dct = {'Списочный результат': base_df, 'Список для проверки': out_answer_df,
                   'Общий свод':svod_all_df,
                   'Среднее Класс ОЭИ': mean_group_oei_df, 'Количество Класс ОЭИ': count_group_oei_df,
                   'Среднее Класс МЭИ': mean_group_mei_df, 'Количество Класс МЭИ': count_group_mei_df,
                   'Среднее Класс ВЭИ': mean_group_vei_df, 'Количество Класс ВЭИ': count_group_vei_df,
                   'Среднее Класс ПЭ': mean_group_pa_df, 'Количество Класс ПЭ': count_group_pa_df,
                   'Среднее Класс УЭ': mean_group_ua_df, 'Количество Класс УЭ': count_group_ua_df,
                   'Среднее Класс Пол ОЭИ': mean_group_sex_oei_df, 'Количество Класс Пол ОЭИ': count_group_sex_oei_df,
                   'Среднее Класс Пол МЭИ': mean_group_sex_mei_df, 'Количество Класс Пол МЭИ': count_group_sex_mei_df,
                   'Среднее Класс Пол ВЭИ': mean_group_sex_vei_df, 'Количество Класс Пол ВЭИ': count_group_sex_vei_df,
                   'Среднее Класс Пол ПЭ': mean_group_sex_pa_df, 'Количество Класс Пол ПЭ': count_group_sex_pa_df,
                   'Среднее Класс Пол УЭ': mean_group_sex_ua_df, 'Количество Класс Пол УЭ': count_group_sex_ua_df,
                   'Среднее Номер_класса ОЭИ': mean_course_oei_df, 'Количество Номер_класса ОЭИ': count_course_oei_df,
                   'Среднее Номер_класса МЭИ': mean_course_mei_df, 'Количество Номер_класса МЭИ': count_course_mei_df,
                   'Среднее Номер_класса ВЭИ': mean_course_vei_df, 'Количество Номер_класса ВЭИ': count_course_vei_df,
                   'Среднее Номер_класса ПЭ': mean_course_pa_df, 'Количество Номер_класса ПЭ': count_course_pa_df,
                   'Среднее Номер_класса УЭ': mean_course_ua_df, 'Количество Номер_класса УЭ': count_course_ua_df,
                   'Среднее Номер_класса Пол ОЭИ': mean_course_sex_oei_df, 'Количество Номер_класса Пол ОЭИ': count_course_sex_oei_df,
                   'Среднее Номер_класса Пол МЭИ': mean_course_sex_mei_df, 'Количество Номер_класса Пол МЭИ': count_course_sex_mei_df,
                   'Среднее Номер_класса Пол ВЭИ': mean_course_sex_vei_df, 'Количество Номер_класса Пол ВЭИ': count_course_sex_vei_df,
                   'Среднее Номер_класса Пол ПЭ': mean_course_sex_pa_df, 'Количество Номер_класса Пол ПЭ': count_course_sex_pa_df,
                   'Среднее Номер_класса Пол УЭ': mean_course_sex_ua_df, 'Количество Номер_класса Пол УЭ': count_course_sex_ua_df,

    }

        return out_dct, part_df

    except BadOrderEI:
        messagebox.showerror('Лахеcис',
                             f'При обработке вопросов теста Эмоциональный интеллект Люсина обнаружены неправильные вопросы. Проверьте названия колонок с вопросами:\n'
                             f'{error_order_message}\n'
                             f'Используйте при создании Яндекс-формы написание вопросов из руководства пользователя программы Лахесис.')
    except BadValueEI:
        messagebox.showerror('Лахеcис',
                             f'При обработке вопросов теста Эмоциональный интеллект Люсина обнаружены неправильные варианты ответов. Проверьте ответы на указанных строках:\n'
                             f'{error_message}\n'
                             f'Используйте при создании Яндекс-формы написание вариантов ответа из руководства пользователя программы Лахесис.')

    except BadCountColumnsEI:
        messagebox.showerror('Лахеcис',
                             f'Проверьте количество колонок с ответами на тест Эмоциональный интеллект Люсина\n'
                             f'Должно быть 46 колонок с вопросами'
                             )


