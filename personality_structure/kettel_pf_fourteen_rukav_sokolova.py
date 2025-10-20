"""
Скрипт для обработки результатов теста Методика многофакторного исследования личности Кеттела
(подростковый вариант) 14-PF Рукавишников Соколова

"""

import pandas as pd
import re
from tkinter import messagebox
from lachesis_support_functions import calc_count_scale,round_mean

class BadOrderKPFRS(Exception):
    """
    Исключение для обработки случая когда колонки не совпадают
    """
    pass


class BadValueKPFRS(Exception):
    """
    Исключение для неправильных значений в вариантах ответов
    """
    pass

class BadCountColumnsKPFRS(Exception):
    """
    Исключение для обработки случая если количество колонок не равно 142
    """
    pass

def processing_kettel_pf_ruk_sok(result_df: pd.DataFrame, answers_df: pd.DataFrame,lst_svod_cols:list):
    """
    Функция для обработки
    :param base_df: часть датафрейма с описательными колонками
    :param answers_df: часть датафрейма с ответами
    :param lst_svod_cols:  список с колонками по которым нужно делать свод
    """
    out_answer_df = result_df.copy()  # делаем копию для последующего соединения с сырыми ответами
    if len(answers_df.columns) != 142:  # проверяем количество колонок с вопросами
        raise BadCountColumnsKPFRS
    # очищаем названия колонок от возможных сочетаний .1 которые добавляет пандас при одинаковых колонках
    clean_df_lst = []
    for name_column in answers_df.columns:
        clean_name = re.sub(r'.\d+$', '', name_column)
        clean_df_lst.append(clean_name)

    answers_df.columns = clean_df_lst
    print('kettel')

