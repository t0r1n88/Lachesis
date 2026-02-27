"""
Скрипт для обработки результатов теста Сильные стороны и трудности SDQ Гудман Ульянина и др.
"""

import pandas as pd
import re
from tkinter import messagebox
from lachesis_support_functions import round_mean_two,calc_count_scale,create_union_svod, create_list_on_level

class BadOrderSDQGU(Exception):
    """
    Исключение для обработки случая когда колонки не совпадают
    """
    pass


class BadValueSDQGU(Exception):
    """
    Исключение для неправильных значений в вариантах ответов
    """
    pass

class BadCountColumnsSDQGU(Exception):
    """
    Исключение для обработки случая если количество колонок не равно 23
    """
    pass

def processing_sdq_good_ul(base_df: pd.DataFrame, answers_df: pd.DataFrame, lst_svod_cols:list):
    """
    Функция для обработки
    :param base_df: часть датафрейма с описательными колонками
    :param answers_df: часть датафрейма с ответами
    :param lst_svod_cols:  список с колонками по которым нужно делать свод
    """
    out_answer_df = base_df.copy()  # делаем копию для последующего соединения с сырыми ответами
    if len(answers_df.columns) != 23:  # проверяем количество колонок с вопросами
        raise BadCountColumnsSDQGU

    # очищаем названия колонок от возможных сочетаний .1 которые добавляет пандас при одинаковых колонках
    clean_df_lst = []
    for name_column in answers_df.columns:
        clean_name = re.sub(r'.\d+$', '', name_column)
        clean_df_lst.append(clean_name)

    answers_df.columns = clean_df_lst
    lst_check_cols = ['Я стараюсь быть хорошим с другими людьми',
                      'Я неугомонный, не могу оставаться спокойным',
                      'У меня часто бывают головные боли, боли в животе и тошнота',
                      'Я обычно делюсь с другими (едой, играми, ручками)',
                      'Я сильно сержусь, раздражаюсь и выхожу из себя',
                      'Я обычно один. Чаще всего я играю в одиночестве и занимаюсь сам',
                      'Я много беспокоюсь',
                      'Я пытаюсь помочь, если кто-нибудь расстроен, обижен или болен',
                      'Я постоянно ерзаю и верчусь',
                      'Я много дерусь. Я могу заставить других людей делать то, что я хочу',

                      'Я часто чувствую себя несчастным, унылым, готов расплакаться',
                      'Я обычно нравлюсь своим сверстникам',
                      'Я легко отвлекаюсь, мне трудно сосредоточиться',
                      'Я нервничаю в новой обстановке, легко теряю уверенность',
                      'Я добр к младшим детям',
                      'Меня часто обвиняют во лжи или обмане',
                      'Другие часто дразнят или задирают меня',
                      'Я часто вызываюсь помочь другим (родителям, учителям, детям)',
                      'Я думаю, прежде чем действовать',
                      'Я беру чужие вещи из дома, школы и других мест',
                      'У меня лучше отношения со взрослыми, чем со сверстниками',
                      'Я многого боюсь, легко пугаюсь',
                      'Я делаю до конца работу, которую начал. У меня хорошее внимание',
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
        raise BadOrderSDQGU
    # словарь для замены слов на числа
    dct_replace_value = {'неверно': 0,
                         'отчасти верно': 1,
                         'верно': 2,
                         }
    valid_values = [0, 1, 2]
    answers_df.replace(dct_replace_value, inplace=True)  # заменяем слова на цифры для подсчетов
    # Проверяем, есть ли значения, отличающиеся от указанных в списке
    lst_error_answers = []  # список для хранения строк где найдены неправильные ответы

    for i in range(23):
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
        raise BadValueSDQGU