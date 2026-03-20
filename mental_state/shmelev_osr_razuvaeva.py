"""
Скрипт для обработки результатов Опросник суицидального риска А.Г. Шмелев Т.Н. Разуваева
"""

import pandas as pd
import re
from tkinter import messagebox
from lachesis_support_functions import round_mean_two,calc_count_scale,create_union_svod, create_list_on_level

class BadOrderOSRSHR(Exception):
    """
    Исключение для обработки случая когда колонки не совпадают
    """
    pass


class BadValueOSRSHR(Exception):
    """
    Исключение для неправильных значений в вариантах ответов
    """
    pass

class BadCountColumnsOSRSHR(Exception):
    """
    Исключение для обработки случая если количество колонок не равно 29
    """
    pass

def calc_level(value):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """
    if 0<= value <= 8:
        return f'0-8 ИП СР'
    elif 9 <= value <= 17:
        return f'9-17 ИП СР'
    elif 18 <= value <= 24:
        return f'18-24 ИП СР'
    else:
        return f'25-29 ИП СР'


def calc_value_d(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [12,14,20,22,27]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_pr:
            if value == 1:
                value_forward += 1

    return value_forward


def calc_level_scale(value,count):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """
    result = round((value / count) * 100)

    return f'{result}%'







def processing_osr_shmel_raz(base_df: pd.DataFrame, answers_df: pd.DataFrame, lst_svod_cols:list):
    """
    Функция для обработки
    :param base_df: часть датафрейма с описательными колонками
    :param answers_df: часть датафрейма с ответами
    :param lst_svod_cols:  список с колонками по которым нужно делать свод
    """
    out_answer_df = base_df.copy()  # делаем копию для последующего соединения с сырыми ответами
    if len(answers_df.columns) != 29:  # проверяем количество колонок с вопросами
        raise BadCountColumnsOSRSHR

    # очищаем названия колонок от возможных сочетаний .1 которые добавляет пандас при одинаковых колонках
    clean_df_lst = []
    for name_column in answers_df.columns:
        clean_name = re.sub(r'.\d+$', '', name_column)
        clean_df_lst.append(clean_name)

    answers_df.columns = clean_df_lst

    lst_check_cols = ['Вы все чувствуете острее, чем большинство людей',
                      'Вас часто одолевают мрачные мысли',
                      'Теперь вы уже не надеетесь добиться желаемого положения в жизни',
                      'В случае неудачи вам трудно начать новое дело',
                      'Вам определенно не везет в жизни',
                      'Учиться вам стало труднее, чем раньше',
                      'Большинство людей довольны жизнью больше, чем вы',
                      'Вы считаете, что смерть является искуплением грехов',
                      'Только зрелый человек может принять решение уйти из жизни',
                      'Временами у вас бывают приступы неудержимого смеха или плача',

                      'Обычно вы осторожны с людьми, которые относятся к вам дружелюбнее, чем вы ожидали',
                      'Вы считаете себя обреченным человеком',
                      'Мало кто искренне пытается помочь другим, если это связано с неудобствами',
                      'У Вас такое впечатление, что вас никто не понимает',
                      'Человек, который вводит других в соблазн, оставляя без присмотра ценное имущество, виноват примерно столько же, сколько и тот, кто это имущество похищает',
                      'В вашей жизни не было таких неудач, когда казалось, что все кончено',
                      'Обычно вы удовлетворены своей судьбой',
                      'Вы считаете, что всегда нужно вовремя поставить точку',
                      'В вашей жизни есть люди, привязанность к которым может очень повлиять на ваши решения и даже изменить их',
                      'Когда вас обижают, вы стремитесь во что бы то ни стало доказать обидчику, что он поступил несправедливо',

                      'Часто вы так переживаете, что это мешает вам говорить',
                      'Вам часто кажется, что обстоятельства, в которых вы оказались, отличаются особой несправедливостью',
                      'Иногда вам кажется, что вы вдруг сделали что-то скверное или даже хуже',
                      'Будущее представляется вам довольно беспросветным',
                      'Большинство людей способны добиваться выгоды не совсем честным путем',
                      'Будущее слишком расплывчато, чтобы строить серьезные планы',
                      'Мало кому в жизни пришлось испытать то, что пережили недавно вы',
                      'Вы склонны так остро переживать неприятности, что не можете выкинуть мысли об этом из головы',
                      'Часто вы действуете необдуманно, повинуясь первому порыву',
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
        raise BadOrderOSRSHR

    # словарь для замены слов на числа
    dct_replace_value = {'нет': 0,
                         'да': 1,
                         }
    valid_values = [0,1]
    answers_df.replace(dct_replace_value, inplace=True)  # заменяем слова на цифры для подсчетов
    # Проверяем, есть ли значения, отличающиеся от указанных в списке
    lst_error_answers = []  # список для хранения строк где найдены неправильные ответы

    for i in range(29):
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
        raise BadValueOSRSHR

    base_df['ИП_Значение'] = answers_df.sum(axis=1)
    base_df['ИП_Диапазон'] = base_df['ИП_Значение'].apply(calc_level)

    base_df['Д_Значение'] = answers_df.apply(calc_value_d,axis=1)
    base_df['Д_Процент'] = base_df['Д_Значение'].apply(lambda x:calc_level_scale(x,5))




    base_df.to_excel('data/res.xlsx')


