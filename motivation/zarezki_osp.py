"""
Скрипт для обработки результатов Опросник Субъектная позиция Зарецкий, Зарецкий, Кулагина
"""

import pandas as pd
import re
from tkinter import messagebox
from lachesis_support_functions import round_mean_two,calc_count_scale,create_union_svod, create_list_on_level

class BadOrderOSPZ(Exception):
    """
    Исключение для обработки случая когда колонки не совпадают
    """
    pass


class BadValueOSPZ(Exception):
    """
    Исключение для неправильных значений в вариантах ответов
    """
    pass

class BadCountColumnsOSPZ(Exception):
    """
    Исключение для обработки случая если количество колонок не равно 12
    """
    pass


def calc_level(value):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """
    if 0<= value <= 4:
        return f'0-4'
    elif 5 <= value <= 8:
        return f'5-8'
    elif 9 <= value <= 12:
        return f'9-12'
    else:
        return f'13-16'




def calc_value_op(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [1,2,4,5]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_pr:
            value_forward += value
    return value_forward

def calc_value_np(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [7,9,11,12]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_pr:
            value_forward += value
    return value_forward

def calc_value_sp(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [3,6,8,10]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_pr:
            value_forward += value
    return value_forward


def create_result_osp_zar(base_df:pd.DataFrame, out_dct:dict, lst_svod_cols:list):
    """
    Функция для подсчета результата если указаны колонки по которым нужно провести свод
    :param df: датафрейм с результатами
    :param out_dct: словарь с уже подсчитанными базовыми данными
    :param lst_svod_cols: список сводных колонок
    :return: словарь
    """
    lst_level = ['0-4', '5-8', '9-12','13-16']

    lst_reindex_one_level_cols = lst_svod_cols.copy()
    lst_reindex_one_level_cols.extend(['0-4', '5-8', '9-12','13-16',
                                       'Итого'])  # Основная шкала

    # АД
    svod_count_one_level_op_df = calc_count_scale(base_df, lst_svod_cols,
                                                 'ОП_Значение',
                                                 'ОП_Диапазон',
                                                 lst_reindex_one_level_cols, lst_level)
    # АД
    svod_count_one_level_np_df = calc_count_scale(base_df, lst_svod_cols,
                                                 'НП_Значение',
                                                 'НП_Диапазон',
                                                 lst_reindex_one_level_cols, lst_level)
    # АД
    svod_count_one_level_sp_df = calc_count_scale(base_df, lst_svod_cols,
                                                 'СП_Значение',
                                                 'СП_Диапазон',
                                                 lst_reindex_one_level_cols, lst_level)

    # Считаем среднее по субшкалам
    svod_mean_one_df = pd.pivot_table(base_df,
                                      index=lst_svod_cols,
                                      values=['ОП_Значение',
                                              'НП_Значение',
                                              'СП_Значение',
                                              ],
                                      aggfunc=round_mean_two)
    svod_mean_one_df.reset_index(inplace=True)

    # упорядочиваем колонки
    new_order_cols = lst_svod_cols.copy()
    new_order_cols.extend((['ОП_Значение',
                            'НП_Значение',
                            'СП_Значение',
                            ]))
    svod_mean_one_df = svod_mean_one_df.reindex(columns=new_order_cols)

    dct_rename_cols_mean = {'ОП_Значение': 'Ср. Шкала Объектная позиция',
                            'НП_Значение': 'Ср. Шкала Негативная позиция',
                            'СП_Значение': 'Ср. Шкала Субъектная позиция',
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
                    f'ОП {out_name}': svod_count_one_level_op_df,
                    f'НП {out_name}': svod_count_one_level_np_df,
                    f'СП {out_name}': svod_count_one_level_sp_df,
                    })

    if len(lst_svod_cols) == 1:
        return out_dct
    else:
        for idx, name_column in enumerate(lst_svod_cols):
            lst_reindex_column_level_cols = [lst_svod_cols[idx], '0-4', '5-8', '9-12','13-16',
                                             'Итого']

            # АД
            svod_count_column_level_op_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                             'ОП_Значение',
                                                             'ОП_Диапазон',
                                                             lst_reindex_column_level_cols, lst_level)
            # АД
            svod_count_column_level_np_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                             'НП_Значение',
                                                             'НП_Диапазон',
                                                             lst_reindex_column_level_cols, lst_level)
            # АД
            svod_count_column_level_sp_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                             'СП_Значение',
                                                             'СП_Диапазон',
                                                             lst_reindex_column_level_cols, lst_level)

            # Считаем среднее по субшкалам
            svod_mean_column_df = pd.pivot_table(base_df,
                                                 index=[lst_svod_cols[idx]],
                                                 values=['ОП_Значение',
                                                         'НП_Значение',
                                                         'СП_Значение',
                                                         ],
                                                 aggfunc=round_mean_two)
            svod_mean_column_df.reset_index(inplace=True)

            # упорядочиваем колонки
            new_order_cols = [lst_svod_cols[idx]].copy()
            new_order_cols.extend((['ОП_Значение',
                                    'НП_Значение',
                                    'СП_Значение',
                                    ]))
            svod_mean_column_df = svod_mean_column_df.reindex(columns=new_order_cols)

            dct_rename_cols_mean = {'ОП_Значение': 'Ср. Шкала Объектная позиция',
                                    'НП_Значение': 'Ср. Шкала Негативная позиция',
                                    'СП_Значение': 'Ср. Шкала Субъектная позиция',
                                    }
            svod_mean_column_df.rename(columns=dct_rename_cols_mean, inplace=True)
            # Готовим наименование
            name_column = lst_svod_cols[idx]
            name_column = re.sub(r'[\[\]\'+()<> :"?*|\\/]', '_', name_column)
            name_column = name_column[:15]

            out_dct.update({f'Ср {name_column}': svod_mean_column_df,
                            f'ОП {name_column}': svod_count_column_level_op_df,
                            f'НП {name_column}': svod_count_column_level_np_df,
                            f'СП {name_column}': svod_count_column_level_sp_df,
                            })
        return out_dct








def processing_osp_zar(base_df: pd.DataFrame, answers_df: pd.DataFrame, lst_svod_cols:list):
    """
    Функция для обработки
    :param base_df: часть датафрейма с описательными колонками
    :param answers_df: часть датафрейма с ответами
    :param lst_svod_cols:  список с колонками по которым нужно делать свод
    """
    try:
        out_answer_df = base_df.copy()  # делаем копию для последующего соединения с сырыми ответами
        if len(answers_df.columns) != 12:  # проверяем количество колонок с вопросами
            raise BadCountColumnsOSPZ

        # очищаем названия колонок от возможных сочетаний .1 которые добавляет пандас при одинаковых колонках
        clean_df_lst = []
        for name_column in answers_df.columns:
            clean_name = re.sub(r'.\d+$', '', name_column)
            clean_df_lst.append(clean_name)

        answers_df.columns = clean_df_lst

        lst_check_cols = ['Родители и учителя говорят, что очень важно учиться, поэтому я учусь и хожу в школу',
                          'Я решаю примеры только так, как говорит учитель',
                          'Если на уроке я что-то не понял, я обязательно постараюсь разобраться в этом',
                          'Я обязан ходить в школу и выполнять все требования учителей',
                          'Когда я выполняю задание, самое важное, чтобы меня похвалили',
                          'Мне часто хочется найти свой способ решения задачи',

                          'Обычно я не делаю домашнее задание',
                          'Мне нравится справляться с трудными задачами',
                          'Я иногда пропускаю занятия',
                          'Когда мы проходим новую тему, мне хочется разобраться в непонятных вопросах',
                          'Можно сказать, что сорванный урок – это развлечение',
                          'Я не стал бы ходить на дополнительные занятия по трудному для меня предмету',
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
            raise BadOrderOSPZ

        # словарь для замены слов на числа
        dct_replace_value = {'нет': 0,
                             'скорее нет, чем да': 1,
                             'скорее да, чем нет': 3,
                             'да': 4,
                             }
        valid_values = [0, 1, 3, 4]
        answers_df.replace(dct_replace_value, inplace=True)  # заменяем слова на цифры для подсчетов
        # Проверяем, есть ли значения, отличающиеся от указанных в списке
        lst_error_answers = []  # список для хранения строк где найдены неправильные ответы

        for i in range(12):
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
            raise BadValueOSPZ

        base_df['ОП_Значение'] = answers_df.apply(calc_value_op, axis=1)
        base_df['ОП_Диапазон'] = base_df['ОП_Значение'].apply(calc_level)

        base_df['НП_Значение'] = answers_df.apply(calc_value_np, axis=1)
        base_df['НП_Диапазон'] = base_df['НП_Значение'].apply(calc_level)

        base_df['СП_Значение'] = answers_df.apply(calc_value_sp, axis=1)
        base_df['СП_Диапазон'] = base_df['СП_Значение'].apply(calc_level)

        # Создаем датафрейм для создания части в общий датафрейм
        part_df = pd.DataFrame()

        # Основные шкалы
        part_df['СПЗЗК_ОП_Значение'] = base_df['ОП_Значение']
        part_df['СПЗЗК_ОП_Диапазон'] = base_df['ОП_Диапазон']

        part_df['СПЗЗК_НП_Значение'] = base_df['НП_Значение']
        part_df['СПЗЗК_НП_Диапазон'] = base_df['НП_Диапазон']

        part_df['СПЗЗК_СП_Значение'] = base_df['СП_Значение']
        part_df['СПЗЗК_СП_Диапазон'] = base_df['СП_Диапазон']

        out_answer_df = pd.concat([out_answer_df, answers_df], axis=1)  # Датафрейм для проверки

        base_df.sort_values(by='НП_Значение', ascending=False, inplace=True)  # сортируем

        # Делаем свод  по  шкалам
        dct_svod_sub = {'ОП_Значение': 'ОП_Диапазон',
                        'НП_Значение': 'НП_Диапазон',
                        'СП_Значение': 'СП_Диапазон',
                        }

        dct_rename_svod_sub = {'ОП_Значение': 'Шкала Объектная позиция',
                               'НП_Значение': 'Шкала Негативная позиция',
                               'СП_Значение': 'Шкала Субъектная позиция',
                               }

        lst_sub = ['0-4', '5-8', '9-12','13-16']

        base_svod_sub_df = create_union_svod(base_df, dct_svod_sub, dct_rename_svod_sub, lst_sub)

        avg_op = round(base_df['ОП_Значение'].mean(), 2)
        avg_np = round(base_df['НП_Значение'].mean(), 2)
        avg_sp = round(base_df['СП_Значение'].mean(), 2)

        avg_dct = {'Среднее значение шкалы Объектная позиция': avg_op,
                   'Среднее значение шкалы Негативная позиция': avg_np,
                   'Среднее значение шкалы Субъектная позиция': avg_sp,
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
            'ОП_Диапазон': 'ОП',
            'НП_Диапазон': 'НП',
            'СП_Диапазон': 'СП',
        }

        out_dct = create_list_on_level(base_df, out_dct, lst_sub, dct_prefix)

        """
                        Сохраняем в зависимости от необходимости делать своды по определенным колонкам
                        """
        if len(lst_svod_cols) == 0:
            return out_dct, part_df

        else:
            out_dct = create_result_osp_zar(base_df, out_dct, lst_svod_cols)
            return out_dct, part_df



    except BadOrderOSPZ:
        messagebox.showerror('Лахеcис',
                             f'При обработке вопросов теста Опросник Субъектная позиция Зарецкий, Зарецкий, Кулагина обнаружены неправильные вопросы. Проверьте названия колонок с вопросами:\n'
                             f'{error_order_message[:5000]}\n'
                             f'Используйте при создании Яндекс-формы написание вопросов из руководства пользователя программы Лахесис.')
    except BadValueOSPZ:
        messagebox.showerror('Лахеcис',
                             f'При обработке вопросов теста Опросник Субъектная позиция Зарецкий, Зарецкий, Кулагина обнаружены неправильные варианты ответов. Проверьте ответы на указанных строках:\n'
                             f'{error_message[:5000]}\n'
                             f'Используйте при создании Яндекс-формы написание вариантов ответа из руководства пользователя программы Лахесис.')


    except BadCountColumnsOSPZ:
        messagebox.showerror('Лахеcис',
                             f'Проверьте количество колонок с ответами на тест Опросник Субъектная позиция Зарецкий, Зарецкий, Кулагина\n'
                             f'Должно быть 12 колонок с ответами')





