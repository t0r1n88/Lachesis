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


def processing_shso(base_df: pd.DataFrame, answers_df: pd.DataFrame):
    """
    Функция для обработки
    :param base_df: часть датафрейма с описательными колонками
    :param answers_df: часть датафрейма с ответами
    """
    out_answer_df = base_df.copy()  # делаем копию для последующего соединения с сырыми ответами
    if len(answers_df.columns) != 14:  # проверяем количество колонок с вопросами
        raise BadCountColumnsSHSO



