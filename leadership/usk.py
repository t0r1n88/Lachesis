"""
Скрипт для обработки результатов теста уровень самооценки Ковалева
"""


import pandas as pd
import os

def processing_usk(base_df: pd.DataFrame, answers_df: pd.DataFrame, size: int,name_test,threshold_base:int,end_folder:str):
    """
    Функция для обработки
    :param base_df: часть датафрейма с описательными колонками
    :param answers_df: часть датафрейма с ответами
    :param size: количество колонок которое должно быть в answers_df
    :param name_test: название теста
    :param threshold_base: количество колонок
    :param end_folder: конечная папка для сохранения
    """
    pass
