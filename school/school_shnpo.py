"""
Скрипт для обработки результатов теста Шкала нарушенных потребностей остракизм Бойкина
"""

import pandas as pd
from tkinter import messagebox
from lachesis_support_functions import round_mean,sort_name_class

class BadOrderSHNPO(Exception):
    """
    Исключение для обработки случая когда колонки не совпадают
    """
    pass


class BadValueSHNPO(Exception):
    """
    Исключение для неправильных значений в вариантах ответов
    """
    pass

class BadCountColumnsSHNPO(Exception):
    """
    Исключение для обработки случая если количество колонок не равно 20
    """
    pass




def calc_sub_value_pr(row):
    """
    Функция для подсчета значения субшкалы Принадлежности
    :param row: строка с ответами
    :return: число
    """
    lst_pr = [1, 4, 6, 7, 13]

    value_forward = 0 # счетчик прямых ответов
    value_reverse = 0 # счетчик обратных ответов
    lst_forward = [1, 6, 13]  # список ответов которые нужно считать простым сложением
    lst_reverse = [4, 7] # обратный подсчет

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

def calc_level_sub_pr_pod(value):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """
    if 1 <= value <= 1.4:
        return 'низкий уровень социального остракизма'
    elif 1.5 <= value <= 2.4:
        return 'средний уровень социального остракизма'
    elif 2.5 <= value <= 5:
        return 'высокий уровень социального остракизма'

def calc_level_sub_pr_mol(value):
    """
    Функция для подсчета уровня субшкалы
    :param value:
    :return:
    """
    if 1 <= value <= 1.6:
        return 'низкий уровень социального остракизма'
    elif 1.7 <= value <= 3:
        return 'средний уровень социального остракизма'
    elif 3.1 <= value <= 5:
        return 'высокий уровень социального остракизма'



def calc_sub_value_sam(row):
    """
    Функция для подсчета значения субшкалы Самоуважение
    :param row: строка с ответами
    :return: число
    """
    lst_pr = [5, 9, 11, 12, 15]

    value_forward = 0 # счетчик прямых ответов
    value_reverse = 0 # счетчик обратных ответов
    lst_forward = [5]  # список ответов которые нужно считать простым сложением
    lst_reverse = [9, 11, 12, 15] # обратный подсчет

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

def calc_level_sub_sam_pod(value):
    """
    Функция для подсчета уровня субшкалы самоуважения
    :param value:
    :return:
    """
    if 1 <= value <= 1.6:
        return 'низкий уровень социального остракизма'
    elif 1.7 <= value <= 2.8:
        return 'средний уровень социального остракизма'
    elif 2.9 <= value <= 5:
        return 'высокий уровень социального остракизма'

def calc_level_sub_sam_mol(value):
    """
    Функция для подсчета уровня субшкалы самоуважения
    :param value:
    :return:
    """
    if 1 <= value <= 1.8:
        return 'низкий уровень социального остракизма'
    elif 1.9 <= value <= 3.2:
        return 'средний уровень социального остракизма'
    elif 3.3 <= value <= 5:
        return 'высокий уровень социального остракизма'



def calc_sub_value_con(row):
    """
    Функция для подсчета значения субшкалы Контроль
    :param row: строка с ответами
    :return: число
    """
    lst_pr = [3, 8, 10, 14, 20]

    value_forward = 0 # счетчик прямых ответов
    value_reverse = 0 # счетчик обратных ответов
    lst_forward = [3,8,14,20]  # список ответов которые нужно считать простым сложением
    lst_reverse = [10] # обратный подсчет

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

def calc_level_sub_con_pod(value):
    """
    Функция для подсчета уровня субшкалы самоуважения
    :param value:
    :return:
    """
    if 1 <= value <= 1.2:
        return 'низкий уровень социального остракизма'
    elif 1.3 <= value <= 2.4:
        return 'средний уровень социального остракизма'
    elif 2.5 <= value <= 5:
        return 'высокий уровень социального остракизма'


def calc_level_sub_con_mol(value):
    """
    Функция для подсчета уровня субшкалы контроля
    :param value:
    :return:
    """
    if 1 <= value <= 1.6:
        return 'низкий уровень социального остракизма'
    elif 1.7 <= value <= 2.8:
        return 'средний уровень социального остракизма'
    elif 2.9 <= value <= 5:
        return 'высокий уровень социального остракизма'


def calc_sub_value_os(row):
    """
    Функция для подсчета значения субшкалы Осмысленное существование
    :param row: строка с ответами
    :return: число
    """
    lst_pr = [2, 16, 17, 18, 19]

    value_forward = 0 # счетчик прямых ответов
    value_reverse = 0 # счетчик обратных ответов
    lst_forward = [16,19]  # список ответов которые нужно считать простым сложением
    lst_reverse = [2, 17, 18] # обратный подсчет

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

def calc_level_sub_os_pod(value):
    """
    Функция для подсчета уровня субшкалы самоуважения
    :param value:
    :return:
    """
    if 1 <= value <= 1.4:
        return 'низкий уровень социального остракизма'
    elif 1.5 <= value <= 2.6:
        return 'средний уровень социального остракизма'
    elif 2.7 <= value <= 5:
        return 'высокий уровень социального остракизма'

def calc_level_sub_os_mol(value):
    """
    Функция для подсчета уровня субшкалы осмысленного существования
    :param value:
    :return:
    """
    if 1 <= value <= 1.8:
        return 'низкий уровень социального остракизма'
    elif 1.9 <= value <= 3.2:
        return 'средний уровень социального остракизма'
    elif 3.3 <= value <= 5:
        return 'высокий уровень социального остракизма'




def count_all_scale_pod(df:pd.DataFrame, lst_cols:list, lst_index:list):
    """
    Функция для подсчета уровней по всем шкалам
    :param df: датарфейм
    :param lst_cols: список колонок по которым нужно вести обработку
    :param lst_index: список индексов
    :return:датафрейм
    """
    base_df = pd.DataFrame(index=lst_index) # базовый датафрейм с индексами
    for scale in lst_cols:
        scale_df = pd.pivot_table(df, index=f'Уровень_субшкалы_{scale}_Подростки',
                                                  values=f'Значение_субшкалы_{scale}',
                                                  aggfunc='count')

        scale_df[f'{scale}% от общего'] = round(
            scale_df[f'Значение_субшкалы_{scale}'] / scale_df[f'Значение_субшкалы_{scale}'].sum(),3) * 100
        scale_df.rename(columns={f'Значение_субшкалы_{scale}':f'Количество_{scale}'},inplace=True)

        # # Создаем суммирующую строку
        scale_df.loc['Итого'] = scale_df.sum()


        base_df = base_df.join(scale_df)

    base_df = base_df.reset_index()
    base_df.rename(columns={'index':'Уровень потребности'},inplace=True)
    return base_df


def count_all_scale_mol(df:pd.DataFrame, lst_cols:list, lst_index:list):
    """
    Функция для подсчета уровней по всем шкалам
    :param df: датарфейм
    :param lst_cols: список колонок по которым нужно вести обработку
    :param lst_index: список индексов
    :return:датафрейм
    """
    base_df = pd.DataFrame(index=lst_index) # базовый датафрейм с индексами
    for scale in lst_cols:
        scale_df = pd.pivot_table(df, index=f'Уровень_субшкалы_{scale}_Молодежь',
                                                  values=f'Значение_субшкалы_{scale}',
                                                  aggfunc='count')

        scale_df[f'{scale}% от общего'] = round(
            scale_df[f'Значение_субшкалы_{scale}'] / scale_df[f'Значение_субшкалы_{scale}'].sum(),3) * 100
        scale_df.rename(columns={f'Значение_субшкалы_{scale}':f'Количество_{scale}'},inplace=True)

        # # Создаем суммирующую строку
        scale_df.loc['Итого'] = scale_df.sum()


        base_df = base_df.join(scale_df)

    base_df = base_df.reset_index()
    base_df.rename(columns={'index':'Уровень потребности'},inplace=True)
    return base_df





def calc_mean(df:pd.DataFrame,type_calc:str,lst_cat:list,val_cat):
    """
    Функция для создания сводных датафреймов

    :param df: датафрейм с данными
    :param type_calc:тип обработки Класс или Номер_класса
    :param lst_cat:список колонок по которым будет формироваться свод
    :param val_cat:значение по которому будет формиваться свод
    :return:датафрейм
    """
    if type_calc == 'Класс':
        calc_mean_df = pd.pivot_table(df, index=lst_cat,
                                           values=[val_cat],
                                           aggfunc=round_mean)
        calc_mean_df.reset_index(inplace=True)
        calc_mean_df.sort_values(by='Класс', key=lambda x: x.map(sort_name_class), inplace=True)  # сортируем
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
    :param type_calc:тип обработки Класс или Номер_класса
    :param lst_cat:список колонок по которым будет формироваться свод
    :param val_cat:значение по которому будет формиваться свод
    :param col_cat: колонка по которой будет формироваться свод
    :param lst_cols:список колонок для правильного порядка сводной таблицы
    :return:датафрейм
    """
    if type_calc == 'Класс':
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

        part_svod_df = count_df.iloc[:-1:]
        part_svod_df.sort_values(by='Класс', key=lambda x: x.map(sort_name_class), inplace=True)  # сортируем
        itog_svod_df = count_df.iloc[-1:]
        count_df = pd.concat([part_svod_df, itog_svod_df])

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









def processing_shnpo(base_df: pd.DataFrame, answers_df: pd.DataFrame):
    """
    Функция для обработки
    :param base_df: часть датафрейма с описательными колонками
    :param answers_df: часть датафрейма с ответами
    """
    out_answer_df = base_df.copy()  # делаем копию для последующего соединения с сырыми ответами
    if len(answers_df.columns) != 20:  # проверяем количество колонок с вопросами
        raise BadCountColumnsSHNPO

    lst_check_cols = ['Я чувствую себя единым целым с другими людьми',
                      'Полагаю, что не вношу значимый вклад во что-либо',
                      'У меня есть уверенность, что я влияю на ход событий в моей жизни',
                      'Среди своего окружения я ощущаю себя лишним',
                      'Люди прислушиваются к моему мнению',
                      'В любой ситуации я чувствую поддержку хоть одного человека',
                      'Я ощущаю себя изгоем',
                      'Я совершенно точно управляю всем в своей жизни',
                      'Мне кажется, большинство из моего окружения невысокого обо мне мнения',
                      'Порой, кажется, что всё зависит от чьей-то чужой воли',
                      'Общаясь с людьми, я чувствую себя неуверенно',
                      'Такое ощущение, что общение с людьми – не моя сильная сторона',
                      'Думаю, что общество, в котором я живу, принимает меня',
                      'Я контролирую свою жизнь',
                      'Я переживаю, что люди плохо думают обо мне',
                      'Мне кажется, что моё участие в жизни окружающих очень важно',
                      'Порой я ощущаю себя невидимкой',
                      'Временами мне кажется, что от меня людям нет никакого толка',
                      'Думаю, мое участие в чем-либо всегда полезно',
                      'Такое ощущение, что у меня впереди еще много разных возможностей'
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
        raise BadOrderSHNPO

    # словарь для замены слов на числа
    dct_replace_value = {'не согласен': 5,
                         'редко': 4,
                         'иногда': 3,
                         'часто': 2,
                         'полностью согласен': 1}

    valid_values = [1, 2, 3, 4, 5]
    answers_df.replace(dct_replace_value, inplace=True)  # заменяем слова на цифры для подсчетов

    # Проверяем, есть ли значения, отличающиеся от указанных в списке
    lst_error_answers = []  # список для хранения строк где найдены неправильные ответы

    for i in range(20):
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
        raise BadValueSHNPO

    # Субшкала Принаддежность
    base_df['Значение_субшкалы_Принадлежность'] = answers_df.apply(calc_sub_value_pr, axis=1)
    base_df['Норма_Принадлежность_Подростки'] = '1,5-2,4 баллов'
    base_df['Уровень_субшкалы_Принадлежность_Подростки'] = base_df['Значение_субшкалы_Принадлежность'].apply(calc_level_sub_pr_pod)

    base_df['Норма_Принадлежность_Молодежь'] = '1,7-3 балла'
    base_df['Уровень_субшкалы_Принадлежность_Молодежь'] = base_df['Значение_субшкалы_Принадлежность'].apply(calc_level_sub_pr_mol)

    # Субшкала Самоуважение
    base_df['Значение_субшкалы_Самоуважение'] = answers_df.apply(calc_sub_value_sam, axis=1)
    base_df['Норма_Самоуважение_Подростки'] = '1,7-2,8 баллов'
    base_df['Уровень_субшкалы_Самоуважение_Подростки'] = base_df['Значение_субшкалы_Самоуважение'].apply(calc_level_sub_sam_pod)

    base_df['Норма_Самоуважение_Молодежь'] = '1,9-3,2 балла'
    base_df['Уровень_субшкалы_Самоуважение_Молодежь'] = base_df['Значение_субшкалы_Самоуважение'].apply(calc_level_sub_sam_mol)

    # Субшкала Контроль
    base_df['Значение_субшкалы_Контроль'] = answers_df.apply(calc_sub_value_con, axis=1)
    base_df['Норма_Контроль_Подростки'] = '1,3-2,4 баллов'
    base_df['Уровень_субшкалы_Контроль_Подростки'] = base_df['Значение_субшкалы_Контроль'].apply(calc_level_sub_con_pod)

    base_df['Норма_Контроль_Молодежь'] = '1,7-2,8 баллов'
    base_df['Уровень_субшкалы_Контроль_Молодежь'] = base_df['Значение_субшкалы_Контроль'].apply(calc_level_sub_con_mol)

    # Субшкала Осмысленное сущенствование
    base_df['Значение_субшкалы_Ос_существование'] = answers_df.apply(calc_sub_value_os, axis=1)
    base_df['Норма_Ос_существование_Подростки'] = '1,5-2,6 баллов'
    base_df['Уровень_субшкалы_Ос_существование_Подростки'] = base_df['Значение_субшкалы_Ос_существование'].apply(calc_level_sub_os_pod)

    base_df['Норма_Ос_существование_Молодежь'] = '1,9-3,2 балла'
    base_df['Уровень_субшкалы_Ос_существование_Молодежь'] = base_df['Значение_субшкалы_Ос_существование'].apply(calc_level_sub_os_mol)

    # Создаем датафрейм для создания части в общий датафрейм
    part_df = pd.DataFrame(
        columns=['ШНПО_ПМ_Принадлежность', 'ШНПО_ПМ_Уровень_Принадлежность_Подростки','ШНПО_ПМ_Уровень_Принадлежность_Молодежь',
                 'ШНПО_ПМ_Самоуважение','ШНПО_ПМ_Уровень_Самоуважение_Подростки', 'ШНПО_ПМ_Уровень_Самоуважение_Молодежь',
                 'ШНПО_ПМ_Контроль','ШНПО_ПМ_Уровень_Контроль_Подростки', 'ШНПО_ПМ_Уровень_Контроль_Молодежь',
                 'ШНПО_ПМ_Ос_существование','ШНПО_ПМ_Уровень_Ос_существование_Подростки', 'ШНПО_ПМ_Уровень_Ос_существование_Молодежь'
                 ])

    part_df['ШНПО_ПМ_Принадлежность'] = base_df['Значение_субшкалы_Принадлежность']
    part_df['ШНПО_ПМ_Уровень_Принадлежность_Подростки'] = base_df['Уровень_субшкалы_Принадлежность_Подростки']
    part_df['ШНПО_ПМ_Уровень_Принадлежность_Молодежь'] = base_df['Уровень_субшкалы_Принадлежность_Молодежь']

    part_df['ШНПО_ПМ_Самоуважение'] = base_df['Значение_субшкалы_Самоуважение']
    part_df['ШНПО_ПМ_Уровень_Самоуважение_Подростки'] = base_df['Уровень_субшкалы_Самоуважение_Подростки']
    part_df['ШНПО_ПМ_Уровень_Самоуважение_Молодежь'] = base_df['Уровень_субшкалы_Самоуважение_Молодежь']

    part_df['ШНПО_ПМ_Контроль'] = base_df['Значение_субшкалы_Контроль']
    part_df['ШНПО_ПМ_Уровень_Контроль_Подростки'] = base_df['Уровень_субшкалы_Контроль_Подростки']
    part_df['ШНПО_ПМ_Уровень_Контроль_Молодежь'] = base_df['Уровень_субшкалы_Контроль_Молодежь']

    part_df['ШНПО_ПМ_Ос_существование'] = base_df['Значение_субшкалы_Ос_существование']
    part_df['ШНПО_ПМ_Уровень_Ос_существование_Подростки'] = base_df['Уровень_субшкалы_Ос_существование_Подростки']
    part_df['ШНПО_ПМ_Уровень_Ос_существование_Молодежь'] = base_df['Уровень_субшкалы_Ос_существование_Молодежь']

    base_df.sort_values(by='Значение_субшкалы_Принадлежность', ascending=False, inplace=True)  # сортируем
    out_answer_df = pd.concat([out_answer_df, answers_df], axis=1)  # Датафрейм для проверки

    """
    Для подростков
    """

    # Общий свод сколько склонностей всего в процентном соотношении Подростки
    svod_all_df_pod = count_all_scale_pod(base_df, ['Принадлежность', 'Самоуважение', 'Контроль', 'Ос_существование'],
                                      ['низкий уровень социального остракизма','средний уровень социального остракизма','высокий уровень социального остракизма', 'Итого'])

    lst_reindex_group_cols = ['Класс', 'низкий уровень социального остракизма','средний уровень социального остракизма','высокий уровень социального остракизма', 'Итого']
    lst_reindex_group_sex_cols = ['Класс', 'Пол', 'низкий уровень социального остракизма','средний уровень социального остракизма','высокий уровень социального остракизма', 'Итого']

    lst_reindex_course_cols = ['Номер_класса', 'низкий уровень социального остракизма','средний уровень социального остракизма','высокий уровень социального остракизма', 'Итого']
    lst_reindex_course_sex_cols = ['Номер_класса', 'Пол', 'низкий уровень социального остракизма','средний уровень социального остракизма','высокий уровень социального остракизма', 'Итого']

    """
    Общий свод для молодежи
    """
    svod_all_df_mol = count_all_scale_mol(base_df, ['Принадлежность', 'Самоуважение', 'Контроль', 'Ос_существование'],
                                      ['низкий уровень социального остракизма','средний уровень социального остракизма','высокий уровень социального остракизма', 'Итого'])




    """
        Обрабатываем Класс
        """

    # Принадлежность
    svod_group_sop_df = calc_mean(base_df, 'Класс', ['Класс'], 'Значение_субшкалы_Принадлежность')
    svod_count_group_sop_df = calc_count(base_df, 'Класс', ['Класс'], 'Значение_субшкалы_Принадлежность', 'Уровень_субшкалы_Принадлежность_Подростки',
                                         lst_reindex_group_cols)
    # Самоуважение
    svod_group_dp_df = calc_mean(base_df, 'Класс', ['Класс'], 'Значение_субшкалы_Самоуважение')
    svod_count_group_dp_df = calc_count(base_df, 'Класс', ['Класс'], 'Значение_субшкалы_Самоуважение', 'Уровень_субшкалы_Самоуважение_Подростки',
                                        lst_reindex_group_cols)

    # Контроль
    svod_group_zp_df = calc_mean(base_df, 'Класс', ['Класс'], 'Значение_субшкалы_Контроль')
    svod_count_group_zp_df = calc_count(base_df, 'Класс', ['Класс'], 'Значение_субшкалы_Контроль', 'Уровень_субшкалы_Контроль_Подростки',
                                        lst_reindex_group_cols)

    # Осмысленное существование
    svod_group_ap_df = calc_mean(base_df, 'Класс', ['Класс'], 'Значение_субшкалы_Ос_существование')
    svod_count_group_ap_df = calc_count(base_df, 'Класс', ['Класс'], 'Значение_субшкалы_Ос_существование', 'Уровень_субшкалы_Ос_существование_Подростки',
                                        lst_reindex_group_cols)



    """
        Обрабатываем Класс Пол
        """

    # Принадлежность
    svod_group_sex_sop_df = calc_mean(base_df, 'Класс', ['Класс','Пол'], 'Значение_субшкалы_Принадлежность')
    svod_count_group_sex_sop_df = calc_count(base_df, 'Класс', ['Класс','Пол'], 'Значение_субшкалы_Принадлежность', 'Уровень_субшкалы_Принадлежность_Подростки',
                                         lst_reindex_group_sex_cols)
    # Самоуважение
    svod_group_sex_dp_df = calc_mean(base_df, 'Класс', ['Класс','Пол'], 'Значение_субшкалы_Самоуважение')
    svod_count_group_sex_dp_df = calc_count(base_df, 'Класс', ['Класс','Пол'], 'Значение_субшкалы_Самоуважение', 'Уровень_субшкалы_Самоуважение_Подростки',
                                        lst_reindex_group_sex_cols)

    # Контроль
    svod_group_sex_zp_df = calc_mean(base_df, 'Класс', ['Класс','Пол'], 'Значение_субшкалы_Контроль')
    svod_count_group_sex_zp_df = calc_count(base_df, 'Класс', ['Класс','Пол'], 'Значение_субшкалы_Контроль', 'Уровень_субшкалы_Контроль_Подростки',
                                        lst_reindex_group_sex_cols)

    # Осмысленное существование
    svod_group_sex_ap_df = calc_mean(base_df, 'Класс', ['Класс','Пол'], 'Значение_субшкалы_Ос_существование')
    svod_count_group_sex_ap_df = calc_count(base_df, 'Класс', ['Класс','Пол'], 'Значение_субшкалы_Ос_существование', 'Уровень_субшкалы_Ос_существование_Подростки',
                                        lst_reindex_group_sex_cols)


    """
        Обрабатываем Номер класса
        """

    # Принадлежность
    svod_course_sop_df = calc_mean(base_df, 'Номер_класса', ['Номер_класса'], 'Значение_субшкалы_Принадлежность')
    svod_count_course_sop_df = calc_count(base_df, 'Номер_класса', ['Номер_класса'], 'Значение_субшкалы_Принадлежность', 'Уровень_субшкалы_Принадлежность_Подростки',
                                         lst_reindex_course_cols)
    # Самоуважение
    svod_course_dp_df = calc_mean(base_df, 'Номер_класса', ['Номер_класса'], 'Значение_субшкалы_Самоуважение')
    svod_count_course_dp_df = calc_count(base_df, 'Номер_класса', ['Номер_класса'], 'Значение_субшкалы_Самоуважение', 'Уровень_субшкалы_Самоуважение_Подростки',
                                        lst_reindex_course_cols)

    # Контроль
    svod_course_zp_df = calc_mean(base_df, 'Номер_класса', ['Номер_класса'], 'Значение_субшкалы_Контроль')
    svod_count_course_zp_df = calc_count(base_df, 'Номер_класса', ['Номер_класса'], 'Значение_субшкалы_Контроль', 'Уровень_субшкалы_Контроль_Подростки',
                                        lst_reindex_course_cols)

    # Осмысленное существование
    svod_course_ap_df = calc_mean(base_df, 'Номер_класса', ['Номер_класса'], 'Значение_субшкалы_Ос_существование')
    svod_count_course_ap_df = calc_count(base_df, 'Номер_класса', ['Номер_класса'], 'Значение_субшкалы_Ос_существование', 'Уровень_субшкалы_Ос_существование_Подростки',
                                        lst_reindex_course_cols)


    """
        Обрабатываем Номер класса Пол
        """

    # Принадлежность
    svod_course_sex_sop_df = calc_mean(base_df, 'Номер_класса', ['Номер_класса', 'Пол'], 'Значение_субшкалы_Принадлежность')
    svod_count_course_sex_sop_df = calc_count(base_df, 'Номер_класса', ['Номер_класса', 'Пол'], 'Значение_субшкалы_Принадлежность', 'Уровень_субшкалы_Принадлежность_Подростки',
                                         lst_reindex_course_sex_cols)
    # Самоуважение
    svod_course_sex_dp_df = calc_mean(base_df, 'Номер_класса', ['Номер_класса', 'Пол'], 'Значение_субшкалы_Самоуважение')
    svod_count_course_sex_dp_df = calc_count(base_df, 'Номер_класса', ['Номер_класса', 'Пол'], 'Значение_субшкалы_Самоуважение', 'Уровень_субшкалы_Самоуважение_Подростки',
                                        lst_reindex_course_sex_cols)

    # Контроль
    svod_course_sex_zp_df = calc_mean(base_df, 'Номер_класса', ['Номер_класса', 'Пол'], 'Значение_субшкалы_Контроль')
    svod_count_course_sex_zp_df = calc_count(base_df, 'Номер_класса', ['Номер_класса', 'Пол'], 'Значение_субшкалы_Контроль', 'Уровень_субшкалы_Контроль_Подростки',
                                        lst_reindex_course_sex_cols)

    # Осмысленное существование
    svod_course_sex_ap_df = calc_mean(base_df, 'Номер_класса', ['Номер_класса', 'Пол'], 'Значение_субшкалы_Ос_существование')
    svod_count_course_sex_ap_df = calc_count(base_df, 'Номер_класса', ['Номер_класса', 'Пол'], 'Значение_субшкалы_Ос_существование', 'Уровень_субшкалы_Ос_существование_Подростки',
                                        lst_reindex_course_sex_cols)






















    out_dct = {'Списочный результат': base_df, 'Список для проверки': out_answer_df,
               'Общий свод Подростки': svod_all_df_pod,
               'Общий свод Молодежь': svod_all_df_mol,


               'Ср Класс Пр Под': svod_group_sop_df, 'Кол Класс Пр Под': svod_count_group_sop_df,
               'Ср Класс Са Под': svod_group_dp_df, 'Кол Класс Са Под': svod_count_group_dp_df,
               'Ср Класс Ко Под': svod_group_zp_df, 'Кол Класс Ко Под': svod_count_group_zp_df,
               'Ср Класс Ос Под': svod_group_ap_df, 'Кол Класс Ос Под': svod_count_group_ap_df,

               'Ср Класс Пол Пр Под': svod_group_sex_sop_df, 'Кол Класс Пол Пр Под': svod_count_group_sex_sop_df,
               'Ср Класс Пол Са Под': svod_group_sex_dp_df, 'Кол Класс Пол Са Под': svod_count_group_sex_dp_df,
               'Ср Класс Пол Ко Под': svod_group_sex_zp_df, 'Кол Класс Пол Ко Под': svod_count_group_sex_zp_df,
               'Ср Класс Пол Ос Под': svod_group_sex_ap_df, 'Кол Класс Пол Ос Под': svod_count_group_sex_ap_df,

               'Ср Номер_класса Пр Под': svod_course_sop_df, 'Кол Номер_класса Пр Под': svod_count_course_sop_df,
               'Ср Номер_класса Са Под': svod_course_dp_df, 'Кол Номер_класса Са Под': svod_count_course_dp_df,
               'Ср Номер_класса Ко Под': svod_course_zp_df, 'Кол Номер_класса Ко Под': svod_count_course_zp_df,
               'Ср Номер_класса Ос Под': svod_course_ap_df, 'Кол Номер_класса Ос Под': svod_count_course_ap_df,

               'Ср Номер_класса Пол Пр Под': svod_course_sex_sop_df,'Кол Номер_класса Пол Пр Под': svod_count_course_sex_sop_df,
               'Ср Номер_класса Пол Са Под': svod_course_sex_dp_df,'Кол Номер_класса Пол Са Под': svod_count_course_sex_dp_df,
               'Ср Номер_класса Пол Ко Под': svod_course_sex_zp_df,'Кол Номер_класса Пол Ко Под': svod_count_course_sex_zp_df,
               'Ср Номер_класса Пол Ос Под': svod_course_sex_ap_df,'Кол Номер_класса Пол Ос Под': svod_count_course_sex_ap_df,





               }


    return out_dct, part_df