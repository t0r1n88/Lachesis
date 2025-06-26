"""
Скрипт для обработки результатов теста BAT краткая версия Демкин
"""

import pandas as pd
import re
from tkinter import messagebox
from lachesis_support_functions import round_mean,create_svod_sub

class BadOrderSBATD(Exception):
    """
    Исключение для обработки случая когда колонки не совпадают
    """
    pass


class BadValueSBATD(Exception):
    """
    Исключение для неправильных значений в вариантах ответов
    """
    pass

class BadCountColumnsSBATD(Exception):
    """
    Исключение для обработки случая если количество колонок не равно 12
    """
    pass


def processing_short_bat_demkin(result_df: pd.DataFrame, answers_df: pd.DataFrame, lst_svod_cols:list):
    """
    Функция для обработки
    :param result_df: часть датафрейма с описательными колонками
    :param answers_df: часть датафрейма с ответами
    :param lst_svod_cols:  список с колонками по которым нужно делать свод
    """
    out_answer_df = result_df.copy()  # делаем копию для последующего соединения с сырыми ответами
    if len(answers_df.columns) != 12:  # проверяем количество колонок с вопросами
        raise BadCountColumnsSBATD

    lst_check_cols = ['На работе я чувствую себя морально истощенным','Все, что я делаю на работе, требует больших усилий','После рабочего дня мне трудно восстановить свои силы',
                      'Я изо всех сил пытаюсь проявить хоть какой-то энтузиазм в своей работе','Я испытываю сильное отвращение к своей работе','Я цинично отношусь к тому, что моя работа значит для других',
                      'На работе мне трудно концентрироваться на задаче','Когда я работаю, мне трудно сосредоточиться','Я совершаю ошибки в своей работе, потому что мои мысли заняты другими вещами',
                      'На работе я чувствую, что не могу контролировать свои эмоции','Я не узнаю себя по тому, как эмоционально реагирую на все на работе','На работе я могу непреднамеренно слишком остро реагировать'
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
        raise BadOrderSBATD

    # словарь для замены слов на числа
    dct_replace_value = {'никогда': 1,
                         'редко': 2,
                         'иногда': 3,
                         'часто': 4,
                         'всегда': 5,
                         }

    valid_values = [1, 2, 3, 4, 5]
    answers_df.replace(dct_replace_value, inplace=True)  # заменяем слова на цифры для подсчетов
    # Проверяем, есть ли значения, отличающиеся от указанных в списке
    lst_error_answers = []  # список для хранения строк где найдены неправильные ответы

    for i in range(12):
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
        raise BadValueSBATD



