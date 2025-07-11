"""
Скрипт для обработки результатов теста Шкала социально психологической адаптированности Роджерс Даймонд Снегирева
"""

import pandas as pd
import re
from tkinter import messagebox
from lachesis_support_functions import round_mean,create_list_on_level, create_union_svod


class BadOrderRDSSPA(Exception):
    """
    Исключение для обработки случая когда колонки не совпадают
    """
    pass


class BadValueRDSSPA(Exception):
    """
    Исключение для неправильных значений в вариантах ответов
    """
    pass

class BadCountColumnsRDSSPA(Exception):
    """
    Исключение для обработки случая если количество колонок не равно 101
    """
    pass


def calc_sub_value_adapt(row):
    """
    Функция для подсчета значения субшкалы
    :param row: строка с ответами
    :return: число
    """
    lst_pr = [4,5,9,12,15,19,22,23,26,27,29,33,35,37,41,44,47,51,53,55,61,63,67,72,74,75,78,80,88,91,94,96,97,98]

    value_forward = 0 # счетчик прямых ответов

    for idx, value in enumerate(row):
        if idx +1 in lst_pr:
            value_forward += value

    return value_forward



def calc_level_sub_adapt(value):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """
    if 0 <= value <= 67:
        return 'очень низкий уровень'
    elif 68 <= value <= 170:
        return 'зона неопределенности'
    else:
        return 'очень высокий уровень'



def calc_sub_value_desadapt(row):
    """
    Функция для подсчета значения субшкалы
    :param row: строка с ответами
    :return: число
    """
    lst_pr = [2,6,7,13,16,18,25,28,32,36,38,40,42,43,49,50,54,56,59,60,62,64,69,71,73,76,77,83,84,86,90,95,99,100]

    value_forward = 0 # счетчик прямых ответов

    for idx, value in enumerate(row):
        if idx +1 in lst_pr:
            value_forward += value

    return value_forward



def calc_level_sub_desadapt(value):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """
    if 0 <= value <= 67:
        return 'очень низкий уровень'
    elif 68 <= value <= 170:
        return 'зона неопределенности'
    else:
        return 'очень высокий уровень'



def calc_adapt(row:pd.Series):
    """
    Функция для подсчета значения интегрального показателя
    :param row: строка с ответами
    :return: число
    """
    lst_row = row.tolist()
    a = lst_row[0]
    b = lst_row[1]
    if a == 0 and b == 0:
        return 0
    else:
        return round((a / (a+b)) * 100,2)




def calc_sub_value_lie_minus(row):
    """
    Функция для подсчета значения субшкалы
    :param row: строка с ответами
    :return: число
    """
    lst_pr = [34,45,48,81,89]

    value_forward = 0 # счетчик прямых ответов

    for idx, value in enumerate(row):
        if idx +1 in lst_pr:
            value_forward += value

    return value_forward


def calc_sub_value_lie_plus(row):
    """
    Функция для подсчета значения субшкалы
    :param row: строка с ответами
    :return: число
    """
    lst_pr = [8,82,92,101]

    value_forward = 0 # счетчик прямых ответов

    for idx, value in enumerate(row):
        if idx +1 in lst_pr:
            value_forward += value

    return value_forward


def calc_sincerity(value):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """
    if 0 <= value <= 17:
        return 'очень низкий уровень'
    elif 18 <= value <= 45:
        return 'зона неопределенности'
    else:
        return 'очень высокий уровень'






def calc_sub_value_self_accept(row):
    """
    Функция для подсчета значения субшкалы
    :param row: строка с ответами
    :return: число
    """
    lst_pr = [33,35,55,67,72,74,75,80,88,94,96]

    value_forward = 0 # счетчик прямых ответов

    for idx, value in enumerate(row):
        if idx +1 in lst_pr:
            value_forward += value

    return value_forward



def calc_level_sub_self_accept(value):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """
    if 0 <= value <= 21:
        return 'очень низкий уровень'
    elif 22 <= value <= 52:
        return 'зона неопределенности'
    else:
        return 'очень высокий уровень'


def calc_sub_value_not_self_accept(row):
    """
    Функция для подсчета значения субшкалы
    :param row: строка с ответами
    :return: число
    """
    lst_pr = [7,59,62,65,90,95,99]

    value_forward = 0 # счетчик прямых ответов

    for idx, value in enumerate(row):
        if idx +1 in lst_pr:
            value_forward += value

    return value_forward



def calc_level_sub_not_self_accept(value):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """
    if 0 <= value <= 13:
        return 'очень низкий уровень'
    elif 14 <= value <= 35:
        return 'зона неопределенности'
    else:
        return 'очень высокий уровень'


def calc_self_accept(row:pd.Series):
    """
    Функция для подсчета значения интегрального показателя
    :param row: строка с ответами
    :return: число
    """
    lst_row = row.tolist()
    a = lst_row[0]
    b = lst_row[1]
    if a == 0 and b == 0:
        return 0
    else:
        return round((a / (a+(1.6*b))) * 100,2)





def calc_sub_value_other_accept(row):
    """
    Функция для подсчета значения субшкалы
    :param row: строка с ответами
    :return: число
    """
    lst_pr = [9,14,22,26,53,97]

    value_forward = 0 # счетчик прямых ответов

    for idx, value in enumerate(row):
        if idx +1 in lst_pr:
            value_forward += value

    return value_forward



def calc_level_sub_other_accept(value):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """
    if 0 <= value <= 11:
        return 'очень низкий уровень'
    elif 12 <= value <= 30:
        return 'зона неопределенности'
    else:
        return 'очень высокий уровень'


def calc_sub_value_not_other_accept(row):
    """
    Функция для подсчета значения субшкалы
    :param row: строка с ответами
    :return: число
    """
    lst_pr = [2,10,21,28,40,60,76]

    value_forward = 0 # счетчик прямых ответов

    for idx, value in enumerate(row):
        if idx +1 in lst_pr:
            value_forward += value

    return value_forward



def calc_level_sub_not_other_accept(value):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """
    if 0 <= value <= 13:
        return 'очень низкий уровень'
    elif 14 <= value <= 35:
        return 'зона неопределенности'
    else:
        return 'очень высокий уровень'


def calc_other_accept(row:pd.Series):
    """
    Функция для подсчета значения интегрального показателя
    :param row: строка с ответами
    :return: число
    """
    lst_row = row.tolist()
    a = lst_row[0]
    b = lst_row[1]
    if a == 0 and b == 0:
        return 0
    else:
        return round(((1.2*a) / ((1.2*a)+b)) * 100,2)




def calc_sub_value_em_comfort(row):
    """
    Функция для подсчета значения субшкалы
    :param row: строка с ответами
    :return: число
    """
    lst_pr = [23,29,30,41,44,47,78]

    value_forward = 0 # счетчик прямых ответов

    for idx, value in enumerate(row):
        if idx +1 in lst_pr:
            value_forward += value

    return value_forward



def calc_level_sub_em_comfort(value):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """
    if 0 <= value <= 13:
        return 'очень низкий уровень'
    elif 14 <= value <= 35:
        return 'зона неопределенности'
    else:
        return 'очень высокий уровень'


def calc_sub_value_em_discomfort(row):
    """
    Функция для подсчета значения субшкалы
    :param row: строка с ответами
    :return: число
    """
    lst_pr = [6,42,43,49,50,83,85]

    value_forward = 0 # счетчик прямых ответов

    for idx, value in enumerate(row):
        if idx +1 in lst_pr:
            value_forward += value

    return value_forward



def calc_level_sub_em_discomfort(value):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """
    if 0 <= value <= 13:
        return 'очень низкий уровень'
    elif 14 <= value <= 35:
        return 'зона неопределенности'
    else:
        return 'очень высокий уровень'



def calc_comfort(row:pd.Series):
    """
    Функция для подсчета значения интегрального показателя
    :param row: строка с ответами
    :return: число
    """
    lst_row = row.tolist()
    a = lst_row[0]
    b = lst_row[1]
    if a == 0 and b == 0:
        return 0
    else:
        return round((a / (a+b)) * 100,2)



def calc_sub_value_self_control(row):
    """
    Функция для подсчета значения субшкалы
    :param row: строка с ответами
    :return: число
    """
    lst_pr = [4,5,11,12,13,19,27,37,51,63,68,79,91,98]

    value_forward = 0 # счетчик прямых ответов

    for idx, value in enumerate(row):
        if idx +1 in lst_pr:
            value_forward += value

    return value_forward



def calc_level_sub_self_control(value):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """
    if 0 <= value <= 25:
        return 'очень низкий уровень'
    elif 26 <= value <= 65:
        return 'зона неопределенности'
    else:
        return 'очень высокий уровень'


def calc_sub_value_outer_control(row):
    """
    Функция для подсчета значения субшкалы
    :param row: строка с ответами
    :return: число
    """
    lst_pr = [25,36,52,57,70,71,73,77]

    value_forward = 0 # счетчик прямых ответов

    for idx, value in enumerate(row):
        if idx +1 in lst_pr:
            value_forward += value

    return value_forward



def calc_level_sub_outer_control(value):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """
    if 0 <= value <= 17:
        return 'очень низкий уровень'
    elif 18 <= value <= 45:
        return 'зона неопределенности'
    else:
        return 'очень высокий уровень'


def calc_control(row:pd.Series):
    """
    Функция для подсчета значения интегрального показателя
    :param row: строка с ответами
    :return: число
    """
    lst_row = row.tolist()
    a = lst_row[0]
    b = lst_row[1]
    if a == 0 and b == 0:
        return 0
    else:
        return round((a / (a+(1.4*b))) * 100,2)





def calc_sub_value_dominating(row):
    """
    Функция для подсчета значения субшкалы
    :param row: строка с ответами
    :return: число
    """
    lst_pr = [58,61,66]

    value_forward = 0 # счетчик прямых ответов

    for idx, value in enumerate(row):
        if idx +1 in lst_pr:
            value_forward += value

    return value_forward



def calc_level_sub_dominating(value):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """
    if 0 <= value <= 5:
        return 'очень низкий уровень'
    elif 6 <= value <= 15:
        return 'зона неопределенности'
    else:
        return 'очень высокий уровень'


def calc_sub_value_not_domin(row):
    """
    Функция для подсчета значения субшкалы
    :param row: строка с ответами
    :return: число
    """
    lst_pr = [16,32,38,69,84,87]

    value_forward = 0 # счетчик прямых ответов

    for idx, value in enumerate(row):
        if idx +1 in lst_pr:
            value_forward += value

    return value_forward



def calc_level_sub_not_domin(value):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """
    if 0 <= value <= 11:
        return 'очень низкий уровень'
    elif 12 <= value <= 30:
        return 'зона неопределенности'
    else:
        return 'очень высокий уровень'


def calc_dominating(row:pd.Series):
    """
    Функция для подсчета значения интегрального показателя
    :param row: строка с ответами
    :return: число
    """
    lst_row = row.tolist()
    a = lst_row[0]
    b = lst_row[1]
    if a == 0 and b == 0:
        return 0
    else:
        return round((2*a / ((2*a)+b)) * 100,2)



def calc_sub_value_escape(row):
    """
    Функция для подсчета значения субшкалы
    :param row: строка с ответами
    :return: число
    """
    lst_pr = [17,18,54,64,86]

    value_forward = 0 # счетчик прямых ответов

    for idx, value in enumerate(row):
        if idx +1 in lst_pr:
            value_forward += value

    return value_forward



def calc_level_sub_escape(value):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """
    if 0 <= value <= 9:
        return 'очень низкий уровень'
    elif 10 <= value <= 25:
        return 'зона неопределенности'
    else:
        return 'очень высокий уровень'


def calc_level_integral(value):
    """
    Функция для подсчета уровня интегральных показателей
    :param value:
    :return:
    """
    if 0 <= value <= 39:
        return 'низкий уровень'
    elif 40 <= value <= 60:
        return 'средний уровень'
    else:
        return 'высокий уровень'

def calc_count_level_sub(df:pd.DataFrame, lst_cat:list, val_cat, col_cat, lst_cols:list):
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
    count_df['% очень низкий уровень от общего'] = round(
        count_df['очень низкий уровень'] / count_df['Итого'], 2) * 100
    count_df['% зона неопределенности от общего'] = round(
        count_df['зона неопределенности'] / count_df['Итого'], 2) * 100
    count_df['% очень высокий уровень от общего'] = round(
        count_df['очень высокий уровень'] / count_df['Итого'], 2) * 100

    return count_df


def calc_count_level_integral(df:pd.DataFrame, lst_cat:list, val_cat, col_cat, lst_cols:list):
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
    count_df['% низкий уровень от общего'] = round(
        count_df['низкий уровень'] / count_df['Итого'], 2) * 100
    count_df['% средний уровень от общего'] = round(
        count_df['средний уровень'] / count_df['Итого'], 2) * 100
    count_df['% высокий уровень от общего'] = round(
        count_df['высокий уровень'] / count_df['Итого'], 2) * 100

    return count_df


def create_result_rdsspa(base_df:pd.DataFrame, out_dct:dict, lst_svod_cols:list):
    """
    Функция для подсчета результата если указаны колонки по которым нужно провести свод
    :param df: датафрейм с результатами
    :param out_dct: словарь с уже подсчитанными базовыми данными
    :param lst_svod_cols: список сводных колонок
    :return: словарь
    """
    lst_reindex_main_level_cols = lst_svod_cols.copy()
    lst_reindex_main_level_cols.extend( ['низкий уровень','средний уровень','высокий уровень',
                                   'Итого'])  # Основная шкала


    lst_reindex_sub_level_cols = lst_svod_cols.copy()
    lst_reindex_sub_level_cols.extend( ['очень низкий уровень','зона неопределенности','очень высокий уровень',
                                   'Итого'])  # Субшкалы

    # Интегральные показатели
    svod_count_one_level_integral_adapt_df = calc_count_level_integral(base_df, lst_svod_cols,
                                                      'Значение_ИП_Адаптация',
                                                      'Уровень_ИП_Адаптация',
                                                      lst_reindex_main_level_cols)
    svod_count_one_level_integral_self_df = calc_count_level_integral(base_df, lst_svod_cols,
                                                      'Значение_ИП_Самопринятие',
                                                      'Уровень_ИП_Самопринятие',
                                                      lst_reindex_main_level_cols)
    svod_count_one_level_integral_other_df = calc_count_level_integral(base_df, lst_svod_cols,
                                                      'Значение_ИП_Принятие_других',
                                                      'Уровень_ИП_Принятие_других',
                                                      lst_reindex_main_level_cols)
    svod_count_one_level_integral_em_comfort_df = calc_count_level_integral(base_df, lst_svod_cols,
                                                      'Значение_ИП_Эмоциональный_комфорт',
                                                      'Уровень_ИП_Эмоциональный_комфорт',
                                                      lst_reindex_main_level_cols)
    svod_count_one_level_integral_internal_df = calc_count_level_integral(base_df, lst_svod_cols,
                                                      'Значение_ИП_Интернальность',
                                                      'Уровень_ИП_Интернальность',
                                                      lst_reindex_main_level_cols)
    svod_count_one_level_integral_domin_df = calc_count_level_integral(base_df, lst_svod_cols,
                                                      'Значение_ИП_Стремление_к_доминированию',
                                                      'Уровень_ИП_Стремление_к_доминированию',
                                                      lst_reindex_main_level_cols)



    # Субшкалы
    svod_count_one_level_adapt_df = calc_count_level_sub(base_df, lst_svod_cols,
                                                      'Значение_субшкалы_Адаптивность',
                                                      'Уровень_субшкалы_Адаптивность',
                                                      lst_reindex_sub_level_cols)
    svod_count_one_level_desadapt_df = calc_count_level_sub(base_df, lst_svod_cols,
                                                      'Значение_субшкалы_Дезадаптивность',
                                                      'Уровень_субшкалы_Дезадаптивность',
                                                      lst_reindex_sub_level_cols)
    svod_count_one_level_lie_df = calc_count_level_sub(base_df, lst_svod_cols,
                                                      'Значение_шкалы_Искренность',
                                                      'Уровень_шкалы_Искренность',
                                                      lst_reindex_sub_level_cols)

    svod_count_one_level_self_accept_df = calc_count_level_sub(base_df, lst_svod_cols,
                                                      'Значение_субшкалы_Принятие_себя',
                                                      'Уровень_субшкалы_Принятие_себя',
                                                      lst_reindex_sub_level_cols)
    svod_count_one_level_not_self_accept_df = calc_count_level_sub(base_df, lst_svod_cols,
                                                      'Значение_субшкалы_Непринятие_себя',
                                                      'Уровень_субшкалы_Непринятие_себя',
                                                      lst_reindex_sub_level_cols)

    svod_count_one_level_other_accept_df = calc_count_level_sub(base_df, lst_svod_cols,
                                                      'Значение_субшкалы_Принятие_других',
                                                      'Уровень_субшкалы_Принятие_других',
                                                      lst_reindex_sub_level_cols)
    svod_count_one_level_not_other_accept_df = calc_count_level_sub(base_df, lst_svod_cols,
                                                      'Значение_субшкалы_Непринятие_других',
                                                      'Уровень_субшкалы_Непринятие_других',
                                                      lst_reindex_sub_level_cols)

    svod_count_one_level_em_comfort_df = calc_count_level_sub(base_df, lst_svod_cols,
                                                      'Значение_субшкалы_Эмоциональный_комфорт',
                                                      'Уровень_субшкалы_Эмоциональный_комфорт',
                                                      lst_reindex_sub_level_cols)
    svod_count_one_level_em_discomfort_df = calc_count_level_sub(base_df, lst_svod_cols,
                                                      'Значение_субшкалы_Эмоциональный_дискомфорт',
                                                      'Уровень_субшкалы_Эмоциональный_дискомфорт',
                                                      lst_reindex_sub_level_cols)

    svod_count_one_level_self_control_df = calc_count_level_sub(base_df, lst_svod_cols,
                                                      'Значение_субшкалы_Внутренний_контроль',
                                                      'Уровень_субшкалы_Внутренний_контроль',
                                                      lst_reindex_sub_level_cols)
    svod_count_one_level_outer_control_df = calc_count_level_sub(base_df, lst_svod_cols,
                                                      'Значение_субшкалы_Внешний_контроль',
                                                      'Уровень_субшкалы_Внешний_контроль',
                                                      lst_reindex_sub_level_cols)

    svod_count_one_level_dominating_df = calc_count_level_sub(base_df, lst_svod_cols,
                                                      'Значение_субшкалы_Доминирование',
                                                      'Уровень_субшкалы_Доминирование',
                                                      lst_reindex_sub_level_cols)
    svod_count_one_level_not_domin_df = calc_count_level_sub(base_df, lst_svod_cols,
                                                      'Значение_субшкалы_Ведомость',
                                                      'Уровень_субшкалы_Ведомость',
                                                      lst_reindex_sub_level_cols)

    svod_count_one_level_escape_df = calc_count_level_sub(base_df, lst_svod_cols,
                                                      'Значение_субшкалы_Эскапизм',
                                                      'Уровень_субшкалы_Эскапизм',
                                                      lst_reindex_sub_level_cols)

    # Считаем среднее по субшкалам
    svod_mean_one_df = pd.pivot_table(base_df,
                                  index=lst_svod_cols,
                                  values=['Значение_шкалы_Искренность',
                                          'Значение_ИП_Адаптация',
                                          'Значение_ИП_Самопринятие',
                                          'Значение_ИП_Принятие_других',
                                          'Значение_ИП_Эмоциональный_комфорт',
                                          'Значение_ИП_Интернальность',
                                          'Значение_ИП_Стремление_к_доминированию',
                                          'Значение_субшкалы_Адаптивность',
                                          'Значение_субшкалы_Дезадаптивность',
                                          'Значение_субшкалы_Лживость_c_минусом',
                                          'Значение_субшкалы_Лживость_с_плюсом',
                                          'Значение_субшкалы_Принятие_себя',
                                          'Значение_субшкалы_Непринятие_себя',
                                          'Значение_субшкалы_Принятие_других',
                                          'Значение_субшкалы_Непринятие_других',
                                          'Значение_субшкалы_Эмоциональный_комфорт',
                                          'Значение_субшкалы_Эмоциональный_дискомфорт',
                                          'Значение_субшкалы_Внутренний_контроль',
                                          'Значение_субшкалы_Внешний_контроль',
                                          'Значение_субшкалы_Доминирование',
                                          'Значение_субшкалы_Ведомость',
                                          'Значение_субшкалы_Эскапизм'
                                          ],
                                  aggfunc=round_mean)
    svod_mean_one_df.reset_index(inplace=True)
    # упорядочиваем колонки
    new_order_cols = lst_svod_cols.copy()
    new_order_cols.extend((['Значение_шкалы_Искренность','Значение_ИП_Адаптация',
                                          'Значение_ИП_Самопринятие',
                                          'Значение_ИП_Принятие_других',
                                          'Значение_ИП_Эмоциональный_комфорт',
                                          'Значение_ИП_Интернальность',
                                          'Значение_ИП_Стремление_к_доминированию',
                                          'Значение_субшкалы_Адаптивность',
                                          'Значение_субшкалы_Дезадаптивность',
                                          'Значение_субшкалы_Лживость_c_минусом',
                                          'Значение_субшкалы_Лживость_с_плюсом',
                                          'Значение_субшкалы_Принятие_себя',
                                          'Значение_субшкалы_Непринятие_себя',
                                          'Значение_субшкалы_Принятие_других',
                                          'Значение_субшкалы_Непринятие_других',
                                          'Значение_субшкалы_Эмоциональный_комфорт',
                                          'Значение_субшкалы_Эмоциональный_дискомфорт',
                                          'Значение_субшкалы_Внутренний_контроль',
                                          'Значение_субшкалы_Внешний_контроль',
                                          'Значение_субшкалы_Доминирование',
                                          'Значение_субшкалы_Ведомость',
                                          'Значение_субшкалы_Эскапизм'
                            ]))
    svod_mean_one_df = svod_mean_one_df.reindex(columns=new_order_cols)

    dct_rename_cols_mean = {'Значение_шкалы_Искренность': 'Ср. Искренность',
                             'Значение_ИП_Адаптация': 'Ср. Адаптация',
                            'Значение_ИП_Самопринятие': 'Ср. Самопринятие',
                            'Значение_ИП_Принятие_других': 'Ср. Принятие других',
                            'Значение_ИП_Эмоциональный_комфорт': 'Ср. Эмоциональный комфорт',
                            'Значение_ИП_Интернальность': 'Ср. Интернальность',
                            'Значение_ИП_Стремление_к_доминированию': 'Ср. Стремление к доминированию',

                            'Значение_субшкалы_Адаптивность': 'Ср. Адаптивность',
                            'Значение_субшкалы_Дезадаптивность': 'Ср. Дезадаптивность',
                            'Значение_субшкалы_Лживость_c_минусом': 'Ср. Лживость -',
                            'Значение_субшкалы_Лживость_с_плюсом': 'Ср. Лживость +',
                            'Значение_субшкалы_Принятие_себя': 'Ср. Принятие себя',
                            'Значение_субшкалы_Непринятие_себя': 'Ср. Непринятие себя',
                            'Значение_субшкалы_Принятие_других': 'Ср. Принятие других',
                            'Значение_субшкалы_Непринятие_других': 'Ср. Непринятие других',
                            'Значение_субшкалы_Эмоциональный_комфорт': 'Ср. Эмоциональный комфорт',
                            'Значение_субшкалы_Эмоциональный_дискомфорт': 'Ср. Эмоциональный дискомфорт',
                            'Значение_субшкалы_Внутренний_контроль': 'Ср. Внутренний контроль',
                            'Значение_субшкалы_Внешний_контроль': 'Ср. Внешний контроль',
                            'Значение_субшкалы_Доминирование': 'Ср. Доминирование',
                            'Значение_субшкалы_Ведомость': 'Ср. Ведомость',
                            'Значение_субшкалы_Эскапизм': 'Ср. Эскапизм',
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


    out_dct.update({f'Ср {out_name}':svod_mean_one_df,
                f'Свод Ад {out_name}': svod_count_one_level_integral_adapt_df,
                f'Свод СП {out_name}': svod_count_one_level_integral_self_df,
                f'Свод ПрД {out_name}': svod_count_one_level_integral_other_df,
                f'Свод ЭмК {out_name}': svod_count_one_level_integral_em_comfort_df,
                f'Свод И {out_name}': svod_count_one_level_integral_internal_df,
                f'Свод СКД {out_name}': svod_count_one_level_integral_domin_df,

                f'Свод Искр {out_name}': svod_count_one_level_lie_df,
                f'Свод А {out_name}': svod_count_one_level_adapt_df,
                f'Свод ДА {out_name}': svod_count_one_level_desadapt_df,
                f'Свод ПС {out_name}': svod_count_one_level_self_accept_df,
                f'Свод НС {out_name}': svod_count_one_level_not_self_accept_df,
                f'Свод ПД {out_name}': svod_count_one_level_other_accept_df,
                f'Свод НД {out_name}': svod_count_one_level_not_other_accept_df,
                f'Свод ЭК {out_name}': svod_count_one_level_em_comfort_df,
                f'Свод ЭД {out_name}': svod_count_one_level_em_discomfort_df,
                f'Свод ВнутрК {out_name}': svod_count_one_level_self_control_df,
                f'Свод ВнешК {out_name}': svod_count_one_level_outer_control_df,
                f'Свод Д {out_name}': svod_count_one_level_dominating_df,
                f'Свод В {out_name}': svod_count_one_level_not_domin_df,
                f'Свод Э {out_name}': svod_count_one_level_escape_df,
                    })

    if len(lst_svod_cols) == 1:
        return out_dct

    else:
        for idx, name_column in enumerate(lst_svod_cols):
            lst_reindex_main_column_cols = [lst_svod_cols[idx],'низкий уровень','средний уровень','высокий уровень',
                                   'Итого']  # Основная шкала

            lst_reindex_sub_column_cols = [lst_svod_cols[idx],'очень низкий уровень','зона неопределенности','очень высокий уровень',
                                   'Итого']  # Основная шкала
            # Интегральные показатели
            svod_count_column_level_integral_adapt_df = calc_count_level_integral(base_df, [lst_svod_cols[idx]],
                                                                                  'Значение_ИП_Адаптация',
                                                                                  'Уровень_ИП_Адаптация',
                                                                                  lst_reindex_main_column_cols)
            svod_count_column_level_integral_self_df = calc_count_level_integral(base_df, [lst_svod_cols[idx]],
                                                                                 'Значение_ИП_Самопринятие',
                                                                                 'Уровень_ИП_Самопринятие',
                                                                                 lst_reindex_main_column_cols)
            svod_count_column_level_integral_other_df = calc_count_level_integral(base_df, [lst_svod_cols[idx]],
                                                                                  'Значение_ИП_Принятие_других',
                                                                                  'Уровень_ИП_Принятие_других',
                                                                                  lst_reindex_main_column_cols)
            svod_count_column_level_integral_em_comfort_df = calc_count_level_integral(base_df, [lst_svod_cols[idx]],
                                                                                       'Значение_ИП_Эмоциональный_комфорт',
                                                                                       'Уровень_ИП_Эмоциональный_комфорт',
                                                                                       lst_reindex_main_column_cols)
            svod_count_column_level_integral_internal_df = calc_count_level_integral(base_df, [lst_svod_cols[idx]],
                                                                                     'Значение_ИП_Интернальность',
                                                                                     'Уровень_ИП_Интернальность',
                                                                                     lst_reindex_main_column_cols)
            svod_count_column_level_integral_domin_df = calc_count_level_integral(base_df, [lst_svod_cols[idx]],
                                                                                  'Значение_ИП_Стремление_к_доминированию',
                                                                                  'Уровень_ИП_Стремление_к_доминированию',
                                                                                  lst_reindex_main_column_cols)

            # Субшкалы
            svod_count_column_level_adapt_df = calc_count_level_sub(base_df, [lst_svod_cols[idx]],
                                                                    'Значение_субшкалы_Адаптивность',
                                                                    'Уровень_субшкалы_Адаптивность',
                                                                    lst_reindex_sub_column_cols)
            svod_count_column_level_desadapt_df = calc_count_level_sub(base_df, [lst_svod_cols[idx]],
                                                                       'Значение_субшкалы_Дезадаптивность',
                                                                       'Уровень_субшкалы_Дезадаптивность',
                                                                       lst_reindex_sub_column_cols)
            svod_count_column_level_lie_df = calc_count_level_sub(base_df, [lst_svod_cols[idx]],
                                                                  'Значение_шкалы_Искренность',
                                                                  'Уровень_шкалы_Искренность',
                                                                  lst_reindex_sub_column_cols)

            svod_count_column_level_self_accept_df = calc_count_level_sub(base_df, [lst_svod_cols[idx]],
                                                                          'Значение_субшкалы_Принятие_себя',
                                                                          'Уровень_субшкалы_Принятие_себя',
                                                                          lst_reindex_sub_column_cols)
            svod_count_column_level_not_self_accept_df = calc_count_level_sub(base_df, [lst_svod_cols[idx]],
                                                                              'Значение_субшкалы_Непринятие_себя',
                                                                              'Уровень_субшкалы_Непринятие_себя',
                                                                              lst_reindex_sub_column_cols)

            svod_count_column_level_other_accept_df = calc_count_level_sub(base_df, [lst_svod_cols[idx]],
                                                                           'Значение_субшкалы_Принятие_других',
                                                                           'Уровень_субшкалы_Принятие_других',
                                                                           lst_reindex_sub_column_cols)
            svod_count_column_level_not_other_accept_df = calc_count_level_sub(base_df, [lst_svod_cols[idx]],
                                                                               'Значение_субшкалы_Непринятие_других',
                                                                               'Уровень_субшкалы_Непринятие_других',
                                                                               lst_reindex_sub_column_cols)

            svod_count_column_level_em_comfort_df = calc_count_level_sub(base_df, [lst_svod_cols[idx]],
                                                                         'Значение_субшкалы_Эмоциональный_комфорт',
                                                                         'Уровень_субшкалы_Эмоциональный_комфорт',
                                                                         lst_reindex_sub_column_cols)
            svod_count_column_level_em_discomfort_df = calc_count_level_sub(base_df, [lst_svod_cols[idx]],
                                                                            'Значение_субшкалы_Эмоциональный_дискомфорт',
                                                                            'Уровень_субшкалы_Эмоциональный_дискомфорт',
                                                                            lst_reindex_sub_column_cols)

            svod_count_column_level_self_control_df = calc_count_level_sub(base_df, [lst_svod_cols[idx]],
                                                                           'Значение_субшкалы_Внутренний_контроль',
                                                                           'Уровень_субшкалы_Внутренний_контроль',
                                                                           lst_reindex_sub_column_cols)
            svod_count_column_level_outer_control_df = calc_count_level_sub(base_df, [lst_svod_cols[idx]],
                                                                            'Значение_субшкалы_Внешний_контроль',
                                                                            'Уровень_субшкалы_Внешний_контроль',
                                                                            lst_reindex_sub_column_cols)

            svod_count_column_level_dominating_df = calc_count_level_sub(base_df, [lst_svod_cols[idx]],
                                                                         'Значение_субшкалы_Доминирование',
                                                                         'Уровень_субшкалы_Доминирование',
                                                                         lst_reindex_sub_column_cols)
            svod_count_column_level_not_domin_df = calc_count_level_sub(base_df, [lst_svod_cols[idx]],
                                                                        'Значение_субшкалы_Ведомость',
                                                                        'Уровень_субшкалы_Ведомость',
                                                                        lst_reindex_sub_column_cols)

            svod_count_column_level_escape_df = calc_count_level_sub(base_df, [lst_svod_cols[idx]],
                                                                     'Значение_субшкалы_Эскапизм',
                                                                     'Уровень_субшкалы_Эскапизм',
                                                                     lst_reindex_sub_column_cols)

            # Считаем среднее по субшкалам
            svod_mean_column_df = pd.pivot_table(base_df,
                                                 index=[lst_svod_cols[idx]],
                                                 values=['Значение_шкалы_Искренность',
                                                         'Значение_ИП_Адаптация',
                                                         'Значение_ИП_Самопринятие',
                                                         'Значение_ИП_Принятие_других',
                                                         'Значение_ИП_Эмоциональный_комфорт',
                                                         'Значение_ИП_Интернальность',
                                                         'Значение_ИП_Стремление_к_доминированию',
                                                         'Значение_субшкалы_Адаптивность',
                                                         'Значение_субшкалы_Дезадаптивность',
                                                         'Значение_субшкалы_Лживость_c_минусом',
                                                         'Значение_субшкалы_Лживость_с_плюсом',
                                                         'Значение_субшкалы_Принятие_себя',
                                                         'Значение_субшкалы_Непринятие_себя',
                                                         'Значение_субшкалы_Принятие_других',
                                                         'Значение_субшкалы_Непринятие_других',
                                                         'Значение_субшкалы_Эмоциональный_комфорт',
                                                         'Значение_субшкалы_Эмоциональный_дискомфорт',
                                                         'Значение_субшкалы_Внутренний_контроль',
                                                         'Значение_субшкалы_Внешний_контроль',
                                                         'Значение_субшкалы_Доминирование',
                                                         'Значение_субшкалы_Ведомость',
                                                         'Значение_субшкалы_Эскапизм'
                                                         ],
                                                 aggfunc=round_mean)
            svod_mean_column_df.reset_index(inplace=True)
            # упорядочиваем колонки
            new_order_cols = [lst_svod_cols[idx]].copy()

            new_order_cols.extend((['Значение_шкалы_Искренность', 'Значение_ИП_Адаптация',
                                    'Значение_ИП_Самопринятие',
                                    'Значение_ИП_Принятие_других',
                                    'Значение_ИП_Эмоциональный_комфорт',
                                    'Значение_ИП_Интернальность',
                                    'Значение_ИП_Стремление_к_доминированию',
                                    'Значение_субшкалы_Адаптивность',
                                    'Значение_субшкалы_Дезадаптивность',
                                    'Значение_субшкалы_Лживость_c_минусом',
                                    'Значение_субшкалы_Лживость_с_плюсом',
                                    'Значение_субшкалы_Принятие_себя',
                                    'Значение_субшкалы_Непринятие_себя',
                                    'Значение_субшкалы_Принятие_других',
                                    'Значение_субшкалы_Непринятие_других',
                                    'Значение_субшкалы_Эмоциональный_комфорт',
                                    'Значение_субшкалы_Эмоциональный_дискомфорт',
                                    'Значение_субшкалы_Внутренний_контроль',
                                    'Значение_субшкалы_Внешний_контроль',
                                    'Значение_субшкалы_Доминирование',
                                    'Значение_субшкалы_Ведомость',
                                    'Значение_субшкалы_Эскапизм'
                                    ]))
            svod_mean_column_df = svod_mean_column_df.reindex(columns=new_order_cols)

            dct_rename_cols_mean = {'Значение_шкалы_Искренность': 'Ср. Искренность',
                                    'Значение_ИП_Адаптация': 'Ср. Адаптация',
                                    'Значение_ИП_Самопринятие': 'Ср. Самопринятие',
                                    'Значение_ИП_Принятие_других': 'Ср. Принятие других',
                                    'Значение_ИП_Эмоциональный_комфорт': 'Ср. Эмоциональный комфорт',
                                    'Значение_ИП_Интернальность': 'Ср. Интернальность',
                                    'Значение_ИП_Стремление_к_доминированию': 'Ср. Стремление к доминированию',

                                    'Значение_субшкалы_Адаптивность': 'Ср. Адаптивность',
                                    'Значение_субшкалы_Дезадаптивность': 'Ср. Дезадаптивность',
                                    'Значение_субшкалы_Лживость_c_минусом': 'Ср. Лживость -',
                                    'Значение_субшкалы_Лживость_с_плюсом': 'Ср. Лживость +',
                                    'Значение_субшкалы_Принятие_себя': 'Ср. Принятие себя',
                                    'Значение_субшкалы_Непринятие_себя': 'Ср. Непринятие себя',
                                    'Значение_субшкалы_Принятие_других': 'Ср. Принятие других',
                                    'Значение_субшкалы_Непринятие_других': 'Ср. Непринятие других',
                                    'Значение_субшкалы_Эмоциональный_комфорт': 'Ср. Эмоциональный комфорт',
                                    'Значение_субшкалы_Эмоциональный_дискомфорт': 'Ср. Эмоциональный дискомфорт',
                                    'Значение_субшкалы_Внутренний_контроль': 'Ср. Внутренний контроль',
                                    'Значение_субшкалы_Внешний_контроль': 'Ср. Внешний контроль',
                                    'Значение_субшкалы_Доминирование': 'Ср. Доминирование',
                                    'Значение_субшкалы_Ведомость': 'Ср. Ведомость',
                                    'Значение_субшкалы_Эскапизм': 'Ср. Эскапизм',
                                    }
            svod_mean_column_df.rename(columns=dct_rename_cols_mean, inplace=True)

            name_column = lst_svod_cols[idx]
            name_column = re.sub(r'[\[\]\'+()<> :"?*|\\/]', '_', name_column)
            name_column = name_column[:15]

            out_dct.update({f'Ср {name_column}': svod_mean_column_df,
                            f'Свод Ад {name_column}': svod_count_column_level_integral_adapt_df,
                            f'Свод СП {name_column}': svod_count_column_level_integral_self_df,
                            f'Свод ПрД {name_column}': svod_count_column_level_integral_other_df,
                            f'Свод ЭмК {name_column}': svod_count_column_level_integral_em_comfort_df,
                            f'Свод И {name_column}': svod_count_column_level_integral_internal_df,
                            f'Свод СКД {name_column}': svod_count_column_level_integral_domin_df,

                            f'Свод Искр {name_column}': svod_count_column_level_lie_df,
                            f'Свод А {name_column}': svod_count_column_level_adapt_df,
                            f'Свод ДА {name_column}': svod_count_column_level_desadapt_df,
                            f'Свод ПС {name_column}': svod_count_column_level_self_accept_df,
                            f'Свод НС {name_column}': svod_count_column_level_not_self_accept_df,
                            f'Свод ПД {name_column}': svod_count_column_level_other_accept_df,
                            f'Свод НД {name_column}': svod_count_column_level_not_other_accept_df,
                            f'Свод ЭК {name_column}': svod_count_column_level_em_comfort_df,
                            f'Свод ЭД {name_column}': svod_count_column_level_em_discomfort_df,
                            f'Свод ВнутрК {name_column}': svod_count_column_level_self_control_df,
                            f'Свод ВнешК {name_column}': svod_count_column_level_outer_control_df,
                            f'Свод Д {name_column}': svod_count_column_level_dominating_df,
                            f'Свод В {name_column}': svod_count_column_level_not_domin_df,
                            f'Свод Э {name_column}': svod_count_column_level_escape_df,
                            })
        return out_dct















def processing_rodjers_daimond_sneg_soc_psych_adapt(result_df: pd.DataFrame, answers_df: pd.DataFrame, lst_svod_cols:list):
    """
    Функция для обработки
    :param result_df: часть датафрейма с описательными колонками
    :param answers_df: часть датафрейма с ответами
    :param lst_svod_cols:  список с колонками по которым нужно делать свод
    """
    try:
        out_answer_df = result_df.copy()  # делаем копию для последующего соединения с сырыми ответами
        if len(answers_df.columns) != 101:  # проверяем количество колонок с вопросами
            raise BadCountColumnsRDSSPA

        # очищаем названия колонок от возможных сочетаний .1 которые добавляет пандас при одинаковых колонках
        clean_df_lst = []
        for name_column in answers_df.columns:
            clean_name = re.sub(r'.\d+$', '', name_column)
            clean_df_lst.append(clean_name)

        answers_df.columns = clean_df_lst


        lst_check_cols = ['Я испытываю внутреннюю неловкость, когда с кем-нибудь разговариваю.','Мне не хочется, чтобы окружающие догадывались, какой я, что у меня на душе, и я представляюсь перед ними, прячу свое лицо под маской.',
                          'Я во всем люблю состязание, соревнование, борьбу.','Я предъявляю к себе большие требования.',
                          'Я часто ругаю себя за то, что делаю.','Я часто чувствую себя униженным.',
                          'Я сомневаюсь в том, что могу понравиться кому-нибудь из девочек (мальчиков).','Я всегда сдерживаю свои обещания.',
                          'У меня теплые, хорошие отношения с окружающими.','Я сдержанный, замкнутый, держусь ото всех чуть в стороне.',
                          'Я сам виноват в своих неудачах.','Я ответственный человек. На меня можно положиться.',
                          'У меня чувство безнадежности. Все напрасно.','Я во многом живу взглядами, правилами и убеждениями моих сверстников.',
                          'Я принимаю большую часть тех правил и требований, которым должны следовать люди.','У меня мало собственных убеждений и правил.',
                          'Я люблю мечтать - иногда прямо среди дня. Трудно возвращаться от мечты к действительности.','У меня такое чувство, будто я зол на весь мир: на всех нападаю, огрызаюсь, никому не даю спуску. А то вдруг застряну на какой-нибудь обиде и мысленно мщу обидчику. Трудно сдерживать себя в таких вещах.',
                          'Я умею управлять собой и своими поступками - заставлять себя, разрешать себе, запрещать. Самоконтроль для меня - не проблема.','У меня часто портится настроение: вдруг находит уныние, хандра.',
                          'Меня не очень волнует то, что касается других. Я сосредоточен на себе, занят самим собой.','Люди, как правило, нравятся мне.',
                          'Я легко, свободно, непринужденно выражаю то, что чувствую.','Если я оказываюсь среди большого количества людей, мне бывает немножко одиноко.',
                          'Мне сейчас очень не по себе. Хочется все бросить, куда-нибудь спрятаться.','Обычно я легко лажу с окружающими.',
                          'Мои самые тяжелые битвы - с самим собой.','Я склонен быть настороже с теми, кто почему-то обходится со мною более приятельски, чем я ожидаю.',
                          'В душе я оптимист и верю в лучшее.','Я неподатливый, упрямый. Таких, как я, называют трудными людьми.',
                          'Я критичен к людям и всегда сужу их, если, с моей точки зрения, они этого заслуживают.','Я чувствую себя не ведущим, а ведомым: мне еще не всегда удается мыслить и действовать самостоятельно.',
                          'Большинство тех, кто знает меня, хорошо ко мне относятся, я нравлюсь им.','Иногда у меня бывают такие мысли, которыми я ни с кем не хотел бы делиться.',
                          'У меня красивая фигура. Я привлекателен (привлекательна).','Я чувствую беспомощность. Мне нужно, чтобы кто-нибудь был рядом.',
                          'Обычно я могу принять решение и твердо следовать ему.','Мои решения - не мои собственные. Даже тогда, когда мне кажется, что я решаю самостоятельно, они все же приняты под влиянием других людей.',
                          'Я часто испытываю чувство вины - даже тогда, когда как будто ни в чем не виноват.','Я чувствую антипатию, неприязнь к тому, что окружает меня.',
                          'Я доволен.','Я выбит из колеи: не могу собраться, взять себя в руки, сосредоточиться, организовать себя.',
                          'Я чувствую вялость, апатию: все, что раньше волновало меня, стало вдруг безразличным.','Я уравновешен, спокоен, у меня ровное настроение.',
                          'Разозлившись, я нередко выхожу из себя.','Я часто чувствую себя обиженным.',
                          'Я импульсивный: порывистый, нетерпеливый, действую по первому побуждению.','Бывает, что я сплетничаю.',
                          'Я не очень доверяю своим чувствам, они подводят меня иногда.','Это довольно трудно - быть самим собой.',
                          'У меня на первом плане разум, а не чувство. Прежде чем что-либо сделать, я обдумываю свои поступки.','Мне кажется, я вижу происходящее со мной не совсем так, как оно есть на самом деле. Вместо того чтобы здраво взглянуть фактам в лицо, толкую их на свой лад... Словом, не отличаюсь реалистичностью.',
                          'Я терпим в своем отношении к людям, и принимаю каждого таким, каков он есть.','Я стараюсь не думать о своих проблемах.',
                          'Я считаю себя интересным человеком - заметным, привлекательным как личность.','Я стеснительный, легко тушуюсь.',
                          'Мне обязательно нужны какие-то напоминания, подталкивания со стороны, чтобы довести дело до конца.','Я чувствую внутреннее превосходство над другими.',
                          'Я никто. Нет ничего, в чем бы я выразил себя, проявил свою индивидуальность, свое «Я».','Я боюсь того, что подумают обо мне другие.',
                          'Я честолюбивый. Я не равнодушен к успехам, похвале. В том, что я считаю существенным, мне важно быть в числе лучших.','Я презираю себя сейчас.',
                          'Я деятелен, энергичен, у меня есть инициатива.','Мне не хватает духу встретить в лицо трудности или ситуацию, которая грозит осложнениями, неприятными переживаниями.',
                          'Я просто не уважаю себя.','Я по натуре вожак и умею влиять на других.',
                          'В целом я хорошо отношусь к себе.','Я настойчивый, напористый, уверенный в себе.',
                          'Я не люблю, когда у меня с кем-то портятся отношения, особенно если разногласия грозят стать окончательными.','Я долго не могу принять решение, как действовать, а потом сомневаюсь в его правильности.',
                          'Я в какой-то растерянности, у меня все спуталось, смешалось.','Я удовлетворен собой.',
                          'Я неудачник. Мне не везет.','Я приятный, симпатичный, располагающий к себе человек.',
                          'Я нравлюсь девочкам (мальчикам) как человек, как личность.','Я стойкий женоненавистник. Презираю всякое общение с девчонками. (Я не люблю мальчишек. Презираю всякое общение с ними.)',
                          'Когда я должен что-то осуществить, меня охватывает страх перед провалом: а вдруг я не справлюсь, вдруг у меня не получится?','У меня легко, спокойно на душе. Нет ничего, что сильно тревожило бы меня.',
                          'Я умею упорно работать.','Я чувствую, что меняюсь, расту, взрослею, мои чувства и отношения к окружающему становятся более зрелыми.',
                          'Случается, что я говорю о вещах, в которых совсем не разбираюсь.','Я всегда говорю только правду.',
                          'Я встревожен, обеспокоен, напряжен.','Чтобы заставить меня что-либо сделать, надо как следует настоять, и я соглашусь, уступлю.',
                          'Я чувствую неуверенность в себе.','Я часто бываю вынужден защищать себя, строить доводы, которые меня оправдывают и делают мои поступки обоснованными.',
                          'Я уступчивый, податливый, мягкий в отношениях с другими.','Я умный.',
                          'Иной раз я люблю прихвастнуть.','Я безнадежен. Принимаю решения и тут же их нарушаю. Презираю свое бессилие, а с собой поделать ничего не могу. У меня нет воли и нет воли ее вырабатывать.',
                          'Я стараюсь полагаться на собственные силы, не рассчитывая ни на чью помощь.','Я никогда не опаздываю.',
                          'У меня ощущение скованности, внутренней несвободы.','Я отличаюсь от других.',
                          'Я не очень надежен, на меня нельзя положиться.','Мне все ясно в себе. Я себя хорошо понимаю.',
                          'Я общительный, открытый человек, легко схожусь с людьми.','Мои силы и способности вполне соответствуют тем задачам, которые ставит передо мной жизнь. Я со всем могу справиться.',
                          'Я ничего не стою. Меня даже не принимают всерьез. Ко мне в лучшем случае снисходительны, просто терпят меня.','Меня беспокоит, что девочки (мальчики) слишком занимают мои мысли.',
                          'Все свои привычки я считаю хорошими.']

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
            raise BadOrderRDSSPA

        # словарь для замены слов на числа
        dct_replace_value = {'это ко мне совершенно не относится': 0,
                             'мне это не свойственно в большинстве случаев': 1,
                             'сомневаюсь, что это можно отнести ко мне': 2,
                             'не решаюсь отнести это к себе': 3,
                             'это похоже на меня, но нет уверенности': 4,
                             'это на меня похоже': 5,
                             'это точно про меня': 6}

        valid_values = [0, 1, 2, 3, 4, 5, 6]
        answers_df.replace(dct_replace_value, inplace=True)  # заменяем слова на цифры для подсчетов
        # Проверяем, есть ли значения, отличающиеся от указанных в списке
        lst_error_answers = []  # список для хранения строк где найдены неправильные ответы

        for i in range(101):
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
            raise BadValueRDSSPA

        base_df = pd.DataFrame()

        # Субшкала адаптивность
        base_df['Значение_субшкалы_Адаптивность'] = answers_df.apply(calc_sub_value_adapt, axis=1)
        base_df['Зона_неопределенности_Адаптивность'] = '68-170 баллов'
        base_df['Уровень_субшкалы_Адаптивность'] = base_df['Значение_субшкалы_Адаптивность'].apply(calc_level_sub_adapt)

        # Субшкала Дезадаптивность
        base_df['Значение_субшкалы_Дезадаптивность'] = answers_df.apply(calc_sub_value_desadapt, axis=1)
        base_df['Зона_неопределенности_Дезадаптивность'] = '68-170 баллов'
        base_df['Уровень_субшкалы_Дезадаптивность'] = base_df['Значение_субшкалы_Дезадаптивность'].apply(calc_level_sub_desadapt)

        base_df['Значение_ИП_Адаптация'] = base_df[['Значение_субшкалы_Адаптивность','Значение_субшкалы_Дезадаптивность']].apply(calc_adapt,axis=1)
        base_df['Уровень_ИП_Адаптация'] = base_df['Значение_ИП_Адаптация'].apply(calc_level_integral)


        # Лживость -
        base_df['Значение_субшкалы_Лживость_c_минусом'] = answers_df.apply(calc_sub_value_lie_minus, axis=1)
        # Лживость +
        base_df['Значение_субшкалы_Лживость_с_плюсом'] = answers_df.apply(calc_sub_value_lie_plus, axis=1)
        # Шкала Искренность
        base_df['Значение_шкалы_Искренность'] = base_df[['Значение_субшкалы_Лживость_c_минусом','Значение_субшкалы_Лживость_с_плюсом']].sum(axis=1)
        base_df['Уровень_шкалы_Искренность'] = base_df['Значение_шкалы_Искренность'].apply(calc_sincerity)


        # Принятие себя
        base_df['Значение_субшкалы_Принятие_себя'] = answers_df.apply(calc_sub_value_self_accept, axis=1)
        base_df['Зона_неопределенности_Принятие_себя'] = '22-52 балла'
        base_df['Уровень_субшкалы_Принятие_себя'] = base_df['Значение_субшкалы_Принятие_себя'].apply(calc_level_sub_self_accept)
        # Непринятие_себя
        base_df['Значение_субшкалы_Непринятие_себя'] = answers_df.apply(calc_sub_value_not_self_accept, axis=1)
        base_df['Зона_неопределенности_Непринятие_себя'] = '14-35 баллов'
        base_df['Уровень_субшкалы_Непринятие_себя'] = base_df['Значение_субшкалы_Непринятие_себя'].apply(calc_level_sub_not_self_accept)

        base_df['Значение_ИП_Самопринятие'] = base_df[['Значение_субшкалы_Принятие_себя','Значение_субшкалы_Непринятие_себя']].apply(calc_self_accept,axis=1)
        base_df['Уровень_ИП_Самопринятие'] = base_df['Значение_ИП_Самопринятие'].apply(calc_level_integral)


        # Принятие_других
        base_df['Значение_субшкалы_Принятие_других'] = answers_df.apply(calc_sub_value_other_accept, axis=1)
        base_df['Зона_неопределенности_Принятие_других'] = '12-30 баллов'
        base_df['Уровень_субшкалы_Принятие_других'] = base_df['Значение_субшкалы_Принятие_других'].apply(calc_level_sub_other_accept)
        # Непринятие_других
        base_df['Значение_субшкалы_Непринятие_других'] = answers_df.apply(calc_sub_value_not_other_accept, axis=1)
        base_df['Зона_неопределенности_Непринятие_других'] = '14-35 баллов'
        base_df['Уровень_субшкалы_Непринятие_других'] = base_df['Значение_субшкалы_Непринятие_других'].apply(calc_level_sub_not_other_accept)

        base_df['Значение_ИП_Принятие_других'] = base_df[['Значение_субшкалы_Принятие_других','Значение_субшкалы_Непринятие_других']].apply(calc_other_accept,axis=1)
        base_df['Уровень_ИП_Принятие_других'] = base_df['Значение_ИП_Принятие_других'].apply(calc_level_integral)

        # Эмоциональный_комфорт
        base_df['Значение_субшкалы_Эмоциональный_комфорт'] = answers_df.apply(calc_sub_value_em_comfort, axis=1)
        base_df['Зона_неопределенности_Эмоциональный_комфорт'] = '14-35 баллов'
        base_df['Уровень_субшкалы_Эмоциональный_комфорт'] = base_df['Значение_субшкалы_Эмоциональный_комфорт'].apply(calc_level_sub_em_comfort)
        # Эмоциональный_дискомфорт
        base_df['Значение_субшкалы_Эмоциональный_дискомфорт'] = answers_df.apply(calc_sub_value_em_discomfort, axis=1)
        base_df['Зона_неопределенности_Эмоциональный_дискомфорт'] = '14-35 баллов'
        base_df['Уровень_субшкалы_Эмоциональный_дискомфорт'] = base_df['Значение_субшкалы_Эмоциональный_дискомфорт'].apply(calc_level_sub_em_discomfort)

        base_df['Значение_ИП_Эмоциональный_комфорт'] = base_df[['Значение_субшкалы_Эмоциональный_комфорт','Значение_субшкалы_Эмоциональный_дискомфорт']].apply(calc_comfort,axis=1)
        base_df['Уровень_ИП_Эмоциональный_комфорт'] = base_df['Значение_ИП_Эмоциональный_комфорт'].apply(calc_level_integral)


        # Внутренний_контроль
        base_df['Значение_субшкалы_Внутренний_контроль'] = answers_df.apply(calc_sub_value_self_control, axis=1)
        base_df['Зона_неопределенности_Внутренний_контроль'] = '26-65 баллов'
        base_df['Уровень_субшкалы_Внутренний_контроль'] = base_df['Значение_субшкалы_Внутренний_контроль'].apply(calc_level_sub_self_control)
        # Внешний_контроль
        base_df['Значение_субшкалы_Внешний_контроль'] = answers_df.apply(calc_sub_value_outer_control, axis=1)
        base_df['Зона_неопределенности_Внешний_контроль'] = '18-45 баллов'
        base_df['Уровень_субшкалы_Внешний_контроль'] = base_df['Значение_субшкалы_Внешний_контроль'].apply(calc_level_sub_outer_control)
        base_df['Значение_ИП_Интернальность'] = base_df[['Значение_субшкалы_Внутренний_контроль','Значение_субшкалы_Внешний_контроль']].apply(calc_control,axis=1)
        base_df['Уровень_ИП_Интернальность'] = base_df['Значение_ИП_Интернальность'].apply(calc_level_integral)


        # Доминирование
        base_df['Значение_субшкалы_Доминирование'] = answers_df.apply(calc_sub_value_dominating, axis=1)
        base_df['Зона_неопределенности_Доминирование'] = '6-15 баллов'
        base_df['Уровень_субшкалы_Доминирование'] = base_df['Значение_субшкалы_Доминирование'].apply(calc_level_sub_dominating)
        # Ведомость
        base_df['Значение_субшкалы_Ведомость'] = answers_df.apply(calc_sub_value_not_domin, axis=1)
        base_df['Зона_неопределенности_Ведомость'] = '12-30 баллов'
        base_df['Уровень_субшкалы_Ведомость'] = base_df['Значение_субшкалы_Ведомость'].apply(calc_level_sub_not_domin)
        base_df['Значение_ИП_Стремление_к_доминированию'] = base_df[['Значение_субшкалы_Доминирование','Значение_субшкалы_Ведомость']].apply(calc_dominating,axis=1)
        base_df['Уровень_ИП_Стремление_к_доминированию'] = base_df['Значение_ИП_Стремление_к_доминированию'].apply(calc_level_integral)


        # Эскапизм
        base_df['Значение_субшкалы_Эскапизм'] = answers_df.apply(calc_sub_value_escape, axis=1)
        base_df['Зона_неопределенности_Эскапизм'] = '10-25 баллов'
        base_df['Уровень_субшкалы_Эскапизм'] = base_df['Значение_субшкалы_Эскапизм'].apply(calc_level_sub_escape)

        # Создаем датафрейм для создания части в общий датафрейм
        part_df = pd.DataFrame()

        part_df['РДССПА_Искренность_Значение'] = base_df['Значение_шкалы_Искренность']
        part_df['РДССПА_Искренность_Уровень'] = base_df['Уровень_шкалы_Искренность']


        part_df['РДССПА_Адаптация_Значение'] = base_df['Значение_ИП_Адаптация']
        part_df['РДССПА_Адаптация_Уровень'] = base_df['Уровень_ИП_Адаптация']

        part_df['РДССПА_Самопринятие_Значение'] = base_df['Значение_ИП_Самопринятие']
        part_df['РДССПА_Самопринятие_Уровень'] = base_df['Уровень_ИП_Самопринятие']

        part_df['РДССПА_Принятие_других_Значение'] = base_df['Значение_ИП_Принятие_других']
        part_df['РДССПА_Принятие_других_Уровень'] = base_df['Уровень_ИП_Принятие_других']

        part_df['РДССПА_Эмоциональный_комфорт_Значение'] = base_df['Значение_ИП_Эмоциональный_комфорт']
        part_df['РДССПА_Эмоциональный_комфорт_Уровень'] = base_df['Уровень_ИП_Эмоциональный_комфорт']

        part_df['РДССПА_Интернальность_Значение'] = base_df['Значение_ИП_Интернальность']
        part_df['РДССПА_Интернальность_Уровень'] = base_df['Уровень_ИП_Интернальность']

        part_df['РДССПА_Стремление_к_доминированию_Значение'] = base_df['Значение_ИП_Стремление_к_доминированию']
        part_df['РДССПА_Стремление_к_доминированию_Уровень'] = base_df['Уровень_ИП_Стремление_к_доминированию']

        part_df['РДССПА_Эскапизм'] = base_df['Значение_субшкалы_Эскапизм']

        part_df['РДССПА_А_Значение'] = base_df['Значение_субшкалы_Адаптивность']
        part_df['РДССПА_А_Уровень'] = base_df['Уровень_субшкалы_Адаптивность']
        part_df['РДССПА_ДА_Значение'] = base_df['Значение_субшкалы_Дезадаптивность']
        part_df['РДССПА_ДА_Уровень'] = base_df['Уровень_субшкалы_Дезадаптивность']

        part_df['РДССПА_ЛМ_Значение'] = base_df['Значение_субшкалы_Лживость_c_минусом']
        part_df['РДССПА_ЛП_Значение'] = base_df['Значение_субшкалы_Лживость_с_плюсом']

        part_df['РДССПА_ПС_Значение'] = base_df['Значение_субшкалы_Принятие_себя']
        part_df['РДССПА_ПС_Уровень'] = base_df['Уровень_субшкалы_Принятие_себя']
        part_df['РДССПА_НС_Значение'] = base_df['Значение_субшкалы_Непринятие_себя']
        part_df['РДССПА_НС_Уровень'] = base_df['Уровень_субшкалы_Непринятие_себя']

        part_df['РДССПА_ПД_Значение'] = base_df['Значение_субшкалы_Принятие_других']
        part_df['РДССПА_ПД_Уровень'] = base_df['Уровень_субшкалы_Принятие_других']
        part_df['РДССПА_НД_Значение'] = base_df['Значение_субшкалы_Непринятие_других']
        part_df['РДССПА_НД_Уровень'] = base_df['Уровень_субшкалы_Непринятие_других']

        part_df['РДССПА_ЭК_Значение'] = base_df['Значение_субшкалы_Эмоциональный_комфорт']
        part_df['РДССПА_ЭК_Уровень'] = base_df['Уровень_субшкалы_Эмоциональный_комфорт']
        part_df['РДССПА_ЭД_Значение'] = base_df['Значение_субшкалы_Эмоциональный_дискомфорт']
        part_df['РДССПА_ЭД_Уровень'] = base_df['Уровень_субшкалы_Эмоциональный_дискомфорт']

        part_df['РДССПА_ВнутрК_Значение'] = base_df['Значение_субшкалы_Внутренний_контроль']
        part_df['РДССПА_ВнутрК_Уровень'] = base_df['Уровень_субшкалы_Внутренний_контроль']
        part_df['РДССПА_ВнешК_Значение'] = base_df['Значение_субшкалы_Внешний_контроль']
        part_df['РДССПА_ВнешК_Уровень'] = base_df['Уровень_субшкалы_Внешний_контроль']

        part_df['РДССПА_Д_Значение'] = base_df['Значение_субшкалы_Доминирование']
        part_df['РДССПА_Д_Уровень'] = base_df['Уровень_субшкалы_Доминирование']
        part_df['РДССПА_В_Значение'] = base_df['Значение_субшкалы_Ведомость']
        part_df['РДССПА_В_Уровень'] = base_df['Уровень_субшкалы_Ведомость']

        part_df['РДССПА_Э_Значение'] = base_df['Значение_субшкалы_Эскапизм']
        part_df['РДССПА_Э_Уровень'] = base_df['Уровень_субшкалы_Эскапизм']

        out_answer_df = pd.concat([out_answer_df, answers_df], axis=1)  # Датафрейм для проверки

        new_order_cols = ['Значение_шкалы_Искренность','Уровень_шкалы_Искренность','Значение_ИП_Адаптация','Уровень_ИП_Адаптация',
                          'Значение_ИП_Самопринятие','Уровень_ИП_Самопринятие',
                          'Значение_ИП_Принятие_других','Уровень_ИП_Принятие_других',
                          'Значение_ИП_Эмоциональный_комфорт','Уровень_ИП_Эмоциональный_комфорт',
                          'Значение_ИП_Интернальность','Уровень_ИП_Интернальность',
                          'Значение_ИП_Стремление_к_доминированию','Уровень_ИП_Стремление_к_доминированию',
                          'Значение_субшкалы_Эскапизм', 'Зона_неопределенности_Эскапизм', 'Уровень_субшкалы_Эскапизм',
                          'Значение_субшкалы_Адаптивность', 'Зона_неопределенности_Адаптивность', 'Уровень_субшкалы_Адаптивность',
                          'Значение_субшкалы_Дезадаптивность', 'Зона_неопределенности_Дезадаптивность', 'Уровень_субшкалы_Дезадаптивность',
                          'Значение_субшкалы_Лживость_c_минусом',
                          'Значение_субшкалы_Лживость_с_плюсом',
                          'Значение_субшкалы_Принятие_себя', 'Зона_неопределенности_Принятие_себя', 'Уровень_субшкалы_Принятие_себя',
                          'Значение_субшкалы_Непринятие_себя', 'Зона_неопределенности_Непринятие_себя', 'Уровень_субшкалы_Непринятие_себя',
                          'Значение_субшкалы_Принятие_других', 'Зона_неопределенности_Принятие_других', 'Уровень_субшкалы_Принятие_других',
                          'Значение_субшкалы_Непринятие_других', 'Зона_неопределенности_Непринятие_других', 'Уровень_субшкалы_Непринятие_других',
                          'Значение_субшкалы_Эмоциональный_комфорт', 'Зона_неопределенности_Эмоциональный_комфорт', 'Уровень_субшкалы_Эмоциональный_комфорт',
                          'Значение_субшкалы_Эмоциональный_дискомфорт', 'Зона_неопределенности_Эмоциональный_дискомфорт', 'Уровень_субшкалы_Эмоциональный_дискомфорт',
                          'Значение_субшкалы_Внутренний_контроль', 'Зона_неопределенности_Внутренний_контроль', 'Уровень_субшкалы_Внутренний_контроль',
                          'Значение_субшкалы_Внешний_контроль', 'Зона_неопределенности_Внешний_контроль', 'Уровень_субшкалы_Внешний_контроль',
                          'Значение_субшкалы_Доминирование', 'Зона_неопределенности_Доминирование', 'Уровень_субшкалы_Доминирование',
                          'Значение_субшкалы_Ведомость', 'Зона_неопределенности_Ведомость', 'Уровень_субшкалы_Ведомость',

                          ]
        base_df = base_df.reindex(columns=new_order_cols)

        # Соединяем анкетную часть с результатной
        base_df = pd.concat([result_df, base_df], axis=1)
        base_df.sort_values(by='Значение_ИП_Адаптация', ascending=False, inplace=True)  # сортируем

        # формируем основной словарь
        out_dct = {'Списочный результат': base_df, 'Список для проверки': out_answer_df,
                   }

        # Делаем свод по интегральным показателям
        dct_svod_integral ={'Значение_ИП_Адаптация':'Уровень_ИП_Адаптация',
                            'Значение_ИП_Самопринятие':'Уровень_ИП_Самопринятие',
                            'Значение_ИП_Принятие_других':'Уровень_ИП_Принятие_других',
                            'Значение_ИП_Эмоциональный_комфорт':'Уровень_ИП_Эмоциональный_комфорт',
                            'Значение_ИП_Интернальность':'Уровень_ИП_Интернальность',
                            'Значение_ИП_Стремление_к_доминированию':'Уровень_ИП_Стремление_к_доминированию',
                            }

        dct_rename_svod_integral ={'Значение_ИП_Адаптация':'Адаптация',
                            'Значение_ИП_Самопринятие':'Самопринятие',
                            'Значение_ИП_Принятие_других':'Принятие других',
                            'Значение_ИП_Эмоциональный_комфорт':'Эмоциональный комфорт',
                            'Значение_ИП_Интернальность':'Интернальность',
                            'Значение_ИП_Стремление_к_доминированию':'Стремление к доминированию',
                            }

        lst_integral = ['низкий уровень','средний уровень','высокий уровень']

        base_svod_integral_df = create_union_svod(base_df,dct_svod_integral,dct_rename_svod_integral,lst_integral)

        # Делаем свод по субшкалам
        lst_sub_level = ['очень низкий уровень','зона неопределенности','очень высокий уровень']
        dct_svod_sub = {'Значение_шкалы_Искренность':'Уровень_шкалы_Искренность',
                        'Значение_субшкалы_Адаптивность':'Уровень_субшкалы_Адаптивность',
                        'Значение_субшкалы_Дезадаптивность':'Уровень_субшкалы_Дезадаптивность',
                        'Значение_субшкалы_Принятие_себя':'Уровень_субшкалы_Принятие_себя',
                        'Значение_субшкалы_Непринятие_себя':'Уровень_субшкалы_Непринятие_себя',
                        'Значение_субшкалы_Принятие_других':'Уровень_субшкалы_Принятие_других',
                        'Значение_субшкалы_Непринятие_других':'Уровень_субшкалы_Непринятие_других',
                        'Значение_субшкалы_Эмоциональный_комфорт':'Уровень_субшкалы_Эмоциональный_комфорт',
                        'Значение_субшкалы_Эмоциональный_дискомфорт':'Уровень_субшкалы_Эмоциональный_дискомфорт',
                        'Значение_субшкалы_Внутренний_контроль':'Уровень_субшкалы_Внутренний_контроль',
                        'Значение_субшкалы_Внешний_контроль':'Уровень_субшкалы_Внешний_контроль',
                        'Значение_субшкалы_Доминирование':'Уровень_субшкалы_Доминирование',
                        'Значение_субшкалы_Ведомость':'Уровень_субшкалы_Ведомость',
                        'Значение_субшкалы_Эскапизм':'Уровень_субшкалы_Эскапизм'
                        }

        dct_rename_svod_sub = {'Значение_шкалы_Искренность':'Искренность',
                        'Значение_субшкалы_Адаптивность':'Адаптивность',
                        'Значение_субшкалы_Дезадаптивность':'Дезадаптивность',
                        'Значение_субшкалы_Принятие_себя':'Принятие себя',
                        'Значение_субшкалы_Непринятие_себя':'Непринятие себя',
                        'Значение_субшкалы_Принятие_других':'Принятие других',
                        'Значение_субшкалы_Непринятие_других':'Непринятие других',
                        'Значение_субшкалы_Эмоциональный_комфорт':'Эмоциональный комфорт',
                        'Значение_субшкалы_Эмоциональный_дискомфорт':'Эмоциональный дискомфорт',
                        'Значение_субшкалы_Внутренний_контроль':'Внутренний контроль',
                        'Значение_субшкалы_Внешний_контроль':'Внешний контроль',
                        'Значение_субшкалы_Доминирование':'Доминирование',
                        'Значение_субшкалы_Ведомость':'Ведомость',
                        'Значение_субшкалы_Эскапизм':'Эскапизм'}

        base_svod_sub_df = create_union_svod(base_df,dct_svod_sub,dct_rename_svod_sub,lst_sub_level)

        # Интегоральные показатели
        avg_lie = round(base_df['Значение_шкалы_Искренность'].mean(), 2)
        avg_integral_adapt = round(base_df['Значение_ИП_Адаптация'].mean(), 2)
        avg_integral_self = round(base_df['Значение_ИП_Самопринятие'].mean(), 2)
        avg_integral_other = round(base_df['Значение_ИП_Принятие_других'].mean(), 2)
        avg_integral_em_comfort = round(base_df['Значение_ИП_Эмоциональный_комфорт'].mean(), 2)
        avg_integral_internal = round(base_df['Значение_ИП_Интернальность'].mean(), 2)
        avg_integral_dominating = round(base_df['Значение_ИП_Стремление_к_доминированию'].mean(), 2)


        # считаем среднее значение по субшкалам
        avg_adapt = round(base_df['Значение_субшкалы_Адаптивность'].mean(), 2)
        avg_desadapt = round(base_df['Значение_субшкалы_Дезадаптивность'].mean(), 2)
        avg_lie_minus = round(base_df['Значение_субшкалы_Лживость_c_минусом'].mean(), 2)
        avg_lie_plus = round(base_df['Значение_субшкалы_Лживость_с_плюсом'].mean(), 2)
        avg_self_accept = round(base_df['Значение_субшкалы_Принятие_себя'].mean(), 2)
        avg_not_self_accept = round(base_df['Значение_субшкалы_Непринятие_себя'].mean(), 2)
        avg_other_accept = round(base_df['Значение_субшкалы_Принятие_других'].mean(), 2)
        avg_not_other_accept = round(base_df['Значение_субшкалы_Непринятие_других'].mean(), 2)
        avg_em_comfort = round(base_df['Значение_субшкалы_Эмоциональный_комфорт'].mean(), 2)
        avg_em_discomfort = round(base_df['Значение_субшкалы_Эмоциональный_дискомфорт'].mean(), 2)
        avg_self_control = round(base_df['Значение_субшкалы_Внутренний_контроль'].mean(), 2)
        avg_outer_control = round(base_df['Значение_субшкалы_Внешний_контроль'].mean(), 2)
        avg_dominating = round(base_df['Значение_субшкалы_Доминирование'].mean(), 2)
        avg_not_domin = round(base_df['Значение_субшкалы_Ведомость'].mean(), 2)
        avg_escape = round(base_df['Значение_субшкалы_Эскапизм'].mean(), 2)

        avg_dct = {'Среднее значение шкалы Искренность':avg_lie,
                   'Среднее значение интегрального показателя Адаптация':avg_integral_adapt,
                   'Среднее значение интегрального показателя Самопринятие': avg_integral_self,
                   'Среднее значение интегрального показателя Принятие других': avg_integral_other,
                   'Среднее значение интегрального показателя Эмоциональный комфорт': avg_integral_em_comfort,
                   'Среднее значение интегрального показателя Интернальность': avg_integral_internal,
                   'Среднее значение интегрального показателя Стремление к доминированию': avg_integral_dominating,
                   'Среднее значение субшкалы Эскапизм': avg_escape,

                   'Среднее значение субшкалы Адаптивность': avg_adapt,
                   'Среднее значение субшкалы Дезадаптивность': avg_desadapt,
                   'Среднее значение субшкалы Лживость -': avg_lie_minus,
                   'Среднее значение субшкалы Лживость +': avg_lie_plus,
                   'Среднее значение субшкалы Принятие себя': avg_self_accept,
                   'Среднее значение субшкалы Непринятие себя': avg_not_self_accept,
                   'Среднее значение субшкалы Принятие других': avg_other_accept,
                   'Среднее значение субшкалы Непринятие других': avg_not_other_accept,
                   'Среднее значение субшкалы Эмоциональный комфорт': avg_em_comfort,
                   'Среднее значение субшкалы Эмоциональный дискомфорт': avg_em_discomfort,
                   'Среднее значение субшкалы Внутренний контроль': avg_self_control,
                   'Среднее значение субшкалы Внешний контроль': avg_outer_control,
                   'Среднее значение субшкалы Доминирование': avg_dominating,
                   'Среднее значение субшкалы Ведомость': avg_not_domin

                   }

        avg_df = pd.DataFrame.from_dict(avg_dct, orient='index')
        avg_df = avg_df.reset_index()
        avg_df.columns = ['Показатель', 'Среднее значение']

        out_dct.update({'Свод Интегральные показатели':base_svod_integral_df,
                        'Свод Субшкалы': base_svod_sub_df,
                        'Среднее': avg_df}
                       )

        # Создаем листы со списками по интегральным показателям
        dct_level = dict()
        for level in lst_sub_level:
            temp_df = base_df[base_df['Уровень_шкалы_Искренность'] == level]
            if temp_df.shape[0] != 0:
                dct_level[f'Искр. {level}'] = temp_df

        out_dct.update(dct_level)
        dct_prefix ={'Уровень_ИП_Адаптация':'Ад',
                     'Уровень_ИП_Самопринятие':'СП',
                     'Уровень_ИП_Принятие_других':'ПД',
                     'Уровень_ИП_Эмоциональный_комфорт':'ЭК',
                     'Уровень_ИП_Интернальность':'И',
                     'Уровень_ИП_Стремление_к_доминированию':'СКД',
                     }


        out_dct = create_list_on_level(base_df,out_dct,lst_integral,dct_prefix)

        # Создаем листы со списками по интегральным показателям
        dct_esk = dict()
        for level in lst_sub_level:
            temp_df = base_df[base_df['Уровень_субшкалы_Эскапизм'] == level]
            if temp_df.shape[0] != 0:
                dct_esk[f'Э. {level}'] = temp_df
        out_dct.update(dct_esk)

        """
            Сохраняем в зависимости от необходимости делать своды по определенным колонкам
            """
        if len(lst_svod_cols) == 0:
            return out_dct, part_df
        else:
            out_dct = create_result_rdsspa(base_df, out_dct, lst_svod_cols)

            return out_dct, part_df

    except BadOrderRDSSPA:
        messagebox.showerror('Лахеcис',
                             f'При обработке вопросов теста Шкала социально психологической адаптированности Роджерс Даймонд Снегирева обнаружены неправильные вопросы. Проверьте названия колонок с вопросами:\n'
                             f'{error_order_message}\n'
                             f'Используйте при создании Яндекс-формы написание вопросов из руководства пользователя программы Лахесис.')
    except BadValueRDSSPA:
        messagebox.showerror('Лахеcис',
                             f'При обработке вопросов теста Шкала социально психологической адаптированности Роджерс Даймонд Снегирева обнаружены неправильные варианты ответов. Проверьте ответы на указанных строках:\n'
                             f'{error_message}\n'
                             f'Используйте при создании Яндекс-формы написание вариантов ответа из руководства пользователя программы Лахесис.')


    except BadCountColumnsRDSSPA:
        messagebox.showerror('Лахеcис',
                             f'Проверьте количество колонок с ответами на тест Шкала социально психологической адаптированности Роджерс Даймонд Снегирева\n'
                             f'Должно быть 101 колонка с ответами')























