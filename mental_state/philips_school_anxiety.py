"""
Скрипт для обработки результатов теста Школьная тревожность Филлипса
"""

import pandas as pd
import re
from tkinter import messagebox
from lachesis_support_functions import round_mean,create_svod_sub

class BadOrderPHSA(Exception):
    """
    Исключение для обработки случая когда колонки не совпадают
    """
    pass


class BadValuePHSA(Exception):
    """
    Исключение для неправильных значений в вариантах ответов
    """
    pass

class BadCountColumnsPHSA(Exception):
    """
    Исключение для обработки случая если количество колонок не равно 58
    """
    pass



def processing_philips_school_anxiety(base_df: pd.DataFrame, answers_df: pd.DataFrame,lst_svod_cols:list):
    """
    Функция для обработки
    :param base_df: часть датафрейма с описательными колонками
    :param answers_df: часть датафрейма с ответами
    :param lst_svod_cols:  список с колонками по которым нужно делать свод
    """
    out_answer_df = base_df.copy()  # делаем копию для последующего соединения с сырыми ответами
    if len(answers_df.columns) != 58:  # проверяем количество колонок с вопросами
        raise BadCountColumnsPHSA

    # очищаем названия колонок от возможных сочетаний .1 которые добавляет пандас при одинаковых колонках
    clean_df_lst = []
    for name_column in answers_df.columns:
        clean_name = re.sub(r'.\d+$', '', name_column)
        clean_df_lst.append(clean_name)

    answers_df.columns = clean_df_lst

    print('Филлипс')