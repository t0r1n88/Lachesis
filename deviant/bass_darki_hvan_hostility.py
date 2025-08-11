"""
Скрипт для обработки результатов теста Опросник враждебности Басса-Дарки, BDHI Хван


"""
import pandas as pd
import re
from tkinter import messagebox
from lachesis_support_functions import round_mean_two,calc_count_scale,create_union_svod


class BadOrderBHDI(Exception):
    """
    Исключение для обработки случая когда колонки не совпадают
    """
    pass


class BadValueBHDI(Exception):
    """
    Исключение для неправильных значений в вариантах ответов
    """
    pass

class BadCountColumnsBHDI(Exception):
    """
    Исключение для обработки случая если количество колонок не равно 75
    """
    pass

def calc_value_fa(row):
    """
    Функция для подсчета значения шкалы Физическая агрессия
    :return: число
    """
    lst_pr = [1,25,33,48,55,62,68,9,17,41]
    lst_plus = [1,25,33,48,55,62,68]

    value_forward = 0 # счетчик прямых ответов

    for idx, value in enumerate(row):
        if idx +1 in lst_pr:
            if idx + 1 in lst_plus:
                if value == 'да':
                    value_forward += 1
            else:
                if value == 'нет':
                    value_forward += 1

    return value_forward * 10



def calc_value_ka(row):
    """
    Функция для подсчета значения шкалы Косвенная агрессия
    :return: число
    """
    lst_pr = [2,18,34,42,56,63,10,26,49]
    lst_plus = [2,18,34,42,56,63]

    value_forward = 0 # счетчик прямых ответов

    for idx, value in enumerate(row):
        if idx +1 in lst_pr:
            if idx + 1 in lst_plus:
                if value == 'да':
                    value_forward += 1
            else:
                if value == 'нет':
                    value_forward += 1

    return value_forward * 11


def calc_value_r(row):
    """
    Функция для подсчета значения шкалы Раздражение
    :return: число
    """
    lst_pr = [3,19,27,43,50,57,64,72,11,35,69]
    lst_plus = [3,19,27,43,50,57,64,72]

    value_forward = 0 # счетчик прямых ответов

    for idx, value in enumerate(row):
        if idx +1 in lst_pr:
            if idx + 1 in lst_plus:
                if value == 'да':
                    value_forward += 1
            else:
                if value == 'нет':
                    value_forward += 1

    return value_forward * 9


def calc_value_n(row):
    """
    Функция для подсчета значения шкалы Негативизм
    :return: число
    """
    lst_pr = [4,12,20,23,36]

    value_forward = 0 # счетчик прямых ответов

    for idx, value in enumerate(row):
        if idx +1 in lst_pr:
            if value == 'да':
                value_forward += 1

    return value_forward * 20


def calc_value_o(row):
    """
    Функция для подсчета значения шкалы Обида
    :return: число
    """
    lst_pr = [5,13,21,29,37,51,58,44]
    lst_plus = [5,13,21,29,37,51,58]

    value_forward = 0 # счетчик прямых ответов

    for idx, value in enumerate(row):
        if idx +1 in lst_pr:
            if idx + 1 in lst_plus:
                if value == 'да':
                    value_forward += 1
            else:
                if value == 'нет':
                    value_forward += 1

    return value_forward * 13


def calc_value_p(row):
    """
    Функция для подсчета значения шкалы Подозрительность
    :return: число
    """
    lst_pr = [6,14,22,30,38,45,52,59,65,70]
    lst_plus = [6,14,22,30,38,45,52,59]

    value_forward = 0 # счетчик прямых ответов

    for idx, value in enumerate(row):
        if idx +1 in lst_pr:
            if idx + 1 in lst_plus:
                if value == 'да':
                    value_forward += 1
            else:
                if value == 'нет':
                    value_forward += 1

    return value_forward * 10


def calc_value_va(row):
    """
    Функция для подсчета значения шкалы Вербальная агрессия
    :return: число
    """
    lst_pr = [7,15,23,31,46,53,60,71,73,39,74,75]
    lst_plus = [7,15,23,31,46,53,60,71,73]

    value_forward = 0 # счетчик прямых ответов

    for idx, value in enumerate(row):
        if idx +1 in lst_pr:
            if idx + 1 in lst_plus:
                if value == 'да':
                    value_forward += 1
            else:
                if value == 'нет':
                    value_forward += 1

    return value_forward * 8


def calc_value_chv(row):
    """
    Функция для подсчета значения шкалы Угрызение совести
    :return: число
    """
    lst_pr = [8,16,24,32,40,47,54,61,67]

    value_forward = 0 # счетчик прямых ответов

    for idx, value in enumerate(row):
        if idx +1 in lst_pr:
            if value == 'да':
                value_forward += 1

    return value_forward * 11


def calc_sten_first(value):
    """
    Функция для подсчета стена для ФА, ВА, Н, ЧВ
    :param value:
    :return:
    """
    if 0 <= value <= 19:
        return 1
    elif 20 <= value <= 30:
        return 2
    elif 31 <= value <= 41:
        return 3
    elif 42 <= value <= 52:
        return 4
    elif 53 <= value <= 63:
        return 5
    elif 64 <= value <= 74:
        return 6
    elif 75 <= value <= 85:
        return 7
    elif 86 <= value <= 96:
        return 8
    else:
        return 9

def calc_level(value):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """
    if 1 <= value <= 2:
        return 'низкий уровень'
    elif 3 <= value <= 4:
        return 'средний уровень'
    elif 5 <= value <= 6:
        return 'повышенный уровень'
    elif value == 7:
        return 'высокий уровень'
    else:
        return 'очень высокий уровень'


def calc_sten_second(value):
    """
    Функция для подсчета стена для КА, Р, П, О
    :param value:
    :return:
    """
    if value == 0:
        return 1
    elif 1 <= value <= 14:
        return 2
    elif 15 <= value <= 25:
        return 3
    elif 26 <= value <= 36:
        return 4
    elif 37 <= value <= 47:
        return 5
    elif 48 <= value <= 58:
        return 6
    elif 59 <= value <= 69:
        return 7
    elif 70 <= value <= 80:
        return 8
    elif 81 <= value <= 92:
        return 9
    else:
        return 10



def calc_sten_aggr(value):
    """
    Функция для подсчета стена Агрессивность
    :param value:
    :return:
    """
    if 0<= value == 17.99:
        return 1
    elif 18 <= value <= 27.99:
        return 2
    elif 28 <= value <= 38.99:
        return 3
    elif 39 <= value <= 49.99:
        return 4
    elif 50 <= value <= 60.99:
        return 5
    elif 61 <= value <= 71.99:
        return 6
    elif 72 <= value <= 82.99:
        return 7
    elif 83 <= value <= 93.99:
        return 8
    else:
        return 9





def calc_sten_host(value):
    """
    Функция для подсчета стена Враждебность
    :param value:
    :return:
    """
    if value == 0:
        return 1
    elif 0.1 <= value <= 14.99:
        return 2
    elif 15 <= value <= 25.99:
        return 3
    elif 26 <= value <= 36.99:
        return 4
    elif 37 <= value <= 47.99:
        return 5
    elif 48 <= value <= 58.99:
        return 6
    elif 59 <= value <= 69.99:
        return 7
    elif 70 <= value <= 80.99:
        return 8
    elif 81 <= value <= 92.99:
        return 9
    else:
        return 10

def calc_level_main(value):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """
    if 1 <= value <= 2:
        return 'низкий уровень'
    elif 3 <= value <= 4:
        return 'средний уровень'
    elif 5 <= value <= 6:
        return 'повышенный уровень'
    elif value == 7:
        return 'высокий уровень'
    else:
        return 'очень высокий уровень'


def create_list_on_level_bhdi(base_df:pd.DataFrame,out_dct:dict,lst_level:list,dct_prefix:dict):
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
                elif level == 'повышенный уровень':
                    level = 'повышенный'
                elif level == 'высокий уровень':
                    level = 'высокий'
                else:
                    level = 'очень высокий'
                dct_level[f'{dct_prefix[key]}. {level}'] = temp_df
        out_dct.update(dct_level)

    return out_dct


def create_result_bass_darki_hvan(base_df:pd.DataFrame, out_dct:dict, lst_svod_cols:list):
    """
    Функция для подсчета результата если указаны колонки по которым нужно провести свод
    :param df: датафрейм с результатами
    :param out_dct: словарь с уже подсчитанными базовыми данными
    :param lst_svod_cols: список сводных колонок
    :return: словарь
    """
    lst_level = ['низкий уровень','средний уровень','повышенный уровень','высокий уровень','очень высокий уровень']
    lst_sten = ['1','2','3','4','5','6','7','8','9','10']

    lst_reindex_one_level_cols = lst_svod_cols.copy()
    lst_reindex_one_level_cols.extend(['низкий уровень','средний уровень','повышенный уровень','высокий уровень','очень высокий уровень',
                                       'Итого'])  # Основная шкала

    lst_reindex_one_sten_cols = lst_svod_cols.copy()
    lst_reindex_one_sten_cols.extend(['1', '2', '3', '4', '5', '6', '7', '8', '9', '10',
                                      'Итого'])  # Стены

    sten_df = base_df.copy()  # делаем копию чтобы стены корректно подсчитались
    sten_df[['Агрессивность_Стен','Враждебность_Стен','ФА_Стен','КА_Стен','Р_Стен','Н_Стен','О_Стен','П_Стен','ВА_Стен','ЧВ_Стен']] = sten_df[['Агрессивность_Стен','Враждебность_Стен','ФА_Стен','КА_Стен','Р_Стен','Н_Стен','О_Стен','П_Стен','ВА_Стен','ЧВ_Стен']].astype(str)

    # Агресивность
    svod_count_one_level_aggr_df = calc_count_scale(base_df, lst_svod_cols,
                                               'Агрессивность_Значение',
                                               'Агрессивность_Уровень',
                                               lst_reindex_one_level_cols, lst_level)

    svod_count_one_sten_aggr_df = calc_count_scale(sten_df, lst_svod_cols,
                                              'Агрессивность_Значение',
                                              'Агрессивность_Стен',
                                              lst_reindex_one_sten_cols, lst_sten)

    # Враждебность
    svod_count_one_level_hos_df = calc_count_scale(base_df, lst_svod_cols,
                                               'Враждебность_Значение',
                                               'Враждебность_Уровень',
                                               lst_reindex_one_level_cols, lst_level)

    svod_count_one_sten_hos_df = calc_count_scale(sten_df, lst_svod_cols,
                                              'Враждебность_Значение',
                                              'Враждебность_Стен',
                                              lst_reindex_one_sten_cols, lst_sten)

    # Физическая агрессия
    svod_count_one_level_fa_df = calc_count_scale(base_df, lst_svod_cols,
                                               'ФА_Значение',
                                               'ФА_Уровень',
                                               lst_reindex_one_level_cols, lst_level)

    svod_count_one_sten_fa_df = calc_count_scale(sten_df, lst_svod_cols,
                                              'ФА_Значение',
                                              'ФА_Стен',
                                              lst_reindex_one_sten_cols, lst_sten)
    # Вербальная агрессия
    svod_count_one_level_va_df = calc_count_scale(base_df, lst_svod_cols,
                                               'ВА_Значение',
                                               'ВА_Уровень',
                                               lst_reindex_one_level_cols, lst_level)

    svod_count_one_sten_va_df = calc_count_scale(sten_df, lst_svod_cols,
                                              'ВА_Значение',
                                              'ВА_Стен',
                                              lst_reindex_one_sten_cols, lst_sten)

    # Косвенная агрессия
    svod_count_one_level_ka_df = calc_count_scale(base_df, lst_svod_cols,
                                               'КА_Значение',
                                               'КА_Уровень',
                                               lst_reindex_one_level_cols, lst_level)

    svod_count_one_sten_ka_df = calc_count_scale(sten_df, lst_svod_cols,
                                              'КА_Значение',
                                              'КА_Стен',
                                              lst_reindex_one_sten_cols, lst_sten)

    # Раздражительность
    svod_count_one_level_r_df = calc_count_scale(base_df, lst_svod_cols,
                                               'Р_Значение',
                                               'Р_Уровень',
                                               lst_reindex_one_level_cols, lst_level)

    svod_count_one_sten_r_df = calc_count_scale(sten_df, lst_svod_cols,
                                              'Р_Значение',
                                              'Р_Стен',
                                              lst_reindex_one_sten_cols, lst_sten)

    # Негативизм
    svod_count_one_level_n_df = calc_count_scale(base_df, lst_svod_cols,
                                               'Н_Значение',
                                               'Н_Уровень',
                                               lst_reindex_one_level_cols, lst_level)

    svod_count_one_sten_n_df = calc_count_scale(sten_df, lst_svod_cols,
                                              'Н_Значение',
                                              'Н_Стен',
                                              lst_reindex_one_sten_cols, lst_sten)

    # Обида
    svod_count_one_level_o_df = calc_count_scale(base_df, lst_svod_cols,
                                               'О_Значение',
                                               'О_Уровень',
                                               lst_reindex_one_level_cols, lst_level)

    svod_count_one_sten_o_df = calc_count_scale(sten_df, lst_svod_cols,
                                              'О_Значение',
                                              'О_Стен',
                                              lst_reindex_one_sten_cols, lst_sten)

    # Подозрительность
    svod_count_one_level_p_df = calc_count_scale(base_df, lst_svod_cols,
                                               'П_Значение',
                                               'П_Уровень',
                                               lst_reindex_one_level_cols, lst_level)

    svod_count_one_sten_p_df = calc_count_scale(sten_df, lst_svod_cols,
                                              'П_Значение',
                                              'П_Стен',
                                              lst_reindex_one_sten_cols, lst_sten)

    # Чувство вины
    svod_count_one_level_chv_df = calc_count_scale(base_df, lst_svod_cols,
                                               'ЧВ_Значение',
                                               'ЧВ_Уровень',
                                               lst_reindex_one_level_cols, lst_level)

    svod_count_one_sten_chv_df = calc_count_scale(sten_df, lst_svod_cols,
                                              'ЧВ_Значение',
                                              'ЧВ_Стен',
                                              lst_reindex_one_sten_cols, lst_sten)

    # Считаем среднее по субшкалам
    svod_mean_one_df = pd.pivot_table(base_df,
                                  index=lst_svod_cols,
                                  values=['Агрессивность_Значение',
                                          'Враждебность_Значение',
                                          'ФА_Значение',
                                          'ВА_Значение',
                                          'КА_Значение',
                                          'Р_Значение',
                                          'Н_Значение',
                                          'О_Значение',
                                          'П_Значение',
                                          'ЧВ_Значение',
                                          ],
                                  aggfunc=round_mean_two)
    svod_mean_one_df.reset_index(inplace=True)
    # упорядочиваем колонки
    new_order_cols = lst_svod_cols.copy()
    new_order_cols.extend((['Агрессивность_Значение', 'Враждебность_Значение',
                            'ФА_Значение','ВА_Значение', 'КА_Значение',
                            'Р_Значение','Н_Значение',
                            'О_Значение','П_Значение','ЧВ_Значение'
                            ]))
    svod_mean_one_df = svod_mean_one_df.reindex(columns=new_order_cols)

    dct_rename_cols_mean = {'Агрессивность_Значение': 'Ср. Агрессивность',
                            'Враждебность_Значение': 'Ср. Враждебность',
                            'ФА_Значение': 'Ср. ФА',
                            'ВА_Значение': 'Ср. ВА',
                            'КА_Значение': 'Ср. КА',
                            'Р_Значение': 'Ср. Р',
                            'Н_Значение': 'Ср. Н',
                            'О_Значение': 'Ср. О',
                            'П_Значение': 'Ср. П',
                            'ЧВ_Значение': 'Ср. ЧВ',
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
                    f'Агр {out_name}': svod_count_one_level_aggr_df,
                    f'Агр Стен {out_name}': svod_count_one_sten_aggr_df,

                    f'Вр {out_name}': svod_count_one_level_hos_df,
                    f'Вр Стен {out_name}': svod_count_one_sten_hos_df,

                    f'ФА {out_name}': svod_count_one_level_fa_df,
                    f'ФА Стен {out_name}': svod_count_one_sten_fa_df,

                    f'ВА {out_name}': svod_count_one_level_va_df,
                    f'ВА Стен {out_name}': svod_count_one_sten_va_df,

                    f'КА {out_name}': svod_count_one_level_ka_df,
                    f'КА Стен {out_name}': svod_count_one_sten_ka_df,

                    f'Р {out_name}': svod_count_one_level_r_df,
                    f'Р Стен {out_name}': svod_count_one_sten_r_df,

                    f'Н {out_name}': svod_count_one_level_n_df,
                    f'Н Стен {out_name}': svod_count_one_sten_n_df,

                    f'О {out_name}': svod_count_one_level_o_df,
                    f'О Стен {out_name}': svod_count_one_sten_o_df,

                    f'П {out_name}': svod_count_one_level_p_df,
                    f'П Стен {out_name}': svod_count_one_sten_p_df,

                    f'ЧВ {out_name}': svod_count_one_level_chv_df,
                    f'ЧВ Стен {out_name}': svod_count_one_sten_chv_df})

    if len(lst_svod_cols) == 1:
        return out_dct

    else:
        for idx, name_column in enumerate(lst_svod_cols):
            lst_reindex_column_level_cols = [lst_svod_cols[idx],'низкий уровень','средний уровень','повышенный уровень','высокий уровень','очень высокий уровень',
                                                  'Итого']

            lst_reindex_column_sten_cols = [lst_svod_cols[idx],'1', '2', '3', '4', '5', '6', '7', '8', '9', '10',
                                                 'Итого']

            # Агресивность
            svod_count_column_level_aggr_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                               'Агрессивность_Значение',
                                                               'Агрессивность_Уровень',
                                                               lst_reindex_column_level_cols, lst_level)

            svod_count_column_sten_aggr_df = calc_count_scale(sten_df, lst_svod_cols[idx],
                                                              'Агрессивность_Значение',
                                                              'Агрессивность_Стен',
                                                              lst_reindex_column_sten_cols, lst_sten)

            # Враждебность
            svod_count_column_level_hos_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                              'Враждебность_Значение',
                                                              'Враждебность_Уровень',
                                                              lst_reindex_column_level_cols, lst_level)

            svod_count_column_sten_hos_df = calc_count_scale(sten_df, lst_svod_cols[idx],
                                                             'Враждебность_Значение',
                                                             'Враждебность_Стен',
                                                             lst_reindex_column_sten_cols, lst_sten)

            # Физическая агрессия
            svod_count_column_level_fa_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                             'ФА_Значение',
                                                             'ФА_Уровень',
                                                             lst_reindex_column_level_cols, lst_level)

            svod_count_column_sten_fa_df = calc_count_scale(sten_df, lst_svod_cols[idx],
                                                            'ФА_Значение',
                                                            'ФА_Стен',
                                                            lst_reindex_column_sten_cols, lst_sten)
            # Вербальная агрессия
            svod_count_column_level_va_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                             'ВА_Значение',
                                                             'ВА_Уровень',
                                                             lst_reindex_column_level_cols, lst_level)

            svod_count_column_sten_va_df = calc_count_scale(sten_df, lst_svod_cols[idx],
                                                            'ВА_Значение',
                                                            'ВА_Стен',
                                                            lst_reindex_column_sten_cols, lst_sten)

            # Косвенная агрессия
            svod_count_column_level_ka_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                             'КА_Значение',
                                                             'КА_Уровень',
                                                             lst_reindex_column_level_cols, lst_level)

            svod_count_column_sten_ka_df = calc_count_scale(sten_df, lst_svod_cols[idx],
                                                            'КА_Значение',
                                                            'КА_Стен',
                                                            lst_reindex_column_sten_cols, lst_sten)

            # Раздражительность
            svod_count_column_level_r_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                            'Р_Значение',
                                                            'Р_Уровень',
                                                            lst_reindex_column_level_cols, lst_level)

            svod_count_column_sten_r_df = calc_count_scale(sten_df, lst_svod_cols[idx],
                                                           'Р_Значение',
                                                           'Р_Стен',
                                                           lst_reindex_column_sten_cols, lst_sten)

            # Негативизм
            svod_count_column_level_n_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                            'Н_Значение',
                                                            'Н_Уровень',
                                                            lst_reindex_column_level_cols, lst_level)

            svod_count_column_sten_n_df = calc_count_scale(sten_df, lst_svod_cols[idx],
                                                           'Н_Значение',
                                                           'Н_Стен',
                                                           lst_reindex_column_sten_cols, lst_sten)

            # Обида
            svod_count_column_level_o_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                            'О_Значение',
                                                            'О_Уровень',
                                                            lst_reindex_column_level_cols, lst_level)

            svod_count_column_sten_o_df = calc_count_scale(sten_df, lst_svod_cols[idx],
                                                           'О_Значение',
                                                           'О_Стен',
                                                           lst_reindex_column_sten_cols, lst_sten)

            # Подозрительность
            svod_count_column_level_p_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                            'П_Значение',
                                                            'П_Уровень',
                                                            lst_reindex_column_level_cols, lst_level)

            svod_count_column_sten_p_df = calc_count_scale(sten_df, lst_svod_cols[idx],
                                                           'П_Значение',
                                                           'П_Стен',
                                                           lst_reindex_column_sten_cols, lst_sten)

            # Чувство вины
            svod_count_column_level_chv_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                              'ЧВ_Значение',
                                                              'ЧВ_Уровень',
                                                              lst_reindex_column_level_cols, lst_level)

            svod_count_column_sten_chv_df = calc_count_scale(sten_df, lst_svod_cols[idx],
                                                             'ЧВ_Значение',
                                                             'ЧВ_Стен',
                                                             lst_reindex_column_sten_cols, lst_sten)

            # Считаем среднее по субшкалам
            svod_mean_column_df = pd.pivot_table(base_df,
                                                 index=[lst_svod_cols[idx]],
                                                 values=['Агрессивность_Значение',
                                                         'Враждебность_Значение',
                                                         'ФА_Значение',
                                                         'ВА_Значение',
                                                         'КА_Значение',
                                                         'Р_Значение',
                                                         'Н_Значение',
                                                         'О_Значение',
                                                         'П_Значение',
                                                         'ЧВ_Значение',
                                                         ],
                                                 aggfunc=round_mean_two)
            svod_mean_column_df.reset_index(inplace=True)
            # упорядочиваем колонки
            new_order_cols = [lst_svod_cols[idx]].copy()
            new_order_cols.extend((['Агрессивность_Значение', 'Враждебность_Значение',
                                    'ФА_Значение', 'ВА_Значение', 'КА_Значение',
                                    'Р_Значение', 'Н_Значение',
                                    'О_Значение', 'П_Значение', 'ЧВ_Значение'
                                    ]))
            svod_mean_column_df = svod_mean_column_df.reindex(columns=new_order_cols)

            dct_rename_cols_mean = {'Агрессивность_Значение': 'Ср. Агрессивность',
                                    'Враждебность_Значение': 'Ср. Враждебность',
                                    'ФА_Значение': 'Ср. ФА',
                                    'ВА_Значение': 'Ср. ВА',
                                    'КА_Значение': 'Ср. КА',
                                    'Р_Значение': 'Ср. Р',
                                    'Н_Значение': 'Ср. Н',
                                    'О_Значение': 'Ср. О',
                                    'П_Значение': 'Ср. П',
                                    'ЧВ_Значение': 'Ср. ЧВ',
                                    }
            svod_mean_column_df.rename(columns=dct_rename_cols_mean, inplace=True)

            # Готовим наименование
            name_column = lst_svod_cols[idx]
            name_column = re.sub(r'[\[\]\'+()<> :"?*|\\/]', '_', name_column)
            name_column = name_column[:15]

            out_dct.update({f'Ср {name_column}': svod_mean_column_df,
                            f'Агр {name_column}': svod_count_column_level_aggr_df,
                            f'Агр Стен {name_column}': svod_count_column_sten_aggr_df,

                            f'Вр {name_column}': svod_count_column_level_hos_df,
                            f'Вр Стен {name_column}': svod_count_column_sten_hos_df,

                            f'ФА {name_column}': svod_count_column_level_fa_df,
                            f'ФА Стен {name_column}': svod_count_column_sten_fa_df,

                            f'ВА {name_column}': svod_count_column_level_va_df,
                            f'ВА Стен {name_column}': svod_count_column_sten_va_df,

                            f'КА {name_column}': svod_count_column_level_ka_df,
                            f'КА Стен {name_column}': svod_count_column_sten_ka_df,

                            f'Р {name_column}': svod_count_column_level_r_df,
                            f'Р Стен {name_column}': svod_count_column_sten_r_df,

                            f'Н {name_column}': svod_count_column_level_n_df,
                            f'Н Стен {name_column}': svod_count_column_sten_n_df,

                            f'О {name_column}': svod_count_column_level_o_df,
                            f'О Стен {name_column}': svod_count_column_sten_o_df,

                            f'П {name_column}': svod_count_column_level_p_df,
                            f'П Стен {name_column}': svod_count_column_sten_p_df,

                            f'ЧВ {name_column}': svod_count_column_level_chv_df,
                            f'ЧВ Стен {name_column}': svod_count_column_sten_chv_df})
        return out_dct


def processing_bass_darki_hvan_hostility(result_df: pd.DataFrame, answers_df: pd.DataFrame, lst_svod_cols:list):
    """
    Функция для обработки
    :param result_df: часть датафрейма с описательными колонками
    :param answers_df: часть датафрейма с ответами
    :param lst_svod_cols:  список с колонками по которым нужно делать свод
    """
    try:
        out_answer_df = result_df.copy()  # делаем копию для последующего соединения с сырыми ответами
        if len(answers_df.columns) != 75:  # проверяем количество колонок с вопросами
            raise BadCountColumnsBHDI

        # очищаем названия колонок от возможных сочетаний .1 которые добавляет пандас при одинаковых колонках
        clean_df_lst = []
        for name_column in answers_df.columns:
            clean_name = re.sub(r'.\d+$', '', name_column)
            clean_df_lst.append(clean_name)

        answers_df.columns = clean_df_lst

        lst_check_cols = ['Временами я не могу справиться с желанием причинить вред другим','Иногда сплетничаю о людях, которых не люблю',
                          'Я легко раздражаюсь, но быстро успокаиваюсь','Если меня не попросят по-хорошему, я не выполню',
                          'Я не всегда получаю то, что мне положено','Я не знаю, что люди говорят обо мне за моей спиной',
                          'Если я не одобряю поведение друзей, я даю им это почувствовать','Когда мне случалось обмануть кого-нибудь, я испытывал мучительные угрызения совести',
                          'Мне кажется, что я не способен ударить человека','Я никогда не раздражаюсь настолько, чтобы кидаться предметами',
                          'Я всегда снисходителен к чужим недостаткам','Если мне не нравится установленное правило, мне хочется нарушить его',
                          'Другие умеют почти всегда пользоваться благоприятными обстоятельствами','Я держусь настороженно с людьми, которые относятся ко мне несколько более дружественно, чем я ожидал',
                          'Я часто бываю не согласен с людьми','Иногда мне на ум приходят мысли, которых я стыжусь',
                          'Если кто-нибудь первым ударит меня, я не отвечу ему','Когда я раздражаюсь, я хлопаю дверьми',
                          'Я гораздо более раздражителен, чем кажется','Если кто-то воображает себя начальником, я всегда поступаю ему наперекор',
                          'Меня немного огорчает моя судьба','Я думаю, что многие люди не любят меня',
                          'Я не могу удержаться от спора, если люди не согласны со мной','Люди, увиливающие от работы, должны испытывать чувство вины',
                          'Тот, кто оскорбляет меня и мою семью, напрашивается на драку','Я не способен на грубые шутки',
                          'Меня охватывает ярость, когда надо мной насмехаются','Когда люди строят из себя начальников, я делаю все, чтобы они не зазнавались',
                          'Почти каждую неделю я вижу кого-нибудь, кто мне не нравится','Довольно многие люди завидуют мне',
                          'Я требую, чтобы люди уважали меня','Меня угнетает то, что я мало делаю для своих родителей',
                          'Люди, которые постоянно изводят вас, стоят того, чтобы их "щелкнули по носу"','Я никогда не бываю мрачен от злости',
                          'Если ко мне относятся хуже, чем я того заслуживаю, я не расстраиваюсь','Если кто-то выводит меня из себя, я не обращаю внимания',
                          'Хотя я и не показываю этого, меня иногда гложет зависть','Иногда мне кажется, что надо мной смеются',
                          'Даже если я злюсь, я не прибегаю к "сильным" выражениям','Мне хочется, чтобы мои грехи были прощены',
                          'Я редко даю сдачи, даже если кто-нибудь ударит меня','Когда получается не, по-моему, я иногда обижаюсь',
                          'Иногда люди раздражают меня одним своим присутствием','Нет людей, которых бы я по-настоящему ненавидел',
                          'Мой принцип: "Никогда не доверять "чужакам"','Если кто-нибудь раздражает меня, я готов сказать, что я о нем думаю',
                          'Я делаю много такого, о чем впоследствии жалею','Если я разозлюсь, я могу ударить кого-нибудь',
                          'С детства я никогда не проявлял вспышек гнева','Я часто чувствую себя как пороховая бочка, готовая взорваться',
                          'Если бы все знали, что я чувствую, меня бы считали человеком, с которым нелегко работать','Я всегда думаю о том, какие тайные причины заставляют людей делать что-нибудь приятное для меня',
                          'Когда на меня кричат, я начинаю кричать в ответ','Неудачи огорчают меня',
                          'Я дерусь не реже и не чаще, чем другие','Я могу вспомнить случаи, когда я был настолько зол, что хватал попавшуюся мне под руку вещь и ломал ее',
                          'Иногда я чувствую, что готов первым начать драку','Иногда я чувствую, что жизнь поступает со мной несправедливо',
                          'Раньше я думал, что большинство людей говорит правду, но теперь я в это не верю','Я ругаюсь только со злости',
                          'Когда я поступаю неправильно, меня мучает совесть','Если для защиты своих прав мне нужно применить физическую силу, я применяю ее',
                          'Иногда я выражаю свой гнев тем, что стучу кулаком по столу','Я бываю грубоват по отношению к людям, которые мне не нравятся',
                          'У меня нет врагов, которые бы хотели мне навредить','Я не умею поставить человека на место, даже если он того заслуживает',
                          'Я часто думаю, что жил неправильно','Я знаю людей, которые способны довести меня до драки',
                          'Я не огорчаюсь из-за мелочей','Мне редко приходит в голову, что люди пытаются разозлить или оскорбить меня',
                          'Я часто только угрожаю людям, хотя и не собираюсь приводить угрозы в исполнение','В последнее время я стал занудой',
                          'В споре я часто повышаю голос','Я стараюсь обычно скрывать свое плохое отношение к людям',
                          'Я лучше соглашусь с чем-либо, чем стану спорить'
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
            raise BadOrderBHDI

        valid_values = ['да', 'нет']
        # Проверяем, есть ли значения, отличающиеся от указанных в списке
        lst_error_answers = []  # список для хранения строк где найдены неправильные ответы

        for i in range(75):
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
            raise BadValueBHDI

        base_df = pd.DataFrame()

        base_df['ФА_Значение'] = answers_df.apply(calc_value_fa, axis=1)
        base_df['ФА_Стен'] = base_df['ФА_Значение'].apply(calc_sten_first)
        base_df['ФА_Уровень'] = base_df['ФА_Стен'].apply(calc_level)


        base_df['КА_Значение'] = answers_df.apply(calc_value_ka, axis=1)
        base_df['КА_Стен'] = base_df['КА_Значение'].apply(calc_sten_second)
        base_df['КА_Уровень'] = base_df['КА_Стен'].apply(calc_level)


        base_df['Р_Значение'] = answers_df.apply(calc_value_r, axis=1)
        base_df['Р_Стен'] = base_df['Р_Значение'].apply(calc_sten_second)
        base_df['Р_Уровень'] = base_df['Р_Стен'].apply(calc_level)


        base_df['Н_Значение'] = answers_df.apply(calc_value_n, axis=1)
        base_df['Н_Стен'] = base_df['Н_Значение'].apply(calc_sten_first)
        base_df['Н_Уровень'] = base_df['Н_Стен'].apply(calc_level)

        base_df['О_Значение'] = answers_df.apply(calc_value_o, axis=1)
        base_df['О_Стен'] = base_df['О_Значение'].apply(calc_sten_second)
        base_df['О_Уровень'] = base_df['О_Стен'].apply(calc_level)

        base_df['П_Значение'] = answers_df.apply(calc_value_p, axis=1)
        base_df['П_Стен'] = base_df['П_Значение'].apply(calc_sten_second)
        base_df['П_Уровень'] = base_df['П_Стен'].apply(calc_level)

        base_df['ВА_Значение'] = answers_df.apply(calc_value_va, axis=1)
        base_df['ВА_Стен'] = base_df['ВА_Значение'].apply(calc_sten_first)
        base_df['ВА_Уровень'] = base_df['ВА_Стен'].apply(calc_level)

        base_df['ЧВ_Значение'] = answers_df.apply(calc_value_chv, axis=1)
        base_df['ЧВ_Стен'] = base_df['ЧВ_Значение'].apply(calc_sten_first)
        base_df['ЧВ_Уровень'] = base_df['ЧВ_Стен'].apply(calc_level)

        base_df['Агрессивность_Значение'] = round(base_df[['ФА_Значение', 'КА_Значение','ВА_Значение']].sum(axis=1) / 3, 2)
        base_df['Агрессивность_Стен'] = base_df['Агрессивность_Значение'].apply(calc_sten_aggr)
        base_df['Агрессивность_Уровень'] = base_df['Агрессивность_Стен'].apply(calc_level_main)

        base_df['Враждебность_Значение'] = round(base_df[['О_Значение','П_Значение']].sum(axis=1) / 2,2)
        base_df['Враждебность_Стен'] = base_df['Враждебность_Значение'].apply(calc_sten_host)
        base_df['Враждебность_Уровень'] = base_df['Враждебность_Стен'].apply(calc_level_main)

        # Создаем датафрейм для создания части в общий датафрейм
        part_df = pd.DataFrame()
        part_df['УАБД_Х_Агр_Значение'] = base_df['Агрессивность_Значение']
        part_df['УАБД_Х_Агр_Стен'] = base_df['Агрессивность_Стен']
        part_df['УАБД_Х_Агр_Уровень'] = base_df['Агрессивность_Уровень']

        part_df['УАБД_Х_Вр_Значение'] = base_df['Враждебность_Значение']
        part_df['УАБД_Х_Вр_Стен'] = base_df['Враждебность_Стен']
        part_df['УАБД_Х_Вр_Уровень'] = base_df['Враждебность_Уровень']

        out_answer_df = pd.concat([out_answer_df, answers_df], axis=1)  # Датафрейм для проверки

        new_order_cols = ['Агрессивность_Значение', 'Агрессивность_Стен','Агрессивность_Уровень',
                          'Враждебность_Значение','Враждебность_Стен','Враждебность_Уровень',
                          'ФА_Значение','ФА_Стен','ФА_Уровень',
                          'ВА_Значение', 'ВА_Стен', 'ВА_Уровень',
                          'КА_Значение','КА_Стен','КА_Уровень',
                          'Р_Значение','Р_Стен','Р_Уровень',
                          'Н_Значение','Н_Стен','Н_Уровень',
                          'О_Значение','О_Стен','О_Уровень',
                          'П_Значение','П_Стен','П_Уровень',
                          'ЧВ_Значение','ЧВ_Стен','ЧВ_Уровень'
                          ]
        base_df = base_df.reindex(columns=new_order_cols)

        # Соединяем анкетную часть с результатной
        base_df = pd.concat([result_df, base_df], axis=1)
        base_df.sort_values(by='Агрессивность_Значение', ascending=False, inplace=True)  # сортируем


        # Делаем свод  по  шкалам
        dct_svod_sub = {'Агрессивность_Значение': 'Агрессивность_Уровень',
                        'Враждебность_Значение': 'Враждебность_Уровень',
                        'ФА_Значение': 'ФА_Уровень',
                        'КА_Значение':'КА_Уровень',
                        'ВА_Значение': 'ВА_Уровень',
                        'Р_Значение':'Р_Уровень',
                        'Н_Значение':'Н_Уровень',
                        'О_Значение':'О_Уровень',
                        'П_Значение':'П_Уровень',
                        'ЧВ_Значение':'ЧВ_Уровень',
                        }

        dct_rename_svod_sub = {'Агрессивность_Значение': 'Агрессивность',
                               'Враждебность_Значение': 'Враждебность',
                               'ФА_Значение': 'Физическая агрессия',
                               'ВА_Значение': 'Вербальная агрессия',
                               'КА_Значение':'Косвенная агрессия',
                               'Р_Значение':'Раздражение',
                               'Н_Значение':'Негативизм',
                               'О_Значение':'Обида',
                               'П_Значение':'Подозрительность',
                               'ЧВ_Значение':'Чувство вины',
                               }

        lst_sub = ['низкий уровень','средний уровень','повышенный уровень','высокий уровень','очень высокий уровень']

        base_svod_sub_df = create_union_svod(base_df, dct_svod_sub, dct_rename_svod_sub, lst_sub)


        # Делаем свод по стенам
        dct_svod_sten = {'Агрессивность_Значение': 'Агрессивность_Стен',
                        'Враждебность_Значение': 'Враждебность_Стен',
                        'ФА_Значение': 'ФА_Стен',
                         'ВА_Значение': 'ВА_Стен',
                         'КА_Значение':'КА_Стен',
                        'Р_Значение':'Р_Стен',
                        'Н_Значение':'Н_Стен',
                        'О_Значение':'О_Стен',
                        'П_Значение':'П_Стен',
                        'ЧВ_Значение':'ЧВ_Стен',
                        }

        dct_rename_svod_sten = {'Агрессивность_Значение': 'Агрессивность',
                               'Враждебность_Значение': 'Враждебность',
                               'ФА_Значение': 'Физическая агрессия',
                                'ВА_Значение': 'Вербальная агрессия',
                                'КА_Значение':'Косвенная агрессия',
                               'Р_Значение':'Раздражение',
                               'Н_Значение':'Негативизм',
                               'О_Значение':'Обида',
                               'П_Значение':'Подозрительность',
                               'ЧВ_Значение':'Чувство вины',
                               }

        lst_sten = [1,2,3,4,5,6,7,8,9,10]

        base_svod_sten_df = create_union_svod(base_df, dct_svod_sten, dct_rename_svod_sten, lst_sten)

        # считаем среднее значение по шкалам
        avg_aggr = round(base_df['Агрессивность_Значение'].mean(), 2)
        avg_hos = round(base_df['Враждебность_Значение'].mean(), 2)
        avg_fa = round(base_df['ФА_Значение'].mean(), 2)
        avg_ka = round(base_df['КА_Значение'].mean(), 2)
        avg_r = round(base_df['Р_Значение'].mean(), 2)
        avg_n = round(base_df['Н_Значение'].mean(), 2)
        avg_o = round(base_df['О_Значение'].mean(), 2)
        avg_p = round(base_df['П_Значение'].mean(), 2)
        avg_va = round(base_df['ВА_Значение'].mean(), 2)
        avg_chv = round(base_df['ЧВ_Значение'].mean(), 2)

        avg_dct = {'Среднее значение индекса Агрессивность': avg_aggr,
                   'Среднее значение индекса Враждебность': avg_hos,
                   'Среднее значение шкалы Физическая агрессия': avg_fa,
                   'Среднее значение шкалы Вербальная агрессия': avg_va,
                   'Среднее значение шкалы Косвенная агрессия': avg_ka,
                   'Среднее значение шкалы Раздражение': avg_r,
                   'Среднее значение шкалы Негативизм': avg_n,
                   'Среднее значение шкалы Обида': avg_o,
                   'Среднее значение шкалы Подозрительность': avg_p,
                   'Среднее значение шкалы Чувство вины': avg_chv,
                   }

        avg_df = pd.DataFrame.from_dict(avg_dct, orient='index')
        avg_df = avg_df.reset_index()
        avg_df.columns = ['Показатель', 'Среднее значение']

        # формируем основной словарь
        out_dct = {'Списочный результат': base_df,
                   'Список для проверки': out_answer_df,
                   'Свод Шкалы':base_svod_sub_df,
                   'Свод Стены':base_svod_sten_df,
                   'Среднее':avg_df,
                   }

        dct_prefix = {'Агрессивность_Уровень': 'Агр',
                      'Враждебность_Уровень': 'Вр',
                      'ФА_Уровень': 'Н',
                      'ВА_Уровень': 'ВА',
                      'КА_Уровень':'КА',
                      'Р_Уровень':'Р',
                      'Н_Уровень':'Н',
                      'О_Уровень':'О',
                      'П_Уровень':'П',
                      'ЧВ_Уровень':'ЧВ',
                      }

        out_dct = create_list_on_level_bhdi(base_df, out_dct, lst_sub, dct_prefix)

        """
                        Сохраняем в зависимости от необходимости делать своды по определенным колонкам
                        """
        if len(lst_svod_cols) == 0:
            return out_dct, part_df

        else:
            out_dct = create_result_bass_darki_hvan(base_df, out_dct, lst_svod_cols)
            return out_dct, part_df


    except BadOrderBHDI:
        messagebox.showerror('Лахеcис',
                             f'При обработке вопросов теста Опросник враждебности Басса-Дарки Хван обнаружены неправильные вопросы. Проверьте названия колонок с вопросами:\n'
                             f'{error_order_message}\n'
                             f'Используйте при создании Яндекс-формы написание вопросов из руководства пользователя программы Лахесис.')
    except BadValueBHDI:
        messagebox.showerror('Лахеcис',
                             f'При обработке вопросов теста Опросник враждебности Басса-Дарки Хван обнаружены неправильные варианты ответов. Проверьте ответы на указанных строках:\n'
                             f'{error_message}\n'
                             f'Используйте при создании Яндекс-формы написание вариантов ответа из руководства пользователя программы Лахесис.')


    except BadCountColumnsBHDI:
        messagebox.showerror('Лахеcис',
                             f'Проверьте количество колонок с ответами на тест Опросник враждебности Басса-Дарки Хван\n'
                             f'Должно быть 75 колонок с ответами')
















