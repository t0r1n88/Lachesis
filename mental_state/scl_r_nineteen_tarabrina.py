"""
Скрипт для обработки результатов теста Опросник выраженности психопатологической симптоматики SCL-90-R Адаптация Н. В. Тарабрина
"""

import pandas as pd
import re
from tkinter import messagebox
from lachesis_support_functions import round_mean_two,create_union_svod,create_list_on_level,calc_count_scale


class BadOrderSCLRNT(Exception):
    """
    Исключение для обработки случая когда колонки не совпадают
    """
    pass


class BadValueSCLRNT(Exception):
    """
    Исключение для неправильных значений в вариантах ответов
    """
    pass

class BadCountColumnsSCLRNT(Exception):
    """
    Исключение для обработки случая если количество колонок не равно 90
    """


def calc_value_gsi(row):
    """
    Функция для подсчета значения GSI
    :param row: строка с ответами
    :return: число
    """
    return round(sum(row)/90,2)



def calc_level(value):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """
    if 0 <= value <= 0.25:
        return '0-0.25'
    elif 0.26 <= value <= 0.50:
        return '0.26-0.5'
    elif 0.51 <= value <= 0.75:
        return '0.51-0.75'
    elif 0.76 <= value <= 1:
        return '0.76-1'
    elif 1.01 <= value <= 1.25:
        return '1.01-1.25'
    elif 1.26 <= value <= 1.50:
        return '1.26-1.50'
    elif 1.51 <= value <= 1.75:
        return '1.51-1.75'
    elif 1.76 <= value <= 2:
        return '1.76-2'
    elif 2.01 <= value <= 2.50:
        return '2.01-2.50'
    elif 2.51 <= value <= 3:
        return '2.51-3'
    elif 3.01 <= value <= 3.50:
        return '3.01-3.50'
    else:
        return '3.51-4'


def calc_value_pst(row):
    """
    Функция для подсчета значения
    :param row: строка с ответами
    :return: число
    """
    return len([value for value in row if value !=0])




def calc_level_pst(value):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """
    if 0 <= value <= 25:
        return '0-25'
    elif 26 <= value <= 50:
        return '26-50'
    elif 51 <= value <= 75:
        return '51-75'
    else:
        return '76-90'


def calc_value_psdi(row):
    """
    Функция для подсчета значения
    :param row: строка с ответами
    :return: число
    """
    pst = len([value for value in row if value !=0])
    if pst == 0:
        return 0
    else:
        return round(sum(row) / pst,2)


def calc_value_som(row):
    """
    Функция для подсчета значения шкалы Соматизация
    :param row: строка с ответами
    :return: число
    """
    lst_pr = [1,4,12,27,40,42,48,49,52,53,56,58]

    value_forward = 0 # сумма

    for idx, value in enumerate(row):
        if idx +1 in lst_pr:
            value_forward += value

    return round(value_forward / len(lst_pr),2)


def calc_value_oc(row):
    """
    Функция для подсчета значения шкалы Обсессивно-компульсивные расстройства
    :param row: строка с ответами
    :return: число
    """
    lst_pr = [3,9,10,28,38,45,46,51,55,65]

    value_forward = 0 # сумма

    for idx, value in enumerate(row):
        if idx +1 in lst_pr:
            value_forward += value

    return round(value_forward / len(lst_pr),2)


def calc_value_int(row):
    """
    Функция для подсчета значения шкалы Межличностная сензитивность
    :param row: строка с ответами
    :return: число
    """
    lst_pr = [6,21,34,36,37,41,61,69,73]

    value_forward = 0 # сумма

    for idx, value in enumerate(row):
        if idx +1 in lst_pr:
            value_forward += value

    return round(value_forward / len(lst_pr),2)

def calc_value_dep(row):
    """
    Функция для подсчета значения шкалы Депрессия
    :param row: строка с ответами
    :return: число
    """
    lst_pr = [5,14,15,20,22,26,29,30,31,32,54,71,79]

    value_forward = 0 # сумма

    for idx, value in enumerate(row):
        if idx +1 in lst_pr:
            value_forward += value

    return round(value_forward / len(lst_pr),2)

def calc_value_anx(row):
    """
    Функция для подсчета значения шкалы Депрессия
    :param row: строка с ответами
    :return: число
    """
    lst_pr = [2,17,23,33,39,57,72,78,80,86]

    value_forward = 0 # сумма

    for idx, value in enumerate(row):
        if idx +1 in lst_pr:
            value_forward += value

    return round(value_forward / len(lst_pr),2)



def calc_value_hos(row):
    """
    Функция для подсчета значения шкалы Враждебность
    :param row: строка с ответами
    :return: число
    """
    lst_pr = [11,24,63,67,74,81]

    value_forward = 0 # сумма

    for idx, value in enumerate(row):
        if idx +1 in lst_pr:
            value_forward += value

    return round(value_forward / len(lst_pr),2)


def calc_value_phob(row):
    """
    Функция для подсчета значения шкалы Фобическая тревожность
    :param row: строка с ответами
    :return: число
    """
    lst_pr = [13,25,47,50,70,75,82]

    value_forward = 0 # сумма

    for idx, value in enumerate(row):
        if idx +1 in lst_pr:
            value_forward += value

    return round(value_forward / len(lst_pr),2)


def calc_value_par(row):
    """
    Функция для подсчета значения шкалы Параноидальные симптомы
    :param row: строка с ответами
    :return: число
    """
    lst_pr = [8,18,43,68,76,83]

    value_forward = 0 # сумма

    for idx, value in enumerate(row):
        if idx +1 in lst_pr:
            value_forward += value

    return round(value_forward / len(lst_pr),2)

def calc_value_psy(row):
    """
    Функция для подсчета значения шкалы Параноидальные симптомы
    :param row: строка с ответами
    :return: число
    """
    lst_pr = [7,16,35,62,77,84,85,87,88,90]

    value_forward = 0 # сумма

    for idx, value in enumerate(row):
        if idx +1 in lst_pr:
            value_forward += value

    return round(value_forward / len(lst_pr),2)


def calc_value_add(row):
    """
    Функция для подсчета значения шкалы Дополнительные вопросы
    :param row: строка с ответами
    :return: число
    """
    lst_pr = [19,60,44,59,64,66,89]

    value_forward = 0 # сумма

    for idx, value in enumerate(row):
        if idx +1 in lst_pr:
            value_forward += value

    return value_forward

def calc_level_add(value):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """
    if 0 <= value <= 6:
        return '0-6'
    elif 7 <= value <= 13:
        return '7-13'
    elif 14 <= value <= 20:
        return '14-20'
    else:
        return '21-28'

def create_result_scl_r_nineteen_tarabrina(base_df:pd.DataFrame, out_dct:dict, lst_svod_cols:list):
    """
    Функция для подсчета результата если указаны колонки по которым нужно провести свод
    :param df: датафрейм с результатами
    :param out_dct: словарь с уже подсчитанными базовыми данными
    :param lst_svod_cols: список сводных колонок
    :return: словарь
    """
    # Списки
    lst_level = ['0-0.25','0.26-0.5','0.51-0.75','0.76-1','1.01-1.25','1.26-1.50','1.51-1.75','1.76-2','2.01-2.50','2.51-3','3.01-3.50','3.51-4']
    lst_pst = ['0-25','26-50','51-75','76-90']
    lst_add = ['0-6','7-13','14-20','21-28']


    # универсальные
    lst_reindex_one_cols = lst_svod_cols.copy()
    lst_reindex_one_cols.extend( ['0-0.25','0.26-0.5','0.51-0.75','0.76-1','1.01-1.25','1.26-1.50','1.51-1.75','1.76-2','2.01-2.50','2.51-3','3.01-3.50','3.51-4',
                                   'Итого'])

    # PST
    lst_reindex_one_pst_cols = lst_svod_cols.copy()
    lst_reindex_one_pst_cols.extend( ['0-25','26-50','51-75','76-90',
                                   'Итого'])
    # ADD
    lst_reindex_one_add_cols = lst_svod_cols.copy()
    lst_reindex_one_add_cols.extend( ['0-6','7-13','14-20','21-28',
                                   'Итого'])

    # Индикаторы
    svod_count_one_gsi_df = calc_count_scale(base_df, lst_svod_cols,
                                                    'Значение_GSI',
                                                    'Диапазон_GSI',
                                                    lst_reindex_one_cols,lst_level)
    svod_count_one_pst_df = calc_count_scale(base_df, lst_svod_cols,
                                                    'Значение_PST',
                                                    'Диапазон_PST',
                                                    lst_reindex_one_pst_cols,lst_pst)

    svod_count_one_psdi_df = calc_count_scale(base_df, lst_svod_cols,
                                                    'Значение_PSDI',
                                                    'Диапазон_PSDI',
                                                    lst_reindex_one_cols,lst_level)

    # Шкалы
    svod_count_one_som_df = calc_count_scale(base_df, lst_svod_cols,
                                             'Значение_SOM',
                                             'Диапазон_SOM',
                                             lst_reindex_one_cols, lst_level)

    svod_count_one_oc_df = calc_count_scale(base_df, lst_svod_cols,
                                             'Значение_OC',
                                             'Диапазон_OC',
                                             lst_reindex_one_cols, lst_level)

    svod_count_one_int_df = calc_count_scale(base_df, lst_svod_cols,
                                             'Значение_INT',
                                             'Диапазон_INT',
                                             lst_reindex_one_cols, lst_level)
    svod_count_one_dep_df = calc_count_scale(base_df, lst_svod_cols,
                                             'Значение_DEP',
                                             'Диапазон_DEP',
                                             lst_reindex_one_cols, lst_level)
    svod_count_one_anx_df = calc_count_scale(base_df, lst_svod_cols,
                                             'Значение_ANX',
                                             'Диапазон_ANX',
                                             lst_reindex_one_cols, lst_level)
    svod_count_one_hos_df = calc_count_scale(base_df, lst_svod_cols,
                                             'Значение_HOS',
                                             'Диапазон_HOS',
                                             lst_reindex_one_cols, lst_level)
    svod_count_one_phob_df = calc_count_scale(base_df, lst_svod_cols,
                                             'Значение_PHOB',
                                             'Диапазон_PHOB',
                                             lst_reindex_one_cols, lst_level)
    svod_count_one_par_df = calc_count_scale(base_df, lst_svod_cols,
                                             'Значение_PAR',
                                             'Диапазон_PAR',
                                             lst_reindex_one_cols, lst_level)

    svod_count_one_psy_df = calc_count_scale(base_df, lst_svod_cols,
                                             'Значение_PSY',
                                             'Диапазон_PSY',
                                             lst_reindex_one_cols, lst_level)

    svod_count_one_add_df = calc_count_scale(base_df, lst_svod_cols,
                                             'Значение_ADD',
                                             'Диапазон_ADD',
                                             lst_reindex_one_add_cols, lst_add)


    # Считаем среднее по шкалам
    svod_mean_df = pd.pivot_table(base_df,
                                  index=lst_svod_cols,
                                  values=['Значение_GSI',
                                          'Значение_PST',
                                          'Значение_PSDI',
                                          'Значение_SOM',
                                          'Значение_OC',
                                          'Значение_INT',
                                          'Значение_DEP',
                                          'Значение_ANX',
                                          'Значение_HOS',
                                          'Значение_PHOB',
                                          'Значение_PAR',
                                          'Значение_PSY',
                                          'Значение_ADD'
                                          ],
                                  aggfunc=round_mean_two)
    svod_mean_df.reset_index(inplace=True)
    # упорядочиваем колонки
    new_order_cols = lst_svod_cols.copy()
    new_order_cols.extend((['Значение_GSI',
                                          'Значение_PST',
                                          'Значение_PSDI',
                                          'Значение_SOM',
                                          'Значение_OC',
                                          'Значение_INT',
                                          'Значение_DEP',
                                          'Значение_ANX',
                                          'Значение_HOS',
                                          'Значение_PHOB',
                                          'Значение_PAR',
                                          'Значение_PSY',
                                          'Значение_ADD'
                            ]))
    svod_mean_df = svod_mean_df.reindex(columns=new_order_cols)

    dct_rename_cols_mean = {'Значение_GSI': 'Ср. GSI',
                            'Значение_PST': 'Ср. PST',
                            'Значение_PSDI': 'Ср. PSDI',
                            'Значение_SOM': 'Ср. SOM',
                            'Значение_OC': 'Ср. OC',
                            'Значение_INT': 'Ср. INT',
                            'Значение_DEP': 'Ср. DEP',
                            'Значение_ANX': 'Ср. ANX',
                            'Значение_HOS': 'Ср. HOS',
                            'Значение_PHOB': 'Ср. PHOB',
                            'Значение_PAR': 'Ср. PAR',
                            'Значение_PSY': 'Ср. PSY',
                            'Значение_ADD': 'Ср. ADD',
             }
    svod_mean_df.rename(columns=dct_rename_cols_mean, inplace=True)

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

    out_dct.update({f'Ср {out_name}': svod_mean_df,
                    f'Свод GSI {out_name}': svod_count_one_gsi_df,
                    f'Свод PST {out_name}': svod_count_one_pst_df,
                    f'Свод PSDI {out_name}': svod_count_one_psdi_df,

                    f'Свод SOM {out_name}': svod_count_one_som_df,
                    f'Свод OC {out_name}': svod_count_one_oc_df,
                    f'Свод INT {out_name}': svod_count_one_int_df,
                    f'Свод DEP {out_name}': svod_count_one_dep_df,
                    f'Свод ANX {out_name}': svod_count_one_anx_df,
                    f'Свод HOS {out_name}': svod_count_one_hos_df,
                    f'Свод PHOB {out_name}': svod_count_one_phob_df,
                    f'Свод PAR {out_name}': svod_count_one_par_df,
                    f'Свод PSY {out_name}': svod_count_one_psy_df,
                    f'Свод ADD {out_name}': svod_count_one_add_df,
                   })

    if len(lst_svod_cols) == 1:
        return out_dct
    else:
        for idx, name_column in enumerate(lst_svod_cols):
            # универсальные
            lst_reindex_column_cols = [lst_svod_cols[idx],'0-0.25', '0.26-0.5', '0.51-0.75', '0.76-1', '1.01-1.25', '1.26-1.50', '1.51-1.75', '1.76-2',
                 '2.01-2.50',
                 '2.51-3', '3.01-3.50', '3.51-4',
                 'Итого']

            # PST
            lst_reindex_column_pst_cols = [lst_svod_cols[idx],'0-25', '26-50', '51-75', '76-90',
                                                'Итого']
            # ADD
            lst_reindex_column_add_cols = [lst_svod_cols[idx],'0-6', '7-13', '14-20', '21-28',
                                                'Итого']

            # Индикаторы
            svod_count_column_gsi_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                        'Значение_GSI',
                                                        'Диапазон_GSI',
                                                        lst_reindex_column_cols, lst_level)
            svod_count_column_pst_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                        'Значение_PST',
                                                        'Диапазон_PST',
                                                        lst_reindex_column_pst_cols, lst_pst)

            svod_count_column_psdi_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                         'Значение_PSDI',
                                                         'Диапазон_PSDI',
                                                         lst_reindex_column_cols, lst_level)

            # Шкалы
            svod_count_column_som_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                        'Значение_SOM',
                                                        'Диапазон_SOM',
                                                        lst_reindex_column_cols, lst_level)

            svod_count_column_oc_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                       'Значение_OC',
                                                       'Диапазон_OC',
                                                       lst_reindex_column_cols, lst_level)

            svod_count_column_int_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                        'Значение_INT',
                                                        'Диапазон_INT',
                                                        lst_reindex_column_cols, lst_level)
            svod_count_column_dep_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                        'Значение_DEP',
                                                        'Диапазон_DEP',
                                                        lst_reindex_column_cols, lst_level)
            svod_count_column_anx_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                        'Значение_ANX',
                                                        'Диапазон_ANX',
                                                        lst_reindex_column_cols, lst_level)
            svod_count_column_hos_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                        'Значение_HOS',
                                                        'Диапазон_HOS',
                                                        lst_reindex_column_cols, lst_level)
            svod_count_column_phob_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                         'Значение_PHOB',
                                                         'Диапазон_PHOB',
                                                         lst_reindex_column_cols, lst_level)
            svod_count_column_par_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                        'Значение_PAR',
                                                        'Диапазон_PAR',
                                                        lst_reindex_column_cols, lst_level)

            svod_count_column_psy_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                        'Значение_PSY',
                                                        'Диапазон_PSY',
                                                        lst_reindex_column_cols, lst_level)

            svod_count_column_add_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                        'Значение_ADD',
                                                        'Диапазон_ADD',
                                                        lst_reindex_column_add_cols, lst_add)

            # Считаем среднее по шкалам
            svod_mean_df = pd.pivot_table(base_df,
                                          index=[lst_svod_cols[idx]],
                                          values=['Значение_GSI',
                                                  'Значение_PST',
                                                  'Значение_PSDI',
                                                  'Значение_SOM',
                                                  'Значение_OC',
                                                  'Значение_INT',
                                                  'Значение_DEP',
                                                  'Значение_ANX',
                                                  'Значение_HOS',
                                                  'Значение_PHOB',
                                                  'Значение_PAR',
                                                  'Значение_PSY',
                                                  'Значение_ADD'
                                                  ],
                                          aggfunc=round_mean_two)
            svod_mean_df.reset_index(inplace=True)
            # упорядочиваем колонки
            new_order_cols = [lst_svod_cols[idx]].copy()
            new_order_cols.extend((['Значение_GSI',
                                    'Значение_PST',
                                    'Значение_PSDI',
                                    'Значение_SOM',
                                    'Значение_OC',
                                    'Значение_INT',
                                    'Значение_DEP',
                                    'Значение_ANX',
                                    'Значение_HOS',
                                    'Значение_PHOB',
                                    'Значение_PAR',
                                    'Значение_PSY',
                                    'Значение_ADD'
                                    ]))
            svod_mean_df = svod_mean_df.reindex(columns=new_order_cols)

            dct_rename_cols_mean = {'Значение_GSI': 'Ср. GSI',
                                    'Значение_PST': 'Ср. PST',
                                    'Значение_PSDI': 'Ср. PSDI',
                                    'Значение_SOM': 'Ср. SOM',
                                    'Значение_OC': 'Ср. OC',
                                    'Значение_INT': 'Ср. INT',
                                    'Значение_DEP': 'Ср. DEP',
                                    'Значение_ANX': 'Ср. ANX',
                                    'Значение_HOS': 'Ср. HOS',
                                    'Значение_PHOB': 'Ср. PHOB',
                                    'Значение_PAR': 'Ср. PAR',
                                    'Значение_PSY': 'Ср. PSY',
                                    'Значение_ADD': 'Ср. ADD',
                                    }
            svod_mean_df.rename(columns=dct_rename_cols_mean, inplace=True)

            name_column = lst_svod_cols[idx]
            name_column = re.sub(r'[\[\]\'+()<> :"?*|\\/]', '_', name_column)
            name_column = name_column[:15]

            out_dct.update({f'Ср {name_column}': svod_mean_df,
                            f'Свод GSI {name_column}': svod_count_column_gsi_df,
                            f'Свод PST {name_column}': svod_count_column_pst_df,
                            f'Свод PSDI {name_column}': svod_count_column_psdi_df,

                            f'Свод SOM {name_column}': svod_count_column_som_df,
                            f'Свод OC {name_column}': svod_count_column_oc_df,
                            f'Свод INT {name_column}': svod_count_column_int_df,
                            f'Свод DEP {name_column}': svod_count_column_dep_df,
                            f'Свод ANX {name_column}': svod_count_column_anx_df,
                            f'Свод HOS {name_column}': svod_count_column_hos_df,
                            f'Свод PHOB {name_column}': svod_count_column_phob_df,
                            f'Свод PAR {name_column}': svod_count_column_par_df,
                            f'Свод PSY {name_column}': svod_count_column_psy_df,
                            f'Свод ADD {name_column}': svod_count_column_add_df,
                            })
        return out_dct

















def processing_scl_r_nineteen_tarabrina(result_df: pd.DataFrame, answers_df: pd.DataFrame, lst_svod_cols:list):
    """
    Функция для обработки
    :param result_df: часть датафрейма с описательными колонками
    :param answers_df: часть датафрейма с ответами
    :param lst_svod_cols:  список с колонками по которым нужно делать свод
    """
    try:
        out_answer_df = result_df.copy()  # делаем копию для последующего соединения с сырыми ответами
        if len(answers_df.columns) != 90:  # проверяем количество колонок с вопросами
            raise BadCountColumnsSCLRNT

        # очищаем названия колонок от возможных сочетаний .1 которые добавляет пандас при одинаковых колонках
        clean_df_lst = []
        for name_column in answers_df.columns:
            clean_name = re.sub(r'.\d+$', '', name_column)
            clean_df_lst.append(clean_name)

        answers_df.columns = clean_df_lst

        lst_check_cols = ['Головные боли','Нервозность или внутренняя дрожь',
                          'Повторяющиеся неприятные неотвязные мысли','Слабость или головокружение',
                          'Потеря сексуального влечения или удовольствия','Чувство недовольства другими',
                          'Ощущение, что кто-то другой может управлять вашими мыслями','Ощущение, что почти во всех ваших неприятностях виноваты другие',
                          'Проблемы с памятью','Ваша небрежность или неряшливость',
                          'Легко возникающая досада или раздражение','Боли в сердце или грудной клетке',
                          'Чувство страха в открытых местах или на улице','Упадок сил или заторможенность',
                          'Мысли о том, чтобы покончить с собой','То, что вы слышите голоса, которых не слышат другие',
                          'Дрожь','Чувство, что большинству людей нельзя доверять',
                          'Плохой аппетит','Слезливость',
                          'Застенчивость или скованность в общении с лицами другого пола','Ощущение, что вы в западне или пойманы',
                          'Неожиданный и беспричинный страх','Вспышки гнева, которые вы не смогли сдержать',
                          'Боязнь выйти из дома одному','Чувство, что вы сами во многом виноваты',
                          'Боли в пояснице','Ощущение, что что-то вам мешает сделать что-либо',
                          'Чувство одиночества','Подавленное настроение, «хандра»',
                          'Чрезмерное беспокойство по разным поводам','Отсутствие интереса к чему бы то ни было',
                          'Чувство страха','То, что ваши чувства легко задеть',
                          'Ощущение, что другие проникают в ваши мысли','Ощущение, что другие не понимают вас или не сочувствуют вам',
                          'Ощущение, что люди недружелюбны или вы им не нравитесь','Необходимость делать все очень медленно, чтоб не допустить ошибки',
                          'Сильное или учащенное сердцебиение','Тошнота или расстройство желудка',
                          'Ощущение, что вы хуже других','Боли в мышцах',
                          'Ощущение, что другие наблюдают за вами или говорят о вас','То, что вам трудно заснуть',
                          'Потребность проверять и перепроверять то, что вы делаете','Трудности в принятии решения',
                          'Боязнь езды в автобусах, метро или поездах','Затрудненное дыхание',
                          'Приступы жара или озноба','Необходимость избегать некоторых мест или действий, так как они вас пугают',
                          'То, что вы легко теряете мысль','Онемение или покалывание в различных частях тела',
                          'Комок в горле','Ощущение, что будущее безнадежно',
                          'То, что вам трудно сосредоточиться','Ощущение слабости в различных частях тела',
                          'Ощущение напряженности или взвинченности','Тяжесть в конечностях',
                          'Мысли о смерти','Переедание',
                          'Ощущение неловкости, когда люди наблюдают за вами или говорят о вас','То, что у вас в голове чужие мысли',
                          'Импульсы причинять телесные повреждения или вред кому-либо','Бессонница по утрам',
                          'Потребность повторять действия прикасаться, мыться, пересчитывать и т.п.','Беспокойный и тревожный сон',
                          'Импульсы ломать или крушить что-нибудь','Наличие у вас идей или верований, которых не разделяют другие',
                          'Чрезмерная застенчивость при общении с другими','Чувство неловкости в людных местах (магазинах, кинотеатрах)',
                          'Чувство, что все, что бы вы ни делали, требует больших усилий','Приступы ужаса или паники',
                          'Чувство неловкости, когда вы едите или пьёте на людях','То, что вы часто вступаете в спор',
                          'Нервозность, когда вы оставались одни','То, что другие недооценивают ваши достижения',
                          'Чувство одиночества, даже когда вы с другими людьми','Такое сильное беспокойство, что вы не могли усидеть на месте',
                          'Ощущение собственной никчемности','Ощущение, что с вами произойдет что-то плохое',
                          'То, что вы кричите и швыряетесь вещами','Боязнь, что вы упадете в обморок на людях',
                          'Ощущение, что люди злоупотребят вашим доверием, если вы им позволите','Нервировавшие вас сексуальные мысли',
                          'Мысль, что вы должны быть наказаны за ваши грехи','Кошмарные мысли или видения',
                          'Мысли о том, что с вашим телом что-то не в порядке','То, что вы не чувствуете близости ни к кому',
                          'Чувство вины','Мысли о том, что с вашим рассудком творится что-то неладное'
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
            raise BadOrderSCLRNT

        # словарь для замены слов на числа
        dct_replace_value = {'совсем нет': 0,
                             'немного': 1,
                             'умеренно': 2,
                             'сильно': 3,
                             'очень сильно': 4,
                             }

        valid_values = [0, 1, 2,3,4]
        answers_df.replace(dct_replace_value, inplace=True)  # заменяем слова на цифры для подсчетов
        # Проверяем, есть ли значения, отличающиеся от указанных в списке
        lst_error_answers = []  # список для хранения строк где найдены неправильные ответы

        for i in range(90):
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
            raise BadValueSCLRNT

        base_df = pd.DataFrame()
        # Основные шкалы
        base_df['Значение_GSI'] = answers_df.apply(calc_value_gsi, axis=1)
        base_df['Диапазон_GSI'] = base_df['Значение_GSI'].apply(calc_level)

        base_df['Значение_PST'] = answers_df.apply(calc_value_pst, axis=1)
        base_df['Диапазон_PST'] = base_df['Значение_PST'].apply(calc_level_pst)

        base_df['Значение_PSDI'] = answers_df.apply(calc_value_psdi, axis=1)
        base_df['Диапазон_PSDI'] = base_df['Значение_PSDI'].apply(calc_level)

        # Субшкалы
        base_df['Значение_SOM'] = answers_df.apply(calc_value_som, axis=1)
        base_df['Диапазон_SOM'] = base_df['Значение_SOM'].apply(calc_level)

        base_df['Значение_OC'] = answers_df.apply(calc_value_oc, axis=1)
        base_df['Диапазон_OC'] = base_df['Значение_OC'].apply(calc_level)

        base_df['Значение_INT'] = answers_df.apply(calc_value_int, axis=1)
        base_df['Диапазон_INT'] = base_df['Значение_INT'].apply(calc_level)

        base_df['Значение_DEP'] = answers_df.apply(calc_value_dep, axis=1)
        base_df['Диапазон_DEP'] = base_df['Значение_DEP'].apply(calc_level)

        base_df['Значение_ANX'] = answers_df.apply(calc_value_anx, axis=1)
        base_df['Диапазон_ANX'] = base_df['Значение_ANX'].apply(calc_level)

        base_df['Значение_HOS'] = answers_df.apply(calc_value_hos, axis=1)
        base_df['Диапазон_HOS'] = base_df['Значение_HOS'].apply(calc_level)

        base_df['Значение_PHOB'] = answers_df.apply(calc_value_phob, axis=1)
        base_df['Диапазон_PHOB'] = base_df['Значение_PHOB'].apply(calc_level)

        base_df['Значение_PAR'] = answers_df.apply(calc_value_par, axis=1)
        base_df['Диапазон_PAR'] = base_df['Значение_PAR'].apply(calc_level)

        base_df['Значение_PSY'] = answers_df.apply(calc_value_psy, axis=1)
        base_df['Диапазон_PSY'] = base_df['Значение_PSY'].apply(calc_level)

        base_df['Значение_ADD'] = answers_df.apply(calc_value_add, axis=1)
        base_df['Диапазон_ADD'] = base_df['Значение_ADD'].apply(calc_level_add)

        # Создаем датафрейм для создания части в общий датафрейм
        part_df = pd.DataFrame()

        part_df['СЦЛ_Р_Т_GSI_Значение'] = base_df['Значение_GSI']
        part_df['СЦЛ_Р_Т_GSI_Диапазон'] = base_df['Диапазон_GSI']

        part_df['СЦЛ_Р_Т_PST_Значение'] = base_df['Значение_PST']
        part_df['СЦЛ_Р_Т_PST_Диапазон'] = base_df['Диапазон_PST']

        part_df['СЦЛ_Р_Т_PSDI_Значение'] = base_df['Значение_PSDI']
        part_df['СЦЛ_Р_Т_PSDI_Диапазон'] = base_df['Диапазон_PSDI']

        part_df['СЦЛ_Р_Т_SOM_Значение'] = base_df['Значение_SOM']
        part_df['СЦЛ_Р_Т_SOM_Диапазон'] = base_df['Диапазон_SOM']

        part_df['СЦЛ_Р_Т_OC_Значение'] = base_df['Значение_OC']
        part_df['СЦЛ_Р_Т_OC_Диапазон'] = base_df['Диапазон_OC']

        part_df['СЦЛ_Р_Т_INT_Значение'] = base_df['Значение_INT']
        part_df['СЦЛ_Р_Т_INT_Диапазон'] = base_df['Диапазон_INT']

        part_df['СЦЛ_Р_Т_DEP_Значение'] = base_df['Значение_DEP']
        part_df['СЦЛ_Р_Т_DEP_Диапазон'] = base_df['Диапазон_DEP']

        part_df['СЦЛ_Р_Т_ANX_Значение'] = base_df['Значение_ANX']
        part_df['СЦЛ_Р_Т_ANX_Диапазон'] = base_df['Диапазон_ANX']

        part_df['СЦЛ_Р_Т_HOS_Значение'] = base_df['Значение_HOS']
        part_df['СЦЛ_Р_Т_HOS_Диапазон'] = base_df['Диапазон_HOS']

        part_df['СЦЛ_Р_Т_PHOB_Значение'] = base_df['Значение_PHOB']
        part_df['СЦЛ_Р_Т_PHOB_Диапазон'] = base_df['Диапазон_PHOB']

        part_df['СЦЛ_Р_Т_PAR_Значение'] = base_df['Значение_PAR']
        part_df['СЦЛ_Р_Т_PAR_Диапазон'] = base_df['Диапазон_PAR']

        part_df['СЦЛ_Р_Т_PSY_Значение'] = base_df['Значение_PSY']
        part_df['СЦЛ_Р_Т_PSY_Диапазон'] = base_df['Диапазон_PSY']

        part_df['СЦЛ_Р_Т_ADD_Значение'] = base_df['Значение_ADD']
        part_df['СЦЛ_Р_Т_ADD_Диапазон'] = base_df['Диапазон_ADD']

        out_answer_df = pd.concat([out_answer_df, answers_df], axis=1)  # Датафрейм для проверки

        # Соединяем анкетную часть с результатной
        base_df = pd.concat([result_df, base_df], axis=1)
        base_df.sort_values(by='Значение_GSI', ascending=False, inplace=True)  # сортируем

        # считаем среднее значение по шкалам
        avg_gsi = round(base_df['Значение_GSI'].mean(), 2)
        avg_pst = round(base_df['Значение_PST'].mean(), 2)
        avg_psdi = round(base_df['Значение_PSDI'].mean(), 2)

        avg_som = round(base_df['Значение_SOM'].mean(), 2)
        avg_oc = round(base_df['Значение_OC'].mean(), 2)
        avg_int = round(base_df['Значение_INT'].mean(), 2)
        avg_dep = round(base_df['Значение_DEP'].mean(), 2)
        avg_anx = round(base_df['Значение_ANX'].mean(), 2)
        avg_hos = round(base_df['Значение_HOS'].mean(), 2)
        avg_phob = round(base_df['Значение_PHOB'].mean(), 2)
        avg_par = round(base_df['Значение_PAR'].mean(), 2)
        avg_psy = round(base_df['Значение_PSY'].mean(), 2)
        avg_add = round(base_df['Значение_ADD'].mean(), 2)

        avg_dct = {'Среднее значение индекса GSI': avg_gsi,
                   'Среднее значение индекса PST': avg_pst,
                   'Среднее значение индекса PSDI': avg_psdi,

                   'Среднее значение шкалы SOM': avg_som,
                   'Среднее значение шкалы OC': avg_oc,
                   'Среднее значение шкалы INT': avg_int,
                   'Среднее значение шкалы DEP': avg_dep,
                   'Среднее значение шкалы ANX': avg_anx,
                   'Среднее значение шкалы HOS': avg_hos,
                   'Среднее значение шкалы PHOB': avg_phob,
                   'Среднее значение шкалы PAR': avg_par,
                   'Среднее значение шкалы PSY': avg_psy,
                   'Среднее значение шкалы ADD': avg_add,
                   }

        avg_df = pd.DataFrame.from_dict(avg_dct, orient='index')
        avg_df = avg_df.reset_index()
        avg_df.columns = ['Показатель', 'Среднее значение']

        # Делаем свод  по  индикаторам
        dct_svod_sub = {'Значение_GSI': 'Диапазон_GSI',
                        'Значение_PSDI': 'Диапазон_PSDI',
                        }

        dct_rename_svod_sub = {'Значение_GSI': 'общий индекс тяжести симптомов (GSI)',
                               'Значение_PSDI': 'индекс наличного симптоматического дистресса (PTSD)',
                               }

        # Списки для шкал
        lst_level = ['0-0.25','0.26-0.5','0.51-0.75','0.76-1','1.01-1.25','1.26-1.50','1.51-1.75','1.76-2','2.01-2.50','2.51-3','3.01-3.50','3.51-4']

        base_svod_sub_df = create_union_svod(base_df, dct_svod_sub, dct_rename_svod_sub, lst_level)

        # Делаем свод  PST
        dct_svod_pst = {'Значение_PST': 'Диапазон_PST',
                        }

        dct_rename_svod_pst = {'Значение_PST': 'общее число утвердительных ответов (PST)',
                               }

        # Списки для шкал
        lst_pst = ['0-25','26-50','51-75','76-90']

        base_svod_pst_df = create_union_svod(base_df, dct_svod_pst, dct_rename_svod_pst, lst_pst)

        # формируем основной словарь
        out_dct = {'Списочный результат': base_df, 'Список для проверки': out_answer_df,
                   'Свод по GSI,PSDI': base_svod_sub_df,
                   'Свод по PST': base_svod_pst_df,
                   'Среднее по шкалам': avg_df,
                   }

        dct_prefix = {'Диапазон_GSI': 'GSI',
                      'Диапазон_PSDI': 'PSDI',
                      }

        out_dct = create_list_on_level(base_df, out_dct, lst_level, dct_prefix)

        dct_prefix_pst = {'Диапазон_PST': 'PST',
                      }

        out_dct = create_list_on_level(base_df, out_dct, lst_pst, dct_prefix_pst)



        """
            Сохраняем в зависимости от необходимости делать своды по определенным колонкам
            """
        if len(lst_svod_cols) == 0:
            return out_dct, part_df
        else:
            out_dct = create_result_scl_r_nineteen_tarabrina(base_df, out_dct, lst_svod_cols)

            return out_dct, part_df


    except BadOrderSCLRNT:
        messagebox.showerror('Лахеcис',
                             f'При обработке вопросов теста Опросник выраженности психопатологической симптоматики SCL-90-R обнаружены неправильные вопросы. Проверьте названия колонок с вопросами:\n'
                             f'{error_order_message}\n'
                             f'Используйте при создании Яндекс-формы написание вопросов из руководства пользователя программы Лахесис.')
    except BadValueSCLRNT:
        messagebox.showerror('Лахеcис',
                             f'При обработке вопросов теста Опросник выраженности психопатологической симптоматики SCL-90-R обнаружены неправильные варианты ответов. Проверьте ответы на указанных строках:\n'
                             f'{error_message[:5000]}\n'
                             f'Используйте при создании Яндекс-формы написание вариантов ответа из руководства пользователя программы Лахесис.')


    except BadCountColumnsSCLRNT:
        messagebox.showerror('Лахеcис',
                             f'Проверьте количество колонок с ответами на тест Опросник выраженности психопатологической симптоматики SCL-90-R\n'
                             f'Должно быть 90 колонок с ответами')










