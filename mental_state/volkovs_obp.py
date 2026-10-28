"""
Скрипт для обработки результатов тестаОпросник благополучия подростков EPOCH Адаптация Е. Н. Волкова, И. В. Волкова

"""

import pandas as pd
import re
from tkinter import messagebox
from lachesis_support_functions import round_mean,create_union_svod,create_list_on_level


class BadOrderOBPVV(Exception):
    """
    Исключение для обработки случая когда колонки не совпадают
    """
    pass


class BadValueOBPVV(Exception):
    """
    Исключение для неправильных значений в вариантах ответов
    """
    pass

class BadCountColumnsOBPVV(Exception):
    """
    Исключение для обработки случая если количество колонок не равно 20
    """
    pass



def calc_value_ip(row):
    """
    Функция для подсчета значения шкалы Тревожность
    :param row: строка с ответами
    :return: число
    """

    value_forward = 0  # счетчик прямых ответов

    for value in row:
        value_forward += value

    return round(value_forward / len(row), 2)



def calc_level(value):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """
    if 1.00 <= value <= 1.99:
        return '1.00-1.99'
    elif 2.00 <= value <= 2.99:
        return '2.00-2.99'
    elif 3.00 <= value <= 3.99:
        return '3.00-3.99'
    else:
        return '4.00-5.00'



def calc_sub_value_engagement(row):
    """
    Функция для подсчета значения шкалы Тревожность
    :param row: строка с ответами
    :return: число
    """
    lst_pr = [5,7,11,12]

    value_forward = 0 # счетчик прямых ответов

    for idx, value in enumerate(row):
        if idx +1 in lst_pr:
            value_forward += value

    return round(value_forward / len(lst_pr), 2)


def calc_sub_value_perseverance(row):
    """
    Функция для подсчета значения шкалы Тревожность
    :param row: строка с ответами
    :return: число
    """
    lst_pr = [2,9,17,19]

    value_forward = 0 # счетчик прямых ответов

    for idx, value in enumerate(row):
        if idx +1 in lst_pr:
            value_forward += value

    return round(value_forward / len(lst_pr), 2)


def calc_sub_value_optimism(row):
    """
    Функция для подсчета значения шкалы Тревожность
    :param row: строка с ответами
    :return: число
    """
    lst_pr = [3,13,15,18]

    value_forward = 0 # счетчик прямых ответов

    for idx, value in enumerate(row):
        if idx +1 in lst_pr:
            value_forward += value

    return round(value_forward / len(lst_pr), 2)


def calc_sub_value_connectedness(row):
    """
    Функция для подсчета значения шкалы Тревожность
    :param row: строка с ответами
    :return: число
    """
    lst_pr = [1,10,14,16]

    value_forward = 0 # счетчик прямых ответов

    for idx, value in enumerate(row):
        if idx +1 in lst_pr:
            value_forward += value

    return round(value_forward / len(lst_pr), 2)


def calc_sub_value_happiness(row):
    """
    Функция для подсчета значения шкалы Тревожность
    :param row: строка с ответами
    :return: число
    """
    lst_pr = [4,6,8,20]

    value_forward = 0 # счетчик прямых ответов

    for idx, value in enumerate(row):
        if idx +1 in lst_pr:
            value_forward += value

    return round(value_forward / len(lst_pr), 2)


def calc_count_level_sub(df:pd.DataFrame, lst_cat:list, val_cat, col_cat, lst_cols:list):
    """
    Функция для создания сводных датафреймов по шкалам

    :param df: датафрейм с данными
    :param lst_cat:список колонок по которым будет формироваться свод
    :param val_cat:значение по которому будет формироваться свод
    :param col_cat: колонка по которой будет формироваться свод
    :param lst_cols: список с колонками
    :return:датафрейм
    """
    count_df = pd.pivot_table(df, index=lst_cat,
                                             columns=col_cat,
                                             values=val_cat,
                                             aggfunc='count', margins=True, margins_name='Итого')


    count_df.reset_index(inplace=True)
    count_df = count_df.reindex(columns=lst_cols)
    count_df['% 1.00-1.99 от общего'] = round(
        count_df['1.00-1.99'] / count_df['Итого'], 2) * 100
    count_df['% 2.00-2.99 от общего'] = round(
        count_df['2.00-2.99'] / count_df['Итого'], 2) * 100
    count_df['% 3.00-3.99 от общего'] = round(
        count_df['3.00-3.99'] / count_df['Итого'], 2) * 100
    count_df['% 4.00-5.00 от общего'] = round(
        count_df['4.00-5.00'] / count_df['Итого'], 2) * 100

    return count_df




def create_result_obpvv(base_df:pd.DataFrame, out_dct:dict, lst_svod_cols:list):
    """
    Функция для подсчета результата если указаны колонки по которым нужно провести свод
    :param df: датафрейм с результатами
    :param out_dct: словарь с уже подсчитанными базовыми данными
    :param lst_svod_cols: список сводных колонок
    :return: словарь
    """
    lst_reindex_one_level_cols = lst_svod_cols.copy()
    lst_reindex_one_level_cols.extend( ['1.00-1.99','2.00-2.99','3.00-3.99','4.00-5.00',
                                   'Итого'])


    # Субшкалы
    svod_count_one_level_anxiety_df = calc_count_level_sub(base_df, lst_svod_cols,
                                                      'Значение_ИП',
                                                      'Диапазон_ИП',
                                                      lst_reindex_one_level_cols)

    svod_count_one_level_frust_df = calc_count_level_sub(base_df, lst_svod_cols,
                                                          'Значение_шкалы_Вовлеченность',
                                                          'Диапазон_шкалы_Вовлеченность',
                                                          lst_reindex_one_level_cols)

    svod_count_one_level_agres_df = calc_count_level_sub(base_df, lst_svod_cols,
                                                         'Значение_шкалы_Упорство',
                                                         'Диапазон_шкалы_Упорство',
                                                         lst_reindex_one_level_cols)

    svod_count_one_level_rig_df = calc_count_level_sub(base_df, lst_svod_cols,
                                                         'Значение_шкалы_Оптимизм',
                                                         'Диапазон_шкалы_Оптимизм',
                                                         lst_reindex_one_level_cols)
    svod_count_one_level_vz_df = calc_count_level_sub(base_df, lst_svod_cols,
                                                         'Значение_шкалы_Взаимосвязь',
                                                         'Диапазон_шкалы_Взаимосвязь',
                                                         lst_reindex_one_level_cols)
    svod_count_one_level_hap_df = calc_count_level_sub(base_df, lst_svod_cols,
                                                         'Значение_шкалы_Счастье',
                                                         'Диапазон_шкалы_Счастье',
                                                         lst_reindex_one_level_cols)

    # Считаем среднее по шкалам
    svod_mean_df = pd.pivot_table(base_df,
                                  index=lst_svod_cols,
                                  values=['Значение_ИП',
                                          'Значение_шкалы_Вовлеченность',
                                          'Значение_шкалы_Упорство',
                                          'Значение_шкалы_Оптимизм',
                                          'Значение_шкалы_Взаимосвязь',
                                          'Значение_шкалы_Счастье',
                                          ],
                                  aggfunc=round_mean)
    svod_mean_df.reset_index(inplace=True)
    # упорядочиваем колонки
    new_order_cols = lst_svod_cols.copy()
    new_order_cols.extend((['Значение_ИП', 'Значение_шкалы_Вовлеченность',
                            'Значение_шкалы_Упорство', 'Значение_шкалы_Оптимизм',
                            'Значение_шкалы_Взаимосвязь', 'Значение_шкалы_Счастье',
                            ]))
    svod_mean_df = svod_mean_df.reindex(columns=new_order_cols)

    dct_rename_cols_mean = {'Значение_ИП': 'Ср. Интегральный показатель',
                            'Значение_шкалы_Вовлеченность': 'Ср. Вовлеченность',
                            'Значение_шкалы_Упорство': 'Ср. Упорство',
                            'Значение_шкалы_Оптимизм': 'Ср. Оптимизм',
                            'Значение_шкалы_Взаимосвязь': 'Ср. Взаимосвязь',
                            'Значение_шкалы_Счастье': 'Ср. Счастье',
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
                    f'Свод ИП {out_name}': svod_count_one_level_anxiety_df,
                    f'Свод В {out_name}': svod_count_one_level_frust_df,
                    f'Свод У {out_name}': svod_count_one_level_agres_df,
                    f'Свод О {out_name}': svod_count_one_level_rig_df,
                    f'Свод ВС {out_name}': svod_count_one_level_vz_df,
                    f'Свод С {out_name}': svod_count_one_level_hap_df,
                    }
                   )

    if len(lst_svod_cols) == 1:
        return out_dct
    else:
        for idx, name_column in enumerate(lst_svod_cols):
            # Тревожность
            lst_reindex_column_level_cols =[lst_svod_cols[idx],'1.00-1.99','2.00-2.99','3.00-3.99','4.00-5.00',
                 'Итого']

            # Субшкалы
            svod_count_column_level_anxiety_df = calc_count_level_sub(base_df, lst_svod_cols[idx],
                                                                      'Значение_ИП',
                                                                      'Диапазон_ИП',
                                                                      lst_reindex_column_level_cols)

            svod_count_column_level_frust_df = calc_count_level_sub(base_df, lst_svod_cols[idx],
                                                                    'Значение_шкалы_Вовлеченность',
                                                                    'Диапазон_шкалы_Вовлеченность',
                                                                    lst_reindex_column_level_cols)

            svod_count_column_level_agres_df = calc_count_level_sub(base_df, lst_svod_cols[idx],
                                                                    'Значение_шкалы_Упорство',
                                                                    'Диапазон_шкалы_Упорство',
                                                                    lst_reindex_column_level_cols)

            svod_count_column_level_rig_df = calc_count_level_sub(base_df, lst_svod_cols[idx],
                                                                  'Значение_шкалы_Оптимизм',
                                                                  'Диапазон_шкалы_Оптимизм',
                                                                  lst_reindex_column_level_cols)
            svod_count_column_level_vz_df = calc_count_level_sub(base_df, lst_svod_cols[idx],
                                                                 'Значение_шкалы_Взаимосвязь',
                                                                 'Диапазон_шкалы_Взаимосвязь',
                                                                 lst_reindex_column_level_cols)
            svod_count_column_level_hap_df = calc_count_level_sub(base_df, lst_svod_cols[idx],
                                                                  'Значение_шкалы_Счастье',
                                                                  'Диапазон_шкалы_Счастье',
                                                                  lst_reindex_column_level_cols)

            # Считаем среднее по шкалам
            svod_mean_df = pd.pivot_table(base_df,
                                          index=[lst_svod_cols[idx]],
                                          values=['Значение_ИП',
                                                  'Значение_шкалы_Вовлеченность',
                                                  'Значение_шкалы_Упорство',
                                                  'Значение_шкалы_Оптимизм',
                                                  'Значение_шкалы_Взаимосвязь',
                                                  'Значение_шкалы_Счастье',
                                                  ],
                                          aggfunc=round_mean)
            svod_mean_df.reset_index(inplace=True)
            # упорядочиваем колонки
            new_order_cols = [lst_svod_cols[idx]].copy()
            new_order_cols.extend((['Значение_ИП', 'Значение_шкалы_Вовлеченность',
                                    'Значение_шкалы_Упорство', 'Значение_шкалы_Оптимизм',
                                    'Значение_шкалы_Взаимосвязь', 'Значение_шкалы_Счастье',
                                    ]))
            svod_mean_df = svod_mean_df.reindex(columns=new_order_cols)

            dct_rename_cols_mean = {'Значение_ИП': 'Ср. Интегральный показатель',
                                    'Значение_шкалы_Вовлеченность': 'Ср. Вовлеченность',
                                    'Значение_шкалы_Упорство': 'Ср. Упорство',
                                    'Значение_шкалы_Оптимизм': 'Ср. Оптимизм',
                                    'Значение_шкалы_Взаимосвязь': 'Ср. Взаимосвязь',
                                    'Значение_шкалы_Счастье': 'Ср. Счастье',
                                    }
            svod_mean_df.rename(columns=dct_rename_cols_mean, inplace=True)

            name_column = lst_svod_cols[idx]
            name_column = re.sub(r'[\[\]\'+()<> :"?*|\\/]', '_', name_column)
            name_column = name_column[:15]



            out_dct.update({f'Ср {name_column}': svod_mean_df,
                            f'Свод ИП {name_column}': svod_count_column_level_anxiety_df,
                            f'Свод В {name_column}': svod_count_column_level_frust_df,
                            f'Свод У {name_column}': svod_count_column_level_agres_df,
                            f'Свод О {name_column}': svod_count_column_level_rig_df,
                            f'Свод ВС {name_column}': svod_count_column_level_vz_df,
                            f'Свод С {name_column}': svod_count_column_level_hap_df,
                            }
                           )
        return out_dct






def processing_volkovs_obp(result_df: pd.DataFrame, answers_df: pd.DataFrame, lst_svod_cols:list):
    """
    Функция для обработки
    :param result_df: часть датафрейма с описательными колонками
    :param answers_df: часть датафрейма с ответами
    :param lst_svod_cols:  список с колонками по которым нужно делать свод
    """
    try:
        out_answer_df = result_df.copy()  # делаем копию для последующего соединения с сырыми ответами
        if len(answers_df.columns) != 20:  # проверяем количество колонок с вопросами
            raise BadCountColumnsOBPVV

        # очищаем названия колонок от возможных сочетаний .1 которые добавляет пандас при одинаковых колонках
        clean_df_lst = []
        for name_column in answers_df.columns:
            clean_name = re.sub(r'.\d+$', '', name_column)
            clean_df_lst.append(clean_name)

        answers_df.columns = clean_df_lst

        lst_check_cols = ['Когда со мной происходит что-то хорошее, мне есть с кем поделиться хорошими новостями',
                          'Я довожу до конца то, что начал',
                          'Я с оптимизмом смотрю в будущее',
                          'Я счастлив',
                          'Когда я чем-то занят, я так сильно увлекаюсь, что теряю счёт времени',
                          'Мне часто бывает весело',
                          'Я полностью погружаюсь в то, что делаю',
                          'Я люблю жизнь',
                          'Я делаю мои домашние задания до конца',
                          'Когда у меня проблемы, мне есть, к кому обратиться',

                          'Я так погружаюсь в деятельность, что забываю обо всем остальном',
                          'Когда я учусь чем-то новому, я забываю, сколько прошло времени',
                          'В смутные времена я надеюсь на хорошее',
                          'В моей жизни есть люди, которые искренне беспокоятся обо мне',
                          'Я думаю, что со мной произойдёт что-нибудь хорошее',
                          'У меня есть друзья, которые мне правда очень дороги',
                          'Если я планирую что-нибудь сделать, я буду придерживаться этого плана',
                          'Я верю, что всё образуется, как бы сложно ни было',
                          'Я трудолюбивый человек',
                          'Я веселый человек'
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
            raise BadOrderOBPVV

        # словарь для замены слов на числа
        dct_replace_value = {'совсем не похоже': 1,
                             'скорее не похоже': 2,
                             'нечто среднее, нельзя сказать, что похоже или не похоже': 3,
                             'скорее похоже': 4,
                             'очень похоже': 5,
    }

        valid_values = [1, 2 , 3, 4,5]
        answers_df.replace(dct_replace_value, inplace=True)  # заменяем слова на цифры для подсчетов
        # Проверяем, есть ли значения, отличающиеся от указанных в списке
        lst_error_answers = []  # список для хранения строк где найдены неправильные ответы

        for i in range(20):
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
            raise BadValueOBPVV

        base_df = pd.DataFrame()

        # Интегральный показатель
        base_df['Значение_ИП'] = answers_df.apply(calc_value_ip, axis=1)
        base_df['Диапазон_ИП'] = base_df['Значение_ИП'].apply(calc_level)
        # Вовлеченность
        base_df['Значение_шкалы_Вовлеченность'] = answers_df.apply(calc_sub_value_engagement, axis=1)
        base_df['Диапазон_шкалы_Вовлеченность'] = base_df['Значение_шкалы_Вовлеченность'].apply(calc_level)

        # Упорство
        base_df['Значение_шкалы_Упорство'] = answers_df.apply(calc_sub_value_perseverance , axis=1)
        base_df['Диапазон_шкалы_Упорство'] = base_df['Значение_шкалы_Упорство'].apply(calc_level)

        # Оптимизм
        base_df['Значение_шкалы_Оптимизм'] = answers_df.apply(calc_sub_value_optimism , axis=1)
        base_df['Диапазон_шкалы_Оптимизм'] = base_df['Значение_шкалы_Оптимизм'].apply(calc_level)

        # Взаимосвязь
        base_df['Значение_шкалы_Взаимосвязь'] = answers_df.apply(calc_sub_value_connectedness , axis=1)
        base_df['Диапазон_шкалы_Взаимосвязь'] = base_df['Значение_шкалы_Взаимосвязь'].apply(calc_level)

        # Счастье
        base_df['Значение_шкалы_Счастье'] = answers_df.apply(calc_sub_value_happiness, axis=1)
        base_df['Диапазон_шкалы_Счастье'] = base_df['Значение_шкалы_Счастье'].apply(calc_level)

        # Создаем датафрейм для создания части в общий датафрейм
        part_df = pd.DataFrame()

        part_df['ОБПВВ_ИП_Значение'] = base_df['Значение_ИП']
        part_df['ОБПВВ_ИП_Диапазон'] = base_df['Диапазон_ИП']

        part_df['ОБПВВ_Вовлеченность_Значение'] = base_df['Значение_шкалы_Вовлеченность']
        part_df['ОБПВВ_Вовлеченность_Диапазон'] = base_df['Диапазон_шкалы_Вовлеченность']

        part_df['ОБПВВ_Упорство_Значение'] = base_df['Значение_шкалы_Упорство']
        part_df['ОБПВВ_Упорство_Диапазон'] = base_df['Диапазон_шкалы_Упорство']

        part_df['ОБПВВ_Оптимизм_Значение'] = base_df['Значение_шкалы_Оптимизм']
        part_df['ОБПВВ_Оптимизм_Диапазон'] = base_df['Диапазон_шкалы_Оптимизм']

        part_df['ОБПВВ_Взаимосвязь_Значение'] = base_df['Значение_шкалы_Взаимосвязь']
        part_df['ОБПВВ_Взаимосвязь_Диапазон'] = base_df['Диапазон_шкалы_Взаимосвязь']

        part_df['ОБПВВ_Счастье_Значение'] = base_df['Значение_шкалы_Счастье']
        part_df['ОБПВВ_Счастье_Диапазон'] = base_df['Диапазон_шкалы_Счастье']

        out_answer_df = pd.concat([out_answer_df, answers_df], axis=1)  # Датафрейм для проверки

        # Соединяем анкетную часть с результатной
        base_df = pd.concat([result_df, base_df], axis=1)
        base_df.sort_values(by='Значение_ИП', ascending=True, inplace=True)  # сортируем

        # считаем среднее значение по шкалам
        avg_anxiety = round(base_df['Значение_ИП'].mean(), 2)
        avg_frust = round(base_df['Значение_шкалы_Вовлеченность'].mean(), 2)
        avg_agres = round(base_df['Значение_шкалы_Упорство'].mean(), 2)
        avg_rig = round(base_df['Значение_шкалы_Оптимизм'].mean(), 2)
        avg_vz = round(base_df['Значение_шкалы_Взаимосвязь'].mean(), 2)
        avg_hap = round(base_df['Значение_шкалы_Счастье'].mean(), 2)

        avg_dct = {'Среднее значение интегрального показателя': avg_anxiety,
                   'Среднее значение шкалы Вовлеченность': avg_frust,
                   'Среднее значение шкалы Упорство': avg_agres,
                   'Среднее значение шкалы Оптимизм': avg_rig,
                   'Среднее значение шкалы Взаимосвязь': avg_vz,
                   'Среднее значение шкалы Счастье': avg_hap,
                   }

        avg_df = pd.DataFrame.from_dict(avg_dct, orient='index')
        avg_df = avg_df.reset_index()
        avg_df.columns = ['Показатель', 'Среднее значение']

        # Делаем свод  по  шкалам
        dct_svod_sub = {'Значение_ИП': 'Диапазон_ИП',
                        'Значение_шкалы_Вовлеченность': 'Диапазон_шкалы_Вовлеченность',
                        'Значение_шкалы_Упорство': 'Диапазон_шкалы_Упорство',
                        'Значение_шкалы_Оптимизм': 'Диапазон_шкалы_Оптимизм',
                        'Значение_шкалы_Взаимосвязь': 'Диапазон_шкалы_Взаимосвязь',
                        'Значение_шкалы_Счастье': 'Диапазон_шкалы_Счастье',
                        }

        dct_rename_svod_sub = {'Значение_ИП': 'Интегральный показатель',
                               'Значение_шкалы_Вовлеченность': 'Вовлеченность',
                               'Значение_шкалы_Упорство': 'Упорство',
                               'Значение_шкалы_Оптимизм': 'Оптимизм',
                               'Значение_шкалы_Взаимосвязь': 'Взаимосвязь',
                               'Значение_шкалы_Счастье': 'Счастье',
                               }

        # Списки для шкал
        lst_level = ['1.00-1.99','2.00-2.99','3.00-3.99','4.00-5.00']

        base_svod_sub_df = create_union_svod(base_df, dct_svod_sub, dct_rename_svod_sub, lst_level)
        # формируем основной словарь
        out_dct = {'Списочный результат': base_df, 'Список для проверки': out_answer_df,
                   'Свод по шкалам': base_svod_sub_df,
                   'Среднее по шкалам': avg_df,
                   }

        dct_prefix = {'Диапазон_ИП': 'ИП',
                      'Диапазон_шкалы_Вовлеченность': 'В',
                      'Диапазон_шкалы_Упорство': 'У',
                      'Диапазон_шкалы_Оптимизм': 'О',
                      'Диапазон_шкалы_Взаимосвязь': 'ВС',
                      'Диапазон_шкалы_Счастье': 'С',
                      }

        out_dct = create_list_on_level(base_df, out_dct, lst_level, dct_prefix)

        """
            Сохраняем в зависимости от необходимости делать своды по определенным колонкам
            """
        if len(lst_svod_cols) == 0:
            return out_dct, part_df
        else:
            out_dct = create_result_obpvv(base_df, out_dct, lst_svod_cols)

            return out_dct, part_df

    except BadOrderOBPVV:
        messagebox.showerror('Лахеcис',
                             f'При обработке вопросов теста Опросник благополучия подростков EPOCH Волкова Волкова обнаружены неправильные вопросы. Проверьте названия колонок с вопросами:\n'
                             f'{error_order_message[:5000]}\n'
                             f'Используйте при создании Яндекс-формы написание вопросов из руководства пользователя программы Лахесис.')
    except BadValueOBPVV:
        messagebox.showerror('Лахеcис',
                             f'При обработке вопросов теста Опросник благополучия подростков EPOCH Волкова Волкова обнаружены неправильные варианты ответов. Проверьте ответы на указанных строках:\n'
                             f'{error_message[:5000]}\n'
                             f'Используйте при создании Яндекс-формы написание вариантов ответа из руководства пользователя программы Лахесис.')


    except BadCountColumnsOBPVV:
        messagebox.showerror('Лахеcис',
                             f'Проверьте количество колонок с ответами на тест Опросник благополучия подростков EPOCH Волкова Волкова\n'
                             f'Должно быть 20 колонок с ответами')













