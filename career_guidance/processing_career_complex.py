"""
Точка входа для обработки выбранных профориентационных тестов
"""
from ddo import processing_ddo # Дифференциально-диагностический опросник
from cok import processing_cok # Ценностные ориентации в карьере
from ptl import processing_ptl # Профессиональный тип личности
from spp import processing_spp # Сфера профессиональных предпочтений

import pandas as pd
import re


class NotSameSize(Exception):
    """
    Исключение для проверки совпадают ли размеры таблицы с количеством колонок требуемых для выполнения тестов указанных в параметрах
    """
    pass


def generate_result_career_guidance(params_career:str,career_data:str,end_folder:str,threshold_base:int):
    """
    Точка входа для обработки профориентационных тестов
    :param params_career: обрабатываемые тесты
    :param career_data: файл с данными
    :param end_folder: конечная папка
    :param threshold_base: сколько колонок в начале таблицы не относятся к тестовым вопросам
    """

    dct_tests = {'ЦОК': (processing_cok, 41), 'ПТЛ': (processing_ptl, 30),
                         'СПП': (processing_spp, 24), 'ДДО': (processing_ddo, 20)}

    dct_out_name_tests = {'СПП':'Сфера профессиональных предпочтений',
                          'ДДО':'Дифференциально-диагностический опросник',
                          'ПТЛ':'Профессиональный тип личности',
                          'ЦОК':'Ценностные ориентации в карьере'}

    params_df = pd.read_excel(params_career, dtype=str, usecols='A',
                              header=None)  # считываем какие тесты нужно использовать
    params_df.dropna(inplace=True)  # удаляем пустые строки
    lst_used_test = params_df.iloc[:, 0].tolist()  # получаем список
    lst_used_test = [value for value in lst_used_test if value in dct_tests.keys()]  # отбираем только те что прописаны

    # создаем счетчик обработанных колонок
    threshold_finshed = threshold_base

    # Проверяем датафрейм на количество колонок
    df = pd.read_excel(career_data, dtype=str)  # считываем датафрейм
    lst_name_cols = [col for col in df.columns if 'Unnamed' not in col]  # отбрасываем колонки без названия
    df = df[lst_name_cols]

    check_size_df = 0  # проверяем размер датафрейма чтобы он совпадал с количеством вопросов в тестах
    for name_test in lst_used_test:
        check_size_df += dct_tests[name_test][1]
    if check_size_df + threshold_base > df.shape[1]:
        raise NotSameSize

    base_df = df.iloc[:, :threshold_base]  # создаем датафрейм с данными не относящимися к тесту
    # делаем строковыми названия колонок
    base_df.columns = list(map(str, base_df.columns))

    # заменяем пробелы на нижнее подчеркивание и очищаем от пробельных символов в начале и конце
    base_df.columns = [column.strip().replace(' ', '_') for column in base_df.columns]
    # очищаем от всех символов кроме букв цифр
    base_df.columns = [re.sub(r'[^_\d\w]', '', column) for column in base_df.columns]







if __name__ == '__main__':
    main_params_career = 'c:/Users/1/PycharmProjects/Lachesis/data/параметры  СППУ ДДО.xlsx'
    main_career_data = 'c:/Users/1/PycharmProjects/Lachesis/data/data career.xlsx'
    main_end_folder = 'c:/Users/1/PycharmProjects/Lachesis/data/Результат'
    main_quantity_descr_cols = 2

    generate_result_career_guidance(main_params_career, main_career_data, main_end_folder, main_quantity_descr_cols)

    print('Lindy Booth')