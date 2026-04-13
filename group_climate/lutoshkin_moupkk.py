"""
Скрипт для обработки результатов теста Методика оценки уровня психологического климата коллектива
А.Н. Лутошкин

"""

import pandas as pd
import re
from tkinter import messagebox
from lachesis_support_functions import round_mean,create_union_svod,create_list_on_level


class BadValueLMOUPKK(Exception):
    """
    Исключение для неправильных значений в вариантах ответов
    """
    pass

class BadCountColumnsLMOUPKK(Exception):
    """
    Исключение для обработки случая если количество колонок не равно 13
    """
    pass


def processing_lutoshkin_moupkk(result_df: pd.DataFrame, answers_df: pd.DataFrame, lst_svod_cols:list):
    """
    Функция для обработки
    :param result_df: часть датафрейма с описательными колонками
    :param answers_df: часть датафрейма с ответами
    :param lst_svod_cols:  список с колонками по которым нужно делать свод
    """
    out_answer_df = result_df.copy()  # делаем копию для последующего соединения с сырыми ответами
    if len(answers_df.columns) != 13:  # проверяем количество колонок с вопросами
        raise BadCountColumnsLMOUPKK

    answers_df.columns = [f'Свойство №{i}' for i in range(1,14)]
    print('MOUPKK')

