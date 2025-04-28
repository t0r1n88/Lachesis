"""
Скрипт для обработки результатов теста Шкала нарушенных потребностей остракизм Бойкина
"""

import pandas as pd
from tkinter import messagebox
from lachesis_support_functions import round_mean,sort_name_class

class BadOrderSHNPO(Exception):
    """
    Исключение для обработки случая когда колонки не совпадают
    """
    pass


class BadValueSHNPO(Exception):
    """
    Исключение для неправильных значений в вариантах ответов
    """
    pass

class BadCountColumnsSHNPO(Exception):
    """
    Исключение для обработки случая если количество колонок не равно 20
    """
    pass




def calc_sub_value_pr(row):
    """
    Функция для подсчета значения субшкалы Принадлежности
    :param row: строка с ответами
    :return: число
    """
    lst_pr = [1, 4, 6, 7, 13]

    value_forward = 0 # счетчик прямых ответов
    value_reverse = 0 # счетчик обратных ответов
    lst_forward = [1, 6, 13]  # список ответов которые нужно считать простым сложением
    lst_reverse = [4, 7] # обратный подсчет

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

def calc_level_sub_pr_pod(value):
    """
    Функция для подсчета уровня субшкалы МП подростков
    :param value:
    :return:
    """
    if 1 <= value <= 1.4:
        return 'низкий'
    elif 1.5 <= value <= 2.4:
        return 'средний'
    elif 2.5 <= value <= 5:
        return 'высокий'


def calc_sub_value_sam(row):
    """
    Функция для подсчета значения субшкалы Самоуважение
    :param row: строка с ответами
    :return: число
    """
    lst_pr = [5, 9, 11, 12, 15]

    value_forward = 0 # счетчик прямых ответов
    value_reverse = 0 # счетчик обратных ответов
    lst_forward = [5]  # список ответов которые нужно считать простым сложением
    lst_reverse = [9, 11, 12, 15] # обратный подсчет

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

def calc_level_sub_sam_pod(value):
    """
    Функция для подсчета уровня субшкалы самоуважения
    :param value:
    :return:
    """
    if 1 <= value <= 1.6:
        return 'низкий'
    elif 1.7 <= value <= 2.8:
        return 'средний'
    elif 2.9 <= value <= 5:
        return 'высокий'



def calc_sub_value_con(row):
    """
    Функция для подсчета значения субшкалы Контроль
    :param row: строка с ответами
    :return: число
    """
    lst_pr = [3, 8, 10, 14, 20]

    value_forward = 0 # счетчик прямых ответов
    value_reverse = 0 # счетчик обратных ответов
    lst_forward = [3,8,14,20]  # список ответов которые нужно считать простым сложением
    lst_reverse = [10] # обратный подсчет

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

def calc_level_sub_con_pod(value):
    """
    Функция для подсчета уровня субшкалы самоуважения
    :param value:
    :return:
    """
    if 1 <= value <= 1.2:
        return 'низкий'
    elif 1.3 <= value <= 2.4:
        return 'средний'
    elif 2.5 <= value <= 5:
        return 'высокий'


def calc_sub_value_os(row):
    """
    Функция для подсчета значения субшкалы Осмысленное существование
    :param row: строка с ответами
    :return: число
    """
    lst_pr = [2, 16, 17, 18, 19]

    value_forward = 0 # счетчик прямых ответов
    value_reverse = 0 # счетчик обратных ответов
    lst_forward = [16,19]  # список ответов которые нужно считать простым сложением
    lst_reverse = [2, 17, 18] # обратный подсчет

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

def calc_level_sub_os_pod(value):
    """
    Функция для подсчета уровня субшкалы самоуважения
    :param value:
    :return:
    """
    if 1 <= value <= 1.4:
        return 'низкий'
    elif 1.5 <= value <= 2.6:
        return 'средний'
    elif 2.7 <= value <= 5:
        return 'высокий'











def processing_shnpo(base_df: pd.DataFrame, answers_df: pd.DataFrame):
    """
    Функция для обработки
    :param base_df: часть датафрейма с описательными колонками
    :param answers_df: часть датафрейма с ответами
    """
    out_answer_df = base_df.copy()  # делаем копию для последующего соединения с сырыми ответами
    if len(answers_df.columns) != 20:  # проверяем количество колонок с вопросами
        raise BadCountColumnsSHNPO

    lst_check_cols = ['Я чувствую себя единым целым с другими людьми',
                      'Полагаю, что не вношу значимый вклад во что-либо',
                      'У меня есть уверенность, что я влияю на ход событий в моей жизни',
                      'Среди своего окружения я ощущаю себя лишним',
                      'Люди прислушиваются к моему мнению',
                      'В любой ситуации я чувствую поддержку хоть одного человека',
                      'Я ощущаю себя изгоем',
                      'Я совершенно точно управляю всем в своей жизни',
                      'Мне кажется, большинство из моего окружения невысокого обо мне мнения',
                      'Порой, кажется, что всё зависит от чьей-то чужой воли',
                      'Общаясь с людьми, я чувствую себя неуверенно',
                      'Такое ощущение, что общение с людьми – не моя сильная сторона',
                      'Думаю, что общество, в котором я живу, принимает меня',
                      'Я контролирую свою жизнь',
                      'Я переживаю, что люди плохо думают обо мне',
                      'Мне кажется, что моё участие в жизни окружающих очень важно',
                      'Порой я ощущаю себя невидимкой',
                      'Временами мне кажется, что от меня людям нет никакого толка',
                      'Думаю, мое участие в чем-либо всегда полезно',
                      'Такое ощущение, что у меня впереди еще много разных возможностей'
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
        raise BadOrderSHNPO

    # словарь для замены слов на числа
    dct_replace_value = {'не согласен': 5,
                         'редко': 4,
                         'иногда': 3,
                         'часто': 2,
                         'полностью согласен': 1}

    valid_values = [1, 2, 3, 4, 5]
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
        raise BadValueSHNPO

    # Субшкала Принаддежность
    base_df['Значение_субшкалы_Принадлежность'] = answers_df.apply(calc_sub_value_pr, axis=1)
    base_df['Норма_Принадлежность_Подростки'] = '1,5-2,4 баллов'
    base_df['Уровень_субшкалы_Принадлежность_Подростки'] = base_df['Значение_субшкалы_Принадлежность'].apply(calc_level_sub_pr_pod)

    # Субшкала Самоуважение
    base_df['Значение_субшкалы_Самоуважение'] = answers_df.apply(calc_sub_value_sam, axis=1)
    base_df['Норма_Самоуважение_Подростки'] = '1,7-2,8 баллов'
    base_df['Уровень_субшкалы_Самоуважение_Подростки'] = base_df['Значение_субшкалы_Самоуважение'].apply(calc_level_sub_sam_pod)

    # Субшкала Контроль
    base_df['Значение_субшкалы_Контроль'] = answers_df.apply(calc_sub_value_con, axis=1)
    base_df['Норма_Контроль_Подростки'] = '1,3-2,4 баллов'
    base_df['Уровень_субшкалы_Контроль_Подростки'] = base_df['Значение_субшкалы_Контроль'].apply(calc_level_sub_con_pod)

    # Субшкала Осмысленное сущенствование
    base_df['Значение_субшкалы_Ос_существование'] = answers_df.apply(calc_sub_value_os, axis=1)
    base_df['Норма_Ос_существование_Подростки'] = '1,5-2,6 баллов'
    base_df['Уровень_субшкалы_Ос_существование_Подростки'] = base_df['Значение_субшкалы_Ос_существование'].apply(calc_level_sub_os_pod)



    base_df.to_excel('sdsad.xlsx')

















