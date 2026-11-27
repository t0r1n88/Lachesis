"""
Скрипт для обработки результатов Опросник самоотношения Столин Пантелеев
"""

import pandas as pd
import re
from tkinter import messagebox
from lachesis_support_functions import round_mean_two,calc_count_scale,create_union_svod, create_list_on_level

class BadOrderOSOSP(Exception):
    """
    Исключение для обработки случая когда колонки не совпадают
    """
    pass


class BadValueOSOSP(Exception):
    """
    Исключение для неправильных значений в вариантах ответов
    """
    pass

class BadCountColumnsOSOSP(Exception):
    """
    Исключение для обработки случая если количество колонок не равно 57
    """
    pass


def calc_value_gs(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [2, 5, 23, 33, 37, 42, 46, 48, 52, 53, 57,
              6, 9, 13, 14, 16, 18, 30, 35, 38, 39, 41, 43, 44, 45, 49, 50, 56]
    lst_neg = [6, 9, 13, 14, 16, 18, 30, 35, 38, 39, 41, 43, 44, 45, 49, 50, 56]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_pr:
            if idx not in lst_neg:
                if value == 'да':
                    value_forward += 1
            else:
                if value == 'нет':
                    value_forward += 1
    return value_forward


def calc_percent_gs(value):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """
    result = 0

    if value == 0:
        result = 0
    elif value == 1:
        result = 0.67
    elif value ==2:
        result =3.00
    elif value ==3:
        result =5.33
    elif value ==4:
        result =6.33
    elif value ==5:
        result =9.00
    elif value ==6:
        result =13.00
    elif value ==7:
        result =16.00
    elif value ==8:
        result =21.33
    elif value ==9:
        result =26.67
    elif value ==10:
        result =32.33
    elif value ==11:
        result =38.33
    elif value ==12:
        result =49.00
    elif value ==13:
        result =55.33
    elif value ==14:
        result =62.67
    elif value ==15:
        result =69.33
    elif value ==16:
        result =74.33
    elif value ==17:
        result =80.00
    elif value ==18:
        result =85.00
    elif value ==19:
        result =88.00
    elif value ==20:
        result =90.67
    elif value ==21:
        result =93.33
    elif value ==22:
        result =96.00
    elif value ==23:
        result =96.67
    elif value ==24:
        result =98.00
    elif value ==25:
        result =98.33
    elif value ==26:
        result =98.67
    elif value ==27:
        result =99.67
    elif value ==28:
        result =100


    return round(result)

def calc_level(value):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """

    if value <= 49:
        return f'признак не выражен'
    elif 50 <= value <= 74:
        return f'признак выражен'
    else:
        return f'признак ярко выражен'


def calc_value_su(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [2, 23, 53, 57,
              8, 13, 25, 27, 31, 35, 38, 39, 40, 41, 50]
    lst_neg = [8, 13, 25, 27, 31, 35, 38, 39, 40, 41, 50]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_pr:
            if idx not in lst_neg:
                if value == 'да':
                    value_forward += 1
            else:
                if value == 'нет':
                    value_forward += 1
    return value_forward

def calc_percent_su(value):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """

    if value == 0:
        result = 1.67
    elif value == 1:
        result =4.00
    elif value ==2:
        result =6.00
    elif value ==3:
        result =9.33
    elif value ==4:
        result =16.00
    elif value ==5:
        result =25.33
    elif value ==6:
        result =34.00
    elif value ==7:
        result =44.67
    elif value == 8:
        result =58.67
    elif value ==9:
        result =71.33
    elif value ==10:
        result =80.00
    elif value ==11:
        result =86.67
    elif value ==12:
        result =91.33
    elif value ==13:
        result =63.67
    elif value ==14:
        result =99.67
    else:
        result =100

    return round(result)


def calc_value_as(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [12, 18, 28, 29, 37, 46, 48, 54,
              4, 9, 11, 16, 19, 24, 45, 56]
    lst_neg = [4, 9, 11, 16, 19, 24, 45, 56]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_pr:
            if idx not in lst_neg:
                if value == 'да':
                    value_forward += 1
            else:
                if value == 'нет':
                    value_forward += 1
    return value_forward

def calc_percent_as(value):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """

    if value == 0:
        result =0.33
    elif value == 1:
        result =3.67
    elif value ==2:
        result =9.00
    elif value ==3:
        result =16.00
    elif value ==4:
        result =21.67
    elif value ==5:
        result =28.00
    elif value ==6:
        result =37.33
    elif value ==7:
        result =47.00
    elif value ==8:
        result =58.33
    elif value ==9:
        result =69.67
    elif value ==10:
        result =77.33
    elif value ==11:
        result =86.00
    elif value ==12:
        result =90.67
    elif value ==13:
        result =96.67
    elif value ==14:
        result =98.33
    elif value ==15:
        result =99.67
    else:
        result =100

    return round(result)


def calc_value_ood(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [1, 5, 10, 15, 42, 55,
              3, 26, 30, 32, 43, 44, 49]
    lst_neg = [3, 26, 30, 32, 43, 44, 49]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_pr:
            if idx not in lst_neg:
                if value == 'да':
                    value_forward += 1
            else:
                if value == 'нет':
                    value_forward += 1
    return value_forward


def calc_percent_ood(value):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """

    if value == 0:
        result =0
    elif value == 1:
        result =0
    elif value ==2:
        result =0.67
    elif value ==3:
        result =1.00
    elif value ==4:
        result =3.33
    elif value ==5:
        result =6.00
    elif value ==6:
        result =9.00
    elif value ==7:
        result =17.67
    elif value ==8:
        result =27.33
    elif value ==9:
        result =39.67
    elif value ==10:
        result =53.00
    elif value ==11:
        result =72.33
    elif value ==12:
        result =91.33
    else:
        result =100

    return round(result)


def calc_value_si(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [7, 17, 20, 33, 34, 52,
              14, 51]
    lst_neg = [14, 51]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_pr:
            if idx not in lst_neg:
                if value == 'да':
                    value_forward += 1
            else:
                if value == 'нет':
                    value_forward += 1
    return value_forward

def calc_percent_si(value):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """

    if value == 0:
        result =0.67
    elif value == 1:
        result =2.00
    elif value ==2:
        result =5.33
    elif value ==3:
        result =16.00
    elif value ==4:
        result =29.00
    elif value ==5:
        result =49.67
    elif value ==6:
        result =71.33
    elif value ==7:
        result =92.33
    else:
        result =100

    return round(result)


def calc_value_usuv(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [2, 23, 37, 42, 46,
              38, 39, 41]
    lst_neg = [38, 39, 41]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_pr:
            if idx not in lst_neg:
                if value == 'да':
                    value_forward += 1
            else:
                if value == 'нет':
                    value_forward += 1
    return value_forward

def calc_percent_usuv(value):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """

    if value == 0:
        result =3.77
    elif value == 1:
        result =7.33
    elif value ==2:
        result =16.67
    elif value ==3:
        result =29.33
    elif value ==4:
        result =49.67
    elif value ==5:
        result =65.67
    elif value ==6:
        result =81.33
    elif value ==7:
        result =92.33
    else:
        result =100

    return round(result)


def calc_value_uod(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [ 1, 5, 10, 52, 55,
               32, 43,44]
    lst_neg = [32, 43, 44]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_pr:
            if idx not in lst_neg:
                if value == 'да':
                    value_forward += 1
            else:
                if value == 'нет':
                    value_forward += 1
    return value_forward


def calc_percent_uod(value):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """

    if value == 0:
        result =0
    elif value == 1:
        result =0.67
    elif value ==2:
        result =3.67
    elif value ==3:
        result =7.33
    elif value ==4:
        result =15.00
    elif value ==5:
        result =32.00
    elif value ==6:
        result =51.33
    elif value ==7:
        result =80.00
    else:
        result =100

    return round(result)

def calc_value_usp(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [12, 18, 28, 47, 48, 54,
              21]
    lst_neg = [21]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_pr:
            if idx not in lst_neg:
                if value == 'да':
                    value_forward += 1
            else:
                if value == 'нет':
                    value_forward += 1
    return value_forward

def calc_percent_usp(value):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """

    if value == 0:
        result =2.67
    elif value == 1:
        result =7.67
    elif value ==2:
        result =16.67
    elif value ==3:
        result =34.33
    elif value ==4:
        result =50.67
    elif value ==5:
        result =70.67
    elif value ==6:
        result =89.67
    else:
        result =100

    return round(result)



def calc_value_usr(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [50, 57,
              25, 27, 31, 35, 36]
    lst_neg = [25, 27, 31, 35, 36]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_pr:
            if idx not in lst_neg:
                if value == 'да':
                    value_forward += 1
            else:
                if value == 'нет':
                    value_forward += 1
    return value_forward

def calc_percent_usr(value):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """

    if value == 0:
        result =3.00
    elif value == 1:
        result =9.67
    elif value ==2:
        result =25.67
    elif value ==3:
        result =38.33
    elif value ==4:
        result =60.33
    elif value ==5:
        result =79.67
    elif value ==6:
        result =92.00
    else:
        result =100

    return round(result)


def calc_value_uso(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [3, 4, 9, 11, 16, 24, 45, 56]
    lst_neg = []
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_pr:
            if idx not in lst_neg:
                if value == 'да':
                    value_forward += 1
            else:
                if value == 'нет':
                    value_forward += 1
    return value_forward


def calc_percent_uso(value):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """

    if value == 0:
        result =1.67
    elif value == 1:
        result =4.67
    elif value ==2:
        result =15.00
    elif value ==3:
        result =27.67
    elif value ==4:
        result =43.33
    elif value ==5:
        result =60.77
    elif value ==6:
        result =81.67
    elif value ==7:
        result =96.67
    else:
        result =100

    return round(result)


def calc_value_usi(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [17, 20, 33,
              26, 30, 49, 51]
    lst_neg = [26, 30, 49, 51]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_pr:
            if idx not in lst_neg:
                if value == 'да':
                    value_forward += 1
            else:
                if value == 'нет':
                    value_forward += 1
    return value_forward


def calc_percent_usi(value):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """

    if value == 0:
        result =0.67
    elif value == 1:
        result =3.00
    elif value ==2:
        result =11.33
    elif value ==3:
        result =20.00
    elif value ==4:
        result =34.33
    elif value ==5:
        result =54.67
    elif value ==6:
        result =80.00
    else:
        result =100

    return round(result)


def calc_value_uspm(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [53,
              6, 8, 13, 15, 22, 40]
    lst_neg = [6, 8, 13, 15, 22, 40]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_pr:
            if idx not in lst_neg:
                if value == 'да':
                    value_forward += 1
            else:
                if value == 'нет':
                    value_forward += 1
    return value_forward


def calc_percent_uspm(value):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """

    if value == 0:
        result =4.33
    elif value == 1:
        result =21.33
    elif value ==2:
        result =43.33
    elif value ==3:
        result =68.67
    elif value ==4:
        result =83.67
    elif value ==5:
        result =94.00
    elif value ==6:
        result =99.33
    else:
        result =100

    return round(result)


def create_itog_stens(row):
    """
    Функция для создания строки с итоговым стеном
    :param row: строка с результатами
    :return:
    """
    lst_out = list(map(str,row))
    return '-'.join(lst_out)


def create_list_on_level_oso(base_df:pd.DataFrame, out_dct:dict, lst_level:list, dct_prefix:dict):
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
                if level == 'признак не выражен':
                    level = 'не выражен'
                elif level == 'признак выражен':
                    level = 'выражен'
                else:
                    level = 'ярко выражен'
                dct_level[f'{dct_prefix[key]}. {level}'] = temp_df
        out_dct.update(dct_level)

    return out_dct

def create_result_oso_stolin_pan(base_df:pd.DataFrame, out_dct:dict, lst_svod_cols:list):
    """
    Функция для подсчета результата если указаны колонки по которым нужно провести свод
    :param df: датафрейм с результатами
    :param out_dct: словарь с уже подсчитанными базовыми данными
    :param lst_svod_cols: список сводных колонок
    :return: словарь
    """
    lst_level = ['признак не выражен','признак выражен','признак ярко выражен']

    lst_reindex_one_level_cols = lst_svod_cols.copy()
    lst_reindex_one_level_cols.extend(['признак не выражен','признак выражен','признак ярко выражен',
                                       'Итого'])  # Основная шкала

    svod_count_one_level_gs_df = calc_count_scale(base_df, lst_svod_cols,
                                                 'ГС_Обработанное_значение_%',
                                                 'ГС_Уровень',
                                                 lst_reindex_one_level_cols, lst_level)


    # АД
    svod_count_one_level_su_df = calc_count_scale(base_df, lst_svod_cols,
                                                 'СУ_Обработанное_значение_%',
                                                 'СУ_Уровень',
                                                 lst_reindex_one_level_cols, lst_level)
    svod_count_one_level_as_df = calc_count_scale(base_df, lst_svod_cols,
                                                 'АС_Обработанное_значение_%',
                                                 'АС_Уровень',
                                                 lst_reindex_one_level_cols, lst_level)

    svod_count_one_level_ood_df = calc_count_scale(base_df, lst_svod_cols,
                                                 'ООД_Обработанное_значение_%',
                                                 'ООД_Уровень',
                                                 lst_reindex_one_level_cols, lst_level)

    svod_count_one_level_si_df = calc_count_scale(base_df, lst_svod_cols,
                                                 'СИ_Обработанное_значение_%',
                                                 'СИ_Уровень',
                                                 lst_reindex_one_level_cols, lst_level)



    svod_count_one_level_usuv_df = calc_count_scale(base_df, lst_svod_cols,
                                                 'УСУВ_Обработанное_значение_%',
                                                 'УСУВ_Уровень',
                                                 lst_reindex_one_level_cols, lst_level)
    svod_count_one_level_uod_df = calc_count_scale(base_df, lst_svod_cols,
                                                 'УОД_Обработанное_значение_%',
                                                 'УОД_Уровень',
                                                 lst_reindex_one_level_cols, lst_level)
    svod_count_one_level_usp_df = calc_count_scale(base_df, lst_svod_cols,
                                                 'УСП_Обработанное_значение_%',
                                                 'УСП_Уровень',
                                                 lst_reindex_one_level_cols, lst_level)
    svod_count_one_level_usr_df = calc_count_scale(base_df, lst_svod_cols,
                                                 'УСР_Обработанное_значение_%',
                                                 'УСР_Уровень',
                                                 lst_reindex_one_level_cols, lst_level)
    svod_count_one_level_uso_df = calc_count_scale(base_df, lst_svod_cols,
                                                 'УСО_Обработанное_значение_%',
                                                 'УСО_Уровень',
                                                 lst_reindex_one_level_cols, lst_level)
    svod_count_one_level_usi_df = calc_count_scale(base_df, lst_svod_cols,
                                                 'УСИ_Обработанное_значение_%',
                                                 'УСИ_Уровень',
                                                 lst_reindex_one_level_cols, lst_level)
    svod_count_one_level_uspm_df = calc_count_scale(base_df, lst_svod_cols,
                                                 'УСПМ_Обработанное_значение_%',
                                                 'УСПМ_Уровень',
                                                 lst_reindex_one_level_cols, lst_level)

    # Считаем среднее по субшкалам
    svod_mean_one_df = pd.pivot_table(base_df,
                                      index=lst_svod_cols,
                                      values=['ГС_Обработанное_значение_%',
                            'СУ_Обработанное_значение_%',
                            'АС_Обработанное_значение_%',
                            'ООД_Обработанное_значение_%',
                            'СИ_Обработанное_значение_%',

                            'УСУВ_Обработанное_значение_%',
                            'УОД_Обработанное_значение_%',
                            'УСП_Обработанное_значение_%',
                            'УСР_Обработанное_значение_%',
                            'УСО_Обработанное_значение_%',
                            'УСИ_Обработанное_значение_%',
                            'УСПМ_Обработанное_значение_%',
                                              ],
                                      aggfunc=round_mean_two)
    svod_mean_one_df.reset_index(inplace=True)

    # упорядочиваем колонки
    new_order_cols = lst_svod_cols.copy()
    new_order_cols.extend((['ГС_Обработанное_значение_%',
                            'СУ_Обработанное_значение_%',
                            'АС_Обработанное_значение_%',
                            'ООД_Обработанное_значение_%',
                            'СИ_Обработанное_значение_%',

                            'УСУВ_Обработанное_значение_%',
                            'УОД_Обработанное_значение_%',
                            'УСП_Обработанное_значение_%',
                            'УСР_Обработанное_значение_%',
                            'УСО_Обработанное_значение_%',
                            'УСИ_Обработанное_значение_%',
                            'УСПМ_Обработанное_значение_%',
                            ]))
    svod_mean_one_df = svod_mean_one_df.reindex(columns=new_order_cols)

    dct_rename_cols_mean = {'ГС_Обработанное_значение_%': 'Ср. Глобальное самоотношение',
                            'СУ_Обработанное_значение_%': 'Ср. Шкала Самоуважение',
                            'АС_Обработанное_значение_%': 'Ср. Шкала Аутосимпатия',
                            'ООД_Обработанное_значение_%': 'Ср. Шкала Ожидаемое отношение от других',
                            'СИ_Обработанное_значение_%': 'Ср. Шкала Самоинтерес',

                            'УСУВ_Обработанное_значение_%': 'Ср. У Самоуверенность',
                            'УОД_Обработанное_значение_%': 'Ср. У Отношение других',
                            'УСП_Обработанное_значение_%': 'Ср. У Самопринятие',
                            'УСР_Обработанное_значение_%': 'Ср. У Саморуководство',
                            'УСО_Обработанное_значение_%': 'Ср. У Самообвинение',
                            'УСИ_Обработанное_значение_%': 'Ср. У Самоинтерес',
                            'УСПМ_Обработанное_значение_%': 'Ср. У Самопонимание',
                            }
    svod_mean_one_df.rename(columns=dct_rename_cols_mean, inplace=True)

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
                    f'ГС {out_name}': svod_count_one_level_gs_df,

                    f'СУ {out_name}': svod_count_one_level_su_df,
                    f'АС {out_name}': svod_count_one_level_as_df,
                    f'ООД {out_name}': svod_count_one_level_ood_df,
                    f'СИ {out_name}': svod_count_one_level_si_df,

                    f'УСУВ {out_name}': svod_count_one_level_usuv_df,
                    f'УОД {out_name}': svod_count_one_level_uod_df,
                    f'УСП {out_name}': svod_count_one_level_usp_df,
                    f'УСР {out_name}': svod_count_one_level_usr_df,
                    f'УСО {out_name}': svod_count_one_level_uso_df,
                    f'УСИ {out_name}': svod_count_one_level_usi_df,
                    f'УСПМ {out_name}': svod_count_one_level_uspm_df,
                    })

    if len(lst_svod_cols) == 1:
        return out_dct

    else:
        for idx, name_column in enumerate(lst_svod_cols):
            lst_reindex_column_level_cols = [lst_svod_cols[idx], 'признак не выражен','признак выражен','признак ярко выражен',
                                               'Итого']

            svod_count_column_level_gs_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                             'ГС_Обработанное_значение_%',
                                                             'ГС_Уровень',
                                                             lst_reindex_column_level_cols, lst_level)

            # АД
            svod_count_column_level_su_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                             'СУ_Обработанное_значение_%',
                                                             'СУ_Уровень',
                                                             lst_reindex_column_level_cols, lst_level)
            svod_count_column_level_as_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                             'АС_Обработанное_значение_%',
                                                             'АС_Уровень',
                                                             lst_reindex_column_level_cols, lst_level)

            svod_count_column_level_ood_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                              'ООД_Обработанное_значение_%',
                                                              'ООД_Уровень',
                                                              lst_reindex_column_level_cols, lst_level)

            svod_count_column_level_si_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                             'СИ_Обработанное_значение_%',
                                                             'СИ_Уровень',
                                                             lst_reindex_column_level_cols, lst_level)

            svod_count_column_level_usuv_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                               'УСУВ_Обработанное_значение_%',
                                                               'УСУВ_Уровень',
                                                               lst_reindex_column_level_cols, lst_level)
            svod_count_column_level_uod_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                              'УОД_Обработанное_значение_%',
                                                              'УОД_Уровень',
                                                              lst_reindex_column_level_cols, lst_level)
            svod_count_column_level_usp_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                              'УСП_Обработанное_значение_%',
                                                              'УСП_Уровень',
                                                              lst_reindex_column_level_cols, lst_level)
            svod_count_column_level_usr_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                              'УСР_Обработанное_значение_%',
                                                              'УСР_Уровень',
                                                              lst_reindex_column_level_cols, lst_level)
            svod_count_column_level_uso_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                              'УСО_Обработанное_значение_%',
                                                              'УСО_Уровень',
                                                              lst_reindex_column_level_cols, lst_level)
            svod_count_column_level_usi_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                              'УСИ_Обработанное_значение_%',
                                                              'УСИ_Уровень',
                                                              lst_reindex_column_level_cols, lst_level)
            svod_count_column_level_uspm_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                               'УСПМ_Обработанное_значение_%',
                                                               'УСПМ_Уровень',
                                                               lst_reindex_column_level_cols, lst_level)

            # Считаем среднее по субшкалам
            svod_mean_column_df = pd.pivot_table(base_df,
                                                 index=[lst_svod_cols[idx]],
                                                 values=['ГС_Обработанное_значение_%',
                                                         'СУ_Обработанное_значение_%',
                                                         'АС_Обработанное_значение_%',
                                                         'ООД_Обработанное_значение_%',
                                                         'СИ_Обработанное_значение_%',

                                                         'УСУВ_Обработанное_значение_%',
                                                         'УОД_Обработанное_значение_%',
                                                         'УСП_Обработанное_значение_%',
                                                         'УСР_Обработанное_значение_%',
                                                         'УСО_Обработанное_значение_%',
                                                         'УСИ_Обработанное_значение_%',
                                                         'УСПМ_Обработанное_значение_%',
                                                         ],
                                                 aggfunc=round_mean_two)
            svod_mean_column_df.reset_index(inplace=True)

            # упорядочиваем колонки
            new_order_cols = [lst_svod_cols[idx]].copy()
            new_order_cols.extend((['ГС_Обработанное_значение_%',
                                    'СУ_Обработанное_значение_%',
                                    'АС_Обработанное_значение_%',
                                    'ООД_Обработанное_значение_%',
                                    'СИ_Обработанное_значение_%',

                                    'УСУВ_Обработанное_значение_%',
                                    'УОД_Обработанное_значение_%',
                                    'УСП_Обработанное_значение_%',
                                    'УСР_Обработанное_значение_%',
                                    'УСО_Обработанное_значение_%',
                                    'УСИ_Обработанное_значение_%',
                                    'УСПМ_Обработанное_значение_%',
                                    ]))
            svod_mean_column_df = svod_mean_column_df.reindex(columns=new_order_cols)

            dct_rename_cols_mean = {'ГС_Обработанное_значение_%': 'Ср. Глобальное самоотношение',
                                    'СУ_Обработанное_значение_%': 'Ср. Шкала Самоуважение',
                                    'АС_Обработанное_значение_%': 'Ср. Шкала Аутосимпатия',
                                    'ООД_Обработанное_значение_%': 'Ср. Шкала Ожидаемое отношение от других',
                                    'СИ_Обработанное_значение_%': 'Ср. Шкала Самоинтерес',

                                    'УСУВ_Обработанное_значение_%': 'Ср. У Самоуверенность',
                                    'УОД_Обработанное_значение_%': 'Ср. У Отношение других',
                                    'УСП_Обработанное_значение_%': 'Ср. У Самопринятие',
                                    'УСР_Обработанное_значение_%': 'Ср. У Саморуководство',
                                    'УСО_Обработанное_значение_%': 'Ср. У Самообвинение',
                                    'УСИ_Обработанное_значение_%': 'Ср. У Самоинтерес',
                                    'УСПМ_Обработанное_значение_%': 'Ср. У Самопонимание',
                                    }
            svod_mean_column_df.rename(columns=dct_rename_cols_mean, inplace=True)

            # Готовим наименование
            name_column = lst_svod_cols[idx]
            name_column = re.sub(r'[\[\]\'+()<> :"?*|\\/]', '_', name_column)
            name_column = name_column[:15]

            out_dct.update({f'Ср {name_column}': svod_mean_column_df,
                            f'ГС {name_column}': svod_count_column_level_gs_df,

                            f'СУ {name_column}': svod_count_column_level_su_df,
                            f'АС {name_column}': svod_count_column_level_as_df,
                            f'ООД {name_column}': svod_count_column_level_ood_df,
                            f'СИ {name_column}': svod_count_column_level_si_df,

                            f'УСУВ {name_column}': svod_count_column_level_usuv_df,
                            f'УОД {name_column}': svod_count_column_level_uod_df,
                            f'УСП {name_column}': svod_count_column_level_usp_df,
                            f'УСР {name_column}': svod_count_column_level_usr_df,
                            f'УСО {name_column}': svod_count_column_level_uso_df,
                            f'УСИ {name_column}': svod_count_column_level_usi_df,
                            f'УСПМ {name_column}': svod_count_column_level_uspm_df,
                            })
        return out_dct






def processing_oso_stolin_pan(base_df: pd.DataFrame, answers_df: pd.DataFrame, lst_svod_cols:list):
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
        if len(answers_df.columns) != 57:  # проверяем количество колонок с вопросами
            raise BadCountColumnsOSOSP

        # очищаем названия колонок от возможных сочетаний .1 которые добавляет пандас при одинаковых колонках
        clean_df_lst = []
        for name_column in answers_df.columns:
            clean_name = re.sub(r'.\d+$', '', name_column)
            clean_df_lst.append(clean_name)

        answers_df.columns = clean_df_lst

        lst_check_cols = ['Думаю, что большинство моих знакомых относится ко мне с симпатией',
                          'Мои слова не так уж часто расходятся с делом',
                          'Думаю, что многие видят во мне что-то сходное с собой',
                          'Когда я пытаюсь себя оценить, я прежде всего вижу свои недостатки',
                          'Думаю, что как личность я вполне могу быть притягательным для других',
                          'Когда я вижу себя глазами любящего меня человека, меня неприятно поражает то, насколько мой образ далек от действительности',
                          'Мое «Я» всегда мне интересно',
                          'Я считаю, что иногда не грех пожалеть самого себя',
                          'В моей жизни есть или, по крайней мере, были люди, с которыми я был чрезвычайно близок',
                          'Собственное уважение мне еще надо заслужить',

                          'Бывало, и не раз, что я сам себя остро ненавидел',
                          'Я вполне доверяю своим внезапно возникшим желаниям',
                          'Я сам хотел во многом себя переделать',
                          'Мое собственное «Я» не представляется мне чем-то достойным глубокого внимания',
                          'Я искренне хочу, чтобы у меня было все хорошо в жизни',
                          'Если я и отношусь к кому-нибудь с укоризной, то прежде всего к самому себе',
                          'Случайному знакомому я скорее всего покажусь человеком приятным',
                          'Чаще всего я одобряю свои планы и поступки',
                          'Собственные слабости вызывают у меня что-то наподобие презрения',
                          'Если бы я раздвоился, то мне было бы довольно интересно общаться со своим двойником',

                          'Некоторые свои качества я ощущаю как посторонние, чужие мне',
                          'Вряд ли кто-либо сможет почувствовать свое сходство со мной',
                          'У меня достаточно способностей и энергии воплотить в жизнь задуманное',
                          'Часто я не без издевки подшучиваю над собой',
                          'Самое разумное, что может сделать человек в своей жизни — это подчиниться собственной судьбе',
                          'Посторонний человек, на первый взгляд, найдет во мне много отталкивающего',
                          'К сожалению, если я и сказал что-то, это не значит, что именно так и буду поступать',
                          'Свое отношение к самому себе можно назвать дружеским',
                          'Быть снисходительным к собственным слабостям вполне естественно',
                          'У меня не получается быть для любимого человека интересным длительное время',

                          'В глубине души я бы хотел, чтобы со мной произошло что-то катастрофическое',
                          'Вряд ли я вызываю симпатию у большинства моих знакомых',
                          'Мне бывает очень приятно увидеть себя глазами любящего меня человека',
                          'Когда у меня возникает какое-либо желание, я прежде всего спрашиваю себя, разумно ли это',
                          'Иногда мне кажется, что, если бы какой-то мудрый человек смог увидеть меня насквозь, он бы тут же понял, какое я ничтожество',
                          'Временами я сам собой восхищаюсь',
                          'Можно сказать, что я ценю себя достаточно высоко',
                          'В глубине души я никак не могу поверить, что я действительно взрослый человек',
                          'Без посторонней помощи я мало что могу сделать',
                          'Иногда я сам себя плохо понимаю',

                          'Мне очень мешает недостаток энергии, воли и целеустремленности',
                          'Думаю, что другие в целом оценивают меня достаточно высоко',
                          'В моей личности есть, наверное, что-то такое, что способно вызывать у других неприязнь',
                          'Большинство моих знакомых не принимают меня уж так всерьез',
                          'Сам у себя я довольно часто вызываю чувство раздражения',
                          'Я вполне могу сказать, что унижаю себя сам',
                          'Даже мои негативные черты не кажутся мне чужими',
                          'В целом, меня устраивает то, какой я есть',
                          'Вряд ли меня можно любить по-настоящему',
                          'Моим мечтам и планам не хватает реалистичности',

                          'Если бы мое второе «Я» существовало, то для меня это был бы самый скучный партнер по общению',
                          'Думаю, что мог бы найти общий язык с любым разумным и знающим человеком',
                          'То, что во мне происходит, как правило, мне понятно',
                          'Мои достоинства вполне перевешивают мои недостатки',
                          'Вряд ли найдется много людей, которые обвинят меня в отсутствии совести',
                          'Когда со мной случаются неприятности, как правило, я говорю: «И поделом тебе»',
                          'Я могу сказать, что в целом я контролирую свою судьбу'
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
            raise BadOrderOSOSP

        valid_values = ['да','нет']

        # Проверяем, есть ли значения, отличающиеся от указанных в списке
        lst_error_answers = []  # список для хранения строк где найдены неправильные ответы

        for i in range(57):
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
            raise BadValueOSOSP

        base_df['ГС_Сырое_Значение'] = answers_df.apply(calc_value_gs, axis=1)
        base_df['ГС_Обработанное_значение_%'] = base_df['ГС_Сырое_Значение'].apply(calc_percent_gs)
        base_df['ГС_Уровень'] = base_df['ГС_Обработанное_значение_%'].apply(calc_level)

        base_df['СУ_Сырое_Значение'] = answers_df.apply(calc_value_su, axis=1)
        base_df['СУ_Обработанное_значение_%'] = base_df['СУ_Сырое_Значение'].apply(calc_percent_su)
        base_df['СУ_Уровень'] = base_df['СУ_Обработанное_значение_%'].apply(calc_level)

        base_df['АС_Сырое_Значение'] = answers_df.apply(calc_value_as, axis=1)
        base_df['АС_Обработанное_значение_%'] = base_df['АС_Сырое_Значение'].apply(calc_percent_as)
        base_df['АС_Уровень'] = base_df['АС_Обработанное_значение_%'].apply(calc_level)

        base_df['ООД_Сырое_Значение'] = answers_df.apply(calc_value_ood, axis=1)
        base_df['ООД_Обработанное_значение_%'] = base_df['ООД_Сырое_Значение'].apply(calc_percent_ood)
        base_df['ООД_Уровень'] = base_df['ООД_Обработанное_значение_%'].apply(calc_level)

        base_df['СИ_Сырое_Значение'] = answers_df.apply(calc_value_si, axis=1)
        base_df['СИ_Обработанное_значение_%'] = base_df['СИ_Сырое_Значение'].apply(calc_percent_si)
        base_df['СИ_Уровень'] = base_df['СИ_Обработанное_значение_%'].apply(calc_level)

        base_df['УСУВ_Сырое_Значение'] = answers_df.apply(calc_value_usuv, axis=1)
        base_df['УСУВ_Обработанное_значение_%'] = base_df['УСУВ_Сырое_Значение'].apply(calc_percent_usuv)
        base_df['УСУВ_Уровень'] = base_df['УСУВ_Обработанное_значение_%'].apply(calc_level)

        base_df['УОД_Сырое_Значение'] = answers_df.apply(calc_value_uod, axis=1)
        base_df['УОД_Обработанное_значение_%'] = base_df['УОД_Сырое_Значение'].apply(calc_percent_uod)
        base_df['УОД_Уровень'] = base_df['УОД_Обработанное_значение_%'].apply(calc_level)

        base_df['УСП_Сырое_Значение'] = answers_df.apply(calc_value_usp, axis=1)
        base_df['УСП_Обработанное_значение_%'] = base_df['УСП_Сырое_Значение'].apply(calc_percent_usp)
        base_df['УСП_Уровень'] = base_df['УСП_Обработанное_значение_%'].apply(calc_level)

        base_df['УСР_Сырое_Значение'] = answers_df.apply(calc_value_usr, axis=1)
        base_df['УСР_Обработанное_значение_%'] = base_df['УСР_Сырое_Значение'].apply(calc_percent_usr)
        base_df['УСР_Уровень'] = base_df['УСР_Обработанное_значение_%'].apply(calc_level)

        base_df['УСО_Сырое_Значение'] = answers_df.apply(calc_value_uso, axis=1)
        base_df['УСО_Обработанное_значение_%'] = base_df['УСО_Сырое_Значение'].apply(calc_percent_uso)
        base_df['УСО_Уровень'] = base_df['УСО_Обработанное_значение_%'].apply(calc_level)

        base_df['УСИ_Сырое_Значение'] = answers_df.apply(calc_value_usi, axis=1)
        base_df['УСИ_Обработанное_значение_%'] = base_df['УСИ_Сырое_Значение'].apply(calc_percent_usi)
        base_df['УСИ_Уровень'] = base_df['УСИ_Обработанное_значение_%'].apply(calc_level)

        base_df['УСПМ_Сырое_Значение'] = answers_df.apply(calc_value_uspm, axis=1)
        base_df['УСПМ_Обработанное_значение_%'] = base_df['УСПМ_Сырое_Значение'].apply(calc_percent_uspm)
        base_df['УСПМ_Уровень'] = base_df['УСПМ_Обработанное_значение_%'].apply(calc_level)

        result_df = base_df.iloc[:, quantity_cols_base_df:]  # отсекаем часть с результатами чтобы упорядочить
        lst_stens = ['ГС_Обработанное_значение_%','СУ_Обработанное_значение_%','АС_Обработанное_значение_%','ООД_Обработанное_значение_%','СИ_Обработанное_значение_%']
        result_df['Значения_главных_шкал'] = result_df[lst_stens].apply(create_itog_stens, axis=1)

        lst_sub_stens = ['УСУВ_Обработанное_значение_%','УОД_Обработанное_значение_%','УСП_Обработанное_значение_%',
                         'УСР_Обработанное_значение_%','УСО_Обработанное_значение_%','УСИ_Обработанное_значение_%','УСПМ_Обработанное_значение_%']

        result_df['Значения_У_шкал'] = result_df[lst_sub_stens].apply(create_itog_stens, axis=1)

        new_order_lst = ['Значения_главных_шкал','Значения_У_шкал',
                         'ГС_Обработанное_значение_%', 'СУ_Обработанное_значение_%', 'АС_Обработанное_значение_%', 'ООД_Обработанное_значение_%',
                         'СИ_Обработанное_значение_%',
                         'УСУВ_Обработанное_значение_%', 'УОД_Обработанное_значение_%', 'УСП_Обработанное_значение_%',
                         'УСР_Обработанное_значение_%', 'УСО_Обработанное_значение_%', 'УСИ_Обработанное_значение_%', 'УСПМ_Обработанное_значение_%',

                         'ГС_Уровень',
                         'СУ_Уровень', 'АС_Уровень', 'ООД_Уровень', 'СИ_Уровень',
                         'УСУВ_Уровень','УОД_Уровень', 'УСП_Уровень',
                         'УСР_Уровень', 'УСО_Уровень', 'УСИ_Уровень', 'УСПМ_Уровень',

                         'ГС_Сырое_Значение', 'СУ_Сырое_Значение', 'АС_Сырое_Значение', 'ООД_Сырое_Значение',
                         'СИ_Сырое_Значение',
                         'УСУВ_Сырое_Значение', 'УОД_Сырое_Значение', 'УСП_Сырое_Значение',
                         'УСР_Сырое_Значение', 'УСО_Сырое_Значение', 'УСИ_Сырое_Значение', 'УСПМ_Сырое_Значение',
                         ]
        result_df = result_df.reindex(columns=new_order_lst)  # изменяем порядок
        base_df = pd.concat([union_base_df, result_df], axis=1)  # соединяем и перезаписываем base_df


        # Создаем датафрейм для создания части в общий датафрейм
        part_df = pd.DataFrame()
        part_df['ОСОСП_Значения_главных_шкал'] = base_df['Значения_главных_шкал']
        part_df['ОСОСП_Значения_У_шкал'] = base_df['Значения_У_шкал']

        part_df['ОСОСП_ГС_Сырое_Значение'] = base_df['ГС_Сырое_Значение']
        part_df['ОСОСП_ГС_Обработанное_значение_%'] = base_df['ГС_Обработанное_значение_%']
        part_df['ОСОСП_ГС_Уровень'] = base_df['ГС_Уровень']

        part_df['ОСОСП_СУ_Сырое_Значение'] = base_df['СУ_Сырое_Значение']
        part_df['ОСОСП_СУ_Обработанное_значение_%'] = base_df['СУ_Обработанное_значение_%']
        part_df['ОСОСП_СУ_Уровень'] = base_df['СУ_Уровень']

        part_df['ОСОСП_АС_Сырое_Значение'] = base_df['АС_Сырое_Значение']
        part_df['ОСОСП_АС_Обработанное_значение_%'] = base_df['АС_Обработанное_значение_%']
        part_df['ОСОСП_АС_Уровень'] = base_df['АС_Уровень']


        part_df['ОСОСП_ООД_Сырое_Значение'] = base_df['ООД_Сырое_Значение']
        part_df['ОСОСП_ООД_Обработанное_значение_%'] = base_df['ООД_Обработанное_значение_%']
        part_df['ОСОСП_ООД_Уровень'] = base_df['ООД_Уровень']

        part_df['ОСОСП_СИ_Сырое_Значение'] = base_df['СИ_Сырое_Значение']
        part_df['ОСОСП_СИ_Обработанное_значение_%'] = base_df['СИ_Обработанное_значение_%']
        part_df['ОСОСП_СИ_Уровень'] = base_df['СИ_Уровень']


        part_df['ОСОСП_УСУВ_Сырое_Значение'] = base_df['УСУВ_Сырое_Значение']
        part_df['ОСОСП_УСУВ_Обработанное_значение_%'] = base_df['УСУВ_Обработанное_значение_%']
        part_df['ОСОСП_УСУВ_Уровень'] = base_df['УСУВ_Уровень']

        part_df['ОСОСП_УОД_Сырое_Значение'] = base_df['УОД_Сырое_Значение']
        part_df['ОСОСП_УОД_Обработанное_значение_%'] = base_df['УОД_Обработанное_значение_%']
        part_df['ОСОСП_УОД_Уровень'] = base_df['УОД_Уровень']

        part_df['ОСОСП_УСП_Сырое_Значение'] = base_df['УСП_Сырое_Значение']
        part_df['ОСОСП_УСП_Обработанное_значение_%'] = base_df['УСП_Обработанное_значение_%']
        part_df['ОСОСП_УСП_Уровень'] = base_df['УСП_Уровень']

        part_df['ОСОСП_УСР_Сырое_Значение'] = base_df['УСР_Сырое_Значение']
        part_df['ОСОСП_УСР_Обработанное_значение_%'] = base_df['УСР_Обработанное_значение_%']
        part_df['ОСОСП_УСР_Уровень'] = base_df['УСР_Уровень']

        part_df['ОСОСП_УСО_Сырое_Значение'] = base_df['УСО_Сырое_Значение']
        part_df['ОСОСП_УСО_Обработанное_значение_%'] = base_df['УСО_Обработанное_значение_%']
        part_df['ОСОСП_УСО_Уровень'] = base_df['УСО_Уровень']

        part_df['ОСОСП_УСИ_Сырое_Значение'] = base_df['УСИ_Сырое_Значение']
        part_df['ОСОСП_УСИ_Обработанное_значение_%'] = base_df['УСИ_Обработанное_значение_%']
        part_df['ОСОСП_УСИ_Уровень'] = base_df['УСИ_Уровень']

        part_df['ОСОСП_УСПМ_Сырое_Значение'] = base_df['УСПМ_Сырое_Значение']
        part_df['ОСОСП_УСПМ_Обработанное_значение_%'] = base_df['УСПМ_Обработанное_значение_%']
        part_df['ОСОСП_УСПМ_Уровень'] = base_df['УСПМ_Уровень']

        base_df.sort_values(by='ГС_Сырое_Значение', ascending=True, inplace=True)  # сортируем
        out_answer_df = pd.concat([out_answer_df, answers_df], axis=1)  # Датафрейм для проверки

        # Делаем свод  по  шкалам
        dct_svod_l = {'ГС_Сырое_Значение': 'ГС_Уровень',
                      }

        dct_rename_svod_l = {'ГС_Сырое_Значение': 'Шкала S Глобальное самоотношение',
                             }

        lst_sub = ['признак не выражен','признак выражен','признак ярко выражен']

        base_svod_l_df = create_union_svod(base_df, dct_svod_l, dct_rename_svod_l, lst_sub)

        # Делаем свод  по  шкалам
        dct_svod_sub = {'СУ_Сырое_Значение': 'СУ_Уровень',
                        'АС_Сырое_Значение': 'АС_Уровень',
                        'ООД_Сырое_Значение': 'ООД_Уровень',
                        'СИ_Сырое_Значение': 'СИ_Уровень',
                        }

        dct_rename_svod_sub = {'СУ_Сырое_Значение': 'Шкала Самоуважение',
                               'АС_Сырое_Значение': 'Шкала Аутосимпатия',
                               'ООД_Сырое_Значение': 'Шкала Ожидаемое отношение от других',
                               'СИ_Сырое_Значение': 'Шкала Самоинтерес',

                               }


        base_svod_sub_df = create_union_svod(base_df, dct_svod_sub, dct_rename_svod_sub, lst_sub)

        # Делаем свод  по  шкалам
        dct_svod_u_sub = {'УСУВ_Сырое_Значение': 'УСУВ_Уровень',
                        'УОД_Сырое_Значение': 'УОД_Уровень',
                        'УСП_Сырое_Значение': 'УСП_Уровень',
                        'УСР_Сырое_Значение': 'УСР_Уровень',

                        'УСО_Сырое_Значение': 'УСО_Уровень',
                        'УСИ_Сырое_Значение': 'УСИ_Уровень',
                        'УСПМ_Сырое_Значение': 'УСПМ_Уровень',
                        }

        dct_rename_svod_u_sub = {'УСУВ_Сырое_Значение': 'Шкала Самоуверенность',
                               'УОД_Сырое_Значение': 'Шкала Отношение других',
                               'УСП_Сырое_Значение': 'Шкала Самопринятие',
                               'УСР_Сырое_Значение': 'Шкала Cаморуководство',

                               'УСО_Сырое_Значение': 'Шкала Самообвинение',
                               'УСИ_Сырое_Значение': 'Шкала Самоинтерес',
                               'УСПМ_Сырое_Значение': 'Шкала Самопонимание',
                               }


        base_svod_u_sub_df = create_union_svod(base_df, dct_svod_u_sub, dct_rename_svod_u_sub, lst_sub)

        avg_gs = round(base_df['ГС_Обработанное_значение_%'].mean(), 2)
        avg_su = round(base_df['СУ_Обработанное_значение_%'].mean(), 2)
        avg_as = round(base_df['АС_Обработанное_значение_%'].mean(), 2)
        avg_ood = round(base_df['ООД_Обработанное_значение_%'].mean(), 2)
        avg_si = round(base_df['СИ_Обработанное_значение_%'].mean(), 2)

        avg_usuv = round(base_df['УСУВ_Обработанное_значение_%'].mean(), 2)
        avg_uod = round(base_df['УОД_Обработанное_значение_%'].mean(), 2)
        avg_usp = round(base_df['УСП_Обработанное_значение_%'].mean(), 2)
        avg_usr = round(base_df['УСР_Обработанное_значение_%'].mean(), 2)
        avg_uso = round(base_df['УСО_Обработанное_значение_%'].mean(), 2)
        avg_usi = round(base_df['УСИ_Обработанное_значение_%'].mean(), 2)
        avg_uspm = round(base_df['УСПМ_Обработанное_значение_%'].mean(), 2)

        avg_dct = {'Среднее Обработанное_значение_% Глобальное самоотношение': avg_gs,
                   'Среднее Обработанное_значение_% шкалы Самоуважение': avg_su,
                   'Среднее Обработанное_значение_% шкалы Аутосимпатия': avg_as,
                   'Среднее Обработанное_значение_% шкалы Ожидаемое отношение от других': avg_ood,
                   'Среднее Обработанное_значение_% шкалы Самоинтерес': avg_si,

                   'Среднее Обработанное_значение_% У Самоуверенность': avg_usuv,
                   'Среднее Обработанное_значение_% У Отношение других': avg_uod,
                   'Среднее Обработанное_значение_% У Самопринятие': avg_usp,
                   'Среднее Обработанное_значение_% У Саморуководство': avg_usr,
                   'Среднее Обработанное_значение_% У Самообвинение': avg_uso,
                   'Среднее Обработанное_значение_% У Самоинтерес': avg_usi,
                   'Среднее Обработанное_значение_% У Самопонимание': avg_uspm,

                   }


        avg_df = pd.DataFrame.from_dict(avg_dct, orient='index')
        avg_df = avg_df.reset_index()
        avg_df.columns = ['Показатель', 'Среднее значение']

        # формируем основной словарь
        out_dct = {'Списочный результат': base_df,
                   'Список для проверки': out_answer_df,
                   'Свод ГС': base_svod_l_df,
                   'Свод Шкалы': base_svod_sub_df,
                   'Свод У Шкалы': base_svod_u_sub_df,
                   'Среднее': avg_df,
                   }

        dct_l = {
            'ГС_Уровень': 'ГС',
        }

        out_dct = create_list_on_level_oso(base_df, out_dct, lst_sub, dct_l)

        dct_prefix = {
            'СУ_Уровень': 'СУ',
            'АС_Уровень': 'АС',
            'ООД_Уровень': 'ООД',
            'СИ_Уровень': 'СИ'
        }

        out_dct = create_list_on_level_oso(base_df, out_dct, lst_sub, dct_prefix)

        dct_u_prefix = {
            'УСУВ_Уровень': 'В',
            'УОД_Уровень': 'К',
            'УСП_Уровень': 'ПР',
            'УСР_Уровень': 'ПР',

            'УСО_Уровень': 'ПР',
            'УСИ_Уровень': 'ПР',
            'УСПМ_Уровень': 'ПР',
        }

        out_dct = create_list_on_level_oso(base_df, out_dct, lst_sub, dct_u_prefix)

        """
                        Сохраняем в зависимости от необходимости делать своды по определенным колонкам
                        """
        if len(lst_svod_cols) == 0:
            return out_dct, part_df
        else:
            out_dct = create_result_oso_stolin_pan(base_df, out_dct, lst_svod_cols)
            return out_dct, part_df


    except BadOrderOSOSP:
        messagebox.showerror('Лахеcис',
                             f'При обработке вопросов теста Опросник самоотношения Столин Пантелеев обнаружены неправильные вопросы. Проверьте названия колонок с вопросами:\n'
                             f'{error_order_message[:5000]}\n'
                             f'Используйте при создании Яндекс-формы написание вопросов из руководства пользователя программы Лахесис.')
    except BadValueOSOSP:
        messagebox.showerror('Лахеcис',
                             f'При обработке вопросов теста Опросник самоотношения Столин Пантелеев обнаружены неправильные варианты ответов. Проверьте ответы на указанных строках:\n'
                             f'{error_message[:5000]}\n'
                             f'Используйте при создании Яндекс-формы написание вариантов ответа из руководства пользователя программы Лахесис.')


    except BadCountColumnsOSOSP:
        messagebox.showerror('Лахеcис',
                             f'Проверьте количество колонок с ответами на Опросник самоотношения Столин Пантелеев\n'
                             f'Должно быть 57 колонок с ответами')











