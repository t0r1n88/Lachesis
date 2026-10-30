"""
Скрипт для обработки результатов теста Шкала личностной тревожности учащихся А. М. Прихожан Форма А

"""

import pandas as pd
import re
import os
import openpyxl
from openpyxl.utils.dataframe import dataframe_to_rows
from openpyxl.styles import Alignment
from openpyxl.utils import get_column_letter
from tkinter import messagebox
from lachesis_support_functions import create_union_svod,create_list_on_level,round_mean

class BadOrderLTUPA(Exception):
    """
    Исключение для обработки случая когда колонки не совпадают
    """
    pass


class BadValueLTUPA(Exception):
    """
    Исключение для неправильных значений в вариантах ответов
    """
    pass

class BadCountColumnsLTUPA(Exception):
    """
    Исключение для обработки случая если количество колонок не равно 40
    """
    pass

class NotReqColumnLTUPA(Exception):
    """
    Исключение для обработки случая когда нет обязательных колонок Пол И Возраст
    """
    pass

class BadValueSexLTUPA(Exception):
    """
    Исключение для обработки случая когда в колонке Пол есть значения отличающиеся от Мужской или Женский
    """
    pass

class BadValueAgeLTUPA(Exception):
    """
    Исключение для обработки случая когда в колонке Пол есть значения отличающиеся от требуемого возраста
    """
    pass

def calc_range(value):
    """
    Функция для подсчета диапазонов
    :param value: значение
    :return:
    """
    if 1 <= value <= 2:
        return 'тревожность отсутствует'
    elif 3 <=value <= 6:
        return 'нормальный уровень'
    elif 7<=value <= 8:
        return 'несколько повышенная тревожность'
    elif value == 9:
        return 'явно повышенная тревожность'
    else:
        return 'очень высокая тревожность'



def calc_ot_sten(ser:pd.Series):
    """
    Функция для подсчета Стена
    :param ser: пол и значение
    :return:
    """
    row = ser.tolist() # превращаем в список
    sex = row[0] # пол
    age = row[1] # возраст
    value = row[2] # значение которое нужно обработать

    if sex == 'Женский':
        if age == '10-11 лет':
            if  0<= value <=33 :
                return 1
            elif  34<= value <=40 :
                return 2
            elif  41<= value <=48 :
                return 3
            elif 49 <= value <=55 :
                return 4
            elif 56<= value <=62:
                return 5
            elif  63<= value <=70 :
                return 6
            elif  71<= value <=77 :
                return 7
            elif  78<= value <=84 :
                return 8
            elif  85<= value <=92 :
                return 9
            else:
                return 10
        else:
            if 0 <= value <= 34 :
                return 1
            elif  35<= value <=43 :
                return 2
            elif  44<= value <=50 :
                return 3
            elif  51<= value <=58 :
                return 4
            elif 59<= value <=66:
                return 5
            elif  67<= value <=74 :
                return 6
            elif  75<= value <=81 :
                return 7
            elif  82<= value <=89 :
                return 8
            elif  90<= value <=97 :
                return 9
            else:
                return 10
    else:
        if age == '10-11 лет':
            if  0<= value <=26 :
                return 1
            elif  27<= value <=32 :
                return 2
            elif  33<= value <=39 :
                return 3
            elif  40<= value <=45 :
                return 4
            elif 46<= value <=52:
                return 5
            elif  53<= value <=58 :
                return 6
            elif  59<= value <=65 :
                return 7
            elif  66<= value <=71 :
                return 8
            elif  72<= value <=77 :
                return 9
            else:
                return 10
        else:
            if  0<= value <=26 :
                return 1
            elif  27<= value <=32 :
                return 2
            elif 33 <= value <=38 :
                return 3
            elif  39<= value <=44 :
                return 4
            elif 45<= value <=50:
                return 5
            elif  51<= value <=56 :
                return 6
            elif  57<= value <=62 :
                return 7
            elif  63<= value <=67 :
                return 8
            elif 68<= value <=73 :
                return 9
            else:
                return 10


def calc_sht_value(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [1,5,7,11,12,16,19,28,30,34]
    value_forward = 0  # результат
    for idx, value in enumerate(row, 1):
        if idx in lst_pr:
            value_forward += value
    return value_forward


def calc_sht_sten(ser:pd.Series):
    """
    Функция для подсчета Стена
    :param ser: пол и значение
    :return:
    """
    row = ser.tolist() # превращаем в список
    sex = row[0] # пол
    age = row[1] # возраст
    value = row[2] # значение которое нужно обработать

    if age == '10-11 лет':
        if sex == 'Женский':
            if 0 <= value <=8 :
                return 1
            elif  9<= value <=11 :
                return 2
            elif  12<= value <=13 :
                return 3
            elif  14<= value <= 16:
                return 4
            elif 17<= value <=18:
                return 5
            elif  19<= value <=20 :
                return 6
            elif  21<= value <=22 :
                return 7
            elif 23 <= value <=25 :
                return 8
            elif  26<= value <=27 :
                return 9
            else:
                return 10
        else:
            if 0 <= value <= 7:
                return 1
            elif  8<= value <=10 :
                return 2
            elif  11<= value <=12 :
                return 3
            elif  13<= value <=14 :
                return 4
            elif 15<= value <=16:
                return 5
            elif 17 <= value <=18 :
                return 6
            elif  19<= value <=20 :
                return 7
            elif  21<= value <= 22:
                return 8
            elif  23<= value <=24 :
                return 9
            else:
                return 10
    else:
        if sex == 'Женский':
            if 0 <= value <=2 :
                return 1
            elif  3<= value <=5 :
                return 2
            elif  6<= value <=7 :
                return 3
            elif  8<= value <=10 :
                return 4
            elif 11<= value <=12:
                return 5
            elif  13<= value <=15 :
                return 6
            elif  16<= value <=17 :
                return 7
            elif  18<= value <=20 :
                return 8
            elif  21<= value <=22 :
                return 9
            else:
                return 10
        else:
            if  0<= value <=7 :
                return 1
            elif 8 <= value <=9 :
                return 2
            elif 9 <= value <= 10:
                return 3
            elif  11<= value <=12 :
                return 4
            elif value ==13:
                return 5
            elif  14<= value <=15 :
                return 6
            elif value ==16 :
                return 7
            elif  17<= value <=18 :
                return 8
            elif 19<= value <=20 :
                return 9
            else:
                return 10


def calc_st_value(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [3, 6, 8, 13, 17, 20, 25, 29, 33, 39]
    value_forward = 0  # результат
    for idx, value in enumerate(row, 1):
        if idx in lst_pr:
            value_forward += value
    return value_forward


def calc_st_sten(ser:pd.Series):
    """
    Функция для подсчета Стена
    :param ser: пол и значение
    :return:
    """
    row = ser.tolist() # превращаем в список
    sex = row[0] # пол
    age = row[1] # возраст
    value = row[2] # значение которое нужно обработать

    if age == '10-11 лет':
        if sex == 'Женский':
            if  0<= value <=10 :
                return 1
            elif  value == 11:
                return 2
            elif  12<= value <=13 :
                return 3
            elif value ==14 :
                return 4
            elif 15<= value <=16:
                return 5
            elif  17<= value <=18 :
                return 6
            elif  value ==19 :
                return 7
            elif  20<= value <=21 :
                return 8
            elif  22<= value <=23 :
                return 9
            else:
                return 10
        else:
            if  0<= value <=7 :
                return 1
            elif  8<= value <=9 :
                return 2
            elif value ==10 :
                return 3
            elif  11<= value <=12 :
                return 4
            elif value ==13:
                return 5
            elif  14<= value <=15 :
                return 6
            elif  16<= value <=17 :
                return 7
            elif  value ==18 :
                return 8
            elif  19<= value <=20 :
                return 9
            else:
                return 10
    else:
        if sex == 'Женский':
            if 0 <= value <=9 :
                return 1
            elif  10<= value <=11 :
                return 2
            elif  12<= value <=13 :
                return 3
            elif 14 <= value <=16 :
                return 4
            elif 17<= value <=18:
                return 5
            elif  19<= value <= 20:
                return 6
            elif  21<= value <=22 :
                return 7
            elif  23<= value <=24 :
                return 8
            elif  25<= value <=27 :
                return 9
            else:
                return 10
        else:
            if  0<= value <=5 :
                return 1
            elif  6<= value <=7 :
                return 2
            elif  value == 8 :
                return 3
            elif  9<= value <=10 :
                return 4
            elif 11<= value <=12:
                return 5
            elif  13<= value <=14 :
                return 7
            elif  value ==15 :
                return 8
            elif  16<= value <=17 :
                return 9
            else:
                return 10


def calc_mt_value(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [2, 9, 15, 18, 22, 24, 26, 32, 36, 38]
    value_forward = 0  # результат
    for idx, value in enumerate(row, 1):
        if idx in lst_pr:
            value_forward += value
    return value_forward


def calc_mt_sten(ser:pd.Series):
    """
    Функция для подсчета Стена
    :param ser: пол и значение
    :return:
    """
    row = ser.tolist() # превращаем в список
    sex = row[0] # пол
    age = row[1] # возраст
    value = row[2] # значение которое нужно обработать

    if age == '10-11 лет':
        if sex == 'Женский':
            if  0<= value <=8 :
                return 1
            elif  value ==9 :
                return 2
            elif  value ==10 :
                return 3
            elif  value ==11 :
                return 4
            elif 12<= value <=13:
                return 5
            elif  value ==14 :
                return 6
            elif  value ==15 :
                return 7
            elif  16<= value <=17 :
                return 8
            elif  value ==18 :
                return 9
            else:
                return 10
        else:
            if  0<= value <=7 :
                return 1
            elif  value ==8 :
                return 2
            elif  value ==9 :
                return 3
            elif  value == 10:
                return 4
            elif 11<= value <=12:
                return 5
            elif  value ==13 :
                return 6
            elif  value ==14 :
                return 7
            elif  value ==15 :
                return 8
            elif  value == 16:
                return 9
            else:
                return 10
    else:
        if sex == 'Женский':
            if  0<= value <=8 :
                return 1
            elif  9<= value <=10 :
                return 2
            elif  11<= value <=12 :
                return 3
            elif  13<= value <= 14:
                return 4
            elif value ==15:
                return 5
            elif  16<= value <= 17:
                return 6
            elif  18<= value <=19 :
                return 7
            elif 20 <= value <=21 :
                return 8
            elif  22<= value <=23:
                return 9
            else:
                return 10
        else:
            if  0<= value <=8 :
                return 1
            elif  value ==9 :
                return 2
            elif  value ==10 :
                return 3
            elif  11<= value <=12 :
                return 4
            elif value ==13:
                return 5
            elif  14<= value <=15 :
                return 6
            elif  value ==16 :
                return 7
            elif  17<= value <=18 :
                return 8
            elif  value ==19 :
                return 9
            else:
                return 10


def calc_magt_value(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [4, 10, 14, 21, 23, 27, 31, 35, 37, 40]
    value_forward = 0  # результат
    for idx, value in enumerate(row, 1):
        if idx in lst_pr:
            value_forward += value
    return value_forward

def calc_magt_sten(ser:pd.Series):
    """
    Функция для подсчета Стена
    :param ser: пол и значение
    :return:
    """
    row = ser.tolist() # превращаем в список
    sex = row[0] # пол
    age = row[1] # возраст
    value = row[2] # значение которое нужно обработать

    if age == '10-11 лет':
        if sex == 'Женский':
            if  0<= value <= 7:
                return 1
            elif  value ==8 :
                return 2
            elif  9<= value <=10 :
                return 3
            elif  11<= value <=12 :
                return 4
            elif 13<= value <=14:
                return 5
            elif  15<= value <=16 :
                return 6
            elif  17<= value <=18 :
                return 7
            elif  19<= value <=20 :
                return 8
            elif  21<= value <=22 :
                return 9
            else:
                return 10
        else:
            if  0<= value <= 6:
                return 1
            elif value ==7 :
                return 2
            elif  8<= value <=9 :
                return 3
            elif  value ==10 :
                return 4
            elif 11<= value <=12:
                return 5
            elif  value ==13 :
                return 6
            elif  value ==14 :
                return 7
            elif  15<= value <=16 :
                return 8
            elif  value ==17 :
                return 9
            else:
                return 10
    else:
        if sex == 'Женский':
            if 0 <= value <=7 :
                return 1
            elif  8<= value <=9 :
                return 2
            elif  10<= value <=11 :
                return 3
            elif  12<= value <=13 :
                return 4
            elif 14<= value <=15:
                return 5
            elif  16<= value <=17 :
                return 6
            elif  18<= value <=20 :
                return 7
            elif  21<= value <=22 :
                return 8
            elif  23<= value <=24 :
                return 9
            else:
                return 10
        else:
            if  0<= value <=4 :
                return 1
            elif 5 <= value <= 6:
                return 2
            elif  value ==7 :
                return 3
            elif  8<= value <=9 :
                return 4
            elif value ==10:
                return 5
            elif  11<= value <=12 :
                return 6
            elif value ==13 :
                return 7
            elif  14<= value <=15 :
                return 8
            elif  value ==16 :
                return 9
            else:
                return 10







def processing_ltu_prih_form_a(base_df: pd.DataFrame, answers_df: pd.DataFrame, lst_svod_cols:list):
    """
    Функция для обработки
    :param base_df: часть датафрейма с описательными колонками
    :param answers_df: часть датафрейма с ответами
    :param lst_svod_cols:  список с колонками по которым нужно делать свод
    """
    union_base_df = base_df.copy()  # делаем копию анкетной части чтобы потом соединить ее с ответной частью
    quantity_cols_base_df = base_df.shape[1]  # количество колонок в анкетной части

    out_answer_df = base_df.copy()  # делаем копию для последующего соединения с сырыми ответами
    if len(answers_df.columns) != 40:  # проверяем количество колонок с вопросами
        raise BadCountColumnsLTUPA

    # очищаем названия колонок от возможных сочетаний .1 которые добавляет пандас при одинаковых колонках
    clean_df_lst = []
    for name_column in answers_df.columns:
        clean_name = re.sub(r'.\d+$', '', name_column)
        clean_df_lst.append(clean_name)

    answers_df.columns = clean_df_lst

    # Проверяем наличие колонок Пол
    diff_req_cols = {'Пол', 'Возраст'}.difference(set(base_df.columns))
    if len(diff_req_cols) != 0:
        raise NotReqColumnLTUPA

    # Проверяем на пол
    diff_sex = set(base_df['Пол'].unique()).difference({'Мужской', 'Женский'})
    if len(diff_sex) != 0:
        raise BadValueSexLTUPA

    # Проверяем на возраст
    diff_age = set(base_df['Возраст'].unique()).difference({'10-11 лет', '12 лет'})
    if len(diff_age) != 0:
        raise BadValueAgeLTUPA


    lst_check_cols = ['Отвечать у доски',
                      'Оказаться среди незнакомых ребят',
                      'Участвовать в соревнованиях, конкурсах, олимпиадах',
                      'Слышать заклятия',
                      'Разговаривать с директором школы',
                      'Сравнивать себя с другими',
                      'Учитель смотрит по журналу, кого спросить',
                      'Тебя критикуют, в чем-то упрекают',
                      'На тебя смотрят, когда ты что-нибудь делаешь (наблюдают за тобой во время работы, решения задачи)',
                      'Видеть плохие сны',

                      'Писать контрольную работу, выполнять тест по какому-нибудь предмету',
                      'После контрольной, теста – учитель называет отметки',
                      'У тебя что-то не получается',
                      'Смотреть на человека, похожего на мага, колдуна',
                      'На тебя не обращают внимания',
                      'Ждешь родителей с родительского собрания',
                      'Тебе грозит неуспех, провал',
                      'Слышать смех за своей спиной',
                      'Не понимать объяснений учителя',
                      'Думаешь о том, чего ты сможешь добиться в будущем',

                      'Слышать предсказания о космических катастрофах',
                      'Выступать перед зрителями',
                      'Слышать, что какой-то человек «напускает порчу» на других',
                      'С тобой не хотят играть',
                      'Проверяются твои способности',
                      'На тебя смотрят как на маленького',
                      'На экзамене тебе достался 13-й билет',
                      'На уроке учитель неожиданно задает тебе вопрос',
                      'Оценивается твоя работа',
                      'Не можешь справиться с домашним заданием',

                      'Засыпать в темной комнате',
                      'Не соглашаешься с родителями',
                      'Берешься за новое дело',
                      'Разговаривать с школьным психологом',
                      'Думать о том, что тебя могут «сглазить»',
                      'Замолчали, когда ты подошел (подошла)',
                      'Слушать страшные истории',
                      'Спорить со своим другом (подругой)',
                      'Думать о своей внешности',
                      'Думать о призраках, других страшных, «потусторонних» существах'
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
        raise BadOrderLTUPA

    # словарь для замены слов на числа
    dct_replace_value = {'нет': 0,
                         'немного': 1,
                         'достаточно': 2,
                         'значительно': 3,
                         'очень': 4,
                         }
    valid_values = [0, 1, 2, 3,4]
    answers_df.replace(dct_replace_value, inplace=True)  # заменяем слова на цифры для подсчетов
    # Проверяем, есть ли значения, отличающиеся от указанных в списке
    lst_error_answers = []  # список для хранения строк где найдены неправильные ответы

    for i in range(40):
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
        raise BadValueLTUPA
    # Общая тревожность
    base_df['ОТ_Сырое'] = answers_df.sum(axis=1)
    base_df['ОТ_Стен'] = base_df[['Пол','Возраст','ОТ_Сырое']].apply(calc_ot_sten,axis=1)
    base_df['ОТ_Уровень'] = base_df['ОТ_Стен'].apply(calc_range)

    base_df['ШТ_Сырое'] = answers_df.apply(calc_sht_value,axis=1)
    base_df['ШТ_Стен'] = base_df[['Пол','Возраст','ШТ_Сырое']].apply(calc_sht_sten,axis=1)
    base_df['ШТ_Уровень'] = base_df['ШТ_Стен'].apply(calc_range)

    base_df['СТ_Сырое'] = answers_df.apply(calc_st_value,axis=1)
    base_df['СТ_Стен'] = base_df[['Пол','Возраст','СТ_Сырое']].apply(calc_st_sten,axis=1)
    base_df['СТ_Уровень'] = base_df['СТ_Стен'].apply(calc_range)

    base_df['МТ_Сырое'] = answers_df.apply(calc_mt_value,axis=1)
    base_df['МТ_Стен'] = base_df[['Пол','Возраст','МТ_Сырое']].apply(calc_mt_sten,axis=1)
    base_df['МТ_Уровень'] = base_df['МТ_Стен'].apply(calc_range)

    base_df['МАГТ_Сырое'] = answers_df.apply(calc_magt_value,axis=1)
    base_df['МАГТ_Стен'] = base_df[['Пол','Возраст','МАГТ_Сырое']].apply(calc_magt_sten,axis=1)
    base_df['МАГТ_Уровень'] = base_df['МАГТ_Стен'].apply(calc_range)






    base_df.to_excel('data/res.xlsx')


