"""
Скрипт для обработки результатов теста Миссисипская шкала посттравматического стрессового расстройства (Mississippi Scale for PTSD, CMS) военный вариант
"""
import pandas as pd
import re
from tkinter import messagebox
from lachesis_support_functions import round_mean,create_union_svod



class BadOrderMSMO(Exception):
    """
    Исключение для обработки случая когда колонки не совпадают
    """
    pass


class BadValueMSMO(Exception):
    """
    Исключение для неправильных значений в вариантах ответов
    """
    pass

class BadCountColumnsMSMO(Exception):
    """
    Исключение для обработки случая если количество колонок не равно 35
    """
    pass



def processing_misisip_scale_military_option(result_df: pd.DataFrame, answers_df: pd.DataFrame, lst_svod_cols:list):
    """
    Функция для обработки
    :param result_df: часть датафрейма с описательными колонками
    :param answers_df: часть датафрейма с ответами
    :param lst_svod_cols:  список с колонками по которым нужно делать свод
    """
    out_answer_df = result_df.copy()  # делаем копию для последующего соединения с сырыми ответами
    if len(answers_df.columns) != 35:  # проверяем количество колонок с вопросами
        raise BadCountColumnsMSMO

    # очищаем названия колонок от возможных сочетаний .1 которые добавляет пандас при одинаковых колонках
    clean_df_lst = []
    for name_column in answers_df.columns:
        clean_name = re.sub(r'.\d+$', '', name_column)
        clean_df_lst.append(clean_name)

    answers_df.columns = clean_df_lst

    print('dfsds')