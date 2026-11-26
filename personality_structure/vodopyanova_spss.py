"""
Скрипт для обработки результатов Стратегия преодоления стрессовых ситуаций, SACS Хобфолл С., 1994
Адаптация Н.Е. Водопьянова, Е.С. Старченкова

"""

import pandas as pd
import re
from tkinter import messagebox
from lachesis_support_functions import round_mean_two,calc_count_scale,create_union_svod, create_list_on_level

class BadOrderSPSSVS(Exception):
    """
    Исключение для обработки случая когда колонки не совпадают
    """
    pass


class BadValueSPSSVS(Exception):
    """
    Исключение для неправильных значений в вариантах ответов
    """
    pass

class BadCountColumnsSPSSVS(Exception):
    """
    Исключение для обработки случая если количество колонок не равно 54
    """
    pass


def calc_value_ad(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [1,10,19,28,37,46]
    lst_neg = [28,46]
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

def calc_level_ad(value):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """
    if 6<= value <=17:
        return f'низкая степень'
    elif 18<= value <=22:
        return f'средняя степень'
    else:
        return f'высокая степень'

def calc_value_vsk(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [2,11,20,29,38,47]
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


def calc_level_vsk(value):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """
    if 6<= value <=21:
        return f'низкая степень'
    elif 22<= value <=25 :
        return f'средняя степень'
    else:
        return f'высокая степень'

def calc_value_psp(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [3,12,21,30,39,48]
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


def calc_level_psp(value):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """
    if 6<= value <=19:
        return f'низкая степень'
    elif 20<= value <=24 :
        return f'средняя степень'
    else:
        return f'высокая степень'



def calc_value_od(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [4,13,22,31,40,49]
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


def calc_level_od(value):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """
    if 6<= value <=17:
        return f'низкая степень'
    elif 18<= value <=23 :
        return f'средняя степень'
    else:
        return f'высокая степень'


def calc_value_id(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [5,14,23,32,41,50]
    lst_neg = [50]
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


def calc_level_id(value):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """
    if 6<= value <=15:
        return f'низкая степень'
    elif 16<= value <=19 :
        return f'средняя степень'
    else:
        return f'высокая степень'


def calc_value_i(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [6,15,24,33,42,51]
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


def calc_level_i(value):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """
    if 6<= value <=12:
        return f'низкая степень'
    elif 13<= value <=17 :
        return f'средняя степень'
    else:
        return f'высокая степень'

def calc_value_nd(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [7,16,25,34,43,52]
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


def calc_level_nd(value):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """
    if 6<= value <=16:
        return f'низкая степень'
    elif 17<= value <=23 :
        return f'средняя степень'
    else:
        return f'высокая степень'


def calc_value_asd(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [8,17,26,35,44,53]
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


def calc_level_asd(value):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """
    if 6<= value <=14:
        return f'низкая степень'
    elif 15<= value <=19 :
        return f'средняя степень'
    else:
        return f'высокая степень'


def calc_value_agd(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [9,18,27,36,45,54]
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


def calc_level_agd(value):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """
    if 6<= value <=13:
        return f'низкая степень'
    elif 14<= value <= 18 :
        return f'средняя степень'
    else:
        return f'высокая степень'

def create_list_on_level_spssvs(base_df:pd.DataFrame, out_dct:dict, lst_level:list, dct_prefix:dict):
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
                if level == 'низкая степень':
                    level = 'низкая'
                elif level == 'средняя степень':
                    level = 'средняя'
                else:
                    level = 'высокая'
                dct_level[f'{dct_prefix[key]}. {level}'] = temp_df
        out_dct.update(dct_level)

    return out_dct


def create_result_spss_vod(base_df:pd.DataFrame, out_dct:dict, lst_svod_cols:list):
    """
    Функция для подсчета результата если указаны колонки по которым нужно провести свод
    :param df: датафрейм с результатами
    :param out_dct: словарь с уже подсчитанными базовыми данными
    :param lst_svod_cols: список сводных колонок
    :return: словарь
    """
    lst_level = ['низкая степень', 'средняя степень', 'высокая степень']

    lst_reindex_one_level_cols = lst_svod_cols.copy()
    lst_reindex_one_level_cols.extend(['низкая степень', 'средняя степень', 'высокая степень',
                                       'Итого'])  # Основная шкала
    svod_count_one_level_ad_df = calc_count_scale(base_df, lst_svod_cols,
                                                    'АД_Значение',
                                                    'АД_Степень',
                                                    lst_reindex_one_level_cols, lst_level)

    svod_count_one_level_vsk_df = calc_count_scale(base_df, lst_svod_cols,
                                                    'ВСК_Значение',
                                                    'ВСК_Степень',
                                                    lst_reindex_one_level_cols, lst_level)

    svod_count_one_level_psp_df = calc_count_scale(base_df, lst_svod_cols,
                                                    'ПСП_Значение',
                                                    'ПСП_Степень',
                                                    lst_reindex_one_level_cols, lst_level)


    svod_count_one_level_od_df = calc_count_scale(base_df, lst_svod_cols,
                                                    'ОД_Значение',
                                                    'ОД_Степень',
                                                    lst_reindex_one_level_cols, lst_level)

    svod_count_one_level_id_df = calc_count_scale(base_df, lst_svod_cols,
                                                    'ИД_Значение',
                                                    'ИД_Степень',
                                                    lst_reindex_one_level_cols, lst_level)

    svod_count_one_level_i_df = calc_count_scale(base_df, lst_svod_cols,
                                                    'И_Значение',
                                                    'И_Степень',
                                                    lst_reindex_one_level_cols, lst_level)

    svod_count_one_level_nd_df = calc_count_scale(base_df, lst_svod_cols,
                                                    'НД_Значение',
                                                    'НД_Степень',
                                                    lst_reindex_one_level_cols, lst_level)

    svod_count_one_level_asd_df = calc_count_scale(base_df, lst_svod_cols,
                                                    'АСД_Значение',
                                                    'АСД_Степень',
                                                    lst_reindex_one_level_cols, lst_level)

    svod_count_one_level_agd_df = calc_count_scale(base_df, lst_svod_cols,
                                                    'АГД_Значение',
                                                    'АГД_Степень',
                                                    lst_reindex_one_level_cols, lst_level)

    # Считаем среднее по субшкалам
    svod_mean_one_df = pd.pivot_table(base_df,
                                      index=lst_svod_cols,
                                      values=[
                                              'АД_Значение',
                                              'ВСК_Значение',
                                              'ПСП_Значение',

                                              'ОД_Значение',
                                              'ИД_Значение',
                                              'И_Значение',

                                              'НД_Значение',
                                              'АСД_Значение',
                                              'АГД_Значение',
                                              ],
                                      aggfunc=round_mean_two)
    svod_mean_one_df.reset_index(inplace=True)

    # упорядочиваем колонки
    new_order_cols = lst_svod_cols.copy()
    new_order_cols.extend(([ 'АД_Значение',
                                              'ВСК_Значение',
                                              'ПСП_Значение',

                                              'ОД_Значение',
                                              'ИД_Значение',
                                              'И_Значение',

                                              'НД_Значение',
                                              'АСД_Значение',
                                              'АГД_Значение',
                            ]))
    svod_mean_one_df = svod_mean_one_df.reindex(columns=new_order_cols)

    dct_rename_cols_mean = {'АД_Значение': 'Ср. Ассертивные действия',
                            'ВСК_Значение': 'Ср. Вступление в социальный контакт',
                            'ПСП_Значение': 'Ср. Поиск социальной поддержки',

                            'ОД_Значение': 'Ср. Осторожные действия',
                            'ИД_Значение': 'Ср. Импульсивные действия',
                            'И_Значение': 'Ср. Избегание',

                            'НД_Значение': 'Ср. Непрямые действия',
                            'АСД_Значение': 'Ср. Асоциальные действия',
                            'АГД_Значение': 'Ср. Агрессивные действия',
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
                    f'АД {out_name}': svod_count_one_level_ad_df,
                    f'ВСК {out_name}': svod_count_one_level_vsk_df,
                    f'ПСП {out_name}': svod_count_one_level_psp_df,

                    f'ОД {out_name}': svod_count_one_level_od_df,
                    f'ИД {out_name}': svod_count_one_level_id_df,
                    f'И {out_name}': svod_count_one_level_i_df,

                    f'НД {out_name}': svod_count_one_level_nd_df,
                    f'АСД {out_name}': svod_count_one_level_asd_df,
                    f'АГД {out_name}': svod_count_one_level_agd_df,
                    })

    if len(lst_svod_cols) == 1:
        return out_dct

    else:
        for idx, name_column in enumerate(lst_svod_cols):
            lst_reindex_column_level_cols = [lst_svod_cols[idx],'низкая степень', 'средняя степень', 'высокая степень',
                                                  'Итого']

            svod_count_column_level_ad_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                             'АД_Значение',
                                                             'АД_Степень',
                                                             lst_reindex_column_level_cols, lst_level)

            svod_count_column_level_vsk_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                              'ВСК_Значение',
                                                              'ВСК_Степень',
                                                              lst_reindex_column_level_cols, lst_level)

            svod_count_column_level_psp_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                              'ПСП_Значение',
                                                              'ПСП_Степень',
                                                              lst_reindex_column_level_cols, lst_level)

            svod_count_column_level_od_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                             'ОД_Значение',
                                                             'ОД_Степень',
                                                             lst_reindex_column_level_cols, lst_level)

            svod_count_column_level_id_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                             'ИД_Значение',
                                                             'ИД_Степень',
                                                             lst_reindex_column_level_cols, lst_level)

            svod_count_column_level_i_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                            'И_Значение',
                                                            'И_Степень',
                                                            lst_reindex_column_level_cols, lst_level)

            svod_count_column_level_nd_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                             'НД_Значение',
                                                             'НД_Степень',
                                                             lst_reindex_column_level_cols, lst_level)

            svod_count_column_level_asd_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                              'АСД_Значение',
                                                              'АСД_Степень',
                                                              lst_reindex_column_level_cols, lst_level)

            svod_count_column_level_agd_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                              'АГД_Значение',
                                                              'АГД_Степень',
                                                              lst_reindex_column_level_cols, lst_level)

            # Считаем среднее по субшкалам
            svod_mean_column_df = pd.pivot_table(base_df,
                                                 index=[lst_svod_cols[idx]],
                                                 values=[
                                                     'АД_Значение',
                                                     'ВСК_Значение',
                                                     'ПСП_Значение',

                                                     'ОД_Значение',
                                                     'ИД_Значение',
                                                     'И_Значение',

                                                     'НД_Значение',
                                                     'АСД_Значение',
                                                     'АГД_Значение',
                                                 ],
                                                 aggfunc=round_mean_two)
            svod_mean_column_df.reset_index(inplace=True)

            # упорядочиваем колонки
            new_order_cols = [lst_svod_cols[idx]].copy()
            new_order_cols.extend((['АД_Значение',
                                    'ВСК_Значение',
                                    'ПСП_Значение',

                                    'ОД_Значение',
                                    'ИД_Значение',
                                    'И_Значение',

                                    'НД_Значение',
                                    'АСД_Значение',
                                    'АГД_Значение',
                                    ]))
            svod_mean_column_df = svod_mean_column_df.reindex(columns=new_order_cols)

            dct_rename_cols_mean = {'АД_Значение': 'Ср. Ассертивные действия',
                                    'ВСК_Значение': 'Ср. Вступление в социальный контакт',
                                    'ПСП_Значение': 'Ср. Поиск социальной поддержки',

                                    'ОД_Значение': 'Ср. Осторожные действия',
                                    'ИД_Значение': 'Ср. Импульсивные действия',
                                    'И_Значение': 'Ср. Избегание',

                                    'НД_Значение': 'Ср. Непрямые действия',
                                    'АСД_Значение': 'Ср. Асоциальные действия',
                                    'АГД_Значение': 'Ср. Агрессивные действия',
                                    }
            svod_mean_column_df.rename(columns=dct_rename_cols_mean, inplace=True)

            # Готовим наименование
            name_column = lst_svod_cols[idx]
            name_column = re.sub(r'[\[\]\'+()<> :"?*|\\/]', '_', name_column)
            name_column = name_column[:15]

            out_dct.update({f'Ср {name_column}': svod_mean_column_df,
                            f'АД {name_column}': svod_count_column_level_ad_df,
                            f'ВСК {name_column}': svod_count_column_level_vsk_df,
                            f'ПСП {name_column}': svod_count_column_level_psp_df,

                            f'ОД {name_column}': svod_count_column_level_od_df,
                            f'ИД {name_column}': svod_count_column_level_id_df,
                            f'И {name_column}': svod_count_column_level_i_df,

                            f'НД {name_column}': svod_count_column_level_nd_df,
                            f'АСД {name_column}': svod_count_column_level_asd_df,
                            f'АГД {name_column}': svod_count_column_level_agd_df,
                            })
        return out_dct






def processing_spss_vod_star(base_df: pd.DataFrame, answers_df: pd.DataFrame, lst_svod_cols:list):
    """
    Функция для обработки
    :param base_df: часть датафрейма с описательными колонками
    :param answers_df: часть датафрейма с ответами
    :param lst_svod_cols:  список с колонками по которым нужно делать свод
    """
    try:
        out_answer_df = base_df.copy()  # делаем копию для последующего соединения с сырыми ответами
        if len(answers_df.columns) != 54:  # проверяем количество колонок с вопросами
            raise BadCountColumnsSPSSVS

        # очищаем названия колонок от возможных сочетаний .1 которые добавляет пандас при одинаковых колонках
        clean_df_lst = []
        for name_column in answers_df.columns:
            clean_name = re.sub(r'.\d+$', '', name_column)
            clean_df_lst.append(clean_name)

        answers_df.columns = clean_df_lst

        lst_check_cols =['В любых сложных ситуациях вы не сдаетесь',
                         'Объединяетесь с другими людьми, чтобы вместе разрешить ситуацию',
                         'Советуетесь с друзьями или близкими о том, что бы они сделали, оказавшись в вашем положении',
                         'Вы всегда очень тщательно взвешиваете возможные варианты решений (лучше быть осторожным, чем подвергать себя риску)',
                         'Вы полагаетесь на свою интуицию',
                         'Как правило, вы откладываете решение возникшей проблемы в надежде, что она разрешится сама',
                         'Стараетесь держать все под контролем, хотя и не показываете этого другим',
                         'Вы полагаете, что иногда необходимо действовать столь быстро и решительно, чтобы застать других врасплох',
                         'Решая неприятные проблемы, выходите из себя и можете наломать немало дров',
                         'Когда кто-либо из близких поступает с вами несправедливо, вы пытаетесь вести себя так, чтобы они не почувствовали, что вы расстроены или обижены',

                         'Стараетесь помочь другим при решении ваших общих проблем',
                         'Не стесняетесь при необходимости обращаться к другим людям за помощью или поддержкой',
                         'Без необходимости не выкладываетесь полностью, предпочитая экономить свои силы',
                         'Вы часто удивляетесь, что наиболее правильным является то решение, которое первым пришло в голову',
                         'Иногда предпочитаете заняться чем угодно, лишь бы забыть о неприятном деле, которое нужно делать',
                         'Для достижения своих целей вам часто приходиться подыгрывать другим или подстраиваться под других людей (несколько кривить душой)',
                         'В определенных ситуациях вы ставите свои личные интересы превыше всего, даже если это пойдет во вред другим',
                         'Как правило, препятствия для решения ваших проблем или достижения желаемого сильно выводят вас из себя, можно сказать, что они просто бесят вас',
                         'Вы считаете, что в сложных ситуациях лучше действовать самому, чем ждать, когда ее будут решать другие',
                         'Находясь в трудной ситуации, вы раздумываете о том, как бы поступили в этом случае другие люди',

                         'В трудные минуты для вас очень важна эмоциональная поддержка близких людей',
                         'Считаете, что во всех случаях лучше семь раз отмерить, прежде чем отрезать',
                         'Вы часто проигрываете из-за того, что не полагаетесь на свои предчувствия',
                         'Вы не тратите свою энергию на разрешение того, что, возможно, само по себе рассеется',
                         'Позволяете другим людям думать, что они могут повлиять на вас, но на самом деле вы — крепкий орешек и никому не позволяете манипулировать собой',
                         'Считаете, что полезно демонстрировать свою власть и превосходство для укрепления собственного авторитета',
                         'Вас можно назвать вспыльчивым человеком',
                         'Вам бывает достаточно трудно ответить отказом на чьи-либо требования или просьбы',
                         'Вы полагаете, что в критических ситуациях лучше действовать сообща с другими',
                         'Вы считаете, что на душе может стать легче, если поделиться с другими своими переживаниями',

                         'Ничего не принимаете на веру, так как полагаете, что в любой ситуации могут быть «подводные камни»',
                         'Ваша интуиция вас никогда не подводит',
                         'В конфликтной ситуации убеждаете себя и других, что проблема не стоит и выеденного яйца',
                         'Иногда вам приходится немного манипулировать людьми (решать свои проблемы, невзирая на интересы других)',
                         'Бывает очень выгодно поставить другого человека в неловкое и зависимое положение',
                         'Вы считаете, что лучше решительно и быстро дать отпор тем, кто не согласен с вашим мнением, чем тянуть кота за хвост',
                         'Вы легко и спокойно можете защитить себя от несправедливых действий со стороны других, в случае необходимости сказать «нет» в ситуации эмоционального давления',
                         'Вы считаете, что общение с другими людьми обогатит ваш жизненный опыт',
                         'Вы полагаете, что поддержка других людей очень помогает вам в трудных ситуациях',
                         'В трудных ситуациях вы долго готовитесь и предпочитаете сначала успокоиться, а потом уже действовать',

                         'В сложных ситуациях лучше следовать первому импульсу, чем долго взвешивать возможные варианты',
                         'По возможности избегаете решительных действий, требующих большой напряженности и ответственности за последствия',
                         'Для достижения своих заветных целей не грех и немного полукавить',
                         'Ищете слабости других людей и используете их со своей выгодой',
                         'Грубость и глупости других людей часто приводят вас в ярость (выводят вас из себя)',
                         'Вы испытываете неловкость, когда вас хвалят или говорят комплименты',
                         'Считаете, что совместные усилия с другими принесут больше пользы в любых ситуациях (при решении любых задач)',
                         'Вы уверены, что в трудных ситуациях вы всегда найдете понимание и сочувствие со стороны близких людей',
                         'Вы полагаете, что во всех случаях нужно следовать принципу «тише едешь, дальше будешь»',
                         'Действие под влиянием первого порыва всегда хуже, чем трезвый расчет',

                         'В конфликтных ситуациях предпочитаете найти какие-либо важные и неотложные дела, позволяя другим заняться решением проблемы или надеясь, что время все расставит на свои места',
                         'Вы полагаете, что хитростью можно добиться порою больше, чем действуя напрямую',
                         'Цель оправдывает средства',
                         'В значимых и конфликтных ситуациях вы бываете агрессивны'
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
            raise BadOrderSPSSVS

        # словарь для замены слов на числа
        dct_replace_value = {'нет, это совсем не так': 1,
                             'скорее нет, чем да': 2,
                             'затрудняюсь ответить': 3,
                             'скорее да, чем нет': 4,
                             'да, совершенно верно': 5,
                             }
        valid_values = [1, 2, 3,4,5]
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
            raise BadValueSPSSVS

        base_df['АД_Значение'] = answers_df.apply(calc_value_ad, axis=1)
        base_df['АД_Степень'] = base_df['АД_Значение'].apply(calc_level_ad)

        base_df['ВСК_Значение'] = answers_df.apply(calc_value_vsk, axis=1)
        base_df['ВСК_Степень'] = base_df['ВСК_Значение'].apply(calc_level_vsk)

        base_df['ПСП_Значение'] = answers_df.apply(calc_value_psp, axis=1)
        base_df['ПСП_Степень'] = base_df['ПСП_Значение'].apply(calc_level_psp)

        base_df['ОД_Значение'] = answers_df.apply(calc_value_od, axis=1)
        base_df['ОД_Степень'] = base_df['ОД_Значение'].apply(calc_level_od)

        base_df['ИД_Значение'] = answers_df.apply(calc_value_id, axis=1)
        base_df['ИД_Степень'] = base_df['ИД_Значение'].apply(calc_level_id)

        base_df['И_Значение'] = answers_df.apply(calc_value_i, axis=1)
        base_df['И_Степень'] = base_df['И_Значение'].apply(calc_level_i)

        base_df['НД_Значение'] = answers_df.apply(calc_value_nd, axis=1)
        base_df['НД_Степень'] = base_df['НД_Значение'].apply(calc_level_nd)

        base_df['АСД_Значение'] = answers_df.apply(calc_value_asd, axis=1)
        base_df['АСД_Степень'] = base_df['АСД_Значение'].apply(calc_level_asd)

        base_df['АГД_Значение'] = answers_df.apply(calc_value_agd, axis=1)
        base_df['АГД_Степень'] = base_df['АГД_Значение'].apply(calc_level_agd)

        # Создаем датафрейм для создания части в общий датафрейм
        part_df = pd.DataFrame()

        # Основные шкалы
        part_df['СПССВС_АД_Значение'] = base_df['АД_Значение']
        part_df['СПССВС_АД_Степень'] = base_df['АД_Степень']

        part_df['СПССВС_ВСК_Значение'] = base_df['ВСК_Значение']
        part_df['СПССВС_ВСК_Степень'] = base_df['ВСК_Степень']

        part_df['СПССВС_ПСП_Значение'] = base_df['ПСП_Значение']
        part_df['СПССВС_ПСП_Степень'] = base_df['ПСП_Степень']

        part_df['СПССВС_ОД_Значение'] = base_df['ОД_Значение']
        part_df['СПССВС_ОД_Степень'] = base_df['ОД_Степень']

        part_df['СПССВС_ИД_Значение'] = base_df['ИД_Значение']
        part_df['СПССВС_ИД_Степень'] = base_df['ИД_Степень']

        part_df['СПССВС_И_Значение'] = base_df['И_Значение']
        part_df['СПССВС_И_Степень'] = base_df['И_Степень']

        part_df['СПССВС_НД_Значение'] = base_df['НД_Значение']
        part_df['СПССВС_НД_Степень'] = base_df['НД_Степень']

        part_df['СПССВС_АСД_Значение'] = base_df['АСД_Значение']
        part_df['СПССВС_АСД_Степень'] = base_df['АСД_Степень']

        part_df['СПССВС_АГД_Значение'] = base_df['АГД_Значение']
        part_df['СПССВС_АГД_Степень'] = base_df['АГД_Степень']

        out_answer_df = pd.concat([out_answer_df, answers_df], axis=1)  # Датафрейм для проверки

        base_df.sort_values(by='АГД_Значение', ascending=False, inplace=True)  # сортируем

        # Делаем свод  по  шкалам
        dct_svod_sub = {'АД_Значение': 'АД_Степень',
                        'ВСК_Значение': 'ВСК_Степень',
                        'ПСП_Значение': 'ПСП_Степень',

                        'ОД_Значение': 'ОД_Степень',
                        'ИД_Значение': 'ИД_Степень',
                        'И_Значение': 'И_Степень',

                        'НД_Значение': 'НД_Степень',
                        'АСД_Значение': 'АСД_Степень',
                        'АГД_Значение': 'АГД_Степень',
                        }

        dct_rename_svod_sub = {'АД_Значение': 'Ассертивные действия',
                               'ВСК_Значение': 'Вступление в социальный контакт',
                               'ПСП_Значение': 'Поиск социальной поддержки',

                               'ОД_Значение': 'Осторожные действия',
                               'ИД_Значение': 'Импульсивные действия',
                               'И_Значение': 'Избегание',

                               'НД_Значение': 'Непрямые действия',
                               'АСД_Значение': 'Асоциальные действия',
                               'АГД_Значение': 'Агрессивные действия',
                               }

        lst_sub = ['низкая степень', 'средняя степень', 'высокая степень']

        base_svod_sub_df = create_union_svod(base_df, dct_svod_sub, dct_rename_svod_sub, lst_sub)

        avg_ad = round(base_df['АД_Значение'].mean(), 2)
        avg_vsk = round(base_df['ВСК_Значение'].mean(), 2)
        avg_psp = round(base_df['ПСП_Значение'].mean(), 2)

        avg_od = round(base_df['ОД_Значение'].mean(), 2)
        avg_id = round(base_df['ИД_Значение'].mean(), 2)
        avg_i = round(base_df['И_Значение'].mean(), 2)

        avg_nd = round(base_df['НД_Значение'].mean(), 2)
        avg_asd = round(base_df['АСД_Значение'].mean(), 2)
        avg_agd = round(base_df['АГД_Значение'].mean(), 2)

        avg_dct = {'Среднее значение степени шкалы Ассертивные действия': avg_ad,
                   'Среднее значение степени шкалы Вступление в социальный контакт': avg_vsk,
                   'Среднее значение степени шкалы Поиск социальной поддержки': avg_psp,

                   'Среднее значение степени шкалы Осторожные действия': avg_od,
                   'Среднее значение степени шкалы Импульсивные действия': avg_id,
                   'Среднее значение степени шкалы Избегание': avg_i,

                   'Среднее значение степени шкалы Непрямые действия': avg_nd,
                   'Среднее значение степени шкалы Асоциальные действия': avg_asd,
                   'Среднее значение степени шкалы Агрессивные действия': avg_agd,
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
            'АД_Степень': 'АД',
            'ВСК_Степень': 'ВСК',
            'ПСП_Степень': 'ПСП',

            'ОД_Степень': 'ОД',
            'ИД_Степень': 'ИД',
            'И_Степень': 'И',

            'НД_Степень': 'НД',
            'АСД_Степень': 'АСД',
            'АГД_Степень': 'АГД',
        }

        out_dct = create_list_on_level_spssvs(base_df, out_dct, lst_sub, dct_prefix)

        """
                        Сохраняем в зависимости от необходимости делать своды по определенным колонкам
                        """
        if len(lst_svod_cols) == 0:
            return out_dct, part_df

        else:
            out_dct = create_result_spss_vod(base_df, out_dct, lst_svod_cols)
            return out_dct, part_df

    except BadOrderSPSSVS:
        messagebox.showerror('Лахеcис',
                             f'При обработке вопросов теста Стратегия преодоления стрессовых ситуаций, SACS, Водопьянова Старченкова обнаружены неправильные вопросы. Проверьте названия колонок с вопросами:\n'
                             f'{error_order_message[:5000]}\n'
                             f'Используйте при создании Яндекс-формы написание вопросов из руководства пользователя программы Лахесис.')
    except BadValueSPSSVS:
        messagebox.showerror('Лахеcис',
                             f'При обработке вопросов теста Стратегия преодоления стрессовых ситуаций, SACS, Водопьянова Старченкова обнаружены неправильные варианты ответов. Проверьте ответы на указанных строках:\n'
                             f'{error_message[:5000]}\n'
                             f'Используйте при создании Яндекс-формы написание вариантов ответа из руководства пользователя программы Лахесис.')


    except BadCountColumnsSPSSVS:
        messagebox.showerror('Лахеcис',
                             f'Проверьте количество колонок с ответами на тест Стратегия преодоления стрессовых ситуаций, SACS, Водопьянова Старченкова\n'
                             f'Должно быть 54 колонки с ответами')





