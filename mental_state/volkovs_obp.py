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


def processing_volkovs_obp(result_df: pd.DataFrame, answers_df: pd.DataFrame, lst_svod_cols:list):
    """
    Функция для обработки
    :param result_df: часть датафрейма с описательными колонками
    :param answers_df: часть датафрейма с ответами
    :param lst_svod_cols:  список с колонками по которым нужно делать свод
    """
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