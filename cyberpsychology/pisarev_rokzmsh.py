"""
Скрипт для обработки результатов теста для родителей младших школьников на определение компьютерной зависимости В.Г. Писарев
"""

import pandas as pd
import re
from tkinter import messagebox
from lachesis_support_functions import round_mean_two,calc_count_scale,create_union_svod, create_list_on_level

class BadOrderROKZMSHP(Exception):
    """
    Исключение для обработки случая когда колонки не совпадают
    """
    pass


class BadValueROKZMSHP(Exception):
    """
    Исключение для неправильных значений в вариантах ответов
    """
    pass

class BadCountColumnsROKZMSHP(Exception):
    """
    Исключение для обработки случая если количество колонок не равно 7
    """
    pass


def calc_value(row):
    """
    Фнукция подсчета значения
    :param row:
    :return:
    """
    value = 0
    # 1
    if row[0] == 'когда нечем заняться':
        value += 1
    elif row[0] == 'через день':
        value += 2
    elif row[0] == 'каждый день':
        value += 3
    # 2
    if row[1] == 'час максимум':
        value += 1
    elif row[1] == 'час или 2 часа':
        value += 2
    elif row[1] == '2–3 часа и больше':
        value += 3
    # 3
    if row[2] == 'ребенок самостоятельно':
        value += 1
    elif row[2] == 'иногда вы, иногда ребенок':
        value += 2
    elif row[2] == 'вы':
        value += 3
    # 4
    if row[3] == 'гуляет на улице или занимается домашними делами':
        value += 1
    elif row[3] == 'иногда может и сесть за компьютер':
        value += 2
    elif row[3] == 'сидит за компьютером':
        value += 3
    # 5
    if row[4] == 'нет':
        value += 1
    elif row[4] == 'было пару раз, но не очень важное событие':
        value += 2
    elif row[4] == 'да, прогуливал':
        value += 3
    # 6
    if row[5] == 'редко, почти никогда':
        value += 1
    elif row[5] == 'иногда рассказывает':
        value += 2
    elif row[5] == 'да, постоянно':
        value += 3
    # 7
    if row[6] == 'ребенок особенно не интересуется компьютером':
        value += 1
    elif row[6] == 'значит много, но есть много других вещей, которые для него важны не меньше':
        value += 2
    elif row[6] == 'это для него все или почти все':
        value += 3
    return value

def calc_level(value):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """
    if 7<= value <= 11:
        return f'отсутствие КЗ'
    elif 12 <= value <= 17:
        return f'склонность к КЗ'
    else:
        return f'наличие КЗ'


def create_result_rokzmsh_pis(base_df:pd.DataFrame, out_dct:dict, lst_svod_cols:list):
    """
    Функция для подсчета результата если указаны колонки по которым нужно провести свод
    :param df: датафрейм с результатами
    :param out_dct: словарь с уже подсчитанными базовыми данными
    :param lst_svod_cols: список сводных колонок
    :return: словарь
    """

    lst_level = ['отсутствие КЗ', 'склонность к КЗ', 'наличие КЗ']

    lst_reindex_one_level_cols = lst_svod_cols.copy()
    lst_reindex_one_level_cols.extend(['отсутствие КЗ', 'склонность к КЗ', 'наличие КЗ',
                                       'Итого'])  # Основная шкала

    svod_count_one_level_vcha_df = calc_count_scale(base_df, lst_svod_cols,
                                                    'КЗ_Значение',
                                                    'КЗ_Уровень',
                                                    lst_reindex_one_level_cols, lst_level)

    # Считаем среднее по субшкалам
    svod_mean_one_df = pd.pivot_table(base_df,
                                      index=lst_svod_cols,
                                      values=[
                                              'КЗ_Значение',
                                              ],
                                      aggfunc=round_mean_two)
    svod_mean_one_df.reset_index(inplace=True)

    # упорядочиваем колонки
    new_order_cols = lst_svod_cols.copy()
    new_order_cols.extend(([ 'КЗ_Значение'
                            ]))
    svod_mean_one_df = svod_mean_one_df.reindex(columns=new_order_cols)

    dct_rename_cols_mean = {'КЗ_Значение': 'Ср. Компьютерная зависимость',
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
                    f'КЗ {out_name}': svod_count_one_level_vcha_df,
                    })

    if len(lst_svod_cols) == 1:
        return out_dct
    else:
        for idx, name_column in enumerate(lst_svod_cols):
            lst_reindex_column_level_cols = [lst_svod_cols[idx],'отсутствие КЗ', 'склонность к КЗ', 'наличие КЗ',
                                                  'Итого']

            svod_count_column_level_vcha_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                               'КЗ_Значение',
                                                               'КЗ_Уровень',
                                                               lst_reindex_column_level_cols, lst_level)

            # Считаем среднее по субшкалам
            svod_mean_column_df = pd.pivot_table(base_df,
                                              index=[lst_svod_cols[idx]],
                                              values=[
                                                  'КЗ_Значение',
                                              ],
                                              aggfunc=round_mean_two)
            svod_mean_column_df.reset_index(inplace=True)

            # упорядочиваем колонки
            new_order_cols = [lst_svod_cols[idx]].copy()
            new_order_cols.extend((['КЗ_Значение'
                                    ]))
            svod_mean_column_df = svod_mean_column_df.reindex(columns=new_order_cols)

            dct_rename_cols_mean = {'КЗ_Значение': 'Ср. Компьютерная зависимость',
                                    }
            svod_mean_column_df.rename(columns=dct_rename_cols_mean, inplace=True)

            # Готовим наименование
            name_column = lst_svod_cols[idx]
            name_column = re.sub(r'[\[\]\'+()<> :"?*|\\/]', '_', name_column)
            name_column = name_column[:15]
            out_dct.update({f'Ср {name_column}': svod_mean_column_df,
                            f'КЗ {name_column}': svod_count_column_level_vcha_df,
                            })
        return out_dct








def processing_rokzmsh_pis(base_df: pd.DataFrame, answers_df: pd.DataFrame, lst_svod_cols:list):
    """
    Функция для обработки
    :param base_df: часть датафрейма с описательными колонками
    :param answers_df: часть датафрейма с ответами
    :param lst_svod_cols:  список с колонками по которым нужно делать свод
    """
    try:
        out_answer_df = base_df.copy()  # делаем копию для последующего соединения с сырыми ответами
        if len(answers_df.columns) != 7:  # проверяем количество колонок с вопросами
            raise BadCountColumnsROKZMSHP

        # очищаем названия колонок от возможных сочетаний .1 которые добавляет пандас при одинаковых колонках
        clean_df_lst = []
        for name_column in answers_df.columns:
            clean_name = re.sub(r'.\d+$', '', name_column)
            clean_df_lst.append(clean_name)

        answers_df.columns = clean_df_lst

        lst_check_cols = ['Как часто ваш ребенок играет за компьютером?',
                          'Сколько времени он тратит на компьютерные игры ежедневно?',
                          'Кто выключает компьютер ребенка?',
                          'Когда у вашего ребенка появляется свободное от учебы время, он:',
                          'Прогуливал ли ваш ребенок учебу или другое важное мероприятие ради того, чтобы поиграть за компьютером?',
                          'Делится ли ребенок впечатлениями о какой-либо компьютерной игре с вами?',
                          'Какую роль в жизни ребенка играет компьютер?',
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
            raise BadOrderROKZMSHP

        valid_values = [['каждый день','через день','когда нечем заняться'],
                        ['2–3 часа и больше','час или 2 часа','час максимум'],
                        ['вы','иногда вы, иногда ребенок','ребенок самостоятельно'],
                        ['сидит за компьютером','иногда может и сесть за компьютер','гуляет на улице или занимается домашними делами'],

                        ['да, прогуливал','было пару раз, но не очень важное событие','нет'],
                        ['да, постоянно','иногда рассказывает','редко, почти никогда'],
                        ['это для него все или почти все','значит много, но есть много других вещей, которые для него важны не меньше','ребенок особенно не интересуется компьютером']
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
            raise BadValueROKZMSHP

        base_df['КЗ_Значение'] = answers_df.apply(calc_value, axis=1)
        base_df['КЗ_Уровень'] = base_df['КЗ_Значение'].apply(calc_level)

        # Создаем датафрейм для создания части в общий датафрейм
        part_df = pd.DataFrame()

        # Основные шкалы

        part_df['РОКЗМШК_Значение'] = base_df['КЗ_Значение']
        part_df['РОКЗМШК_Уровень'] = base_df['КЗ_Уровень']

        out_answer_df = pd.concat([out_answer_df, answers_df], axis=1)  # Датафрейм для проверки

        base_df.sort_values(by='КЗ_Значение', ascending=False, inplace=True)  # сортируем

        # Делаем свод  по  шкалам
        dct_svod_sub = {'КЗ_Значение': 'КЗ_Уровень',
                        }

        dct_rename_svod_sub = {
            'КЗ_Значение': 'Уровень компьютерной зависимости',
        }

        lst_sub = ['отсутствие КЗ', 'склонность к КЗ', 'наличие КЗ']

        base_svod_sub_df = create_union_svod(base_df, dct_svod_sub, dct_rename_svod_sub, lst_sub)

        avg_psp = round(base_df['КЗ_Значение'].mean(), 2)

        avg_dct = {'Среднее значение Компьютерной зависимости': avg_psp,
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

        dct_prefix = {'КЗ_Уровень': 'КЗ',
                      }

        out_dct = create_list_on_level(base_df, out_dct, lst_sub, dct_prefix)

        """
                        Сохраняем в зависимости от необходимости делать своды по определенным колонкам
                        """
        if len(lst_svod_cols) == 0:
            return out_dct, part_df
        else:
            out_dct = create_result_rokzmsh_pis(base_df, out_dct, lst_svod_cols)
            return out_dct, part_df


    except BadOrderROKZMSHP:
        messagebox.showerror('Лахеcис',
                             f'При обработке вопросов теста для Родителей младших школьников на определение компьютерной зависимости Писарев обнаружены неправильные вопросы. Проверьте названия колонок с вопросами:\n'
                             f'{error_order_message[:5000]}\n'
                             f'Используйте при создании Яндекс-формы написание вопросов из руководства пользователя программы Лахесис.')
    except BadValueROKZMSHP:
        messagebox.showerror('Лахеcис',
                             f'При обработке вопросов теста для Родителей младших школьников на определение компьютерной зависимости Писарев обнаружены неправильные варианты ответов. Проверьте ответы на указанных строках:\n'
                             f'{error_message[:5000]}\n'
                             f'Используйте при создании Яндекс-формы написание вариантов ответа из руководства пользователя программы Лахесис.')


    except BadCountColumnsROKZMSHP:
        messagebox.showerror('Лахеcис',
                             f'Проверьте количество колонок с ответами на тест для Родителей младших школьников на определение компьютерной зависимости Писарев\n'
                             f'Должно быть 7 колонок с ответами')