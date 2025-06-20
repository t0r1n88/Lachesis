"""
Скрипт для обработки результатов теста MBI Профессиональное выгорание Маслач Водопьянова исходный вариант
"""

import pandas as pd
import re
from tkinter import messagebox
from lachesis_support_functions import round_mean,create_svod_sub


class BadOrderMPBV(Exception):
    """
    Исключение для обработки случая когда колонки не совпадают
    """
    pass


class BadValueMPBV(Exception):
    """
    Исключение для неправильных значений в вариантах ответов
    """
    pass

class BadCountColumnsMPBV(Exception):
    """
    Исключение для обработки случая если количество колонок не равно 22
    """
    pass


def calc_sub_value_em_attrition(row):
    """
    Функция для подсчета значения субшкалы Эмоциональное истощение
    :param row: строка с ответами
    :return: число
    """
    lst_pr = [1,2,3,6,8,13,14,16,20]

    value_forward = 0 # счетчик прямых ответов

    for idx, value in enumerate(row):
        if idx +1 in lst_pr:
            value_forward += value

    return value_forward


def calc_level_sub_em_attrition(value):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """
    if 0 <= value <= 10:
        return 'крайне низкий уровень'
    elif 11 <= value <= 20:
        return 'низкий уровень'
    elif 21 <= value <= 30:
        return 'средний уровень'
    elif 31 <= value <= 40:
        return 'высокий уровень'
    else:
        return 'крайне высокий уровень'



def calc_sub_value_depers(row):
    """
    Функция для подсчета значения субшкалы Деперсонализация
    :param row: строка с ответами
    :return: число
    """
    lst_pr = [5,10,11,15,22]

    value_forward = 0 # счетчик прямых ответов

    for idx, value in enumerate(row):
        if idx +1 in lst_pr:
            value_forward += value

    return value_forward


def calc_level_sub_depers(value):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """
    if 0 <= value <= 5:
        return 'крайне низкий уровень'
    elif 6 <= value <= 11:
        return 'низкий уровень'
    elif 12 <= value <= 17:
        return 'средний уровень'
    elif 18 <= value <= 23:
        return 'высокий уровень'
    else:
        return 'крайне высокий уровень'


def calc_sub_value_reduc(row):
    """
    Функция для подсчета значения субшкалы Редукция персональных достижений
    :param row: строка с ответами
    :return: число
    """
    lst_pr = [4,7,9,12,17,18,19,21]

    value_forward = 0 # счетчик прямых ответов

    for idx, value in enumerate(row):
        if idx +1 in lst_pr:
            if value == 6:
                value_forward += 0
            elif value == 5:
                value_forward += 1
            elif value == 4:
                value_forward += 2
            elif value == 3:
                value_forward += 3
            elif value == 2:
                value_forward += 4
            elif value == 1:
                value_forward += 5
            elif value == 0:
                value_forward += 6

    return value_forward


def calc_level_sub_reduc(value):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """
    if 0 <= value <= 8:
        return 'крайне низкий уровень'
    elif 9 <= value <= 18:
        return 'низкий уровень'
    elif 19 <= value <= 28:
        return 'средний уровень'
    elif 29 <= value <= 38:
        return 'высокий уровень'
    else:
        return 'крайне высокий уровень'

def calc_level_psy(value):
    """
    Функция для подсчета психического выгорания
    :param value:
    :return:
    """
    if 0 <= value <= 23:
        return 'крайне низкий уровень'
    elif 24 <= value <= 49:
        return 'низкий уровень'
    elif 50 <= value <= 75:
        return 'средний уровень'
    elif 76 <= value <= 101:
        return 'высокий уровень'
    else:
        return 'крайне высокий уровень'





def processing_maslach_prof_burnout_vod(base_df: pd.DataFrame, answers_df: pd.DataFrame, lst_svod_cols:list):
    """
    Функция для обработки
    :param base_df: часть датафрейма с описательными колонками
    :param answers_df: часть датафрейма с ответами
    :param lst_svod_cols:  список с колонками по которым нужно делать свод
    """
    out_answer_df = base_df.copy()  # делаем копию для последующего соединения с сырыми ответами
    if len(answers_df.columns) != 22:  # проверяем количество колонок с вопросами
        raise BadCountColumnsMPBV

    lst_check_cols = ['Я чувствую себя эмоционально опустошенным(ой).',
                      'После работы я чувствую себя как «выжатый лимон».',
                      'Утром я чувствую усталость и нежелание идти на работу.',
                      'Я хорошо понимаю, что чувствуют мои подчиненные и коллеги, и стараюсь учитывать это в интересах дела.',
                      'Я чувствую, что общаюсь с некоторыми подчиненными и коллегами как с предметами (без теплоты и расположения к ним).',
                      'После работы на некоторое время хочется уединиться от всех и всего.',
                      'Я умею находить правильное решение в конфликтных ситуациях, возникающих при общении с коллегами.',
                      'Я чувствую угнетенность и апатию.',
                      'Я уверен(а), что моя работа нужна людям.',
                      'В последнее время я стал(а) более «черствым» по отношению к тем, с кем работаю.',
                      'Я замечаю, что моя работа ожесточает меня.',
                      'У меня много планов на будущее, и я верю в их осуществление.',
                      'Моя работа все больше меня разочаровывает.',
                      'Мне кажется, что я слишком много работаю.',
                      'Бывает, что мне действительно безразлично то, что происходит c некоторыми моими подчиненными и коллегами.',
                      'Мне хочется уединиться и отдохнуть от всего и всех.',
                      'Я легко могу создать атмосферу доброжелательности и сотрудничества в коллективе.',
                      'Во время работы я чувствую приятное оживление.',
                      'Благодаря своей работе я уже сделал(а) в жизни много действительно ценного.',
                      'Я чувствую равнодушие и потерю интереса ко многому, что радовало меня в моей работе.',
                      'На работе я спокойно справляюсь с эмоциональными проблемами.',
                      'В последнее время мне кажется, что коллеги и подчиненные все чаще перекладывают на меня груз своих проблем и обязанностей.',
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
        raise BadOrderMPBV

    # словарь для замены слов на числа
    dct_replace_value = {'никогда': 0,
                         'очень редко': 1,
                         'редко': 2,
                         'иногда': 3,
                         'часто': 4,
                         'очень часто': 5,
                         'ежедневно': 6}

    valid_values = [0, 1, 2, 3, 4, 5, 6]
    answers_df.replace(dct_replace_value, inplace=True)  # заменяем слова на цифры для подсчетов
    # Проверяем, есть ли значения, отличающиеся от указанных в списке
    lst_error_answers = []  # список для хранения строк где найдены неправильные ответы

    for i in range(22):
        mask = ~answers_df.iloc[:, i].isin(valid_values)  # проверяем на допустимые значения
        result_check = answers_df.iloc[:, i][mask]
        if len(result_check) != 0:
            error_row = list(map(lambda x: x + 2, result_check.index))
            error_row = list(map(str, error_row))
            error_row_lst = [f'В {i + 1} вопросной колонке на строке {value}' for value in error_row]
            error_in_column = ','.join(error_row_lst)
            lst_error_answers.append(error_in_column)

    if len(lst_error_answers) != 0:
        error_message = ';'.join(lst_error_answers)
        raise BadValueMPBV

    # Субшкала Эмоциональное истощение
    base_df['Значение_субшкалы_Эмоциональное_истощение'] = answers_df.apply(calc_sub_value_em_attrition, axis=1)
    base_df['Норма_Эмоциональное_истощение'] = '0-30 баллов'
    base_df['Уровень_субшкалы_Эмоциональное_истощение'] = base_df['Значение_субшкалы_Эмоциональное_истощение'].apply(
        calc_level_sub_em_attrition)

    # Субшкала Деперсонализация
    base_df['Значение_субшкалы_Деперсонализация'] = answers_df.apply(calc_sub_value_depers, axis=1)
    base_df['Норма_Деперсонализация'] = '0-17 баллов'
    base_df['Уровень_субшкалы_Деперсонализация'] = base_df['Значение_субшкалы_Деперсонализация'].apply(
        calc_level_sub_depers)

    # Субшкала Редукция персональных достижений
    base_df['Значение_субшкалы_Редукция_персональных_достижений'] = answers_df.apply(calc_sub_value_reduc, axis=1)
    base_df['Норма_Редукция_персональных_достижений'] = '0-28 баллов'
    base_df['Уровень_субшкалы_Редукция_персональных_достижений'] = base_df[
        'Значение_субшкалы_Редукция_персональных_достижений'].apply(calc_level_sub_reduc)

    # Уровень выгорания
    base_df['Значение_уровня_психического_выгорания'] = base_df[['Значение_субшкалы_Эмоциональное_истощение','Значение_субшкалы_Деперсонализация','Значение_субшкалы_Редукция_персональных_достижений']].sum(axis=1)
    base_df['Уровень_психического_выгорания'] = base_df['Значение_уровня_психического_выгорания'].apply(calc_level_psy)





    base_df.to_excel('res.xlsx')






