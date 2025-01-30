"""
Скрипт для обработки тестов студентов СПО
"""
from spo_kondash_anxiety import processing_kondash_anxiety # функция для обработки результатов теста тревожности Кондаша
from bek_depress import processing_bek_depress # функция для обработки результатов теста тревожности Кондаша
from lachesis_support_functions import write_df_to_excel, del_sheet # функции для создания итогового файла

import pandas as pd
pd.options.mode.copy_on_write = True
import openpyxl
from tkinter import messagebox
import re
import time


class NotSameSize(Exception):
    """
    Исключение для проверки совпадают ли размеры таблицы с количеством колонок требуемых для выполнения тестов указанных в параметрах
    """
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
    try:
        # генерируем текущее время
        t = time.localtime()
        current_time = time.strftime('%H_%M_%S', t)

        dct_tests = {'ШТК': (processing_kondash_anxiety, 30), 'ШДБ': (processing_bek_depress, 52),
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

        # если есть колонка с группой
        if 'Введите_свою_группу' in base_df.columns:
            base_df['Введите_свою_группу'] = base_df['Введите_свою_группу'].astype(str) # приводим к строковому формату
            base_df['Введите_свою_группу'] = base_df['Введите_свою_группу'].apply(str.upper) # делаем заглавными
            # очищаем от лишних пробелов
            base_df['Введите_свою_группу'] = base_df['Введите_свою_группу'].apply(lambda x:re.sub(r'\s+',' ',x))


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
            temp_base_df = base_df.copy()

            # получаем колонки относящиеся к тесту
            temp_df = df.iloc[:, threshold_finshed:threshold_finshed + dct_tests[name_test][1]]
            # обрабатываем и получаем датафреймы для добавления в основные таблицы
            temp_dct = dct_tests[name_test][0](temp_base_df, temp_df
                                                                  )

            base_df_for_func = pd.concat([base_df_for_func, temp_dct['Списочный результат']],
                                axis=1)  # соединяем анкетные данные и вопросы вместе с результатами
            result_df = pd.concat([result_df, temp_dct['Список для проверки']], axis=1)
            # Сохраняем в удобном виде
            temp_wb = write_df_to_excel(temp_dct, write_index=False)
            temp_wb = del_sheet(temp_wb, ['Sheet', 'Sheet1', 'Для подсчета'])
            temp_wb.save(f'{end_folder}/Результат {name_test}.xlsx')


            # увеличиваем предел обозначающий количество обработанных колонок
            threshold_finshed += dct_tests[name_test][1]

    except FileNotFoundError:
        messagebox.showerror('Лахеcис',
                                 f'Перенесите файлы которые вы хотите обработать или конечную папку в корень диска. Проблема может быть\n '
                                 f'в слишком длинном пути к обрабатываемым файлам')
    else:
        messagebox.showinfo('Лахеcис',
                                'Данные успешно обработаны')


if __name__ == '__main__':
    main_params_spo = 'data/параметры для СПО.xlsx'
    main_spo_data = 'data/data.xlsx'
    main_end_folder = 'data/Результат'
    main_quantity_descr_cols = 4

    generate_result_spo(main_params_spo, main_spo_data, main_end_folder, main_quantity_descr_cols)

    print('Lindy Booth')
