"""
Скрипт для обработки результатов теста Шкала враждебности Кука-Медлей Менджерицкая
"""

"""
Скрипт для обработки результатов теста Методика оценки нервно-психической устойчивости «Прогноз-2»  В.Ю. Рыбников


"""
import pandas as pd
import re
from tkinter import messagebox
from lachesis_support_functions import round_mean_two,calc_count_scale,create_list_on_level,create_union_svod


class BadOrderCMMH(Exception):
    """
    Исключение для обработки случая когда колонки не совпадают
    """
    pass


class BadValueCMMH(Exception):
    """
    Исключение для неправильных значений в вариантах ответов
    """
    pass

class BadCountColumnsCMMH(Exception):
    """
    Исключение для обработки случая если количество колонок не равно 27
    """
    pass







def processing_cook_medley_mend_hostility(result_df: pd.DataFrame, answers_df: pd.DataFrame, lst_svod_cols:list):
    """
    Функция для обработки
    :param result_df: часть датафрейма с описательными колонками
    :param answers_df: часть датафрейма с ответами
    :param lst_svod_cols:  список с колонками по которым нужно делать свод
    """
    out_answer_df = result_df.copy()  # делаем копию для последующего соединения с сырыми ответами
    if len(answers_df.columns) != 27:  # проверяем количество колонок с вопросами
        raise BadCountColumnsCMMH

    # очищаем названия колонок от возможных сочетаний .1 которые добавляет пандас при одинаковых колонках
    clean_df_lst = []
    for name_column in answers_df.columns:
        clean_name = re.sub(r'.\d+$', '', name_column)
        clean_df_lst.append(clean_name)

    answers_df.columns = clean_df_lst




















