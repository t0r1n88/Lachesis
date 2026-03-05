"""
Скрипт для обработки результатов теста Виртуальная идентичность пользователей социальных сетей Погорелов
"""

import pandas as pd
import re
from tkinter import messagebox
from lachesis_support_functions import round_mean_two,calc_count_scale,create_union_svod, create_list_on_level

class BadOrderVIPSSP(Exception):
    """
    Исключение для обработки случая когда колонки не совпадают
    """
    pass


class BadValueVIPSSP(Exception):
    """
    Исключение для неправильных значений в вариантах ответов
    """
    pass

class BadCountColumnsVIPSSP(Exception):
    """
    Исключение для обработки случая если количество колонок не равно 43
    """
    pass

class NotReqColumn(Exception):
    """
    Исключение для обработки случая когда нет обязательной колонки Возраст
    """
    pass

class BadValueAge(Exception):
    """
    Исключение для обработки случая когда в колонке Возраст есть значения отличающиеся от требуемых
    """
    pass




def calc_value_ka(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [2,4,8,11,14,16,20,22,23,26,28,35,38,39,41,42,43]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_pr:
            value_forward += value
    return value_forward

def calc_ka_sten(ser:pd.Series):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """
    row = ser.tolist() # превращаем в список
    age = row[0] # возраст
    value = row[1] # значение которое нужно обработать

    if age == '18-35 лет':
        if value <= 39:
            return 1
        elif 40<= value <= 44:
            return 2
        elif 45<= value <=49:
            return 3
        elif 50<= value <=53:
            return 4
        elif 54<=value <=58:
            return 5
        elif 59<= value <= 62:
            return 6
        elif 63<= value <= 67:
            return 7
        elif 68<= value <=72:
            return 8
        elif 73<= value <=76:
            return 9
        else:
            return 10
    elif age == '36-57 лет':
        if value <= 37:
            return 1
        elif 38<= value <=41:
            return 2
        elif 42<= value <=45:
            return 3
        elif 46<= value <=49:
            return 4
        elif 50<=value ==54:
            return 5
        elif 55<= value <=58:
            return 6
        elif 59<= value <=62:
            return 7
        elif 63<= value <=67:
            return 8
        elif 68<= value <=71:
            return 9
        else:
            return 10

def calc_level(value):
    """
    Функция для подсчета диапазонов
    :param value: значение
    :return:
    """
    if 1 <= value <= 3:
        return 'низкий уровень'
    elif 4 <=value <= 7:
        return 'средний уровень'
    else:
        return 'высокий уровень'


def calc_value_ps(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [3,6,7,12,13,15,18,19,24,27,31,32,34,37,40]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_pr:
            value_forward += value
    return value_forward


def calc_ps_sten(ser:pd.Series):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """
    row = ser.tolist() # превращаем в список
    age = row[0] # возраст
    value = row[1] # значение которое нужно обработать
    if age == '18-35 лет':
        if  value <=30 :
            return 1
        elif  31<= value <=35 :
            return 2
        elif  36<= value <=39 :
            return 3
        elif  40<= value <=44 :
            return 4
        elif 45<= value <=48 :
            return 5
        elif  49<= value <=53 :
            return 6
        elif  54<= value <=57 :
            return 7
        elif 58<= value <=62 :
            return 8
        elif  63<= value <=66 :
            return 9
        else:
            return 10
    elif age == '36-57 лет':
        if value <= 30:
            return 1
        elif 31<= value <=34 :
            return 2
        elif 35<= value <=39 :
            return 3
        elif 40<= value <=43 :
            return 4
        elif 44<=value <=47 :
            return 5
        elif  48<= value <=52 :
            return 6
        elif  53<= value <=56 :
            return 7
        elif  57<= value <=60 :
            return 8
        elif  61<= value <=64 :
            return 9
        else:
            return 10


def calc_value_vo(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [1,5,9,10,17,21,25,29,30,33,36]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_pr:
            value_forward += value
    return value_forward


def calc_vo_sten(ser:pd.Series):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """
    row = ser.tolist() # превращаем в список
    age = row[0] # возраст
    value = row[1] # значение которое нужно обработать
    if age == '18-35 лет':
        if  value <=24 :
            return 1
        elif  25<= value <=27 :
            return 2
        elif  28<= value <=31 :
            return 3
        elif  32<= value <=34 :
            return 4
        elif 35<= value <=38 :
            return 5
        elif  39<= value <=41 :
            return 6
        elif  42<= value <=45 :
            return 7
        elif 46<= value <=49 :
            return 8
        elif  50<= value <=52 :
            return 9
        else:
            return 10
    elif age == '36-57 лет':
        if value <= 20:
            return 1
        elif 21<= value <=23 :
            return 2
        elif 24<= value <=26 :
            return 3
        elif 27<= value <=30 :
            return 4
        elif 31<=value <=33 :
            return 5
        elif  34<= value <=36 :
            return 6
        elif  37<= value <=39 :
            return 7
        elif  40<= value <=42 :
            return 8
        elif  43<= value <=45 :
            return 9
        else:
            return 10



def calc_ip_sten(ser:pd.Series):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """
    row = ser.tolist() # превращаем в список
    age = row[0] # возраст
    value = row[1] # значение которое нужно обработать
    if age == '18-35 лет':
        if  value <= 91:
            return 1
        elif  92<= value <=104 :
            return 2
        elif  105<= value <=117 :
            return 3
        elif  118<= value <=131 :
            return 4
        elif 132<= value <=144 :
            return 5
        elif  145<= value <=157 :
            return 6
        elif  158<= value <=170 :
            return 7
        elif 171<= value <=184 :
            return 8
        elif  185<= value <=197 :
            return 9
        else:
            return 10
    elif age == '36-57 лет':
        if value <= 84:
            return 1
        elif 85<= value <= 97:
            return 2
        elif 98<= value <=109 :
            return 3
        elif 110<= value <=121 :
            return 4
        elif 122<=value <=134 :
            return 5
        elif  135<= value <=146 :
            return 6
        elif  147<= value <=158 :
            return 7
        elif  159<= value <=171 :
            return 8
        elif  172<= value <=183 :
            return 9
        else:
            return 10


def create_itog_stens(row):
    """
    Функция для создания строки с итоговым стеном
    :param row: строка с результатами
    :return:
    """
    lst_out = list(map(str,row))
    return '-'.join(lst_out)


def create_list_on_level_vipssp(base_df:pd.DataFrame, out_dct:dict, lst_level:list, dct_prefix:dict):
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
                if level == 'низкий уровень':
                    level = 'низкий'
                elif level == 'средний уровень':
                    level = 'средний'
                else:
                    level = 'высокий'
                dct_level[f'{dct_prefix[key]}. {level}'] = temp_df
        out_dct.update(dct_level)

    return out_dct


def create_result_vipssp(base_df:pd.DataFrame, out_dct:dict, lst_svod_cols:list):
    """
    Функция для подсчета результата если указаны колонки по которым нужно провести свод
    :param df: датафрейм с результатами
    :param out_dct: словарь с уже подсчитанными базовыми данными
    :param lst_svod_cols: список сводных колонок
    :return: словарь
    """

    lst_level = ['низкий уровень', 'средний уровень', 'высокий уровень']

    lst_reindex_one_level_cols = lst_svod_cols.copy()
    lst_reindex_one_level_cols.extend(['низкий уровень', 'средний уровень', 'высокий уровень',
                                       'Итого'])  # Основная шкала

    # Интегральные показатели
    svod_count_one_level_ka_df = calc_count_scale(base_df, lst_svod_cols,
                                                    'КА_Стен',
                                                    'КА_Уровень',
                                                    lst_reindex_one_level_cols, lst_level)
    svod_count_one_level_ps_df = calc_count_scale(base_df, lst_svod_cols,
                                                    'ПС_Стен',
                                                    'ПС_Уровень',
                                                    lst_reindex_one_level_cols, lst_level)
    svod_count_one_level_vo_df = calc_count_scale(base_df, lst_svod_cols,
                                                    'ВО_Стен',
                                                    'ВО_Уровень',
                                                    lst_reindex_one_level_cols, lst_level)
    svod_count_one_level_ip_df = calc_count_scale(base_df, lst_svod_cols,
                                                    'ИП_Стен',
                                                    'ИП_Уровень',
                                                    lst_reindex_one_level_cols, lst_level)

    # Считаем среднее по субшкалам
    svod_mean_one_df = pd.pivot_table(base_df,
                                      index=lst_svod_cols,
                                      values=['КА_Стен',
                                              'ПС_Стен',
                                              'ВО_Стен',
                                              'ИП_Стен',
                                              ],
                                      aggfunc=round_mean_two)
    svod_mean_one_df.reset_index(inplace=True)

    # упорядочиваем колонки
    new_order_cols = lst_svod_cols.copy()
    new_order_cols.extend((['КА_Стен',
                            'ПС_Стен',
                            'ВО_Стен',
                            'ИП_Стен',
                            ]))
    svod_mean_one_df = svod_mean_one_df.reindex(columns=new_order_cols)
    dct_rename_cols_mean = {'КА_Стен': 'Ср. значение стена Кибераддикция',
                            'ПС_Стен': 'Ср. значение стена Принятие субкультуры',
                            'ВО_Стен': 'Ср. значение стена Виртуальный образ',
                            'ИП_Стен': 'Ср. значение стена Интегральный показатель'}

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
                    f'КА {out_name}': svod_count_one_level_ka_df,
                    f'ПС {out_name}': svod_count_one_level_ps_df,
                    f'ВО {out_name}': svod_count_one_level_vo_df,
                    f'ИП {out_name}': svod_count_one_level_ip_df,
                    })

    if len(lst_svod_cols) == 1:
        return out_dct
    else:
        for idx, name_column in enumerate(lst_svod_cols):
            lst_reindex_column_level_cols = [lst_svod_cols[idx],'низкий уровень', 'средний уровень', 'высокий уровень',
                                                  'Итого']

            # Интегральные показатели
            svod_count_column_level_ka_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                          'КА_Стен',
                                                          'КА_Уровень',
                                                          lst_reindex_column_level_cols, lst_level)
            svod_count_column_level_ps_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                          'ПС_Стен',
                                                          'ПС_Уровень',
                                                          lst_reindex_column_level_cols, lst_level)
            svod_count_column_level_vo_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                          'ВО_Стен',
                                                          'ВО_Уровень',
                                                          lst_reindex_column_level_cols, lst_level)
            svod_count_column_level_ip_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                          'ИП_Стен',
                                                          'ИП_Уровень',
                                                          lst_reindex_column_level_cols, lst_level)

            # Считаем среднее по субшкалам
            svod_mean_column_df = pd.pivot_table(base_df,
                                              index=[lst_svod_cols[idx]],
                                              values=['КА_Стен',
                                                      'ПС_Стен',
                                                      'ВО_Стен',
                                                      'ИП_Стен',
                                                      ],
                                              aggfunc=round_mean_two)
            svod_mean_column_df.reset_index(inplace=True)

            # упорядочиваем колонки
            new_order_cols = [lst_svod_cols[idx]].copy()
            new_order_cols.extend((['КА_Стен',
                                    'ПС_Стен',
                                    'ВО_Стен',
                                    'ИП_Стен',
                                    ]))
            svod_mean_column_df = svod_mean_column_df.reindex(columns=new_order_cols)
            dct_rename_cols_mean = {'КА_Стен': 'Ср. значение стена Кибераддикция',
                                    'ПС_Стен': 'Ср. значение стена Принятие субкультуры',
                                    'ВО_Стен': 'Ср. значение стена Виртуальный образ',
                                    'ИП_Стен': 'Ср. значение стена Интегральный показатель'}

            svod_mean_column_df.rename(columns=dct_rename_cols_mean, inplace=True)
            # Готовим наименование
            name_column = lst_svod_cols[idx]
            name_column = re.sub(r'[\[\]\'+()<> :"?*|\\/]', '_', name_column)
            name_column = name_column[:15]
            out_dct.update({f'Ср {name_column}': svod_mean_column_df,
                            f'КА {name_column}': svod_count_column_level_ka_df,
                            f'ПС {name_column}': svod_count_column_level_ps_df,
                            f'ВО {name_column}': svod_count_column_level_vo_df,
                            f'ИП {name_column}': svod_count_column_level_ip_df,
                            })
        return out_dct
















def processing_vipss_pog(base_df: pd.DataFrame, answers_df: pd.DataFrame, lst_svod_cols:list):
    """
    Функция для обработки
    :param base_df: часть датафрейма с описательными колонками
    :param answers_df: часть датафрейма с ответами
    :param lst_svod_cols:  список с колонками по которым нужно делать свод
    """
    try:
        union_base_df = base_df.copy()  # делаем копию анкетной части чтобы потом соединить ее с ответной частью
        quantity_cols_base_df = base_df.shape[1]  # количество колонок в анкетной части

        # Проверяем наличие колонок Пол
        diff_req_cols = {'Возраст'}.difference(set(base_df.columns))
        if len(diff_req_cols) != 0:
            raise NotReqColumn

        # Проверяем на значения
        diff_sex = set(base_df['Возраст'].unique()).difference({'18-35 лет', '36-57 лет'})
        if len(diff_sex) != 0:
            raise BadValueAge


        out_answer_df = base_df.copy()  # делаем копию для последующего соединения с сырыми ответами
        if len(answers_df.columns) != 43:  # проверяем количество колонок с вопросами
            raise BadCountColumnsVIPSSP

        # очищаем названия колонок от возможных сочетаний .1 которые добавляет пандас при одинаковых колонках
        clean_df_lst = []
        for name_column in answers_df.columns:
            clean_name = re.sub(r'.\d+$', '', name_column)
            clean_df_lst.append(clean_name)

        answers_df.columns = clean_df_lst

        lst_check_cols = ['Я часто прибегаю к ретуши собственных фотографий, прежде чем выкладываю их в сеть Интернет',
                          'Я предпочитаю пребывание в сети интимному общению с партнером',
                          'Я считаю, что оскорбления и нецензурная брать в Интернете — это нормально',
                          'Мне приятнее смотреть изображения или видео в Интернете, чем читать текст',
                          'Я считаю, что в социальных сетях не стоит выкладывать фотографии, на которых заметны недостатки внешности',
                          'Интернет позволяет мне выразить себя',
                          'Я общаюсь в Интернете с людьми из других городов или стран',
                          'Бывает, что я захожу в социальные сети без намерения с кем-либо пообщаться',
                          'Я испытываю чувство вины, когда понимаю, что мой образ в реальном мире отличается от моего образа в социальных сетях',
                          'Я преувеличиваю значимость моих достижений в Интернете',

                          'Я терплю поражение в попытках сократить время, проводимое «онлайн»',
                          'Мне нравится, что в Интернете можно полностью проявить себя',
                          'Иногда я указываю неверные данные о своей личности в Интернете',
                          'Я публикую фотографии важных событий своей жизни в социальных сетях',
                          'Я не всегда указываю истинные данные о своей личности, такие как имя, фотография, местоположение, при регистрации в социальных сетях',
                          'Я считаю, что посты в социальных сетях позволяют мне донести мои мысли до большого количества людей',
                          'Я состою в Интернете в группах, посвященных идеальной внешности',
                          'Я часто посещаю профили незнакомых людей в социальных сетях',
                          'Я считаю, что в Интернете необязательно соблюдать правила русского языка',
                          'К несчастью, достоинства человека в реальной среде часто остаются непризнанными, как бы он ни старался',

                          'Я произвожу впечатление успешного и привлекательного человека в социальных сетях',
                          'Игры в интернете или посещение социальных сетей помогает мне изменить настроение',
                          'Я чувствую пустоту, депрессию, раздражение, находясь не за компьютером',
                          'В Интернете гораздо удобнее совершать покупки',
                          'Я считаю, что в сети Интернет мой образ должен быть идеальным',
                          'Я проверяю электронную почту и открываю страницы в социальных сетях первым делом после пробуждения',
                          'Я считаю, что вполне допустимо выдавать себя за другого человека в Интернете',
                          'Интернет позволяет мне избавиться от скуки',
                          'Пользователи Интернета считают, что я более профессионален, чем есть на самом деле',
                          'Я считаю, что на фотографиях и видео в Интернете я выгляжу моложе и привлекательнее',

                          'Случалось, что я вступал в конфликты в социальных сетях, не идентифицируя свою реальную личность',
                          'У меня есть альтернативные страницы в социальных сетях, где я выдаю себя за других людей',
                          'Я считаю, что выгляжу на фотографиях более эффектно в сравнении с реальностью',
                          'Если я плохого мнения о человеке и мне не нравится его поведение в Интернете, то почти не стараюсь скрыть это от него',
                          'Я замечаю, что время, проводимое мной в Интернете, увеличивается',
                          'Пользователи Интернета думают, что я умнее, чем есть на самом деле',
                          'Я не хожу в библиотеку, так как мне проще найти любую информацию в Интернете',
                          'Я часто листаю ленту новостей в социальной сети «просто так»',
                          'Порой я чувствую непреодолимое желание обновить страницу в социальной сети',
                          'Бывает, что настаиваю на своем при обсуждении в Интернете, даже когда не уверен в своей правоте',
                          'При использовании Интернета мое настроение улучшается',
                          'Свои достижения и успехи я обязательно освещаю в социальных сетях',
                          'Бывает, я бесцельно просматриваю чужие страницы в социальных сетях',
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
            raise BadOrderVIPSSP

        # словарь для замены слов на числа
        dct_replace_value = {'совершенно не согласен': 1,
                             'отчасти не согласен': 2,
                             'не знаю ответа': 3,
                             'согласен': 4,
                             'полностью согласен': 5,
                             }
        valid_values = [1, 2, 3, 4, 5]
        answers_df.replace(dct_replace_value, inplace=True)  # заменяем слова на цифры для подсчетов
        # Проверяем, есть ли значения, отличающиеся от указанных в списке
        lst_error_answers = []  # список для хранения строк где найдены неправильные ответы

        for i in range(43):
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
            raise BadValueVIPSSP

        base_df['КА_Сырое'] = answers_df.apply(calc_value_ka, axis=1)
        base_df['КА_Стен'] = base_df[['Возраст','КА_Сырое']].apply(calc_ka_sten,axis=1)
        base_df['КА_Уровень'] = base_df['КА_Стен'].apply(calc_level)

        base_df['ПС_Сырое'] = answers_df.apply(calc_value_ps, axis=1)
        base_df['ПС_Стен'] = base_df[['Возраст','ПС_Сырое']].apply(calc_ps_sten,axis=1)
        base_df['ПС_Уровень'] = base_df['ПС_Стен'].apply(calc_level)

        base_df['ВО_Сырое'] = answers_df.apply(calc_value_vo, axis=1)
        base_df['ВО_Стен'] = base_df[['Возраст','ВО_Сырое']].apply(calc_vo_sten,axis=1)
        base_df['ВО_Уровень'] = base_df['ВО_Стен'].apply(calc_level)

        base_df['ИП_Сырое'] = answers_df.sum(axis=1)
        base_df['ИП_Стен'] = base_df[['Возраст','ИП_Сырое']].apply(calc_ip_sten,axis=1)
        base_df['ИП_Уровень'] = base_df['ИП_Стен'].apply(calc_level)

        # Упорядочиваем
        result_df = base_df.iloc[:, quantity_cols_base_df:]  # отсекаем часть с результатами чтобы упорядочить
        lst_stens = [column for column in result_df.columns if 'Стен' in column]
        result_df['Итоговые_стены'] = result_df[lst_stens].apply(create_itog_stens, axis=1)
        new_order_lst = ['Итоговые_стены',
                         'КА_Стен', 'ПС_Стен', 'ВО_Стен', 'ИП_Стен',

                         'КА_Уровень', 'ПС_Уровень', 'ВО_Уровень', 'ИП_Уровень',

                         'КА_Сырое', 'ПС_Сырое', 'ВО_Сырое', 'ИП_Сырое',
                         ]
        result_df = result_df.reindex(columns=new_order_lst)  # изменяем порядок
        base_df = pd.concat([union_base_df, result_df], axis=1)  # соединяем и перезаписываем base_df

        # Создаем датафрейм для создания части в общий датафрейм
        part_df = pd.DataFrame()
        # Стены
        part_df['ВИПССП_Итоговые_стены'] = base_df['Итоговые_стены']
        part_df['ВИПССП_КА_Стен'] = base_df['КА_Стен']
        part_df['ВИПССП_ПС_Стен'] = base_df['ПС_Стен']
        part_df['ВИПССП_ВО_Стен'] = base_df['ВО_Стен']
        part_df['ВИПССП_ИП_Стен'] = base_df['ИП_Стен']

        # Уровни
        part_df['ВИПССП_КА_Уровень'] = base_df['КА_Уровень']
        part_df['ВИПССП_ПС_Уровень'] = base_df['ПС_Уровень']
        part_df['ВИПССП_ВО_Уровень'] = base_df['ВО_Уровень']
        part_df['ВИПССП_ИП_Уровень'] = base_df['ИП_Уровень']

        # Значения
        part_df['ВИПССП_КА_Сырое'] = base_df['КА_Сырое']
        part_df['ВИПССП_ПС_Сырое'] = base_df['ПС_Сырое']
        part_df['ВИПССП_ВО_Сырое'] = base_df['ВО_Сырое']
        part_df['ВИПССП_ИП_Сырое'] = base_df['ИП_Сырое']

        out_answer_df = pd.concat([out_answer_df, answers_df], axis=1)  # Датафрейм для проверки
        base_df.sort_values(by='ИП_Сырое', ascending=False, inplace=True)  # сортируем

        # формируем основной словарь
        out_dct = {'Списочный результат': base_df, 'Список для проверки': out_answer_df,
                   }

        # Делаем свод по шкалам
        dct_svod_integral = {'КА_Стен': 'КА_Уровень',
                             'ПС_Стен': 'ПС_Уровень',
                             'ВО_Стен': 'ВО_Уровень',
                             'ИП_Стен': 'ИП_Уровень',

                             }

        dct_rename_svod_integral = {'КА_Стен': 'Кибераддикция',
                                    'ПС_Стен': 'Принятие субкультуры',
                                    'ВО_Стен': 'Виртуальный образ',
                                    'ИП_Стен': 'Интегральный показатель',
                                    }

        lst_integral = ['низкий уровень', 'средний уровень', 'высокий уровень']
        base_svod_integral_df = create_union_svod(base_df, dct_svod_integral, dct_rename_svod_integral, lst_integral)

        # Считаем среднее по шкалам
        avg_a = round(base_df['КА_Стен'].mean(), 2)
        avg_b = round(base_df['ПС_Стен'].mean(), 2)
        avg_c = round(base_df['ВО_Стен'].mean(), 2)
        avg_d = round(base_df['ИП_Стен'].mean(), 2)

        avg_dct = {'Среднее значение стена шкалы Кибераддикция': avg_a,
                   'Среднее значение стена шкалы Принятие субкультуры': avg_b,
                   'Среднее значение стена шкалы Виртуальный образ': avg_c,
                   'Среднее значение стена Интегрального показателя': avg_d,

                   }

        avg_df = pd.DataFrame.from_dict(avg_dct, orient='index')
        avg_df = avg_df.reset_index()
        avg_df.columns = ['Показатель', 'Среднее значение']

        out_dct.update({'Свод Шкалы': base_svod_integral_df,
                        'Среднее': avg_df}
                       )

        dct_prefix = {'КА_Уровень': 'КА',
                      'ПС_Уровень': 'ПС',
                      'ВО_Уровень': 'ВО',
                      'ИП_Уровень': 'ИП',
                      }

        out_dct = create_list_on_level_vipssp(base_df, out_dct, lst_integral, dct_prefix)

        """
            Сохраняем в зависимости от необходимости делать своды по определенным колонкам
            """
        if len(lst_svod_cols) == 0:
            return out_dct, part_df
        else:
            out_dct = create_result_vipssp(base_df, out_dct, lst_svod_cols)

            return out_dct, part_df

    except BadOrderVIPSSP:
        messagebox.showerror('Лахеcис',
                             f'При обработке вопросов теста Виртуальная идентичность пользователей социальных сетей Погорелов обнаружены неправильные вопросы. Проверьте названия колонок с вопросами:\n'
                             f'{error_order_message[:5000]}\n'
                             f'Используйте при создании Яндекс-формы написание вопросов из руководства пользователя программы Лахесис.')
    except BadValueVIPSSP:
        messagebox.showerror('Лахеcис',
                             f'При обработке вопросов теста Виртуальная идентичность пользователей социальных сетей Погорелов обнаружены неправильные варианты ответов. Проверьте ответы на указанных строках:\n'
                             f'{error_message[:5000]}\n'
                             f'Используйте при создании Яндекс-формы написание вариантов ответа из руководства пользователя программы Лахесис.')


    except BadCountColumnsVIPSSP:
        messagebox.showerror('Лахеcис',
                             f'Проверьте количество колонок с ответами на тест Виртуальная идентичность пользователей социальных сетей Погорелов\n'
                             f'Должно быть 43 колонки с ответами')









