"""
Скрипт для обработки результатов теста Опросник мотивации к достижению цели, к успеху Элерс Котик
"""

import pandas as pd
import re
from tkinter import messagebox
from lachesis_support_functions import create_union_svod, calc_count_scale,round_mean_two

class BadOrderKMT(Exception):
    """
    Исключение для обработки случая когда колонки не совпадают
    """
    pass


class BadValueKMT(Exception):
    """
    Исключение для неправильных значений в вариантах ответов
    """
    pass

class BadCountColumnsKMT(Exception):
    """
    Исключение для обработки случая если количество колонок не равно 41
    """
    pass


def processing_kotik_motiv_target(result_df: pd.DataFrame, answers_df: pd.DataFrame,lst_svod_cols:list):
    """
    Функция для обработки
    :param base_df: часть датафрейма с описательными колонками
    :param answers_df: часть датафрейма с ответами
    :param lst_svod_cols:  список с колонками по которым нужно делать свод
    """
    out_answer_df = result_df.copy()  # делаем копию для последующего соединения с сырыми ответами
    if len(answers_df.columns) != 41:  # проверяем количество колонок с вопросами
        raise BadCountColumnsKMT

    print('kotik')