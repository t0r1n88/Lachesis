"""
Скрипт для обработки результатов Опросник суицидального риска А.Г. Шмелев Т.Н. Разуваева
"""

import pandas as pd
import re
from tkinter import messagebox
from lachesis_support_functions import round_mean_two,calc_count_scale,create_union_svod, create_list_on_level

class BadOrderOSRSHR(Exception):
    """
    Исключение для обработки случая когда колонки не совпадают
    """
    pass


class BadValueOSRSHR(Exception):
    """
    Исключение для неправильных значений в вариантах ответов
    """
    pass

class BadCountColumnsOSRSHR(Exception):
    """
    Исключение для обработки случая если количество колонок не равно 29
    """
    pass

def calc_level(value):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """
    if 0<= value <= 8:
        return f'0-8 ИП СР'
    elif 9 <= value <= 17:
        return f'9-17 ИП СР'
    elif 18 <= value <= 24:
        return f'18-24 ИП СР'
    else:
        return f'25-29 ИП СР'


def calc_value_d(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [12,14,20,22,27]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_pr:
            if value == 1:
                value_forward += 1

    return value_forward

def calc_value_a(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [1,10,20,23,28,29]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_pr:
            if value == 1:
                value_forward += 1

    return value_forward

def calc_value_u(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [1,12,14,22,27]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_pr:
            if value == 1:
                value_forward += 1

    return value_forward

def calc_value_n(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [2,3,6,7,17]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_pr:
            if value == 1:
                value_forward += 1

    return value_forward

def calc_value_sp(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [5,11,13,15,17,22,25]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_pr:
            if value == 1:
                value_forward += 1

    return value_forward

def calc_value_skb(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [8,9,18]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_pr:
            if value == 1:
                value_forward += 1

    return value_forward

def calc_value_m(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [4,16]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_pr:
            if value == 1:
                value_forward += 1

    return value_forward

def calc_value_vp(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [2,3,12,24,26,27]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_pr:
            if value == 1:
                value_forward += 1

    return value_forward

def calc_value_af(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [19,21]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_pr:
            if value == 1:
                value_forward += 1

    return value_forward


def calc_level_scale(value,count):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """
    result = round((value / count) * 100)

    return f'{result}%'


def calc_level_procent(value:str):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """
    try:
        value = int(value.replace('%',''))
        if 0 <= value <= 25:
            return '0-25%'
        elif 26<= value <= 50:
            return '26-50%'
        elif 51 <= value <= 75:
            return '51-75%'
        else:
            return '76-100%'

    except:
        return 'ошибочное значение'


def create_itog_stens(row):
    """
    Функция для создания строки с итоговым стеном
    :param row: строка с результатами
    :return:
    """
    lst_out = list(map(str,row))
    return '-'.join(lst_out)



def create_list_on_level_ip(base_df:pd.DataFrame, out_dct:dict, lst_level:list, dct_prefix:dict):
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
                if level == '0-8 ИП СР':
                    level = '0-8'
                elif level == '9-17 ИП СР':
                    level = '9-17'
                elif level == '18-24 ИП СР':
                    level = '18-24'
                else:
                    level = '25-29'
                dct_level[f'{dct_prefix[key]}. {level}'] = temp_df
        out_dct.update(dct_level)

    return out_dct





def create_result_osr_shm_raz(base_df:pd.DataFrame, out_dct:dict, lst_svod_cols:list):
    """
    Функция для подсчета результата если указаны колонки по которым нужно провести свод
    :param df: датафрейм с результатами
    :param out_dct: словарь с уже подсчитанными базовыми данными
    :param lst_svod_cols: список сводных колонок
    :return: словарь
    """
    lst_level = ['редкое использование', 'умеренное использование', 'выраженное использование']
    lst_reindex_one_level_cols = lst_svod_cols.copy()
    lst_reindex_one_level_cols.extend(['редкое использование', 'умеренное использование', 'выраженное использование', 'высокий показатель',
                                       'Итого'])  # Основная шкала





def processing_osr_shmel_raz(base_df: pd.DataFrame, answers_df: pd.DataFrame, lst_svod_cols:list):
    """
    Функция для обработки
    :param base_df: часть датафрейма с описательными колонками
    :param answers_df: часть датафрейма с ответами
    :param lst_svod_cols:  список с колонками по которым нужно делать свод
    """
    out_answer_df = base_df.copy()  # делаем копию для последующего соединения с сырыми ответами
    union_base_df = base_df.copy()  # делаем копию анкетной части чтобы потом соединить ее с ответной частью
    quantity_cols_base_df = base_df.shape[1]  # количество колонок в анкетной части

    if len(answers_df.columns) != 29:  # проверяем количество колонок с вопросами
        raise BadCountColumnsOSRSHR

    # очищаем названия колонок от возможных сочетаний .1 которые добавляет пандас при одинаковых колонках
    clean_df_lst = []
    for name_column in answers_df.columns:
        clean_name = re.sub(r'.\d+$', '', name_column)
        clean_df_lst.append(clean_name)

    answers_df.columns = clean_df_lst

    lst_check_cols = ['Вы все чувствуете острее, чем большинство людей',
                      'Вас часто одолевают мрачные мысли',
                      'Теперь вы уже не надеетесь добиться желаемого положения в жизни',
                      'В случае неудачи вам трудно начать новое дело',
                      'Вам определенно не везет в жизни',
                      'Учиться вам стало труднее, чем раньше',
                      'Большинство людей довольны жизнью больше, чем вы',
                      'Вы считаете, что смерть является искуплением грехов',
                      'Только зрелый человек может принять решение уйти из жизни',
                      'Временами у вас бывают приступы неудержимого смеха или плача',

                      'Обычно вы осторожны с людьми, которые относятся к вам дружелюбнее, чем вы ожидали',
                      'Вы считаете себя обреченным человеком',
                      'Мало кто искренне пытается помочь другим, если это связано с неудобствами',
                      'У Вас такое впечатление, что вас никто не понимает',
                      'Человек, который вводит других в соблазн, оставляя без присмотра ценное имущество, виноват примерно столько же, сколько и тот, кто это имущество похищает',
                      'В вашей жизни не было таких неудач, когда казалось, что все кончено',
                      'Обычно вы удовлетворены своей судьбой',
                      'Вы считаете, что всегда нужно вовремя поставить точку',
                      'В вашей жизни есть люди, привязанность к которым может очень повлиять на ваши решения и даже изменить их',
                      'Когда вас обижают, вы стремитесь во что бы то ни стало доказать обидчику, что он поступил несправедливо',

                      'Часто вы так переживаете, что это мешает вам говорить',
                      'Вам часто кажется, что обстоятельства, в которых вы оказались, отличаются особой несправедливостью',
                      'Иногда вам кажется, что вы вдруг сделали что-то скверное или даже хуже',
                      'Будущее представляется вам довольно беспросветным',
                      'Большинство людей способны добиваться выгоды не совсем честным путем',
                      'Будущее слишком расплывчато, чтобы строить серьезные планы',
                      'Мало кому в жизни пришлось испытать то, что пережили недавно вы',
                      'Вы склонны так остро переживать неприятности, что не можете выкинуть мысли об этом из головы',
                      'Часто вы действуете необдуманно, повинуясь первому порыву',
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
        raise BadOrderOSRSHR

    # словарь для замены слов на числа
    dct_replace_value = {'нет': 0,
                         'да': 1,
                         }
    valid_values = [0,1]
    answers_df.replace(dct_replace_value, inplace=True)  # заменяем слова на цифры для подсчетов
    # Проверяем, есть ли значения, отличающиеся от указанных в списке
    lst_error_answers = []  # список для хранения строк где найдены неправильные ответы

    for i in range(29):
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
        raise BadValueOSRSHR

    base_df['ИП_Значение'] = answers_df.sum(axis=1)
    base_df['ИП_Диапазон'] = base_df['ИП_Значение'].apply(calc_level)

    base_df['Д_Значение'] = answers_df.apply(calc_value_d,axis=1)
    base_df['Д_Процент'] = base_df['Д_Значение'].apply(lambda x:calc_level_scale(x,5))
    base_df['Д_Диапазон_Пр'] = base_df['Д_Процент'].apply(calc_level_procent)

    base_df['А_Значение'] = answers_df.apply(calc_value_a,axis=1)
    base_df['А_Процент'] = base_df['А_Значение'].apply(lambda x:calc_level_scale(x,6))
    base_df['А_Диапазон_Пр'] = base_df['А_Процент'].apply(calc_level_procent)

    base_df['У_Значение'] = answers_df.apply(calc_value_u,axis=1)
    base_df['У_Процент'] = base_df['У_Значение'].apply(lambda x:calc_level_scale(x,5))
    base_df['У_Диапазон_Пр'] = base_df['У_Процент'].apply(calc_level_procent)

    base_df['Н_Значение'] = answers_df.apply(calc_value_n,axis=1)
    base_df['Н_Процент'] = base_df['Н_Значение'].apply(lambda x:calc_level_scale(x,5))
    base_df['Н_Диапазон_Пр'] = base_df['Н_Процент'].apply(calc_level_procent)

    base_df['СП_Значение'] = answers_df.apply(calc_value_sp,axis=1)
    base_df['СП_Процент'] = base_df['СП_Значение'].apply(lambda x:calc_level_scale(x,7))
    base_df['СП_Диапазон_Пр'] = base_df['СП_Процент'].apply(calc_level_procent)

    base_df['СКБ_Значение'] = answers_df.apply(calc_value_skb,axis=1)
    base_df['СКБ_Процент'] = base_df['СКБ_Значение'].apply(lambda x:calc_level_scale(x,3))
    base_df['СКБ_Диапазон_Пр'] = base_df['СКБ_Процент'].apply(calc_level_procent)

    base_df['М_Значение'] = answers_df.apply(calc_value_m,axis=1)
    base_df['М_Процент'] = base_df['М_Значение'].apply(lambda x:calc_level_scale(x,2))
    base_df['М_Диапазон_Пр'] = base_df['М_Процент'].apply(calc_level_procent)

    base_df['ВП_Значение'] = answers_df.apply(calc_value_vp,axis=1)
    base_df['ВП_Процент'] = base_df['ВП_Значение'].apply(lambda x:calc_level_scale(x,6))
    base_df['ВП_Диапазон_Пр'] = base_df['ВП_Процент'].apply(calc_level_procent)

    base_df['АФ_Значение'] = answers_df.apply(calc_value_af,axis=1)
    base_df['АФ_Процент'] = base_df['АФ_Значение'].apply(lambda x:calc_level_scale(x,2))
    base_df['АФ_Диапазон_Пр'] = base_df['АФ_Процент'].apply(calc_level_procent)

    # Упорядочиваем
    result_df = base_df.iloc[:, quantity_cols_base_df:]  # отсекаем часть с результатами чтобы упорядочить
    lst_stens = [column for column in result_df.columns if 'Процент' in column]
    result_df['Проценты_по_шкалам'] = result_df[lst_stens].apply(create_itog_stens, axis=1)

    new_order_lst = ['ИП_Значение','ИП_Диапазон','Проценты_по_шкалам',
                     'Д_Процент', 'А_Процент', 'У_Процент', 'Н_Процент',
                     'СП_Процент', 'СКБ_Процент', 'М_Процент', 'ВП_Процент',
                     'АФ_Процент',

                     'Д_Диапазон_Пр', 'А_Диапазон_Пр', 'У_Диапазон_Пр', 'Н_Диапазон_Пр',
                     'СП_Диапазон_Пр', 'СКБ_Диапазон_Пр', 'М_Диапазон_Пр', 'ВП_Диапазон_Пр',
                     'АФ_Диапазон_Пр',

                     'Д_Значение', 'А_Значение', 'У_Значение', 'Н_Значение',
                     'СП_Значение', 'СКБ_Значение', 'М_Значение', 'ВП_Значение',
                     'АФ_Значение'
                     ]
    result_df = result_df.reindex(columns=new_order_lst)  # изменяем порядок
    base_df = pd.concat([union_base_df, result_df], axis=1)  # соединяем и перезаписываем base_df

    # Создаем датафрейм для создания части в общий датафрейм
    part_df = pd.DataFrame()
    # Общая тревожность
    part_df['ОСРШР_ИП_Значение'] = base_df['ИП_Значение']
    part_df['ОСРШР_ИП_Диапазон'] = base_df['ИП_Диапазон']
    part_df['ОСРШР_Проценты_по_шкалам'] = base_df['Проценты_по_шкалам']

    part_df['ОСРШР_Д_Процент'] = base_df['Д_Процент']
    part_df['ОСРШР_А_Процент'] = base_df['А_Процент']
    part_df['ОСРШР_У_Процент'] = base_df['У_Процент']
    part_df['ОСРШР_Н_Процент'] = base_df['Н_Процент']

    part_df['ОСРШР_СП_Процент'] = base_df['СП_Процент']
    part_df['ОСРШР_СКБ_Процент'] = base_df['СКБ_Процент']
    part_df['ОСРШР_М_Процент'] = base_df['М_Процент']
    part_df['ОСРШР_ВП_Процент'] = base_df['ВП_Процент']

    part_df['ОСРШР_АФ_Процент'] = base_df['АФ_Процент']

    part_df['ОСРШР_Д_Диапазон_Пр'] = base_df['Д_Диапазон_Пр']
    part_df['ОСРШР_А_Диапазон_Пр'] = base_df['А_Диапазон_Пр']
    part_df['ОСРШР_У_Диапазон_Пр'] = base_df['У_Диапазон_Пр']
    part_df['ОСРШР_Н_Диапазон_Пр'] = base_df['Н_Диапазон_Пр']

    part_df['ОСРШР_СП_Диапазон_Пр'] = base_df['СП_Диапазон_Пр']
    part_df['ОСРШР_СКБ_Диапазон_Пр'] = base_df['СКБ_Диапазон_Пр']
    part_df['ОСРШР_М_Диапазон_Пр'] = base_df['М_Диапазон_Пр']
    part_df['ОСРШР_ВП_Диапазон_Пр'] = base_df['ВП_Диапазон_Пр']

    part_df['ОСРШР_АФ_Диапазон_Пр'] = base_df['АФ_Диапазон_Пр']

    part_df['ОСРШР_Д_Значение'] = base_df['Д_Значение']
    part_df['ОСРШР_А_Значение'] = base_df['А_Значение']
    part_df['ОСРШР_У_Значение'] = base_df['У_Значение']
    part_df['ОСРШР_Н_Значение'] = base_df['Н_Значение']

    part_df['ОСРШР_СП_Значение'] = base_df['СП_Значение']
    part_df['ОСРШР_СКБ_Значение'] = base_df['СКБ_Значение']
    part_df['ОСРШР_М_Значение'] = base_df['М_Значение']
    part_df['ОСРШР_ВП_Значение'] = base_df['ВП_Значение']

    part_df['ОСРШР_АФ_Значение'] = base_df['АФ_Значение']

    out_answer_df = pd.concat([out_answer_df, answers_df], axis=1)  # Датафрейм для проверки

    base_df.sort_values(by='ИП_Значение', inplace=True, ascending=False)

    # Делаем свод  по  ИП
    dct_svod = {'ИП_Значение': 'ИП_Диапазон',
                    }

    dct_rename_svod = {
        'ИП_Значение': 'Диапазон интегрального показателя суицидального риска',
    }

    lst_base = ['0-8 ИП СР', '9-17 ИП СР', '18-24 ИП СР', '25-29 ИП СР']
    base_svod_df = create_union_svod(base_df, dct_svod, dct_rename_svod, lst_base)

    # Делаем свод  по  шкалам
    dct_svod_sub = {'Д_Значение': 'Д_Диапазон_Пр',
                    'А_Значение': 'А_Диапазон_Пр',
                    'У_Значение': 'У_Диапазон_Пр',
                    'Н_Значение': 'Н_Диапазон_Пр',

                    'СП_Значение': 'СП_Диапазон_Пр',
                    'СКБ_Значение': 'СКБ_Диапазон_Пр',
                    'М_Значение': 'М_Диапазон_Пр',
                    'ВП_Значение': 'ВП_Диапазон_Пр',
                    'АФ_Значение': 'АФ_Диапазон_Пр',
                    }

    dct_rename_svod_sub = {'Д_Значение': 'Д',
                           'А_Значение': 'А',
                           'У_Значение': 'У',
                           'Н_Значение': 'Н',

                           'СП_Значение': 'СП',
                           'СКБ_Значение': 'СКБ',
                           'М_Значение': 'М',
                           'ВП_Значение': 'ВП',
                           'АФ_Значение': 'АФ',
                           }

    lst_sub = ['0-25%', '26-50%', '51-75%', '76-100%']

    base_svod_sub_df = create_union_svod(base_df, dct_svod_sub, dct_rename_svod_sub, lst_sub)

    # считаем среднее значение по шкалам
    avg_ip = round(base_df['ИП_Значение'].mean(), 2)
    avg_k = round(base_df['Д_Значение'].mean(), 2)
    avg_d = round(base_df['А_Значение'].mean(), 2)
    avg_s = round(base_df['У_Значение'].mean(), 2)
    avg_psp = round(base_df['Н_Значение'].mean(), 2)

    avg_po = round(base_df['СП_Значение'].mean(), 2)
    avg_bi = round(base_df['СКБ_Значение'].mean(), 2)
    avg_prp = round(base_df['М_Значение'].mean(), 2)
    avg_pp = round(base_df['ВП_Значение'].mean(), 2)
    avg_af = round(base_df['АФ_Значение'].mean(), 2)

    avg_dct = {'Среднее значение интегрального показателя': avg_ip,
               'Среднее значение субшкалы Демонстративность': avg_k,
               'Среднее значение субшкалы Аффективность': avg_d,
               'Среднее значение субшкалы Уникальность': avg_s,
               'Среднее значение субшкалы Несостоятельность': avg_psp,

               'Среднее значение субшкалы Социальный пессимизм': avg_po,
               'Среднее значение субшкалы Слом культурных барьеров': avg_bi,
               'Среднее значение субшкалы Максимализм': avg_prp,
               'Среднее значение субшкалы Временная перспектива': avg_pp,
               'Среднее значение субшкалы Антисуицидальный фактор': avg_af,
               }

    avg_df = pd.DataFrame.from_dict(avg_dct, orient='index')
    avg_df = avg_df.reset_index()
    avg_df.columns = ['Показатель', 'Среднее значение']

    # формируем основной словарь
    out_dct = {'Списочный результат': base_df,
               'Список для проверки': out_answer_df,
               'Свод ИП': base_svod_df,
               'Свод Шкалы': base_svod_sub_df,
               'Среднее': avg_df,
               }

    dct_prefix_ip = {'ИП_Диапазон': 'ИП',

                  }
    out_dct = create_list_on_level_ip(base_df, out_dct, lst_base, dct_prefix_ip)

    dct_prefix = {'Д_Диапазон_Пр': 'Д',
                  'А_Диапазон_Пр': 'А',
                  'У_Диапазон_Пр': 'У',
                  'Н_Диапазон_Пр': 'Н',

                  'СП_Диапазон_Пр': 'СП',
                  'СКБ_Диапазон_Пр': 'СКБ',
                  'М_Диапазон_Пр': 'М',
                  'ВП_Диапазон_Пр': 'ВП',
                  'АФ_Диапазон_Пр': 'АФ',

                  }

    out_dct = create_list_on_level(base_df, out_dct, lst_sub, dct_prefix)
    """
                    Сохраняем в зависимости от необходимости делать своды по определенным колонкам
                    """
    if len(lst_svod_cols) == 0:
        return out_dct, part_df

    else:
        out_dct = create_result_osr_shm_raz(base_df, out_dct, lst_svod_cols)
        return out_dct, part_df
















