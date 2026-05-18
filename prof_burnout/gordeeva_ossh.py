"""
Скрипт для обработки результатов Опросник Ситуации в школе Гордеева, Сычев
"""

import pandas as pd
import re
from tkinter import messagebox
from lachesis_support_functions import round_mean_two,calc_count_scale,create_union_svod, create_list_on_level

class BadOrderOSSHGS(Exception):
    """
    Исключение для обработки случая когда колонки не совпадают
    """
    pass


class BadValueOSSHGS(Exception):
    """
    Исключение для неправильных значений в вариантах ответов
    """
    pass

class BadCountColumnsOSSHGS(Exception):
    """
    Исключение для обработки случая если количество колонок не равно 60
    """
    pass

def calc_level(value):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """
    if 1<= value < 2:
        return f'1-1.99'
    elif 2 <= value < 3:
        return f'2-2.99'
    elif 3 <= value < 4:
        return f'3-3.99'
    elif 4 <= value < 5:
        return f'4-4.99'
    elif 5 <= value < 6:
        return f'5-5.99'
    else:
        return f'6-7'


def calc_value_pa(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [4,7,12,16,19,21,26,29,36,38,41,45,51,55,59]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_pr:
            value_forward += value
    return round(value_forward / len(lst_pr),2)


def calc_value_ss(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [1,5,9,15,18,23,28,31,34,39,44,46,50,54,58]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_pr:
            value_forward += value
    return round(value_forward / len(lst_pr),2)


def calc_value_cs(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [3,8,11,14,17,22,27,30,33,37,42,48,49,53,57]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_pr:
            value_forward += value
    return round(value_forward / len(lst_pr),2)

def calc_value_hs(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [2,6,10,13,20,24,25,32,35,40,43,47,52,56,60]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_pr:
            value_forward += value
    return round(value_forward / len(lst_pr),2)


def calc_value_vs(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [4,19,41,55,59]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_pr:
            value_forward += value
    return round(value_forward / len(lst_pr),2)

def calc_value_ps(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [7,12,16,21,26,29,36,38,45,51]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_pr:
            value_forward += value
    return round(value_forward / len(lst_pr),2)


def calc_value_ns(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [15,18,23,28,31,34,50,54]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_pr:
            value_forward += value
    return round(value_forward / len(lst_pr),2)


def calc_value_obs(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [1,5,9,39,44,46,58]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_pr:
            value_forward += value
    return round(value_forward / len(lst_pr),2)

def calc_value_ts(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [3,8,11,17,22,37,49,57]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_pr:
            value_forward += value
    return round(value_forward / len(lst_pr),2)


def calc_value_ds(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [14,27,30,33,42,48,53]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_pr:
            value_forward += value
    return round(value_forward / len(lst_pr),2)

def calc_value_ots(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [20,24,25,32,35,40,47,52,56,60]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_pr:
            value_forward += value
    return round(value_forward / len(lst_pr),2)

def calc_value_ogs(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [2,6,10,13,43]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_pr:
            value_forward += value
    return round(value_forward / len(lst_pr),2)


def create_str(row:pd.Series):
    """
    Функция для соединения через дефис
    :param row:
    :return:
    """
    row = list(map(lambda x:str(round(x)),row.tolist()))
    return '-'.join(row)



def create_result_ossh_gordeeva(base_df:pd.DataFrame, out_dct:dict, lst_svod_cols:list):
    """
    Функция для подсчета результата если указаны колонки по которым нужно провести свод
    :param df: датафрейм с результатами
    :param out_dct: словарь с уже подсчитанными базовыми данными
    :param lst_svod_cols: список сводных колонок
    :return: словарь
    """

    lst_level = ['1-1.99', '2-2.99', '3-3.99', '4-4.99','5-5.99','6-7']

    lst_reindex_one_level_cols = lst_svod_cols.copy()
    lst_reindex_one_level_cols.extend(['1-1.99', '2-2.99', '3-3.99', '4-4.99','5-5.99','6-7',
                                       'Итого'])  # Основная шкала

    # АД
    svod_count_one_level_pa_df = calc_count_scale(base_df, lst_svod_cols,
                                                 'ПА_Значение',
                                                 'ПА_Диапазон',
                                                 lst_reindex_one_level_cols, lst_level)

    # АД
    svod_count_one_level_ss_df = calc_count_scale(base_df, lst_svod_cols,
                                                 'СС_Значение',
                                                 'СС_Диапазон',
                                                 lst_reindex_one_level_cols, lst_level)

    # АД
    svod_count_one_level_cs_df = calc_count_scale(base_df, lst_svod_cols,
                                                 'КС_Значение',
                                                 'КС_Диапазон',
                                                 lst_reindex_one_level_cols, lst_level)

    # АД
    svod_count_one_level_hs_df = calc_count_scale(base_df, lst_svod_cols,
                                                 'ХС_Значение',
                                                 'ХС_Диапазон',
                                                 lst_reindex_one_level_cols, lst_level)

    # АД
    svod_count_one_level_vs_df = calc_count_scale(base_df, lst_svod_cols,
                                                 'ВС_Значение',
                                                 'ВС_Диапазон',
                                                 lst_reindex_one_level_cols, lst_level)

    # АД
    svod_count_one_level_ps_df = calc_count_scale(base_df, lst_svod_cols,
                                                 'ПС_Значение',
                                                 'ПС_Диапазон',
                                                 lst_reindex_one_level_cols, lst_level)

    # АД
    svod_count_one_level_ns_df = calc_count_scale(base_df, lst_svod_cols,
                                                 'НС_Значение',
                                                 'НС_Диапазон',
                                                 lst_reindex_one_level_cols, lst_level)

    # АД
    svod_count_one_level_obs_df = calc_count_scale(base_df, lst_svod_cols,
                                                 'ОБС_Значение',
                                                 'ОБС_Диапазон',
                                                 lst_reindex_one_level_cols, lst_level)

    # АД
    svod_count_one_level_ts_df = calc_count_scale(base_df, lst_svod_cols,
                                                 'ТС_Значение',
                                                 'ТС_Диапазон',
                                                 lst_reindex_one_level_cols, lst_level)

    # АД
    svod_count_one_level_ds_df = calc_count_scale(base_df, lst_svod_cols,
                                                 'ДС_Значение',
                                                 'ДС_Диапазон',
                                                 lst_reindex_one_level_cols, lst_level)

    # АД
    svod_count_one_level_ots_df = calc_count_scale(base_df, lst_svod_cols,
                                                 'ОТС_Значение',
                                                 'ОТС_Диапазон',
                                                 lst_reindex_one_level_cols, lst_level)

    # АД
    svod_count_one_level_ogs_df = calc_count_scale(base_df, lst_svod_cols,
                                                 'ОЖС_Значение',
                                                 'ОЖС_Диапазон',
                                                 lst_reindex_one_level_cols, lst_level)

    # Считаем среднее по субшкалам
    svod_mean_one_df = pd.pivot_table(base_df,
                                      index=lst_svod_cols,
                                      values=['ПА_Значение',
                                              'СС_Значение',
                                              'КС_Значение',
                                              'ХС_Значение',

                                              'ВС_Значение',
                                              'ПС_Значение',
                                              'НС_Значение',
                                              'ОБС_Значение',

                                              'ТС_Значение',
                                              'ДС_Значение',
                                              'ОТС_Значение',
                                              'ОЖС_Значение'
                                              ],
                                      aggfunc=round_mean_two)
    svod_mean_one_df.reset_index(inplace=True)

    # упорядочиваем колонки
    new_order_cols = lst_svod_cols.copy()
    new_order_cols.extend(([  'ПА_Значение',
                              'СС_Значение',
                              'КС_Значение',
                              'ХС_Значение',

                              'ВС_Значение',
                              'ПС_Значение',
                              'НС_Значение',
                              'ОБС_Значение',

                              'ТС_Значение',
                              'ДС_Значение',
                              'ОТС_Значение',
                              'ОЖС_Значение'
                            ]))
    svod_mean_one_df = svod_mean_one_df.reindex(columns=new_order_cols)

    dct_rename_cols_mean = {'ПА_Значение': 'Ср. Поддержка автономии',
                            'СС_Значение': 'Ср. Структурирующий стиль',
                            'КС_Значение': 'Ср. Контролирующий стиль',
                            'ХС_Значение': 'Ср. Хаотический стиль',

                            'ВС_Значение': 'Ср. Вовлекающийся стиль',
                            'ПС_Значение': 'Ср. Подстраивающийся стиль',
                            'НС_Значение': 'Ср. Направляющий стиль',
                            'ОБС_Значение': 'Ср. Объясняющий стиль',

                            'ТС_Значение': 'Ср. Требовательный стиль',
                            'ДС_Значение': 'Ср. Деспотический стиль',
                            'ОТС_Значение': 'Ср. Отстраняющийся стиль',
                            'ОЖС_Значение': 'Ср. Ожидающий стиль'
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
                    f'ПА {out_name}': svod_count_one_level_pa_df,
                    f'СС {out_name}': svod_count_one_level_ss_df,
                    f'КС {out_name}': svod_count_one_level_cs_df,
                    f'ХС {out_name}': svod_count_one_level_hs_df,

                    f'ВС {out_name}': svod_count_one_level_vs_df,
                    f'ПС {out_name}': svod_count_one_level_ps_df,
                    f'НС {out_name}': svod_count_one_level_ns_df,
                    f'ОБС {out_name}': svod_count_one_level_obs_df,

                    f'ТС {out_name}': svod_count_one_level_ts_df,
                    f'ДС {out_name}': svod_count_one_level_ds_df,
                    f'ОТС {out_name}': svod_count_one_level_ots_df,
                    f'ОЖС {out_name}': svod_count_one_level_ogs_df,
                    })

    if len(lst_svod_cols) == 1:
        return out_dct
    else:
        for idx, name_column in enumerate(lst_svod_cols):
            lst_reindex_column_level_cols = [lst_svod_cols[idx], '1-1.99', '2-2.99', '3-3.99', '4-4.99','5-5.99','6-7',
                                             'Итого']
            # АД
            svod_count_column_level_pa_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                             'ПА_Значение',
                                                             'ПА_Диапазон',
                                                             lst_reindex_column_level_cols, lst_level)

            # АД
            svod_count_column_level_ss_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                             'СС_Значение',
                                                             'СС_Диапазон',
                                                             lst_reindex_column_level_cols, lst_level)

            # АД
            svod_count_column_level_cs_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                             'КС_Значение',
                                                             'КС_Диапазон',
                                                             lst_reindex_column_level_cols, lst_level)

            # АД
            svod_count_column_level_hs_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                             'ХС_Значение',
                                                             'ХС_Диапазон',
                                                             lst_reindex_column_level_cols, lst_level)

            # АД
            svod_count_column_level_vs_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                             'ВС_Значение',
                                                             'ВС_Диапазон',
                                                             lst_reindex_column_level_cols, lst_level)

            # АД
            svod_count_column_level_ps_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                             'ПС_Значение',
                                                             'ПС_Диапазон',
                                                             lst_reindex_column_level_cols, lst_level)

            # АД
            svod_count_column_level_ns_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                             'НС_Значение',
                                                             'НС_Диапазон',
                                                             lst_reindex_column_level_cols, lst_level)

            # АД
            svod_count_column_level_obs_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                              'ОБС_Значение',
                                                              'ОБС_Диапазон',
                                                              lst_reindex_column_level_cols, lst_level)

            # АД
            svod_count_column_level_ts_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                             'ТС_Значение',
                                                             'ТС_Диапазон',
                                                             lst_reindex_column_level_cols, lst_level)

            # АД
            svod_count_column_level_ds_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                             'ДС_Значение',
                                                             'ДС_Диапазон',
                                                             lst_reindex_column_level_cols, lst_level)

            # АД
            svod_count_column_level_ots_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                              'ОТС_Значение',
                                                              'ОТС_Диапазон',
                                                              lst_reindex_column_level_cols, lst_level)

            # АД
            svod_count_column_level_ogs_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                              'ОЖС_Значение',
                                                              'ОЖС_Диапазон',
                                                              lst_reindex_column_level_cols, lst_level)

            # Считаем среднее по субшкалам
            svod_mean_column_df = pd.pivot_table(base_df,
                                                 index=[lst_svod_cols[idx]],
                                                 values=['ПА_Значение',
                                                         'СС_Значение',
                                                         'КС_Значение',
                                                         'ХС_Значение',

                                                         'ВС_Значение',
                                                         'ПС_Значение',
                                                         'НС_Значение',
                                                         'ОБС_Значение',

                                                         'ТС_Значение',
                                                         'ДС_Значение',
                                                         'ОТС_Значение',
                                                         'ОЖС_Значение'
                                                         ],
                                                 aggfunc=round_mean_two)
            svod_mean_column_df.reset_index(inplace=True)

            # упорядочиваем колонки
            new_order_cols = [lst_svod_cols[idx]].copy()
            new_order_cols.extend((['ПА_Значение',
                                    'СС_Значение',
                                    'КС_Значение',
                                    'ХС_Значение',

                                    'ВС_Значение',
                                    'ПС_Значение',
                                    'НС_Значение',
                                    'ОБС_Значение',

                                    'ТС_Значение',
                                    'ДС_Значение',
                                    'ОТС_Значение',
                                    'ОЖС_Значение'
                                    ]))
            svod_mean_column_df = svod_mean_column_df.reindex(columns=new_order_cols)

            dct_rename_cols_mean = {'ПА_Значение': 'Ср. Поддержка автономии',
                                    'СС_Значение': 'Ср. Структурирующий стиль',
                                    'КС_Значение': 'Ср. Контролирующий стиль',
                                    'ХС_Значение': 'Ср. Хаотический стиль',

                                    'ВС_Значение': 'Ср. Вовлекающийся стиль',
                                    'ПС_Значение': 'Ср. Подстраивающийся стиль',
                                    'НС_Значение': 'Ср. Направляющий стиль',
                                    'ОБС_Значение': 'Ср. Объясняющий стиль',

                                    'ТС_Значение': 'Ср. Требовательный стиль',
                                    'ДС_Значение': 'Ср. Деспотический стиль',
                                    'ОТС_Значение': 'Ср. Отстраняющийся стиль',
                                    'ОЖС_Значение': 'Ср. Ожидающий стиль'
                                    }
            svod_mean_column_df.rename(columns=dct_rename_cols_mean, inplace=True)

            # Готовим наименование
            name_column = lst_svod_cols[idx]
            name_column = re.sub(r'[\[\]\'+()<> :"?*|\\/]', '_', name_column)
            name_column = name_column[:15]



            out_dct.update({f'Ср {name_column}': svod_mean_column_df,
                            f'ПА {name_column}': svod_count_column_level_pa_df,
                            f'СС {name_column}': svod_count_column_level_ss_df,
                            f'КС {name_column}': svod_count_column_level_cs_df,
                            f'ХС {name_column}': svod_count_column_level_hs_df,

                            f'ВС {name_column}': svod_count_column_level_vs_df,
                            f'ПС {name_column}': svod_count_column_level_ps_df,
                            f'НС {name_column}': svod_count_column_level_ns_df,
                            f'ОБС {name_column}': svod_count_column_level_obs_df,

                            f'ТС {name_column}': svod_count_column_level_ts_df,
                            f'ДС {name_column}': svod_count_column_level_ds_df,
                            f'ОТС {name_column}': svod_count_column_level_ots_df,
                            f'ОЖС {name_column}': svod_count_column_level_ogs_df,
                            })
        return out_dct











def processing_ossh_gor(base_df: pd.DataFrame, answers_df: pd.DataFrame, lst_svod_cols:list):
    """
    Функция для обработки
    :param base_df: часть датафрейма с описательными колонками
    :param answers_df: часть датафрейма с ответами
    :param lst_svod_cols:  список с колонками по которым нужно делать свод
    """
    try:
        count_descr_cols = base_df.shape[1]  # количество анкетных колонок
        union_base_df = base_df.copy()  # делаем копию анкетной части чтобы потом соединить ее с ответной частью

        out_answer_df = base_df.copy()  # делаем копию для последующего соединения с сырыми ответами
        if len(answers_df.columns) != 60:  # проверяем количество колонок с вопросами
            raise BadCountColumnsOSSHGS

        # очищаем названия колонок от возможных сочетаний .1 которые добавляет пандас при одинаковых колонках
        clean_df_lst = []
        for name_column in answers_df.columns:
            clean_name = re.sub(r'.\d+$', '', name_column)
            clean_df_lst.append(clean_name)

        answers_df.columns = clean_df_lst

        lst_check_cols = ['Сообщаете о своих ожиданиях и нормах поведения для успешного взаимодействия',
                          'Не сильно беспокоитесь о правилах и нормах',
                          'Сообщаете свои правила. Говорите учащимся, что они должны соблюдать все правила и предупреждаете о последствиях в случае их нарушения',
                          'Предлагаете учащимся самим предложить набор рекомендаций, которые помогут им чувствовать себя комфортно в классе',
                          'Сообщить учащимся, какие учебные цели должны быть достигнуты ими к концу урока',
                          'Не планировать и не организовывать слишком много. Урок пойдет своим чередом',
                          'Предложить очень интересный, увлекательный урок',
                          'Настаивать, чтобы ученики завершили всю необходимую работу — без исключений и оправданий',
                          'Предоставите четкий пошаговый план урока',
                          'Не планируете слишком много. Вместо этого позволяете уроку идти своим чередом',

                          'Твердо настаиваете на том, чтобы учащиеся учились тому, чему их учат; Ваша обязанность — учить, а их — учиться',
                          'Спросите учащихся, что им интересно узнать, чтобы учесть это при изложении темы',
                          'Минимизировать запланированное; пусть то, что происходит — происходит',
                          'Стукнуть по столу и громко произнести: «А сейчас все внимание!»',
                          'Предложить помощь и руководство',
                          'Объяснить личную пользу учебного материала для повседневной жизни учащихся',
                          'Называете фамилию ученика и требуете от него ответа на поставленный вопрос/задачу',
                          'Уточните и переформулируете вопрос, чтобы ученики могли на него ответить',
                          'Попросите учеников обсудить вопрос со своим соседом и затем предлагаете им поделиться своим ответом в своих группах',
                          'Вздохнете, сами ответите на вопрос и продолжите урок',

                          'Посочувствуете им. Скажете, что Вы открыты для их предложений и пожеланий',
                          'Настаиваете, чтобы они сконцентрировались. Они должны выучить этот материал для их же пользы',
                          'Научите их полезной стратегии решения проблемы разбиением задачи на части и решения ее «шаг за шагом»',
                          'Просто проигнорируете нытье и жалобы. Им нужно научиться самим преодолевать трудности',
                          'Не беспокоитесь, так как ученики сами должны понять, что им нужно приложить много усилий',
                          'Попробуете найти способы сделать урок более интересным и приятным для учеников',
                          'Твердо настаиваете на том, что «сейчас настало время для серьезной работы!»',
                          'Скажете: «Поскольку эта тема очень сложная, я готов(а) вам максимально помочь, если это необходимо»',
                          'Признаете, что они выглядят обеспокоенными и напряженными. Попросите учеников рассказать, что их беспокоит',
                          'Скажете, что они уже взрослые и должны вести себя соответственно',

                          'Разделите задание на части, чтобы ученики почувствовали, что они могут с ним справиться',
                          'Не беспокоитесь об этом — пусть это пройдет само по себе',
                          'Даете учащимся команду поторопиться и закончить последнее задание',
                          'Проверяете (отслеживаете), насколько каждый ученик готов и способен перейти к новой деятельности',
                          'Просто начинаете новое задание (тему, задачу) – возможно, кто-то готов его начать',
                          'Будете терпеливы; подтвердите, что у тех, кто все еще усердно работает, будет достаточно времени, чтобы завершить предыдущую работу',
                          'Скажете, что они должны вернуться к заданию, иначе будут плохие последствия',
                          'Объясните причины, по которым Вы хотите, чтобы они вели себя правильно. Позже поговорите с ними индивидуально, внимательно выслушав их точку зрения',
                          'Сообщите классу, каковы Ваши ожидания относительно поведения и норм общения',
                          'Пустите ситуацию на самотек, потому что вмешиваться — сплошная морока',

                          'Спросите учеников, над какими упражнениями они хотят проработать больше всего',
                          'Потребуете, чтобы они начали работать, нравится им это или нет. Скажете им, что им иногда необходимо научиться делать что-то, даже если нет желания',
                          'Не будете планировать слишком много и посмотрите, как все будет развиваться',
                          'Пошагово объясните решение одной задачи/проблемы, а затем будете сопровождать их в решении дальнейших задач',
                          'Отвести спорящих в сторону, кратко описать, что Вы видели и спросить их мнение и предложения о том, что делать',
                          'Четко определить, каковы правила и ожидания в классе. Укажете, что представляет собой полезное сотрудничество и конструктивное поведение',
                          'Не вмешиваетесь, просто позволите ученикам самим решать проблемы',
                          'Скажете им, что им должно быть стыдно за свое поведение и что, если они продолжат, последуют санкции (наказания)',
                          'Настаиваете на том, что такие низкие результаты для Вас неприемлемы. Скажете ученикам, что они должны улучшить результат для их же блага',
                          'Поможете ученикам разобрать свои неправильные ответы, чтобы они поняли, что они сделали не так и, как это улучшить',

                          'Выслушаете с терпением и пониманием, что ученики говорят о выполнении контрольной',
                          'Не будете тратить время в классе на плохо успевающих учеников',
                          'Настаиваете: «Постарайся делать все правильно и как следует. Серьезнее. В противном случае, у тебя будут проблемы»',
                          'Повторно и более подробно будете объяснять учебный материал, пока они не поймут его лучше',
                          'Скажете: «Хорошо, с чего начнем, какие есть предложения?»',
                          'Не будете вмешиваться и подождете, пока они сами не попросят дополнительной помощи',
                          'Даете понять, что домашнее задание должно быть выполнено хорошо, иначе будут плохие оценки',
                          'Сообщите, что нужно, чтобы правильно выполнить домашнее задание. Убедитесь, что все понимают, что требуется для успешного выполнения домашней работы',
                          'Предложите несколько различных домашних заданий (например, три) и попросите учеников выбрать несколько из них (например, два)',
                          'Полагаете, что домашнее задание говорит само за себя и нет нужды все без конца объяснять'
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
            raise BadOrderOSSHGS

        answers_df = answers_df.astype(str) # делаем на всякий случай строковыми

        # словарь для замены слов на числа
        dct_replace_value = {
                             '1-Совсем не описывает меня (мое поведение)': 1,
                             '2': 2,
                             '3': 3,
                             '4- В какой-то степени описывает меня': 4,
                             '5': 5,
                             '6': 6,
                             '7- Полностью описывает меня (мое поведение)': 7,
                             }
        valid_values = [1, 2, 3,4,5,6,7]
        answers_df.replace(dct_replace_value, inplace=True)  # заменяем слова на цифры для подсчетов
        # Проверяем, есть ли значения, отличающиеся от указанных в списке
        lst_error_answers = []  # список для хранения строк где найдены неправильные ответы

        for i in range(60):
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
            raise BadValueOSSHGS

        base_df['ПА_Значение'] = answers_df.apply(calc_value_pa, axis=1)
        base_df['ПА_Диапазон'] = base_df['ПА_Значение'].apply(calc_level)

        base_df['СС_Значение'] = answers_df.apply(calc_value_ss, axis=1)
        base_df['СС_Диапазон'] = base_df['СС_Значение'].apply(calc_level)

        base_df['КС_Значение'] = answers_df.apply(calc_value_cs, axis=1)
        base_df['КС_Диапазон'] = base_df['КС_Значение'].apply(calc_level)

        base_df['ХС_Значение'] = answers_df.apply(calc_value_hs, axis=1)
        base_df['ХС_Диапазон'] = base_df['ХС_Значение'].apply(calc_level)


        base_df['ВС_Значение'] = answers_df.apply(calc_value_vs, axis=1)
        base_df['ВС_Диапазон'] = base_df['ВС_Значение'].apply(calc_level)

        base_df['ПС_Значение'] = answers_df.apply(calc_value_ps, axis=1)
        base_df['ПС_Диапазон'] = base_df['ПС_Значение'].apply(calc_level)

        base_df['НС_Значение'] = answers_df.apply(calc_value_ns, axis=1)
        base_df['НС_Диапазон'] = base_df['НС_Значение'].apply(calc_level)

        base_df['ОБС_Значение'] = answers_df.apply(calc_value_obs, axis=1)
        base_df['ОБС_Диапазон'] = base_df['ОБС_Значение'].apply(calc_level)

        base_df['ТС_Значение'] = answers_df.apply(calc_value_ts, axis=1)
        base_df['ТС_Диапазон'] = base_df['ТС_Значение'].apply(calc_level)

        base_df['ДС_Значение'] = answers_df.apply(calc_value_ds, axis=1)
        base_df['ДС_Диапазон'] = base_df['ДС_Значение'].apply(calc_level)

        base_df['ОТС_Значение'] = answers_df.apply(calc_value_ots, axis=1)
        base_df['ОТС_Диапазон'] = base_df['ОТС_Значение'].apply(calc_level)

        base_df['ОЖС_Значение'] = answers_df.apply(calc_value_ogs, axis=1)
        base_df['ОЖС_Диапазон'] = base_df['ОЖС_Значение'].apply(calc_level)

        base_df['Основные_Шкалы'] = base_df[['ПА_Значение','СС_Значение','КС_Значение','ХС_Значение']].apply(create_str,axis=1)
        base_df['Вспомогательные_Шкалы'] = base_df[['ВС_Значение','ПС_Значение','НС_Значение','ОБС_Значение',
                                                    'ТС_Значение','ДС_Значение','ОТС_Значение','ОЖС_Значение']].apply(create_str,axis=1)

        result_df = base_df.iloc[:, count_descr_cols:]  # отсекаем часть с результатами чтобы упорядочить
        new_order_lst = ['Основные_Шкалы','Вспомогательные_Шкалы',
                         'ПА_Значение','ПА_Диапазон','СС_Значение','СС_Диапазон',
                         'КС_Значение','КС_Диапазон','ХС_Значение','ХС_Диапазон',

                         'ВС_Значение','ВС_Диапазон','ПС_Значение','ПС_Диапазон',
                         'НС_Значение','НС_Диапазон','ОБС_Значение','ОБС_Диапазон',

                         'ТС_Значение','ТС_Диапазон','ДС_Значение','ДС_Диапазон',
                         'ОТС_Значение','ОТС_Диапазон','ОЖС_Значение','ОЖС_Диапазон'
                         ]

        result_df = result_df.reindex(columns=new_order_lst)  # изменяем порядок
        base_df = pd.concat([union_base_df, result_df], axis=1)  # соединяем и перезаписываем base_df


        # Создаем датафрейм для создания части в общий датафрейм
        temp_df = base_df.copy()  # делаем копию
        part_df = temp_df.iloc[:, count_descr_cols:]
        part_df = part_df.add_prefix('ОСШГС_')

        out_answer_df = pd.concat([out_answer_df, answers_df], axis=1)  # Датафрейм для проверки

        # Делаем свод  по  шкалам
        dct_main_svod_sub = {'ПА_Значение': 'ПА_Диапазон',
                        'СС_Значение': 'СС_Диапазон',
                        'КС_Значение': 'КС_Диапазон',
                        'ХС_Значение': 'ХС_Диапазон',
                        }

        dct_rename_maint_svod_sub = {'ПА_Значение': 'Поддержка автономии',
                               'СС_Значение': 'Структурирующий стиль',
                               'КС_Значение': 'Контролирующий стиль',
                               'ХС_Значение': 'Хаотический стиль',
                               }

        lst_sub = ['1-1.99', '2-2.99', '3-3.99', '4-4.99','5-5.99','6-7']

        base_svod_main_df = create_union_svod(base_df, dct_main_svod_sub, dct_rename_maint_svod_sub, lst_sub)

        # Делаем свод  по  субшкалам
        dct_svod_sub = {
                        'ВС_Значение': 'ВС_Диапазон',
                        'ПС_Значение': 'ПС_Диапазон',
                        'НС_Значение': 'НС_Диапазон',
                        'ОБС_Значение': 'ОБС_Диапазон',

                        'ТС_Значение': 'ТС_Диапазон',
                        'ДС_Значение': 'ДС_Диапазон',
                        'ОТС_Значение': 'ОТС_Диапазон',
                        'ОЖС_Значение': 'ОЖС_Диапазон',
                        }

        dct_rename_svod_sub = {
                               'ВС_Значение': 'Вовлекающийся стиль',
                               'ПС_Значение': 'Подстраивающийся стиль',
                               'НС_Значение': 'Направляющий стиль',
                               'ОБС_Значение': 'Объясняющий стиль',

                               'ТС_Значение': 'Требовательный стиль',
                               'ДС_Значение': 'Деспотический стиль',
                               'ОТС_Значение': 'Отстраняющийся стиль',
                               'ОЖС_Значение': 'Ожидающий стиль',
                               }

        lst_sub = ['1-1.99', '2-2.99', '3-3.99', '4-4.99','5-5.99','6-7']

        base_svod_sub_df = create_union_svod(base_df, dct_svod_sub, dct_rename_svod_sub, lst_sub)





        avg_pa = round(base_df['ПА_Значение'].mean(), 2)
        avg_ss = round(base_df['СС_Значение'].mean(), 2)
        avg_cs = round(base_df['КС_Значение'].mean(), 2)
        avg_hs = round(base_df['ХС_Значение'].mean(), 2)

        avg_vs = round(base_df['ВС_Значение'].mean(), 2)
        avg_ps = round(base_df['ПС_Значение'].mean(), 2)
        avg_ns = round(base_df['НС_Значение'].mean(), 2)
        avg_obs = round(base_df['ОБС_Значение'].mean(), 2)

        avg_ts = round(base_df['ТС_Значение'].mean(), 2)
        avg_ds = round(base_df['ДС_Значение'].mean(), 2)
        avg_ots = round(base_df['ОТС_Значение'].mean(), 2)
        avg_ogs = round(base_df['ОЖС_Значение'].mean(), 2)

        avg_dct = {'Среднее значение шкалы Поддержка автономии': avg_pa,
                   'Среднее значение шкалы Структурирующий стиль': avg_ss,
                   'Среднее значение шкалы Контролирующий стиль': avg_cs,
                   'Среднее значение шкалы Хаотический стиль': avg_hs,

                   'Среднее значение шкалы Вовлекающийся стиль': avg_vs,
                   'Среднее значение шкалы Подстраивающийся стиль': avg_ps,
                   'Среднее значение шкалы Направляющий стиль': avg_ns,
                   'Среднее значение шкалы Объясняющий стиль': avg_obs,

                   'Среднее значение шкалы Требовательный стиль': avg_ts,
                   'Среднее значение шкалы Деспотический стиль': avg_ds,
                   'Среднее значение шкалы Отстраняющийся стиль': avg_ots,
                   'Среднее значение шкалы Ожидающий стиль': avg_ogs,
                   }

        avg_df = pd.DataFrame.from_dict(avg_dct, orient='index')
        avg_df = avg_df.reset_index()
        avg_df.columns = ['Показатель', 'Среднее значение']

        # формируем основной словарь
        out_dct = {'Списочный результат': base_df,
                   'Список для проверки': out_answer_df,
                   'Основные Шкалы': base_svod_main_df,
                   'Субшкалы': base_svod_sub_df,
                   'Среднее': avg_df,
                   }

        dct_prefix = {
            'ПА_Диапазон': 'ПА',
            'СС_Диапазон': 'СС',
            'КС_Диапазон': 'КС',
            'ХС_Диапазон': 'ХС',

            'ВС_Диапазон': 'ВС',
            'ПС_Диапазон': 'ПС',
            'НС_Диапазон': 'НС',
            'ОБС_Диапазон': 'ОБС',

            'ТС_Диапазон': 'ТС',
            'ДС_Диапазон': 'ДС',
            'ОТС_Диапазон': 'ОТС',
            'ОЖС_Диапазон': 'ОЖС',
        }

        out_dct = create_list_on_level(base_df, out_dct, lst_sub, dct_prefix)

        """
                        Сохраняем в зависимости от необходимости делать своды по определенным колонкам
                        """
        if len(lst_svod_cols) == 0:
            return out_dct, part_df

        else:
            out_dct = create_result_ossh_gordeeva(base_df, out_dct, lst_svod_cols)
            return out_dct, part_df

    except BadOrderOSSHGS:
        messagebox.showerror('Лахеcис',
                             f'При обработке вопросов теста Опросник Ситуации в школе Гордеева, Сычев обнаружены неправильные вопросы. Проверьте названия колонок с вопросами:\n'
                             f'{error_order_message[:5000]}\n'
                             f'Используйте при создании Яндекс-формы написание вопросов из руководства пользователя программы Лахесис.')
    except BadValueOSSHGS:
        messagebox.showerror('Лахеcис',
                             f'При обработке вопросов теста Опросник Ситуации в школе Гордеева, Сычев обнаружены неправильные варианты ответов. Проверьте ответы на указанных строках:\n'
                             f'{error_message[:5000]}\n'
                             f'Используйте при создании Яндекс-формы написание вариантов ответа из руководства пользователя программы Лахесис.')


    except BadCountColumnsOSSHGS:
        messagebox.showerror('Лахеcис',
                             f'Проверьте количество колонок с ответами на тест Опросник Ситуации в школе Гордеева, Сычев\n'
                             f'Должно быть 60 колонок с ответами')





