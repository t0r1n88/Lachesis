"""
Скрипт для обработки тестов студентов СПО
"""
from spo_kondash_anxiety import processing_kondash_anxiety # функция для обработки результатов теста тревожности Кондаша


import pandas as pd
import openpyxl
from tkinter import messagebox
import re


class NotSameSize(Exception):
    """
    Исключение для проверки совпадают ли размеры таблицы с количеством колонок требуемых для выполнения тестов указанных в параметрах
    """
    pass




def processing_bek(base_df: pd.DataFrame, answers_df: pd.DataFrame, size: int, name_test):
    pass


def generate_result_spo(params_spo: str, data_spo: str, end_folder: str, threshold_base: int):
    """
    Функция для генерации результатов комплексного теста на оценку состояния тревожности
    :param params_spo: какие тесты используются и в каком порядке
    :param data_spo: файл с данными
    :param end_folder: конечная папка
    :param threshold_base: количество колонок с вводными данными
    :return:
    """
    dct_tests = {'ШТК': (processing_kondash_anxiety, 30), 'ШТБ': (processing_bek, 21),
                 }  # словарь с наименованием теста функцией для его обработки и количеством колонок

    params_df = pd.read_excel(params_spo, dtype=str, usecols='A',
                              header=None)  # считываем какие тесты нужно использовать
    params_df.dropna(inplace=True)  # удаляем пустые строки
    lst_used_test = params_df.iloc[:, 0].tolist()  # получаем список
    lst_used_test = [value for value in lst_used_test if value in dct_tests.keys()]  # отбираем только те что прописаны

    # создаем счетчик обработанных колонок
    threshold_finshed = threshold_base

    # Проверяем датафрейм на количество колонок
    df = pd.read_excel(data_spo, dtype=str)  # считываем датафрейм
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

    # Создаем копию датафрейма с анкетными данными для передачи в функцию
    base_df_for_func = base_df.copy()
    # создаем копию для датафрейма с результатами
    result_df = base_df.copy()

    # Перебираем полученные названия тестов
    for name_test in lst_used_test:
        """
        запускаем функцию хранящуюся в словаре
        передаем туда датафрейм с анкетными данными, датафрейм с данными теста, количество колонок которое занимает данный тест
        получаем 2 датафрейма с результатами для данного теста которые добавляем в основные датафреймы
        """
        # получаем колонки относящиеся к тесту
        temp_df = df.iloc[:, threshold_finshed:threshold_finshed + dct_tests[name_test][1]]
        # обрабатываем и получаем датафреймы для добавления в основные таблицы
        temp_full_df, temp_result_df = dct_tests[name_test][0](base_df_for_func, temp_df,
                                                               dct_tests[name_test][1], name_test)

        base_df = pd.concat([base_df, temp_full_df],
                            axis=1)  # соединяем анкетные данные и вопросы вместе с результатами
        result_df = pd.concat([result_df, temp_result_df], axis=1)
        # увеличиваем предел обозначающий количество обработанных колонок
        threshold_finshed += dct_tests[name_test][1]








if __name__ == '__main__':
    main_params_spo = 'data/параметры для СПО.xlsx'
    main_spo_data = 'data/data.xlsx'
    main_end_folder = 'data/Результат'
    main_quantity_descr_cols = 2

    generate_result_spo(main_params_spo, main_spo_data, main_end_folder, main_quantity_descr_cols)

    print('Lindy Booth')
