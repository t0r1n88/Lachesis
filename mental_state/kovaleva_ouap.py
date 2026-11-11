"""
Скрипт для обработки результатов Опросник для учителя по адаптации первоклассников Ковалева Тарасенко
"""

import pandas as pd
import re
from tkinter import messagebox
from lachesis_support_functions import round_mean_two,calc_count_scale,create_union_svod, create_list_on_level

class BadOrderKTOUAP(Exception):
    """
    Исключение для обработки случая когда колонки не совпадают
    """
    pass


class BadValueKTOUAP(Exception):
    """
    Исключение для неправильных значений в вариантах ответов
    """
    pass

class BadCountColumnsKTOUAP(Exception):
    """
    Исключение для обработки случая если количество колонок не равно 46
    """
    pass

def calc_value_kda(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_one = [1,2,5,6,7,8,9,12,13,14,17,18,19,
               22,23,27,31,32,33,36,41,42]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_one:
            if value == 'да':
                value_forward += 1
        else:
            if value =='да':
                value_forward += 2

    return value_forward





def calc_level_scale(value,count):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """
    result = round((value / count) * 100)

    return f'{result}%'


def calc_level_procent(value:str):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """
    try:
        value = int(value.replace('%',''))
        if 0 <= value <= 25:
            return '0-25%'
        elif 26<= value <= 50:
            return '26-50%'
        elif 51 <= value <= 75:
            return '51-75%'
        else:
            return '76-100%'

    except:
        return 'ошибочное значение'


def calc_level(value:str):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """
    try:
        value = int(value.replace('%',''))
        if 0 <= value <= 14:
            return 'низкий уровень'
        elif 15<= value <= 30:
            return 'средний уровень'
        elif 31 <= value <= 40:
            return 'выше среднего'
        else:
            return 'высокий уровень'

    except:
        return 'ошибочное значение'



def calc_value_ro(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_one = [1]
    lst_double = []
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_one:
            if value == 'да':
                value_forward += 1
        elif idx in lst_double:
            if value =='да':
                value_forward += 2

    return value_forward


def calc_value_ngsh(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_one = [2]
    lst_double = [3,4]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_one:
            if value == 'да':
                value_forward += 1
        elif idx in lst_double:
            if value =='да':
                value_forward += 2

    return value_forward

def calc_value_l(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_one = [5,6]
    lst_double = []
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_one:
            if value == 'да':
                value_forward += 1
        elif idx in lst_double:
            if value =='да':
                value_forward += 2

    return value_forward

def calc_value_ns(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_one = [7,8,9]
    lst_double = [10,11]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_one:
            if value == 'да':
                value_forward += 1
        elif idx in lst_double:
            if value =='да':
                value_forward += 2

    return value_forward


def calc_value_i(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_one = [12,13,14]
    lst_double = [15,16]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_one:
            if value == 'да':
                value_forward += 1
        elif idx in lst_double:
            if value =='да':
                value_forward += 2

    return value_forward

def calc_value_gs(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_one = [17,18,19]
    lst_double = [20,21]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_one:
            if value == 'да':
                value_forward += 1
        elif idx in lst_double:
            if value =='да':
                value_forward += 2

    return value_forward

def calc_value_ins(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_one = [22,23]
    lst_double = [24,25,26]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_one:
            if value == 'да':
                value_forward += 1
        elif idx in lst_double:
            if value =='да':
                value_forward += 2

    return value_forward


def calc_value_np(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_one = [27]
    lst_double = [28,29,30]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_one:
            if value == 'да':
                value_forward += 1
        elif idx in lst_double:
            if value =='да':
                value_forward += 2

    return value_forward


def calc_value_nm(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_one = [31,32,33]
    lst_double = [34,35]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_one:
            if value == 'да':
                value_forward += 1
        elif idx in lst_double:
            if value =='да':
                value_forward += 2

    return value_forward

def calc_value_as(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_one = [36]
    lst_double = [37,38,39,40]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_one:
            if value == 'да':
                value_forward += 1
        elif idx in lst_double:
            if value =='да':
                value_forward += 2

    return value_forward

def calc_value_nid(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_one = [41,42]
    lst_double = [43,44,45,46]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_one:
            if value == 'да':
                value_forward += 1
        elif idx in lst_double:
            if value =='да':
                value_forward += 2

    return value_forward

def create_itog_stens(row):
    """
    Функция для создания строки с итоговым стеном
    :param row: строка с результатами
    :return:
    """
    lst_out = list(map(str,row))
    return '-'.join(lst_out)


def create_list_on_level_kda(base_df:pd.DataFrame, out_dct:dict, lst_level:list, dct_prefix:dict):
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
                if level == 'низкий уровень':
                    level = 'низкий'
                elif level == 'средний уровень':
                    level = 'средний'
                elif level == 'выше среднего':
                    level = 'выше среднего'
                else:
                    level = 'высокий'
                dct_level[f'{dct_prefix[key]}. {level}'] = temp_df
        out_dct.update(dct_level)

    return out_dct

def create_result_ouap_kov_tar(base_df:pd.DataFrame, out_dct:dict, lst_svod_cols:list):
    """
    Функция для подсчета результата если указаны колонки по которым нужно провести свод
    :param df: датафрейм с результатами
    :param out_dct: словарь с уже подсчитанными базовыми данными
    :param lst_svod_cols: список сводных колонок
    :return: словарь
    """
    lst_base_one_level = ['низкий уровень','средний уровень','выше среднего','высокий уровень']

    lst_reindex_one_base_level_cols = lst_svod_cols.copy()
    lst_reindex_one_base_level_cols.extend(['низкий уровень','средний уровень','выше среднего','высокий уровень',
                                       'Итого'])  # Основная шкала

    svod_count_one_level_base_df = calc_count_scale(base_df, lst_svod_cols,
                                                    'КДА_Значение',
                                                    'КДА_Уровень',
                                                    lst_reindex_one_base_level_cols, lst_base_one_level)

    lst_level = ['0-25%', '26-50%', '51-75%', '76-100%']
    lst_reindex_one_level_cols = lst_svod_cols.copy()
    lst_reindex_one_level_cols.extend(
        ['0-25%', '26-50%', '51-75%', '76-100%',
         'Итого'])  # Основная шкала

    svod_count_one_level_ro_df = calc_count_scale(base_df, lst_svod_cols,
                                                'РО_Значение',
                                                'РО_Диапазон',
                                                lst_reindex_one_level_cols, lst_level)
    svod_count_one_level_ngsh_df = calc_count_scale(base_df, lst_svod_cols,
                                                'НГШ_Значение',
                                                'НГШ_Диапазон',
                                                lst_reindex_one_level_cols, lst_level)
    svod_count_one_level_l_df = calc_count_scale(base_df, lst_svod_cols,
                                                'Л_Значение',
                                                'Л_Диапазон',
                                                lst_reindex_one_level_cols, lst_level)
    svod_count_one_level_ns_df = calc_count_scale(base_df, lst_svod_cols,
                                                'НС_Значение',
                                                'НС_Диапазон',
                                                lst_reindex_one_level_cols, lst_level)
    svod_count_one_level_i_df = calc_count_scale(base_df, lst_svod_cols,
                                                'И_Значение',
                                                'И_Диапазон',
                                                lst_reindex_one_level_cols, lst_level)

    svod_count_one_level_gs_df = calc_count_scale(base_df, lst_svod_cols,
                                                'ГС_Значение',
                                                'ГС_Диапазон',
                                                lst_reindex_one_level_cols, lst_level)
    svod_count_one_level_ins_df = calc_count_scale(base_df, lst_svod_cols,
                                                'ИНС_Значение',
                                                'ИНС_Диапазон',
                                                lst_reindex_one_level_cols, lst_level)
    svod_count_one_level_np_df = calc_count_scale(base_df, lst_svod_cols,
                                                'НП_Значение',
                                                'НП_Диапазон',
                                                lst_reindex_one_level_cols, lst_level)
    svod_count_one_level_nm_df = calc_count_scale(base_df, lst_svod_cols,
                                                'НМ_Значение',
                                                'НМ_Диапазон',
                                                lst_reindex_one_level_cols, lst_level)
    svod_count_one_level_as_df = calc_count_scale(base_df, lst_svod_cols,
                                                'АС_Значение',
                                                'АС_Диапазон',
                                                lst_reindex_one_level_cols, lst_level)
    svod_count_one_level_nid_df = calc_count_scale(base_df, lst_svod_cols,
                                                'НИД_Значение',
                                                'НИД_Диапазон',
                                                lst_reindex_one_level_cols, lst_level)

    # Считаем среднее по субшкалам
    svod_mean_one_df = pd.pivot_table(base_df,
                                      index=lst_svod_cols,
                                      values=['КДА_Значение',
                                              'РО_Значение',
                                              'НГШ_Значение',
                                              'Л_Значение',
                                              'НС_Значение',
                                              'И_Значение',

                                              'ГС_Значение',
                                              'ИНС_Значение',
                                              'НП_Значение',
                                              'НМ_Значение',
                                              'АС_Значение',
                                              'НИД_Значение',
                                              ],
                                      aggfunc=round_mean_two)
    svod_mean_one_df.reset_index(inplace=True)

    # упорядочиваем колонки
    new_order_cols = lst_svod_cols.copy()
    new_order_cols.extend((['КДА_Значение',
                                              'РО_Значение',
                                              'НГШ_Значение',
                                              'Л_Значение',
                                              'НС_Значение',
                                              'И_Значение',

                                              'ГС_Значение',
                                              'ИНС_Значение',
                                              'НП_Значение',
                                              'НМ_Значение',
                                              'АС_Значение',
                                              'НИД_Значение',
                            ]))
    svod_mean_one_df = svod_mean_one_df.reindex(columns=new_order_cols)

    dct_rename_cols_mean = {'КДА_Значение': 'Ср. Коэффициент дезадаптации ',
                            'РО_Значение': 'Ср. Родительское отношение',
                            'НГШ_Значение': 'Ср. Неготовность к школе',
                            'Л_Значение': 'Ср. Леворукость',
                            'НС_Значение': 'Ср. Невротические симптомы',
                            'И_Значение': 'Ср. Инфантилизм',

                            'ГС_Значение': 'Ср. Гиперкинетический синдром',
                            'ИНС_Значение': 'Ср. Инертность нервной системы',
                            'НП_Значение': 'Ср. Недостаточная произвольность психических функций',
                            'НМ_Значение': 'Ср. Низкая мотивация учебной деятельности',
                            'АС_Значение': 'Ср. Астенический синдром',
                            'НИД_Значение': 'Ср. Нарушения интеллектуальной деятельности',
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
                    f'КДА {out_name}': svod_count_one_level_base_df,
                    f'РО {out_name}': svod_count_one_level_ro_df,
                    f'НГШ {out_name}': svod_count_one_level_ngsh_df,
                    f'Л {out_name}': svod_count_one_level_l_df,
                    f'НС {out_name}': svod_count_one_level_ns_df,
                    f'И {out_name}': svod_count_one_level_i_df,

                    f'ГС {out_name}': svod_count_one_level_gs_df,
                    f'ИНС {out_name}': svod_count_one_level_ins_df,
                    f'НП {out_name}': svod_count_one_level_np_df,
                    f'НМ {out_name}': svod_count_one_level_nm_df,
                    f'АС {out_name}': svod_count_one_level_as_df,
                    f'НИД {out_name}': svod_count_one_level_nid_df,
                    })

    if len(lst_svod_cols) == 1:
        return out_dct

    else:
        for idx, name_column in enumerate(lst_svod_cols):

            lst_reindex_column_base_level_cols = [lst_svod_cols[idx],'низкий уровень','средний уровень','выше среднего','высокий уровень',
                                                  'Итого']

            svod_count_column_level_base_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                            'КДА_Значение',
                                                            'КДА_Уровень',
                                                            lst_reindex_column_base_level_cols, lst_base_one_level)

            lst_reindex_column_level_cols = [lst_svod_cols[idx],'0-25%', '26-50%', '51-75%', '76-100%',
                                                  'Итого']

            svod_count_column_level_ro_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                             'РО_Значение',
                                                             'РО_Диапазон',
                                                             lst_reindex_column_level_cols, lst_level)
            svod_count_column_level_ngsh_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                               'НГШ_Значение',
                                                               'НГШ_Диапазон',
                                                               lst_reindex_column_level_cols, lst_level)
            svod_count_column_level_l_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                            'Л_Значение',
                                                            'Л_Диапазон',
                                                            lst_reindex_column_level_cols, lst_level)
            svod_count_column_level_ns_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                             'НС_Значение',
                                                             'НС_Диапазон',
                                                             lst_reindex_column_level_cols, lst_level)
            svod_count_column_level_i_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                            'И_Значение',
                                                            'И_Диапазон',
                                                            lst_reindex_column_level_cols, lst_level)

            svod_count_column_level_gs_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                             'ГС_Значение',
                                                             'ГС_Диапазон',
                                                             lst_reindex_column_level_cols, lst_level)
            svod_count_column_level_ins_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                              'ИНС_Значение',
                                                              'ИНС_Диапазон',
                                                              lst_reindex_column_level_cols, lst_level)
            svod_count_column_level_np_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                             'НП_Значение',
                                                             'НП_Диапазон',
                                                             lst_reindex_column_level_cols, lst_level)
            svod_count_column_level_nm_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                             'НМ_Значение',
                                                             'НМ_Диапазон',
                                                             lst_reindex_column_level_cols, lst_level)
            svod_count_column_level_as_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                             'АС_Значение',
                                                             'АС_Диапазон',
                                                             lst_reindex_column_level_cols, lst_level)
            svod_count_column_level_nid_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                              'НИД_Значение',
                                                              'НИД_Диапазон',
                                                              lst_reindex_column_level_cols, lst_level)

            # Считаем среднее по субшкалам
            svod_mean_column_df = pd.pivot_table(base_df,
                                                 index=[lst_svod_cols[idx]],
                                                 values=['КДА_Значение',
                                                         'РО_Значение',
                                                         'НГШ_Значение',
                                                         'Л_Значение',
                                                         'НС_Значение',
                                                         'И_Значение',

                                                         'ГС_Значение',
                                                         'ИНС_Значение',
                                                         'НП_Значение',
                                                         'НМ_Значение',
                                                         'АС_Значение',
                                                         'НИД_Значение',
                                                         ],
                                                 aggfunc=round_mean_two)
            svod_mean_column_df.reset_index(inplace=True)

            # упорядочиваем колонки
            new_order_cols =  [lst_svod_cols[idx]].copy()
            new_order_cols.extend((['КДА_Значение',
                                    'РО_Значение',
                                    'НГШ_Значение',
                                    'Л_Значение',
                                    'НС_Значение',
                                    'И_Значение',

                                    'ГС_Значение',
                                    'ИНС_Значение',
                                    'НП_Значение',
                                    'НМ_Значение',
                                    'АС_Значение',
                                    'НИД_Значение',
                                    ]))
            svod_mean_column_df = svod_mean_column_df.reindex(columns=new_order_cols)

            dct_rename_cols_mean = {'КДА_Значение': 'Ср. Коэффициент дезадаптации ',
                                    'РО_Значение': 'Ср. Родительское отношение',
                                    'НГШ_Значение': 'Ср. Неготовность к школе',
                                    'Л_Значение': 'Ср. Леворукость',
                                    'НС_Значение': 'Ср. Невротические симптомы',
                                    'И_Значение': 'Ср. Инфантилизм',

                                    'ГС_Значение': 'Ср. Гиперкинетический синдром',
                                    'ИНС_Значение': 'Ср. Инертность нервной системы',
                                    'НП_Значение': 'Ср. Недостаточная произвольность психических функций',
                                    'НМ_Значение': 'Ср. Низкая мотивация учебной деятельности',
                                    'АС_Значение': 'Ср. Астенический синдром',
                                    'НИД_Значение': 'Ср. Нарушения интеллектуальной деятельности',
                                    }
            svod_mean_column_df.rename(columns=dct_rename_cols_mean, inplace=True)

            # Готовим наименование
            name_column = lst_svod_cols[idx]
            name_column = re.sub(r'[\[\]\'+()<> :"?*|\\/]', '_', name_column)
            name_column = name_column[:15]

            out_dct.update({f'Ср {name_column}': svod_mean_column_df,
                            f'КДА {name_column}': svod_count_column_level_base_df,
                            f'РО {name_column}': svod_count_column_level_ro_df,
                            f'НГШ {name_column}': svod_count_column_level_ngsh_df,
                            f'Л {name_column}': svod_count_column_level_l_df,
                            f'НС {name_column}': svod_count_column_level_ns_df,
                            f'И {name_column}': svod_count_column_level_i_df,

                            f'ГС {name_column}': svod_count_column_level_gs_df,
                            f'ИНС {name_column}': svod_count_column_level_ins_df,
                            f'НП {name_column}': svod_count_column_level_np_df,
                            f'НМ {name_column}': svod_count_column_level_nm_df,
                            f'АС {name_column}': svod_count_column_level_as_df,
                            f'НИД {name_column}': svod_count_column_level_nid_df,
                            })
        return out_dct









def processing_ouap_kov_tar(base_df: pd.DataFrame, answers_df: pd.DataFrame, lst_svod_cols:list):
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
        if len(answers_df.columns) != 46:  # проверяем количество колонок с вопросами
            raise BadCountColumnsKTOUAP

        # очищаем названия колонок от возможных сочетаний .1 которые добавляет пандас при одинаковых колонках
        clean_df_lst = []
        for name_column in answers_df.columns:
            clean_name = re.sub(r'.\d+$', '', name_column)
            clean_df_lst.append(clean_name)

        answers_df.columns = clean_df_lst

        lst_check_cols = ['Родители совершенно устранились от воспитания, почти не бывают в школе',
                          'При поступлении в школу ребёнок не владел элементарными учебными навыками (не умел считать, не знал буквы и т. п.)',
                          'Не знает многое из того, что известно большинству детей его возраста (например, дни недели, времена года, сказки и т. п.)',
                          'Плохо развиты мелкие мышцы рук (трудности с письмом, неравномерные буквы, тремор и т. п.)',
                          'Пишет правой рукой, но со слов родителей является переученным левшой',
                          'Пишет левой рукой',
                          'Бесцельно двигает руками',
                          'Часто моргает',
                          'Сосёт палец или ручку',
                          'Иногда заикается',

                          'Грызёт ногти',
                          'У ребёнка хрупкое телосложение, маленький рост',
                          'Ребёнок явно «домашний», нуждается в доброжелательной атмосфере, любит, когда его гладят, обнимают',
                          'Очень любит играть, играет даже на уроках',
                          'Такое впечатление, что он младше других детей, хотя по возрасту им ровесник',
                          'Речь инфантильная, напоминает речь 4-5-летнего ребёнка',
                          'Чрезмерно беспокоен на уроках',
                          'Быстро примиряется с неудачами',
                          'Любит шумные, подвижные игры на переменах',
                          'Не может долго сосредоточиться на одном задании, всегда старается сделать побыстрее, не заботясь о качестве',

                          'После интересной игры, физкультурной паузы его невозможно настроить на серьёзную работу',
                          'Долго переживает неудачи',
                          'При неожиданном вопросе учителя часто теряется. Если дать время на обдумывание, может ответить хорошо',
                          'Очень долго выполняет любое задание',
                          'Домашние задания выполняет гораздо лучше классных (разница очень существенная, больше, чем у других детей)',
                          'Очень долго перестраивается с одной деятельности на другую',
                          'Часто не может повторить за учителем самый простой материал, при этом демонстрирует отличную память, когда речь идёт об интересующих его вещах (например, знает марки машин, но не может повторить самое простое правило)',
                          'Требует к себе постоянного внимания со стороны учителя. Почти всё делает только после персонального обращения: «Пиши!» и т. п.',
                          'Допускает много ошибок при списывании',
                          'Чтобы отвлечь его от задания, достаточно малейшей причины: скрипнула дверь, что-то упало и т. д.',

                          'Приносит в школу игрушки и играет на уроках',
                          'Никогда ничего не сделает сверх положенного минимума: не стремится узнать что-то, рассказать',
                          'Родители жалуются, что с трудом усаживают его за уроки',
                          'Такое впечатление, что на уроках ему плохо, оживает только на переменах',
                          'Не любит никаких усилий, если что-то не получается, бросает, ищет каких-то оправданий: рука болит и т. п.',
                          'Не совсем здоровый вид (бледный, худенький)',
                          'К концу урока работает хуже, часто отвлекается, сидит с отсутствующим видом',
                          'Если что-то не получается, раздражается, плачет',
                          'Плохо работает в условиях ограниченного времени. Если его торопить, может совсем «отключиться», бросить работу',
                          'Часто жалуется на усталость, головную боль',

                          'Почти никогда не отвечает правильно, если вопрос поставлен нестандартно, требует сообразительности',
                          'Ответы становятся лучше, если есть опора на какие-то внешние объекты (считает пальцы и т. п.)',
                          'После объяснения учителя не может выполнить аналогичное задание',
                          'Затрудняется применять ранее усвоенные понятия, навыки при объяснении учителем нового материала',
                          'Часто отвечает не по существу, не может выделить главное',
                          'Такое впечатление, что ему трудно понять объяснение, так как основные навыки, понятия у него не сформированы'
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
            raise BadOrderKTOUAP

        valid_values = ['да','нет']
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
            raise BadValueKTOUAP

        base_df['КДА_Значение'] = answers_df.apply(calc_value_kda, axis=1)
        base_df['КДА_Процент'] = base_df['КДА_Значение'].apply(lambda x: calc_level_scale(x, 70))
        base_df['КДА_Уровень'] = base_df['КДА_Процент'].apply(calc_level)

        base_df['РО_Значение'] = answers_df.apply(calc_value_ro, axis=1)
        base_df['РО_Процент'] = base_df['РО_Значение'].apply(lambda x: calc_level_scale(x, 1))
        base_df['РО_Диапазон'] = base_df['РО_Процент'].apply(calc_level_procent)

        base_df['НГШ_Значение'] = answers_df.apply(calc_value_ngsh, axis=1)
        base_df['НГШ_Процент'] = base_df['НГШ_Значение'].apply(lambda x: calc_level_scale(x, 5))
        base_df['НГШ_Диапазон'] = base_df['НГШ_Процент'].apply(calc_level_procent)

        base_df['Л_Значение'] = answers_df.apply(calc_value_l, axis=1)
        base_df['Л_Процент'] = base_df['Л_Значение'].apply(lambda x: calc_level_scale(x, 2))
        base_df['Л_Диапазон'] = base_df['Л_Процент'].apply(calc_level_procent)

        base_df['НС_Значение'] = answers_df.apply(calc_value_ns, axis=1)
        base_df['НС_Процент'] = base_df['НС_Значение'].apply(lambda x: calc_level_scale(x, 7))
        base_df['НС_Диапазон'] = base_df['НС_Процент'].apply(calc_level_procent)

        base_df['И_Значение'] = answers_df.apply(calc_value_i, axis=1)
        base_df['И_Процент'] = base_df['И_Значение'].apply(lambda x: calc_level_scale(x, 7))
        base_df['И_Диапазон'] = base_df['И_Процент'].apply(calc_level_procent)

        base_df['ГС_Значение'] = answers_df.apply(calc_value_gs, axis=1)
        base_df['ГС_Процент'] = base_df['ГС_Значение'].apply(lambda x: calc_level_scale(x, 7))
        base_df['ГС_Диапазон'] = base_df['ГС_Процент'].apply(calc_level_procent)

        base_df['ИНС_Значение'] = answers_df.apply(calc_value_ins, axis=1)
        base_df['ИНС_Процент'] = base_df['ИНС_Значение'].apply(lambda x: calc_level_scale(x, 8))
        base_df['ИНС_Диапазон'] = base_df['ИНС_Процент'].apply(calc_level_procent)

        base_df['НП_Значение'] = answers_df.apply(calc_value_np, axis=1)
        base_df['НП_Процент'] = base_df['НП_Значение'].apply(lambda x: calc_level_scale(x, 7))
        base_df['НП_Диапазон'] = base_df['НП_Процент'].apply(calc_level_procent)

        base_df['НМ_Значение'] = answers_df.apply(calc_value_nm, axis=1)
        base_df['НМ_Процент'] = base_df['НМ_Значение'].apply(lambda x: calc_level_scale(x, 7))
        base_df['НМ_Диапазон'] = base_df['НМ_Процент'].apply(calc_level_procent)

        base_df['АС_Значение'] = answers_df.apply(calc_value_as, axis=1)
        base_df['АС_Процент'] = base_df['АС_Значение'].apply(lambda x: calc_level_scale(x, 9))
        base_df['АС_Диапазон'] = base_df['АС_Процент'].apply(calc_level_procent)

        base_df['НИД_Значение'] = answers_df.apply(calc_value_nid, axis=1)
        base_df['НИД_Процент'] = base_df['НИД_Значение'].apply(lambda x: calc_level_scale(x, 10))
        base_df['НИД_Диапазон'] = base_df['НИД_Процент'].apply(calc_level_procent)

        # Упорядочиваем
        result_df = base_df.iloc[:, quantity_cols_base_df:]  # отсекаем часть с результатами чтобы упорядочить
        lst_stens = [column for column in result_df.columns if 'Процент' in column]
        result_df['Итоговые_проценты_факторы'] = result_df[lst_stens].apply(create_itog_stens, axis=1)

        new_order_lst = ['КДА_Значение','КДА_Процент','КДА_Уровень',
            'Итоговые_проценты_факторы',
                         'РО_Процент', 'НГШ_Процент', 'Л_Процент', 'НС_Процент', 'И_Процент',
                         'ГС_Процент', 'ИНС_Процент', 'НП_Процент', 'НМ_Процент', 'АС_Процент','НИД_Процент',

                         'РО_Диапазон', 'НГШ_Диапазон', 'Л_Диапазон', 'НС_Диапазон', 'И_Диапазон',
                         'ГС_Диапазон', 'ИНС_Диапазон', 'НП_Диапазон', 'НМ_Диапазон', 'АС_Диапазон','НИД_Диапазон',

                         'РО_Значение', 'НГШ_Значение', 'Л_Значение', 'НС_Значение', 'И_Значение',
                         'ГС_Значение', 'ИНС_Значение', 'НП_Значение', 'НМ_Значение', 'АС_Значение','НИД_Значение'
                         ]
        result_df = result_df.reindex(columns=new_order_lst)  # изменяем порядок
        base_df = pd.concat([union_base_df, result_df], axis=1)  # соединяем и перезаписываем base_df




        # Создаем датафрейм для создания части в общий датафрейм
        part_df = pd.DataFrame()

        part_df['ОУАПКТ_КДА_Значение'] = base_df['КДА_Значение']
        part_df['ОУАПКТ_КДА_Процент'] = base_df['КДА_Процент']
        part_df['ОУАПКТ_КДА_Уровень'] = base_df['КДА_Уровень']

        part_df['ОУАПКТ_Итоговые_проценты_факторы'] = base_df['Итоговые_проценты_факторы']



        part_df['ОУАПКТ_РО_Значение'] = base_df['РО_Значение']
        part_df['ОУАПКТ_РО_Процент'] = base_df['РО_Процент']
        part_df['ОУАПКТ_РО_Диапазон'] = base_df['РО_Диапазон']

        part_df['ОУАПКТ_НГШ_Значение'] = base_df['НГШ_Значение']
        part_df['ОУАПКТ_НГШ_Процент'] = base_df['НГШ_Процент']
        part_df['ОУАПКТ_НГШ_Диапазон'] = base_df['НГШ_Диапазон']

        part_df['ОУАПКТ_Л_Значение'] = base_df['Л_Значение']
        part_df['ОУАПКТ_Л_Процент'] = base_df['Л_Процент']
        part_df['ОУАПКТ_Л_Диапазон'] = base_df['Л_Диапазон']

        part_df['ОУАПКТ_НС_Значение'] = base_df['НС_Значение']
        part_df['ОУАПКТ_НС_Процент'] = base_df['НС_Процент']
        part_df['ОУАПКТ_НС_Диапазон'] = base_df['НС_Диапазон']

        part_df['ОУАПКТ_И_Значение'] = base_df['И_Значение']
        part_df['ОУАПКТ_И_Процент'] = base_df['И_Процент']
        part_df['ОУАПКТ_И_Диапазон'] = base_df['И_Диапазон']



        part_df['ОУАПКТ_ГС_Значение'] = base_df['ГС_Значение']
        part_df['ОУАПКТ_ГС_Процент'] = base_df['ГС_Процент']
        part_df['ОУАПКТ_ГС_Диапазон'] = base_df['ГС_Диапазон']

        part_df['ОУАПКТ_ИНС_Значение'] = base_df['ИНС_Значение']
        part_df['ОУАПКТ_ИНС_Процент'] = base_df['ИНС_Процент']
        part_df['ОУАПКТ_ИНС_Диапазон'] = base_df['ИНС_Диапазон']

        part_df['ОУАПКТ_НП_Значение'] = base_df['НП_Значение']
        part_df['ОУАПКТ_НП_Процент'] = base_df['НП_Процент']
        part_df['ОУАПКТ_НП_Диапазон'] = base_df['НП_Диапазон']

        part_df['ОУАПКТ_НМ_Значение'] = base_df['НМ_Значение']
        part_df['ОУАПКТ_НМ_Процент'] = base_df['НМ_Процент']
        part_df['ОУАПКТ_НМ_Диапазон'] = base_df['НМ_Диапазон']

        part_df['ОУАПКТ_АС_Значение'] = base_df['АС_Значение']
        part_df['ОУАПКТ_АС_Процент'] = base_df['АС_Процент']
        part_df['ОУАПКТ_АС_Диапазон'] = base_df['АС_Диапазон']

        part_df['ОУАПКТ_НИД_Значение'] = base_df['НИД_Значение']
        part_df['ОУАПКТ_НИД_Процент'] = base_df['НИД_Процент']
        part_df['ОУАПКТ_НИД_Диапазон'] = base_df['НИД_Диапазон']

        part_df.replace({'низкий уровень': 'низкий уровень КДА', 'средний уровень': 'средний уровень КДА', 'выше среднего': 'выше среднего КДА', 'высокий уровень': 'высокий уровень КДА',
                         }, inplace=True)

        out_answer_df = pd.concat([out_answer_df, answers_df], axis=1)  # Датафрейм для проверки

        base_df.sort_values(by='КДА_Значение', inplace=True, ascending=False)


        # Делаем свод  по  основному показателю
        dct_svod = {'КДА_Значение': 'КДА_Уровень',
                    }

        dct_rename_svod = {
            'КДА_Значение': 'Уровень коэффициента дезадаптации',
        }

        lst_base = ['низкий уровень','средний уровень','выше среднего','высокий уровень']
        base_svod_df = create_union_svod(base_df, dct_svod, dct_rename_svod, lst_base)

        # Делаем свод  по  шкалам
        dct_svod_sub = {'РО_Значение': 'РО_Диапазон',
                        'НГШ_Значение': 'НГШ_Диапазон',
                        'Л_Значение': 'Л_Диапазон',
                        'НС_Значение': 'НС_Диапазон',
                        'И_Значение': 'И_Диапазон',

                        'ГС_Значение': 'ГС_Диапазон',
                        'ИНС_Значение': 'ИНС_Диапазон',
                        'НП_Значение': 'НП_Диапазон',
                        'НМ_Значение': 'НМ_Диапазон',
                        'АС_Значение': 'АС_Диапазон',
                        'НИД_Значение': 'НИД_Диапазон',
                        }

        dct_rename_svod_sub = {'РО_Значение': 'РО',
                               'НГШ_Значение': 'НГШ',
                               'Л_Значение': 'Л',
                               'НС_Значение': 'НС',
                               'И_Значение': 'И',

                               'ГС_Значение': 'ГС',
                               'ИНС_Значение': 'ИНС',
                               'НП_Значение': 'НП',
                               'НМ_Значение': 'НМ',
                               'АС_Значение': 'АС',
                               'НИД_Значение': 'НИД',
                               }

        lst_sub = ['0-25%', '26-50%', '51-75%', '76-100%']

        base_svod_sub_df = create_union_svod(base_df, dct_svod_sub, dct_rename_svod_sub, lst_sub)

        # считаем среднее значение по шкалам
        avg_kda = round(base_df['КДА_Значение'].mean(), 2)
        avg_ro = round(base_df['РО_Значение'].mean(), 2)
        avg_ngsh = round(base_df['НГШ_Значение'].mean(), 2)
        avg_l = round(base_df['Л_Значение'].mean(), 2)
        avg_ns = round(base_df['НС_Значение'].mean(), 2)
        avg_i = round(base_df['И_Значение'].mean(), 2)

        avg_gs = round(base_df['ГС_Значение'].mean(), 2)
        avg_ins = round(base_df['ИНС_Значение'].mean(), 2)
        avg_np = round(base_df['НП_Значение'].mean(), 2)
        avg_nm = round(base_df['НМ_Значение'].mean(), 2)
        avg_as = round(base_df['АС_Значение'].mean(), 2)
        avg_nid = round(base_df['НИД_Значение'].mean(), 2)

        avg_dct = {'Среднее значение коэффициента дезадаптации': avg_kda,
                   'Среднее значение шкалы Родительское отношение': avg_ro,
                   'Среднее значение шкалы Неготовность к школе': avg_ngsh,
                   'Среднее значение шкалы Леворукость': avg_l,
                   'Среднее значение шкалы Невротические симптомы': avg_ns,
                   'Среднее значение шкалы Инфантилизм': avg_i,

                   'Среднее значение шкалы Гиперкинетический синдром': avg_gs,
                   'Среднее значение шкалы Инертность нервной системы': avg_ins,
                   'Среднее значение шкалы Недостаточная произвольность психических функций': avg_np,
                   'Среднее значение шкалы Низкая мотивация учебной деятельности': avg_nm,
                   'Среднее значение шкалы Астенический синдром': avg_as,
                   'Среднее значение шкалы Нарушения интеллектуальной деятельности': avg_nid,
                   }

        avg_df = pd.DataFrame.from_dict(avg_dct, orient='index')
        avg_df = avg_df.reset_index()
        avg_df.columns = ['Показатель', 'Среднее значение']

        # формируем основной словарь
        out_dct = {'Списочный результат': base_df,
                   'Список для проверки': out_answer_df,
                   'Свод КДА': base_svod_df,
                   'Свод Шкалы': base_svod_sub_df,
                   'Среднее': avg_df,
                   }

        dct_prefix_ip = {'КДА_Уровень': 'КДА',

                         }
        out_dct = create_list_on_level_kda(base_df, out_dct, lst_base, dct_prefix_ip)

        dct_prefix = {'РО_Диапазон': 'РО',
                      'НГШ_Диапазон': 'НГШ',
                      'Л_Диапазон': 'Л',
                      'НС_Диапазон': 'НС',
                      'И_Диапазон': 'И',

                      'ГС_Диапазон': 'ГС',
                      'ИНС_Диапазон': 'ИНС',
                      'НП_Диапазон': 'НП',
                      'НМ_Диапазон': 'НМ',
                      'АС_Диапазон': 'АС',
                      'НИД_Диапазон': 'НИД',

                      }

        out_dct = create_list_on_level(base_df, out_dct, lst_sub, dct_prefix)
        """
                        Сохраняем в зависимости от необходимости делать своды по определенным колонкам
                        """
        if len(lst_svod_cols) == 0:
            return out_dct, part_df

        else:
            out_dct = create_result_ouap_kov_tar(base_df, out_dct, lst_svod_cols)
            return out_dct, part_df

    except BadOrderKTOUAP:
        messagebox.showerror('Лахеcис',
                             f'При обработке вопросов теста Опросник для учителя по адаптации первоклассников Ковалева Тарасенко обнаружены неправильные вопросы. Проверьте названия колонок с вопросами:\n'
                             f'{error_order_message[:5000]}\n'
                             f'Используйте при создании Яндекс-формы написание вопросов из руководства пользователя программы Лахесис.')
    except BadValueKTOUAP:
        messagebox.showerror('Лахеcис',
                             f'При обработке вопросов теста Опросник для учителя по адаптации первоклассников Ковалева Тарасенко обнаружены неправильные варианты ответов. Проверьте ответы на указанных строках:\n'
                             f'{error_message[:5000]}\n'
                             f'Используйте при создании Яндекс-формы написание вариантов ответа из руководства пользователя программы Лахесис.')


    except BadCountColumnsKTOUAP:
        messagebox.showerror('Лахеcис',
                             f'Проверьте количество колонок с ответами на Опросник для учителя по адаптации первоклассников Ковалева Тарасенко\n'
                             f'Должно быть 46 колонок с ответами')















