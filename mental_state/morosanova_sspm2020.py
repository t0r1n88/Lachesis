"""
Скрипт для обработки результатов Стиль саморегуляции поведения, ССПМ-2020 В.И. Моросанова, Н.Г. Кондратюк

"""

import pandas as pd
import re
from tkinter import messagebox
from lachesis_support_functions import round_mean_two,calc_count_scale,create_union_svod, create_list_on_level

class BadOrderSSPMTTMK(Exception):
    """
    Исключение для обработки случая когда колонки не совпадают
    """
    pass


class BadValueSSPMTTMK(Exception):
    """
    Исключение для неправильных значений в вариантах ответов
    """
    pass

class BadCountColumnsSSPMTTMK(Exception):
    """
    Исключение для обработки случая если количество колонок не равно 28
    """
    pass


def calc_value_ous(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_neg = [1,15,
               4,18,24,
               11,
               17,23,
               6,13,20,27]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
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


def calc_level(value):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """
    if 28 <= value <= 50:
        return '28-50'
    elif 51 <= value <= 73:
        return '51-73'
    elif 74 <= value <= 95:
        return '74-95'
    elif 96 <= value <= 118:
        return '96-118'

    else:
        return '119-140'

def calc_level_sub(value):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """
    if 4 <= value <= 7:
        return '4-7'
    elif 8 <= value <= 11:
        return '8-11'
    elif 12 <= value <= 15:
        return '12-15'
    else:
        return '16-20'


def calc_value_pc(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [1,8,15,22]
    lst_neg = [1,15]
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

def calc_value_mu(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [4,10,18,24]
    lst_neg = [4,18,24]
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


def calc_value_pd(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [2,11,16,26]
    lst_neg = [11]
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

def calc_value_or(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [3,9,17,23]
    lst_neg = [17,23]
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


def calc_value_g(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [5,12,19,25]
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

def calc_value_n(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [6,13,20,27]
    lst_neg = [6,13,20,27]
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


def calc_value_ns(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [7,14,21,28]
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


def create_result_sspmtt_mor(base_df:pd.DataFrame, out_dct:dict, lst_svod_cols:list):
    """
    Функция для подсчета результата если указаны колонки по которым нужно провести свод
    :param df: датафрейм с результатами
    :param out_dct: словарь с уже подсчитанными базовыми данными
    :param lst_svod_cols: список сводных колонок
    :return: словарь
    """
    lst_l = ['28-50','51-73','74-95','96-118','119-140']
    lst_reindex_one_level_l_cols = lst_svod_cols.copy()
    lst_reindex_one_level_l_cols.extend(['28-50','51-73','74-95','96-118','119-140',
                                       'Итого'])  # Основная шкала

    svod_count_one_level_l_df = calc_count_scale(base_df, lst_svod_cols,
                                                 'ОУС_Значение',
                                                 'ОУС_Диапазон',
                                                 lst_reindex_one_level_l_cols, lst_l)


    lst_level = ['4-7','8-11','12-15','16-20']

    lst_reindex_one_level_cols = lst_svod_cols.copy()
    lst_reindex_one_level_cols.extend(['4-7','8-11','12-15','16-20',
                                       'Итого'])  # Основная шкала


    # АД
    svod_count_one_level_pc_df = calc_count_scale(base_df, lst_svod_cols,
                                                 'ПЦ_Значение',
                                                 'ПЦ_Диапазон',
                                                 lst_reindex_one_level_cols, lst_level)
    svod_count_one_level_mu_df = calc_count_scale(base_df, lst_svod_cols,
                                                 'МУ_Значение',
                                                 'МУ_Диапазон',
                                                 lst_reindex_one_level_cols, lst_level)
    svod_count_one_level_pd_df = calc_count_scale(base_df, lst_svod_cols,
                                                 'ПД_Значение',
                                                 'ПД_Диапазон',
                                                 lst_reindex_one_level_cols, lst_level)
    svod_count_one_level_or_df = calc_count_scale(base_df, lst_svod_cols,
                                                 'ОР_Значение',
                                                 'ОР_Диапазон',
                                                 lst_reindex_one_level_cols, lst_level)

    svod_count_one_level_g_df = calc_count_scale(base_df, lst_svod_cols,
                                                 'Г_Значение',
                                                 'Г_Диапазон',
                                                 lst_reindex_one_level_cols, lst_level)

    svod_count_one_level_n_df = calc_count_scale(base_df, lst_svod_cols,
                                                 'Н_Значение',
                                                 'Н_Диапазон',
                                                 lst_reindex_one_level_cols, lst_level)

    svod_count_one_level_ns_df = calc_count_scale(base_df, lst_svod_cols,
                                                 'НС_Значение',
                                                 'НС_Диапазон',
                                                 lst_reindex_one_level_cols, lst_level)

    # Считаем среднее по субшкалам
    svod_mean_one_df = pd.pivot_table(base_df,
                                      index=lst_svod_cols,
                                      values=['ОУС_Значение',
                                              'ПЦ_Значение',
                                              'МУ_Значение',
                                              'ПД_Значение',
                                              'ОР_Значение',

                                              'Г_Значение',
                                              'Н_Значение',
                                              'НС_Значение',
                                              ],
                                      aggfunc=round_mean_two)
    svod_mean_one_df.reset_index(inplace=True)

    # упорядочиваем колонки
    new_order_cols = lst_svod_cols.copy()
    new_order_cols.extend((['ОУС_Значение',
                                              'ПЦ_Значение',
                                              'МУ_Значение',
                                              'ПД_Значение',
                                              'ОР_Значение',

                                              'Г_Значение',
                                              'Н_Значение',
                                              'НС_Значение',
                            ]))
    svod_mean_one_df = svod_mean_one_df.reindex(columns=new_order_cols)

    dct_rename_cols_mean = {'ОУС_Значение': 'Ср. Общий уровень саморегуляции',
                            'ПЦ_Значение': 'Ср. Планирование целей',
                            'МУ_Значение': 'Ср. Моделирование значимых условий достижения целей',
                            'ПД_Значение': 'Ср. Программирование действий',
                            'ОР_Значение': 'Ср. Оценивание результатов',

                            'Г_Значение': 'Ср. Гибкость',
                            'Н_Значение': 'Ср. Надежность',
                            'НС_Значение': 'Ср. Настойчивость',
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
                    f'ОУС {out_name}': svod_count_one_level_l_df,
                    f'ПЦ {out_name}': svod_count_one_level_pc_df,
                    f'МУ {out_name}': svod_count_one_level_mu_df,
                    f'ПД {out_name}': svod_count_one_level_pd_df,
                    f'ОР {out_name}': svod_count_one_level_or_df,

                    f'Г {out_name}': svod_count_one_level_g_df,
                    f'Н {out_name}': svod_count_one_level_n_df,
                    f'НС {out_name}': svod_count_one_level_ns_df,
                    })


    if len(lst_svod_cols) == 1:
        return out_dct

    else:
        for idx, name_column in enumerate(lst_svod_cols):
            lst_reindex_column_level_l_cols = [lst_svod_cols[idx], '28-50','51-73','74-95','96-118','119-140',
                                               'Итого']

            svod_count_column_level_l_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                            'ОУС_Значение',
                                                            'ОУС_Диапазон',
                                                            lst_reindex_column_level_l_cols, lst_l)

            lst_level = ['4-7','8-11','12-15','16-20']

            lst_reindex_column_level_cols = [lst_svod_cols[idx], '4-7','8-11','12-15','16-20',
                                             'Итого']

            # АД
            svod_count_column_level_pc_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                             'ПЦ_Значение',
                                                             'ПЦ_Диапазон',
                                                             lst_reindex_column_level_cols, lst_level)
            svod_count_column_level_mu_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                             'МУ_Значение',
                                                             'МУ_Диапазон',
                                                             lst_reindex_column_level_cols, lst_level)
            svod_count_column_level_pd_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                             'ПД_Значение',
                                                             'ПД_Диапазон',
                                                             lst_reindex_column_level_cols, lst_level)
            svod_count_column_level_or_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                             'ОР_Значение',
                                                             'ОР_Диапазон',
                                                             lst_reindex_column_level_cols, lst_level)

            svod_count_column_level_g_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                            'Г_Значение',
                                                            'Г_Диапазон',
                                                            lst_reindex_column_level_cols, lst_level)

            svod_count_column_level_n_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                            'Н_Значение',
                                                            'Н_Диапазон',
                                                            lst_reindex_column_level_cols, lst_level)

            svod_count_column_level_ns_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                             'НС_Значение',
                                                             'НС_Диапазон',
                                                             lst_reindex_column_level_cols, lst_level)

            # Считаем среднее по субшкалам
            svod_mean_column_df = pd.pivot_table(base_df,
                                                 index=[lst_svod_cols[idx]],
                                                 values=['ОУС_Значение',
                                                         'ПЦ_Значение',
                                                         'МУ_Значение',
                                                         'ПД_Значение',
                                                         'ОР_Значение',

                                                         'Г_Значение',
                                                         'Н_Значение',
                                                         'НС_Значение',
                                                         ],
                                                 aggfunc=round_mean_two)
            svod_mean_column_df.reset_index(inplace=True)

            # упорядочиваем колонки
            new_order_cols = [lst_svod_cols[idx]].copy()
            new_order_cols.extend((['ОУС_Значение',
                                    'ПЦ_Значение',
                                    'МУ_Значение',
                                    'ПД_Значение',
                                    'ОР_Значение',

                                    'Г_Значение',
                                    'Н_Значение',
                                    'НС_Значение',
                                    ]))
            svod_mean_column_df = svod_mean_column_df.reindex(columns=new_order_cols)

            dct_rename_cols_mean = {'ОУС_Значение': 'Ср. Общий уровень саморегуляции',
                                    'ПЦ_Значение': 'Ср. Планирование целей',
                                    'МУ_Значение': 'Ср. Моделирование значимых условий достижения целей',
                                    'ПД_Значение': 'Ср. Программирование действий',
                                    'ОР_Значение': 'Ср. Оценивание результатов',

                                    'Г_Значение': 'Ср. Гибкость',
                                    'Н_Значение': 'Ср. Надежность',
                                    'НС_Значение': 'Ср. Настойчивость',
                                    }
            svod_mean_column_df.rename(columns=dct_rename_cols_mean, inplace=True)

            # Готовим наименование
            name_column = lst_svod_cols[idx]
            name_column = re.sub(r'[\[\]\'+()<> :"?*|\\/]', '_', name_column)
            name_column = name_column[:15]

            out_dct.update({f'Ср {name_column}': svod_mean_column_df,
                            f'ОУС {name_column}': svod_count_column_level_l_df,
                            f'ПЦ {name_column}': svod_count_column_level_pc_df,
                            f'МУ {name_column}': svod_count_column_level_mu_df,
                            f'ПД {name_column}': svod_count_column_level_pd_df,
                            f'ОР {name_column}': svod_count_column_level_or_df,

                            f'Г {name_column}': svod_count_column_level_g_df,
                            f'Н {name_column}': svod_count_column_level_n_df,
                            f'НС {name_column}': svod_count_column_level_ns_df,
                            })
        return out_dct















def processing_sspmtt_moros(base_df: pd.DataFrame, answers_df: pd.DataFrame, lst_svod_cols:list):
    """
    Функция для обработки
    :param base_df: часть датафрейма с описательными колонками
    :param answers_df: часть датафрейма с ответами
    :param lst_svod_cols:  список с колонками по которым нужно делать свод
    """
    try:
        out_answer_df = base_df.copy()  # делаем копию для последующего соединения с сырыми ответами
        if len(answers_df.columns) != 28:  # проверяем количество колонок с вопросами
            raise BadCountColumnsSSPMTTMK

        # очищаем названия колонок от возможных сочетаний .1 которые добавляет пандас при одинаковых колонках
        clean_df_lst = []
        for name_column in answers_df.columns:
            clean_name = re.sub(r'.\d+$', '', name_column)
            clean_df_lst.append(clean_name)

        answers_df.columns = clean_df_lst

        lst_check_cols = ['Не строю планы на будущее, так как обстоятельства могут их изменить',
                          'Для успеха дела мне необходима программа действий',
                          'В конце дня подвожу итоги того, что было сделано',
                          'Не всегда вовремя замечаю изменения обстоятельств и из-за этого терплю неудачи',
                          'Люблю перемены в жизни, смену обстановки и образа жизни',
                          'Как правило, мне трудно работать, когда я расстроен',
                          'Всегда добиваюсь удовлетворяющего меня результата',
                          'Цели на будущее детально планирую',
                          'Накануне Нового года оцениваю, что удалось сделать в уходящем году',
                          'Я всегда замечаю изменение ситуации и использую это в своих интересах',

                          'Начиная работу, не считаю необходимым заранее продумать свои действия и их последовательность',
                          'Без труда переключаюсь на новое дело',
                          'После ссоры с близким человеком не могу следовать намеченному на день плану',
                          'Проявляю упорство в решении сложной задачи',
                          'Не задумываюсь много о жизненных целях, скорее «плыву по течению»',
                          'Принимаясь за выполнение сложного дела, делю его на этапы',
                          'Не оцениваю промежуточные итоги работы, считая это необязательным',
                          'Мне трудно вовремя учесть изменение обстоятельств',
                          'Переход на новую систему работы не причиняет мне особых неудобств',
                          'Результат моей работы часто зависит от моего настроения',

                          'Не отступаюсь от начатого дела в любых условиях',
                          'Заранее планирую свою жизнь',
                          'Мне не свойственно подводить итоги того, что было сделано за день',
                          'Не всегда удается определить главные условия достижения задуманного',
                          'Легко адаптируюсь в новых ситуациях',
                          'Для выполнения дела мне нужно определить последовательность своих действий',
                          'Допускаю много ошибок, когда волнуюсь',
                          'Настойчиво стремлюсь добиться нужного результата'
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
            raise BadOrderSSPMTTMK

        # словарь для замены слов на числа
        dct_replace_value = {'неверно': 1,
                             'пожалуй, неверно': 2,
                             'затрудняюсь ответить': 3,
                             'пожалуй, верно': 4,
                             'верно': 5,
                             }
        valid_values = [1, 2, 3, 4, 5]
        answers_df.replace(dct_replace_value, inplace=True)  # заменяем слова на цифры для подсчетов

        # Проверяем, есть ли значения, отличающиеся от указанных в списке
        lst_error_answers = []  # список для хранения строк где найдены неправильные ответы

        for i in range(28):
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
            raise BadValueSSPMTTMK

        base_df['ОУС_Значение'] = answers_df.apply(calc_value_ous, axis=1)
        base_df['ОУС_Диапазон'] = base_df['ОУС_Значение'].apply(calc_level)

        base_df['ПЦ_Значение'] = answers_df.apply(calc_value_pc, axis=1)
        base_df['ПЦ_Диапазон'] = base_df['ПЦ_Значение'].apply(calc_level_sub)

        base_df['МУ_Значение'] = answers_df.apply(calc_value_mu, axis=1)
        base_df['МУ_Диапазон'] = base_df['МУ_Значение'].apply(calc_level_sub)

        base_df['ПД_Значение'] = answers_df.apply(calc_value_pd, axis=1)
        base_df['ПД_Диапазон'] = base_df['ПД_Значение'].apply(calc_level_sub)

        base_df['ОР_Значение'] = answers_df.apply(calc_value_or, axis=1)
        base_df['ОР_Диапазон'] = base_df['ОР_Значение'].apply(calc_level_sub)

        base_df['Г_Значение'] = answers_df.apply(calc_value_g, axis=1)
        base_df['Г_Диапазон'] = base_df['Г_Значение'].apply(calc_level_sub)

        base_df['Н_Значение'] = answers_df.apply(calc_value_n, axis=1)
        base_df['Н_Диапазон'] = base_df['Н_Значение'].apply(calc_level_sub)

        base_df['НС_Значение'] = answers_df.apply(calc_value_ns, axis=1)
        base_df['НС_Диапазон'] = base_df['НС_Значение'].apply(calc_level_sub)

        # Создаем датафрейм для создания части в общий датафрейм
        part_df = pd.DataFrame()
        part_df['ССПМДД_ОУС_Значение'] = base_df['ОУС_Значение']
        part_df['ССПМДД_ОУС_Диапазон'] = base_df['ОУС_Диапазон']

        part_df['ССПМДД_ПЦ_Значение'] = base_df['ПЦ_Значение']
        part_df['ССПМДД_ПЦ_Диапазон'] = base_df['ПЦ_Диапазон']

        part_df['ССПМДД_МУ_Значение'] = base_df['МУ_Значение']
        part_df['ССПМДД_МУ_Диапазон'] = base_df['МУ_Диапазон']

        part_df['ССПМДД_ПД_Значение'] = base_df['ПД_Значение']
        part_df['ССПМДД_ПД_Диапазон'] = base_df['ПД_Диапазон']

        part_df['ССПМДД_ОР_Значение'] = base_df['ОР_Значение']
        part_df['ССПМДД_ОР_Диапазон'] = base_df['ОР_Диапазон']

        part_df['ССПМДД_Г_Значение'] = base_df['Г_Значение']
        part_df['ССПМДД_Г_Диапазон'] = base_df['Г_Диапазон']

        part_df['ССПМДД_Н_Значение'] = base_df['Н_Значение']
        part_df['ССПМДД_Н_Диапазон'] = base_df['Н_Диапазон']

        part_df['ССПМДД_НС_Значение'] = base_df['НС_Значение']
        part_df['ССПМДД_НС_Диапазон'] = base_df['НС_Диапазон']

        base_df.sort_values(by='ОУС_Значение', ascending=True, inplace=True)  # сортируем
        out_answer_df = pd.concat([out_answer_df, answers_df], axis=1)  # Датафрейм для проверки

        # Делаем свод  по  шкалам
        dct_svod_l = {'ОУС_Значение': 'ОУС_Диапазон',
                      }

        dct_rename_svod_l = {'ОУС_Значение': 'Общий уровень саморегуляции',
                             }

        lst_l = ['28-50','51-73','74-95','96-118','119-140']

        base_svod_l_df = create_union_svod(base_df, dct_svod_l, dct_rename_svod_l, lst_l)

        # Делаем свод  по  шкалам
        dct_svod_sub = {'ПЦ_Значение': 'ПЦ_Диапазон',
                        'МУ_Значение': 'МУ_Диапазон',
                        'ПД_Значение': 'ПД_Диапазон',
                        'ОР_Значение': 'ОР_Диапазон',

                        'Г_Значение': 'Г_Диапазон',
                        'Н_Значение': 'Н_Диапазон',
                        'НС_Значение': 'НС_Диапазон',
                        }

        dct_rename_svod_sub = {'ПЦ_Значение': 'Планирование целей',
                               'МУ_Значение': 'Моделирование значимых условий достижения целей',
                               'ПД_Значение': 'Программирование действий',
                               'ОР_Значение': 'Оценивание результатов',

                               'Г_Значение': 'Гибкость',
                               'Н_Значение': 'Надежность',
                               'НС_Значение': 'Настойчивость',

                               }

        lst_sub = ['4-7','8-11','12-15','16-20']

        base_svod_sub_df = create_union_svod(base_df, dct_svod_sub, dct_rename_svod_sub, lst_sub)

        avg_ous = round(base_df['ОУС_Значение'].mean(), 2)

        avg_pc = round(base_df['ПЦ_Значение'].mean(), 2)
        avg_mu = round(base_df['МУ_Значение'].mean(), 2)
        avg_pd = round(base_df['ПД_Значение'].mean(), 2)
        avg_or = round(base_df['ОР_Значение'].mean(), 2)

        avg_g = round(base_df['Г_Значение'].mean(), 2)
        avg_n = round(base_df['Н_Значение'].mean(), 2)
        avg_ns = round(base_df['НС_Значение'].mean(), 2)

        avg_dct = {'Среднее значение Общий уровень саморегуляции': avg_ous,

                   'Среднее значение шкалы Планирование целей': avg_pc,
                   'Среднее значение шкалы Моделирование значимых условий достижения целей': avg_mu,
                   'Среднее значение шкалы Программирование действий': avg_pd,
                   'Среднее значение шкалы Оценивание результатов': avg_or,

                   'Среднее значение шкалы Гибкость': avg_g,
                   'Среднее значение шкалы Надежность': avg_n,
                   'Среднее значение шкалы Настойчивость': avg_ns,
                   }

        avg_df = pd.DataFrame.from_dict(avg_dct, orient='index')
        avg_df = avg_df.reset_index()
        avg_df.columns = ['Показатель', 'Среднее значение']

        # формируем основной словарь
        out_dct = {'Списочный результат': base_df,
                   'Список для проверки': out_answer_df,
                   'Свод ОУС': base_svod_l_df,
                   'Свод Шкалы': base_svod_sub_df,
                   'Среднее': avg_df,
                   }

        dct_l = {
            'ОУС_Диапазон': 'ОУС',
        }

        out_dct = create_list_on_level(base_df, out_dct, lst_l, dct_l)

        dct_prefix = {
            'ПЦ_Диапазон': 'ПЦ',
            'МУ_Диапазон': 'МУ',
            'ПД_Диапазон': 'ПД',
            'ОР_Диапазон': 'ОР',

            'Г_Диапазон': 'Г',
            'Н_Диапазон': 'Н',
            'НС_Диапазон': 'НС',
        }

        out_dct = create_list_on_level(base_df, out_dct, lst_sub, dct_prefix)

        """
                        Сохраняем в зависимости от необходимости делать своды по определенным колонкам
                        """
        if len(lst_svod_cols) == 0:
            return out_dct, part_df
        else:
            out_dct = create_result_sspmtt_mor(base_df, out_dct, lst_svod_cols)
            return out_dct, part_df

    except BadOrderSSPMTTMK:
        messagebox.showerror('Лахеcис',
                             f'При обработке вопросов теста Стиль саморегуляции поведения, ССПМ 2020 Моросанова обнаружены неправильные вопросы. Проверьте названия колонок с вопросами:\n'
                             f'{error_order_message[:5000]}\n'
                             f'Используйте при создании Яндекс-формы написание вопросов из руководства пользователя программы Лахесис.')
    except BadValueSSPMTTMK:
        messagebox.showerror('Лахеcис',
                             f'При обработке вопросов теста Стиль саморегуляции поведения, ССПМ 2020 Моросанова  обнаружены неправильные варианты ответов. Проверьте ответы на указанных строках:\n'
                             f'{error_message[:5000]}\n'
                             f'Используйте при создании Яндекс-формы написание вариантов ответа из руководства пользователя программы Лахесис.')


    except BadCountColumnsSSPMTTMK:
        messagebox.showerror('Лахеcис',
                             f'Проверьте количество колонок с ответами на Тест Стиль саморегуляции поведения, ССПМ 2020 Моросанова\n'
                             f'Должно быть 28 колонок с ответами')



















