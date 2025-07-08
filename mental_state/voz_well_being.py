"""
Скрипт для обработки результатов теста общего самочувствия ВОЗ 1999 для школьников
"""
from lachesis_support_functions import round_mean,create_union_svod,create_list_on_level
import pandas as pd
import re
from tkinter import messagebox


class BadOrderVozWellBeing(Exception):
    """
    Исключение для обработки случая когда колонки не совпадают
    """
    pass


class BadValueVozWellBeing(Exception):
    """
    Исключение для неправильных значений в вариантах ответов
    """
    pass


class BadCountColumnsVozWellBeing(Exception):
    """
    Исключение для обработки случая если количество колонок не равно 5
    """
    pass


def calc_value_voz_well_being(row):
    """
    Функция для подсчета значения индекса общего самочувствия ВОЗ 1999
    :param row: строка с ответами
    :return: число
    """
    sum_row = sum(row) # получаем сумму
    return sum_row * 4

def calc_level_voz(value):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """
    if 0 <= value <= 19:
        return '0-19'
    elif 20 <= value <= 39:
        return '20-39'
    elif 40 <= value <= 59:
        return '40-59'
    elif 60 <= value <= 79:
        return '60-79'
    else:
        return '80-100'


def calc_count_level(df:pd.DataFrame, lst_cat:list, val_cat, col_cat, lst_cols:list):
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
    count_df['% 0-19 от общего'] = round(
        count_df['0-19'] / count_df['Итого'], 2) * 100
    count_df['% 20-39 от общего'] = round(
        count_df['20-39'] / count_df['Итого'], 2) * 100
    count_df['% 40-59 от общего'] = round(
        count_df['40-59'] / count_df['Итого'], 2) * 100
    count_df['% 60-79 от общего'] = round(
        count_df['60-79'] / count_df['Итого'], 2) * 100
    count_df['% 80-100 от общего'] = round(
        count_df['80-100'] / count_df['Итого'], 2) * 100

    return count_df

def create_result_voz_well_being(base_df:pd.DataFrame, out_dct:dict, lst_svod_cols:list):
    """
    Функция для подсчета результата если указаны колонки по которым нужно провести свод
    :param df: датафрейм с результатами
    :param out_dct: словарь с уже подсчитанными базовыми данными
    :param lst_svod_cols: список сводных колонок
    :return: словарь
    """
    lst_reindex_one_level_cols = lst_svod_cols.copy()
    lst_reindex_one_level_cols.extend( ['0-19', '20-39',
             '40-59', '60-79', '80-100','Итого'])

    svod_count_one_level_voz_df = calc_count_level(base_df, lst_svod_cols,
                                                      'Значение_общего_самочувствия',
                                                      'Диапазон_общего_самочувствия',
                                                      lst_reindex_one_level_cols)

    # Считаем среднее по субшкалам
    svod_mean_one_df = pd.pivot_table(base_df,
                                      index=lst_svod_cols,
                                      values=['Значение_общего_самочувствия',
                                              ],
                                      aggfunc=round_mean)
    svod_mean_one_df.reset_index(inplace=True)
    # упорядочиваем колонки
    new_order_cols = lst_svod_cols.copy()
    new_order_cols.extend((['Значение_общего_самочувствия',
                            ]))
    svod_mean_one_df = svod_mean_one_df.reindex(columns=new_order_cols)

    dct_rename_cols_mean = {'Значение_общего_самочувствия': 'Среднее значение общего самочувствия',
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
                    f'Свод {out_name}': svod_count_one_level_voz_df})

    if len(lst_svod_cols) == 1:
        return out_dct
    else:
        for idx, name_column in enumerate(lst_svod_cols):
            # Тревожность
            lst_reindex_column_level_cols = [lst_svod_cols[idx],'0-19', '20-39',
             '40-59', '60-79', '80-100','Итого']


            svod_count_column_level_voz_df = calc_count_level(base_df, lst_svod_cols[idx],
                                                           'Значение_общего_самочувствия',
                                                           'Диапазон_общего_самочувствия',
                                                           lst_reindex_column_level_cols)

            # Считаем среднее по субшкалам
            svod_mean_column_df = pd.pivot_table(base_df,
                                              index=[lst_svod_cols[idx]],
                                              values=['Значение_общего_самочувствия',
                                                      ],
                                              aggfunc=round_mean)
            svod_mean_column_df.reset_index(inplace=True)
            # упорядочиваем колонки
            new_order_cols = [lst_svod_cols[idx]].copy()
            new_order_cols.extend((['Значение_общего_самочувствия',
                                    ]))
            svod_mean_column_df = svod_mean_column_df.reindex(columns=new_order_cols)

            dct_rename_cols_mean = {'Значение_общего_самочувствия': 'Среднее значение общего самочувствия',
                                    }
            svod_mean_column_df.rename(columns=dct_rename_cols_mean, inplace=True)

            name_column = lst_svod_cols[idx]
            name_column = re.sub(r'[\[\]\'+()<> :"?*|\\/]', '_', name_column)
            name_column = name_column[:15]
            out_dct.update({f'Ср {name_column}': svod_mean_column_df,
                            f'Свод {name_column}': svod_count_column_level_voz_df})
        return out_dct











def processing_voz_well_being(result_df: pd.DataFrame, answers_df: pd.DataFrame,lst_svod_cols:list):
    """
    Функция для обработки
    :param result_df: часть датафрейма с описательными колонками
    :param answers_df: часть датафрейма с ответами
    :param lst_svod_cols:  список с колонками по которым нужно делать свод
    """
    try:
        out_answer_df = result_df.copy()  # делаем копию для последующего соединения с сырыми ответами

        if len(answers_df.columns) != 5:  # проверяем количество колонок
            raise BadCountColumnsVozWellBeing

        # Словарь с проверочными данными
        lst_check_cols = ['Я чувствую себя бодрой(-ым) и в хорошем настроении',
                          'Я чувствую себя спокойной(-ым) и раскованной(-ым)',
                          'Я чувствую себя активной(-ым) и энергичной(-ым)',
                          'Я просыпаюсь и чувствую себя свежей(-им) и отдохнувшей(-им)',
                          'Каждый день со мной происходят вещи, представляющие для меня интерес']

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
            raise BadOrderVozWellBeing

        # словарь для замены слов на числа
        dct_replace_value = {'Никогда': 0,
                             'Некоторое время': 1,
                             'Менее половины времени': 2,
                             'Более половины времени': 3,
                             'Большую часть времени': 4,
                             'Все время': 5,
                             }

        valid_values = [0, 1, 2, 3, 4, 5]
        answers_df.replace(dct_replace_value, inplace=True)  # заменяем слова на цифры для подсчетов

        # Проверяем, есть ли значения, отличающиеся от указанных в списке
        lst_error_answers = []  # список для хранения строк где найдены неправильные ответы

        for i in range(5):
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
            raise BadValueVozWellBeing

        base_df = pd.DataFrame()
        base_df['Значение_общего_самочувствия'] = answers_df.apply(calc_value_voz_well_being, axis=1)
        base_df['Диапазон_общего_самочувствия'] = base_df['Значение_общего_самочувствия'].apply(calc_level_voz)
        # Создаем датафрейм для создания части в общий датафрейм
        part_df = pd.DataFrame()
        part_df['ИОСВОЗ_Значение'] = base_df['Значение_общего_самочувствия']
        part_df['ИОСВОЗ_Диапазон'] = base_df['Диапазон_общего_самочувствия']

        out_answer_df = pd.concat([out_answer_df, answers_df], axis=1)  # Датафрейм для проверки
        # Соединяем анкетную часть с результатной
        base_df = pd.concat([result_df, base_df], axis=1)

        base_df.sort_values(by='Значение_общего_самочувствия', ascending=False, inplace=True)  # сортируем

        # Делаем свод  по  шкалам
        dct_svod_sub = {'Значение_общего_самочувствия': 'Диапазон_общего_самочувствия',
                        }

        dct_rename_svod_sub = {'Значение_общего_самочувствия': 'Диапазон общего самочувствия',
                               }

        # Списки для шкал
        lst_level = ['0-19', '20-39',
                     '40-59','60-79','80-100']

        base_svod_sub_df = create_union_svod(base_df, dct_svod_sub, dct_rename_svod_sub, lst_level)



        # считаем среднее значение по шкалам
        avg_voz = round(base_df['Значение_общего_самочувствия'].mean(), 2)

        avg_dct = {'Среднее значение индекса общего самочувствия ВОЗ 1999': avg_voz,
                   }

        avg_df = pd.DataFrame.from_dict(avg_dct, orient='index')
        avg_df = avg_df.reset_index()
        avg_df.columns = ['Показатель', 'Среднее значение']

        # формируем основной словарь
        out_dct = {'Списочный результат': base_df, 'Список для проверки': out_answer_df,
                   'Свод':base_svod_sub_df,
                   'Среднее': avg_df,
                   }

        """
            Сохраняем в зависимости от необходимости делать своды по определенным колонкам
            """
        if len(lst_svod_cols) == 0:
            return out_dct, part_df
        else:
            out_dct = create_result_voz_well_being(base_df, out_dct, lst_svod_cols)

            return out_dct, part_df

    except BadOrderVozWellBeing:
        messagebox.showerror('Лахеcис',
                             f'При обработке вопросов теста Индекс общего самочувствия ВОЗ 1999 обнаружены неправильные вопросы. Проверьте названия колонок с вопросами:\n'
                             f'{error_order_message}\n'
                             f'Используйте при создании Яндекс-формы написание вопросов из руководства пользователя программы Лахесис.')
    except BadValueVozWellBeing:
        messagebox.showerror('Лахеcис',
                             f'При обработке вопросов теста Индекс общего самочувствия ВОЗ 1999 обнаружены неправильные варианты ответов. Проверьте ответы на указанных строках:\n'
                             f'{error_message}\n'
                             f'Используйте при создании Яндекс-формы написание вариантов ответа из руководства пользователя программы Лахесис.')

    except BadCountColumnsVozWellBeing:
        messagebox.showerror('Лахеcис',
                             f'Проверьте количество колонок с ответами на тест Индекс общего самочувствия ВОЗ 1999\n'
                             f'Должно быть 5 колонок с вопросами'
                             )




