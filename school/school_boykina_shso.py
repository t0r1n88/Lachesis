"""
Скрипт для обработки результатов теста Шкала субъективного остракизма Бойкина
"""
import pandas as pd
from tkinter import messagebox
from lachesis_support_functions import round_mean,sort_name_class

class BadOrderSHSO(Exception):
    """
    Исключение для обработки случая когда колонки не совпадают
    """
    pass


class BadValueSHSO(Exception):
    """
    Исключение для неправильных значений в вариантах ответов
    """
    pass

class BadCountColumnsSHSO(Exception):
    """
    Исключение для обработки случая если количество колонок не равно 14
    """
    pass


def calc_sub_value_ig(row):
    """
    Функция для подсчета значения субшкалы Игнорирование
    :param row: строка с ответами
    :return: число
    """
    lst_pr = [1, 2, 4, 7, 10]

    value_forward = 0 # счетчик прямых ответов
    value_reverse = 0 # счетчик обратных ответов
    lst_forward = [1, 2, 4,7, 10]  # список ответов которые нужно считать простым сложением
    lst_reverse = [] # обратный подсчет

    for idx, value in enumerate(row):
        if idx +1 in lst_pr:
            if idx + 1 in lst_forward:
                # print(f'Прямой подсчет {idx +1}') # Для проверки корректности
                value_forward += value
            elif idx +1 in lst_reverse:
                # print(f'Обратный подсчет {idx +1}')# Для проверки корректности
                if value == 5:
                    value_reverse += 1
                elif value == 4:
                    value_reverse += 2
                elif value == 3:
                    value_reverse += 3
                elif value == 2:
                    value_reverse += 4
                elif value == 1:
                    value_reverse += 5

    return round((value_forward + value_reverse) /5,1)

def calc_level_sub_ig(value):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """
    if 1 <= value <= 1.3:
        return 'низкий уровень социального остракизма'
    elif 1.4 <= value <= 2:
        return 'средний уровень социального остракизма'
    elif 2.1 <= value <= 5:
        return 'высокий уровень социального остракизма'



def calc_sub_value_isk(row):
    """
    Функция для подсчета значения субшкалы Исключение
    :return: число
    """
    lst_pr = [5, 8, 9, 12, 13]

    value_forward = 0 # счетчик прямых ответов
    value_reverse = 0 # счетчик обратных ответов
    lst_forward = []  # список ответов которые нужно считать простым сложением
    lst_reverse = [5, 8, 9, 12, 13] # обратный подсчет

    for idx, value in enumerate(row):
        if idx +1 in lst_pr:
            if idx + 1 in lst_forward:
                # print(f'Прямой подсчет {idx +1}') # Для проверки корректности
                value_forward += value
            elif idx +1 in lst_reverse:
                # print(f'Обратный подсчет {idx +1}')# Для проверки корректности
                if value == 5:
                    value_reverse += 1
                elif value == 4:
                    value_reverse += 2
                elif value == 3:
                    value_reverse += 3
                elif value == 2:
                    value_reverse += 4
                elif value == 1:
                    value_reverse += 5

    return round((value_forward + value_reverse) /5,1)

def calc_level_sub_isk(value):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """
    if 1 <= value <= 2.3:
        return 'низкий уровень социального остракизма'
    elif 2.4 <= value <= 3.4:
        return 'средний уровень социального остракизма'
    elif 3.5 <= value <= 5:
        return 'высокий уровень социального остракизма'



def calc_sub_value_ot(row):
    """
    Функция для подсчета значения субшкалы Отвержение
    :return: число
    """
    lst_pr = [3, 6, 11, 14]

    value_forward = 0 # счетчик прямых ответов
    value_reverse = 0 # счетчик обратных ответов
    lst_forward = [6, 11, 14]  # список ответов которые нужно считать простым сложением
    lst_reverse = [3] # обратный подсчет

    for idx, value in enumerate(row):
        if idx +1 in lst_pr:
            if idx + 1 in lst_forward:
                print(f'Прямой подсчет {idx +1}') # Для проверки корректности
                value_forward += value
            elif idx +1 in lst_reverse:
                print(f'Обратный подсчет {idx +1}')# Для проверки корректности
                if value == 5:
                    value_reverse += 1
                elif value == 4:
                    value_reverse += 2
                elif value == 3:
                    value_reverse += 3
                elif value == 2:
                    value_reverse += 4
                elif value == 1:
                    value_reverse += 5

    return round((value_forward + value_reverse) /5,1)

def calc_level_sub_ot(value):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """
    if 1 <= value <= 1.6:
        return 'низкий уровень социального остракизма'
    elif 1.7 <= value <= 2.5:
        return 'средний уровень социального остракизма'
    elif 2.6 <= value <= 5:
        return 'высокий уровень социального остракизма'














def processing_shso(base_df: pd.DataFrame, answers_df: pd.DataFrame):
    """
    Функция для обработки
    :param base_df: часть датафрейма с описательными колонками
    :param answers_df: часть датафрейма с ответами
    """
    out_answer_df = base_df.copy()  # делаем копию для последующего соединения с сырыми ответами
    if len(answers_df.columns) != 14:  # проверяем количество колонок с вопросами
        raise BadCountColumnsSHSO

    lst_check_cols = ['В основном, другие относятся ко мне как к невидимке',
                      'В основном, другие смотрят сквозь меня, будто я не существую',
                      'В основном, другие отвергают мои предложения',
                      'В основном, другие игнорируют меня во время разговора',
                      'В основном, другие приглашают меня на выходные',
                      'В основном, другие отказывают мне, когда я что-либо спрашиваю',
                      'В основном, другие игнорируют меня',
                      'В основном, другие проводят время со мной у меня дома',
                      'В основном, другие приглашают меня стать членом их клуба, организации, группы',
                      'В основном, другие игнорируют мои приветствия при встрече',
                      'В основном, другие не стесняются писать мне в соцсети, что не пойдут со мной на встречу',
                      'В основном, другие всячески стараются привлечь моё внимание',
                      'В основном, другие приглашают меня присоединиться к ним в хобби, провести вместе выходные или сходить куда-нибудь',
                      'В основном, другие часто противоречат мне в большой компании',
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
        raise BadOrderSHSO

    # словарь для замены слов на числа
    dct_replace_value = {'всегда': 5,
                         'часто': 4,
                         'иногда': 3,
                         'редко': 2,
                         'никогда': 1}

    valid_values = [1, 2, 3, 4, 5]
    answers_df.replace(dct_replace_value, inplace=True)  # заменяем слова на цифры для подсчетов

    # Проверяем, есть ли значения, отличающиеся от указанных в списке
    lst_error_answers = []  # список для хранения строк где найдены неправильные ответы

    for i in range(14):
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
        raise BadValueSHSO

    # Субшкала Принаддежность
    base_df['Значение_субшкалы_Игнорирование'] = answers_df.apply(calc_sub_value_ig, axis=1)
    base_df['Норма_Игнорирование'] = '1,4-2 балла'
    base_df['Уровень_субшкалы_Игнорирование'] = base_df['Значение_субшкалы_Игнорирование'].apply(
        calc_level_sub_ig)

    # Субшкала Исключение
    base_df['Значение_субшкалы_Исключение'] = answers_df.apply(calc_sub_value_isk, axis=1)
    base_df['Норма_Исключение'] = '2,4-3,4 баллов'
    base_df['Уровень_субшкалы_Исключение'] = base_df['Значение_субшкалы_Исключение'].apply(
        calc_level_sub_isk)

    # Субшкала Отвержение
    base_df['Значение_субшкалы_Отвержение'] = answers_df.apply(calc_sub_value_ot, axis=1)
    base_df['Норма_Отвержение'] = '1,7-2,5 баллов'
    base_df['Уровень_субшкалы_Отвержение'] = base_df['Значение_субшкалы_Отвержение'].apply(
        calc_level_sub_ot)








