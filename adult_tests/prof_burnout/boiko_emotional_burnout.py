"""
Скрипт для обработки теста Диагностика уровня эмоционального выгорания В.В.Бойко исходная версия
"""
import pandas as pd
import re
from tkinter import messagebox
from lachesis_support_functions import round_mean,create_svod_sub



class BadOrderBEB(Exception):
    """
    Исключение для обработки случая когда колонки не совпадают
    """
    pass


class BadValueBEB(Exception):
    """
    Исключение для неправильных значений в вариантах ответов
    """
    pass

class BadCountColumnsBEB(Exception):
    """
    Исключение для обработки случая если количество колонок не равно 84
    """
    pass


def calc_level_sub(value):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """
    if 0 <= value <= 9:
        return 'не сложившийся симптом'
    elif 10 <= value <= 15:
        return 'складывающийся симптом'
    elif 16 <= value <= 19:
        return 'сложившийся симптом'
    else:
        return 'доминирующий симптом'

def calc_level_phase(value):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """
    if 0 <= value <= 36:
        return 'фаза не сформировалась'
    elif 37 <= value <= 60:
        return 'фаза в стадии формирования'
    else:
        return 'сформировавшаяся фаза'

def calc_level_em_burnout(value):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """
    if 0 <= value <= 99:
        return '0-99'
    elif 100 <= value <= 149:
        return '100-149'
    elif 150 <= value <= 199:
        return '150-199'
    elif 200 <= value <= 249:
        return '200-249'
    elif 250 <= value <= 299:
        return '250-299'
    else:
        return '300 и более'



def calc_sub_value_ppo(row):
    """
    Функция для подсчета значения субшкалы Переживание психотравмирующих обстоятельств
    :param row: строка с ответами
    :return: число
    """
    lst_pr = [1,13,25,37,49,61,73] # вопросы
    result = 0 # результат
    for idx, value in enumerate(row):
        if idx +1 in lst_pr:
            if idx + 1 == 1: # Вопрос 1
                if value == 'да':
                    result += 2
            elif idx + 1 == 13: # Вопрос 13
                if value == 'да':
                    result += 3
            elif idx + 1 == 25: # Вопрос 25
                if value == 'да':
                    result += 2
            elif idx + 1 == 37: # Вопрос 37
                if value == 'нет':
                    result += 3
            elif idx + 1 == 49: # Вопрос 49
                if value == 'да':
                    result += 10
            elif idx + 1 == 61: # Вопрос 61
                if value == 'да':
                    result += 5
            elif idx + 1 == 73: # Вопрос 73
                if value == 'нет':
                    result += 5
    return result


def calc_sub_value_ns(row):
    """
    Функция для подсчета значения субшкалы Неудовлетворенность собой
    :param row: строка с ответами
    :return: число
    """
    lst_pr = [2,14,26,38,50,62,74] # вопросы
    result = 0 # результат
    for idx, value in enumerate(row):
        if idx +1 in lst_pr:
            if idx + 1 == 2: # Вопрос 2
                if value == 'нет':
                    result += 3
            elif idx + 1 == 14: # Вопрос 14
                if value == 'да':
                    result += 2
            elif idx + 1 == 26: # Вопрос 26
                if value == 'да':
                    result += 2
            elif idx + 1 == 38: # Вопрос 38
                if value == 'нет':
                    result += 10
            elif idx + 1 == 50: # Вопрос 50
                if value == 'нет':
                    result += 5
            elif idx + 1 == 62: # Вопрос 62
                if value == 'да':
                    result += 5
            elif idx + 1 == 74: # Вопрос 74
                if value == 'да':
                    result += 3
    return result

def calc_sub_value_zk(row):
    """
    Функция для подсчета значения субшкалы «Загнанность в клетку»
    :param row: строка с ответами
    :return: число
    """
    lst_pr = [3,15,27,39,51,63,75] # вопросы
    result = 0 # результат
    for idx, value in enumerate(row):
        if idx +1 in lst_pr:
            if idx + 1 == 3: # Вопрос 3
                if value == 'да':
                    result += 10
            elif idx + 1 == 15: # Вопрос 15
                if value == 'да':
                    result += 5
            elif idx + 1 == 27: # Вопрос 27
                if value == 'да':
                    result += 2
            elif idx + 1 == 39: # Вопрос 39
                if value == 'да':
                    result += 2
            elif idx + 1 == 51: # Вопрос 51
                if value == 'да':
                    result += 5
            elif idx + 1 == 63: # Вопрос 63
                if value == 'да':
                    result += 1
            elif idx + 1 == 75: # Вопрос 75
                if value == 'нет':
                    result += 5
    return result


def calc_sub_value_td(row):
    """
    Функция для подсчета значения субшкалы Тревога и депрессия
    :param row: строка с ответами
    :return: число
    """
    lst_pr = [4,16,28,40,52,64,76] # вопросы
    result = 0 # результат
    for idx, value in enumerate(row):
        if idx +1 in lst_pr:
            if idx + 1 == 4: # Вопрос 4
                if value == 'да':
                    result += 2
            elif idx + 1 == 16: # Вопрос 16
                if value == 'да':
                    result += 3
            elif idx + 1 == 28: # Вопрос 28
                if value == 'да':
                    result += 5
            elif idx + 1 == 40: # Вопрос 40
                if value == 'да':
                    result += 5
            elif idx + 1 == 52: # Вопрос 52
                if value == 'да':
                    result += 10
            elif idx + 1 == 64: # Вопрос 64
                if value == 'да':
                    result += 2
            elif idx + 1 == 76: # Вопрос 76
                if value == 'да':
                    result += 3


    return result


def calc_sub_value_niar(row):
    """
    Функция для подсчета значения субшкалы Неадекватное избирательное эмоциональное реагирование
    :param row: строка с ответами
    :return: число
    """
    lst_pr = [5,17,29,41,53,65,77] # вопросы
    result = 0 # результат
    for idx, value in enumerate(row):
        if idx +1 in lst_pr:
            if idx + 1 == 5: # Вопрос 5
                if value == 'да':
                    result += 5
            elif idx + 1 == 17: # Вопрос 17
                if value == 'нет':
                    result += 3
            elif idx + 1 == 29: # Вопрос 29
                if value == 'да':
                    result += 10
            elif idx + 1 == 41: # Вопрос 41
                if value == 'да':
                    result += 2
            elif idx + 1 == 53: # Вопрос 53
                if value == 'да':
                    result += 2
            elif idx + 1 == 65: # Вопрос 65
                if value == 'да':
                    result += 3
            elif idx + 1 == 77: # Вопрос 77
                if value == 'да':
                    result += 5



    return result


def calc_sub_value_and(row):
    """
    Функция для подсчета значения субшкалы Эмоционально-нравственная дезориентация
    :param row: строка с ответами
    :return: число
    """
    lst_pr = [6,18,30,42,54,66,78] # вопросы
    result = 0 # результат
    for idx, value in enumerate(row):
        if idx +1 in lst_pr:
            if idx + 1 == 6: # Вопрос 6
                if value == 'да':
                    result += 10
            elif idx + 1 == 18: # Вопрос 18
                if value == 'нет':
                    result += 3
            elif idx + 1 == 30: # Вопрос 30
                if value == 'да':
                    result += 3
            elif idx + 1 == 42: # Вопрос 42
                if value == 'да':
                    result += 5
            elif idx + 1 == 54: # Вопрос 54
                if value == 'да':
                    result += 2
            elif idx + 1 == 66: # Вопрос 66
                if value == 'да':
                    result += 2
            elif idx + 1 == 78: # Вопрос 78
                if value == 'нет':
                    result += 5




    return result


def calc_sub_value_rsaa(row):
    """
    Функция для подсчета значения субшкалы Расширение сферы экономии эмоций
    :param row: строка с ответами
    :return: число
    """
    lst_pr = [7,19,31,43,55,67,79] # вопросы
    result = 0 # результат
    for idx, value in enumerate(row):
        if idx +1 in lst_pr:
            if idx + 1 == 7: # Вопрос 7
                if value == 'да':
                    result += 2
            elif idx + 1 == 19: # Вопрос 19
                if value == 'да':
                    result += 10
            elif idx + 1 == 31: # Вопрос 31
                if value == 'нет':
                    result += 2
            elif idx + 1 == 43: # Вопрос 43
                if value == 'да':
                    result += 5
            elif idx + 1 == 55: # Вопрос 55
                if value == 'да':
                    result += 3
            elif idx + 1 == 67: # Вопрос 67
                if value == 'да':
                    result += 3
            elif idx + 1 == 79: # Вопрос 79
                if value == 'нет':
                    result += 5




    return result


def calc_sub_value_rpo(row):
    """
    Функция для подсчета значения субшкалы Редукция профессиональных обязанностей
    :param row: строка с ответами
    :return: число
    """
    lst_pr = [8,20,32,44,56,68,80] # вопросы
    result = 0 # результат
    for idx, value in enumerate(row):
        if idx +1 in lst_pr:
            if idx + 1 == 8: # Вопрос 8
                if value == 'да':
                    result += 5
            elif idx + 1 == 20: # Вопрос 20
                if value == 'да':
                    result += 5
            elif idx + 1 == 32: # Вопрос 32
                if value == 'да':
                    result += 2
            elif idx + 1 == 44: # Вопрос 44
                if value == 'нет':
                    result += 2
            elif idx + 1 == 56: # Вопрос 56
                if value == 'да':
                    result += 3
            elif idx + 1 == 68: # Вопрос 68
                if value == 'да':
                    result += 3
            elif idx + 1 == 80: # Вопрос 80
                if value == 'да':
                    result += 10



    return result



def calc_sub_value_ad(row):
    """
    Функция для подсчета значения субшкалы Эмоциональный дефицит
    :param row: строка с ответами
    :return: число
    """
    lst_pr = [9,21,33,45,57,69,81] # вопросы
    result = 0 # результат
    for idx, value in enumerate(row):
        if idx +1 in lst_pr:
            if idx + 1 == 9: # Вопрос 9
                if value == 'да':
                    result += 3
            elif idx + 1 == 21: # Вопрос 21
                if value == 'да':
                    result += 2
            elif idx + 1 == 33: # Вопрос 33
                if value == 'да':
                    result += 5
            elif idx + 1 == 45: # Вопрос 45
                if value == 'нет':
                    result += 5
            elif idx + 1 == 57: # Вопрос 57
                if value == 'да':
                    result += 3
            elif idx + 1 == 69: # Вопрос 69
                if value == 'нет':
                    result += 10
            elif idx + 1 == 81: # Вопрос 81
                if value == 'да':
                    result += 2


    return result

def calc_sub_value_ao(row):
    """
    Функция для подсчета значения субшкалы Эмоциональная отстраненность
    :param row: строка с ответами
    :return: число
    """
    lst_pr = [10,22,34,46,58,70,82] # вопросы
    result = 0 # результат
    for idx, value in enumerate(row):
        if idx +1 in lst_pr:
            if idx + 1 == 10: # Вопрос 10
                if value == 'да':
                    result += 2
            elif idx + 1 == 22: # Вопрос 22
                if value == 'да':
                    result += 3
            elif idx + 1 == 34: # Вопрос 34
                if value == 'нет':
                    result += 2
            elif idx + 1 == 46: # Вопрос 46
                if value == 'да':
                    result += 3
            elif idx + 1 == 58: # Вопрос 58
                if value == 'да':
                    result += 5
            elif idx + 1 == 70: # Вопрос 70
                if value == 'да':
                    result += 5
            elif idx + 1 == 82: # Вопрос 82
                if value == 'да':
                    result += 5


    return result


def calc_sub_value_lo(row):
    """
    Функция для подсчета значения субшкалы Личностная отстраненность (деперсонализация)
    :param row: строка с ответами
    :return: число
    """
    lst_pr = [11,23,35,47,59,72,83] # вопросы
    result = 0 # результат
    for idx, value in enumerate(row):
        if idx +1 in lst_pr:
            if idx + 1 == 11: # Вопрос 11
                if value == 'да':
                    result += 5
            elif idx + 1 == 23: # Вопрос 23
                if value == 'да':
                    result += 3
            elif idx + 1 == 35: # Вопрос 35
                if value == 'да':
                    result += 3
            elif idx + 1 == 47: # Вопрос 47
                if value == 'да':
                    result += 5
            elif idx + 1 == 59: # Вопрос 59
                if value == 'да':
                    result += 5
            elif idx + 1 == 72: # Вопрос 72
                if value == 'да':
                    result += 2
            elif idx + 1 == 83: # Вопрос 83
                if value == 'да':
                    result += 10


    return result


def calc_sub_value_ppn(row):
    """
    Функция для подсчета значения субшкалы Психосоматические и психовегетативные нарушения
    :param row: строка с ответами
    :return: число
    """
    lst_pr = [12,24,36,48,60,72,84] # вопросы
    result = 0 # результат
    for idx, value in enumerate(row):
        if idx +1 in lst_pr:
            if idx + 1 == 12: # Вопрос 12
                if value == 'да':
                    result += 3
            elif idx + 1 == 24: # Вопрос 24
                if value == 'да':
                    result += 2
            elif idx + 1 == 36: # Вопрос 36
                if value == 'да':
                    result += 5
            elif idx + 1 == 48: # Вопрос 48
                if value == 'да':
                    result += 3
            elif idx + 1 == 60: # Вопрос 60
                if value == 'да':
                    result += 2
            elif idx + 1 == 72: # Вопрос 72
                if value == 'да':
                    result += 10
            elif idx + 1 == 84: # Вопрос 84
                if value == 'да':
                    result += 5

    return result


def calc_count_main_level(df:pd.DataFrame, lst_cat:list, val_cat, col_cat, lst_cols:list):
    """
    Функция для создания сводных датафреймов

    :param df: датафрейм с данными
    :param lst_cat:список колонок по которым будет формироваться свод
    :param val_cat:значение по которому будет формироваться свод
    :param col_cat: колонка по которой будет формироваться свод
    :param lst_cols: список с колонками
    :return:датафрейм
    """
    count_df = pd.pivot_table(df, index=lst_cat,
                                             columns=col_cat,
                                             values=val_cat,
                                             aggfunc='count', margins=True, margins_name='Итого')


    count_df.reset_index(inplace=True)
    count_df = count_df.reindex(columns=lst_cols)
    count_df['% 0-99 от общего'] = round(
        count_df['0-99'] / count_df['Итого'], 2) * 100
    count_df['% 100-149 от общего'] = round(
        count_df['100-149'] / count_df['Итого'], 2) * 100
    count_df['% 150-199 от общего'] = round(
        count_df['150-199'] / count_df['Итого'], 2) * 100
    count_df['% 200-249 от общего'] = round(
        count_df['200-249'] / count_df['Итого'], 2) * 100
    count_df['% 250-299 от общего'] = round(
        count_df['250-299'] / count_df['Итого'], 2) * 100
    count_df['% 300 и более от общего'] = round(
        count_df['300 и более'] / count_df['Итого'], 2) * 100

    return count_df

def calc_count_level_phase(df:pd.DataFrame, lst_cat:list, val_cat, col_cat, lst_cols:list):
    """
    Функция для создания сводных датафреймов по фазам

    :param df: датафрейм с данными
    :param lst_cat:список колонок по которым будет формироваться свод
    :param val_cat:значение по которому будет формироваться свод
    :param col_cat: колонка по которой будет формироваться свод
    :param lst_cols: список с колонками
    :return:датафрейм
    """
    count_df = pd.pivot_table(df, index=lst_cat,
                                             columns=col_cat,
                                             values=val_cat,
                                             aggfunc='count', margins=True, margins_name='Итого')


    count_df.reset_index(inplace=True)
    count_df = count_df.reindex(columns=lst_cols)
    count_df['% фаза не сформировалась от общего'] = round(
        count_df['фаза не сформировалась'] / count_df['Итого'], 2) * 100
    count_df['% фаза в стадии формирования от общего'] = round(
        count_df['фаза в стадии формирования'] / count_df['Итого'], 2) * 100
    count_df['% сформировавшаяся фаза от общего'] = round(
        count_df['сформировавшаяся фаза'] / count_df['Итого'], 2) * 100

    return count_df


def calc_count_level_sub(df:pd.DataFrame, lst_cat:list, val_cat, col_cat, lst_cols:list):
    """
    Функция для создания сводных датафреймов по субшкалам

    :param df: датафрейм с данными
    :param lst_cat:список колонок по которым будет формироваться свод
    :param val_cat:значение по которому будет формироваться свод
    :param col_cat: колонка по которой будет формироваться свод
    :param lst_cols: список с колонками
    :return:датафрейм
    """
    count_df = pd.pivot_table(df, index=lst_cat,
                                             columns=col_cat,
                                             values=val_cat,
                                             aggfunc='count', margins=True, margins_name='Итого')


    count_df.reset_index(inplace=True)
    count_df = count_df.reindex(columns=lst_cols)
    count_df['% не сложившийся симптом от общего'] = round(
        count_df['не сложившийся симптом'] / count_df['Итого'], 2) * 100
    count_df['% складывающийся симптом от общего'] = round(
        count_df['складывающийся симптом'] / count_df['Итого'], 2) * 100
    count_df['% сложившийся симптом от общего'] = round(
        count_df['сложившийся симптом'] / count_df['Итого'], 2) * 100
    count_df['% доминирующий симптом от общего'] = round(
        count_df['доминирующий симптом'] / count_df['Итого'], 2) * 100

    return count_df

def calc_mean(df:pd.DataFrame,lst_cat:list,val_cat):
    """
    Функция для создания сводных датафреймов

    :param df: датафрейм с данными
    :param lst_cat:список колонок по которым будет формироваться свод
    :param val_cat:значение по которому будет формиваться свод
    :return:датафрейм
    """
    calc_mean_df = pd.pivot_table(df, index=lst_cat,
                                       values=val_cat,
                                       aggfunc=round_mean)
    calc_mean_df.reset_index(inplace=True)
    calc_mean_df.rename(columns={val_cat:'Среднее значение'},inplace=True)
    return calc_mean_df



def calc_dominus_simptom(row:pd.Series,dct_replace:dict):
    """
    Функция для выявления доминирующих симптомов
    :param row: строка
    :param dct_replace: словарь для замены на аббревиатуры
    :return: названия симптомов
    """
    lst_simptom = [] # список для доминируюищх симтомов
    dct_row = row.to_dict() # превращаем в словарь
    for name_cols in dct_row.keys():
        # перебираем ключи словаря с названиями колонок
        if name_cols in dct_replace:
            if dct_row[name_cols] == 'доминирующий симптом':
                lst_simptom.append(dct_replace[name_cols])
    if len(lst_simptom) == 0:
        return 'отсутствуют доминирующие симптомы'
    else:
        return ',\n'.join(lst_simptom)


def create_result_beb(base_df:pd.DataFrame,out_dct:dict,lst_svod_cols:list):
    """
    Функция для подсчета результата если указаны колонки по которым нужно провести свод
    :param df: датафрейм с результатами
    :param out_dct: словарь с уже подсчитанными базовыми данными
    :param lst_svod_cols: список сводных колонок
    :return: словарь
    """
    lst_reindex_main_level_cols = lst_svod_cols.copy()
    lst_reindex_main_level_cols.extend(['0-99', '100-149', '150-199', '200-249', '250-299', '300 и более',
   'Итого'])  # Основная шкала

    lst_reindex_phase_level_cols = lst_svod_cols.copy()
    lst_reindex_phase_level_cols.extend(['фаза не сформировалась', 'фаза в стадии формирования',
                                    'сформировавшаяся фаза',
                                    'Итого'])  # Фазы
    lst_reindex_sub_level_cols = lst_svod_cols.copy()
    lst_reindex_sub_level_cols.extend(['не сложившийся симптом', 'складывающийся симптом',
                                  'сложившийся симптом', 'доминирующий симптом',
                                  'Итого'])  # Симптомы

    # основная шкала
    svod_count_one_level_df = calc_count_main_level(base_df, lst_svod_cols,
                                                    'Итоговое_значение_эмоционального_выгорания',
                                                    'Диапазон_эмоционального_выгорания',
                                                    lst_reindex_main_level_cols)

    # Фазы
    svod_count_one_phase_stress_df = calc_count_level_phase(base_df, lst_svod_cols,
                                                            'Значение_фазы_Напряжение',
                                                            'Уровень_фазы_Напряжение',
                                                            lst_reindex_phase_level_cols)

    svod_count_one_phase_resistance_df = calc_count_level_phase(base_df, lst_svod_cols,
                                                                'Значение_фазы_Резистенция',
                                                                'Уровень_фазы_Резистенция',
                                                                lst_reindex_phase_level_cols)
    svod_count_one_phase_exhaustion_df = calc_count_level_phase(base_df, lst_svod_cols,
                                                                'Значение_фазы_Истощение',
                                                                'Уровень_фазы_Истощение',
                                                                lst_reindex_phase_level_cols)

    # Симптомы
    # 1 phase
    svod_count_one_level_ppo_df = calc_count_level_sub(base_df, lst_svod_cols,
                                                       'Значение_симптома_Переживание_психотравмирующих_обстоятельств',
                                                       'Уровень_симптома_Переживание_психотравмирующих_обстоятельств',
                                                       lst_reindex_sub_level_cols)
    svod_count_one_level_ns_df = calc_count_level_sub(base_df, lst_svod_cols,
                                                      'Значение_симптома_Неудовлетворенность_собой',
                                                      'Уровень_симптома_Неудовлетворенность_собой',
                                                      lst_reindex_sub_level_cols)
    svod_count_one_level_zk_df = calc_count_level_sub(base_df, lst_svod_cols,
                                                      'Значение_симптома_Загнанность_в_клетку',
                                                      'Уровень_симптома_Загнанность_в_клетку',
                                                      lst_reindex_sub_level_cols)
    svod_count_one_level_td_df = calc_count_level_sub(base_df, lst_svod_cols,
                                                      'Значение_симптома_Тревога_и_депрессия',
                                                      'Уровень_симптома_Тревога_и_депрессия',
                                                      lst_reindex_sub_level_cols)
    # 2 phase
    svod_count_one_level_niar_df = calc_count_level_sub(base_df, lst_svod_cols,
                                                        'Значение_симптома_Неадекватное_избирательное_эмоциональное_реагирование',
                                                        'Уровень_симптома_Неадекватное_избирательное_эмоциональное_реагирование',
                                                        lst_reindex_sub_level_cols)
    svod_count_one_level_and_df = calc_count_level_sub(base_df, lst_svod_cols,
                                                       'Значение_симптома_Эмоционально_нравственная_дезориентация',
                                                       'Уровень_симптома_Эмоционально_нравственная_дезориентация',
                                                       lst_reindex_sub_level_cols)
    svod_count_one_level_rsaa_df = calc_count_level_sub(base_df, lst_svod_cols,
                                                        'Значение_симптома_Расширение_сферы_экономии_эмоций',
                                                        'Уровень_симптома_Расширение_сферы_экономии_эмоций',
                                                        lst_reindex_sub_level_cols)
    svod_count_one_level_rpo_df = calc_count_level_sub(base_df, lst_svod_cols,
                                                       'Значение_симптома_Редукция_профессиональных_обязанностей',
                                                       'Уровень_симптома_Редукция_профессиональных_обязанностей',
                                                       lst_reindex_sub_level_cols)
    # 3 phase
    svod_count_one_level_ad_df = calc_count_level_sub(base_df, lst_svod_cols,
                                                      'Значение_симптома_Эмоциональный_дефицит',
                                                      'Уровень_симптома_Эмоциональный_дефицит',
                                                      lst_reindex_sub_level_cols)
    svod_count_one_level_ao_df = calc_count_level_sub(base_df, lst_svod_cols,
                                                      'Значение_симптома_Эмоциональная_отстраненность',
                                                      'Уровень_симптома_Эмоциональная_отстраненность',
                                                      lst_reindex_sub_level_cols)
    svod_count_one_level_lo_df = calc_count_level_sub(base_df, lst_svod_cols,
                                                      'Значение_симптома_Личностная_отстраненность',
                                                      'Уровень_симптома_Личностная_отстраненность',
                                                      lst_reindex_sub_level_cols)
    svod_count_one_level_ppn_df = calc_count_level_sub(base_df, lst_svod_cols,
                                                       'Значение_симптома_Психосоматические_и_психовегетативные_нарушения',
                                                       'Уровень_симптома_Психосоматические_и_психовегетативные_нарушения',
                                                       lst_reindex_sub_level_cols)



    # Считаем среднее по субшкалам
    svod_mean_df = pd.pivot_table(base_df,
                                  index=[lst_svod_cols[0]],
                                  values=['Итоговое_значение_эмоционального_выгорания', 'Значение_фазы_Напряжение',
                                          'Значение_фазы_Резистенция', 'Значение_фазы_Истощение',
                                          'Значение_симптома_Переживание_психотравмирующих_обстоятельств',
                                          'Значение_симптома_Неудовлетворенность_собой',
                                          'Значение_симптома_Загнанность_в_клетку',
                                          'Значение_симптома_Тревога_и_депрессия',
                                          'Значение_симптома_Неадекватное_избирательное_эмоциональное_реагирование',
                                          'Значение_симптома_Эмоционально_нравственная_дезориентация',
                                          'Значение_симптома_Расширение_сферы_экономии_эмоций',
                                          'Значение_симптома_Редукция_профессиональных_обязанностей',
                                          'Значение_симптома_Эмоциональный_дефицит',
                                          'Значение_симптома_Эмоциональная_отстраненность',
                                          'Значение_симптома_Личностная_отстраненность',
                                          'Значение_симптома_Психосоматические_и_психовегетативные_нарушения'
                                          ],
                                  aggfunc=round_mean)
    svod_mean_df.reset_index(inplace=True)
    # упорядочиваем колонки
    new_order_cols = lst_svod_cols.copy()
    new_order_cols.extend(
        ['Итоговое_значение_эмоционального_выгорания', 'Значение_фазы_Напряжение', 'Значение_фазы_Резистенция',
         'Значение_фазы_Истощение',
         'Значение_симптома_Переживание_психотравмирующих_обстоятельств', 'Значение_симптома_Неудовлетворенность_собой',
         'Значение_симптома_Загнанность_в_клетку', 'Значение_симптома_Тревога_и_депрессия',
         'Значение_симптома_Неадекватное_избирательное_эмоциональное_реагирование',
         'Значение_симптома_Эмоционально_нравственная_дезориентация',
         'Значение_симптома_Расширение_сферы_экономии_эмоций',
         'Значение_симптома_Редукция_профессиональных_обязанностей',
         'Значение_симптома_Эмоциональный_дефицит', 'Значение_симптома_Эмоциональная_отстраненность',
         'Значение_симптома_Личностная_отстраненность',
         'Значение_симптома_Психосоматические_и_психовегетативные_нарушения'])
    svod_mean_df = svod_mean_df.reindex(columns=new_order_cols)
    dct_rename_cols_mean = {'Итоговое_значение_эмоционального_выгорания': 'Ср. эмоционального выгорания',
                            'Значение_фазы_Напряжение': 'Ср. фазы Напряжение',
                            'Значение_фазы_Резистенция': 'Ср. фазы Резистенция',
                            'Значение_фазы_Истощение': 'Ср. фазы Истощение',
                            'Значение_симптома_Переживание_психотравмирующих_обстоятельств': 'Ср. ППО',
                            'Значение_симптома_Неудовлетворенность_собой': 'Ср. НС',
                            'Значение_симптома_Загнанность_в_клетку': 'Ср. ЗК',
                            'Значение_симптома_Тревога_и_депрессия': 'Ср. ТД',

                            'Значение_симптома_Неадекватное_избирательное_эмоциональное_реагирование': 'Ср. НИЭР',
                            'Значение_симптома_Эмоционально_нравственная_дезориентация': 'Ср. ЭНД',
                            'Значение_симптома_Расширение_сферы_экономии_эмоций': 'Ср. РСЭЭ',
                            'Значение_симптома_Редукция_профессиональных_обязанностей': 'Ср. РПО',

                            'Значение_симптома_Эмоциональный_дефицит': 'Ср. ЭД',
                            'Значение_симптома_Эмоциональная_отстраненность': 'Ср. ЭО',
                            'Значение_симптома_Личностная_отстраненность': 'Ср. ЛО',
                            'Значение_симптома_Психосоматические_и_психовегетативные_нарушения': 'Ср. ППН'}
    svod_mean_df.rename(columns=dct_rename_cols_mean, inplace=True)

    # очищаем название колонки по которой делали свод
    out_name_lst = []


    for name_col in lst_svod_cols:
        name = re.sub(r'[\[\]\'+()<> :"?*|\\/]', '_', name_col)
        out_name_lst.append(name[:10])

    out_name = ' '.join(out_name_lst)
    if len(out_name) > 14:
        out_name = out_name[:14]




    out_dct.update({f'Свод {out_name}': svod_count_one_level_df,
                    f'Ср. {out_name}': svod_mean_df,
                    f'Свод Напряжение {out_name}': svod_count_one_phase_stress_df,
                    f'Свод Резистенция {out_name}': svod_count_one_phase_resistance_df,
                    f'Свод Истощение {out_name}': svod_count_one_phase_exhaustion_df,

                    f'Свод ППО {out_name}': svod_count_one_level_ppo_df,
                    f'Свод НС {out_name}': svod_count_one_level_ns_df,
                    f'Свод ЗК {out_name}': svod_count_one_level_zk_df,
                    f'Свод ТД {out_name}': svod_count_one_level_td_df,

                    f'Свод НИЭР {out_name}': svod_count_one_level_niar_df,
                    f'Свод ЭНД {out_name}': svod_count_one_level_and_df,
                    f'Свод РСЭЭ {out_name}': svod_count_one_level_rsaa_df,
                    f'Свод РПО {out_name}': svod_count_one_level_rpo_df,

                    f'Свод ЭД {out_name}': svod_count_one_level_ad_df,
                    f'Свод ЭО {out_name}': svod_count_one_level_ao_df,
                    f'Свод ЛО {out_name}': svod_count_one_level_lo_df,
                    f'Свод ППН {out_name}': svod_count_one_level_ppn_df,

                    })

    if len(lst_svod_cols) == 1:
        return out_dct
    else:
        for idx,name_column in enumerate(lst_svod_cols):
            lst_reindex_column_level_cols = [lst_svod_cols[idx], '0-99', '100-149', '150-199', '200-249', '250-299',
                                           '300 и более',
                                           'Итого']  # Основная шкала

            lst_reindex_column_phase_level_cols = [lst_svod_cols[idx], 'фаза не сформировалась', 'фаза в стадии формирования',
                                            'сформировавшаяся фаза',
                                            'Итого']  # Фазы
            lst_reindex_column_sub_level_cols = [lst_svod_cols[idx], 'не сложившийся симптом', 'складывающийся симптом',
                                          'сложившийся симптом', 'доминирующий симптом',
                                          'Итого']  # Симптомы

            svod_count_column_level_df = calc_count_main_level(base_df, [lst_svod_cols[idx]],
                                                               'Итоговое_значение_эмоционального_выгорания',
                                                               'Диапазон_эмоционального_выгорания',
                                                               lst_reindex_column_level_cols)

            # Фазы
            svod_count_column_phase_stress_df = calc_count_level_phase(base_df, [lst_svod_cols[idx]],
                                                                       'Значение_фазы_Напряжение',
                                                                       'Уровень_фазы_Напряжение',
                                                                       lst_reindex_column_phase_level_cols)

            svod_count_column_phase_resistance_df = calc_count_level_phase(base_df, [lst_svod_cols[idx]],
                                                                           'Значение_фазы_Резистенция',
                                                                           'Уровень_фазы_Резистенция',
                                                                           lst_reindex_column_phase_level_cols)
            svod_count_column_phase_exhaustion_df = calc_count_level_phase(base_df, [lst_svod_cols[idx]],
                                                                           'Значение_фазы_Истощение',
                                                                           'Уровень_фазы_Истощение',
                                                                           lst_reindex_column_phase_level_cols)

            # Симптомы
            # 1 phase
            svod_count_column_level_ppo_df = calc_count_level_sub(base_df, [lst_svod_cols[idx]],
                                                                  'Значение_симптома_Переживание_психотравмирующих_обстоятельств',
                                                                  'Уровень_симптома_Переживание_психотравмирующих_обстоятельств',
                                                                  lst_reindex_column_sub_level_cols)
            svod_count_column_level_ns_df = calc_count_level_sub(base_df, [lst_svod_cols[idx]],
                                                                 'Значение_симптома_Неудовлетворенность_собой',
                                                                 'Уровень_симптома_Неудовлетворенность_собой',
                                                                 lst_reindex_column_sub_level_cols)
            svod_count_column_level_zk_df = calc_count_level_sub(base_df, [lst_svod_cols[idx]],
                                                                 'Значение_симптома_Загнанность_в_клетку',
                                                                 'Уровень_симптома_Загнанность_в_клетку',
                                                                 lst_reindex_column_sub_level_cols)
            svod_count_column_level_td_df = calc_count_level_sub(base_df, [lst_svod_cols[idx]],
                                                                 'Значение_симптома_Тревога_и_депрессия',
                                                                 'Уровень_симптома_Тревога_и_депрессия',
                                                                 lst_reindex_column_sub_level_cols)
            # 2 phase
            svod_count_column_level_niar_df = calc_count_level_sub(base_df, [lst_svod_cols[idx]],
                                                                   'Значение_симптома_Неадекватное_избирательное_эмоциональное_реагирование',
                                                                   'Уровень_симптома_Неадекватное_избирательное_эмоциональное_реагирование',
                                                                   lst_reindex_column_sub_level_cols)
            svod_count_column_level_and_df = calc_count_level_sub(base_df, [lst_svod_cols[idx]],
                                                                  'Значение_симптома_Эмоционально_нравственная_дезориентация',
                                                                  'Уровень_симптома_Эмоционально_нравственная_дезориентация',
                                                                  lst_reindex_column_sub_level_cols)
            svod_count_column_level_rsaa_df = calc_count_level_sub(base_df, [lst_svod_cols[idx]],
                                                                   'Значение_симптома_Расширение_сферы_экономии_эмоций',
                                                                   'Уровень_симптома_Расширение_сферы_экономии_эмоций',
                                                                   lst_reindex_column_sub_level_cols)
            svod_count_column_level_rpo_df = calc_count_level_sub(base_df, [lst_svod_cols[idx]],
                                                                  'Значение_симптома_Редукция_профессиональных_обязанностей',
                                                                  'Уровень_симптома_Редукция_профессиональных_обязанностей',
                                                                  lst_reindex_column_sub_level_cols)
            # 3 phase
            svod_count_column_level_ad_df = calc_count_level_sub(base_df, [lst_svod_cols[idx]],
                                                                 'Значение_симптома_Эмоциональный_дефицит',
                                                                 'Уровень_симптома_Эмоциональный_дефицит',
                                                                 lst_reindex_column_sub_level_cols)
            svod_count_column_level_ao_df = calc_count_level_sub(base_df, [lst_svod_cols[idx]],
                                                                 'Значение_симптома_Эмоциональная_отстраненность',
                                                                 'Уровень_симптома_Эмоциональная_отстраненность',
                                                                 lst_reindex_column_sub_level_cols)
            svod_count_column_level_lo_df = calc_count_level_sub(base_df, [lst_svod_cols[idx]],
                                                                 'Значение_симптома_Личностная_отстраненность',
                                                                 'Уровень_симптома_Личностная_отстраненность',
                                                                 lst_reindex_column_sub_level_cols)
            svod_count_column_level_ppn_df = calc_count_level_sub(base_df, [lst_svod_cols[idx]],
                                                                  'Значение_симптома_Психосоматические_и_психовегетативные_нарушения',
                                                                  'Уровень_симптома_Психосоматические_и_психовегетативные_нарушения',
                                                                  lst_reindex_column_sub_level_cols)

            # Считаем среднее по субшкалам
            svod_mean_column_df = pd.pivot_table(base_df,
                                                 index=[lst_svod_cols[idx]],
                                                 values=['Итоговое_значение_эмоционального_выгорания',
                                                         'Значение_фазы_Напряжение',
                                                         'Значение_фазы_Резистенция', 'Значение_фазы_Истощение',
                                                         'Значение_симптома_Переживание_психотравмирующих_обстоятельств',
                                                         'Значение_симптома_Неудовлетворенность_собой',
                                                         'Значение_симптома_Загнанность_в_клетку',
                                                         'Значение_симптома_Тревога_и_депрессия',
                                                         'Значение_симптома_Неадекватное_избирательное_эмоциональное_реагирование',
                                                         'Значение_симптома_Эмоционально_нравственная_дезориентация',
                                                         'Значение_симптома_Расширение_сферы_экономии_эмоций',
                                                         'Значение_симптома_Редукция_профессиональных_обязанностей',
                                                         'Значение_симптома_Эмоциональный_дефицит',
                                                         'Значение_симптома_Эмоциональная_отстраненность',
                                                         'Значение_симптома_Личностная_отстраненность',
                                                         'Значение_симптома_Психосоматические_и_психовегетативные_нарушения'
                                                         ],
                                                 aggfunc=round_mean)
            svod_mean_column_df.reset_index(inplace=True)
            # упорядочиваем колонки
            new_order_cols = [lst_svod_cols[idx]].copy()
            new_order_cols.extend(
                ['Итоговое_значение_эмоционального_выгорания', 'Значение_фазы_Напряжение', 'Значение_фазы_Резистенция',
                 'Значение_фазы_Истощение',
                 'Значение_симптома_Переживание_психотравмирующих_обстоятельств',
                 'Значение_симптома_Неудовлетворенность_собой',
                 'Значение_симптома_Загнанность_в_клетку', 'Значение_симптома_Тревога_и_депрессия',
                 'Значение_симптома_Неадекватное_избирательное_эмоциональное_реагирование',
                 'Значение_симптома_Эмоционально_нравственная_дезориентация',
                 'Значение_симптома_Расширение_сферы_экономии_эмоций',
                 'Значение_симптома_Редукция_профессиональных_обязанностей',
                 'Значение_симптома_Эмоциональный_дефицит', 'Значение_симптома_Эмоциональная_отстраненность',
                 'Значение_симптома_Личностная_отстраненность',
                 'Значение_симптома_Психосоматические_и_психовегетативные_нарушения'])
            svod_mean_column_df = svod_mean_column_df.reindex(columns=new_order_cols)
            dct_rename_cols_mean = {'Итоговое_значение_эмоционального_выгорания': 'Ср. эмоционального выгорания',
                                    'Значение_фазы_Напряжение': 'Ср. фазы Напряжение',
                                    'Значение_фазы_Резистенция': 'Ср. фазы Резистенция',
                                    'Значение_фазы_Истощение': 'Ср. фазы Истощение',
                                    'Значение_симптома_Переживание_психотравмирующих_обстоятельств': 'Ср. ППО',
                                    'Значение_симптома_Неудовлетворенность_собой': 'Ср. НС',
                                    'Значение_симптома_Загнанность_в_клетку': 'Ср. ЗК',
                                    'Значение_симптома_Тревога_и_депрессия': 'Ср. ТД',

                                    'Значение_симптома_Неадекватное_избирательное_эмоциональное_реагирование': 'Ср. НИЭР',
                                    'Значение_симптома_Эмоционально_нравственная_дезориентация': 'Ср. ЭНД',
                                    'Значение_симптома_Расширение_сферы_экономии_эмоций': 'Ср. РСЭЭ',
                                    'Значение_симптома_Редукция_профессиональных_обязанностей': 'Ср. РПО',

                                    'Значение_симптома_Эмоциональный_дефицит': 'Ср. ЭД',
                                    'Значение_симптома_Эмоциональная_отстраненность': 'Ср. ЭО',
                                    'Значение_симптома_Личностная_отстраненность': 'Ср. ЛО',
                                    'Значение_симптома_Психосоматические_и_психовегетативные_нарушения': 'Ср. ППН'}
            svod_mean_column_df.rename(columns=dct_rename_cols_mean, inplace=True)

            name_column = lst_svod_cols[idx]
            name_column = re.sub(r'[\[\]\'+()<> :"?*|\\/]', '_', name_column)
            name_column = name_column[:15]

            out_dct.update({f'Свод {name_column}': svod_count_column_level_df,
            f'Ср. {name_column}': svod_mean_column_df,
            f'Свод Напряжение {name_column[:10]}': svod_count_column_phase_stress_df,
            f'Свод Резистенция {name_column[:10]}': svod_count_column_phase_resistance_df,
            f'Свод Истощение {name_column[:10]}': svod_count_column_phase_exhaustion_df,

            f'Свод ППО {name_column}': svod_count_column_level_ppo_df,
            f'Свод НС {name_column}': svod_count_column_level_ns_df,
            f'Свод ЗК {name_column}': svod_count_column_level_zk_df,
            f'Свод ТД {name_column}': svod_count_column_level_td_df,

            f'Свод НИЭР {name_column}': svod_count_column_level_niar_df,
            f'Свод ЭНД {name_column}': svod_count_column_level_and_df,
            f'Свод РСЭЭ {name_column}': svod_count_column_level_rsaa_df,
            f'Свод РПО {name_column}': svod_count_column_level_rpo_df,

            f'Свод ЭД {name_column}': svod_count_column_level_ad_df,
            f'Свод ЭО {name_column}': svod_count_column_level_ao_df,
            f'Свод ЛО {name_column}': svod_count_column_level_lo_df,
            f'Свод ППН {name_column}': svod_count_column_level_ppn_df})


        return out_dct
















def processing_boiko_emotional_burnout(base_df: pd.DataFrame, answers_df: pd.DataFrame, lst_svod_cols:list):
    """
    Функция для обработки
    :param base_df: часть датафрейма с описательными колонками
    :param answers_df: часть датафрейма с ответами
    :param lst_svod_cols:  список с колонками по которым нужно делать свод
    """
    out_answer_df = base_df.copy()  # делаем копию для последующего соединения с сырыми ответами
    if len(answers_df.columns) != 84:  # проверяем количество колонок с вопросами
        raise BadCountColumnsBEB

    lst_check_cols = ['Организационные недостатки на работе постоянно заставляют нервничать, переживать, напрягаться.',
                      'Сегодня я доволен(а) своей профессией не меньше, чем в начале карьеры.',
                      'Я ошибся(лась) в выборе профессии или профиля деятельности (занимаю не свое место).',
                      'Меня беспокоит то, что я стал(а) хуже работать (менее продуктивно, качественно, медленнее).',
                      'Теплота взаимодействия с партнерами очень зависит от моего настроения - хорошего или плохого.',
                      'От меня как профессионала мало зависит благополучие партнера.',
                      'Когда я прихожу с работы домой, то некоторое время (часа 2-3) мне хочется побыть наедине, чтобы со мной никто не общался.',
                      'Когда я чувствую усталость или напряжение, то стараюсь поскорее решить проблемы партнера (свернуть взаимодействие).',
                      'Мне кажется, что эмоционально я не могу дать партнерам того, что требует профессиональный долг.',
                      'Моя работа притупляет эмоции.',
                      'Я откровенно устал(а) от человеческих проблем, с которыми приходится иметь дело на работе.',
                      'Бывает, я плохо засыпаю (сплю) из-за переживаний, связанных с работой.',
                      'Взаимодействие с партнерами требует от меня большого напряжения.',
                      'Работа с людьми приносит мне все меньше удовлетворения.',
                      'Я бы сменил(а) место работы, если бы представилась возможность.',
                      'Меня часто расстраивает то, что я не могу должным образом оказать партнеру профессиональную поддержку, услугу, помощь.',
                      'Мне всегда удается предотвратить влияние плохого настроения на деловые контакты.',
                      'Меня очень огорчает, если что-то не ладится в отношениях с деловым партнером.',
                      'Я настолько устаю на работе, что дома стараюсь общаться как можно меньше.',
                      'Из-за нехватки времени, усталости или напряжения часто уделяю внимание партнеру меньше, чем положено.',
                      'Иногда самые обычные ситуации общения на работе вызывают раздражение.',
                      'Я спокойно воспринимаю обоснованные претензии партнеров.',
                      'Общение с партнерами побудило меня сторониться людей.',
                      'При воспоминании о некоторых коллегах по работе или партнерах у меня портится настроение.',
                      'Конфликты или разногласия с коллегами отнимают много сил и эмоций.',
                      'Мне все труднее устанавливать или поддерживать контакты с деловыми партнерами.',
                      'Обстановка на работе мне кажется очень трудной, сложной.',
                      'У меня часто возникают тревожные ожидания, связанные с работой: что-то должно случиться, как бы не допустить ошибки, смогу ли я сделать все как надо, не сократят ли и т. д.',
                      'Если партнер мне неприятен, я стараюсь ограничить время общения с ним или меньше уделять ему внимания.',
                      'В общении не работе я придерживаюсь принципа: «не делай людям добра, не получишь зла».',
                      'Я охотно рассказываю домашним о своей работе.',
                      'Бывают дни, когда мое эмоциональное состояние плохо сказывается на результатах работы (меньше делаю, снижается качество, случаются конфликты).',
                      'Порой я чувствую, что надо проявить к партнеру эмоциональную отзывчивость, но не могу.',
                      'Я очень переживаю за свою работу.',
                      'Партнерам по работе отдаешь внимания и заботы больше, чем получаешь от них признательности.',
                      'При мысли о работе мне обычно становится не по себе начинает колоть в области сердца, повышается давление, появляется головная боль.',
                      'У меня хорошие (вполне удовлетворительные) отношения с непосредственным руководителем.',
                      'Я часто радуюсь, видя, что моя работа приносит пользу людям.',
                      'Последнее время (или как всегда) меня преследуют неудачи на работе.',
                      'Некоторые стороны (факты) моей работы вызывают глубокое разочарование, повергают в уныние.',
                      'Бывают дни, когда контакты с партнерами складываются хуже, чем обычно.',
                      'Я разделяю деловых партнеров (субъектов деятельности) на приятных и неприятных.',
                      'Усталость от работы приводит к тому, что я стараюсь сократить общение с друзьями и знакомыми.',
                      'Я обычно проявляю интерес к личности партнера помимо того) что касается дела.',
                      'Обычно я прихожу на работу отдохнувшим, со свежими силами, в хорошем настроении.',
                      'Я иногда ловлю себя на том, что работаю с партнерами автоматически, без души.',
                      'На работе встречаются настолько неприятные люди, что невольно желаешь им чего-нибудь плохого.',
                      'После общения с неприятными партнерами у меня бывает ухудшение психического и физического самочувствия.',
                      'На работе я испытываю постоянные физические и психические перегрузки.',
                      'Успехи в работе вдохновляют меня.',
                      'Ситуация на работе, в которой я оказался, кажется безысходной.',
                      'Я потерял(а) покой из-за работы.',
                      'На протяжении последнего года были жалобы (была жалоба) в мой адрес со стороны партнеров.',
                      'Мне удается беречь нервы благодаря тому, что многое происходящее с партнерами я не принимаю близко к сердцу.',
                      'Я часто с работы приношу домой отрицательные эмоции.',
                      'Я часто работаю через силу.',
                      'Прежде я был(а) более отзывчивым и внимательным к партнерам, чем теперь.',
                      'В работе с людьми руководствуюсь принципом: не трать нервы, береги здоровье.',
                      'Иногда иду на работу с тяжелым чувством: как все надоело, никого бы не видеть и не слышать.',
                      'После напряженного рабочего дня я чувствую недомогание.',
                      'Контингент партеров, с которыми я работаю, очень трудный.',
                      'Иногда мне кажется, что результаты моей работы не стоят тех усилий, которые я затрачиваю.',
                      'Если бы мне повезло с работой, я был(а) бы более счастлив.',
                      'Я в отчаянии оттого, что на работе у меня серьезные проблемы.',
                      'Иногда я поступаю со своими партнерами так, как не хотел бы, чтобы поступали со мною.',
                      'Я осуждаю партеров, которые рассчитывают на особое снисхождение, внимание.',
                      'Чаще всего после рабочего дня у меня нет сил заниматься домашними делами.',
                      'Обычно я тороплю время: скорей бы рабочий день кончился.',
                      'Состояния, просьбы, потребности партнеров обычно меня искренне волнуют.',
                      'Работая с людьми, я обычно как бы ставлю экран, защищающий меня от чужих страданий, и отрицательных эмоций.',
                      'Работа с людьми (партнерами) очень разочаровала меня.',
                      'Чтобы восстановить силы, я часто принимаю лекарства.',
                      'Как правило, мой рабочий день проходит спокойно и легко.',
                      'Мои требования к выполняемой работе выше, чем то, чего я - достигаю в силу обстоятельств.',
                      'Моя карьера сложилась удачно.',
                      'Я очень нервничаю из-за всего, что связано с работой.',
                      'Некоторых из своих постоянных партнеров я не хотел(а) бы видеть и слышать.',
                      'Я одобряю коллег, которые полностью посвящают себя людям (партнерам), забывая о собственных интересах.',
                      'Моя усталость на работе обычно мало сказывается (никак не сказывается) в общении с домашними и друзьями.',
                      'Если предоставляется случай, я уделяю партнеру меньше внимания, но так, чтобы он этого не заметил.',
                      'Меня часто подводят нервы в общении с людьми на работе.',
                      'Ко всему (почти ко всему), что происходит на работе, я утратил(а) интерес, живое чувство.',
                      'Работа с людьми плохо повлияла на меня как профессионала - обозлила, сделала нервным(ой), притупила эмоции.',
                      'Работа с людьми явно подрывает мое здоровье.',
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
        raise BadOrderBEB

    valid_values = ['да', 'нет']
    # Проверяем, есть ли значения, отличающиеся от указанных в списке
    lst_error_answers = []  # список для хранения строк где найдены неправильные ответы

    for i in range(84):
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
        raise BadValueBEB

    # Симптом Переживание психотравмирующих обстоятельств
    base_df['Норма_Для_симптомов'] = '0-9 баллов'
    base_df['Значение_симптома_Переживание_психотравмирующих_обстоятельств'] = answers_df.apply(calc_sub_value_ppo, axis=1)
    base_df['Уровень_симптома_Переживание_психотравмирующих_обстоятельств'] = base_df[
        'Значение_симптома_Переживание_психотравмирующих_обстоятельств'].apply(
        calc_level_sub)

    # Симптом Неудовлетворенность собой
    base_df['Значение_симптома_Неудовлетворенность_собой'] = answers_df.apply(calc_sub_value_ns, axis=1)
    base_df['Уровень_симптома_Неудовлетворенность_собой'] = base_df[
        'Значение_симптома_Неудовлетворенность_собой'].apply(
        calc_level_sub)

    # Симптом «Загнанность в клетку»
    base_df['Значение_симптома_Загнанность_в_клетку'] = answers_df.apply(calc_sub_value_zk, axis=1)
    base_df['Уровень_симптома_Загнанность_в_клетку'] = base_df[
        'Значение_симптома_Загнанность_в_клетку'].apply(
        calc_level_sub)

    # Симптом Тревога и депрессия
    base_df['Значение_симптома_Тревога_и_депрессия'] = answers_df.apply(calc_sub_value_td, axis=1)
    base_df['Уровень_симптома_Тревога_и_депрессия'] = base_df[
        'Значение_симптома_Тревога_и_депрессия'].apply(
        calc_level_sub)

    # Фаза Напряжение
    base_df['Значение_фазы_Напряжение'] = base_df[['Значение_симптома_Переживание_психотравмирующих_обстоятельств',
                                                   'Значение_симптома_Неудовлетворенность_собой',
                                                   'Значение_симптома_Загнанность_в_клетку','Значение_симптома_Тревога_и_депрессия']].sum(axis=1)

    base_df['Уровень_фазы_Напряжение'] = base_df[
        'Значение_фазы_Напряжение'].apply(calc_level_phase)


    # 2 фаза
    # Симптом Неадекватное избирательное эмоциональное реагирование
    base_df['Значение_симптома_Неадекватное_избирательное_эмоциональное_реагирование'] = answers_df.apply(calc_sub_value_niar, axis=1)
    base_df['Уровень_симптома_Неадекватное_избирательное_эмоциональное_реагирование'] = base_df[
        'Значение_симптома_Неадекватное_избирательное_эмоциональное_реагирование'].apply(
        calc_level_sub)

    # Симптом Эмоционально-нравственная дезориентация
    base_df['Значение_симптома_Эмоционально_нравственная_дезориентация'] = answers_df.apply(calc_sub_value_and, axis=1)
    base_df['Уровень_симптома_Эмоционально_нравственная_дезориентация'] = base_df[
        'Значение_симптома_Эмоционально_нравственная_дезориентация'].apply(
        calc_level_sub)

    # Симптом Расширение сферы экономии эмоций
    base_df['Значение_симптома_Расширение_сферы_экономии_эмоций'] = answers_df.apply(calc_sub_value_rsaa, axis=1)
    base_df['Уровень_симптома_Расширение_сферы_экономии_эмоций'] = base_df[
        'Значение_симптома_Расширение_сферы_экономии_эмоций'].apply(
        calc_level_sub)

    # Симптом Редукция профессиональных обязанностей
    base_df['Значение_симптома_Редукция_профессиональных_обязанностей'] = answers_df.apply(calc_sub_value_rpo, axis=1)
    base_df['Уровень_симптома_Редукция_профессиональных_обязанностей'] = base_df[
        'Значение_симптома_Редукция_профессиональных_обязанностей'].apply(
        calc_level_sub)


    # Фаза РЕЗИСТЕНЦИЯ
    base_df['Значение_фазы_Резистенция'] = base_df[['Значение_симптома_Неадекватное_избирательное_эмоциональное_реагирование',
                                                   'Значение_симптома_Эмоционально_нравственная_дезориентация',
                                                   'Значение_симптома_Расширение_сферы_экономии_эмоций',
                                                    'Значение_симптома_Редукция_профессиональных_обязанностей']].sum(axis=1)

    base_df['Уровень_фазы_Резистенция'] = base_df[
        'Значение_фазы_Резистенция'].apply(calc_level_phase)



    # 3 фаза
    # Симптом Эмоциональный дефицит
    base_df['Значение_симптома_Эмоциональный_дефицит'] = answers_df.apply(calc_sub_value_ad, axis=1)
    base_df['Уровень_симптома_Эмоциональный_дефицит'] = base_df[
        'Значение_симптома_Эмоциональный_дефицит'].apply(
        calc_level_sub)

    # Симптом Эмоциональная отстраненность
    base_df['Значение_симптома_Эмоциональная_отстраненность'] = answers_df.apply(calc_sub_value_ao, axis=1)
    base_df['Уровень_симптома_Эмоциональная_отстраненность'] = base_df[
        'Значение_симптома_Эмоциональная_отстраненность'].apply(
        calc_level_sub)

    # Симптом Личностная отстраненность (деперсонализация)
    base_df['Значение_симптома_Личностная_отстраненность'] = answers_df.apply(calc_sub_value_lo, axis=1)
    base_df['Уровень_симптома_Личностная_отстраненность'] = base_df[
        'Значение_симптома_Личностная_отстраненность'].apply(
        calc_level_sub)

    # Симптом Психосоматические и психовегетативные нарушения
    base_df['Значение_симптома_Психосоматические_и_психовегетативные_нарушения'] = answers_df.apply(calc_sub_value_ppn, axis=1)
    base_df['Уровень_симптома_Психосоматические_и_психовегетативные_нарушения'] = base_df[
        'Значение_симптома_Психосоматические_и_психовегетативные_нарушения'].apply(
        calc_level_sub)

    # Фаза Истощение
    base_df['Значение_фазы_Истощение'] = base_df[['Значение_симптома_Эмоциональный_дефицит',
                                                   'Значение_симптома_Эмоциональная_отстраненность',
                                                   'Значение_симптома_Личностная_отстраненность',
                                                    'Значение_симптома_Психосоматические_и_психовегетативные_нарушения']].sum(axis=1)

    base_df['Уровень_фазы_Истощение'] = base_df[
        'Значение_фазы_Истощение'].apply(calc_level_phase)

    # Итоговый показатель эмоционального выгорания
    base_df['Итоговое_значение_эмоционального_выгорания'] = base_df[['Значение_фазы_Напряжение',
                                                   'Значение_фазы_Резистенция',
                                                   'Значение_фазы_Истощение'
                                                    ]].sum(axis=1)

    base_df['Диапазон_эмоционального_выгорания'] = base_df['Итоговое_значение_эмоционального_выгорания'].apply(calc_level_em_burnout)
    # считаем доминирующие синдромы
    dct_rep = {'Уровень_симптома_Переживание_психотравмирующих_обстоятельств':'Переживание психотравмирующих обстоятельств',
               'Уровень_симптома_Неудовлетворенность_собой':'Неудовлетворенность собой',
               'Уровень_симптома_Загнанность_в_клетку':'«Загнанность в клетку»',
               'Уровень_симптома_Тревога_и_депрессия':'Тревога и депрессия',
               'Уровень_симптома_Неадекватное_избирательное_эмоциональное_реагирование':'Неадекватное избирательное эмоциональное реагирование',
               'Уровень_симптома_Эмоционально_нравственная_дезориентация':'Эмоционально-нравственная дезориентация',
               'Уровень_симптома_Расширение_сферы_экономии_эмоций':'Расширение сферы экономии эмоций',
               'Уровень_симптома_Редукция_профессиональных_обязанностей':'Редукция профессиональных обязанностей',
               'Уровень_симптома_Эмоциональный_дефицит':'Эмоциональный дефицит',
               'Уровень_симптома_Эмоциональная_отстраненность':'Эмоциональная отстраненность',
               'Уровень_симптома_Личностная_отстраненность':'Личностная отстраненность (деперсонализация)',
               'Уровень_симптома_Психосоматические_и_психовегетативные_нарушения':'Психосоматические и психовегетативные нарушения',
               }
    base_df['Доминирующие_симптомы'] = base_df.apply(lambda x:calc_dominus_simptom(x,dct_rep),axis=1)



    # Создаем датафрейм для создания части в общий датафрейм
    part_df = pd.DataFrame()

    part_df['ЭВБ_Значение_эмоционального_выгорания'] = base_df['Итоговое_значение_эмоционального_выгорания']
    part_df['ЭВБ_Диапазон_эмоционального_выгорания'] = base_df['Диапазон_эмоционального_выгорания']

    part_df['ЭВБ_Напряжение_Значение'] = base_df['Значение_фазы_Напряжение']
    part_df['ЭВБ_Напряжение_Уровень'] = base_df['Уровень_фазы_Напряжение']

    part_df['ЭВБ_Резистенция_Значение'] = base_df['Значение_фазы_Резистенция']
    part_df['ЭВБ_Резистенция_Уровень'] = base_df['Уровень_фазы_Резистенция']

    part_df['ЭВБ_Истощение_Значение'] = base_df['Значение_фазы_Истощение']
    part_df['ЭВБ_Истощение_Уровень'] = base_df['Уровень_фазы_Истощение']

    part_df['ЭВБ_ППО_Значение'] = base_df['Значение_симптома_Переживание_психотравмирующих_обстоятельств']
    part_df['ЭВБ_ППО_Уровень'] = base_df['Уровень_симптома_Переживание_психотравмирующих_обстоятельств']

    part_df['ЭВБ_НС_Значение'] = base_df['Значение_симптома_Неудовлетворенность_собой']
    part_df['ЭВБ_НС_Уровень'] = base_df['Уровень_симптома_Неудовлетворенность_собой']

    part_df['ЭВБ_ЗК_Значение'] = base_df['Значение_симптома_Загнанность_в_клетку']
    part_df['ЭВБ_ЗК_Уровень'] = base_df['Уровень_симптома_Загнанность_в_клетку']

    part_df['ЭВБ_ТД_Значение'] = base_df['Значение_симптома_Тревога_и_депрессия']
    part_df['ЭВБ_ТД_Уровень'] = base_df['Уровень_симптома_Тревога_и_депрессия']

    #2 фаза
    part_df['ЭВБ_НИЭР_Значение'] = base_df['Значение_симптома_Неадекватное_избирательное_эмоциональное_реагирование']
    part_df['ЭВБ_НИЭР_Уровень'] = base_df['Уровень_симптома_Неадекватное_избирательное_эмоциональное_реагирование']

    part_df['ЭВБ_ЭНД_Значение'] = base_df['Значение_симптома_Эмоционально_нравственная_дезориентация']
    part_df['ЭВБ_ЭНД_Уровень'] = base_df['Уровень_симптома_Эмоционально_нравственная_дезориентация']

    part_df['ЭВБ_РСЭЭ_Значение'] = base_df['Значение_симптома_Расширение_сферы_экономии_эмоций']
    part_df['ЭВБ_РСЭЭ_Уровень'] = base_df['Уровень_симптома_Расширение_сферы_экономии_эмоций']

    part_df['ЭВБ_РПО_Значение'] = base_df['Значение_симптома_Редукция_профессиональных_обязанностей']
    part_df['ЭВБ_РПО_Уровень'] = base_df['Уровень_симптома_Редукция_профессиональных_обязанностей']

    # 3 фаза
    part_df['ЭВБ_ЭД_Значение'] = base_df['Значение_симптома_Эмоциональный_дефицит']
    part_df['ЭВБ_ЭД_Уровень'] = base_df['Уровень_симптома_Эмоциональный_дефицит']

    part_df['ЭВБ_ЭО_Значение'] = base_df['Значение_симптома_Эмоциональная_отстраненность']
    part_df['ЭВБ_ЭО_Уровень'] = base_df['Уровень_симптома_Эмоциональная_отстраненность']

    part_df['ЭВБ_ЛО_Значение'] = base_df['Значение_симптома_Личностная_отстраненность']
    part_df['ЭВБ_ЛО_Уровень'] = base_df['Уровень_симптома_Личностная_отстраненность']

    part_df['ЭВБ_ППН_Значение'] = base_df['Значение_симптома_Психосоматические_и_психовегетативные_нарушения']
    part_df['ЭВБ_ППН_Уровень'] = base_df['Уровень_симптома_Психосоматические_и_психовегетативные_нарушения']

    base_df.sort_values(by='Итоговое_значение_эмоционального_выгорания', ascending=False, inplace=True)  # сортируем
    out_answer_df = pd.concat([out_answer_df, answers_df], axis=1)  # Датафрейм для проверки

    # Общий свод по уровням общей шкалы всего в процентном соотношении
    base_svod_all_df = pd.DataFrame(
        index=['0-99','100-149','150-199','200-249','250-299','300 и более'])

    svod_level_df = pd.pivot_table(base_df, index='Диапазон_эмоционального_выгорания',
                                   values='Итоговое_значение_эмоционального_выгорания',
                                   aggfunc='count')

    svod_level_df['% от общего'] = round(
        svod_level_df['Итоговое_значение_эмоционального_выгорания'] / svod_level_df[
            'Итоговое_значение_эмоционального_выгорания'].sum(), 3) * 100

    base_svod_all_df = base_svod_all_df.join(svod_level_df)

    # # Создаем суммирующую строку
    base_svod_all_df.loc['Итого'] = svod_level_df.sum()
    base_svod_all_df.reset_index(inplace=True)
    base_svod_all_df.rename(columns={'index': 'Уровень', 'Итоговое_значение_эмоционального_выгорания': 'Количество'},
                            inplace=True)
    # формируем основной словарь
    out_dct = {'Списочный результат': base_df, 'Список для проверки': out_answer_df,
               'Свод Общий': base_svod_all_df,
               }

    lst_level = ['0-99','100-149','150-199','200-249','250-299','300 и более']
    dct_level = dict()

    for level in lst_level:
        temp_df = base_df[base_df['Диапазон_эмоционального_выгорания'] == level]
        if temp_df.shape[0] != 0:
            dct_level[level] = temp_df

    out_dct.update(dct_level)

    lst_phase = ['фаза не сформировалась','фаза в стадии формирования','сформировавшаяся фаза']
    lst_simptom = ['не сложившийся симптом','складывающийся симптом','сложившийся симптом','доминирующий симптом']

    # Своды по фазам
    svod_stress = create_svod_sub(base_df, lst_phase, 'Уровень_фазы_Напряжение',
                                           'Значение_фазы_Напряжение', 'count')

    svod_resistance = create_svod_sub(base_df, lst_phase, 'Уровень_фазы_Резистенция',
                                           'Значение_фазы_Резистенция', 'count')

    svod_exhaustion = create_svod_sub(base_df, lst_phase, 'Уровень_фазы_Истощение',
                                           'Значение_фазы_Истощение', 'count')

    # Своды по симптомам
    # 1 фаза
    svod_ppo = create_svod_sub(base_df, lst_simptom, 'Уровень_симптома_Переживание_психотравмирующих_обстоятельств',
                                           'Значение_симптома_Переживание_психотравмирующих_обстоятельств', 'count')

    svod_ns = create_svod_sub(base_df, lst_simptom, 'Уровень_симптома_Неудовлетворенность_собой',
                                           'Значение_симптома_Неудовлетворенность_собой', 'count')

    svod_zk = create_svod_sub(base_df, lst_simptom, 'Уровень_симптома_Загнанность_в_клетку',
                                           'Значение_симптома_Загнанность_в_клетку', 'count')

    svod_td = create_svod_sub(base_df, lst_simptom, 'Уровень_симптома_Тревога_и_депрессия',
                                           'Значение_симптома_Тревога_и_депрессия', 'count')
    # 2 фаза
    svod_niar = create_svod_sub(base_df, lst_simptom, 'Уровень_симптома_Неадекватное_избирательное_эмоциональное_реагирование',
                                           'Значение_симптома_Неадекватное_избирательное_эмоциональное_реагирование', 'count')

    svod_and = create_svod_sub(base_df, lst_simptom, 'Уровень_симптома_Эмоционально_нравственная_дезориентация',
                                           'Значение_симптома_Эмоционально_нравственная_дезориентация', 'count')

    svod_rsaa = create_svod_sub(base_df, lst_simptom, 'Уровень_симптома_Расширение_сферы_экономии_эмоций',
                                           'Значение_симптома_Расширение_сферы_экономии_эмоций', 'count')

    svod_rpo = create_svod_sub(base_df, lst_simptom, 'Уровень_симптома_Редукция_профессиональных_обязанностей',
                                           'Значение_симптома_Редукция_профессиональных_обязанностей', 'count')
    # 3 фаза
    svod_ad = create_svod_sub(base_df, lst_simptom, 'Уровень_симптома_Эмоциональный_дефицит',
                                           'Значение_симптома_Эмоциональный_дефицит', 'count')

    svod_ao = create_svod_sub(base_df, lst_simptom, 'Уровень_симптома_Эмоциональная_отстраненность',
                                           'Значение_симптома_Эмоциональная_отстраненность', 'count')

    svod_lo = create_svod_sub(base_df, lst_simptom, 'Уровень_симптома_Личностная_отстраненность',
                                           'Значение_симптома_Личностная_отстраненность', 'count')

    svod_ppn = create_svod_sub(base_df, lst_simptom, 'Уровень_симптома_Психосоматические_и_психовегетативные_нарушения',
                                           'Значение_симптома_Психосоматические_и_психовегетативные_нарушения', 'count')

    # Считаем среднее
    avg_em = round(base_df['Итоговое_значение_эмоционального_выгорания'].mean(), 1) # общее
    # Фазы
    avg_stress = round(base_df['Значение_фазы_Напряжение'].mean(), 1)
    avg_resistance = round(base_df['Значение_фазы_Резистенция'].mean(), 1)
    avg_exhaustion = round(base_df['Значение_фазы_Истощение'].mean(), 1)

    # Симптомы
    avg_ppo = round(base_df['Значение_симптома_Переживание_психотравмирующих_обстоятельств'].mean(), 1)
    avg_ns = round(base_df['Значение_симптома_Неудовлетворенность_собой'].mean(), 1)
    avg_zk = round(base_df['Значение_симптома_Загнанность_в_клетку'].mean(), 1)
    avg_td = round(base_df['Значение_симптома_Тревога_и_депрессия'].mean(), 1)

    avg_niar = round(base_df['Значение_симптома_Неадекватное_избирательное_эмоциональное_реагирование'].mean(), 1)
    avg_and = round(base_df['Значение_симптома_Эмоционально_нравственная_дезориентация'].mean(), 1)
    avg_rsaa = round(base_df['Значение_симптома_Расширение_сферы_экономии_эмоций'].mean(), 1)
    avg_rpo = round(base_df['Значение_симптома_Редукция_профессиональных_обязанностей'].mean(), 1)

    avg_ad = round(base_df['Значение_симптома_Эмоциональный_дефицит'].mean(), 1)
    avg_ao = round(base_df['Значение_симптома_Эмоциональная_отстраненность'].mean(), 1)
    avg_lo = round(base_df['Значение_симптома_Личностная_отстраненность'].mean(), 1)
    avg_ppn = round(base_df['Значение_симптома_Психосоматические_и_психовегетативные_нарушения'].mean(), 1)

    avg_dct = {'Среднее значение эмоционального выгорания':avg_em,
               'Среднее значение фазы Напряжения': avg_stress,
               'Среднее значение фазы Резистенция': avg_resistance,
               'Среднее значение фазы Истощение': avg_exhaustion,

               'Среднее значение симптома Переживание психотравмирующих обстоятельств': avg_ppo,
               'Среднее значение симптома Неудовлетворенность собой': avg_ns,
               'Среднее значение симптома «Загнанность в клетку»': avg_zk,
               'Среднее значение симптома Тревога и депрессия': avg_td,

               'Среднее значение симптома Неадекватное избирательное эмоциональное реагирование': avg_niar,
               'Среднее значение симптома Эмоционально-нравственная дезориентация': avg_and,
               'Среднее значение симптома Расширение сферы экономии эмоций': avg_rsaa,
               'Среднее значение симптома Редукция профессиональных обязанностей': avg_rpo,

               'Среднее значение симптома Эмоциональный дефицит': avg_ad,
               'Среднее значение симптома Эмоциональная отстраненность': avg_ao,
               'Среднее значение симптома Личностная отстраненность (деперсонализация)': avg_lo,
               'Среднее значение симптома Психосоматические и психовегетативные нарушения': avg_ppn,
               }

    avg_df = pd.DataFrame.from_dict(avg_dct, orient='index')
    avg_df = avg_df.reset_index()
    avg_df.columns = ['Показатель', 'Среднее значение']

    out_dct.update({'Среднее по симптомам': avg_df,
                    'Свод Напряжение': svod_stress,
                    'Свод Резистенция': svod_resistance,
                    'Свод Истощение': svod_exhaustion,

                    'Свод ППО': svod_ppo,
                    'Свод НС': svod_ns,
                    'Свод ЗК': svod_zk,
                    'Свод ТД': svod_td,

                    'Свод НИЭР': svod_niar,
                    'Свод ЭНД': svod_and,
                    'Свод РСЭЭ': svod_rsaa,
                    'Свод РПО': svod_rpo,

                    'Свод ЭД': svod_ad,
                    'Свод ЭО': svod_ao,
                    'Свод ЛО': svod_lo,
                    'Свод ППН': svod_ppn
                    })

    """
            Сохраняем в зависимости от необходимости делать своды по определенным колонкам
            """
    if len(lst_svod_cols) == 0:
        return out_dct, part_df

    # elif len(lst_svod_cols) == 1:
    else:
        out_dct = create_result_beb(base_df,out_dct,lst_svod_cols)

        return out_dct,part_df


        # lst_reindex_main_level_cols = [lst_svod_cols[0],'0-99','100-149','150-199','200-249','250-299','300 и более',
        #                                'Итого']  # Основная шкала
        #
        # lst_reindex_phase_level_cols = [lst_svod_cols[0], 'фаза не сформировалась','фаза в стадии формирования','сформировавшаяся фаза',
        #                               'Итого']  # Фазы
        # lst_reindex_sub_level_cols = [lst_svod_cols[0], 'не сложившийся симптом','складывающийся симптом','сложившийся симптом','доминирующий симптом',
        #                               'Итого']  # Симптомы
        #
        # # основная шкала
        # svod_count_one_level_df = calc_count_main_level(base_df, lst_svod_cols,
        #                                                 'Итоговое_значение_эмоционального_выгорания',
        #                                                 'Диапазон_эмоционального_выгорания',
        #                                                 lst_reindex_main_level_cols)
        #
        #
        # # Фазы
        # svod_count_one_phase_stress_df = calc_count_level_phase(base_df, lst_svod_cols,
        #                                                                'Значение_фазы_Напряжение',
        #                                                                'Уровень_фазы_Напряжение',
        #                                                                lst_reindex_phase_level_cols)
        #
        # svod_count_one_phase_resistance_df = calc_count_level_phase(base_df, lst_svod_cols,
        #                                                                'Значение_фазы_Резистенция',
        #                                                                'Уровень_фазы_Резистенция',
        #                                                                lst_reindex_phase_level_cols)
        # svod_count_one_phase_exhaustion_df = calc_count_level_phase(base_df, lst_svod_cols,
        #                                                                'Значение_фазы_Истощение',
        #                                                                'Уровень_фазы_Истощение',
        #                                                                lst_reindex_phase_level_cols)
        #
        # # Симптомы
        # # 1 phase
        # svod_count_one_level_ppo_df = calc_count_level_sub(base_df, lst_svod_cols,
        #                                                                'Значение_симптома_Переживание_психотравмирующих_обстоятельств',
        #                                                                'Уровень_симптома_Переживание_психотравмирующих_обстоятельств',
        #                                                                lst_reindex_sub_level_cols)
        # svod_count_one_level_ns_df = calc_count_level_sub(base_df, lst_svod_cols,
        #                                                                'Значение_симптома_Неудовлетворенность_собой',
        #                                                                'Уровень_симптома_Неудовлетворенность_собой',
        #                                                                lst_reindex_sub_level_cols)
        # svod_count_one_level_zk_df = calc_count_level_sub(base_df, lst_svod_cols,
        #                                                                'Значение_симптома_Загнанность_в_клетку',
        #                                                                'Уровень_симптома_Загнанность_в_клетку',
        #                                                                lst_reindex_sub_level_cols)
        # svod_count_one_level_td_df = calc_count_level_sub(base_df, lst_svod_cols,
        #                                                                'Значение_симптома_Тревога_и_депрессия',
        #                                                                'Уровень_симптома_Тревога_и_депрессия',
        #                                                                lst_reindex_sub_level_cols)
        # # 2 phase
        # svod_count_one_level_niar_df = calc_count_level_sub(base_df, lst_svod_cols,
        #                                                                'Значение_симптома_Неадекватное_избирательное_эмоциональное_реагирование',
        #                                                                'Уровень_симптома_Неадекватное_избирательное_эмоциональное_реагирование',
        #                                                                lst_reindex_sub_level_cols)
        # svod_count_one_level_and_df = calc_count_level_sub(base_df, lst_svod_cols,
        #                                                                'Значение_симптома_Эмоционально_нравственная_дезориентация',
        #                                                                'Уровень_симптома_Эмоционально_нравственная_дезориентация',
        #                                                                lst_reindex_sub_level_cols)
        # svod_count_one_level_rsaa_df = calc_count_level_sub(base_df, lst_svod_cols,
        #                                                                'Значение_симптома_Расширение_сферы_экономии_эмоций',
        #                                                                'Уровень_симптома_Расширение_сферы_экономии_эмоций',
        #                                                                lst_reindex_sub_level_cols)
        # svod_count_one_level_rpo_df = calc_count_level_sub(base_df, lst_svod_cols,
        #                                                                'Значение_симптома_Редукция_профессиональных_обязанностей',
        #                                                                'Уровень_симптома_Редукция_профессиональных_обязанностей',
        #                                                                lst_reindex_sub_level_cols)
        # # 3 phase
        # svod_count_one_level_ad_df = calc_count_level_sub(base_df, lst_svod_cols,
        #                                                                'Значение_симптома_Эмоциональный_дефицит',
        #                                                                'Уровень_симптома_Эмоциональный_дефицит',
        #                                                                lst_reindex_sub_level_cols)
        # svod_count_one_level_ao_df = calc_count_level_sub(base_df, lst_svod_cols,
        #                                                                'Значение_симптома_Эмоциональная_отстраненность',
        #                                                                'Уровень_симптома_Эмоциональная_отстраненность',
        #                                                                lst_reindex_sub_level_cols)
        # svod_count_one_level_lo_df = calc_count_level_sub(base_df, lst_svod_cols,
        #                                                                'Значение_симптома_Личностная_отстраненность',
        #                                                                'Уровень_симптома_Личностная_отстраненность',
        #                                                                lst_reindex_sub_level_cols)
        # svod_count_one_level_ppn_df = calc_count_level_sub(base_df, lst_svod_cols,
        #                                                                'Значение_симптома_Психосоматические_и_психовегетативные_нарушения',
        #                                                                'Уровень_симптома_Психосоматические_и_психовегетативные_нарушения',
        #                                                                lst_reindex_sub_level_cols)
        #
        # # очищаем название колонки по которой делали свод
        # name_one = lst_svod_cols[0]
        # name_one = re.sub(r'[\[\]\'+()<> :"?*|\\/]', '_', name_one)
        # name_one = name_one[:15]
        #
        # # Считаем среднее по субшкалам
        # svod_mean_df = pd.pivot_table(base_df,
        #                               index=[lst_svod_cols[0]],
        #                               values=['Итоговое_значение_эмоционального_выгорания','Значение_фазы_Напряжение','Значение_фазы_Резистенция','Значение_фазы_Истощение',
        #                                       'Значение_симптома_Переживание_психотравмирующих_обстоятельств','Значение_симптома_Неудовлетворенность_собой','Значение_симптома_Загнанность_в_клетку','Значение_симптома_Тревога_и_депрессия',
        #                                       'Значение_симптома_Неадекватное_избирательное_эмоциональное_реагирование','Значение_симптома_Эмоционально_нравственная_дезориентация','Значение_симптома_Расширение_сферы_экономии_эмоций','Значение_симптома_Редукция_профессиональных_обязанностей',
        #                                       'Значение_симптома_Эмоциональный_дефицит','Значение_симптома_Эмоциональная_отстраненность','Значение_симптома_Личностная_отстраненность','Значение_симптома_Психосоматические_и_психовегетативные_нарушения'
        #                                       ],
        #                               aggfunc=round_mean)
        # svod_mean_df.reset_index(inplace=True)
        # # упорядочиваем колонки
        # new_order_cols = lst_svod_cols.copy()
        # new_order_cols.extend(['Итоговое_значение_эмоционального_выгорания','Значение_фазы_Напряжение','Значение_фазы_Резистенция','Значение_фазы_Истощение',
        #                                       'Значение_симптома_Переживание_психотравмирующих_обстоятельств','Значение_симптома_Неудовлетворенность_собой','Значение_симптома_Загнанность_в_клетку','Значение_симптома_Тревога_и_депрессия',
        #                                       'Значение_симптома_Неадекватное_избирательное_эмоциональное_реагирование','Значение_симптома_Эмоционально_нравственная_дезориентация','Значение_симптома_Расширение_сферы_экономии_эмоций','Значение_симптома_Редукция_профессиональных_обязанностей',
        #                                       'Значение_симптома_Эмоциональный_дефицит','Значение_симптома_Эмоциональная_отстраненность','Значение_симптома_Личностная_отстраненность','Значение_симптома_Психосоматические_и_психовегетативные_нарушения'])
        # svod_mean_df = svod_mean_df.reindex(columns=new_order_cols)
        # dct_rename_cols_mean = {'Итоговое_значение_эмоционального_выгорания':'Ср. эмоционального выгорания',
        #                         'Значение_фазы_Напряжение':'Ср. фазы Напряжение','Значение_фазы_Резистенция':'Ср. фазы Резистенция','Значение_фазы_Истощение':'Ср. фазы Истощение',
        #                                       'Значение_симптома_Переживание_психотравмирующих_обстоятельств':'Ср. ППО','Значение_симптома_Неудовлетворенность_собой':'Ср. НС',
        #                         'Значение_симптома_Загнанность_в_клетку':'Ср. ЗК','Значение_симптома_Тревога_и_депрессия':'Ср. ТД',
        #
        #                                       'Значение_симптома_Неадекватное_избирательное_эмоциональное_реагирование':'Ср. НИЭР','Значение_симптома_Эмоционально_нравственная_дезориентация':'Ср. ЭНД',
        #                         'Значение_симптома_Расширение_сферы_экономии_эмоций':'Ср. РСЭЭ','Значение_симптома_Редукция_профессиональных_обязанностей':'Ср. РПО',
        #
        #                                       'Значение_симптома_Эмоциональный_дефицит':'Ср. ЭД','Значение_симптома_Эмоциональная_отстраненность':'Ср. ЭО',
        #                         'Значение_симптома_Личностная_отстраненность':'Ср. ЛО','Значение_симптома_Психосоматические_и_психовегетативные_нарушения':'Ср. ППН'}
        # svod_mean_df.rename(columns=dct_rename_cols_mean,inplace=True)
        #
        #
        # out_dct.update({f'Свод {name_one}': svod_count_one_level_df,
        #                 f'Ср. {name_one}': svod_mean_df,
        #                 f'Свод Напряжение {name_one[:10]}': svod_count_one_phase_stress_df,
        #                 f'Свод Резистенция {name_one[:10]}': svod_count_one_phase_resistance_df,
        #                 f'Свод Истощение {name_one[:10]}': svod_count_one_phase_exhaustion_df,
        #
        #
        #                 f'Свод ППО {name_one}': svod_count_one_level_ppo_df,
        #                 f'Свод НС {name_one}': svod_count_one_level_ns_df,
        #                 f'Свод ЗК {name_one}': svod_count_one_level_zk_df,
        #                 f'Свод ТД {name_one}': svod_count_one_level_td_df,
        #
        #                 f'Свод НИЭР {name_one}': svod_count_one_level_niar_df,
        #                 f'Свод ЭНД {name_one}': svod_count_one_level_and_df,
        #                 f'Свод РСЭЭ {name_one}': svod_count_one_level_rsaa_df,
        #                 f'Свод РПО {name_one}': svod_count_one_level_rpo_df,
        #
        #                 f'Свод ЭД {name_one}': svod_count_one_level_ad_df,
        #                 f'Свод ЭО {name_one}': svod_count_one_level_ao_df,
        #                 f'Свод ЛО {name_one}': svod_count_one_level_lo_df,
        #                 f'Свод ППН {name_one}': svod_count_one_level_ppn_df,
        #
        #                 })
        #
        # return out_dct, part_df


    # elif len(lst_svod_cols) == 2:
        # 2 колонки


        # lst_reindex_main_level_cols = [lst_svod_cols[0], lst_svod_cols[1], '0-99','100-149','150-199','200-249','250-299','300 и более', 'Итого']  # Основная шкала
        # lst_reindex_main_phase_level_cols = [lst_svod_cols[0], lst_svod_cols[1], 'фаза не сформировалась','фаза в стадии формирования','сформировавшаяся фаза', 'Итого']  # Фазы
        # lst_reindex_main_sub_level_cols = [lst_svod_cols[0], lst_svod_cols[1], 'не сложившийся симптом','складывающийся симптом','сложившийся симптом','доминирующий симптом', 'Итого']  # Субшкалы
        #
        # # 1 колонка
        # lst_reindex_first_level_cols = [lst_svod_cols[0], '0-99','100-149','150-199','200-249','250-299','300 и более', 'Итого']  # Основная шкала
        # lst_reindex_first_phase_level_cols = [lst_svod_cols[0], 'фаза не сформировалась','фаза в стадии формирования','сформировавшаяся фаза', 'Итого']  # Фазы
        # lst_reindex_first_sub_level_cols = [lst_svod_cols[0], 'не сложившийся симптом','складывающийся симптом','сложившийся симптом','доминирующий симптом', 'Итого']  # Субшкалы
        #
        # # 2 колонка
        # lst_reindex_second_level_cols = [lst_svod_cols[1], '0-99','100-149','150-199','200-249','250-299','300 и более', 'Итого']  # Основная шкала
        # lst_reindex_second_phase_level_cols = [lst_svod_cols[1], 'фаза не сформировалась','фаза в стадии формирования','сформировавшаяся фаза', 'Итого']  # Фазы
        # lst_reindex_second_sub_level_cols = [lst_svod_cols[1], 'не сложившийся симптом','складывающийся симптом','сложившийся симптом','доминирующий симптом', 'Итого']  # Субшкалы
        #
        # # основная шкала
        # svod_count_two_level_df = calc_count_main_level(base_df, lst_svod_cols,
        #                                                 'Итоговое_значение_эмоционального_выгорания',
        #                                                 'Диапазон_эмоционального_выгорания',
        #                                                 lst_reindex_main_level_cols)
        #
        # # Фазы
        # svod_count_two_phase_stress_df = calc_count_level_phase(base_df, lst_svod_cols,
        #                                                         'Значение_фазы_Напряжение',
        #                                                         'Уровень_фазы_Напряжение',
        #                                                         lst_reindex_main_phase_level_cols)
        #
        # svod_count_two_phase_resistance_df = calc_count_level_phase(base_df, lst_svod_cols,
        #                                                             'Значение_фазы_Резистенция',
        #                                                             'Уровень_фазы_Резистенция',
        #                                                             lst_reindex_main_phase_level_cols)
        # svod_count_two_phase_exhaustion_df = calc_count_level_phase(base_df, lst_svod_cols,
        #                                                             'Значение_фазы_Истощение',
        #                                                             'Уровень_фазы_Истощение',
        #                                                             lst_reindex_main_phase_level_cols)
        #
        # # Симптомы
        # # 1 phase
        # svod_count_two_level_ppo_df = calc_count_level_sub(base_df, lst_svod_cols,
        #                                                    'Значение_симптома_Переживание_психотравмирующих_обстоятельств',
        #                                                    'Уровень_симптома_Переживание_психотравмирующих_обстоятельств',
        #                                                    lst_reindex_main_sub_level_cols)
        # svod_count_two_level_ns_df = calc_count_level_sub(base_df, lst_svod_cols,
        #                                                   'Значение_симптома_Неудовлетворенность_собой',
        #                                                   'Уровень_симптома_Неудовлетворенность_собой',
        #                                                   lst_reindex_main_sub_level_cols)
        # svod_count_two_level_zk_df = calc_count_level_sub(base_df, lst_svod_cols,
        #                                                   'Значение_симптома_Загнанность_в_клетку',
        #                                                   'Уровень_симптома_Загнанность_в_клетку',
        #                                                   lst_reindex_main_sub_level_cols)
        # svod_count_two_level_td_df = calc_count_level_sub(base_df, lst_svod_cols,
        #                                                   'Значение_симптома_Тревога_и_депрессия',
        #                                                   'Уровень_симптома_Тревога_и_депрессия',
        #                                                   lst_reindex_main_sub_level_cols)
        # # 2 phase
        # svod_count_two_level_niar_df = calc_count_level_sub(base_df, lst_svod_cols,
        #                                                     'Значение_симптома_Неадекватное_избирательное_эмоциональное_реагирование',
        #                                                     'Уровень_симптома_Неадекватное_избирательное_эмоциональное_реагирование',
        #                                                     lst_reindex_main_sub_level_cols)
        # svod_count_two_level_and_df = calc_count_level_sub(base_df, lst_svod_cols,
        #                                                    'Значение_симптома_Эмоционально_нравственная_дезориентация',
        #                                                    'Уровень_симптома_Эмоционально_нравственная_дезориентация',
        #                                                    lst_reindex_main_sub_level_cols)
        # svod_count_two_level_rsaa_df = calc_count_level_sub(base_df, lst_svod_cols,
        #                                                     'Значение_симптома_Расширение_сферы_экономии_эмоций',
        #                                                     'Уровень_симптома_Расширение_сферы_экономии_эмоций',
        #                                                     lst_reindex_main_sub_level_cols)
        # svod_count_two_level_rpo_df = calc_count_level_sub(base_df, lst_svod_cols,
        #                                                    'Значение_симптома_Редукция_профессиональных_обязанностей',
        #                                                    'Уровень_симптома_Редукция_профессиональных_обязанностей',
        #                                                    lst_reindex_main_sub_level_cols)
        # # 3 phase
        # svod_count_two_level_ad_df = calc_count_level_sub(base_df, lst_svod_cols,
        #                                                   'Значение_симптома_Эмоциональный_дефицит',
        #                                                   'Уровень_симптома_Эмоциональный_дефицит',
        #                                                   lst_reindex_main_sub_level_cols)
        # svod_count_two_level_ao_df = calc_count_level_sub(base_df, lst_svod_cols,
        #                                                   'Значение_симптома_Эмоциональная_отстраненность',
        #                                                   'Уровень_симптома_Эмоциональная_отстраненность',
        #                                                   lst_reindex_main_sub_level_cols)
        # svod_count_two_level_lo_df = calc_count_level_sub(base_df, lst_svod_cols,
        #                                                   'Значение_симптома_Личностная_отстраненность',
        #                                                   'Уровень_симптома_Личностная_отстраненность',
        #                                                   lst_reindex_main_sub_level_cols)
        # svod_count_two_level_ppn_df = calc_count_level_sub(base_df, lst_svod_cols,
        #                                                    'Значение_симптома_Психосоматические_и_психовегетативные_нарушения',
        #                                                    'Уровень_симптома_Психосоматические_и_психовегетативные_нарушения',
        #                                                    lst_reindex_main_sub_level_cols)
        #
        # # очищаем название колонки по которой делали свод
        # name_one = lst_svod_cols[0]
        # name_one = re.sub(r'[\[\]\'+()<> :"?*|\\/]', '_', name_one)
        # name_one = name_one[:15]
        #
        # name_two = lst_svod_cols[1]
        # name_two = re.sub(r'[\[\]\'+()<> :"?*|\\/]', '_', name_two)
        # name_two = name_two[:15]
        # # Считаем среднее по субшкалам
        # svod_mean_df = pd.pivot_table(base_df,
        #                               index=lst_svod_cols,
        #                               values=['Итоговое_значение_эмоционального_выгорания', 'Значение_фазы_Напряжение',
        #                                       'Значение_фазы_Резистенция', 'Значение_фазы_Истощение',
        #                                       'Значение_симптома_Переживание_психотравмирующих_обстоятельств',
        #                                       'Значение_симптома_Неудовлетворенность_собой',
        #                                       'Значение_симптома_Загнанность_в_клетку',
        #                                       'Значение_симптома_Тревога_и_депрессия',
        #                                       'Значение_симптома_Неадекватное_избирательное_эмоциональное_реагирование',
        #                                       'Значение_симптома_Эмоционально_нравственная_дезориентация',
        #                                       'Значение_симптома_Расширение_сферы_экономии_эмоций',
        #                                       'Значение_симптома_Редукция_профессиональных_обязанностей',
        #                                       'Значение_симптома_Эмоциональный_дефицит',
        #                                       'Значение_симптома_Эмоциональная_отстраненность',
        #                                       'Значение_симптома_Личностная_отстраненность',
        #                                       'Значение_симптома_Психосоматические_и_психовегетативные_нарушения'
        #                                       ],
        #                               aggfunc=round_mean)
        # svod_mean_df.reset_index(inplace=True)
        # # упорядочиваем колонки
        # new_order_cols = lst_svod_cols.copy()
        # new_order_cols.extend(
        #     ['Итоговое_значение_эмоционального_выгорания', 'Значение_фазы_Напряжение', 'Значение_фазы_Резистенция',
        #      'Значение_фазы_Истощение',
        #      'Значение_симптома_Переживание_психотравмирующих_обстоятельств',
        #      'Значение_симптома_Неудовлетворенность_собой',
        #      'Значение_симптома_Загнанность_в_клетку', 'Значение_симптома_Тревога_и_депрессия',
        #      'Значение_симптома_Неадекватное_избирательное_эмоциональное_реагирование',
        #      'Значение_симптома_Эмоционально_нравственная_дезориентация',
        #      'Значение_симптома_Расширение_сферы_экономии_эмоций',
        #      'Значение_симптома_Редукция_профессиональных_обязанностей',
        #      'Значение_симптома_Эмоциональный_дефицит', 'Значение_симптома_Эмоциональная_отстраненность',
        #      'Значение_симптома_Личностная_отстраненность',
        #      'Значение_симптома_Психосоматические_и_психовегетативные_нарушения'])
        # svod_mean_df = svod_mean_df.reindex(columns=new_order_cols)
        # dct_rename_cols_mean = {'Итоговое_значение_эмоционального_выгорания': 'Ср. эмоционального выгорания',
        #                         'Значение_фазы_Напряжение': 'Ср. фазы Напряжение',
        #                         'Значение_фазы_Резистенция': 'Ср. фазы Резистенция',
        #                         'Значение_фазы_Истощение': 'Ср. фазы Истощение',
        #                         'Значение_симптома_Переживание_психотравмирующих_обстоятельств': 'Ср. ППО',
        #                         'Значение_симптома_Неудовлетворенность_собой': 'Ср. НС',
        #                         'Значение_симптома_Загнанность_в_клетку': 'Ср. ЗК',
        #                         'Значение_симптома_Тревога_и_депрессия': 'Ср. ТД',
        #
        #                         'Значение_симптома_Неадекватное_избирательное_эмоциональное_реагирование': 'Ср. НИЭР',
        #                         'Значение_симптома_Эмоционально_нравственная_дезориентация': 'Ср. ЭНД',
        #                         'Значение_симптома_Расширение_сферы_экономии_эмоций': 'Ср. РСЭЭ',
        #                         'Значение_симптома_Редукция_профессиональных_обязанностей': 'Ср. РПО',
        #
        #                         'Значение_симптома_Эмоциональный_дефицит': 'Ср. ЭД',
        #                         'Значение_симптома_Эмоциональная_отстраненность': 'Ср. ЭО',
        #                         'Значение_симптома_Личностная_отстраненность': 'Ср. ЛО',
        #                         'Значение_симптома_Психосоматические_и_психовегетативные_нарушения': 'Ср. ППН'}
        # svod_mean_df.rename(columns=dct_rename_cols_mean, inplace=True)
        #
        #
        # """
        # По колонке один
        # """
        # # основная шкала
        # svod_count_first_level_df = calc_count_main_level(base_df, [lst_svod_cols[0]],
        #                                                   'Итоговое_значение_эмоционального_выгорания',
        #                                                   'Диапазон_эмоционального_выгорания',
        #                                                   lst_reindex_first_level_cols)
        #
        # # Фазы
        # svod_count_first_phase_stress_df = calc_count_level_phase(base_df, [lst_svod_cols[0]],
        #                                                           'Значение_фазы_Напряжение',
        #                                                           'Уровень_фазы_Напряжение',
        #                                                           lst_reindex_first_phase_level_cols)
        #
        # svod_count_first_phase_resistance_df = calc_count_level_phase(base_df, [lst_svod_cols[0]],
        #                                                               'Значение_фазы_Резистенция',
        #                                                               'Уровень_фазы_Резистенция',
        #                                                               lst_reindex_first_phase_level_cols)
        # svod_count_first_phase_exhaustion_df = calc_count_level_phase(base_df, [lst_svod_cols[0]],
        #                                                               'Значение_фазы_Истощение',
        #                                                               'Уровень_фазы_Истощение',
        #                                                               lst_reindex_first_phase_level_cols)
        #
        # # Симптомы
        # # 1 phase
        # svod_count_first_level_ppo_df = calc_count_level_sub(base_df, [lst_svod_cols[0]],
        #                                                      'Значение_симптома_Переживание_психотравмирующих_обстоятельств',
        #                                                      'Уровень_симптома_Переживание_психотравмирующих_обстоятельств',
        #                                                      lst_reindex_first_sub_level_cols)
        # svod_count_first_level_ns_df = calc_count_level_sub(base_df, [lst_svod_cols[0]],
        #                                                     'Значение_симптома_Неудовлетворенность_собой',
        #                                                     'Уровень_симптома_Неудовлетворенность_собой',
        #                                                     lst_reindex_first_sub_level_cols)
        # svod_count_first_level_zk_df = calc_count_level_sub(base_df, [lst_svod_cols[0]],
        #                                                     'Значение_симптома_Загнанность_в_клетку',
        #                                                     'Уровень_симптома_Загнанность_в_клетку',
        #                                                     lst_reindex_first_sub_level_cols)
        # svod_count_first_level_td_df = calc_count_level_sub(base_df, [lst_svod_cols[0]],
        #                                                     'Значение_симптома_Тревога_и_депрессия',
        #                                                     'Уровень_симптома_Тревога_и_депрессия',
        #                                                     lst_reindex_first_sub_level_cols)
        # # 2 phase
        # svod_count_first_level_niar_df = calc_count_level_sub(base_df, [lst_svod_cols[0]],
        #                                                       'Значение_симптома_Неадекватное_избирательное_эмоциональное_реагирование',
        #                                                       'Уровень_симптома_Неадекватное_избирательное_эмоциональное_реагирование',
        #                                                       lst_reindex_first_sub_level_cols)
        # svod_count_first_level_and_df = calc_count_level_sub(base_df, [lst_svod_cols[0]],
        #                                                      'Значение_симптома_Эмоционально_нравственная_дезориентация',
        #                                                      'Уровень_симптома_Эмоционально_нравственная_дезориентация',
        #                                                      lst_reindex_first_sub_level_cols)
        # svod_count_first_level_rsaa_df = calc_count_level_sub(base_df, [lst_svod_cols[0]],
        #                                                       'Значение_симптома_Расширение_сферы_экономии_эмоций',
        #                                                       'Уровень_симптома_Расширение_сферы_экономии_эмоций',
        #                                                       lst_reindex_first_sub_level_cols)
        # svod_count_first_level_rpo_df = calc_count_level_sub(base_df, [lst_svod_cols[0]],
        #                                                      'Значение_симптома_Редукция_профессиональных_обязанностей',
        #                                                      'Уровень_симптома_Редукция_профессиональных_обязанностей',
        #                                                      lst_reindex_first_sub_level_cols)
        # # 3 phase
        # svod_count_first_level_ad_df = calc_count_level_sub(base_df, [lst_svod_cols[0]],
        #                                                     'Значение_симптома_Эмоциональный_дефицит',
        #                                                     'Уровень_симптома_Эмоциональный_дефицит',
        #                                                     lst_reindex_first_sub_level_cols)
        # svod_count_first_level_ao_df = calc_count_level_sub(base_df, [lst_svod_cols[0]],
        #                                                     'Значение_симптома_Эмоциональная_отстраненность',
        #                                                     'Уровень_симптома_Эмоциональная_отстраненность',
        #                                                     lst_reindex_first_sub_level_cols)
        # svod_count_first_level_lo_df = calc_count_level_sub(base_df, [lst_svod_cols[0]],
        #                                                     'Значение_симптома_Личностная_отстраненность',
        #                                                     'Уровень_симптома_Личностная_отстраненность',
        #                                                     lst_reindex_first_sub_level_cols)
        # svod_count_first_level_ppn_df = calc_count_level_sub(base_df, [lst_svod_cols[0]],
        #                                                      'Значение_симптома_Психосоматические_и_психовегетативные_нарушения',
        #                                                      'Уровень_симптома_Психосоматические_и_психовегетативные_нарушения',
        #                                                      lst_reindex_first_sub_level_cols)
        #
        #
        # # Считаем среднее по субшкалам
        # svod_mean_first_df = pd.pivot_table(base_df,
        #                                     index=[[lst_svod_cols[0]],
        #                                     values=['Итоговое_значение_эмоционального_выгорания',
        #                                             'Значение_фазы_Напряжение',
        #                                             'Значение_фазы_Резистенция', 'Значение_фазы_Истощение',
        #                                             'Значение_симптома_Переживание_психотравмирующих_обстоятельств',
        #                                             'Значение_симптома_Неудовлетворенность_собой',
        #                                             'Значение_симптома_Загнанность_в_клетку',
        #                                             'Значение_симптома_Тревога_и_депрессия',
        #                                             'Значение_симптома_Неадекватное_избирательное_эмоциональное_реагирование',
        #                                             'Значение_симптома_Эмоционально_нравственная_дезориентация',
        #                                             'Значение_симптома_Расширение_сферы_экономии_эмоций',
        #                                             'Значение_симптома_Редукция_профессиональных_обязанностей',
        #                                             'Значение_симптома_Эмоциональный_дефицит',
        #                                             'Значение_симптома_Эмоциональная_отстраненность',
        #                                             'Значение_симптома_Личностная_отстраненность',
        #                                             'Значение_симптома_Психосоматические_и_психовегетативные_нарушения'
        #                                             ],
        #                                     aggfunc=round_mean)
        # svod_mean_first_df.reset_index(inplace=True)
        # # упорядочиваем колонки
        # new_order_cols = [lst_svod_cols[0]].copy()
        # new_order_cols.extend(
        #     ['Итоговое_значение_эмоционального_выгорания', 'Значение_фазы_Напряжение', 'Значение_фазы_Резистенция',
        #      'Значение_фазы_Истощение',
        #      'Значение_симптома_Переживание_психотравмирующих_обстоятельств',
        #      'Значение_симптома_Неудовлетворенность_собой',
        #      'Значение_симптома_Загнанность_в_клетку', 'Значение_симптома_Тревога_и_депрессия',
        #      'Значение_симптома_Неадекватное_избирательное_эмоциональное_реагирование',
        #      'Значение_симптома_Эмоционально_нравственная_дезориентация',
        #      'Значение_симптома_Расширение_сферы_экономии_эмоций',
        #      'Значение_симптома_Редукция_профессиональных_обязанностей',
        #      'Значение_симптома_Эмоциональный_дефицит', 'Значение_симптома_Эмоциональная_отстраненность',
        #      'Значение_симптома_Личностная_отстраненность',
        #      'Значение_симптома_Психосоматические_и_психовегетативные_нарушения'])
        # svod_mean_first_df = svod_mean_first_df.reindex(columns=new_order_cols)
        # dct_rename_cols_mean = {'Итоговое_значение_эмоционального_выгорания': 'Ср. эмоционального выгорания',
        #                         'Значение_фазы_Напряжение': 'Ср. фазы Напряжение',
        #                         'Значение_фазы_Резистенция': 'Ср. фазы Резистенция',
        #                         'Значение_фазы_Истощение': 'Ср. фазы Истощение',
        #                         'Значение_симптома_Переживание_психотравмирующих_обстоятельств': 'Ср. ППО',
        #                         'Значение_симптома_Неудовлетворенность_собой': 'Ср. НС',
        #                         'Значение_симптома_Загнанность_в_клетку': 'Ср. ЗК',
        #                         'Значение_симптома_Тревога_и_депрессия': 'Ср. ТД',
        #
        #                         'Значение_симптома_Неадекватное_избирательное_эмоциональное_реагирование': 'Ср. НИЭР',
        #                         'Значение_симптома_Эмоционально_нравственная_дезориентация': 'Ср. ЭНД',
        #                         'Значение_симптома_Расширение_сферы_экономии_эмоций': 'Ср. РСЭЭ',
        #                         'Значение_симптома_Редукция_профессиональных_обязанностей': 'Ср. РПО',
        #
        #                         'Значение_симптома_Эмоциональный_дефицит': 'Ср. ЭД',
        #                         'Значение_симптома_Эмоциональная_отстраненность': 'Ср. ЭО',
        #                         'Значение_симптома_Личностная_отстраненность': 'Ср. ЛО',
        #                         'Значение_симптома_Психосоматические_и_психовегетативные_нарушения': 'Ср. ППН'}
        # svod_mean_first_df.rename(columns=dct_rename_cols_mean, inplace=True)
        #
        # """
        # вторая колонка
        # """
        # # основная шкала
        # svod_count_second_level_df = calc_count_main_level(base_df, [lst_svod_cols[1]],
        #                                                    'Итоговое_значение_эмоционального_выгорания',
        #                                                    'Диапазон_эмоционального_выгорания',
        #                                                    lst_reindex_second_level_cols)
        #
        # # Фазы
        # svod_count_second_phase_stress_df = calc_count_level_phase(base_df, [lst_svod_cols[1]],
        #                                                            'Значение_фазы_Напряжение',
        #                                                            'Уровень_фазы_Напряжение',
        #                                                            lst_reindex_second_phase_level_cols)
        #
        # svod_count_second_phase_resistance_df = calc_count_level_phase(base_df, [lst_svod_cols[1]],
        #                                                                'Значение_фазы_Резистенция',
        #                                                                'Уровень_фазы_Резистенция',
        #                                                                lst_reindex_second_phase_level_cols)
        # svod_count_second_phase_exhaustion_df = calc_count_level_phase(base_df, [lst_svod_cols[1]],
        #                                                                'Значение_фазы_Истощение',
        #                                                                'Уровень_фазы_Истощение',
        #                                                                lst_reindex_second_phase_level_cols)
        #
        # # Симптомы
        # # 1 phase
        # svod_count_second_level_ppo_df = calc_count_level_sub(base_df, [lst_svod_cols[1]],
        #                                                       'Значение_симптома_Переживание_психотравмирующих_обстоятельств',
        #                                                       'Уровень_симптома_Переживание_психотравмирующих_обстоятельств',
        #                                                       lst_reindex_second_sub_level_cols)
        # svod_count_second_level_ns_df = calc_count_level_sub(base_df, [lst_svod_cols[1]],
        #                                                      'Значение_симптома_Неудовлетворенность_собой',
        #                                                      'Уровень_симптома_Неудовлетворенность_собой',
        #                                                      lst_reindex_second_sub_level_cols)
        # svod_count_second_level_zk_df = calc_count_level_sub(base_df, [lst_svod_cols[1]],
        #                                                      'Значение_симптома_Загнанность_в_клетку',
        #                                                      'Уровень_симптома_Загнанность_в_клетку',
        #                                                      lst_reindex_second_sub_level_cols)
        # svod_count_second_level_td_df = calc_count_level_sub(base_df, [lst_svod_cols[1]],
        #                                                      'Значение_симптома_Тревога_и_депрессия',
        #                                                      'Уровень_симптома_Тревога_и_депрессия',
        #                                                      lst_reindex_second_sub_level_cols)
        # # 2 phase
        # svod_count_second_level_niar_df = calc_count_level_sub(base_df, [lst_svod_cols[1]],
        #                                                        'Значение_симптома_Неадекватное_избирательное_эмоциональное_реагирование',
        #                                                        'Уровень_симптома_Неадекватное_избирательное_эмоциональное_реагирование',
        #                                                        lst_reindex_second_sub_level_cols)
        # svod_count_second_level_and_df = calc_count_level_sub(base_df, [lst_svod_cols[1]],
        #                                                       'Значение_симптома_Эмоционально_нравственная_дезориентация',
        #                                                       'Уровень_симптома_Эмоционально_нравственная_дезориентация',
        #                                                       lst_reindex_second_sub_level_cols)
        # svod_count_second_level_rsaa_df = calc_count_level_sub(base_df, [lst_svod_cols[1]],
        #                                                        'Значение_симптома_Расширение_сферы_экономии_эмоций',
        #                                                        'Уровень_симптома_Расширение_сферы_экономии_эмоций',
        #                                                        lst_reindex_second_sub_level_cols)
        # svod_count_second_level_rpo_df = calc_count_level_sub(base_df, [lst_svod_cols[1]],
        #                                                       'Значение_симптома_Редукция_профессиональных_обязанностей',
        #                                                       'Уровень_симптома_Редукция_профессиональных_обязанностей',
        #                                                       lst_reindex_second_sub_level_cols)
        # # 3 phase
        # svod_count_second_level_ad_df = calc_count_level_sub(base_df, [lst_svod_cols[1]],
        #                                                      'Значение_симптома_Эмоциональный_дефицит',
        #                                                      'Уровень_симптома_Эмоциональный_дефицит',
        #                                                      lst_reindex_second_sub_level_cols)
        # svod_count_second_level_ao_df = calc_count_level_sub(base_df, [lst_svod_cols[1]],
        #                                                      'Значение_симптома_Эмоциональная_отстраненность',
        #                                                      'Уровень_симптома_Эмоциональная_отстраненность',
        #                                                      lst_reindex_second_sub_level_cols)
        # svod_count_second_level_lo_df = calc_count_level_sub(base_df, [lst_svod_cols[1]],
        #                                                      'Значение_симптома_Личностная_отстраненность',
        #                                                      'Уровень_симптома_Личностная_отстраненность',
        #                                                      lst_reindex_second_sub_level_cols)
        # svod_count_second_level_ppn_df = calc_count_level_sub(base_df, [lst_svod_cols[1]],
        #                                                       'Значение_симптома_Психосоматические_и_психовегетативные_нарушения',
        #                                                       'Уровень_симптома_Психосоматические_и_психовегетативные_нарушения',
        #                                                       lst_reindex_second_sub_level_cols)
        #
        # # Считаем среднее по субшкалам
        # svod_mean_second_df = pd.pivot_table(base_df,
        #                                      index=[[lst_svod_cols[1]],
        #                                      values=['Итоговое_значение_эмоционального_выгорания',
        #                                              'Значение_фазы_Напряжение',
        #                                              'Значение_фазы_Резистенция', 'Значение_фазы_Истощение',
        #                                              'Значение_симптома_Переживание_психотравмирующих_обстоятельств',
        #                                              'Значение_симптома_Неудовлетворенность_собой',
        #                                              'Значение_симптома_Загнанность_в_клетку',
        #                                              'Значение_симптома_Тревога_и_депрессия',
        #                                              'Значение_симптома_Неадекватное_избирательное_эмоциональное_реагирование',
        #                                              'Значение_симптома_Эмоционально_нравственная_дезориентация',
        #                                              'Значение_симптома_Расширение_сферы_экономии_эмоций',
        #                                              'Значение_симптома_Редукция_профессиональных_обязанностей',
        #                                              'Значение_симптома_Эмоциональный_дефицит',
        #                                              'Значение_симптома_Эмоциональная_отстраненность',
        #                                              'Значение_симптома_Личностная_отстраненность',
        #                                              'Значение_симптома_Психосоматические_и_психовегетативные_нарушения'
        #                                              ],
        #                                      aggfunc=round_mean)
        # svod_mean_second_df.reset_index(inplace=True)
        # # упорядочиваем колонки
        # new_order_cols = [lst_svod_cols[1]].copy()
        # new_order_cols.extend(
        #     ['Итоговое_значение_эмоционального_выгорания', 'Значение_фазы_Напряжение', 'Значение_фазы_Резистенция',
        #      'Значение_фазы_Истощение',
        #      'Значение_симптома_Переживание_психотравмирующих_обстоятельств',
        #      'Значение_симптома_Неудовлетворенность_собой',
        #      'Значение_симптома_Загнанность_в_клетку', 'Значение_симптома_Тревога_и_депрессия',
        #      'Значение_симптома_Неадекватное_избирательное_эмоциональное_реагирование',
        #      'Значение_симптома_Эмоционально_нравственная_дезориентация',
        #      'Значение_симптома_Расширение_сферы_экономии_эмоций',
        #      'Значение_симптома_Редукция_профессиональных_обязанностей',
        #      'Значение_симптома_Эмоциональный_дефицит', 'Значение_симптома_Эмоциональная_отстраненность',
        #      'Значение_симптома_Личностная_отстраненность',
        #      'Значение_симптома_Психосоматические_и_психовегетативные_нарушения'])
        # svod_mean_second_df = svod_mean_second_df.reindex(columns=new_order_cols)
        # dct_rename_cols_mean = {'Итоговое_значение_эмоционального_выгорания': 'Ср. эмоционального выгорания',
        #                         'Значение_фазы_Напряжение': 'Ср. фазы Напряжение',
        #                         'Значение_фазы_Резистенция': 'Ср. фазы Резистенция',
        #                         'Значение_фазы_Истощение': 'Ср. фазы Истощение',
        #                         'Значение_симптома_Переживание_психотравмирующих_обстоятельств': 'Ср. ППО',
        #                         'Значение_симптома_Неудовлетворенность_собой': 'Ср. НС',
        #                         'Значение_симптома_Загнанность_в_клетку': 'Ср. ЗК',
        #                         'Значение_симптома_Тревога_и_депрессия': 'Ср. ТД',
        #
        #                         'Значение_симптома_Неадекватное_избирательное_эмоциональное_реагирование': 'Ср. НИЭР',
        #                         'Значение_симптома_Эмоционально_нравственная_дезориентация': 'Ср. ЭНД',
        #                         'Значение_симптома_Расширение_сферы_экономии_эмоций': 'Ср. РСЭЭ',
        #                         'Значение_симптома_Редукция_профессиональных_обязанностей': 'Ср. РПО',
        #
        #                         'Значение_симптома_Эмоциональный_дефицит': 'Ср. ЭД',
        #                         'Значение_симптома_Эмоциональная_отстраненность': 'Ср. ЭО',
        #                         'Значение_симптома_Личностная_отстраненность': 'Ср. ЛО',
        #                         'Значение_симптома_Психосоматические_и_психовегетативные_нарушения': 'Ср. ППН'}
        # svod_mean_second_df.rename(columns=dct_rename_cols_mean, inplace=True)
        #
        #
        #
        #
        #
        #
        # out_dct.update({f'Свод {name_one[:10]}_{name_two[:10]}': svod_count_two_level_df,
        #                 f'Ср. {name_one[:10]}_{name_two[:10]}': svod_mean_df,
        #                 f'Свод Напряжение {name_one[:10]}_{name_two[:10]}': svod_count_two_phase_stress_df,
        #                 f'Свод Резистенция {name_one[:10]}_{name_two[:10]}': svod_count_two_phase_resistance_df,
        #                 f'Свод Истощение {name_one[:10]}_{name_two[:10]}': svod_count_two_phase_exhaustion_df,
        #
        #                 f'Свод ППО {name_one[:10]}_{name_two[:10]}': svod_count_two_level_ppo_df,
        #                 f'Свод НС {name_one[:10]}_{name_two[:10]}': svod_count_two_level_ns_df,
        #                 f'Свод ЗК {name_one[:10]}_{name_two[:10]}': svod_count_two_level_zk_df,
        #                 f'Свод ТД {name_one[:10]}_{name_two[:10]}': svod_count_two_level_td_df,
        #
        #                 f'Свод НИЭР {name_one[:10]}_{name_two[:10]}': svod_count_two_level_niar_df,
        #                 f'Свод ЭНД {name_one[:10]}_{name_two[:10]}': svod_count_two_level_and_df,
        #                 f'Свод РСЭЭ {name_one[:10]}_{name_two[:10]}': svod_count_two_level_rsaa_df,
        #                 f'Свод РПО {name_one[:10]}_{name_two[:10]}': svod_count_two_level_rpo_df,
        #
        #                 f'Свод ЭД {name_one[:10]}_{name_two[:10]}': svod_count_two_level_ad_df,
        #                 f'Свод ЭО {name_one[:10]}_{name_two[:10]}': svod_count_two_level_ao_df,
        #                 f'Свод ЛО {name_one[:10]}_{name_two[:10]}': svod_count_two_level_lo_df,
        #                 f'Свод ППН {name_one[:10]}_{name_two[:10]}': svod_count_two_level_ppn_df,
        #
        #
        #                 f'Свод {name_one}': svod_count_first_level_df,
        #                 f'Ср. {name_one}': svod_mean_first_df,
        #                 f'Свод Напряжение {name_one[:10]}': svod_count_first_phase_stress_df,
        #                 f'Свод Резистенция {name_one[:10]}': svod_count_first_phase_resistance_df,
        #                 f'Свод Истощение {name_one[:10]}': svod_count_first_phase_exhaustion_df,
        #
        #                 f'Свод ППО {name_one}': svod_count_first_level_ppo_df,
        #                 f'Свод НС {name_one}': svod_count_first_level_ns_df,
        #                 f'Свод ЗК {name_one}': svod_count_first_level_zk_df,
        #                 f'Свод ТД {name_one}': svod_count_first_level_td_df,
        #
        #                 f'Свод НИЭР {name_one}': svod_count_first_level_niar_df,
        #                 f'Свод ЭНД {name_one}': svod_count_first_level_and_df,
        #                 f'Свод РСЭЭ {name_one}': svod_count_first_level_rsaa_df,
        #                 f'Свод РПО {name_one}': svod_count_first_level_rpo_df,
        #
        #                 f'Свод ЭД {name_one}': svod_count_first_level_ad_df,
        #                 f'Свод ЭО {name_one}': svod_count_first_level_ao_df,
        #                 f'Свод ЛО {name_one}': svod_count_first_level_lo_df,
        #                 f'Свод ППН {name_one}': svod_count_first_level_ppn_df,
        #
        #                 f'Свод {name_two}': svod_count_second_level_df,
        #                 f'Ср. {name_two}': svod_mean_second_df,
        #                 f'Свод Напряжение {name_two[:10]}': svod_count_second_phase_stress_df,
        #                 f'Свод Резистенция {name_two[:10]}': svod_count_second_phase_resistance_df,
        #                 f'Свод Истощение {name_two[:10]}': svod_count_second_phase_exhaustion_df,
        #
        #                 f'Свод ППО {name_two}': svod_count_second_level_ppo_df,
        #                 f'Свод НС {name_two}': svod_count_second_level_ns_df,
        #                 f'Свод ЗК {name_two}': svod_count_second_level_zk_df,
        #                 f'Свод ТД {name_two}': svod_count_second_level_td_df,
        #
        #                 f'Свод НИЭР {name_two}': svod_count_second_level_niar_df,
        #                 f'Свод ЭНД {name_two}': svod_count_second_level_and_df,
        #                 f'Свод РСЭЭ {name_two}': svod_count_second_level_rsaa_df,
        #                 f'Свод РПО {name_two}': svod_count_second_level_rpo_df,
        #
        #                 f'Свод ЭД {name_two}': svod_count_second_level_ad_df,
        #                 f'Свод ЭО {name_two}': svod_count_second_level_ao_df,
        #                 f'Свод ЛО {name_two}': svod_count_second_level_lo_df,
        #                 f'Свод ППН {name_two}': svod_count_second_level_ppn_df,
        #
        #                 })



































































