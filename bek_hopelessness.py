"""
Скрипт для обработки результатов теста Шкала безадежности Бека
"""
from lachesis_support_functions import round_mean
import pandas as pd
from tkinter import messagebox


class BadOrderBekHopelessness(Exception):
    """
    Исключение для обработки случая когда колонки не совпадают
    """
    pass


class BadValueBekHopelessness(Exception):
    """
    Исключение для неправильных значений в вариантах ответов
    """
    pass


def calc_value_hopelessness(row):
    """
    Функция для подсчета уровня безнадежности
    :param row: строка с ответами респондента
    :return:
    """
    value_hopelessness = 0 # счетчик безнадежности
    # обрабатываем
    if row[0] == 'НЕВЕРНО':
        value_hopelessness += 1
    if row[1] == 'ВЕРНО':
        value_hopelessness += 1
    if row[2] == 'НЕВЕРНО':
        value_hopelessness += 1
    if row[3] == 'ВЕРНО':
        value_hopelessness += 1
    if row[4] == 'НЕВЕРНО':
        value_hopelessness += 1

    if row[5] == 'НЕВЕРНО':
        value_hopelessness += 1
    if row[6] == 'ВЕРНО':
        value_hopelessness += 1
    if row[7] == 'НЕВЕРНО':
        value_hopelessness += 1
    if row[8] == 'ВЕРНО':
        value_hopelessness += 1
    if row[9] == 'НЕВЕРНО':
        value_hopelessness += 1

    if row[10] == 'ВЕРНО':
        value_hopelessness += 1
    if row[11] == 'ВЕРНО':
        value_hopelessness += 1
    if row[12] == 'НЕВЕРНО':
        value_hopelessness += 1
    if row[13] == 'ВЕРНО':
        value_hopelessness += 1
    if row[14] == 'НЕВЕРНО':
        value_hopelessness += 1

    if row[15] == 'ВЕРНО':
        value_hopelessness += 1
    if row[16] == 'ВЕРНО':
        value_hopelessness += 1
    if row[17] == 'ВЕРНО':
        value_hopelessness += 1
    if row[18] == 'НЕВЕРНО':
        value_hopelessness += 1
    if row[19] == 'ВЕРНО':
        value_hopelessness += 1

    return value_hopelessness

def calc_level_hopelessness(value):
    """
    Функция для вычисления уровня безнадежности
    :param value: числовое значение
    :return: строка с уровнем
    """
    if 0 <= value <= 3:
        return 'безнадёжность не выявлена'
    elif 4 <= value <= 8:
        return 'безнадежность лёгкая'
    elif 9 <= value <= 14:
        return 'безнадежность умеренная'
    elif value >= 15:
        return 'безнадежность тяжёлая'






def processing_bek_hopelessness(base_df: pd.DataFrame, answers_df: pd.DataFrame):
    # Словарь с проверочными данными
    lst_check_cols = ['Я жду будущего с надеждой и энтузиазмом',
                      'Мне пора сдаться, т.к. я ничего не могу изменить к лучшему',
                      'Когда дела идут плохо, мне помогает мысль, что так не может продолжаться всегда',
                      'Я не могу представить, на что будет похожа моя жизнь через 10 лет',
                      'У меня достаточно времени, чтобы завершить дела, которыми я больше всего хочу заниматься',
                      'В будущем, я надеюсь достичь успеха в том, что мне больше всего нравится',
                      'Будущее представляется мне во тьме',
                      'Я надеюсь получить в жизни больше хорошего, чем средний человек',
                      'У меня нет никаких просветов и нет причин верить, что они появятся в будущем',
                      'Мой прошлый опыт хорошо меня подготовил к будущему',
                      'Всё, что я вижу впереди - скорее, неприятности, чем радости',
                      'Я не надеюсь достичь того, чего действительно хочу',
                      'Когда я заглядываю в будущее, я надеюсь быть счастливее, чем я есть сейчас',
                      'Дела идут не так, как мне хочется',
                      'Я сильно верю в своё будущее',
                      'Я никогда не достигаю того, что хочу, поэтому глупо что-либо хотеть',
                      'Весьма маловероятно, что я получу реальное удовлетворение в будущем',
                      'Будущее представляется- мне расплывчатым и неопределённым',
                      'В будущем меня ждёт больше хороших дней, чем плохих',
                      'Бесполезно пытаться получить то, что я хочу, потому что, вероятно, я не добьюсь этого'
                      ]

    # Проверяем порядок колонок
    order_main_columns = lst_check_cols  # порядок колонок и названий как должно быть
    order_temp_df_columns = list(answers_df.columns)  # порядок колонок проверяемого файла
    error_order_lst = []  # список для несовпадающих пар
    # Сравниваем попарно колонки
    for main, temp in zip(order_main_columns, order_temp_df_columns):
        if main != temp:
            error_order_lst.append(f'На месте колонки {main} находится колонка {temp}')
    if len(error_order_lst) != 0:
        raise BadOrderBekHopelessness

    valid_values = ['ВЕРНО','НЕВЕРНО']

    # Проверяем, есть ли значения, отличающиеся от указанных в списке
    mask = ~answers_df.isin(valid_values)

    # Получаем строки с отличающимися значениями
    result_check = answers_df[mask.any(axis=1)]
    if len(result_check) != 0:
        error_row = list(map(lambda x: x + 2, result_check.index))
        error_row = list(map(str, error_row))
        error_message = ';'.join(error_row)
        raise BadValueBekHopelessness

    base_df['Значение_безнадежности'] = answers_df.apply(calc_value_hopelessness, axis=1)
    base_df['Уровень_безнадежности'] = base_df['Значение_безнадежности'].apply(calc_level_hopelessness)

    print(base_df)




    raise ZeroDivisionError