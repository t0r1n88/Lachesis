"""
Скрипт для обработки результатов Опросник Буллинг Олвеус
"""

import pandas as pd
import re
from tkinter import messagebox
from lachesis_support_functions import round_mean_two,calc_count_scale,create_union_svod, create_list_on_level

class BadOrderOBO(Exception):
    """
    Исключение для обработки случая когда колонки не совпадают
    """
    pass


class BadValueOBO(Exception):
    """
    Исключение для неправильных значений в вариантах ответов
    """
    pass

class BadCountColumnsOBO(Exception):
    """
    Исключение для обработки случая если количество колонок не равно 13
    """
    pass

def calc_value_ab(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [1,3,5,6,2,4]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_pr:
            value_forward += value



    return value_forward


def calc_value_pb(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [1,3,5,6]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_pr:
            value_forward += value



    return value_forward

def calc_value_kb(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [2,4]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_pr:
            value_forward += value



    return value_forward

def calc_value_v(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [7,10,11,13,8,9,12]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_pr:
            value_forward += value



    return value_forward


def calc_value_pv(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [7,10,11,13]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_pr:
            value_forward += value



    return value_forward


def calc_value_kv(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [8,9,12]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_pr:
            value_forward += value



    return value_forward



def calc_level(value,quantity):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """

    result =round((value / quantity),1)

    if 0<= result <= 1:
        return f'слабо выражен'
    elif 1 < result < 3:
        return f'умеренно выражен'
    else:
        return f'ярко выражен'


def create_result_ob_olveus(base_df:pd.DataFrame, out_dct:dict, lst_svod_cols:list):
    """
    Функция для подсчета результата если указаны колонки по которым нужно провести свод
    :param df: датафрейм с результатами
    :param out_dct: словарь с уже подсчитанными базовыми данными
    :param lst_svod_cols: список сводных колонок
    :return: словарь
    """
    lst_level = ['слабо выражен', 'умеренно выражен', 'ярко выражен']

    lst_reindex_one_level_cols = lst_svod_cols.copy()
    lst_reindex_one_level_cols.extend(['слабо выражен', 'умеренно выражен', 'ярко выражен',
                                       'Итого'])  # Основная шкала

    # АД
    svod_count_one_level_ab_df = calc_count_scale(base_df, lst_svod_cols,
                                                 'АБ_Значение',
                                                 'АБ_Уровень',
                                                 lst_reindex_one_level_cols, lst_level)
    # АВА
    svod_count_one_level_pb_df = calc_count_scale(base_df, lst_svod_cols,
                                                 'ПБ_Значение',
                                                 'ПБ_Уровень',
                                                 lst_reindex_one_level_cols, lst_level)

    svod_count_one_level_kb_df = calc_count_scale(base_df, lst_svod_cols,
                                                 'КБ_Значение',
                                                 'КБ_Уровень',
                                                 lst_reindex_one_level_cols, lst_level)


    # АД
    svod_count_one_level_v_df = calc_count_scale(base_df, lst_svod_cols,
                                                 'В_Значение',
                                                 'В_Уровень',
                                                 lst_reindex_one_level_cols, lst_level)
    # АВА
    svod_count_one_level_pv_df = calc_count_scale(base_df, lst_svod_cols,
                                                 'ПВ_Значение',
                                                 'ПВ_Уровень',
                                                 lst_reindex_one_level_cols, lst_level)

    svod_count_one_level_kv_df = calc_count_scale(base_df, lst_svod_cols,
                                                 'КВ_Значение',
                                                 'КВ_Уровень',
                                                 lst_reindex_one_level_cols, lst_level)

    # Считаем среднее по субшкалам
    svod_mean_one_df = pd.pivot_table(base_df,
                                      index=lst_svod_cols,
                                      values=['АБ_Значение',
                                              'ПБ_Значение',
                                              'КБ_Значение',

                                              'В_Значение',
                                              'ПВ_Значение',
                                              'КВ_Значение',
                                              ],
                                      aggfunc=round_mean_two)
    svod_mean_one_df.reset_index(inplace=True)

    # упорядочиваем колонки
    new_order_cols = lst_svod_cols.copy()
    new_order_cols.extend((['АБ_Значение',
                            'ПБ_Значение',
                            'КБ_Значение',

                            'В_Значение',
                            'ПВ_Значение',
                            'КВ_Значение',
                            ]))
    svod_mean_one_df = svod_mean_one_df.reindex(columns=new_order_cols)

    dct_rename_cols_mean = {'АБ_Значение': 'Ср. Активный буллинг',
                            'ПБ_Значение': 'Ср. Прямой буллинг',
                            'КБ_Значение': 'Ср. Косвенный буллинг',

                            'В_Значение': 'Ср. Виктимизация',
                            'ПВ_Значение': 'Ср. Прямая виктимизация',
                            'КВ_Значение': 'Ср. Косвенная виктимизация',
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
                    f'АБ {out_name}': svod_count_one_level_ab_df,
                    f'ПБ {out_name}': svod_count_one_level_pb_df,
                    f'КБ {out_name}': svod_count_one_level_kb_df,

                    f'В {out_name}': svod_count_one_level_v_df,
                    f'ПВ {out_name}': svod_count_one_level_pv_df,
                    f'КВ {out_name}': svod_count_one_level_kv_df,
                    })


    if len(lst_svod_cols) == 1:
        return out_dct
    else:

        for idx, name_column in enumerate(lst_svod_cols):
            lst_reindex_column_level_cols = [lst_svod_cols[idx], 'слабо выражен', 'умеренно выражен', 'ярко выражен',
                                               'Итого']

            svod_count_column_level_ab_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                            'АБ_Значение',
                                                            'АБ_Уровень',
                                                            lst_reindex_column_level_cols, lst_level)
            # АВА
            svod_count_column_level_pb_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                            'ПБ_Значение',
                                                            'ПБ_Уровень',
                                                            lst_reindex_column_level_cols, lst_level)
            svod_count_column_level_kb_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                             'КБ_Значение',
                                                             'КБ_Уровень',
                                                             lst_reindex_column_level_cols, lst_level)


            svod_count_column_level_v_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                            'В_Значение',
                                                            'В_Уровень',
                                                            lst_reindex_column_level_cols, lst_level)
            # АВА
            svod_count_column_level_pv_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                            'ПВ_Значение',
                                                            'ПВ_Уровень',
                                                            lst_reindex_column_level_cols, lst_level)
            svod_count_column_level_kv_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                             'КВ_Значение',
                                                             'КВ_Уровень',
                                                             lst_reindex_column_level_cols, lst_level)

            # Считаем среднее по субшкалам
            svod_mean_column_df = pd.pivot_table(base_df,
                                              index=[lst_svod_cols[idx]],
                                              values=['АБ_Значение',
                                                      'ПБ_Значение',
                                                      'КБ_Значение',

                                                      'В_Значение',
                                                      'ПВ_Значение',
                                                      'КВ_Значение',
                                                      ],
                                              aggfunc=round_mean_two)
            svod_mean_column_df.reset_index(inplace=True)

            # упорядочиваем колонки
            new_order_cols = [lst_svod_cols[idx]].copy()
            new_order_cols.extend((['АБ_Значение',
                                    'ПБ_Значение',
                                    'КБ_Значение',

                                    'В_Значение',
                                    'ПВ_Значение',
                                    'КВ_Значение',
                                    ]))
            svod_mean_column_df = svod_mean_column_df.reindex(columns=new_order_cols)

            dct_rename_cols_mean = {'АБ_Значение': 'Ср. Активный буллинг',
                                    'ПБ_Значение': 'Ср. Прямой буллинг',
                                    'КБ_Значение': 'Ср. Косвенный буллинг',

                                    'В_Значение': 'Ср. Виктимизация',
                                    'ПВ_Значение': 'Ср. Прямая виктимизация',
                                    'КВ_Значение': 'Ср. Косвенная виктимизация',
                                    }
            svod_mean_column_df.rename(columns=dct_rename_cols_mean, inplace=True)

            # Готовим наименование
            name_column = lst_svod_cols[idx]
            name_column = re.sub(r'[\[\]\'+()<> :"?*|\\/]', '_', name_column)
            name_column = name_column[:15]
            out_dct.update({f'Ср {name_column}': svod_mean_column_df,
                            f'АБ {name_column}': svod_count_column_level_ab_df,
                            f'ПБ {name_column}': svod_count_column_level_pb_df,
                            f'КБ {name_column}': svod_count_column_level_kb_df,

                            f'В {name_column}': svod_count_column_level_v_df,
                            f'ПВ {name_column}': svod_count_column_level_pv_df,
                            f'КВ {name_column}': svod_count_column_level_kv_df,
                            })
        return out_dct














def processing_ob_olveus(base_df: pd.DataFrame, answers_df: pd.DataFrame, lst_svod_cols:list):
    """
    Функция для обработки
    :param base_df: часть датафрейма с описательными колонками
    :param answers_df: часть датафрейма с ответами
    :param lst_svod_cols:  список с колонками по которым нужно делать свод
    """
    try:
        out_answer_df = base_df.copy()  # делаем копию для последующего соединения с сырыми ответами
        if len(answers_df.columns) != 13:  # проверяем количество колонок с вопросами
            raise BadCountColumnsOBO

        # очищаем названия колонок от возможных сочетаний .1 которые добавляет пандас при одинаковых колонках
        clean_df_lst = []
        for name_column in answers_df.columns:
            clean_name = re.sub(r'.\d+$', '', name_column)
            clean_df_lst.append(clean_name)

        answers_df.columns = clean_df_lst
        lst_check_cols = ['я кого-то обозвал',
                          'я с кем-то специально не разговаривал',
                          'я нанес кому-то физический вред, например, толкнул или ударил',
                          'я распространял о ком-то сплетни',
                          'я угрожал',
                          'я украл или испортил чьи-то вещи',
                          'меня обзывали',
                          'обо мне распространяли сплетни',
                          'никто не хочет сидеть со мной или проводить свободное время',
                          'у меня украли вещи',
                          'мне нанесли физический вред (ударили, толкнули)',
                          'никто не говорит со мной',
                          'мне угрожали'
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
            raise BadOrderOBO

        # словарь для замены слов на числа
        dct_replace_value = {'никогда не было': 0,
                             'было раз или два': 1,
                             'бывает иногда': 2,
                             'бывает раз в неделю': 3,
                             'бывает несколько раз в неделю': 4,
                             }
        valid_values = [0, 1, 2, 3, 4]
        answers_df.replace(dct_replace_value, inplace=True)  # заменяем слова на цифры для подсчетов
        # Проверяем, есть ли значения, отличающиеся от указанных в списке
        lst_error_answers = []  # список для хранения строк где найдены неправильные ответы

        for i in range(13):
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
            raise BadValueOBO

        base_df['АБ_Значение'] = answers_df.apply(calc_value_ab,axis=1)
        base_df['АБ_Уровень'] = base_df['АБ_Значение'].apply(lambda x:calc_level(x,6))

        base_df['ПБ_Значение'] = answers_df.apply(calc_value_pb,axis=1)
        base_df['ПБ_Уровень'] = base_df['ПБ_Значение'].apply(lambda x:calc_level(x,4))

        base_df['КБ_Значение'] = answers_df.apply(calc_value_kb,axis=1)
        base_df['КБ_Уровень'] = base_df['КБ_Значение'].apply(lambda x:calc_level(x,2))

        base_df['В_Значение'] = answers_df.apply(calc_value_v,axis=1)
        base_df['В_Уровень'] = base_df['В_Значение'].apply(lambda x:calc_level(x,7))

        base_df['ПВ_Значение'] = answers_df.apply(calc_value_pv,axis=1)
        base_df['ПВ_Уровень'] = base_df['ПВ_Значение'].apply(lambda x:calc_level(x,4))

        base_df['КВ_Значение'] = answers_df.apply(calc_value_kv,axis=1)
        base_df['КВ_Уровень'] = base_df['КВ_Значение'].apply(lambda x:calc_level(x,3))

        # Создаем датафрейм для создания части в общий датафрейм
        part_df = pd.DataFrame()

        # Основные шкалы
        part_df['ОБО_АБ_Значение'] = base_df['АБ_Значение']
        part_df['ОБО_АБ_Уровень'] = base_df['АБ_Уровень']

        part_df['ОБО_ПБ_Значение'] = base_df['ПБ_Значение']
        part_df['ОБО_ПБ_Уровень'] = base_df['ПБ_Уровень']

        part_df['ОБО_КБ_Значение'] = base_df['КБ_Значение']
        part_df['ОБО_КБ_Уровень'] = base_df['КБ_Уровень']

        part_df['ОБО_В_Значение'] = base_df['В_Значение']
        part_df['ОБО_В_Уровень'] = base_df['В_Уровень']

        part_df['ОБО_ПВ_Значение'] = base_df['ПВ_Значение']
        part_df['ОБО_ПВ_Уровень'] = base_df['ПВ_Уровень']

        part_df['ОБО_КВ_Значение'] = base_df['КВ_Значение']
        part_df['ОБО_КВ_Уровень'] = base_df['КВ_Уровень']

        out_answer_df = pd.concat([out_answer_df, answers_df], axis=1)  # Датафрейм для проверки

        base_df.sort_values(by='В_Значение', ascending=False, inplace=True)  # сортируем

        # Делаем свод  по  шкалам
        dct_svod_l = {'АБ_Значение': 'АБ_Уровень',
                      'ПБ_Значение': 'ПБ_Уровень',
                      'КБ_Значение': 'КБ_Уровень',

                      'В_Значение': 'В_Уровень',
                      'ПВ_Значение': 'ПВ_Уровень',
                      'КВ_Значение': 'КВ_Уровень',
                      }

        dct_rename_svod_l = {'АБ_Значение': 'Активный буллинг',
                             'ПБ_Значение': 'Прямой буллинг',
                             'КБ_Значение': 'Косвенный буллинг',

                             'В_Значение': 'Виктимизация',
                             'ПВ_Значение': 'Прямая виктимизация',
                             'КВ_Значение': 'Косвенная виктимизация',

                             }

        lst_sub = ['слабо выражен', 'умеренно выражен', 'ярко выражен']

        base_svod_l_df = create_union_svod(base_df, dct_svod_l, dct_rename_svod_l, lst_sub)

        avg_ab = round(base_df['АБ_Значение'].mean(), 2)
        avg_pb = round(base_df['ПБ_Значение'].mean(), 2)
        avg_kb = round(base_df['КБ_Значение'].mean(), 2)
        avg_v = round(base_df['В_Значение'].mean(), 2)
        avg_pv = round(base_df['ПВ_Значение'].mean(), 2)
        avg_kv = round(base_df['КВ_Значение'].mean(), 2)

        avg_dct = {'Среднее значение шкалы Активный буллинг': avg_ab,
                   'Среднее значение шкалы Прямой буллинг': avg_pb,
                   'Среднее значение шкалы Косвенный буллинг': avg_kb,
                   'Среднее значение шкалы Виктимизация': avg_v,
                   'Среднее значение шкалы Прямая виктимизация': avg_pv,
                   'Среднее значение шкалы Косвенная виктимизация': avg_kv,
                   }

        avg_df = pd.DataFrame.from_dict(avg_dct, orient='index')
        avg_df = avg_df.reset_index()
        avg_df.columns = ['Показатель', 'Среднее значение']
        # формируем основной словарь
        out_dct = {'Списочный результат': base_df,
                   'Список для проверки': out_answer_df,
                   'Свод Шкалы': base_svod_l_df,
                   'Среднее': avg_df,
                   }

        dct_prefix = {
            'АБ_Уровень': 'АБ',
            'ПБ_Уровень': 'ПБ',
            'КБ_Уровень': 'КБ',
            'В_Уровень': 'В',
            'ПВ_Уровень': 'ПВ',
            'КВ_Уровень': 'КВ',
        }

        out_dct = create_list_on_level(base_df, out_dct, lst_sub, dct_prefix)

        """
                        Сохраняем в зависимости от необходимости делать своды по определенным колонкам
                        """
        if len(lst_svod_cols) == 0:
            return out_dct, part_df

        else:
            out_dct = create_result_ob_olveus(base_df, out_dct, lst_svod_cols)
            return out_dct, part_df

    except BadOrderOBO:
        messagebox.showerror('Лахеcис',
                             f'При обработке вопросов теста Опросник Буллинг Олвеус обнаружены неправильные вопросы. Проверьте названия колонок с вопросами:\n'
                             f'{error_order_message[:5000]}\n'
                             f'Используйте при создании Яндекс-формы написание вопросов из руководства пользователя программы Лахесис.')
    except BadValueOBO:
        messagebox.showerror('Лахеcис',
                             f'При обработке вопросов теста Опросник Буллинг Олвеус обнаружены неправильные варианты ответов. Проверьте ответы на указанных строках:\n'
                             f'{error_message[:5000]}\n'
                             f'Используйте при создании Яндекс-формы написание вариантов ответа из руководства пользователя программы Лахесис.')


    except BadCountColumnsOBO:
        messagebox.showerror('Лахеcис',
                             f'Проверьте количество колонок с ответами на тест Опросник Буллинг Олвеус\n'
                             f'Должно быть 13 колонок с ответами')









