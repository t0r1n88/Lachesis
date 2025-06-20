"""
Скрипт для обработки тестов для взрослых
"""
# Тесты Профессиональное выгорание
from prof_burnout.vodopyanova_prof_burnout import processing_vod_prof_burnout # Профессиональное выгорание Водопьянова
from prof_burnout.boiko_emotional_burnout import processing_boiko_emotional_burnout # Эмоциональное выгорание Бойко
from prof_burnout.kapponi_burnout import processing_kapponi_burnout # Выгорание Каппони Новак

from lachesis_support_functions import write_df_to_excel, del_sheet, count_attention # функции для создания итогового файла

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

class NotCorrectParamsTests(Exception):
    """
    Исключение для проверки есть ли хотя бы один реализованный тест
    """
    pass

class NotCorrectSvodCols(Exception):
    """
    Исключение для проверки корректности строки с колонками по которым нужно сделать свод
    """
    pass

class BadSvodCols(Exception):
    """
    Исключение для проверки правильности введенной строки с перечислением колонок по которым нужно сделать свод
    """
    pass


def check_svod_cols(df:pd.DataFrame,str_svod_cols:str,threshold:int):
    """
    Фцнкция для проверки корректности
    :param df: датафрейм с анкетными данными
    :param str_svod_cols: строка с порядоквыми номерами
    :param threshold: количество колонок в анкетной части
    :return: список
    """
    try:
        result = re.findall(r'\d+',str_svod_cols)
        if result:
            if len(result) == 1:
                value = int(result[0])
                if value > threshold:
                    raise NotCorrectSvodCols
                elif value == 0:
                    raise NotCorrectSvodCols
                else:
                    return [df.columns[value-1]]
            elif len(result) == 2:
                for idx,value in enumerate(result):
                    value = int(value)
                    if value > threshold:
                        raise NotCorrectSvodCols
                    elif value == 0:
                        raise NotCorrectSvodCols
                    else:
                        result[idx] = df.columns[value-1]
                return result
            else:
                raise NotCorrectSvodCols

        else:
            return []
    except:
        raise NotCorrectSvodCols



def generate_result_adults(params_adults: str, data_adults: str, end_folder: str, threshold_base: int,svod_cols:str):
    """
    Функция для генерации результатов комплексного теста для взрослых
    :param params_adults: какие тесты используются и в каком порядке
    :param data_adults: файл с данными
    :param end_folder: конечная папка
    :param threshold_base: количество колонок с вводными данными
    :param svod_cols: строка с перечислением колонок по которым нужно сделать свод
    :return:
    """
    try:
        # генерируем текущее время
        t = time.localtime()
        current_time = time.strftime('%H_%M_%S', t)

        dct_tests = {'Профессиональное выгорание педагогов Водопьянова': (processing_vod_prof_burnout, 22),
                     'Эмоциональное выгорание Бойко Ильин': (processing_boiko_emotional_burnout, 35),
                     'Выгорание Каппони Новак': (processing_kapponi_burnout, 10),
                     }  # словарь с наименованием теста функцией для его обработки и количеством колонок

        dct_out_name_tests = {'Профессиональное выгорание педагогов Водопьянова': 'Профессиональное выгорание педагогов Водопьянова',
                              'Эмоциональное выгорание Бойко Ильин': 'Эмоциональное выгорание Бойко Ильин',
                              'Выгорание Каппони Новак': 'Экспресс-оценка выгорания Каппони Новак',
                              }  # словарь с наименованием теста функцией для его обработки и количеством колонок

        # Списки для проверки, чтобы листы Особое внимание и зона риска создавались только если в параметрах указаны эти тесты
        lst_alert_tests = ['Профессиональное выгорание педагогов Водопьянова','Эмоциональное выгорание Бойко Ильин',
                           'Выгорание Каппони Новак']
        lst_check_alert_tests = []

        # Списки для проверки наличия профориентационных тестов
        lst_career_tests = ['ЦОК','ПТЛ','СПП','ДДО','Профессиональная идентичность Азбель','Карта интересов Голомшток Азбель',
                            'Характер и профессия Резапкина','СИТТ Азбель','НТФП Грецов','Профессиональные установки подростков Андреева','НВИД Годлиник']
        lst_check_career_tests = []


        params_df = pd.read_excel(params_adults, dtype=str, usecols='A',
                                  header=None)  # считываем какие тесты нужно использовать
        params_df.dropna(inplace=True)  # удаляем пустые строки
        lst_used_test = params_df.iloc[:, 0].tolist()  # получаем список
        lst_used_test = [value for value in lst_used_test if value in dct_tests.keys()]  # отбираем только те что прописаны

        if len(lst_used_test) == 0:
            raise NotCorrectParamsTests

        # создаем счетчик обработанных колонок
        threshold_finshed = threshold_base

        # Проверяем датафрейм на количество колонок
        df = pd.read_excel(data_adults, dtype=str)  # считываем датафрейм
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

        # проверяем и обрабатываем строку с колонками по которым нужно делать свод
        lst_svod_cols = check_svod_cols(base_df,svod_cols,threshold_base)

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
            # Присутствует ли тест среди тестов на где нужно выделять опасные состояния
            if name_test in lst_alert_tests:
                lst_check_alert_tests.append(name_test)

            # Присутствует ли тест среди профориентационных тестов
            if name_test in lst_career_tests:
                lst_check_career_tests.append(name_test)

            temp_base_df = base_df.copy()

            # получаем колонки относящиеся к тесту
            temp_df = df.iloc[:, threshold_finshed:threshold_finshed + dct_tests[name_test][1]]
            # обрабатываем и получаем датафреймы для добавления в основные таблицы
            temp_dct,temp_itog_df = dct_tests[name_test][0](temp_base_df, temp_df,lst_svod_cols)

            base_df_for_func = pd.concat([base_df_for_func, temp_dct['Списочный результат']],
                                axis=1)  # соединяем анкетные данные и вопросы вместе с результатами
            result_df = pd.concat([result_df, temp_dct['Список для проверки']], axis=1)

            # Добавляем в итоговый свод
            main_itog_df = pd.concat([main_itog_df,temp_itog_df],axis=1)

            # Сохраняем в зависимости от типа теста. Если профориентационный то сохраняем через pandas,
            # чтобы текст в колонке Описание результата не обрезался
            if name_test in lst_check_career_tests:
                with pd.ExcelWriter(f'{end_folder}/{dct_out_name_tests[name_test]}.xlsx', engine='xlsxwriter') as writer:
                    for sheet_name, dataframe in temp_dct.items():
                        dataframe.to_excel(writer, sheet_name=sheet_name,index=False)
            else:
                temp_wb = write_df_to_excel(temp_dct, write_index=False)
                temp_wb = del_sheet(temp_wb, ['Sheet', 'Sheet1', 'Для подсчета'])
                temp_wb.save(f'{end_folder}/{dct_out_name_tests[name_test]}.xlsx')


            # увеличиваем предел обозначающий количество обработанных колонок
            threshold_finshed += dct_tests[name_test][1]

        # Сохраняем в удобном виде
        if len(lst_check_alert_tests) != 0:
            # Отбираем тех кто требует внимания.
            set_alert_value = ['высокий уровень выгорания','имеется выгорание','критический уровень выгорания'] # особое внимание
            set_attention_value = ['пограничное выгорание','симптомы выгорания','начинающееся выгорание','средний уровень выгорания'] # обратить внимание

            alert_df = main_itog_df[main_itog_df.isin(set_alert_value).any(axis=1)] # фильтруем требующих особого внимания
            attention_df = main_itog_df[~main_itog_df.isin(set_alert_value).any(axis=1)] # получаем оставшихся
            attention_df = attention_df[attention_df.apply(lambda x:count_attention(x,set_attention_value),axis=1)]

            # # Создаем сводную таблицу по группам
            # svod_group_df = main_itog_df.groupby(by='Группа').agg({'Пол':'count'}).rename(columns={'Пол':'Количество прошедших'})
            # svod_group_df = svod_group_df.reset_index()
            # Сохраняем в зависимости от количества сводных колонок
            if len(lst_svod_cols) == 0:
                temp_wb = write_df_to_excel({'Свод по всем тестам':main_itog_df,'Особое внимание':alert_df,'Зона риска':attention_df}, write_index=False)
                temp_wb = del_sheet(temp_wb, ['Sheet', 'Sheet1', 'Для подсчета'])
                temp_wb.save(f'{end_folder}/Общий результат.xlsx')

            elif len(lst_svod_cols) == 1:
                main_itog_df.sort_values(by=lst_svod_cols[0], inplace=True)  # сортируем
                svod_one_df = main_itog_df.groupby(by=lst_svod_cols[0]).agg({main_itog_df.columns[-1]:'count'}).rename(columns={main_itog_df.columns[-1]:'Количество прошедших тестирование'})
                svod_one_df = svod_one_df.reset_index()
                svod_one_df.sort_values(by='Количество прошедших тестирование',ascending=False,inplace=True)

                # очищаем название колонки по которой делали свод
                name_one = lst_svod_cols[0]
                name_one = re.sub(r'[\[\]\'+()<> :"?*|\\/]', '_', name_one)
                name_one = name_one[:20]

                temp_wb = write_df_to_excel({'Свод по всем тестам':main_itog_df,'Особое внимание':alert_df,'Зона риска':attention_df,
                                             name_one:svod_one_df}, write_index=False)
                temp_wb = del_sheet(temp_wb, ['Sheet', 'Sheet1', 'Для подсчета'])
                temp_wb.save(f'{end_folder}/Общий результат.xlsx')

            elif len(lst_svod_cols) == 2:
                main_itog_df.sort_values(by=lst_svod_cols[0], inplace=True)  # сортируем
                svod_one_df = main_itog_df.groupby(by=lst_svod_cols[0]).agg({main_itog_df.columns[-1]:'count'}).rename(columns={main_itog_df.columns[-1]:'Количество прошедших тестирование'})
                svod_one_df = svod_one_df.reset_index()
                svod_one_df.sort_values(by='Количество прошедших тестирование',ascending=False,inplace=True)

                # очищаем название колонки по которой делали свод
                name_one = lst_svod_cols[0]
                name_one = re.sub(r'[\[\]\'+()<> :"?*|\\/]', '_', name_one)
                name_one = name_one[:20]

                # Делаем по второй колонке
                svod_two_df = main_itog_df.groupby(by=lst_svod_cols[1]).agg({main_itog_df.columns[-1]: 'count'}).rename(
                    columns={main_itog_df.columns[-1]: 'Количество прошедших тестирование'})
                svod_two_df = svod_two_df.reset_index()
                svod_two_df.sort_values(by='Количество прошедших тестирование', ascending=False, inplace=True)

                # очищаем название колонки по которой делали свод
                name_two = lst_svod_cols[1]
                name_two = re.sub(r'[\[\]\'+()<> :"?*|\\/]', '_', name_two)
                name_two = name_two[:20]

                all_svod_df = pd.pivot_table(data=main_itog_df,
                                             index=lst_svod_cols,
                                             values=main_itog_df.columns[-1],
                                             aggfunc='count',
                                             )

                all_svod_df = all_svod_df.reset_index()
                all_svod_df.rename(columns={main_itog_df.columns[-1]: 'Количество прошедших тестирование'},inplace=True)

                temp_wb = write_df_to_excel(
                    {'Свод по всем тестам': main_itog_df, 'Особое внимание': alert_df, 'Зона риска': attention_df,
                     name_one: svod_one_df,name_two:svod_two_df,f'{name_one[:12]}_{name_two[:12]}':all_svod_df}, write_index=False)
                temp_wb = del_sheet(temp_wb, ['Sheet', 'Sheet1', 'Для подсчета'])
                temp_wb.save(f'{end_folder}/Общий результат.xlsx')

        else:
            # Если есть профориентационные тесты, то сохраняем через пандас
            if len(lst_check_career_tests) != 0:

                with pd.ExcelWriter(f'{end_folder}/Общий результат.xlsx', engine='xlsxwriter') as writer:
                    for sheet_name, dataframe in {'Свод по всем тестам': main_itog_df}:
                        dataframe.to_excel(writer, sheet_name=sheet_name,index=False)
            else:
                temp_wb = write_df_to_excel(
                    {'Свод по всем тестам': main_itog_df,
                     }, write_index=False)
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
    except NotSameSize:
        messagebox.showerror('Лахеcис',
                                 f'Не совпадает количество колонок с ответами на тесты с эталонным количеством. В файле {df.shape[1]} колонок а должно быть {check_size_df+threshold_base}.')
    except NotCorrectParamsTests:
        messagebox.showerror('Лахеcис',
                                 f'В файле с параметрами тестирования (в котором вы указали использованные тесты) не найдено ни одного правильного названия теста.\nПроверьте написание названий тестов.')

    except NotCorrectSvodCols:
        messagebox.showerror('Лахеcис',
                                 f'Проверьте правильность написания порядковых номеров колонок по которым вы хотите сделать свод.\nПравильный формат это не более двух чисел разделенных запятой, начиная с цифры 1, '
                                 f'например 1,3 или 2 а если вам не нужны своды то оставьте это поле пустым.\n'
                                 f'Проверьте числа которые вы указали потому что, порядковый номер колонки не может превышать количество колонок в анкетной части вашего файла с ответами на тест.')
    else:
        messagebox.showinfo('Лахеcис',
                                'Данные успешно обработаны')


if __name__ == '__main__':
    main_params_adults = 'c:/Users/1/PycharmProjects/Lachesis/data/параметры Выгорание.xlsx'

    main_adults_data = 'c:/Users/1/PycharmProjects/Lachesis/data/Профессионально выгорание.xlsx'


    main_end_folder = 'c:/Users/1/PycharmProjects/Lachesis/data/Результат'
    main_quantity_descr_cols = 3
    main_svod_cols = ''

    generate_result_adults(main_params_adults, main_adults_data, main_end_folder, main_quantity_descr_cols,main_svod_cols)

    print('Lindy Booth')
