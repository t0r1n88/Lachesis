"""
Скрипт для обработки результатов теста Эмоциональный интеллект Люсин
"""

import pandas as pd
import re
from tkinter import messagebox
from lachesis_support_functions import round_mean,create_union_svod,create_list_on_level


class BadOrderLEI(Exception):
    """
    Исключение для обработки случая когда колонки не совпадают
    """
    pass


class BadValueLEI(Exception):
    """
    Исключение для неправильных значений в вариантах ответов
    """
    pass

class BadCountColumnsLEI(Exception):
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
        return 'очень низкое значение'
    elif 72 <= value <= 78:
        return 'низкое значение'
    elif 79 <= value <= 92:
        return 'среднее значение'
    elif 93 <= value <= 104:
        return 'высокое значение'
    else:
        return 'очень высокое значение'



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
        return 'очень низкое значение'
    elif 20 <= value <= 22:
        return 'низкое значение'
    elif 23 <= value <= 26:
        return 'среднее значение'
    elif 27 <= value <= 30:
        return 'высокое значение'
    else:
        return 'очень высокое значение'


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
        return 'очень низкое значение'
    elif 15 <= value <= 17:
        return 'низкое значение'
    elif 18 <= value <= 21:
        return 'среднее значение'
    elif 22 <= value <= 24:
        return 'высокое значение'
    else:
        return 'очень высокое значение'


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
        return 'очень низкое значение'
    elif 14 <= value <= 16:
        return 'низкое значение'
    elif 17 <= value <= 21:
        return 'среднее значение'
    elif 22 <= value <= 25:
        return 'высокое значение'
    else:
        return 'очень высокое значение'

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
        return 'очень низкое значение'
    elif 10 <= value <= 12:
        return 'низкое значение'
    elif 13 <= value <= 15:
        return 'среднее значение'
    elif 16 <= value <= 17:
        return 'высокое значение'
    else:
        return 'очень высокое значение'


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
        return 'очень низкое значение'
    elif 7 <= value <= 9:
        return 'низкое значение'
    elif 10 <= value <= 12:
        return 'среднее значение'
    elif 13 <= value <= 15:
        return 'высокое значение'
    else:
        return 'очень высокое значение'


def calc_level_mei(value):
    """
    Функция для подсчета уровня шкалы МЭИ
    :param value:
    :return:
    """
    if 0 <= value <= 34:
        return 'очень низкое значение'
    elif 35 <= value <= 39:
        return 'низкое значение'
    elif 40 <= value <= 46:
        return 'среднее значение'
    elif 47 <= value <= 52:
        return 'высокое значение'
    else:
        return 'очень высокое значение'

def calc_level_vei(value):
    """
    Функция для подсчета уровня шкалы ВЭИ
    :param value:
    :return:
    """
    if 0 <= value <= 33:
        return 'очень низкое значение'
    elif 34 <= value <= 38:
        return 'низкое значение'
    elif 39 <= value <= 47:
        return 'среднее значение'
    elif 48 <= value <= 53:
        return 'высокое значение'
    else:
        return 'очень высокое значение'


def calc_level_pa(value):
    """
    Функция для подсчета уровня шкалы ПЭ
    :param value:
    :return:
    """
    if 0 <= value <= 34:
        return 'очень низкое значение'
    elif 35 <= value <= 39:
        return 'низкое значение'
    elif 40 <= value <= 47:
        return 'среднее значение'
    elif 48 <= value <= 53:
        return 'высокое значение'
    else:
        return 'очень высокое значение'


def calc_level_ua(value):
    """
    Функция для подсчета уровня шкалы УЭ
    :param value:
    :return:
    """
    if 0 <= value <= 33:
        return 'очень низкое значение'
    elif 34 <= value <= 39:
        return 'низкое значение'
    elif 40 <= value <= 47:
        return 'среднее значение'
    elif 48 <= value <= 53:
        return 'высокое значение'
    else:
        return 'очень высокое значение'


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


def calc_count_level(df:pd.DataFrame, lst_cat:list, val_cat, col_cat, lst_cols:list):
    """
    Функция для создания сводных датафреймов по субшкалам

    :param df: датафрейм с данными
    :param lst_cat:список колонок по которым будет формироваться свод
    :param val_cat:значение по которому будет формироваться свод
    :param col_cat: колонка по которой будет формироваться свод
    :param lst_cols: список с колонками
    :return:датафрейм
    """
    count_df = pd.pivot_table(df, index=lst_cat,
                                             columns=col_cat,
                                             values=val_cat,
                                             aggfunc='count', margins=True, margins_name='Итого')


    count_df.reset_index(inplace=True)
    count_df = count_df.reindex(columns=lst_cols)
    count_df['% очень низкое значение от общего'] = round(
        count_df['очень низкое значение'] / count_df['Итого'], 2) * 100
    count_df['% низкое значение от общего'] = round(
        count_df['низкое значение'] / count_df['Итого'], 2) * 100
    count_df['% среднее значение от общего'] = round(
        count_df['среднее значение'] / count_df['Итого'], 2) * 100
    count_df['% высокое значение от общего'] = round(
        count_df['высокое значение'] / count_df['Итого'], 2) * 100
    count_df['% очень высокое значение от общего'] = round(
        count_df['очень высокое значение'] / count_df['Итого'], 2) * 100

    return count_df





def create_result_lei(base_df:pd.DataFrame, out_dct:dict, lst_svod_cols:list):
    """
    Функция для подсчета результата если указаны колонки по которым нужно провести свод
    :param df: датафрейм с результатами
    :param out_dct: словарь с уже подсчитанными базовыми данными
    :param lst_svod_cols: список сводных колонок
    :return: словарь
    """
    lst_reindex_main_level_cols = lst_svod_cols.copy()
    lst_reindex_main_level_cols.extend( ['очень низкое значение', 'низкое значение', 'среднее значение',
                'высокое значение', 'очень высокое значение',
                                   'Итого'])  # Основная шкала


    svod_count_one_level_ei_df = calc_count_level(base_df, lst_svod_cols,
                                                      'Значение_общего_ЭИ',
                                                      'Уровень_общего_ЭИ',
                                                  lst_reindex_main_level_cols)
    svod_count_one_level_mei_df = calc_count_level(base_df, lst_svod_cols,
                                                      'Значение_шкалы_МЭИ',
                                                      'Уровень_шкалы_МЭИ',
                                                   lst_reindex_main_level_cols)
    svod_count_one_level_vei_df = calc_count_level(base_df, lst_svod_cols,
                                                      'Значение_шкалы_ВЭИ',
                                                      'Уровень_шкалы_ВЭИ',
                                                   lst_reindex_main_level_cols)
    svod_count_one_level_pa_df = calc_count_level(base_df, lst_svod_cols,
                                                      'Значение_шкалы_ПЭ',
                                                      'Уровень_шкалы_ПЭ',
                                                  lst_reindex_main_level_cols)
    svod_count_one_level_ua_df = calc_count_level(base_df, lst_svod_cols,
                                                      'Значение_шкалы_УЭ',
                                                      'Уровень_шкалы_УЭ',
                                                  lst_reindex_main_level_cols)

    svod_count_one_level_mp_df = calc_count_level(base_df, lst_svod_cols,
                                                      'Значение_субшкалы_МП',
                                                      'Уровень_субшкалы_МП',
                                                  lst_reindex_main_level_cols)
    svod_count_one_level_mu_df = calc_count_level(base_df, lst_svod_cols,
                                                      'Значение_субшкалы_МУ',
                                                      'Уровень_субшкалы_МУ',
                                                  lst_reindex_main_level_cols)
    svod_count_one_level_vp_df = calc_count_level(base_df, lst_svod_cols,
                                                      'Значение_субшкалы_ВП',
                                                      'Уровень_субшкалы_ВП',
                                                  lst_reindex_main_level_cols)
    svod_count_one_level_vu_df = calc_count_level(base_df, lst_svod_cols,
                                                      'Значение_субшкалы_ВУ',
                                                      'Уровень_субшкалы_ВУ',
                                                  lst_reindex_main_level_cols)
    svod_count_one_level_va_df = calc_count_level(base_df, lst_svod_cols,
                                                      'Значение_субшкалы_ВЭ',
                                                      'Уровень_субшкалы_ВЭ',
                                                  lst_reindex_main_level_cols)

    # Считаем среднее по субшкалам
    svod_mean_one_df = pd.pivot_table(base_df,
                                      index=lst_svod_cols,
                                      values=['Значение_общего_ЭИ',
                                              'Значение_шкалы_МЭИ',
                                              'Значение_шкалы_ВЭИ',
                                              'Значение_шкалы_ПЭ',
                                              'Значение_шкалы_УЭ',
                                              'Значение_субшкалы_МП',
                                              'Значение_субшкалы_МУ',
                                              'Значение_субшкалы_ВП',
                                              'Значение_субшкалы_ВУ',
                                              'Значение_субшкалы_ВЭ',
                                              ],
                                      aggfunc=round_mean)
    svod_mean_one_df.reset_index(inplace=True)
    # упорядочиваем колонки
    new_order_cols = lst_svod_cols.copy()
    new_order_cols.extend((['Значение_общего_ЭИ',
                                              'Значение_шкалы_МЭИ',
                                              'Значение_шкалы_ВЭИ',
                                              'Значение_шкалы_ПЭ',
                                              'Значение_шкалы_УЭ',
                                              'Значение_субшкалы_МП',
                                              'Значение_субшкалы_МУ',
                                              'Значение_субшкалы_ВП',
                                              'Значение_субшкалы_ВУ',
                                              'Значение_субшкалы_ВЭ',
                            ]))
    svod_mean_one_df = svod_mean_one_df.reindex(columns=new_order_cols)

    dct_rename_cols_mean = {'Значение_общего_ЭИ': 'Ср. ОЭИ',
                            'Значение_шкалы_МЭИ': 'Ср. МЭИ',
                            'Значение_шкалы_ВЭИ': 'Ср. ВЭИ',
                            'Значение_шкалы_ПЭ': 'Ср. ПЭ',
                            'Значение_шкалы_УЭ': 'Ср. УЭ',
                            'Значение_субшкалы_МП': 'Ср. МП',
                            'Значение_субшкалы_МУ': 'Ср. МУ',
                            'Значение_субшкалы_ВП': 'Ср. ВП',
                            'Значение_субшкалы_ВУ': 'Ср. ВУ',
                            'Значение_субшкалы_ВЭ': 'Ср. ВЭ',
                            }
    svod_mean_one_df.rename(columns=dct_rename_cols_mean, inplace=True)

    # очищаем название колонки по которой делали свод
    out_name_lst = []

    for name_col in lst_svod_cols:
        name = re.sub(r'[\[\]\'+()<> :"?*|\\/]', '_', name_col)
        if len(lst_svod_cols) == 1:
            out_name_lst.append(name[:14])
        elif len(lst_svod_cols) == 2:
            out_name_lst.append(name[:7])
        else:
            out_name_lst.append(name[:4])

    out_name = ' '.join(out_name_lst)
    if len(out_name) > 14:
        out_name = out_name[:14]

    out_dct.update({f'Ср {out_name}': svod_mean_one_df,
                    f'Свод ОЭИ {out_name}': svod_count_one_level_ei_df,
                    f'Свод МЭИ {out_name}': svod_count_one_level_mei_df,
                    f'Свод ВЭИ {out_name}': svod_count_one_level_vei_df,
                    f'Свод ПЭ {out_name}': svod_count_one_level_pa_df,
                    f'Свод УЭ {out_name}': svod_count_one_level_ua_df,

                    f'Свод МП {out_name}': svod_count_one_level_mp_df,
                    f'Свод МУ {out_name}': svod_count_one_level_mu_df,
                    f'Свод ВП {out_name}': svod_count_one_level_vp_df,
                    f'Свод ВУ {out_name}': svod_count_one_level_vu_df,
                    f'Свод ВЭ {out_name}': svod_count_one_level_va_df,
                    })

    if len(lst_svod_cols) == 1:
        return out_dct

    else:
        for idx, name_column in enumerate(lst_svod_cols):
            lst_reindex_main_column_cols = [lst_svod_cols[idx], 'очень низкое значение', 'низкое значение', 'среднее значение',
                'высокое значение', 'очень высокое значение',
                                            'Итого']

            svod_count_column_level_ei_df = calc_count_level(base_df, lst_svod_cols[idx],
                                                             'Значение_общего_ЭИ',
                                                             'Уровень_общего_ЭИ',
                                                             lst_reindex_main_column_cols)
            svod_count_column_level_mei_df = calc_count_level(base_df, lst_svod_cols[idx],
                                                              'Значение_шкалы_МЭИ',
                                                              'Уровень_шкалы_МЭИ',
                                                              lst_reindex_main_column_cols)
            svod_count_column_level_vei_df = calc_count_level(base_df, lst_svod_cols[idx],
                                                              'Значение_шкалы_ВЭИ',
                                                              'Уровень_шкалы_ВЭИ',
                                                              lst_reindex_main_column_cols)
            svod_count_column_level_pa_df = calc_count_level(base_df, lst_svod_cols[idx],
                                                             'Значение_шкалы_ПЭ',
                                                             'Уровень_шкалы_ПЭ',
                                                             lst_reindex_main_column_cols)
            svod_count_column_level_ua_df = calc_count_level(base_df, lst_svod_cols[idx],
                                                             'Значение_шкалы_УЭ',
                                                             'Уровень_шкалы_УЭ',
                                                             lst_reindex_main_column_cols)

            svod_count_column_level_mp_df = calc_count_level(base_df, lst_svod_cols[idx],
                                                             'Значение_субшкалы_МП',
                                                             'Уровень_субшкалы_МП',
                                                             lst_reindex_main_column_cols)
            svod_count_column_level_mu_df = calc_count_level(base_df, lst_svod_cols[idx],
                                                             'Значение_субшкалы_МУ',
                                                             'Уровень_субшкалы_МУ',
                                                             lst_reindex_main_column_cols)
            svod_count_column_level_vp_df = calc_count_level(base_df, lst_svod_cols[idx],
                                                             'Значение_субшкалы_ВП',
                                                             'Уровень_субшкалы_ВП',
                                                             lst_reindex_main_column_cols)
            svod_count_column_level_vu_df = calc_count_level(base_df, lst_svod_cols[idx],
                                                             'Значение_субшкалы_ВУ',
                                                             'Уровень_субшкалы_ВУ',
                                                             lst_reindex_main_column_cols)
            svod_count_column_level_va_df = calc_count_level(base_df, lst_svod_cols[idx],
                                                             'Значение_субшкалы_ВЭ',
                                                             'Уровень_субшкалы_ВЭ',
                                                             lst_reindex_main_column_cols)

            # Считаем среднее по субшкалам
            svod_mean_column_df = pd.pivot_table(base_df,
                                                 index=[lst_svod_cols[idx]],
                                                 values=['Значение_общего_ЭИ',
                                                         'Значение_шкалы_МЭИ',
                                                         'Значение_шкалы_ВЭИ',
                                                         'Значение_шкалы_ПЭ',
                                                         'Значение_шкалы_УЭ',
                                                         'Значение_субшкалы_МП',
                                                         'Значение_субшкалы_МУ',
                                                         'Значение_субшкалы_ВП',
                                                         'Значение_субшкалы_ВУ',
                                                         'Значение_субшкалы_ВЭ',
                                                         ],
                                                 aggfunc=round_mean)
            svod_mean_column_df.reset_index(inplace=True)
            # упорядочиваем колонки
            new_order_cols = [lst_svod_cols[idx]].copy()
            new_order_cols.extend((['Значение_общего_ЭИ',
                                    'Значение_шкалы_МЭИ',
                                    'Значение_шкалы_ВЭИ',
                                    'Значение_шкалы_ПЭ',
                                    'Значение_шкалы_УЭ',
                                    'Значение_субшкалы_МП',
                                    'Значение_субшкалы_МУ',
                                    'Значение_субшкалы_ВП',
                                    'Значение_субшкалы_ВУ',
                                    'Значение_субшкалы_ВЭ',
                                    ]))
            svod_mean_column_df = svod_mean_column_df.reindex(columns=new_order_cols)

            dct_rename_cols_mean = {'Значение_общего_ЭИ': 'Ср. ОЭИ',
                                    'Значение_шкалы_МЭИ': 'Ср. МЭИ',
                                    'Значение_шкалы_ВЭИ': 'Ср. ВЭИ',
                                    'Значение_шкалы_ПЭ': 'Ср. ПЭ',
                                    'Значение_шкалы_УЭ': 'Ср. УЭ',
                                    'Значение_субшкалы_МП': 'Ср. МП',
                                    'Значение_субшкалы_МУ': 'Ср. МУ',
                                    'Значение_субшкалы_ВП': 'Ср. ВП',
                                    'Значение_субшкалы_ВУ': 'Ср. ВУ',
                                    'Значение_субшкалы_ВЭ': 'Ср. ВЭ',
                                    }
            svod_mean_column_df.rename(columns=dct_rename_cols_mean, inplace=True)

            name_column = lst_svod_cols[idx]
            name_column = re.sub(r'[\[\]\'+()<> :"?*|\\/]', '_', name_column)
            name_column = name_column[:15]

            out_dct.update({f'Ср {name_column}': svod_mean_column_df,
                            f'Свод ОЭИ {name_column}': svod_count_column_level_ei_df,
                            f'Свод МЭИ {name_column}': svod_count_column_level_mei_df,
                            f'Свод ВЭИ {name_column}': svod_count_column_level_vei_df,
                            f'Свод ПЭ {name_column}': svod_count_column_level_pa_df,
                            f'Свод УЭ {name_column}': svod_count_column_level_ua_df,

                            f'Свод МП {name_column}': svod_count_column_level_mp_df,
                            f'Свод МУ {name_column}': svod_count_column_level_mu_df,
                            f'Свод ВП {name_column}': svod_count_column_level_vp_df,
                            f'Свод ВУ {name_column}': svod_count_column_level_vu_df,
                            f'Свод ВЭ {name_column}': svod_count_column_level_va_df,
                            })
        return out_dct









def processing_lusin_ei(result_df: pd.DataFrame, answers_df: pd.DataFrame, lst_svod_cols:list):
    """
    Функция для обработки
    :param result_df: часть датафрейма с описательными колонками
    :param answers_df: часть датафрейма с ответами
    :param lst_svod_cols:  список с колонками по которым нужно делать свод
    """
    try:
        out_answer_df = result_df.copy()  # делаем копию для последующего соединения с сырыми ответами
        if len(answers_df.columns) != 46:  # проверяем количество колонок с вопросами
            raise BadCountColumnsLEI

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
            raise BadOrderLEI

        # словарь для замены слов на числа
        dct_replace_value = {'совсем не согласен': 0,
                             'скорее не согласен': 1,
                             'скорее согласен': 2,
                             'полностью согласен': 3}

        valid_values = [0, 1, 2, 3]
        answers_df.replace(dct_replace_value, inplace=True)  # заменяем слова на цифры для подсчетов

        # Проверяем, есть ли значения, отличающиеся от указанных в списке
        lst_error_answers = []  # список для хранения строк где найдены неправильные ответы

        for i in range(46):
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
            raise BadValueLEI

        base_df = pd.DataFrame()
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
        base_df['Значение_шкалы_ВЭИ'] = base_df['Значение_субшкалы_ВП'] + base_df['Значение_субшкалы_ВУ'] + base_df[
            'Значение_субшкалы_ВЭ']
        base_df['Норма_ВЭИ'] = '34-54 баллов'
        base_df['Уровень_шкалы_ВЭИ'] = base_df['Значение_шкалы_ВЭИ'].apply(calc_level_vei)
        base_df['Стенайн_шкалы_ВЭИ'] = base_df['Значение_шкалы_ВЭИ'].apply(calc_stenain_vei)

        # Шкала ПЭ Понимание эмоций
        base_df['Значение_шкалы_ПЭ'] = base_df['Значение_субшкалы_МП'] + base_df['Значение_субшкалы_ВП']
        base_df['Норма_ПЭ'] = '34-54 баллов'
        base_df['Уровень_шкалы_ПЭ'] = base_df['Значение_шкалы_ПЭ'].apply(calc_level_pa)
        base_df['Стенайн_шкалы_ПЭ'] = base_df['Значение_шкалы_ПЭ'].apply(calc_stenain_pa)

        # Шкала УЭ Управление эмоциями
        base_df['Значение_шкалы_УЭ'] = base_df['Значение_субшкалы_МУ'] + base_df['Значение_субшкалы_ВУ'] + base_df[
            'Значение_субшкалы_ВЭ']
        base_df['Норма_УЭ'] = '34-53 баллов'
        base_df['Уровень_шкалы_УЭ'] = base_df['Значение_шкалы_УЭ'].apply(calc_level_ua)
        base_df['Стенайн_шкалы_УЭ'] = base_df['Значение_шкалы_ПЭ'].apply(calc_stenain_ua)

        # Создаем датафрейм для создания части в общий датафрейм
        part_df = pd.DataFrame()

        part_df['ЛЭИ_ОЭИ_Значение'] = base_df['Значение_общего_ЭИ']
        part_df['ЛЭИ_ОЭИ_Уровень'] = base_df['Уровень_общего_ЭИ']


        part_df['ЛЭИ_МЭИ_Значение'] = base_df['Значение_шкалы_МЭИ']
        part_df['ЛЭИ_МЭИ_Уровень'] = base_df['Уровень_шкалы_МЭИ']

        part_df['ЛЭИ_ВЭИ_Значение'] = base_df['Значение_шкалы_ВЭИ']
        part_df['ЛЭИ_ВЭИ_Уровень'] = base_df['Уровень_шкалы_ВЭИ']

        part_df['ЛЭИ_ПЭ_Значение'] = base_df['Значение_шкалы_ПЭ']
        part_df['ЛЭИ_ПЭ_Уровень'] = base_df['Уровень_шкалы_ПЭ']

        part_df['ЛЭИ_УЭ_Значение'] = base_df['Значение_шкалы_УЭ']
        part_df['ЛЭИ_УЭ_Уровень'] = base_df['Уровень_шкалы_УЭ']

        out_answer_df = pd.concat([out_answer_df, answers_df], axis=1)  # Датафрейм для проверки

        new_order_cols = ['Значение_общего_ЭИ','Норма_общего_ЭИ','Уровень_общего_ЭИ',
                          'Значение_шкалы_МЭИ', 'Норма_МЭИ', 'Уровень_шкалы_МЭИ','Стенайн_шкалы_МЭИ',
                          'Значение_шкалы_ВЭИ', 'Норма_ВЭИ', 'Уровень_шкалы_ВЭИ','Стенайн_шкалы_ВЭИ',
                          'Значение_шкалы_ПЭ', 'Норма_ПЭ', 'Уровень_шкалы_ПЭ','Стенайн_шкалы_ПЭ',
                          'Значение_шкалы_УЭ', 'Норма_УЭ', 'Уровень_шкалы_УЭ','Стенайн_шкалы_УЭ',
                          'Значение_субшкалы_МП','Норма_МП','Уровень_субшкалы_МП',
                          'Значение_субшкалы_МУ','Норма_МУ','Уровень_субшкалы_МУ',
                          'Значение_субшкалы_ВП','Норма_ВП','Уровень_субшкалы_ВП',
                          'Значение_субшкалы_ВУ','Норма_ВУ','Уровень_субшкалы_ВУ',
                          'Значение_субшкалы_ВЭ','Норма_ВЭ','Уровень_субшкалы_ВЭ',

                          ]
        base_df = base_df.reindex(columns=new_order_cols)

        # Соединяем анкетную часть с результатной
        base_df = pd.concat([result_df, base_df], axis=1)
        base_df.sort_values(by='Значение_общего_ЭИ', ascending=False, inplace=True)  # сортируем

        # формируем основной словарь
        out_dct = {'Списочный результат': base_df, 'Список для проверки': out_answer_df,
                   }

        # Делаем свод по интегральным показателям
        dct_svod_integral = {'Значение_общего_ЭИ': 'Уровень_общего_ЭИ',
                             'Значение_шкалы_МЭИ': 'Уровень_шкалы_МЭИ',
                             'Значение_шкалы_ВЭИ': 'Уровень_шкалы_ВЭИ',
                             'Значение_шкалы_ПЭ': 'Уровень_шкалы_ПЭ',
                             'Значение_шкалы_УЭ': 'Уровень_шкалы_УЭ',

                             'Значение_субшкалы_МП': 'Уровень_субшкалы_МП',
                             'Значение_субшкалы_МУ': 'Уровень_субшкалы_МУ',
                             'Значение_субшкалы_ВП': 'Уровень_субшкалы_ВП',
                             'Значение_субшкалы_ВУ': 'Уровень_субшкалы_ВУ',
                             'Значение_субшкалы_ВЭ': 'Уровень_субшкалы_ВЭ',
                             }

        dct_rename_svod_integral = {'Значение_общего_ЭИ': 'ОЭИ',
                             'Значение_шкалы_МЭИ': 'МЭИ',
                             'Значение_шкалы_ВЭИ': 'ВЭИ',
                             'Значение_шкалы_ПЭ': 'ПЭ',
                             'Значение_шкалы_УЭ': 'УЭ',

                             'Значение_субшкалы_МП': 'МП',
                             'Значение_субшкалы_МУ': 'МУ',
                             'Значение_субшкалы_ВП': 'ВП',
                             'Значение_субшкалы_ВУ': 'ВУ',
                             'Значение_субшкалы_ВЭ': 'ВЭ',
                                    }

        lst_integral = ['очень низкое значение', 'низкое значение', 'среднее значение',
                         'высокое значение', 'очень высокое значение']


        base_svod_integral_df = create_union_svod(base_df, dct_svod_integral, dct_rename_svod_integral, lst_integral)

        # Стенайны

        # считаем среднее
        avg_ei = round(base_df['Значение_общего_ЭИ'].mean(), 2)
        avg_mei = round(base_df['Значение_шкалы_МЭИ'].mean(), 2)
        avg_vei = round(base_df['Значение_шкалы_ВЭИ'].mean(), 2)
        avg_pa = round(base_df['Значение_шкалы_ПЭ'].mean(), 2)
        avg_ua = round(base_df['Значение_шкалы_УЭ'].mean(), 2)
        avg_mp = round(base_df['Значение_субшкалы_МП'].mean(), 2)
        avg_mu = round(base_df['Значение_субшкалы_МУ'].mean(), 2)
        avg_vp = round(base_df['Значение_субшкалы_ВП'].mean(), 2)
        avg_vu = round(base_df['Значение_субшкалы_ВУ'].mean(), 2)
        avg_va = round(base_df['Значение_субшкалы_ВЭ'].mean(), 2)

        avg_dct = {'Среднее значение Общий эмоциональный интеллект ': avg_ei,
                   'Среднее значение шкалы Межличностный эмоциональный интеллект': avg_mei,
                   'Среднее значение шкалы Внутриличностный эмоциональный интеллект': avg_vei,
                   'Среднее значение шкалы Понимание эмоций': avg_pa,
                   'Среднее значение шкалы Управление эмоциями': avg_ua,
                   'Среднее значение субшкалы Понимание чужих эмоций': avg_mp,
                   'Среднее значение субшкалы Управление чужими эмоциями': avg_mu,
                   'Среднее значение субшкалы Понимание своих эмоций': avg_vp,
                   'Среднее значение субшкалы Управление своими эмоциями': avg_vu,
                   'Среднее значение субшкалы Контроль экспрессии': avg_va,

                   }

        avg_df = pd.DataFrame.from_dict(avg_dct, orient='index')
        avg_df = avg_df.reset_index()
        avg_df.columns = ['Показатель', 'Среднее значение']

        out_dct.update({'Свод Шкалы': base_svod_integral_df,
                        'Среднее': avg_df}
                       )

        # Создаем листы со списками общему интеллекту
        dct_level = dict()
        for level in lst_integral:
            temp_df = base_df[base_df['Уровень_общего_ЭИ'] == level]
            if temp_df.shape[0] != 0:
                dct_level[level] = temp_df

        out_dct.update(dct_level)

        """
            Сохраняем в зависимости от необходимости делать своды по определенным колонкам
            """
        if len(lst_svod_cols) == 0:
            return out_dct, part_df
        else:
            out_dct = create_result_lei(base_df, out_dct, lst_svod_cols)

            return out_dct, part_df

    except BadOrderLEI:
        messagebox.showerror('Лахеcис',
                             f'При обработке вопросов теста Эмоциональный интеллект Люсин обнаружены неправильные вопросы. Проверьте названия колонок с вопросами:\n'
                             f'{error_order_message}\n'
                             f'Используйте при создании Яндекс-формы написание вопросов из руководства пользователя программы Лахесис.')
    except BadValueLEI:
        messagebox.showerror('Лахеcис',
                             f'При обработке вопросов теста Эмоциональный интеллект Люсин обнаружены неправильные варианты ответов. Проверьте ответы на указанных строках:\n'
                             f'{error_message}\n'
                             f'Используйте при создании Яндекс-формы написание вариантов ответа из руководства пользователя программы Лахесис.')

    except BadCountColumnsLEI:
        messagebox.showerror('Лахеcис',
                             f'Проверьте количество колонок с ответами на тест Эмоциональный интеллект Люсин\n'
                             f'Должно быть 46 колонок с вопросами'
                             )







