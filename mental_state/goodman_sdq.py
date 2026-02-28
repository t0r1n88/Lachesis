"""
Скрипт для обработки результатов теста Сильные стороны и трудности SDQ Гудман Ульянина и др.
"""

import pandas as pd
import re
from tkinter import messagebox
from lachesis_support_functions import round_mean_two,calc_count_scale,create_union_svod, create_list_on_level

class BadOrderSDQGU(Exception):
    """
    Исключение для обработки случая когда колонки не совпадают
    """
    pass


class BadValueSDQGU(Exception):
    """
    Исключение для неправильных значений в вариантах ответов
    """
    pass

class BadCountColumnsSDQGU(Exception):
    """
    Исключение для обработки случая если количество колонок не равно 23
    """
    pass

class NotReqColumn(Exception):
    """
    Исключение для обработки случая когда нет обязательных колонок Пол
    """
    pass

class BadValueSex(Exception):
    """
    Исключение для обработки случая когда в колонке Пол есть значения отличающиеся от Мужской или Женский
    """
    pass

class BadValueAge(Exception):
    """
    Исключение для обработки случая когда в колонке Возраст есть значения отличающиеся от 10-13 лет и 14-17 лет
    """
    pass


def calc_value_psp(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [1,4,8,15,18]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_pr:
            value_forward += value
    return value_forward


def calc_level_sex_psp(row:pd.Series):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """
    sex,value = row

    if sex == 'Мужской':
        if 0 <= value <= 5:
            return f'отклоняющиеся'
        elif value == 6:
            return f'пограничные'
        else:
            return f'норма'
    else:
        if 0 <= value <= 4:
            return f'отклоняющиеся'
        elif 5<= value <= 6:
            return f'пограничные'
        else:
            return f'норма'

def calc_level_age_psp(row:pd.Series):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """
    age,value = row

    if age == '10-13 лет':
        if 0 <= value <= 4:
            return f'отклоняющиеся'
        elif 5<= value <= 6:
            return f'пограничные'
        else:
            return f'норма'
    else:
        if 0 <= value <= 5:
            return f'отклоняющиеся'
        elif value == 6:
            return f'пограничные'
        else:
            return f'норма'



def calc_value_ga(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [2,9,13,19,23]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_pr:
            if idx not in (19,23):
                value_forward += value
            else:
                if value == 0:
                    value_forward += 2
                elif value == 1:
                    value_forward += 1
                else:
                    value_forward += 0

    return value_forward

def calc_level_sex_ga(row:pd.Series):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """
    sex,value = row

    if sex == 'Мужской':
        if 6 <= value <= 10 :
            return f'отклоняющиеся'
        elif value == 5:
            return f'пограничные'
        else:
            return f'норма'
    else:
        if  6<= value <= 10 :
            return f'отклоняющиеся'
        elif value == 5:
            return f'пограничные'
        else:
            return f'норма'



def calc_level_age_ga(row:pd.Series):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """
    age,value = row

    if age == '10-13 лет':
        if  6<= value <=10 :
            return f'отклоняющиеся'
        elif value == 5 :
            return f'пограничные'
        else:
            return f'норма'
    else:
        if  5<= value <=10 :
            return f'отклоняющиеся'
        elif value == 4:
            return f'пограничные'
        else:
            return f'норма'


def calc_value_emo(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [3,7,11,14,22]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_pr:
            value_forward += value
    return value_forward

def calc_level_sex_emo(row:pd.Series):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """
    sex,value = row

    if sex == 'Мужской':
        if  6<= value <= 10:
            return f'отклоняющиеся'
        elif value == 5:
            return f'пограничные'
        else:
            return f'норма'
    else:
        if  8<= value <=10 :
            return f'отклоняющиеся'
        elif 6<= value <=7 :
            return f'пограничные'
        else:
            return f'норма'



def calc_level_age_emo(row:pd.Series):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """
    age,value = row

    if age == '10-13 лет':
        if  7<= value <= 10:
            return f'отклоняющиеся'
        elif value == 6:
            return f'пограничные'
        else:
            return f'норма'
    else:
        if  7<= value <=10 :
            return f'отклоняющиеся'
        elif 5<= value <= 6:
            return f'пограничные'
        else:
            return f'норма'


def calc_value_pp(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [5,10,16,20]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_pr:
            value_forward += value
    return value_forward

def calc_level_sex_pp(row:pd.Series):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """
    sex,value = row

    if sex == 'Мужской':
        if  4<= value <= 8:
            return f'отклоняющиеся'
        elif value == 3:
            return f'пограничные'
        else:
            return f'норма'
    else:
        if  4<= value <= 8:
            return f'отклоняющиеся'
        elif value == 3:
            return f'пограничные'
        else:
            return f'норма'



def calc_level_age_pp(row:pd.Series):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """
    age,value = row

    if age == '10-13 лет':
        if 4 <= value <=8 :
            return f'отклоняющиеся'
        elif value == 3 :
            return f'пограничные'
        else:
            return f'норма'
    else:
        if 3 <= value <=8 :
            return f'отклоняющиеся'
        elif value == 2:
            return f'пограничные'
        else:
            return f'норма'


def calc_value_ps(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [6,12,17,21]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_pr:
            if idx != 12:
                value_forward += value
            else:
                if value == 0:
                    value_forward += 2
                elif value == 1:
                    value_forward += 1
                else:
                    value_forward += 0
    return value_forward


def calc_level_sex_ps(row:pd.Series):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """
    sex,value = row

    if sex == 'Мужской':
        if  5<= value <=8 :
            return f'отклоняющиеся'
        elif value == 4:
            return f'пограничные'
        else:
            return f'норма'
    else:
        if  5<= value <=8 :
            return f'отклоняющиеся'
        elif value == 4:
            return f'пограничные'
        else:
            return f'норма'



def calc_level_age_ps(row:pd.Series):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """
    age,value = row

    if age == '10-13 лет':
        if  5<= value <=8 :
            return f'отклоняющиеся'
        elif value == 4:
            return f'пограничные'
        else:
            return f'норма'
    else:
        if  5<= value <= 8:
            return f'отклоняющиеся'
        elif value == 4:
            return f'пограничные'
        else:
            return f'норма'


def calc_value_ochp(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [2,3,5,6,7,9,10,11,12,13,14,16,17,19,20,21,22,23]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_pr:
            if idx not in (12,19,23):
                value_forward += value
            else:
                if value == 0:
                    value_forward += 2
                elif value == 1:
                    value_forward += 1
                else:
                    value_forward += 0
    return value_forward

def calc_level_sex_ochp(row:pd.Series):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """
    sex,value = row

    if sex == 'Мужской':
        if  19<= value <=36 :
            return f'отклоняющиеся'
        elif 15<= value <= 18 :
            return f'пограничные'
        else:
            return f'норма'
    else:
        if  19<= value <=36 :
            return f'отклоняющиеся'
        elif 17<= value <=18 :
            return f'пограничные'
        else:
            return f'норма'



def calc_level_age_ochp(row:pd.Series):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """
    age,value = row

    if age == '10-13 лет':
        if 20 <= value <=36 :
            return f'отклоняющиеся'
        elif 17<= value <= 19 :
            return f'пограничные'
        else:
            return f'норма'
    else:
        if  18<= value <= 36 :
            return f'отклоняющиеся'
        elif 15 <= value <= 17:
            return f'пограничные'
        else:
            return f'норма'

def create_result_sdq_goodman_ul(base_df:pd.DataFrame, out_dct:dict, lst_svod_cols:list):
    """
    Функция для подсчета результата если указаны колонки по которым нужно провести свод
    :param df: датафрейм с результатами
    :param out_dct: словарь с уже подсчитанными базовыми данными
    :param lst_svod_cols: список сводных колонок
    :return: словарь
    """
    lst_level = ['норма', 'пограничные', 'отклоняющиеся']
    lst_reindex_one_level_cols = lst_svod_cols.copy()
    lst_reindex_one_level_cols.extend(['норма', 'пограничные', 'отклоняющиеся',
                                       'Итого'])  # Основная шкала

    # Пол
    svod_count_one_sex_level_psp_df = calc_count_scale(base_df, lst_svod_cols,
                                                    'ПСП_Значение',
                                                    'ПСП_Пол_Уровень',
                                                    lst_reindex_one_level_cols, lst_level)

    svod_count_one_sex_level_ga_df = calc_count_scale(base_df, lst_svod_cols,
                                                    'ГА_Значение',
                                                    'ГА_Пол_Уровень',
                                                    lst_reindex_one_level_cols, lst_level)

    svod_count_one_sex_level_emo_df = calc_count_scale(base_df, lst_svod_cols,
                                                    'ЭС_Значение',
                                                    'ЭС_Пол_Уровень',
                                                    lst_reindex_one_level_cols, lst_level)

    svod_count_one_sex_level_pp_df = calc_count_scale(base_df, lst_svod_cols,
                                                    'ПП_Значение',
                                                    'ПП_Пол_Уровень',
                                                    lst_reindex_one_level_cols, lst_level)

    svod_count_one_sex_level_ps_df = calc_count_scale(base_df, lst_svod_cols,
                                                    'ПС_Значение',
                                                    'ПС_Пол_Уровень',
                                                    lst_reindex_one_level_cols, lst_level)

    svod_count_one_sex_level_ochp_df = calc_count_scale(base_df, lst_svod_cols,
                                                    'ОЧП_Значение',
                                                    'ОЧП_Пол_Уровень',
                                                    lst_reindex_one_level_cols, lst_level)

    # Возраст
    svod_count_one_age_level_psp_df = calc_count_scale(base_df, lst_svod_cols,
                                                       'ПСП_Значение',
                                                       'ПСП_Возраст_Уровень',
                                                       lst_reindex_one_level_cols, lst_level)

    svod_count_one_age_level_ga_df = calc_count_scale(base_df, lst_svod_cols,
                                                      'ГА_Значение',
                                                      'ГА_Возраст_Уровень',
                                                      lst_reindex_one_level_cols, lst_level)

    svod_count_one_age_level_emo_df = calc_count_scale(base_df, lst_svod_cols,
                                                       'ЭС_Значение',
                                                       'ЭС_Возраст_Уровень',
                                                       lst_reindex_one_level_cols, lst_level)

    svod_count_one_age_level_pp_df = calc_count_scale(base_df, lst_svod_cols,
                                                      'ПП_Значение',
                                                      'ПП_Возраст_Уровень',
                                                      lst_reindex_one_level_cols, lst_level)

    svod_count_one_age_level_ps_df = calc_count_scale(base_df, lst_svod_cols,
                                                      'ПС_Значение',
                                                      'ПС_Возраст_Уровень',
                                                      lst_reindex_one_level_cols, lst_level)

    svod_count_one_age_level_ochp_df = calc_count_scale(base_df, lst_svod_cols,
                                                        'ОЧП_Значение',
                                                        'ОЧП_Возраст_Уровень',
                                                        lst_reindex_one_level_cols, lst_level)

    # Считаем среднее по субшкалам
    svod_mean_one_df = pd.pivot_table(base_df,
                                      index=lst_svod_cols,
                                      values=['ПСП_Значение',
                                              'ГА_Значение',
                                              'ЭС_Значение',
                                              'ПП_Значение',

                                              'ПС_Значение',
                                              'ОЧП_Значение',
                                              ],
                                      aggfunc=round_mean_two)
    svod_mean_one_df.reset_index(inplace=True)

    # упорядочиваем колонки
    new_order_cols = lst_svod_cols.copy()
    new_order_cols.extend((['ПСП_Значение',
                          'ГА_Значение',
                          'ЭС_Значение',
                          'ПП_Значение',

                          'ПС_Значение',
                          'ОЧП_Значение',
                            ]))
    svod_mean_one_df = svod_mean_one_df.reindex(columns=new_order_cols)

    dct_rename_cols_mean = {'ПСП_Значение': 'Ср. Просоциальное поведение',
                            'ГА_Значение': 'Ср. Гиперактивность',
                            'ЭС_Значение': 'Ср. Эмоциональные симптомы',
                            'ПП_Значение': 'Ср. ППроблемы с поведением',

                            'ПС_Значение': 'Ср. Проблемы со сверстниками',
                            'ОЧП_Значение': 'Ср. Общее число проблем'
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
                    f'ПСП_П {out_name}': svod_count_one_sex_level_psp_df,
                    f'ГА_П {out_name}': svod_count_one_sex_level_ga_df,
                    f'ЭС_П {out_name}': svod_count_one_sex_level_emo_df,
                    f'ПП_П {out_name}': svod_count_one_sex_level_pp_df,
                    f'ПС_П {out_name}': svod_count_one_sex_level_ps_df,
                    f'ОЧП_П {out_name}': svod_count_one_sex_level_ochp_df,

                    f'ПСП_В {out_name}': svod_count_one_age_level_psp_df,
                    f'ГА_В {out_name}': svod_count_one_age_level_ga_df,
                    f'ЭС_В {out_name}': svod_count_one_age_level_emo_df,
                    f'ПП_В {out_name}': svod_count_one_age_level_pp_df,
                    f'ПС_В {out_name}': svod_count_one_age_level_ps_df,
                    f'ОЧП_В {out_name}': svod_count_one_age_level_ochp_df,
                    })

    if len(lst_svod_cols) == 1:
        return out_dct
    else:
        for idx, name_column in enumerate(lst_svod_cols):
            lst_reindex_column_level_cols = [lst_svod_cols[idx],'норма', 'пограничные', 'отклоняющиеся',
                                                  'Итого']

            # Пол
            svod_count_column_sex_level_psp_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                                  'ПСП_Значение',
                                                                  'ПСП_Пол_Уровень',
                                                                  lst_reindex_column_level_cols, lst_level)

            svod_count_column_sex_level_ga_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                                 'ГА_Значение',
                                                                 'ГА_Пол_Уровень',
                                                                 lst_reindex_column_level_cols, lst_level)

            svod_count_column_sex_level_emo_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                                  'ЭС_Значение',
                                                                  'ЭС_Пол_Уровень',
                                                                  lst_reindex_column_level_cols, lst_level)

            svod_count_column_sex_level_pp_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                                 'ПП_Значение',
                                                                 'ПП_Пол_Уровень',
                                                                 lst_reindex_column_level_cols, lst_level)

            svod_count_column_sex_level_ps_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                                 'ПС_Значение',
                                                                 'ПС_Пол_Уровень',
                                                                 lst_reindex_column_level_cols, lst_level)

            svod_count_column_sex_level_ochp_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                                   'ОЧП_Значение',
                                                                   'ОЧП_Пол_Уровень',
                                                                   lst_reindex_column_level_cols, lst_level)

            # Возраст
            svod_count_column_age_level_psp_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                                  'ПСП_Значение',
                                                                  'ПСП_Возраст_Уровень',
                                                                  lst_reindex_column_level_cols, lst_level)

            svod_count_column_age_level_ga_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                                 'ГА_Значение',
                                                                 'ГА_Возраст_Уровень',
                                                                 lst_reindex_column_level_cols, lst_level)

            svod_count_column_age_level_emo_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                                  'ЭС_Значение',
                                                                  'ЭС_Возраст_Уровень',
                                                                  lst_reindex_column_level_cols, lst_level)

            svod_count_column_age_level_pp_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                                 'ПП_Значение',
                                                                 'ПП_Возраст_Уровень',
                                                                 lst_reindex_column_level_cols, lst_level)

            svod_count_column_age_level_ps_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                                 'ПС_Значение',
                                                                 'ПС_Возраст_Уровень',
                                                                 lst_reindex_column_level_cols, lst_level)

            svod_count_column_age_level_ochp_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                                   'ОЧП_Значение',
                                                                   'ОЧП_Возраст_Уровень',
                                                                   lst_reindex_column_level_cols, lst_level)

            # Считаем среднее по субшкалам
            svod_mean_column_df = pd.pivot_table(base_df,
                                              index=[lst_svod_cols[idx]],
                                              values=['ПСП_Значение',
                                                      'ГА_Значение',
                                                      'ЭС_Значение',
                                                      'ПП_Значение',

                                                      'ПС_Значение',
                                                      'ОЧП_Значение',
                                                      ],
                                              aggfunc=round_mean_two)
            svod_mean_column_df.reset_index(inplace=True)

            # упорядочиваем колонки
            new_order_cols = [lst_svod_cols[idx]].copy()
            new_order_cols.extend((['ПСП_Значение',
                                    'ГА_Значение',
                                    'ЭС_Значение',
                                    'ПП_Значение',

                                    'ПС_Значение',
                                    'ОЧП_Значение',
                                    ]))
            svod_mean_column_df = svod_mean_column_df.reindex(columns=new_order_cols)

            dct_rename_cols_mean = {'ПСП_Значение': 'Ср. Просоциальное поведение',
                                    'ГА_Значение': 'Ср. Гиперактивность',
                                    'ЭС_Значение': 'Ср. Эмоциональные симптомы',
                                    'ПП_Значение': 'Ср. ППроблемы с поведением',

                                    'ПС_Значение': 'Ср. Проблемы со сверстниками',
                                    'ОЧП_Значение': 'Ср. Общее число проблем'
                                    }
            svod_mean_column_df.rename(columns=dct_rename_cols_mean, inplace=True)
            # Готовим наименование
            name_column = lst_svod_cols[idx]
            name_column = re.sub(r'[\[\]\'+()<> :"?*|\\/]', '_', name_column)
            name_column = name_column[:15]
            out_dct.update({f'Ср {name_column}': svod_mean_column_df,
                            f'ПСП_П {name_column}': svod_count_column_sex_level_psp_df,
                            f'ГА_П {name_column}': svod_count_column_sex_level_ga_df,
                            f'ЭС_П {name_column}': svod_count_column_sex_level_emo_df,
                            f'ПП_П {name_column}': svod_count_column_sex_level_pp_df,
                            f'ПС_П {name_column}': svod_count_column_sex_level_ps_df,
                            f'ОЧП_П {name_column}': svod_count_column_sex_level_ochp_df,

                            f'ПСП_В {name_column}': svod_count_column_age_level_psp_df,
                            f'ГА_В {name_column}': svod_count_column_age_level_ga_df,
                            f'ЭС_В {name_column}': svod_count_column_age_level_emo_df,
                            f'ПП_В {name_column}': svod_count_column_age_level_pp_df,
                            f'ПС_В {name_column}': svod_count_column_age_level_ps_df,
                            f'ОЧП_В {name_column}': svod_count_column_age_level_ochp_df,
                            })
        return out_dct





def processing_sdq_good_ul(base_df: pd.DataFrame, answers_df: pd.DataFrame, lst_svod_cols:list):
    """
    Функция для обработки
    :param base_df: часть датафрейма с описательными колонками
    :param answers_df: часть датафрейма с ответами
    :param lst_svod_cols:  список с колонками по которым нужно делать свод
    """
    try:
        out_answer_df = base_df.copy()  # делаем копию для последующего соединения с сырыми ответами
        if len(answers_df.columns) != 23:  # проверяем количество колонок с вопросами
            raise BadCountColumnsSDQGU

        # очищаем названия колонок от возможных сочетаний .1 которые добавляет пандас при одинаковых колонках
        clean_df_lst = []
        for name_column in answers_df.columns:
            clean_name = re.sub(r'.\d+$', '', name_column)
            clean_df_lst.append(clean_name)

        answers_df.columns = clean_df_lst

        # Проверяем наличие колонок Пол и Возраст
        diff_req_cols = {'Пол','Возраст'}.difference(set(base_df.columns))
        if len(diff_req_cols) != 0:
            raise NotReqColumn

        # на случай пустых
        base_df['Пол'].fillna('Не заполнено', inplace=True)
        # очищаем от лишних пробелов
        base_df['Пол'] = base_df['Пол'].apply(str.strip)

        base_df['Возраст'].fillna('Не заполнено', inplace=True)
        # очищаем от лишних пробелов
        base_df['Возраст'] = base_df['Возраст'].apply(str.strip)

        # Проверяем на пол
        diff_sex = set(base_df['Пол'].unique()).difference({'Мужской', 'Женский'})
        if len(diff_sex) != 0:
            raise BadValueSex

        # Проверяем на возраст
        diff_age = set(base_df['Возраст'].unique()).difference({'10-13 лет', '14-17 лет'})
        if len(diff_age) != 0:
            raise BadValueAge


        lst_check_cols = ['Я стараюсь быть хорошим с другими людьми',
                          'Я неугомонный, не могу оставаться спокойным',
                          'У меня часто бывают головные боли, боли в животе и тошнота',
                          'Я обычно делюсь с другими (едой, играми, ручками)',
                          'Я сильно сержусь, раздражаюсь и выхожу из себя',
                          'Я обычно один. Чаще всего я играю в одиночестве и занимаюсь сам',
                          'Я много беспокоюсь',
                          'Я пытаюсь помочь, если кто-нибудь расстроен, обижен или болен',
                          'Я постоянно ерзаю и верчусь',
                          'Я много дерусь. Я могу заставить других людей делать то, что я хочу',

                          'Я часто чувствую себя несчастным, унылым, готов расплакаться',
                          'Я обычно нравлюсь своим сверстникам',
                          'Я легко отвлекаюсь, мне трудно сосредоточиться',
                          'Я нервничаю в новой обстановке, легко теряю уверенность',
                          'Я добр к младшим детям',
                          'Меня часто обвиняют во лжи или обмане',
                          'Другие часто дразнят или задирают меня',
                          'Я часто вызываюсь помочь другим (родителям, учителям, детям)',
                          'Я думаю, прежде чем действовать',
                          'Я беру чужие вещи из дома, школы и других мест',
                          'У меня лучше отношения со взрослыми, чем со сверстниками',
                          'Я многого боюсь, легко пугаюсь',
                          'Я делаю до конца работу, которую начал. У меня хорошее внимание',
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
            raise BadOrderSDQGU
        # словарь для замены слов на числа
        dct_replace_value = {'неверно': 0,
                             'отчасти верно': 1,
                             'верно': 2,
                             }
        valid_values = [0, 1, 2]
        answers_df.replace(dct_replace_value, inplace=True)  # заменяем слова на цифры для подсчетов
        # Проверяем, есть ли значения, отличающиеся от указанных в списке
        lst_error_answers = []  # список для хранения строк где найдены неправильные ответы

        for i in range(23):
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
            raise BadValueSDQGU

        base_df['ПСП_Значение'] = answers_df.apply(calc_value_psp,axis=1)
        base_df['ПСП_Пол_Уровень'] = base_df[['Пол','ПСП_Значение']].apply(calc_level_sex_psp, axis=1)
        base_df['ПСП_Возраст_Уровень'] = base_df[['Возраст','ПСП_Значение']].apply(calc_level_age_psp, axis=1)

        base_df['ГА_Значение'] = answers_df.apply(calc_value_ga,axis=1)
        base_df['ГА_Пол_Уровень'] = base_df[['Пол','ГА_Значение']].apply(calc_level_sex_ga, axis=1)
        base_df['ГА_Возраст_Уровень'] = base_df[['Возраст','ГА_Значение']].apply(calc_level_age_ga, axis=1)


        base_df['ЭС_Значение'] = answers_df.apply(calc_value_emo,axis=1)
        base_df['ЭС_Пол_Уровень'] = base_df[['Пол','ЭС_Значение']].apply(calc_level_sex_emo, axis=1)
        base_df['ЭС_Возраст_Уровень'] = base_df[['Возраст','ЭС_Значение']].apply(calc_level_age_emo, axis=1)


        base_df['ПП_Значение'] = answers_df.apply(calc_value_pp,axis=1)
        base_df['ПП_Пол_Уровень'] = base_df[['Пол','ПП_Значение']].apply(calc_level_sex_pp, axis=1)
        base_df['ПП_Возраст_Уровень'] = base_df[['Возраст','ПП_Значение']].apply(calc_level_age_pp, axis=1)

        base_df['ПС_Значение'] = answers_df.apply(calc_value_ps,axis=1)
        base_df['ПС_Пол_Уровень'] = base_df[['Пол','ПС_Значение']].apply(calc_level_sex_ps, axis=1)
        base_df['ПС_Возраст_Уровень'] = base_df[['Возраст','ПС_Значение']].apply(calc_level_age_ps, axis=1)

        base_df['ОЧП_Значение'] = answers_df.apply(calc_value_ochp,axis=1)
        base_df['ОЧП_Пол_Уровень'] = base_df[['Пол','ОЧП_Значение']].apply(calc_level_sex_ochp, axis=1)
        base_df['ОЧП_Возраст_Уровень'] = base_df[['Возраст','ОЧП_Значение']].apply(calc_level_age_ochp, axis=1)

        # Создаем датафрейм для создания части в общий датафрейм
        part_df = pd.DataFrame()

        part_df['ССТУ_ПСП_Значение'] = base_df['ПСП_Значение']
        part_df['ССТУ_ПСП_Пол_Уровень'] = base_df['ПСП_Пол_Уровень']
        part_df['ССТУ_ПСП_Возраст_Уровень'] = base_df['ПСП_Возраст_Уровень']

        part_df['ССТУ_ГА_Значение'] = base_df['ГА_Значение']
        part_df['ССТУ_ГА_Пол_Уровень'] = base_df['ГА_Пол_Уровень']
        part_df['ССТУ_ГА_Возраст_Уровень'] = base_df['ГА_Возраст_Уровень']

        part_df['ССТУ_ЭС_Значение'] = base_df['ЭС_Значение']
        part_df['ССТУ_ЭС_Пол_Уровень'] = base_df['ЭС_Пол_Уровень']
        part_df['ССТУ_ЭС_Возраст_Уровень'] = base_df['ЭС_Возраст_Уровень']

        part_df['ССТУ_ПП_Значение'] = base_df['ПП_Значение']
        part_df['ССТУ_ПП_Пол_Уровень'] = base_df['ПП_Пол_Уровень']
        part_df['ССТУ_ПП_Возраст_Уровень'] = base_df['ПП_Возраст_Уровень']

        part_df['ССТУ_ПС_Значение'] = base_df['ПС_Значение']
        part_df['ССТУ_ПС_Пол_Уровень'] = base_df['ПС_Пол_Уровень']
        part_df['ССТУ_ПС_Возраст_Уровень'] = base_df['ПС_Возраст_Уровень']

        part_df['ССТУ_ОЧП_Значение'] = base_df['ОЧП_Значение']
        part_df['ССТУ_ОЧП_Пол_Уровень'] = base_df['ОЧП_Пол_Уровень']
        part_df['ССТУ_ОЧП_Возраст_Уровень'] = base_df['ОЧП_Возраст_Уровень']

        out_answer_df = pd.concat([out_answer_df, answers_df], axis=1)  # Датафрейм для проверки

        base_df.sort_values(by='ОЧП_Значение', inplace=True, ascending=False)

        # Делаем свод  по  шкале Пола
        dct_svod_sex_sub = {'ПСП_Значение': 'ПСП_Пол_Уровень',
                        'ГА_Значение': 'ГА_Пол_Уровень',
                        'ЭС_Значение': 'ЭС_Пол_Уровень',
                        'ПП_Значение': 'ПП_Пол_Уровень',

                        'ПС_Значение': 'ПС_Пол_Уровень',
                        'ОЧП_Значение': 'ОЧП_Пол_Уровень',
                        }

        dct_rename_svod_sex_sub = {'ПСП_Значение': 'ПСП',
                               'ГА_Значение': 'ГА',
                               'ЭС_Значение': 'ЭС',
                               'ПП_Значение': 'ПП',

                               'ПС_Значение': 'ПС',
                               'ОЧП_Значение': 'ОЧП',
                               }

        lst_sub = ['норма', 'пограничные', 'отклоняющиеся']

        base_svod_sex_sub_df = create_union_svod(base_df, dct_svod_sex_sub, dct_rename_svod_sex_sub, lst_sub)

        # Делаем свод  по  шкале Возраста
        dct_svod_age_sub = {'ПСП_Значение': 'ПСП_Возраст_Уровень',
                        'ГА_Значение': 'ГА_Возраст_Уровень',
                        'ЭС_Значение': 'ЭС_Возраст_Уровень',
                        'ПП_Значение': 'ПП_Возраст_Уровень',

                        'ПС_Значение': 'ПС_Возраст_Уровень',
                        'ОЧП_Значение': 'ОЧП_Возраст_Уровень',
                        }

        dct_rename_svod_age_sub = {'ПСП_Значение': 'ПСП',
                               'ГА_Значение': 'ГА',
                               'ЭС_Значение': 'ЭС',
                               'ПП_Значение': 'ПП',

                               'ПС_Значение': 'ПС',
                               'ОЧП_Значение': 'ОЧП',
                               }

        lst_sub = ['норма', 'пограничные', 'отклоняющиеся']

        base_svod_age_sub_df = create_union_svod(base_df, dct_svod_age_sub, dct_rename_svod_age_sub, lst_sub)

        # считаем среднее значение по шкалам
        avg_k = round(base_df['ПСП_Значение'].mean(), 2)
        avg_d = round(base_df['ГА_Значение'].mean(), 2)
        avg_s = round(base_df['ЭС_Значение'].mean(), 2)
        avg_psp = round(base_df['ПП_Значение'].mean(), 2)

        avg_po = round(base_df['ПС_Значение'].mean(), 2)
        avg_bi = round(base_df['ОЧП_Значение'].mean(), 2)

        avg_dct = {'Среднее значение шкалы Просоциальное поведение': avg_k,
                   'Среднее значение шкалы Гиперактивность': avg_d,
                   'Среднее значение шкалы Эмоциональные симптомы': avg_s,
                   'Среднее значение шкалы Проблемы с поведением': avg_psp,

                   'Среднее значение шкалы Проблемы со сверстниками': avg_po,
                   'Среднее значение шкалы Общее число проблем': avg_bi,
                   }

        avg_df = pd.DataFrame.from_dict(avg_dct, orient='index')
        avg_df = avg_df.reset_index()
        avg_df.columns = ['Показатель', 'Среднее значение']

        # формируем основной словарь
        out_dct = {'Списочный результат': base_df,
                   'Список для проверки': out_answer_df,
                   'Нормирование Пол': base_svod_sex_sub_df,
                   'Нормирование Возраст': base_svod_age_sub_df,
                   'Среднее': avg_df,
                   }

        dct_prefix_sex = {'ПСП_Пол_Уровень': 'ПСП_П',
                     'ГА_Пол_Уровень': 'ГА_П',
                     'ЭС_Пол_Уровень': 'ЭС_П',
                     'ПП_Пол_Уровень': 'ПП_П',

                     'ПС_Пол_Уровень': 'ПС_П',
                     'ОЧП_Пол_Уровень': 'ОЧП_П',

                     }

        out_dct = create_list_on_level(base_df, out_dct, lst_sub, dct_prefix_sex)

        dct_prefix_age = {'ПСП_Возраст_Уровень': 'ПСП_В',
                     'ГА_Возраст_Уровень': 'ГА_В',
                     'ЭС_Возраст_Уровень': 'ЭС_В',
                     'ПП_Возраст_Уровень': 'ПП_В',

                     'ПС_Возраст_Уровень': 'ПС_В',
                     'ОЧП_Возраст_Уровень': 'ОЧП_В',

                     }

        out_dct = create_list_on_level(base_df, out_dct, lst_sub, dct_prefix_age)
        """
                        Сохраняем в зависимости от необходимости делать своды по определенным колонкам
                        """
        if len(lst_svod_cols) == 0:
            return out_dct, part_df

        else:
            out_dct = create_result_sdq_goodman_ul(base_df, out_dct, lst_svod_cols)
            return out_dct, part_df

    except BadOrderSDQGU:
        messagebox.showerror('Лахеcис',
                             f'При обработке вопросов теста Сильные стороны и трудности SDQ Гудман Ульянина и др. обнаружены неправильные вопросы. Проверьте названия колонок с вопросами:\n'
                             f'{error_order_message[:5000]}\n'
                             f'Используйте при создании Яндекс-формы написание вопросов из руководства пользователя программы Лахесис.')
    except BadValueSDQGU:
        messagebox.showerror('Лахеcис',
                             f'При обработке вопросов теста Сильные стороны и трудности SDQ Гудман Ульянина и др. обнаружены неправильные варианты ответов. Проверьте ответы на указанных строках:\n'
                             f'{error_message[:5000]}\n'
                             f'Используйте при создании Яндекс-формы написание вариантов ответа из руководства пользователя программы Лахесис.')


    except BadCountColumnsSDQGU:
        messagebox.showerror('Лахеcис',
                             f'Проверьте количество колонок с ответами на тест Сильные стороны и трудности SDQ Гудман Ульянина и др.\n'
                             f'Должно быть 23 колонки с ответами')

    except NotReqColumn:
        messagebox.showerror('Лахеcис',
                             f'В таблице отсутствуют обязательные колонки {diff_req_cols}\n'
                             f'В таблице обязательно должны быть колонка с названием Пол и колонка с названием Возраст')

    except BadValueSex:
        messagebox.showerror('Лахеcис',
                             f'В колонке Пол найдены значения отличающиеся от допустимых {diff_sex}\n'
                             f'Допускаются значения: Мужской и Женский\n'
                             f'Прочитайте страницу 1 и 2 файла инструкции к тесту Сильные стороны и трудности SDQ Гудман Ульянина и др.')
    except BadValueAge:
        messagebox.showerror('Лахеcис',
                             f'В колонке Возраст найдены значения отличающиеся от допустимых {diff_age}\n'
                             f'Допускаются значения: 10-13 лет и 14-17 лет\n'
                             f'Прочитайте страницу 1 и 2 файла инструкции к тесту Сильные стороны и трудности SDQ Гудман Ульянина и др.')










