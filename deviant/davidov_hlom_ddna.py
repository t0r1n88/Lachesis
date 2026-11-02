"""
Скрипт для обработки результатов Методика диагностики диспозиций насильственного экстремизма Давыдов Хломов
"""

import pandas as pd
import re
from tkinter import messagebox
from lachesis_support_functions import round_mean_two,calc_count_scale,create_union_svod, create_list_on_level

class BadOrderDDNADH(Exception):
    """
    Исключение для обработки случая когда колонки не совпадают
    """
    pass


class BadValueDDNADH(Exception):
    """
    Исключение для неправильных значений в вариантах ответов
    """
    pass

class BadCountColumnsDDNADH(Exception):
    """
    Исключение для обработки случая если количество колонок не равно 66
    """
    pass



def calc_level(value):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """
    if 6<= value <= 12:
        return f'6-12'
    elif 13 <= value <= 19:
        return f'13-19'
    elif 20 <= value <= 23:
        return f'20-23'
    elif 24 <= value <= 27:
        return f'24-26'
    else:
        return f'28-30'



def calc_value_ks(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [1,2,3,4,5,6]
    lst_neg = [6]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_pr:
            if idx not in lst_neg:
                value_forward += value
            else:
                if value == 1:
                    value_forward += 5
                elif value == 2:
                    value_forward += 4
                elif value == 3:
                    value_forward += 3
                elif value == 4:
                    value_forward += 2
                elif value == 5:
                    value_forward += 1
    return value_forward

def calc_value_da(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [7,8,9,10,11,12]
    lst_neg = []
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_pr:
            if idx not in lst_neg:
                value_forward += value
            else:
                if value == 1:
                    value_forward += 5
                elif value == 2:
                    value_forward += 4
                elif value == 3:
                    value_forward += 3
                elif value == 4:
                    value_forward += 2
                elif value == 5:
                    value_forward += 1
    return value_forward


def calc_value_it(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [13,14,15,16,17,18]
    lst_neg = [17,18]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_pr:
            if idx not in lst_neg:
                value_forward += value
            else:
                if value == 1:
                    value_forward += 5
                elif value == 2:
                    value_forward += 4
                elif value == 3:
                    value_forward += 3
                elif value == 4:
                    value_forward += 2
                elif value == 5:
                    value_forward += 1
    return value_forward


def calc_value_kp(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [19,20,21,22,23,24]
    lst_neg = []
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_pr:
            if idx not in lst_neg:
                value_forward += value
            else:
                if value == 1:
                    value_forward += 5
                elif value == 2:
                    value_forward += 4
                elif value == 3:
                    value_forward += 3
                elif value == 4:
                    value_forward += 2
                elif value == 5:
                    value_forward += 1
    return value_forward

def calc_value_sp(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [25,26,27,28,29,30]
    lst_neg = []
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_pr:
            if idx not in lst_neg:
                value_forward += value
            else:
                if value == 1:
                    value_forward += 5
                elif value == 2:
                    value_forward += 4
                elif value == 3:
                    value_forward += 3
                elif value == 4:
                    value_forward += 2
                elif value == 5:
                    value_forward += 1
    return value_forward


def calc_value_m(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [31,32,33,34,35,36]
    lst_neg = []
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_pr:
            if idx not in lst_neg:
                value_forward += value
            else:
                if value == 1:
                    value_forward += 5
                elif value == 2:
                    value_forward += 4
                elif value == 3:
                    value_forward += 3
                elif value == 4:
                    value_forward += 2
                elif value == 5:
                    value_forward += 1
    return value_forward


def calc_value_dc(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [37,38,39,40,41,42]
    lst_neg = [42]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_pr:
            if idx not in lst_neg:
                value_forward += value
            else:
                if value == 1:
                    value_forward += 5
                elif value == 2:
                    value_forward += 4
                elif value == 3:
                    value_forward += 3
                elif value == 4:
                    value_forward += 2
                elif value == 5:
                    value_forward += 1
    return value_forward


def calc_value_pa(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [43,44,45,46,47,48]
    lst_neg = []
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_pr:
            if idx not in lst_neg:
                value_forward += value
            else:
                if value == 1:
                    value_forward += 5
                elif value == 2:
                    value_forward += 4
                elif value == 3:
                    value_forward += 3
                elif value == 4:
                    value_forward += 2
                elif value == 5:
                    value_forward += 1
    return value_forward


def calc_value_nn(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [49,50,51,52,53,54]
    lst_neg = [53,54]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_pr:
            if idx not in lst_neg:
                value_forward += value
            else:
                if value == 1:
                    value_forward += 5
                elif value == 2:
                    value_forward += 4
                elif value == 3:
                    value_forward += 3
                elif value == 4:
                    value_forward += 2
                elif value == 5:
                    value_forward += 1
    return value_forward


def calc_value_ai(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [55,56,57,58,59,60]
    lst_neg = [60]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_pr:
            if idx not in lst_neg:
                value_forward += value
            else:
                if value == 1:
                    value_forward += 5
                elif value == 2:
                    value_forward += 4
                elif value == 3:
                    value_forward += 3
                elif value == 4:
                    value_forward += 2
                elif value == 5:
                    value_forward += 1
    return value_forward

def calc_value_k(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [61,62,63,64,65,66]
    lst_neg = []
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_pr:
            if idx not in lst_neg:
                value_forward += value
            else:
                if value == 1:
                    value_forward += 5
                elif value == 2:
                    value_forward += 4
                elif value == 3:
                    value_forward += 3
                elif value == 4:
                    value_forward += 2
                elif value == 5:
                    value_forward += 1
    return value_forward


def create_result_ddna_dav_hlo(base_df:pd.DataFrame, out_dct:dict, lst_svod_cols:list):
    """
    Функция для подсчета результата если указаны колонки по которым нужно провести свод
    :param df: датафрейм с результатами
    :param out_dct: словарь с уже подсчитанными базовыми данными
    :param lst_svod_cols: список сводных колонок
    :return: словарь
    """
    lst_level = ['6-12','13-19','20-23','24-26','28-30']

    lst_reindex_one_level_cols = lst_svod_cols.copy()
    lst_reindex_one_level_cols.extend(['6-12','13-19','20-23','24-26','28-30',
                                       'Итого'])  # Основная шкала

    # АД
    svod_count_one_level_ks_df = calc_count_scale(base_df, lst_svod_cols,
                                                 'КС_Значение',
                                                 'КС_Диапазон',
                                                 lst_reindex_one_level_cols, lst_level)

    svod_count_one_level_da_df = calc_count_scale(base_df, lst_svod_cols,
                                                 'ДА_Значение',
                                                 'ДА_Диапазон',
                                                 lst_reindex_one_level_cols, lst_level)

    svod_count_one_level_it_df = calc_count_scale(base_df, lst_svod_cols,
                                                 'ИТ_Значение',
                                                 'ИТ_Диапазон',
                                                 lst_reindex_one_level_cols, lst_level)

    svod_count_one_level_kp_df = calc_count_scale(base_df, lst_svod_cols,
                                                 'КП_Значение',
                                                 'КП_Диапазон',
                                                 lst_reindex_one_level_cols, lst_level)

    svod_count_one_level_sp_df = calc_count_scale(base_df, lst_svod_cols,
                                                 'СП_Значение',
                                                 'СП_Диапазон',
                                                 lst_reindex_one_level_cols, lst_level)

    svod_count_one_level_m_df = calc_count_scale(base_df, lst_svod_cols,
                                                 'М_Значение',
                                                 'М_Диапазон',
                                                 lst_reindex_one_level_cols, lst_level)


    svod_count_one_level_dc_df = calc_count_scale(base_df, lst_svod_cols,
                                                 'ДЦ_Значение',
                                                 'ДЦ_Диапазон',
                                                 lst_reindex_one_level_cols, lst_level)

    svod_count_one_level_pa_df = calc_count_scale(base_df, lst_svod_cols,
                                                 'ПА_Значение',
                                                 'ПА_Диапазон',
                                                 lst_reindex_one_level_cols, lst_level)

    svod_count_one_level_nn_df = calc_count_scale(base_df, lst_svod_cols,
                                                 'НН_Значение',
                                                 'НН_Диапазон',
                                                 lst_reindex_one_level_cols, lst_level)

    svod_count_one_level_ai_df = calc_count_scale(base_df, lst_svod_cols,
                                                 'АИ_Значение',
                                                 'АИ_Диапазон',
                                                 lst_reindex_one_level_cols, lst_level)

    svod_count_one_level_k_df = calc_count_scale(base_df, lst_svod_cols,
                                                 'К_Значение',
                                                 'К_Диапазон',
                                                 lst_reindex_one_level_cols, lst_level)


    # Считаем среднее по субшкалам
    svod_mean_one_df = pd.pivot_table(base_df,
                                      index=lst_svod_cols,
                                      values=['КС_Значение',
                                              'ДА_Значение',
                                              'ИТ_Значение',
                                              'КП_Значение',
                                              'СП_Значение',

                                              'М_Значение',
                                              'ДЦ_Значение',
                                              'ПА_Значение',
                                              'НН_Значение',
                                              'АИ_Значение',
                                              'К_Значение',
                                              ],
                                      aggfunc=round_mean_two)
    svod_mean_one_df.reset_index(inplace=True)

    # упорядочиваем колонки
    new_order_cols = lst_svod_cols.copy()
    new_order_cols.extend((['КС_Значение',
                          'ДА_Значение',
                          'ИТ_Значение',
                          'КП_Значение',
                          'СП_Значение',

                          'М_Значение',
                          'ДЦ_Значение',
                          'ПА_Значение',
                          'НН_Значение',
                          'АИ_Значение',
                          'К_Значение',

                            ]))
    svod_mean_one_df = svod_mean_one_df.reindex(columns=new_order_cols)
    dct_rename_cols_mean = {'КС_Значение': 'Ср. шкалы Культ силы',
                            'ДА_Значение': 'Ср. шкалы Допустимость агрессии',
                            'ИТ_Значение': 'Ср. шкалы Интолерантность',
                            'КП_Значение': 'Ср. шкалы Конвенциональное принуждение',
                            'СП_Значение': 'Ср. шкалы Социальный пессимизм',

                            'М_Значение': 'Ср. шкалы Мистичность',
                            'ДЦ_Значение': 'Ср. шкалы Деструктивность и цинизм',
                            'ПА_Значение': 'Ср. шкалы Протестная активность',
                            'НН_Значение': 'Ср. шкалы Нормативный нигилизм',
                            'АИ_Значение': 'Ср. шкалы Антиинтрацепция',
                            'К_Значение': 'Ср. шкалы Конформизм',

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
                    f'КС {out_name}': svod_count_one_level_ks_df,
                    f'ДА {out_name}': svod_count_one_level_da_df,
                    f'ИТ {out_name}': svod_count_one_level_it_df,
                    f'КП {out_name}': svod_count_one_level_kp_df,
                    f'СП {out_name}': svod_count_one_level_sp_df,

                    f'М {out_name}': svod_count_one_level_m_df,
                    f'ДЦ {out_name}': svod_count_one_level_dc_df,
                    f'ПА {out_name}': svod_count_one_level_pa_df,
                    f'НН {out_name}': svod_count_one_level_nn_df,
                    f'АИ {out_name}': svod_count_one_level_ai_df,
                    f'К {out_name}': svod_count_one_level_k_df,
                    })

    if len(lst_svod_cols) == 1:
        return out_dct
    else:
        for idx, name_column in enumerate(lst_svod_cols):
            lst_reindex_column_level_cols = [lst_svod_cols[idx], '6-12','13-19','20-23','24-26','28-30',
                                             'Итого']

            svod_count_column_level_ks_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                             'КС_Значение',
                                                             'КС_Диапазон',
                                                             lst_reindex_column_level_cols, lst_level)

            svod_count_column_level_da_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                             'ДА_Значение',
                                                             'ДА_Диапазон',
                                                             lst_reindex_column_level_cols, lst_level)

            svod_count_column_level_it_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                             'ИТ_Значение',
                                                             'ИТ_Диапазон',
                                                             lst_reindex_column_level_cols, lst_level)

            svod_count_column_level_kp_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                             'КП_Значение',
                                                             'КП_Диапазон',
                                                             lst_reindex_column_level_cols, lst_level)

            svod_count_column_level_sp_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                             'СП_Значение',
                                                             'СП_Диапазон',
                                                             lst_reindex_column_level_cols, lst_level)

            svod_count_column_level_m_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                            'М_Значение',
                                                            'М_Диапазон',
                                                            lst_reindex_column_level_cols, lst_level)

            svod_count_column_level_dc_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                             'ДЦ_Значение',
                                                             'ДЦ_Диапазон',
                                                             lst_reindex_column_level_cols, lst_level)

            svod_count_column_level_pa_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                             'ПА_Значение',
                                                             'ПА_Диапазон',
                                                             lst_reindex_column_level_cols, lst_level)

            svod_count_column_level_nn_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                             'НН_Значение',
                                                             'НН_Диапазон',
                                                             lst_reindex_column_level_cols, lst_level)

            svod_count_column_level_ai_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                             'АИ_Значение',
                                                             'АИ_Диапазон',
                                                             lst_reindex_column_level_cols, lst_level)

            svod_count_column_level_k_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                            'К_Значение',
                                                            'К_Диапазон',
                                                            lst_reindex_column_level_cols, lst_level)

            # Считаем среднее по субшкалам
            svod_mean_column_df = pd.pivot_table(base_df,
                                                 index=[lst_svod_cols[idx]],
                                                 values=['КС_Значение',
                                                         'ДА_Значение',
                                                         'ИТ_Значение',
                                                         'КП_Значение',
                                                         'СП_Значение',

                                                         'М_Значение',
                                                         'ДЦ_Значение',
                                                         'ПА_Значение',
                                                         'НН_Значение',
                                                         'АИ_Значение',
                                                         'К_Значение',
                                                         ],
                                                 aggfunc=round_mean_two)
            svod_mean_column_df.reset_index(inplace=True)

            # упорядочиваем колонки
            new_order_cols = [lst_svod_cols[idx]].copy()
            new_order_cols.extend((['КС_Значение',
                                    'ДА_Значение',
                                    'ИТ_Значение',
                                    'КП_Значение',
                                    'СП_Значение',

                                    'М_Значение',
                                    'ДЦ_Значение',
                                    'ПА_Значение',
                                    'НН_Значение',
                                    'АИ_Значение',
                                    'К_Значение',

                                    ]))
            svod_mean_column_df = svod_mean_column_df.reindex(columns=new_order_cols)
            dct_rename_cols_mean = {'КС_Значение': 'Ср. шкалы Культ силы',
                                    'ДА_Значение': 'Ср. шкалы Допустимость агрессии',
                                    'ИТ_Значение': 'Ср. шкалы Интолерантность',
                                    'КП_Значение': 'Ср. шкалы Конвенциональное принуждение',
                                    'СП_Значение': 'Ср. шкалы Социальный пессимизм',

                                    'М_Значение': 'Ср. шкалы Мистичность',
                                    'ДЦ_Значение': 'Ср. шкалы Деструктивность и цинизм',
                                    'ПА_Значение': 'Ср. шкалы Протестная активность',
                                    'НН_Значение': 'Ср. шкалы Нормативный нигилизм',
                                    'АИ_Значение': 'Ср. шкалы Антиинтрацепция',
                                    'К_Значение': 'Ср. шкалы Конформизм',

                                    }
            svod_mean_column_df.rename(columns=dct_rename_cols_mean, inplace=True)

            # Готовим наименование
            name_column = lst_svod_cols[idx]
            name_column = re.sub(r'[\[\]\'+()<> :"?*|\\/]', '_', name_column)
            name_column = name_column[:15]

            out_dct.update({f'Ср {name_column}': svod_mean_column_df,
                            f'КС {name_column}': svod_count_column_level_ks_df,
                            f'ДА {name_column}': svod_count_column_level_da_df,
                            f'ИТ {name_column}': svod_count_column_level_it_df,
                            f'КП {name_column}': svod_count_column_level_kp_df,
                            f'СП {name_column}': svod_count_column_level_sp_df,

                            f'М {name_column}': svod_count_column_level_m_df,
                            f'ДЦ {name_column}': svod_count_column_level_dc_df,
                            f'ПА {name_column}': svod_count_column_level_pa_df,
                            f'НН {name_column}': svod_count_column_level_nn_df,
                            f'АИ {name_column}': svod_count_column_level_ai_df,
                            f'К {name_column}': svod_count_column_level_k_df,
                            })
        return out_dct










def processing_ddna_dav_hlom(base_df: pd.DataFrame, answers_df: pd.DataFrame, lst_svod_cols:list):
    """
    Функция для обработки
    :param base_df: часть датафрейма с описательными колонками
    :param answers_df: часть датафрейма с ответами
    :param lst_svod_cols:  список с колонками по которым нужно делать свод
    """
    try:
        out_answer_df = base_df.copy()  # делаем копию для последующего соединения с сырыми ответами
        if len(answers_df.columns) != 66:  # проверяем количество колонок с вопросами
            raise BadCountColumnsDDNADH

        # очищаем названия колонок от возможных сочетаний .1 которые добавляет пандас при одинаковых колонках
        clean_df_lst = []
        for name_column in answers_df.columns:
            clean_name = re.sub(r'.\d+$', '', name_column)
            clean_df_lst.append(clean_name)

        answers_df.columns = clean_df_lst

        lst_check_cols = ['Все люди делятся на сильных и слабых',
                          'Добро должно быть с кулаками, уметь защитить себя',
                          'Исконный образ жизни моего народа можно защитить только силой',
                          'Люди не будут хорошо трудиться, если их не заставлять',
                          'При общении с приезжими надо показывать, кто в доме хозяин',
                          'Почти все разногласия можно решить с помощью переговоров',
                          'Если меня кто-то оскорбит, я могу действовать очень жестко',
                          'Часто попадаются люди, которые раздражают меня одним своим присутствием',
                          'Иногда невозможно удержаться от драки',
                          'Надписи на стенах — приемлемый способ выразить свое недовольство, если нет других путей',

                          'Не стоит церемониться с людьми, которые тебе не нравятся',
                          'Человека можно понять, если его разозлили, а он ударил в ответ или сломал какую-либо вещь',
                          'К некоторым нациям и народам трудно хорошо относиться',
                          'Каждый человек либо хороший, либо плохой',
                          'Мой принцип: «Никогда не доверять «чужакам»',
                          'Нормально считать, что твой народ лучше, чем все остальные',
                          'Я могу представить человека другой расы своим близким другом',
                          'Я хочу, чтобы среди моих друзей были люди разных национальностей',
                          'Мне всегда важно, чтобы обидчик был наказан, а жертва отомщена',
                          'Многие социальные проблемы будут решены, если мы избавимся от аморальных и малодушных людей',

                          'Прежде всего, нашему обществу нужна дисциплина и решительность в борьбе за наши исконные ценности',
                          'Оскорбление чести и достоинства всегда нужно карать',
                          'В нашем обществе добиться справедливости важнее, чем проявлять жалость к отдельным людям',
                          'Некоторые преступления заслуживают более тяжкого наказания, чем тюрьма: иногда преступников следует публично казнить',
                          'Вполне возможно, что эта серия войн и конфликтов раз и навсегда будет остановлена землетрясением, наводнением или иной катастрофой, которая уничтожит мир',
                          'В нашем обществе нет смысла быть честным и заботиться о среде обитания — все равно другие продолжают обманывать и все портить',
                          'Сегодня везде царит неуверенность, мы должны быть готовы к кризисам, жестким конфликтам и переворотам',
                          'Наше общество стоит на пороге гибели',
                          'Нет смысла в напряженной учебе или работе — все равно все достается тем, кого устроят родители',
                          'Я отлично знаю, что в этом обществе от меня ничего не зависит',

                          'Есть знаки, в которых скрыто особое знание',
                          'Каждый должен верить в свое предназначение, идти дорогой, которая предначертана судьбой',
                          'Люди не осознают, что наша жизнь управляется заговорами и тайными организациями',
                          'Наука не всегда полезна, поскольку существует много такого, что человеческий разум не в силах понять',
                          'От символов, которые используют люди, часто зависит их судьба',
                          'Тот, кто понимает тайное значение древних символов, может влиять на других людей',
                          'Безопаснее всего предполагать, что в каждом человеке есть злые черты, которые вылезут на поверхность при возможности',
                          'Все продается и все покупается, вопрос только в цене',
                          'Мне не нравятся большинство окружающих меня людей и вообще мир вокруг',
                          'Человек человеку волк, и все заботятся лишь о себе',

                          'Чем больше возможностей, тем вероятнее, что человек ступит на плохой путь',
                          'Со всеми людьми можно найти общий язык',
                          'В наше время требуется больше увлеченных романтиков и энтузиастов',
                          'Люди, у которых нет планов преобразовать наше общество, кажутся мне странными',
                          'Известности и признания заслуживают только смелые люди, действующие наперекор пассивному большинству',
                          'Худший недостаток — быть занудным человеком, который всегда действует по инструкции',
                          'Человека, который много сделал для человечества, можно простить за жесткие поступки и неуживчивый характер',
                          'Я считаю, что люди должны быть способны отдать жизнь за свои идеи',
                          'Нам нужны не программы и законы, а несколько храбрых, неутомимых и преданных лидеров, в которых люди могут верить',
                          'Правы люди, которые всегда следуют пословице: «Если нельзя, но очень хочется, то можно»',

                          'Среди тех, кто сидит в тюрьме, многие — настоящие герои',
                          'Только слабые и трусливые люди стремятся выполнять все правила и законы',
                          'Законы у нас принимают для того, чтобы в стране был порядок',
                          'Работа полицейских всегда заслуживает уважения',
                          'Бизнесмен или хороший менеджер сейчас важнее для общества, чем художник или профессор',
                          'Нашему народу нужно меньше рассуждать и больше заниматься конкретными делами',
                          'Никому не интересны переживания разных интеллигентов',
                          'Обсуждение разных взглядов только запутывает людей — решение многих социальных проблем лежит на поверхности',
                          'Слишком часто люди выносят свою личную жизнь наружу',
                          'Рассказы, повествующие о мыслях и чувствах, читать интереснее, чем те, где описываются поступки или приключения',

                          'Если точку зрения разделяет большинство моих друзей, значит, она верная',
                          'Обычно я делаю то, о чем меня просят друзья, даже если это не нравится другим',
                          'Я всегда поддержу своих друзей, даже если общество против них',
                          'Я часто развлекаюсь в компании с друзьями, хотя мне не совсем по душе некоторые наши проделки',
                          'Драться за честь своей команды — почетнее, чем быть успешным индивидуалистом',
                          'Надо пройти через опасности и испытания, чтобы тебя приняли в команду настоящих друзей',

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
            raise BadOrderDDNADH

        # словарь для замены слов на числа
        dct_replace_value = {'категорически не согласен': 1,
                             'не согласен': 2,
                             'затрудняюсь ответить': 3,
                             'согласен': 4,
                             'полностью согласен': 5,
                             }
        valid_values = [1, 2, 3, 4,5]
        answers_df.replace(dct_replace_value, inplace=True)  # заменяем слова на цифры для подсчетов
        # Проверяем, есть ли значения, отличающиеся от указанных в списке
        lst_error_answers = []  # список для хранения строк где найдены неправильные ответы

        for i in range(66):
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
            raise BadValueDDNADH

        base_df['КС_Значение'] = answers_df.apply(calc_value_ks, axis=1)
        base_df['КС_Диапазон'] = base_df['КС_Значение'].apply(calc_level)

        base_df['ДА_Значение'] = answers_df.apply(calc_value_da, axis=1)
        base_df['ДА_Диапазон'] = base_df['ДА_Значение'].apply(calc_level)

        base_df['ИТ_Значение'] = answers_df.apply(calc_value_it, axis=1)
        base_df['ИТ_Диапазон'] = base_df['ИТ_Значение'].apply(calc_level)

        base_df['КП_Значение'] = answers_df.apply(calc_value_kp, axis=1)
        base_df['КП_Диапазон'] = base_df['КП_Значение'].apply(calc_level)

        base_df['СП_Значение'] = answers_df.apply(calc_value_sp, axis=1)
        base_df['СП_Диапазон'] = base_df['СП_Значение'].apply(calc_level)

        base_df['М_Значение'] = answers_df.apply(calc_value_m, axis=1)
        base_df['М_Диапазон'] = base_df['М_Значение'].apply(calc_level)

        base_df['ДЦ_Значение'] = answers_df.apply(calc_value_dc, axis=1)
        base_df['ДЦ_Диапазон'] = base_df['ДЦ_Значение'].apply(calc_level)

        base_df['ПА_Значение'] = answers_df.apply(calc_value_pa, axis=1)
        base_df['ПА_Диапазон'] = base_df['ПА_Значение'].apply(calc_level)

        base_df['НН_Значение'] = answers_df.apply(calc_value_nn, axis=1)
        base_df['НН_Диапазон'] = base_df['НН_Значение'].apply(calc_level)

        base_df['АИ_Значение'] = answers_df.apply(calc_value_ai, axis=1)
        base_df['АИ_Диапазон'] = base_df['АИ_Значение'].apply(calc_level)

        base_df['К_Значение'] = answers_df.apply(calc_value_k, axis=1)
        base_df['К_Диапазон'] = base_df['К_Значение'].apply(calc_level)


        # Создаем датафрейм для создания части в общий датафрейм
        part_df = pd.DataFrame()

        # Основные шкалы
        part_df['ДДНЭДХ_КС_Значение'] = base_df['КС_Значение']
        part_df['ДДНЭДХ_КС_Диапазон'] = base_df['КС_Диапазон']

        part_df['ДДНЭДХ_ДА_Значение'] = base_df['ДА_Значение']
        part_df['ДДНЭДХ_ДА_Диапазон'] = base_df['ДА_Диапазон']

        part_df['ДДНЭДХ_ИТ_Значение'] = base_df['ИТ_Значение']
        part_df['ДДНЭДХ_ИТ_Диапазон'] = base_df['ИТ_Диапазон']

        part_df['ДДНЭДХ_КП_Значение'] = base_df['КП_Значение']
        part_df['ДДНЭДХ_КП_Диапазон'] = base_df['КП_Диапазон']

        part_df['ДДНЭДХ_СП_Значение'] = base_df['СП_Значение']
        part_df['ДДНЭДХ_СП_Диапазон'] = base_df['СП_Диапазон']

        part_df['ДДНЭДХ_М_Значение'] = base_df['М_Значение']
        part_df['ДДНЭДХ_М_Диапазон'] = base_df['М_Диапазон']

        part_df['ДДНЭДХ_ДЦ_Значение'] = base_df['ДЦ_Значение']
        part_df['ДДНЭДХ_ДЦ_Диапазон'] = base_df['ДЦ_Диапазон']

        part_df['ДДНЭДХ_ПА_Значение'] = base_df['ПА_Значение']
        part_df['ДДНЭДХ_ПА_Диапазон'] = base_df['ПА_Диапазон']

        part_df['ДДНЭДХ_НН_Значение'] = base_df['НН_Значение']
        part_df['ДДНЭДХ_НН_Диапазон'] = base_df['НН_Диапазон']

        part_df['ДДНЭДХ_АИ_Значение'] = base_df['АИ_Значение']
        part_df['ДДНЭДХ_АИ_Диапазон'] = base_df['АИ_Диапазон']

        part_df['ДДНЭДХ_К_Значение'] = base_df['К_Значение']
        part_df['ДДНЭДХ_К_Диапазон'] = base_df['К_Диапазон']

        part_df.replace({'6-12':'6-12 ДДНЭ','13-19':'13-19 ДДНЭ','20-23':'20-23 ДДНЭ','24-26':'24-26 ДДНЭ','28-30':'28-30 ДДНЭ'},inplace=True)

        out_answer_df = pd.concat([out_answer_df, answers_df], axis=1)  # Датафрейм для проверки

        base_df.sort_values(by='ДЦ_Значение', ascending=False, inplace=True)  # сортируем

        # Делаем свод  по  шкалам
        dct_svod_sub = {'КС_Значение': 'КС_Диапазон',
                        'ДА_Значение': 'ДА_Диапазон',
                        'ИТ_Значение': 'ИТ_Диапазон',
                        'КП_Значение': 'КП_Диапазон',
                        'СП_Значение': 'СП_Диапазон',

                        'М_Значение': 'М_Диапазон',
                        'ДЦ_Значение': 'ДЦ_Диапазон',
                        'ПА_Значение': 'ПА_Диапазон',
                        'НН_Значение': 'НН_Диапазон',
                        'АИ_Значение': 'АИ_Диапазон',
                        'К_Значение': 'К_Диапазон'
                        }

        dct_rename_svod_sub = {'КС_Значение': 'Диапазон шкалы Культ силы',
                               'ДА_Значение': 'Диапазон шкалы Допустимость агрессии',
                               'ИТ_Значение': 'Диапазон шкалы Интолерантность',
                               'КП_Значение': 'Диапазон шкалы Конвенциональное принуждение',
                               'СП_Значение': 'Диапазон шкалы Социальный пессимизм',

                               'М_Значение': 'Диапазон шкалы Мистичность',
                               'ДЦ_Значение': 'Диапазон шкалы Деструктивность и цинизм',
                               'ПА_Значение': 'Диапазон шкалы Протестная активность',
                               'НН_Значение': 'Диапазон шкалы Нормативный нигилизм',
                               'АИ_Значение': 'Диапазон шкалы Антиинтрацепция',
                               'К_Значение': 'Диапазон шкалы Конформизм'
                               }

        lst_sub = ['6-12','13-19','20-23','24-26','28-30']

        base_svod_sub_df = create_union_svod(base_df, dct_svod_sub, dct_rename_svod_sub, lst_sub)

        avg_ks = round(base_df['КС_Значение'].mean(), 2)
        avg_da = round(base_df['ДА_Значение'].mean(), 2)
        avg_it = round(base_df['ИТ_Значение'].mean(), 2)
        avg_kp = round(base_df['КП_Значение'].mean(), 2)
        avg_sp = round(base_df['СП_Значение'].mean(), 2)

        avg_m = round(base_df['М_Значение'].mean(), 2)
        avg_dc = round(base_df['ДЦ_Значение'].mean(), 2)
        avg_pa = round(base_df['ПА_Значение'].mean(), 2)
        avg_nn = round(base_df['НН_Значение'].mean(), 2)
        avg_ai = round(base_df['АИ_Значение'].mean(), 2)
        avg_k = round(base_df['К_Значение'].mean(), 2)

        avg_dct = {'Среднее значение шкалы Культ силы': avg_ks,
                   'Среднее значение шкалы Допустимость агрессии': avg_da,
                   'Среднее значение шкалы Интолерантность': avg_it,
                   'Среднее значение шкалы Конвенциональное принуждение': avg_kp,
                   'Среднее значение шкалы Социальный пессимизм': avg_sp,

                   'Среднее значение шкалы Мистичность': avg_m,
                   'Среднее значение шкалы Деструктивность и цинизм': avg_dc,
                   'Среднее значение шкалы Протестная активность': avg_pa,
                   'Среднее значение шкалы Нормативный нигилизм': avg_nn,
                   'Среднее значение шкалы Антиинтрацепция': avg_ai,
                   'Среднее значение шкалы Конформизм': avg_k,
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

        dct_prefix = {
            'КС_Диапазон': 'КС',
            'ДА_Диапазон': 'ДА',
            'ИТ_Диапазон': 'ИТ',
            'КП_Диапазон': 'КП',
            'СП_Диапазон': 'СП',

            'М_Диапазон': 'М',
            'ДЦ_Диапазон': 'ДЦ',
            'ПА_Диапазон': 'ПА',
            'НН_Диапазон': 'НН',
            'АИ_Диапазон': 'АИ',
            'К_Диапазон': 'К',
        }

        out_dct = create_list_on_level(base_df, out_dct, lst_sub, dct_prefix)

        """
                        Сохраняем в зависимости от необходимости делать своды по определенным колонкам
                        """
        if len(lst_svod_cols) == 0:
            return out_dct, part_df

        else:
            out_dct = create_result_ddna_dav_hlo(base_df, out_dct, lst_svod_cols)
            return out_dct, part_df


    except BadOrderDDNADH:
        messagebox.showerror('Лахеcис',
                             f'При обработке вопросов теста Методика диагностики диспозиций насильственного экстремизма Давыдов Хломов обнаружены неправильные вопросы. Проверьте названия колонок с вопросами:\n'
                             f'{error_order_message[:5000]}\n'
                             f'Используйте при создании Яндекс-формы написание вопросов из руководства пользователя программы Лахесис.')
    except BadValueDDNADH:
        messagebox.showerror('Лахеcис',
                             f'При обработке вопросов теста Методика диагностики диспозиций насильственного экстремизма Давыдов Хломов обнаружены неправильные варианты ответов. Проверьте ответы на указанных строках:\n'
                             f'{error_message[:5000]}\n'
                             f'Используйте при создании Яндекс-формы написание вариантов ответа из руководства пользователя программы Лахесис.')


    except BadCountColumnsDDNADH:
        messagebox.showerror('Лахеcис',
                             f'Проверьте количество колонок с ответами на тест Методика диагностики диспозиций насильственного экстремизма Давыдов Хломов\n'
                             f'Должно быть 66 колонок с ответами')



