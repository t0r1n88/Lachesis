"""
Скрипт для обработки результатов теста Методика многомерной оценки детской тревожности Ромицына Вассерман
"""

import pandas as pd
import re
from tkinter import messagebox
from lachesis_support_functions import round_mean_two,calc_count_scale,create_list_on_level,create_union_svod


class BadOrderMODTRV(Exception):
    """
    Исключение для обработки случая когда колонки не совпадают
    """
    pass


class BadValueMODTRV(Exception):
    """
    Исключение для неправильных значений в вариантах ответов
    """
    pass

class BadCountColumnsMODTRV(Exception):
    """
    Исключение для обработки случая если количество колонок не равно 100
    """
    pass


class NotReqColumnMODTRV(Exception):
    """
    Исключение для обработки случая когда нет обязательных колонок Пол И ФИО
    """
    pass

class BadValueSexMODTRV(Exception):
    """
    Исключение для обработки случая когда в колонке Пол есть значения отличающиеся от Мужской или Женский
    """
    pass

class BadValueAgeMODTRV(Exception):
    """
    Исключение для обработки случая когда в колонке Возраст есть значения отличающиеся от-7-10 лет, 11-12 лет, 13-14 лет, 15-17 лет
    """
    pass



def calc_value_ot(row):
    """
    Функция для подсчета значения
    :return: число
    """
    value_forward = 0  # результат
    for idx, value in enumerate(row):
        if value == 'да':
            value_forward += 1

    return value_forward

def calc_level_ot(ser:pd.Series):
    """
    Функция для подсчета уровня общей тревожности
    :param ser: пол,возраст и значение
    :param dct_value: словарь со значениями перевода
    :return:
    """
    row = ser.tolist() # превращаем в список
    sex = row[0] # пол
    age = row[1] # возраст
    value = row[2] # значение для обработки

    if sex == 'Мужской':
        if age == '7-10 лет':
            if 0 <= value <= 1:
                return 'низкий уровень тревоги'
            elif 2 <= value <= 6:
                return 'средний уровень тревоги'
            elif 7 <= value <= 8:
                return 'высокий уровень тревоги'
            else:
                return 'крайне высокий уровень тревоги'
        elif age == '11-12 лет':
            if 0 <= value <= 1:
                return 'низкий уровень тревоги'
            elif 2 <= value <= 5:
                return 'средний уровень тревоги'
            elif 6 <= value <= 7:
                return 'высокий уровень тревоги'
            else:
                return 'крайне высокий уровень тревоги'
        elif age == '13-14 лет':
            if 0 <= value <= 1:
                return 'низкий уровень тревоги'
            elif 2 <= value <= 4:
                return 'средний уровень тревоги'
            elif 5 <= value <= 7:
                return 'высокий уровень тревоги'
            else:
                return 'крайне высокий уровень тревоги'
        else:
            if value == 0:
                return 'низкий уровень тревоги'
            elif 1 <= value <= 4:
                return 'средний уровень тревоги'
            elif 5 <= value <= 6:
                return 'высокий уровень тревоги'
            else:
                return 'крайне высокий уровень тревоги'
    else:
        if age == '7-10 лет':
            if 0 <= value <= 2:
                return 'низкий уровень тревоги'
            elif 3 <= value <= 7:
                return 'средний уровень тревоги'
            elif 8 <= value <= 9:
                return 'высокий уровень тревоги'
            else:
                return 'крайне высокий уровень тревоги'
        elif age == '11-12 лет':
            if 0 <= value <= 1:
                return 'низкий уровень тревоги'
            elif 2 <= value <= 6:
                return 'средний уровень тревоги'
            elif 7 <= value <= 8:
                return 'высокий уровень тревоги'
            else:
                return 'крайне высокий уровень тревоги'
        elif age == '13-14 лет':
            if 0 <= value <= 1:
                return 'низкий уровень тревоги'
            elif 2 <= value <= 5:
                return 'средний уровень тревоги'
            elif 6 <= value <= 7:
                return 'высокий уровень тревоги'
            else:
                return 'крайне высокий уровень тревоги'
        else:
            if 0 <= value <= 1:
                return 'низкий уровень тревоги'
            elif 2 <= value <= 5:
                return 'средний уровень тревоги'
            elif 6 <= value <= 7:
                return 'высокий уровень тревоги'
            else:
                return 'крайне высокий уровень тревоги'



def calc_value_tvvss(row):
    """
    Функция для подсчета значения Тревога во взаимоотношениях со сверстниками
    :return: число
    """
    value_forward = 0  # результат
    lst_pos = [2,12,22,52,72,82]
    lst_neg = [32,42,62,92]
    for idx, value in enumerate(row,1):
        if idx in lst_neg:
            if value == 'нет':
                value_forward += 1
        elif idx in lst_pos:
            if value == 'да':
                value_forward += 1

    return value_forward


def calc_level_tvvss(ser:pd.Series):
    """
    Функция для подсчета уровня
    :param ser: пол,возраст и значение
    :return:
    """
    row = ser.tolist() # превращаем в список
    sex = row[0] # пол
    age = row[1] # возраст
    value = row[2] # значение для обработки
    if sex == 'Мужской':
        if age == '7-10 лет':
            if 0 <= value <= 1:
                return 'низкий уровень тревоги'
            elif 2 <= value <= 6:
                return 'средний уровень тревоги'
            elif 7 <= value <= 8:
                return 'высокий уровень тревоги'
            else:
                return 'крайне высокий уровень тревоги'
        elif age == '11-12 лет':
            if 0 <= value <= 1:
                return 'низкий уровень тревоги'
            elif 2 <= value <= 5:
                return 'средний уровень тревоги'
            elif 6 <= value <= 7:
                return 'высокий уровень тревоги'
            else:
                return 'крайне высокий уровень тревоги'
        elif age == '13-14 лет':
            if 0 <= value <= 1:
                return 'низкий уровень тревоги'
            elif 2 <= value <= 5:
                return 'средний уровень тревоги'
            elif 6 <= value <= 7:
                return 'высокий уровень тревоги'
            else:
                return 'крайне высокий уровень тревоги'
        else:
            if 0 <= value <= 1 :
                return 'низкий уровень тревоги'
            elif 2 <= value <= 5:
                return 'средний уровень тревоги'
            elif 6 <= value <= 7:
                return 'высокий уровень тревоги'
            else:
                return 'крайне высокий уровень тревоги'
    else:
        if age == '7-10 лет':
            if 0 <= value <= 2:
                return 'низкий уровень тревоги'
            elif 3 <= value <= 6:
                return 'средний уровень тревоги'
            elif 7 <= value <= 8:
                return 'высокий уровень тревоги'
            else:
                return 'крайне высокий уровень тревоги'
        elif age == '11-12 лет':
            if 0 <= value <= 1:
                return 'низкий уровень тревоги'
            elif 2 <= value <= 6:
                return 'средний уровень тревоги'
            elif value == 7:
                return 'высокий уровень тревоги'
            else:
                return 'крайне высокий уровень тревоги'
        elif age == '13-14 лет':
            if 0 <= value <= 1:
                return 'низкий уровень тревоги'
            elif 2 <= value <= 5:
                return 'средний уровень тревоги'
            elif 6 <= value <= 7:
                return 'высокий уровень тревоги'
            else:
                return 'крайне высокий уровень тревоги'
        else:
            if 0 <= value <= 1:
                return 'низкий уровень тревоги'
            elif 2 <= value <= 5:
                return 'средний уровень тревоги'
            elif 6 <= value <= 7:
                return 'высокий уровень тревоги'
            else:
                return 'крайне высокий уровень тревоги'



def calc_value_tvssoo(row):
    """
    Функция для подсчета значения Тревога в связи с оценкой окружающих
    :return: число
    """
    value_forward = 0  # результат
    lst_pos = [3,13,23,33,43,53,63,83,93]
    lst_neg = [73]
    for idx, value in enumerate(row,1):
        if idx in lst_neg:
            if value == 'нет':
                value_forward += 1
        elif idx in lst_pos:
            if value == 'да':
                value_forward += 1

    return value_forward




def calc_level_tvssoo(ser:pd.Series):
    """
    Функция для подсчета уровня
    :param ser: пол,возраст и значение
    :return:
    """
    row = ser.tolist() # превращаем в список
    sex = row[0] # пол
    age = row[1] # возраст
    value = row[2] # значение для обработки
    if sex == 'Мужской':
        if age == '7-10 лет':
            if 0 <= value <= 2:
                return 'низкий уровень тревоги'
            elif 3 <= value <= 6:
                return 'средний уровень тревоги'
            elif 7 <= value <= 8:
                return 'высокий уровень тревоги'
            else:
                return 'крайне высокий уровень тревоги'
        elif age == '11-12 лет':
            if 0 <= value <= 1:
                return 'низкий уровень тревоги'
            elif 2 <= value <= 6:
                return 'средний уровень тревоги'
            elif 7 <= value <= 8:
                return 'высокий уровень тревоги'
            else:
                return 'крайне высокий уровень тревоги'
        elif age == '13-14 лет':
            if 0 <= value <= 1:
                return 'низкий уровень тревоги'
            elif 2 <= value <= 6:
                return 'средний уровень тревоги'
            elif 7 <= value <= 8:
                return 'высокий уровень тревоги'
            else:
                return 'крайне высокий уровень тревоги'
        else:
            if 0 <= value <= 1:
                return 'низкий уровень тревоги'
            elif 2 <= value <= 5:
                return 'средний уровень тревоги'
            elif 6 <= value <= 8:
                return 'высокий уровень тревоги'
            else:
                return 'крайне высокий уровень тревоги'
    else:
        if age == '7-10 лет':
            if 0 <= value <= 3:
                return 'низкий уровень тревоги'
            elif 4 <= value <= 8:
                return 'средний уровень тревоги'
            elif  value == 9:
                return 'высокий уровень тревоги'
            else:
                return 'крайне высокий уровень тревоги'
        elif age == '11-12 лет':
            if 0 <= value <= 2:
                return 'низкий уровень тревоги'
            elif 3 <= value <= 6:
                return 'средний уровень тревоги'
            elif 7 <= value <= 8:
                return 'высокий уровень тревоги'
            else:
                return 'крайне высокий уровень тревоги'
        elif age == '13-14 лет':
            if 0 <= value <= 2:
                return 'низкий уровень тревоги'
            elif 3 <= value <= 7:
                return 'средний уровень тревоги'
            elif  value == 8:
                return 'высокий уровень тревоги'
            else:
                return 'крайне высокий уровень тревоги'
        else:
            if 0 <= value <= 1:
                return 'низкий уровень тревоги'
            elif 2 <= value <= 6:
                return 'средний уровень тревоги'
            elif 7 <= value <= 8:
                return 'высокий уровень тревоги'
            else:
                return 'крайне высокий уровень тревоги'




def calc_value_tvvsu(row):
    """
    Функция для подсчета значения Тревога во взаимоотношениях с учителями
    :return: число
    """
    value_forward = 0  # результат
    lst_pos = [4,24,34,44,54,64,74,84,94]
    lst_neg = [14]
    for idx, value in enumerate(row,1):
        if idx in lst_neg:
            if value == 'нет':
                value_forward += 1
        elif idx in lst_pos:
            if value == 'да':
                value_forward += 1

    return value_forward


def calc_level_tvvsu(ser:pd.Series):
    """
    Функция для подсчета уровня
    :param ser: пол,возраст и значение
    :return:
    """
    row = ser.tolist() # превращаем в список
    sex = row[0] # пол
    age = row[1] # возраст
    value = row[2] # значение для обработки
    if sex == 'Мужской':
        if age == '7-10 лет':
            if 0 <= value <= 2:
                return 'низкий уровень тревоги'
            elif 3 <= value <= 6:
                return 'средний уровень тревоги'
            elif 7 <= value <= 8:
                return 'высокий уровень тревоги'
            else:
                return 'крайне высокий уровень тревоги'
        elif age == '11-12 лет':
            if 0 <= value <= 1:
                return 'низкий уровень тревоги'
            elif 2 <= value <= 6:
                return 'средний уровень тревоги'
            elif 7 <= value <= 8:
                return 'высокий уровень тревоги'
            else:
                return 'крайне высокий уровень тревоги'
        elif age == '13-14 лет':
            if 0 <= value <= 1:
                return 'низкий уровень тревоги'
            elif 2 <= value <= 6:
                return 'средний уровень тревоги'
            elif 7 <= value <= 8:
                return 'высокий уровень тревоги'
            else:
                return 'крайне высокий уровень тревоги'
        else:
            if 0 <= value <= 1:
                return 'низкий уровень тревоги'
            elif 2 <= value <= 5:
                return 'средний уровень тревоги'
            elif 6 <= value <= 7:
                return 'высокий уровень тревоги'
            else:
                return 'крайне высокий уровень тревоги'
    else:
        if age == '7-10 лет':
            if 0 <= value <= 3:
                return 'низкий уровень тревоги'
            elif 4 <= value <= 7:
                return 'средний уровень тревоги'
            elif  value == 8:
                return 'высокий уровень тревоги'
            else:
                return 'крайне высокий уровень тревоги'
        elif age == '11-12 лет':
            if 0 <= value <= 1:
                return 'низкий уровень тревоги'
            elif 2 <= value <= 6:
                return 'средний уровень тревоги'
            elif 7 <= value <= 8:
                return 'высокий уровень тревоги'
            else:
                return 'крайне высокий уровень тревоги'
        elif age == '13-14 лет':
            if 0 <= value <= 1:
                return 'низкий уровень тревоги'
            elif 2 <= value <= 5:
                return 'средний уровень тревоги'
            elif 6 <= value <= 7:
                return 'высокий уровень тревоги'
            else:
                return 'крайне высокий уровень тревоги'
        else:
            if 0 <= value <= 1:
                return 'низкий уровень тревоги'
            elif 2 <= value <= 5:
                return 'средний уровень тревоги'
            elif 6 <= value <= 7:
                return 'высокий уровень тревоги'
            else:
                return 'крайне высокий уровень тревоги'


def calc_value_tvvsr(row):
    """
    Функция для подсчета значения Тревога во взаимоотношениях с родителями
    :return: число
    """
    value_forward = 0  # результат
    lst_pos = [25,45,75,85,95]
    lst_neg = [5,15,35,55,65]
    for idx, value in enumerate(row,1):
        if idx in lst_neg:
            if value == 'нет':
                value_forward += 1
        elif idx in lst_pos:
            if value == 'да':
                value_forward += 1

    return value_forward


def calc_level_tvvsr(ser:pd.Series):
    """
    Функция для подсчета уровня
    :param ser: пол,возраст и значение
    :return:
    """
    row = ser.tolist() # превращаем в список
    sex = row[0] # пол
    age = row[1] # возраст
    value = row[2] # значение для обработки
    if sex == 'Мужской':
        if age == '7-10 лет':
            if 0 <= value <= 2:
                return 'низкий уровень тревоги'
            elif 3 <= value <= 6:
                return 'средний уровень тревоги'
            elif  value == 7:
                return 'высокий уровень тревоги'
            else:
                return 'крайне высокий уровень тревоги'
        elif age == '11-12 лет':
            if 0 <= value <= 1:
                return 'низкий уровень тревоги'
            elif 2 <= value <= 5:
                return 'средний уровень тревоги'
            elif 6 <= value <= 7:
                return 'высокий уровень тревоги'
            else:
                return 'крайне высокий уровень тревоги'
        elif age == '13-14 лет':
            if 0 <= value <= 2:
                return 'низкий уровень тревоги'
            elif 3 <= value <= 6:
                return 'средний уровень тревоги'
            elif 7 <= value <= 8:
                return 'высокий уровень тревоги'
            else:
                return 'крайне высокий уровень тревоги'
        else:
            if 0 <= value <= 2:
                return 'низкий уровень тревоги'
            elif 3 <= value <= 6:
                return 'средний уровень тревоги'
            elif 7 <= value <= 9:
                return 'высокий уровень тревоги'
            else:
                return 'крайне высокий уровень тревоги'
    else:
        if age == '7-10 лет':
            if 0 <= value <= 2:
                return 'низкий уровень тревоги'
            elif 3 <= value <= 6:
                return 'средний уровень тревоги'
            elif 7 <= value <= 8:
                return 'высокий уровень тревоги'
            else:
                return 'крайне высокий уровень тревоги'
        elif age == '11-12 лет':
            if 0 <= value <= 1:
                return 'низкий уровень тревоги'
            elif 2 <= value <= 6:
                return 'средний уровень тревоги'
            elif  value == 7:
                return 'высокий уровень тревоги'
            else:
                return 'крайне высокий уровень тревоги'
        elif age == '13-14 лет':
            if 0 <= value <= 1:
                return 'низкий уровень тревоги'
            elif 2 <= value <= 6:
                return 'средний уровень тревоги'
            elif 7 <= value <= 8:
                return 'высокий уровень тревоги'
            else:
                return 'крайне высокий уровень тревоги'
        else:
            if 0 <= value <= 1:
                return 'низкий уровень тревоги'
            elif 2 <= value <= 6:
                return 'средний уровень тревоги'
            elif 7 <= value <= 8:
                return 'высокий уровень тревоги'
            else:
                return 'крайне высокий уровень тревоги'


def calc_value_tssuvo(row):
    """
    Функция для подсчета значения Тревога, связанная с успешностью в обучении
    :return: число
    """
    value_forward = 0  # результат
    lst_pos = [6,16,26,36,46,56,76,86,96]
    lst_neg = [66]
    for idx, value in enumerate(row,1):
        if idx in lst_neg:
            if value == 'нет':
                value_forward += 1
        elif idx in lst_pos:
            if value == 'да':
                value_forward += 1

    return value_forward


def calc_level_tssuvo(ser:pd.Series):
    """
    Функция для подсчета уровня
    :param ser: пол,возраст и значение
    :return:
    """
    row = ser.tolist() # превращаем в список
    sex = row[0] # пол
    age = row[1] # возраст
    value = row[2] # значение для обработки
    if sex == 'Мужской':
        if age == '7-10 лет':
            if 0 <= value <= 2:
                return 'низкий уровень тревоги'
            elif 3 <= value <= 6:
                return 'средний уровень тревоги'
            elif value == 7:
                return 'высокий уровень тревоги'
            else:
                return 'крайне высокий уровень тревоги'
        elif age == '11-12 лет':
            if 0 <= value <= 2:
                return 'низкий уровень тревоги'
            elif 3 <= value <= 5:
                return 'средний уровень тревоги'
            elif 6 <= value <= 7:
                return 'высокий уровень тревоги'
            else:
                return 'крайне высокий уровень тревоги'
        elif age == '13-14 лет':
            if 0 <= value <= 1:
                return 'низкий уровень тревоги'
            elif 2 <= value <= 5:
                return 'средний уровень тревоги'
            elif 6 <= value <= 7:
                return 'высокий уровень тревоги'
            else:
                return 'крайне высокий уровень тревоги'
        else:
            if 0 <= value <= 1:
                return 'низкий уровень тревоги'
            elif 2 <= value <= 5:
                return 'средний уровень тревоги'
            elif 6 <= value <= 7:
                return 'высокий уровень тревоги'
            else:
                return 'крайне высокий уровень тревоги'
    else:
        if age == '7-10 лет':
            if 0 <= value <= 2:
                return 'низкий уровень тревоги'
            elif 3 <= value <= 7:
                return 'средний уровень тревоги'
            elif value == 8:
                return 'высокий уровень тревоги'
            else:
                return 'крайне высокий уровень тревоги'
        elif age == '11-12 лет':
            if 0 <= value <= 1:
                return 'низкий уровень тревоги'
            elif 2 <= value <= 5:
                return 'средний уровень тревоги'
            elif 6 <= value <= 7:
                return 'высокий уровень тревоги'
            else:
                return 'крайне высокий уровень тревоги'
        elif age == '13-14 лет':
            if 0 <= value <= 1:
                return 'низкий уровень тревоги'
            elif 2 <= value <= 5:
                return 'средний уровень тревоги'
            elif value == 6:
                return 'высокий уровень тревоги'
            else:
                return 'крайне высокий уровень тревоги'
        else:
            if 0 <= value <= 1:
                return 'низкий уровень тревоги'
            elif 2 <= value <= 4:
                return 'средний уровень тревоги'
            elif 5 <= value <= 6:
                return 'высокий уровень тревоги'
            else:
                return 'крайне высокий уровень тревоги'



def calc_value_tvvssv(row):
    """
    Функция для подсчета значения Тревога, возникающая в ситуациях самовыражения
    :return: число
    """
    value_forward = 0  # результат
    lst_pos = [7,17,27,37,47,57,67,87,97]
    lst_neg = [77]
    for idx, value in enumerate(row,1):
        if idx in lst_neg:
            if value == 'нет':
                value_forward += 1
        elif idx in lst_pos:
            if value == 'да':
                value_forward += 1

    return value_forward



def calc_level_tvvssv(ser:pd.Series):
    """
    Функция для подсчета уровня
    :param ser: пол,возраст и значение
    :return:
    """
    row = ser.tolist() # превращаем в список
    sex = row[0] # пол
    age = row[1] # возраст
    value = row[2] # значение для обработки
    if sex == 'Мужской':
        if age == '7-10 лет':
            if 0 <= value <= 2:
                return 'низкий уровень тревоги'
            elif 3 <= value <= 6:
                return 'средний уровень тревоги'
            elif 7 <= value <= 8:
                return 'высокий уровень тревоги'
            else:
                return 'крайне высокий уровень тревоги'
        elif age == '11-12 лет':
            if 0 <= value <= 1:
                return 'низкий уровень тревоги'
            elif 2 <= value <= 6:
                return 'средний уровень тревоги'
            elif 7 <= value <= 8:
                return 'высокий уровень тревоги'
            else:
                return 'крайне высокий уровень тревоги'
        elif age == '13-14 лет':
            if 0 <= value <= 1:
                return 'низкий уровень тревоги'
            elif 2 <= value <= 5:
                return 'средний уровень тревоги'
            elif 6 <= value <= 8:
                return 'высокий уровень тревоги'
            else:
                return 'крайне высокий уровень тревоги'
        else:
            if 0 <= value <= 1:
                return 'низкий уровень тревоги'
            elif 2 <= value <= 5:
                return 'средний уровень тревоги'
            elif 6 <= value <= 7:
                return 'высокий уровень тревоги'
            else:
                return 'крайне высокий уровень тревоги'
    else:
        if age == '7-10 лет':
            if 0 <= value <= 3:
                return 'низкий уровень тревоги'
            elif 4 <= value <= 8:
                return 'средний уровень тревоги'
            elif value == 9:
                return 'высокий уровень тревоги'
            else:
                return 'крайне высокий уровень тревоги'
        elif age == '11-12 лет':
            if 0 <= value <= 2:
                return 'низкий уровень тревоги'
            elif 3 <= value <= 6:
                return 'средний уровень тревоги'
            elif 7 <= value <= 8:
                return 'высокий уровень тревоги'
            else:
                return 'крайне высокий уровень тревоги'
        elif age == '13-14 лет':
            if 0 <= value <= 1:
                return 'низкий уровень тревоги'
            elif 2 <= value <= 5:
                return 'средний уровень тревоги'
            elif 6 <= value <= 7:
                return 'высокий уровень тревоги'
            else:
                return 'крайне высокий уровень тревоги'
        else:
            if 0 <= value <= 1:
                return 'низкий уровень тревоги'
            elif 2 <= value <= 5:
                return 'средний уровень тревоги'
            elif 6 <= value <= 7:
                return 'высокий уровень тревоги'
            else:
                return 'крайне высокий уровень тревоги'



def calc_value_tvvspz(row):
    """
    Функция для подсчета значения Тревога, возникающая в ситуациях проверки знаний
    :return: число
    """
    value_forward = 0  # результат
    lst_pos = [8,18,28,38,48,68,78,88,98]
    lst_neg = [58]
    for idx, value in enumerate(row,1):
        if idx in lst_neg:
            if value == 'нет':
                value_forward += 1
        elif idx in lst_pos:
            if value == 'да':
                value_forward += 1

    return value_forward


def calc_level_tvvspz(ser:pd.Series):
    """
    Функция для подсчета уровня
    :param ser: пол,возраст и значение
    :return:
    """
    row = ser.tolist() # превращаем в список
    sex = row[0] # пол
    age = row[1] # возраст
    value = row[2] # значение для обработки
    if sex == 'Мужской':
        if age == '7-10 лет':
            if 0 <= value <= 2:
                return 'низкий уровень тревоги'
            elif 3 <= value <= 7:
                return 'средний уровень тревоги'
            elif 8 <= value <= 9:
                return 'высокий уровень тревоги'
            else:
                return 'крайне высокий уровень тревоги'
        elif age == '11-12 лет':
            if 0 <= value <= 1:
                return 'низкий уровень тревоги'
            elif 2 <= value <= 6:
                return 'средний уровень тревоги'
            elif 7 <= value <= 8:
                return 'высокий уровень тревоги'
            else:
                return 'крайне высокий уровень тревоги'
        elif age == '13-14 лет':
            if 0 <= value <= 1:
                return 'низкий уровень тревоги'
            elif 2 <= value <= 6:
                return 'средний уровень тревоги'
            elif 7 <= value <= 8:
                return 'высокий уровень тревоги'
            else:
                return 'крайне высокий уровень тревоги'
        else:
            if 0 <= value <= 1:
                return 'низкий уровень тревоги'
            elif 2 <= value <= 5:
                return 'средний уровень тревоги'
            elif 6 <= value <= 7:
                return 'высокий уровень тревоги'
            else:
                return 'крайне высокий уровень тревоги'
    else:
        if age == '7-10 лет':
            if 0 <= value <= 3:
                return 'низкий уровень тревоги'
            elif 4 <= value <= 8:
                return 'средний уровень тревоги'
            elif value == 9:
                return 'высокий уровень тревоги'
            else:
                return 'крайне высокий уровень тревоги'
        elif age == '11-12 лет':
            if 0 <= value <= 2:
                return 'низкий уровень тревоги'
            elif 3 <= value <= 7:
                return 'средний уровень тревоги'
            elif 8 <= value <= 9:
                return 'высокий уровень тревоги'
            else:
                return 'крайне высокий уровень тревоги'
        elif age == '13-14 лет':
            if 0 <= value <= 1:
                return 'низкий уровень тревоги'
            elif 2 <= value <= 6:
                return 'средний уровень тревоги'
            elif 7 <= value <= 8:
                return 'высокий уровень тревоги'
            else:
                return 'крайне высокий уровень тревоги'
        else:
            if 0 <= value <= 1:
                return 'низкий уровень тревоги'
            elif 2 <= value <= 6:
                return 'средний уровень тревоги'
            elif 7 <= value <= 8:
                return 'высокий уровень тревоги'
            else:
                return 'крайне высокий уровень тревоги'




def calc_value_spacct(row):
    """
    Функция для подсчета значения Снижение психической активности, связанное с тревогой
    :return: число
    """
    value_forward = 0  # результат
    lst_pos = [9,29,39,49,69,79,89,99]
    lst_neg = [19,59]
    for idx, value in enumerate(row,1):
        if idx in lst_neg:
            if value == 'нет':
                value_forward += 1
        elif idx in lst_pos:
            if value == 'да':
                value_forward += 1

    return value_forward



def calc_level_spacct(ser:pd.Series):
    """
    Функция для подсчета уровня
    :param ser: пол,возраст и значение
    :return:
    """
    row = ser.tolist() # превращаем в список
    sex = row[0] # пол
    age = row[1] # возраст
    value = row[2] # значение для обработки
    if sex == 'Мужской':
        if age == '7-10 лет':
            if 0 <= value <= 2:
                return 'низкий уровень тревоги'
            elif 3 <= value <= 6:
                return 'средний уровень тревоги'
            elif 7 <= value <= 8:
                return 'высокий уровень тревоги'
            else:
                return 'крайне высокий уровень тревоги'
        elif age == '11-12 лет':
            if 0 <= value <= 1:
                return 'низкий уровень тревоги'
            elif 2 <= value <= 5:
                return 'средний уровень тревоги'
            elif 6 <= value <= 7:
                return 'высокий уровень тревоги'
            else:
                return 'крайне высокий уровень тревоги'
        elif age == '13-14 лет':
            if 0 <= value <= 1:
                return 'низкий уровень тревоги'
            elif 2 <= value <= 5:
                return 'средний уровень тревоги'
            elif 6 <= value <= 7:
                return 'высокий уровень тревоги'
            else:
                return 'крайне высокий уровень тревоги'
        else:
            if 0 <= value <= 2:
                return 'низкий уровень тревоги'
            elif 3 <= value <= 5:
                return 'средний уровень тревоги'
            elif 6 <= value <= 7:
                return 'высокий уровень тревоги'
            else:
                return 'крайне высокий уровень тревоги'
    else:
        if age == '7-10 лет':
            if 0 <= value <= 2:
                return 'низкий уровень тревоги'
            elif 3 <= value <= 7:
                return 'средний уровень тревоги'
            elif value == 8:
                return 'высокий уровень тревоги'
            else:
                return 'крайне высокий уровень тревоги'
        elif age == '11-12 лет':
            if 0 <= value <= 1:
                return 'низкий уровень тревоги'
            elif 2 <= value <= 6:
                return 'средний уровень тревоги'
            elif value == 7:
                return 'высокий уровень тревоги'
            else:
                return 'крайне высокий уровень тревоги'
        elif age == '13-14 лет':
            if 0 <= value <= 2:
                return 'низкий уровень тревоги'
            elif 3 <= value <= 6:
                return 'средний уровень тревоги'
            elif 7 <= value <= 8:
                return 'высокий уровень тревоги'
            else:
                return 'крайне высокий уровень тревоги'
        else:
            if 0 <= value <= 2:
                return 'низкий уровень тревоги'
            elif 3 <= value <= 6:
                return 'средний уровень тревоги'
            elif 7 <= value <= 8:
                return 'высокий уровень тревоги'
            else:
                return 'крайне высокий уровень тревоги'



def calc_value_pvrsst(row):
    """
    Функция для подсчета значения Повышение вегетативной реактивности, связанное с тревогой
    :return: число
    """
    value_forward = 0  # результат
    lst_pos = [10,20,30,40,50,60,70,80,90,100]
    for idx, value in enumerate(row,1):
        if idx in lst_pos:
            if value == 'да':
                value_forward += 1

    return value_forward


def calc_level_pvrsst(ser:pd.Series):
    """
    Функция для подсчета уровня
    :param ser: пол,возраст и значение
    :return:
    """
    row = ser.tolist() # превращаем в список
    sex = row[0] # пол
    age = row[1] # возраст
    value = row[2] # значение для обработки
    if sex == 'Мужской':
        if age == '7-10 лет':
            if 0 <= value <= 1:
                return 'низкий уровень тревоги'
            elif 2 <= value <= 6:
                return 'средний уровень тревоги'
            elif 7 <= value <= 8:
                return 'высокий уровень тревоги'
            else:
                return 'крайне высокий уровень тревоги'
        elif age == '11-12 лет':
            if 0 <= value <= 1:
                return 'низкий уровень тревоги'
            elif 2 <= value <= 5:
                return 'средний уровень тревоги'
            elif 6 <= value <= 7:
                return 'высокий уровень тревоги'
            else:
                return 'крайне высокий уровень тревоги'
        elif age == '13-14 лет':
            if 0 <= value <= 1:
                return 'низкий уровень тревоги'
            elif 2 <= value <= 4:
                return 'средний уровень тревоги'
            elif 5 <= value <= 6:
                return 'высокий уровень тревоги'
            else:
                return 'крайне высокий уровень тревоги'
        else:
            if value == 0:
                return 'низкий уровень тревоги'
            elif 1 <= value <= 4:
                return 'средний уровень тревоги'
            elif 5 <= value <= 6:
                return 'высокий уровень тревоги'
            else:
                return 'крайне высокий уровень тревоги'
    else:
        if age == '7-10 лет':
            if 0 <= value <= 2:
                return 'низкий уровень тревоги'
            elif 3 <= value <= 7:
                return 'средний уровень тревоги'
            elif value == 8:
                return 'высокий уровень тревоги'
            else:
                return 'крайне высокий уровень тревоги'
        elif age == '11-12 лет':
            if 0 <= value <= 1:
                return 'низкий уровень тревоги'
            elif 2 <= value <= 6:
                return 'средний уровень тревоги'
            elif value == 7:
                return 'высокий уровень тревоги'
            else:
                return 'крайне высокий уровень тревоги'
        elif age == '13-14 лет':
            if 0 <= value <= 1:
                return 'низкий уровень тревоги'
            elif 2 <= value <= 5:
                return 'средний уровень тревоги'
            elif 6 <= value <= 7:
                return 'высокий уровень тревоги'
            else:
                return 'крайне высокий уровень тревоги'
        else:
            if 0 <= value <= 1:
                return 'низкий уровень тревоги'
            elif 2 <= value <= 6:
                return 'средний уровень тревоги'
            elif 7 <= value <= 8:
                return 'высокий уровень тревоги'
            else:
                return 'крайне высокий уровень тревоги'


def create_list_on_level_modt(base_df:pd.DataFrame, out_dct:dict, lst_level:list, dct_prefix:dict):
    """
    Функция для создания списков по уровням шкал
    :param base_df: датафрейм с результатами
    :param out_dct: словарь с датафреймами
    :param lst_level: список уровней по которым нужно сделать списки
    :param dct_prefix: префиксы для названий листов
    :return: обновлейнный out dct
    """
    for key,value in dct_prefix.items():
        dct_level = dict()
        for level in lst_level:
            temp_df = base_df[base_df[key] == level]
            if temp_df.shape[0] != 0:
                if level == 'низкий уровень тревоги':
                    level = 'низкий'
                elif level == 'средний уровень тревоги':
                    level = 'средний'
                elif level == 'высокий уровень тревоги':
                    level = 'высокий'
                else:
                    level = 'крайне высокий'
                dct_level[f'{dct_prefix[key]}. {level}'] = temp_df
        out_dct.update(dct_level)

    return out_dct


def create_result_modt(base_df:pd.DataFrame, out_dct:dict, lst_svod_cols:list):
    """
    Функция для подсчета результата если указаны колонки по которым нужно провести свод
    :param df: датафрейм с результатами
    :param out_dct: словарь с уже подсчитанными базовыми данными
    :param lst_svod_cols: список сводных колонок
    :return: словарь
    """
    lst_level = ['низкий уровень тревоги', 'средний уровень тревоги', 'высокий уровень тревоги', 'крайне высокий уровень тревоги']

    lst_reindex_one_level_cols = lst_svod_cols.copy()
    lst_reindex_one_level_cols.extend(['низкий уровень тревоги', 'средний уровень тревоги', 'высокий уровень тревоги', 'крайне высокий уровень тревоги',
                                       'Итого'])  # Основная шкала

    # ВЧА
    svod_count_one_level_vcha_df = calc_count_scale(base_df, lst_svod_cols,
                                                    'ОТ_Значение',
                                                    'ОТ_Уровень',
                                                    lst_reindex_one_level_cols, lst_level)

    # О
    svod_count_one_level_o_df = calc_count_scale(base_df, lst_svod_cols,
                                                 'ТВВСС_Значение',
                                                 'ТВВСС_Уровень',
                                                 lst_reindex_one_level_cols, lst_level)
    # РУВС
    svod_count_one_level_ruvs_df = calc_count_scale(base_df, lst_svod_cols,
                                                    'ТВССОО_Значение',
                                                    'ТВССОО_Уровень',
                                                    lst_reindex_one_level_cols, lst_level)

    # ПСП
    svod_count_one_level_psp_df = calc_count_scale(base_df, lst_svod_cols,
                                                   'ТВВСУ_Значение',
                                                   'ТВВСУ_Уровень',
                                                   lst_reindex_one_level_cols, lst_level)
    # ППВС
    svod_count_one_level_ppvs_df = calc_count_scale(base_df, lst_svod_cols,
                                                    'ТВВСР_Значение',
                                                    'ТВВСР_Уровень',
                                                    lst_reindex_one_level_cols, lst_level)
    # ИП
    svod_count_one_level_ip_df = calc_count_scale(base_df, lst_svod_cols,
                                                  'ТССУВО_Значение',
                                                  'ТССУВО_Уровень',
                                                  lst_reindex_one_level_cols, lst_level)

    # ПРП
    svod_count_one_level_prp_df = calc_count_scale(base_df, lst_svod_cols,
                                                   'ТВВССВ_Значение',
                                                   'ТВВССВ_Уровень',
                                                   lst_reindex_one_level_cols, lst_level)
    # ППБД
    svod_count_one_level_ppbd_df = calc_count_scale(base_df, lst_svod_cols,
                                                    'ТВВСПЗ_Значение',
                                                    'ТВВСПЗ_Уровень',
                                                    lst_reindex_one_level_cols, lst_level)
    # ППП
    svod_count_one_level_ppp_df = calc_count_scale(base_df, lst_svod_cols,
                                                   'СПАССТ_Значение',
                                                   'СПАССТ_Уровень',
                                                   lst_reindex_one_level_cols, lst_level)

    # УЗ
    svod_count_one_level_uz_df = calc_count_scale(base_df, lst_svod_cols,
                                                  'ПВРССТ_Значение',
                                                  'ПВРССТ_Уровень',
                                                  lst_reindex_one_level_cols, lst_level)

    # Считаем среднее по субшкалам
    svod_mean_one_df = pd.pivot_table(base_df,
                                      index=lst_svod_cols,
                                      values=['ОТ_Значение',
                                              'ТВВСС_Значение',
                                              'ТВССОО_Значение',
                                              'ТВВСУ_Значение',

                                              'ТВВСР_Значение',
                                              'ТССУВО_Значение',
                                              'ТВВССВ_Значение',
                                              'ТВВСПЗ_Значение',

                                              'СПАССТ_Значение',
                                              'ПВРССТ_Значение',
                                              ],
                                      aggfunc=round_mean_two)
    svod_mean_one_df.reset_index(inplace=True)

    # упорядочиваем колонки
    new_order_cols = lst_svod_cols.copy()
    new_order_cols.extend((['ОТ_Значение', 'ТВВСС_Значение',
                            'ТВССОО_Значение', 'ТВВСУ_Значение',
                            'ТВВСР_Значение', 'ТССУВО_Значение',
                            'ТВВССВ_Значение', 'ТВВСПЗ_Значение',
                            'СПАССТ_Значение', 'ПВРССТ_Значение',
                            ]))
    svod_mean_one_df = svod_mean_one_df.reindex(columns=new_order_cols)

    dct_rename_cols_mean = {'ОТ_Значение': 'Ср. Общая тревожность',
                            'ТВВСС_Значение': 'Ср. Тревога во взаимоотношениях со сверстниками',
                            'ТВССОО_Значение': 'Ср. Тревога в связи с оценкой окружающих',
                            'ТВВСУ_Значение': 'Ср. Тревога во взаимоотношениях с учителями',

                            'ТВВСР_Значение': 'Ср. Тревога во взаимоотношениях с родителями',
                            'ТССУВО_Значение': 'Ср. Тревога, связанная с успешностью в обучении',
                            'ТВВССВ_Значение': 'Ср. Тревога, возникающая в ситуациях самовыражения',
                            'ТВВСПЗ_Значение': 'Ср. Тревога, возникающая в ситуациях проверки знаний',

                            'СПАССТ_Значение': 'Ср. Снижение психической активности, связанное с тревогой',
                            'ПВРССТ_Значение': 'Ср. Повышение вегетативной реактивности, связанное с тревогой',
                            }
    svod_mean_one_df.rename(columns=dct_rename_cols_mean, inplace=True)

    # очищаем название колонки по которой делали свод
    out_name_lst = []

    for name_col in lst_svod_cols:
        name = re.sub(r'[\[\]\'+()<> :"?*|\\/]', '_', name_col)
        if len(lst_svod_cols) == 1:
            out_name_lst.append(name[:14])
        elif len(lst_svod_cols) == 2:
            out_name_lst.append(name[:7])
        else:
            out_name_lst.append(name[:4])

    out_name = ' '.join(out_name_lst)
    if len(out_name) > 14:
        out_name = out_name[:14]

    out_dct.update({f'Ср {out_name}': svod_mean_one_df,
                    f'ОТ {out_name}': svod_count_one_level_vcha_df,
                    f'ТВВСС {out_name}': svod_count_one_level_o_df,
                    f'ТВССОО {out_name}': svod_count_one_level_ruvs_df,
                    f'ТВВСУ {out_name}': svod_count_one_level_psp_df,

                    f'ТВВСР {out_name}': svod_count_one_level_ppvs_df,
                    f'ТССУВО {out_name}': svod_count_one_level_ip_df,
                    f'ТВВССВ {out_name}': svod_count_one_level_prp_df,
                    f'ТВВСПЗ {out_name}': svod_count_one_level_ppbd_df,

                    f'СПАССТ {out_name}': svod_count_one_level_ppp_df,
                    f'ПВРССТ {out_name}': svod_count_one_level_uz_df,
                    })

    if len(lst_svod_cols) == 1:
        return out_dct
    else:
        for idx, name_column in enumerate(lst_svod_cols):
            lst_reindex_column_level_cols = [lst_svod_cols[idx],'низкий уровень тревоги', 'средний уровень тревоги', 'высокий уровень тревоги', 'крайне высокий уровень тревоги',
                                                  'Итого']
            # ВЧА
            svod_count_column_level_vcha_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                               'ОТ_Значение',
                                                               'ОТ_Уровень',
                                                               lst_reindex_column_level_cols, lst_level)

            # О
            svod_count_column_level_o_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                            'ТВВСС_Значение',
                                                            'ТВВСС_Уровень',
                                                            lst_reindex_column_level_cols, lst_level)
            # РУВС
            svod_count_column_level_ruvs_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                               'ТВССОО_Значение',
                                                               'ТВССОО_Уровень',
                                                               lst_reindex_column_level_cols, lst_level)

            # ПСП
            svod_count_column_level_psp_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                              'ТВВСУ_Значение',
                                                              'ТВВСУ_Уровень',
                                                              lst_reindex_column_level_cols, lst_level)
            # ППВС
            svod_count_column_level_ppvs_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                               'ТВВСР_Значение',
                                                               'ТВВСР_Уровень',
                                                               lst_reindex_column_level_cols, lst_level)
            # ИП
            svod_count_column_level_ip_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                             'ТССУВО_Значение',
                                                             'ТССУВО_Уровень',
                                                             lst_reindex_column_level_cols, lst_level)

            # ПРП
            svod_count_column_level_prp_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                              'ТВВССВ_Значение',
                                                              'ТВВССВ_Уровень',
                                                              lst_reindex_column_level_cols, lst_level)
            # ППБД
            svod_count_column_level_ppbd_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                               'ТВВСПЗ_Значение',
                                                               'ТВВСПЗ_Уровень',
                                                               lst_reindex_column_level_cols, lst_level)
            # ППП
            svod_count_column_level_ppp_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                              'СПАССТ_Значение',
                                                              'СПАССТ_Уровень',
                                                              lst_reindex_column_level_cols, lst_level)

            # УЗ
            svod_count_column_level_uz_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                             'ПВРССТ_Значение',
                                                             'ПВРССТ_Уровень',
                                                             lst_reindex_column_level_cols, lst_level)

            # Считаем среднее по субшкалам
            svod_mean_column_df = pd.pivot_table(base_df,
                                              index=[lst_svod_cols[idx]],
                                              values=['ОТ_Значение',
                                                      'ТВВСС_Значение',
                                                      'ТВССОО_Значение',
                                                      'ТВВСУ_Значение',

                                                      'ТВВСР_Значение',
                                                      'ТССУВО_Значение',
                                                      'ТВВССВ_Значение',
                                                      'ТВВСПЗ_Значение',

                                                      'СПАССТ_Значение',
                                                      'ПВРССТ_Значение',
                                                      ],
                                              aggfunc=round_mean_two)
            svod_mean_column_df.reset_index(inplace=True)

            # упорядочиваем колонки
            new_order_cols = [lst_svod_cols[idx]].copy()
            new_order_cols.extend((['ОТ_Значение', 'ТВВСС_Значение',
                                    'ТВССОО_Значение', 'ТВВСУ_Значение',
                                    'ТВВСР_Значение', 'ТССУВО_Значение',
                                    'ТВВССВ_Значение', 'ТВВСПЗ_Значение',
                                    'СПАССТ_Значение', 'ПВРССТ_Значение',
                                    ]))
            svod_mean_column_df = svod_mean_column_df.reindex(columns=new_order_cols)

            dct_rename_cols_mean = {'ОТ_Значение': 'Ср. Общая тревожность',
                                    'ТВВСС_Значение': 'Ср. Тревога во взаимоотношениях со сверстниками',
                                    'ТВССОО_Значение': 'Ср. Тревога в связи с оценкой окружающих',
                                    'ТВВСУ_Значение': 'Ср. Тревога во взаимоотношениях с учителями',

                                    'ТВВСР_Значение': 'Ср. Тревога во взаимоотношениях с родителями',
                                    'ТССУВО_Значение': 'Ср. Тревога, связанная с успешностью в обучении',
                                    'ТВВССВ_Значение': 'Ср. Тревога, возникающая в ситуациях самовыражения',
                                    'ТВВСПЗ_Значение': 'Ср. Тревога, возникающая в ситуациях проверки знаний',

                                    'СПАССТ_Значение': 'Ср. Снижение психической активности, связанное с тревогой',
                                    'ПВРССТ_Значение': 'Ср. Повышение вегетативной реактивности, связанное с тревогой',
                                    }
            svod_mean_column_df.rename(columns=dct_rename_cols_mean, inplace=True)

            # Готовим наименование
            name_column = lst_svod_cols[idx]
            name_column = re.sub(r'[\[\]\'+()<> :"?*|\\/]', '_', name_column)
            name_column = name_column[:15]
            out_dct.update({f'Ср {name_column}': svod_mean_column_df,
                            f'ОТ {name_column}': svod_count_column_level_vcha_df,
                            f'ТВВСС {name_column}': svod_count_column_level_o_df,
                            f'ТВССОО {name_column}': svod_count_column_level_ruvs_df,
                            f'ТВВСУ {name_column}': svod_count_column_level_psp_df,

                            f'ТВВСР {name_column}': svod_count_column_level_ppvs_df,
                            f'ТССУВО {name_column}': svod_count_column_level_ip_df,
                            f'ТВВССВ {name_column}': svod_count_column_level_prp_df,
                            f'ТВВСПЗ {name_column}': svod_count_column_level_ppbd_df,

                            f'СПАССТ {name_column}': svod_count_column_level_ppp_df,
                            f'ПВРССТ {name_column}': svod_count_column_level_uz_df,
                            })
        return out_dct












def processing_modt_rom_vas(base_df: pd.DataFrame, answers_df: pd.DataFrame,lst_svod_cols:list):
    """
    Функция для обработки
    :param base_df: часть датафрейма с описательными колонками
    :param answers_df: часть датафрейма с ответами
    :param lst_svod_cols:  список с колонками по которым нужно делать свод
    """
    try:
        out_answer_df = base_df.copy()  # делаем копию для последующего соединения с сырыми ответами

        # очищаем названия колонок от возможных сочетаний .1 которые добавляет пандас при одинаковых колонках
        clean_df_lst = []
        for name_column in answers_df.columns:
            clean_name = re.sub(r'.\d+$', '', name_column)
            clean_df_lst.append(clean_name)

        answers_df.columns = clean_df_lst

        # Проверяем наличие колонок Пол и Возраст
        diff_req_cols = {'Пол','Возраст'}.difference(set(base_df.columns))
        if len(diff_req_cols) != 0:
            raise NotReqColumnMODTRV

        # на случай пустых
        base_df['Пол'].fillna('Не заполнено',inplace=True)
        base_df['Возраст'].fillna('Не заполнено',inplace=True)
        # очищаем от лишних пробелов
        base_df['Пол'] = base_df['Пол'].apply(str.strip)
        base_df['Возраст'] = base_df['Возраст'].apply(str.strip)

        # Проверяем на пол
        diff_sex = set(base_df['Пол'].unique()).difference({'Мужской', 'Женский'})
        if len(diff_sex) != 0:
            raise BadValueSexMODTRV

        # Проверяем на возраст
        diff_age = set(base_df['Возраст'].unique()).difference({'7-10 лет', '11-12 лет', '13-14 лет', '15-17 лет'})
        if len(diff_age) != 0:
            raise BadValueAgeMODTRV

        if len(answers_df.columns) != 100:  # проверяем количество колонок с вопросами
            raise BadCountColumnsMODTRV


        lst_check_cols = ['Часто ли ты чувствуешь себя обеспокоенным и взволнованным?',
                          'Часто ли твои одноклассники смеются над тобой, когда вы играете в разные игры?',
                          'Стараешься ли ты избегать игр, в которых делается выбор только потому, что тебя могут не выбрать?',
                          'Как ты думаешь, теряют ли симпатии учителей те из учеников, которые не справляются с учебой?',
                          'Можешь ли ты свободно говорить с родителями о вещах, которые тебя беспокоят?',
                          'Трудно ли тебе учиться не хуже других ребят?',
                          'Боишься ли ты вступать в спор?',
                          'Волнуешься ли ты, когда учитель говорит, что собирается проверить, насколько ты знаешь материал?',
                          'Часто ли ты чувствуешь себя усталым?',
                          'Сказывается ли на желудке твое волнение?',
                          'Когда вечером ты лежишь в постели, часто ли ты испытываешь беспокойство по поводу того, что будет завтра?',
                          'Часто ли у тебя возникает ощущение, что никто из твоих одноклассников не хочет делать того, что хочешь делать ты?',
                          'Кажется ли тебе, что окружающие часто недооценивают тебя?',
                          'Доволен ли ты тем, как к тебе относятся учителя?',
                          'Можешь ли ты обратиться со своими проблемами к близким, не испытывая страха, что тебе будет хуже?',
                          'Часто ли тебе ставят более низкую оценку, чем ты ожидал?',
                          'Часто ли ты боишься выглядеть нелепо?',
                          'Обычно ты волнуешься при ответе или выполнении контрольных заданий?',
                          'Чувствуешь ли ты себя бодрым после отдыха?',
                          'Случается ли тебе попадать в такие ситуации, когда ты чувствуешь, что твое сердце вот-вот остановится?',

                          'Часто ли тебя что-то мучает, а что - не можешь понять?',
                          'Часто ли ты чувствуешь себя не таким, как большинство твоих одноклассников?',
                          'Часто ли ты боишься, что тебе не о чем будет говорить, когда кто-то начинает с тобой разговор?',
                          'Обладают ли способные ученики какими-то особыми правами, которых нет у других ребят в классе?',
                          'Кажется ли тебе иногда, что никто из родителей тебя хорошо не понимает?',
                          'Часто ли твои одноклассники смеются над тобой, когда ты делаешь ошибки?',
                          'Обычно тебя волнует то, что думают о тебе окружающие?',
                          'Выполнив задание, беспокоишься ли ты о том, хорошо ли с ним справился?',
                          'Чувствуешь ли ты себя хуже от волнений и ожидания неприятностей?',
                          'Случается ли, что ты испытываешь кожный зуд и покалывание, когда волнуешься?',
                          'Часто ли ты волнуешься из-за того, что, как выясняется позже, не имеет никакого значения?',
                          'Верно ли, что большинство ребят относится к тебе по-дружески?',
                          'Испытываешь ли ты стеснение, находясь среди малознакомых людей?',
                          'Волнуешься ли ты, когда учитель просит остаться после уроков и поработать с ним индивидуально?',
                          'Когда у тебя плохое настроение, советуют ли тебе твои родители успокоиться и отвлечься?',
                          'Когда ты получаешь хорошие отметки, думает ли кто-нибудь из твоих друзей, что ты хочешь выделиться?',
                          'Часто ли, отвечая на уроке, ты переживаешь о том, что думают о тебе в это время другие?',
                          'Мечтаешь ли ты о том, чтобы поменьше волноваться, когда тебя спрашивают?',
                          'Часто ли у тебя болит голова после напряженного дня?',
                          'Бывает ли у тебя сильное сердцебиение в тревожных для тебя ситуациях?',

                          'Часто ли ты чувствуешь неуверенность в себе?',
                          'Нравится ли тебе тот одноклассник, к которому другие ребята относятся лучше всех?',
                          'Обычно ты боишься невольно обидеть других людей своими случайно сказанными словами или поведением?',
                          'Боишься ли ты критики со стороны учителя?',
                          'Начинают ли твои родители сердиться и возмущаться по поводу любого пустяка, совершенного тобой?',
                          'Надеешься ли ты в будущем учиться лучше, чем теперь?',
                          'Часто ли одноклассники смеются над твоей внешностью и поведением?',
                          'Бывает ли так, что, отвечая перед классом, ты начинаешь заикаться и не можешь ясно произнести ни одного слова?',
                          'Трудно ли тебе вставать по утрам вовремя?',
                          'Бывают ли у тебя внезапные чувства жара или озноба?',
                          'Трудно ли тебе сосредоточиться на чем-то одном?',
                          'Верно ли, что большинство твоих одноклассников не обращают на тебя внимания?',
                          'Часто ли ты, услышав смех, чувствуешь себя задетым и думаешь, что смеются над тобой?',
                          'Легко ли учителю привести тебя в замешательство своим неожиданным вопросом?',
                          'Часто ли твои родители интересуются тем, что тебя волнует и чего ты хочешь?',
                          'Боишься ли ты не справиться со своей работой?',
                          'Часто ли ты упрекаешь себя в том, что не используешь многие свои способности?',
                          'Обычно ты спишь спокойно накануне контрольной или экзамена?',
                          'Легко ли ты засыпаешь вечером?',
                          'Кажется ли тебе иногда, что твое сердце бьется неравномерно?',

                          'Часто ли тебе снятся страшные сны?',
                          'Считаешь ли ты, что одеваешься в школу так же хорошо, как и твои одноклассники?',
                          'Боишься ли ты потерять симпатии других людей?',
                          'Считаешь ли ты, что педагоги относятся к тебе несправедливо?',
                          'Всегда ли родители с пониманием выслушивают твои взгляды и мнения?',
                          'Можешь ли ты быть очень настойчивым, если хочешь добиться определенной цели?',
                          'Трудно ли тебе писать, если при этом кто-то смотрит на твои руки?',
                          'Часто ли ты получаешь низкую оценку, хорошо зная материал только из-за того, что волнуешься и теряешься при ответе?',
                          'Часто ли ты сердишься по мелочам?',
                          'Бывает ли так, что при волнении у тебя появляются красные пятна на шее и на лице?',
                          'Часто ли ты испытываешь страх в тех ситуациях, когда точно знаешь, что тебе ничто не угрожает?',
                          'Злятся ли некоторые из твоих одноклассников, когда тебе удается быть лучше их?',
                          'Обычно тебе безразлично, что думают о тебе другие?',
                          'Боишься ли ты, что тебя могут вызвать к директору?',
                          'Если ты сделаешь что-нибудь не так, будут ли твои родители постоянно и везде говорить об этом?',
                          'Снится ли тебе иногда, что ты в школе и не можешь ответить на вопрос учителя?',
                          'Нравится ли тебе быть первым, чтобы другие тебе подражали и следовали бы за тобой?',
                          'Если ты не можешь ответить, когда тебя спрашивают, чувствуешь ли ты, что вот-вот расплачешься?',
                          'Часто ли тебе приходится дома доделывать задания, которые ты не успел выполнить в классе?',
                          'Бывает ли тебе трудно дышать из-за волнения?',

                          'Боишься ли ты оставаться дома один?',
                          'Мешает ли тебе твоя застенчивость подружиться с тем, с кем хотелось бы?',
                          'Часто ли бывает, что тебе кажется, будто окружающие смотрят на тебя, как на никчемного и ненужного человека?',
                          '«Холодеет» ли у тебя все внутри, когда учитель делает тебе замечание?',
                          'Бывает ли тебе обидно, когда твое мнение не совпадает с мнением твоих родителей, а они категорически настаивают на своем?',
                          'Часто ли тебе снится, что твои одноклассники могут сделать то, что не можешь ты?',
                          'Боишься ли ты, что тебя неправильно поймут, когда ты захочешь что-то сказать?',
                          'Часто ли бывает такое, что у тебя слегка дрожит рука при выполнении контрольных заданий?',
                          'Легко ли тебе расплакаться из-за ерунды?',
                          'Боишься ли ты, что тебе вдруг станет дурно в классе?',
                          'Страшно ли тебе оставаться одному в темной комнате?',
                          'Доволен ли ты тем, как к тебе относятся одноклассники?',
                          'Трудно ли тебе получать такие отметки, каких ждут от тебя окружающие?',
                          'Снится ли тебе временами, что учитель в ярости из-за того, что ты не знаешь урок?',
                          'Чувствуешь ли ты себя никому не нужным каждый раз после ссоры с родителями?',
                          'Сильно ли ты переживаешь по поводу замечаний и отметок, которые тебя не удовлетворяют?',
                          'Дрожит ли слегка твоя рука, когда учитель просит сделать задание на доске перед всем классом?',
                          'Беспокоишься ли ты по дороге в школу, что учитель может дать классу проверочную работу?',
                          'Часто ли ты получаешь более низкую оценку, чем мог бы получить из-за того, что не успел чего-то сделать?',
                          'Потеют ли у тебя руки и ноги при волнении?',
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
            raise BadOrderMODTRV

        valid_values = ['да','нет']

        lst_error_answers = []  # список для хранения строк где найдены неправильные ответы

        for i in range(100):
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
            raise BadValueMODTRV

        # Шкала 1 Общая тревожность
        lst_ot = [1,11,21,31,41,51,61,71,81,91]
        lst_ot = list(map(lambda x: x - 1, lst_ot))
        base_df['ОТ_Значение'] = answers_df.take(lst_ot, axis=1).apply(calc_value_ot, axis=1)
        base_df['ОТ_Уровень'] = base_df[['Пол', 'Возраст', 'ОТ_Значение']].apply(lambda x: calc_level_ot(x),axis=1)

        # Шкала 2 Тревога во взаимоотношениях со сверстниками
        base_df['ТВВСС_Значение'] = answers_df.apply(calc_value_tvvss, axis=1)
        base_df['ТВВСС_Уровень'] = base_df[['Пол', 'Возраст', 'ТВВСС_Значение']].apply(lambda x: calc_level_tvvss(x),axis=1)

        # Шкала 3 Тревога в связи с оценкой окружающих
        base_df['ТВССОО_Значение'] = answers_df.apply(calc_value_tvssoo, axis=1)
        base_df['ТВССОО_Уровень'] = base_df[['Пол', 'Возраст', 'ТВССОО_Значение']].apply(lambda x: calc_level_tvssoo(x), axis=1)

        # Шкала 4 Тревога во взаимоотношениях с учителями
        base_df['ТВВСУ_Значение'] = answers_df.apply(calc_value_tvvsu, axis=1)
        base_df['ТВВСУ_Уровень'] = base_df[['Пол', 'Возраст', 'ТВВСУ_Значение']].apply(lambda x: calc_level_tvvsu(x), axis=1)

        # Шкала 5 Тревога во взаимоотношениях с родителями
        base_df['ТВВСР_Значение'] = answers_df.apply(calc_value_tvvsr, axis=1)
        base_df['ТВВСР_Уровень'] = base_df[['Пол', 'Возраст', 'ТВВСР_Значение']].apply(lambda x: calc_level_tvvsr(x), axis=1)

        # Шкала 6 Тревога, связанная с успешностью в обучении
        base_df['ТССУВО_Значение'] = answers_df.apply(calc_value_tssuvo, axis=1)
        base_df['ТССУВО_Уровень'] = base_df[['Пол', 'Возраст', 'ТССУВО_Значение']].apply(lambda x: calc_level_tssuvo(x), axis=1)

        # Шкала 7 Тревога, возникающая в ситуациях самовыражения
        base_df['ТВВССВ_Значение'] = answers_df.apply(calc_value_tvvssv, axis=1)
        base_df['ТВВССВ_Уровень'] = base_df[['Пол', 'Возраст', 'ТВВССВ_Значение']].apply(lambda x: calc_level_tvvssv(x), axis=1)

        # Шкала 8 Тревога, возникающая в ситуациях проверки знаний
        base_df['ТВВСПЗ_Значение'] = answers_df.apply(calc_value_tvvspz, axis=1)
        base_df['ТВВСПЗ_Уровень'] = base_df[['Пол', 'Возраст', 'ТВВСПЗ_Значение']].apply(lambda x: calc_level_tvvspz(x), axis=1)

        # Шкала 9 Снижение психической активности, связанное с тревогой
        base_df['СПАССТ_Значение'] = answers_df.apply(calc_value_spacct, axis=1)
        base_df['СПАССТ_Уровень'] = base_df[['Пол', 'Возраст', 'СПАССТ_Значение']].apply(lambda x: calc_level_spacct(x), axis=1)

        # Шкала 10 Повышение вегетативной реактивности, связанное с тревогой
        base_df['ПВРССТ_Значение'] = answers_df.apply(calc_value_pvrsst, axis=1)
        base_df['ПВРССТ_Уровень'] = base_df[['Пол', 'Возраст', 'ПВРССТ_Значение']].apply(lambda x: calc_level_pvrsst(x), axis=1)

        # Создаем датафрейм для создания части в общий датафрейм
        part_df = pd.DataFrame()
        part_df['МОДТРВ_ОТ_Значение'] = base_df['ОТ_Значение']
        part_df['МОДТРВ_ОТ_Диапазон'] = base_df['ОТ_Уровень']

        part_df['МОДТРВ_ТВВСС_Значение'] = base_df['ТВВСС_Значение']
        part_df['МОДТРВ_ТВВСС_Диапазон'] = base_df['ТВВСС_Уровень']

        part_df['МОДТРВ_ТВССОО_Значение'] = base_df['ТВССОО_Значение']
        part_df['МОДТРВ_ТВССОО_Диапазон'] = base_df['ТВССОО_Уровень']

        part_df['МОДТРВ_ТВВСУ_Значение'] = base_df['ТВВСУ_Значение']
        part_df['МОДТРВ_ТВВСУ_Диапазон'] = base_df['ТВВСУ_Уровень']

        part_df['МОДТРВ_ТВВСР_Значение'] = base_df['ТВВСР_Значение']
        part_df['МОДТРВ_ТВВСР_Диапазон'] = base_df['ТВВСР_Уровень']

        part_df['МОДТРВ_ТССУВО_Значение'] = base_df['ТССУВО_Значение']
        part_df['МОДТРВ_ТССУВО_Диапазон'] = base_df['ТССУВО_Уровень']

        part_df['МОДТРВ_ТВВССВ_Значение'] = base_df['ТВВССВ_Значение']
        part_df['МОДТРВ_ТВВССВ_Диапазон'] = base_df['ТВВССВ_Уровень']

        part_df['МОДТРВ_ТВВСПЗ_Значение'] = base_df['ТВВСПЗ_Значение']
        part_df['МОДТРВ_ТВВСПЗ_Диапазон'] = base_df['ТВВСПЗ_Уровень']

        part_df['МОДТРВ_СПАССТ_Значение'] = base_df['СПАССТ_Значение']
        part_df['МОДТРВ_СПАССТ_Диапазон'] = base_df['СПАССТ_Уровень']

        part_df['МОДТРВ_ПВРССТ_Значение'] = base_df['ПВРССТ_Значение']
        part_df['МОДТРВ_ПВРССТ_Диапазон'] = base_df['ПВРССТ_Уровень']

        out_answer_df = pd.concat([out_answer_df, answers_df], axis=1)  # Датафрейм для проверки
        base_df.sort_values(by='ОТ_Значение', ascending=False, inplace=True)  # сортируем

        # Делаем свод  по  шкалам
        dct_svod_sub = {'ОТ_Значение': 'ОТ_Уровень',
                        'ТВВСС_Значение': 'ТВВСС_Уровень',
                        'ТВССОО_Значение': 'ТВССОО_Уровень',
                        'ТВВСУ_Значение': 'ТВВСУ_Уровень',
                        'ТВВСР_Значение': 'ТВВСР_Уровень',

                        'ТССУВО_Значение': 'ТССУВО_Уровень',
                        'ТВВССВ_Значение': 'ТВВССВ_Уровень',
                        'ТВВСПЗ_Значение': 'ТВВСПЗ_Уровень',
                        'СПАССТ_Значение': 'СПАССТ_Уровень',
                        'ПВРССТ_Значение': 'ПВРССТ_Уровень',
                        }

        dct_rename_svod_sub = {'ОТ_Значение': 'ОТ',
                        'ТВВСС_Значение': 'ТВВСС',
                        'ТВССОО_Значение': 'ТВССОО',
                        'ТВВСУ_Значение': 'ТВВСУ',
                        'ТВВСР_Значение': 'ТВВСР',

                        'ТССУВО_Значение': 'ТССУВО',
                        'ТВВССВ_Значение': 'ТВВССВ',
                        'ТВВСПЗ_Значение': 'ТВВСПЗ',
                        'СПАССТ_Значение': 'СПАССТ',
                        'ПВРССТ_Значение': 'ПВРССТ',
                               }

        lst_sub = ['низкий уровень тревоги', 'средний уровень тревоги', 'высокий уровень тревоги', 'крайне высокий уровень тревоги']

        base_svod_sub_df = create_union_svod(base_df, dct_svod_sub, dct_rename_svod_sub, lst_sub)

        # считаем среднее значение по шкалам
        avg_vcha = round(base_df['ОТ_Значение'].mean(), 2)
        avg_o = round(base_df['ТВВСС_Значение'].mean(), 2)
        avg_ruvs = round(base_df['ТВССОО_Значение'].mean(), 2)

        avg_psp = round(base_df['ТВВСУ_Значение'].mean(), 2)
        avg_ppvs = round(base_df['ТВВСР_Значение'].mean(), 2)
        avg_ip = round(base_df['ТССУВО_Значение'].mean(), 2)

        avg_prp = round(base_df['ТВВССВ_Значение'].mean(), 2)
        avg_ppbd = round(base_df['ТВВСПЗ_Значение'].mean(), 2)
        avg_ppp = round(base_df['СПАССТ_Значение'].mean(), 2)

        avg_uz = round(base_df['ПВРССТ_Значение'].mean(), 2)

        avg_dct = {'Среднее значение шкалы Общая тревожность': avg_vcha,
                   'Среднее значение шкалы Тревога во взаимоотношениях со сверстниками': avg_o,
                   'Среднее значение шкалы Тревога в связи с оценкой окружающих': avg_ruvs,

                   'Среднее значение шкалы Тревога во взаимоотношениях с учителями': avg_psp,
                   'Среднее значение шкалы Тревога во взаимоотношениях с родителями': avg_ppvs,
                   'Среднее значение шкалы Тревога, связанная с успешностью в обучении': avg_ip,

                   'Среднее значение шкалы Тревога, возникающая в ситуациях самовыражения': avg_prp,
                   'Среднее значение шкалы Тревога, возникающая в ситуациях проверки знаний': avg_ppbd,
                   'Среднее значение шкалы Снижение психической активности, связанное с тревогой': avg_ppp,

                   'Среднее значение шкалы Повышение вегетативной реактивности, связанное с тревогой': avg_uz,
                   }

        avg_df = pd.DataFrame.from_dict(avg_dct, orient='index')
        avg_df = avg_df.reset_index()
        avg_df.columns = ['Показатель', 'Среднее значение']

        # формируем основной словарь
        out_dct = {'Списочный результат': base_df,
                   'Список для проверки': out_answer_df,
                   'Свод Шкалы': base_svod_sub_df,
                   'Среднее': avg_df,
                   }

        dct_prefix = {'ОТ_Уровень': 'ОТ',
                      'ТВВСС_Уровень': 'ТВВСС',
                      'ТВССОО_Уровень': 'ТВССОО',

                      'ТВВСУ_Уровень': 'ТВВСУ',
                      'ТВВСР_Уровень': 'ТВВСР',
                      'ТССУВО_Уровень': 'ТССУВО',

                      'ТВВССВ_Уровень': 'ТВВССВ',
                      'ТВВСПЗ_Уровень': 'ТВВСПЗ',
                      'СПАССТ_Уровень': 'СПАССТ',

                      'ПВРССТ_Уровень': 'ПВРССТ',
                      }

        out_dct = create_list_on_level_modt(base_df, out_dct, lst_sub, dct_prefix)

        """
                        Сохраняем в зависимости от необходимости делать своды по определенным колонкам
                        """
        if len(lst_svod_cols) == 0:
            return out_dct, part_df

        else:
            out_dct = create_result_modt(base_df, out_dct, lst_svod_cols)
            return out_dct, part_df


    except BadOrderMODTRV:
        messagebox.showerror('Лахеcис',
                             f'При обработке вопросов теста Многомерная оценка детской тревожности Ромицына Вассерман обнаружены неправильные вопросы. Проверьте названия колонок с вопросами:\n'
                             f'{error_order_message[:5000]}\n'
                             f'Используйте при создании Яндекс-формы написание вопросов из руководства пользователя программы Лахесис.')
    except BadValueMODTRV:
        messagebox.showerror('Лахеcис',
                             f'При обработке вопросов теста Многомерная оценка детской тревожности Ромицына Вассерман обнаружены неправильные варианты ответов. Проверьте ответы на указанных строках:\n'
                             f'{error_message[:5000]}\n'
                             f'Используйте при создании Яндекс-формы написание вариантов ответа из руководства пользователя программы Лахесис.')


    except BadCountColumnsMODTRV:
        messagebox.showerror('Лахеcис',
                             f'Проверьте количество колонок с ответами на тест Многомерная оценка детской тревожности Ромицына Вассерман\n'
                             f'Должно быть 100 колонок с ответами')

    except NotReqColumnMODTRV:
        messagebox.showerror('Лахеcис',
                             f'В таблице отсутствуют обязательные колонки {diff_req_cols}\n'
                             f'В таблице обязательно должны быть колонка с названием Пол и колонка с названием Возраст')

    except BadValueSexMODTRV:
        messagebox.showerror('Лахеcис',
                             f'В колонке Пол найдены значения отличающиеся от допустимых {diff_sex}\n'
                             f'Допускаются значения: Мужской и Женский\n'
                             f'Прочитайте страницу 1 и 2 файла инструкции к тесту Многомерная оценка детской тревожности Ромицына Вассерман')
    except BadValueAgeMODTRV:
        messagebox.showerror('Лахеcис',
                             f'В колонке Возраст найдены значения отличающиеся от допустимых {diff_age}\n'
                             f'Допускаются значения: 7-10 лет, 11-12 лет, 13-14 лет, 15-17 лет\n'
                             f'Прочитайте страницу 1 и 2 файла инструкции к тесту Многомерная оценка детской тревожности Ромицына Вассерман')
































