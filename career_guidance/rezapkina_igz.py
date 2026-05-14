"""
Скрипт для обработки результатов Иерархия жизненных ценностей Г.В. Резапкина
"""

import pandas as pd
import re
from tkinter import messagebox
from lachesis_support_functions import round_mean_two,calc_count_scale,create_union_svod

class BadOrderIGZR(Exception):
    """
    Исключение для обработки случая когда колонки не совпадают
    """
    pass


class BadValueIGZR(Exception):
    """
    Исключение для неправильных значений в вариантах ответов
    """
    pass

class BadCountColumnsIGZR(Exception):
    """
    Исключение для обработки случая если количество колонок не равно 40
    """
    pass


def calc_level(value):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """
    if -5<= value <= -3:
        return f'отвергаемая ценность'
    elif -2 <= value <= 0:
        return f'низкая значимость ценности'
    elif 1 <= value <= 3:
        return f'умеренно значимая ценность'
    else:
        return f'значимая ценность'




def calc_value_z(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [1,2,3,4,5]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_pr:
            value_forward += value
    return value_forward

def calc_value_mo(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [6,7,8,9,10]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_pr:
            value_forward += value
    return value_forward


def calc_value_t(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [11,12,13,14,15]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_pr:
            value_forward += value
    return value_forward

def calc_value_s(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [16,17,18,19,20]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_pr:
            value_forward += value
    return value_forward

def calc_value_k(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [21,22,23,24,25]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_pr:
            value_forward += value
    return value_forward

def calc_value_sj(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [26,27,28,29,30]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_pr:
            value_forward += value
    return value_forward

def calc_value_sv(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [31,32,33,34,35]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_pr:
            value_forward += value
    return value_forward

def calc_value_o(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [36,37,38,39,40]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_pr:
            value_forward += value
    return value_forward

def create_list_on_level_igz(base_df:pd.DataFrame,out_dct:dict,lst_level:list,dct_prefix:dict):
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
                if level == 'отвергаемая ценность':
                    level = 'отвергаемая'
                elif level == 'низкая значимость ценности':
                    level = 'низкая'
                elif level == 'умеренно значимая ценность':
                    level = 'умеренно'
                else:
                    level = 'значимая'
                dct_level[f'{dct_prefix[key]}. {level}'] = temp_df
        out_dct.update(dct_level)

    return out_dct

def create_result_igz_rezapkina(base_df:pd.DataFrame, out_dct:dict, lst_svod_cols:list):
    """
    Функция для подсчета результата если указаны колонки по которым нужно провести свод
    :param df: датафрейм с результатами
    :param out_dct: словарь с уже подсчитанными базовыми данными
    :param lst_svod_cols: список сводных колонок
    :return: словарь
    """

    lst_level = ['отвергаемая ценность', 'низкая значимость ценности', 'умеренно значимая ценность','значимая ценность']

    lst_reindex_one_level_cols = lst_svod_cols.copy()
    lst_reindex_one_level_cols.extend(['отвергаемая ценность', 'низкая значимость ценности', 'умеренно значимая ценность','значимая ценность',
                                       'Итого'])  # Основная шкала

    # АД
    svod_count_one_level_z_df = calc_count_scale(base_df, lst_svod_cols,
                                                 'З_Значение',
                                                 'З_Уровень',
                                                 lst_reindex_one_level_cols, lst_level)

    # АД
    svod_count_one_level_mo_df = calc_count_scale(base_df, lst_svod_cols,
                                                 'МО_Значение',
                                                 'МО_Уровень',
                                                 lst_reindex_one_level_cols, lst_level)

    # АД
    svod_count_one_level_t_df = calc_count_scale(base_df, lst_svod_cols,
                                                 'Т_Значение',
                                                 'Т_Уровень',
                                                 lst_reindex_one_level_cols, lst_level)

    # АД
    svod_count_one_level_s_df = calc_count_scale(base_df, lst_svod_cols,
                                                 'С_Значение',
                                                 'С_Уровень',
                                                 lst_reindex_one_level_cols, lst_level)

    # АД
    svod_count_one_level_k_df = calc_count_scale(base_df, lst_svod_cols,
                                                 'К_Значение',
                                                 'К_Уровень',
                                                 lst_reindex_one_level_cols, lst_level)

    # АД
    svod_count_one_level_sj_df = calc_count_scale(base_df, lst_svod_cols,
                                                 'СЖ_Значение',
                                                 'СЖ_Уровень',
                                                 lst_reindex_one_level_cols, lst_level)
    # АД
    svod_count_one_level_sv_df = calc_count_scale(base_df, lst_svod_cols,
                                                 'СВ_Значение',
                                                 'СВ_Уровень',
                                                 lst_reindex_one_level_cols, lst_level)
    # АД
    svod_count_one_level_o_df = calc_count_scale(base_df, lst_svod_cols,
                                                 'О_Значение',
                                                 'О_Уровень',
                                                 lst_reindex_one_level_cols, lst_level)

    # Считаем среднее по субшкалам
    svod_mean_one_df = pd.pivot_table(base_df,
                                      index=lst_svod_cols,
                                      values=['З_Значение',
                                              'МО_Значение',
                                              'Т_Значение',
                                              'С_Значение',

                                              'К_Значение',
                                              'СЖ_Значение',
                                              'СВ_Значение',
                                              'О_Значение',
                                              ],
                                      aggfunc=round_mean_two)
    svod_mean_one_df.reset_index(inplace=True)

    # упорядочиваем колонки
    new_order_cols = lst_svod_cols.copy()
    new_order_cols.extend((['З_Значение',
                            'МО_Значение',
                            'Т_Значение',
                            'С_Значение',

                            'К_Значение',
                            'СЖ_Значение',
                            'СВ_Значение',
                            'О_Значение',
                            ]))
    svod_mean_one_df = svod_mean_one_df.reindex(columns=new_order_cols)

    dct_rename_cols_mean = {'З_Значение': 'Ср. Здоровье',
                            'МО_Значение': 'Ср. Шкала Материальная обеспеченность',
                            'Т_Значение': 'Ср. Шкала Творчество',
                            'С_Значение': 'Ср. Шкала Семья',

                            'К_Значение': 'Ср. Шкала Карьера',
                            'СЖ_Значение': 'Ср. Шкала Служение',
                            'СВ_Значение': 'Ср. Шкала Слава',
                            'О_Значение': 'Ср. Шкала Отдых',
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
                    f'З {out_name}': svod_count_one_level_z_df,
                    f'МО {out_name}': svod_count_one_level_mo_df,
                    f'Т {out_name}': svod_count_one_level_t_df,
                    f'С {out_name}': svod_count_one_level_s_df,

                    f'К {out_name}': svod_count_one_level_k_df,
                    f'СЖ {out_name}': svod_count_one_level_sj_df,
                    f'СВ {out_name}': svod_count_one_level_sv_df,
                    f'О {out_name}': svod_count_one_level_o_df,
                    })

    if len(lst_svod_cols) == 1:
        return out_dct
    else:
        for idx, name_column in enumerate(lst_svod_cols):

            lst_reindex_column_level_cols = [lst_svod_cols[idx], 'отвергаемая ценность', 'низкая значимость ценности', 'умеренно значимая ценность','значимая ценность',
                                             'Итого']

            # АД
            svod_count_column_level_z_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                            'З_Значение',
                                                            'З_Уровень',
                                                            lst_reindex_column_level_cols, lst_level)

            # АД
            svod_count_column_level_mo_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                             'МО_Значение',
                                                             'МО_Уровень',
                                                             lst_reindex_column_level_cols, lst_level)

            # АД
            svod_count_column_level_t_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                            'Т_Значение',
                                                            'Т_Уровень',
                                                            lst_reindex_column_level_cols, lst_level)

            # АД
            svod_count_column_level_s_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                            'С_Значение',
                                                            'С_Уровень',
                                                            lst_reindex_column_level_cols, lst_level)

            # АД
            svod_count_column_level_k_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                            'К_Значение',
                                                            'К_Уровень',
                                                            lst_reindex_column_level_cols, lst_level)

            # АД
            svod_count_column_level_sj_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                             'СЖ_Значение',
                                                             'СЖ_Уровень',
                                                             lst_reindex_column_level_cols, lst_level)
            # АД
            svod_count_column_level_sv_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                             'СВ_Значение',
                                                             'СВ_Уровень',
                                                             lst_reindex_column_level_cols, lst_level)
            # АД
            svod_count_column_level_o_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                            'О_Значение',
                                                            'О_Уровень',
                                                            lst_reindex_column_level_cols, lst_level)

            # Считаем среднее по субшкалам
            svod_mean_column_df = pd.pivot_table(base_df,
                                                 index=[lst_svod_cols[idx]],
                                                 values=['З_Значение',
                                                         'МО_Значение',
                                                         'Т_Значение',
                                                         'С_Значение',

                                                         'К_Значение',
                                                         'СЖ_Значение',
                                                         'СВ_Значение',
                                                         'О_Значение',
                                                         ],
                                                 aggfunc=round_mean_two)
            svod_mean_column_df.reset_index(inplace=True)

            # упорядочиваем колонки
            new_order_cols = [lst_svod_cols[idx]].copy()
            new_order_cols.extend((['З_Значение',
                                    'МО_Значение',
                                    'Т_Значение',
                                    'С_Значение',

                                    'К_Значение',
                                    'СЖ_Значение',
                                    'СВ_Значение',
                                    'О_Значение',
                                    ]))
            svod_mean_column_df = svod_mean_column_df.reindex(columns=new_order_cols)

            dct_rename_cols_mean = {'З_Значение': 'Ср. Здоровье',
                                    'МО_Значение': 'Ср. Шкала Материальная обеспеченность',
                                    'Т_Значение': 'Ср. Шкала Творчество',
                                    'С_Значение': 'Ср. Шкала Семья',

                                    'К_Значение': 'Ср. Шкала Карьера',
                                    'СЖ_Значение': 'Ср. Шкала Служение',
                                    'СВ_Значение': 'Ср. Шкала Слава',
                                    'О_Значение': 'Ср. Шкала Отдых',
                                    }
            svod_mean_column_df.rename(columns=dct_rename_cols_mean, inplace=True)
            # Готовим наименование
            name_column = lst_svod_cols[idx]
            name_column = re.sub(r'[\[\]\'+()<> :"?*|\\/]', '_', name_column)
            name_column = name_column[:15]

            out_dct.update({f'Ср {name_column}': svod_mean_column_df,
                            f'З {name_column}': svod_count_column_level_z_df,
                            f'МО {name_column}': svod_count_column_level_mo_df,
                            f'Т {name_column}': svod_count_column_level_t_df,
                            f'С {name_column}': svod_count_column_level_s_df,

                            f'К {name_column}': svod_count_column_level_k_df,
                            f'СЖ {name_column}': svod_count_column_level_sj_df,
                            f'СВ {name_column}': svod_count_column_level_sv_df,
                            f'О {name_column}': svod_count_column_level_o_df,
                            })
        return out_dct







def processing_igz_rez(base_df: pd.DataFrame, answers_df: pd.DataFrame, lst_svod_cols:list):
    """
    Функция для обработки
    :param base_df: часть датафрейма с описательными колонками
    :param answers_df: часть датафрейма с ответами
    :param lst_svod_cols:  список с колонками по которым нужно делать свод
    """
    try:
        count_descr_cols = base_df.shape[1] # количество анкетных колонок

        out_answer_df = base_df.copy()  # делаем копию для последующего соединения с сырыми ответами
        if len(answers_df.columns) != 40:  # проверяем количество колонок с вопросами
            raise BadCountColumnsIGZR

        # очищаем названия колонок от возможных сочетаний .1 которые добавляет пандас при одинаковых колонках
        clean_df_lst = []
        for name_column in answers_df.columns:
            clean_name = re.sub(r'.\d+$', '', name_column)
            clean_df_lst.append(clean_name)

        answers_df.columns = clean_df_lst

        lst_check_cols = ['Я планирую выбрать профессию, которая не создаст мне проблем со здоровьем',
                          'Я слежу за своим здоровьем (регулярно прохожу медосмотр, соблюдаю режим, диету, занимаюсь спортом)',
                          'Я очень боюсь заболеть или потерять физическую форму',
                          'Я люблю читать статьи о новых методах лечениях и оздоровительных системах',
                          'Мне нравится высказывание "Здоровье это не всё, но без него всё - ничто"',
                          'Я планирую выбрать высокооплачиваемую профессию',
                          'Я ищу и нахожу возможные способы зарабатывания денег, чтобы не зависеть от родителей',
                          'За большие деньги я возьмусь за любую работу',
                          'Я внимательно слежу за курсом валют и биржевыми новостями',
                          'Мне нравится высказывание "Чтобы заработать на жизнь, надо работать. Но чтобы разбогатеть, надо придумать что-то другое"',

                          'Я планирую выбрать профессию, которая даст мне возможность заниматься творчеством',
                          'Свободное время я пишу стихи и рассказы, сочиняю музыку, рисую, снимаю видео, играю в спектаклях, выступаю на концертах и т.д.',
                          'Друзья и знакомые высоко оценивают мое творчество',
                          'Я часто бываю на выставках, спектаклях и концертах',
                          'Мне нравится высказывание "Кто испытал наслаждение творчества, для того все другие наслаждения не существуют"',
                          'Я хочу выбрать профессию, которая позволит мне много времени уделять своей семье',
                          'Я всегда выполняю просьбы родных о помощи по хозяйству',
                          'Я могу отложить любые дела ради моих родных и близких',
                          'Для меня очень важна поддержка моих родителей',
                          'Мне нравится высказывание "Самое главное для меня - жизнь и здоровье тех, кого я люблю"',

                          'Я планирую выбрать профессию, которая обеспечит мой карьерный рост',
                          'Я занимаюсь общественной работой, потому что это поможет мне в достижении моих целей',
                          'Я стараюсь знакомиться с людьми, которые помогут мне в карьерном росте',
                          'Я готов (а) бороться со своими конкурентами за "место под солнцем"',
                          'Мне нравится высказывание "Карьеру не сделаешь, карабкаясь по обшарпанным ступеням - нужно оказаться в лифте в подходящей компании"',
                          'Я планирую выбрать работу, смысл которой - помощь людям',
                          'Я не могу пройти мимо человека, который просит о помощи',
                          'Я испытываю жалость к бомжам и нищим',
                          'Я принимаю участие в благотворительных акциях (донорство, сбор средств на лечение, помощь сиротам и т.д.)',
                          'Мне нравится высказывание "Если вы ищете способ сделать свою жизнь осмысленной, начните служить другим людям и помогать им"',

                          'Я планирую выбрать профессию, которая принесет мне известность',
                          'Я хочу походить на моих кумиров (в спорте, политике, шоу-бизнесе, искусстве, науке и т.д.)',
                          'Мне нравится быть в центре внимания',
                          'Я с интересом читаю статьи и смотрю передачи о жизни знаменитостей',
                          'Мне нравится высказывание "Стремление к славе похвально и полезно для общества, так как побуждает совершать благородные деяния"',
                          'Я планирую выбрать профессию, которая не помешает мне иметь много свободного времени для отдыха и развлечений',
                          'Я могу целями днями гулять, общаться с друзьями в инете и реале, смотреть телевизор',
                          'Если бы у меня было много денег, я бы вообще не работал (а)',
                          'Мне нравятся развлекательные передачи',
                          'Мне нравится высказывание "Я никогда не стою, если имею возможность сидеть, и никогда не сижу, если имею возможность лежать"'
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
            raise BadOrderIGZR

        # словарь для замены слов на числа
        dct_replace_value = {'нет': -1,
                             'сомневаюсь': 0,
                             'да': 1,
                             }
        valid_values = [-1, 0, 1]
        answers_df.replace(dct_replace_value, inplace=True)  # заменяем слова на цифры для подсчетов
        # Проверяем, есть ли значения, отличающиеся от указанных в списке
        lst_error_answers = []  # список для хранения строк где найдены неправильные ответы

        for i in range(40):
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
            raise BadValueIGZR

        base_df['З_Значение'] = answers_df.apply(calc_value_z, axis=1)
        base_df['З_Уровень'] = base_df['З_Значение'].apply(calc_level)

        base_df['МО_Значение'] = answers_df.apply(calc_value_mo, axis=1)
        base_df['МО_Уровень'] = base_df['МО_Значение'].apply(calc_level)

        base_df['Т_Значение'] = answers_df.apply(calc_value_t, axis=1)
        base_df['Т_Уровень'] = base_df['Т_Значение'].apply(calc_level)

        base_df['С_Значение'] = answers_df.apply(calc_value_s, axis=1)
        base_df['С_Уровень'] = base_df['С_Значение'].apply(calc_level)

        base_df['К_Значение'] = answers_df.apply(calc_value_k, axis=1)
        base_df['К_Уровень'] = base_df['К_Значение'].apply(calc_level)

        base_df['СЖ_Значение'] = answers_df.apply(calc_value_sj, axis=1)
        base_df['СЖ_Уровень'] = base_df['СЖ_Значение'].apply(calc_level)

        base_df['СВ_Значение'] = answers_df.apply(calc_value_sv, axis=1)
        base_df['СВ_Уровень'] = base_df['СВ_Значение'].apply(calc_level)

        base_df['О_Значение'] = answers_df.apply(calc_value_o, axis=1)
        base_df['О_Уровень'] = base_df['О_Значение'].apply(calc_level)


        # Создаем датафрейм для создания части в общий датафрейм
        temp_df = base_df.copy() # делаем копию
        part_df = temp_df.iloc[:,count_descr_cols:]
        part_df = part_df.add_prefix('ИЖЦР_')

        out_answer_df = pd.concat([out_answer_df, answers_df], axis=1)  # Датафрейм для проверки

        base_df.sort_values(by='СЖ_Значение', ascending=False, inplace=True)  # сортируем

        # Делаем свод  по  шкалам
        dct_svod_sub = {'З_Значение': 'З_Уровень',
                        'МО_Значение': 'МО_Уровень',
                        'Т_Значение': 'Т_Уровень',
                        'С_Значение': 'С_Уровень',

                        'К_Значение': 'К_Уровень',
                        'СЖ_Значение': 'СЖ_Уровень',
                        'СВ_Значение': 'СВ_Уровень',
                        'О_Значение': 'О_Уровень',

                        }

        dct_rename_svod_sub = {'З_Значение': 'Здоровье',
                               'МО_Значение': 'Материальная обеспеченность',
                               'Т_Значение': 'Творчество',
                               'С_Значение': 'Семья',

                               'К_Значение': 'Карьера',
                               'СЖ_Значение': 'Служение',
                               'СВ_Значение': 'Слава',
                               'О_Значение': 'Отдых',
                               }

        lst_sub = ['отвергаемая ценность', 'низкая значимость ценности', 'умеренно значимая ценность','значимая ценность']

        base_svod_sub_df = create_union_svod(base_df, dct_svod_sub, dct_rename_svod_sub, lst_sub)

        avg_z = round(base_df['З_Значение'].mean(), 2)
        avg_mo = round(base_df['МО_Значение'].mean(), 2)
        avg_t = round(base_df['Т_Значение'].mean(), 2)
        avg_s = round(base_df['С_Значение'].mean(), 2)

        avg_k = round(base_df['К_Значение'].mean(), 2)
        avg_sj = round(base_df['СЖ_Значение'].mean(), 2)
        avg_sv = round(base_df['СВ_Значение'].mean(), 2)
        avg_o = round(base_df['О_Значение'].mean(), 2)

        avg_dct = {'Среднее значение шкалы Здоровье': avg_z,
                   'Среднее значение шкалы Материальная обеспеченность': avg_mo,
                   'Среднее значение шкалы Творчество': avg_t,
                   'Среднее значение шкалы Семья': avg_s,

                   'Среднее значение шкалы Карьера': avg_k,
                   'Среднее значение шкалы Служение': avg_sj,
                   'Среднее значение шкалы Слава': avg_sv,
                   'Среднее значение шкалы Отдых': avg_o,
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

        dct_prefix = {
            'З_Уровень': 'З',
            'МО_Уровень': 'МО',
            'Т_Уровень': 'Т',
            'С_Уровень': 'С',

            'К_Уровень': 'К',
            'СЖ_Уровень': 'СЖ',
            'СВ_Уровень': 'СВ',
            'О_Уровень': 'О',
        }

        out_dct = create_list_on_level_igz(base_df, out_dct, lst_sub, dct_prefix)

        """
                        Сохраняем в зависимости от необходимости делать своды по определенным колонкам
                        """
        if len(lst_svod_cols) == 0:
            return out_dct, part_df

        else:
            out_dct = create_result_igz_rezapkina(base_df, out_dct, lst_svod_cols)
            return out_dct, part_df


    except BadOrderIGZR:
        messagebox.showerror('Лахеcис',
                             f'При обработке вопросов теста Иерархия жизненных ценностей Резапкина обнаружены неправильные вопросы. Проверьте названия колонок с вопросами:\n'
                             f'{error_order_message[:5000]}\n'
                             f'Используйте при создании Яндекс-формы написание вопросов из руководства пользователя программы Лахесис.')
    except BadValueIGZR:
        messagebox.showerror('Лахеcис',
                             f'При обработке вопросов теста Иерархия жизненных ценностей Резапкина обнаружены неправильные варианты ответов. Проверьте ответы на указанных строках:\n'
                             f'{error_message[:5000]}\n'
                             f'Используйте при создании Яндекс-формы написание вариантов ответа из руководства пользователя программы Лахесис.')


    except BadCountColumnsIGZR:
        messagebox.showerror('Лахеcис',
                             f'Проверьте количество колонок с ответами на тест Иерархия жизненных ценностей Резапкина \n'
                             f'Должно быть 40 колонок с ответами')









