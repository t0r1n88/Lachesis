"""
Скрипт для обработки результатов теста Опросник мотивации к избеганию неудач Элерс Котик
"""

import pandas as pd
import re
from tkinter import messagebox
from lachesis_support_functions import calc_count_scale,round_mean

class BadValueKAF(Exception):
    """
    Исключение для неправильных значений в вариантах ответов
    """
    pass

class BadCountColumnsKAF(Exception):
    """
    Исключение для обработки случая если количество колонок не равно 30
    """
    pass

def calc_value_avoid_fail(row):
    """
    Обработка результатов тестирования
    """
    value_avoid = 0 # количество совпадений с ключом

    # 1
    if row[0] == 'бдительный':
        value_avoid += 1

    # 2
    if row[1] != 'упрямый':
        value_avoid += 1

    # 3
    if row[2] != 'решительный':
        value_avoid += 1

    # 4
    if row[3] == 'внимательный':
        value_avoid += 1

    # 5
    if row[4] == 'трусливый':
        value_avoid += 1

    # 6
    if row[5] == 'предусмотрительный':
        value_avoid += 1

    # 7
    if row[6] != 'хладнокровный':
        value_avoid += 1

    # 8
    if row[7] == 'боязливый':
        value_avoid += 1

    # 9
    if row[8] != 'непредусмотрительный':
        value_avoid += 1

    # 10
    if row[9] == 'добросовестный':
        value_avoid += 1

    # 11
    if row[10] != 'неустойчивый':
        value_avoid += 1

    # 12
    if row[11] != 'небрежный':
        value_avoid += 1

    # 13
    if row[12] != 'опрометчивый':
        value_avoid += 1

    # 14
    if row[13] == 'внимательный':
        value_avoid += 1

    # 15
    if row[14] == 'рассудительный':
        value_avoid += 1

    # 16
    if row[15] != 'предприимчивый':
        value_avoid += 1

    # 17
    if row[16] =='робкий':
        value_avoid += 1

    # 18
    if row[17] == 'малодушный':
        value_avoid += 1

    # 19
    if row[18] != 'нервный':
        value_avoid += 1

    # 20
    if row[19] !='авантюрный':
        value_avoid += 1

    # 21
    if row[20] == 'предусмотрительный':
        value_avoid += 1

    # 22
    if row[21] == 'укрощенный':
        value_avoid += 1

    # 23
    if row[22] != 'беззаботный':
        value_avoid +=1

    # 24
    if row[23] != 'храбрый':
        value_avoid += 1

    # 25
    if row[24] == 'предвидящий':
        value_avoid += 1

    # 26
    if row[25] == 'пугливый':
        value_avoid += 1

    # 27
    if row[26] == 'пессимистичный':
        value_avoid += 1

    # 28
    if row[27] != 'предприимчивый':
        value_avoid += 1

    # 29
    if row[28] != 'неорганизованный':
        value_avoid += 1

    # 30
    if row[29] == 'бдительный':
        value_avoid += 1

    return value_avoid



def calc_level_avoid_fail(value:int):
    """
    Уровень мотивации к успеху
    :param value: значение
    :return:
    """
    if value <= 10:
        return 'низкий уровень мотивации к избеганию неудач'
    elif 11 <= value <= 16:
        return 'средний уровень мотивации к избеганию неудач'
    elif 17 <= value <= 20:
        return 'высокий уровень мотивации к избеганию неудач'
    else:
        return 'слишком высокий уровень мотивации к избеганию неудач'







def processing_kotik_avoiding_fail(base_df: pd.DataFrame, answers_df: pd.DataFrame,lst_svod_cols:list):
    """
    Функция для обработки
    :param base_df: часть датафрейма с описательными колонками
    :param answers_df: часть датафрейма с ответами
    :param lst_svod_cols:  список с колонками по которым нужно делать свод
    """
    out_answer_df = base_df.copy()  # делаем копию для последующего соединения с сырыми ответами
    if len(answers_df.columns) != 30:  # проверяем количество колонок с вопросами
        raise BadCountColumnsKAF

    answers_df.columns = [f'Вопрос {i}' for i in range(1, 31)]

    # делаем список списков
    valid_values = [['смелый','бдительный','предприимчивый'],
                    ['кроткий','робкий','упрямый'],
                    ['осторожный','решительный','пессимистичный'],
                    ['непостоянный','бесцеремонный','внимательный'],
                    ['неумный','трусливый','не думающий'],
                    ['ловкий','бойкий','предусмотрительный'],
                    ['хладнокровный','колеблющийся','удалой'],
                    ['стремительный','легкомысленный','боязливый'],
                    ['не задумывающийся','жеманный','непредусмотрительный'],
                    ['оптимистичный','добросовестный','чуткий'],
                    ['меланхоличный','сомневающийся','неустойчивый'],
                    ['трусливый','небрежный','взволнованный'],
                    ['опрометчивый','тихий','боязливый'],
                    ['внимательный','неблагоразумный','смелый'],
                    ['рассудительный','быстрый','мужественный'],
                    ['предприимчивый','осторожный','предусмотрительный'],
                    ['взволнованный','рассеянный','робкий'],
                    ['малодушный','неосторожный','бесцеремонный'],
                    ['пугливый','нерешительный','нервный'],
                    ['исполнительный','преданный','авантюрный'],
                    ['предусмотрительный','бойкий','отчаянный'],
                    ['укрощенный','безразличный','небрежный'],
                    ['осторожный','беззаботный','терпеливый'],
                    ['разумный','заботливый','храбрый'],
                    ['предвидящий','неустрашимый','добросовестный'],
                    ['поспешный','пугливый','беззаботный'],
                    ['рассеянный','опрометчивый','пессимистичный'],
                    ['осмотрительный','рассудительный','предприимчивый'],
                    ['тихий','неорганизованный','боязливый'],
                    ['оптимистичный','бдительный','беззаботный'],
                    ]

    lst_error_answers = []  # список для хранения строк где найдены неправильные ответы

    for idx, lst_values in enumerate(valid_values):
        mask = ~answers_df.iloc[:, idx].isin(lst_values)  # проверяем на допустимые значения
        # Получаем строки с отличающимися значениями
        result_check = answers_df.iloc[:, idx][mask]

        if len(result_check) != 0:
            error_row = list(map(lambda x: x + 2, result_check.index))
            error_row = list(map(str, error_row))
            error_row_lst = [f'В {idx + 1} вопросной колонке на строке {value}' for value in error_row]
            error_in_column = ','.join(error_row_lst)
            lst_error_answers.append(error_in_column)

    if len(lst_error_answers) != 0:
        error_message = ';'.join(lst_error_answers)
        raise BadValueKAF

    base_df[f'Значение_Избегание'] = answers_df.apply(calc_value_avoid_fail, axis=1)
    base_df['Уровень_Избегание'] = base_df['Значение_Избегание'].apply(calc_level_avoid_fail)  # Уровень Избегание







    base_df.to_excel('data/dgfd.xlsx')



