"""
Точка входа для обработки выбранных профориентационных тестов
"""
from school_career_guidance.ddo import processing_ddo # Дифференциально-диагностический опросник
from school_career_guidance.cok import processing_cok # Ценностные ориентации в карьере
from school_career_guidance.ptl import processing_ptl # Профессиональный тип личности
from school_career_guidance.spp import processing_spp # Сфера профессиональных предпочтений

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
                                                                       dct_tests[name_test][1], name_test,threshold_base,end_folder)
        base_df = pd.concat([base_df, temp_full_df],
                            axis=1)  # соединяем анкетные данные и вопросы вместе с результатами
        result_df = pd.concat([result_df, temp_result_df], axis=1)
        # увеличиваем предел обозначающий количество обработанных колонок
        threshold_finshed += dct_tests[name_test][1]

    # Сохраняем результаты
    base_df.to_excel(
        f'{end_folder}/Полная таблица.xlsx',
        index=False,
        engine='xlsxwriter')

    result_df.to_excel(
        f'{end_folder}/Краткая таблица.xlsx',
        index=False,
        engine='xlsxwriter')





if __name__ == '__main__':
    main_params_career = 'c:/Users/1/PycharmProjects/Lachesis/data/параметры  СППУ ДДО.xlsx'
    main_params_career = 'c:/Users/1/PycharmProjects/Lachesis/data/параметры ДЦОК ОПТЛ СППУ ДДО.xlsx'
    main_career_data = 'c:/Users/1/PycharmProjects/Lachesis/data/data career.xlsx'
    main_career_data = 'c:/Users/1/PycharmProjects/Lachesis/data/Яндекс Форма с ответами школьников.xlsx'
    main_end_folder = 'c:/Users/1/PycharmProjects/Lachesis/data/Результат'
    main_quantity_descr_cols = 6

    generate_result_career_guidance(main_params_career, main_career_data, main_end_folder, main_quantity_descr_cols)

    print('Lindy Booth')