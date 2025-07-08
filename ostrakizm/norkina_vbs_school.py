"""
Скрипт для обработки результатов теста Выявление буллинг структуры Норкина
"""

import pandas as pd
import re
from tkinter import messagebox
from lachesis_support_functions import round_mean,create_union_svod,create_list_on_level

class BadOrderVBS(Exception):
    """
    Исключение для обработки случая когда колонки не совпадают
    """
    pass


class BadValueVBS(Exception):
    """
    Исключение для неправильных значений в вариантах ответов
    """
    pass

class BadCountColumnsVBS(Exception):
    """
    Исключение для обработки случая если количество колонок не равно 25
    """
    pass


def extract_key_max_value(cell:str) ->str:
    """
    Функция для извлечения ключа с максимальным значением
    :param cell: строка формата ключ - значение;
    :return: ключ словаря в формате строки
    """
    dct_result = {}
    cell = cell.replace('\n','') # убираем переносы
    lst_temp = cell.split(';') # сплитим по точке с запятой
    for result in lst_temp:
        # отбрасываем пустую строку
        if result:
            key,value = result.split(': ') # извлекаем ключ и значение
            dct_result[key] = int(value)

    # возвращаем элемент с максимальным значением
    return max(dct_result, key=dct_result.get)

def extract_max_value(cell:str):
    """
    Функция для извлечения значения ключа с максимальным значением , ха звучит странно
    :param cell: строка формата ключ - значение;
    :return: ключ словаря в формате строки
    """
    dct_result = {}
    cell = cell.replace('\n','') # убираем переносы
    lst_temp = cell.split(';') # сплитим по точке с запятой
    for result in lst_temp:
        # отбрасываем пустую строку
        if result:
            key,value = result.split(': ') # извлекаем ключ и значение
            dct_result[key] = int(value)

    # возвращаем элемент с максимальным значением
    return dct_result[max(dct_result, key=dct_result.get)]






def processing_result_vbs(row):
    """
    Обработка результатов тестирования
    """

    # Создаем словарь для хранения данных
    dct_type = {'инициатор': 0, 'помощник': 0, 'защитник': 0,
                'жертва': 0,
                'наблюдатель': 0
                }

    # 1
    if row[0] == 'да, я дружу со всеми':
        dct_type['инициатор'] += 1
        dct_type['защитник'] += 1
    elif row[0] == 'у меня есть пару друзей':
        dct_type['помощник'] += 1
        dct_type['жертва'] += 1
    elif row[0] == 'нет, я ни с кем не дружу':
        pass
    elif row[0] == 'мне бы хотелось дружить со всеми':
        dct_type['наблюдатель'] += 1

    # 2
    if row[1] == 'да, если человек мне не симпатичен, я не буду с ним общаться':
        dct_type['помощник'] += 1
    elif row[1] == 'нет, главное, чтобы человек был интересен':
        dct_type['защитник'] += 1
        dct_type['наблюдатель'] += 1
    elif row[1] == 'я сам страдаю из-за своей внешности':
        dct_type['жертва'] += 1
    elif row[1] == 'конечно, если человек не обладает хорошей внешностью, он не заслуживает ничего хорошего':
        dct_type['инициатор'] += 1

    # 3
    if row[2] == 'да, один или два':
        dct_type['жертва'] += 1
    elif row[2] == 'нет, мне приятны все':
        dct_type['защитник'] += 1
    elif row[2] == 'мне все не нравятся':
        dct_type['наблюдатель'] += 1
    elif row[2] == 'да, но они не приятны всем в классе':
        dct_type['инициатор'] += 1
        dct_type['помощник'] += 1

    # 4
    if row[3] == 'да, во всем':
        pass
    elif row[3] == 'иногда':
        dct_type['жертва'] += 1
    elif row[3] == 'нет, на меня все равняются':
        dct_type['инициатор'] += 1
        dct_type['защитник'] += 1
        dct_type['наблюдатель'] += 1
    elif row[3] == 'нет, я не чувствую себя хуже других':
        dct_type['помощник'] += 1

    # 5
    if row[4] == 'буду общаться с ним так же, как всегда,':
        dct_type['защитник'] += 1
        dct_type['жертва'] += 1
    elif row[4] == 'буду смеяться над ним':
        dct_type['помощник'] += 1
    elif row[4] == 'перестану с ним общаться':
        dct_type['инициатор'] += 1
    elif row[4] == 'буду общаться только тогда, когда не видят другие ребята':
        dct_type['наблюдатель'] += 1

    # 6
    if row[5] == 'да мы очень дружны':
        dct_type['инициатор'] += 1
    elif row[5] == 'нет, мы почти не общаемся':
        dct_type['помощник'] += 1
    elif row[5] == 'в основном да, если не считать некоторых':
        pass
    elif row[5] == 'у нас есть ребята, которые всех «задирают»':
        dct_type['защитник'] += 1
        dct_type['жертва'] += 1
        dct_type['наблюдатель'] += 1

    # 7
    if row[6] == 'да':
        dct_type['жертва'] += 1
    elif row[6] == 'нет':
        dct_type['защитник'] += 1
        dct_type['инициатор'] += 1
    elif row[6] == 'иногда':
        dct_type['помощник'] += 1
        dct_type['наблюдатель'] += 1
    elif row[6] == 'часто':
        pass

    # 8
    if row[7] == 'облегчение, хорошо, что меня это не касается':
        dct_type['наблюдатель'] += 1
    elif row[7] == 'несправедливость и заступаюсь за одноклассника':
        dct_type['защитник'] += 1
    elif row[7] == 'ничего не чувствую, наверняка он это заслужил':
        dct_type['помощник'] += 1
    elif row[7] == 'мне нет до этого никакого дела':
        dct_type['инициатор'] += 1
        dct_type['жертва'] += 1

    # 9
    if row[8] == 'да, но это бывает редко':
        dct_type['защитник'] += 1
    elif row[8] == 'мы и так постоянно проводим свободное время вместе':
        dct_type['инициатор'] += 1
    elif row[8] == 'нет, мне с ними не интересно':
        dct_type['помощник'] += 1
        dct_type['жертва'] += 1
    elif row[8] == 'нет, потому что некоторые ребята все портят':
        dct_type['наблюдатель'] += 1

    # 10
    if row[9] == 'да это так и мне это неприятно':
        dct_type['наблюдатель'] += 1
    elif row[9] == 'нет, со мной все дружат':
        dct_type['защитник'] += 1
        dct_type['инициатор'] += 1
    elif row[9] == 'да, но меня это устраивает':
        dct_type['жертва'] += 1
    elif row[9] == 'это я не хочу с ними общаться':
        dct_type['помощник'] += 1

    # 11
    if row[10] == 'да, я думаю, что я один из них':
        dct_type['инициатор'] += 1
        dct_type['защитник'] += 1
    elif row[10] == 'да, но они этого не заслуживают':
        dct_type['жертва'] += 1
        dct_type['наблюдатель'] += 1
    elif row[10] == 'нет, у нас таких нет':
        dct_type['помощник'] += 1
    elif row[10] == 'да, я тоже на них равняюсь':
        pass

    # 12
    if row[11] == 'да':
        dct_type['инициатор'] += 1
    elif row[11] == 'нет':
        dct_type['наблюдатель'] += 1
    elif row[11] == 'иногда':
        dct_type['защитник'] += 1
        dct_type['жертва'] += 1
    elif row[11] == 'часто':
        dct_type['помощник'] += 1

    # 14
    if row[13] == 'да, мне не нравится наш коллектив':
        dct_type['наблюдатель'] += 1
    elif row[13] == 'нет, меня все устраивает':
        dct_type['инициатор'] += 1
        dct_type['помощник'] += 1
    elif row[13] == 'иногда, после ссоры с одноклассниками':
        dct_type['защитник'] += 1
    elif row[13] == 'нет, а вдруг там будет хуже':
        dct_type['жертва'] += 1

    # 15
    if row[14] == 'да это самый действенный способ':
        dct_type['помощник'] += 1
    elif row[14] == 'нет, лучше решать «мирным» путем':
        dct_type['защитник'] += 1
    elif row[14] == 'иногда без этого не обойтись':
        dct_type['жертва'] += 1
    elif row[14] == 'все зависит от обстоятельств и от людей':
        dct_type['инициатор'] += 1
        dct_type['наблюдатель'] += 1

    # 16
    if row[15] == 'да и мне их жаль':
        dct_type['защитник'] += 1
    elif row[15] == 'нет, мы все дружим':
        dct_type['инициатор'] += 1
    elif row[15] == 'да, но они этого заслуживают':
        dct_type['помощник'] += 1
        dct_type['наблюдатель'] += 1
    elif row[15] == 'я сам из их числа':
        dct_type['жертва'] += 1

    # 18
    if row[17] == 'пройду мимо это меня не касается':
        dct_type['жертва'] += 1
    elif row[17] == 'обязательно остановлюсь и посмотрю':
        dct_type['инициатор'] += 1
        dct_type['наблюдатель'] += 1
    elif row[17] == 'сниму это все на телефон, и после размещу в интернете, пусть все увидят':
        dct_type['помощник'] += 1
    elif row[17] == 'попытаюсь остановить драку и выяснить в чем дело':
        dct_type['защитник'] += 1

    # 19
    if row[18] == 'да':
        dct_type['помощник'] += 1
    elif row[18] == 'нет':
        dct_type['защитник'] += 1
        dct_type['инициатор'] += 1
    elif row[18] == 'иногда':
        dct_type['наблюдатель'] += 1
    elif row[18] == 'часто':
        dct_type['жертва'] += 1

    # 21
    if row[20] == 'капитаном':
        dct_type['инициатор'] += 1
        dct_type['защитник'] += 1
    elif row[20] == 'помощником капитана':
        dct_type['помощник'] += 1
    elif row[20] == 'обычным матросом':
        dct_type['наблюдатель'] += 1
    elif row[20] == 'юнгой':
        dct_type['жертва'] += 1

    # 22
    if row[21] == 'это повод для насмешек':
        dct_type['помощник'] += 1
    elif row[21] == 'я с таким не буду общаться':
        pass
    elif row[21] == 'меня это не беспокоит, буду общаться':
        dct_type['защитник'] += 1
        dct_type['жертва'] += 1
    elif row[21] == 'не буду общаться, чтобы не уронить свою репутацию':
        dct_type['инициатор'] += 1
        dct_type['наблюдатель'] += 1

    # 23
    if row[22] == 'я буду поступать так же, как все':
        dct_type['инициатор'] += 1
        dct_type['наблюдатель'] += 1
    elif row[22] == 'встану на его защиту':
        dct_type['защитник'] += 1
    elif row[22] == 'один из первых стану смеяться над ним':
        dct_type['помощник'] += 1
    elif row[22] == 'ничего делать не буду, меня это не касается':
        dct_type['жертва'] += 1

    # 24
    if row[23] == 'да, для меня это очень важно':
        dct_type['помощник'] += 1
    elif row[23] == 'нет, мне все равно':
        dct_type['защитник'] += 1
        dct_type['наблюдатель'] += 1
    elif row[23] == 'я всегда пользуюсь успехом':
        dct_type['инициатор'] += 1
    elif row[23] == 'нет, я никогда не был успешен в классе':
        dct_type['жертва'] += 1

    # 25
    if row[24] == 'да':
        dct_type['наблюдатель'] += 1
    elif row[24] == 'нет':
        dct_type['защитник'] += 1
    elif row[24] == 'иногда':
        dct_type['инициатор'] += 1
        dct_type['жертва'] += 1
    elif row[24] == 'часто':
        dct_type['помощник'] += 1

    # сортируем по убыванию
    result_lst = sorted(dct_type.items(), key=lambda t: t[1], reverse=True)
    begin_str = '\n'
    # создаем строку с результатами
    for sphere, value in result_lst:
        begin_str += f'{sphere}: {value};\n'

    # добавляем описание
    return begin_str

def calc_count_level_role(df:pd.DataFrame, lst_cat:list, val_cat, col_cat, lst_cols:list):
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
    count_df['% инициатор от общего'] = round(
        count_df['инициатор'] / count_df['Итого'], 2) * 100
    count_df['% помощник от общего'] = round(
        count_df['помощник'] / count_df['Итого'], 2) * 100
    count_df['% защитник от общего'] = round(
        count_df['защитник'] / count_df['Итого'], 2) * 100
    count_df['% жертва от общего'] = round(
        count_df['жертва'] / count_df['Итого'], 2) * 100
    count_df['% наблюдатель от общего'] = round(
        count_df['наблюдатель'] / count_df['Итого'], 2) * 100

    return count_df


def calc_count_level_thirteen(df:pd.DataFrame, lst_cat:list, val_cat, col_cat, lst_cols:list):
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
    count_df['% да, они всех унижают, а иногда и бьют от общего'] = round(
        count_df['да, они всех унижают, а иногда и бьют'] / count_df['Итого'], 2) * 100
    count_df['% нет, у нас таких нет от общего'] = round(
        count_df['нет, у нас таких нет'] / count_df['Итого'], 2) * 100
    count_df['% я и сам из их числа — меня все боятся от общего'] = round(
        count_df['я и сам из их числа — меня все боятся'] / count_df['Итого'], 2) * 100
    count_df['% конечно, так и должно быть, это нормально от общего'] = round(
        count_df['конечно, так и должно быть, это нормально'] / count_df['Итого'], 2) * 100

    return count_df


def calc_count_level_seventeen(df:pd.DataFrame, lst_cat:list, val_cat, col_cat, lst_cols:list):
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
    count_df['% да, постоянно ссоры и драки от общего'] = round(
        count_df['да, постоянно ссоры и драки'] / count_df['Итого'], 2) * 100
    count_df['% нет, у нас такого не бывает от общего'] = round(
        count_df['нет, у нас такого не бывает'] / count_df['Итого'], 2) * 100
    count_df['% почти нет, если не считать пару случаев от общего'] = round(
        count_df['почти нет, если не считать пару случаев'] / count_df['Итого'], 2) * 100
    count_df['% конечно, так и должно быть от общего'] = round(
        count_df['конечно, так и должно быть'] / count_df['Итого'], 2) * 100

    return count_df

def calc_count_level_twenty(df:pd.DataFrame, lst_cat:list, val_cat, col_cat, lst_cols:list):
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
    count_df['% да от общего'] = round(
        count_df['да'] / count_df['Итого'], 2) * 100
    count_df['% нет от общего'] = round(
        count_df['нет'] / count_df['Итого'], 2) * 100
    count_df['% иногда от общего'] = round(
        count_df['иногда'] / count_df['Итого'], 2) * 100
    count_df['% часто от общего'] = round(
        count_df['часто'] / count_df['Итого'], 2) * 100

    return count_df




def create_result_nvbs(base_df:pd.DataFrame, out_dct:dict, lst_svod_cols:list):
    """
    Функция для подсчета результата если указаны колонки по которым нужно провести свод
    :param df: датафрейм с результатами
    :param out_dct: словарь с уже подсчитанными базовыми данными
    :param lst_svod_cols: список сводных колонок
    :return: словарь
    """
    # Роль
    lst_reindex_one_role_cols = lst_svod_cols.copy()
    lst_reindex_one_role_cols.extend( ['инициатор', 'помощник',
           'защитник','жертва', 'наблюдатель','Итого'])
    # Важные вопросы
    lst_reindex_one_thirteen_cols = lst_svod_cols.copy()
    lst_reindex_one_thirteen_cols.extend( ['да, они всех унижают, а иногда и бьют', 'нет, у нас таких нет',
           'я и сам из их числа — меня все боятся',
           'конечно, так и должно быть, это нормально','Итого'])

    lst_reindex_one_seventeen_cols = lst_svod_cols.copy()
    lst_reindex_one_seventeen_cols.extend( ['да, постоянно ссоры и драки', 'нет, у нас такого не бывает',
           'почти нет, если не считать пару случаев',
           'конечно, так и должно быть','Итого'])

    lst_reindex_one_twenty_cols = lst_svod_cols.copy()
    lst_reindex_one_twenty_cols.extend( ['да', 'нет',
           'иногда','часто','Итого'])

    # Субшкалы
    svod_count_one_level_role_df = calc_count_level_role(base_df, lst_svod_cols,
                                                      'Числовое_значение_роли',
                                                      'Ведущая_Роль',
                                                      lst_reindex_one_role_cols)

    svod_count_one_level_thirteen_df = calc_count_level_thirteen(base_df, lst_svod_cols,
                                                          'Числовое_значение_роли',
                                                          'Вопрос_13',
                                                          lst_reindex_one_thirteen_cols)

    svod_count_one_level_seventeen_df = calc_count_level_seventeen(base_df, lst_svod_cols,
                                                         'Числовое_значение_роли',
                                                         'Вопрос_17',
                                                         lst_reindex_one_seventeen_cols)

    svod_count_one_level_twenty_df = calc_count_level_twenty(base_df, lst_svod_cols,
                                                         'Числовое_значение_роли',
                                                         'Вопрос_20',
                                                         lst_reindex_one_twenty_cols)

    # Считаем среднее по субшкалам
    svod_mean_one_df = pd.pivot_table(base_df,
                                      index=lst_svod_cols,
                                      values=['Числовое_значение_роли',
                                              ],
                                      aggfunc=round_mean)
    svod_mean_one_df.reset_index(inplace=True)
    # упорядочиваем колонки
    new_order_cols = lst_svod_cols.copy()
    new_order_cols.extend((['Числовое_значение_роли',
                            ]))
    svod_mean_one_df = svod_mean_one_df.reindex(columns=new_order_cols)

    dct_rename_cols_mean = {'Числовое_значение_роли': 'Среднее значение ведущей роли',
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
                    f'Свод Роли {out_name}': svod_count_one_level_role_df,
                    f'Свод 13 {out_name}': svod_count_one_level_thirteen_df,
                    f'Свод 17 {out_name}': svod_count_one_level_seventeen_df,
                    f'Свод 20 {out_name}': svod_count_one_level_twenty_df})

    if len(lst_svod_cols) == 1:
        return out_dct
    else:
        for idx, name_column in enumerate(lst_svod_cols):
            # Тревожность
            lst_reindex_column_role_cols = [lst_svod_cols[idx],'инициатор', 'помощник',
                                  'защитник', 'жертва', 'наблюдатель',
                                             'Итого']
            lst_reindex_column_thirteen_cols = [lst_svod_cols[idx],'да, они всех унижают, а иногда и бьют', 'нет, у нас таких нет',
                                      'я и сам из их числа — меня все боятся',
                                      'конечно, так и должно быть, это нормально',
                                             'Итого']
            lst_reindex_column_seventeen_cols = [lst_svod_cols[idx],'да, постоянно ссоры и драки', 'нет, у нас такого не бывает',
                                       'почти нет, если не считать пару случаев',
                                       'конечно, так и должно быть',
                                             'Итого']
            lst_reindex_column_twenty_cols = [lst_svod_cols[idx],'да', 'нет',
                                    'иногда', 'часто',
                                             'Итого']

            # Субшкалы
            svod_count_column_level_role_df = calc_count_level_role(base_df, lst_svod_cols[idx],
                                                                 'Числовое_значение_роли',
                                                                 'Ведущая_Роль',
                                                                 lst_reindex_column_role_cols)

            svod_count_column_level_thirteen_df = calc_count_level_thirteen(base_df, lst_svod_cols[idx],
                                                                         'Числовое_значение_роли',
                                                                         'Вопрос_13',
                                                                         lst_reindex_column_thirteen_cols)

            svod_count_column_level_seventeen_df = calc_count_level_seventeen(base_df, lst_svod_cols[idx],
                                                                           'Числовое_значение_роли',
                                                                           'Вопрос_17',
                                                                           lst_reindex_column_seventeen_cols)

            svod_count_column_level_twenty_df = calc_count_level_twenty(base_df, lst_svod_cols[idx],
                                                                     'Числовое_значение_роли',
                                                                     'Вопрос_20',
                                                                     lst_reindex_column_twenty_cols)

            # Считаем среднее по субшкалам
            svod_mean_column_df = pd.pivot_table(base_df,
                                              index=[lst_svod_cols[idx]],
                                              values=['Числовое_значение_роли',
                                                      ],
                                              aggfunc=round_mean)
            svod_mean_column_df.reset_index(inplace=True)
            # упорядочиваем колонки
            new_order_cols = [lst_svod_cols[idx]].copy()
            new_order_cols.extend((['Числовое_значение_роли',
                                    ]))
            svod_mean_column_df = svod_mean_column_df.reindex(columns=new_order_cols)

            dct_rename_cols_mean = {'Числовое_значение_роли': 'Среднее значение ведущей роли',
                                    }
            svod_mean_column_df.rename(columns=dct_rename_cols_mean, inplace=True)

            name_column = lst_svod_cols[idx]
            name_column = re.sub(r'[\[\]\'+()<> :"?*|\\/]', '_', name_column)
            name_column = name_column[:15]

            out_dct.update({f'Ср {name_column}': svod_mean_column_df,
                            f'Свод Роли {name_column}': svod_count_column_level_role_df,
                            f'Свод 13 {name_column}': svod_count_column_level_thirteen_df,
                            f'Свод 17 {name_column}': svod_count_column_level_seventeen_df,
                            f'Свод 20 {name_column}': svod_count_column_level_twenty_df})
        return out_dct



















def processing_norkina_vbs_school(result_df: pd.DataFrame, answers_df: pd.DataFrame, lst_svod_cols:list):
    """
    Функция для обработки
    :param result_df: часть датафрейма с описательными колонками
    :param answers_df: часть датафрейма с ответами
    :param lst_svod_cols:  список с колонками по которым нужно делать свод
    """
    try:
        out_answer_df = result_df.copy()  # делаем копию для последующего соединения с сырыми ответами
        if len(answers_df.columns) != 25:  # проверяем количество колонок с вопросами
            raise BadCountColumnsVBS

        # очищаем названия колонок от возможных сочетаний .1 которые добавляет пандас при одинаковых колонках
        clean_df_lst = []
        for name_column in answers_df.columns:
            clean_name = re.sub(r'.\d+$', '', name_column)
            clean_df_lst.append(clean_name)

        answers_df.columns = clean_df_lst

        lst_check_cols = ['Среди одноклассников у меня много друзей',
                          'Для меня важна внешность окружающих',
                          'В моем классе есть ребята, которые мне не приятны',
                          'Мне кажется, что мои одноклассники лучше меня',
                          'Если мой одноклассник пришел в очках',
                          'У меня очень дружный класс',
                          'Я часто испытываю чувство одиночества и тревоги',
                          'Если при мне обижают одноклассника, я чувствую',
                          'Я бы хотел проводить больше времени с одноклассниками',
                          'Мне кажется, что мои одноклассники не хотят со мной общаться',
                          'У нас в классе есть пару ребят, на которых все равняются',
                          'Когда меня ругают, я испытываю чувство гнева',
                          'В нашем классе есть несколько ребят, которых все боятся',
                          'Мне бы хотелось учиться в другом классе или школе',
                          'Мне кажется, что с помощью силы можно решить любую проблему',
                          'В моем классе есть один (несколько) человек, с которыми никто не дружит',
                          'Мне кажется, что в нашем классе часто происходят акты насилия (обзывания, насмешки, обидные жесты или действия)',
                          'Если я увижу драку между одноклассниками, то я',
                          'Мне кажется, что в коллективе меня недооценивают',
                          'По-моему, педагоги в школе унижают и оскорбляют учащихся',
                          'Если бы мой класс был на корабле, я бы стал',
                          'Если у человека изъяны во внешности (бородавки, косоглазие, ожирение и др.)',
                          'Если при мне кто-то подвергается насмешкам',
                          'Я часто огорчаюсь, когда не пользуюсь успехом в классе',
                          'Я нуждаюсь в поддержке одноклассников',
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
            raise BadOrderVBS

        valid_values = [['да, я дружу со всеми', 'у меня есть пару друзей', 'нет, я ни с кем не дружу',
                         'мне бы хотелось дружить со всеми'],
                        ['да, если человек мне не симпатичен, я не буду с ним общаться',
                         'нет, главное, чтобы человек был интересен', 'я сам страдаю из-за своей внешности',
                         'конечно, если человек не обладает хорошей внешностью, он не заслуживает ничего хорошего'],
                        ['да, один или два', 'нет, мне приятны все', 'мне все не нравятся',
                         'да, но они не приятны всем в классе'],
                        ['да, во всем', 'иногда', 'нет, на меня все равняются', 'нет, я не чувствую себя хуже других'],
                        ['буду общаться с ним так же, как всегда,', 'буду смеяться над ним', 'перестану с ним общаться',
                         'буду общаться только тогда, когда не видят другие ребята'],
                        ['да мы очень дружны', 'нет, мы почти не общаемся', 'в основном да, если не считать некоторых',
                         'у нас есть ребята, которые всех «задирают»'],
                        ['да', 'нет', 'иногда', 'часто'],
                        ['облегчение, хорошо, что меня это не касается', 'несправедливость и заступаюсь за одноклассника',
                         'ничего не чувствую, наверняка он это заслужил', 'мне нет до этого никакого дела'],
                        ['да, но это бывает редко', 'мы и так постоянно проводим свободное время вместе',
                         'нет, мне с ними не интересно', 'нет, потому что некоторые ребята все портят'],
                        ['да это так и мне это неприятно', 'нет, со мной все дружат', 'да, но меня это устраивает',
                         'это я не хочу с ними общаться'],
                        ['да, я думаю, что я один из них', 'да, но они этого не заслуживают', 'нет, у нас таких нет',
                         'да, я тоже на них равняюсь'],
                        ['да', 'нет', 'иногда', 'часто'],
                        ['да, они всех унижают, а иногда и бьют', 'нет, у нас таких нет',
                         'я и сам из их числа — меня все боятся', 'конечно, так и должно быть, это нормально'],
                        ['да, мне не нравится наш коллектив', 'нет, меня все устраивает',
                         'иногда, после ссоры с одноклассниками', 'нет, а вдруг там будет хуже'],
                        ['да это самый действенный способ', 'нет, лучше решать «мирным» путем',
                         'иногда без этого не обойтись', 'все зависит от обстоятельств и от людей'],
                        ['да и мне их жаль', 'нет, мы все дружим', 'да, но они этого заслуживают', 'я сам из их числа'],
                        ['да, постоянно ссоры и драки', 'нет, у нас такого не бывает',
                         'почти нет, если не считать пару случаев', 'конечно, так и должно быть'],
                        ['пройду мимо это меня не касается', 'обязательно остановлюсь и посмотрю',
                         'сниму это все на телефон, и после размещу в интернете, пусть все увидят',
                         'попытаюсь остановить драку и выяснить в чем дело'],
                        ['да', 'нет', 'иногда', 'часто'],
                        ['да', 'нет', 'иногда', 'часто'],
                        ['капитаном', 'помощником капитана', 'обычным матросом', 'юнгой'],
                        ['это повод для насмешек', 'я с таким не буду общаться', 'меня это не беспокоит, буду общаться',
                         'не буду общаться, чтобы не уронить свою репутацию'],
                        ['я буду поступать так же, как все', 'встану на его защиту',
                         'один из первых стану смеяться над ним', 'ничего делать не буду, меня это не касается'],
                        ['да, для меня это очень важно', 'нет, мне все равно', 'я всегда пользуюсь успехом',
                         'нет, я никогда не был успешен в классе'],
                        ['да', 'нет', 'иногда', 'часто']
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
            raise BadValueVBS

        base_df = pd.DataFrame()

        base_df[f'Распределение'] = answers_df.apply(processing_result_vbs, axis=1)
        base_df[f'Ведущая_Роль'] = base_df[f'Распределение'].apply(
            extract_key_max_value)
        base_df[f'Числовое_значение_роли'] = base_df[f'Распределение'].apply(
            extract_max_value)
        base_df['Вопрос_13'] = answers_df['В нашем классе есть несколько ребят, которых все боятся']
        base_df['Вопрос_17'] = answers_df[
            'Мне кажется, что в нашем классе часто происходят акты насилия (обзывания, насмешки, обидные жесты или действия)']
        base_df['Вопрос_20'] = answers_df['По-моему, педагоги в школе унижают и оскорбляют учащихся']


        # Создаем датафрейм для создания части в общий датафрейм
        part_df = pd.DataFrame()
        part_df['ВБС_Распределение'] = base_df['Распределение']
        part_df['ВБС_Ведущая_Роль'] = base_df['Ведущая_Роль']
        part_df['ВБС_Ведущая_Роль_Значение'] = base_df['Числовое_значение_роли']

        out_answer_df = pd.concat([out_answer_df, answers_df], axis=1)  # Датафрейм для проверки
        # Соединяем анкетную часть с результатной
        base_df = pd.concat([result_df, base_df], axis=1)
        base_df.sort_values(by='Числовое_значение_роли', ascending=False, inplace=True)  # сортируем

        # считаем среднее значение по шкалам
        avg_role = round(base_df['Числовое_значение_роли'].mean(), 2)

        avg_dct = {'Среднее значение ведущей роли': avg_role,
                   }

        avg_df = pd.DataFrame.from_dict(avg_dct, orient='index')
        avg_df = avg_df.reset_index()
        avg_df.columns = ['Показатель', 'Среднее значение']

        # Общий свод по ролям всего в процентном соотношении
        base_svod_all_df = pd.DataFrame(
            index=['инициатор', 'помощник',
                   'защитник',
                   'жертва', 'наблюдатель', 'Итого'])

        svod_level_df = pd.pivot_table(base_df, index='Ведущая_Роль',
                                       values='Числовое_значение_роли',
                                       aggfunc='count')

        svod_level_df['% от общего'] = round(
            svod_level_df['Числовое_значение_роли'] / svod_level_df['Числовое_значение_роли'].sum(), 3) * 100

        base_svod_all_df = base_svod_all_df.join(svod_level_df)

        # # Создаем суммирующую строку
        base_svod_all_df.loc['Итого'] = svod_level_df.sum()
        base_svod_all_df.reset_index(inplace=True)
        base_svod_all_df.rename(columns={'index': 'Роль', 'Максимум': 'Количество'}, inplace=True)

        # Общий свод по вопросу 13 в процентном соотношении
        thirteen_svod_all_df = pd.DataFrame(
            index=['да, они всех унижают, а иногда и бьют', 'нет, у нас таких нет',
                   'я и сам из их числа — меня все боятся',
                   'конечно, так и должно быть, это нормально', 'Итого'])

        thirteen_svod_level_df = pd.pivot_table(base_df, index='Вопрос_13',
                                                values='Числовое_значение_роли',
                                                aggfunc='count')

        thirteen_svod_level_df['% от общего'] = round(
            thirteen_svod_level_df['Числовое_значение_роли'] / thirteen_svod_level_df['Числовое_значение_роли'].sum(),
            3) * 100

        thirteen_svod_all_df = thirteen_svod_all_df.join(thirteen_svod_level_df)

        # # Создаем суммирующую строку
        thirteen_svod_all_df.loc['Итого'] = svod_level_df.sum()
        thirteen_svod_all_df.reset_index(inplace=True)
        thirteen_svod_all_df.rename(columns={'index': 'Ответ', 'Числовое_значение_роли': 'Количество'}, inplace=True)

        # Общий свод по вопросу 17 в процентном соотношении
        seventeen_svod_all_df = pd.DataFrame(
            index=['да, постоянно ссоры и драки', 'нет, у нас такого не бывает',
                   'почти нет, если не считать пару случаев',
                   'конечно, так и должно быть', 'Итого'])

        seventeen_svod_level_df = pd.pivot_table(base_df, index='Вопрос_17',
                                                 values='Числовое_значение_роли',
                                                 aggfunc='count')

        seventeen_svod_level_df['% от общего'] = round(
            seventeen_svod_level_df['Числовое_значение_роли'] / seventeen_svod_level_df['Числовое_значение_роли'].sum(),
            3) * 100

        seventeen_svod_all_df = seventeen_svod_all_df.join(seventeen_svod_level_df)

        # # Создаем суммирующую строку
        seventeen_svod_all_df.loc['Итого'] = svod_level_df.sum()
        seventeen_svod_all_df.reset_index(inplace=True)
        seventeen_svod_all_df.rename(columns={'index': 'Ответ', 'Числовое_значение_роли': 'Количество'}, inplace=True)

        # Общий свод по вопросу 20 в процентном соотношении
        twenty_svod_all_df = pd.DataFrame(
            index=['да', 'нет',
                   'иногда',
                   'часто', 'Итого'])

        twenty_svod_level_df = pd.pivot_table(base_df, index='Вопрос_20',
                                              values='Числовое_значение_роли',
                                              aggfunc='count')

        twenty_svod_level_df['% от общего'] = round(
            twenty_svod_level_df['Числовое_значение_роли'] / twenty_svod_level_df['Числовое_значение_роли'].sum(), 3) * 100

        twenty_svod_all_df = twenty_svod_all_df.join(twenty_svod_level_df)

        # # Создаем суммирующую строку
        twenty_svod_all_df.loc['Итого'] = svod_level_df.sum()
        twenty_svod_all_df.reset_index(inplace=True)
        twenty_svod_all_df.rename(columns={'index': 'Ответ', 'Числовое_значение_роли': 'Количество'}, inplace=True)

        # формируем основной словарь
        out_dct = {'Списочный результат': base_df, 'Список для проверки': out_answer_df,
                   'Свод по ролям': base_svod_all_df,
                   'Среднее':avg_df,
                   'Свод по вопросу 13': thirteen_svod_all_df,
                   'Свод по вопросу 17': seventeen_svod_all_df,
                   'Свод по вопросу 20': twenty_svod_all_df,

                   }

        lst_level = ['инициатор', 'помощник',
                     'защитник',
                     'жертва', 'наблюдатель']
        dct_level = dict()

        for level in lst_level:
            temp_df = base_df[base_df['Ведущая_Роль'] == level]
            if temp_df.shape[0] != 0:
                dct_level[level] = temp_df

        out_dct.update(dct_level)

        """
            Сохраняем в зависимости от необходимости делать своды по определенным колонкам
            """
        if len(lst_svod_cols) == 0:
            return out_dct, part_df
        else:
            out_dct = create_result_nvbs(base_df, out_dct, lst_svod_cols)

            return out_dct, part_df

    except BadOrderVBS:
        messagebox.showerror('Лахеcис',
                             f'При обработке вопросов теста Выявление буллинг-структуры Норкина обнаружены неправильные вопросы. Проверьте названия колонок с вопросами:\n'
                             f'{error_order_message}\n'
                             f'Используйте при создании Яндекс-формы написание вопросов из руководства пользователя программы Лахесис.')
    except BadValueVBS:
        messagebox.showerror('Лахеcис',
                             f'При обработке вопросов теста Выявление буллинг-структуры Норкина обнаружены неправильные варианты ответов. Проверьте ответы на указанных строках:\n'
                             f'{error_message}\n'
                             f'Используйте при создании Яндекс-формы написание вариантов ответа из руководства пользователя программы Лахесис.')


    except BadCountColumnsVBS:
        messagebox.showerror('Лахеcис',
                             f'Проверьте количество колонок с ответами на тест Выявление буллинг-структуры Норкина\n'
                             f'Должно быть 25 колонок с ответами')
