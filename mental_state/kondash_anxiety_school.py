"""
Скрипт для обработки результатов теста тревожности Кондаша для школьников
"""
from lachesis_support_functions import round_mean, sort_name_class,convert_to_int,create_union_svod
import pandas as pd
import re
from tkinter import messagebox


class BadOrderCondashAnxiety(Exception):
    """
    Исключение для обработки случая когда колонки не совпадают
    """
    pass


class BadValueCondashAnxiety(Exception):
    """
    Исключение для неправильных значений в вариантах ответов
    """
    pass

class BadCountColumnsCondashAnxiety(Exception):
    """
    Исключение для обработки случая если количество колонок не равно 30
    """
    pass


class NotReqColumn(Exception):
    """
    Исключение для обработки случая когда нет обязательных колонок Номер_класса, Буква_класса, Пол
    """
    pass

class BadValueSex(Exception):
    """
    Исключение для обработки случая когда в колонке Пол есть значения отличающиеся от Мужской или Женский
    """
    pass


def calc_level_all_condash_anxiety(ser:pd.Series):
    """
    Функция для подсчета уровня тревожности
    """
    row = ser.tolist() # превращаем в список
    group = int(row[0]) # Номер_класса
    sex = row[1] # пол
    value = row[2] # значение которое нужно обработать
    if group  == 9:
        if sex == 'Женский':
            if 30 <= value <= 62:
                return 'нормальный уровень тревожности'
            elif 63 <= value <= 78:
                return 'несколько повышенный уровень тревожности'
            elif 79 <= value <= 94:
                return 'высокий уровень тревожности'
            elif value > 94:
                return 'очень высокий уровень тревожности'
            else:
                return 'чрезмерное спокойствие'
        else:
            if 17 <= value <= 54:
                return 'нормальный уровень тревожности'
            elif 55 <= value <= 73:
                return 'несколько повышенный уровень тревожности'
            elif 74 <= value <= 91:
                return 'высокий уровень тревожности'
            elif value > 91:
                return 'очень высокий уровень тревожности'
            else:
                return 'чрезмерное спокойствие'
    elif group == 10:
        if sex == 'Женский':
            if 17 <= value <= 54:
                return 'нормальный уровень тревожности'
            elif 55 <= value <= 73:
                return 'несколько повышенный уровень тревожности'
            elif 74 <= value <= 90:
                return 'высокий уровень тревожности'
            elif value > 90:
                return 'очень высокий уровень тревожности'
            else:
                return 'чрезмерное спокойствие'
        else:
            if 10 <= value <= 48:
                return 'нормальный уровень тревожности'
            elif 49 <= value <= 67:
                return 'несколько повышенный уровень тревожности'
            elif 68 <= value <= 86:
                return 'высокий уровень тревожности'
            elif value > 86:
                return 'очень высокий уровень тревожности'
            else:
                return 'чрезмерное спокойствие'
    elif group == 11:
        if sex == 'Женский':
            if 35 <= value <= 62:
                return 'нормальный уровень тревожности'
            elif 63 <= value <= 76:
                return 'несколько повышенный уровень тревожности'
            elif 77 <= value <= 90:
                return 'высокий уровень тревожности'
            elif value > 90:
                return 'очень высокий уровень тревожности'
            else:
                return 'чрезмерное спокойствие'
        else:
            if 23 <= value <= 47:
                return 'нормальный уровень тревожности'
            elif 48 <= value <= 60:
                return 'несколько повышенный уровень тревожности'
            elif 61 <= value <= 72:
                return 'высокий уровень тревожности'
            elif value > 72:
                return 'очень высокий уровень тревожности'
            else:
                return 'чрезмерное спокойствие'
    else:
        return 'Для данного Номера класса нет методики подсчета. Обрабатываются только 9,10,11 классы'


def calc_norm_all_condash_anxiety(ser:pd.Series):
    """
    Функция для подсчета уровня тревожности
    """
    row = ser.tolist() # превращаем в список
    group = int(row[0]) # курс
    sex = row[1] # пол

    if group == 9:
        if sex == 'Женский':
            return '30-78 баллов'

        else:
            return '17-73 баллов'

    elif group == 10:
        if sex == 'Женский':
            return '17-73 баллов'
        else:
            return '10-67 баллов'
    elif group == 11:
        if sex == 'Женский':
            return '35-76 баллов'
        else:
            return '23-60 баллов'
    else:
        return 'Для данного Номера класса нет методики подсчета. Обрабатываются только 9,10,11 классы'


def calc_level_study_condash_anxiety(ser:pd.Series):
    """
    Функция для подсчета учебной тревожности по шкале Кондаша
    """
    row = ser.tolist() # превращаем в список
    group = int(row[0]) # Номер_класса
    sex = row[1] # пол
    value = row[2] # значение которое нужно обработать

    if group == 9:
        if sex == 'Женский':
            if 7 <= value <= 19:
                return 'нормальный уровень тревожности'
            elif 20 <= value <= 25:
                return 'несколько повышенный уровень тревожности'
            elif 26 <= value <= 31:
                return 'высокий уровень тревожности'
            elif value > 31:
                return 'очень высокий уровень тревожности'
            else:
                return 'чрезмерное спокойствие'
        else:
            if 4 <= value <= 17:
                return 'нормальный уровень тревожности'
            elif 18 <= value <= 23:
                return 'несколько повышенный уровень тревожности'
            elif 24 <= value <= 30:
                return 'высокий уровень тревожности'
            elif value > 30:
                return 'очень высокий уровень тревожности'
            else:
                return 'чрезмерное спокойствие'
    elif group == 10:
        if sex == 'Женский':
            if 2 <= value <= 14:
                return 'нормальный уровень тревожности'
            elif 15 <= value <= 20:
                return 'несколько повышенный уровень тревожности'
            elif 21 <= value <= 26:
                return 'высокий уровень тревожности'
            elif value > 26:
                return 'очень высокий уровень тревожности'
            else:
                return 'чрезмерное спокойствие'
        else:
            if 1 <= value <= 13:
                return 'нормальный уровень тревожности'
            elif 14 <= value <= 19:
                return 'несколько повышенный уровень тревожности'
            elif 20 <= value <= 25:
                return 'высокий уровень тревожности'
            elif value > 25:
                return 'очень высокий уровень тревожности'
            else:
                return 'чрезмерное спокойствие'
    elif group == 11:
        if sex == 'Женский':
            if 5 <= value <= 17:
                return 'нормальный уровень тревожности'
            elif 18 <= value <= 23:
                return 'несколько повышенный уровень тревожности'
            elif 24 <= value <= 30:
                return 'высокий уровень тревожности'
            elif value > 30:
                return 'очень высокий уровень тревожности'
            else:
                return 'чрезмерное спокойствие'
        else:
            if 5 <= value <= 14:
                return 'нормальный уровень тревожности'
            elif 15 <= value <= 19:
                return 'несколько повышенный уровень тревожности'
            elif 20 <= value <= 24:
                return 'высокий уровень тревожности'
            elif value > 24:
                return 'очень высокий уровень тревожности'
            else:
                return 'чрезмерное спокойствие'
    else:
        return 'Для данного Номера класса нет методики подсчета. Обрабатываются только 9,10,11 классы'

def calc_norm_study_condash_anxiety(ser:pd.Series):
    """
    Функция для подсчета уровня тревожности
    """
    row = ser.tolist() # превращаем в список
    group = int(row[0]) # курс
    sex = row[1] # пол

    if group == 9:
        if sex == 'Женский':
            return '7-25 баллов'

        else:
            return '4-23 баллов'

    elif group == 10:
        if sex == 'Женский':
            return '2-20 баллов'
        else:
            return '1-19 баллов'
    elif group == 11:
        if sex == 'Женский':
            return '5-23 баллов'
        else:
            return '5-19 баллов'
    else:
        return 'Для данного Номера класса нет методики подсчета. Обрабатываются только 9,10,11 классы'


def calc_level_self_condash_anxiety(ser:pd.Series):
    """
    Функция для подсчета самоценочной тревожности
    """
    row = ser.tolist() # превращаем в список
    group = int(row[0]) # Номер_класса
    sex = row[1] # пол
    value = row[2] # значение которое нужно обработать

    if group == 9:
        if sex == 'Женский':
            if 11 <= value <= 21:
                return 'нормальный уровень тревожности'
            elif 22 <= value <= 26:
                return 'несколько повышенный уровень тревожности'
            elif 27 <= value <= 31:
                return 'высокий уровень тревожности'
            elif value > 31:
                return 'очень высокий уровень тревожности'
            else:
                return 'чрезмерное спокойствие'
        else:
            if 4 <= value <= 18:
                return 'нормальный уровень тревожности'
            elif 19 <= value <= 25:
                return 'несколько повышенный уровень тревожности'
            elif 26 <= value <= 32:
                return 'высокий уровень тревожности'
            elif value > 32:
                return 'очень высокий уровень тревожности'
            else:
                return 'чрезмерное спокойствие'
    elif group == 10:
        if sex == 'Женский':
            if 6 <= value <= 19:
                return 'нормальный уровень тревожности'
            elif 20 <= value <= 26:
                return 'несколько повышенный уровень тревожности'
            elif 27 <= value <= 32:
                return 'высокий уровень тревожности'
            elif value > 32:
                return 'очень высокий уровень тревожности'
            else:
                return 'чрезмерное спокойствие'
        else:
            if 1 <= value <= 17:
                return 'нормальный уровень тревожности'
            elif 18 <= value <= 26:
                return 'несколько повышенный уровень тревожности'
            elif 27 <= value <= 34:
                return 'высокий уровень тревожности'
            elif value > 34:
                return 'очень высокий уровень тревожности'
            else:
                return 'чрезмерное спокойствие'
    elif group == 11:
        if sex == 'Женский':
            if 12 <= value <= 23:
                return 'нормальный уровень тревожности'
            elif 24 <= value <= 29:
                return 'несколько повышенный уровень тревожности'
            elif 30 <= value <= 34:
                return 'высокий уровень тревожности'
            elif value > 34:
                return 'очень высокий уровень тревожности'
            else:
                return 'чрезмерное спокойствие'
        else:
            if 8 <= value <= 17:
                return 'нормальный уровень тревожности'
            elif 18 <= value <= 22:
                return 'несколько повышенный уровень тревожности'
            elif 23 <= value <= 27:
                return 'высокий уровень тревожности'
            elif value > 27:
                return 'очень высокий уровень тревожности'
            else:
                return 'чрезмерное спокойствие'
    else:
        return 'Для данного Номера класса нет методики подсчета. Обрабатываются только 9,10,11 классы'

def calc_norm_self_condash_anxiety(ser:pd.Series):
    """
    Функция для подсчета уровня тревожности
    """
    row = ser.tolist() # превращаем в список
    group = int(row[0]) # курс
    sex = row[1] # пол

    if group == 9:
        if sex == 'Женский':
            return '11-26 баллов'
        else:
            return '4-25 баллов'

    elif group == 10:
        if sex == 'Женский':
            return '6-26 баллов'
        else:
            return '1-26 баллов'
    elif group == 11:
        if sex == 'Женский':
            return '12-29 баллов'
        else:
            return '8-22 баллов'
    else:
        return 'Для данного Номера класса нет методики подсчета. Обрабатываются только 9,10,11 классы'




def calc_level_soc_condash_anxiety(ser:pd.Series):
    """
    Функция для подсчета межличностной тревожности
    """
    row = ser.tolist() # превращаем в список
    group = int(row[0]) # Номер_класса
    sex = row[1] # пол
    value = row[2] # значение которое нужно обработать

    if group == 9:
        if sex == 'Женский':
            if 7 <= value <= 20:
                return 'нормальный уровень тревожности'
            elif 21 <= value <= 27:
                return 'несколько повышенный уровень тревожности'
            elif 28 <= value <= 33:
                return 'высокий уровень тревожности'
            elif value > 33:
                return 'очень высокий уровень тревожности'
            else:
                return 'чрезмерное спокойствие'
        else:
            if 5 <= value <= 17:
                return 'нормальный уровень тревожности'
            elif 18 <= value <= 24:
                return 'несколько повышенный уровень тревожности'
            elif 25 <= value <= 30:
                return 'высокий уровень тревожности'
            elif value > 30:
                return 'очень высокий уровень тревожности'
            else:
                return 'чрезмерное спокойствие'
    elif group == 10:
        if sex == 'Женский':
            if 4 <= value <= 19:
                return 'нормальный уровень тревожности'
            elif 20 <= value <= 26:
                return 'несколько повышенный уровень тревожности'
            elif 27 <= value <= 33:
                return 'высокий уровень тревожности'
            elif value > 33:
                return 'очень высокий уровень тревожности'
            else:
                return 'чрезмерное спокойствие'
        else:
            if 3 <= value <= 17:
                return 'нормальный уровень тревожности'
            elif 18 <= value <= 25:
                return 'несколько повышенный уровень тревожности'
            elif 26 <= value <= 32:
                return 'высокий уровень тревожности'
            elif value > 32:
                return 'очень высокий уровень тревожности'
            else:
                return 'чрезмерное спокойствие'
    elif group == 11:
        if sex == 'Женский':
            if 5 <= value <= 20:
                return 'нормальный уровень тревожности'
            elif 21 <= value <= 28:
                return 'несколько повышенный уровень тревожности'
            elif 29 <= value <= 36:
                return 'высокий уровень тревожности'
            elif value > 36:
                return 'очень высокий уровень тревожности'
            else:
                return 'чрезмерное спокойствие'
        else:
            if 5 <= value <= 14:
                return 'нормальный уровень тревожности'
            elif 15 <= value <= 19:
                return 'несколько повышенный уровень тревожности'
            elif 20 <= value <= 23:
                return 'высокий уровень тревожности'
            elif value > 23:
                return 'очень высокий уровень тревожности'
            else:
                return 'чрезмерное спокойствие'
    else:
        return 'Для данного Номера класса нет методики подсчета. Обрабатываются только 9,10,11 классы'

def calc_norm_soc_condash_anxiety(ser:pd.Series):
    """
    Функция для подсчета уровня тревожности
    """
    row = ser.tolist() # превращаем в список
    group = int(row[0]) # курс
    sex = row[1] # пол

    if group == 9:
        if sex == 'Женский':
            return '7-27 баллов'
        else:
            return '5-24 баллов'

    elif group == 10:
        if sex == 'Женский':
            return '4-26 баллов'
        else:
            return '3-25 баллов'
    elif group == 11:
        if sex == 'Женский':
            return '5-28 баллов'
        else:
            return '5-19 баллов'
    else:
        return 'Для данного Номера класса нет методики подсчета. Обрабатываются только 9,10,11 классы'


def create_kondash_list_on_level(base_df:pd.DataFrame,out_dct:dict,lst_level:list,dct_prefix:dict):
    """
    Функция для создания списков по уровням шкал
    :param base_df: датафрейм с результатами
    :param out_dct: словарь с датафреймами
    :param lst_level: список уровней по которым нужно сделать списки
    :param dct_prefix: префиксы для названий листов
    :return: обновлейнный out dct
    """
    for key,value in dct_prefix.items():
        dct_level = dict()
        for level in lst_level:
            temp_df = base_df[base_df[key] == level]
            if temp_df.shape[0] != 0:
                if level == 'нормальный уровень тревожности':
                    level = 'нормальный'
                elif level == 'несколько повышенный уровень тревожности':
                    level = 'несколько повышенный'
                elif level == 'высокий уровень тревожности':
                    level = 'высокий'
                elif level == 'очень высокий уровень тревожности':
                    level = 'очень высокий'
                else:
                    level = 'чрезмерное спокойствие'
                dct_level[f'{dct_prefix[key]}. {level}'] = temp_df
        out_dct.update(dct_level)

    return out_dct


def calc_count_level(df:pd.DataFrame, lst_cat, val_cat, col_cat, lst_cols:list):
    """
    Функция для создания сводных датафреймов по шкалам

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
    count_df['% нормальный уровень тревожности от общего'] = round(
        count_df['нормальный уровень тревожности'] / count_df['Итого'], 2) * 100
    count_df['% несколько повышенный уровень тревожности от общего'] = round(
        count_df['несколько повышенный уровень тревожности'] / count_df['Итого'], 2) * 100
    count_df['% высокий уровень тревожности от общего'] = round(
        count_df['высокий уровень тревожности'] / count_df['Итого'], 2) * 100
    count_df['% очень высокий уровень тревожности от общего'] = round(
        count_df['очень высокий уровень тревожности'] / count_df['Итого'], 2) * 100
    count_df['% чрезмерное спокойствие от общего'] = round(
        count_df['чрезмерное спокойствие'] / count_df['Итого'], 2) * 100


    return count_df




def create_result_kondash(base_df:pd.DataFrame, out_dct:dict,):
    """
    Функция для подсчета результата если указаны колонки по которым нужно провести свод
    :param df: датафрейм с результатами
    :param out_dct: словарь с уже подсчитанными базовыми данными
    :param lst_svod_cols: список сводных колонок
    :return: словарь
    """
    lst_reindex_one_level_cols = ['Номер_класса','Класс','Пол','нормальный уровень тревожности', 'несколько повышенный уровень тревожности',
             'высокий уровень тревожности','очень высокий уровень тревожности','чрезмерное спокойствие',
                                                      'Итого']

    lst_kondash_svod_cols = ['Номер_класса','Класс','Пол']

    # Субшкалы
    svod_count_one_level_ot_df = calc_count_level(base_df, lst_kondash_svod_cols,
                                                      'Значение_общей_тревожности',
                                                      'Уровень_общей_тревожности',
                                                      lst_reindex_one_level_cols)

    svod_count_one_level_ut_df = calc_count_level(base_df, lst_kondash_svod_cols,
                                                          'Значение_учебной_тревожности',
                                                          'Уровень_учебной_тревожности',
                                                          lst_reindex_one_level_cols)

    svod_count_one_level_st_df = calc_count_level(base_df, lst_kondash_svod_cols,
                                                         'Значение_самооценочной_тревожности',
                                                         'Уровень_самооценочной_тревожности',
                                                         lst_reindex_one_level_cols)
    svod_count_one_level_mt_df = calc_count_level(base_df, lst_kondash_svod_cols,
                                                         'Значение_межличностной_тревожности',
                                                         'Уровень_межличностной_тревожности',
                                                         lst_reindex_one_level_cols)

    # Считаем среднее по субшкалам
    svod_mean_one_df = pd.pivot_table(base_df,
                                      index=lst_kondash_svod_cols,
                                      values=['Значение_общей_тревожности',
                                              'Значение_учебной_тревожности',
                                              'Значение_самооценочной_тревожности',
                                              'Значение_межличностной_тревожности',
                                              ],
                                      aggfunc=round_mean)
    svod_mean_one_df.reset_index(inplace=True)
    # упорядочиваем колонки
    new_order_cols = lst_kondash_svod_cols.copy()
    new_order_cols.extend((['Значение_общей_тревожности',
                            'Значение_учебной_тревожности',
                            'Значение_самооценочной_тревожности',
                            'Значение_межличностной_тревожности',
                            ]))
    svod_mean_one_df = svod_mean_one_df.reindex(columns=new_order_cols)

    dct_rename_cols_mean = {'Значение_общей_тревожности': 'Ср. ОТ',
                            'Значение_учебной_тревожности': 'Ср. УТ',
                            'Значение_самооценочной_тревожности': 'Ср. СТ',
                            'Значение_межличностной_тревожности': 'Ср. МТ',
                            }
    svod_mean_one_df.rename(columns=dct_rename_cols_mean, inplace=True)

    out_dct.update({f'Ср Номер Класс Пол': svod_mean_one_df,
                    f'Свод Номер Класс Пол ОТ': svod_count_one_level_ot_df,
                    f'Свод Номер Класс Пол УТ': svod_count_one_level_ut_df,
                    f'Свод Номер Класс Пол СТ': svod_count_one_level_st_df,
                    f'Свод Номер Класс Пол МТ': svod_count_one_level_mt_df})

    for idx, name_column in enumerate(lst_kondash_svod_cols):
        # Тревожность
        lst_reindex_column_level_cols = [lst_kondash_svod_cols[idx], 'нормальный уровень тревожности', 'несколько повышенный уровень тревожности',
             'высокий уровень тревожности','очень высокий уровень тревожности','чрезмерное спокойствие',
                                         'Итого']

        # Субшкалы
        svod_count_column_level_ot_df = calc_count_level(base_df, lst_kondash_svod_cols[idx],
                                                      'Значение_общей_тревожности',
                                                      'Уровень_общей_тревожности',
                                                      lst_reindex_column_level_cols)

        svod_count_column_level_ut_df = calc_count_level(base_df, lst_kondash_svod_cols[idx],
                                                      'Значение_учебной_тревожности',
                                                      'Уровень_учебной_тревожности',
                                                      lst_reindex_column_level_cols)

        svod_count_column_level_st_df = calc_count_level(base_df, lst_kondash_svod_cols[idx],
                                                      'Значение_самооценочной_тревожности',
                                                      'Уровень_самооценочной_тревожности',
                                                      lst_reindex_column_level_cols)
        svod_count_column_level_mt_df = calc_count_level(base_df, lst_kondash_svod_cols[idx],
                                                      'Значение_межличностной_тревожности',
                                                      'Уровень_межличностной_тревожности',
                                                      lst_reindex_column_level_cols)

        # Считаем среднее по субшкалам
        svod_mean_column_df = pd.pivot_table(base_df,
                                          index=[lst_kondash_svod_cols[idx]],
                                          values=['Значение_общей_тревожности',
                                                  'Значение_учебной_тревожности',
                                                  'Значение_самооценочной_тревожности',
                                                  'Значение_межличностной_тревожности',
                                                  ],
                                          aggfunc=round_mean)
        svod_mean_column_df.reset_index(inplace=True)
        # упорядочиваем колонки
        new_order_cols = [lst_kondash_svod_cols[idx]].copy()
        new_order_cols.extend((['Значение_общей_тревожности',
                                'Значение_учебной_тревожности',
                                'Значение_самооценочной_тревожности',
                                'Значение_межличностной_тревожности',
                                ]))
        svod_mean_column_df = svod_mean_column_df.reindex(columns=new_order_cols)
        dct_rename_cols_mean = {'Значение_общей_тревожности': 'Ср. ОТ',
                                'Значение_учебной_тревожности': 'Ср. УТ',
                                'Значение_самооценочной_тревожности': 'Ср. СТ',
                                'Значение_межличностной_тревожности': 'Ср. МТ',
                                }
        svod_mean_column_df.rename(columns=dct_rename_cols_mean, inplace=True)

        out_dct.update({f'Ср {name_column}': svod_mean_column_df,
                        f'Свод {name_column} ОТ': svod_count_column_level_ot_df,
                        f'Свод {name_column} УТ': svod_count_column_level_ut_df,
                        f'Свод {name_column} СТ': svod_count_column_level_st_df,
                        f'Свод {name_column} МТ': svod_count_column_level_mt_df})
    return out_dct








def processing_kondash_anxiety_school(base_df: pd.DataFrame, answers_df: pd.DataFrame,lst_svod_cols:list):
    """
    Проверка колонок и значений таблицы
    """
    try:
        # Проверяем наличие колонок Номер класса, Буква класса, Пол
        diff_req_cols = {'Номер_класса','Буква_класса','Пол'}.difference(set(base_df.columns))
        if len(diff_req_cols) !=0:
            raise NotReqColumn

        # Обрабатываем колонку номер класса
        base_df['Номер_класса'] = base_df['Номер_класса'].apply(convert_to_int)
        base_df['Номер_класса'] = base_df['Номер_класса'].astype(str)
        base_df['Буква_класса'] = base_df['Буква_класса'].astype(str)
        # Проверяем на пол
        diff_sex = set(base_df['Пол'].unique()).difference({'Мужской','Женский'})
        if len(diff_sex) != 0:
            raise BadValueSex

        # Создаем колонку класс
        base_df['Класс'] = base_df['Номер_класса']+base_df['Буква_класса']

        out_answer_df = base_df.copy() # делаем копию для последующего соединения с сырыми ответами
        if len(answers_df.columns) != 30:
            raise BadCountColumnsCondashAnxiety

        # очищаем названия колонок от возможных сочетаний .1 которые добавляет пандас при одинаковых колонках
        clean_df_lst = []
        for name_column in answers_df.columns:
            clean_name = re.sub(r'.\d+$', '', name_column)
            clean_df_lst.append(clean_name)


        answers_df.columns = clean_df_lst

        dct_replace_value = {'ситуация совершенно не кажется вам неприятной': 0,
                             'ситуация немного волнует, беспокоит вас': 1,
                             'ситуация достаточно неприятна и вызывает такое беспокойство, что вы предпочли бы избежать её': 2,
                             'ситуация очень неприятна и вызывает сильное беспокойство, тревогу, страх': 3,
                             'ситуация для вас крайне неприятна, если вы не можете перенести её и она вызывает у вас очень сильное беспокойство, очень сильный страх': 4}

        # Словарь с проверочными данными
        lst_check_cols = ['Отвечать у доски', 'Пойти в дом к незнакомым людям',
                          'Участвовать в соревнованиях, конкурсах, в олимпиадах',
                          'Разговаривать с директором школы', 'Думать о своем будущем',
                          'Учитель смотрит по журналу, кого бы спросить',
                          'Тебя критикуют, в чем- то обвиняют',
                          'На тебя смотрят, когда ты что-нибудь делаешь (наблюдают за тобой во время работы, решения задачи)',
                          'Пишешь контрольную работу',
                          'После контрольной учитель называет отметки', 'На тебя не обращают внимания',
                          'У тебя что-то не получается',
                          'Ждешь родителей с родительского собрания', 'Тебе грозит неуспех, провал',
                          'Слышишь за своей спиной смех',
                          'Сдаешь экзамены в школе', 'На тебя сердятся (непонятно почему)',
                          'Выступать перед большой аудиторией',
                          'Предстоит важное, решающее дело', 'Не понимаешь объяснений учителя',
                          'С тобой не согласны, противоречат тебе',
                          'Сравниваешь себя с другими', 'Проверяют твои способности', 'На тебя смотрят как на маленького',
                          'На уроке учитель неожиданно задает тебе вопрос', 'Замолчали, когда ты подошел',
                          'Оценивается твоя работа',
                          'Думаешь о своих делах', 'Тебе надо принять для себя решение',
                          'Не можешь справиться с домашним заданием']

        # Проверяем порядок колонок
        order_main_columns = lst_check_cols  # порядок колонок и названий как должно быть
        order_temp_df_columns = list(answers_df.columns)  # порядок колонок проверяемого файла
        error_order_lst = []  # список для несовпадающих пар
        # Сравниваем попарно колонки
        for main, temp in zip(order_main_columns, order_temp_df_columns):
            if main != temp:
                error_order_lst.append(f'На месте колонки {main} находится колонка {temp}')
        if len(error_order_lst) != 0:
            raise BadOrderCondashAnxiety

        answers_df.replace(dct_replace_value, inplace=True)  # заменяем слова на цифры для подсчетов

        # Проверяем правильность замены слов на цифры
        valid_values = [0, 1, 2, 3, 4]

        # Проверяем, есть ли значения, отличающиеся от указанных в списке
        lst_error_answers = []  # список для хранения строк где найдены неправильные ответы

        for i in range(30):
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
            raise BadValueCondashAnxiety

        # Колонки учебной тревожности
        lst_study_anxiety = ['Отвечать у доски', 'Разговаривать с директором школы',
                             'Учитель смотрит по журналу, кого бы спросить', 'Пишешь контрольную работу',
                             'После контрольной учитель называет отметки', 'Ждешь родителей с родительского собрания',
                             'Сдаешь экзамены в школе', 'Не понимаешь объяснений учителя',
                             'На уроке учитель неожиданно задает тебе вопрос',
                             'Не можешь справиться с домашним заданием']

        # Колонки самооценки
        lst_self_anxiety = ['Участвовать в соревнованиях, конкурсах, в олимпиадах', 'Думать о своем будущем',
                            'У тебя что-то не получается', 'Тебе грозит неуспех, провал',
                            'Предстоит важное, решающее дело', 'Сравниваешь себя с другими',
                            'Проверяют твои способности', 'Оценивается твоя работа',
                            'Думаешь о своих делах', 'Тебе надо принять для себя решение']

        # Колонки межличностной тревожности
        lst_soc_anxiety = ['Пойти в дом к незнакомым людям', 'Тебя критикуют, в чем- то обвиняют',
                           'На тебя смотрят, когда ты что-нибудь делаешь (наблюдают за тобой во время работы, решения задачи)',
                           'На тебя не обращают внимания',
                           'Слышишь за своей спиной смех', 'На тебя сердятся (непонятно почему)',
                           'Выступать перед большой аудиторией',
                           'С тобой не согласны, противоречат тебе',
                           'На тебя смотрят как на маленького', 'Замолчали, когда ты подошел']

        # Считаем результат общая тревожность
        base_df['Значение_общей_тревожности'] = answers_df.sum(axis=1)
        base_df['Норма_общей_тревожности'] = base_df[['Номер_класса', 'Пол']].apply(calc_norm_all_condash_anxiety,
                                                                                    axis=1)
        base_df['Уровень_общей_тревожности'] = base_df[['Номер_класса', 'Пол', 'Значение_общей_тревожности']].apply(
            calc_level_all_condash_anxiety, axis=1)

        # Считаем учебную тревожность в оригинале школьная
        base_df['Значение_учебной_тревожности'] = answers_df[lst_study_anxiety].sum(axis=1)
        base_df['Норма_учебной_тревожности'] = base_df[['Номер_класса', 'Пол']].apply(calc_norm_study_condash_anxiety,
                                                                                      axis=1)
        base_df['Уровень_учебной_тревожности'] = base_df[
            ['Номер_класса', 'Пол', 'Значение_учебной_тревожности']].apply(calc_level_study_condash_anxiety,
                                                                           axis=1)

        # Считаем самооценочную тревожность
        base_df['Значение_самооценочной_тревожности'] = answers_df[lst_self_anxiety].sum(axis=1)
        base_df['Норма_самоценочной_тревожности'] = base_df[['Номер_класса', 'Пол']].apply(
            calc_norm_self_condash_anxiety,
            axis=1)
        base_df['Уровень_самооценочной_тревожности'] = base_df[
            ['Номер_класса', 'Пол', 'Значение_самооценочной_тревожности']].apply(calc_level_self_condash_anxiety,
                                                                                 axis=1)
        # Считаем межличностную тревожность
        base_df['Значение_межличностной_тревожности'] = answers_df[lst_soc_anxiety].sum(axis=1)
        base_df['Норма_межличностной_тревожности'] = base_df[['Номер_класса', 'Пол']].apply(
            calc_norm_soc_condash_anxiety,
            axis=1)
        base_df['Уровень_межличностной_тревожности'] = base_df[
            ['Номер_класса', 'Пол', 'Значение_межличностной_тревожности']].apply(calc_level_soc_condash_anxiety,
                                                                                 axis=1)

        # Создаем датафрейм для создания части в общий датафрейм
        part_df = pd.DataFrame()

        part_df['ШТК_ОТ_Значение'] = base_df['Значение_общей_тревожности']
        part_df['ШТК_ОТ_Уровень'] = base_df['Уровень_общей_тревожности']
        part_df['ШТК_УТ_Значение'] = base_df['Значение_учебной_тревожности']
        part_df['ШТК_УТ_Уровень'] = base_df['Уровень_учебной_тревожности']
        part_df['ШТК_СТ_Значение'] = base_df['Значение_самооценочной_тревожности']
        part_df['ШТК_СТ_Уровень'] = base_df['Уровень_самооценочной_тревожности']
        part_df['ШТК_МТ_Значение'] = base_df['Значение_межличностной_тревожности']
        part_df['ШТК_МТ_Уровень'] = base_df['Уровень_межличностной_тревожности']

        out_answer_df = pd.concat([out_answer_df, answers_df], axis=1)  # Датафрейм для проверки

        # Соединяем анкетную часть с результатной
        base_df.sort_values(by='Значение_общей_тревожности', ascending=False, inplace=True)  # сортируем

        # Делаем свод  по  шкалам
        dct_svod_sub = {'Значение_общей_тревожности': 'Уровень_общей_тревожности',
                        'Значение_учебной_тревожности': 'Уровень_учебной_тревожности',
                        'Значение_самооценочной_тревожности': 'Уровень_самооценочной_тревожности',
                        'Значение_межличностной_тревожности': 'Уровень_межличностной_тревожности',
                        }

        dct_rename_svod_sub = {'Значение_общей_тревожности': 'ОТ',
                               'Значение_учебной_тревожности': 'УТ',
                               'Значение_самооценочной_тревожности': 'СТ',
                               'Значение_межличностной_тревожности': 'МТ',
                               }

        # Списки для шкал
        lst_level = ['нормальный уровень тревожности', 'несколько повышенный уровень тревожности',
                     'высокий уровень тревожности','очень высокий уровень тревожности','чрезмерное спокойствие']

        base_svod_sub_df = create_union_svod(base_df, dct_svod_sub, dct_rename_svod_sub, lst_level)

        # считаем среднее значение по шкалам
        avg_ot = round(base_df['Значение_общей_тревожности'].mean(), 2)
        avg_ut = round(base_df['Значение_учебной_тревожности'].mean(), 2)
        avg_st = round(base_df['Значение_самооценочной_тревожности'].mean(), 2)
        avg_mt = round(base_df['Значение_межличностной_тревожности'].mean(), 2)

        avg_dct = {'Среднее значение шкалы Общая тревожность': avg_ot,
                   'Среднее значение шкалы Учебная тревожность': avg_ut,
                   'Среднее значение шкалы Самооценочная тревожность': avg_st,
                   'Среднее значение шкалы Межличностная тревожность': avg_mt,
                   }

        avg_df = pd.DataFrame.from_dict(avg_dct, orient='index')
        avg_df = avg_df.reset_index()
        avg_df.columns = ['Показатель', 'Среднее значение']

        # формируем основной словарь
        out_dct = {'Списочный результат': base_df, 'Список для проверки': out_answer_df,
                   'Свод по шкалам': base_svod_sub_df,
                   'Среднее по шкалам': avg_df,
                   }

        # Делаем списки
        dct_prefix = {'Уровень_общей_тревожности': 'ОТ',
                      'Уровень_учебной_тревожности': 'УТ',
                      'Уровень_самооценочной_тревожности': 'СТ',
                      'Уровень_межличностной_тревожности': 'МТ',
                      }

        out_dct = create_kondash_list_on_level(base_df, out_dct, lst_level, dct_prefix)

        out_dct = create_result_kondash(base_df, out_dct)

        return out_dct, part_df

    except BadOrderCondashAnxiety:
        messagebox.showerror('Лахеcис',
                             f'При обработке вопросов теста Шкала тревожности Кондаш обнаружены неправильные вопросы. Проверьте названия колонок с вопросами:\n'
                             f'{error_order_lst}\n'
                             f'Используйте при создании Яндекс-формы написание вопросов из руководства пользователя программы Лахесис.')
    except BadValueCondashAnxiety:
        messagebox.showerror('Лахеcис',
                             f'При обработке вопросов теста Шкала тревожности Кондаш обнаружены неправильные варианты ответов. Проверьте ответы на указанных строках:\n'
                             f'{error_message}\n'
                             f'Используйте при создании Яндекс-формы написание вариантов ответа из руководства пользователя программы Лахесис.')

    except BadCountColumnsCondashAnxiety:
        messagebox.showerror('Лахеcис',
                             f'Проверьте количество колонок с ответами на тест Шкала тревожности Кондаш\n'
                             f'Должно быть 30колонок с ответами')
    except NotReqColumn:
        messagebox.showerror('Лахеcис',
                             f'В анкетной части отсутствуют обязательные для теста Шкала тревожности Кондаша колонки {diff_req_cols}')
    except BadValueSex:
        messagebox.showerror('Лахеcис',
                             f'В колонке Пол найдены значения отличающиеся от допустимых значений: Мужской или Женский {diff_sex}')








