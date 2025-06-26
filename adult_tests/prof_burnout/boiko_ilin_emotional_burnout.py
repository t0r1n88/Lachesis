"""
Скрипт для обработки теста Диагностика уровня эмоционального выгорания В.В.Бойко (в модиф. Е.Ильина)
"""
import pandas as pd
import re
from tkinter import messagebox
from lachesis_support_functions import round_mean,create_svod_sub



class BadOrderBOIEB(Exception):
    """
    Исключение для обработки случая когда колонки не совпадают
    """
    pass


class BadValueBOIEB(Exception):
    """
    Исключение для неправильных значений в вариантах ответов
    """
    pass

class BadCountColumnsBOIEB(Exception):
    """
    Исключение для обработки случая если количество колонок не равно 35
    """
    pass


def calc_sub_value_dissatisfaction(row):
    """
    Функция для подсчета значения субшкалы Неудовлетворенность собой
    :param row: строка с ответами
    :return: число
    """
    lst_pr = [1,6,11,16,21,26,31] # вопросы
    result = 0 # результат
    for idx, value in enumerate(row):
        if idx +1 in lst_pr:
            if idx + 1 == 1: # Вопрос 1
                if value == 'нет':
                    result += 3
            elif idx + 1 == 6: # Вопрос 6
                if value == 'да':
                    result += 2
            elif idx + 1 == 11: # Вопрос 11
                if value == 'да':
                    result += 2
            elif idx + 1 == 16: # Вопрос 16
                if value == 'нет':
                    result += 10
            elif idx + 1 == 21: # Вопрос 21
                if value == 'нет':
                    result += 5
            elif idx + 1 == 26: # Вопрос 26
                if value == 'да':
                    result += 5
            elif idx + 1 == 31: # Вопрос 31
                if value == 'да':
                    result += 3

    return result


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
    else:
        return 'сложившийся симптом'


def calc_sub_value_trapped(row):
    """
    Функция для подсчета значения субшкалы Загнанность в клетку
    :param row: строка с ответами
    :return: число
    """
    lst_pr = [2,7,12,17,22,27,32] # вопросы
    result = 0 # результат
    for idx, value in enumerate(row):
        if idx +1 in lst_pr:
            if idx + 1 == 2: # Вопрос 2
                if value == 'да':
                    result += 10
            elif idx +1 == 7: # Вопрос 7
                if value == 'да':
                    result += 5
            elif idx +1 == 12: # Вопрос 12
                if value == 'да':
                    result += 2
            elif idx +1 == 17: # Вопрос 17
                if value == 'да':
                    result += 2
            elif idx +1 == 22: # Вопрос 22
                if value == 'да':
                    result += 5
            elif idx +1 == 27: # Вопрос 27
                if value == 'да':
                    result += 1
            elif idx +1 == 32: # Вопрос 32
                if value == 'нет':
                    result += 5
    return result


def calc_sub_value_reduc(row):
    """
    Функция для подсчета значения субшкалы Редукция профессиональных обязанностей
    :param row: строка с ответами
    :return: число
    """
    lst_pr = [3,8,13,18,26,28,33] # вопросы
    result = 0 # результат
    for idx, value in enumerate(row):
        if idx +1 in lst_pr:
            if idx + 1 == 3: # Вопрос 3
                if value == 'да':
                    result += 5
            elif idx +1 == 8: # Вопрос 8
                if value == 'да':
                    result += 5
            elif idx +1 == 13: # Вопрос 13
                if value == 'да':
                    result += 2
            elif idx +1 == 18: # Вопрос 18
                if value == 'нет':
                    result += 2
            elif idx +1 == 26: # Вопрос 26
                if value == 'да':
                    result += 3
            elif idx +1 == 28: # Вопрос 28
                if value == 'да':
                    result += 3
            elif idx +1 == 33: # Вопрос 33
                if value == 'да':
                    result += 10
    return result


def calc_sub_value_detachment(row):
    """
    Функция для подсчета значения субшкалы Эмоциональная отстраненность
    :param row: строка с ответами
    :return: число
    """
    lst_pr = [4,9,14,19,24,29,34] # вопросы
    result = 0 # результат
    for idx, value in enumerate(row):
        if idx +1 in lst_pr:
            if idx + 1 == 4: # Вопрос 4
                if value == 'да':
                    result += 2
            elif idx +1 == 9: # Вопрос 9
                if value == 'да':
                    result += 3
            elif idx +1 == 14: # Вопрос 14
                if value == 'нет':
                    result += 2
            elif idx +1 == 19: # Вопрос 19
                if value == 'да':
                    result += 3
            elif idx +1 == 24: # Вопрос 24
                if value == 'да':
                    result += 5
            elif idx +1 == 29: # Вопрос 29
                if value == 'да':
                    result += 5
            elif idx +1 == 34: # Вопрос 34
                if value == 'да':
                    result += 10
    return result



def calc_sub_value_self_detachment(row):
    """
    Функция для подсчета значения субшкалы Эмоциональная отстраненность
    :param row: строка с ответами
    :return: число
    """
    lst_pr = [5,10,15,20,25,30,35] # вопросы
    result = 0 # результат
    for idx, value in enumerate(row):
        if idx +1 in lst_pr:
            if idx + 1 == 5: # Вопрос 5
                if value == 'да':
                    result += 5
            elif idx +1 == 10: # Вопрос 10
                if value == 'да':
                    result += 3
            elif idx +1 == 15: # Вопрос 15
                if value == 'да':
                    result += 3
            elif idx +1 == 20: # Вопрос 20
                if value == 'да':
                    result += 2
            elif idx +1 == 25: # Вопрос 25
                if value == 'да':
                    result += 5
            elif idx +1 == 30: # Вопрос 30
                if value == 'да':
                    result += 2
            elif idx +1 == 35: # Вопрос 35
                if value == 'да':
                    result += 10

    return result



def calc_level_attrition(value):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """
    if 0 <= value <= 45:
        return 'отсутствие выгорания'
    elif 46 <= value <= 49:
        return 'симптомы начинающегося выгорания'
    elif 50 <= value <= 75:
        return 'начинающееся выгорание'
    elif 76 <= value <= 79:
        return 'симптомы выгорания'
    else:
        return 'имеется выгорание'


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
    count_df['% отсутствие выгорания от общего'] = round(
        count_df['отсутствие выгорания'] / count_df['Итого'], 2) * 100
    count_df['% симптомы начинающегося выгорания от общего'] = round(
        count_df['симптомы начинающегося выгорания'] / count_df['Итого'], 2) * 100
    count_df['% начинающееся выгорание от общего'] = round(
        count_df['начинающееся выгорание'] / count_df['Итого'], 2) * 100
    count_df['% симптомы выгорания от общего'] = round(
        count_df['симптомы выгорания'] / count_df['Итого'], 2) * 100
    count_df['% имеется выгорание от общего'] = round(
        count_df['имеется выгорание'] / count_df['Итого'], 2) * 100

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



def create_result_biem(base_df:pd.DataFrame, out_dct:dict, lst_svod_cols:list):
    """
    Функция для подсчета результата если указаны колонки по которым нужно провести свод
    :param df: датафрейм с результатами
    :param out_dct: словарь с уже подсчитанными базовыми данными
    :param lst_svod_cols: список сводных колонок
    :return: словарь
    """
    # основная шкала
    lst_reindex_main_level_cols = lst_svod_cols.copy()
    lst_reindex_main_level_cols.extend(['отсутствие выгорания', 'симптомы начинающегося выгорания',
                               'начинающееся выгорание', 'симптомы выгорания', 'имеется выгорание',
                               'Итого'])
    # субшкалы
    lst_reindex_sub_level_cols = lst_svod_cols.copy()
    lst_reindex_sub_level_cols.extend(['не сложившийся симптом', 'складывающийся симптом',
                              'сложившийся симптом',
                              'Итого'])

    # основная шкала
    svod_count_one_level_df = calc_count_main_level(base_df, lst_svod_cols,
                                                    'Значение_уровня_выгорания',
                                                    'Уровень_выгорания',
                                                    lst_reindex_main_level_cols)

    # Симптомы
    svod_count_one_level_dissatisfaction_df = calc_count_level_sub(base_df, lst_svod_cols,
                                                                   'Значение_симптома_Неудовлетворенность_собой',
                                                                   'Уровень_симптома_Неудовлетворенность_собой',
                                                                   lst_reindex_sub_level_cols)

    svod_count_one_level_trapped_df = calc_count_level_sub(base_df, lst_svod_cols,
                                                           'Значение_симптома_Загнанность_в_клетку',
                                                           'Уровень_симптома_Загнанность_в_клетку',
                                                           lst_reindex_sub_level_cols)

    svod_count_one_level_reduc_df = calc_count_level_sub(base_df, lst_svod_cols,
                                                         'Значение_симптома_Редукция_профессиональных_обязанностей',
                                                         'Уровень_симптома_Редукция_профессиональных_обязанностей',
                                                         lst_reindex_sub_level_cols)
    svod_count_one_level_detachment_df = calc_count_level_sub(base_df, lst_svod_cols,
                                                              'Значение_симптома_Эмоциональная_отстраненность',
                                                              'Уровень_симптома_Эмоциональная_отстраненность',
                                                              lst_reindex_sub_level_cols)
    svod_count_one_level_self_detachment_df = calc_count_level_sub(base_df, lst_svod_cols,
                                                                   'Значение_симптома_Личностная_отстраненность',
                                                                   'Уровень_симптома_Личностная_отстраненность',
                                                                   lst_reindex_sub_level_cols)

    # Считаем среднее по субшкалам
    svod_mean_df = pd.pivot_table(base_df,
                                  index=lst_svod_cols,
                                  values=['Значение_уровня_выгорания',
                                          'Значение_симптома_Неудовлетворенность_собой',
                                          'Значение_симптома_Загнанность_в_клетку',
                                          'Значение_симптома_Редукция_профессиональных_обязанностей',
                                          'Значение_симптома_Эмоциональная_отстраненность',
                                          'Значение_симптома_Личностная_отстраненность',
                                          ],
                                  aggfunc=round_mean)
    svod_mean_df.reset_index(inplace=True)
    # упорядочиваем колонки
    new_order_cols = lst_svod_cols.copy()
    new_order_cols.extend(
        ['Значение_уровня_выгорания',
         'Значение_симптома_Неудовлетворенность_собой',
         'Значение_симптома_Загнанность_в_клетку',
         'Значение_симптома_Редукция_профессиональных_обязанностей',
         'Значение_симптома_Эмоциональная_отстраненность',
         'Значение_симптома_Личностная_отстраненность',
         ])
    svod_mean_df = svod_mean_df.reindex(columns=new_order_cols)
    dct_rename_cols_mean = {'Значение_уровня_выгорания': 'Ср. эмоционального выгорания',
                            'Значение_симптома_Неудовлетворенность_собой': 'Ср. Неудовлетворенность собой',
                            'Значение_симптома_Загнанность_в_клетку': 'Ср. Загнанность в клетку',
                            'Значение_симптома_Редукция_профессиональных_обязанностей': 'Ср. Редукция_профессиональных обязанностей',
                            'Значение_симптома_Эмоциональная_отстраненность': 'Ср.Эмоциональная отстраненность',
                            'Значение_симптома_Личностная_отстраненность': 'Ср. Личностная отстраненность',
                            }
    svod_mean_df.rename(columns=dct_rename_cols_mean, inplace=True)

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


    out_dct.update({f'Свод {out_name}': svod_count_one_level_df,
                    f'Ср. {out_name}': svod_mean_df,

                    f'Свод НС {out_name}': svod_count_one_level_dissatisfaction_df,
                    f'Свод ЗК {out_name}': svod_count_one_level_trapped_df,
                    f'Свод РПО {out_name}': svod_count_one_level_reduc_df,
                    f'Свод ЭО {out_name}': svod_count_one_level_detachment_df,
                    f'Свод ЛО {out_name}': svod_count_one_level_self_detachment_df,

                    })

    if len(lst_svod_cols) == 1:
        return out_dct
    else:
        for idx, name_column in enumerate(lst_svod_cols):
            lst_reindex_column_main_level_cols = [lst_svod_cols[idx], 'отсутствие выгорания', 'симптомы начинающегося выгорания',
                               'начинающееся выгорание', 'симптомы выгорания', 'имеется выгорание',
                               'Итого']  # Основная шкала

            lst_reindex_column_sub_level_cols = [lst_svod_cols[idx], 'не сложившийся симптом', 'складывающийся симптом',
                              'сложившийся симптом',
                              'Итого']  # Субшкалы

            # основная шкала
            svod_count_column_level_df = calc_count_main_level(base_df, [lst_svod_cols[idx]],
                                                               'Значение_уровня_выгорания',
                                                               'Уровень_выгорания',
                                                               lst_reindex_column_main_level_cols)

            # Субшкалы
            svod_count_column_level_dissatisfaction_df = calc_count_level_sub(base_df, [lst_svod_cols[idx]],
                                                                              'Значение_симптома_Неудовлетворенность_собой',
                                                                              'Уровень_симптома_Неудовлетворенность_собой',
                                                                              lst_reindex_column_sub_level_cols)

            svod_count_column_level_trapped_df = calc_count_level_sub(base_df, [lst_svod_cols[idx]],
                                                                      'Значение_симптома_Загнанность_в_клетку',
                                                                      'Уровень_симптома_Загнанность_в_клетку',
                                                                      lst_reindex_column_sub_level_cols)

            svod_count_column_level_reduc_df = calc_count_level_sub(base_df, [lst_svod_cols[idx]],
                                                                    'Значение_симптома_Редукция_профессиональных_обязанностей',
                                                                    'Уровень_симптома_Редукция_профессиональных_обязанностей',
                                                                    lst_reindex_column_sub_level_cols)
            svod_count_column_level_detachment_df = calc_count_level_sub(base_df, [lst_svod_cols[idx]],
                                                                         'Значение_симптома_Эмоциональная_отстраненность',
                                                                         'Уровень_симптома_Эмоциональная_отстраненность',
                                                                         lst_reindex_column_sub_level_cols)
            svod_count_column_level_self_detachment_df = calc_count_level_sub(base_df, [lst_svod_cols[idx]],
                                                                              'Значение_симптома_Личностная_отстраненность',
                                                                              'Уровень_симптома_Личностная_отстраненность',
                                                                              lst_reindex_column_sub_level_cols)

            svod_mean_column_df = pd.pivot_table(base_df,
                                          index=[lst_svod_cols[idx]],
                                          values=['Значение_уровня_выгорания',
                                                  'Значение_симптома_Неудовлетворенность_собой',
                                                  'Значение_симптома_Загнанность_в_клетку',
                                                  'Значение_симптома_Редукция_профессиональных_обязанностей',
                                                  'Значение_симптома_Эмоциональная_отстраненность',
                                                  'Значение_симптома_Личностная_отстраненность',
                                                  ],
                                          aggfunc=round_mean)
            svod_mean_column_df.reset_index(inplace=True)
            # упорядочиваем колонки
            new_order_cols = [lst_svod_cols[idx]].copy()

            new_order_cols.extend(
                ['Значение_уровня_выгорания',
                 'Значение_симптома_Неудовлетворенность_собой',
                 'Значение_симптома_Загнанность_в_клетку',
                 'Значение_симптома_Редукция_профессиональных_обязанностей',
                 'Значение_симптома_Эмоциональная_отстраненность',
                 'Значение_симптома_Личностная_отстраненность',
                 ])
            svod_mean_column_df = svod_mean_column_df.reindex(columns=new_order_cols)
            dct_rename_cols_mean = {'Значение_уровня_выгорания': 'Ср. эмоционального выгорания',
                                    'Значение_симптома_Неудовлетворенность_собой': 'Ср. Неудовлетворенность собой',
                                    'Значение_симптома_Загнанность_в_клетку': 'Ср. Загнанность в клетку',
                                    'Значение_симптома_Редукция_профессиональных_обязанностей': 'Ср. Редукция_профессиональных обязанностей',
                                    'Значение_симптома_Эмоциональная_отстраненность': 'Ср.Эмоциональная отстраненность',
                                    'Значение_симптома_Личностная_отстраненность': 'Ср. Личностная отстраненность',
                                    }
            svod_mean_column_df.rename(columns=dct_rename_cols_mean, inplace=True)

            name_column = lst_svod_cols[idx]
            name_column = re.sub(r'[\[\]\'+()<> :"?*|\\/]', '_', name_column)
            name_column = name_column[:15]

            out_dct.update({f'Свод {name_column}': svod_count_column_level_df,
                            f'Ср. {name_column}': svod_mean_column_df,
                            f'Свод НС {name_column}': svod_count_column_level_dissatisfaction_df,
                            f'Свод ЗК {name_column}': svod_count_column_level_trapped_df,
                            f'Свод РПО {name_column}': svod_count_column_level_reduc_df,
                            f'Свод ЭО {name_column}': svod_count_column_level_detachment_df,
                            f'Свод ЛО {name_column}': svod_count_column_level_self_detachment_df})
        return out_dct















def processing_boiko_ilin_emotional_burnout(result_df: pd.DataFrame, answers_df: pd.DataFrame, lst_svod_cols:list):
    """
    Функция для обработки
    :param result_df: часть датафрейма с описательными колонками
    :param answers_df: часть датафрейма с ответами
    :param lst_svod_cols:  список с колонками по которым нужно делать свод
    """
    try:
        out_answer_df = result_df.copy()  # делаем копию для последующего соединения с сырыми ответами
        if len(answers_df.columns) != 35:  # проверяем количество колонок с вопросами
            raise BadCountColumnsBOIEB

        lst_check_cols = ['Сегодня я доволен своей профессией не меньше, чем в начале карьеры.',
                          'Я ошибся в выборе профессии или профиля деятельности (занимаю не свое место).',
                          'Когда я чувствую усталость или напряжение, то стараюсь поскорее “свернуть” дело.',
                          'Моя работа притупляет эмоции.',
                          'Я откровенно устал от проблем, с которыми приходится иметь дело на работе.',
                          'Работа приносит мне все больше удовлетворения.',
                          'Я бы сменил место работы, если бы представилась возможность.',
                          'Из-за усталости или напряжения я уделяю своим делам меньше внимания, чем положено.',
                          'Я спокойно воспринимаю претензии ко мне начальства и коллег по работе.',
                          'Общение с коллегами по работе побуждает меня сторониться людей.',
                          'Мне все труднее устанавливать и поддерживать контакты с коллегами.',
                          'Обстановка на работе мне кажется очень трудной, сложной.',
                          'Бывают дни, когда мое эмоциональное состояние плохо сказывается на результатах работы.',
                          'Я очень переживаю за свою работу.',
                          'Коллегам по работе я уделяю внимания больше, чем получаю от них.',
                          'Я часто радуюсь, видя, что моя работа приносит пользу людям.',
                          'Последнее время меня преследуют неудачи на работе.',
                          'Я обычно проявляю интерес к коллегам и помимо того, что касается дела.',
                          'Я иногда ловлю себя на мысли, что работаю автоматически, без души.',
                          'По работе встречаются настолько неприятные люди, что невольно желаешь им чего-нибудь плохого.',
                          'Успехи в работе вдохновляют меня.',
                          'Ситуация на работе, в которой я оказался, кажется почти безвыходной.',
                          'Я часто работаю через силу.',
                          'В работе с людьми я руководствуюсь принципом: не трать нервы, береги здоровье.',
                          'Иногда я иду на работу с тяжелым чувством: как все надоело, никого бы не видеть и не слышать.',
                          'Иногда мне кажется, что результаты моей работы не стоят тех усилий, которые я затрачиваю.',
                          'Если бы мне повезло с работой, я был бы более счастлив.',
                          'Обычно я тороплю время: скорее бы рабочий день кончился.',
                          'Работая с людьми, я обычно как бы ставлю экран, защищающий от чужих страданий и отрицательных эмоций.',
                          'Моя работа меня очень разочаровала.',
                          'Мои требования к выполняемой работе выше, чем-то, чего я достигаю в силу обстоятельств.',
                          'Моя карьера сложилась удачно.',
                          'Если предоставляется возможность, я уделяю работе меньше внимания, но так, чтобы этого никто не заметил.',
                          'Ко всему, что происходит на работе, я утратил интерес.',
                          'Моя работа плохо на меня повлияла – обозлила, притупила эмоции, сделала нервным.',
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
            raise BadOrderBOIEB

        valid_values = ['да','нет']
        # Проверяем, есть ли значения, отличающиеся от указанных в списке
        lst_error_answers = []  # список для хранения строк где найдены неправильные ответы

        for i in range(35):
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
            raise BadValueBOIEB

        base_df = pd.DataFrame()
        # Симптом Неудовлетворенность собой
        base_df['Значение_симптома_Неудовлетворенность_собой'] = answers_df.apply(calc_sub_value_dissatisfaction, axis=1)
        base_df['Уровень_симптома_Неудовлетворенность_собой'] = base_df['Значение_симптома_Неудовлетворенность_собой'].apply(
            calc_level_sub)

        # Симптом Загнанность в клетку
        base_df['Значение_симптома_Загнанность_в_клетку'] = answers_df.apply(calc_sub_value_trapped, axis=1)
        base_df['Уровень_симптома_Загнанность_в_клетку'] = base_df['Значение_симптома_Загнанность_в_клетку'].apply(
            calc_level_sub)

        # Симптом Редукция профессиональных обязанностей
        base_df['Значение_симптома_Редукция_профессиональных_обязанностей'] = answers_df.apply(calc_sub_value_reduc, axis=1)
        base_df['Уровень_симптома_Редукция_профессиональных_обязанностей'] = base_df['Значение_симптома_Редукция_профессиональных_обязанностей'].apply(
            calc_level_sub)

        # Симптом Эмоциональная отстраненность
        base_df['Значение_симптома_Эмоциональная_отстраненность'] = answers_df.apply(calc_sub_value_detachment, axis=1)
        base_df['Уровень_симптома_Эмоциональная_отстраненность'] = base_df['Значение_симптома_Эмоциональная_отстраненность'].apply(
            calc_level_sub)

        # Симптом Личностная отстраненность (деперсонализация)»:
        base_df['Значение_симптома_Личностная_отстраненность'] = answers_df.apply(calc_sub_value_self_detachment, axis=1)
        base_df['Уровень_симптома_Личностная_отстраненность'] = base_df['Значение_симптома_Личностная_отстраненность'].apply(
            calc_level_sub)

        base_df['Значение_уровня_выгорания'] = base_df[['Значение_симптома_Неудовлетворенность_собой','Значение_симптома_Загнанность_в_клетку',
                                                        'Значение_симптома_Редукция_профессиональных_обязанностей','Значение_симптома_Эмоциональная_отстраненность',
                                                        'Значение_симптома_Личностная_отстраненность']].sum(axis=1)
        base_df['Уровень_выгорания'] = base_df['Значение_уровня_выгорания'].apply(
            calc_level_attrition)

        base_df['Норма_Для_симптомов'] = '0-9 баллов'


        # Создаем датафрейм для создания части в общий датафрейм
        part_df = pd.DataFrame()

        part_df['ЭВБИ_Значение_выгорания'] = base_df['Значение_уровня_выгорания']
        part_df['ЭВБИ_Уровень_выгорания'] = base_df['Уровень_выгорания']

        part_df['ЭВБИ_НС_Значение'] = base_df['Значение_симптома_Неудовлетворенность_собой']
        part_df['ЭВБИ_НС_Уровень'] = base_df['Уровень_симптома_Неудовлетворенность_собой']

        part_df['ЭВБИ_ЗК_Значение'] = base_df['Значение_симптома_Загнанность_в_клетку']
        part_df['ЭВБИ_ЗК_Уровень'] = base_df['Уровень_симптома_Загнанность_в_клетку']

        part_df['ЭВБИ_РПО_Значение'] = base_df['Значение_симптома_Редукция_профессиональных_обязанностей']
        part_df['ЭВБИ_РПО_Уровень'] = base_df['Уровень_симптома_Редукция_профессиональных_обязанностей']

        part_df['ЭВБИ_ЭО_Значение'] = base_df['Значение_симптома_Эмоциональная_отстраненность']
        part_df['ЭВБИ_ЭО_Уровень'] = base_df['Уровень_симптома_Эмоциональная_отстраненность']

        part_df['ЭВБИ_ЛО_Значение'] = base_df['Значение_симптома_Личностная_отстраненность']
        part_df['ЭВБИ_ЛО_Уровень'] = base_df['Уровень_симптома_Личностная_отстраненность']

        new_order_cols = ['Значение_уровня_выгорания','Уровень_выгорания','Норма_Для_симптомов',
                          'Значение_симптома_Неудовлетворенность_собой','Уровень_симптома_Неудовлетворенность_собой',
                          'Значение_симптома_Загнанность_в_клетку','Уровень_симптома_Загнанность_в_клетку',
                          'Значение_симптома_Редукция_профессиональных_обязанностей','Уровень_симптома_Редукция_профессиональных_обязанностей',
                          'Значение_симптома_Эмоциональная_отстраненность','Уровень_симптома_Эмоциональная_отстраненность',
                          'Значение_симптома_Личностная_отстраненность','Уровень_симптома_Личностная_отстраненность',
                          ]

        base_df = base_df.reindex(columns=new_order_cols)
        # Соединяем анкетную часть с результатной
        base_df = pd.concat([result_df, base_df], axis=1)

        base_df.sort_values(by='Значение_уровня_выгорания', ascending=False, inplace=True)  # сортируем
        out_answer_df = pd.concat([out_answer_df, answers_df], axis=1)  # Датафрейм для проверки

        # Общий свод по уровням общей шкалы всего в процентном соотношении
        base_svod_all_df = pd.DataFrame(
            index=['отсутствие выгорания', 'симптомы начинающегося выгорания',
                   'начинающееся выгорание','симптомы выгорания','имеется выгорание'])

        svod_level_df = pd.pivot_table(base_df, index='Уровень_выгорания',
                                       values='Значение_уровня_выгорания',
                                       aggfunc='count')

        svod_level_df['% от общего'] = round(
            svod_level_df['Значение_уровня_выгорания'] / svod_level_df[
                'Значение_уровня_выгорания'].sum(), 3) * 100

        base_svod_all_df = base_svod_all_df.join(svod_level_df)

        # # Создаем суммирующую строку
        base_svod_all_df.loc['Итого'] = svod_level_df.sum()
        base_svod_all_df.reset_index(inplace=True)
        base_svod_all_df.rename(columns={'index': 'Уровень', 'Значение_уровня_выгорания': 'Количество'},
                                inplace=True)
        # формируем основной словарь
        out_dct = {'Списочный результат': base_df, 'Список для проверки': out_answer_df,
                   'Свод Общий': base_svod_all_df,
                   }

        lst_level = ['отсутствие выгорания', 'симптомы начинающегося выгорания',
                   'начинающееся выгорание','симптомы выгорания','имеется выгорание']
        dct_level = dict()

        for level in lst_level:
            temp_df = base_df[base_df['Уровень_выгорания'] == level]
            if temp_df.shape[0] != 0:
                if level == 'симптомы начинающегося выгорания':
                    level = 'симптомы начин-ся выгорания'
                dct_level[level] = temp_df

        out_dct.update(dct_level)

        lst_simptom = ['не сложившийся симптом','складывающийся симптом','сложившийся симптом']

        # Свод по уровням симптомов всего в процентном соотношении
        svod_dissatisfaction = create_svod_sub(base_df,lst_simptom,'Уровень_симптома_Неудовлетворенность_собой','Значение_симптома_Неудовлетворенность_собой','count')
        svod_trapped = create_svod_sub(base_df,lst_simptom,'Уровень_симптома_Загнанность_в_клетку','Значение_симптома_Загнанность_в_клетку','count')
        svod_reduc = create_svod_sub(base_df,lst_simptom,'Уровень_симптома_Редукция_профессиональных_обязанностей','Значение_симптома_Редукция_профессиональных_обязанностей','count')
        svod_detachment = create_svod_sub(base_df,lst_simptom,'Уровень_симптома_Эмоциональная_отстраненность','Значение_симптома_Эмоциональная_отстраненность','count')
        svod_self_detachment = create_svod_sub(base_df,lst_simptom,'Уровень_симптома_Личностная_отстраненность','Значение_симптома_Личностная_отстраненность','count')

        # Среднее значение по симптомам
        # считаем среднее значение по субшкалам
        avg_dissatisfaction = round(base_df['Значение_симптома_Неудовлетворенность_собой'].mean(), 1)
        avg_trapped = round(base_df['Значение_симптома_Загнанность_в_клетку'].mean(), 1)
        avg_reduc = round(base_df['Значение_симптома_Редукция_профессиональных_обязанностей'].mean(), 1)
        avg_detachment = round(base_df['Значение_симптома_Эмоциональная_отстраненность'].mean(), 1)
        avg_self_detachment = round(base_df['Значение_симптома_Личностная_отстраненность'].mean(), 1)

        avg_dct = {'Среднее значение симптома Неудовлетворенность собой': avg_dissatisfaction,
                   'Среднее значение симптома Загнанность в клетку': avg_trapped,
                   'Среднее значение симптома Редукция профессиональных обязанностей': avg_reduc,
                   'Среднее значение симптома Эмоциональная отстраненность': avg_detachment,
                   'Среднее значение симптома Личностная отстраненность': avg_self_detachment,
                   }

        avg_df = pd.DataFrame.from_dict(avg_dct, orient='index')
        avg_df = avg_df.reset_index()
        avg_df.columns = ['Показатель', 'Среднее значение']

        out_dct.update({'Свод НС':svod_dissatisfaction,
                        'Свод ЗК':svod_trapped,
                        'Свод РПО':svod_reduc,
                        'Свод ЭО':svod_detachment,
                        'Свод ЛО':svod_self_detachment,
                        'Среднее по симптомам':avg_df})

        """
                Сохраняем в зависимости от необходимости делать своды по определенным колонкам
                """
        if len(lst_svod_cols) == 0:
            return out_dct, part_df
        else:
            out_dct = create_result_biem(base_df, out_dct, lst_svod_cols)

            return out_dct, part_df
    except BadOrderBOIEB:
        messagebox.showerror('Лахеcис',
                             f'При обработке вопросов теста Эмоциональное выгорание Бойко Ильин обнаружены неправильные вопросы. Проверьте названия колонок с вопросами:\n'
                             f'{error_order_message}\n'
                             f'Используйте при создании Яндекс-формы написание вопросов из руководства пользователя программы Лахесис.')
    except BadValueBOIEB:
        messagebox.showerror('Лахеcис',
                             f'При обработке вопросов теста Эмоциональное выгорание Бойко Ильин обнаружены неправильные варианты ответов. Проверьте ответы на указанных строках:\n'
                             f'{error_message}\n'
                             f'Используйте при создании Яндекс-формы написание вариантов ответа из руководства пользователя программы Лахесис.')


    except BadCountColumnsBOIEB:
        messagebox.showerror('Лахеcис',
                             f'Проверьте количество колонок с ответами на тест Эмоциональное выгорание Бойко Ильин\n'
                             f'Должно быть 35 колонок с ответами')















