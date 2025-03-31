"""
Скрипт для обработки результатов теста Шкала депрессии Цунга
"""
import numpy as np

from lachesis_support_functions import round_mean
import pandas as pd
from tkinter import messagebox


class BadOrderZungDepress(Exception):
    """
    Исключение для обработки случая когда колонки не совпадают
    """
    pass


class BadValueZungDepress(Exception):
    """
    Исключение для неправильных значений в вариантах ответов
    """
    pass

class BadCountColumnsZungDepress(Exception):
    """
    Исключение для обработки случая если количество колонок не равно 20
    """
    pass


def calc_value_zung_depress(row):
    """
    Функция для подсчета значения депрессии Цунга
    :param row: строка с ответами
    :return: число
    """
    value_depress_forward = 0 # счетчик депрессии прямых ответов
    value_depress_reverse = 0 # счетчик депрессии обратных ответов
    lst_forward = [0,2,3,6,7,8,9,12,14,18] # список ответов которые нужно считать простым сложением
    lst_reverse = [1,4,5,10,11,13,15,16,17,19] # обратный подсчет
    for idx, value in enumerate(row):
        if idx in lst_forward:
            value_depress_forward += value
        elif idx in lst_reverse:
            if value == 1:
                value_depress_reverse += 4
            elif value == 2:
                value_depress_reverse += 3
            elif value == 3:
                value_depress_reverse += 2
            elif value == 4:
                value_depress_reverse += 1

    return value_depress_forward + value_depress_reverse





def calc_level_zung_depress(value):
    """
    Функция для подсчета уровня депрессии по шкале Цунга
    :param value:
    :return:
    """
    if 0 <= value <= 50:
        return 'депрессия не выявлена'
    elif 51 <= value <= 59:
        return 'легкая депрессия ситуативного или невротического генеза'
    elif 60 <= value <= 69:
        return 'субдепрессивное состояние или маскированная депрессия'
    else:
        return 'истинное депрессивное состояние'






def processing_zung_depress(base_df: pd.DataFrame, answers_df: pd.DataFrame):
    """
    Функция для обработки результатов
    :param base_df: датафрейм с описательными колонками
    :param answers_df: датафрейм с ответами
    :return: словарь
    """
    try:
        out_answer_df = base_df.copy()  # делаем копию для последующего соединения с сырыми ответами
        if len(answers_df.columns) != 20: # проверяем количество колонок
            raise BadCountColumnsZungDepress

        # Словарь с проверочными данными
        lst_check_cols = ['Я чувствую подавленность, тоску',
                          'Утром я чувствую себя лучше всего',
                          'У меня бывают периоды плача или близости к слезам',
                          'У меня плохой ночной сон',
                          'Аппетит у меня не хуже обычного',
                          'Мне приятно смотреть на привлекательных людей, разговаривать с ними, находиться рядом',
                          'Я замечаю, что теряю вес',
                          'Меня беспокоят запоры',
                          'Сердце бьется быстрее, чем обычно',
                          'Я устаю без всяких причин',
                          'Я мыслю так же ясно, как всегда',
                          'Мне легко делать то, что я умею',
                          'Чувствую беспокойство и не могу усидеть на месте',
                          'У меня есть надежды на будущее',
                          'Я более раздражителен, чем обычно',
                          'Мне легко принимать решения',
                          'Я чувствую, что полезен и необходим',
                          'Я живу достаточно полной жизнью',
                          'Я чувствую, что другим людям станет лучше, если я умру',
                          'Меня до сих пор радует то, что радовало всегда'
                          ]

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
            raise BadOrderZungDepress

        # словарь для замены слов на числа
        dct_replace_value = {'никогда или изредка': 1,
                             'иногда': 2,
                             'часто': 3,
                             'почти всегда или постоянно': 4}

        valid_values = [1, 2,3,4]
        answers_df.replace(dct_replace_value, inplace=True)  # заменяем слова на цифры для подсчетов

        # Проверяем, есть ли значения, отличающиеся от указанных в списке
        mask = ~answers_df.isin(valid_values)

        # Получаем строки с отличающимися значениями
        result_check = answers_df[mask.any(axis=1)]
        if len(result_check) != 0:
            error_row = list(map(lambda x: x + 2, result_check.index))
            error_row = list(map(str, error_row))
            error_message = ';'.join(error_row)
            raise BadValueZungDepress

        # Проводим подсчет
        base_df['Значение_депрессии'] = answers_df.apply(calc_value_zung_depress, axis=1)
        base_df['Значение_нормы'] = '0-50 баллов'
        base_df['Уровень_депрессии'] = base_df['Значение_депрессии'].apply(calc_level_zung_depress)

        # Создаем датафрейм для создания части в общий датафрейм
        part_df = pd.DataFrame(columns=['Значение_депрессии_Цунг','Уровень_депрессии_Цунг'])
        part_df['Значение_депрессии_Цунг'] = base_df['Значение_депрессии']
        part_df['Уровень_депрессии_Цунг'] = base_df['Уровень_депрессии']


        base_df.sort_values(by='Значение_депрессии', ascending=False, inplace=True)  # сортируем

        # Делаем сводную таблицу по курсу
        svod_all_course_df = pd.pivot_table(base_df, index=['Курс'],
                                            values=['Значение_депрессии'],
                                            aggfunc=round_mean)
        svod_all_course_df.reset_index(inplace=True)
        svod_all_course_df['Уровень_депрессии'] = svod_all_course_df['Значение_депрессии'].apply(
            calc_level_zung_depress)  # считаем уровень

        # делаем сводную по курсу
        svod_all_count_course_df = pd.pivot_table(base_df, index=['Курс'],
                                                  columns='Уровень_депрессии',
                                                  values='Значение_депрессии',
                                                  aggfunc='count', margins=True, margins_name='Итого')
        svod_all_count_course_df.reset_index(inplace=True)
        svod_all_count_course_df = svod_all_count_course_df.reindex(
            columns=['Курс', 'депрессия не выявлена', 'легкая депрессия ситуативного или невротического генеза',
                     'субдепрессивное состояние или маскированная депрессия', 'истинное депрессивное состояние',
                     'Итого'])

        svod_all_count_course_df['% депрессия не выявлена  от общего'] = round(
            svod_all_count_course_df['депрессия не выявлена'] / svod_all_count_course_df['Итого'], 2)*100

        svod_all_count_course_df['% легкая депрессия ситуативного или невротического генеза от общего'] = round(
            svod_all_count_course_df['легкая депрессия ситуативного или невротического генеза'] /
            svod_all_count_course_df['Итого'], 2)*100

        svod_all_count_course_df['% субдепрессивное состояние или маскированная депрессия от общего'] = round(
            svod_all_count_course_df['субдепрессивное состояние или маскированная депрессия'] /
            svod_all_count_course_df['Итого'], 2)*100

        svod_all_count_course_df['% истинное депрессивное состояние от общего'] = round(
            svod_all_count_course_df['истинное депрессивное состояние'] / svod_all_count_course_df['Итого'], 2)*100


        # Делаем сводную таблицу средних значений для курса и пола.
        svod_all_course_sex_df = pd.pivot_table(base_df, index=['Курс', 'Пол'],
                                                values=['Значение_депрессии'],
                                                aggfunc=round_mean)
        svod_all_course_sex_df.reset_index(inplace=True)
        svod_all_course_sex_df['Уровень_депрессии'] = svod_all_course_sex_df['Значение_депрессии'].apply(
            calc_level_zung_depress)  # считаем уровень

        # Делаем свод по количеству
        svod_all_count_course_sex_df = pd.pivot_table(base_df, index=['Курс', 'Пол'],
                                                      columns='Уровень_депрессии',
                                                      values='Значение_депрессии',
                                                      aggfunc='count', margins=True, margins_name='Итого')
        svod_all_count_course_sex_df.reset_index(inplace=True)
        svod_all_count_course_sex_df = svod_all_count_course_sex_df.reindex(
            columns=['Группа', 'депрессия не выявлена', 'легкая депрессия ситуативного или невротического генеза',
                     'субдепрессивное состояние или маскированная депрессия', 'истинное депрессивное состояние',
                     'Итого'])

        svod_all_count_course_sex_df['% депрессия не выявлена  от общего'] = round(
            svod_all_count_course_sex_df['депрессия не выявлена'] / svod_all_count_course_sex_df['Итого'], 2)*100

        svod_all_count_course_sex_df['% легкая депрессия ситуативного или невротического генеза от общего'] = round(
            svod_all_count_course_sex_df['легкая депрессия ситуативного или невротического генеза'] /
            svod_all_count_course_sex_df['Итого'], 2)*100

        svod_all_count_course_sex_df['% субдепрессивное состояние или маскированная депрессия от общего'] = round(
            svod_all_count_course_sex_df['субдепрессивное состояние или маскированная депрессия'] /
            svod_all_count_course_sex_df['Итого'], 2)*100

        svod_all_count_course_sex_df['% истинное депрессивное состояние от общего'] = round(
            svod_all_count_course_sex_df['истинное депрессивное состояние'] / svod_all_count_course_sex_df['Итого'], 2)*100


        # Датафрейм для проверки

        out_answer_df = pd.concat([out_answer_df, answers_df], axis=1)


        # Делаем сводную таблицу по группам
        svod_all_group_df = pd.pivot_table(base_df, index=['Группа'],
                                           values=['Значение_депрессии'],
                                           aggfunc=round_mean)
        svod_all_group_df.reset_index(inplace=True)
        svod_all_group_df['Уровень_депрессии'] = svod_all_group_df['Значение_депрессии'].apply(
            calc_level_zung_depress)  # считаем уровень

        # делаем сводную
        svod_all_count_group_df = pd.pivot_table(base_df, index=['Группа'],
                                                 columns='Уровень_депрессии',
                                                 values='Значение_депрессии',
                                                 aggfunc='count', margins=True, margins_name='Итого')
        svod_all_count_group_df.reset_index(inplace=True)

        svod_all_count_group_df = svod_all_count_group_df.reindex(
            columns=['Группа', 'депрессия не выявлена', 'легкая депрессия ситуативного или невротического генеза',
                     'субдепрессивное состояние или маскированная депрессия', 'истинное депрессивное состояние',
                     'Итого'])

        svod_all_count_group_df['% депрессия не выявлена  от общего'] = round(
            svod_all_count_group_df['депрессия не выявлена'] / svod_all_count_group_df['Итого'], 2)*100

        svod_all_count_group_df['% легкая депрессия ситуативного или невротического генеза от общего'] = round(
            svod_all_count_group_df['легкая депрессия ситуативного или невротического генеза'] /
            svod_all_count_group_df['Итого'], 2)*100

        svod_all_count_group_df['% субдепрессивное состояние или маскированная депрессия от общего'] = round(
            svod_all_count_group_df['субдепрессивное состояние или маскированная депрессия'] /
            svod_all_count_group_df['Итого'], 2)*100

        svod_all_count_group_df['% истинное депрессивное состояние от общего'] = round(
            svod_all_count_group_df['истинное депрессивное состояние'] / svod_all_count_group_df['Итого'], 2)*100


        # Делаем сводную таблицу средних значений для группы и пола.
        svod_all_group_sex_df = pd.pivot_table(base_df, index=['Группа', 'Пол'],
                                               values=['Значение_депрессии'],
                                               aggfunc=round_mean)
        svod_all_group_sex_df.reset_index(inplace=True)
        svod_all_group_sex_df['Уровень_депрессии'] = svod_all_group_sex_df['Значение_депрессии'].apply(
            calc_level_zung_depress)  # считаем уровень

        # Делаем свод по количеству для группы и пола
        svod_all_count_group_sex_df = pd.pivot_table(base_df, index=['Группа', 'Пол'],
                                                     columns='Уровень_депрессии',
                                                     values='Значение_депрессии',
                                                     aggfunc='count', margins=True, margins_name='Итого')
        svod_all_count_group_sex_df.reset_index(inplace=True)
        svod_all_count_group_sex_df = svod_all_count_group_sex_df.reindex(
            columns=['Группа', 'Пол', 'депрессия не выявлена', 'легкая депрессия ситуативного или невротического генеза',
                     'субдепрессивное состояние или маскированная депрессия', 'истинное депрессивное состояние',
                     'Итого'])


        svod_all_count_group_sex_df['% депрессия не выявлена  от общего'] = round(
            svod_all_count_group_sex_df['депрессия не выявлена'] / svod_all_count_group_sex_df['Итого'], 2)*100

        svod_all_count_group_sex_df['% легкая депрессия ситуативного или невротического генеза от общего'] = round(
            svod_all_count_group_sex_df['легкая депрессия ситуативного или невротического генеза'] /
            svod_all_count_group_sex_df['Итого'], 2)*100

        svod_all_count_group_sex_df['% субдепрессивное состояние или маскированная депрессия от общего'] = round(
            svod_all_count_group_sex_df['субдепрессивное состояние или маскированная депрессия'] /
            svod_all_count_group_sex_df['Итого'], 2)*100

        svod_all_count_group_sex_df['% истинное депрессивное состояние от общего'] = round(
            svod_all_count_group_sex_df['истинное депрессивное состояние'] / svod_all_count_group_sex_df['Итого'],
            2)*100


        # формируем словарь
        out_dct = {'Списочный результат': base_df, 'Список для проверки': out_answer_df,
                   'Среднее по группам': svod_all_group_df, 'Количество по группам': svod_all_count_group_df,
                   'Среднее по группам и полам': svod_all_group_sex_df,
                   'Количество по группам и полам': svod_all_count_group_sex_df,
                   'Среднее по курсу': svod_all_course_df, 'Количество по курсу': svod_all_count_course_df,
                   'Среднее по курсу и полу': svod_all_course_sex_df,
                   'Количество по курсу и полу': svod_all_count_course_sex_df,

                   }

        return out_dct, part_df

    except BadOrderZungDepress:
        messagebox.showerror('Лахеcис',
                             f'При обработке вопросов теста Шкала депрессии Цунга обнаружены неправильные вопросы. Проверьте названия колонок с вопросами:\n'
                             f'{error_order_message}\n'
                             f'Используйте при создании Яндекс-формы написание вопросов из руководства пользователя программы Лахесис.')
    except BadValueZungDepress:
        messagebox.showerror('Лахеcис',
                             f'При обработке вопросов теста Шкала депрессии Цунга обнаружены неправильные варианты ответов. Проверьте ответы на указанных строках:\n'
                             f'{error_message}\n'
                             f'Используйте при создании Яндекс-формы написание вариантов ответа из руководства пользователя программы Лахесис.')

    except BadCountColumnsZungDepress:
        messagebox.showerror('Лахеcис',
                             f'Проверьте количество колонок с ответами на тест Шкала депрессии Цунга\n'
                             f'Должно быть 20 колонок с вопросами'
                             )




