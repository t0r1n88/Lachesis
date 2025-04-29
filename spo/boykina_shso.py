"""
Скрипт для обработки результатов теста Шкала субъективного остракизма Бойкина
"""
import pandas as pd
from tkinter import messagebox
from lachesis_support_functions import round_mean,sort_name_class

class BadOrderSHSO(Exception):
    """
    Исключение для обработки случая когда колонки не совпадают
    """
    pass


class BadValueSHSO(Exception):
    """
    Исключение для неправильных значений в вариантах ответов
    """
    pass

class BadCountColumnsSHSO(Exception):
    """
    Исключение для обработки случая если количество колонок не равно 14
    """
    pass


def calc_sub_value_ig(row):
    """
    Функция для подсчета значения субшкалы Игнорирование
    :param row: строка с ответами
    :return: число
    """
    lst_pr = [1, 2, 4, 7, 10]

    value_forward = 0 # счетчик прямых ответов
    value_reverse = 0 # счетчик обратных ответов
    lst_forward = [1, 2, 4,7, 10]  # список ответов которые нужно считать простым сложением
    lst_reverse = [] # обратный подсчет

    for idx, value in enumerate(row):
        if idx +1 in lst_pr:
            if idx + 1 in lst_forward:
                # print(f'Прямой подсчет {idx +1}') # Для проверки корректности
                value_forward += value
            elif idx +1 in lst_reverse:
                # print(f'Обратный подсчет {idx +1}')# Для проверки корректности
                if value == 5:
                    value_reverse += 1
                elif value == 4:
                    value_reverse += 2
                elif value == 3:
                    value_reverse += 3
                elif value == 2:
                    value_reverse += 4
                elif value == 1:
                    value_reverse += 5

    return round((value_forward + value_reverse) /5,1)

def calc_level_sub_ig(value):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """
    if 1 <= value <= 1.3:
        return 'низкий уровень социального остракизма'
    elif 1.4 <= value <= 2:
        return 'средний уровень социального остракизма'
    elif 2.1 <= value <= 5:
        return 'высокий уровень социального остракизма'



def calc_sub_value_isk(row):
    """
    Функция для подсчета значения субшкалы Исключение
    :return: число
    """
    lst_pr = [5, 8, 9, 12, 13]

    value_forward = 0 # счетчик прямых ответов
    value_reverse = 0 # счетчик обратных ответов
    lst_forward = []  # список ответов которые нужно считать простым сложением
    lst_reverse = [5, 8, 9, 12, 13] # обратный подсчет

    for idx, value in enumerate(row):
        if idx +1 in lst_pr:
            if idx + 1 in lst_forward:
                # print(f'Прямой подсчет {idx +1}') # Для проверки корректности
                value_forward += value
            elif idx +1 in lst_reverse:
                # print(f'Обратный подсчет {idx +1}')# Для проверки корректности
                if value == 5:
                    value_reverse += 1
                elif value == 4:
                    value_reverse += 2
                elif value == 3:
                    value_reverse += 3
                elif value == 2:
                    value_reverse += 4
                elif value == 1:
                    value_reverse += 5

    return round((value_forward + value_reverse) /5,1)

def calc_level_sub_isk(value):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """
    if 1 <= value <= 2.3:
        return 'низкий уровень социального остракизма'
    elif 2.4 <= value <= 3.4:
        return 'средний уровень социального остракизма'
    elif 3.5 <= value <= 5:
        return 'высокий уровень социального остракизма'



def calc_sub_value_ot(row):
    """
    Функция для подсчета значения субшкалы Отвержение
    :return: число
    """
    lst_pr = [3, 6, 11, 14]

    value_forward = 0 # счетчик прямых ответов
    value_reverse = 0 # счетчик обратных ответов
    lst_forward = [6, 11, 14]  # список ответов которые нужно считать простым сложением
    lst_reverse = [3] # обратный подсчет

    for idx, value in enumerate(row):
        if idx +1 in lst_pr:
            if idx + 1 in lst_forward:
                # print(f'Прямой подсчет {idx +1}') # Для проверки корректности
                value_forward += value
            elif idx +1 in lst_reverse:
                # print(f'Обратный подсчет {idx +1}')# Для проверки корректности
                if value == 5:
                    value_reverse += 1
                elif value == 4:
                    value_reverse += 2
                elif value == 3:
                    value_reverse += 3
                elif value == 2:
                    value_reverse += 4
                elif value == 1:
                    value_reverse += 5

    return round((value_forward + value_reverse) /4,1)

def calc_level_sub_ot(value):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """
    if 1 <= value <= 1.6:
        return 'низкий уровень социального остракизма'
    elif 1.7 <= value <= 2.5:
        return 'средний уровень социального остракизма'
    elif 2.6 <= value <= 5:
        return 'высокий уровень социального остракизма'


def count_all_scale(df:pd.DataFrame, lst_cols:list, lst_index:list):
    """
    Функция для подсчета уровней по всем шкалам
    :param df: датарфейм
    :param lst_cols: список колонок по которым нужно вести обработку
    :param lst_index: список индексов
    :return:датафрейм
    """
    base_df = pd.DataFrame(index=lst_index) # базовый датафрейм с индексами
    for scale in lst_cols:
        scale_df = pd.pivot_table(df, index=f'Уровень_субшкалы_{scale}',
                                                  values=f'Значение_субшкалы_{scale}',
                                                  aggfunc='count')

        scale_df[f'{scale}% от общего'] = round(
            scale_df[f'Значение_субшкалы_{scale}'] / scale_df[f'Значение_субшкалы_{scale}'].sum(),3) * 100
        scale_df.rename(columns={f'Значение_субшкалы_{scale}':f'Количество_{scale}'},inplace=True)

        # # Создаем суммирующую строку
        scale_df.loc['Итого'] = scale_df.sum()


        base_df = base_df.join(scale_df)

    base_df = base_df.reset_index()
    base_df.rename(columns={'index':'Уровень остракизма'},inplace=True)
    return base_df


def calc_mean(df:pd.DataFrame,type_calc:str,lst_cat:list,val_cat):
    """
    Функция для создания сводных датафреймов

    :param df: датафрейм с данными
    :param type_calc:тип обработки Группа или Курс
    :param lst_cat:список колонок по которым будет формироваться свод
    :param val_cat:значение по которому будет формиваться свод
    :return:датафрейм
    """
    if type_calc == 'Группа':
        calc_mean_df = pd.pivot_table(df, index=lst_cat,
                                           values=[val_cat],
                                           aggfunc=round_mean)
        calc_mean_df.reset_index(inplace=True)
        return calc_mean_df
    else:
        calc_mean_df = pd.pivot_table(df, index=lst_cat,
                                           values=val_cat,
                                           aggfunc=round_mean)
        calc_mean_df.reset_index(inplace=True)
        return calc_mean_df



def calc_count(df:pd.DataFrame,type_calc:str,lst_cat:list,val_cat,col_cat,lst_cols:list):
    """
    Функция для создания сводных датафреймов

    :param df: датафрейм с данными
    :param type_calc:тип обработки Группа или Курс
    :param lst_cat:список колонок по которым будет формироваться свод
    :param val_cat:значение по которому будет формиваться свод
    :param col_cat: колонка по которой будет формироваться свод
    :param lst_cols:список колонок для правильного порядка сводной таблицы
    :return:датафрейм
    """
    if type_calc == 'Группа':
        count_df = pd.pivot_table(df, index=lst_cat,
                                                 columns=col_cat,
                                                 values=val_cat,
                                                 aggfunc='count', margins=True, margins_name='Итого')

        count_df.reset_index(inplace=True)
        count_df = count_df.reindex(columns=lst_cols)

        count_df['% низкий уровень социального остракизма от общего'] = round(
            count_df['низкий уровень социального остракизма'] / count_df['Итого'], 2) * 100

        count_df['% средний уровень социального остракизма от общего'] = round(
            count_df['средний уровень социального остракизма'] / count_df['Итого'], 2) * 100

        count_df['% высокий уровень социального остракизма от общего'] = round(
            count_df['высокий уровень социального остракизма'] / count_df['Итого'], 2) * 100


        return count_df
    else:
        count_df = pd.pivot_table(df, index=lst_cat,
                                  columns=col_cat,
                                  values=val_cat,
                                  aggfunc='count', margins=True, margins_name='Итого')

        count_df.reset_index(inplace=True)
        count_df = count_df.reindex(columns=lst_cols)

        count_df['% низкий уровень социального остракизма от общего'] = round(
            count_df['низкий уровень социального остракизма'] / count_df['Итого'], 2) * 100

        count_df['% средний уровень социального остракизма от общего'] = round(
            count_df['средний уровень социального остракизма'] / count_df['Итого'], 2) * 100

        count_df['% высокий уровень социального остракизма от общего'] = round(
            count_df['высокий уровень социального остракизма'] / count_df['Итого'], 2) * 100

        return count_df












def processing_shso(base_df: pd.DataFrame, answers_df: pd.DataFrame):
    """
    Функция для обработки
    :param base_df: часть датафрейма с описательными колонками
    :param answers_df: часть датафрейма с ответами
    """
    try:
        out_answer_df = base_df.copy()  # делаем копию для последующего соединения с сырыми ответами
        if len(answers_df.columns) != 14:  # проверяем количество колонок с вопросами
            raise BadCountColumnsSHSO

        lst_check_cols = ['В основном, другие относятся ко мне как к невидимке',
                          'В основном, другие смотрят сквозь меня, будто я не существую',
                          'В основном, другие отвергают мои предложения',
                          'В основном, другие игнорируют меня во время разговора',
                          'В основном, другие приглашают меня на выходные',
                          'В основном, другие отказывают мне, когда я что-либо спрашиваю',
                          'В основном, другие игнорируют меня',
                          'В основном, другие проводят время со мной у меня дома',
                          'В основном, другие приглашают меня стать членом их клуба, организации, группы',
                          'В основном, другие игнорируют мои приветствия при встрече',
                          'В основном, другие не стесняются писать мне в соцсети, что не пойдут со мной на встречу',
                          'В основном, другие всячески стараются привлечь моё внимание',
                          'В основном, другие приглашают меня присоединиться к ним в хобби, провести вместе выходные или сходить куда-нибудь',
                          'В основном, другие часто противоречат мне в большой компании',
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
            raise BadOrderSHSO

        # словарь для замены слов на числа
        dct_replace_value = {'всегда': 5,
                             'часто': 4,
                             'иногда': 3,
                             'редко': 2,
                             'никогда': 1}

        valid_values = [1, 2, 3, 4, 5]
        answers_df.replace(dct_replace_value, inplace=True)  # заменяем слова на цифры для подсчетов

        # Проверяем, есть ли значения, отличающиеся от указанных в списке
        lst_error_answers = []  # список для хранения строк где найдены неправильные ответы

        for i in range(14):
            mask = ~answers_df.iloc[:, i].isin(valid_values)  # проверяем на допустимые значения
            result_check = answers_df.iloc[:, i][mask]
            if len(result_check) != 0:
                error_row = list(map(lambda x: x + 2, result_check.index))
                error_row = list(map(str, error_row))
                error_row_lst = [f'В {i + 1} вопросной колонке на строке {value}' for value in error_row]
                error_in_column = ','.join(error_row_lst)
                lst_error_answers.append(error_in_column)

        if len(lst_error_answers) != 0:
            error_message = ';'.join(lst_error_answers)
            raise BadValueSHSO

        # Субшкала Игнорирование
        base_df['Значение_субшкалы_Игнорирование'] = answers_df.apply(calc_sub_value_ig, axis=1)
        base_df['Норма_Игнорирование'] = '1,4-2 балла'
        base_df['Уровень_субшкалы_Игнорирование'] = base_df['Значение_субшкалы_Игнорирование'].apply(
            calc_level_sub_ig)

        # Субшкала Исключение
        base_df['Значение_субшкалы_Исключение'] = answers_df.apply(calc_sub_value_isk, axis=1)
        base_df['Норма_Исключение'] = '2,4-3,4 баллов'
        base_df['Уровень_субшкалы_Исключение'] = base_df['Значение_субшкалы_Исключение'].apply(
            calc_level_sub_isk)

        # Субшкала Отвержение
        base_df['Значение_субшкалы_Отвержение'] = answers_df.apply(calc_sub_value_ot, axis=1)
        base_df['Норма_Отвержение'] = '1,7-2,5 баллов'
        base_df['Уровень_субшкалы_Отвержение'] = base_df['Значение_субшкалы_Отвержение'].apply(
            calc_level_sub_ot)

        # Создаем датафрейм для создания части в общий датафрейм
        part_df = pd.DataFrame()

        part_df['ШСО_Игнорирование'] = base_df['Значение_субшкалы_Игнорирование']
        part_df['ШСО_Уровень_Игнорирование'] = base_df['Уровень_субшкалы_Игнорирование']

        part_df['ШСО_Исключение'] = base_df['Значение_субшкалы_Исключение']
        part_df['ШСО_Уровень_Исключение'] = base_df['Уровень_субшкалы_Исключение']

        part_df['ШСО_Отвержение'] = base_df['Значение_субшкалы_Отвержение']
        part_df['ШСО_Уровень_Отвержение'] = base_df['Уровень_субшкалы_Отвержение']


        base_df.sort_values(by='Значение_субшкалы_Игнорирование', ascending=False, inplace=True)  # сортируем
        out_answer_df = pd.concat([out_answer_df, answers_df], axis=1)  # Датафрейм для проверки

        # Общий свод сколько склонностей всего в процентном соотношении
        svod_all_df = count_all_scale(base_df, ['Игнорирование', 'Исключение', 'Отвержение'],
                                              ['низкий уровень социального остракизма',
                                               'средний уровень социального остракизма',
                                               'высокий уровень социального остракизма', 'Итого'])

        lst_reindex_group_cols = ['Группа', 'низкий уровень социального остракизма',
                                  'средний уровень социального остракизма', 'высокий уровень социального остракизма',
                                  'Итого']
        lst_reindex_group_sex_cols = ['Группа', 'Пол', 'низкий уровень социального остракизма',
                                      'средний уровень социального остракизма', 'высокий уровень социального остракизма',
                                      'Итого']

        lst_reindex_course_cols = ['Курс', 'низкий уровень социального остракизма',
                                   'средний уровень социального остракизма', 'высокий уровень социального остракизма',
                                   'Итого']
        lst_reindex_course_sex_cols = ['Курс', 'Пол', 'низкий уровень социального остракизма',
                                       'средний уровень социального остракизма',
                                       'высокий уровень социального остракизма',
                                       'Итого']

        """
                    Обрабатываем Группа
                    """

        # Игнорирование
        svod_group_sop_df = calc_mean(base_df, 'Группа', ['Группа'], 'Значение_субшкалы_Игнорирование')
        svod_count_group_sop_df = calc_count(base_df, 'Группа', ['Группа'], 'Значение_субшкалы_Игнорирование',
                                             'Уровень_субшкалы_Игнорирование',
                                             lst_reindex_group_cols)
        # Исключение
        svod_group_dp_df = calc_mean(base_df, 'Группа', ['Группа'], 'Значение_субшкалы_Исключение')
        svod_count_group_dp_df = calc_count(base_df, 'Группа', ['Группа'], 'Значение_субшкалы_Исключение',
                                            'Уровень_субшкалы_Исключение',
                                            lst_reindex_group_cols)

        # Отвержение
        svod_group_zp_df = calc_mean(base_df, 'Группа', ['Группа'], 'Значение_субшкалы_Отвержение')
        svod_count_group_zp_df = calc_count(base_df, 'Группа', ['Группа'], 'Значение_субшкалы_Отвержение',
                                            'Уровень_субшкалы_Отвержение',
                                            lst_reindex_group_cols)

        """
                      Обрабатываем Группа Пол
                      """

        # Игнорирование
        svod_group_sex_sop_df = calc_mean(base_df, 'Группа', ['Группа', 'Пол'], 'Значение_субшкалы_Игнорирование')
        svod_count_group_sex_sop_df = calc_count(base_df, 'Группа', ['Группа', 'Пол'], 'Значение_субшкалы_Игнорирование',
                                                 'Уровень_субшкалы_Игнорирование',
                                                 lst_reindex_group_sex_cols)
        # Исключение
        svod_group_sex_dp_df = calc_mean(base_df, 'Группа', ['Группа', 'Пол'], 'Значение_субшкалы_Исключение')
        svod_count_group_sex_dp_df = calc_count(base_df, 'Группа', ['Группа', 'Пол'], 'Значение_субшкалы_Исключение',
                                                'Уровень_субшкалы_Исключение',
                                                lst_reindex_group_sex_cols)

        # Отвержение
        svod_group_sex_zp_df = calc_mean(base_df, 'Группа', ['Группа', 'Пол'], 'Значение_субшкалы_Отвержение')
        svod_count_group_sex_zp_df = calc_count(base_df, 'Группа', ['Группа', 'Пол'], 'Значение_субшкалы_Отвержение',
                                                'Уровень_субшкалы_Отвержение',
                                                lst_reindex_group_sex_cols)

        """
                     Обрабатываем Номер класса
                     """

        # Игнорирование
        svod_course_sop_df = calc_mean(base_df, 'Курс', ['Курс'], 'Значение_субшкалы_Игнорирование')
        svod_count_course_sop_df = calc_count(base_df, 'Курс', ['Курс'], 'Значение_субшкалы_Игнорирование',
                                              'Уровень_субшкалы_Игнорирование',
                                              lst_reindex_course_cols)
        # Исключение
        svod_course_dp_df = calc_mean(base_df, 'Курс', ['Курс'], 'Значение_субшкалы_Исключение')
        svod_count_course_dp_df = calc_count(base_df, 'Курс', ['Курс'], 'Значение_субшкалы_Исключение',
                                             'Уровень_субшкалы_Исключение',
                                             lst_reindex_course_cols)

        # Отвержение
        svod_course_zp_df = calc_mean(base_df, 'Курс', ['Курс'], 'Значение_субшкалы_Отвержение')
        svod_count_course_zp_df = calc_count(base_df, 'Курс', ['Курс'], 'Значение_субшкалы_Отвержение',
                                             'Уровень_субшкалы_Отвержение',
                                             lst_reindex_course_cols)

        """
                     Обрабатываем Номер класса Пол
                     """

        # Игнорирование
        svod_course_sex_sop_df = calc_mean(base_df, 'Курс', ['Курс', 'Пол'],
                                           'Значение_субшкалы_Игнорирование')
        svod_count_course_sex_sop_df = calc_count(base_df, 'Курс', ['Курс', 'Пол'],
                                                  'Значение_субшкалы_Игнорирование',
                                                  'Уровень_субшкалы_Игнорирование',
                                                  lst_reindex_course_sex_cols)
        # Исключение
        svod_course_sex_dp_df = calc_mean(base_df, 'Курс', ['Курс', 'Пол'],
                                          'Значение_субшкалы_Исключение')
        svod_count_course_sex_dp_df = calc_count(base_df, 'Курс', ['Курс', 'Пол'],
                                                 'Значение_субшкалы_Исключение',
                                                 'Уровень_субшкалы_Исключение',
                                                 lst_reindex_course_sex_cols)

        # Отвержение
        svod_course_sex_zp_df = calc_mean(base_df, 'Курс', ['Курс', 'Пол'], 'Значение_субшкалы_Отвержение')
        svod_count_course_sex_zp_df = calc_count(base_df, 'Курс', ['Курс', 'Пол'],
                                                 'Значение_субшкалы_Отвержение', 'Уровень_субшкалы_Отвержение',
                                                 lst_reindex_course_sex_cols)

        out_dct = {'Списочный результат': base_df, 'Список для проверки': out_answer_df,
                   'Общий свод': svod_all_df,
                   'Среднее Группа Иг': svod_group_sop_df, 'Количество Группа Иг': svod_count_group_sop_df,
                   'Среднее Группа Ис': svod_group_dp_df, 'Количество Группа Ис': svod_count_group_dp_df,
                   'Среднее Группа От': svod_group_zp_df, 'Количество Группа От': svod_count_group_zp_df,

                   'Среднее Группа Пол Иг': svod_group_sex_sop_df, 'Количество Группа Пол Иг': svod_count_group_sex_sop_df,
                   'Среднее Группа Пол Ис': svod_group_sex_dp_df, 'Количество Группа Пол Ис': svod_count_group_sex_dp_df,
                   'Среднее Группа Пол От': svod_group_sex_zp_df, 'Количество Группа Пол От': svod_count_group_sex_zp_df,

                   'Среднее Курс Иг': svod_course_sop_df, 'Количество Курс Иг': svod_count_course_sop_df,
                   'Среднее Курс Ис': svod_course_dp_df, 'Количество Курс Ис': svod_count_course_dp_df,
                   'Среднее Курс От': svod_course_zp_df, 'Количество Курс От': svod_count_course_zp_df,

                   'Среднее Курс Пол Иг': svod_course_sex_sop_df,'Количество Курс Пол Иг': svod_count_course_sex_sop_df,
                   'Среднее Курс Пол Ис': svod_course_sex_dp_df,'Количество Курс Пол Ис': svod_count_course_sex_dp_df,
                   'Среднее Курс Пол От': svod_course_sex_zp_df,'Количество Курс Пол От': svod_count_course_sex_zp_df,
                   }

        return out_dct, part_df
    except BadOrderSHSO:
        messagebox.showerror('Лахеcис',
                             f'При обработке вопросов теста Шкала субъективного остракизма Бойкина обнаружены неправильные вопросы. Проверьте названия колонок с вопросами:\n'
                             f'{error_order_message}\n'
                             f'Используйте при создании Яндекс-формы написание вопросов из руководства пользователя программы Лахесис.')
    except BadValueSHSO:
        messagebox.showerror('Лахеcис',
                             f'При обработке вопросов теста Шкала субъективного остракизма Бойкина обнаружены неправильные варианты ответов. Проверьте ответы на указанных строках:\n'
                             f'{error_message}\n'
                             f'Используйте при создании Яндекс-формы написание вариантов ответа из руководства пользователя программы Лахесис.')


    except BadCountColumnsSHSO:
        messagebox.showerror('Лахеcис',
                             f'Проверьте количество колонок с ответами на тест Шкала субъективного остракизма Бойкина\n'
                             f'Должно быть 14 колонок с ответами')

















