"""
Скрипт для обработки результатов Шкала организационного цинизма, OCS Павлова, Дзюбенко, Нартова-Бочавер
"""

import pandas as pd
import re
from tkinter import messagebox
from lachesis_support_functions import round_mean_two,calc_count_scale,create_union_svod, create_list_on_level

class BadOrderOCSPDN(Exception):
    """
    Исключение для обработки случая когда колонки не совпадают
    """
    pass


class BadValueOCSPDN(Exception):
    """
    Исключение для неправильных значений в вариантах ответов
    """
    pass

class BadCountColumnsOCSPDN(Exception):
    """
    Исключение для обработки случая если количество колонок не равно 13
    """
    pass

def calc_value_ka(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [1,2,3,4,5]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_pr:
            value_forward += value


    return round(value_forward/5,2)

def calc_level(value):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """

    if 1<= value <2:
        return f'1-1,99'
    elif 2 <= value <3:
        return f'2-2,99'
    elif 3 <= value <4:
        return f'3-3,99'
    else:
        return f'4-5'






def calc_value_aa(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [6,7,8]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_pr:
            value_forward += value


    return round(value_forward/3,2)



def calc_value_pa(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [9,10,11,12,13]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_pr:
            value_forward += value


    return round(value_forward/5,2)

def create_result_ocs_pavlova(base_df:pd.DataFrame, out_dct:dict, lst_svod_cols:list):
    """
    Функция для подсчета результата если указаны колонки по которым нужно провести свод
    :param df: датафрейм с результатами
    :param out_dct: словарь с уже подсчитанными базовыми данными
    :param lst_svod_cols: список сводных колонок
    :return: словарь
    """
    lst_level = ['1-1,99', '2-2,99', '3-3,99','4-5']

    lst_reindex_one_level_cols = lst_svod_cols.copy()
    lst_reindex_one_level_cols.extend(['1-1,99', '2-2,99', '3-3,99','4-5',
                                       'Итого'])
    # Основная шкала
    svod_count_one_level_ip_df = calc_count_scale(base_df, lst_svod_cols,
                                                 'ИП_Значение',
                                                 'ИП_Диапазон',
                                                 lst_reindex_one_level_cols, lst_level)

    svod_count_one_level_ka_df = calc_count_scale(base_df, lst_svod_cols,
                                                 'КА_Значение',
                                                 'КА_Диапазон',
                                                 lst_reindex_one_level_cols, lst_level)
    # АВА
    svod_count_one_level_aa_df = calc_count_scale(base_df, lst_svod_cols,
                                                 'ЭА_Значение',
                                                 'ЭА_Диапазон',
                                                 lst_reindex_one_level_cols, lst_level)

    svod_count_one_level_pa_df = calc_count_scale(base_df, lst_svod_cols,
                                                 'ПА_Значение',
                                                 'ПА_Диапазон',
                                                 lst_reindex_one_level_cols, lst_level)

    # Считаем среднее по субшкалам
    svod_mean_one_df = pd.pivot_table(base_df,
                                      index=lst_svod_cols,
                                      values=['ИП_Значение',
                                              'КА_Значение',
                                              'ЭА_Значение',
                                              'ПА_Значение',
                                              ],
                                      aggfunc=round_mean_two)
    svod_mean_one_df.reset_index(inplace=True)

    # упорядочиваем колонки
    new_order_cols = lst_svod_cols.copy()
    new_order_cols.extend((['ИП_Значение',
                            'КА_Значение',
                            'ЭА_Значение',
                            'ПА_Значение',
                            ]))
    svod_mean_one_df = svod_mean_one_df.reindex(columns=new_order_cols)

    dct_rename_cols_mean = {'ИП_Значение': 'Ср. Интегральный показатель',
                            'КА_Значение': 'Ср. Когнитивный аспект',
                            'ЭА_Значение': 'Ср. Эмоциональный аспект',
                            'ПА_Значение': 'Ср. Поведенческий аспект',
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
                    f'ИП {out_name}': svod_count_one_level_ip_df,
                    f'КА {out_name}': svod_count_one_level_ka_df,
                    f'ЭА {out_name}': svod_count_one_level_aa_df,
                    f'ПА {out_name}': svod_count_one_level_pa_df,
                    })

    if len(lst_svod_cols) == 1:
        return out_dct
    else:
        for idx, name_column in enumerate(lst_svod_cols):
            lst_reindex_column_level_cols = [lst_svod_cols[idx], '1-1,99', '2-2,99', '3-3,99','4-5',
                                             'Итого']
            # АД
            svod_count_column_level_ip_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                            'ИП_Значение',
                                                            'ИП_Диапазон',
                                                            lst_reindex_column_level_cols, lst_level)

            # АД
            svod_count_column_level_ka_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                            'КА_Значение',
                                                            'КА_Диапазон',
                                                            lst_reindex_column_level_cols, lst_level)
            # АВА
            svod_count_column_level_aa_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                            'ЭА_Значение',
                                                            'ЭА_Диапазон',
                                                            lst_reindex_column_level_cols, lst_level)
            svod_count_column_level_pa_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                            'ПА_Значение',
                                                            'ПА_Диапазон',
                                                            lst_reindex_column_level_cols, lst_level)

            # Считаем среднее по субшкалам
            svod_mean_column_df = pd.pivot_table(base_df,
                                              index=[lst_svod_cols[idx]],
                                              values=['ИП_Значение',
                                                      'КА_Значение',
                                                      'ЭА_Значение',
                                                      'ПА_Значение',
                                                      ],
                                              aggfunc=round_mean_two)
            svod_mean_column_df.reset_index(inplace=True)

            # упорядочиваем колонки
            new_order_cols = [lst_svod_cols[idx]].copy()
            new_order_cols.extend((['ИП_Значение',
                                    'КА_Значение',
                                    'ЭА_Значение',
                                    'ПА_Значение',
                                    ]))
            svod_mean_column_df = svod_mean_column_df.reindex(columns=new_order_cols)

            dct_rename_cols_mean = {'ИП_Значение': 'Ср. Интегральный показатель',
                                    'КА_Значение': 'Ср. Когнитивный аспект',
                                    'ЭА_Значение': 'Ср. Эмоциональный аспект',
                                    'ПА_Значение': 'Ср. Поведенческий аспект',
                                    }
            svod_mean_column_df.rename(columns=dct_rename_cols_mean, inplace=True)

            # Готовим наименование
            name_column = lst_svod_cols[idx]
            name_column = re.sub(r'[\[\]\'+()<> :"?*|\\/]', '_', name_column)
            name_column = name_column[:15]
            out_dct.update({f'Ср {name_column}': svod_mean_column_df,
                            f'ИП {name_column}': svod_count_column_level_ip_df,
                            f'КА {name_column}': svod_count_column_level_ka_df,
                            f'ЭА {name_column}': svod_count_column_level_aa_df,
                            f'ПА {name_column}': svod_count_column_level_pa_df,
                            })
        return out_dct


def processing_ocs_pav(base_df: pd.DataFrame, answers_df: pd.DataFrame, lst_svod_cols:list):
    """
    Функция для обработки
    :param base_df: часть датафрейма с описательными колонками
    :param answers_df: часть датафрейма с ответами
    :param lst_svod_cols:  список с колонками по которым нужно делать свод
    """
    try:
        out_answer_df = base_df.copy()  # делаем копию для последующего соединения с сырыми ответами
        if len(answers_df.columns) != 13:  # проверяем количество колонок с вопросами
            raise BadCountColumnsOCSPDN

        # очищаем названия колонок от возможных сочетаний .1 которые добавляет пандас при одинаковых колонках
        clean_df_lst = []
        for name_column in answers_df.columns:
            clean_name = re.sub(r'.\d+$', '', name_column)
            clean_df_lst.append(clean_name)

        answers_df.columns = clean_df_lst
        lst_check_cols = ['Я считаю, что моя организация говорит одно, а делает другое',
                          'Стратегия, задачи и действия моей организации имеют мало общего между собой',
                          'Когда моя организация заявляет, что хочет что-то предпринять, я удивлюсь, если это произойдет на самом деле',
                          'Моя организация ожидает от своих сотрудников одного, а вознаграждает за другое',
                          'Я вижу мало общего между тем, что моя организация обещает сделать и что делает на самом деле',

                          'Как часто вы испытываете раздражение, когда думаете о своей организации?',
                          'Как часто вы испытываете напряжение, думая о своей организации?',
                          'Как часто вы испытываете беспокойство, думая о своей организации?',

                          'Я жалуюсь на то, что происходит в моей организации, друзьям, которые в ней не работают',
                          'Бывает, я обмениваюсь со своими коллегами понимающими взглядами',
                          'Я часто обсуждаю с другими, как обстоят дела в моей организации',
                          'Я критикую действия и стратегию своей организации при других людях',
                          'Порой я ловлю себя на том, что высмеиваю лозунг и инициативы моей организации',
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
            raise BadOrderOCSPDN

        # словарь для замены слов на числа
        dct_replace_value = {'никогда': 1,
                             'редко': 2,
                             'иногда': 3,
                             'часто': 4,
                             'всегда': 5,
                             }
        valid_values = [1, 2, 3, 4, 5]
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
            raise BadValueOCSPDN

        base_df['ИП_Значение'] = answers_df.sum(axis=1)
        base_df['ИП_Значение'] = round(base_df['ИП_Значение']/13,2)
        base_df['ИП_Диапазон'] = base_df['ИП_Значение'].apply(calc_level)

        base_df['КА_Значение'] = answers_df.apply(calc_value_ka, axis=1)
        base_df['КА_Диапазон'] = base_df['КА_Значение'].apply(calc_level)

        base_df['ЭА_Значение'] = answers_df.apply(calc_value_aa, axis=1)
        base_df['ЭА_Диапазон'] = base_df['ЭА_Значение'].apply(calc_level)

        base_df['ПА_Значение'] = answers_df.apply(calc_value_pa, axis=1)
        base_df['ПА_Диапазон'] = base_df['ПА_Значение'].apply(calc_level)

        # Создаем датафрейм для создания части в общий датафрейм
        part_df = pd.DataFrame()
        # Основные шкалы
        part_df['ШОЦПДН_ИП_Значение'] = base_df['ИП_Значение']
        part_df['ШОЦПДН_ИП_Диапазон'] = base_df['ИП_Диапазон']

        part_df['ШОЦПДН_КА_Значение'] = base_df['КА_Значение']
        part_df['ШОЦПДН_КА_Диапазон'] = base_df['КА_Диапазон']

        part_df['ШОЦПДН_ЭА_Значение'] = base_df['ЭА_Значение']
        part_df['ШОЦПДН_ЭА_Диапазон'] = base_df['ЭА_Диапазон']

        part_df['ШОЦПДН_ПА_Значение'] = base_df['ПА_Значение']
        part_df['ШОЦПДН_ПА_Диапазон'] = base_df['ПА_Диапазон']

        out_answer_df = pd.concat([out_answer_df, answers_df], axis=1)  # Датафрейм для проверки

        base_df.sort_values(by='ИП_Значение', ascending=False, inplace=True)  # сортируем

        # Делаем свод  по  шкалам
        dct_svod_l = {'ИП_Значение': 'ИП_Диапазон',
                      }

        dct_rename_svod_l = {'ИП_Значение': 'Интегральный показатель',
                             }

        lst_sub = ['1-1,99', '2-2,99', '3-3,99','4-5']

        base_svod_l_df = create_union_svod(base_df, dct_svod_l, dct_rename_svod_l, lst_sub)

        # Делаем свод  по  шкалам
        dct_svod_sub = {'КА_Значение': 'КА_Диапазон',
                        'ЭА_Значение': 'ЭА_Диапазон',
                        'ПА_Значение': 'ПА_Диапазон',
                        }

        dct_rename_svod_sub = {'КА_Значение': 'Когнитивный аспект"',
                               'ЭА_Значение': 'Эмоциональный аспект',
                               'ПА_Значение': 'Поведенческий аспект',
                               }


        base_svod_sub_df = create_union_svod(base_df, dct_svod_sub, dct_rename_svod_sub, lst_sub)

        avg_vcha = round(base_df['ИП_Значение'].mean(), 2)
        avg_o = round(base_df['КА_Значение'].mean(), 2)
        avg_ruvs = round(base_df['ЭА_Значение'].mean(), 2)
        avg_ap = round(base_df['ПА_Значение'].mean(), 2)

        avg_dct = {'Среднее значение интегрального показателя': avg_vcha,
                   'Среднее значение шкалы Когнитивный аспект': avg_o,
                   'Среднее значение шкалы Эмоциональный аспект': avg_ruvs,
                   'Среднее значение шкалы Поведенческий аспект': avg_ap,
                   }

        avg_df = pd.DataFrame.from_dict(avg_dct, orient='index')
        avg_df = avg_df.reset_index()
        avg_df.columns = ['Показатель', 'Среднее значение']

        # формируем основной словарь
        out_dct = {'Списочный результат': base_df,
                   'Список для проверки': out_answer_df,
                   'Свод ИП': base_svod_l_df,
                   'Свод Шкалы': base_svod_sub_df,
                   'Среднее': avg_df,
                   }

        dct_l = {
            'ИП_Диапазон': 'ИП',
        }

        out_dct = create_list_on_level(base_df, out_dct, lst_sub, dct_l)

        dct_prefix = {
            'КА_Диапазон': 'КА',
            'ЭА_Диапазон': 'ЭА',
            'ПА_Диапазон': 'ПА',
        }

        out_dct = create_list_on_level(base_df, out_dct, lst_sub, dct_prefix)

        """
                        Сохраняем в зависимости от необходимости делать своды по определенным колонкам
                        """
        if len(lst_svod_cols) == 0:
            return out_dct, part_df
        else:
            out_dct = create_result_ocs_pavlova(base_df, out_dct, lst_svod_cols)
            return out_dct, part_df

    except BadOrderOCSPDN:
        messagebox.showerror('Лахеcис',
                             f'При обработке вопросов теста Шкала организационного цинизма, OCS Павлова, Дзюбенко, Нартова-Бочавер обнаружены неправильные вопросы. Проверьте названия колонок с вопросами:\n'
                             f'{error_order_message[:5000]}\n'
                             f'Используйте при создании Яндекс-формы написание вопросов из руководства пользователя программы Лахесис.')
    except BadValueOCSPDN:
        messagebox.showerror('Лахеcис',
                             f'При обработке вопросов теста Шкала организационного цинизма, OCS Павлова, Дзюбенко, Нартова-Бочавер обнаружены неправильные варианты ответов. Проверьте ответы на указанных строках:\n'
                             f'{error_message[:5000]}\n'
                             f'Используйте при создании Яндекс-формы написание вариантов ответа из руководства пользователя программы Лахесис.')


    except BadCountColumnsOCSPDN:
        messagebox.showerror('Лахеcис',
                             f'Проверьте количество колонок с ответами на тест Шкала организационного цинизма, OCS Павлова, Дзюбенко, Нартова-Бочавер\n'
                             f'Должно быть 13 колонок с ответами')












