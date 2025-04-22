"""
Скрипт для обработки результатов теста Профессиональные установки подростков Андреева
"""

import pandas as pd
from tkinter import messagebox
from lachesis_support_functions import convert_to_int,round_mean,sort_name_class

class BadOrderPUP(Exception):
    """
    Исключение для обработки случая когда колонки не совпадают
    """
    pass

class BadValuePUP(Exception):
    """
    Исключение для неправильных значений в вариантах ответов
    """
    pass


class BadCountColumnsPUP(Exception):
    """
    Исключение для обработки случая если количество колонок не равно 24
    """
    pass

def calc_value_confidence(row):
    """
    Функция для подсчета уровня уверенности
    :param row: строка с ответами респондента
    :return:
    """
    value_confidence = 0 # счетчик уверенности
    lst_confidence = [1,2,4,5,7,8,9,12,13,15,17,18,19,20,22,23]

    for idx,value in enumerate(row):
        if idx in lst_confidence:
            value_confidence += value

    return value_confidence


def calc_level_confidence(value):
    """
    Функция для вычисления уровня уверенности
    :param value: числовое значение
    :return: строка с уровнем
    """
    if 0 <= value <= 53:
        return 'низкий'
    elif 54 <= value <= 66:
        return 'средний'
    elif 67 <= value:
        return 'высокий'


def calc_value_indecision(row):
    """
    Функция для подсчета уровня неуверенности
    :param row: строка с ответами респондента
    :return:
    """
    value_indecision = 0 # счетчик уверенности
    lst_indecision = [0,3,6,10,11,14,16,21]

    for idx,value in enumerate(row):
        if idx in lst_indecision:
            value_indecision += value

    return value_indecision


def calc_level_indecision(value):
    """
    Функция для вычисления уровня неуверенности
    :param value: числовое значение
    :return: строка с уровнем
    """
    if 0 <= value <= 12:
        return 'низкий'
    elif 13 <= value <= 19:
        return 'средний'
    elif 20 <= value:
        return 'высокий'








def processing_pup(base_df: pd.DataFrame, answers_df: pd.DataFrame):
    """
    Функция для обработки теста Профессиональные установки подростков
    :param base_df:
    :param answers_df:
    :return:
    """
    out_answer_df = base_df.copy()  # делаем копию для последующего соединения с сырыми ответами
    if answers_df.shape[1] != 24:
        raise BadCountColumnsPUP


    lst_check_cols = ['Я слишком плохо знаю мир профессий','Выбор профессии не должен делаться под влиянием эмоций',
                      'Я могу отказаться от многих удовольствий ради престижной будущей профессии','Мне нужна поддержка и помощь в выборе профессии',
                      'Я чувствую, что уже пора готовиться к будущей профессии','Я верю, что стану первоклассным специалистом',
                      'Мне трудно сделать выбор между привлекательными профессиями','Я верю, что смогу развить свои способности ради будущей профессии',
                      'Я знаю, что найду профессию по себе','Я чувствую себя уверенно, когда знаю, что мой профессиональный выбор одобряют другие люди',
                      'Совершенно не знаю, на что ориентироваться при выборе профессии','Реклама многих профессий редко соответствует их реальному содержанию',
                      'Я надеюсь, что выбранная профессия позволит раскрыть мою индивидуальность','Я надеюсь, что моя профессия будет востребованной в будущем',
                      'Совершенно не знаю, с чего мне начать свой профессиональный путь','Я верю, что работа даст мне независимость от родителей',
                      'В выборе профессии я слишком поддаюсь внешним влияниям, советам, примерам','Я знаю, на какого профессионала я хочу стать похожим',
                      'Я надеюсь, что я буду с удовольствием заниматься выбранной профессией','Я приложу все усилия, чтобы сделать успешную карьеру',
                      'Я совсем не стремлюсь к взрослой и самостоятельной жизни','Я плохо представляю свое профессиональное будущее',
                      'Для меня важна не профессия, а карьера','В будущей профессии мне хотелось бы стать известным человеком'
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
        raise BadOrderPUP

    answers_df = answers_df.applymap(convert_to_int)  # приводим к инту
    # проверяем правильность
    valid_values = [1, 2, 3, 4, 5,6]
    # Проверяем, есть ли значения, отличающиеся от указанных в списке
    lst_error_answers = []  # список для хранения строк где найдены неправильные ответы

    for i in range(24):
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
        raise BadValuePUP

    base_df[f'Значение_уверенности'] = answers_df.apply(calc_value_confidence, axis=1)
    base_df['Уровень_уверенности'] = base_df['Значение_уверенности'].apply(calc_level_confidence)

    base_df[f'Значение_нерешительности'] = answers_df.apply(calc_value_indecision, axis=1)
    base_df['Уровень_нерешительности'] = base_df['Значение_нерешительности'].apply(calc_level_indecision)

    # Создаем датафрейм для создания части в общий датафрейм
    part_df = pd.DataFrame(columns=['ПУП_Значение_уверенности', 'ПУП_Уровень_уверенности', 'ПУП_Значение_нерешительности','ПУП_Уровень_нерешительности'])
    part_df['ПУП_Значение_уверенности'] = base_df['Значение_уверенности']
    part_df['ПУП_Уровень_уверенности'] = base_df['Уровень_уверенности']
    part_df['ПУП_Значение_нерешительности'] = base_df['Значение_нерешительности']
    part_df['ПУП_Уровень_нерешительности'] = base_df['Уровень_нерешительности']

    base_df.sort_values(by='Значение_уверенности', ascending=False, inplace=True)  # сортируем
    out_answer_df = pd.concat([out_answer_df, answers_df], axis=1)  # Датафрейм для проверки













