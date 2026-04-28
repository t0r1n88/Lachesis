"""
Скрипт для обработки результатов Индекс социокультурной безопасности школьника Гилемханова
"""

import pandas as pd
import re
from tkinter import messagebox
from lachesis_support_functions import round_mean_two,calc_count_scale,create_union_svod, create_list_on_level

class BadOrderISKBSHG(Exception):
    """
    Исключение для обработки случая когда колонки не совпадают
    """
    pass


class BadValueISKBSHG(Exception):
    """
    Исключение для неправильных значений в вариантах ответов
    """
    pass

class BadCountColumnsISKBSHG(Exception):
    """
    Исключение для обработки случая если количество колонок не равно 35
    """
    pass

def processing_iskbsh_gil(base_df: pd.DataFrame, answers_df: pd.DataFrame, lst_svod_cols:list):
    """
    Функция для обработки
    :param base_df: часть датафрейма с описательными колонками
    :param answers_df: часть датафрейма с ответами
    :param lst_svod_cols:  список с колонками по которым нужно делать свод
    """
    out_answer_df = base_df.copy()  # делаем копию для последующего соединения с сырыми ответами
    if len(answers_df.columns) != 35:  # проверяем количество колонок с вопросами
        raise BadCountColumnsISKBSHG

    # очищаем названия колонок от возможных сочетаний .1 которые добавляет пандас при одинаковых колонках
    clean_df_lst = []
    for name_column in answers_df.columns:
        clean_name = re.sub(r'.\d+$', '', name_column)
        clean_df_lst.append(clean_name)

    answers_df.columns = clean_df_lst

    print('ISKBSH')