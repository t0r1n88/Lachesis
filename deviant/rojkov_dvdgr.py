"""
Скрипт для обработки результатов Методика первичной диагностики и выявления детей «группы риска М.И. Рожков, М.А. Ковальчук

"""

import pandas as pd
import re
from tkinter import messagebox
from lachesis_support_functions import round_mean_two,calc_count_scale,create_union_svod, create_list_on_level

class BadOrderDVDGRRK(Exception):
    """
    Исключение для обработки случая когда колонки не совпадают
    """
    pass


class BadValueDVDGRRK(Exception):
    """
    Исключение для неправильных значений в вариантах ответов
    """
    pass

class BadCountColumnsDVDGRRK(Exception):
    """
    Исключение для обработки случая если количество колонок не равно 74
    """
    pass


def calc_value_os(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [5,6,21,22,25,28,29,37,
              38,39,45,46,53,54,66,67,71]
    lst_neg = [22]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_pr:
            if idx not in lst_neg:
                if value == 'да':
                    value_forward += 1
            else:
                if value == 'нет':
                    value_forward += 1

    return value_forward


def calc_level_os(value):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """
    if value < 8:
        return f'норма'
    else:
        return f'группа риска'



def calc_value_a(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [13,14,19,20,
              35,36,42,57,58,64,65]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_pr:
            if value == 'да':
                value_forward += 1

    return value_forward


def calc_level_a(value):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """
    if value < 6:
        return f'норма'
    else:
        return f'группа риска'


def calc_value_nl(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [1,2,3,4,15,16,17,18,
              34,43,44,59,63,72]
    lst_neg = [1,3,17,59]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_pr:
            if idx not in lst_neg:
                if value == 'да':
                    value_forward += 1
            else:
                if value == 'нет':
                    value_forward += 1

    return value_forward


def calc_level_nl(value):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """
    if value < 7:
        return f'норма'
    else:
        return f'группа риска'


def calc_value_ns(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [7,8,23,24,30,31,32,33,
              40,41,47,55,56,68,69,73]
    lst_neg = [23]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_pr:
            if idx not in lst_neg:
                if value == 'да':
                    value_forward += 1
            else:
                if value == 'нет':
                    value_forward += 1

    return value_forward


def calc_level_ns(value):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """
    if value < 7:
        return f'норма'
    else:
        return f'группа риска'


def calc_value_g(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [48,49,60,74]
    lst_neg = [60]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_pr:
            if idx not in lst_neg:
                if value == 'да':
                    value_forward += 1
            else:
                if value == 'нет':
                    value_forward += 1

    return value_forward


def calc_level(value):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """
    if value < 3:
        return f'норма'
    else:
        return f'группа риска'




def calc_value_i(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [9,10,50,61]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_pr:
            if value == 'да':
                value_forward += 1

    return value_forward

def calc_value_sh(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [26,27,51,70]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_pr:
            if value == 'да':
                value_forward += 1

    return value_forward

def calc_value_al(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [11,12,52,62]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_pr:
            if value == 'да':
                value_forward += 1

    return value_forward



def create_result_dvdgr_roj_kov(base_df:pd.DataFrame, out_dct:dict, lst_svod_cols:list):
    """
    Функция для подсчета результата если указаны колонки по которым нужно провести свод
    :param df: датафрейм с результатами
    :param out_dct: словарь с уже подсчитанными базовыми данными
    :param lst_svod_cols: список сводных колонок
    :return: словарь
    """
    lst_level = ['норма', 'группа риска']

    lst_reindex_one_level_cols = lst_svod_cols.copy()
    lst_reindex_one_level_cols.extend(['норма', 'группа риска',
                                       'Итого'])  # Основная шкала

    # АД
    svod_count_one_level_os_df = calc_count_scale(base_df, lst_svod_cols,
                                                 'ОС_Значение',
                                                 'ОС_Уровень',
                                                 lst_reindex_one_level_cols, lst_level)
    # АВА
    svod_count_one_level_a_df = calc_count_scale(base_df, lst_svod_cols,
                                                 'А_Значение',
                                                 'А_Уровень',
                                                 lst_reindex_one_level_cols, lst_level)
    # ИЗ
    svod_count_one_level_nl_df = calc_count_scale(base_df, lst_svod_cols,
                                                 'НЛ_Значение',
                                                 'НЛ_Уровень',
                                                 lst_reindex_one_level_cols, lst_level)
    # АД
    svod_count_one_level_ns_df = calc_count_scale(base_df, lst_svod_cols,
                                                 'НС_Значение',
                                                 'НС_Уровень',
                                                 lst_reindex_one_level_cols, lst_level)

    # АВА
    svod_count_one_level_g_df = calc_count_scale(base_df, lst_svod_cols,
                                                 'Г_Значение',
                                                 'Г_Уровень',
                                                 lst_reindex_one_level_cols, lst_level)
    # ИЗ
    svod_count_one_level_i_df = calc_count_scale(base_df, lst_svod_cols,
                                                 'И_Значение',
                                                 'И_Уровень',
                                                 lst_reindex_one_level_cols, lst_level)
    # АВА
    svod_count_one_level_sh_df = calc_count_scale(base_df, lst_svod_cols,
                                                 'Ш_Значение',
                                                 'Ш_Уровень',
                                                 lst_reindex_one_level_cols, lst_level)
    # ИЗ
    svod_count_one_level_al_df = calc_count_scale(base_df, lst_svod_cols,
                                                 'ЭЛ_Значение',
                                                 'ЭЛ_Уровень',
                                                 lst_reindex_one_level_cols, lst_level)

    # Считаем среднее по субшкалам
    svod_mean_one_df = pd.pivot_table(base_df,
                                      index=lst_svod_cols,
                                      values=['ОС_Значение',
                                              'А_Значение',
                                              'НЛ_Значение',
                                              'НС_Значение',

                                              'Г_Значение',
                                              'И_Значение',
                                              'Ш_Значение',
                                              'ЭЛ_Значение',
                                              ],
                                      aggfunc=round_mean_two)
    svod_mean_one_df.reset_index(inplace=True)

    # упорядочиваем колонки
    new_order_cols = lst_svod_cols.copy()
    new_order_cols.extend((['ОС_Значение',
                            'А_Значение',
                            'НЛ_Значение',
                            'НС_Значение',

                            'Г_Значение',
                            'И_Значение',
                            'Ш_Значение',
                            'ЭЛ_Значение',
                            ]))
    svod_mean_one_df = svod_mean_one_df.reindex(columns=new_order_cols)

    dct_rename_cols_mean = {'ОС_Значение': 'Ср. Отношения в семье',
                            'А_Значение': 'Ср. Агрессивность',
                            'НЛ_Значение': 'Ср. Недоверие к людям',
                            'НС_Значение': 'Ср. Неуверенность в себе',

                            'Г_Значение': 'Ср. Гипертимная акцентуация',
                            'И_Значение': 'Ср. Истероидная акцентуация',
                            'Ш_Значение': 'Ср. Шизоидная акцентуация',
                            'ЭЛ_Значение': 'Ср. Эмоционально-лабильная акцентуация',
                            }
    svod_mean_one_df.rename(columns=dct_rename_cols_mean, inplace=True)

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
                    f'ОС {out_name}': svod_count_one_level_os_df,
                    f'А {out_name}': svod_count_one_level_a_df,
                    f'НЛ {out_name}': svod_count_one_level_nl_df,
                    f'НС {out_name}': svod_count_one_level_ns_df,

                    f'Г {out_name}': svod_count_one_level_g_df,
                    f'И {out_name}': svod_count_one_level_i_df,
                    f'Ш {out_name}': svod_count_one_level_sh_df,
                    f'ЭЛ {out_name}': svod_count_one_level_al_df,
                    })

    if len(lst_svod_cols) == 1:
        return out_dct
    else:
        for idx, name_column in enumerate(lst_svod_cols):
            lst_reindex_column_level_cols = [lst_svod_cols[idx], 'норма', 'группа риска',
                                             'Итого']

            # АД
            svod_count_column_level_os_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                             'ОС_Значение',
                                                             'ОС_Уровень',
                                                             lst_reindex_column_level_cols, lst_level)
            # АВА
            svod_count_column_level_a_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                            'А_Значение',
                                                            'А_Уровень',
                                                            lst_reindex_column_level_cols, lst_level)
            # ИЗ
            svod_count_column_level_nl_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                             'НЛ_Значение',
                                                             'НЛ_Уровень',
                                                             lst_reindex_column_level_cols, lst_level)
            # АД
            svod_count_column_level_ns_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                             'НС_Значение',
                                                             'НС_Уровень',
                                                             lst_reindex_column_level_cols, lst_level)

            # АВА
            svod_count_column_level_g_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                            'Г_Значение',
                                                            'Г_Уровень',
                                                            lst_reindex_column_level_cols, lst_level)
            # ИЗ
            svod_count_column_level_i_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                            'И_Значение',
                                                            'И_Уровень',
                                                            lst_reindex_column_level_cols, lst_level)
            # АВА
            svod_count_column_level_sh_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                             'Ш_Значение',
                                                             'Ш_Уровень',
                                                             lst_reindex_column_level_cols, lst_level)
            # ИЗ
            svod_count_column_level_al_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                             'ЭЛ_Значение',
                                                             'ЭЛ_Уровень',
                                                             lst_reindex_column_level_cols, lst_level)

            # Считаем среднее по субшкалам
            svod_mean_column_df = pd.pivot_table(base_df,
                                                 index=[lst_svod_cols[idx]],
                                                 values=['ОС_Значение',
                                                         'А_Значение',
                                                         'НЛ_Значение',
                                                         'НС_Значение',

                                                         'Г_Значение',
                                                         'И_Значение',
                                                         'Ш_Значение',
                                                         'ЭЛ_Значение',
                                                         ],
                                                 aggfunc=round_mean_two)
            svod_mean_column_df.reset_index(inplace=True)

            # упорядочиваем колонки
            new_order_cols = [lst_svod_cols[idx]].copy()
            new_order_cols.extend((['ОС_Значение',
                                    'А_Значение',
                                    'НЛ_Значение',
                                    'НС_Значение',

                                    'Г_Значение',
                                    'И_Значение',
                                    'Ш_Значение',
                                    'ЭЛ_Значение',
                                    ]))
            svod_mean_column_df = svod_mean_column_df.reindex(columns=new_order_cols)

            dct_rename_cols_mean = {'ОС_Значение': 'Ср. Отношения в семье',
                                    'А_Значение': 'Ср. Агрессивность',
                                    'НЛ_Значение': 'Ср. Недоверие к людям',
                                    'НС_Значение': 'Ср. Неуверенность в себе',

                                    'Г_Значение': 'Ср. Гипертимная акцентуация',
                                    'И_Значение': 'Ср. Истероидная акцентуация',
                                    'Ш_Значение': 'Ср. Шизоидная акцентуация',
                                    'ЭЛ_Значение': 'Ср. Эмоционально-лабильная акцентуация',
                                    }
            svod_mean_column_df.rename(columns=dct_rename_cols_mean, inplace=True)

            # Готовим наименование
            name_column = lst_svod_cols[idx]
            name_column = re.sub(r'[\[\]\'+()<> :"?*|\\/]', '_', name_column)
            name_column = name_column[:15]

            out_dct.update({f'Ср {name_column}': svod_mean_column_df,
                            f'ОС {name_column}': svod_count_column_level_os_df,
                            f'А {name_column}': svod_count_column_level_a_df,
                            f'НЛ {name_column}': svod_count_column_level_nl_df,
                            f'НС {name_column}': svod_count_column_level_ns_df,

                            f'Г {name_column}': svod_count_column_level_g_df,
                            f'И {name_column}': svod_count_column_level_i_df,
                            f'Ш {name_column}': svod_count_column_level_sh_df,
                            f'ЭЛ {name_column}': svod_count_column_level_al_df,
                            })
        return out_dct








def processing_dvdgr_roj_kov(base_df: pd.DataFrame, answers_df: pd.DataFrame, lst_svod_cols:list):
    """
    Функция для обработки
    :param base_df: часть датафрейма с описательными колонками
    :param answers_df: часть датафрейма с ответами
    :param lst_svod_cols:  список с колонками по которым нужно делать свод
    """
    try:
        out_answer_df = base_df.copy()  # делаем копию для последующего соединения с сырыми ответами


        if len(answers_df.columns) != 74:  # проверяем количество колонок с вопросами
            raise BadCountColumnsDVDGRRK

        # очищаем названия колонок от возможных сочетаний .1 которые добавляет пандас при одинаковых колонках
        clean_df_lst = []
        for name_column in answers_df.columns:
            clean_name = re.sub(r'.\d+$', '', name_column)
            clean_df_lst.append(clean_name)

        answers_df.columns = clean_df_lst

        lst_check_cols = ['Считаешь ли ты, то людям можно доверять?',
                          'Думаешь ли ты, что единственный способ достичь чего-то в жизни – это заботиться прежде всего о себе?',
                          'Легко ли ты заводишь друзей?',
                          'Трудно ли тебе говорить людям «нет»?',
                          'Часто ли кто-нибудь из родителей несправедливо критикует тебя?',
                          'Бывает ли так, что твои родители возражают против друзей, с которыми ты встречаешься?',
                          'Часто ли ты нервничаешь?',
                          'Бывают ли у тебя беспричинные колебания настроения?',
                          'Являешься ли ты обычно центром внимания в компании сверстников?',
                          'Можешь ли ты быть приветливым даже с теми, кого явно не любишь?',

                          'Ты не любишь, когда тебя критикуют?',
                          'Можешь ли ты быть откровенным с близкими друзьями?',
                          'Раздражаешься ли ты иногда настолько, что начинаешь кидаться предметами?',
                          'Способен ли ты на грубые шутки?',
                          'Часто ли у тебя возникает чувство, что тебя не понимают?',
                          'Бывает ли у тебя чувство, что за твоей спиной люди говорят о тебе плохо?',
                          'Много ли у тебя близких друзей?',
                          'Стесняешься ли ты обращаться к людям за помощью?',
                          'Нравится ли тебе нарушать установленные правила?',
                          'Бывает ли у тебя иногда желание причинять вред другим людям?',

                          'Раздражают ли тебя родители?',
                          'Всегда ли дома ты обеспечен всем жизненно необходимым?',
                          'Ты всегда уверен в себе?',
                          'Ты обычно вздрагиваешь при необычном звуке?',
                          'Кажется ли тебе, что твои родители тебя не понимают?',
                          'Свои неудачи ты переживаешь сам?',
                          'Бывает ли, что, когда ты остаешься один, твое настроение улучшается?',
                          'Кажется ли тебе, что у твоих друзей более счастливая семья, чем у тебя?',
                          'Чувствуешь ли ты себя несчастным из-за недостатка денег в семье?',
                          'Бывает, что ты злишься на всех?',

                          'Часто ли ты чувствуешь себя беззащитным?',
                          'Легко ли ты осваиваешься в новом коллективе?',
                          'Трудно ли тебе отвечать в школе перед всем классом?',
                          'Есть ли у тебя знакомые, которых ты вообще не можешь переносить?',
                          'Можешь ли ты ударить человека?',
                          'Ты иногда угрожаешь людям?',
                          'Часто ли родители наказывали тебя?',
                          'Появлялось ли у тебя когда-нибудь сильное желание убежать из дома?',
                          'Думаешь ли ты, что твои родители часто обходятся с тобой как с ребенком?',
                          'Часто ли ты чувствуешь себя несчастным?',

                          'Легко ли ты можешь рассердиться?',
                          'Рискнул бы ты схватить за уздечку бегущую лошадь?',
                          'Считаешь ли ты, что есть много глупых моральных норм поведения?',
                          'Страдаешь ли ты от робости и застенчивости?',
                          'Испытывал ли ты чувство, что тебя недостаточно любят в семье?',
                          'Твои родители живут отдельно от тебя?',
                          'Часто ли ты теряешь уверенность в себе из-за внешнего вида?',
                          'Часто ли у тебя бывает веселое и беззаботное настроение?',
                          'Ты подвижный человек?',
                          'Любят ли тебя твои знакомые, друзья?',

                          'Бывает ли, что твои родители тебя не понимают и кажутся тебе чужими?',
                          'При неудачах бывает ли у тебя желание убежать куда-нибудь подальше и не возвращаться?',
                          'Бывало ли, что кто-то из родителей вызывал у тебя чувство страха?',
                          'Критикуют ли родители твой внешний вид?',
                          'Завидуешь ли ты иногда счастью других?',
                          'Часто ли ты чувствуешь себя одиноким, даже находясь среди людей?',
                          'Есть ли люди, которых ты ненавидишь по-настоящему?',
                          'Часто ли ты дерешься?',
                          'Легко ли ты просишь помощи у другого человека?',
                          'Легко ли тебе усидеть на месте?',

                          'Ты охотно отвечаешь у доски в школе?',
                          'Бывает ли, что ты так расстроен, что долго не можешь уснуть?',
                          'Часто ли ты обнаруживал, что твой приятель тебя обманул?',
                          'Часто ли ты ругаешься?',
                          'Мог бы ты без тренировки управлять парусной лодкой?',
                          'Часто ли в вашей семье бывают ссоры?',
                          'Является ли один из твоих родителей очень нервным?',
                          'Часто ли ты чувствуешь ты себя ничтожным?',
                          'Беспокоит ли тебя ощущение, что люди могут угадать твои мысли?',
                          'Ты всегда делаешь все по-своему?',

                          'Бывают ли твои родители чересчур строги к тебе?',
                          'Стесняешься ли ты в обществе малознакомых людей?',
                          'Часто ли тебе кажется, что ты чем-то хуже других?',
                          'Легко ли тебе удается поднять настроение друзей?',
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
            raise BadOrderDVDGRRK

        valid_values = ['да','нет']
        # Проверяем, есть ли значения, отличающиеся от указанных в списке
        lst_error_answers = []  # список для хранения строк где найдены неправильные ответы

        for i in range(74):
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
            raise BadValueDVDGRRK

        base_df['ОС_Значение'] = answers_df.apply(calc_value_os, axis=1)
        base_df['ОС_Уровень'] = base_df['ОС_Значение'].apply(calc_level_os)

        base_df['А_Значение'] = answers_df.apply(calc_value_a, axis=1)
        base_df['А_Уровень'] = base_df['А_Значение'].apply(calc_level_a)

        base_df['НЛ_Значение'] = answers_df.apply(calc_value_nl, axis=1)
        base_df['НЛ_Уровень'] = base_df['НЛ_Значение'].apply(calc_level_nl)

        base_df['НС_Значение'] = answers_df.apply(calc_value_ns, axis=1)
        base_df['НС_Уровень'] = base_df['НС_Значение'].apply(calc_level_ns)

        base_df['Г_Значение'] = answers_df.apply(calc_value_g, axis=1)
        base_df['Г_Уровень'] = base_df['Г_Значение'].apply(calc_level)

        base_df['И_Значение'] = answers_df.apply(calc_value_i, axis=1)
        base_df['И_Уровень'] = base_df['И_Значение'].apply(calc_level)

        base_df['Ш_Значение'] = answers_df.apply(calc_value_sh, axis=1)
        base_df['Ш_Уровень'] = base_df['Ш_Значение'].apply(calc_level)

        base_df['ЭЛ_Значение'] = answers_df.apply(calc_value_al, axis=1)
        base_df['ЭЛ_Уровень'] = base_df['ЭЛ_Значение'].apply(calc_level)

        # Создаем датафрейм для создания части в общий датафрейм
        part_df = pd.DataFrame()

        # Основные шкалы
        part_df['ДВДГРРК_ОС_Значение'] = base_df['ОС_Значение']
        part_df['ДВДГРРК_ОС_Уровень'] = base_df['ОС_Уровень']

        part_df['ДВДГРРК_А_Значение'] = base_df['А_Значение']
        part_df['ДВДГРРК_А_Уровень'] = base_df['А_Уровень']

        part_df['ДВДГРРК_НЛ_Значение'] = base_df['НЛ_Значение']
        part_df['ДВДГРРК_НЛ_Уровень'] = base_df['НЛ_Уровень']

        part_df['ДВДГРРК_НС_Значение'] = base_df['НС_Значение']
        part_df['ДВДГРРК_НС_Уровень'] = base_df['НС_Уровень']

        part_df['ДВДГРРК_Г_Значение'] = base_df['Г_Значение']
        part_df['ДВДГРРК_Г_Уровень'] = base_df['Г_Уровень']

        part_df['ДВДГРРК_И_Значение'] = base_df['И_Значение']
        part_df['ДВДГРРК_И_Уровень'] = base_df['И_Уровень']

        part_df['ДВДГРРК_Ш_Значение'] = base_df['Ш_Значение']
        part_df['ДВДГРРК_Ш_Уровень'] = base_df['Ш_Уровень']

        out_answer_df = pd.concat([out_answer_df, answers_df], axis=1)  # Датафрейм для проверки

        base_df.sort_values(by='А_Значение', ascending=False, inplace=True)  # сортируем

        # Делаем свод  по  шкалам
        dct_svod_sub = {'ОС_Значение': 'ОС_Уровень',
                        'А_Значение': 'А_Уровень',
                        'НЛ_Значение': 'НЛ_Уровень',
                        'НС_Значение': 'НС_Уровень',

                        'Г_Значение': 'Г_Уровень',
                        'И_Значение': 'И_Уровень',
                        'Ш_Значение': 'Ш_Уровень',
                        'ЭЛ_Значение': 'ЭЛ_Уровень',
                        }

        dct_rename_svod_sub = {'ОС_Значение': 'Отношения в семье',
                               'А_Значение': 'Агрессивность',
                               'НЛ_Значение': 'Недоверие к людям',
                               'НС_Значение': 'Неуверенность в себе',

                               'Г_Значение': 'Гипертимная акцентуация',
                               'И_Значение': 'Истероидная акцентуация',
                               'Ш_Значение': 'Шизоидная акцентуация',
                               'ЭЛ_Значение': 'Эмоционально-лабильная акцентуация',
                               }

        lst_sub = ['норма', 'группа риска']

        base_svod_sub_df = create_union_svod(base_df, dct_svod_sub, dct_rename_svod_sub, lst_sub)

        avg_os = round(base_df['ОС_Значение'].mean(), 2)
        avg_a = round(base_df['А_Значение'].mean(), 2)
        avg_nl = round(base_df['НЛ_Значение'].mean(), 2)
        avg_ns = round(base_df['НС_Значение'].mean(), 2)

        avg_g = round(base_df['Г_Значение'].mean(), 2)
        avg_i = round(base_df['И_Значение'].mean(), 2)
        avg_sh = round(base_df['Ш_Значение'].mean(), 2)
        avg_al = round(base_df['ЭЛ_Значение'].mean(), 2)

        avg_dct = {'Среднее значение показателя Отношения в семье': avg_os,
                   'Среднее значение показателя Агрессивность': avg_a,
                   'Среднее значение показателя Недоверие к людям': avg_nl,
                   'Среднее значение показателя Неуверенность в себе': avg_ns,

                   'Среднее значение показателя Гипертимная акцентуация': avg_g,
                   'Среднее значение показателя Истероидная акцентуация': avg_i,
                   'Среднее значение показателя Шизоидная акцентуация': avg_sh,
                   'Среднее значение показателя Эмоционально-лабильная акцентуация': avg_al,
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

        dct_prefix = {'ОС_Уровень': 'ОС',
                      'А_Уровень': 'А',
                      'НЛ_Уровень': 'НЛ',
                      'НС_Уровень': 'НС',

                      'Г_Уровень': 'Г',
                      'И_Уровень': 'И',
                      'Ш_Уровень': 'Ш',
                      'ЭЛ_Уровень': 'ЭЛ',
                      }

        out_dct = create_list_on_level(base_df, out_dct, lst_sub, dct_prefix)
        """
                        Сохраняем в зависимости от необходимости делать своды по определенным колонкам
                        """
        if len(lst_svod_cols) == 0:
            return out_dct, part_df

        else:
            out_dct = create_result_dvdgr_roj_kov(base_df, out_dct, lst_svod_cols)
            return out_dct, part_df

    except BadOrderDVDGRRK:
        messagebox.showerror('Лахеcис',
                             f'При обработке вопросов теста Методика первичной диагностики и выявления детей «группы риска Рожков Ковальчук обнаружены неправильные вопросы. Проверьте названия колонок с вопросами:\n'
                             f'{error_order_message[:5000]}\n'
                             f'Используйте при создании Яндекс-формы написание вопросов из руководства пользователя программы Лахесис.')
    except BadValueDVDGRRK:
        messagebox.showerror('Лахеcис',
                             f'При обработке вопросов теста Методика первичной диагностики и выявления детей «группы риска Рожков Ковальчук обнаружены неправильные варианты ответов. Проверьте ответы на указанных строках:\n'
                             f'{error_message[:5000]}\n'
                             f'Используйте при создании Яндекс-формы написание вариантов ответа из руководства пользователя программы Лахесис.')


    except BadCountColumnsDVDGRRK:
        messagebox.showerror('Лахеcис',
                             f'Проверьте количество колонок с ответами на тест Методика первичной диагностики и выявления детей «группы риска Рожков Ковальчук\n'
                             f'Должно быть 74 колонки с ответами')











