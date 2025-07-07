"""
Скрипт для обработки результатов теста Шкала нарушенных потребностей остракизм Бойкина
"""
import pandas as pd
import re
from tkinter import messagebox
from lachesis_support_functions import round_mean,create_union_svod

class BadOrderSHNPO(Exception):
    """
    Исключение для обработки случая когда колонки не совпадают
    """
    pass


class BadValueSHNPO(Exception):
    """
    Исключение для неправильных значений в вариантах ответов
    """
    pass

class BadCountColumnsSHNPO(Exception):
    """
    Исключение для обработки случая если количество колонок не равно 20
    """
    pass


def create_boykina_list_on_level(base_df:pd.DataFrame,out_dct:dict,lst_level:list,dct_prefix:dict):
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
                if level == 'низкий уровень социального остракизма':
                    level = 'низкий уровень'
                elif level == 'средний уровень социального остракизма':
                    level = 'средний уровень'
                else:
                    level = 'высокий уровень'
                dct_level[f'{dct_prefix[key]}. {level}'] = temp_df
        out_dct.update(dct_level)

    return out_dct



def calc_sub_value_pr(row):
    """
    Функция для подсчета значения субшкалы Принадлежности
    :param row: строка с ответами
    :return: число
    """
    lst_pr = [1, 4, 6, 7, 13]

    value_forward = 0 # счетчик прямых ответов
    value_reverse = 0 # счетчик обратных ответов
    lst_forward = [1, 6, 13]  # список ответов которые нужно считать простым сложением
    lst_reverse = [4, 7] # обратный подсчет

    for idx, value in enumerate(row):
        if idx +1 in lst_pr:
            if idx + 1 in lst_forward:
                # print(f'Прямой подсчет {idx +1}') # Для проверки корректности
                value_forward += value
            elif idx +1 in lst_reverse:
                # print(f'Обратный подсчет {idx +1}')# Для проверки корректности
                if value == 5:
                    value_reverse += 1
                elif value == 4:
                    value_reverse += 2
                elif value == 3:
                    value_reverse += 3
                elif value == 2:
                    value_reverse += 4
                elif value == 1:
                    value_reverse += 5

    return round((value_forward + value_reverse) /5,1)

def calc_level_sub_pr_pod(value):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """
    if 1 <= value <= 1.4:
        return 'низкий уровень социального остракизма'
    elif 1.5 <= value <= 2.4:
        return 'средний уровень социального остракизма'
    elif 2.5 <= value <= 5:
        return 'высокий уровень социального остракизма'

def calc_level_sub_pr_mol(value):
    """
    Функция для подсчета уровня субшкалы
    :param value:
    :return:
    """
    if 1 <= value <= 1.6:
        return 'низкий уровень социального остракизма'
    elif 1.7 <= value <= 3:
        return 'средний уровень социального остракизма'
    elif 3.1 <= value <= 5:
        return 'высокий уровень социального остракизма'



def calc_sub_value_sam(row):
    """
    Функция для подсчета значения субшкалы Самоуважение
    :param row: строка с ответами
    :return: число
    """
    lst_pr = [5, 9, 11, 12, 15]

    value_forward = 0 # счетчик прямых ответов
    value_reverse = 0 # счетчик обратных ответов
    lst_forward = [5]  # список ответов которые нужно считать простым сложением
    lst_reverse = [9, 11, 12, 15] # обратный подсчет

    for idx, value in enumerate(row):
        if idx +1 in lst_pr:
            if idx + 1 in lst_forward:
                # print(f'Прямой подсчет {idx +1}') # Для проверки корректности
                value_forward += value
            elif idx +1 in lst_reverse:
                # print(f'Обратный подсчет {idx +1}')# Для проверки корректности
                if value == 5:
                    value_reverse += 1
                elif value == 4:
                    value_reverse += 2
                elif value == 3:
                    value_reverse += 3
                elif value == 2:
                    value_reverse += 4
                elif value == 1:
                    value_reverse += 5

    return round((value_forward + value_reverse) /5,1)

def calc_level_sub_sam_pod(value):
    """
    Функция для подсчета уровня субшкалы самоуважения
    :param value:
    :return:
    """
    if 1 <= value <= 1.6:
        return 'низкий уровень социального остракизма'
    elif 1.7 <= value <= 2.8:
        return 'средний уровень социального остракизма'
    elif 2.9 <= value <= 5:
        return 'высокий уровень социального остракизма'

def calc_level_sub_sam_mol(value):
    """
    Функция для подсчета уровня субшкалы самоуважения
    :param value:
    :return:
    """
    if 1 <= value <= 1.8:
        return 'низкий уровень социального остракизма'
    elif 1.9 <= value <= 3.2:
        return 'средний уровень социального остракизма'
    elif 3.3 <= value <= 5:
        return 'высокий уровень социального остракизма'



def calc_sub_value_con(row):
    """
    Функция для подсчета значения субшкалы Контроль
    :param row: строка с ответами
    :return: число
    """
    lst_pr = [3, 8, 10, 14, 20]

    value_forward = 0 # счетчик прямых ответов
    value_reverse = 0 # счетчик обратных ответов
    lst_forward = [3,8,14,20]  # список ответов которые нужно считать простым сложением
    lst_reverse = [10] # обратный подсчет

    for idx, value in enumerate(row):
        if idx +1 in lst_pr:
            if idx + 1 in lst_forward:
                # print(f'Прямой подсчет {idx +1}') # Для проверки корректности
                value_forward += value
            elif idx +1 in lst_reverse:
                # print(f'Обратный подсчет {idx +1}')# Для проверки корректности
                if value == 5:
                    value_reverse += 1
                elif value == 4:
                    value_reverse += 2
                elif value == 3:
                    value_reverse += 3
                elif value == 2:
                    value_reverse += 4
                elif value == 1:
                    value_reverse += 5

    return round((value_forward + value_reverse) /5,1)

def calc_level_sub_con_pod(value):
    """
    Функция для подсчета уровня субшкалы самоуважения
    :param value:
    :return:
    """
    if 1 <= value <= 1.2:
        return 'низкий уровень социального остракизма'
    elif 1.3 <= value <= 2.4:
        return 'средний уровень социального остракизма'
    elif 2.5 <= value <= 5:
        return 'высокий уровень социального остракизма'


def calc_level_sub_con_mol(value):
    """
    Функция для подсчета уровня субшкалы контроля
    :param value:
    :return:
    """
    if 1 <= value <= 1.6:
        return 'низкий уровень социального остракизма'
    elif 1.7 <= value <= 2.8:
        return 'средний уровень социального остракизма'
    elif 2.9 <= value <= 5:
        return 'высокий уровень социального остракизма'


def calc_sub_value_os(row):
    """
    Функция для подсчета значения субшкалы Осмысленное существование
    :param row: строка с ответами
    :return: число
    """
    lst_pr = [2, 16, 17, 18, 19]

    value_forward = 0 # счетчик прямых ответов
    value_reverse = 0 # счетчик обратных ответов
    lst_forward = [16,19]  # список ответов которые нужно считать простым сложением
    lst_reverse = [2, 17, 18] # обратный подсчет

    for idx, value in enumerate(row):
        if idx +1 in lst_pr:
            if idx + 1 in lst_forward:
                # print(f'Прямой подсчет {idx +1}') # Для проверки корректности
                value_forward += value
            elif idx +1 in lst_reverse:
                # print(f'Обратный подсчет {idx +1}')# Для проверки корректности
                if value == 5:
                    value_reverse += 1
                elif value == 4:
                    value_reverse += 2
                elif value == 3:
                    value_reverse += 3
                elif value == 2:
                    value_reverse += 4
                elif value == 1:
                    value_reverse += 5

    return round((value_forward + value_reverse) /5,1)

def calc_level_sub_os_pod(value):
    """
    Функция для подсчета уровня субшкалы самоуважения
    :param value:
    :return:
    """
    if 1 <= value <= 1.4:
        return 'низкий уровень социального остракизма'
    elif 1.5 <= value <= 2.6:
        return 'средний уровень социального остракизма'
    elif 2.7 <= value <= 5:
        return 'высокий уровень социального остракизма'

def calc_level_sub_os_mol(value):
    """
    Функция для подсчета уровня субшкалы осмысленного существования
    :param value:
    :return:
    """
    if 1 <= value <= 1.8:
        return 'низкий уровень социального остракизма'
    elif 1.9 <= value <= 3.2:
        return 'средний уровень социального остракизма'
    elif 3.3 <= value <= 5:
        return 'высокий уровень социального остракизма'



def calc_count_level(df:pd.DataFrame, lst_cat:list, val_cat, col_cat, lst_cols:list):
    """
    Функция для создания сводных датафреймов по шкалам

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
    count_df['% низкий уровень социального остракизма от общего'] = round(
        count_df['низкий уровень социального остракизма'] / count_df['Итого'], 2) * 100
    count_df['% средний уровень социального остракизма от общего'] = round(
        count_df['средний уровень социального остракизма'] / count_df['Итого'], 2) * 100
    count_df['% высокий уровень социального остракизма от общего'] = round(
        count_df['высокий уровень социального остракизма'] / count_df['Итого'], 2) * 100

    return count_df





def create_result_shnpo(base_df:pd.DataFrame, out_dct:dict, lst_svod_cols:list):
    """
    Функция для подсчета результата если указаны колонки по которым нужно провести свод
    :param df: датафрейм с результатами
    :param out_dct: словарь с уже подсчитанными базовыми данными
    :param lst_svod_cols: список сводных колонок
    :return: словарь
    """
    # Тревожность
    lst_reindex_one_level_cols = lst_svod_cols.copy()
    lst_reindex_one_level_cols.extend( ['низкий уровень социального остракизма', 'средний уровень социального остракизма', 'высокий уровень социального остракизма',
                                                      'Итого'])


    # Субшкалы
    svod_count_one_level_pr_pod_df = calc_count_level(base_df, lst_svod_cols,
                                                      'Значение_субшкалы_Принадлежность_Подростки',
                                                      'Уровень_субшкалы_Принадлежность_Подростки',
                                                       lst_reindex_one_level_cols)
    svod_count_one_level_pr__mol_df = calc_count_level(base_df, lst_svod_cols,
                                                      'Значение_субшкалы_Принадлежность_Молодежь',
                                                      'Уровень_субшкалы_Принадлежность_Молодежь',
                                                       lst_reindex_one_level_cols)



    svod_count_one_level_self_pod_df = calc_count_level(base_df, lst_svod_cols,
                                                          'Значение_субшкалы_Самоуважение_Подростки',
                                                          'Уровень_субшкалы_Самоуважение_Подростки',
                                                     lst_reindex_one_level_cols)
    svod_count_one_level_self_mol_df = calc_count_level(base_df, lst_svod_cols,
                                                          'Значение_субшкалы_Самоуважение_Молодежь',
                                                          'Уровень_субшкалы_Самоуважение_Молодежь',
                                                     lst_reindex_one_level_cols)

    svod_count_one_level_control_pod_df = calc_count_level(base_df, lst_svod_cols,
                                                          'Значение_субшкалы_Контроль_Подростки',
                                                          'Уровень_субшкалы_Контроль_Подростки',
                                                     lst_reindex_one_level_cols)
    svod_count_one_level_control_mol_df = calc_count_level(base_df, lst_svod_cols,
                                                          'Значение_субшкалы_Контроль_Молодежь',
                                                          'Уровень_субшкалы_Контроль_Молодежь',
                                                     lst_reindex_one_level_cols)


    svod_count_one_level_os_pod_df = calc_count_level(base_df, lst_svod_cols,
                                                          'Значение_субшкалы_ОС_Подростки',
                                                          'Уровень_субшкалы_ОС_Подростки',
                                                     lst_reindex_one_level_cols)

    svod_count_one_level_os_mol_df = calc_count_level(base_df, lst_svod_cols,
                                                          'Значение_субшкалы_ОС_Молодежь',
                                                          'Уровень_субшкалы_ОС_Молодежь',
                                                     lst_reindex_one_level_cols)

    # Считаем среднее по субшкалам
    svod_mean_one_df = pd.pivot_table(base_df,
                                      index=lst_svod_cols,
                                      values=['Значение_субшкалы_Принадлежность_Подростки',
                                              'Значение_субшкалы_Принадлежность_Молодежь',
                                              'Значение_субшкалы_Самоуважение_Подростки',
                                              'Значение_субшкалы_Самоуважение_Молодежь',
                                              'Значение_субшкалы_Контроль_Подростки',
                                              'Значение_субшкалы_Контроль_Молодежь',
                                              'Значение_субшкалы_ОС_Подростки',
                                              'Значение_субшкалы_ОС_Молодежь',
                                              ],
                                      aggfunc=round_mean)
    svod_mean_one_df.reset_index(inplace=True)
    # упорядочиваем колонки
    new_order_cols = lst_svod_cols.copy()
    new_order_cols.extend((['Значение_субшкалы_Принадлежность_Подростки',
                                              'Значение_субшкалы_Принадлежность_Молодежь',
                                              'Значение_субшкалы_Самоуважение_Подростки',
                                              'Значение_субшкалы_Самоуважение_Молодежь',
                                              'Значение_субшкалы_Контроль_Подростки',
                                              'Значение_субшкалы_Контроль_Молодежь',
                                              'Значение_субшкалы_ОС_Подростки',
                                              'Значение_субшкалы_ОС_Молодежь'
                            ]))
    svod_mean_one_df = svod_mean_one_df.reindex(columns=new_order_cols)

    dct_rename_cols_mean = {'Значение_субшкалы_Принадлежность_Подростки': 'Ср. П Под',
                            'Значение_субшкалы_Принадлежность_Молодежь': 'Ср. П Мол',

                            'Значение_субшкалы_Самоуважение_Подростки': 'Ср. С Под',
                            'Значение_субшкалы_Самоуважение_Молодежь': 'Ср. С Мол',

                            'Значение_субшкалы_Контроль_Подростки': 'Ср. К Под',
                            'Значение_субшкалы_Контроль_Молодежь': 'Ср. К Мол',

                            'Значение_субшкалы_ОС_Подростки': 'Ср. ОС Под',
                            'Значение_субшкалы_ОС_Молодежь': 'Ср. ОС Мол',
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
                    f'Свод П Под {out_name}': svod_count_one_level_pr_pod_df,
                    f'Свод П Мол {out_name}': svod_count_one_level_pr__mol_df,

                    f'Свод С Под {out_name}': svod_count_one_level_self_pod_df,
                    f'Свод С Мол {out_name}': svod_count_one_level_self_mol_df,

                    f'Свод К Под {out_name}': svod_count_one_level_control_pod_df,
                    f'Свод К Мол {out_name}': svod_count_one_level_control_mol_df,

                    f'Свод ОС Под {out_name}': svod_count_one_level_os_pod_df,
                    f'Свод ОС Мол {out_name}': svod_count_one_level_os_mol_df,
                    })

    if len(lst_svod_cols) == 1:
        return out_dct
    else:

        for idx, name_column in enumerate(lst_svod_cols):
            lst_reindex_column_level_cols = [lst_svod_cols[idx], 'низкий уровень социального остракизма', 'средний уровень социального остракизма', 'высокий уровень социального остракизма', 'Итого']

            # Субшкалы
            svod_count_column_level_pr_pod_df = calc_count_level(base_df, lst_svod_cols[idx],
            'Значение_субшкалы_Принадлежность_Подростки',
            'Уровень_субшкалы_Принадлежность_Подростки',
            lst_reindex_column_level_cols)
            svod_count_column_level_pr__mol_df = calc_count_level(base_df, lst_svod_cols[idx],
            'Значение_субшкалы_Принадлежность_Молодежь',
            'Уровень_субшкалы_Принадлежность_Молодежь',
            lst_reindex_column_level_cols)

            svod_count_column_level_self_pod_df = calc_count_level(base_df, lst_svod_cols[idx],
            'Значение_субшкалы_Самоуважение_Подростки',
            'Уровень_субшкалы_Самоуважение_Подростки',
            lst_reindex_column_level_cols)
            svod_count_column_level_self_mol_df = calc_count_level(base_df, lst_svod_cols[idx],
            'Значение_субшкалы_Самоуважение_Молодежь',
            'Уровень_субшкалы_Самоуважение_Молодежь',
            lst_reindex_column_level_cols)

            svod_count_column_level_control_pod_df = calc_count_level(base_df, lst_svod_cols[idx],
            'Значение_субшкалы_Контроль_Подростки',
            'Уровень_субшкалы_Контроль_Подростки',
            lst_reindex_column_level_cols)
            svod_count_column_level_control_mol_df = calc_count_level(base_df, lst_svod_cols[idx],
            'Значение_субшкалы_Контроль_Молодежь',
            'Уровень_субшкалы_Контроль_Молодежь',
            lst_reindex_column_level_cols)

            svod_count_column_level_os_pod_df = calc_count_level(base_df, lst_svod_cols[idx],
            'Значение_субшкалы_ОС_Подростки',
            'Уровень_субшкалы_ОС_Подростки',
            lst_reindex_column_level_cols)

            svod_count_column_level_os_mol_df = calc_count_level(base_df, lst_svod_cols[idx],
            'Значение_субшкалы_ОС_Молодежь',
            'Уровень_субшкалы_ОС_Молодежь',
            lst_reindex_column_level_cols)

            # Считаем среднее по субшкалам
            svod_mean_column_df = pd.pivot_table(base_df,
                                                 index=[lst_svod_cols[idx]],
            values = ['Значение_субшкалы_Принадлежность_Подростки',
                      'Значение_субшкалы_Принадлежность_Молодежь',
                      'Значение_субшкалы_Самоуважение_Подростки',
                      'Значение_субшкалы_Самоуважение_Молодежь',
                      'Значение_субшкалы_Контроль_Подростки',
                      'Значение_субшкалы_Контроль_Молодежь',
                      'Значение_субшкалы_ОС_Подростки',
                      'Значение_субшкалы_ОС_Молодежь',
                      ],
            aggfunc = round_mean)
            svod_mean_column_df.reset_index(inplace=True)
            # упорядочиваем колонки
            new_order_cols = [lst_svod_cols[idx]].copy()

            new_order_cols.extend((['Значение_субшкалы_Принадлежность_Подростки',
                                    'Значение_субшкалы_Принадлежность_Молодежь',
                                    'Значение_субшкалы_Самоуважение_Подростки',
                                    'Значение_субшкалы_Самоуважение_Молодежь',
                                    'Значение_субшкалы_Контроль_Подростки',
                                    'Значение_субшкалы_Контроль_Молодежь',
                                    'Значение_субшкалы_ОС_Подростки',
                                    'Значение_субшкалы_ОС_Молодежь'
                                    ]))
            svod_mean_column_df = svod_mean_column_df.reindex(columns=new_order_cols)

            dct_rename_cols_mean = {'Значение_субшкалы_Принадлежность_Подростки': 'Ср. П Под',
                                    'Значение_субшкалы_Принадлежность_Молодежь': 'Ср. П Мол',

                                    'Значение_субшкалы_Самоуважение_Подростки': 'Ср. С Под',
                                    'Значение_субшкалы_Самоуважение_Молодежь': 'Ср. С Мол',

                                    'Значение_субшкалы_Контроль_Подростки': 'Ср. К Под',
                                    'Значение_субшкалы_Контроль_Молодежь': 'Ср. К Мол',

                                    'Значение_субшкалы_ОС_Подростки': 'Ср. ОС Под',
                                    'Значение_субшкалы_ОС_Молодежь': 'Ср. ОС Мол',
                                    }
            svod_mean_column_df.rename(columns=dct_rename_cols_mean, inplace=True)

            name_column = lst_svod_cols[idx]
            name_column = re.sub(r'[\[\]\'+()<> :"?*|\\/]', '_', name_column)
            name_column = name_column[:15]

            out_dct.update({f'Ср {name_column}': svod_mean_column_df,
                            f'Свод П Под {name_column}': svod_count_column_level_pr_pod_df,
                            f'Свод П Мол {name_column}': svod_count_column_level_pr__mol_df,

                            f'Свод С Под {name_column}': svod_count_column_level_self_pod_df,
                            f'Свод С Мол {name_column}': svod_count_column_level_self_mol_df,

                            f'Свод К Под {name_column}': svod_count_column_level_control_pod_df,
                            f'Свод К Мол {name_column}': svod_count_column_level_control_mol_df,

                            f'Свод ОС Под {name_column}': svod_count_column_level_os_pod_df,
                            f'Свод ОС Мол {name_column}': svod_count_column_level_os_mol_df,
                            })
        return out_dct












def processing_boykina_shnpo(result_df: pd.DataFrame, answers_df: pd.DataFrame,lst_svod_cols:list):
    """
    Функция для обработки
    :param result_df: часть датафрейма с описательными колонками
    :param answers_df: часть датафрейма с ответами
    :param lst_svod_cols:  список с колонками по которым нужно делать свод
    """
    try:
        out_answer_df = result_df.copy()  # делаем копию для последующего соединения с сырыми ответами
        if len(answers_df.columns) != 20:  # проверяем количество колонок с вопросами
            raise BadCountColumnsSHNPO

        # очищаем названия колонок от возможных сочетаний .1 которые добавляет пандас при одинаковых колонках
        clean_df_lst = []
        for name_column in answers_df.columns:
            clean_name = re.sub(r'.\d+$', '', name_column)
            clean_df_lst.append(clean_name)

        answers_df.columns = clean_df_lst

        lst_check_cols = ['Я чувствую себя единым целым с другими людьми',
                          'Полагаю, что не вношу значимый вклад во что-либо',
                          'У меня есть уверенность, что я влияю на ход событий в моей жизни',
                          'Среди своего окружения я ощущаю себя лишним',
                          'Люди прислушиваются к моему мнению',
                          'В любой ситуации я чувствую поддержку хоть одного человека',
                          'Я ощущаю себя изгоем',
                          'Я совершенно точно управляю всем в своей жизни',
                          'Мне кажется, большинство из моего окружения невысокого обо мне мнения',
                          'Порой, кажется, что всё зависит от чьей-то чужой воли',
                          'Общаясь с людьми, я чувствую себя неуверенно',
                          'Такое ощущение, что общение с людьми – не моя сильная сторона',
                          'Думаю, что общество, в котором я живу, принимает меня',
                          'Я контролирую свою жизнь',
                          'Я переживаю, что люди плохо думают обо мне',
                          'Мне кажется, что моё участие в жизни окружающих очень важно',
                          'Порой я ощущаю себя невидимкой',
                          'Временами мне кажется, что от меня людям нет никакого толка',
                          'Думаю, мое участие в чем-либо всегда полезно',
                          'Такое ощущение, что у меня впереди еще много разных возможностей'
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
            raise BadOrderSHNPO

        # словарь для замены слов на числа
        dct_replace_value = {'не согласен': 5,
                             'редко': 4,
                             'иногда': 3,
                             'часто': 2,
                             'полностью согласен': 1}

        valid_values = [1, 2, 3, 4, 5]
        answers_df.replace(dct_replace_value, inplace=True)  # заменяем слова на цифры для подсчетов

        # Проверяем, есть ли значения, отличающиеся от указанных в списке
        lst_error_answers = []  # список для хранения строк где найдены неправильные ответы

        for i in range(20):
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
            raise BadValueSHNPO

        base_df = pd.DataFrame()

        # Субшкала Принаддежность
        base_df['Значение_субшкалы_Принадлежность'] = answers_df.apply(calc_sub_value_pr, axis=1)
        base_df['Норма_Принадлежность_Подростки'] = '1,5-2,4 баллов'
        base_df['Уровень_субшкалы_Принадлежность_Подростки'] = base_df['Значение_субшкалы_Принадлежность'].apply(
            calc_level_sub_pr_pod)

        base_df['Норма_Принадлежность_Молодежь'] = '1,7-3 балла'
        base_df['Уровень_субшкалы_Принадлежность_Молодежь'] = base_df['Значение_субшкалы_Принадлежность'].apply(
            calc_level_sub_pr_mol)

        # Субшкала Самоуважение
        base_df['Значение_субшкалы_Самоуважение'] = answers_df.apply(calc_sub_value_sam, axis=1)
        base_df['Норма_Самоуважение_Подростки'] = '1,7-2,8 баллов'
        base_df['Уровень_субшкалы_Самоуважение_Подростки'] = base_df['Значение_субшкалы_Самоуважение'].apply(
            calc_level_sub_sam_pod)

        base_df['Норма_Самоуважение_Молодежь'] = '1,9-3,2 балла'
        base_df['Уровень_субшкалы_Самоуважение_Молодежь'] = base_df['Значение_субшкалы_Самоуважение'].apply(
            calc_level_sub_sam_mol)

        # Субшкала Контроль
        base_df['Значение_субшкалы_Контроль'] = answers_df.apply(calc_sub_value_con, axis=1)
        base_df['Норма_Контроль_Подростки'] = '1,3-2,4 баллов'
        base_df['Уровень_субшкалы_Контроль_Подростки'] = base_df['Значение_субшкалы_Контроль'].apply(
            calc_level_sub_con_pod)

        base_df['Норма_Контроль_Молодежь'] = '1,7-2,8 баллов'
        base_df['Уровень_субшкалы_Контроль_Молодежь'] = base_df['Значение_субшкалы_Контроль'].apply(
            calc_level_sub_con_mol)

        # Субшкала Осмысленное существование
        base_df['Значение_субшкалы_ОС'] = answers_df.apply(calc_sub_value_os, axis=1)
        base_df['Норма_ОС_Подростки'] = '1,5-2,6 баллов'
        base_df['Уровень_субшкалы_ОС_Подростки'] = base_df['Значение_субшкалы_ОС'].apply(
            calc_level_sub_os_pod)

        base_df['Норма_ОС_Молодежь'] = '1,9-3,2 балла'
        base_df['Уровень_субшкалы_ОС_Молодежь'] = base_df['Значение_субшкалы_ОС'].apply(
            calc_level_sub_os_mol)

        # Создаем датафрейм для создания части в общий датафрейм
        part_df = pd.DataFrame()

        part_df['ШНПО_П_Значение'] = base_df['Значение_субшкалы_Принадлежность']
        part_df['ШНПО_П_Под_Уровень'] = base_df['Уровень_субшкалы_Принадлежность_Подростки']
        part_df['ШНПО_П_Мол_Уровень'] = base_df['Уровень_субшкалы_Принадлежность_Молодежь']

        part_df['ШНПО_С_Значение'] = base_df['Значение_субшкалы_Самоуважение']
        part_df['ШНПО_С_Под_Уровень'] = base_df['Уровень_субшкалы_Самоуважение_Подростки']
        part_df['ШНПО_С_Мол_Уровень'] = base_df['Уровень_субшкалы_Самоуважение_Молодежь']

        part_df['ШНПО_К_Значение'] = base_df['Значение_субшкалы_Контроль']
        part_df['ШНПО_К_Под_Уровень'] = base_df['Уровень_субшкалы_Контроль_Подростки']
        part_df['ШНПО_К_Мол_Уровень'] = base_df['Уровень_субшкалы_Контроль_Молодежь']

        part_df['ШНПО_ОС_Значение'] = base_df['Значение_субшкалы_ОС']
        part_df['ШНПО_ОС_Под_Уровень'] = base_df['Уровень_субшкалы_ОС_Подростки']
        part_df['ШНПО_ОС_Мол_Уровень'] = base_df['Уровень_субшкалы_ОС_Молодежь']


        out_answer_df = pd.concat([out_answer_df, answers_df], axis=1)  # Датафрейм для проверки

        # Соединяем анкетную часть с результатной
        base_df = pd.concat([result_df, base_df], axis=1)
        base_df.sort_values(by='Значение_субшкалы_Принадлежность', ascending=False, inplace=True)  # сортируем

        # формируем основной словарь
        out_dct = {'Списочный результат': base_df, 'Список для проверки': out_answer_df,
                   }

        dop_base_df = base_df.copy() # делаем копию чтобы лишние колонки не попадали


        # Создаем колонки для подсчета сводов
        dop_base_df['Значение_субшкалы_Принадлежность_Подростки'] = base_df['Значение_субшкалы_Принадлежность']
        dop_base_df['Значение_субшкалы_Принадлежность_Молодежь'] = base_df['Значение_субшкалы_Принадлежность']

        dop_base_df['Значение_субшкалы_Самоуважение_Подростки'] = base_df['Значение_субшкалы_Самоуважение']
        dop_base_df['Значение_субшкалы_Самоуважение_Молодежь'] = base_df['Значение_субшкалы_Самоуважение']

        dop_base_df['Значение_субшкалы_Контроль_Подростки'] = base_df['Значение_субшкалы_Контроль']
        dop_base_df['Значение_субшкалы_Контроль_Молодежь'] = base_df['Значение_субшкалы_Контроль']

        dop_base_df['Значение_субшкалы_ОС_Подростки'] = base_df['Значение_субшкалы_ОС']
        dop_base_df['Значение_субшкалы_ОС_Молодежь'] = base_df['Значение_субшкалы_ОС']


        # Делаем свод по интегральным показателям
        dct_svod_integral = {'Значение_субшкалы_Принадлежность_Подростки': 'Уровень_субшкалы_Принадлежность_Подростки',
                             'Значение_субшкалы_Принадлежность_Молодежь': 'Уровень_субшкалы_Принадлежность_Молодежь',

                             'Значение_субшкалы_Самоуважение_Подростки': 'Уровень_субшкалы_Самоуважение_Подростки',
                             'Значение_субшкалы_Самоуважение_Молодежь': 'Уровень_субшкалы_Самоуважение_Молодежь',

                             'Значение_субшкалы_Контроль_Подростки': 'Уровень_субшкалы_Контроль_Подростки',
                             'Значение_субшкалы_Контроль_Молодежь': 'Уровень_субшкалы_Контроль_Молодежь',

                             'Значение_субшкалы_ОС_Подростки': 'Уровень_субшкалы_ОС_Подростки',
                             'Значение_субшкалы_ОС_Молодежь': 'Уровень_субшкалы_ОС_Молодежь',
                             }

        dct_rename_svod_integral = {'Значение_субшкалы_Принадлежность_Подростки': 'П Под',
                                    'Значение_субшкалы_Принадлежность_Молодежь': 'П Мол',

                                    'Значение_субшкалы_Самоуважение_Подростки': 'С Под',
                                    'Значение_субшкалы_Самоуважение_Молодежь': 'С Мол',

                                    'Значение_субшкалы_Контроль_Подростки': 'К Под',
                                    'Значение_субшкалы_Контроль_Молодежь': 'К Мол',

                                    'Значение_субшкалы_ОС_Подростки': 'ОС Под',
                                    'Значение_субшкалы_ОС_Молодежь': 'ОС Мол',
                                    }

        lst_integral = ['низкий уровень социального остракизма', 'средний уровень социального остракизма', 'высокий уровень социального остракизма'
                       ]

        base_svod_integral_df = create_union_svod(dop_base_df, dct_svod_integral, dct_rename_svod_integral, lst_integral)

        # считаем среднее
        avg_pr_pod = round(dop_base_df['Значение_субшкалы_Принадлежность_Подростки'].mean(), 2)
        avg_pr_mol = round(dop_base_df['Значение_субшкалы_Принадлежность_Молодежь'].mean(), 2)

        avg_self_pod = round(dop_base_df['Значение_субшкалы_Самоуважение_Подростки'].mean(), 2)
        avg_self_mol = round(dop_base_df['Значение_субшкалы_Самоуважение_Молодежь'].mean(), 2)

        avg_contol_pod = round(dop_base_df['Значение_субшкалы_Контроль_Подростки'].mean(), 2)
        avg_control_mol = round(dop_base_df['Значение_субшкалы_Контроль_Молодежь'].mean(), 2)

        avg_os_pod = round(dop_base_df['Значение_субшкалы_ОС_Подростки'].mean(), 2)
        avg_os_mol = round(dop_base_df['Значение_субшкалы_ОС_Молодежь'].mean(), 2)

        avg_dct = {'Среднее значение Принадлежность Подростки ': avg_pr_pod,
                   'Среднее значение Принадлежность Молодежь': avg_pr_mol,

                   'Среднее значение Самоуважение Подростки': avg_self_pod,
                   'Среднее значение Самоуважение Молодежь': avg_self_mol,

                   'Среднее значение Контроль Подростки': avg_contol_pod,
                   'Среднее значение Контроль Молодежь': avg_control_mol,

                   'Среднее значение Осмысленное существование Подростки': avg_os_pod,
                   'Среднее значение Осмысленное существование Молодежь': avg_os_mol,

                   }

        avg_df = pd.DataFrame.from_dict(avg_dct, orient='index')
        avg_df = avg_df.reset_index()
        avg_df.columns = ['Показатель', 'Среднее значение']

        out_dct.update({'Свод Субшкалы': base_svod_integral_df,
                        'Среднее': avg_df}
                       )

        dct_prefix = {'Уровень_субшкалы_Принадлежность_Подростки': 'П Под',
                      'Уровень_субшкалы_Принадлежность_Молодежь': 'П Мол',

                      'Уровень_субшкалы_Самоуважение_Подростки': 'С Под',
                      'Уровень_субшкалы_Самоуважение_Молодежь': 'С Мол',

                      'Уровень_субшкалы_Контроль_Подростки': 'К Под',
                      'Уровень_субшкалы_Контроль_Молодежь': 'К Мол',

                      'Уровень_субшкалы_ОС_Подростки': 'ОС Под',
                      'Уровень_субшкалы_ОС_Молодежь': 'ОС Мол',
                      }

        out_dct = create_boykina_list_on_level(dop_base_df, out_dct, lst_integral, dct_prefix)

        """
            Сохраняем в зависимости от необходимости делать своды по определенным колонкам
            """
        if len(lst_svod_cols) == 0:
            return out_dct, part_df
        else:
            out_dct = create_result_shnpo(dop_base_df, out_dct, lst_svod_cols)

            return out_dct, part_df

    except BadOrderSHNPO:
        messagebox.showerror('Лахеcис',
                             f'При обработке вопросов теста Шкала нарушения потребностей, остракизм Бойкина обнаружены неправильные вопросы. Проверьте названия колонок с вопросами:\n'
                             f'{error_order_message}\n'
                             f'Используйте при создании Яндекс-формы написание вопросов из руководства пользователя программы Лахесис.')
    except BadValueSHNPO:
        messagebox.showerror('Лахеcис',
                             f'При обработке вопросов теста Шкала нарушения потребностей, остракизм Бойкина обнаружены неправильные варианты ответов. Проверьте ответы на указанных строках:\n'
                             f'{error_message}\n'
                             f'Используйте при создании Яндекс-формы написание вариантов ответа из руководства пользователя программы Лахесис.')


    except BadCountColumnsSHNPO:
        messagebox.showerror('Лахеcис',
                             f'Проверьте количество колонок с ответами на тест Шкала нарушения потребностей, остракизм Бойкина\n'
                             f'Должно быть 20 колонок с ответами')


























