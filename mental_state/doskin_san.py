"""
Скрипт для обработки результатов теста Опросник САН Доскин Мирошников
"""

import pandas as pd
import re
from tkinter import messagebox
from lachesis_support_functions import round_mean,create_svod_sub


class BadValueDSAN(Exception):
    """
    Исключение для неправильных значений в вариантах ответов
    """
    pass

class BadCountColumnsDSAN(Exception):
    """
    Исключение для обработки случая если количество колонок не равно 30
    """
    pass



def calc_sub_value_well_being(row):
    """
    Функция для подсчета значения шкалы Самочувствие
    :param row: строка с ответами
    :return: число
    """
    lst_pr = [1,2,7,8,13,14,19,20,25,26]

    value_forward = 0

    for idx, value in enumerate(row):
        if idx +1 in lst_pr:
            if idx+1 == 1: # 1
                if value == 'Самочувствие хорошее на 3 балла':
                    value_forward += 7
                elif value == 'Самочувствие хорошее на 2 балла':
                    value_forward +=6
                elif value == 'Самочувствие хорошее на 1 балл':
                    value_forward +=5
                elif value == 'Затрудняюсь ответить':
                    value_forward +=4
                elif value == 'Самочувствие плохое на 1 балл':
                    value_forward +=3
                elif value == 'Самочувствие плохое на 2 балла':
                    value_forward +=2
                elif value == 'Самочувствие плохое на 3 балла':
                    value_forward +=1
            elif idx +1 == 2: # 2
                if value == 'Чувствую себя сильным на 3 балла':
                    value_forward += 7
                elif value == 'Чувствую себя сильным на 2 балла':
                    value_forward += 6
                elif value == 'Чувствую себя сильным на 1 балл':
                    value_forward += 5
                elif value == 'Затрудняюсь ответить':
                    value_forward += 4
                elif value == 'Чувствую себя слабым на 1 балл':
                    value_forward += 3
                elif value == 'Чувствую себя слабым на 2 балла':
                    value_forward += 2
                elif value == 'Чувствую себя слабым на 3 балла':
                    value_forward += 1
            elif idx + 1 == 7: #7
                if value == 'Работоспособный на 3 балла':
                    value_forward += 7
                elif value == 'Работоспособный на 2 балла':
                    value_forward += 6
                elif value == 'Работоспособный на 1 балл':
                    value_forward += 5
                elif value == 'Затрудняюсь ответить':
                    value_forward += 4
                elif value == 'Разбитый на 1 балл':
                    value_forward += 3
                elif value == 'Разбитый на 2 балла':
                    value_forward += 2
                elif value == 'Разбитый на 3 балла':
                    value_forward += 1
            elif idx +1 == 8: #8
                if value == 'Полный сил на 3 балла':
                    value_forward += 7
                elif value == 'Полный сил на 2 балла':
                    value_forward += 6
                elif value == 'Полный сил на 1 балл':
                    value_forward += 5
                elif value == 'Затрудняюсь ответить':
                    value_forward += 4
                elif value == 'Обессиленный на 1 балл':
                    value_forward += 3
                elif value == 'Обессиленный на 2 балла':
                    value_forward += 2
                elif value == 'Обессиленный на 3 балла':
                    value_forward += 1
            elif idx +1 == 13: #13
                if value == 'Напряженный на 3 балла':
                    value_forward += 7
                elif value == 'Напряженный на 2 балла':
                    value_forward += 6
                elif value == 'Напряженный на 1 балл':
                    value_forward += 5
                elif value == 'Затрудняюсь ответить':
                    value_forward += 4
                elif value == 'Расслабленный на 1 балл':
                    value_forward += 3
                elif value == 'Расслабленный на 2 балла':
                    value_forward += 2
                elif value == 'Расслабленный на 3 балла':
                    value_forward += 1
            elif idx+1 == 14: #14
                if value == 'Здоровый на 3 балла':
                    value_forward += 7
                elif value == 'Здоровый на 2 балла':
                    value_forward += 6
                elif value == 'Здоровый на 1 балл':
                    value_forward += 5
                elif value == 'Затрудняюсь ответить':
                    value_forward += 4
                elif value == 'Больной на 1 балл':
                    value_forward += 3
                elif value == 'Больной на 2 балла':
                    value_forward += 2
                elif value == 'Больной на 3 балла':
                    value_forward += 1
            elif idx+1 == 19: # 19
                if value == 'Отдохнувший на 3 балла':
                    value_forward += 7
                elif value == 'Отдохнувший на 2 балла':
                    value_forward += 6
                elif value == 'Отдохнувший на 1 балл':
                    value_forward += 5
                elif value == 'Затрудняюсь ответить':
                    value_forward += 4
                elif value == 'Усталый на 1 балл':
                    value_forward += 3
                elif value == 'Усталый на 2 балла':
                    value_forward += 2
                elif value == 'Усталый на 3 балла':
                    value_forward += 1
            elif idx+1 == 20: #20
                if value == 'Свежий на 3 балла':
                    value_forward += 7
                elif value == 'Свежий на 2 балла':
                    value_forward += 6
                elif value == 'Свежий на 1 балл':
                    value_forward += 5
                elif value == 'Затрудняюсь ответить':
                    value_forward += 4
                elif value == 'Изнуренный на 1 балл':
                    value_forward += 3
                elif value == 'Изнуренный на 2 балла':
                    value_forward += 2
                elif value == 'Изнуренный на 3 балла':
                    value_forward += 1
            elif idx + 1 == 25: #25
                if value == 'Выносливый на 3 балла':
                    value_forward += 7
                elif value == 'Выносливый на 2 балла':
                    value_forward += 6
                elif value == 'Выносливый на 1 балл':
                    value_forward += 5
                elif value == 'Затрудняюсь ответить':
                    value_forward += 4
                elif value == 'Утомляемый на 1 балл':
                    value_forward += 3
                elif value == 'Утомляемый на 2 балла':
                    value_forward += 2
                elif value == 'Утомляемый на 3 балла':
                    value_forward += 1
            elif idx+1 == 26: #26
                if value == 'Бодрый на 3 балла':
                    value_forward += 7
                elif value == 'Бодрый на 2 балла':
                    value_forward += 6
                elif value == 'Бодрый на 1 балл':
                    value_forward += 5
                elif value == 'Затрудняюсь ответить':
                    value_forward += 4
                elif value == 'Вялый на 1 балл':
                    value_forward += 3
                elif value == 'Вялый на 2 балла':
                    value_forward += 2
                elif value == 'Вялый на 3 балла':
                    value_forward += 1

    return round(value_forward/10,2)

def calc_level_sub(value):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """
    if 0 <= value <= 3.99:
        return 'не благоприятное состояние'
    elif 5.0 <= value <= 5.5:
        return 'нормальное состояние'
    else:
        return 'благоприятное состояние'




def calc_sub_value_activ(row):
    """
    Функция для подсчета значения шкалы Активность
    :param row: строка с ответами
    :return: число
    """
    lst_pr = [3,4,9,10,15,16,21,22,27,28]

    value_forward = 0

    for idx, value in enumerate(row):
        if idx +1 in lst_pr:
            if idx+1 == 3: # 3
                if value == 'Пассивный на 3 балла':
                    value_forward += 1
                elif value == 'Пассивный на 2 балла':
                    value_forward += 2
                elif value == 'Пассивный на 1 балл':
                    value_forward += 3
                elif value == 'Затрудняюсь ответить':
                    value_forward += 4
                elif value == 'Активный на 1 балл':
                    value_forward += 5
                elif value == 'Активный на 2 балла':
                    value_forward += 6
                elif value == 'Активный на 3 балла':
                    value_forward += 7
            elif idx +1 == 4: #4
                if value == 'Малоподвижный на 3 балла':
                    value_forward += 1
                elif value == 'Малоподвижный на 2 балла':
                    value_forward += 2
                elif value == 'Малоподвижный на 1 балл':
                    value_forward += 3
                elif value == 'Затрудняюсь ответить':
                    value_forward += 4
                elif value == 'Подвижный на 1 балл':
                    value_forward += 5
                elif value == 'Подвижный на 2 балла':
                    value_forward += 6
                elif value == 'Подвижный на 3 балла':
                    value_forward += 7
            elif idx+1 == 9: # 9
                if value == 'Медлительный на 3 балла':
                    value_forward += 1
                elif value == 'Медлительный на 2 балла':
                    value_forward += 2
                elif value == 'Медлительный на 1 балл':
                    value_forward += 3
                elif value == 'Затрудняюсь ответить':
                    value_forward += 4
                elif value == 'Быстрый на 1 балл':
                    value_forward += 5
                elif value == 'Быстрый на 2 балла':
                    value_forward += 6
                elif value == 'Быстрый на 3 балла':
                    value_forward += 7
            elif idx+1 == 10:
                if value == 'Бездеятельный на 3 балла':
                    value_forward += 1
                elif value == 'Бездеятельный на 2 балла':
                    value_forward += 2
                elif value == 'Бездеятельный на 1 балл':
                    value_forward += 3
                elif value == 'Затрудняюсь ответить':
                    value_forward += 4
                elif value == 'Деятельный на 1 балл':
                    value_forward += 5
                elif value == 'Деятельный на 2 балла':
                    value_forward += 6
                elif value == 'Деятельный на 3 балла':
                    value_forward += 7
            elif idx+1 == 15: # 15
                if value == 'Безучастный на 3 балла':
                    value_forward += 1
                elif value == 'Безучастный на 2 балла':
                    value_forward += 2
                elif value == 'Безучастный на 1 балл':
                    value_forward += 3
                elif value == 'Затрудняюсь ответить':
                    value_forward += 4
                elif value == 'Увлеченный на 1 балл':
                    value_forward += 5
                elif value == 'Увлеченный на 2 балла':
                    value_forward += 6
                elif value == 'Увлеченный на 3 балла':
                    value_forward += 7
            elif idx+1 == 16: #16
                if value == 'Равнодушный на 3 балла':
                    value_forward += 1
                elif value == 'Равнодушный на 2 балла':
                    value_forward += 2
                elif value == 'Равнодушный на 1 балл':
                    value_forward += 3
                elif value == 'Затрудняюсь ответить':
                    value_forward += 4
                elif value == 'Заинтересованный на 1 балл':
                    value_forward += 5
                elif value == 'Заинтересованный на 2 балла':
                    value_forward += 6
                elif value == 'Заинтересованный на 3 балла':
                    value_forward += 7

            elif idx+1 == 21: # 21
                if value == 'Сонливый на 3 балла':
                    value_forward += 1
                elif value == 'Сонливый на 2 балла':
                    value_forward += 2
                elif value == 'Сонливый на 1 балл':
                    value_forward += 3
                elif value == 'Затрудняюсь ответить':
                    value_forward += 4
                elif value == 'Возбужденный на 1 балл':
                    value_forward += 5
                elif value == 'Возбужденный на 2 балла':
                    value_forward += 6
                elif value == 'Возбужденный на 3 балла':
                    value_forward += 7
            elif idx+1 == 22: # 22
                if value == 'Желание отдохнуть на 3 балла':
                    value_forward += 1
                elif value == 'Желание отдохнуть на 2 балла':
                    value_forward += 2
                elif value == 'Желание отдохнуть на 1 балл':
                    value_forward += 3
                elif value == 'Затрудняюсь ответить':
                    value_forward += 4
                elif value == 'Желание работать на 1 балл':
                    value_forward += 5
                elif value == 'Желание работать на 2 балла':
                    value_forward += 6
                elif value == 'Желание работать на 3 балла':
                    value_forward += 7
            elif idx+1 == 27: # 27
                if value == 'Соображать трудно на 3 балла':
                    value_forward += 1
                elif value == 'Соображать трудно на 2 балла':
                    value_forward += 2
                elif value == 'Соображать трудно на 1 балл':
                    value_forward += 3
                elif value == 'Затрудняюсь ответить':
                    value_forward += 4
                elif value == 'Соображать легко на 1 балл':
                    value_forward += 5
                elif value == 'Соображать легко на 2 балла':
                    value_forward += 6
                elif value == 'Соображать легко на 3 балла':
                    value_forward += 7
            elif idx+1 == 28: # 28
                if value == 'Рассеянный на 3 балла':
                    value_forward += 1
                elif value == 'Рассеянный на 2 балла':
                    value_forward += 2
                elif value == 'Рассеянный на 1 балл':
                    value_forward += 3
                elif value == 'Затрудняюсь ответить':
                    value_forward += 4
                elif value == 'Внимательный на 1 балл':
                    value_forward += 5
                elif value == 'Внимательный на 2 балла':
                    value_forward += 6
                elif value == 'Внимательный на 3 балла':
                    value_forward += 7
    return round(value_forward/10,2)


def calc_sub_value_mood(row):
    """
    Функция для подсчета значения шкалы Активность
    :param row: строка с ответами
    :return: число
    """
    lst_pr = [5,6,11,12,17,18,23,24,29,30]

    value_forward = 0

    for idx, value in enumerate(row):
        if idx +1 in lst_pr:
            if idx+1 == 5: # 5
                if value == 'Веселый на 3 балла':
                    value_forward += 7
                elif value == 'Веселый на 2 балла':
                    value_forward += 6
                elif value == 'Веселый на 1 балл':
                    value_forward += 5
                elif value == 'Затрудняюсь ответить':
                    value_forward += 4
                elif value == 'Грустный на 1 балл':
                    value_forward += 3
                elif value == 'Грустный на 2 балла':
                    value_forward += 2
                elif value == 'Грустный на 3 балла':
                    value_forward += 1
            elif idx+1 == 6: # 6
                if value == 'Хорошее настроение на 3 балла':
                    value_forward += 7
                elif value == 'Хорошее настроение на 2 балла':
                    value_forward += 6
                elif value == 'Хорошее настроение на 1 балл':
                    value_forward += 5
                elif value == 'Затрудняюсь ответить':
                    value_forward += 4
                elif value == 'Плохое настроение на 1 балл':
                    value_forward += 3
                elif value == 'Плохое настроение на 2 балла':
                    value_forward += 2
                elif value == 'Плохое настроение на 3 балла':
                    value_forward += 1
            elif idx+1 == 11: # 11
                if value == 'Счастливый на 3 балла':
                    value_forward += 7
                elif value == 'Счастливый на 2 балла':
                    value_forward += 6
                elif value == 'Счастливый на 1 балл':
                    value_forward += 5
                elif value == 'Затрудняюсь ответить':
                    value_forward += 4
                elif value == 'Несчастный на 1 балл':
                    value_forward += 3
                elif value == 'Несчастный на 2 балла':
                    value_forward += 2
                elif value == 'Несчастный на 3 балла':
                    value_forward += 1
            elif idx+1 ==12: #12
                if value == 'Жизнерадостный на 3 балла':
                    value_forward += 7
                elif value == 'Жизнерадостный на 2 балла':
                    value_forward += 6
                elif value == 'Жизнерадостный на 1 балл':
                    value_forward += 5
                elif value == 'Затрудняюсь ответить':
                    value_forward += 4
                elif value == 'Мрачный на 1 балл':
                    value_forward += 3
                elif value == 'Мрачный на 2 балла':
                    value_forward += 2
                elif value == 'Мрачный на 3 балла':
                    value_forward += 1
            elif idx+1 == 17: #17
                if value == 'Восторженный на 3 балла':
                    value_forward += 7
                elif value == 'Восторженный на 2 балла':
                    value_forward += 6
                elif value == 'Восторженный на 1 балл':
                    value_forward += 5
                elif value == 'Затрудняюсь ответить':
                    value_forward += 4
                elif value == 'Унылый на 1 балл':
                    value_forward += 3
                elif value == 'Унылый на 2 балла':
                    value_forward += 2
                elif value == 'Унылый на 3 балла':
                    value_forward += 1
            elif idx+1 == 18: # 18
                if value == 'Радостный на 3 балла':
                    value_forward += 7
                elif value == 'Радостный на 2 балла':
                    value_forward += 6
                elif value == 'Радостный на 1 балл':
                    value_forward += 5
                elif value == 'Затрудняюсь ответить':
                    value_forward += 4
                elif value == 'Печальный на 1 балл':
                    value_forward += 3
                elif value == 'Печальный на 2 балла':
                    value_forward += 2
                elif value == 'Печальный на 3 балла':
                    value_forward += 1
            elif idx+1 == 23: #23
                if value == 'Спокойный на 3 балла':
                    value_forward += 7
                elif value == 'Спокойный на 2 балла':
                    value_forward += 6
                elif value == 'Спокойный на 1 балл':
                    value_forward += 5
                elif value == 'Затрудняюсь ответить':
                    value_forward += 4
                elif value == 'Взволнованный на 1 балл':
                    value_forward += 3
                elif value == 'Взволнованный на 2 балла':
                    value_forward += 2
                elif value == 'Взволнованный на 3 балла':
                    value_forward += 1
            elif idx+1 == 24: # 24
                if value == 'Оптимистичный на 3 балла':
                    value_forward += 7
                elif value == 'Оптимистичный на 2 балла':
                    value_forward += 6
                elif value == 'Оптимистичный на 1 балл':
                    value_forward += 5
                elif value == 'Затрудняюсь ответить':
                    value_forward += 4
                elif value == 'Пессимистичный на 1 балл':
                    value_forward += 3
                elif value == 'Пессимистичный на 2 балла':
                    value_forward += 2
                elif value == 'Пессимистичный на 3 балла':
                    value_forward += 1
            elif idx+1 == 29: #29
                if value == 'Полный надежд на 3 балла':
                    value_forward += 7
                elif value == 'Полный надежд на 2 балла':
                    value_forward += 6
                elif value == 'Полный надежд на 1 балл':
                    value_forward += 5
                elif value == 'Затрудняюсь ответить':
                    value_forward += 4
                elif value == 'Разочарованный на 1 балл':
                    value_forward += 3
                elif value == 'Разочарованный на 2 балла':
                    value_forward += 2
                elif value == 'Разочарованный на 3 балла':
                    value_forward += 1
            elif idx+1 == 30: # 30
                if value == 'Довольный на 3 балла':
                    value_forward += 7
                elif value == 'Довольный на 2 балла':
                    value_forward += 6
                elif value == 'Довольный на 1 балл':
                    value_forward += 5
                elif value == 'Затрудняюсь ответить':
                    value_forward += 4
                elif value == 'Недовольный на 1 балл':
                    value_forward += 3
                elif value == 'Недовольный на 2 балла':
                    value_forward += 2
                elif value == 'Недовольный на 3 балла':
                    value_forward += 1
    return round(value_forward/10,2)




















def processing_doskin_san(result_df: pd.DataFrame, answers_df: pd.DataFrame, lst_svod_cols:list):
    """
    Функция для обработки
    :param result_df: часть датафрейма с описательными колонками
    :param answers_df: часть датафрейма с ответами
    :param lst_svod_cols:  список с колонками по которым нужно делать свод
    """
    out_answer_df = result_df.copy()  # делаем копию для последующего соединения с сырыми ответами
    if len(answers_df.columns) != 30:  # проверяем количество колонок с вопросами
        raise BadCountColumnsDSAN

    answers_df.columns = [f'Состояние №{i}' for i in range(1,31)]

    valid_values = [['Самочувствие хорошее на 3 балла','Самочувствие хорошее на 2 балла','Самочувствие хорошее на 1 балл','Затрудняюсь ответить','Самочувствие плохое на 1 балл','Самочувствие плохое на 2 балла','Самочувствие плохое на 3 балла'],
                    ['Чувствую себя сильным на 3 балла','Чувствую себя сильным на 2 балла','Чувствую себя сильным на 1 балл','Затрудняюсь ответить','Чувствую себя слабым на 1 балл','Чувствую себя слабым на 2 балла','Чувствую себя слабым на 3 балла'],
                    ['Пассивный на 3 балла','Пассивный на 2 балла','Пассивный на 1 балл','Затрудняюсь ответить','Активный на 1 балл','Активный на 2 балла','Активный на 3 балла'],
                    ['Малоподвижный на 3 балла','Малоподвижный на 2 балла','Малоподвижный на 1 балл','Затрудняюсь ответить','Подвижный на 1 балл','Подвижный на 2 балла','Подвижный на 3 балла'],
                    ['Веселый на 3 балла','Веселый на 2 балла','Веселый на 1 балл','Затрудняюсь ответить','Грустный на 1 балл','Грустный на 2 балла','Грустный на 3 балла'],
                    ['Хорошее настроение на 3 балла','Хорошее настроение на 2 балла','Хорошее настроение на 1 балл','Затрудняюсь ответить','Плохое настроение на 1 балл','Плохое настроение на 2 балла','Плохое настроение на 3 балла'],
                    ['Работоспособный на 3 балла','Работоспособный на 2 балла','Работоспособный на 1 балл','Затрудняюсь ответить','Разбитый на 1 балл','Разбитый на 2 балла','Разбитый на 3 балла'],
                    ['Полный сил на 3 балла','Полный сил на 2 балла','Полный сил на 1 балл','Затрудняюсь ответить','Обессиленный на 1 балл','Обессиленный на 2 балла','Обессиленный на 3 балла'],
                    ['Медлительный на 3 балла','Медлительный на 2 балла','Медлительный на 1 балл','Затрудняюсь ответить','Быстрый на 1 балл','Быстрый на 2 балла','Быстрый на 3 балла'],
                    ['Бездеятельный на 3 балла','Бездеятельный на 2 балла','Бездеятельный на 1 балл','Затрудняюсь ответить','Деятельный на 1 балл','Деятельный на 2 балла','Деятельный на 3 балла'],
                    ['Счастливый на 3 балла','Счастливый на 2 балла','Счастливый на 1 балл','Затрудняюсь ответить','Несчастный на 1 балл','Несчастный на 2 балла','Несчастный на 3 балла'],
                    ['Жизнерадостный на 3 балла','Жизнерадостный на 2 балла','Жизнерадостный на 1 балл','Затрудняюсь ответить','Мрачный на 1 балл','Мрачный на 2 балла','Мрачный на 3 балла'],
                    ['Напряженный на 3 балла','Напряженный на 2 балла','Напряженный на 1 балл','Затрудняюсь ответить','Расслабленный на 1 балл','Расслабленный на 2 балла','Расслабленный на 3 балла'],
                    ['Здоровый на 3 балла','Здоровый на 2 балла','Здоровый на 1 балл','Затрудняюсь ответить','Больной на 1 балл','Больной на 2 балла','Больной на 3 балла'],
                    ['Безучастный на 3 балла','Безучастный на 2 балла','Безучастный на 1 балл','Затрудняюсь ответить','Увлеченный на 1 балл','Увлеченный на 2 балла','Увлеченный на 3 балла'],
                    ['Равнодушный на 3 балла','Равнодушный на 2 балла','Равнодушный на 1 балл','Затрудняюсь ответить','Заинтересованный на 1 балл','Заинтересованный на 2 балла','Заинтересованный на 3 балла'],
                    ['Восторженный на 3 балла','Восторженный на 2 балла','Восторженный на 1 балл','Затрудняюсь ответить','Унылый на 1 балл','Унылый на 2 балла','Унылый на 3 балла'],
                    ['Радостный на 3 балла','Радостный на 2 балла','Радостный на 1 балл','Затрудняюсь ответить','Печальный на 1 балл','Печальный на 2 балла','Печальный на 3 балла'],
                    ['Отдохнувший на 3 балла','Отдохнувший на 2 балла','Отдохнувший на 1 балл','Затрудняюсь ответить','Усталый на 1 балл','Усталый на 2 балла','Усталый на 3 балла'],
                    ['Свежий на 3 балла','Свежий на 2 балла','Свежий на 1 балл','Затрудняюсь ответить','Изнуренный на 1 балл','Изнуренный на 2 балла','Изнуренный на 3 балла'],
                    ['Сонливый на 3 балла','Сонливый на 2 балла','Сонливый на 1 балл','Затрудняюсь ответить','Возбужденный на 1 балл','Возбужденный на 2 балла','Возбужденный на 3 балла'],
                    ['Желание отдохнуть на 3 балла','Желание отдохнуть на 2 балла','Желание отдохнуть на 1 балл','Затрудняюсь ответить','Желание работать на 1 балл','Желание работать на 2 балла','Желание работать на 3 балла'],
                    ['Спокойный на 3 балла','Спокойный на 2 балла','Спокойный на 1 балл','Затрудняюсь ответить','Взволнованный на 1 балл','Взволнованный на 2 балла','Взволнованный на 3 балла'],
                    ['Оптимистичный на 3 балла','Оптимистичный на 2 балла','Оптимистичный на 1 балл','Затрудняюсь ответить','Пессимистичный на 1 балл','Пессимистичный на 2 балла','Пессимистичный на 3 балла'],
                    ['Выносливый на 3 балла','Выносливый на 2 балла','Выносливый на 1 балл','Затрудняюсь ответить','Утомляемый на 1 балл','Утомляемый на 2 балла','Утомляемый на 3 балла'],
                    ['Бодрый на 3 балла','Бодрый на 2 балла','Бодрый на 1 балл','Затрудняюсь ответить','Вялый на 1 балл','Вялый на 2 балла','Вялый на 3 балла'],
                    ['Соображать трудно на 3 балла','Соображать трудно на 2 балла','Соображать трудно на 1 балл','Затрудняюсь ответить','Соображать легко на 1 балл','Соображать легко на 2 балла','Соображать легко на 3 балла'],
                    ['Рассеянный на 3 балла','Рассеянный на 2 балла','Рассеянный на 1 балл','Затрудняюсь ответить','Внимательный на 1 балл','Внимательный на 2 балла','Внимательный на 3 балла'],
                    ['Полный надежд на 3 балла','Полный надежд на 2 балла','Полный надежд на 1 балл','Затрудняюсь ответить','Разочарованный на 1 балл','Разочарованный на 2 балла','Разочарованный на 3 балла'],
                    ['Довольный на 3 балла','Довольный на 2 балла','Довольный на 1 балл','Затрудняюсь ответить','Недовольный на 1 балл','Недовольный на 2 балла','Недовольный на 3 балла'],
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
        raise BadValueDSAN

    base_df = pd.DataFrame()
    base_df['Значение_шкалы_Самочувствие'] = answers_df.apply(calc_sub_value_well_being, axis=1)
    base_df['Уровень_шкалы_Самочувствие'] = base_df['Значение_шкалы_Самочувствие'].apply(calc_level_sub)

    base_df['Значение_шкалы_Активность'] = answers_df.apply(calc_sub_value_activ, axis=1)
    base_df['Уровень_шкалы_Активность'] = base_df['Значение_шкалы_Активность'].apply(calc_level_sub)

    base_df['Значение_шкалы_Настроение'] = answers_df.apply(calc_sub_value_mood, axis=1)
    base_df['Уровень_шкалы_Настроение'] = base_df['Значение_шкалы_Настроение'].apply(calc_level_sub)




    base_df.to_excel('res.xlsx')











