"""
Скрипт для обработки результатов Экспертная оценка адаптированности ребёнка к школе Чирков Соколова Сорокина
"""

import pandas as pd
import re
from tkinter import messagebox
from lachesis_support_functions import round_mean_two,calc_count_scale,create_union_svod, create_list_on_level

class BadOrderAORSHCHSS(Exception):
    """
    Исключение для обработки случая когда колонки не совпадают
    """
    pass


class BadValueAORSHCHSS(Exception):
    """
    Исключение для неправильных значений в вариантах ответов
    """
    pass

class BadCountColumnsAORSHCHSS(Exception):
    """
    Исключение для обработки случая если количество колонок не равно 7
    """
    pass


def calc_level(value):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """
    if 0<= value <= 14 :
        return f'дезадаптация'
    elif 15<= value <=21 :
        return f'неполная адаптация'
    else:
        return f'нормальная адаптация'


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


def calc_value_aud(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_one = [1,2]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_one:
                value_forward += value

    return value_forward

def calc_value_ushnp(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_one = [3,4]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_one:
                value_forward += value

    return value_forward

def calc_value_usk(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_one = [5,6]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_one:
                value_forward += value

    return value_forward



def calc_value_ab(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_one = [7]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_one:
                value_forward += value

    return value_forward


def calc_value_ua(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_one = [1]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_one:
                value_forward += value

    return value_forward

def calc_value_uz(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_one = [2]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_one:
                value_forward += value

    return value_forward

def calc_value_pu(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_one = [3]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_one:
                value_forward += value

    return value_forward

def calc_value_pp(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_one = [4]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_one:
                value_forward += value

    return value_forward

def calc_value_vo(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_one = [5]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_one:
                value_forward += value

    return value_forward

def calc_value_ou(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_one = [6]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_one:
                value_forward += value

    return value_forward

def calc_value_a(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_one = [7]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_one:
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

def create_list_on_level_spa(base_df:pd.DataFrame, out_dct:dict, lst_level:list, dct_prefix:dict):
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
                if level == 'нормальная адаптация':
                    level = 'нормальная'
                elif level == 'неполная адаптация':
                    level = 'неполная'
                dct_level[f'{dct_prefix[key]}. {level}'] = temp_df
        out_dct.update(dct_level)

    return out_dct


def create_result_aoarsh_chir_ss(base_df:pd.DataFrame, out_dct:dict, lst_svod_cols:list):
    """
    Функция для подсчета результата если указаны колонки по которым нужно провести свод
    :param df: датафрейм с результатами
    :param out_dct: словарь с уже подсчитанными базовыми данными
    :param lst_svod_cols: список сводных колонок
    :return: словарь
    """
    lst_base_one_level = ['нормальная адаптация','неполная адаптация','дезадаптация']

    lst_reindex_one_base_level_cols = lst_svod_cols.copy()
    lst_reindex_one_base_level_cols.extend(['нормальная адаптация','неполная адаптация','дезадаптация',
                                       'Итого'])  # Основная шкала

    svod_count_one_level_base_df = calc_count_scale(base_df, lst_svod_cols,
                                                    'СПА_Значение',
                                                    'СПА_Уровень',
                                                    lst_reindex_one_base_level_cols, lst_base_one_level)

    lst_level = ['76-100%', '51-75%', '26-50%', '0-25%']
    lst_reindex_one_level_cols = lst_svod_cols.copy()
    lst_reindex_one_level_cols.extend(
        ['76-100%', '51-75%', '26-50%', '0-25%',
         'Итого'])  # Основная шкала

    svod_count_one_level_factor_aud_df = calc_count_scale(base_df, lst_svod_cols,
                                                'ЭУД_Значение',
                                                'ЭУД_Диапазон',
                                                lst_reindex_one_level_cols, lst_level)

    svod_count_one_level_factor_ushnp_df = calc_count_scale(base_df, lst_svod_cols,
                                                'УШНП_Значение',
                                                'УШНП_Диапазон',
                                                lst_reindex_one_level_cols, lst_level)

    svod_count_one_level_factor_usk_df = calc_count_scale(base_df, lst_svod_cols,
                                                'УСК_Значение',
                                                'УСК_Диапазон',
                                                lst_reindex_one_level_cols, lst_level)

    svod_count_one_level_factor_ab_df = calc_count_scale(base_df, lst_svod_cols,
                                                'ЭБ_Значение',
                                                'ЭБ_Диапазон',
                                                lst_reindex_one_level_cols, lst_level)



    svod_count_one_level_ro_df = calc_count_scale(base_df, lst_svod_cols,
                                                'УА_Значение',
                                                'УА_Диапазон',
                                                lst_reindex_one_level_cols, lst_level)
    svod_count_one_level_ngsh_df = calc_count_scale(base_df, lst_svod_cols,
                                                'УЗ_Значение',
                                                'УЗ_Диапазон',
                                                lst_reindex_one_level_cols, lst_level)
    svod_count_one_level_l_df = calc_count_scale(base_df, lst_svod_cols,
                                                'ПУ_Значение',
                                                'ПУ_Диапазон',
                                                lst_reindex_one_level_cols, lst_level)
    svod_count_one_level_ns_df = calc_count_scale(base_df, lst_svod_cols,
                                                'ПП_Значение',
                                                'ПП_Диапазон',
                                                lst_reindex_one_level_cols, lst_level)
    svod_count_one_level_i_df = calc_count_scale(base_df, lst_svod_cols,
                                                'ВО_Значение',
                                                'ВО_Диапазон',
                                                lst_reindex_one_level_cols, lst_level)

    svod_count_one_level_gs_df = calc_count_scale(base_df, lst_svod_cols,
                                                'ОУ_Значение',
                                                'ОУ_Диапазон',
                                                lst_reindex_one_level_cols, lst_level)
    svod_count_one_level_ins_df = calc_count_scale(base_df, lst_svod_cols,
                                                'Э_Значение',
                                                'Э_Диапазон',
                                                lst_reindex_one_level_cols, lst_level)

    # Считаем среднее по субшкалам
    svod_mean_one_df = pd.pivot_table(base_df,
                                      index=lst_svod_cols,
                                      values=['СПА_Значение',
                                              'ЭУД_Значение',
                                              'УШНП_Значение',
                                              'УСК_Значение',
                                              'ЭБ_Значение',

                                              'УА_Значение',
                                              'УЗ_Значение',
                                              'ПУ_Значение',
                                              'ПП_Значение',
                                              'ВО_Значение',
                                              'ОУ_Значение',
                                              'Э_Значение',
                                              ],
                                      aggfunc=round_mean_two)
    svod_mean_one_df.reset_index(inplace=True)

    # упорядочиваем колонки
    new_order_cols = lst_svod_cols.copy()
    new_order_cols.extend((['СПА_Значение',
                                              'ЭУД_Значение',
                                              'УШНП_Значение',
                                              'УСК_Значение',
                                              'ЭБ_Значение',

                                              'УА_Значение',
                                              'УЗ_Значение',
                                              'ПУ_Значение',
                                              'ПП_Значение',
                                              'ВО_Значение',
                                              'ОУ_Значение',
                                              'Э_Значение',
                            ]))
    svod_mean_one_df = svod_mean_one_df.reindex(columns=new_order_cols)

    dct_rename_cols_mean = {'СПА_Значение': 'Ср. Социально-психологическая адаптация ',
                            'ЭУД_Значение': 'Ср. Эффективность учебной деятельности',
                            'УШНП_Значение': 'Ср. Усвоение школьных норм поведения',
                            'УСК_Значение': 'Ср. Успешность социальных контактов',
                            'ЭБ_Значение': 'Ср. Эмоциональное благополучие',

                            'УА_Значение': 'Ср. Учебная активность',
                            'УЗ_Значение': 'Ср. Усвоение знаний (успеваемость)',
                            'ПУ_Значение': 'Ср. Поведение на уроке',
                            'ПП_Значение': 'Ср. Поведение на перемене',
                            'ВО_Значение': 'Ср. Взаимоотношения с одноклассниками',
                            'ОУ_Значение': 'Ср. Отношение к учителю',
                            'Э_Значение': 'Ср. Эмоции',
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

                    f'ЭУД {out_name}': svod_count_one_level_factor_aud_df,
                    f'УШНП {out_name}': svod_count_one_level_factor_ushnp_df,
                    f'УСК {out_name}': svod_count_one_level_factor_usk_df,
                    f'ЭБ {out_name}': svod_count_one_level_factor_ab_df,


                    f'УА {out_name}': svod_count_one_level_ro_df,
                    f'УЗ {out_name}': svod_count_one_level_ngsh_df,
                    f'ПУ {out_name}': svod_count_one_level_l_df,
                    f'ПП {out_name}': svod_count_one_level_ns_df,
                    f'ВО {out_name}': svod_count_one_level_i_df,
                    f'ОУ {out_name}': svod_count_one_level_gs_df,
                    f'Э {out_name}': svod_count_one_level_ins_df,
                    })

    if len(lst_svod_cols) == 1:
        return out_dct

    else:
        for idx, name_column in enumerate(lst_svod_cols):

            lst_reindex_column_base_level_cols = [lst_svod_cols[idx],'нормальная адаптация','неполная адаптация','дезадаптация',
                                                  'Итого']

            svod_count_column_level_base_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                            'СПА_Значение',
                                                            'СПА_Уровень',
                                                            lst_reindex_column_base_level_cols, lst_base_one_level)

            lst_reindex_column_level_cols = [lst_svod_cols[idx],'76-100%', '51-75%', '26-50%', '0-25%',
                                                  'Итого']

            svod_count_column_level_factor_aud_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                                     'ЭУД_Значение',
                                                                     'ЭУД_Диапазон',
                                                                     lst_reindex_column_level_cols, lst_level)

            svod_count_column_level_factor_ushnp_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                                       'УШНП_Значение',
                                                                       'УШНП_Диапазон',
                                                                       lst_reindex_column_level_cols, lst_level)

            svod_count_column_level_factor_usk_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                                     'УСК_Значение',
                                                                     'УСК_Диапазон',
                                                                     lst_reindex_column_level_cols, lst_level)

            svod_count_column_level_factor_ab_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                                    'ЭБ_Значение',
                                                                    'ЭБ_Диапазон',
                                                                    lst_reindex_column_level_cols, lst_level)

            svod_count_column_level_ro_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                             'УА_Значение',
                                                             'УА_Диапазон',
                                                             lst_reindex_column_level_cols, lst_level)
            svod_count_column_level_ngsh_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                               'УЗ_Значение',
                                                               'УЗ_Диапазон',
                                                               lst_reindex_column_level_cols, lst_level)
            svod_count_column_level_l_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                            'ПУ_Значение',
                                                            'ПУ_Диапазон',
                                                            lst_reindex_column_level_cols, lst_level)
            svod_count_column_level_ns_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                             'ПП_Значение',
                                                             'ПП_Диапазон',
                                                             lst_reindex_column_level_cols, lst_level)
            svod_count_column_level_i_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                            'ВО_Значение',
                                                            'ВО_Диапазон',
                                                            lst_reindex_column_level_cols, lst_level)

            svod_count_column_level_gs_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                             'ОУ_Значение',
                                                             'ОУ_Диапазон',
                                                             lst_reindex_column_level_cols, lst_level)
            svod_count_column_level_ins_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                              'Э_Значение',
                                                              'Э_Диапазон',
                                                              lst_reindex_column_level_cols, lst_level)

            # Считаем среднее по субшкалам
            svod_mean_column_df = pd.pivot_table(base_df,
                                                 index=[lst_svod_cols[idx]],
                                                 values=['СПА_Значение',
                                                         'ЭУД_Значение',
                                                         'УШНП_Значение',
                                                         'УСК_Значение',
                                                         'ЭБ_Значение',

                                                         'УА_Значение',
                                                         'УЗ_Значение',
                                                         'ПУ_Значение',
                                                         'ПП_Значение',
                                                         'ВО_Значение',
                                                         'ОУ_Значение',
                                                         'Э_Значение',
                                                         ],
                                                 aggfunc=round_mean_two)
            svod_mean_column_df.reset_index(inplace=True)

            # упорядочиваем колонки
            new_order_cols = [lst_svod_cols[idx]].copy()
            new_order_cols.extend((['СПА_Значение',
                                    'ЭУД_Значение',
                                    'УШНП_Значение',
                                    'УСК_Значение',
                                    'ЭБ_Значение',

                                    'УА_Значение',
                                    'УЗ_Значение',
                                    'ПУ_Значение',
                                    'ПП_Значение',
                                    'ВО_Значение',
                                    'ОУ_Значение',
                                    'Э_Значение',
                                    ]))
            svod_mean_column_df = svod_mean_column_df.reindex(columns=new_order_cols)

            dct_rename_cols_mean = {'СПА_Значение': 'Ср. Социально-психологическая адаптация ',
                                    'ЭУД_Значение': 'Ср. Эффективность учебной деятельности',
                                    'УШНП_Значение': 'Ср. Усвоение школьных норм поведения',
                                    'УСК_Значение': 'Ср. Успешность социальных контактов',
                                    'ЭБ_Значение': 'Ср. Эмоциональное благополучие',

                                    'УА_Значение': 'Ср. Учебная активность',
                                    'УЗ_Значение': 'Ср. Усвоение знаний (успеваемость)',
                                    'ПУ_Значение': 'Ср. Поведение на уроке',
                                    'ПП_Значение': 'Ср. Поведение на перемене',
                                    'ВО_Значение': 'Ср. Взаимоотношения с одноклассниками',
                                    'ОУ_Значение': 'Ср. Отношение к учителю',
                                    'Э_Значение': 'Ср. Эмоции',
                                    }
            svod_mean_column_df.rename(columns=dct_rename_cols_mean, inplace=True)

            # Готовим наименование
            name_column = lst_svod_cols[idx]
            name_column = re.sub(r'[\[\]\'+()<> :"?*|\\/]', '_', name_column)
            name_column = name_column[:15]

            out_dct.update({f'Ср {name_column}': svod_mean_column_df,
                            f'КДА {name_column}': svod_count_column_level_base_df,

                            f'ЭУД {name_column}': svod_count_column_level_factor_aud_df,
                            f'УШНП {name_column}': svod_count_column_level_factor_ushnp_df,
                            f'УСК {name_column}': svod_count_column_level_factor_usk_df,
                            f'ЭБ {name_column}': svod_count_column_level_factor_ab_df,

                            f'УА {name_column}': svod_count_column_level_ro_df,
                            f'УЗ {name_column}': svod_count_column_level_ngsh_df,
                            f'ПУ {name_column}': svod_count_column_level_l_df,
                            f'ПП {name_column}': svod_count_column_level_ns_df,
                            f'ВО {name_column}': svod_count_column_level_i_df,
                            f'ОУ {name_column}': svod_count_column_level_gs_df,
                            f'Э {name_column}': svod_count_column_level_ins_df,
                            })
        return out_dct










def processing_aoarsh_chir_ss(base_df: pd.DataFrame, answers_df: pd.DataFrame, lst_svod_cols:list):
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
        if len(answers_df.columns) != 7:  # проверяем количество колонок с вопросами
            raise BadCountColumnsAORSHCHSS

        # очищаем названия колонок от возможных сочетаний .1 которые добавляет пандас при одинаковых колонках
        clean_df_lst = []
        for name_column in answers_df.columns:
            clean_name = re.sub(r'.\d+$', '', name_column)
            clean_df_lst.append(clean_name)

        answers_df.columns = clean_df_lst

        lst_check_cols = ['Учебная активность',
                          'Усвоение знаний (успеваемость)',
                          'Поведение на уроке',
                          'Поведение на перемене',
                          'Взаимоотношения с одноклассниками',
                          'Отношение к учителю',
                          'Эмоции'
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
            raise BadOrderAORSHCHSS

        valid_values = [['Учебная активность отсутствует (ребенок не включается в учебный процесс)','Пассивен на уроке, дает отрицательные ответы или не отвечает совсем, часто переписывает готовое с доски','Учебная активность на уроке носит кратковременный характер, часто отвлекается, не слышит вопроса','Редко поднимает руку, но отвечает правильно','На уроке работает, положительные и отрицательные ответы чередуются','Активно работает на уроке, часто поднимает руку и отвечает правильно'],
                        ['Плохое усвоение программного материала по всем предметам – грубые ошибки, большое их количество (низкая успеваемость по всем предметам, средний балл ниже 3,3)','Частые ошибки, неаккуратное выполнение заданий, много исправлений, зачеркиваний (непостоянство оценок, средний балл 3,5 и ниже)','Плохое усвоение материала по одному из основных предметов, обилие ошибок (средний балл по этому предмету 3,5 и ниже)','Редкие ошибки, связанные с пропуском букв и их заменой (средний балл 3,9–3,6)','Небольшие помарки, единичные ошибки (средний балл 4,5–4)','Правильное безошибочное выполнение школьных заданий (средний балл 5–4,6)'],
                        ['Не выполняет требования учителя: большую часть урока занимается посторонними делами','Выполняет требования учителя частично, отвлекается на посторонние занятия, вертится или постоянно разговаривает','Часто наблюдается скованность в движениях, позе, напряженность в ответах','Изредка поворачивается, обменивается короткими репликами с товарищами','Выполняет требования учителя, но иногда, на короткое время, отвлекается от урока','Сидит спокойно, добросовестно выполняет все требования учителя'],
                        ['Часто нарушает нормы поведения: мешает другим детям играть, нападает на них, кричит, бегает, не меняет своего поведения, когда делают замечания (не владеет собой)','Пассивный, движения скованные, избегает других детей','Не может найти себе занятие, переходит от одной группы детей к другой','Активность ребенка ограничивается занятиями, связанными с подготовкой к следующему уроку (готовит учебники, тетради, моет доску, убирает класс)','Активность выражена в малой степени – предпочитает занятия в классе с кем-нибудь из ребят, чтение книг, спокойные игры','Высокая игровая активность, охотно участвует в подвижных, коллективных играх'],
                        ['Проявляет негативизм по отношению к детям, постоянно ссорится и обижает их (другие дети его не любят)','Замкнут, изолирован от других детей, предпочитает находиться один (другие дети равнодушны к нему)','Предпочитает находиться рядом с детьми, но не вступает с ними в контакт','Сфера общения ограничена: контактирует только с некоторыми ребятами','Малоинициативный, но легко вступает в контакт, когда к нему обращаются дети','Общительный, легко контактирует с детьми'],
                        ['Общение с учителем приводит к отрицательным эмоциям, обижается, плачет при малейшем замечании','Избегает контакта с учителем, при общении с ним легко смущается, теряется, говорит тихо, запинается','Выполняет требования учителя формально, не заинтересован в общении с ним, старается быть незаметным','Старательно выполняет требования учителя, но за помощью обращается чаще к одноклассникам','Дорожит хорошим мнением учителя о себе, стремится выполнять все его требования, в случае необходимости сам обращается к нему за помощью','Проявляет дружелюбие по отношению к учителю, стремится понравиться ему, после урока часто подходит к учителю, общается с ним'],
                        ['Преобладание депрессивного настроения. Агрессия (вспышки гнева, злости) проявляются в отношениях с детьми (может ударить, что-то сломать, затеять драку) и в отношениях с учителем','Отдельные депрессивные проявления, плач без всяких на то причин. Агрессивные реакции: часто ссорится с детьми, повышает голос','Отрицательные эмоции: - тревожность, огорчение, иногда страх; - обидчивость, вспыльчивость, раздражительность','Эпизодически проявление сниженного настроения','Спокойное эмоциональное состояние','Хорошее настроение, часто улыбается, смеется']
                        ]

        lst_error_answers = []  # список для хранения строк где найдены неправильные ответы

        for idx, lst_values in enumerate(valid_values):
            mask = ~answers_df.iloc[:, idx].isin(lst_values)  # проверяем на допустимые значения
            # Получаем строки с отличающимися значениями
            result_check = answers_df.iloc[:, idx][mask]

            if len(result_check) != 0:
                error_row = list(map(lambda x: x + 2, result_check.index))
                error_row = list(map(str, error_row))
                error_row_lst = [f'В {idx + 1} вопросной колонке на строке {value}' for value in error_row]
                error_in_column = ','.join(error_row_lst)
                lst_error_answers.append(error_in_column)


        if len(lst_error_answers) != 0:
            error_message = ';'.join(lst_error_answers)
            raise BadValueAORSHCHSS

        # словарь для замены слов на числа
        dct_replace_value = {'Учебная активность отсутствует (ребенок не включается в учебный процесс)': 0,
                             'Пассивен на уроке, дает отрицательные ответы или не отвечает совсем, часто переписывает готовое с доски': 1,
                             'Учебная активность на уроке носит кратковременный характер, часто отвлекается, не слышит вопроса': 2,
                             'Редко поднимает руку, но отвечает правильно': 3,
                             'На уроке работает, положительные и отрицательные ответы чередуются': 4,
                             'Активно работает на уроке, часто поднимает руку и отвечает правильно': 5,

                             'Плохое усвоение программного материала по всем предметам – грубые ошибки, большое их количество (низкая успеваемость по всем предметам, средний балл ниже 3,3)': 0,
                             'Частые ошибки, неаккуратное выполнение заданий, много исправлений, зачеркиваний (непостоянство оценок, средний балл 3,5 и ниже)': 1,
                             'Плохое усвоение материала по одному из основных предметов, обилие ошибок (средний балл по этому предмету 3,5 и ниже)': 2,
                             'Редкие ошибки, связанные с пропуском букв и их заменой (средний балл 3,9–3,6)': 3,
                             'Небольшие помарки, единичные ошибки (средний балл 4,5–4)': 4,
                             'Правильное безошибочное выполнение школьных заданий (средний балл 5–4,6)': 5,

                             'Не выполняет требования учителя: большую часть урока занимается посторонними делами': 0,
                             'Выполняет требования учителя частично, отвлекается на посторонние занятия, вертится или постоянно разговаривает': 1,
                             'Часто наблюдается скованность в движениях, позе, напряженность в ответах': 2,
                             'Изредка поворачивается, обменивается короткими репликами с товарищами': 3,
                             'Выполняет требования учителя, но иногда, на короткое время, отвлекается от урока': 4,
                             'Сидит спокойно, добросовестно выполняет все требования учителя': 5,

                             'Часто нарушает нормы поведения: мешает другим детям играть, нападает на них, кричит, бегает, не меняет своего поведения, когда делают замечания (не владеет собой)': 0,
                             'Пассивный, движения скованные, избегает других детей': 1,
                             'Не может найти себе занятие, переходит от одной группы детей к другой': 2,
                             'Активность ребенка ограничивается занятиями, связанными с подготовкой к следующему уроку (готовит учебники, тетради, моет доску, убирает класс)': 3,
                             'Активность выражена в малой степени – предпочитает занятия в классе с кем-нибудь из ребят, чтение книг, спокойные игры': 4,
                             'Высокая игровая активность, охотно участвует в подвижных, коллективных играх': 5,

                             'Проявляет негативизм по отношению к детям, постоянно ссорится и обижает их (другие дети его не любят)': 0,
                             'Замкнут, изолирован от других детей, предпочитает находиться один (другие дети равнодушны к нему)': 1,
                             'Предпочитает находиться рядом с детьми, но не вступает с ними в контакт': 2,
                             'Сфера общения ограничена: контактирует только с некоторыми ребятами': 3,
                             'Малоинициативный, но легко вступает в контакт, когда к нему обращаются дети': 4,
                             'Общительный, легко контактирует с детьми': 5,

                             'Общение с учителем приводит к отрицательным эмоциям, обижается, плачет при малейшем замечании': 0,
                             'Избегает контакта с учителем, при общении с ним легко смущается, теряется, говорит тихо, запинается': 1,
                             'Выполняет требования учителя формально, не заинтересован в общении с ним, старается быть незаметным': 2,
                             'Старательно выполняет требования учителя, но за помощью обращается чаще к одноклассникам': 3,
                             'Дорожит хорошим мнением учителя о себе, стремится выполнять все его требования, в случае необходимости сам обращается к нему за помощью': 4,
                             'Проявляет дружелюбие по отношению к учителю, стремится понравиться ему, после урока часто подходит к учителю, общается с ним': 5,

                             'Преобладание депрессивного настроения. Агрессия (вспышки гнева, злости) проявляются в отношениях с детьми (может ударить, что-то сломать, затеять драку) и в отношениях с учителем': 0,
                             'Отдельные депрессивные проявления, плач без всяких на то причин. Агрессивные реакции: часто ссорится с детьми, повышает голос': 1,
                             'Отрицательные эмоции: - тревожность, огорчение, иногда страх; - обидчивость, вспыльчивость, раздражительность': 2,
                             'Эпизодически проявление сниженного настроения': 3,
                             'Спокойное эмоциональное состояние': 4,
                             'Хорошее настроение, часто улыбается, смеется': 5

                             }
        answers_df.replace(dct_replace_value, inplace=True)  # заменяем слова на цифры для подсчетов

        base_df['СПА_Значение'] = answers_df.sum(axis=1)
        base_df['СПА_Уровень'] = base_df['СПА_Значение'].apply(calc_level)

        base_df['ЭУД_Значение'] = answers_df.apply(calc_value_aud, axis=1)
        base_df['ЭУД_Процент'] = base_df['ЭУД_Значение'].apply(lambda x: calc_level_scale(x,10 ))
        base_df['ЭУД_Диапазон'] = base_df['ЭУД_Процент'].apply(calc_level_procent)

        base_df['УШНП_Значение'] = answers_df.apply(calc_value_ushnp, axis=1)
        base_df['УШНП_Процент'] = base_df['УШНП_Значение'].apply(lambda x: calc_level_scale(x, 10))
        base_df['УШНП_Диапазон'] = base_df['УШНП_Процент'].apply(calc_level_procent)

        base_df['УСК_Значение'] = answers_df.apply(calc_value_usk, axis=1)
        base_df['УСК_Процент'] = base_df['УСК_Значение'].apply(lambda x: calc_level_scale(x, 10))
        base_df['УСК_Диапазон'] = base_df['УСК_Процент'].apply(calc_level_procent)

        base_df['ЭБ_Значение'] = answers_df.apply(calc_value_ab, axis=1)
        base_df['ЭБ_Процент'] = base_df['ЭБ_Значение'].apply(lambda x: calc_level_scale(x, 5))
        base_df['ЭБ_Диапазон'] = base_df['ЭБ_Процент'].apply(calc_level_procent)

        base_df['УА_Значение'] = answers_df.apply(calc_value_ua, axis=1)
        base_df['УА_Процент'] = base_df['УА_Значение'].apply(lambda x: calc_level_scale(x, 5))
        base_df['УА_Диапазон'] = base_df['УА_Процент'].apply(calc_level_procent)

        base_df['УЗ_Значение'] = answers_df.apply(calc_value_uz, axis=1)
        base_df['УЗ_Процент'] = base_df['УЗ_Значение'].apply(lambda x: calc_level_scale(x, 5))
        base_df['УЗ_Диапазон'] = base_df['УЗ_Процент'].apply(calc_level_procent)

        base_df['ПУ_Значение'] = answers_df.apply(calc_value_pu, axis=1)
        base_df['ПУ_Процент'] = base_df['ПУ_Значение'].apply(lambda x: calc_level_scale(x, 5))
        base_df['ПУ_Диапазон'] = base_df['ПУ_Процент'].apply(calc_level_procent)

        base_df['ПП_Значение'] = answers_df.apply(calc_value_pp, axis=1)
        base_df['ПП_Процент'] = base_df['ПП_Значение'].apply(lambda x: calc_level_scale(x, 5))
        base_df['ПП_Диапазон'] = base_df['ПП_Процент'].apply(calc_level_procent)

        base_df['ВО_Значение'] = answers_df.apply(calc_value_vo, axis=1)
        base_df['ВО_Процент'] = base_df['ВО_Значение'].apply(lambda x: calc_level_scale(x, 5))
        base_df['ВО_Диапазон'] = base_df['ВО_Процент'].apply(calc_level_procent)

        base_df['ОУ_Значение'] = answers_df.apply(calc_value_ou, axis=1)
        base_df['ОУ_Процент'] = base_df['ОУ_Значение'].apply(lambda x: calc_level_scale(x, 5))
        base_df['ОУ_Диапазон'] = base_df['ОУ_Процент'].apply(calc_level_procent)

        base_df['Э_Значение'] = answers_df.apply(calc_value_a, axis=1)
        base_df['Э_Процент'] = base_df['Э_Значение'].apply(lambda x: calc_level_scale(x, 5))
        base_df['Э_Диапазон'] = base_df['Э_Процент'].apply(calc_level_procent)

        # Упорядочиваем
        result_df = base_df.iloc[:, quantity_cols_base_df:]  # отсекаем часть с результатами чтобы упорядочить
        lst_stens = ['ЭУД_Процент','УШНП_Процент','УСК_Процент','ЭБ_Процент']
        lst_sub_sh = ['УА_Процент','УЗ_Процент','ПУ_Процент','ПП_Процент','ВО_Процент','ОУ_Процент','Э_Процент',]
        result_df['Итоговые_проценты_критерии'] = result_df[lst_stens].apply(create_itog_stens, axis=1)
        result_df['Итоговые_проценты_шкалы'] = result_df[lst_sub_sh].apply(create_itog_stens, axis=1)

        new_order_lst = ['СПА_Значение', 'СПА_Уровень',
                         'Итоговые_проценты_критерии','Итоговые_проценты_шкалы',

                         'ЭУД_Процент', 'УШНП_Процент', 'УСК_Процент', 'ЭБ_Процент',
                         'УА_Процент','УЗ_Процент', 'ПУ_Процент', 'ПП_Процент', 'ВО_Процент', 'ОУ_Процент', 'Э_Процент',

                         'ЭУД_Диапазон', 'УШНП_Диапазон', 'УСК_Диапазон', 'ЭБ_Диапазон',
                         'УА_Диапазон','УЗ_Диапазон', 'ПУ_Диапазон', 'ПП_Диапазон', 'ВО_Диапазон', 'ОУ_Диапазон', 'Э_Диапазон',

                         'ЭУД_Значение', 'УШНП_Значение', 'УСК_Значение', 'ЭБ_Значение',
                         'УА_Значение','УЗ_Значение', 'ПУ_Значение', 'ПП_Значение', 'ВО_Значение', 'ОУ_Значение', 'Э_Значение'
                         ]
        result_df = result_df.reindex(columns=new_order_lst)  # изменяем порядок
        base_df = pd.concat([union_base_df, result_df], axis=1)  # соединяем и перезаписываем base_df

        # Создаем датафрейм для создания части в общий датафрейм
        part_df = pd.DataFrame()

        part_df['ЭОАРШЧСС_СПА_Значение'] = base_df['СПА_Значение']
        part_df['ЭОАРШЧСС_СПА_Уровень'] = base_df['СПА_Уровень']

        part_df['ЭОАРШЧСС_Итоговые_проценты_критерии'] = base_df['Итоговые_проценты_критерии']
        part_df['ЭОАРШЧСС_Итоговые_проценты_шкалы'] = base_df['Итоговые_проценты_шкалы']

        part_df['ЭОАРШЧСС_ЭУД_Значение'] = base_df['ЭУД_Значение']
        part_df['ЭОАРШЧСС_ЭУД_Процент'] = base_df['ЭУД_Процент']
        part_df['ЭОАРШЧСС_ЭУД_Диапазон'] = base_df['ЭУД_Диапазон']

        part_df['ЭОАРШЧСС_УШНП_Значение'] = base_df['УШНП_Значение']
        part_df['ЭОАРШЧСС_УШНП_Процент'] = base_df['УШНП_Процент']
        part_df['ЭОАРШЧСС_УШНП_Диапазон'] = base_df['УШНП_Диапазон']

        part_df['ЭОАРШЧСС_УСК_Значение'] = base_df['УСК_Значение']
        part_df['ЭОАРШЧСС_УСК_Процент'] = base_df['УСК_Процент']
        part_df['ЭОАРШЧСС_УСК_Диапазон'] = base_df['УСК_Диапазон']

        part_df['ЭОАРШЧСС_ЭБ_Значение'] = base_df['ЭБ_Значение']
        part_df['ЭОАРШЧСС_ЭБ_Процент'] = base_df['ЭБ_Процент']
        part_df['ЭОАРШЧСС_ЭБ_Диапазон'] = base_df['ЭБ_Диапазон']


        part_df['ЭОАРШЧСС_УА_Значение'] = base_df['УА_Значение']
        part_df['ЭОАРШЧСС_УА_Процент'] = base_df['УА_Процент']
        part_df['ЭОАРШЧСС_УА_Диапазон'] = base_df['УА_Диапазон']

        part_df['ЭОАРШЧСС_УЗ_Значение'] = base_df['УЗ_Значение']
        part_df['ЭОАРШЧСС_УЗ_Процент'] = base_df['УЗ_Процент']
        part_df['ЭОАРШЧСС_УЗ_Диапазон'] = base_df['УЗ_Диапазон']

        part_df['ЭОАРШЧСС_ПУ_Значение'] = base_df['ПУ_Значение']
        part_df['ЭОАРШЧСС_ПУ_Процент'] = base_df['ПУ_Процент']
        part_df['ЭОАРШЧСС_ПУ_Диапазон'] = base_df['ПУ_Диапазон']

        part_df['ЭОАРШЧСС_ПП_Значение'] = base_df['ПП_Значение']
        part_df['ЭОАРШЧСС_ПП_Процент'] = base_df['ПП_Процент']
        part_df['ЭОАРШЧСС_ПП_Диапазон'] = base_df['ПП_Диапазон']

        part_df['ЭОАРШЧСС_ВО_Значение'] = base_df['ВО_Значение']
        part_df['ЭОАРШЧСС_ВО_Процент'] = base_df['ВО_Процент']
        part_df['ЭОАРШЧСС_ВО_Диапазон'] = base_df['ВО_Диапазон']

        part_df['ЭОАРШЧСС_ОУ_Значение'] = base_df['ОУ_Значение']
        part_df['ЭОАРШЧСС_ОУ_Процент'] = base_df['ОУ_Процент']
        part_df['ЭОАРШЧСС_ОУ_Диапазон'] = base_df['ОУ_Диапазон']

        part_df['ЭОАРШЧСС_Э_Значение'] = base_df['Э_Значение']
        part_df['ЭОАРШЧСС_Э_Процент'] = base_df['Э_Процент']
        part_df['ЭОАРШЧСС_Э_Диапазон'] = base_df['Э_Диапазон']

        part_df.replace({'76-100%': '76-100% СПА', '51-75%': '51-75% СПА',
                         '26-50%': '26-50% СПА', '0-25%': '0-25% СПА',
                         }, inplace=True)

        out_answer_df = pd.concat([out_answer_df, answers_df], axis=1)  # Датафрейм для проверки

        base_df.sort_values(by='СПА_Значение', inplace=True, ascending=True)

        # Делаем свод  по  основному показателю
        dct_svod = {'СПА_Значение': 'СПА_Уровень',
                    }

        dct_rename_svod = {
            'СПА_Значение': 'Уровень социально психологической адаптации',
        }

        lst_base = ['нормальная адаптация','неполная адаптация','дезадаптация']
        base_svod_df = create_union_svod(base_df, dct_svod, dct_rename_svod, lst_base)


        # Делаем свод  по  основному показателю
        dct_factor_svod = {'ЭУД_Значение': 'ЭУД_Диапазон',
                           'УШНП_Значение': 'УШНП_Диапазон',
                           'УСК_Значение': 'УСК_Диапазон',
                           'ЭБ_Значение': 'ЭБ_Диапазон',
                    }

        dct_rename_factor_svod = {
            'ЭУД_Значение': 'Критерий ЭУД',
            'УШНП_Значение': 'Критерий УШНП',
            'УСК_Значение': 'Критерий СК',
            'ЭБ_Значение': 'Критерий ЭБ',
        }

        lst_sub = ['76-100%', '51-75%', '26-50%', '0-25%']
        base_factor_svod_df = create_union_svod(base_df, dct_factor_svod, dct_rename_factor_svod, lst_sub)

        # Делаем свод  по  шкалам
        dct_svod_sub = {'УА_Значение': 'УА_Диапазон',
                        'УЗ_Значение': 'УЗ_Диапазон',
                        'ПУ_Значение': 'ПУ_Диапазон',
                        'ПП_Значение': 'ПП_Диапазон',
                        'ВО_Значение': 'ВО_Диапазон',

                        'ОУ_Значение': 'ОУ_Диапазон',
                        'Э_Значение': 'Э_Диапазон',
                        }

        dct_rename_svod_sub = {'УА_Значение': 'УА',
                               'УЗ_Значение': 'УЗ',
                               'ПУ_Значение': 'ПУ',
                               'ПП_Значение': 'ПП',
                               'ВО_Значение': 'ВО',

                               'ОУ_Значение': 'ОУ',
                               'Э_Значение': 'Э',
                               }


        base_svod_sub_df = create_union_svod(base_df, dct_svod_sub, dct_rename_svod_sub, lst_sub)

        # считаем среднее значение по шкалам
        avg_kda = round(base_df['СПА_Значение'].mean(), 2)
        avg_ro = round(base_df['ЭУД_Значение'].mean(), 2)
        avg_ngsh = round(base_df['УШНП_Значение'].mean(), 2)
        avg_l = round(base_df['УСК_Значение'].mean(), 2)
        avg_ns = round(base_df['ЭБ_Значение'].mean(), 2)

        avg_i = round(base_df['УА_Значение'].mean(), 2)
        avg_gs = round(base_df['УЗ_Значение'].mean(), 2)
        avg_ins = round(base_df['ПУ_Значение'].mean(), 2)
        avg_np = round(base_df['ПП_Значение'].mean(), 2)
        avg_nm = round(base_df['ВО_Значение'].mean(), 2)
        avg_as = round(base_df['ОУ_Значение'].mean(), 2)
        avg_nid = round(base_df['Э_Значение'].mean(), 2)

        avg_dct = {'Среднее значение социально психологической адаптации': avg_kda,
                   'Среднее значение критерия Родительское отношение': avg_ro,
                   'Среднее значение критерия Неготовность к школе': avg_ngsh,
                   'Среднее значение критерия Леворукость': avg_l,
                   'Среднее значение критерия Невротические симптомы': avg_ns,

                   'Среднее значение шкалы Учебная активность': avg_i,
                   'Среднее значение шкалы Усвоение знаний (успеваемость)': avg_gs,
                   'Среднее значение шкалы Поведение на уроке': avg_ins,
                   'Среднее значение шкалы Поведение на перемене': avg_np,
                   'Среднее значение шкалы Взаимоотношения с одноклассниками': avg_nm,
                   'Среднее значение шкалы Отношение к учителю': avg_as,
                   'Среднее значение шкалы Эмоции': avg_nid,
                   }

        avg_df = pd.DataFrame.from_dict(avg_dct, orient='index')
        avg_df = avg_df.reset_index()
        avg_df.columns = ['Показатель', 'Среднее значение']

        # формируем основной словарь
        out_dct = {'Списочный результат': base_df,
                   'Список для проверки': out_answer_df,
                   'Свод СПА': base_svod_df,
                   'Свод Критерии': base_factor_svod_df,
                   'Свод Шкалы': base_svod_sub_df,
                   'Среднее': avg_df,
                   }

        dct_prefix_ip = {'СПА_Уровень': 'СПА',

                         }
        out_dct = create_list_on_level_spa(base_df, out_dct, lst_base, dct_prefix_ip)

        dct_prefix_factor = {'ЭУД_Диапазон': 'ЭУД',
                             'УШНП_Диапазон': 'УШНП',
                             'УСК_Диапазон': 'УСК',
                             'ЭБ_Диапазон': 'ЭБ',

                         }
        out_dct = create_list_on_level(base_df, out_dct, lst_sub, dct_prefix_factor)

        dct_prefix = {'УА_Диапазон': 'РО',
                      'УЗ_Диапазон': 'НГШ',
                      'ПУ_Диапазон': 'Л',
                      'ПП_Диапазон': 'НС',
                      'ВО_Диапазон': 'И',

                      'ОУ_Диапазон': 'ГС',
                      'Э_Диапазон': 'ИНС',

                      }

        out_dct = create_list_on_level(base_df, out_dct, lst_sub, dct_prefix)

        """
                        Сохраняем в зависимости от необходимости делать своды по определенным колонкам
                        """
        if len(lst_svod_cols) == 0:
            return out_dct, part_df

        else:
            out_dct = create_result_aoarsh_chir_ss(base_df, out_dct, lst_svod_cols)
            return out_dct, part_df

    except BadOrderAORSHCHSS:
        messagebox.showerror('Лахеcис',
                             f'При обработке вопросов теста Экспертная оценка адаптированности ребёнка к школе Чирков Соколова Сорокина обнаружены неправильные вопросы. Проверьте названия колонок с вопросами:\n'
                             f'{error_order_message[:5000]}\n'
                             f'Используйте при создании Яндекс-формы написание вопросов из руководства пользователя программы Лахесис.')
    except BadValueAORSHCHSS:
        messagebox.showerror('Лахеcис',
                             f'При обработке вопросов теста Экспертная оценка адаптированности ребёнка к школе Чирков Соколова Сорокина обнаружены неправильные варианты ответов. Проверьте ответы на указанных строках:\n'
                             f'{error_message[:5000]}\n'
                             f'Используйте при создании Яндекс-формы написание вариантов ответа из руководства пользователя программы Лахесис.')


    except BadCountColumnsAORSHCHSS:
        messagebox.showerror('Лахеcис',
                             f'Проверьте количество колонок с ответами на Экспертная оценка адаптированности ребёнка к школе Чирков Соколова Сорокина\n'
                             f'Должно быть 7 колонок с ответами')

































