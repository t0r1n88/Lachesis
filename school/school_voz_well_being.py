"""
Скрипт для обработки результатов теста общего самочувствия ВОЗ 1999 для школьников
"""
from lachesis_support_functions import round_mean, sort_name_class
import pandas as pd
from tkinter import messagebox


class BadOrderVozWellBeing(Exception):
    """
    Исключение для обработки случая когда колонки не совпадают
    """
    pass


class BadValueVozWellBeing(Exception):
    """
    Исключение для неправильных значений в вариантах ответов
    """
    pass


class BadCountColumnsVozWellBeing(Exception):
    """
    Исключение для обработки случая если количество колонок не равно 5
    """
    pass


def calc_value_voz_well_being(row):
    """
    Функция для подсчета значения индекса общего самочувствия ВОЗ 1999
    :param row: строка с ответами
    :return: число
    """
    sum_row = sum(row) # получаем сумму
    return sum_row * 4





def processing_voz_well_being(base_df: pd.DataFrame, answers_df: pd.DataFrame):
    """
    Функция для обработки результатов
    :param base_df: датафрейм с описательными колонками
    :param answers_df: датафрейм с ответами
    :return: словарь
    """
    try:
        out_answer_df = base_df.copy()  # делаем копию для последующего соединения с сырыми ответами
        if len(answers_df.columns) != 5: # проверяем количество колонок
            raise BadCountColumnsVozWellBeing

        # Словарь с проверочными данными
        lst_check_cols = ['Я чувствую себя бодрой(-ым) и в хорошем настроении',
                          'Я чувствую себя спокойной(-ым) и раскованной(-ым)',
                          'Я чувствую себя активной(-ым) и энергичной(-ым)',
                          'Я просыпаюсь и чувствую себя свежей(-им) и отдохнувшей(-им)',
                          'Каждый день со мной происходят вещи, представляющие для меня интерес']

        # Проверяем порядок колонок
        order_main_columns = lst_check_cols  # порядок колонок и названий как должно быть
        order_temp_df_columns = list(answers_df.columns)  # порядок колонок проверяемого файла
        error_order_lst = []  # список для несовпадающих пар
        # Сравниваем попарно колонки
        for main, temp in zip(order_main_columns, order_temp_df_columns):
            if main != temp:
                error_order_lst.append(f'На месте колонки {main} находится колонка {temp}')
                error_order_message = ';'.join(error_order_lst)
        if len(error_order_lst) != 0:
            raise BadOrderVozWellBeing

        # словарь для замены слов на числа
        dct_replace_value = {'Никогда': 0,
                             'Некоторое время': 1,
                             'Менее половины времени': 2,
                             'Более половины времени': 3,
                             'Большую часть времени': 4,
                             'Все время': 5,
                             }

        valid_values = [0, 1, 2,3,4, 5]
        answers_df.replace(dct_replace_value, inplace=True)  # заменяем слова на цифры для подсчетов

        # Проверяем, есть ли значения, отличающиеся от указанных в списке
        mask = ~answers_df.isin(valid_values)

        # Получаем строки с отличающимися значениями
        result_check = answers_df[mask.any(axis=1)]
        if len(result_check) != 0:
            error_row = list(map(lambda x: x + 2, result_check.index))
            error_row = list(map(str, error_row))
            error_message = ';'.join(error_row)
            raise BadValueVozWellBeing

        # Проводим подсчет
        base_df['Значение_общего_самочувствия'] = answers_df.apply(calc_value_voz_well_being, axis=1)
        # Создаем датафрейм для создания части в общий датафрейм
        part_df = pd.DataFrame(columns=['Индекс_общего_самочувствия_ВОЗ'])
        part_df['Индекс_общего_самочувствия_ВОЗ'] = base_df['Значение_общего_самочувствия']


        base_df.sort_values(by='Значение_общего_самочувствия', ascending=False, inplace=True)  # сортируем

        # Делаем сводную таблицу по Номер_классау
        svod_all_course_df = pd.pivot_table(base_df, index=['Номер_класса'],
                                            values=['Значение_общего_самочувствия'],
                                            aggfunc=round_mean)
        svod_all_course_df.reset_index(inplace=True)

        # Делаем сводную таблицу средних значений для Номер_классаа и пола.
        svod_all_course_sex_df = pd.pivot_table(base_df, index=['Номер_класса', 'Пол'],
                                                values=['Значение_общего_самочувствия'],
                                                aggfunc=round_mean)
        svod_all_course_sex_df.reset_index(inplace=True)

        # Датафрейм для проверки

        out_answer_df = pd.concat([out_answer_df, answers_df], axis=1)
        svod_all_group_df = pd.pivot_table(base_df, index=['Класс'],
                                           values=['Значение_общего_самочувствия'],
                                           aggfunc=round_mean)
        svod_all_group_df.reset_index(inplace=True)
        svod_all_group_df.sort_values(by='Класс', key=lambda x: x.map(sort_name_class), inplace=True)  # сортируем

        # Делаем сводную таблицу средних значений для группы и пола.
        svod_all_group_sex_df = pd.pivot_table(base_df, index=['Класс', 'Пол'],
                                               values=['Значение_общего_самочувствия'],
                                               aggfunc=round_mean)
        svod_all_group_sex_df.reset_index(inplace=True)
        svod_all_group_sex_df.sort_values(by='Класс', key=lambda x: x.map(sort_name_class), inplace=True)  # сортируем

        # формируем словарь
        out_dct = {'Списочный результат': base_df, 'Список для проверки': out_answer_df,
                   'Среднее по Классам': svod_all_group_df, 'Среднее Класс Пол': svod_all_group_sex_df,
                   'Среднее по Номер_класса': svod_all_course_df,'Среднее Номер_класса Пол': svod_all_course_sex_df

                  }

        return out_dct,part_df
    except BadOrderVozWellBeing:
        messagebox.showerror('Лахеcис',
                             f'При обработке вопросов теста Индекс общего самочувствия ВОЗ 1999 обнаружены неправильные вопросы. Проверьте названия колонок с вопросами:\n'
                             f'{error_order_message}\n'
                             f'Используйте при создании Яндекс-формы написание вопросов из руководства пользователя программы Лахесис.')
    except BadValueVozWellBeing:
        messagebox.showerror('Лахеcис',
                             f'При обработке вопросов теста Индекс общего самочувствия ВОЗ 1999 обнаружены неправильные варианты ответов. Проверьте ответы на указанных строках:\n'
                             f'{error_message}\n'
                             f'Используйте при создании Яндекс-формы написание вариантов ответа из руководства пользователя программы Лахесис.')

    except BadCountColumnsVozWellBeing:
        messagebox.showerror('Лахеcис',
                             f'Проверьте количество колонок с ответами на тест Индекс общего самочувствия ВОЗ 1999\n'
                             f'Должно быть 5 колонок с вопросами'
                             )


