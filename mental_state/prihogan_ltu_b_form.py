"""
Скрипт для обработки результатов теста Шкала личностной тревожности учащихся А. М. Прихожан Форма Б

"""

import pandas as pd
import re
import os
import openpyxl
from openpyxl.utils.dataframe import dataframe_to_rows
from openpyxl.styles import Alignment
from openpyxl.utils import get_column_letter
from tkinter import messagebox
from lachesis_support_functions import round_mean_two,calc_count_scale,create_union_svod, create_list_on_level

class BadOrderLTUPB(Exception):
    """
    Исключение для обработки случая когда колонки не совпадают
    """
    pass


class BadValueLTUPB(Exception):
    """
    Исключение для неправильных значений в вариантах ответов
    """
    pass

class BadCountColumnsLTUPB(Exception):
    """
    Исключение для обработки случая если количество колонок не равно 40
    """
    pass

class NotReqColumnLTUPB(Exception):
    """
    Исключение для обработки случая когда нет обязательных колонок Пол И Возраст
    """
    pass

class BadValueSexLTUPB(Exception):
    """
    Исключение для обработки случая когда в колонке Пол есть значения отличающиеся от Мужской или Женский
    """
    pass

class BadValueAgeLTUPB(Exception):
    """
    Исключение для обработки случая когда в колонке Пол есть значения отличающиеся от требуемого возраста
    """
    pass

def calc_range(value):
    """
    Функция для подсчета диапазонов
    :param value: значение
    :return:
    """
    if 1 <= value <= 2:
        return 'тревожность отсутствует'
    elif 3 <=value <= 6:
        return 'нормальный уровень'
    elif 7<=value <= 8:
        return 'несколько повышенная тревожность'
    elif value == 9:
        return 'явно повышенная тревожность'
    else:
        return 'очень высокая тревожность'



def calc_ot_sten(ser:pd.Series):
    """
    Функция для подсчета Стена
    :param ser: пол и значение
    :return:
    """
    row = ser.tolist() # превращаем в список
    sex = row[0] # пол
    age = row[1] # возраст
    value = row[2] # значение которое нужно обработать

    if age == '13-14 лет':
        if sex == 'Женский':
            if  0<= value <=34 :
                return 1
            elif  35<= value <=43 :
                return 2
            elif  44<= value <=52 :
                return 3
            elif  53<= value <=61 :
                return 4
            elif 62<= value <=70:
                return 5
            elif  71<= value <=80 :
                return 6
            elif  81<= value <=88 :
                return 7
            elif  89<= value <=98 :
                return 8
            elif  99<= value <=107 :
                return 9
            else:
                return 10
        else:
            if  0<= value <=37 :
                return 1
            elif  38<= value <=45 :
                return 2
            elif  46<= value <=53 :
                return 3
            elif  54<= value <=61 :
                return 4
            elif 62<= value <=69:
                return 5
            elif  70<= value <=77 :
                return 6
            elif  78<= value <=85 :
                return 7
            elif  86<= value <=93 :
                return 8
            elif  94<= value <=101 :
                return 9
            else:
                return 10
    else:
        if sex == 'Женский':
            if  0<= value <=33 :
                return 1
            elif  34<= value <=39 :
                return 2
            elif  40<= value <=46 :
                return 3
            elif  47<= value <=53 :
                return 4
            elif 54<= value <=60:
                return 5
            elif  61<= value <=67 :
                return 6
            elif  68<= value <=74 :
                return 7
            elif  75<= value <=80 :
                return 8
            elif  81<= value <=87 :
                return 9
            else:
                return 10
        else:
            if  0<= value <=27 :
                return 1
            elif  28<= value <=34 :
                return 2
            elif  35<= value <=41 :
                return 3
            elif  42<= value <=47 :
                return 4
            elif 48<= value <=54:
                return 5
            elif  55<= value <=61 :
                return 6
            elif  62<= value <=68 :
                return 7
            elif  69<= value <=75 :
                return 8
            elif  76<= value <=82 :
                return 9
            else:
                return 10


def calc_sht_sten(ser:pd.Series):
    """
    Функция для подсчета Стена
    :param ser: пол и значение
    :return:
    """
    row = ser.tolist() # превращаем в список
    sex = row[0] # пол
    age = row[1] # возраст
    value = row[2] # значение которое нужно обработать

    if age == '13-14 лет':
        if sex == 'Женский':
            if 0 <= value <= 8:
                return 1
            elif 9 <= value <=10 :
                return 2
            elif  11<= value <=13 :
                return 3
            elif  14<= value <= 15:
                return 4
            elif 16<= value <=18:
                return 5
            elif  19<= value <=20 :
                return 6
            elif  21<= value <= 22:
                return 7
            elif  23<= value <= 25:
                return 8
            elif  26<= value <=27 :
                return 9
            else:
                return 10
        else:
            if  0<= value <=7 :
                return 1
            elif  8<= value <=9 :
                return 2
            elif  10<= value <=12 :
                return 3
            elif  13<= value <=15 :
                return 4
            elif 16<= value <=17:
                return 5
            elif  18<= value <=20 :
                return 6
            elif  21<= value <= 22:
                return 7
            elif  23<= value <= 25:
                return 8
            elif  26<= value <=28 :
                return 9
            else:
                return 10
    else:
        if sex == 'Женский':
            if 0 <= value <=7 :
                return 1
            elif  8<= value <=9 :
                return 2
            elif  10<= value <=11 :
                return 3
            elif  12<= value <= 13:
                return 4
            elif value ==14:
                return 5
            elif  15<= value <=16 :
                return 6
            elif  17<= value <=18 :
                return 7
            elif 19 <= value <=20 :
                return 8
            elif  21<= value <=22 :
                return 9
            else:
                return 10
        else:
            if  0<= value <=6 :
                return 1
            elif  value ==7 :
                return 2
            elif  value == 8:
                return 3
            elif value == 9:
                return 4
            elif value ==10:
                return 5
            elif  value ==11 :
                return 6
            elif  12<= value <=13 :
                return 7
            elif  value ==14 :
                return 8
            elif  value ==15 :
                return 9
            else:
                return 10




def calc_st_sten(ser:pd.Series):
    """
    Функция для подсчета Стена
    :param ser: пол и значение
    :return:
    """
    row = ser.tolist() # превращаем в список
    sex = row[0] # пол
    age = row[1] # возраст
    value = row[2] # значение которое нужно обработать

    if age == '13-14 лет':
        if sex == 'Женский':
            if  0<= value <=8 :
                return 1
            elif 9 <= value <=10 :
                return 2
            elif 11 <= value <=13 :
                return 3
            elif  14<= value <=16 :
                return 4
            elif 17<= value <=18:
                return 5
            elif  19<= value <=21 :
                return 6
            elif  22<= value <=24 :
                return 7
            elif  25<= value <=26 :
                return 8
            elif 27 <= value <=29 :
                return 9
            else:
                return 10
        else:
            if  0<= value <=7 :
                return 1
            elif  8<= value <=10 :
                return 2
            elif  11<= value <=13 :
                return 3
            elif  14<= value <=16 :
                return 4
            elif 17<= value <=19:
                return 5
            elif  20<= value <=22 :
                return 6
            elif  23<= value <=25 :
                return 7
            elif  26<= value <=28 :
                return 8
            elif  29<= value <=31 :
                return 9
            else:
                return 10
    else:
        if sex == 'Женский':
            if  0<= value <=6 :
                return 1
            elif  7<= value <=8 :
                return 2
            elif 9 <= value <= 11 :
                return 3
            elif  12<= value <= 13:
                return 4
            elif 14<= value <=16:
                return 5
            elif  17<= value <=18 :
                return 6
            elif 19 <= value <=21 :
                return 7
            elif  22<= value <= 23:
                return 8
            elif  24<= value <=26 :
                return 9
            else:
                return 10
        else:
            if  0<= value <=7 :
                return 1
            elif  8<= value <=9 :
                return 2
            elif  10<= value <=12 :
                return 3
            elif  13<= value <=15 :
                return 4
            elif 16<= value <=17:
                return 5
            elif 18 <= value <=20 :
                return 6
            elif  21<= value <=23 :
                return 7
            elif  24<= value <=25 :
                return 8
            elif  26<= value <=28 :
                return 9
            else:
                return 10


def calc_mt_sten(ser:pd.Series):
    """
    Функция для подсчета Стена
    :param ser: пол и значение
    :return:
    """
    row = ser.tolist() # превращаем в список
    sex = row[0] # пол
    age = row[1] # возраст
    value = row[2] # значение которое нужно обработать

    if age == '13-14 лет':
        if sex == 'Женский':
            if 0 <= value <=6 :
                return 1
            elif  7<= value <=9 :
                return 2
            elif 10 <= value <=12 :
                return 3
            elif  13<= value <=15 :
                return 4
            elif 16<= value <=17:
                return 5
            elif  18<= value <=20 :
                return 6
            elif  21<= value <=23 :
                return 7
            elif  24<= value <=26 :
                return 8
            elif  27<= value <=29 :
                return 9
            else:
                return 10
        else:
            if  0<= value <=8 :
                return 1
            elif  9<= value <=11 :
                return 2
            elif  12<= value <=14 :
                return 3
            elif  15<= value <= 17:
                return 4
            elif 18<= value <=20:
                return 5
            elif  21<= value <=23 :
                return 6
            elif  24<= value <=26 :
                return 7
            elif 27 <= value <=29 :
                return 8
            elif  30<= value <=32 :
                return 9
            else:
                return 10
    else:
        if sex == 'Женский':
            if  0<= value <= 6:
                return 1
            elif 7 <= value <=8 :
                return 2
            elif  9<= value <=11 :
                return 3
            elif  12<= value <= 13:
                return 4
            elif 14<= value <=15:
                return 5
            elif  16<= value <=18 :
                return 6
            elif  19<= value <=20 :
                return 7
            elif  21<= value <=23 :
                return 8
            elif  24<= value <=25 :
                return 9
            else:
                return 10
        else:
            if  0<= value <=7 :
                return 1
            elif 8 <= value <=9 :
                return 2
            elif  10<= value <=12 :
                return 3
            elif 13 <= value <=15 :
                return 4
            elif 16<= value <=17:
                return 5
            elif  18<= value <=20 :
                return 6
            elif  21<= value <=23 :
                return 7
            elif  24<= value <=26 :
                return 8
            elif  27<= value <=28 :
                return 9
            else:
                return 10



def calc_magt_sten(ser:pd.Series):
    """
    Функция для подсчета Стена
    :param ser: пол и значение
    :return:
    """
    row = ser.tolist() # превращаем в список
    sex = row[0] # пол
    age = row[1] # возраст
    value = row[2] # значение которое нужно обработать

    if age == '13-14 лет':
        if sex == 'Женский':
            if  0<= value <=5:
                return 1
            elif  6<= value <=7 :
                return 2
            elif  9<= value <= 10:
                return 3
            elif  11<= value <= 13:
                return 4
            elif 14<= value <=15:
                return 5
            elif 16 <= value <=18 :
                return 6
            elif  19<= value <=21 :
                return 7
            elif  22<= value <=23 :
                return 8
            elif 24 <= value <=26 :
                return 9
            else:
                return 10
        else:
            if  0<= value <=6 :
                return 1
            elif  7<= value <=8 :
                return 2
            elif  10<= value <=11 :
                return 3
            elif  11<= value <=12 :
                return 4
            elif 13<= value <=14:
                return 5
            elif  15<= value <=16 :
                return 6
            elif 17 <= value <=18 :
                return 7
            elif  19<= value <=20 :
                return 8
            elif  21<= value <=23 :
                return 9
            else:
                return 10
    else:
        if sex == 'Женский':
            if  0<= value <=6 :
                return 1
            elif  7<= value <=9 :
                return 2
            elif  10<= value <=11 :
                return 3
            elif  12<= value <=14 :
                return 4
            elif 15<= value <=16:
                return 5
            elif  17<= value <=19 :
                return 6
            elif  20<= value <=22 :
                return 7
            elif  23<= value <=24 :
                return 8
            elif  25<= value <=27 :
                return 9
            else:
                return 10
        else:
            if  0<= value <=5 :
                return 1
            elif  6<= value <=7 :
                return 2
            elif  8<= value <=9 :
                return 3
            elif  value ==10 :
                return 4
            elif 11<= value <=12:
                return 5
            elif  value ==13 :
                return 6
            elif  14<= value <=15 :
                return 7
            elif  16<= value <=17 :
                return 8
            elif  value == 18:
                return 9
            else:
                return 10









def calc_sht_value(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [1,5,7,11,12,16,19,28,30,34]
    value_forward = 0  # результат
    for idx, value in enumerate(row, 1):
        if idx in lst_pr:
            value_forward += value
    return value_forward





def calc_st_value(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [3, 6, 8, 13, 17, 20, 25, 29, 33, 39]
    value_forward = 0  # результат
    for idx, value in enumerate(row, 1):
        if idx in lst_pr:
            value_forward += value
    return value_forward



def calc_mt_value(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [2, 9, 15, 18, 22, 24, 26, 32, 36, 38]
    value_forward = 0  # результат
    for idx, value in enumerate(row, 1):
        if idx in lst_pr:
            value_forward += value
    return value_forward



def calc_magt_value(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [4, 10, 14, 21, 23, 27, 31, 35, 37, 40]
    value_forward = 0  # результат
    for idx, value in enumerate(row, 1):
        if idx in lst_pr:
            value_forward += value
    return value_forward



def create_itog_stens(row):
    """
    Функция для создания строки с итоговым стеном
    :param row: строка с результатами
    :return:
    """
    lst_out = list(map(str,row))
    return '-'.join(lst_out)


def create_list_on_level_ltu_prih(base_df:pd.DataFrame, out_dct:dict, lst_level:list, dct_prefix:dict):
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
                if level == 'тревожность отсутствует':
                    level = 'отсутствует'
                elif level == 'нормальный уровень':
                    level = 'нормальный'
                elif level == 'несколько повышенная тревожность':
                    level = 'несколько повышенная'
                elif level == 'явно повышенная тревожность':
                    level = 'явно повышенная'
                else:
                    level = 'очень высокая'
                dct_level[f'{dct_prefix[key]}. {level}'] = temp_df
        out_dct.update(dct_level)

    return out_dct


def create_result_ltu_prih(base_df:pd.DataFrame, out_dct:dict, lst_svod_cols:list):
    """
    Функция для подсчета результата если указаны колонки по которым нужно провести свод
    :param df: датафрейм с результатами
    :param out_dct: словарь с уже подсчитанными базовыми данными
    :param lst_svod_cols: список сводных колонок
    :return: словарь
    """

    lst_level = ['тревожность отсутствует','нормальный уровень','несколько повышенная тревожность','явно повышенная тревожность','очень высокая тревожность']

    lst_reindex_one_level_cols = lst_svod_cols.copy()
    lst_reindex_one_level_cols.extend(['тревожность отсутствует','нормальный уровень','несколько повышенная тревожность','явно повышенная тревожность','очень высокая тревожность',
                                       'Итого'])  # Основная шкала

    # Интегральные показатели
    svod_count_one_level_s_df = calc_count_scale(base_df, lst_svod_cols,
                                                    'ОТ_Стен',
                                                    'ОТ_Уровень',
                                                    lst_reindex_one_level_cols, lst_level)
    svod_count_one_level_r_df = calc_count_scale(base_df, lst_svod_cols,
                                                    'ШТ_Стен',
                                                    'ШТ_Уровень',
                                                    lst_reindex_one_level_cols, lst_level)
    svod_count_one_level_b_df = calc_count_scale(base_df, lst_svod_cols,
                                                    'СТ_Стен',
                                                    'СТ_Уровень',
                                                    lst_reindex_one_level_cols, lst_level)
    svod_count_one_level_so_df = calc_count_scale(base_df, lst_svod_cols,
                                                    'МТ_Стен',
                                                    'МТ_Уровень',
                                                    lst_reindex_one_level_cols, lst_level)

    svod_count_one_level_ip_df = calc_count_scale(base_df, lst_svod_cols,
                                                    'МАГТ_Стен',
                                                    'МАГТ_Уровень',
                                                    lst_reindex_one_level_cols, lst_level)

    # Считаем среднее по субшкалам
    svod_mean_one_df = pd.pivot_table(base_df,
                                      index=lst_svod_cols,
                                      values=['ОТ_Стен',
                                              'ШТ_Стен',
                                              'СТ_Стен',
                                              'МТ_Стен',
                                              'МАГТ_Стен',
                                              ],
                                      aggfunc=round_mean_two)
    svod_mean_one_df.reset_index(inplace=True)

    # упорядочиваем колонки
    new_order_cols = lst_svod_cols.copy()
    new_order_cols.extend((['ОТ_Стен',
                            'ШТ_Стен',
                            'СТ_Стен',
                            'МТ_Стен',
                            'МАГТ_Стен',
                            ]))
    svod_mean_one_df = svod_mean_one_df.reindex(columns=new_order_cols)
    dct_rename_cols_mean = {'ОТ_Стен': 'Ср. значение стена Общая тревожность',
                            'ШТ_Стен': 'Ср. значение стена Школьная тревожность',
                            'СТ_Стен': 'Ср. значение стена Самооценочная тревожность',
                            'МТ_Стен': 'Ср. значение стена Межличностная тревожность',
                            'МАГТ_Стен': 'Ср. значение стена Магическая тревожность'}

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
                    f'ОТ {out_name}': svod_count_one_level_s_df,
                    f'ШТ {out_name}': svod_count_one_level_r_df,
                    f'СТ {out_name}': svod_count_one_level_b_df,
                    f'МТ {out_name}': svod_count_one_level_so_df,
                    f'МАГТ {out_name}': svod_count_one_level_ip_df,
                    })

    if len(lst_svod_cols) == 1:
        return out_dct
    else:
        for idx, name_column in enumerate(lst_svod_cols):
            lst_reindex_column_level_cols = [lst_svod_cols[idx],'тревожность отсутствует','нормальный уровень','несколько повышенная тревожность','явно повышенная тревожность','очень высокая тревожность',
                                                  'Итого']

            # Интегральные показатели
            svod_count_column_level_s_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                            'ОТ_Стен',
                                                            'ОТ_Уровень',
                                                            lst_reindex_column_level_cols, lst_level)
            svod_count_column_level_r_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                            'ШТ_Стен',
                                                            'ШТ_Уровень',
                                                            lst_reindex_column_level_cols, lst_level)
            svod_count_column_level_b_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                            'СТ_Стен',
                                                            'СТ_Уровень',
                                                            lst_reindex_column_level_cols, lst_level)
            svod_count_column_level_so_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                             'МТ_Стен',
                                                             'МТ_Уровень',
                                                             lst_reindex_column_level_cols, lst_level)

            svod_count_column_level_ip_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                             'МАГТ_Стен',
                                                             'МАГТ_Уровень',
                                                             lst_reindex_column_level_cols, lst_level)

            # Считаем среднее по субшкалам
            svod_mean_column_df = pd.pivot_table(base_df,
                                                 index=[lst_svod_cols[idx]],
                                                 values=['ОТ_Стен',
                                                         'ШТ_Стен',
                                                         'СТ_Стен',
                                                         'МТ_Стен',
                                                         'МАГТ_Стен',
                                                         ],
                                                 aggfunc=round_mean_two)
            svod_mean_column_df.reset_index(inplace=True)

            # упорядочиваем колонки
            new_order_cols = [lst_svod_cols[idx]].copy()
            new_order_cols.extend((['ОТ_Стен',
                                    'ШТ_Стен',
                                    'СТ_Стен',
                                    'МТ_Стен',
                                    'МАГТ_Стен',
                                    ]))
            svod_mean_column_df = svod_mean_column_df.reindex(columns=new_order_cols)
            dct_rename_cols_mean = {'ОТ_Стен': 'Ср. значение стена Общая тревожность',
                                    'ШТ_Стен': 'Ср. значение стена Школьная тревожность',
                                    'СТ_Стен': 'Ср. значение стена Самооценочная тревожность',
                                    'МТ_Стен': 'Ср. значение стена Межличностная тревожность',
                                    'МАГТ_Стен': 'Ср. значение стена Магическая тревожность'}

            svod_mean_column_df.rename(columns=dct_rename_cols_mean, inplace=True)

            # Готовим наименование
            name_column = lst_svod_cols[idx]
            name_column = re.sub(r'[\[\]\'+()<> :"?*|\\/]', '_', name_column)
            name_column = name_column[:15]

            out_dct.update({f'Ср {name_column}': svod_mean_column_df,
                            f'ОТ {name_column}': svod_count_column_level_s_df,
                            f'ШТ {name_column}': svod_count_column_level_r_df,
                            f'СТ {name_column}': svod_count_column_level_b_df,
                            f'МТ {name_column}': svod_count_column_level_so_df,
                            f'МАГТ {name_column}': svod_count_column_level_ip_df,
                            })
        return out_dct


def processing_ltu_prih_form_b(base_df: pd.DataFrame, answers_df: pd.DataFrame, lst_svod_cols:list):
    """
    Функция для обработки
    :param base_df: часть датафрейма с описательными колонками
    :param answers_df: часть датафрейма с ответами
    :param lst_svod_cols:  список с колонками по которым нужно делать свод
    """
    try:
        union_base_df = base_df.copy()  # делаем копию анкетной части чтобы потом соединить ее с ответной частью
        quantity_cols_base_df = base_df.shape[1]  # количество колонок в анкетной части

        out_answer_df = base_df.copy()  # делаем копию для последующего соединения с сырыми ответами
        if len(answers_df.columns) != 40:  # проверяем количество колонок с вопросами
            raise BadCountColumnsLTUPB

        # очищаем названия колонок от возможных сочетаний .1 которые добавляет пандас при одинаковых колонках
        clean_df_lst = []
        for name_column in answers_df.columns:
            clean_name = re.sub(r'.\d+$', '', name_column)
            clean_df_lst.append(clean_name)

        answers_df.columns = clean_df_lst

        # Проверяем наличие колонок Пол
        diff_req_cols = {'Пол', 'Возраст'}.difference(set(base_df.columns))
        if len(diff_req_cols) != 0:
            raise NotReqColumnLTUPB

        # Проверяем на пол
        diff_sex = set(base_df['Пол'].unique()).difference({'Мужской', 'Женский'})
        if len(diff_sex) != 0:
            raise BadValueSexLTUPB

        # Проверяем на возраст
        diff_age = set(base_df['Возраст'].unique()).difference({'13-14 лет', '15-16 лет'})
        if len(diff_age) != 0:
            raise BadValueAgeLTUPB


        lst_check_cols = ['Отвечать у доски',
                          'Требуется обратиться с вопросом, просьбой к незнакомому человеку',
                          'Участвовать в соревнованиях, конкурсах, олимпиадах',
                          'Слышать заклятия',
                          'Разговаривать с директором школы',
                          'Сравнивать себя с другими',
                          'Учитель делает тебе замечание',
                          'Тебя критикуют, в чем-то упрекают',
                          'На тебя смотрят, когда ты что-нибудь делаешь (наблюдают за тобой во время работы, решения задачи)',
                          'Видеть плохие или «вещие» сны',

                          'Писать контрольную работу, выполнять тест по какому-нибудь предмету',
                          'После контрольной, теста учитель называет отметки',
                          'У тебя что-то не получается',
                          'Мысль о том, что неосторожным поступком можно навлечь на себя гнев потусторонних сил',
                          'На тебя не обращают внимания',
                          'Ждешь родителей с родительского собрания',
                          'Тебе грозит неуспех, провал',
                          'Слышать смех за своей спиной',
                          'Не понимать объяснений учителя',
                          'Думаешь о своем будущем',

                          'Слышать предсказания о космических катастрофах',
                          'Выступать перед большой аудиторией',
                          'Слышать, что какой-то человек «напускает порчу» на других',
                          'Ссориться с родителями',
                          'Участвовать в психологическом эксперименте',
                          'На тебя смотрят как на маленького',
                          'На экзамене тебе достался 13-й билет',
                          'На уроке учитель неожиданно задает тебе вопрос',
                          'Думаешь о своей привлекательности для девочек (мальчиков)',
                          'Не можешь справиться с домашним заданием',

                          'Оказаться в темноте, видеть неясные силуэты, слышать непонятные шорохи',
                          'Не соглашаешься с родителями',
                          'Берешься за новое дело',
                          'Разговаривать со школьным психологом',
                          'Думать о том, что тебя могут «сглазить»',
                          'Замолчали, когда ты подошел (подошла)',
                          'Общаться с человеком, похожим на мага, экстрасенса',
                          'Слушать, как кто-то говорит о своих любовных похождениях',
                          'Смотреться в зеркало',
                          'Кажется, что нечто непонятное, сверхъестественное может помешать тебе добиться желаемого'

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
            raise BadOrderLTUPB

        # словарь для замены слов на числа
        dct_replace_value = {'нет': 0,
                             'немного': 1,
                             'достаточно': 2,
                             'значительно': 3,
                             'очень': 4,
                             }
        valid_values = [0, 1, 2, 3,4]
        answers_df.replace(dct_replace_value, inplace=True)  # заменяем слова на цифры для подсчетов
        # Проверяем, есть ли значения, отличающиеся от указанных в списке
        lst_error_answers = []  # список для хранения строк где найдены неправильные ответы

        for i in range(40):
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
            raise BadValueLTUPB
        # Общая тревожность
        base_df['ОТ_Сырое'] = answers_df.sum(axis=1)
        base_df['ОТ_Стен'] = base_df[['Пол','Возраст','ОТ_Сырое']].apply(calc_ot_sten,axis=1)
        base_df['ОТ_Уровень'] = base_df['ОТ_Стен'].apply(calc_range)

        base_df['ШТ_Сырое'] = answers_df.apply(calc_sht_value,axis=1)
        base_df['ШТ_Стен'] = base_df[['Пол','Возраст','ШТ_Сырое']].apply(calc_sht_sten,axis=1)
        base_df['ШТ_Уровень'] = base_df['ШТ_Стен'].apply(calc_range)

        base_df['СТ_Сырое'] = answers_df.apply(calc_st_value,axis=1)
        base_df['СТ_Стен'] = base_df[['Пол','Возраст','СТ_Сырое']].apply(calc_st_sten,axis=1)
        base_df['СТ_Уровень'] = base_df['СТ_Стен'].apply(calc_range)

        base_df['МТ_Сырое'] = answers_df.apply(calc_mt_value,axis=1)
        base_df['МТ_Стен'] = base_df[['Пол','Возраст','МТ_Сырое']].apply(calc_mt_sten,axis=1)
        base_df['МТ_Уровень'] = base_df['МТ_Стен'].apply(calc_range)

        base_df['МАГТ_Сырое'] = answers_df.apply(calc_magt_value,axis=1)
        base_df['МАГТ_Стен'] = base_df[['Пол','Возраст','МАГТ_Сырое']].apply(calc_magt_sten,axis=1)
        base_df['МАГТ_Уровень'] = base_df['МАГТ_Стен'].apply(calc_range)

        # Упорядочиваем
        result_df = base_df.iloc[:, quantity_cols_base_df:]  # отсекаем часть с результатами чтобы упорядочить
        lst_stens = [column for column in result_df.columns if 'Стен' in column]
        result_df['Итоговые_стены'] = result_df[lst_stens].apply(create_itog_stens, axis=1)

        new_order_lst = ['Итоговые_стены',
                         'ОТ_Стен', 'ШТ_Стен', 'СТ_Стен', 'МТ_Стен', 'МАГТ_Стен',

                         'ОТ_Уровень', 'ШТ_Уровень', 'СТ_Уровень', 'МТ_Уровень', 'МАГТ_Уровень',

                         'ОТ_Сырое', 'ШТ_Сырое', 'СТ_Сырое', 'МТ_Сырое', 'МАГТ_Сырое'
                         ]
        result_df = result_df.reindex(columns=new_order_lst)  # изменяем порядок
        base_df = pd.concat([union_base_df, result_df], axis=1)  # соединяем и перезаписываем base_df

        # Создаем датафрейм для создания части в общий датафрейм
        part_df = pd.DataFrame()
        # Стены
        part_df['ШЛТУПБ_Итоговые_стены'] = base_df['Итоговые_стены']
        part_df['ШЛТУПБ_ОТ_Стен'] = base_df['ОТ_Стен']
        part_df['ШЛТУПБ_ШТ_Стен'] = base_df['ШТ_Стен']
        part_df['ШЛТУПБ_СТ_Стен'] = base_df['СТ_Стен']
        part_df['ШЛТУПБ_МТ_Стен'] = base_df['МТ_Стен']
        part_df['ШЛТУПБ_МАГТ_Стен'] = base_df['МАГТ_Стен']

        part_df['ШЛТУПБ_ОТ_Уровень'] = base_df['ОТ_Уровень']
        part_df['ШЛТУПБ_ШТ_Уровень'] = base_df['ШТ_Уровень']
        part_df['ШЛТУПБ_СТ_Уровень'] = base_df['СТ_Уровень']
        part_df['ШЛТУПБ_МТ_Уровень'] = base_df['МТ_Уровень']
        part_df['ШЛТУПБ_МАГТ_Уровень'] = base_df['МАГТ_Уровень']

        part_df['ШЛТУПБ_ОТ_Сырое'] = base_df['ОТ_Сырое']
        part_df['ШЛТУПБ_ШТ_Сырое'] = base_df['ШТ_Сырое']
        part_df['ШЛТУПБ_СТ_Сырое'] = base_df['СТ_Сырое']
        part_df['ШЛТУПБ_МТ_Сырое'] = base_df['МТ_Сырое']
        part_df['ШЛТУПБ_МАГТ_Сырое'] = base_df['МАГТ_Сырое']

        out_answer_df = pd.concat([out_answer_df, answers_df], axis=1)  # Датафрейм для проверки
        base_df.sort_values(by='ОТ_Сырое', ascending=False, inplace=True)  # сортируем

        # формируем основной словарь
        out_dct = {'Списочный результат': base_df, 'Список для проверки': out_answer_df,
                   }

        # Делаем свод по шкалам
        dct_svod_integral = {'ОТ_Стен': 'ОТ_Уровень',
                             'ШТ_Стен': 'ШТ_Уровень',
                             'СТ_Стен': 'СТ_Уровень',
                             'МТ_Стен': 'МТ_Уровень',
                             'МАГТ_Стен': 'МАГТ_Уровень',

                             }

        dct_rename_svod_integral = {'ОТ_Стен': 'Общая тревожность',
                                    'ШТ_Стен': 'Школьная тревожность',
                                    'СТ_Стен': 'Самооценочная тревожность',
                                    'МТ_Стен': 'Межличностная тревожность',
                                    'МАГТ_Стен': 'Магическая тревожность',
                                    }

        lst_integral = ['тревожность отсутствует','нормальный уровень','несколько повышенная тревожность','явно повышенная тревожность','очень высокая тревожность']
        base_svod_integral_df = create_union_svod(base_df, dct_svod_integral, dct_rename_svod_integral, lst_integral)

        # Считаем среднее по шкалам
        avg_a = round(base_df['ОТ_Стен'].mean(), 2)
        avg_b = round(base_df['ШТ_Стен'].mean(), 2)
        avg_c = round(base_df['СТ_Стен'].mean(), 2)
        avg_so = round(base_df['МТ_Стен'].mean(), 2)
        avg_d = round(base_df['МАГТ_Стен'].mean(), 2)

        avg_dct = {'Среднее значение стена Общая тревожность': avg_a,
                   'Среднее значение стена шкалы Школьная тревожность': avg_b,
                   'Среднее значение стена шкалы Самооценочная тревожность': avg_c,
                   'Среднее значение стена шкалы Межличностная тревожность': avg_so,
                   'Среднее значение стена Магическая тревожность': avg_d,

                   }

        avg_df = pd.DataFrame.from_dict(avg_dct, orient='index')
        avg_df = avg_df.reset_index()
        avg_df.columns = ['Показатель', 'Среднее значение']

        out_dct.update({'Свод Шкалы': base_svod_integral_df,
                        'Среднее': avg_df}
                       )

        dct_prefix = {'ОТ_Уровень': 'ОТ',
                      'ШТ_Уровень': 'ШТ',
                      'СТ_Уровень': 'СТ',
                      'МТ_Уровень': 'МТ',
                      'МАГТ_Уровень': 'МАГТ',
                      }

        out_dct = create_list_on_level_ltu_prih(base_df, out_dct, lst_integral, dct_prefix)

        """
            Сохраняем в зависимости от необходимости делать своды по определенным колонкам
            """
        if len(lst_svod_cols) == 0:
            return out_dct, part_df
        else:
            out_dct = create_result_ltu_prih(base_df, out_dct, lst_svod_cols)

            return out_dct, part_df


    except NotReqColumnLTUPB:
        messagebox.showerror('Лахеcис',
                             f'При обработке вопросов теста Шкала личностной тревожности учащихся А. М. Прихожан Форма Б обнаружено отсутствие обязательных колонок:\n'
                             f'{diff_req_cols}\n В таблице с ответами обязательно должны быть колонки с названием Пол и Возраст'
                             f'Используйте при создании Яндекс-формы написание вопросов из руководства пользователя программы Лахесис.')
    except BadValueSexLTUPB:
        messagebox.showerror('Лахеcис',
                             f'При обработке вопросов теста Шкала личностной тревожности учащихся А. М. Прихожан Форма Б в колонке Пол обнаружены значения отличающиеся от допустимых:\n'
                             f'{diff_sex}\n В колонке Пол допустимы только значения Мужской и Женский.'
                             f'Используйте при создании Яндекс-формы написание вопросов из руководства пользователя программы Лахесис.')
    except BadValueAgeLTUPB:
        messagebox.showerror('Лахеcис',
                             f'При обработке вопросов теста Шкала личностной тревожности учащихся А. М. Прихожан Форма Б в колонке Возраст обнаружены значения отличающиеся от допустимых:\n'
                             f'{diff_sex}\n В колонке Возраст допустимы только значения 10-11 лет и 12 лет.'
                             f'Используйте при создании Яндекс-формы написание вопросов из руководства пользователя программы Лахесис.')

    except BadOrderLTUPB:
        messagebox.showerror('Лахеcис',
                             f'При обработке вопросов теста Шкала личностной тревожности учащихся А. М. Прихожан Форма Б обнаружены неправильные вопросы. Проверьте названия колонок с вопросами:\n'
                             f'{error_order_message[:5000]}\n'
                             f'Используйте при создании Яндекс-формы написание вопросов из руководства пользователя программы Лахесис.')
    except BadValueLTUPB:
        messagebox.showerror('Лахеcис',
                             f'При обработке вопросов теста Шкала личностной тревожности учащихся А. М. Прихожан Форма Б обнаружены неправильные варианты ответов. Проверьте ответы на указанных строках:\n'
                             f'{error_message[:5000]}\n'
                             f'Используйте при создании Яндекс-формы написание вариантов ответа из руководства пользователя программы Лахесис.')


    except BadCountColumnsLTUPB:
        messagebox.showerror('Лахеcис',
                             f'Проверьте количество колонок с ответами на тест Шкала личностной тревожности учащихся А. М. Прихожан Форма Б\n'
                             f'Должно быть 40 колонок с ответами')




