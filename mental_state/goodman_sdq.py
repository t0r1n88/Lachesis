"""
Скрипт для обработки результатов теста Сильные стороны и трудности SDQ Гудман Ульянина и др.
"""

import pandas as pd
import re
from tkinter import messagebox
from lachesis_support_functions import round_mean_two,calc_count_scale,create_union_svod, create_list_on_level

class BadOrderSDQGU(Exception):
    """
    Исключение для обработки случая когда колонки не совпадают
    """
    pass


class BadValueSDQGU(Exception):
    """
    Исключение для неправильных значений в вариантах ответов
    """
    pass

class BadCountColumnsSDQGU(Exception):
    """
    Исключение для обработки случая если количество колонок не равно 23
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


def calc_value_psp(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [1,4,8,15,18]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_pr:
            value_forward += value
    return value_forward


def calc_level_sex_psp(row:pd.Series):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """
    sex,value = row

    if sex == 'Мужской':
        if 0 <= value <= 5:
            return f'отклоняющиеся'
        elif value == 6:
            return f'пограничные'
        else:
            return f'норма'
    else:
        if 0 <= value <= 4:
            return f'отклоняющиеся'
        elif 5<= value <= 6:
            return f'пограничные'
        else:
            return f'норма'

def calc_level_age_psp(row:pd.Series):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """
    age,value = row

    if age == '10-13 лет':
        if 0 <= value <= 4:
            return f'отклоняющиеся'
        elif 5<= value <= 6:
            return f'пограничные'
        else:
            return f'норма'
    else:
        if 0 <= value <= 5:
            return f'отклоняющиеся'
        elif value == 6:
            return f'пограничные'
        else:
            return f'норма'



def calc_value_ga(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [2,9,13,19,23]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_pr:
            if idx not in (19,23):
                value_forward += value
            else:
                if value == 0:
                    value_forward += 2
                elif value == 1:
                    value_forward += 1
                else:
                    value_forward += 0

    return value_forward

def calc_level_sex_ga(row:pd.Series):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """
    sex,value = row

    if sex == 'Мужской':
        if 6 <= value <= 10 :
            return f'отклоняющиеся'
        elif value == 5:
            return f'пограничные'
        else:
            return f'норма'
    else:
        if  6<= value <= 10 :
            return f'отклоняющиеся'
        elif value == 5:
            return f'пограничные'
        else:
            return f'норма'



def calc_level_age_ga(row:pd.Series):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """
    age,value = row

    if age == '10-13 лет':
        if  6<= value <=10 :
            return f'отклоняющиеся'
        elif value == 5 :
            return f'пограничные'
        else:
            return f'норма'
    else:
        if  5<= value <=10 :
            return f'отклоняющиеся'
        elif value == 4:
            return f'пограничные'
        else:
            return f'норма'


def calc_value_emo(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [3,7,11,14,22]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_pr:
            value_forward += value
    return value_forward

def calc_level_sex_emo(row:pd.Series):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """
    sex,value = row

    if sex == 'Мужской':
        if  6<= value <= 10:
            return f'отклоняющиеся'
        elif value == 5:
            return f'пограничные'
        else:
            return f'норма'
    else:
        if  8<= value <=10 :
            return f'отклоняющиеся'
        elif 6<= value <=7 :
            return f'пограничные'
        else:
            return f'норма'



def calc_level_age_emo(row:pd.Series):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """
    age,value = row

    if age == '10-13 лет':
        if  7<= value <= 10:
            return f'отклоняющиеся'
        elif value == 6:
            return f'пограничные'
        else:
            return f'норма'
    else:
        if  7<= value <=10 :
            return f'отклоняющиеся'
        elif 5<= value <= 6:
            return f'пограничные'
        else:
            return f'норма'


def calc_value_pp(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [5,10,16,20]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_pr:
            value_forward += value
    return value_forward

def calc_level_sex_pp(row:pd.Series):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """
    sex,value = row

    if sex == 'Мужской':
        if  4<= value <= 8:
            return f'отклоняющиеся'
        elif value == 3:
            return f'пограничные'
        else:
            return f'норма'
    else:
        if  4<= value <= 8:
            return f'отклоняющиеся'
        elif value == 3:
            return f'пограничные'
        else:
            return f'норма'



def calc_level_age_pp(row:pd.Series):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """
    age,value = row

    if age == '10-13 лет':
        if 4 <= value <=8 :
            return f'отклоняющиеся'
        elif value == 3 :
            return f'пограничные'
        else:
            return f'норма'
    else:
        if 3 <= value <=8 :
            return f'отклоняющиеся'
        elif value == 2:
            return f'пограничные'
        else:
            return f'норма'


def calc_value_ps(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [6,12,17,21]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_pr:
            if idx != 12:
                value_forward += value
            else:
                if value == 0:
                    value_forward += 2
                elif value == 1:
                    value_forward += 1
                else:
                    value_forward += 0
    return value_forward


def calc_level_sex_ps(row:pd.Series):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """
    sex,value = row

    if sex == 'Мужской':
        if  5<= value <=8 :
            return f'отклоняющиеся'
        elif value == 4:
            return f'пограничные'
        else:
            return f'норма'
    else:
        if  5<= value <=8 :
            return f'отклоняющиеся'
        elif value == 4:
            return f'пограничные'
        else:
            return f'норма'



def calc_level_age_ps(row:pd.Series):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """
    age,value = row

    if age == '10-13 лет':
        if  5<= value <=8 :
            return f'отклоняющиеся'
        elif value == 4:
            return f'пограничные'
        else:
            return f'норма'
    else:
        if  5<= value <= 8:
            return f'отклоняющиеся'
        elif value == 4:
            return f'пограничные'
        else:
            return f'норма'


def calc_value_ochp(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [2,3,5,6,7,9,10,11,12,13,14,16,17,19,20,21,22,23]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_pr:
            if idx not in (12,19,23):
                value_forward += value
            else:
                if value == 0:
                    value_forward += 2
                elif value == 1:
                    value_forward += 1
                else:
                    value_forward += 0
    return value_forward

def calc_level_sex_ochp(row:pd.Series):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """
    sex,value = row

    if sex == 'Мужской':
        if  19<= value <=36 :
            return f'отклоняющиеся'
        elif 15<= value <= 18 :
            return f'пограничные'
        else:
            return f'норма'
    else:
        if  19<= value <=36 :
            return f'отклоняющиеся'
        elif 17<= value <=18 :
            return f'пограничные'
        else:
            return f'норма'



def calc_level_age_ochp(row:pd.Series):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """
    age,value = row

    if age == '10-13 лет':
        if 20 <= value <=36 :
            return f'отклоняющиеся'
        elif 17<= value <= 19 :
            return f'пограничные'
        else:
            return f'норма'
    else:
        if  18<= value <= 36 :
            return f'отклоняющиеся'
        elif 15 <= value <= 17:
            return f'пограничные'
        else:
            return f'норма'







def processing_sdq_good_ul(base_df: pd.DataFrame, answers_df: pd.DataFrame, lst_svod_cols:list):
    """
    Функция для обработки
    :param base_df: часть датафрейма с описательными колонками
    :param answers_df: часть датафрейма с ответами
    :param lst_svod_cols:  список с колонками по которым нужно делать свод
    """
    out_answer_df = base_df.copy()  # делаем копию для последующего соединения с сырыми ответами
    if len(answers_df.columns) != 23:  # проверяем количество колонок с вопросами
        raise BadCountColumnsSDQGU

    # очищаем названия колонок от возможных сочетаний .1 которые добавляет пандас при одинаковых колонках
    clean_df_lst = []
    for name_column in answers_df.columns:
        clean_name = re.sub(r'.\d+$', '', name_column)
        clean_df_lst.append(clean_name)

    answers_df.columns = clean_df_lst

    # Проверяем наличие колонок Пол и Возраст
    diff_req_cols = {'Пол'}.difference(set(base_df.columns))
    if len(diff_req_cols) != 0:
        raise NotReqColumn

    # на случай пустых
    base_df['Пол'].fillna('Не заполнено', inplace=True)
    # очищаем от лишних пробелов
    base_df['Пол'] = base_df['Пол'].apply(str.strip)

    # Проверяем на пол
    diff_sex = set(base_df['Пол'].unique()).difference({'Мужской', 'Женский'})
    if len(diff_sex) != 0:
        raise BadValueSex


    lst_check_cols = ['Я стараюсь быть хорошим с другими людьми',
                      'Я неугомонный, не могу оставаться спокойным',
                      'У меня часто бывают головные боли, боли в животе и тошнота',
                      'Я обычно делюсь с другими (едой, играми, ручками)',
                      'Я сильно сержусь, раздражаюсь и выхожу из себя',
                      'Я обычно один. Чаще всего я играю в одиночестве и занимаюсь сам',
                      'Я много беспокоюсь',
                      'Я пытаюсь помочь, если кто-нибудь расстроен, обижен или болен',
                      'Я постоянно ерзаю и верчусь',
                      'Я много дерусь. Я могу заставить других людей делать то, что я хочу',

                      'Я часто чувствую себя несчастным, унылым, готов расплакаться',
                      'Я обычно нравлюсь своим сверстникам',
                      'Я легко отвлекаюсь, мне трудно сосредоточиться',
                      'Я нервничаю в новой обстановке, легко теряю уверенность',
                      'Я добр к младшим детям',
                      'Меня часто обвиняют во лжи или обмане',
                      'Другие часто дразнят или задирают меня',
                      'Я часто вызываюсь помочь другим (родителям, учителям, детям)',
                      'Я думаю, прежде чем действовать',
                      'Я беру чужие вещи из дома, школы и других мест',
                      'У меня лучше отношения со взрослыми, чем со сверстниками',
                      'Я многого боюсь, легко пугаюсь',
                      'Я делаю до конца работу, которую начал. У меня хорошее внимание',
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
        raise BadOrderSDQGU
    # словарь для замены слов на числа
    dct_replace_value = {'неверно': 0,
                         'отчасти верно': 1,
                         'верно': 2,
                         }
    valid_values = [0, 1, 2]
    answers_df.replace(dct_replace_value, inplace=True)  # заменяем слова на цифры для подсчетов
    # Проверяем, есть ли значения, отличающиеся от указанных в списке
    lst_error_answers = []  # список для хранения строк где найдены неправильные ответы

    for i in range(23):
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
        raise BadValueSDQGU

    base_df['ПСП_Значение'] = answers_df.apply(calc_value_psp,axis=1)
    base_df['ПСП_Пол_Уровень'] = base_df[['Пол','ПСП_Значение']].apply(calc_level_sex_psp, axis=1)
    base_df['ПСП_Возраст_Уровень'] = base_df[['Возраст','ПСП_Значение']].apply(calc_level_age_psp, axis=1)

    base_df['ГА_Значение'] = answers_df.apply(calc_value_ga,axis=1)
    base_df['ГА_Пол_Уровень'] = base_df[['Пол','ГА_Значение']].apply(calc_level_sex_ga, axis=1)
    base_df['ГА_Возраст_Уровень'] = base_df[['Возраст','ГА_Значение']].apply(calc_level_age_ga, axis=1)


    base_df['ЭС_Значение'] = answers_df.apply(calc_value_emo,axis=1)
    base_df['ЭС_Пол_Уровень'] = base_df[['Пол','ЭС_Значение']].apply(calc_level_sex_emo, axis=1)
    base_df['ЭС_Возраст_Уровень'] = base_df[['Возраст','ЭС_Значение']].apply(calc_level_age_emo, axis=1)


    base_df['ПП_Значение'] = answers_df.apply(calc_value_pp,axis=1)
    base_df['ПП_Пол_Уровень'] = base_df[['Пол','ПП_Значение']].apply(calc_level_sex_pp, axis=1)
    base_df['ПП_Возраст_Уровень'] = base_df[['Возраст','ПП_Значение']].apply(calc_level_age_pp, axis=1)

    base_df['ПС_Значение'] = answers_df.apply(calc_value_ps,axis=1)
    base_df['ПС_Пол_Уровень'] = base_df[['Пол','ПС_Значение']].apply(calc_level_sex_ps, axis=1)
    base_df['ПС_Возраст_Уровень'] = base_df[['Возраст','ПС_Значение']].apply(calc_level_age_ps, axis=1)

    base_df['ОЧП_Значение'] = answers_df.apply(calc_value_ochp,axis=1)
    base_df['ОЧП_Пол_Уровень'] = base_df[['Пол','ОЧП_Значение']].apply(calc_level_sex_ochp, axis=1)
    base_df['ОЧП_Возраст_Уровень'] = base_df[['Возраст','ОЧП_Значение']].apply(calc_level_age_ochp, axis=1)



    base_df.to_excel('data/res.xlsx',index=False)

