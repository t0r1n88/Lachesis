"""
Скрипт для обработки результатов теста Школьная тревожность Филлипса
"""

import pandas as pd
import re
from tkinter import messagebox
from lachesis_support_functions import create_union_svod, calc_count_scale,round_mean_two

class BadOrderPHSA(Exception):
    """
    Исключение для обработки случая когда колонки не совпадают
    """
    pass


class BadValuePHSA(Exception):
    """
    Исключение для неправильных значений в вариантах ответов
    """
    pass

class BadCountColumnsPHSA(Exception):
    """
    Исключение для обработки случая если количество колонок не равно 58
    """
    pass



def create_list_on_level_shtf(base_df:pd.DataFrame, out_dct:dict, lst_level:list, dct_prefix:dict):
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
                if level == 'нормальный уровень ШТФ':
                    level = 'нормальный'
                elif level == 'повышенный уровень ШТФ':
                    level = 'повышенный'
                else:
                    level = 'высокий'
                dct_level[f'{dct_prefix[key]}. {level}'] = temp_df
        out_dct.update(dct_level)

    return out_dct




def calc_all_value(row):
    """
    Функция для подсчета значения общей тревожности
    :param row: строка с ответами
    :return: число
    """
    key_lst = ['нет','нет','нет','нет','нет',
               'нет','нет','нет','нет','нет',

               'да','нет','нет','нет','нет',
               'нет','нет','нет','нет','да',

               'нет','да','нет','да','да',
               'нет','нет','нет','нет','да',

               'нет','нет','нет','нет','да',
               'да','нет','да','да','нет',

               'да','нет','да','да','нет',
               'нет','нет','нет','нет','нет',

               'нет','нет','нет','нет','нет',
               'нет','нет','нет'
               ]

    differences_count = sum(x != y for x, y in zip(list(row), key_lst)) # считаем количество отличий
    return differences_count


def calc_level_anxiety(value:int):
    """
    Уровень общей тревожности
    :param value: значение
    :return:
    """
    if value >= 44:
        return 'высокий уровень ШТФ'
    elif value > 29:
        return 'повышенный уровень ШТФ'
    else:
        return 'нормальный уровень ШТФ'


def calc_oth_value(row):
    """
    Фнукция подсчета общей тревожности в школе
    :param row:
    :return:
    """
    key_lst = ['нет','нет',
               'нет','нет',
               'нет','нет',
               'нет','нет',
               'нет','нет',
               'нет','нет',
               'нет','нет',
               'нет','нет',
               'нет','нет',
               'нет','нет',
               'нет','нет',
               ]

    differences_count = sum(x != y for x, y in zip(list(row), key_lst)) # считаем количество отличий
    return differences_count


def calc_level_oth(value:int):
    """
    Уровень общей тревожности в школе
    :param value: значение
    :return:
    """
    if value >= 16:
        return 'высокий уровень ШТФ'
    elif value > 11:
        return 'повышенный уровень ШТФ'
    else:
        return 'нормальный уровень ШТФ'



def calc_pss_value(row):
    """
    Фнукция подсчета переживания социального стресса
    :param row:
    :return:
    """
    key_lst = ['нет','нет',
               'нет', 'да',
               'да', 'да',
               'нет', 'да',
               'да', 'нет',
               'да'
               ]

    differences_count = sum(x != y for x, y in zip(list(row), key_lst)) # считаем количество отличий
    return differences_count


def calc_level_pss(value:int):
    """
    Уровень общей тревожности в школе
    :param value: значение
    :return:
    """
    if value >= 9:
        return 'высокий уровень ШТФ'
    elif value > 5:
        return 'повышенный уровень ШТФ'
    else:
        return 'нормальный уровень ШТФ'


def calc_fpvdu_value(row):
    """
    Фнукция подсчета Фрустрация потребности в достижении успеха
    :param row:
    :return:
    """
    key_lst = ['нет','нет',
               'нет', 'да',
               'нет', 'нет',
               'да', 'нет',
               'нет', 'да',
               'да', 'да',
               'да' ]

    differences_count = sum(x != y for x, y in zip(list(row), key_lst)) # считаем количество отличий
    return differences_count


def calc_level_fpvdu(value:int):
    """
    :param value: значение
    :return:
    """
    if value >= 10:
        return 'высокий уровень ШТФ'
    elif value > 6:
        return 'повышенный уровень ШТФ'
    else:
        return 'нормальный уровень ШТФ'



def calc_ss_value(row):
    """
    Фнукция подсчета Фрустрация потребности в достижении успеха
    :param row:
    :return:
    """
    key_lst = ['нет','нет',
               'нет', 'нет',
               'нет', 'нет'
]

    differences_count = sum(x != y for x, y in zip(list(row), key_lst)) # считаем количество отличий
    return differences_count


def calc_level_ss(value:int):
    """
    :param value: значение
    :return:
    """
    if value >= 5:
        return 'высокий уровень ШТФ'
    elif value > 3:
        return 'повышенный уровень ШТФ'
    else:
        return 'нормальный уровень ШТФ'


def calc_sspz_value(row):
    """
    Фнукция подсчета Страх ситуации проверки знаний
    :param row:
    :return:
    """
    key_lst = ['нет','нет',
               'нет', 'нет',
               'нет', 'нет'
]

    differences_count = sum(x != y for x, y in zip(list(row), key_lst)) # считаем количество отличий
    return differences_count


def calc_level_sspz(value:int):
    """
    :param value: значение
    :return:
    """
    if value >= 5:
        return 'высокий уровень ШТФ'
    elif value > 3:
        return 'повышенный уровень ШТФ'
    else:
        return 'нормальный уровень ШТФ'



def calc_snsoo_value(row):
    """
    Фнукция подсчета Страх не соответствовать ожиданиям окружающих
    :param row:
    :return:
    """
    key_lst = ['нет','нет',
               'нет', 'нет',
               'да'
]

    differences_count = sum(x != y for x, y in zip(list(row), key_lst)) # считаем количество отличий
    return differences_count


def calc_level_snsoo(value:int):
    """
    :param value: значение
    :return:
    """
    if value >= 4:
        return 'высокий уровень ШТФ'
    elif value > 2:
        return 'повышенный уровень ШТФ'
    else:
        return 'нормальный уровень ШТФ'



def calc_nfss_value(row):
    """
    Фнукция подсчета Низкая физиологическая сопротивляемость стрессу
    :param row:
    :return:
    """
    key_lst = ['нет','нет',
               'нет', 'нет',
               'нет'
]

    differences_count = sum(x != y for x, y in zip(list(row), key_lst)) # считаем количество отличий
    return differences_count


def calc_level_nfss(value:int):
    """
    :param value: значение
    :return:
    """
    if value >= 4:
        return 'высокий уровень ШТФ'
    elif value > 2:
        return 'повышенный уровень ШТФ'
    else:
        return 'нормальный уровень ШТФ'



def calc_psou_value(row):
    """
    Фнукция подсчета Проблемы и страхи в отношениях с учителями
    :param row:
    :return:
    """
    key_lst = ['нет','нет',
               'да', 'нет',
               'да', 'да',
               'да', 'нет'
]

    differences_count = sum(x != y for x, y in zip(list(row), key_lst)) # считаем количество отличий
    return differences_count


def calc_level_psou(value:int):
    """
    :param value: значение
    :return:
    """
    if value > 6:
        return 'высокий уровень ШТФ'
    elif value > 4:
        return 'повышенный уровень ШТФ'
    else:
        return 'нормальный уровень ШТФ'



def create_result_shtf(base_df:pd.DataFrame, out_dct:dict, lst_svod_cols:list):
    """
    Функция для подсчета результата если указаны колонки по которым нужно провести свод
    :param df: датафрейм с результатами
    :param out_dct: словарь с уже подсчитанными базовыми данными
    :param lst_svod_cols: список сводных колонок
    :return: словарь
    """
    lst_level = ['нормальный уровень ШТФ','повышенный уровень ШТФ','высокий уровень ШТФ']
    lst_reindex_main_level_cols = lst_svod_cols.copy()
    lst_reindex_main_level_cols.extend( ['нормальный уровень ШТФ','повышенный уровень ШТФ','высокий уровень ШТФ',
                                   'Итого'])  # Основная шкала

    # Интегральные показатели
    svod_count_anxiety_one_level_df = calc_count_scale(base_df, lst_svod_cols,
                                                    'Значение_Тревожность',
                                                    'Уровень_Тревожность',
                                                    lst_reindex_main_level_cols,lst_level)
    svod_count_oth_one_level_df = calc_count_scale(base_df, lst_svod_cols,
                                                    'ОТШ_Значение',
                                                    'ОТШ_Уровень',
                                                    lst_reindex_main_level_cols,lst_level)
    svod_count_pss_one_level_df = calc_count_scale(base_df, lst_svod_cols,
                                                    'ПСС_Значение',
                                                    'ПСС_Уровень',
                                                    lst_reindex_main_level_cols, lst_level)
    svod_count_fpvdu_one_level_df = calc_count_scale(base_df, lst_svod_cols,
                                                    'ФПВДУ_Значение',
                                                    'ФПВДУ_Уровень',
                                                    lst_reindex_main_level_cols, lst_level)
    svod_count_ss_one_level_df = calc_count_scale(base_df, lst_svod_cols,
                                                    'СС_Значение',
                                                    'СС_Уровень',
                                                    lst_reindex_main_level_cols, lst_level)
    svod_count_sspz_one_level_df = calc_count_scale(base_df, lst_svod_cols,
                                                    'ССПЗ_Значение',
                                                    'ССПЗ_Уровень',
                                                    lst_reindex_main_level_cols, lst_level)
    svod_count_snsoo_one_level_df = calc_count_scale(base_df, lst_svod_cols,
                                                    'СНСОО_Значение',
                                                    'СНСОО_Уровень',
                                                    lst_reindex_main_level_cols, lst_level)
    svod_count_nfss_one_level_df = calc_count_scale(base_df, lst_svod_cols,
                                                    'НФСС_Значение',
                                                    'НФСС_Уровень',
                                                    lst_reindex_main_level_cols, lst_level)
    svod_count_psou_one_level_df = calc_count_scale(base_df, lst_svod_cols,
                                                    'ПСОУ_Значение',
                                                    'ПСОУ_Уровень',
                                                    lst_reindex_main_level_cols, lst_level)

    # Считаем среднее по субшкалам
    svod_mean_one_df = pd.pivot_table(base_df,
                                  index=lst_svod_cols,
                                  values=['Значение_Тревожность',
                                          'ОТШ_Значение',
                                          'ПСС_Значение',
                                          'ФПВДУ_Значение',
                                          'СС_Значение',
                                          'ССПЗ_Значение',
                                          'СНСОО_Значение',
                                          'НФСС_Значение',
                                          'ПСОУ_Значение',
                                          ],
                                  aggfunc=round_mean_two)

    svod_mean_one_df.reset_index(inplace=True)
    # упорядочиваем колонки
    new_order_cols = lst_svod_cols.copy()
    new_order_cols.extend((['Значение_Тревожность',
                                          'ОТШ_Значение',
                                          'ПСС_Значение',
                                          'ФПВДУ_Значение',
                                          'СС_Значение',
                                          'ССПЗ_Значение',
                                          'СНСОО_Значение',
                                          'НФСС_Значение',
                                          'ПСОУ_Значение',
                                          ]))

    svod_mean_one_df = svod_mean_one_df.reindex(columns=new_order_cols)
    dct_rename_cols_mean = {'Значение_Тревожность': 'Ср. Тревожность',
                            'ОТШ_Значение': 'Ср. Общая тревожность в школе',
                            'ПСС_Значение': 'Ср. Переживание социального стресса',
                            'ФПВДУ_Значение': 'Ср. Фрустрация потребности в достижении успеха',
                            'СС_Значение': 'Ср. Страх самовыражения',
                            'ССПЗ_Значение': 'Ср. Страх ситуации проверки знаний',
                            'СНСОО_Значение': 'Ср. Страх не соответствовать ожиданиям окружающих',
                            'НФСС_Значение': 'Ср. Низкая физиологическая сопротивляемость стрессу',
                            'ПСОУ_Значение': 'Ср. Проблемы и страхи в отношениях с учителями',
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

    out_dct.update({f'Ср {out_name}':svod_mean_one_df,
                f'Свод Тревожность {out_name}': svod_count_anxiety_one_level_df,
                f'Свод ОТШ {out_name}': svod_count_oth_one_level_df,
                f'Свод ПСС {out_name}': svod_count_pss_one_level_df,
                f'Свод ФПВДУ {out_name}': svod_count_fpvdu_one_level_df,
                f'Свод СС {out_name}': svod_count_ss_one_level_df,
                f'Свод ССПЗ {out_name}': svod_count_sspz_one_level_df,
                f'Свод СНСОО {out_name}': svod_count_snsoo_one_level_df,
                f'Свод НФСС {out_name}': svod_count_nfss_one_level_df,
                f'Свод ПСОУ {out_name}': svod_count_psou_one_level_df,
                    })

    if len(lst_svod_cols) == 1:
        return out_dct
    else:
        for idx, name_column in enumerate(lst_svod_cols):
            lst_reindex_main_column_cols = [lst_svod_cols[idx],'нормальный уровень ШТФ','повышенный уровень ШТФ','высокий уровень ШТФ',
                                   'Итого']  # Основная шкала

            # Интегральные показатели
            svod_count_anxiety_column_level_df = calc_count_scale(base_df, [lst_svod_cols[idx]],
                                                                  'Значение_Тревожность',
                                                                  'Уровень_Тревожность',
                                                                  lst_reindex_main_column_cols, lst_level)
            svod_count_oth_column_level_df = calc_count_scale(base_df, [lst_svod_cols[idx]],
                                                              'ОТШ_Значение',
                                                              'ОТШ_Уровень',
                                                              lst_reindex_main_column_cols, lst_level)
            svod_count_pss_column_level_df = calc_count_scale(base_df, [lst_svod_cols[idx]],
                                                              'ПСС_Значение',
                                                              'ПСС_Уровень',
                                                              lst_reindex_main_column_cols, lst_level)
            svod_count_fpvdu_column_level_df = calc_count_scale(base_df, [lst_svod_cols[idx]],
                                                                'ФПВДУ_Значение',
                                                                'ФПВДУ_Уровень',
                                                                lst_reindex_main_column_cols, lst_level)
            svod_count_ss_column_level_df = calc_count_scale(base_df, [lst_svod_cols[idx]],
                                                             'СС_Значение',
                                                             'СС_Уровень',
                                                             lst_reindex_main_column_cols, lst_level)
            svod_count_sspz_column_level_df = calc_count_scale(base_df, [lst_svod_cols[idx]],
                                                               'ССПЗ_Значение',
                                                               'ССПЗ_Уровень',
                                                               lst_reindex_main_column_cols, lst_level)
            svod_count_snsoo_column_level_df = calc_count_scale(base_df, [lst_svod_cols[idx]],
                                                                'СНСОО_Значение',
                                                                'СНСОО_Уровень',
                                                                lst_reindex_main_column_cols, lst_level)
            svod_count_nfss_column_level_df = calc_count_scale(base_df, [lst_svod_cols[idx]],
                                                               'НФСС_Значение',
                                                               'НФСС_Уровень',
                                                               lst_reindex_main_column_cols, lst_level)
            svod_count_psou_column_level_df = calc_count_scale(base_df, [lst_svod_cols[idx]],
                                                               'ПСОУ_Значение',
                                                               'ПСОУ_Уровень',
                                                               lst_reindex_main_column_cols, lst_level)

            # Считаем среднее по субшкалам
            svod_mean_column_df = pd.pivot_table(base_df,
                                                 index=[lst_svod_cols[idx]],
                                                 values=['Значение_Тревожность',
                                                         'ОТШ_Значение',
                                                         'ПСС_Значение',
                                                         'ФПВДУ_Значение',
                                                         'СС_Значение',
                                                         'ССПЗ_Значение',
                                                         'СНСОО_Значение',
                                                         'НФСС_Значение',
                                                         'ПСОУ_Значение',
                                                         ],
                                                 aggfunc=round_mean_two)

            svod_mean_column_df.reset_index(inplace=True)
            # упорядочиваем колонки
            new_order_cols = [lst_svod_cols[idx]].copy()
            new_order_cols.extend((['Значение_Тревожность',
                                    'ОТШ_Значение',
                                    'ПСС_Значение',
                                    'ФПВДУ_Значение',
                                    'СС_Значение',
                                    'ССПЗ_Значение',
                                    'СНСОО_Значение',
                                    'НФСС_Значение',
                                    'ПСОУ_Значение',
                                    ]))

            svod_mean_column_df = svod_mean_column_df.reindex(columns=new_order_cols)
            dct_rename_cols_mean = {'Значение_Тревожность': 'Ср. Тревожность',
                                    'ОТШ_Значение': 'Ср. Общая тревожность в школе',
                                    'ПСС_Значение': 'Ср. Переживание социального стресса',
                                    'ФПВДУ_Значение': 'Ср. Фрустрация потребности в достижении успеха',
                                    'СС_Значение': 'Ср. Страх самовыражения',
                                    'ССПЗ_Значение': 'Ср. Страх ситуации проверки знаний',
                                    'СНСОО_Значение': 'Ср. Страх не соответствовать ожиданиям окружающих',
                                    'НФСС_Значение': 'Ср. Низкая физиологическая сопротивляемость стрессу',
                                    'ПСОУ_Значение': 'Ср. Проблемы и страхи в отношениях с учителями',
                                    }
            svod_mean_column_df.rename(columns=dct_rename_cols_mean, inplace=True)
            name_column = lst_svod_cols[idx]
            name_column = re.sub(r'[\[\]\'+()<> :"?*|\\/]', '_', name_column)
            name_column = name_column[:15]

            out_dct.update({f'Ср {name_column}': svod_mean_column_df,
                            f'Свод Тревожность {name_column}': svod_count_anxiety_column_level_df,
                            f'Свод ОТШ {name_column}': svod_count_oth_column_level_df,
                            f'Свод ПСС {name_column}': svod_count_pss_column_level_df,
                            f'Свод ФПВДУ {name_column}': svod_count_fpvdu_column_level_df,
                            f'Свод СС {name_column}': svod_count_ss_column_level_df,
                            f'Свод ССПЗ {name_column}': svod_count_sspz_column_level_df,
                            f'Свод СНСОО {name_column}': svod_count_snsoo_column_level_df,
                            f'Свод НФСС {name_column}': svod_count_nfss_column_level_df,
                            f'Свод ПСОУ {name_column}': svod_count_psou_column_level_df,
                            })
        return out_dct











def processing_philips_school_anxiety(result_df: pd.DataFrame, answers_df: pd.DataFrame,lst_svod_cols:list):
    """
    Функция для обработки
    :param base_df: часть датафрейма с описательными колонками
    :param answers_df: часть датафрейма с ответами
    :param lst_svod_cols:  список с колонками по которым нужно делать свод
    """
    try:
        out_answer_df = result_df.copy()  # делаем копию для последующего соединения с сырыми ответами
        if len(answers_df.columns) != 58:  # проверяем количество колонок с вопросами
            raise BadCountColumnsPHSA

        # очищаем названия колонок от возможных сочетаний .1 которые добавляет пандас при одинаковых колонках
        clean_df_lst = []
        for name_column in answers_df.columns:
            clean_name = re.sub(r'.\d+$', '', name_column)
            clean_df_lst.append(clean_name)

        answers_df.columns = clean_df_lst

        lst_check_cols = ['Трудно ли тебе держаться на одном уровне знаний со всем классом?',
                          'Волнуешься ли ты, когда учитель говорит, что собирается проверить, насколько ты знаешь материал?',
                          'Трудно ли тебе работать в классе так, как этого хочет учитель?',
                          'Снится ли тебе временами, что учитель в ярости от того, что ты не знаешь урок?',
                          'Случалось ли, что кто-нибудь из твоего класса бил или ударял тебя?',
                          'Часто ли тебе хочется, чтобы учитель не торопился при объяснении нового материала, пока ты не поймешь, что он говорит?',
                          'Сильно ли ты волнуешься при ответе или выполнении задания?',
                          'Случается ли с тобой, что ты опасаешься высказываться на уроке, потому что боишься сделать глупую ошибку?',
                          'Дрожат ли у тебя колени, когда тебя вызывают отвечать?',
                          'Часто ли твои одноклассники смеются над тобой, когда вы играете в разные игры?',
                          'Случается ли, что тебе ставят более низкую оценку, чем ты ожидал?',
                          'Волнует ли тебя вопрос о том, не оставят ли тебя на второй год?',
                          'Стараешься ли ты избегать игр, в которых делается выбор, потому что тебя, как правило, не выбирают?',
                          'Бывает ли временами, что ты весь дрожишь, когда тебя вызывают отвечать?',
                          'Часто ли у тебя возникает ощущение, что никто из твоих одноклассников не хочет делать то, что хочешь ты?',
                          'Сильно ли ты волнуешься перед тем, как начать выполнять задание?',
                          'Трудно ли тебе получать такие отметки, каких ждут от тебя родители?',
                          'Боишься ли ты временами, что тебе станет дурно в классе?',
                          'Будут ли твои одноклассники смеяться над тобой, если ты сделаешь ошибку при ответе?',
                          'Похож ли ты на своих одноклассников?',
                          'Выполнив задание, беспокоишься ли ты о том, хорошо ли с ним справился?',
                          'Когда ты работаешь в классе, уверен ли ты в том, что все хорошо запомнишь?',
                          'Снится ли тебе иногда, что ты в школе и не можешь ответить на вопрос учителя?',
                          'Верно ли, что большинство ребят относится к тебе по-дружески?',
                          'Работаешь ли ты более усердно, если знаешь, что результаты твоей работы будут сравниваться в классе с результатами твоих одноклассников?',
                          'Часто ли мечтаешь о том, чтобы поменьше волноваться, когда тебя спрашивают?',
                          'Боишься ли ты временами вступать в спор?',
                          'Чувствуешь ли ты, что твое сердце начинает сильно биться, когда учитель говорит, что собирается проверить твою готовность к уроку?',
                          'Когда ты получаешь хорошие отметки, думает ли кто-нибудь из твоих друзей, что ты хочешь выслужиться?',
                          'Хорошо ли ты себя чувствуешь с теми из твоих одноклассников, к которым ребята относятся с особым вниманием?',
                          'Бывает ли, что некоторые ребята в классе говорят что-то, что тебя задевает?',
                          'Как ты думаешь, теряют ли расположение остальных те ученики, которые не справляются с учебой?',
                          'Похоже ли на то, что большинство твоих одноклассников не обращают на тебя внимания?',
                          'Часто ли ты боишься выглядеть нелепо?',
                          'Доволен ли ты тем, как к тебе относятся учителя?',
                          'Помогает ли твоя мама в организации вечеров, как другие мамы твоих одноклассников?',
                          'Волновало ли тебя когда-нибудь, что думают о тебе окружающие?',
                          'Надеешься ли ты в будущем учиться лучше, чем раньше?',
                          'Считаешь ли ты, что одеваешься в школу так же хорошо, как и твои одноклассники?',
                          'Часто ли, отвечая на уроке, ты задумываешься о том, что думают о тебе в это время другие?',
                          'Обладают ли способные ученики какими-то особыми правами, которых нет у других ребят в классе?',
                          'Злятся ли некоторые из твоих одноклассников, когда тебе удается быть лучше их?',
                          'Доволен ли ты тем, как к тебе относятся одноклассники?',
                          'Хорошо ли ты себя чувствуешь, когда остаешься один на один с учителем?',
                          'Высмеивают ли временами одноклассники твою внешность и поведение?',
                          'Думаешь ли ты, что беспокоишься о своих школьных делах больше, чем другие ребята?',
                          'Если ты не можешь ответить, когда тебя спрашивают, чувствуешь ли ты, что вот-вот расплачешься?',
                          'Когда вечером ты лежишь в постели, думаешь ли ты временами с беспокойством о том, что будет завтра в школе?',
                          'Работая над трудным заданием, чувствуешь ли ты порой, что совершенно забыл вещи, которые хорошо знал раньше?',
                          'Дрожит ли слегка твоя рука, когда ты работаешь над заданием?',
                          'Чувствуешь ли ты, что начинаешь нервничать, когда учитель говорит, что собирается дать классу задание?',
                          'Пугает ли тебя проверка твоих знаний в школе?',
                          'Когда учитель говорит, что собирается дать классу задание, чувствуешь ли ты страх, что не справишься с ним?',
                          'Снилось ли тебе временами, что твои одноклассники могут сделать то, что не можешь ты?',
                          'Когда учитель объясняет материал, кажется ли тебе, что твои одноклассники понимают его лучше, чем ты?',
                          'Беспокоишься ли ты по дороге в школу, что учитель может дать классу проверочную работу?',
                          'Когда ты выполняешь задание, чувствуешь ли ты обычно, что делаешь это плохо?',
                          'Дрожит ли слегка твоя рука, когда учитель просит сделать задание на доске перед всем классом?',
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
            raise BadOrderPHSA

        valid_values = ['да','нет']
        # Проверяем, есть ли значения, отличающиеся от указанных в списке
        lst_error_answers = []  # список для хранения строк где найдены неправильные ответы

        for i in range(58):
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
            raise BadValuePHSA

        base_df = pd.DataFrame()
        # Основные шкалы
        base_df['Значение_Тревожность'] = answers_df.apply(calc_all_value, axis=1) # Общая тревожность Значение
        base_df['Уровень_Тревожность'] = base_df['Значение_Тревожность'].apply(calc_level_anxiety) # Уровень общая тревожность

        lst_oth = [2,4,7,12,16,21,23,26,28,46,47,48,49,50,51,52,53,54,55,56,57,58]
        lst_oth = list(map(lambda x:x-1,lst_oth))
        base_df['ОТШ_Значение'] =answers_df.take(lst_oth,axis=1).apply(calc_oth_value,axis=1)
        base_df['ОТШ_Уровень'] = base_df['ОТШ_Значение'].apply(calc_level_oth) # Уровень общая тревожность в школе

        lst_pss = [5,10,15,20,24,30,33,36,39,42,44]
        lst_pss = list(map(lambda x:x-1,lst_pss))
        base_df['ПСС_Значение'] =answers_df.take(lst_pss,axis=1).apply(calc_pss_value,axis=1)
        base_df['ПСС_Уровень'] = base_df['ПСС_Значение'].apply(calc_level_pss) # Уровень переживание социального стресса

        lst_fpvdu = [1,3,6,11,17,19,25,29,32,35,38,41,43]
        lst_fpvdu = list(map(lambda x:x-1,lst_fpvdu))
        base_df['ФПВДУ_Значение'] =answers_df.take(lst_fpvdu,axis=1).apply(calc_fpvdu_value,axis=1)
        base_df['ФПВДУ_Уровень'] = base_df['ФПВДУ_Значение'].apply(calc_level_fpvdu) # Фрустрация потребности в достижении успеха

        lst_ss = [27,31,34,37,40,45]
        lst_ss = list(map(lambda x:x-1,lst_ss))
        base_df['СС_Значение'] =answers_df.take(lst_ss,axis=1).apply(calc_ss_value,axis=1)
        base_df['СС_Уровень'] = base_df['СС_Значение'].apply(calc_level_ss) # Страх самовыражения

        lst_sspz = [2,7,12,16,21,26]
        lst_sspz = list(map(lambda x:x-1,lst_sspz))
        base_df['ССПЗ_Значение'] =answers_df.take(lst_sspz,axis=1).apply(calc_sspz_value,axis=1)
        base_df['ССПЗ_Уровень'] = base_df['ССПЗ_Значение'].apply(calc_level_sspz) # Страх ситуации проверки знаний

        lst_snsoo = [3,8,13,17,22]
        lst_snsoo = list(map(lambda x:x-1,lst_snsoo))
        base_df['СНСОО_Значение'] =answers_df.take(lst_snsoo,axis=1).apply(calc_snsoo_value,axis=1)
        base_df['СНСОО_Уровень'] = base_df['СНСОО_Значение'].apply(calc_level_snsoo) # Страх не соответствовать ожиданиям окружающих

        lst_nfss = [9,14,18,23,28]
        lst_nfss = list(map(lambda x:x-1,lst_nfss))
        base_df['НФСС_Значение'] =answers_df.take(lst_nfss,axis=1).apply(calc_nfss_value,axis=1)
        base_df['НФСС_Уровень'] = base_df['НФСС_Значение'].apply(calc_level_nfss) # Низкая физиологическая сопротивляемость стрессу


        lst_psou = [2,6,11,32,35,41,44,47]
        lst_psou = list(map(lambda x:x-1,lst_psou))
        base_df['ПСОУ_Значение'] =answers_df.take(lst_psou,axis=1).apply(calc_psou_value,axis=1)
        base_df['ПСОУ_Уровень'] = base_df['ПСОУ_Значение'].apply(calc_level_psou) # Проблемы и страхи в отношениях с учителями

        # Создаем датафрейм для создания части в общий датафрейм
        part_df = pd.DataFrame()
        # Общая тревожность
        part_df['ШТФ_Тревожность_Значение'] = base_df['Значение_Тревожность']
        part_df['ШТФ_Тревожность_Уровень'] = base_df['Уровень_Тревожность']
        # Общая тревожность в школе
        part_df['ШТФ_ОТШ_Значение'] = base_df['ОТШ_Значение']
        part_df['ШТФ_ОТШ_Уровень'] = base_df['ОТШ_Уровень']
        # Уровень переживание социального стресса
        part_df['ШТФ_ПСС_Значение'] = base_df['ПСС_Значение']
        part_df['ШТФ_ПСС_Уровень'] = base_df['ПСС_Уровень']
        # Фрустрация потребности в достижении успеха
        part_df['ШТФ_ФПВДУ_Значение'] = base_df['ФПВДУ_Значение']
        part_df['ШТФ_ФПВДУ_Уровень'] = base_df['ФПВДУ_Уровень']
        # Страх самовыражения
        part_df['ШТФ_СС_Значение'] = base_df['СС_Значение']
        part_df['ШТФ_СС_Уровень'] = base_df['СС_Уровень']
        # Страх ситуации проверки знаний
        part_df['ШТФ_ССПЗ_Значение'] = base_df['ССПЗ_Значение']
        part_df['ШТФ_ССПЗ_Уровень'] = base_df['ССПЗ_Уровень']
        # Страх не соответствовать ожиданиям окружающих
        part_df['ШТФ_СНСОО_Значение'] = base_df['СНСОО_Значение']
        part_df['ШТФ_СНСОО_Уровень'] = base_df['СНСОО_Уровень']
        # Низкая физиологическая сопротивляемость стрессу
        part_df['ШТФ_НФСС_Значение'] = base_df['НФСС_Значение']
        part_df['ШТФ_НФСС_Уровень'] = base_df['НФСС_Уровень']
        # Проблемы и страхи в отношениях с учителями
        part_df['ШТФ_ПСОУ_Значение'] = base_df['ПСОУ_Значение']
        part_df['ШТФ_ПСОУ_Уровень'] = base_df['ПСОУ_Уровень']

        out_answer_df = pd.concat([out_answer_df, answers_df], axis=1)  # Датафрейм для проверки
        # Соединяем анкетную часть с результатной
        base_df = pd.concat([result_df, base_df], axis=1)
        base_df.sort_values(by='Значение_Тревожность', ascending=False, inplace=True)  # сортируем

        # формируем основной словарь
        out_dct = {'Списочный результат': base_df, 'Список для проверки': out_answer_df,
                   }

        # Делаем свод по интегральным показателям
        dct_svod_integral = {'Значение_Тревожность': 'Уровень_Тревожность',
                             'ОТШ_Значение': 'ОТШ_Уровень',
                             'ПСС_Значение': 'ПСС_Уровень',
                             'ФПВДУ_Значение': 'ФПВДУ_Уровень',
                             'СС_Значение': 'СС_Уровень',
                             'ССПЗ_Значение': 'ССПЗ_Уровень',
                             'СНСОО_Значение': 'СНСОО_Уровень',
                             'НФСС_Значение': 'НФСС_Уровень',
                             'ПСОУ_Значение': 'ПСОУ_Уровень',
                             }

        dct_rename_svod_integral = {'Значение_Тревожность': 'Тревожность',
                                    'ОТШ_Значение': 'Общая тревожность в школе',
                                    'ПСС_Значение': 'Переживание социального стресса',
                                    'ФПВДУ_Значение': 'Фрустрация потребности в достижении успеха',
                                    'СС_Значение': 'Страх самовыражения',
                                    'ССПЗ_Значение': 'Страх ситуации проверки знаний',
                                    'СНСОО_Значение': 'Страх не соответствовать ожиданиям окружающих',
                                    'НФСС_Значение': 'Низкая физиологическая сопротивляемость стрессу',
                                    'ПСОУ_Значение': 'Проблемы и страхи в отношениях с учителями',
                                    }

        lst_integral = ['нормальный уровень ШТФ', 'повышенный уровень ШТФ', 'высокий уровень ШТФ']

        base_svod_integral_df = create_union_svod(base_df, dct_svod_integral, dct_rename_svod_integral, lst_integral)

        # Интегральные показатели
        avg_anxiety = round(base_df['Значение_Тревожность'].mean(), 2)
        avg_oth = round(base_df['ОТШ_Значение'].mean(), 2)
        avg_pss = round(base_df['ПСС_Значение'].mean(), 2)
        avg_fpvdu = round(base_df['ФПВДУ_Значение'].mean(), 2)
        avg_ss = round(base_df['СС_Значение'].mean(), 2)
        avg_sspz = round(base_df['ССПЗ_Значение'].mean(), 2)
        avg_snsoo = round(base_df['СНСОО_Значение'].mean(), 2)
        avg_nfss = round(base_df['НФСС_Значение'].mean(), 2)
        avg_psou = round(base_df['ПСОУ_Значение'].mean(), 2)

        avg_dct = {'Среднее значение Тревожности': avg_anxiety,
                   'Среднее значение Общая тревожность в школе': avg_oth,
                   'Среднее значение Переживание социального стресса': avg_pss,
                   'Среднее значение Фрустрация потребности в достижении успеха': avg_fpvdu,
                   'Среднее значение Страх самовыражения': avg_ss,
                   'Среднее значение Страх ситуации проверки знаний': avg_sspz,
                   'Среднее значение Страх не соответствовать ожиданиям окружающих': avg_snsoo,
                   'Среднее значение Низкая физиологическая сопротивляемость стрессу': avg_nfss,
                   'Среднее значение Проблемы и страхи в отношениях с учителями': avg_psou
                   }

        avg_df = pd.DataFrame.from_dict(avg_dct, orient='index')
        avg_df = avg_df.reset_index()
        avg_df.columns = ['Показатель', 'Среднее значение']

        out_dct.update({'Свод Факторы': base_svod_integral_df,
                        'Среднее Факторы': avg_df}
                       )

        dct_prefix = {'Уровень_Тревожность': 'Тревожность',
                      'ОТШ_Уровень': 'ОТШ',
                      'ПСС_Уровень': 'ПСС',
                      'ФПВДУ_Уровень': 'ФПВДУ',
                      'СС_Уровень': 'СС',
                      'ССПЗ_Уровень': 'ССПЗ',
                      'СНСОО_Уровень': 'СНСОО',
                      'НФСС_Уровень': 'НФСС',
                      'ПСОУ_Уровень': 'ПСОУ',
                      }

        out_dct = create_list_on_level_shtf(base_df, out_dct, lst_integral, dct_prefix)

        """
            Сохраняем в зависимости от необходимости делать своды по определенным колонкам
            """
        if len(lst_svod_cols) == 0:
            return out_dct, part_df
        else:
            out_dct = create_result_shtf(base_df, out_dct, lst_svod_cols)

            return out_dct, part_df
    except BadOrderPHSA:
        messagebox.showerror('Лахеcис',
                             f'При обработке вопросов теста Школьная тревожность Филлипс обнаружены неправильные вопросы. Проверьте названия колонок с вопросами:\n'
                             f'{error_order_message}\n'
                             f'Используйте при создании Яндекс-формы написание вопросов из руководства пользователя программы Лахесис.')
    except BadValuePHSA:
        messagebox.showerror('Лахеcис',
                             f'При обработке вопросов теста Школьная тревожность Филлипс обнаружены неправильные варианты ответов. Проверьте ответы на указанных строках:\n'
                             f'{error_message}\n'
                             f'Используйте при создании Яндекс-формы написание вариантов ответа из руководства пользователя программы Лахесис.')


    except BadCountColumnsPHSA:
        messagebox.showerror('Лахеcис',
                             f'Проверьте количество колонок с ответами на тест Школьная тревожность Филлипс\n'
                             f'Должно быть 58 колонок с ответами')


























