"""
Скрипт для обработки результатов Семантический дифференциал жизненной ситуации Александрова., Дерманова
"""

import pandas as pd
import re
from tkinter import messagebox
from lachesis_support_functions import round_mean_two,calc_count_scale,create_union_svod


class BadValueSDJSAD(Exception):
    """
    Исключение для неправильных значений в вариантах ответов
    """
    pass

class BadCountColumnsSDJSAD(Exception):
    """
    Исключение для обработки случая если количество колонок не равно 39
    """
    pass



def calc_value_vs(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [5,6,8,10,15,22,25,26,31,32,34]
    lst_neg = [5,6,8,10,15,22,25,26,31,32,34]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_pr:
            if idx not in lst_neg:
                value_forward += value
            else:
                if value == 1:
                    value_forward += 6
                elif value == 2:
                    value_forward += 5
                elif value == 3:
                    value_forward += 4
                elif value == 4:
                    value_forward += 3
                elif value == 5:
                    value_forward += 2
                else:
                    value_forward += 1

    return round(value_forward / len(lst_pr), 2)


def calc_level_vs(value):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """
    if value <2.89:
        return f'существенно пониженный уровень'
    elif 2.89 <= value < 4.12:
        return f'пониженный уровень'
    elif 4.12 <= value <= 5.35:
        return f'повышенный уровень'
    else:
        return f'существенно повышенный уровень'


def calc_value_aps(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [12,14,18,22,24,28,29,30,34]
    lst_neg = [12,14,18,22,24,28,30,34]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_pr:
            if idx not in lst_neg:
                value_forward += value
            else:
                if value == 1:
                    value_forward += 6
                elif value == 2:
                    value_forward += 5
                elif value == 3:
                    value_forward += 4
                elif value == 4:
                    value_forward += 3
                elif value == 5:
                    value_forward += 2
                else:
                    value_forward += 1

    return round(value_forward/len(lst_pr),2)


def calc_level_aps(value):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """
    if value < 2.7:
        return f'существенно пониженный уровень'
    elif  2.7<= value < 3.91:
        return f'пониженный уровень'
    elif  3.91<= value <= 5.12:
        return f'повышенный уровень'
    else:
        return f'существенно повышенный уровень'


def calc_value_pos(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [1,3,11,13,29,33]
    lst_neg = []
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_pr:
            if idx not in lst_neg:
                value_forward += value
            else:
                if value == 1:
                    value_forward += 6
                elif value == 2:
                    value_forward += 5
                elif value == 3:
                    value_forward += 4
                elif value == 4:
                    value_forward += 3
                elif value == 5:
                    value_forward += 2
                else:
                    value_forward += 1

    return round(value_forward/len(lst_pr),2)


def calc_level_pos(value):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """
    if value <2.9:
        return f'существенно пониженный уровень'
    elif  2.9<= value <4.03 :
        return f'пониженный уровень'
    elif  4.03<= value <= 5.16 :
        return f'повышенный уровень'
    else:
        return f'существенно повышенный уровень'


def calc_value_ops(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [21,23,27,37]
    lst_neg = [37]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_pr:
            if idx not in lst_neg:
                value_forward += value
            else:
                if value == 1:
                    value_forward += 6
                elif value == 2:
                    value_forward += 5
                elif value == 3:
                    value_forward += 4
                elif value == 4:
                    value_forward += 3
                elif value == 5:
                    value_forward += 2
                else:
                    value_forward += 1

    return round(value_forward/len(lst_pr),2)


def calc_level_ops(value):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """
    if value < 2.24:
        return f'существенно пониженный уровень'
    elif  2.24<= value < 3.44 :
        return f'пониженный уровень'
    elif  3.44<= value <=4.64 :
        return f'повышенный уровень'
    else:
        return f'существенно повышенный уровень'


def calc_value_rs(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [7,9,20,24,36]
    lst_neg = [7,9,20,24,36]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_pr:
            if idx not in lst_neg:
                value_forward += value
            else:
                if value == 1:
                    value_forward += 6
                elif value == 2:
                    value_forward += 5
                elif value == 3:
                    value_forward += 4
                elif value == 4:
                    value_forward += 3
                elif value == 5:
                    value_forward += 2
                else:
                    value_forward += 1

    return round(value_forward/len(lst_pr),2)


def calc_level_rs(value):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """
    if value <2.6:
        return f'существенно пониженный уровень'
    elif  2.6<= value < 3.80:
        return f'пониженный уровень'
    elif  3.80<= value <=5 :
        return f'повышенный уровень'
    else:
        return f'существенно повышенный уровень'


def calc_value_lvv(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [19,22,35]
    lst_neg = [19,22,35]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_pr:
            if idx not in lst_neg:
                value_forward += value
            else:
                if value == 1:
                    value_forward += 6
                elif value == 2:
                    value_forward += 5
                elif value == 3:
                    value_forward += 4
                elif value == 4:
                    value_forward += 3
                elif value == 5:
                    value_forward += 2
                else:
                    value_forward += 1

    return round(value_forward/len(lst_pr),2)


def calc_level_lvv(value):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """
    if value <2.46:
        return f'существенно пониженный уровень'
    elif  2.46<= value <3.84 :
        return f'пониженный уровень'
    elif  3.84<= value <=5.22 :
        return f'повышенный уровень'
    else:
        return f'существенно повышенный уровень'


def calc_value_azs(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [2,8]
    lst_neg = [2,8]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_pr:
            if idx not in lst_neg:
                value_forward += value
            else:
                if value == 1:
                    value_forward += 6
                elif value == 2:
                    value_forward += 5
                elif value == 3:
                    value_forward += 4
                elif value == 4:
                    value_forward += 3
                elif value == 5:
                    value_forward += 2
                else:
                    value_forward += 1

    return round(value_forward/len(lst_pr),2)


def calc_level_azs(value):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """
    if value <2.36:
        return f'существенно пониженный уровень'
    elif  2.36<= value <3.64 :
        return f'пониженный уровень'
    elif  3.64<= value <=4.92 :
        return f'повышенный уровень'
    else:
        return f'существенно повышенный уровень'


def calc_value_ups(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [16,17,38,39]
    lst_neg = [16,38,39]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_pr:
            if idx not in lst_neg:
                value_forward += value
            else:
                if value == 1:
                    value_forward += 6
                elif value == 2:
                    value_forward += 5
                elif value == 3:
                    value_forward += 4
                elif value == 4:
                    value_forward += 3
                elif value == 5:
                    value_forward += 2
                else:
                    value_forward += 1

    return round(value_forward/len(lst_pr),2)


def calc_level_ups(value):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """
    if value <2.42:
        return f'существенно пониженный уровень'
    elif  2.42<= value <3.65 :
        return f'пониженный уровень'
    elif  3.65<= value <= 4.88:
        return f'повышенный уровень'
    else:
        return f'существенно повышенный уровень'






def processing_sdjs_alex(base_df: pd.DataFrame, answers_df: pd.DataFrame, lst_svod_cols:list):
    """
    Функция для обработки
    :param base_df: часть датафрейма с описательными колонками
    :param answers_df: часть датафрейма с ответами
    :param lst_svod_cols:  список с колонками по которым нужно делать свод
    """
    count_descr_cols = base_df.shape[1] # количество анкетных колонок

    out_answer_df = base_df.copy()  # делаем копию для последующего соединения с сырыми ответами
    if len(answers_df.columns) != 39:  # проверяем количество колонок с вопросами
        raise BadCountColumnsSDJSAD

    answers_df.columns = [f'Состояние №{i}' for i in range(1, 40)]

    dct_replace_value = {'Пассивная на 3 балла':1,
                   'Пассивная на 2 балла':2,
                   'Пассивная на 1 балл':3,
                   'Активная на 1 балл':4,
                   'Активная на 2 балла':5,
                   'Активная на 3 балла':6,

                   'Возбуждающая на 3 балла':1,
                   'Возбуждающая на 2 балла':2,
                   'Возбуждающая на 1 балл':3,
                   'Расслабляющая на 1 балл':4,
                   'Расслабляющая на 2 балла':5,
                   'Расслабляющая на 3 балла':6,

                   'Равнодушная на 3 балла': 1,
                   'Равнодушная на 2 балла': 2,
                   'Равнодушная на 1 балл': 3,
                   'Отзывчивая на 1 балл': 4,
                   'Отзывчивая на 2 балла': 5,
                   'Отзывчивая на 3 балла': 6,

                   'Обратимая на 3 балла': 1,
                   'Обратимая на 2 балла': 2,
                   'Обратимая на 1 балл': 3,
                   'Безвозвратная на 1 балл': 4,
                   'Безвозвратная на 2 балла': 5,
                   'Безвозвратная на 3 балла': 6,

                   'Избавляющая на 3 балла': 1,
                   'Избавляющая на 2 балла': 2,
                   'Избавляющая на 1 балл': 3,
                   'Уничтожающая на 1 балл': 4,
                   'Уничтожающая на 2 балла': 5,
                   'Уничтожающая на 3 балла': 6,

                   'Сильная на 3 балла': 1,
                   'Сильная на 2 балла': 2,
                   'Сильная на 1 балл': 3,
                   'Слабая на 1 балл': 4,
                   'Слабая на 2 балла': 5,
                   'Слабая на 3 балла': 6,

                   'Легкая на 3 балла': 1,
                   'Легкая на 2 балла': 2,
                   'Легкая на 1 балл': 3,
                   'Трудная на 1 балл': 4,
                   'Трудная на 2 балла': 5,
                   'Трудная на 3 балла': 6,

                   'Логичная на 3 балла': 1,
                   'Логичная на 2 балла': 2,
                   'Логичная 1 балл': 3,
                   'Иррациональная на 1 балл': 4,
                   'Иррациональная на 2 балла': 5,
                   'Иррациональная на 3 балла': 6,

                   'Беспроигрышная на 3 балла': 1,
                   'Беспроигрышная на 2 балла': 2,
                   'Беспроигрышная на 1 балл': 3,
                   'Проигрышная на 1 балл': 4,
                   'Проигрышная на 2 балла': 5,
                   'Проигрышная на 3 балла': 6,

                   'Энергичная на 3 балла': 1,
                   'Энергичная на 2 балла': 2,
                   'Энергичная на 1 балл': 3,
                   'Вялая на 1 балл': 4,
                   'Вялая на 2 балла': 5,
                   'Вялая на 3 балла': 6,

                   'Безнадежная на 3 балла': 1,
                   'Безнадежная на 2 балла': 2,
                   'Безнадежная на 1 балл': 3,
                   'Обнадеживающая на 1 балл': 4,
                   'Обнадеживающая на 2 балла': 5,
                   'Обнадеживающая на 3 балла': 6,

                   'Оптимистичная на 3 балла': 1,
                   'Оптимистичная на 2 балла': 2,
                   'Оптимистичная на 1 балл': 3,
                   'Пессимистичная на 1 балл': 4,
                   'Пессимистичная на 2 балла': 5,
                   'Пессимистичная на 3 балла': 6,

                   'Жестокая на 3 балла': 1,
                   'Жестокая на 2 балла': 2,
                   'Жестокая на 1 балл': 3,
                   'Добрая на 1 балл': 4,
                   'Добрая на 2 балла': 5,
                   'Добрая на 3 балла': 6,

                   'Желанная на 3 балла': 1,
                   'Желанная на 2 балла': 2,
                   'Желанная на 1 балл': 3,
                   'Невыносимая на 1 балл': 4,
                   'Невыносимая на 2 балла': 5,
                   'Невыносимая на 3 балла': 6,

                   'Веселая на 3 балла': 1,
                   'Веселая на 2 балла': 2,
                   'Веселая на 1 балл': 3,
                   'Грустная на 1 балл': 4,
                   'Грустная на 2 балла': 5,
                   'Грустная на 3 балла': 6,

                   'Очевидная на 3 балла': 1,
                   'Очевидная на 2 балла': 2,
                   'Очевидная на 1 балл': 3,
                   'Таинственная на 1 балл': 4,
                   'Таинственная на 2 балла': 5,
                   'Таинственная на 3 балла': 6,

                   'Непонятная на 3 балла': 1,
                   'Непонятная на 2 балла': 2,
                   'Непонятная на 1 балл': 3,
                   'Понятная на 1 балл': 4,
                   'Понятная на 2 балла': 5,
                   'Понятная на 3 балла': 6,

                   'Значимая на 3 балла': 1,
                   'Значимая на 2 балла': 2,
                   'Значимая на 1 балл': 3,
                   'Незначимая на 1 балл': 4,
                   'Незначимая на 2 балла': 5,
                   'Незначимая на 3 балла': 6,

                   'Личная на 3 балла': 1,
                   'Личная на 2 балла': 2,
                   'Личная на 1 балл': 3,
                   'Публичная на 1 балл': 4,
                   'Публичная на 2 балла': 5,
                   'Публичная на 3 балла': 6,

                   'Разрешимая на 3 балла': 1,
                   'Разрешимая на 2 балла': 2,
                   'Разрешимая на 1 балл': 3,
                   'Неразрешимая на 1 балл': 4,
                   'Неразрешимая на 2 балла': 5,
                   'Неразрешимая на 3 балла': 6,

                   'Изменчивая на 3 балла': 1,
                   'Изменчивая на 2 балла': 2,
                   'Изменчивая на 1 балл': 3,
                   'Устойчивая на 1 балл': 4,
                   'Устойчивая на 2 балла': 5,
                   'Устойчивая на 3 балла': 6,

                   'Преодолимая на 3 балла': 1,
                   'Преодолимая на 2 балла': 2,
                   'Преодолимая на 1 балл': 3,
                   'Тупиковая на 1 балл': 4,
                   'Тупиковая на 2 балла': 5,
                   'Тупиковая на 3 балла': 6,

                   'Сложная на 3 балла': 1,
                   'Сложная на 2 балла': 2,
                   'Сложная на 1 балл': 3,
                   'Простая на 1 балл': 4,
                   'Простая на 2 балла': 5,
                   'Простая на 3 балла': 6,

                   'Добровольная на 3 балла': 1,
                   'Добровольная на 2 балла': 2,
                   'Добровольная на 1 балл': 3,
                   'Вынужденная на 1 балл': 4,
                   'Вынужденная на 2 балла': 5,
                   'Вынужденная на 3 балла': 6,

                   'Контролируемая на 3 балла': 1,
                   'Контролируемая на 2 балла': 2,
                   'Контролируемая на 1 балл': 3,
                   'Неконтролируемая на 1 балл': 4,
                   'Неконтролируемая на 2 балла': 5,
                   'Неконтролируемая на 3 балла': 6,

                   'Безопасная на 3 балла': 1,
                   'Безопасная на 2 балла': 2,
                   'Безопасная на 1 балл': 3,
                   'Угрожающая на 1 балл': 4,
                   'Угрожающая на 2 балла': 5,
                   'Угрожающая на 3 балла': 6,

                   'Острая на 3 балла': 1,
                   'Острая на 2 балла': 2,
                   'Острая на 1 балл': 3,
                   'Мягкая на 1 балл': 4,
                   'Мягкая на 2 балла': 5,
                   'Мягкая на 3 балла': 6,

                   'Приятная на 3 балла': 1,
                   'Приятная на 2 балла': 2,
                   'Приятная на 1 балл': 3,
                   'Ужасная на 1 балл': 4,
                   'Ужасная на 2 балла': 5,
                   'Ужасная на 3 балла': 6,

                   'Смертельная на 3 балла': 1,
                   'Смертельная на 2 балла': 2,
                   'Смертельная на 1 балл': 3,
                   'Жизнеутверждающая на 1 балл': 4,
                   'Жизнеутверждающая на 2 балла': 5,
                   'Жизнеутверждающая на 3 балла': 6,

                   'Близкая на 3 балла': 1,
                   'Близкая на 2 балла': 2,
                   'Близкая на 1 балл': 3,
                   'Далекая на 1 балл': 4,
                   'Далекая на 2 балла': 5,
                   'Далекая на 3 балла': 6,

                   'Дружественная на 3 балла': 1,
                   'Дружественная на 2 балла': 2,
                   'Дружественная на 1 балл': 3,
                   'Враждебная на 1 балл': 4,
                   'Враждебная на 2 балла': 5,
                   'Враждебная на 3 балла': 6,

                   'Освобождающая на 3 балла': 1,
                   'Освобождающая на 2 балла': 2,
                   'Освобождающая на 1 балл': 3,
                   'Сковывающая на 1 балл': 4,
                   'Сковывающая на 2 балла': 5,
                   'Сковывающая на 3 балла': 6,

                   'Пустая на 3 балла': 1,
                   'Пустая на 2 балла': 2,
                   'Пустая на 1 балл': 3,
                   'Информативная на 1 балл': 4,
                   'Информативная на 2 балла': 5,
                   'Информативная на 3 балла': 6,

                   'Принимающая на 3 балла': 1,
                   'Принимающая на 2 балла': 2,
                   'Принимающая на 1 балл': 3,
                   'Отвергающая на 1 балл': 4,
                   'Отвергающая на 2 балла': 5,
                   'Отвергающая на 3 балла': 6,

                   'Глубокая на 3 балла': 1,
                   'Глубокая на 2 балла': 2,
                   'Глубокая на 1 балл': 3,
                   'Поверхностная на 1 балл': 4,
                   'Поверхностная на 2 балла': 5,
                   'Поверхностная на 3 балла': 6,

                   'Определенная на 3 балла': 1,
                   'Определенная на 2 балла': 2,
                   'Определенная на 1 балл': 3,
                   'Неопределенная на 1 балл': 4,
                   'Неопределенная на 2 балла': 5,
                   'Неопределенная на 3 балла': 6,

                   'Уникальная на 3 балла': 1,
                   'Уникальная на 2 балла': 2,
                   'Уникальная на 1 балл': 3,
                   'Обычная на 1 балл': 4,
                   'Обычная на 2 балла': 5,
                   'Обычная на 3 балла': 6,

                   'Нормальная на 3 балла': 1,
                   'Нормальная на 2 балла': 2,
                   'Нормальная на 1 балл': 3,
                   'Отклоняющаяся от нормы на 1 балл': 4,
                   'Отклоняющаяся от нормы на 2 балла': 5,
                   'Отклоняющаяся от нормы на 3 балла': 6,

                   'Однозначная на 3 балла': 1,
                   'Однозначная на 2 балла': 2,
                   'Однозначная на 1 балл': 3,
                   'Многозначная на 1 балл': 4,
                   'Многозначная на 2 балла': 5,
                   'Многозначная на 3 балла': 6


    }

    valid_values = [1,2,3,4,5,6]
    answers_df.replace(dct_replace_value, inplace=True)  # заменяем слова на цифры для подсчетов
    # Проверяем, есть ли значения, отличающиеся от указанных в списке
    lst_error_answers = []  # список для хранения строк где найдены неправильные ответы

    for i in range(39):
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
        raise BadValueSDJSAD


    base_df['ВС_Значение'] = answers_df.apply(calc_value_vs, axis=1)
    base_df['ВС_Уровень'] = base_df['ВС_Значение'].apply(calc_level_vs)

    base_df['ЭПС_Значение'] = answers_df.apply(calc_value_aps, axis=1)
    base_df['ЭПС_Уровень'] = base_df['ЭПС_Значение'].apply(calc_level_aps)

    base_df['ПОС_Значение'] = answers_df.apply(calc_value_pos, axis=1)
    base_df['ПОС_Уровень'] = base_df['ЭПС_Значение'].apply(calc_level_pos)

    base_df['ОПС_Значение'] = answers_df.apply(calc_value_ops, axis=1)
    base_df['ОПС_Уровень'] = base_df['ОПС_Значение'].apply(calc_level_ops)

    base_df['РС_Значение'] = answers_df.apply(calc_value_rs, axis=1)
    base_df['РС_Уровень'] = base_df['РС_Значение'].apply(calc_level_rs)

    base_df['ЛВВ_Значение'] = answers_df.apply(calc_value_lvv, axis=1)
    base_df['ЛВВ_Уровень'] = base_df['ЛВВ_Значение'].apply(calc_level_lvv)

    base_df['ЭЗС_Значение'] = answers_df.apply(calc_value_azs, axis=1)
    base_df['ЭЗС_Уровень'] = base_df['ЭЗС_Значение'].apply(calc_level_azs)

    base_df['УПС_Значение'] = answers_df.apply(calc_value_ups, axis=1)
    base_df['УПС_Уровень'] = base_df['УПС_Значение'].apply(calc_level_ups)






    base_df.to_excel('data/res.xlsx')









