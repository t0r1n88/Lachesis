"""
Скрипт для обработки теста Экспресс оценка выгорания В. Каппони, Т. Новак
"""

import pandas as pd
import re
from tkinter import messagebox
from lachesis_support_functions import round_mean,create_svod_sub

class BadOrderBKN(Exception):
    """
    Исключение для обработки случая когда колонки не совпадают
    """
    pass


class BadValueBKN(Exception):
    """
    Исключение для неправильных значений в вариантах ответов
    """
    pass

class BadCountColumnsBKN(Exception):
    """
    Исключение для обработки случая если количество колонок не равно 10
    """
    pass


def calc_level_attrition(value):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """
    if 0 <= value <= 1:
        return 'выгорание отсутствует'
    elif 2 <= value <= 6:
        return 'средний уровень выгорания'
    elif 7 <= value <= 9:
        return 'высокий уровень выгорания'
    else:
        return 'критический уровень выгорания'


def calc_count_main_level(df:pd.DataFrame, lst_cat:list, val_cat, col_cat, lst_cols:list):
    """
    Функция для создания сводных датафреймов

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
    count_df['% выгорание отсутствует от общего'] = round(
        count_df['выгорание отсутствует'] / count_df['Итого'], 2) * 100
    count_df['% средний уровень выгорания от общего'] = round(
        count_df['средний уровень выгорания'] / count_df['Итого'], 2) * 100
    count_df['% высокий уровень выгорания от общего'] = round(
        count_df['высокий уровень выгорания'] / count_df['Итого'], 2) * 100
    count_df['% критический уровень выгорания от общего'] = round(
        count_df['критический уровень выгорания'] / count_df['Итого'], 2) * 100

    return count_df

def calc_mean(df:pd.DataFrame,lst_cat:list,val_cat):
    """
    Функция для создания сводных датафреймов

    :param df: датафрейм с данными
    :param lst_cat:список колонок по которым будет формироваться свод
    :param val_cat:значение по которому будет формиваться свод
    :return:датафрейм
    """
    calc_mean_df = pd.pivot_table(df, index=lst_cat,
                                       values=val_cat,
                                       aggfunc=round_mean)
    calc_mean_df.reset_index(inplace=True)
    calc_mean_df.rename(columns={val_cat:'Среднее значение'},inplace=True)
    return calc_mean_df







def processing_kapponi_burnout(base_df: pd.DataFrame, answers_df: pd.DataFrame,lst_svod_cols:list):
    """
    Функция для обработки
    :param base_df: часть датафрейма с описательными колонками
    :param answers_df: часть датафрейма с ответами
    :param lst_svod_cols:  список с колонками по которым нужно делать свод
    """
    try:
        out_answer_df = base_df.copy()  # делаем копию для последующего соединения с сырыми ответами
        if len(answers_df.columns) != 10:  # проверяем количество колонок с вопросами
            raise BadCountColumnsBKN

        lst_check_cols = ['Когда в воскресенье пополудни я вспоминаю о том, что завтра снова идти на работу, то остаток выходного дня уже испорчен',
                          'Если бы у меня была возможность уйти на пенсию (по выслуге лет, инвалидности), я сделал (а) бы это без промедления',
                          'Коллеги на работе раздражают меня. Невозможно терпеть их одни и те же разговоры',
                          'То насколько меня раздражают коллеги, еще мелочи по сравнению с тем, как выводят меня из равновесия клиенты (пациенты, ученики, посетители, заказчики)',
                          'На протяжении последних трех месяцев я отказывался (отказывалась) от курсов повышения квалификации, от участия в конференциях и т.д.',
                          'Коллегам (посетителям, заказчикам, ученикам и т.д.) я придумал (а) обидные прозвища (например, "идиоты"), которые использую мысленно',
                          'С делами по службе я справляюсь "одной левой" нет ничего такого, что могло бы удивить меня в ней своей новизной',
                          'О моей работе мне едва ли кто скажет что-нибудь новое',
                          'Стоит мне только вспомнить о своей работе, как хочется взять и послать ее ко всем чертям',
                          'За последние три месяца мне не попала в руки ни одна специальная книга, из которой я почерпнул бы что-нибудь новенькое',
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
            raise BadOrderBKN

        # словарь для замены слов на числа
        dct_replace_value = {'нет': 0,
                             'да': 1}


        valid_values = [0, 1]
        answers_df.replace(dct_replace_value, inplace=True)  # заменяем слова на цифры для подсчетов
        # Проверяем, есть ли значения, отличающиеся от указанных в списке
        lst_error_answers = []  # список для хранения строк где найдены неправильные ответы

        for i in range(10):
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
            raise BadValueBKN

        base_df['Значение_уровня_выгорания'] = answers_df.sum(axis=1)
        base_df['Норма_выгорания'] = '0-1 баллов'
        base_df['Уровень_выгорания'] = base_df['Значение_уровня_выгорания'].apply(calc_level_attrition)

        # Создаем датафрейм для создания части в общий датафрейм
        part_df = pd.DataFrame()

        part_df['ВКН_Значение_выгорания'] = base_df['Значение_уровня_выгорания']
        part_df['ВКН_Уровень_выгорания'] = base_df['Уровень_выгорания']

        base_df.sort_values(by='Значение_уровня_выгорания', ascending=False, inplace=True)  # сортируем
        out_answer_df = pd.concat([out_answer_df, answers_df], axis=1)  # Датафрейм для проверки

        # Общий свод по уровням общей шкалы всего в процентном соотношении
        base_svod_all_df = pd.DataFrame(
            index=['выгорание отсутствует', 'средний уровень выгорания',
                   'высокий уровень выгорания', 'критический уровень выгорания'])

        svod_level_df = pd.pivot_table(base_df, index='Уровень_выгорания',
                                       values='Значение_уровня_выгорания',
                                       aggfunc='count')

        svod_level_df['% от общего'] = round(
            svod_level_df['Значение_уровня_выгорания'] / svod_level_df[
                'Значение_уровня_выгорания'].sum(), 3) * 100

        base_svod_all_df = base_svod_all_df.join(svod_level_df)

        # # Создаем суммирующую строку
        base_svod_all_df.loc['Итого'] = svod_level_df.sum()
        base_svod_all_df.reset_index(inplace=True)
        base_svod_all_df.rename(columns={'index': 'Уровень', 'Значение_уровня_выгорания': 'Количество'},
                                inplace=True)
        # формируем основной словарь
        out_dct = {'Списочный результат': base_df, 'Список для проверки': out_answer_df,
                   'Свод Общий': base_svod_all_df,
                   }

        lst_level = ['выгорание отсутствует', 'средний уровень выгорания',
                   'высокий уровень выгорания', 'критический уровень выгорания']
        dct_level = dict()

        for level in lst_level:
            temp_df = base_df[base_df['Уровень_выгорания'] == level]
            if temp_df.shape[0] != 0:
                dct_level[level] = temp_df

        out_dct.update(dct_level)

        """
                Сохраняем в зависимости от необходимости делать своды по определенным колонкам
                """
        if len(lst_svod_cols) == 0:
            return out_dct, part_df

        elif len(lst_svod_cols) == 1:
            lst_reindex_main_level_cols = [lst_svod_cols[0], 'выгорание отсутствует', 'средний уровень выгорания',
                                           'высокий уровень выгорания', 'критический уровень выгорания',
                                           'Итого']  #

            svod_count_one_level_df = calc_count_main_level(base_df, lst_svod_cols,
                                                            'Значение_уровня_выгорания',
                                                            'Уровень_выгорания',
                                                            lst_reindex_main_level_cols)

            # очищаем название колонки по которой делали свод
            name_one = lst_svod_cols[0]
            name_one = re.sub(r'[\[\]\'+()<> :"?*|\\/]', '_', name_one)
            name_one = name_one[:15]

            # Считаем среднее
            svod_mean_df = calc_mean(base_df, [lst_svod_cols[0]], 'Значение_уровня_выгорания')

            out_dct.update({f'Свод {name_one}': svod_count_one_level_df,
                            f'Ср. {name_one}': svod_mean_df,})

            return out_dct, part_df

        elif len(lst_svod_cols) == 2:
            lst_reindex_main_level_cols = [lst_svod_cols[0], lst_svod_cols[1], 'выгорание отсутствует', 'средний уровень выгорания',
                                           'высокий уровень выгорания', 'критический уровень выгорания',
                                           'Итого']  #

            # первая колонка
            lst_reindex_first_main_level_cols = [lst_svod_cols[0], 'выгорание отсутствует', 'средний уровень выгорания',
                                           'высокий уровень выгорания', 'критический уровень выгорания',
                                           'Итого']
            # вторая колонка
            lst_reindex_second_main_level_cols = [lst_svod_cols[1], 'выгорание отсутствует', 'средний уровень выгорания',
                                           'высокий уровень выгорания', 'критический уровень выгорания',
                                           'Итого']  #




            svod_count_two_level_df = calc_count_main_level(base_df, lst_svod_cols,
                                                            'Значение_уровня_выгорания',
                                                            'Уровень_выгорания',
                                                            lst_reindex_main_level_cols)
            # Считаем среднее по субшкалам
            svod_mean_df = calc_mean(base_df, lst_svod_cols, 'Значение_уровня_выгорания')


            # Первая колонка
            svod_count_first_level_df = calc_count_main_level(base_df, [lst_svod_cols[0]],
                                                            'Значение_уровня_выгорания',
                                                            'Уровень_выгорания',
                                                            lst_reindex_first_main_level_cols)

            # Считаем среднее
            svod_mean_first_df = calc_mean(base_df, [lst_svod_cols[0]], 'Значение_уровня_выгорания')

            # Вторая колонка
            svod_count_second_level_df = calc_count_main_level(base_df, [lst_svod_cols[1]],
                                                              'Значение_уровня_выгорания',
                                                              'Уровень_выгорания',
                                                              lst_reindex_second_main_level_cols)

            # Считаем среднее
            svod_mean_second_df = calc_mean(base_df, [lst_svod_cols[1]], 'Значение_уровня_выгорания')

            # очищаем название колонки по которой делали свод
            name_one = lst_svod_cols[0]
            name_one = re.sub(r'[\[\]\'+()<> :"?*|\\/]', '_', name_one)
            name_one = name_one[:15]

            name_two = lst_svod_cols[1]
            name_two = re.sub(r'[\[\]\'+()<> :"?*|\\/]', '_', name_two)
            name_two = name_two[:15]


            out_dct.update({f'Свод {name_one}': svod_count_first_level_df,
                            f'Ср. {name_one}': svod_mean_first_df,

                            f'Свод {name_two}': svod_count_second_level_df,
                            f'Ср. {name_two}': svod_mean_second_df,

                            f'Свод {name_one[:10]}_{name_two[:10]}': svod_count_two_level_df,
                            f'Ср. {name_one[:10]}_{name_two[:10]}': svod_mean_df})

            return out_dct, part_df

    except BadOrderBKN:
        messagebox.showerror('Лахеcис',
                             f'При обработке вопросов теста Экспресс-оценка выгорания Каппони Новак обнаружены неправильные вопросы. Проверьте названия колонок с вопросами:\n'
                             f'{error_order_message}\n'
                             f'Используйте при создании Яндекс-формы написание вопросов из руководства пользователя программы Лахесис.')
    except BadValueBKN:
        messagebox.showerror('Лахеcис',
                             f'При обработке вопросов теста Экспресс-оценка выгорания Каппони Новак обнаружены неправильные варианты ответов. Проверьте ответы на указанных строках:\n'
                             f'{error_message}\n'
                             f'Используйте при создании Яндекс-формы написание вариантов ответа из руководства пользователя программы Лахесис.')


    except BadCountColumnsBKN:
        messagebox.showerror('Лахеcис',
                             f'Проверьте количество колонок с ответами на тест Экспресс-оценка выгорания Каппони Новак\n'
                             f'Должно быть 10 колонок с ответами')









