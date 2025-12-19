"""
Скрипт для обработки результатов теста Копинг-установки подростков ACOPE Польская
"""

import pandas as pd
import re
from tkinter import messagebox
from lachesis_support_functions import round_mean_two,calc_count_scale,create_list_on_level,create_union_svod



class BadOrderACOPEP(Exception):
    """
    Исключение для обработки случая когда колонки не совпадают
    """
    pass


class BadValueACOPEP(Exception):
    """
    Исключение для неправильных значений в вариантах ответов
    """
    pass

class BadCountColumnsACOPEP(Exception):
    """
    Исключение для обработки случая если количество колонок не равно 54
    """
    pass

def calc_value_vcha(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [19,28,49,26,51,22]
    value_forward = 0  # результат
    for idx, value in enumerate(row):
        if idx +1 in lst_pr:
            value_forward += value

    value_forward = round(value_forward / len(lst_pr),2)

    return value_forward


def calc_value_o(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [48,37,11,2,33,43,9,53]
    value_forward = 0  # результат
    for idx, value in enumerate(row):
        if idx +1 in lst_pr:
            value_forward += value

    value_forward = round(value_forward / len(lst_pr),2)

    return value_forward


def calc_value_ruvs(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [32,25,15,47,40]
    value_forward = 0  # результат
    for idx, value in enumerate(row):
        if idx +1 in lst_pr:
            value_forward += value

    value_forward = round(value_forward / len(lst_pr),2)

    return value_forward

def calc_value_psp(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [30,52,14,35,18,4]
    value_forward = 0  # результат
    for idx, value in enumerate(row):
        if idx +1 in lst_pr:
            value_forward += value

    value_forward = round(value_forward / len(lst_pr),2)

    return value_forward


def calc_value_ppvs(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [50,31,41,39,12,1]
    value_forward = 0  # результат
    for idx, value in enumerate(row):
        if idx +1 in lst_pr:
            value_forward += value

    value_forward = round(value_forward / len(lst_pr),2)

    return value_forward


def calc_value_ip(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [24,46,42,8,36]
    value_forward = 0  # результат
    for idx, value in enumerate(row):
        if idx +1 in lst_pr:
            value_forward += value

    value_forward = round(value_forward / len(lst_pr),2)

    return value_forward


def calc_value_prp(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [23,44,21]
    value_forward = 0  # результат
    for idx, value in enumerate(row):
        if idx +1 in lst_pr:
            value_forward += value

    value_forward = round(value_forward / len(lst_pr),2)

    return value_forward

def calc_value_ppbd(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [29,16]
    value_forward = 0  # результат
    for idx, value in enumerate(row):
        if idx +1 in lst_pr:
            value_forward += value

    value_forward = round(value_forward / len(lst_pr),2)

    return value_forward


def calc_value_ppp(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [34,6]
    value_forward = 0  # результат
    for idx, value in enumerate(row):
        if idx +1 in lst_pr:
            value_forward += value

    value_forward = round(value_forward / len(lst_pr),2)

    return value_forward


def calc_value_uz(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [54,10,13,27]
    value_forward = 0  # результат
    for idx, value in enumerate(row):
        if idx +1 in lst_pr:
            value_forward += value

    value_forward = round(value_forward / len(lst_pr),2)

    return value_forward

def calc_value_opchu(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [20,3]
    value_forward = 0  # результат
    for idx, value in enumerate(row):
        if idx +1 in lst_pr:
            value_forward += value

    value_forward = round(value_forward / len(lst_pr),2)

    return value_forward

def calc_value_r(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [38,5,7,17]
    value_forward = 0  # результат
    for idx, value in enumerate(row):
        if idx +1 in lst_pr:
            value_forward += value

    value_forward = round(value_forward / len(lst_pr),2)

    return value_forward


def calc_level(value):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """
    if value <= 2:
        return f'1-2'
    elif 2.01 <= value <= 3.0:
        return f'2.01-3'
    elif 3.01 <= value <= 4.0:
        return f'3.01-4'
    else:
        return f'4.01-5'


def create_list_on_level_acope(base_df:pd.DataFrame, out_dct:dict, lst_level:list, dct_prefix:dict):
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
                dct_level[f'{dct_prefix[key]}. {level}'] = temp_df
        out_dct.update(dct_level)

    return out_dct


def create_result_acope_polskaya(base_df:pd.DataFrame, out_dct:dict, lst_svod_cols:list):
    """
    Функция для подсчета результата если указаны колонки по которым нужно провести свод
    :param df: датафрейм с результатами
    :param out_dct: словарь с уже подсчитанными базовыми данными
    :param lst_svod_cols: список сводных колонок
    :return: словарь
    """
    lst_level = ['1-2', '2.01-3', '3.01-4', '4.01-5']

    lst_reindex_one_level_cols = lst_svod_cols.copy()
    lst_reindex_one_level_cols.extend(['1-2', '2.01-3', '3.01-4', '4.01-5',
                                       'Итого'])  # Основная шкала

    # ВЧА
    svod_count_one_level_vcha_df = calc_count_scale(base_df, lst_svod_cols,
                                                   'ВЧА_Значение',
                                                   'ВЧА_Диапазон',
                                                   lst_reindex_one_level_cols, lst_level)

    # О
    svod_count_one_level_o_df = calc_count_scale(base_df, lst_svod_cols,
                                                   'О_Значение',
                                                   'О_Диапазон',
                                                   lst_reindex_one_level_cols, lst_level)
    # РУВС
    svod_count_one_level_ruvs_df = calc_count_scale(base_df, lst_svod_cols,
                                                   'РУВС_Значение',
                                                   'РУВС_Диапазон',
                                                   lst_reindex_one_level_cols, lst_level)

    # ПСП
    svod_count_one_level_psp_df = calc_count_scale(base_df, lst_svod_cols,
                                                  'ПСП_Значение',
                                                  'ПСП_Диапазон',
                                                  lst_reindex_one_level_cols, lst_level)
    # ППВС
    svod_count_one_level_ppvs_df = calc_count_scale(base_df, lst_svod_cols,
                                                  'ППВС_Значение',
                                                  'ППВС_Диапазон',
                                                  lst_reindex_one_level_cols, lst_level)
    # ИП
    svod_count_one_level_ip_df = calc_count_scale(base_df, lst_svod_cols,
                                                  'ИП_Значение',
                                                  'ИП_Диапазон',
                                                  lst_reindex_one_level_cols, lst_level)

    # ПРП
    svod_count_one_level_prp_df = calc_count_scale(base_df, lst_svod_cols,
                                                  'ПРП_Значение',
                                                  'ПРП_Диапазон',
                                                  lst_reindex_one_level_cols, lst_level)
    # ППБД
    svod_count_one_level_ppbd_df = calc_count_scale(base_df, lst_svod_cols,
                                                  'ППБД_Значение',
                                                  'ППБД_Диапазон',
                                                  lst_reindex_one_level_cols, lst_level)
    # ППП
    svod_count_one_level_ppp_df = calc_count_scale(base_df, lst_svod_cols,
                                                  'ППП_Значение',
                                                  'ППП_Диапазон',
                                                  lst_reindex_one_level_cols, lst_level)

    # УЗ
    svod_count_one_level_uz_df = calc_count_scale(base_df, lst_svod_cols,
                                                  'УЗ_Значение',
                                                  'УЗ_Диапазон',
                                                  lst_reindex_one_level_cols, lst_level)
    # ОПЧЮ
    svod_count_one_level_opchu_df = calc_count_scale(base_df, lst_svod_cols,
                                                  'ОПЧЮ_Значение',
                                                  'ОПЧЮ_Диапазон',
                                                  lst_reindex_one_level_cols, lst_level)
    # Р
    svod_count_one_level_r_df = calc_count_scale(base_df, lst_svod_cols,
                                                  'Р_Значение',
                                                  'Р_Диапазон',
                                                  lst_reindex_one_level_cols, lst_level)

    # Считаем среднее по субшкалам
    svod_mean_one_df = pd.pivot_table(base_df,
                                      index=lst_svod_cols,
                                      values=['ВЧА_Значение',
                                              'О_Значение',
                                              'РУВС_Значение',
                                              'ПСП_Значение',

                                              'ППВС_Значение',
                                              'ИП_Значение',
                                              'ПРП_Значение',
                                              'ППБД_Значение',

                                              'ППП_Значение',
                                              'УЗ_Значение',
                                              'ОПЧЮ_Значение',
                                              'Р_Значение',
                                              ],
                                      aggfunc=round_mean_two)
    svod_mean_one_df.reset_index(inplace=True)

    # упорядочиваем колонки
    new_order_cols = lst_svod_cols.copy()
    new_order_cols.extend((['ВЧА_Значение', 'О_Значение',
                            'РУВС_Значение','ПСП_Значение',
                            'ППВС_Значение','ИП_Значение',
                            'ПРП_Значение','ППБД_Значение',
                            'ППП_Значение','УЗ_Значение',
                            'ОПЧЮ_Значение','Р_Значение',
                            ]))
    svod_mean_one_df = svod_mean_one_df.reindex(columns=new_order_cols)

    dct_rename_cols_mean = {'ВЧА_Значение': 'Ср. Выброс чувств (агрессия)',
                            'О_Значение': 'Ср. Отвлечение',
                            'РУВС_Значение': 'Ср. Развитие уверенности в себе',
                            'ПСП_Значение': 'Ср. Поиск социальной поддержки',

                            'ППВС_Значение': 'Ср. Поиск поддержки в семье',
                            'ИП_Значение': 'Ср. Избегание проблем',
                            'ПРП_Значение': 'Ср. Поиск религиозной поддержки',
                            'ППБД_Значение': 'Ср. Поиск поддержки у близких друзей',

                            'ППП_Значение': 'Ср. Поиск профессиональной поддержки',
                            'УЗ_Значение': 'Ср. Усиленные занятия',
                            'ОПЧЮ_Значение': 'Ср. Отношение к проблеме с чувством юмора',
                            'Р_Значение': 'Ср. Релаксация',
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
                    f'ВЧА {out_name}': svod_count_one_level_vcha_df,
                    f'О {out_name}': svod_count_one_level_o_df,
                    f'РУВС {out_name}': svod_count_one_level_ruvs_df,
                    f'ПСП {out_name}': svod_count_one_level_psp_df,

                    f'ППВ {out_name}': svod_count_one_level_ppvs_df,
                    f'ИП {out_name}': svod_count_one_level_ip_df,
                    f'ПРП {out_name}': svod_count_one_level_prp_df,
                    f'ППБД {out_name}': svod_count_one_level_ppbd_df,

                    f'ППП {out_name}': svod_count_one_level_ppp_df,
                    f'УЗ {out_name}': svod_count_one_level_uz_df,
                    f'ОПЧЮ {out_name}': svod_count_one_level_opchu_df,
                    f'Р {out_name}': svod_count_one_level_r_df,
                    })

    if len(lst_svod_cols) == 1:
        return out_dct
    else:
        for idx, name_column in enumerate(lst_svod_cols):
            lst_reindex_column_level_cols = [lst_svod_cols[idx],'1-2', '2.01-3', '3.01-4', '4.01-5',
                                                  'Итого']

            # ВЧА
            svod_count_column_level_vcha_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                               'ВЧА_Значение',
                                                               'ВЧА_Диапазон',
                                                               lst_reindex_column_level_cols, lst_level)

            # О
            svod_count_column_level_o_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                            'О_Значение',
                                                            'О_Диапазон',
                                                            lst_reindex_column_level_cols, lst_level)
            # РУВС
            svod_count_column_level_ruvs_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                               'РУВС_Значение',
                                                               'РУВС_Диапазон',
                                                               lst_reindex_column_level_cols, lst_level)

            # ПСП
            svod_count_column_level_psp_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                              'ПСП_Значение',
                                                              'ПСП_Диапазон',
                                                              lst_reindex_column_level_cols, lst_level)
            # ППВС
            svod_count_column_level_ppvs_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                               'ППВС_Значение',
                                                               'ППВС_Диапазон',
                                                               lst_reindex_column_level_cols, lst_level)
            # ИП
            svod_count_column_level_ip_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                             'ИП_Значение',
                                                             'ИП_Диапазон',
                                                             lst_reindex_column_level_cols, lst_level)

            # ПРП
            svod_count_column_level_prp_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                              'ПРП_Значение',
                                                              'ПРП_Диапазон',
                                                              lst_reindex_column_level_cols, lst_level)
            # ППБД
            svod_count_column_level_ppbd_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                               'ППБД_Значение',
                                                               'ППБД_Диапазон',
                                                               lst_reindex_column_level_cols, lst_level)
            # ППП
            svod_count_column_level_ppp_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                              'ППП_Значение',
                                                              'ППП_Диапазон',
                                                              lst_reindex_column_level_cols, lst_level)

            # УЗ
            svod_count_column_level_uz_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                             'УЗ_Значение',
                                                             'УЗ_Диапазон',
                                                             lst_reindex_column_level_cols, lst_level)
            # ОПЧЮ
            svod_count_column_level_opchu_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                                'ОПЧЮ_Значение',
                                                                'ОПЧЮ_Диапазон',
                                                                lst_reindex_column_level_cols, lst_level)
            # Р
            svod_count_column_level_r_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                            'Р_Значение',
                                                            'Р_Диапазон',
                                                            lst_reindex_column_level_cols, lst_level)

            # Считаем среднее по субшкалам
            svod_mean_column_df = pd.pivot_table(base_df,
                                              index=[lst_svod_cols[idx]],
                                              values=['ВЧА_Значение',
                                                      'О_Значение',
                                                      'РУВС_Значение',
                                                      'ПСП_Значение',

                                                      'ППВС_Значение',
                                                      'ИП_Значение',
                                                      'ПРП_Значение',
                                                      'ППБД_Значение',

                                                      'ППП_Значение',
                                                      'УЗ_Значение',
                                                      'ОПЧЮ_Значение',
                                                      'Р_Значение',
                                                      ],
                                              aggfunc=round_mean_two)
            svod_mean_column_df.reset_index(inplace=True)

            # упорядочиваем колонки
            new_order_cols = [lst_svod_cols[idx]].copy()
            new_order_cols.extend((['ВЧА_Значение', 'О_Значение',
                                    'РУВС_Значение', 'ПСП_Значение',
                                    'ППВС_Значение', 'ИП_Значение',
                                    'ПРП_Значение', 'ППБД_Значение',
                                    'ППП_Значение', 'УЗ_Значение',
                                    'ОПЧЮ_Значение', 'Р_Значение',
                                    ]))
            svod_mean_column_df = svod_mean_column_df.reindex(columns=new_order_cols)

            dct_rename_cols_mean = {'ВЧА_Значение': 'Ср. Выброс чувств (агрессия)',
                                    'О_Значение': 'Ср. Отвлечение',
                                    'РУВС_Значение': 'Ср. Развитие уверенности в себе',
                                    'ПСП_Значение': 'Ср. Поиск социальной поддержки',

                                    'ППВС_Значение': 'Ср. Поиск поддержки в семье',
                                    'ИП_Значение': 'Ср. Избегание проблем',
                                    'ПРП_Значение': 'Ср. Поиск религиозной поддержки',
                                    'ППБД_Значение': 'Ср. Поиск поддержки у близких друзей',

                                    'ППП_Значение': 'Ср. Поиск профессиональной поддержки',
                                    'УЗ_Значение': 'Ср. Усиленные занятия',
                                    'ОПЧЮ_Значение': 'Ср. Отношение к проблеме с чувством юмора',
                                    'Р_Значение': 'Ср. Релаксация',
                                    }
            svod_mean_column_df.rename(columns=dct_rename_cols_mean, inplace=True)

            # Готовим наименование
            name_column = lst_svod_cols[idx]
            name_column = re.sub(r'[\[\]\'+()<> :"?*|\\/]', '_', name_column)
            name_column = name_column[:15]
            out_dct.update({f'Ср {name_column}': svod_mean_column_df,
                            f'ВЧА {name_column}': svod_count_column_level_vcha_df,
                            f'О {name_column}': svod_count_column_level_o_df,
                            f'РУВС {name_column}': svod_count_column_level_ruvs_df,
                            f'ПСП {name_column}': svod_count_column_level_psp_df,

                            f'ППВ {name_column}': svod_count_column_level_ppvs_df,
                            f'ИП {name_column}': svod_count_column_level_ip_df,
                            f'ПРП {name_column}': svod_count_column_level_prp_df,
                            f'ППБД {name_column}': svod_count_column_level_ppbd_df,

                            f'ППП {name_column}': svod_count_column_level_ppp_df,
                            f'УЗ {name_column}': svod_count_column_level_uz_df,
                            f'ОПЧЮ {name_column}': svod_count_column_level_opchu_df,
                            f'Р {name_column}': svod_count_column_level_r_df,
                            })
        return out_dct












def processing_acope_polskaya(base_df: pd.DataFrame, answers_df: pd.DataFrame, lst_svod_cols:list):
    """
    Функция для обработки
    :param base_df: часть датафрейма с описательными колонками
    :param answers_df: часть датафрейма с ответами
    :param lst_svod_cols:  список с колонками по которым нужно делать свод
    """
    try:
        out_answer_df = base_df.copy()  # делаем копию для последующего соединения с сырыми ответами
        if len(answers_df.columns) != 54:  # проверяем количество колонок с вопросами
            raise BadCountColumnsACOPEP

        # очищаем названия колонок от возможных сочетаний .1 которые добавляет пандас при одинаковых колонках
        clean_df_lst = []
        for name_column in answers_df.columns:
            clean_name = re.sub(r'.\d+$', '', name_column)
            clean_df_lst.append(clean_name)

        answers_df.columns = clean_df_lst

        lst_check_cols = ['Когда ты сталкиваешься с серьезной проблемой или трудностями, как часто ты следуешь советам родителей?',
                          'Когда ты сталкиваешься с серьезной проблемой или трудностями, как часто ты читаешь?',
                          'Когда ты сталкиваешься с серьезной проблемой или трудностями, как часто ты пытаешься не придавать проблеме большого значения?',
                          'Когда ты сталкиваешься с серьезной проблемой или трудностями, как часто ты просишь прощения у окружающих?',
                          'Когда ты сталкиваешься с серьезной проблемой или трудностями, как часто ты слушаешь музыку?',
                          'Когда ты сталкиваешься с серьезной проблемой или трудностями, как часто ты советуешься с учителем или школьным психологом?',
                          'Когда ты сталкиваешься с серьезной проблемой или трудностями, как часто ты стараешься поесть повкуснее?',
                          'Когда ты сталкиваешься с серьезной проблемой или трудностями, как часто ты стараешься меньше бывать дома?',
                          'Когда ты сталкиваешься с серьезной проблемой или трудностями, как часто ты принимаешь лекарства, назначенные врачом, чтобы успокоиться?',
                          'Когда ты сталкиваешься с серьезной проблемой или трудностями, как часто ты активно участвуешь в школьных мероприятиях?',

                          'Когда ты сталкиваешься с серьезной проблемой или трудностями, как часто ты отправляешься по магазинам за покупками?',
                          'Когда ты сталкиваешься с серьезной проблемой или трудностями, как часто ты пытаешься все обговорить с родителями и прийти к общему соглашению?',
                          'Когда ты сталкиваешься с серьезной проблемой или трудностями, как часто ты самосовершенствуешься (приводишь себя в форму, стараешься получать хорошие оценки и т. д.)?',
                          'Когда ты сталкиваешься с серьезной проблемой или трудностями, как часто ты плачешь?',
                          'Когда ты сталкиваешься с серьезной проблемой или трудностями, как часто ты думаешь о хорошем?',
                          'Когда ты сталкиваешься с серьезной проблемой или трудностями, как часто ты встречаешься со своим парнем или своей девушкой?',
                          'Когда ты сталкиваешься с серьезной проблемой или трудностями, как часто ты садишься на любой транспорт и просто катаешься?',
                          'Когда ты сталкиваешься с серьезной проблемой или трудностями, как часто ты делаешь окружающим комплименты?',
                          'Когда ты сталкиваешься с серьезной проблемой или трудностями, как часто ты злишься и кричишь на окружающих?',
                          'Когда ты сталкиваешься с серьезной проблемой или трудностями, как часто ты шутишь и сохраняешь чувство юмора?',

                          'Когда ты сталкиваешься с серьезной проблемой или трудностями, как часто ты обсуждаешь проблему со священнослужителем?',
                          'Когда ты сталкиваешься с серьезной проблемой или трудностями, как часто ты «выпускаешь пар», жалуясь членам семьи?',
                          'Когда ты сталкиваешься с серьезной проблемой или трудностями, как часто ты идешь в храм?',
                          'Когда ты сталкиваешься с серьезной проблемой или трудностями, как часто ты принимаешь лекарства, не назначенные врачом, чтобы успокоиться?',
                          'Когда ты сталкиваешься с серьезной проблемой или трудностями, как часто ты планируешь, что ты должен делать в данной ситуации?',
                          'Когда ты сталкиваешься с серьезной проблемой или трудностями, как часто ты сквернословишь?',
                          'Когда ты сталкиваешься с серьезной проблемой или трудностями, как часто ты сосредотачиваешься на школьных заданиях?',
                          'Когда ты сталкиваешься с серьезной проблемой или трудностями, как часто ты винишь окружающих в том, что что-то идет не так?',
                          'Когда ты сталкиваешься с серьезной проблемой или трудностями, как часто ты еще больше сближаешься с самыми близкими друзьями?',
                          'Когда ты сталкиваешься с серьезной проблемой или трудностями, как часто ты пытаешься помочь окружающим в решении их проблем?',

                          'Когда ты сталкиваешься с серьезной проблемой или трудностями, как часто ты делишься с матерью своими проблемами?',
                          'Когда ты сталкиваешься с серьезной проблемой или трудностями, как часто ты самостоятельно ищешь выход из сложной ситуации?',
                          'Когда ты сталкиваешься с серьезной проблемой или трудностями, как часто ты больше времени отдаешь своему хобби (увлечению)?',
                          'Когда ты сталкиваешься с серьезной проблемой или трудностями, как часто ты обращаешься к психологу, не работающему в школе?',
                          'Когда ты сталкиваешься с серьезной проблемой или трудностями, как часто ты поддерживаешь прежние дружеские связи или заводишь новых друзей?',
                          'Когда ты сталкиваешься с серьезной проблемой или трудностями, как часто ты убеждаешь себя в том, что проблема не очень важна?',
                          'Когда ты сталкиваешься с серьезной проблемой или трудностями, как часто ты идешь в кино?',
                          'Когда ты сталкиваешься с серьезной проблемой или трудностями, как часто ты мечтаешь о том, как все могло быть иначе?',
                          'Когда ты сталкиваешься с серьезной проблемой или трудностями, как часто ты рассказываешь брату или сестре о своей проблеме?',
                          'Когда ты сталкиваешься с серьезной проблемой или трудностями, как часто ты устраиваешься на работу или старательнее работаешь на прежней работе?',

                          'Когда ты сталкиваешься с серьезной проблемой или трудностями, как часто ты занимаешься делами вместе со своей семьей?',
                          'Когда ты сталкиваешься с серьезной проблемой или трудностями, как часто ты куришь?',
                          'Когда ты сталкиваешься с серьезной проблемой или трудностями, как часто ты смотришь телевизор?',
                          'Когда ты сталкиваешься с серьезной проблемой или трудностями, как часто ты молишься?',
                          'Когда ты сталкиваешься с серьезной проблемой или трудностями, как часто ты ищешь что-то хорошее в трудной ситуации?',
                          'Когда ты сталкиваешься с серьезной проблемой или трудностями, как часто ты пьешь пиво, принимаешь спиртные напитки?',
                          'Когда ты сталкиваешься с серьезной проблемой или трудностями, как часто ты пытаешься принимать решения самостоятельно?',
                          'Когда ты сталкиваешься с серьезной проблемой или трудностями, как часто ты спишь?',
                          'Когда ты сталкиваешься с серьезной проблемой или трудностями, как часто ты говоришь окружающим обидные, злые вещи?',
                          'Когда ты сталкиваешься с серьезной проблемой или трудностями, как часто ты делишься с отцом своими проблемами?',

                          'Когда ты сталкиваешься с серьезной проблемой или трудностями, как часто ты «выпускаешь пар», жалуясь друзьям?',
                          'Когда ты сталкиваешься с серьезной проблемой или трудностями, как часто ты рассказываешь другу о своих переживаниях?',
                          'Когда ты сталкиваешься с серьезной проблемой или трудностями, как часто ты играешь в компьютерные игры?',
                          'Когда ты сталкиваешься с серьезной проблемой или трудностями, как часто ты занимаешься активными видами спорта?'
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
            raise BadOrderACOPEP

        # словарь для замены слов на числа
        dct_replace_value = {'всегда': 5,
                             'часто': 4,
                             'иногда': 3,
                             'очень редко': 2,
                             'никогда': 1,
                             }
        valid_values = [1, 2, 3, 4, 5]
        answers_df.replace(dct_replace_value, inplace=True)  # заменяем слова на цифры для подсчетов
        # Проверяем, есть ли значения, отличающиеся от указанных в списке
        lst_error_answers = []  # список для хранения строк где найдены неправильные ответы

        for i in range(54):
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
            raise BadValueACOPEP

        base_df['ВЧА_Значение'] = answers_df.apply(calc_value_vcha, axis=1)
        base_df['ВЧА_Диапазон'] = base_df['ВЧА_Значение'].apply(calc_level)

        base_df['О_Значение'] = answers_df.apply(calc_value_o, axis=1)
        base_df['О_Диапазон'] = base_df['О_Значение'].apply(calc_level)

        base_df['РУВС_Значение'] = answers_df.apply(calc_value_ruvs, axis=1)
        base_df['РУВС_Диапазон'] = base_df['РУВС_Значение'].apply(calc_level)

        base_df['ПСП_Значение'] = answers_df.apply(calc_value_psp, axis=1)
        base_df['ПСП_Диапазон'] = base_df['ПСП_Значение'].apply(calc_level)

        base_df['ППВС_Значение'] = answers_df.apply(calc_value_ppvs, axis=1)
        base_df['ППВС_Диапазон'] = base_df['ППВС_Значение'].apply(calc_level)


        base_df['ИП_Значение'] = answers_df.apply(calc_value_ip, axis=1)
        base_df['ИП_Диапазон'] = base_df['ИП_Значение'].apply(calc_level)

        base_df['ПРП_Значение'] = answers_df.apply(calc_value_prp, axis=1)
        base_df['ПРП_Диапазон'] = base_df['ПРП_Значение'].apply(calc_level)

        base_df['ППБД_Значение'] = answers_df.apply(calc_value_ppbd, axis=1)
        base_df['ППБД_Диапазон'] = base_df['ППБД_Значение'].apply(calc_level)

        base_df['ППП_Значение'] = answers_df.apply(calc_value_ppp, axis=1)
        base_df['ППП_Диапазон'] = base_df['ППП_Значение'].apply(calc_level)

        base_df['УЗ_Значение'] = answers_df.apply(calc_value_uz, axis=1)
        base_df['УЗ_Диапазон'] = base_df['УЗ_Значение'].apply(calc_level)

        base_df['ОПЧЮ_Значение'] = answers_df.apply(calc_value_opchu, axis=1)
        base_df['ОПЧЮ_Диапазон'] = base_df['ОПЧЮ_Значение'].apply(calc_level)

        base_df['Р_Значение'] = answers_df.apply(calc_value_r, axis=1)
        base_df['Р_Диапазон'] = base_df['Р_Значение'].apply(calc_level)

        # Создаем датафрейм для создания части в общий датафрейм
        part_df = pd.DataFrame()
        part_df['КУП_П_ВЧА_Значение'] = base_df['ВЧА_Значение']
        part_df['КУП_П_ВЧА_Диапазон'] = base_df['ВЧА_Диапазон']

        part_df['КУП_П_О_Значение'] = base_df['О_Значение']
        part_df['КУП_П_О_Диапазон'] = base_df['О_Диапазон']

        part_df['КУП_П_РУВС_Значение'] = base_df['РУВС_Значение']
        part_df['КУП_П_РУВС_Диапазон'] = base_df['РУВС_Диапазон']

        part_df['КУП_П_ПСП_Значение'] = base_df['ПСП_Значение']
        part_df['КУП_П_ПСП_Диапазон'] = base_df['ПСП_Диапазон']

        part_df['КУП_П_ППВС_Значение'] = base_df['ППВС_Значение']
        part_df['КУП_П_ППВС_Диапазон'] = base_df['ППВС_Диапазон']

        part_df['КУП_П_ИП_Значение'] = base_df['ИП_Значение']
        part_df['КУП_П_ИП_Диапазон'] = base_df['ИП_Диапазон']

        part_df['КУП_П_ПРП_Значение'] = base_df['ПРП_Значение']
        part_df['КУП_П_ПРП_Диапазон'] = base_df['ПРП_Диапазон']

        part_df['КУП_П_ППБД_Значение'] = base_df['ППБД_Значение']
        part_df['КУП_П_ППБД_Диапазон'] = base_df['ППБД_Диапазон']

        part_df['КУП_П_ППП_Значение'] = base_df['ППП_Значение']
        part_df['КУП_П_ППП_Диапазон'] = base_df['ППП_Диапазон']

        part_df['КУП_П_УЗ_Значение'] = base_df['УЗ_Значение']
        part_df['КУП_П_УЗ_Диапазон'] = base_df['УЗ_Диапазон']

        part_df['КУП_П_ОПЧЮ_Значение'] = base_df['ОПЧЮ_Значение']
        part_df['КУП_П_ОПЧЮ_Диапазон'] = base_df['ОПЧЮ_Диапазон']

        part_df['КУП_П_Р_Значение'] = base_df['Р_Значение']
        part_df['КУП_П_Р_Диапазон'] = base_df['Р_Диапазон']

        out_answer_df = pd.concat([out_answer_df, answers_df], axis=1)  # Датафрейм для проверки
        base_df.sort_values(by='ВЧА_Значение', ascending=False, inplace=True)  # сортируем

        # Делаем свод  по  шкалам
        dct_svod_sub = {'ВЧА_Значение': 'ВЧА_Диапазон',
                        'О_Значение': 'О_Диапазон',
                        'РУВС_Значение': 'РУВС_Диапазон',
                        'ПСП_Значение': 'ПСП_Диапазон',
                        'ППВС_Значение': 'ППВС_Диапазон',

                        'ИП_Значение': 'ИП_Диапазон',
                        'ПРП_Значение': 'ПРП_Диапазон',
                        'ППБД_Значение': 'ППБД_Диапазон',
                        'ППП_Значение': 'ППП_Диапазон',
                        'УЗ_Значение': 'УЗ_Диапазон',
                        'ОПЧЮ_Значение': 'ОПЧЮ_Диапазон',
                        'Р_Значение': 'Р_Диапазон',
                        }

        dct_rename_svod_sub = {'ВЧА_Значение': 'ВЧА',
                               'О_Значение': 'О',
                               'РУВС_Значение': 'РУВС',
                               'ПСП_Значение': 'ПСП',
                               'ППВС_Значение': 'ППВС',
                               'ИП_Значение': 'ИП',

                               'ПРП_Значение': 'ПРП',
                               'ППБД_Значение': 'ППБД',
                               'ППП_Значение': 'ППП',
                               'УЗ_Значение': 'УЗ',
                               'ОПЧЮ_Значение': 'ОПЧЮ',
                               'Р_Значение': 'Р',
                               }

        lst_sub = ['1-2', '2.01-3', '3.01-4', '4.01-5']

        base_svod_sub_df = create_union_svod(base_df, dct_svod_sub, dct_rename_svod_sub, lst_sub)

        # считаем среднее значение по шкалам
        avg_vcha = round(base_df['ВЧА_Значение'].mean(), 2)
        avg_o = round(base_df['О_Значение'].mean(), 2)
        avg_ruvs = round(base_df['РУВС_Значение'].mean(), 2)

        avg_psp = round(base_df['ПСП_Значение'].mean(), 2)
        avg_ppvs = round(base_df['ППВС_Значение'].mean(), 2)
        avg_ip = round(base_df['ИП_Значение'].mean(), 2)

        avg_prp = round(base_df['ПРП_Значение'].mean(), 2)
        avg_ppbd = round(base_df['ППБД_Значение'].mean(), 2)
        avg_ppp = round(base_df['ППП_Значение'].mean(), 2)

        avg_uz = round(base_df['УЗ_Значение'].mean(), 2)
        avg_opchu = round(base_df['ОПЧЮ_Значение'].mean(), 2)
        avg_r = round(base_df['Р_Значение'].mean(), 2)

        avg_dct = {'Среднее значение фактора Выброс чувств (агрессия)': avg_vcha,
                   'Среднее значение фактора Отвлечение': avg_o,
                   'Среднее значение фактора Развитие уверенности в себе': avg_ruvs,

                   'Среднее значение фактора Поиск социальной поддержки': avg_psp,
                   'Среднее значение фактора Поиск поддержки в семье': avg_ppvs,
                   'Среднее значение фактора Избегание проблем': avg_ip,

                   'Среднее значение фактора Поиск религиозной поддержки': avg_prp,
                   'Среднее значение фактора Поиск поддержки у близких друзей': avg_ppbd,
                   'Среднее значение фактора Поиск профессиональной поддержки': avg_ppp,

                   'Среднее значение фактора Усиленные занятия': avg_uz,
                   'Среднее значение фактора Отношение к проблеме с чувством юмора': avg_opchu,
                   'Среднее значение фактора Релаксация': avg_r
                   }

        avg_df = pd.DataFrame.from_dict(avg_dct, orient='index')
        avg_df = avg_df.reset_index()
        avg_df.columns = ['Показатель', 'Среднее значение']

        # формируем основной словарь
        out_dct = {'Списочный результат': base_df,
                   'Список для проверки': out_answer_df,
                   'Свод Шкалы': base_svod_sub_df,
                   'Среднее': avg_df,
                   }

        dct_prefix = {'ВЧА_Диапазон': 'ВЧА',
                      'О_Диапазон': 'О',
                      'РУВС_Диапазон': 'РУВС',

                      'ПСП_Диапазон': 'ПСП',
                      'ППВС_Диапазон': 'ППВС',
                      'ИП_Диапазон': 'ИП',

                      'ПРП_Диапазон': 'ПРП',
                      'ППБД_Диапазон': 'ППБД',
                      'ППП_Диапазон': 'ППП',

                      'УЗ_Диапазон': 'УЗ',
                      'ОПЧЮ_Диапазон': 'ОПЧЮ',
                      'Р_Диапазон': 'Р',
                      }

        out_dct = create_list_on_level_acope(base_df, out_dct, lst_sub, dct_prefix)

        """
                        Сохраняем в зависимости от необходимости делать своды по определенным колонкам
                        """
        if len(lst_svod_cols) == 0:
            return out_dct, part_df

        else:
            out_dct = create_result_acope_polskaya(base_df, out_dct, lst_svod_cols)
            return out_dct, part_df


    except BadOrderACOPEP:
        messagebox.showerror('Лахеcис',
                             f'При обработке вопросов теста Опросник копинг-установок подростков, ACOPE Польская обнаружены неправильные вопросы. Проверьте названия колонок с вопросами:\n'
                             f'{error_order_message[:5000]}\n'
                             f'Используйте при создании Яндекс-формы написание вопросов из руководства пользователя программы Лахесис.')
    except BadValueACOPEP:
        messagebox.showerror('Лахеcис',
                             f'При обработке вопросов теста Опросник копинг-установок подростков, ACOPE Польская обнаружены неправильные варианты ответов. Проверьте ответы на указанных строках:\n'
                             f'{error_message[:5000]}\n'
                             f'Используйте при создании Яндекс-формы написание вариантов ответа из руководства пользователя программы Лахесис.')


    except BadCountColumnsACOPEP:
        messagebox.showerror('Лахеcис',
                             f'Проверьте количество колонок с ответами на тест Опросник копинг-установок подростков, ACOPE Польская\n'
                             f'Должно быть 54 колонки с ответами')






