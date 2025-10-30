"""
Скрипт для обработки результатов теста Методика многофакторного исследования личности Кеттела
(подростковый вариант) 14-PF Рукавишников Соколова

"""

import pandas as pd
import re
from tkinter import messagebox
from lachesis_support_functions import calc_count_scale,round_mean,create_union_svod,create_list_on_level

class BadOrderKPFRS(Exception):
    """
    Исключение для обработки случая когда колонки не совпадают
    """
    pass


class BadValueKPFRS(Exception):
    """
    Исключение для неправильных значений в вариантах ответов
    """
    pass

class BadCountColumnsKPFRS(Exception):
    """
    Исключение для обработки случая если количество колонок не равно 142
    """
    pass

class NotReqColumn(Exception):
    """
    Исключение для обработки случая когда нет обязательных колонок Пол
    """
    pass

class BadValueSex(Exception):
    """
    Исключение для обработки случая когда в колонке Пол есть значения отличающиеся от Мужской или Женский
    """
    pass





def calc_a_value(row):
    """
    Фнукция подсчета значения
    :param row:
    :return:
    """
    value = 0
    # 1
    if row[0] == 'в одиночку осматривать лес':
        value += 0
    elif row[0] == 'трудно сказать':
        value += 1
    elif row[0] == 'играть с товарищами вокруг костра':
        value += 2
    # 2
    if row[1] == 'да':
        value += 2
    elif row[1] == 'иногда':
        value += 1
    elif row[1] == 'нет':
        value += 0
    # 3
    if row[2] == 'да':
        value += 2
    elif row[2] == 'не уверен':
        value += 1
    elif row[2] == 'нет':
        value += 0
    # 4
    if row[3] == 'да':
        value += 0
    elif row[3] == 'иногда':
        value += 1
    elif row[3] == 'нет':
        value += 2
    # 5
    if row[4] == 'да':
        value += 2
    elif row[4] == 'может быть':
        value += 1
    elif row[4] == 'нет':
        value += 0
    # 6
    if row[5] == 'да':
        value += 0
    elif row[5] == 'может быть':
        value += 1
    elif row[5] == 'нет':
        value += 2
    # 7
    if row[6] == 'да':
        value += 0
    elif row[6] == 'иногда':
        value += 1
    elif row[6] == 'нет, я не испытываю неприятного чувства':
        value += 2
    # 8
    if row[7] == 'быстро осваиваетесь со всеми':
        value += 2
    elif row[7] == 'трудно сказать':
        value += 1
    elif row[7] == 'вам нужно много времени, чтобы узнать каждого':
        value += 0
    # 9
    if row[8] == 'в тиши лесов, где слышно только пение птиц':
        value += 0
    elif row[8] == 'трудно сказать':
        value += 1
    elif row[8] == 'на многолюдной улице, где много происшествий':
        value += 2
    # 10
    if row[9] == 'проводником, имеющим дело с пассажирами':
        value += 2
    elif row[9] == 'трудно решить':
        value += 1
    elif row[9] == 'машинистом, ведущим поезд':
        value += 0

    return value

def calc_a_sten(ser:pd.Series):
    """
    Функция для подсчета Стена
    :param ser: пол и значение
    :return:
    """
    row = ser.tolist() # превращаем в список
    sex = row[0] # пол
    value = row[1] # значение которое нужно обработать

    if sex == 'Женский':
        if 0 <= value <= 4:
            return 1
        elif 5 <= value <= 6:
            return 2
        elif 7 <= value <= 8:
            return 3
        elif 9 <= value <= 10:
            return 4
        elif value == 11:
            return 5
        elif 12 <= value <= 13:
            return 6
        elif 14 <= value <= 15:
            return 7
        elif 16 <= value <= 17:
            return 8
        elif 18 <= value <= 19:
            return 9
        else:
            return 10
    else:
        if 0 <= value <= 3:
            return 1
        elif 4 <= value <= 5:
            return 2
        elif value == 6:
            return 3
        elif 7 <= value <= 8:
            return 4
        elif 9 <= value == 10:
            return 5
        elif value == 11:
            return 6
        elif value == 12:
            return 7
        elif 13 <= value <= 14:
            return 8
        elif value == 15:
            return 9
        else:
            return 10



# B
def calc_b_value(row):
    """
    Фнукция подсчета значения
    :param row:
    :return:
    """
    value = 0 # сумматор

    # 1
    if row[0] == 'могущественный':
        value += 1
    else:
        value += 0
    # 2
    if row[1] == 'ложь':
        value += 1
    else:
        value += 0
    # 3
    if row[2] == 'продавать':
        value += 1
    else:
        value += 0
    # 4
    if row[3] == 'голодный':
        value += 1
    else:
        value += 0
    # 5
    if row[4] == 'дядей':
        value += 1
    else:
        value += 0
    # 6
    if row[5] == 'нога':
        value += 1
    else:
        value += 0
    # 7
    if row[6] == 'как правило':
        value += 1
    else:
        value += 0
    # 8
    if row[7] == 'моя мать':
        value += 1
    else:
        value += 0
    # 9
    if row[8] == 'бумага':
        value += 1
    else:
        value += 0
    # 10
    if row[9] == 'между':
        value += 1
    else:
        value += 0
    return value


def calc_b_sten(ser: pd.Series):
    """
    Функция для подсчета Стена
    :param ser: пол и значение
    :return:
    """
    row = ser.tolist() # превращаем в список
    sex = row[0] # пол
    value = row[1] # значение которое нужно обработать

    if sex == 'Женский':
        if 0 <= value <= 2:
            return 1
        elif value == 3:
            return 2
        elif value == 4:
            return 4
        elif value == 5:
            return 5
        elif value == 6:
            return 7
        elif value == 7:
            return 8
        elif value == 8:
            return 9
        else:
            return 10
    else:
        if 0 <= value <= 2:
            return 1
        elif value == 3:
            return 2
        elif value == 4:
            return 3
        elif value == 5:
            return 4
        elif value == 6:
            return 5
        elif value == 7:
            return 6
        elif value == 8:
            return 7
        elif value == 9:
            return 8
        else:
            return 10

# C
def calc_c_value(row):
    """
    Фнукция подсчета значения
    :param row:
    :return:
    """
    value = 0 # сумматор
    # 1
    if row[0] == 'да':
        value += 0
    elif row[0] == 'может быть':
        value += 1
    elif row[0] == 'нет':
        value += 2
    # 2
    if row[1] == 'да':
        value += 2
    elif row[1] == 'иногда':
        value += 1
    elif row[1] == 'нет':
        value += 0
    # 3
    if row[2] == 'сомневаетесь – вдруг захочется изменить свое решение':
        value += 0
    elif row[2] == 'верно нечто среднее':
        value += 1
    elif row[2] == 'чувствуете уверенность, что решение останется в силе':
        value += 2
    # 4
    if row[3] == 'да':
        value += 2
    elif row[3] == 'обычно':
        value += 1
    elif row[3] == 'нет':
        value += 0
    # 5
    if row[4] == 'да':
        value += 0
    elif row[4] == 'может быть':
        value += 1
    elif row[4] == 'нет':
        value += 2
    # 6
    if row[5] == 'да':
        value += 2
    elif row[5] == 'трудно сказать':
        value += 1
    elif row[5] == 'нет':
        value += 0
    # 7
    if row[6] == 'да':
        value += 0
    elif row[6] == 'иногда':
        value += 1
    elif row[6] == 'нет':
        value += 2
    # 8
    if row[7] == 'да':
        value += 2
    elif row[7] == 'среднее':
        value += 1
    elif row[7] == 'нет':
        value += 0
    # 9
    if row[8] == 'да':
        value += 0
    elif row[8] == 'иногда':
        value += 1
    elif row[8] == 'нет':
        value += 2
    # 10
    if row[9] == 'рады этому и показываете, на что способны':
        value += 2
    elif row[9] == 'трудно сказать':
        value += 1
    elif row[9] == 'чувствуете, что не справитесь':
        value += 0

    return value


def calc_c_sten(ser: pd.Series):
    """
    Функция для подсчета Стена
    :param ser: пол и значение
    :return:
    """
    row = ser.tolist() # превращаем в список
    sex = row[0] # пол
    value = row[1] # значение которое нужно обработать

    if sex == 'Женский':
        if 0 <= value <= 2:
            return 1
        elif 3 <= value == 4:
            return 2
        elif 5 <= value <= 6:
            return 3
        elif value == 7:
            return 4
        elif 8 <=value <= 9:
            return 5
        elif 10 <= value <= 11:
            return 6
        elif 12 <= value <= 13:
            return 7
        elif value == 14:
            return 8
        elif 15 <= value <= 16:
            return 9
        else:
            return 10
    else:
        if 0 <= value <= 3:
            return 1
        elif value== 4:
            return 2
        elif value == 5:
            return 3
        elif 6 <= value <= 7:
            return 4
        elif 8 <= value <= 9:
            return 5
        elif value == 10:
            return 6
        elif 11 <= value <= 12:
            return 7
        elif value == 13:
            return 8
        elif 14 <= value <= 15:
            return 9
        else:
            return 10

# D
def calc_d_value(row):
    """
    Фнукция подсчета значения
    :param row:
    :return:
    """
    value = 0 # сумматор

    # 1
    if row[0] == 'да':
        value += 0
    elif row[0] == 'возможно':
        value += 1
    elif row[0] == 'нет':
        value += 2
    # 2
    if row[1] == 'часто':
        value += 2
    elif row[1] == 'иногда':
        value += 1
    elif row[1] == 'редко':
        value += 0
    # 3
    if row[2] == 'считаете это простой случайностью':
        value += 0
    elif row[2] == 'нечто среднее':
        value += 1
    elif row[2] == 'обижаетесь и сердитесь':
        value += 2
    # 4
    if row[3] == 'да':
        value += 2
    elif row[3] == 'возможно':
        value += 1
    elif row[3] == 'нет':
        value += 0
    # 5
    if row[4] == 'как правило':
        value += 0
    elif row[4] == 'трудно сказать':
        value += 1
    elif row[4] == 'нет':
        value += 2
    # 6
    if row[5] == 'да':
        value += 2
    elif row[5] == 'может быть':
        value += 1
    elif row[5] == 'нет':
        value += 0
    # 7
    if row[6] == 'да':
        value += 0
    elif row[6] == 'может быть':
        value += 1
    elif row[6] == 'нет, я выхожу из себя':
        value += 2
    # 8
    if row[7] == 'да':
        value += 2
    elif row[7] == 'может быть':
        value += 1
    elif row[7] == 'нет':
        value += 0
    # 9
    if row[8] == 'хорошо':
        value += 0
    elif row[8] == 'трудно сказать':
        value += 1
    elif row[8] == 'это мешает и раздражает':
        value += 2
    # 10
    if row[9] == 'иногда':
        value += 2
    elif row[9] == 'редко':
        value += 1
    elif row[9] == 'никогда':
        value += 0

    return value

def calc_d_sten(ser: pd.Series):
    """
    Функция для подсчета Стена
    :param ser: пол и значение
    :return:
    """
    row = ser.tolist() # превращаем в список
    sex = row[0] # пол
    value = row[1] # значение которое нужно обработать

    if sex == 'Женский':
        if 0 <= value <= 4:
            return 1
        elif 5 <= value <= 6:
            return 2
        elif value == 7:
            return 3
        elif value == 8:
            return 4
        elif 9 <=value <= 10:
            return 5
        elif 11 <= value <= 12:
            return 6
        elif value == 13:
            return 7
        elif 14 <= value <= 15:
            return 8
        elif 16 <= value <= 17:
            return 9
        else:
            return 10
    else:
        if 0 <= value <= 4:
            return 1
        elif value == 5:
            return 2
        elif 6 <= value <= 7:
            return 3
        elif 8 <= value <= 9:
            return 4
        elif value == 10:
            return 5
        elif 11 <= value <= 12:
            return 6
        elif value == 13:
            return 7
        elif 14 <= value <= 15:
            return 8
        elif value == 16:
            return 9
        else:
            return 10

# E
def calc_e_value(row):
    """
    Фнукция подсчета значения
    :param row:
    :return:
    """
    value = 0 # сумматор

    # 1
    if row[0] == 'да':
        value += 0
    elif row[0] == 'иногда':
        value += 1
    elif row[0] == 'нет':
        value += 2
    # 2
    if row[1] == 'редко':
        value += 2
    elif row[1] == 'иногда':
        value += 1
    elif row[1] == 'часто':
        value += 0
    # 3
    if row[2] == 'уступаете и даете ему высказаться':
        value += 0
    elif row[2] == 'трудно решить':
        value += 1
    elif row[2] == 'даете понять, что это невежливо, и не позволяете прерывать себя':
        value += 2
    # 4
    if row[3] == 'своим обычным голосом':
        value += 2
    elif row[3] == 'нечто среднее':
        value += 1
    elif row[3] == 'как можно тише':
        value += 0
    # 5
    if row[4] == 'да':
        value += 0
    elif row[4] == 'может быть':
        value += 1
    elif row[4] == 'нет':
        value += 2
    # 6
    if row[5] == 'архитектором-проектировщиком':
        value += 2
    elif row[5] == 'трудно решить':
        value += 1
    elif row[5] == 'певцом или музыкантом в эстрадном оркестре':
        value += 0
    # 7
    if row[6] == 'да':
        value += 0
    elif row[6] == 'может быть':
        value += 1
    elif row[6] == 'нет':
        value += 2
    # 8
    if row[7] == 'часто':
        value += 2
    elif row[7] == 'иногда':
        value += 1
    elif row[7] == 'никогда не думал':
        value += 0
    # 9
    if row[8] == 'учителем':
        value += 0
    elif row[8] == 'трудно решить':
        value += 1
    elif row[8] == 'ученым':
        value += 2
    # 10
    if row[9] == 'чтобы вас заранее спросили, какой подарок вам хочется':
        value += 2
    elif row[9] == 'трудно сказать':
        value += 1
    elif row[9] == 'чтобы подарок был для вас сюрпризом':
        value += 0

    return value

def calc_e_sten(ser: pd.Series):
    """
    Функция для подсчета Стена
    :param ser: пол и значение
    :return:
    """
    row = ser.tolist() # превращаем в список
    sex = row[0] # пол
    value = row[1] # значение которое нужно обработать

    if sex == 'Женский':
        if 0 <= value <= 2:
            return 1
        elif value == 3:
            return 2
        elif value == 4:
            return 3
        elif 5 <= value <= 6:
            return 4
        elif value == 7:
            return 5
        elif value == 8:
            return 6
        elif 9 <= value <= 10:
            return 7
        elif value == 11:
            return 8
        elif 12 <= value <= 13:
            return 9
        else:
            return 10
    else:
        if 0 <= value <= 4:
            return 1
        elif 5 <= value <= 6:
            return 2
        elif value == 7:
            return 3
        elif value == 8:
            return 4
        elif value == 9:
            return 5
        elif value == 10:
            return 6
        elif value == 11:
            return 7
        elif value == 12:
            return 8
        elif value == 13:
            return 9
        else:
            return 10

# F
def calc_f_value(row):
    """
    Фнукция подсчета значения
    :param row:
    :return:
    """
    value = 0 # сумматор

    # 1
    if row[0] == 'в шумных забавах':
        value += 2
    elif row[0] == 'трудно сказать':
        value += 1
    elif row[0] == 'в серьезной беседе о своих увлечениях':
        value += 0
    # 2
    if row[1] == 'да':
        value += 0
    elif row[1] == 'иногда':
        value += 1
    elif row[1] == 'редко':
        value += 2
    # 3
    if row[2] == 'да':
        value += 2
    elif row[2] == 'иногда':
        value += 1
    elif row[2] == 'нет':
        value += 0
    # 4
    if row[3] == 'быть самым популярным человеком в школе':
        value += 2
    elif row[3] == 'трудно сказать':
        value += 1
    elif row[3] == 'иметь самые лучшие оценки':
        value += 0
    # 5
    if row[4] == 'да':
        value += 2
    elif row[4] == 'иногда':
        value += 1
    elif row[4] == 'нет':
        value += 0
    # 6
    if row[5] == 'безопасную и с размеренным ритмом, хотя и требующую напряжения':
        value += 0
    elif row[5] == 'не уверен':
        value += 1
    elif row[5] == 'связанную с разъездами и встречами с новыми людьми':
        value += 2
    # 7
    if row[6] == 'да':
        value += 2
    elif row[6] == 'иногда':
        value += 1
    elif row[6] == 'нет':
        value += 0
    # 8
    if row[7] == 'вероятно, не стали бы этого делать':
        value += 0
    elif row[7] == 'не уверен':
        value += 1
    elif row[7] == 'определенно сделали бы':
        value += 2
    # 9
    if row[8] == 'думает':
        value += 0
    elif row[8] == 'трудно сказать':
        value += 1
    elif row[8] == 'действует':
        value += 2
    # 10
    if row[9] == 'да':
        value += 0
    elif row[9] == 'может быть':
        value += 1
    elif row[9] == 'нет':
        value += 2

    return value

def calc_f_sten(ser: pd.Series):
    """
    Функция для подсчета Стена
    :param ser: пол и значение
    :return:
    """
    row = ser.tolist() # превращаем в список
    sex = row[0] # пол
    value = row[1] # значение которое нужно обработать

    if sex == 'Женский':
        if 0 <= value <= 5:
            return 1
        elif value == 6:
            return 2
        elif 7 <= value <= 8:
            return 3
        elif 9 <= value <= 10:
            return 4
        elif 11<= value <= 12:
            return 5
        elif 13 <= value <= 14:
            return 6
        elif 15 <= value <= 16:
            return 7
        elif value == 17:
            return 8
        elif 18 <= value <= 19:
            return 9
        else:
            return 10
    else:
        if 0 <= value <= 4:
            return 1
        elif 5 <= value <= 6:
            return 2
        elif 7 <= value <= 8:
            return 3
        elif 9 <= value <= 10:
            return 4
        elif 11 <=value <= 12:
            return 5
        elif 13 <= value <= 14:
            return 6
        elif value == 15:
            return 7
        elif 16 <= value <= 17:
            return 8
        elif 18 <= value <= 19:
            return 9
        else:
            return 10

# G
def calc_g_value(row):
    """
    Фнукция подсчета значения
    :param row:
    :return:
    """
    value = 0 # сумматор

    # 1
    if row[0] == 'надежный вожак':
        value += 2
    elif row[0] == 'нечто среднее':
        value += 1
    elif row[0] == 'симпатичный, приятный человек':
        value += 0
    # 2
    if row[1] == 'часто':
        value += 2
    elif row[1] == 'иногда':
        value += 1
    elif row[1] == 'редко':
        value += 0
    # 3
    if row[2] == 'да':
        value += 2
    elif row[2] == 'иногда':
        value += 1
    elif row[2] == 'нет':
        value += 0
    # 4
    if row[3] == 'присоединились бы к ним':
        value += 0
    elif row[3] == 'трудно решить':
        value += 1
    elif row[3] == 'делали бы то, что считаете правильным':
        value += 2
    # 5
    if row[4] == 'очень часто просто не делаете этого':
        value += 0
    elif row[4] == 'нечто среднее':
        value += 1
    elif row[4] == 'всегда делаете это вовремя':
        value += 2
    # 6
    if row[5] == 'да':
        value += 2
    elif row[5] == 'иногда':
        value += 1
    elif row[5] == 'нет':
        value += 0
    # 7
    if row[6] == 'да':
        value += 0
    elif row[6] == 'иногда':
        value += 1
    elif row[6] == 'нет':
        value += 2
    # 8
    if row[7] == 'да':
        value += 0
    elif row[7] == 'может быть':
        value += 1
    elif row[7] == 'нет':
        value += 2
    # 9
    if row[8] == 'предоставите ему возможность справиться самому':
        value += 0
    elif row[8] == 'трудно сказать':
        value += 1
    elif row[8] == 'поможете ему':
        value += 2
    # 10
    if row[9] == 'всегда':
        value += 2
    elif row[9] == 'как правило':
        value += 1
    elif row[9] == 'редко':
        value += 0

    return value

def calc_g_sten(ser: pd.Series):
    """
    Функция для подсчета Стена
    :param ser: пол и значение
    :return:
    """
    row = ser.tolist() # превращаем в список
    sex = row[0] # пол
    value = row[1] # значение которое нужно обработать

    if sex == 'Женский':
        if 0 <= value <= 3:
            return 1
        elif 4 <= value <= 5:
            return 2
        elif value == 6:
            return 3
        elif 7 <= value <= 8:
            return 4
        elif value == 9:
            return 5
        elif 10 <= value <= 11:
            return 6
        elif value == 12:
            return 7
        elif 13 <= value <= 14:
            return 8
        elif 15 <= value <= 16:
            return 9
        else:
            return 10
    else:
        if 0 <= value <= 3:
            return 1
        elif value == 4:
            return 2
        elif 5 <= value <= 6:
            return 3
        elif value == 7:
            return 4
        elif value == 8:
            return 5
        elif 9 <= value <= 10:
            return 6
        elif value == 11:
            return 7
        elif value == 12:
            return 8
        elif 13 <= value <= 14:
            return 9
        else:
            return 10

# H
def calc_h_value(row):
    """
    Фнукция подсчета значения
    :param row:
    :return:
    """
    value = 0 # сумматор

    # 1
    if row[0] == 'да':
        value += 0
    elif row[0] == 'возможно':
        value += 1
    elif row[0] == 'нет':
        value += 2
    # 2
    if row[1] == 'да':
        value += 2
    elif row[1] == 'может быть':
        value += 1
    elif row[1] == 'нет':
        value += 0
    # 3
    if row[2] == 'да':
        value += 0
    elif row[2] == 'может быть':
        value += 1
    elif row[2] == 'нет':
        value += 2
    # 4
    if row[3] == 'да':
        value += 2
    elif row[3] == 'возможно':
        value += 1
    elif row[3] == 'нет':
        value += 0
    # 5
    if row[4] == 'почти всегда':
        value += 0
    elif row[4] == 'иногда':
        value += 1
    elif row[4] == 'никогда':
        value += 2
    # 6
    if row[5] == 'показать лично':
        value += 2
    elif row[5] == 'трудно сказать':
        value += 1
    elif row[5] == 'чтоб ее показал кто-то другой без вашего личного присутствия':
        value += 0
    # 7
    if row[6] == 'склонным к унынию и переменам настроения':
        value += 0
    elif row[6] == 'трудно решить':
        value += 1
    elif row[6] == 'вовсе не унылым':
        value += 2
    # 8
    if row[7] == 'очень часто':
        value += 2
    elif row[7] == 'иногда':
        value += 1
    elif row[7] == 'почти никогда':
        value += 0
    # 9
    if row[8] == 'часто':
        value += 0
    elif row[8] == 'иногда':
        value += 1
    elif row[8] == 'никогда':
        value += 2
    # 10
    if row[9] == 'да':
        value += 2
    elif row[9] == 'может быть':
        value += 1
    elif row[9] == 'нет':
        value += 0
    return value


def calc_h_sten(ser: pd.Series):
    """
    Функция для подсчета Стена
    :param ser: пол и значение
    :return:
    """
    row = ser.tolist() # превращаем в список
    sex = row[0] # пол
    value = row[1] # значение которое нужно обработать

    if sex == 'Женский':
        if 0 <= value <= 3:
            return 1
        elif 4 <= value <= 5:
            return 2
        elif 6 <= value <= 7:
            return 3
        elif 8 <= value <= 9:
            return 4
        elif 10 <= value <= 11:
            return 5
        elif value == 12:
            return 6
        elif 13 <= value <= 14:
            return 7
        elif 15 <= value <= 16:
            return 8
        elif 17 <= value <= 18:
            return 9
        else:
            return 10
    else:
        if 0 <= value <= 4:
            return 1
        elif 5 <= value <= 6:
            return 2
        elif value == 7:
            return 3
        elif 8 <= value <= 9:
            return 4
        elif 10 <= value <= 11:
            return 5
        elif value == 12:
            return 6
        elif value == 13:
            return 7
        elif 14 <= value <= 15:
            return 8
        elif 16 <= value <= 17:
            return 9
        else:
            return 10

# I
def calc_i_value(row):
    """
    Фнукция подсчета значения
    :param row:
    :return:
    """
    value = 0 # сумматор

    # 1
    if row[0] == 'да':
        value += 0
    elif row[0] == 'может быть':
        value += 1
    elif row[0] == 'нет':
        value += 2
    # 2
    if row[1] == 'да':
        value += 2
    elif row[1] == 'нечто среднее':
        value += 1
    elif row[1] == 'нет':
        value += 0
    # 3
    if row[2] == 'да':
        value += 0
    elif row[2] == 'трудно сказать':
        value += 1
    elif row[2] == 'нет':
        value += 2
    # 4
    if row[3] == 'подождать их':
        value += 2
    elif row[3] == 'трудно решить':
        value += 1
    elif row[3] == 'поторопить их':
        value += 0
    # 5
    if row[4] == 'знаменитым спортсменом':
        value += 0
    elif row[4] == 'трудно решить':
        value += 1
    elif row[4] == 'знаменитым поэтом':
        value += 2
    # 6
    if row[5] == 'в живописном парке':
        value += 2
    elif row[5] == 'не уверен':
        value += 1
    elif row[5] == 'на стадионе':
        value += 0
    # 7
    if row[6] == 'смотреть рискованные лодочные гонки':
        value += 0
    elif row[6] == 'не уверен':
        value += 1
    elif row[6] == 'прогуливаться красивым берегом с другом':
        value += 2
    # 8
    if row[7] == 'посмотреть мотогонки':
        value += 0
    elif row[7] == 'трудно сказать':
        value += 1
    elif row[7] == 'послушать музыку на открытой эстраде':
        value += 2
    # 9
    if row[8] == 'музыкальные':
        value += 2
    elif row[8] == 'трудно сказать':
        value += 1
    elif row[8] == 'о войне':
        value += 0
    # 10
    if row[9] == 'да, часто':
        value += 2
    elif row[9] == 'иногда':
        value += 1
    elif row[9] == 'нет, никогда':
        value += 0

    return value

def calc_i_sten(ser: pd.Series):
    """
    Функция для подсчета Стена
    :param ser: пол и значение
    :return:
    """
    row = ser.tolist() # превращаем в список
    sex = row[0] # пол
    value = row[1] # значение которое нужно обработать

    if sex == 'Женский':
        if 0 <= value <= 5:
            return 1
        elif 6 <= value <= 7:
            return 2
        elif 8 <= value <= 9:
            return 3
        elif value == 10:
            return 4
        elif 11 <= value <= 12:
            return 5
        elif 13 <= value <= 14:
            return 6
        elif 15 <= value <= 16:
            return 7
        elif value == 17:
            return 8
        elif 18 <= value <= 19:
            return 9
        else:
            return 10
    else:
        if 0 <= value <= 1:
            return 1
        elif value == 2:
            return 2
        elif 3 <= value <= 4:
            return 3
        elif 5 <= value <= 6:
            return 4
        elif 7 <= value <= 8:
            return 5
        elif 9 <= value <= 10:
            return 6
        elif value == 11:
            return 7
        elif 12 <= value <= 13:
            return 8
        elif 14 <= value <= 15:
            return 9
        else:
            return 10

# J
def calc_j_value(row):
    """
    Фнукция подсчета значения
    :param row:
    :return:
    """
    value = 0 # сумматор

    # 1
    if row[0] == 'да':
        value += 0
    elif row[0] == 'может быть':
        value += 1
    elif row[0] == 'нет':
        value += 2
    # 2
    if row[1] == 'да':
        value += 2
    elif row[1] == 'трудно сказать':
        value += 1
    elif row[1] == 'нет':
        value += 0
    # 3
    if row[2] == 'да':
        value += 0
    elif row[2] == 'может быть':
        value += 1
    elif row[2] == 'нет':
        value += 2
    # 4
    if row[3] == 'один, с книгой или коллекцией почтовых марок':
        value += 2
    elif row[3] == 'трудно решить':
        value += 1
    elif row[3] == 'занимаясь под руководством других каким-либо общим делом':
        value += 0
    # 5
    if row[4] == 'общаетесь с друзьями':
        value += 0
    elif row[4] == 'трудно сказать':
        value += 1
    elif row[4] == 'наблюдаете за происходящим':
        value += 2
    # 6
    if row[5] == 'да':
        value += 2
    elif row[5] == 'не уверен':
        value += 1
    elif row[5] == 'нет':
        value += 0
    # 7
    if row[6] == 'забудете об этом':
        value += 0
    elif row[6] == 'трудно сказать':
        value += 1
    elif row[6] == 'не упустите случая припомнить':
        value += 2
    # 8
    if row[7] == 'да':
        value += 2
    elif row[7] == 'может быть':
        value += 1
    elif row[7] == 'нет':
        value += 0
    # 9
    if row[8] == 'организовать классный пикник':
        value += 0
    elif row[8] == 'трудно сказать':
        value += 1
    elif row[8] == 'изучать в лесу различные породы деревьев':
        value += 2
    # 10
    if row[9] == 'занимаете особую позицию':
        value += 2
    elif row[9] == 'трудно сказать':
        value += 1
    elif row[9] == 'соглашаетесь с остальными':
        value += 0

    return value


def calc_j_sten(ser: pd.Series):
    """
    Функция для подсчета Стена
    :param ser: пол и значение
    :return:
    """
    row = ser.tolist() # превращаем в список
    sex = row[0] # пол
    value = row[1] # значение которое нужно обработать

    if sex == 'Женский':
        if 0 <= value <= 2:
            return 1
        elif 3 <= value <= 4:
            return 2
        elif value == 5:
            return 3
        elif 6 <= value <= 7:
            return 4
        elif value == 8:
            return 5
        elif 9 <= value <= 10:
            return 6
        elif value == 11:
            return 7
        elif 12 <= value <= 13:
            return 8
        elif 14 <= value <= 15:
            return 9
        else:
            return 10
    else:
        if 0 <= value <= 3:
            return 1
        elif value == 4:
            return 2
        elif 5 <= value <= 6:
            return 3
        elif value == 7:
            return 4
        elif 8 <=value <= 9:
            return 5
        elif value == 10:
            return 6
        elif 11 <= value <= 12:
            return 7
        elif 13 <= value <= 14:
            return 8
        elif 15 <= value <= 16:
            return 9
        else:
            return 10

# Q1
def calc_o_value(row):
    """
    Фнукция подсчета значения
    :param row:
    :return:
    """
    value = 0 # сумматор

    # 1
    if row[0] == 'да':
        value += 0
    elif row[0] == 'не уверен':
        value += 1
    elif row[0] == 'нет':
        value += 2
    # 2
    if row[1] == 'да':
        value += 2
    elif row[1] == 'может быть':
        value += 1
    elif row[1] == 'нет':
        value += 0
    # 3
    if row[2] == 'да':
        value += 0
    elif row[2] == 'трудно сказать':
        value += 1
    elif row[2] == 'нет':
        value += 2
    # 4
    if row[3] == 'да':
        value += 2
    elif row[3] == 'трудно сказать':
        value += 1
    elif row[3] == 'нет':
        value += 0
    # 5
    if row[4] == 'да':
        value += 0
    elif row[4] == 'может быть':
        value += 1
    elif row[4] == 'нет':
        value += 2
    # 6
    if row[5] == 'готовы почти что «прыгать от радости»':
        value += 2
    elif row[5] == 'трудно решить':
        value += 1
    elif row[5] == 'внутренне радуетесь, но внешне кажетесь спокойным':
        value += 0
    # 7
    if row[6] == 'да':
        value += 0
    elif row[6] == 'нечто среднее':
        value += 1
    elif row[6] == 'нет':
        value += 2
    # 8
    if row[7] == 'да':
        value += 2
    elif row[7] == 'трудно сказать':
        value += 1
    elif row[7] == 'нет':
        value += 0
    # 9
    if row[8] == 'да':
        value += 0
    elif row[8] == 'может быть':
        value += 1
    elif row[8] == 'нет':
        value += 2
    # 10
    if row[9] == 'часто':
        value += 2
    elif row[9] == 'иногда':
        value += 1
    elif row[9] == 'редко':
        value += 0

    return value

def calc_o_sten(ser: pd.Series):
    """
    Функция для подсчета Стена
    :param ser: пол и значение
    :return:
    """
    row = ser.tolist() # превращаем в список
    sex = row[0] # пол
    value = row[1] # значение которое нужно обработать

    if sex == 'Женский':
        if 0 <= value <= 2:
            return 1
        elif value == 3:
            return 2
        elif 4 <= value <= 5:
            return 3
        elif 6 <= value <= 7:
            return 4
        elif 8 <= value <= 9:
            return 5
        elif 10 <= value <= 11:
            return 6
        elif value == 12:
            return 7
        elif 13 <= value <= 14:
            return 8
        elif 15 <= value <= 16:
            return 9
        else:
            return 10
    else:
        if 0 <= value <= 1:
            return 1
        elif value == 2:
            return 2
        elif 3 <= value <= 4:
            return 3
        elif 5 <= value <= 6:
            return 4
        elif 7 <= value <= 8:
            return 5
        elif 9 <= value <= 10:
            return 6
        elif value == 11:
            return 7
        elif 12 <= value <= 13:
            return 8
        elif 14 <= value <= 15:
            return 9
        else:
            return 10

# Q2
def calc_q_two_value(row):
    """
    Фнукция подсчета значения
    :param row:
    :return:
    """
    value = 0 # сумматор

    # 1
    if row[0] == 'да':
        value += 0
    elif row[0] == 'иногда':
        value += 1
    elif row[0] == 'нет':
        value += 2
    # 2
    if row[1] == 'да':
        value += 2
    elif row[1] == 'не уверен':
        value += 1
    elif row[1] == 'нет':
        value += 0
    # 3
    if row[2] == 'принимаете в этом активное участие':
        value += 0
    elif row[2] == 'нечто среднее':
        value += 1
    elif row[2] == 'обычно только наблюдаете со стороны':
        value += 2
    # 4
    if row[3] == 'один':
        value += 2
    elif row[3] == 'трудно решить':
        value += 1
    elif row[3] == 'с группой':
        value += 0
    # 5
    if row[4] == 'позвать несколько друзей и заняться чем-нибудь вместе':
        value += 0
    elif row[4] == 'трудно ответить':
        value += 1
    elif row[4] == 'почитать любимую книгу или заняться любимым делом':
        value += 2
    # 6
    if row[5] == 'инженером-мостостроителем':
        value += 2
    elif row[5] == 'трудно решить':
        value += 1
    elif row[5] == 'артистом балета или цирка':
        value += 0
    # 7
    if row[6] == 'да':
        value += 0
    elif row[6] == 'трудно сказать':
        value += 1
    elif row[6] == 'нет':
        value += 2
    # 8
    if row[7] == 'да':
        value += 2
    elif row[7] == 'может быть':
        value += 1
    elif row[7] == 'нет':
        value += 0
    # 9
    if row[8] == 'дурачиться':
        value += 0
    elif row[8] == 'трудно сказать':
        value += 1
    elif row[8] == 'быть более серьезными':
        value += 2
    # 10
    if row[9] == 'орлом на горной вершине':
        value += 2
    elif row[9] == 'трудно сказать':
        value += 1
    elif row[9] == 'тюленем в стаде, на берегу моря':
        value += 0

    return value

def calc_q_two_sten(ser: pd.Series):
    """
    Функция для подсчета Стена
    :param ser: пол и значение
    :return:
    """
    row = ser.tolist() # превращаем в список
    sex = row[0] # пол
    value = row[1] # значение которое нужно обработать

    if sex == 'Женский':
        if 0 <= value <= 4:
            return 1
        elif 5 <= value <= 6:
            return 2
        elif value == 7:
            return 3
        elif value == 8:
            return 4
        elif value == 9:
            return 5
        elif value == 10:
            return 6
        elif 11 <= value <= 12:
            return 7
        elif value == 13:
            return 8
        elif value == 14:
            return 9
        else:
            return 10
    else:
        if 0 <= value <= 4:
            return 1
        elif value == 5:
            return 2
        elif 6 <= value <= 7:
            return 3
        elif 8 <= value <= 9:
            return 4
        elif value == 10:
            return 5
        elif 11 <= value <= 12:
            return 6
        elif value == 13:
            return 7
        elif 14 <= value <= 15:
            return 8
        elif 16 <= value <= 17:
            return 9
        else:
            return 10

# Q3
def calc_q_three_value(row):
    """
    Фнукция подсчета значения
    :param row:
    :return:
    """
    value = 0 # сумматор

    # 1
    if row[0] == 'актером эстрады':
        value += 0
    elif row[0] == 'трудно сказать':
        value += 1
    elif row[0] == 'врачом':
        value += 2
    # 2
    if row[1] == 'да':
        value += 2
    elif row[1] == 'может быть':
        value += 1
    elif row[1] == 'нет':
        value += 0
    # 3
    if row[2] == 'да':
        value += 0
    elif row[2] == 'может быть':
        value += 1
    elif row[2] == 'нет':
        value += 2
    # 4
    if row[3] == 'стараться не обращать внимания на это, пока не остынешь':
        value += 2
    elif row[3] == 'трудно решить':
        value += 1
    elif row[3] == 'найти способ разрядиться':
        value += 0
    # 5
    if row[4] == 'да':
        value += 0
    elif row[4] == 'может быть':
        value += 1
    elif row[4] == 'нет':
        value += 2
    # 6
    if row[5] == 'да':
        value += 2
    elif row[5] == 'трудно сказать':
        value += 1
    elif row[5] == 'нет':
        value += 0
    # 7
    if row[6] == 'часто':
        value += 0
    elif row[6] == 'иногда':
        value += 1
    elif row[6] == 'нет':
        value += 2
    # 8
    if row[7] == 'да':
        value += 2
    elif row[7] == 'не уверен':
        value += 1
    elif row[7] == 'нет':
        value += 0
    # 9
    if row[8] == 'да':
        value += 0
    elif row[8] == 'может быть':
        value += 1
    elif row[8] == 'нет':
        value += 2
    # 10
    if row[9] == 'да':
        value += 2
    elif row[9] == 'нечто среднее':
        value += 1
    elif row[9] == 'нет':
        value += 0

    return value

def calc_q_three_sten(ser: pd.Series):
    """
    Функция для подсчета Стена
    :param ser: пол и значение
    :return:
    """
    row = ser.tolist() # превращаем в список
    sex = row[0] # пол
    value = row[1] # значение которое нужно обработать

    if sex == 'Женский':
        if 0 <= value <= 4:
            return 1
        elif value == 5:
            return 2
        elif 6 <= value <= 7:
            return 3
        elif value == 8:
            return 4
        elif 9<= value <= 10:
            return 5
        elif value == 11:
            return 6
        elif 12 <= value <= 13:
            return 7
        elif value == 14:
            return 8
        elif 15 <= value <= 16:
            return 9
        else:
            return 10
    else:
        if 0 <= value <= 4:
            return 1
        elif 5 <= value <= 6:
            return 2
        elif 7 <= value <= 8:
            return 3
        elif value == 9:
            return 4
        elif value == 10:
            return 5
        elif 11 <= value <= 12:
            return 6
        elif 13 <= value <= 14:
            return 7
        elif value == 15:
            return 8
        elif value == 16:
            return 9
        else:
            return 10

# Q4
def calc_q_four_value(row):
    """
    Фнукция подсчета значения
    :param row:
    :return:
    """
    value = 0 # сумматор

    # 1
    if row[0] == 'да':
        value += 0
    elif row[0] == 'возможно':
        value += 1
    elif row[0] == 'нет':
        value += 2
    # 2
    if row[1] == 'да, часто':
        value += 2
    elif row[1] == 'иногда':
        value += 1
    elif row[1] == 'нет, почти никогда':
        value += 0
    # 3
    if row[2] == 'просто получаете удовольствие':
        value += 0
    elif row[2] == 'трудно решить':
        value += 1
    elif row[2] == 'волнуетесь, благополучно ли она закончится':
        value += 2
    # 4
    if row[3] == 'да':
        value += 2
    elif row[3] == 'нечто среднее':
        value += 1
    elif row[3] == 'нет':
        value += 0
    # 5
    if row[4] == 'остаетесь совершенно спокойным и хладнокровным':
        value += 2
    elif row[4] == 'нечто среднее':
        value += 1
    elif row[4] == 'становитесь очень напряженным и теряете покой':
        value += 0
    # 6
    if row[5] == 'да':
        value += 2
    elif row[5] == 'может быть':
        value += 1
    elif row[5] == 'нет':
        value += 0
    # 7
    if row[6] == 'говорите «В конце концов, это ведь только игра»':
        value += 0
    elif row[6] == 'трудно ответить':
        value += 1
    elif row[6] == 'сердитесь или злитесь на себя':
        value += 2
    # 8
    if row[7] == 'да':
        value += 2
    elif row[7] == 'иногда':
        value += 1
    elif row[7] == 'нет':
        value += 0
    # 9
    if row[8] == 'даете ему высказать всё, что он хочет':
        value += 0
    elif row[8] == 'трудно сказать':
        value += 1
    elif row[8] == 'обычно перебиваете его раньше, чем он закончит':
        value += 2
    # 10
    if row[9] == 'да':
        value += 2
    elif row[9] == 'может быть':
        value += 1
    elif row[9] == 'нет':
        value += 0

    return value

def calc_q_four_sten(ser: pd.Series):
    """
    Функция для подсчета Стена
    :param ser: пол и значение
    :return:
    """
    row = ser.tolist() # превращаем в список
    sex = row[0] # пол
    value = row[1] # значение которое нужно обработать

    if sex == 'Женский':
        if 0 <= value <= 4:
            return 1
        elif 5 <= value <= 6:
            return 2
        elif value == 7:
            return 3
        elif 8 <= value <= 9:
            return 4
        elif 10 <= value <= 11:
            return 5
        elif value == 12:
            return 6
        elif 13 <= value <= 14:
            return 7
        elif 15 <= value <= 16:
            return 8
        elif 17 <= value <= 18:
            return 9
        else:
            return 10
    else:
        if 0 <= value <= 3:
            return 1
        elif 4 <= value <= 5:
            return 2
        elif value == 6:
            return 3
        elif 7 <= value <= 8:
            return 4
        elif value == 9:
            return 5
        elif value == 10:
            return 6
        elif 11 <= value <= 12:
            return 7
        elif value == 13:
            return 8
        elif 14 <= value <= 15:
            return 9
        else:
            return 10

def create_itog_stens(row):
    """
    Функция для создания строки с итоговым стеном
    :param row: строка с результатами
    :return:
    """
    lst_out = list(map(str,row))
    return '-'.join(lst_out)

def calc_range(value):
    """
    Функция для подсчета диапазонов
    :param value: значение
    :return:
    """
    if 1 <= value <= 3:
        return '1-3'
    elif 4 <=value <= 7:
        return '4-7'
    else:
        return '8-10'



def create_result_krshspq(base_df:pd.DataFrame, out_dct:dict, lst_svod_cols:list):
    """
    Функция для подсчета результата если указаны колонки по которым нужно провести свод
    :param df: датафрейм с результатами
    :param out_dct: словарь с уже подсчитанными базовыми данными
    :param lst_svod_cols: список сводных колонок
    :return: словарь
    """

    lst_reindex_main_level_cols = lst_svod_cols.copy()
    lst_reindex_main_level_cols.extend( ['низкий уровень','средний уровень','высокий уровень',
                                   'Итого'])  # Основная шкала












def processing_kettel_pf_ruk_sok(base_df: pd.DataFrame, answers_df: pd.DataFrame,lst_svod_cols:list):
    """
    Функция для обработки
    :param base_df: часть датафрейма с описательными колонками
    :param answers_df: часть датафрейма с ответами
    :param lst_svod_cols:  список с колонками по которым нужно делать свод
    """
    union_base_df = base_df.copy() # делаем копию анкетной части чтобы потом соединить ее с ответной частью
    quantity_cols_base_df = base_df.shape[1] # количество колонок в анкетной части


    # Проверяем наличие колонок Пол
    diff_req_cols = {'Пол','ФИО'}.difference(set(base_df.columns))
    if len(diff_req_cols) != 0:
        raise NotReqColumn

    # Проверяем на пол
    diff_sex = set(base_df['Пол'].unique()).difference({'Мужской', 'Женский'})
    if len(diff_sex) != 0:
        raise BadValueSex

    base_df['ФИО'] = base_df['ФИО'].fillna('Не заполнено')
    base_df['ФИО'] = base_df['ФИО'].astype(str)

    out_answer_df = base_df.copy()  # делаем копию для последующего соединения с сырыми ответами
    if len(answers_df.columns) != 142:  # проверяем количество колонок с вопросами
        raise BadCountColumnsKPFRS
    # очищаем названия колонок от возможных сочетаний .1 которые добавляет пандас при одинаковых колонках
    clean_df_lst = []
    for name_column in answers_df.columns:
        clean_name = re.sub(r'.\d+$', '', name_column)
        clean_df_lst.append(clean_name)

    answers_df.columns = clean_df_lst

    lst_check_cols = ['Вы поняли инструкцию?',
                      'Во время коллективной загородной прогулки или похода вы бы предпочли:',
                      'Вы любите высказываться во время коллективного обсуждения.',
                      'Если вы сделали какую-то глупость, вам бывает настолько плохо, что хочется «провалиться сквозь землю».',
                      'Вам легко хранить увлекательный секрет.',
                      'Когда вы что-то решаете, вы:',
                      'Вы можете напряженно работать над чем-либо, не отвлекаясь, если стоит шум.',
                      'Когда предложения товарищей расходятся с вашими, вы не говорите, что ваше предложение лучше, потому что стараетесь не обидеть друзей.',
                      'Вы обычно просите кого-нибудь о помощи, когда самому вам трудно выполнить какое-то задание.',
                      'Вы предпочитаете проводить время:',

                      'Из этих характеристик вам больше подходит:',
                      'Собираясь на вечер или в гости, вы чувствуете, что вам не так уж интересно туда идти.',
                      'Если вы на кого-то справедливо сердитесь, вы обычно кричите.',
                      'Когда одноклассники(одногруппники) вас разыгрывают, вы обычно веселитесь вместе с остальными, не чувствуя ни малейшего огорчения.',
                      'Вас раздражает, если кто-то заговаривает с вами, когда вы о чем-то размышляете.',
                      'Вы можете сохранять бодрость, даже если дела идут плохо.',
                      'Вы стараетесь, чтобы ваши интересы и увлечения совпадали с интересами одноклассников(одногруппников).',
                      'У большинства людей больше друзей, чем у вас.',
                      'Вы предпочли бы быть:',
                      'Вы считаете, что ваша жизнь идет более гладко, чем у многих других.',

                      'Бывает так, что вы не можете сосредоточиться на чем-то из-за посторонних мыслей?',
                      'Вам хотелось бы играть на сцене, например, в школьной самодеятельности.',
                      'Слово «сильный» означает то же, что и слово:',
                      'Слово «правда» противоположно по смыслу слову:',
                      'Вы полностью понимаете то, что проходите в школе (техникуме, колледже).',
                      'Когда мел скрипит по доске, у вас от этого пробегает «мороз по коже».',
                      'Когда что-то никак не получается, вам удается сдерживать свое раздражение, не срывая его на других людях.',
                      'Если кто-то в разговоре перебивает вас, то вы:',
                      'Вы избегаете забираться в узкие пещеры (места) или подниматься на большую высоту.',
                      'Вы всегда не прочь показать другим, как хорошо вы можете работать по сравнению с остальными.',

                      'Вы спрашиваете совета у родителей относительно своих дел и поступков в школе (техникуме, колледже).',
                      'Вы можете беседовать с группой незнакомых людей, не запинаясь и не затрудняясь в выборе слов.',
                      'Когда люди говорят про вас что-то плохое, вас это сильно расстраивает.',
                      'Вам больше нравится смотреть соревнование по боксу, чем танцы на льду.',
                      'Если кто-то обидел вас, вы вскоре снова сможете ему довериться.',
                      'Вы чувствуете иногда, что мало на что годитесь и никогда не совершите ничего стоящего.',
                      'Когда группа людей что-то делает, вы:',
                      'Вы предпочли бы отправиться в путешествие:',
                      'Вас считают человеком, на которого всегда можно положиться и который всё сделает точно и как следует?',
                      'Читая приключенческую повесть, вы:',

                      'Вы испытываете раздражение, если приходится тихо сидеть и ждать, пока что-то начнется.',
                      'Вас раздражает, если люди берут ваши вещи без спроса.',
                      'Слово «покупать» противоположно по смыслу слову:',
                      'Слово «госпиталь» так относится к слову «больной», как слово «столовая» – к слову:',
                      'Вы всегда хорошо ладили со своими родителями, братьями и сестрами.',
                      'Если одноклассники(одногруппники) играют во что-то без вас, вы:',
                      'Люди говорят, что вы иногда несобранны и легко увлекаетесь, хотя они считают вас хорошим человеком.',
                      'Находясь в автобусе или поезде, вы говорите:',
                      'Вы бы предпочли:',
                      'Находясь в компании, вы часто шутите и рассказываете смешные истории.',

                      'Вы любите говорить ребятам о том, что нужно соблюдать правила.',
                      'Вас легко обидеть.',
                      'Когда другие, отставая, тормозят вашу работу, по-вашему, лучше:',
                      'Вы больше восхищаетесь:',
                      'Вы бы предпочли провести свободное время:',
                      'Вы считаете, что ваши дела идут хорошо и что вы делаете всё, что можно от вас ожидать.',
                      'Вам трудно вести себя так или быть таким, каким вас хотят видеть другие люди.',
                      'Если вам нечего делать вечером, вы бы предпочли:',
                      'Вам бы хотелось быть очень красивым, чтобы люди везде обращали на вас внимание.',
                      'Когда приближается что-то важное, например, экзамен или ответственное соревнование, вы:',

                      'Если кто-то включает громкую музыку, когда вы пытаетесь работать, вы чувствуете, что вам необходимо удалиться.',
                      'Вы легко схватываете новый ритм в танце или в музыке.',
                      'Слово «шоссе» так относится к слову «колесо», как слово «тропа» – к слову:',
                      'Если мать Сережи – сестра моего отца, то Сережин отец приходится моему брату:',
                      'Вы часто с увлечением составляете большие планы, а потом выясняется, что ничего из этого не выйдет.',
                      'Если вас застали в затруднительной, неловкой ситуации, вы можете превратить всё в шутку и выйти из положения.',
                      'Когда вы запоминаете что-то иначе, чем другие, вы часто спорите о том, что произошло на самом деле.',
                      'У вас бывает иногда так хорошо на душе, что буквально хочется петь и кричать.',
                      'Вы бы предпочли работу:',
                      'Вы любите делать что-то совершенно неожиданное и поражающее других.',

                      'Если бы все стали делать нечто такое, что вы считаете неправильным, вы:',
                      'Вы можете нормально работать, не ощущая неловкости, если за вами наблюдают.',
                      'Вы бы предпочли провести свободное время:',
                      'Отдыхая на море, на озере, вы бы предпочли:',
                      'Находясь в компании, вы большей частью:',
                      'Вы всегда можете определить свои чувства, например, отличить усталость от скуки.',
                      'Когда у вас всё великолепно, вы:',
                      'Вы бы предпочли быть:',
                      'Если вам что-то сильно досаждает, по-вашему, лучше:',
                      'Вы говорите иногда глупости только для того, чтобы посмотреть, что скажут на это другие.',

                      'Если вы проигрываете важную игру, вы:',
                      'Вы стараетесь избегать переполненных автобусов и многолюдных улиц, даже если это удлиняет дорогу.',
                      'Слово «обычно» обозначает то же самое, что и слово:',
                      'Бабушка дочери сестры моего брата – это:',
                      'У вас почти всегда хорошее настроение.',
                      'Если у вас всё время что-нибудь портится или ломается, вы, тем не менее, сохраняете спокойствие.',
                      'Вы когда-либо чувствовали неудовлетворенность и говорили себе: «Я наверняка мог бы сделать нашу школу (техникум, колледж) лучше, чем это удается учителям(преподавателям)!»',
                      'Вы хотели бы быть:',
                      'Если бы представился случай совершить что-то действительно необычное и увлекательное, но в то же время опасное, вы:',
                      'Когда вам нужно сделать что-то по дому, вы:',

                      'Вы обычно обсуждаете свои дела с родителями:',
                      'Вы участвуете в обсуждении каких-либо дел вашего класса(группы):',
                      'Если какая-то сделанная вами работа должна быть показана важному лицу, вы предпочли бы:',
                      'Погожим вечером вы бы предпочли:',
                      'Ваши манеры лучше, чем у большинства ваших друзей.',
                      'Вы легко усваиваете новые игры?',
                      'Вы считаете, что большинству людей вы кажетесь порою угрюмым и унылым.',
                      'Можно сказать, что вы, как и большинство людей, слегка побаиваетесь разряда молний.',
                      'Вы любите, когда вам подробно объясняют, что и как следует делать.',
                      'Вы замечали иногда, просыпаясь утром, что так ворочались и метались во сне, что вся постель в беспорядке.',

                      'Когда вы по тихой, безлюдной улице возвращаетесь домой вечером, вам часто кажется, что кто-то идет за вами.',
                      'Вам неприятно в разговорах с одноклассниками(одногруппниками) рассказывать о своих переживаниях.',
                      'Попадая в новую компанию, вы:',
                      'Прочитайте пять слов: «циркуль», «отвёртка», «карандаш», «бумага», «линейка». Отметьте слово, которое не подходит к остальным:',
                      'Бывает так, что у вас без определенных причин резко изменяется настроение.',
                      'Когда вы слушаете радио или смотрите телевизор, а вокруг смеются, разговаривают, вам:',
                      'Если в компании вы случайно скажете что-то неудачно или невпопад, то вы долго помните об этом и испытываете неловкость.',
                      'Вы, бывало, всерьез думали о том, что могли бы стать видным общественно-политическим деятелем, известным на всю страну.',
                      'Вас чаще считают человеком, который:',
                      'Вас легко вовлечь в действия, которые, как вам известно, являются плохими и неправильными.',

                      'Вы бы расстроились, если бы вам пришлось переезжать на новое место и заводить там новых друзей.',
                      'Вы считаете себя:',
                      'Вы часто проводите время или делаете что-то вместе с группой(классом).',
                      'Вы больше любите фильмы:',
                      'Если кто-то испортил принадлежащую вам вещь, вы:',
                      'Можно сказать, что вы довольно взыскательны и даже привередливы в выборе друзей.',
                      'Вам легко подойти и представиться важному лицу.',
                      'Вы считаете, что при совместном обсуждении вопросов люди часто тратят больше времени и принимают худшее решение, чем это сделал бы один человек.',
                      'Вы считаете, что делаете то, что должны делать в жизни.',
                      'Вы чувствуете себя порой настолько запутавшимся, что сами не понимаете, что делаете.',

                      'Если кто-то спорит с вами, то вы:',
                      'Если бы пришлось выбирать, вы предпочли бы жить:',
                      'Работая на железной дороге, вы предпочли бы быть:',
                      'Прочтите эти пять слов: «внизу», «около», «над», «позади», «между». Слово, которое не подходит к остальным:',
                      'Если вас просят взять на себя новое трудное дело, вы:',
                      'Если вы поднимете руку для ответа и другие одновременно делают то же, вы испытываете возбуждение.',
                      'Вы предпочли бы быть:',
                      'В свой день рождения вы предпочитаете:',
                      'Вы очень заботитесь о том, чтобы не задеть и не обидеть других, даже в шутку.',
                      'Если вы видите незнакомого человека с тяжелым чемоданом, вы:',

                      'Перед тем как высказать что-то в классе(группе), вы заранее убеждаетесь в собственной правоте.',
                      'Бывает так, что из боязни последствий вы стараетесь уклониться от принятия решения.',
                      'В угрожающей ситуации вы можете улыбаться и сохранять спокойствие.',
                      'Вам случается почти что плакать над некоторыми книгами или пьесами.',
                      'Оказавшись за городом, вы бы предпочли:',
                      'Во время коллективного обсуждения вы часто замечаете, что:',
                      'Ваши чувства бывают так напряжены, что вы, кажется, готовы «взорваться» от их избытка.',
                      'Вы предпочитаете друзей, которые любят:',
                      'Если бы вы не были человеком, вы бы предпочли быть:',
                      'Вы обычно точный и аккуратный человек.',
                      'Вам действуют на нервы мелкие неприятности, даже если вы знаете, что они не очень существенны.',
                      'Вы уверены, что ответили на все вопросы?'
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
        raise BadOrderKPFRS

    valid_values = [['да','не уверен','нет'],
                    ['в одиночку осматривать лес','трудно сказать','играть с товарищами вокруг костра'],
                    ['да','иногда','нет'],
                    ['да','может быть','нет'],
                    ['да','иногда','нет'],
                    ['сомневаетесь – вдруг захочется изменить свое решение','верно нечто среднее','чувствуете уверенность, что решение останется в силе'],
                    ['да','возможно','нет'],
                    ['да','иногда','нет'],
                    ['редко','иногда','часто'],
                    ['в шумных забавах','трудно сказать','в серьезной беседе о своих увлечениях'],

                    ['надежный вожак','нечто среднее','симпатичный, приятный человек'],
                    ['да','возможно','нет'],
                    ['да','может быть','нет'],
                    ['да','может быть','нет'],
                    ['да','трудно сказать','нет'],
                    ['да','не уверен','нет'],
                    ['да','иногда','нет'],
                    ['да','не уверен','нет'],
                    ['актером эстрады','трудно сказать','врачом'],
                    ['да','возможно','нет'],

                    ['да, часто','иногда','нет, почти никогда'],
                    ['да','не уверен','нет'],
                    ['могущественный','суровый','выносливый'],
                    ['фантазия','ложь','отрицание'],
                    ['да','обычно','нет'],
                    ['да','может быть','нет'],
                    ['часто','иногда','редко'],
                    ['уступаете и даете ему высказаться','трудно решить','даете понять, что это невежливо, и не позволяете прерывать себя'],
                    ['да','иногда','редко'],
                    ['да','иногда','нет'],

                    ['часто','иногда','редко'],
                    ['да','может быть','нет'],
                    ['да','нечто среднее','нет'],
                    ['да','трудно сказать','нет'],
                    ['да','может быть','нет'],
                    ['да','может быть','нет'],
                    ['принимаете в этом активное участие','нечто среднее','обычно только наблюдаете со стороны'],
                    ['один','трудно решить','с группой'],
                    ['да','может быть','нет'],
                    ['просто получаете удовольствие','трудно решить','волнуетесь, благополучно ли она закончится'],

                    ['да','нечто среднее','нет'],
                    ['да','иногда','нет'],
                    ['давать','одалживать','продавать'],
                    ['голодный','еда','обед'],
                    ['да','трудно сказать','нет'],
                    ['считаете это простой случайностью','нечто среднее','обижаетесь и сердитесь'],
                    ['да','возможно','нет'],
                    ['своим обычным голосом','нечто среднее','как можно тише'],
                    ['быть самым популярным человеком в школе','трудно сказать','иметь самые лучшие оценки'],
                    ['да','иногда','нет'],

                    ['да','иногда','нет'],
                    ['да','может быть','нет'],
                    ['подождать их','трудно решить','поторопить их'],
                    ['знаменитым спортсменом','трудно решить','знаменитым поэтом'],
                    ['один, с книгой или коллекцией почтовых марок','трудно решить','занимаясь под руководством других каким-либо общим делом'],
                    ['да','трудно сказать','нет'],
                    ['да','трудно сказать','нет'],
                    ['позвать несколько друзей и заняться чем-нибудь вместе','трудно ответить','почитать любимую книгу или заняться любимым делом'],
                    ['да','может быть','нет'],
                    ['остаетесь совершенно спокойным и хладнокровным','нечто среднее','становитесь очень напряженным и теряете покой'],

                    ['да','может быть','нет'],
                    ['да','может быть','нет'],
                    ['пешеход','нога','телега'],
                    ['двоюродным братом','дедушкой','дядей'],
                    ['да','иногда','нет'],
                    ['как правило','трудно сказать','нет'],
                    ['да','может быть','нет'],
                    ['да','может быть','нет'],
                    ['безопасную и с размеренным ритмом, хотя и требующую напряжения','не уверен','связанную с разъездами и встречами с новыми людьми'],
                    ['да','иногда','нет'],

                    ['присоединились бы к ним','трудно решить','делали бы то, что считаете правильным'],
                    ['да','возможно','нет'],
                    ['в живописном парке','не уверен','на стадионе'],
                    ['смотреть рискованные лодочные гонки','не уверен','прогуливаться красивым берегом с другом'],
                    ['общаетесь с друзьями','трудно сказать','наблюдаете за происходящим'],
                    ['да','может быть','нет'],
                    ['готовы почти что «прыгать от радости»','трудно решить','внутренне радуетесь, но внешне кажетесь спокойным'],
                    ['инженером-мостостроителем','трудно решить','артистом балета или цирка'],
                    ['стараться не обращать внимания на это, пока не остынешь','трудно решить','найти способ разрядиться'],
                    ['да','может быть','нет'],

                    ['говорите «В конце концов, это ведь только игра»','трудно ответить','сердитесь или злитесь на себя'],
                    ['да','может быть','нет'],
                    ['иногда','всегда','как правило'],
                    ['моя мать','жена моего брата','моя племянница'],
                    ['да','среднее','нет'],
                    ['да','может быть','нет, я выхожу из себя'],
                    ['да','может быть','нет'],
                    ['архитектором-проектировщиком','трудно решить','певцом или музыкантом в эстрадном оркестре'],
                    ['вероятно, не стали бы этого делать','не уверен','определенно сделали бы'],
                    ['очень часто просто не делаете этого','нечто среднее','всегда делаете это вовремя'],

                    ['да','иногда','нет'],
                    ['почти всегда','иногда','никогда'],
                    ['показать лично','трудно сказать','чтоб ее показал кто-то другой без вашего личного присутствия'],
                    ['посмотреть мотогонки','трудно сказать','послушать музыку на открытой эстраде'],
                    ['да','не уверен','нет'],
                    ['да','нечто среднее','нет'],
                    ['да','трудно сказать','нет'],
                    ['да','трудно сказать','нет'],
                    ['да','трудно сказать','нет'],
                    ['часто','иногда','нет'],

                    ['да','иногда','нет'],
                    ['да','иногда','нет, я не испытываю неприятного чувства'],
                    ['быстро осваиваетесь со всеми','трудно сказать','вам нужно много времени, чтобы узнать каждого'],
                    ['отвёртка','бумага','линейка'],
                    ['да','иногда','нет'],
                    ['хорошо','трудно сказать','это мешает и раздражает'],
                    ['да','может быть','нет'],
                    ['часто','иногда','никогда не думал'],
                    ['думает','трудно сказать','действует'],
                    ['да','иногда','нет'],

                    ['да','может быть','нет'],
                    ['склонным к унынию и переменам настроения','трудно решить','вовсе не унылым'],
                    ['очень часто','иногда','почти никогда'],
                    ['музыкальные','трудно сказать','о войне'],
                    ['забудете об этом','трудно сказать','не упустите случая припомнить'],
                    ['да','может быть','нет'],
                    ['да','может быть','нет'],
                    ['да','может быть','нет'],
                    ['да','не уверен','нет'],
                    ['да','может быть','нет'],

                    ['даете ему высказать всё, что он хочет','трудно сказать','обычно перебиваете его раньше, чем он закончит'],
                    ['в тиши лесов, где слышно только пение птиц','трудно сказать','на многолюдной улице, где много происшествий'],
                    ['проводником, имеющим дело с пассажирами','трудно решить','машинистом, ведущим поезд'],
                    ['внизу','между','около'],
                    ['рады этому и показываете, на что способны','трудно сказать','чувствуете, что не справитесь'],
                    ['иногда','редко','никогда'],
                    ['учителем','трудно решить','ученым'],
                    ['чтобы вас заранее спросили, какой подарок вам хочется','трудно сказать','чтобы подарок был для вас сюрпризом'],
                    ['да','может быть','нет'],
                    ['предоставите ему возможность справиться самому','трудно сказать','поможете ему'],

                    ['всегда','как правило','редко'],
                    ['часто','иногда','никогда'],
                    ['да','может быть','нет'],
                    ['да, часто','иногда','нет, никогда'],
                    ['организовать классный пикник','трудно сказать','изучать в лесу различные породы деревьев'],
                    ['занимаете особую позицию','трудно сказать','соглашаетесь с остальными'],
                    ['часто','иногда','редко'],
                    ['дурачиться','трудно сказать','быть более серьезными'],
                    ['орлом на горной вершине','трудно сказать','тюленем в стаде, на берегу моря'],
                    ['да','нечто среднее','нет'],

                    ['да','может быть','нет'],
                    ['да','может быть','нет']
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
        raise BadValueKPFRS

    # 1 Шкала А
    lst_a = [2,3,22,42,62,82,102,103,122,123]
    lst_a = list(map(lambda x: x - 1, lst_a))
    base_df['A_Значение'] = answers_df.take(lst_a,axis=1).apply(calc_a_value,axis=1)
    base_df['A_Стен'] = base_df[['Пол','A_Значение']].apply(calc_a_sten,axis=1)

    # 2 Шкала B
    lst_b = [23,24,43,44,64,63,83,84,104,124]
    lst_b = list(map(lambda x: x - 1, lst_b))
    base_df['B_Значение'] = answers_df.take(lst_b,axis=1).apply(calc_b_value,axis=1)
    base_df['B_Стен'] = base_df[['Пол','B_Значение']].apply(calc_b_sten,axis=1)

    # 3 Шкала C
    lst_c = [4,5,6,25,26,45,65,85,105,125]
    lst_c = list(map(lambda x: x - 1, lst_c))
    base_df['C_Значение'] = answers_df.take(lst_c,axis=1).apply(calc_c_value,axis=1)
    base_df['C_Стен'] = base_df[['Пол','C_Значение']].apply(calc_c_sten,axis=1)

    # 4 Шкала D
    lst_d = [7,27,46,47,66,67,86,87,106,126]
    lst_d = list(map(lambda x: x - 1, lst_d))
    base_df['D_Значение'] = answers_df.take(lst_d,axis=1).apply(calc_d_value,axis=1)
    base_df['D_Стен'] = base_df[['Пол','D_Значение']].apply(calc_d_sten,axis=1)

    # 5 Шкала E
    lst_e = [8,9,28,48,68,88,107,108,127,128]
    lst_e = list(map(lambda x: x - 1, lst_e))
    base_df['E_Значение'] = answers_df.take(lst_e,axis=1).apply(calc_e_value,axis=1)
    base_df['E_Стен'] = base_df[['Пол','E_Значение']].apply(calc_e_sten,axis=1)

    # 6 Шкала F
    lst_f = [10,29,30,49,50,69,70,89,109,129]
    lst_f = list(map(lambda x: x - 1, lst_f))
    base_df['F_Значение'] = answers_df.take(lst_f,axis=1).apply(calc_f_value,axis=1)
    base_df['F_Стен'] = base_df[['Пол','F_Значение']].apply(calc_f_sten,axis=1)

    # 7 Шкала G
    lst_g = [11,31,51,71,90,91,110,111,130,131]
    lst_g = list(map(lambda x: x - 1, lst_g))
    base_df['G_Значение'] = answers_df.take(lst_g,axis=1).apply(calc_g_value,axis=1)
    base_df['G_Стен'] = base_df[['Пол','G_Значение']].apply(calc_g_sten,axis=1)

    # 8 Шкала H
    lst_h = [12,32,52,72,92,93,112,113,132,133]
    lst_h = list(map(lambda x: x - 1, lst_h))
    base_df['H_Значение'] = answers_df.take(lst_h,axis=1).apply(calc_h_value,axis=1)
    base_df['H_Стен'] = base_df[['Пол','H_Значение']].apply(calc_h_sten,axis=1)

    # 9 Шкала I
    lst_i = [13,33,34,53,54,73,74,94,114,134]
    lst_i = list(map(lambda x: x - 1, lst_i))
    base_df['I_Значение'] = answers_df.take(lst_i,axis=1).apply(calc_i_value,axis=1)
    base_df['I_Стен'] = base_df[['Пол','I_Значение']].apply(calc_i_sten,axis=1)

    # 10 Шкала J
    lst_j = [14,15,35,55,75,95,115,116,135,136]
    lst_j = list(map(lambda x: x - 1, lst_j))
    base_df['J_Значение'] = answers_df.take(lst_j,axis=1).apply(calc_j_value,axis=1)
    base_df['J_Стен'] = base_df[['Пол','J_Значение']].apply(calc_j_sten,axis=1)

    # 11 Шкала O
    lst_q_one = [16,36,56,57,76,77,96,97,117,137]
    lst_q_one = list(map(lambda x: x - 1, lst_q_one))
    base_df['O_Значение'] = answers_df.take(lst_q_one,axis=1).apply(calc_o_value, axis=1)
    base_df['O_Стен'] = base_df[['Пол','O_Значение']].apply(calc_o_sten, axis=1)

    # 12 Шкала Q2
    lst_q_two = [17,18,37,38,58,78,98,118,138,139]
    lst_q_two = list(map(lambda x: x - 1, lst_q_two))
    base_df['Q2_Значение'] = answers_df.take(lst_q_two,axis=1).apply(calc_q_two_value,axis=1)
    base_df['Q2_Стен'] = base_df[['Пол','Q2_Значение']].apply(calc_q_two_sten,axis=1)

    # 13 Шкала Q3
    lst_q_three = [19,39,59,79,80,99,100,119,120,140]
    lst_q_three = list(map(lambda x: x - 1, lst_q_three))
    base_df['Q3_Значение'] = answers_df.take(lst_q_three,axis=1).apply(calc_q_three_value,axis=1)
    base_df['Q3_Стен'] = base_df[['Пол','Q3_Значение']].apply(calc_q_three_sten,axis=1)

    # 14 Шкала Q4
    lst_q_four = [20,21,40,41,60,61,81,101,121,141]
    lst_q_four = list(map(lambda x: x - 1, lst_q_four))
    base_df['Q4_Значение'] = answers_df.take(lst_q_four,axis=1).apply(calc_q_four_value,axis=1)
    base_df['Q4_Стен'] = base_df[['Пол','Q4_Значение']].apply(calc_q_four_sten,axis=1)

    # Добавляем колонки с диапазонами
    base_df['A_Диапазон'] = base_df['A_Стен'].apply(calc_range)
    base_df['B_Диапазон'] = base_df['B_Стен'].apply(calc_range)
    base_df['C_Диапазон'] = base_df['C_Стен'].apply(calc_range)
    base_df['D_Диапазон'] = base_df['D_Стен'].apply(calc_range)

    base_df['E_Диапазон'] = base_df['E_Стен'].apply(calc_range)
    base_df['F_Диапазон'] = base_df['F_Стен'].apply(calc_range)
    base_df['G_Диапазон'] = base_df['G_Стен'].apply(calc_range)
    base_df['H_Диапазон'] = base_df['H_Стен'].apply(calc_range)

    base_df['I_Диапазон'] = base_df['I_Стен'].apply(calc_range)
    base_df['J_Диапазон'] = base_df['J_Стен'].apply(calc_range)
    base_df['O_Диапазон'] = base_df['O_Стен'].apply(calc_range)
    base_df['Q2_Диапазон'] = base_df['Q2_Стен'].apply(calc_range)

    base_df['Q3_Диапазон'] = base_df['Q3_Стен'].apply(calc_range)
    base_df['Q4_Диапазон'] = base_df['Q4_Стен'].apply(calc_range)



    # Упорядочиваем
    result_df = base_df.iloc[:,quantity_cols_base_df:] # отсекаем часть с результатами чтобы упорядочить
    lst_stens = [column for column in result_df.columns if 'Стен' in column]
    result_df['Итоговые_стены'] = result_df[lst_stens].apply(create_itog_stens,axis=1)
    new_order_lst = ['Итоговые_стены',
                     'A_Стен','B_Стен','C_Стен','D_Стен',
                     'E_Стен','F_Стен','G_Стен','H_Стен',
                     'I_Стен','J_Стен','O_Стен','Q2_Стен',
                     'Q3_Стен','Q4_Стен',

                     'A_Диапазон','B_Диапазон','C_Диапазон','D_Диапазон',
                     'E_Диапазон','F_Диапазон','G_Диапазон','H_Диапазон',
                     'I_Диапазон','J_Диапазон','O_Диапазон','Q2_Диапазон',
                     'Q3_Диапазон','Q4_Диапазон',

                     'A_Значение','B_Значение','C_Значение','D_Значение',
                     'E_Значение','F_Значение','G_Значение','H_Значение',
                     'I_Значение','J_Значение','O_Значение','Q2_Значение',
                     'Q3_Значение','Q4_Значение'
                     ]
    result_df = result_df.reindex(columns=new_order_lst) # изменяем порядок
    base_df = pd.concat([union_base_df,result_df],axis=1) # соединяем и перезаписываем base_df




    # Создаем датафрейм для создания части в общий датафрейм
    part_df = pd.DataFrame()
    # Общая тревожность
    part_df['КРС14_Итоговые_стены'] = base_df['Итоговые_стены']
    part_df['КРС14_A_Стен'] = base_df['A_Стен']
    part_df['КРС14_B_Стен'] = base_df['B_Стен']
    part_df['КРС14_C_Стен'] = base_df['C_Стен']
    part_df['КРС14_D_Стен'] = base_df['D_Стен']

    part_df['КРС14_E_Стен'] = base_df['A_Стен']
    part_df['КРС14_F_Стен'] = base_df['A_Стен']
    part_df['КРС14_G_Стен'] = base_df['A_Стен']
    part_df['КРС14_H_Стен'] = base_df['A_Стен']

    part_df['КРС14_I_Стен'] = base_df['A_Стен']
    part_df['КРС14_J_Стен'] = base_df['A_Стен']
    part_df['КРС14_O_Стен'] = base_df['A_Стен']
    part_df['КРС14_Q2_Стен'] = base_df['A_Стен']

    part_df['КРС14_Q3_Стен'] = base_df['A_Стен']
    part_df['КРС14_Q4_Стен'] = base_df['A_Стен']

    part_df['КРС14_A_Значение'] = base_df['A_Значение']
    part_df['КРС14_B_Значение'] = base_df['B_Значение']
    part_df['КРС14_C_Значение'] = base_df['C_Значение']
    part_df['КРС14_D_Значение'] = base_df['D_Значение']

    part_df['КРС14_E_Значение'] = base_df['E_Значение']
    part_df['КРС14_F_Значение'] = base_df['F_Значение']
    part_df['КРС14_G_Значение'] = base_df['G_Значение']
    part_df['КРС14_H_Значение'] = base_df['H_Значение']

    part_df['КРС14_I_Значение'] = base_df['I_Значение']
    part_df['КРС14_J_Значение'] = base_df['J_Значение']
    part_df['КРС14_O_Значение'] = base_df['O_Значение']
    part_df['КРС14_Q2_Значение'] = base_df['Q2_Значение']

    part_df['КРС14_Q3_Значение'] = base_df['Q3_Значение']
    part_df['КРС14_Q4_Значение'] = base_df['Q4_Значение']
    # Диапазон
    part_df['КРС14_A_Диапазон'] = base_df['A_Диапазон']
    part_df['КРС14_B_Диапазон'] = base_df['B_Диапазон']
    part_df['КРС14_C_Диапазон'] = base_df['C_Диапазон']
    part_df['КРС14_D_Диапазон'] = base_df['D_Диапазон']

    part_df['КРС14_E_Диапазон'] = base_df['E_Диапазон']
    part_df['КРС14_F_Диапазон'] = base_df['F_Диапазон']
    part_df['КРС14_G_Диапазон'] = base_df['G_Диапазон']
    part_df['КРС14_H_Диапазон'] = base_df['H_Диапазон']

    part_df['КРС14_I_Диапазон'] = base_df['I_Диапазон']
    part_df['КРС14_J_Диапазон'] = base_df['J_Диапазон']
    part_df['КРС14_O_Диапазон'] = base_df['O_Диапазон']
    part_df['КРС14_Q2_Диапазон'] = base_df['Q2_Диапазон']

    part_df['КРС14_Q3_Диапазон'] = base_df['Q3_Диапазон']
    part_df['КРС14_Q4_Диапазон'] = base_df['Q4_Диапазон']

    out_answer_df = pd.concat([out_answer_df, answers_df], axis=1)  # Датафрейм для проверки

    # формируем основной словарь
    out_dct = {'Списочный результат': base_df, 'Список для проверки': out_answer_df,
               }
    
    

    # Делаем свод по шкалам
    dct_svod_integral = {'A_Стен': 'A_Диапазон',
                         'B_Стен': 'B_Диапазон',
                         'C_Стен': 'C_Диапазон',
                         'D_Стен': 'D_Диапазон',

                         'E_Стен': 'E_Диапазон',
                         'F_Стен': 'F_Диапазон',
                         'G_Стен': 'G_Диапазон',
                         'H_Стен': 'H_Диапазон',

                         'I_Стен': 'I_Диапазон',
                         'J_Стен': 'J_Диапазон',
                         'O_Стен': 'O_Диапазон',
                         'Q2_Стен': 'Q2_Диапазон',

                         'Q3_Стен': 'Q3_Диапазон',
                         'Q4_Стен': 'Q4_Диапазон',
                         }

    dct_rename_svod_integral = {'A_Стен': 'Фактор A',
                                'B_Стен': 'Фактор B',
                                'C_Стен': 'Фактор C',
                                'D_Стен': 'Фактор D',

                                'E_Стен': 'Фактор E',
                                'F_Стен': 'Фактор F',
                                'G_Стен': 'Фактор G',
                                'H_Стен': 'Фактор H',

                                'I_Стен': 'Фактор I',
                                'J_Стен': 'Фактор J',
                                'O_Стен': 'Фактор O',
                                'Q2_Стен': 'Фактор Q2',

                                'Q3_Стен': 'Фактор Q3',
                                'Q4_Стен': 'Фактор Q4',
                                }


    lst_integral = ['1-3', '4-7', '8-10']
    base_svod_integral_df = create_union_svod(base_df, dct_svod_integral, dct_rename_svod_integral, lst_integral)

    # Считаем среднее по шкалам
    avg_a = round(base_df['A_Значение'].mean(), 1)
    avg_b = round(base_df['B_Значение'].mean(), 1)
    avg_c = round(base_df['C_Значение'].mean(), 1)
    avg_d = round(base_df['D_Значение'].mean(), 1)

    avg_e = round(base_df['E_Значение'].mean(), 1)
    avg_f = round(base_df['F_Значение'].mean(), 1)
    avg_g = round(base_df['G_Значение'].mean(), 1)
    avg_h = round(base_df['H_Значение'].mean(), 1)

    avg_i = round(base_df['I_Значение'].mean(), 1)
    avg_j = round(base_df['J_Значение'].mean(), 1)
    avg_o = round(base_df['O_Значение'].mean(), 1)
    avg_q_two = round(base_df['Q2_Значение'].mean(), 1)

    avg_q_three = round(base_df['Q3_Значение'].mean(), 1)
    avg_q_four = round(base_df['Q4_Значение'].mean(), 1)

    avg_dct = {'Среднее сырое значение шкалы A': avg_a,
               'Среднее сырое значение шкалы B': avg_b,
               'Среднее сырое значение шкалы C': avg_c,
               'Среднее сырое значение шкалы D': avg_d,
               
               'Среднее сырое значение шкалы E': avg_e,
               'Среднее сырое значение шкалы F': avg_f,
               'Среднее сырое значение шкалы G': avg_g,
               'Среднее сырое значение шкалы H': avg_h,
               
               'Среднее сырое значение шкалы I': avg_i,
               'Среднее сырое значение шкалы J': avg_j,
               'Среднее сырое значение шкалы O': avg_o,
               'Среднее сырое значение шкалы Q2': avg_q_two,
               
               'Среднее сырое значение шкалы Q3': avg_q_three,
               'Среднее сырое значение шкалы Q4': avg_q_four,
               }

    avg_df = pd.DataFrame.from_dict(avg_dct, orient='index')
    avg_df = avg_df.reset_index()
    avg_df.columns = ['Показатель', 'Среднее значение']

    out_dct.update({'Свод Интегральные показатели': base_svod_integral_df,
                    'Среднее': avg_df}
                   )

    dct_prefix = {'A_Диапазон': 'A',
                  'B_Диапазон': 'B',
                  'C_Диапазон': 'C',
                  'D_Диапазон': 'D',
                  
                  'E_Диапазон': 'E',
                  'F_Диапазон': 'F',
                  'G_Диапазон': 'G',
                  'H_Диапазон': 'H',
                  
                  'I_Диапазон': 'I',
                  'J_Диапазон': 'J',
                  'O_Диапазон': 'O',
                  'Q2_Диапазон': 'Q2',
                  
                  'Q3_Диапазон': 'Q3',
                  'Q4_Диапазон': 'Q4',
                  }

    out_dct = create_list_on_level(base_df, out_dct, lst_integral, dct_prefix)

    """
        Сохраняем в зависимости от необходимости делать своды по определенным колонкам
        """
    if len(lst_svod_cols) == 0:
        return out_dct, part_df
    else:
        out_dct = create_result_krshspq(base_df, out_dct, lst_svod_cols)

        return out_dct, part_df











