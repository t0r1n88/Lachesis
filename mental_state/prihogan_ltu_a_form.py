"""
Скрипт для обработки результатов теста Шкала личностной тревожности учащихся А. М. Прихожан Форма А

"""

import pandas as pd
import re
import os
import openpyxl
from openpyxl.utils.dataframe import dataframe_to_rows
from openpyxl.styles import Alignment
from openpyxl.utils import get_column_letter
from tkinter import messagebox
from lachesis_support_functions import create_union_svod,create_list_on_level,round_mean

class BadOrderLTUPA(Exception):
    """
    Исключение для обработки случая когда колонки не совпадают
    """
    pass


class BadValueLTUPA(Exception):
    """
    Исключение для неправильных значений в вариантах ответов
    """
    pass

class BadCountColumnsLTUPA(Exception):
    """
    Исключение для обработки случая если количество колонок не равно 40
    """
    pass

class NotReqColumnLTUPA(Exception):
    """
    Исключение для обработки случая когда нет обязательных колонок Пол И Возраст
    """
    pass

class BadValueSexLTUPA(Exception):
    """
    Исключение для обработки случая когда в колонке Пол есть значения отличающиеся от Мужской или Женский
    """
    pass

class BadValueAgeLTUPA(Exception):
    """
    Исключение для обработки случая когда в колонке Пол есть значения отличающиеся от требуемого возраста
    """
    pass






def processing_ltu_prih_form_a(base_df: pd.DataFrame, answers_df: pd.DataFrame, lst_svod_cols:list):
    """
    Функция для обработки
    :param base_df: часть датафрейма с описательными колонками
    :param answers_df: часть датафрейма с ответами
    :param lst_svod_cols:  список с колонками по которым нужно делать свод
    """
    union_base_df = base_df.copy()  # делаем копию анкетной части чтобы потом соединить ее с ответной частью
    quantity_cols_base_df = base_df.shape[1]  # количество колонок в анкетной части

    out_answer_df = base_df.copy()  # делаем копию для последующего соединения с сырыми ответами
    if len(answers_df.columns) != 40:  # проверяем количество колонок с вопросами
        raise BadCountColumnsLTUPA

    # очищаем названия колонок от возможных сочетаний .1 которые добавляет пандас при одинаковых колонках
    clean_df_lst = []
    for name_column in answers_df.columns:
        clean_name = re.sub(r'.\d+$', '', name_column)
        clean_df_lst.append(clean_name)

    answers_df.columns = clean_df_lst

    lst_check_cols = ['Отвечать у доски',
                      'Оказаться среди незнакомых ребят',
                      'Участвовать в соревнованиях, конкурсах, олимпиадах',
                      'Слышать заклятия',
                      'Разговаривать с директором школы',
                      'Сравнивать себя с другими',
                      'Учитель смотрит по журналу, кого спросить',
                      'Тебя критикуют, в чем-то упрекают',
                      'На тебя смотрят, когда ты что-нибудь делаешь (наблюдают за тобой во время работы, решения задачи)',
                      'Видеть плохие сны',

                      'Писать контрольную работу, выполнять тест по какому-нибудь предмету',
                      'После контрольной, теста – учитель называет отметки',
                      'У тебя что-то не получается',
                      'Смотреть на человека, похожего на мага, колдуна',
                      'На тебя не обращают внимания',
                      'Ждешь родителей с родительского собрания',
                      'Тебе грозит неуспех, провал',
                      'Слышать смех за своей спиной',
                      'Не понимать объяснений учителя',
                      'Думаешь о том, чего ты сможешь добиться в будущем',

                      'Слышать предсказания о космических катастрофах',
                      'Выступать перед зрителями',
                      'Слышать, что какой-то человек «напускает порчу» на других',
                      'С тобой не хотят играть',
                      'Проверяются твои способности',
                      'На тебя смотрят как на маленького',
                      'На экзамене тебе достался 13-й билет',
                      'На уроке учитель неожиданно задает тебе вопрос',
                      'Оценивается твоя работа',
                      'Не можешь справиться с домашним заданием',

                      'Засыпать в темной комнате',
                      'Не соглашаешься с родителями',
                      'Берешься за новое дело',
                      'Разговаривать с школьным психологом',
                      'Думать о том, что тебя могут «сглазить»',
                      'Замолчали, когда ты подошел (подошла)',
                      'Слушать страшные истории',
                      'Спорить со своим другом (подругой)',
                      'Думать о своей внешности',
                      'Думать о призраках, других страшных, «потусторонних» существах'
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
        raise BadOrderLTUPA

    # словарь для замены слов на числа
    dct_replace_value = {'нет': 0,
                         'немного': 1,
                         'достаточно': 2,
                         'значительно': 3,
                         'очень': 4,
                         }
    valid_values = [0, 1, 2, 3,4]
    answers_df.replace(dct_replace_value, inplace=True)  # заменяем слова на цифры для подсчетов
    # Проверяем, есть ли значения, отличающиеся от указанных в списке
    lst_error_answers = []  # список для хранения строк где найдены неправильные ответы

    for i in range(40):
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
        raise BadValueLTUPA