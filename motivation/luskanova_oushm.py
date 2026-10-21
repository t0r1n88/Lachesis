"""
Скрипт для обработки результатов Анкета «Оценка уровня школьной мотивации» Н.Г.Лусканова
"""

import pandas as pd
import re
from tkinter import messagebox
from lachesis_support_functions import round_mean_two,calc_count_scale,create_union_svod, create_list_on_level

class BadOrderOUSHML(Exception):
    """
    Исключение для обработки случая когда колонки не совпадают
    """
    pass


class BadValueOUSHML(Exception):
    """
    Исключение для неправильных значений в вариантах ответов
    """
    pass

class BadCountColumnsOUSHML(Exception):
    """
    Исключение для обработки случая если количество колонок не равно 10
    """
    pass

def calc_value(row):
    """
    Функция для подсчета значения
    :return: число
    """
    value = 0  # результат
    # 1
    if row[0] == 'не очень':
        value += 1
    elif row[0] == 'нравится':
        value += 3
    elif row[0] == 'не нравится':
        value += 0
    # 2
    if row[1] == 'чаще хочется остаться дома':
        value += 0
    elif row[1] == 'бывает по-разному':
        value += 1
    elif row[1] == 'иду с радостью':
        value += 3
    # 3
    if row[2] == 'не знаю':
        value += 1
    elif row[2] == 'остался бы дома':
        value += 0
    elif row[2] == 'пошел бы в школу':
        value += 3
    # 4
    if row[3] == 'не нравится':
        value += 3
    elif row[3] == 'бывает по-разному':
        value += 1
    elif row[3] == 'нравится':
        value += 0
    # 5
    if row[4] == 'хотел бы':
        value += 0
    elif row[4] == 'не хотел бы':
        value += 3
    elif row[4] == 'не знаю':
        value += 1
    # 6
    if row[5] == 'не знаю':
        value += 1
    elif row[5] == 'не хотел бы':
        value += 3
    elif row[5] == 'хотел бы':
        value += 0
    # 7
    if row[6] == 'часто':
        value += 3
    elif row[6] == 'редко':
        value += 1
    elif row[6] == 'не рассказываю':
        value += 0
    # 8
    if row[7] == 'точно не знаю':
        value += 1
    elif row[7] == 'хотел бы':
        value += 0
    elif row[7] == 'не хотел бы':
        value += 3
    # 9
    if row[8] == 'мало':
        value += 1
    elif row[8] == 'много':
        value += 3
    elif row[8] == 'нет друзей':
        value += 0
    # 10
    if row[9] == 'да':
        value += 3
    elif row[9] == 'не очень':
        value += 1
    elif row[9] == 'нет':
        value += 0

    return value

def calc_level(value):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """
    if 25<= value <= 30:
        return f'очень высокий уровень'
    elif 20 <= value <= 24:
        return f'высокий уровень'
    elif 15 <= value <= 19:
        return f'средний уровень'
    elif 10 <= value <= 14:
        return f'низкий уровень'
    else:
        return f'очень низкий'




def processing_oushm_lus(base_df: pd.DataFrame, answers_df: pd.DataFrame, lst_svod_cols:list):
    """
    Функция для обработки
    :param base_df: часть датафрейма с описательными колонками
    :param answers_df: часть датафрейма с ответами
    :param lst_svod_cols:  список с колонками по которым нужно делать свод
    """

    out_answer_df = base_df.copy()  # делаем копию для последующего соединения с сырыми ответами
    if len(answers_df.columns) != 10:  # проверяем количество колонок с вопросами
        raise BadCountColumnsOUSHML

    # очищаем названия колонок от возможных сочетаний .1 которые добавляет пандас при одинаковых колонках
    clean_df_lst = []
    for name_column in answers_df.columns:
        clean_name = re.sub(r'.\d+$', '', name_column)
        clean_df_lst.append(clean_name)

    answers_df.columns = clean_df_lst

    lst_check_cols = ['Тебе нравится в школе?',
                      'Утром, когда ты просыпаешься, ты всегда с радостью идешь в школу или тебе часто хочется остаться дома?',
                      'Если бы учитель сказал, что завтра в школу не обязательно приходить всем ученикам, желающим можно остаться дома, ты бы пошел бы в школу или остался бы дома?',
                      'Тебе нравится, когда у вас отменяют какие-нибудь уроки?',
                      'Ты хотел бы, чтобы тебе не задавали домашних заданий?',
                      'Ты хотел бы, чтобы в школе остались одни перемены?',
                      'Ты часто рассказываешь о школе родителям?',
                      'Ты хотел бы, чтобы у тебя был менее строгий учитель?',
                      'У тебя в классе много друзей?',
                      'Тебе нравятся твои одноклассники?'
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
        raise BadOrderOUSHML


    valid_values = [['не очень','нравится','не нравится'],
                    ['чаще хочется остаться дома', 'бывает по-разному', 'иду с радостью'],
                    ['не знаю', 'остался бы дома', 'пошел бы в школу'],
                    ['не нравится', 'бывает по-разному', 'нравится'],
                    ['хотел бы', 'не хотел бы', 'не знаю'],

                    ['не знаю', 'не хотел бы', 'хотел бы'],
                    ['часто', 'редко', 'не рассказываю'],
                    ['точно не знаю', 'хотел бы', 'не хотел бы'],
                    ['мало', 'много', 'нет друзей'],
                    ['да', 'не очень', 'нет']
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
        raise BadValueOUSHML

    base_df['ОУШМ_Значение'] = answers_df.apply(calc_value, axis=1)
    base_df['ОУШМ_Уровень'] = base_df['ОУШМ_Значение'].apply(calc_level)



    base_df.to_excel('data/res.xlsx',index=False)














