"""
Скрипт для обработки результатов теста MBI Профессиональное выгорание Маслач Водопьянова исходный вариант
"""

import pandas as pd
import re
from tkinter import messagebox
from lachesis_support_functions import round_mean,create_union_svod


class BadOrderMPBV(Exception):
    """
    Исключение для обработки случая когда колонки не совпадают
    """
    pass


class BadValueMPBV(Exception):
    """
    Исключение для неправильных значений в вариантах ответов
    """
    pass

class BadCountColumnsMPBV(Exception):
    """
    Исключение для обработки случая если количество колонок не равно 22
    """
    pass


def calc_sub_value_em_attrition(row):
    """
    Функция для подсчета значения субшкалы Эмоциональное истощение
    :param row: строка с ответами
    :return: число
    """
    lst_pr = [1,2,3,6,8,13,14,16,20]

    value_forward = 0 # счетчик прямых ответов

    for idx, value in enumerate(row):
        if idx +1 in lst_pr:
            value_forward += value

    return value_forward


def calc_level_sub_em_attrition(value):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """
    if 0 <= value <= 10:
        return 'крайне низкий уровень'
    elif 11 <= value <= 20:
        return 'низкий уровень'
    elif 21 <= value <= 30:
        return 'средний уровень'
    elif 31 <= value <= 40:
        return 'высокий уровень'
    else:
        return 'крайне высокий уровень'



def calc_sub_value_depers(row):
    """
    Функция для подсчета значения субшкалы Деперсонализация
    :param row: строка с ответами
    :return: число
    """
    lst_pr = [5,10,11,15,22]

    value_forward = 0 # счетчик прямых ответов

    for idx, value in enumerate(row):
        if idx +1 in lst_pr:
            value_forward += value

    return value_forward


def calc_level_sub_depers(value):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """
    if 0 <= value <= 5:
        return 'крайне низкий уровень'
    elif 6 <= value <= 11:
        return 'низкий уровень'
    elif 12 <= value <= 17:
        return 'средний уровень'
    elif 18 <= value <= 23:
        return 'высокий уровень'
    else:
        return 'крайне высокий уровень'


def calc_sub_value_reduc(row):
    """
    Функция для подсчета значения субшкалы Редукция персональных достижений
    :param row: строка с ответами
    :return: число
    """
    lst_pr = [4,7,9,12,17,18,19,21]

    value_forward = 0 # счетчик прямых ответов

    for idx, value in enumerate(row):
        if idx +1 in lst_pr:
            if value == 6:
                value_forward += 0
            elif value == 5:
                value_forward += 1
            elif value == 4:
                value_forward += 2
            elif value == 3:
                value_forward += 3
            elif value == 2:
                value_forward += 4
            elif value == 1:
                value_forward += 5
            elif value == 0:
                value_forward += 6

    return value_forward


def calc_level_sub_reduc(value):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """
    if 0 <= value <= 8:
        return 'крайне низкий уровень'
    elif 9 <= value <= 18:
        return 'низкий уровень'
    elif 19 <= value <= 28:
        return 'средний уровень'
    elif 29 <= value <= 38:
        return 'высокий уровень'
    else:
        return 'крайне высокий уровень'

def calc_level_psy(value):
    """
    Функция для подсчета психического выгорания
    :param value:
    :return:
    """
    if 0 <= value <= 23:
        return 'крайне низкий уровень'
    elif 24 <= value <= 49:
        return 'низкий уровень'
    elif 50 <= value <= 75:
        return 'средний уровень'
    elif 76 <= value <= 101:
        return 'высокий уровень'
    else:
        return 'крайне высокий уровень'


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


def calc_count_level(df:pd.DataFrame, lst_cat:list, val_cat, col_cat, lst_cols:list):
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
    count_df['% крайне низкий уровень от общего'] = round(
        count_df['крайне низкий уровень'] / count_df['Итого'], 2) * 100
    count_df['% низкий уровень от общего'] = round(
        count_df['низкий уровень'] / count_df['Итого'], 2) * 100
    count_df['% средний уровень от общего'] = round(
        count_df['средний уровень'] / count_df['Итого'], 2) * 100
    count_df['% высокий уровень от общего'] = round(
        count_df['высокий уровень'] / count_df['Итого'], 2) * 100
    count_df['% крайне высокий уровень от общего'] = round(
        count_df['крайне высокий уровень'] / count_df['Итого'], 2) * 100

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
    count_df['% крайне низкий уровень от общего'] = round(
        count_df['крайне низкий уровень'] / count_df['Итого'], 2) * 100
    count_df['% низкий уровень от общего'] = round(
        count_df['низкий уровень'] / count_df['Итого'], 2) * 100
    count_df['% средний уровень от общего'] = round(
        count_df['средний уровень'] / count_df['Итого'], 2) * 100
    count_df['% высокий уровень от общего'] = round(
        count_df['высокий уровень'] / count_df['Итого'], 2) * 100
    count_df['% крайне высокий уровень от общего'] = round(
        count_df['крайне высокий уровень'] / count_df['Итого'], 2) * 100

    return count_df


def create_result_mpbv(base_df:pd.DataFrame,out_dct:dict,lst_svod_cols:list):
    """
    Функция для подсчета результата если указаны колонки по которым нужно провести свод
    :param df: датафрейм с результатами
    :param out_dct: словарь с уже подсчитанными базовыми данными
    :param lst_svod_cols: список сводных колонок
    :return: словарь
    """
    lst_reindex_main_level_cols = lst_svod_cols.copy()
    lst_reindex_main_level_cols.extend( ['крайне низкий уровень', 'низкий уровень',
                                   'средний уровень', 'высокий уровень', 'крайне высокий уровень',
                                   'Итого'])  # Основная шкала

    # основная шкала
    svod_count_one_level_df = calc_count_level(base_df, lst_svod_cols,
                                               'Значение_уровня_психического_выгорания',
                                               'Уровень_психического_выгорания',
                                               lst_reindex_main_level_cols)

    # Субшкалы
    svod_count_one_level_em_df = calc_count_level_sub(base_df, lst_svod_cols,
                                                      'Значение_субшкалы_Психоэмоциональное_истощение',
                                                      'Уровень_субшкалы_Психоэмоциональное_истощение',
                                                      lst_reindex_main_level_cols)

    svod_count_one_level_depers_df = calc_count_level_sub(base_df, lst_svod_cols,
                                                          'Значение_субшкалы_Деперсонализация',
                                                          'Уровень_субшкалы_Деперсонализация',
                                                          lst_reindex_main_level_cols)

    svod_count_one_level_reduc_df = calc_count_level_sub(base_df, lst_svod_cols,
                                                         'Значение_субшкалы_Редукция_личных_достижений',
                                                         'Уровень_субшкалы_Редукция_личных_достижений',
                                                         lst_reindex_main_level_cols)

    # Считаем среднее по субшкалам
    svod_mean_df = pd.pivot_table(base_df,
                                  index=lst_svod_cols,
                                  values=['Значение_уровня_психического_выгорания', 'Значение_субшкалы_Психоэмоциональное_истощение',
                                          'Значение_субшкалы_Деперсонализация', 'Значение_субшкалы_Редукция_личных_достижений',
                                                                                   ],
                                  aggfunc=round_mean)
    svod_mean_df.reset_index(inplace=True)
    # упорядочиваем колонки
    new_order_cols = lst_svod_cols.copy()
    new_order_cols.extend((['Значение_уровня_психического_выгорания', 'Значение_субшкалы_Психоэмоциональное_истощение',
                                          'Значение_субшкалы_Деперсонализация', 'Значение_субшкалы_Редукция_личных_достижений',
                                                                                   ]))
    svod_mean_df = svod_mean_df.reindex(columns=new_order_cols)

    dct_rename_cols_mean = {'Значение_уровня_психического_выгорания': 'Ср. психическое выгорание',
                            'Значение_субшкалы_Психоэмоциональное_истощение': 'Ср. Психоэмоциональное истощение',
                            'Значение_субшкалы_Деперсонализация': 'Ср. Деперсонализация',
                            'Значение_субшкалы_Редукция_личных_достижений': 'Ср. Редукция личных достижений',}
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
                    f'Ср {out_name}':svod_mean_df,
                f'Свод ПЭИ {out_name}': svod_count_one_level_em_df,
                f'Свод ДП {out_name}': svod_count_one_level_depers_df,
                f'Свод РЛД {out_name}': svod_count_one_level_reduc_df})

    if len(lst_svod_cols) == 1:
        return out_dct
    else:
        for idx, name_column in enumerate(lst_svod_cols):
            lst_reindex_column_cols = [lst_svod_cols[idx],'крайне низкий уровень', 'низкий уровень',
                                   'средний уровень', 'высокий уровень', 'крайне высокий уровень',
                                   'Итого']  # Основная шкала

            # основная шкала
            svod_count_column_level_df = calc_count_level(base_df, lst_svod_cols[idx],
                                                       'Значение_уровня_психического_выгорания',
                                                       'Уровень_психического_выгорания',
                                                       lst_reindex_column_cols)

            # Субшкалы
            svod_count_column_level_em_df = calc_count_level_sub(base_df, lst_svod_cols[idx],
                                                              'Значение_субшкалы_Психоэмоциональное_истощение',
                                                              'Уровень_субшкалы_Психоэмоциональное_истощение',
                                                              lst_reindex_column_cols)

            svod_count_column_level_depers_df = calc_count_level_sub(base_df, lst_svod_cols[idx],
                                                                  'Значение_субшкалы_Деперсонализация',
                                                                  'Уровень_субшкалы_Деперсонализация',
                                                                  lst_reindex_column_cols)

            svod_count_column_level_reduc_df = calc_count_level_sub(base_df, lst_svod_cols[idx],
                                                                 'Значение_субшкалы_Редукция_личных_достижений',
                                                                 'Уровень_субшкалы_Редукция_личных_достижений',
                                                                 lst_reindex_column_cols)
            # Считаем среднее по субшкалам
            svod_mean_column_df = pd.pivot_table(base_df,
                                          index=[lst_svod_cols[idx]],
                                          values=['Значение_уровня_психического_выгорания',
                                                  'Значение_субшкалы_Психоэмоциональное_истощение',
                                                  'Значение_субшкалы_Деперсонализация',
                                                  'Значение_субшкалы_Редукция_личных_достижений',
                                                  ],
                                          aggfunc=round_mean)
            svod_mean_column_df.reset_index(inplace=True)
            # упорядочиваем колонки
            new_order_cols = [lst_svod_cols[idx]].copy()
            new_order_cols.extend(
                (['Значение_уровня_психического_выгорания', 'Значение_субшкалы_Психоэмоциональное_истощение',
                  'Значение_субшкалы_Деперсонализация', 'Значение_субшкалы_Редукция_личных_достижений',
                  ]))
            svod_mean_column_df = svod_mean_column_df.reindex(columns=new_order_cols)

            dct_rename_cols_mean = {'Значение_уровня_психического_выгорания': 'Ср. психическое выгорание',
                                    'Значение_субшкалы_Психоэмоциональное_истощение': 'Ср. Психоэмоциональное истощение',
                                    'Значение_субшкалы_Деперсонализация': 'Ср. Деперсонализация',
                                    'Значение_субшкалы_Редукция_личных_достижений': 'Ср. Редукция личных достижений', }
            svod_mean_column_df.rename(columns=dct_rename_cols_mean, inplace=True)

            name_column = lst_svod_cols[idx]
            name_column = re.sub(r'[\[\]\'+()<> :"?*|\\/]', '_', name_column)
            name_column = name_column[:15]

            out_dct.update({f'Свод {name_column}': svod_count_column_level_df,
                    f'Ср {name_column}':svod_mean_column_df,
                f'Свод ПЭИ {name_column}': svod_count_column_level_em_df,
                f'Свод ДП {name_column}': svod_count_column_level_depers_df,
                f'Свод РЛД {name_column}': svod_count_column_level_reduc_df})

        return out_dct















def processing_maslach_prof_burnout_vod(result_df: pd.DataFrame, answers_df: pd.DataFrame, lst_svod_cols:list):
    """
    Функция для обработки
    :param result_df: часть датафрейма с описательными колонками
    :param answers_df: часть датафрейма с ответами
    :param lst_svod_cols:  список с колонками по которым нужно делать свод
    """
    try:
        out_answer_df = result_df.copy()  # делаем копию для последующего соединения с сырыми ответами
        if len(answers_df.columns) != 22:  # проверяем количество колонок с вопросами
            raise BadCountColumnsMPBV

        # очищаем названия колонок от возможных сочетаний .1 которые добавляет пандас при одинаковых колонках
        clean_df_lst = []
        for name_column in answers_df.columns:
            clean_name = re.sub(r'.\d+$', '', name_column)
            clean_df_lst.append(clean_name)

        answers_df.columns = clean_df_lst


        lst_check_cols = ['Я чувствую себя эмоционально опустошенным(ой).',
                          'После работы я чувствую себя как «выжатый лимон».',
                          'Утром я чувствую усталость и нежелание идти на работу.',
                          'Я хорошо понимаю, что чувствуют мои подчиненные и коллеги, и стараюсь учитывать это в интересах дела.',
                          'Я чувствую, что общаюсь с некоторыми подчиненными и коллегами как с предметами (без теплоты и расположения к ним).',
                          'После работы на некоторое время хочется уединиться от всех и всего.',
                          'Я умею находить правильное решение в конфликтных ситуациях, возникающих при общении с коллегами.',
                          'Я чувствую угнетенность и апатию.',
                          'Я уверен(а), что моя работа нужна людям.',
                          'В последнее время я стал(а) более «черствым» по отношению к тем, с кем работаю.',
                          'Я замечаю, что моя работа ожесточает меня.',
                          'У меня много планов на будущее, и я верю в их осуществление.',
                          'Моя работа все больше меня разочаровывает.',
                          'Мне кажется, что я слишком много работаю.',
                          'Бывает, что мне действительно безразлично то, что происходит c некоторыми моими подчиненными и коллегами.',
                          'Мне хочется уединиться и отдохнуть от всего и всех.',
                          'Я легко могу создать атмосферу доброжелательности и сотрудничества в коллективе.',
                          'Во время работы я чувствую приятное оживление.',
                          'Благодаря своей работе я уже сделал(а) в жизни много действительно ценного.',
                          'Я чувствую равнодушие и потерю интереса ко многому, что радовало меня в моей работе.',
                          'На работе я спокойно справляюсь с эмоциональными проблемами.',
                          'В последнее время мне кажется, что коллеги и подчиненные все чаще перекладывают на меня груз своих проблем и обязанностей.',
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
            raise BadOrderMPBV

        # словарь для замены слов на числа
        dct_replace_value = {'никогда': 0,
                             'очень редко': 1,
                             'редко': 2,
                             'иногда': 3,
                             'часто': 4,
                             'очень часто': 5,
                             'ежедневно': 6}

        valid_values = [0, 1, 2, 3, 4, 5, 6]
        answers_df.replace(dct_replace_value, inplace=True)  # заменяем слова на цифры для подсчетов
        # Проверяем, есть ли значения, отличающиеся от указанных в списке
        lst_error_answers = []  # список для хранения строк где найдены неправильные ответы

        for i in range(22):
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
            raise BadValueMPBV

        # Субшкала Эмоциональное истощение
        base_df = pd.DataFrame()
        base_df['Значение_субшкалы_Психоэмоциональное_истощение'] = answers_df.apply(calc_sub_value_em_attrition, axis=1)
        base_df['Норма_Психоэмоциональное_истощение'] = '0-30 баллов'
        base_df['Уровень_субшкалы_Психоэмоциональное_истощение'] = base_df['Значение_субшкалы_Психоэмоциональное_истощение'].apply(
            calc_level_sub_em_attrition)

        # Субшкала Деперсонализация
        base_df['Значение_субшкалы_Деперсонализация'] = answers_df.apply(calc_sub_value_depers, axis=1)
        base_df['Норма_Деперсонализация'] = '0-17 баллов'
        base_df['Уровень_субшкалы_Деперсонализация'] = base_df['Значение_субшкалы_Деперсонализация'].apply(
            calc_level_sub_depers)

        # Субшкала Редукция персональных достижений
        base_df['Значение_субшкалы_Редукция_личных_достижений'] = answers_df.apply(calc_sub_value_reduc, axis=1)
        base_df['Норма_Редукция_личных_достижений'] = '0-28 баллов'
        base_df['Уровень_субшкалы_Редукция_личных_достижений'] = base_df[
            'Значение_субшкалы_Редукция_личных_достижений'].apply(calc_level_sub_reduc)

        # Уровень выгорания
        base_df['Значение_уровня_психического_выгорания'] = base_df[['Значение_субшкалы_Психоэмоциональное_истощение','Значение_субшкалы_Деперсонализация','Значение_субшкалы_Редукция_личных_достижений']].sum(axis=1)
        base_df['Уровень_психического_выгорания'] = base_df['Значение_уровня_психического_выгорания'].apply(calc_level_psy)

        # Создаем датафрейм для создания части в общий датафрейм
        part_df = pd.DataFrame()

        part_df['МПВВ_Значение_психического_выгорания'] = base_df['Значение_уровня_психического_выгорания']
        part_df['МПВВ_Уровень_психического_выгорания'] = base_df['Уровень_психического_выгорания']

        part_df['МПВВ_ПЭИ_Значение'] = base_df['Значение_субшкалы_Психоэмоциональное_истощение']
        part_df['МПВВ_ПЭИ_Уровень'] = base_df['Уровень_субшкалы_Психоэмоциональное_истощение']

        part_df['МПВВ_ДП_Значение'] = base_df['Значение_субшкалы_Деперсонализация']
        part_df['МПВВ_ДП_Уровень'] = base_df['Уровень_субшкалы_Деперсонализация']

        part_df['МПВВ_РЛД_Значение'] = base_df['Значение_субшкалы_Редукция_личных_достижений']
        part_df['МПВВ_РЛД_Уровень'] = base_df['Уровень_субшкалы_Редукция_личных_достижений']

        out_answer_df = pd.concat([out_answer_df, answers_df], axis=1)  # Датафрейм для проверки

        new_order_cols = ['Значение_уровня_психического_выгорания','Уровень_психического_выгорания'
                                  ,'Значение_субшкалы_Психоэмоциональное_истощение','Уровень_субшкалы_Психоэмоциональное_истощение',
                               'Значение_субшкалы_Деперсонализация','Уровень_субшкалы_Деперсонализация',
                               'Значение_субшкалы_Редукция_личных_достижений','Уровень_субшкалы_Редукция_личных_достижений',
                               ]
        base_df = base_df.reindex(columns=new_order_cols)


        # Соединяем анкетную часть с результатной
        base_df = pd.concat([result_df, base_df], axis=1)
        base_df.sort_values(by='Значение_уровня_психического_выгорания', ascending=False, inplace=True)  # сортируем


        # Общий свод по уровням общей шкалы всего в процентном соотношении
        base_svod_all_df = pd.DataFrame(
            index=['крайне низкий уровень', 'низкий уровень',
                   'средний уровень','высокий уровень','крайне высокий уровень'])

        svod_level_df = pd.pivot_table(base_df, index='Уровень_психического_выгорания',
                                       values='Значение_уровня_психического_выгорания',
                                       aggfunc='count')

        svod_level_df['% от общего'] = round(
            svod_level_df['Значение_уровня_психического_выгорания'] / svod_level_df[
                'Значение_уровня_психического_выгорания'].sum(), 3) * 100

        base_svod_all_df = base_svod_all_df.join(svod_level_df)

        # # Создаем суммирующую строку
        base_svod_all_df.loc['Итого'] = svod_level_df.sum()
        base_svod_all_df.reset_index(inplace=True)
        base_svod_all_df.rename(columns={'index': 'Уровень', 'Значение_уровня_психического_выгорания': 'Количество'},
                                inplace=True)
        # формируем основной словарь
        out_dct = {'Списочный результат': base_df, 'Список для проверки': out_answer_df,
                   'Свод Общий': base_svod_all_df,
                   }

        lst_level = ['крайне низкий уровень', 'низкий уровень',
                   'средний уровень','высокий уровень','крайне высокий уровень']
        dct_level = dict()

        for level in lst_level:
            temp_df = base_df[base_df['Уровень_психического_выгорания'] == level]
            if temp_df.shape[0] != 0:
                dct_level[level] = temp_df

        out_dct.update(dct_level)

        # Делаем свод  по  шкалам
        dct_svod_sub = {'Значение_субшкалы_Психоэмоциональное_истощение': 'Уровень_субшкалы_Психоэмоциональное_истощение',
                        'Значение_субшкалы_Деперсонализация': 'Уровень_субшкалы_Деперсонализация',
                        'Значение_субшкалы_Редукция_личных_достижений': 'Уровень_субшкалы_Редукция_личных_достижений',
                        }

        dct_rename_svod_sub = {'Значение_субшкалы_Психоэмоциональное_истощение': 'Психоэмоциональное истощение',
                               'Значение_субшкалы_Деперсонализация': 'Деперсонализация',
                               'Значение_субшкалы_Редукция_личных_достижений': 'Редукция личных достижений',
                               }

        base_svod_sub_df = create_union_svod(base_df, dct_svod_sub, dct_rename_svod_sub, lst_level)

        # считаем среднее значение по субшкалам
        avg_psych_burnout = round(base_df['Значение_уровня_психического_выгорания'].mean(), 1)
        avg_em = round(base_df['Значение_субшкалы_Психоэмоциональное_истощение'].mean(), 1)
        avg_depers = round(base_df['Значение_субшкалы_Деперсонализация'].mean(), 1)
        avg_reduc = round(base_df['Значение_субшкалы_Редукция_личных_достижений'].mean(), 1)

        avg_dct = {'Среднее значение уровня психического выгорания': avg_psych_burnout,
                   'Среднее значение субшкалы Эмоциональное истощение': avg_em,
                   'Среднее значение субшкалы Деперсонализация': avg_depers,
                   'Среднее значение субшкалы Редукция персональных достижений': avg_reduc,
                   }

        avg_df = pd.DataFrame.from_dict(avg_dct, orient='index')
        avg_df = avg_df.reset_index()
        avg_df.columns = ['Показатель', 'Среднее значение']

        out_dct.update({'Свод по субшкалам': base_svod_sub_df,
                        'Среднее по субшкалам': avg_df}
                       )

        """
            Сохраняем в зависимости от необходимости делать своды по определенным колонкам
            """
        if len(lst_svod_cols) == 0:
            return out_dct, part_df
        else:
            out_dct = create_result_mpbv(base_df, out_dct, lst_svod_cols)

            return out_dct, part_df

    except BadOrderMPBV:
        messagebox.showerror('Лахеcис',
                             f'При обработке вопросов теста Профессиональное выгорание Маслач Водопьянова обнаружены неправильные вопросы. Проверьте названия колонок с вопросами:\n'
                             f'{error_order_message[:5000]}\n'
                             f'Используйте при создании Яндекс-формы написание вопросов из руководства пользователя программы Лахесис.')
    except BadValueMPBV:
        messagebox.showerror('Лахеcис',
                             f'При обработке вопросов теста Профессиональное выгорание Маслач Водопьянова обнаружены неправильные варианты ответов. Проверьте ответы на указанных строках:\n'
                             f'{error_message[:5000]}\n'
                             f'Используйте при создании Яндекс-формы написание вариантов ответа из руководства пользователя программы Лахесис.')


    except BadCountColumnsMPBV:
        messagebox.showerror('Лахеcис',
                             f'Проверьте количество колонок с ответами на тест Профессиональное выгорание Маслач Водопьянова\n'
                             f'Должно быть 22 колонки с ответами')








