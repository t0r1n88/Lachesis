"""
Скрипт для обработки тестов студентов СПО
"""
# Тесты тревожность и безнадежность
from spo.spo_kondash_anxiety import processing_kondash_anxiety # функция для обработки результатов теста тревожности Кондаша
from spo.bek_depress import processing_bek_depress # функция для обработки результатов теста депрессии Бека
from spo.bek_hopelessness import processing_bek_hopelessness # функция для обработки результатов теста безнадежности Бека
from spo.zung_depress import processing_zung_depress # функция для обработки результатов теста депрессии Цунга
from spo.voz_well_being import processing_voz_well_being # функция для обработки результатов теста общего самочувствия ВОЗ 1999

# Лидерство, самооценка, эмоциональный интеллект
from spo_leadership.ei import processing_ei # эмоциональный интеллект
from spo_leadership.kos_one import processing_kos # коммуникативные и организаторские способности Федоришин
from spo_leadership.usk import processing_usk # уровень самооценки Ковалев



from lachesis_support_functions import write_df_to_excel, del_sheet, convert_to_int,count_attention # функции для создания итогового файла

import pandas as pd
pd.options.mode.chained_assignment = None
from tkinter import messagebox
import re
import time


class NotSameSize(Exception):
    """
    Исключение для проверки совпадают ли размеры таблицы с количеством колонок требуемых для выполнения тестов указанных в параметрах
    """
    pass

class NotRequiredColumns(Exception):
    """
    Исключение для проверки есть ли колонки Курс, Группа, Пол в файле с ответами
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

        dct_tests = {'Шкала тревожности Кондаша': (processing_kondash_anxiety, 30), 'Шкала депрессии Бека': (processing_bek_depress, 52),
                     'Шкала безнадежности Бека':(processing_bek_hopelessness,20),
                     'Шкала депрессии Цунга':(processing_zung_depress,20),
                     'Индекс общего самочувствия ВОЗ 1999':(processing_voz_well_being,5),
                     'Эмоциональный интеллект Люсин':(processing_ei,46),
                     'КОС-1':(processing_kos,40),
                     'Уровень самооценки Ковалев':(processing_usk,32)
                     }  # словарь с наименованием теста функцией для его обработки и количеством колонок

        dct_out_name_tests = {'Шкала тревожности Кондаша': 'Шкала тревожности Кондаша', 'Шкала депрессии Бека':'Шкала депрессии Бека',
                     'Шкала безнадежности Бека': 'Шкала безнадежности Бека',
                              'Шкала депрессии Цунга': 'Шкала депрессии Цунга',
                              'Индекс общего самочувствия ВОЗ 1999':'Индекс общего самочувствия ВОЗ 1999',
                              'Эмоциональный интеллект Люсин':'Эмоциональный интеллект Люсин',
                              'КОС-1':'КОС-1 Оценка коммуникативных и организаторских способностей',
                              'Уровень самооценки Ковалев':'Уровень самооценки Ковалев'
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

        # Проверяем наличие колонок Курс, Пол, Группа
        check_cols_set = {'Курс','Пол','Группа'} # Множество для проверки
        diff_cols = check_cols_set.difference(set(base_df.columns))
        if len(diff_cols) !=0 :
            raise NotRequiredColumns

        # заменяем пробелы на нижнее подчеркивание и очищаем от пробельных символов в начале и конце
        base_df.columns = [column.strip().replace(' ', '_') for column in base_df.columns]

        # очищаем от всех символов кроме букв цифр
        base_df.columns = [re.sub(r'[^_\d\w]', '', column) for column in base_df.columns]

        # если есть колонка с группой
        if 'Группа' in base_df.columns:
            base_df['Группа'] = base_df['Группа'].astype(str) # приводим к строковому формату
            base_df['Группа'] = base_df['Группа'].apply(str.upper) # делаем заглавными
            # очищаем от лишних пробелов
            base_df['Группа'] = base_df['Группа'].apply(lambda x:re.sub(r'\s+',' ',x))

        base_df['Курс'] = base_df['Курс'].apply(convert_to_int) # приводим курс к инту


        # Создаем копию датафрейма с анкетными данными для передачи в функцию
        base_df_for_func = base_df.copy()
        # Создаем копию анкетных данных для создания свода по всем тестам
        main_itog_df = base_df.copy()

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
            temp_dct,temp_itog_df = dct_tests[name_test][0](temp_base_df, temp_df)

            base_df_for_func = pd.concat([base_df_for_func, temp_dct['Списочный результат']],
                                axis=1)  # соединяем анкетные данные и вопросы вместе с результатами
            result_df = pd.concat([result_df, temp_dct['Список для проверки']], axis=1)

            # Добавляем в итоговый свод
            main_itog_df = pd.concat([main_itog_df,temp_itog_df],axis=1)


            # Сохраняем в удобном виде
            temp_wb = write_df_to_excel(temp_dct, write_index=False)
            temp_wb = del_sheet(temp_wb, ['Sheet', 'Sheet1', 'Для подсчета'])
            temp_wb.save(f'{end_folder}/{dct_out_name_tests[name_test]}.xlsx')


            # увеличиваем предел обозначающий количество обработанных колонок
            threshold_finshed += dct_tests[name_test][1]

        # Сохраняем в удобном виде
        main_itog_df.sort_values(by='Группа',inplace=True) # сортируем
        # Отбираем тех кто требует внимания.
        set_alert_value = ['тяжелая депрессия','безнадежность тяжёлая','Очень высокий уровень тревожности','истинное депрессивное состояние'] # особое внимание
        set_attention_value = ['умеренная депрессия','безнадежность умеренная','Высокий уровень тревожности','субдепрессивное состояние или маскированная депрессия'] # обратить внимание

        alert_df = main_itog_df[main_itog_df.isin(set_alert_value).any(axis=1)] # фильтруем требующих особого внимания
        attention_df = main_itog_df[~main_itog_df.isin(set_alert_value).any(axis=1)] # получаем оставшихся
        attention_df = attention_df[attention_df.apply(lambda x:count_attention(x,set_attention_value),axis=1)]

        # Создаем сводную таблицу по группам
        svod_group_df = main_itog_df.groupby(by='Группа').agg({'ФИО':'count'}).rename(columns={'ФИО':'Количество прошедших'})
        svod_group_df = svod_group_df.reset_index()

        temp_wb = write_df_to_excel({'Свод по всем тестам':main_itog_df,'Особое внимание':alert_df,'Зона риска':attention_df,'Свод по группам':svod_group_df}, write_index=False)
        temp_wb = del_sheet(temp_wb, ['Sheet', 'Sheet1', 'Для подсчета'])
        temp_wb.save(f'{end_folder}/Общий результат.xlsx')

    except FileNotFoundError:
        messagebox.showerror('Лахеcис',
                                 f'Перенесите файлы которые вы хотите обработать или конечную папку в корень диска. Проблема может быть\n '
                                 f'в слишком длинном пути к обрабатываемым файлам')
    except PermissionError:
        messagebox.showerror('Лахеcис',
                                 f'Закройте все файлы созданные программой Лахесис и запустите повторно обработку'
                                 )
    except NotRequiredColumns:
        messagebox.showerror('Лахеcис',
                                 f'Проверьте наличие колонок с названием: Курс, Пол, Группа. В файле с ответами не хватает колонок: {diff_cols}'
                                 )
    except NotSameSize:
        messagebox.showerror('Лахеcис',
                                 f'Не совпадает количество колонок с ответами на тесты с эталонным количеством. В файле {df.shape[1]} колонок а должно быть {check_size_df+threshold_base}.')
    else:
        messagebox.showinfo('Лахеcис',
                                'Данные успешно обработаны')


if __name__ == '__main__':
    main_params_spo = 'c:/Users/1/PycharmProjects/Lachesis/data/параметры для СПО.xlsx'
    main_params_spo = 'c:/Users/1/PycharmProjects/Lachesis/data/параметры лидерство.xlsx'
    main_spo_data = 'c:/Users/1/PycharmProjects/Lachesis/data/data.xlsx'
    main_end_folder = 'c:/Users/1/PycharmProjects/Lachesis/data/Результат'
    main_quantity_descr_cols = 4

    generate_result_spo(main_params_spo, main_spo_data, main_end_folder, main_quantity_descr_cols)

    print('Lindy Booth')
