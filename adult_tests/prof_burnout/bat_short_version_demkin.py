"""
Скрипт для обработки результатов теста BAT краткая версия Демкин
"""

import pandas as pd
import re
from tkinter import messagebox
from lachesis_support_functions import round_mean,create_svod_sub

class BadOrderSBATD(Exception):
    """
    Исключение для обработки случая когда колонки не совпадают
    """
    pass


class BadValueSBATD(Exception):
    """
    Исключение для неправильных значений в вариантах ответов
    """
    pass

class BadCountColumnsSBATD(Exception):
    """
    Исключение для обработки случая если количество колонок не равно 12
    """
    pass


def calc_level_exhaustion(value):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """
    if 1.0 <= value <= 1.66:
        return 'низкий уровень'
    elif 1.67 <= value <= 2.99:
        return 'средний уровень'
    elif 3.0 <= value <= 3.99:
        return 'высокий уровень'
    else:
        return 'очень высокий уровень'


def calc_level_distance(value):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """
    if value == 1.0:
        return 'низкий уровень'
    elif 1.01 <= value <= 2.65:
        return 'средний уровень'
    elif 2.66 <= value <= 3.99:
        return 'высокий уровень'
    else:
        return 'очень высокий уровень'


def calc_level_cog_problem(value):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """
    if 1.0 <=value <= 1.66:
        return 'низкий уровень'
    elif 1.67 <= value <= 2.33:
        return 'средний уровень'
    elif 2.34 <= value <= 3.32:
        return 'высокий уровень'
    else:
        return 'очень высокий уровень'

def calc_level_emo_problem(value):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """
    if value == 1.0:
        return 'низкий уровень'
    elif 1.01 <= value <= 2.0:
        return 'средний уровень'
    elif 2.01 <= value <= 3.0:
        return 'высокий уровень'
    else:
        return 'очень высокий уровень'


def calc_level_burnout(value):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """
    if 1.0 <=value <= 1.50:
        return 'низкий уровень'
    elif 1.51 <= value <= 2.35:
        return 'средний уровень'
    elif 2.36 <= value <= 3.17:
        return 'высокий уровень'
    else:
        return 'очень высокий уровень'




def processing_short_bat_demkin(result_df: pd.DataFrame, answers_df: pd.DataFrame, lst_svod_cols:list):
    """
    Функция для обработки
    :param result_df: часть датафрейма с описательными колонками
    :param answers_df: часть датафрейма с ответами
    :param lst_svod_cols:  список с колонками по которым нужно делать свод
    """
    out_answer_df = result_df.copy()  # делаем копию для последующего соединения с сырыми ответами
    if len(answers_df.columns) != 12:  # проверяем количество колонок с вопросами
        raise BadCountColumnsSBATD

    lst_check_cols = ['На работе я чувствую себя морально истощенным','Все, что я делаю на работе, требует больших усилий','После рабочего дня мне трудно восстановить свои силы',
                      'Я изо всех сил пытаюсь проявить хоть какой-то энтузиазм в своей работе','Я испытываю сильное отвращение к своей работе','Я цинично отношусь к тому, что моя работа значит для других',
                      'На работе мне трудно концентрироваться на задаче','Когда я работаю, мне трудно сосредоточиться','Я совершаю ошибки в своей работе, потому что мои мысли заняты другими вещами',
                      'На работе я чувствую, что не могу контролировать свои эмоции','Я не узнаю себя по тому, как эмоционально реагирую на все на работе','На работе я могу непреднамеренно слишком остро реагировать'
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
        raise BadOrderSBATD

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
        raise BadValueSBATD


    base_df = pd.DataFrame()
    base_df['Значение_Истощение'] = round(answers_df.iloc[:,0:3].sum(axis=1) / 3,2)
    base_df['Уровень_Истощение'] = base_df['Значение_Истощение'].apply(calc_level_exhaustion)

    base_df['Значение_Дистанцирование'] = round(answers_df.iloc[:,3:6].sum(axis=1)/3,2)
    base_df['Уровень_Дистанцирование'] = base_df['Значение_Дистанцирование'].apply(calc_level_distance)

    base_df['Значение_Когнитивные_проблемы'] = round(answers_df.iloc[:,6:9].sum(axis=1)/3,2)
    base_df['Уровень_Когнитивные_проблемы'] = base_df['Значение_Когнитивные_проблемы'].apply(calc_level_cog_problem)

    base_df['Значение_Эмоциональные_проблемы'] = round(answers_df.iloc[:,9:12].sum(axis=1)/3,2)
    base_df['Уровень_Эмоциональные_проблемы'] = base_df['Значение_Эмоциональные_проблемы'].apply(calc_level_emo_problem)

    base_df['Значение_профессионального_выгорания'] = round(answers_df.sum(axis=1)/12,2)
    base_df['Уровень_профессионального_выгорания'] = base_df['Значение_профессионального_выгорания'].apply(calc_level_burnout)

    # Создаем датафрейм для создания части в общий датафрейм
    part_df = pd.DataFrame()
    part_df['БАТКД_Значение_профессионального_выгорания'] = base_df['Значение_профессионального_выгорания']
    part_df['БАТКД_Уровень_профессионального_выгорания'] = base_df['Уровень_профессионального_выгорания']

    part_df['БАТКД_Значение_Истощение'] = base_df['Значение_Истощение']
    part_df['БАТКД_Уровень_Истощение'] = base_df['Уровень_Истощение']

    part_df['БАТКД_Значение_Дистанцирование'] = base_df['Значение_Дистанцирование']
    part_df['БАТКД_Уровень_Дистанцирование'] = base_df['Уровень_Дистанцирование']

    part_df['БАТКД_Когнитивные_проблемы'] = base_df['Значение_Когнитивные_проблемы']
    part_df['БАТКД_Когнитивные_проблемы'] = base_df['Уровень_Когнитивные_проблемы']

    part_df['БАТКД_Эмоциональные_проблемы'] = base_df['Значение_Эмоциональные_проблемы']
    part_df['БАТКД_Эмоциональные_проблемы'] = base_df['Уровень_Эмоциональные_проблемы']

    new_order_cols = ['Значение_профессионального_выгорания','Уровень_профессионального_выгорания',
                      'Значение_Истощение','Уровень_Истощение',
                      'Значение_Дистанцирование','Уровень_Дистанцирование',
                      'Значение_Когнитивные_проблемы','Уровень_Когнитивные_проблемы',
                      'Значение_Эмоциональные_проблемы','Уровень_Эмоциональные_проблемы',
                      ]

    base_df = base_df.reindex(columns=new_order_cols)
    # Соединяем анкетную часть с результатной
    base_df = pd.concat([result_df, base_df], axis=1)

    base_df.sort_values(by='Значение_профессионального_выгорания', ascending=False, inplace=True)  # сортируем
    out_answer_df = pd.concat([out_answer_df, answers_df], axis=1)  # Датафрейм для проверки

    # Общий свод по уровням общей шкалы всего в процентном соотношении
    base_svod_all_df = pd.DataFrame(
        index=['низкий уровень', 'средний уровень',
               'высокий уровень','очень высокий уровень'])

    svod_level_df = pd.pivot_table(base_df, index='Уровень_профессионального_выгорания',
                                   values='Значение_профессионального_выгорания',
                                   aggfunc='count')

    svod_level_df['% от общего'] = round(
        svod_level_df['Значение_профессионального_выгорания'] / svod_level_df[
            'Значение_профессионального_выгорания'].sum(), 3) * 100

    base_svod_all_df = base_svod_all_df.join(svod_level_df)

    # # Создаем суммирующую строку
    base_svod_all_df.loc['Итого'] = svod_level_df.sum()
    base_svod_all_df.reset_index(inplace=True)
    base_svod_all_df.rename(columns={'index': 'Уровень', 'Значение_профессионального_выгорания': 'Количество'},
                            inplace=True)
    # формируем основной словарь
    out_dct = {'Списочный результат': base_df, 'Список для проверки': out_answer_df,
               'Свод Общий': base_svod_all_df,
               }

    lst_level = ['низкий уровень', 'средний уровень',
               'высокий уровень','очень высокий уровень']
    dct_level = dict()

    for level in lst_level:
        temp_df = base_df[base_df['Уровень_выгорания'] == level]
        if temp_df.shape[0] != 0:
            dct_level[level] = temp_df

    out_dct.update(dct_level)

    # Свод по шкалам
    base_svod_exhaustion = create_svod_sub(base_df, lst_level, 'Уровень_Истощение',
                        'Значение_Истощение', 'count')
    base_svod_distance = create_svod_sub(base_df, lst_level, 'Уровень_Истощение',
                        'Значение_Истощение', 'count')
    base_svod_cog_problem = create_svod_sub(base_df, lst_level, 'Уровень_Истощение',
                        'Значение_Истощение', 'count')
    base_svod_emo_problem = create_svod_sub(base_df, lst_level, 'Уровень_Истощение',
                        'Значение_Истощение', 'count')



















