"""
Скрипт для обработки результатов Опросник благополучия PERMA-Profiler Исаева, Акимова, Волкова
"""

import pandas as pd
import re
from tkinter import messagebox
from lachesis_support_functions import round_mean_two,calc_count_scale,create_union_svod, create_list_on_level

class BadOrderOBIAV(Exception):
    """
    Исключение для обработки случая когда колонки не совпадают
    """
    pass


class BadValueOBIAV(Exception):
    """
    Исключение для неправильных значений в вариантах ответов
    """
    pass

class BadCountColumnsOBIAV(Exception):
    """
    Исключение для обработки случая если количество колонок не равно 23
    """
    pass


def calc_level_opb(value):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """
    if value < 6.19:
        return f'низкий уровень'
    elif 6.19<= value <= 8.25 :
        return f'средний уровень'
    else:
        return f'высокий уровень'

def calc_value_opb(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [1,5,15,2,10,17,3,
              13,22,7,9,20,8,19,21,23]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_pr:
            value_forward += value

    return round(value_forward/16,2)

def calc_value_pa(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [3,13,22]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_pr:
            value_forward += value

    return round(value_forward/3,2)

def calc_level_pa(value):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """
    if value < 6.33:
        return f'низкий уровень'
    elif 6.33<= value <=8.67:
        return f'средний уровень'
    else:
        return f'высокий уровень'


def calc_value_vv(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [2,10,17]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_pr:
            value_forward += value


    return round(value_forward/3,2)

def calc_level_vv(value):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """
    if value <6.00:
        return f'низкий уровень'
    elif 6.00<= value <=8.33:
        return f'средний уровень'
    else:
        return f'высокий уровень'


def calc_value_vo(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [8,19,21]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_pr:
            value_forward += value


    return round(value_forward/3,2)



def calc_level_vo(value):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """
    if value <5.67:
        return f'низкий уровень'
    elif 5.67<= value <=8.67:
        return f'средний уровень'
    else:
        return f'высокий уровень'


def calc_value_s(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [7,9,20]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_pr:
            value_forward += value


    return round(value_forward/3,2)



def calc_level_s(value):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """
    if value <6.00:
        return f'низкий уровень'
    elif 6.00<= value <=8.33:
        return f'средний уровень'
    else:
        return f'высокий уровень'


def calc_value_d(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [1,5,15]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_pr:
            value_forward += value


    return round(value_forward/3,2)



def calc_level_d(value):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """
    if value <6.33:
        return f'низкий уровень'
    elif 6.33<= value <=8.33:
        return f'средний уровень'
    else:
        return f'высокий уровень'


def calc_value_ch(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [23]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_pr:
            value_forward += value


    return round(value_forward/1,2)



def calc_level_ch(value):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """
    if value <6.25:
        return f'низкий уровень'
    elif 6.25<= value <=8.25:
        return f'средний уровень'
    else:
        return f'высокий уровень'


def calc_value_na(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [4,14,16]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_pr:
            value_forward += value


    return round(value_forward/3,2)



def calc_level_na(value):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """
    if value <4.33:
        return f'низкий уровень'
    elif 4.33<= value <=7.00:
        return f'средний уровень'
    else:
        return f'высокий уровень'

def calc_value_z(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [6,12,18]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_pr:
            value_forward += value


    return round(value_forward/3,2)



def calc_level_z(value):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """
    if value <5.33:
        return f'низкий уровень'
    elif 5.33<= value <=8.00:
        return f'средний уровень'
    else:
        return f'высокий уровень'


def calc_value_o(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [11]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_pr:
            value_forward += value


    return round(value_forward/1,2)



def calc_level_o(value):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """
    if value <2.00:
        return f'низкий уровень'
    elif 2.00<= value <=7.0:
        return f'средний уровень'
    else:
        return f'высокий уровень'



def create_result_ob_isaeva(base_df:pd.DataFrame, out_dct:dict, lst_svod_cols:list):
    """
    Функция для подсчета результата если указаны колонки по которым нужно провести свод
    :param df: датафрейм с результатами
    :param out_dct: словарь с уже подсчитанными базовыми данными
    :param lst_svod_cols: список сводных колонок
    :return: словарь
    """

    lst_level = ['низкий уровень', 'средний уровень', 'высокий уровень']

    lst_reindex_one_level_cols = lst_svod_cols.copy()
    lst_reindex_one_level_cols.extend(['низкий уровень', 'средний уровень', 'высокий уровень',
                                       'Итого'])  # Основная шкала

    # АД
    svod_count_one_level_opb_df = calc_count_scale(base_df, lst_svod_cols,
                                                 'ОПБ_Значение',
                                                 'ОПБ_Уровень',
                                                 lst_reindex_one_level_cols, lst_level)
    # АВА
    svod_count_one_level_pa_df = calc_count_scale(base_df, lst_svod_cols,
                                                 'ПЭ_Значение',
                                                 'ПЭ_Уровень',
                                                 lst_reindex_one_level_cols, lst_level)

    svod_count_one_level_vv_df = calc_count_scale(base_df, lst_svod_cols,
                                                 'ВВ_Значение',
                                                 'ВВ_Уровень',
                                                 lst_reindex_one_level_cols, lst_level)

    # АД
    svod_count_one_level_vo_df = calc_count_scale(base_df, lst_svod_cols,
                                                 'ВО_Значение',
                                                 'ВО_Уровень',
                                                 lst_reindex_one_level_cols, lst_level)
    # АВА
    svod_count_one_level_s_df = calc_count_scale(base_df, lst_svod_cols,
                                                 'С_Значение',
                                                 'С_Уровень',
                                                 lst_reindex_one_level_cols, lst_level)

    svod_count_one_level_d_df = calc_count_scale(base_df, lst_svod_cols,
                                                 'Д_Значение',
                                                 'Д_Уровень',
                                                 lst_reindex_one_level_cols, lst_level)

    # АД
    svod_count_one_level_ch_df = calc_count_scale(base_df, lst_svod_cols,
                                                 'СЧ_Значение',
                                                 'СЧ_Уровень',
                                                 lst_reindex_one_level_cols, lst_level)
    # АВА
    svod_count_one_level_na_df = calc_count_scale(base_df, lst_svod_cols,
                                                 'НЭ_Значение',
                                                 'НЭ_Уровень',
                                                 lst_reindex_one_level_cols, lst_level)

    svod_count_one_level_z_df = calc_count_scale(base_df, lst_svod_cols,
                                                 'З_Значение',
                                                 'З_Уровень',
                                                 lst_reindex_one_level_cols, lst_level)
    svod_count_one_level_o_df = calc_count_scale(base_df, lst_svod_cols,
                                                 'О_Значение',
                                                 'О_Уровень',
                                                 lst_reindex_one_level_cols, lst_level)

    # Считаем среднее по субшкалам
    svod_mean_one_df = pd.pivot_table(base_df,
                                      index=lst_svod_cols,
                                      values=['ОПБ_Значение',
                                              'ПЭ_Значение',
                                              'ВВ_Значение',
                                              'ВО_Значение',
                                              'С_Значение',

                                              'Д_Значение',
                                              'СЧ_Значение',
                                              'НЭ_Значение',
                                              'З_Значение',
                                              'О_Значение',
                                              ],
                                      aggfunc=round_mean_two)
    svod_mean_one_df.reset_index(inplace=True)

    # упорядочиваем колонки
    new_order_cols = lst_svod_cols.copy()
    new_order_cols.extend((['ОПБ_Значение',
                            'ПЭ_Значение',
                            'ВВ_Значение',
                            'ВО_Значение',
                            'С_Значение',

                            'Д_Значение',
                            'СЧ_Значение',
                            'НЭ_Значение',
                            'З_Значение',
                            'О_Значение',
                            ]))
    svod_mean_one_df = svod_mean_one_df.reindex(columns=new_order_cols)

    dct_rename_cols_mean = {'ОПБ_Значение': 'Ср. Общий показатель благополучия PERMA',
                            'ПЭ_Значение': 'Ср. Позитивные эмоции',
                            'ВВ_Значение': 'Ср. Вовлеченность',
                            'ВО_Значение': 'Ср. Взаимоотношения',
                            'С_Значение': 'Ср. Смысл',

                            'Д_Значение': 'Ср. Достижения',
                            'СЧ_Значение': 'Ср. Счастье',
                            'НЭ_Значение': 'Ср. Негативные эмоции',
                            'З_Значение': 'Ср. Здоровье',
                            'О_Значение': 'Ср. Одиночество',
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
                    f'ОПБ {out_name}': svod_count_one_level_opb_df,
                    f'ПЭ {out_name}': svod_count_one_level_pa_df,
                    f'ВВ {out_name}': svod_count_one_level_vv_df,
                    f'ВО {out_name}': svod_count_one_level_vo_df,
                    f'С {out_name}': svod_count_one_level_s_df,

                    f'Д {out_name}': svod_count_one_level_d_df,
                    f'СЧ {out_name}': svod_count_one_level_ch_df,
                    f'НЭ {out_name}': svod_count_one_level_na_df,
                    f'З {out_name}': svod_count_one_level_z_df,
                    f'О {out_name}': svod_count_one_level_o_df,
                    })

    if len(lst_svod_cols) == 1:
        return out_dct
    else:
        for idx, name_column in enumerate(lst_svod_cols):
            lst_reindex_column_level_cols = [lst_svod_cols[idx], 'низкий уровень', 'средний уровень', 'высокий уровень',
                                             'Итого']

            # АД
            svod_count_column_level_opb_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                              'ОПБ_Значение',
                                                              'ОПБ_Уровень',
                                                              lst_reindex_column_level_cols, lst_level)
            # АВА
            svod_count_column_level_pa_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                             'ПЭ_Значение',
                                                             'ПЭ_Уровень',
                                                             lst_reindex_column_level_cols, lst_level)

            svod_count_column_level_vv_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                             'ВВ_Значение',
                                                             'ВВ_Уровень',
                                                             lst_reindex_column_level_cols, lst_level)

            # АД
            svod_count_column_level_vo_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                             'ВО_Значение',
                                                             'ВО_Уровень',
                                                             lst_reindex_column_level_cols, lst_level)
            # АВА
            svod_count_column_level_s_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                            'С_Значение',
                                                            'С_Уровень',
                                                            lst_reindex_column_level_cols, lst_level)

            svod_count_column_level_d_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                            'Д_Значение',
                                                            'Д_Уровень',
                                                            lst_reindex_column_level_cols, lst_level)

            # АД
            svod_count_column_level_ch_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                             'СЧ_Значение',
                                                             'СЧ_Уровень',
                                                             lst_reindex_column_level_cols, lst_level)
            # АВА
            svod_count_column_level_na_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                             'НЭ_Значение',
                                                             'НЭ_Уровень',
                                                             lst_reindex_column_level_cols, lst_level)

            svod_count_column_level_z_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                            'З_Значение',
                                                            'З_Уровень',
                                                            lst_reindex_column_level_cols, lst_level)
            svod_count_column_level_o_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                            'О_Значение',
                                                            'О_Уровень',
                                                            lst_reindex_column_level_cols, lst_level)

            # Считаем среднее по субшкалам
            svod_mean_column_df = pd.pivot_table(base_df,
                                              index=[lst_svod_cols[idx]],
                                              values=['ОПБ_Значение',
                                                      'ПЭ_Значение',
                                                      'ВВ_Значение',
                                                      'ВО_Значение',
                                                      'С_Значение',

                                                      'Д_Значение',
                                                      'СЧ_Значение',
                                                      'НЭ_Значение',
                                                      'З_Значение',
                                                      'О_Значение',
                                                      ],
                                              aggfunc=round_mean_two)
            svod_mean_column_df.reset_index(inplace=True)

            # упорядочиваем колонки
            new_order_cols = [lst_svod_cols[idx]].copy()
            new_order_cols.extend((['ОПБ_Значение',
                                    'ПЭ_Значение',
                                    'ВВ_Значение',
                                    'ВО_Значение',
                                    'С_Значение',

                                    'Д_Значение',
                                    'СЧ_Значение',
                                    'НЭ_Значение',
                                    'З_Значение',
                                    'О_Значение',
                                    ]))
            svod_mean_column_df = svod_mean_column_df.reindex(columns=new_order_cols)

            dct_rename_cols_mean = {'ОПБ_Значение': 'Ср. Общий показатель благополучия PERMA',
                                    'ПЭ_Значение': 'Ср. Позитивные эмоции',
                                    'ВВ_Значение': 'Ср. Вовлеченность',
                                    'ВО_Значение': 'Ср. Взаимоотношения',
                                    'С_Значение': 'Ср. Смысл',

                                    'Д_Значение': 'Ср. Достижения',
                                    'СЧ_Значение': 'Ср. Счастье',
                                    'НЭ_Значение': 'Ср. Негативные эмоции',
                                    'З_Значение': 'Ср. Здоровье',
                                    'О_Значение': 'Ср. Одиночество',
                                    }
            svod_mean_column_df.rename(columns=dct_rename_cols_mean, inplace=True)
            # Готовим наименование
            name_column = lst_svod_cols[idx]
            name_column = re.sub(r'[\[\]\'+()<> :"?*|\\/]', '_', name_column)
            name_column = name_column[:15]
            out_dct.update({f'Ср {name_column}': svod_mean_column_df,
                            f'ОПБ {name_column}': svod_count_column_level_opb_df,
                            f'ПЭ {name_column}': svod_count_column_level_pa_df,
                            f'ВВ {name_column}': svod_count_column_level_vv_df,
                            f'ВО {name_column}': svod_count_column_level_vo_df,
                            f'С {name_column}': svod_count_column_level_s_df,

                            f'Д {name_column}': svod_count_column_level_d_df,
                            f'СЧ {name_column}': svod_count_column_level_ch_df,
                            f'НЭ {name_column}': svod_count_column_level_na_df,
                            f'З {name_column}': svod_count_column_level_z_df,
                            f'О {name_column}': svod_count_column_level_o_df,
                            })
        return out_dct







def processing_ob_isaeva(base_df: pd.DataFrame, answers_df: pd.DataFrame, lst_svod_cols:list):
    """
    Функция для обработки
    :param base_df: часть датафрейма с описательными колонками
    :param answers_df: часть датафрейма с ответами
    :param lst_svod_cols:  список с колонками по которым нужно делать свод
    """
    try:
        out_answer_df = base_df.copy()  # делаем копию для последующего соединения с сырыми ответами
        if len(answers_df.columns) != 23:  # проверяем количество колонок с вопросами
            raise BadCountColumnsOBIAV

        # очищаем названия колонок от возможных сочетаний .1 которые добавляет пандас при одинаковых колонках
        clean_df_lst = []
        for name_column in answers_df.columns:
            clean_name = re.sub(r'.\d+$', '', name_column)
            clean_df_lst.append(clean_name)

        answers_df.columns = clean_df_lst
        lst_check_cols = ['Как часто Вы чувствуете, что приближаетесь к своей цели?',
                          'Как часто Вы бываете полностью поглощены тем, что делаете?',
                          'Как часто Вы испытываете радость?',
                          'Как часто Вы испытываете беспокойство?',
                          'Как часто Вы достигаете важных целей, которые ставите перед собой?',
                          'В целом, как Вы оцениваете Ваше здоровье?',
                          'В какой степени Вы целеустремлённы и живете полной/осмысленной жизнью?',
                          'В какой степени Вы удовлетворены тем, какую помощь и поддержку от других Вы получаете, когда в ней нуждаетесь?',
                          'В какой степени Вы считаете, что то, что Вы делаете в своей жизни, полезно и ценно?',
                          'Как Вам кажется, насколько Вы увлечены или заинтересованы в чем-то?',

                          'Насколько одиноким Вы себя чувствуете в этой жизни?',
                          'Насколько Вы удовлетворены своим нынешним физическим здоровьем?',
                          'Как часто Вы испытываете положительные (позитивные) эмоции?',
                          'Как часто Вы злитесь?',
                          'Как часто Вы выполняете возложенные на Вас обязанности?',
                          'Как часто Вам бывает грустно?',
                          'Как часто Вы бываете чем-то так сильно увлечены, что теряете счет времени?',
                          'По сравнению с другими людьми того же возраста и пола как Вы оцениваете Ваше здоровье?',
                          'В какой степени Вы чувствуете себя любимым?',
                          'Насколько, как Вам кажется, Ваша жизнь имеет цель, и Вы движетесь к этой цели?',

                          'Насколько Вы довольны взаимоотношениями в личной жизни?',
                          'В целом, насколько Вы довольны своей жизнью?',
                          'В целом, как Вам кажется, насколько Вы счастливы?',
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
            raise BadOrderOBIAV

        answers_df = answers_df.astype(str) # делаем строковым на всякий случай

        # словарь для замены слов на числа
        dct_replace_value = {'0 – никогда, ужасно, совсем нет, минимально': 0,
                             '1': 1,
                             '2': 2,
                             '3': 3,
                             '4': 4,
                             '5': 5,
                             '6': 6,
                             '7': 7,
                             '8': 8,
                             '9': 9,
                             '10 – всегда, великолепно, максимум, максимально': 10,
                             }
        valid_values = [0, 1, 2, 3, 4,5,6,7,8,9,10]
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
            raise BadValueOBIAV

        base_df['ОПБ_Значение'] = answers_df.apply(calc_value_opb, axis=1)
        base_df['ОПБ_Уровень'] = base_df['ОПБ_Значение'].apply(calc_level_opb)

        base_df['ПЭ_Значение'] = answers_df.apply(calc_value_pa, axis=1)
        base_df['ПЭ_Уровень'] = base_df['ПЭ_Значение'].apply(calc_level_pa)

        base_df['ВВ_Значение'] = answers_df.apply(calc_value_vv, axis=1)
        base_df['ВВ_Уровень'] = base_df['ВВ_Значение'].apply(calc_level_vv)

        base_df['ВО_Значение'] = answers_df.apply(calc_value_vo, axis=1)
        base_df['ВО_Уровень'] = base_df['ВО_Значение'].apply(calc_level_vo)

        base_df['С_Значение'] = answers_df.apply(calc_value_s, axis=1)
        base_df['С_Уровень'] = base_df['С_Значение'].apply(calc_level_s)

        base_df['Д_Значение'] = answers_df.apply(calc_value_d, axis=1)
        base_df['Д_Уровень'] = base_df['Д_Значение'].apply(calc_level_d)

        base_df['СЧ_Значение'] = answers_df.apply(calc_value_ch, axis=1)
        base_df['СЧ_Уровень'] = base_df['СЧ_Значение'].apply(calc_level_ch)

        base_df['НЭ_Значение'] = answers_df.apply(calc_value_na, axis=1)
        base_df['НЭ_Уровень'] = base_df['НЭ_Значение'].apply(calc_level_na)

        base_df['З_Значение'] = answers_df.apply(calc_value_z, axis=1)
        base_df['З_Уровень'] = base_df['З_Значение'].apply(calc_level_z)

        base_df['О_Значение'] = answers_df.apply(calc_value_o, axis=1)
        base_df['О_Уровень'] = base_df['О_Значение'].apply(calc_level_o)

        # Создаем датафрейм для создания части в общий датафрейм
        part_df = pd.DataFrame()

        # Основные шкалы
        part_df['ОБИАВ_ОПБ_Значение'] = base_df['ОПБ_Значение']
        part_df['ОБИАВ_ОПБ_Уровень'] = base_df['ОПБ_Уровень']

        part_df['ОБИАВ_ПЭ_Значение'] = base_df['ПЭ_Значение']
        part_df['ОБИАВ_ПЭ_Уровень'] = base_df['ПЭ_Уровень']

        part_df['ОБИАВ_ВВ_Значение'] = base_df['ВВ_Значение']
        part_df['ОБИАВ_ВВ_Уровень'] = base_df['ВВ_Уровень']

        part_df['ОБИАВ_ВО_Значение'] = base_df['ВО_Значение']
        part_df['ОБИАВ_ВО_Уровень'] = base_df['ВО_Уровень']

        part_df['ОБИАВ_С_Значение'] = base_df['С_Значение']
        part_df['ОБИАВ_С_Уровень'] = base_df['С_Уровень']

        part_df['ОБИАВ_Д_Значение'] = base_df['Д_Значение']
        part_df['ОБИАВ_Д_Уровень'] = base_df['Д_Уровень']

        part_df['ОБИАВ_СЧ_Значение'] = base_df['СЧ_Значение']
        part_df['ОБИАВ_СЧ_Уровень'] = base_df['СЧ_Уровень']

        part_df['ОБИАВ_НЭ_Значение'] = base_df['НЭ_Значение']
        part_df['ОБИАВ_НЭ_Уровень'] = base_df['НЭ_Уровень']

        part_df['ОБИАВ_З_Значение'] = base_df['З_Значение']
        part_df['ОБИАВ_З_Уровень'] = base_df['З_Уровень']

        part_df['ОБИАВ_О_Значение'] = base_df['О_Значение']
        part_df['ОБИАВ_О_Уровень'] = base_df['О_Уровень']

        out_answer_df = pd.concat([out_answer_df, answers_df], axis=1)  # Датафрейм для проверки

        base_df.sort_values(by='ОПБ_Значение', ascending=True, inplace=True)  # сортируем




        # Делаем свод  по  шкалам
        dct_svod_sub = {'ОПБ_Значение': 'ОПБ_Уровень',
                        'ПЭ_Значение': 'ПЭ_Уровень',
                        'ВВ_Значение': 'ВВ_Уровень',
                        'ВО_Значение': 'ВО_Уровень',
                        'С_Значение': 'С_Уровень',

                        'Д_Значение': 'Д_Уровень',
                        'СЧ_Значение': 'СЧ_Уровень',
                        'НЭ_Значение': 'НЭ_Уровень',
                        'З_Значение': 'З_Уровень',
                        'О_Значение': 'О_Уровень',
                        }

        dct_rename_svod_sub = {'ОПБ_Значение': 'Общий показатель благополучия PERMA"',
                               'ПЭ_Значение': 'Позитивные эмоции',
                               'ВВ_Значение': 'Вовлеченность',
                               'ВО_Значение': 'Взаимоотношения',
                               'С_Значение': 'Смысл',

                               'Д_Значение': 'Достижения',
                               'СЧ_Значение': 'Счастье',
                               'НЭ_Значение': 'Негативные эмоции',
                               'З_Значение': 'Здоровье',
                               'О_Значение': 'Одиночество',
                               }

        lst_sub = ['низкий уровень', 'средний уровень', 'высокий уровень']

        base_svod_sub_df = create_union_svod(base_df, dct_svod_sub, dct_rename_svod_sub, lst_sub)

        avg_opb = round(base_df['ОПБ_Значение'].mean(), 2)
        avg_pa = round(base_df['ПЭ_Значение'].mean(), 2)
        avg_vv = round(base_df['ВВ_Значение'].mean(), 2)
        avg_vo = round(base_df['ВО_Значение'].mean(), 2)
        avg_s = round(base_df['С_Значение'].mean(), 2)

        avg_d = round(base_df['Д_Значение'].mean(), 2)
        avg_ch = round(base_df['СЧ_Значение'].mean(), 2)
        avg_na = round(base_df['НЭ_Значение'].mean(), 2)
        avg_z = round(base_df['З_Значение'].mean(), 2)
        avg_o = round(base_df['О_Значение'].mean(), 2)

        avg_dct = {'Среднее значение шкалы Общий показатель благополучия PERMA': avg_opb,
                   'Среднее значение шкалы Позитивные эмоции': avg_pa,
                   'Среднее значение шкалы Вовлеченность': avg_vv,
                   'Среднее значение шкалы Взаимоотношения': avg_vo,
                   'Среднее значение шкалы Смысл': avg_s,

                   'Среднее значение шкалы Достижения': avg_d,
                   'Среднее значение шкалы Счастье': avg_ch,
                   'Среднее значение шкалы Негативные эмоции': avg_na,
                   'Среднее значение шкалы Здоровье': avg_z,
                   'Среднее значение шкалы Одиночество': avg_o,
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
            'ОПБ_Уровень': 'ОПБ',
            'ПЭ_Уровень': 'ПЭ',
            'ВВ_Уровень': 'ВВ',
            'ВО_Уровень': 'ВО',
            'С_Уровень': 'С',

            'Д_Уровень': 'Д',
            'СЧ_Уровень': 'СЧ',
            'НЭ_Уровень': 'НЭ',
            'З_Уровень': 'З',
            'О_Уровень': 'О',
        }

        out_dct = create_list_on_level(base_df, out_dct, lst_sub, dct_prefix)

        """
                        Сохраняем в зависимости от необходимости делать своды по определенным колонкам
                        """
        if len(lst_svod_cols) == 0:
            return out_dct, part_df

        else:
            out_dct = create_result_ob_isaeva(base_df, out_dct, lst_svod_cols)
            return out_dct, part_df

    except BadOrderOBIAV:
        messagebox.showerror('Лахеcис',
                             f'При обработке вопросов теста Опросник благополучия PERMA-Profiler Исаева, Акимова, Волкова обнаружены неправильные вопросы. Проверьте названия колонок с вопросами:\n'
                             f'{error_order_message[:5000]}\n'
                             f'Используйте при создании Яндекс-формы написание вопросов из руководства пользователя программы Лахесис.')
    except BadValueOBIAV:
        messagebox.showerror('Лахеcис',
                             f'При обработке вопросов теста Опросник благополучия PERMA-Profiler Исаева, Акимова, Волкова обнаружены неправильные варианты ответов. Проверьте ответы на указанных строках:\n'
                             f'{error_message[:5000]}\n'
                             f'Используйте при создании Яндекс-формы написание вариантов ответа из руководства пользователя программы Лахесис.')


    except BadCountColumnsOBIAV:
        messagebox.showerror('Лахеcис',
                             f'Проверьте количество колонок с ответами на тест Опросник благополучия PERMA-Profiler Исаева, Акимова, Волкова\n'
                             f'Должно быть 23 колонки с ответами')












