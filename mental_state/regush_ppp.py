"""
Скрипт для обработки результатов теста Психологические проблемы подростков в реальной и виртуальной сфере Регуш
"""

import pandas as pd
import re
from tkinter import messagebox
from lachesis_support_functions import round_mean_two,calc_count_scale,create_list_on_level,create_union_svod


class BadOrderPPPR(Exception):
    """
    Исключение для обработки случая когда колонки не совпадают
    """
    pass


class BadValuePPPR(Exception):
    """
    Исключение для неправильных значений в вариантах ответов
    """
    pass

class BadCountColumnsPPPR(Exception):
    """
    Исключение для обработки случая если количество колонок не равно 60
    """
    pass


def calc_value_opo(row):
    """
    Функция для подсчета значения
    :return: число
    """
    value_forward = 0  # результат
    for idx, value in enumerate(row):
        value_forward += value

    value_forward = round(value_forward / 60,2)

    return value_forward


def calc_value_solb(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [1,2,3,4,5,6,7,8,9,10]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_pr:
            value_forward += value

    value_forward = round(value_forward / len(lst_pr),2)

    return value_forward

def calc_value_si(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [11,12,13,14,15,16,17,18,19,20]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_pr:
            value_forward += value

    value_forward = round(value_forward / len(lst_pr),2)

    return value_forward


def calc_value_so(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [21,22,23,24,25,26,27,28,29,30]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_pr:
            value_forward += value

    value_forward = round(value_forward / len(lst_pr),2)

    return value_forward

def calc_value_vr(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [31,32,33,34,35,36,37,38,39,40]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_pr:
            value_forward += value

    value_forward = round(value_forward / len(lst_pr),2)

    return value_forward

def calc_value_spi(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [41,42,43,44,45,46,47,48,49,50]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_pr:
            value_forward += value

    value_forward = round(value_forward / len(lst_pr),2)

    return value_forward


def calc_value_ssh(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [51,52,53,54,55,56,57,58,59,60]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_pr:
            value_forward += value

    value_forward = round(value_forward / len(lst_pr),2)

    return value_forward

def calc_level(value):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """
    if value <= 2:
        return f'1-2'
    elif 2.01 <= value <= 3.0:
        return f'2.01-3'
    elif 3.01 <= value <= 4.0:
        return f'3.01-4'
    else:
        return f'4.01-5'



def create_list_on_level_pppr(base_df:pd.DataFrame, out_dct:dict, lst_level:list, dct_prefix:dict):
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
                dct_level[f'{dct_prefix[key]}. {level}'] = temp_df
        out_dct.update(dct_level)

    return out_dct


def create_result_ppp_regush(base_df:pd.DataFrame, out_dct:dict, lst_svod_cols:list):
    """
    Функция для подсчета результата если указаны колонки по которым нужно провести свод
    :param df: датафрейм с результатами
    :param out_dct: словарь с уже подсчитанными базовыми данными
    :param lst_svod_cols: список сводных колонок
    :return: словарь
    """
    lst_level = ['1-2', '2.01-3', '3.01-4', '4.01-5']

    lst_reindex_one_level_cols = lst_svod_cols.copy()
    lst_reindex_one_level_cols.extend(['1-2', '2.01-3', '3.01-4', '4.01-5',
                                       'Итого'])  # Основная шкала

    # ВЧА
    svod_count_one_level_vcha_df = calc_count_scale(base_df, lst_svod_cols,
                                                    'ОПО_Значение',
                                                    'ОПО_Диапазон',
                                                    lst_reindex_one_level_cols, lst_level)

    # О
    svod_count_one_level_o_df = calc_count_scale(base_df, lst_svod_cols,
                                                 'СОЛБ_Значение',
                                                 'СОЛБ_Диапазон',
                                                 lst_reindex_one_level_cols, lst_level)
    # РУВС
    svod_count_one_level_ruvs_df = calc_count_scale(base_df, lst_svod_cols,
                                                    'СИ_Значение',
                                                    'СИ_Диапазон',
                                                    lst_reindex_one_level_cols, lst_level)

    # ПСП
    svod_count_one_level_psp_df = calc_count_scale(base_df, lst_svod_cols,
                                                   'СО_Значение',
                                                   'СО_Диапазон',
                                                   lst_reindex_one_level_cols, lst_level)
    # ППВС
    svod_count_one_level_ppvs_df = calc_count_scale(base_df, lst_svod_cols,
                                                    'ВР_Значение',
                                                    'ВР_Диапазон',
                                                    lst_reindex_one_level_cols, lst_level)
    # ИП
    svod_count_one_level_ip_df = calc_count_scale(base_df, lst_svod_cols,
                                                  'СПИ_Значение',
                                                  'СПИ_Диапазон',
                                                  lst_reindex_one_level_cols, lst_level)

    # ПРП
    svod_count_one_level_prp_df = calc_count_scale(base_df, lst_svod_cols,
                                                   'СШ_Значение',
                                                   'СШ_Диапазон',
                                                   lst_reindex_one_level_cols, lst_level)

    # Считаем среднее по субшкалам
    svod_mean_one_df = pd.pivot_table(base_df,
                                      index=lst_svod_cols,
                                      values=['ОПО_Значение',
                                              'СОЛБ_Значение',
                                              'СИ_Значение',
                                              'СО_Значение',

                                              'ВР_Значение',
                                              'СПИ_Значение',
                                              'СШ_Значение',
                                              ],
                                      aggfunc=round_mean_two)
    svod_mean_one_df.reset_index(inplace=True)

    # упорядочиваем колонки
    new_order_cols = lst_svod_cols.copy()
    new_order_cols.extend((['ОПО_Значение', 'СОЛБ_Значение',
                            'СИ_Значение', 'СО_Значение',
                            'ВР_Значение', 'СПИ_Значение',
                            'СШ_Значение'
                            ]))
    svod_mean_one_df = svod_mean_one_df.reindex(columns=new_order_cols)

    dct_rename_cols_mean = {'ОПО_Значение': 'Ср. Общая проблемная озабоченность',
                            'СОЛБ_Значение': 'Ср. Проблемы, связанные с общественной и личной безопасностью',
                            'СИ_Значение': 'Ср. Проблемы становления идентичности',
                            'СО_Значение': 'Ср. Проблемы, связанные с общением',

                            'ВР_Значение': 'Ср. Проблемы во взаимоотношениях с родителями',
                            'СПИ_Значение': 'Ср. Проблемы, связанные с погруженностью в Интернет',
                            'СШ_Значение': 'Ср. Проблемы, связанные со школой',
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
                    f'ВЧА {out_name}': svod_count_one_level_vcha_df,
                    f'О {out_name}': svod_count_one_level_o_df,
                    f'РУВС {out_name}': svod_count_one_level_ruvs_df,
                    f'ПСП {out_name}': svod_count_one_level_psp_df,

                    f'ППВ {out_name}': svod_count_one_level_ppvs_df,
                    f'ИП {out_name}': svod_count_one_level_ip_df,
                    f'ПРП {out_name}': svod_count_one_level_prp_df,
                    })

    if len(lst_svod_cols) == 1:
        return out_dct
    else:
        for idx, name_column in enumerate(lst_svod_cols):
            lst_reindex_column_level_cols = [lst_svod_cols[idx],'1-2', '2.01-3', '3.01-4', '4.01-5',
                                                  'Итого']

            # ВЧА
            svod_count_column_level_vcha_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                               'ОПО_Значение',
                                                               'ОПО_Диапазон',
                                                               lst_reindex_column_level_cols, lst_level)

            # О
            svod_count_column_level_o_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                            'СОЛБ_Значение',
                                                            'СОЛБ_Диапазон',
                                                            lst_reindex_column_level_cols, lst_level)
            # РУВС
            svod_count_column_level_ruvs_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                               'СИ_Значение',
                                                               'СИ_Диапазон',
                                                               lst_reindex_column_level_cols, lst_level)

            # ПСП
            svod_count_column_level_psp_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                              'СО_Значение',
                                                              'СО_Диапазон',
                                                              lst_reindex_column_level_cols, lst_level)
            # ППВС
            svod_count_column_level_ppvs_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                               'ВР_Значение',
                                                               'ВР_Диапазон',
                                                               lst_reindex_column_level_cols, lst_level)
            # ИП
            svod_count_column_level_ip_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                             'СПИ_Значение',
                                                             'СПИ_Диапазон',
                                                             lst_reindex_column_level_cols, lst_level)

            # ПРП
            svod_count_column_level_prp_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                              'СШ_Значение',
                                                              'СШ_Диапазон',
                                                              lst_reindex_column_level_cols, lst_level)

            # Считаем среднее по субшкалам
            svod_mean_column_df = pd.pivot_table(base_df,
                                              index=[lst_svod_cols[idx]],
                                              values=['ОПО_Значение',
                                                      'СОЛБ_Значение',
                                                      'СИ_Значение',
                                                      'СО_Значение',

                                                      'ВР_Значение',
                                                      'СПИ_Значение',
                                                      'СШ_Значение',
                                                      ],
                                              aggfunc=round_mean_two)
            svod_mean_column_df.reset_index(inplace=True)

            # упорядочиваем колонки
            new_order_cols = [lst_svod_cols[idx]].copy()
            new_order_cols.extend((['ОПО_Значение', 'СОЛБ_Значение',
                                    'СИ_Значение', 'СО_Значение',
                                    'ВР_Значение', 'СПИ_Значение',
                                    'СШ_Значение'
                                    ]))
            svod_mean_column_df = svod_mean_column_df.reindex(columns=new_order_cols)

            dct_rename_cols_mean = {'ОПО_Значение': 'Ср. Общая проблемная озабоченность',
                                    'СОЛБ_Значение': 'Ср. Проблемы, связанные с общественной и личной безопасностью',
                                    'СИ_Значение': 'Ср. Проблемы становления идентичности',
                                    'СО_Значение': 'Ср. Проблемы, связанные с общением',

                                    'ВР_Значение': 'Ср. Проблемы во взаимоотношениях с родителями',
                                    'СПИ_Значение': 'Ср. Проблемы, связанные с погруженностью в Интернет',
                                    'СШ_Значение': 'Ср. Проблемы, связанные со школой',
                                    }
            svod_mean_column_df.rename(columns=dct_rename_cols_mean, inplace=True)

            # Готовим наименование
            name_column = lst_svod_cols[idx]
            name_column = re.sub(r'[\[\]\'+()<> :"?*|\\/]', '_', name_column)
            name_column = name_column[:15]
            out_dct.update({f'Ср {name_column}': svod_mean_column_df,
                            f'ВЧА {name_column}': svod_count_column_level_vcha_df,
                            f'О {name_column}': svod_count_column_level_o_df,
                            f'РУВС {name_column}': svod_count_column_level_ruvs_df,
                            f'ПСП {name_column}': svod_count_column_level_psp_df,

                            f'ППВ {name_column}': svod_count_column_level_ppvs_df,
                            f'ИП {name_column}': svod_count_column_level_ip_df,
                            f'ПРП {name_column}': svod_count_column_level_prp_df,
                            })
        return out_dct













def processing_ppp_regush(base_df: pd.DataFrame, answers_df: pd.DataFrame, lst_svod_cols:list):
    """
    Функция для обработки
    :param base_df: часть датафрейма с описательными колонками
    :param answers_df: часть датафрейма с ответами
    :param lst_svod_cols:  список с колонками по которым нужно делать свод
    """
    try:
        out_answer_df = base_df.copy()  # делаем копию для последующего соединения с сырыми ответами
        if len(answers_df.columns) != 60:  # проверяем количество колонок с вопросами
            raise BadCountColumnsPPPR

        # очищаем названия колонок от возможных сочетаний .1 которые добавляет пандас при одинаковых колонках
        clean_df_lst = []
        for name_column in answers_df.columns:
            clean_name = re.sub(r'.\d+$', '', name_column)
            clean_df_lst.append(clean_name)

        answers_df.columns = clean_df_lst

        lst_check_cols = ['Меня тревожит проблема наркомании и алкоголизма в современном обществе',
                          'Меня беспокоит, что в современном обществе часто встречается равнодушие и безразличие людей друг к другу',
                          'Меня беспокоит проблема терроризма и насилия в современном мире',
                          'Я боюсь, что может начаться война',
                          'Меня волнует падение моральных норм в обществе, распущенность и хамство',
                          'Меня беспокоит широкое распространение в обществе болезней, многие из которых неизлечимы',
                          'Я обеспокоен экологической обстановкой, люди утратили бережное отношение к природе',
                          'Меня беспокоит несоблюдение законов и прав человека',
                          'Я расстраиваюсь из-за плохих новостей (эпидемии, катастрофы и пр.)',
                          'Я переживаю, что в связи с развитием виртуальной среды исчезнут многие вещи из реальной жизни',

                          'Мое будущее кажется мне слишком неопределенным',
                          'Я боюсь не оправдать ожидания родителей',
                          'Я до сих пор не знаю, чем займусь после окончания школы',
                          'Я боюсь, что в будущем я не смогу в полной мере проявить себя',
                          'Я не уверен, что в будущем буду зарабатывать достаточно, чтобы не нуждаться в материальной помощи со стороны родных',
                          'Я плохо понимаю себя',
                          'Я не знаю, чего я хочу добиться в жизни',
                          'Я никак не могу разобраться, к чему у меня есть способности',
                          'Я часто ощущаю себя одиноким, никому не нужным',
                          'Я испытываю чувство вины из-за некоторых своих действий и поступков',

                          'Общаясь с друзьями, я часто чувствую неуверенность в себе',
                          'Я чувствую себя скованно в общении с представителями противоположного пола',
                          'Мне сложно найти взаимопонимание со сверстниками',
                          'Меня беспокоит, что я не пользуюсь популярностью у представителей противоположного пола',
                          'Я стесняюсь сделать первый шаг в отношениях, завязать знакомство',
                          'Общаться со сверстниками тяжело, так как они грубят, хамят',
                          'Я редко высказываю свое мнение, так как боюсь, что сверстники будут надо мной смеяться',
                          'Я хотел бы быть лидером в группе сверстников, но у меня не получается',
                          'Мне бывает трудно отстаивать свою точку зрения',
                          'Мне трудно делиться с другими своими чувствами',

                          'Я опасаюсь, что, когда я стану взрослым, родители по-прежнему будут слишком активно вмешиваться в мою личную жизнь',
                          'У меня часто бывают ссоры, конфликты с родителями',
                          'Мои родители часто не понимают меня',
                          'Меня возмущает, когда родители вмешиваются в мою жизнь',
                          'Зачастую я не понимаю моих родителей',
                          'Мне не нравится, что родители по-прежнему считают меня маленьким',
                          'Родители до сих пор постоянно контролируют меня',
                          'Нам с родителями часто совершенно не о чем поговорить, кроме моей учебы и питания',
                          'Родители слишком давят на меня из-за школьных оценок',
                          'Мои родители пытаются влиять на организацию моего досуга',

                          'Без Интернета чувствуешь себя «как без рук»',
                          'Без Интернета я боюсь не узнать каких-то важных событий, происходящих в стране и мире',
                          'При отключении электричества / проблемах со связью теряется возможность решать многие жизненные вопросы',
                          'Боюсь, что моя жизнь будет безрадостной, если исчезнет Интернет',
                          'Если у меня нет Интернета, я боюсь оказаться не в курсе каких-то важных событий для меня и друзей',
                          'Мне трудно распределять время между Интернетом и выполнением домашних обязанностей',
                          'Я не могу контролировать время, проводимое в Интернете',
                          'Я недоволен тем, что из-за привязанности к Интернету откладываю важные дела на «потом», не успеваю сделать их вовремя',
                          'Я не успеваю за всеми новыми возможностями, которые появляются в Интернете',
                          'Интернет занимает все мое свободное время',

                          'Мне бы хотелось, чтобы учителя относились ко мне с большим пониманием и уважением',
                          'Я не справляюсь с таким большим объемом домашних заданий',
                          'Бывает, что учителя относятся ко мне несправедливо',
                          'Многие учебные предметы кажутся мне скучными и неинтересными',
                          'Мне не нравятся те требования к одежде, которые предъявляются в школе',
                          'Меня не устраивает школьное расписание',
                          'Мне было бы значительно легче, если бы уроки начинались на 1–2 часа позже',
                          'Школьные классы и коридоры выглядят неуютно',
                          'Если бы было можно не учиться в школе, я бы согласился',
                          'Школа и домашние обязанности занимают слишком много времени',
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
            raise BadOrderPPPR

        # словарь для замены слов на числа
        dct_replace_value = {'совершенно согласен': 5,
                             'скорее согласен': 4,
                             'трудно сказать (ни да, ни нет)': 3,
                             'скорее нет': 2,
                             'абсолютно не согласен': 1,
                             }
        valid_values = [1, 2, 3, 4, 5]
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
            raise BadValuePPPR

        base_df['ОПО_Значение'] = answers_df.apply(calc_value_opo, axis=1)
        base_df['ОПО_Диапазон'] = base_df['ОПО_Значение'].apply(calc_level)

        base_df['СОЛБ_Значение'] = answers_df.apply(calc_value_solb, axis=1)
        base_df['СОЛБ_Диапазон'] = base_df['СОЛБ_Значение'].apply(calc_level)

        base_df['СИ_Значение'] = answers_df.apply(calc_value_si, axis=1)
        base_df['СИ_Диапазон'] = base_df['СИ_Значение'].apply(calc_level)

        base_df['СО_Значение'] = answers_df.apply(calc_value_so, axis=1)
        base_df['СО_Диапазон'] = base_df['СО_Значение'].apply(calc_level)

        base_df['ВР_Значение'] = answers_df.apply(calc_value_vr, axis=1)
        base_df['ВР_Диапазон'] = base_df['ВР_Значение'].apply(calc_level)

        base_df['СПИ_Значение'] = answers_df.apply(calc_value_spi, axis=1)
        base_df['СПИ_Диапазон'] = base_df['СПИ_Значение'].apply(calc_level)

        base_df['СШ_Значение'] = answers_df.apply(calc_value_ssh, axis=1)
        base_df['СШ_Диапазон'] = base_df['СШ_Значение'].apply(calc_level)


     # Создаем датафрейм для создания части в общий датафрейм
        part_df = pd.DataFrame()
        part_df['ПППВРСР_ОПО_Значение'] = base_df['ОПО_Значение']
        part_df['ПППВРСР_ОПО_Диапазон'] = base_df['ОПО_Диапазон']

        part_df['ПППВРСР_СОЛБ_Значение'] = base_df['СОЛБ_Значение']
        part_df['ПППВРСР_СОЛБ_Диапазон'] = base_df['СОЛБ_Диапазон']

        part_df['ПППВРСР_СИ_Значение'] = base_df['СИ_Значение']
        part_df['ПППВРСР_СИ_Диапазон'] = base_df['СИ_Диапазон']

        part_df['ПППВРСР_СО_Значение'] = base_df['СО_Значение']
        part_df['ПППВРСР_СО_Диапазон'] = base_df['СО_Диапазон']

        part_df['ПППВРСР_ВР_Значение'] = base_df['ВР_Значение']
        part_df['ПППВРСР_ВР_Диапазон'] = base_df['ВР_Диапазон']

        part_df['ПППВРСР_СПИ_Значение'] = base_df['СПИ_Значение']
        part_df['ПППВРСР_СПИ_Диапазон'] = base_df['СПИ_Диапазон']

        part_df['ПППВРСР_СШ_Значение'] = base_df['СШ_Значение']
        part_df['ПППВРСР_СШ_Диапазон'] = base_df['СШ_Диапазон']

        out_answer_df = pd.concat([out_answer_df, answers_df], axis=1)  # Датафрейм для проверки
        base_df.sort_values(by='ОПО_Значение', ascending=False, inplace=True)  # сортируем

        # Делаем свод  по  шкалам
        dct_svod_sub = {'ОПО_Значение': 'ОПО_Диапазон',
                        'СОЛБ_Значение': 'СОЛБ_Диапазон',
                        'СИ_Значение': 'СИ_Диапазон',
                        'СО_Значение': 'СО_Диапазон',
                        'ВР_Значение': 'ВР_Диапазон',

                        'СПИ_Значение': 'СПИ_Диапазон',
                        'СШ_Значение': 'СШ_Диапазон',
                        }

        dct_rename_svod_sub = {'ОПО_Значение': 'ОПО',
                        'СОЛБ_Значение': 'СОЛБ',
                        'СИ_Значение': 'СИ',
                        'СО_Значение': 'СО',
                        'ВР_Значение': 'ВР',

                        'СПИ_Значение': 'СПИ',
                        'СШ_Значение': 'СШ',
                              }

        lst_sub = ['1-2', '2.01-3', '3.01-4', '4.01-5']

        base_svod_sub_df = create_union_svod(base_df, dct_svod_sub, dct_rename_svod_sub, lst_sub)

        # считаем среднее значение по шкалам
        avg_vcha = round(base_df['ОПО_Значение'].mean(), 2)
        avg_o = round(base_df['СОЛБ_Значение'].mean(), 2)
        avg_ruvs = round(base_df['СИ_Значение'].mean(), 2)

        avg_psp = round(base_df['СО_Значение'].mean(), 2)
        avg_ppvs = round(base_df['ВР_Значение'].mean(), 2)
        avg_ip = round(base_df['СПИ_Значение'].mean(), 2)

        avg_prp = round(base_df['СШ_Значение'].mean(), 2)

        avg_dct = {'Среднее значение шкалы Общая проблемная озабоченность': avg_vcha,
                   'Среднее значение шкалы Проблемы, связанные с общественной и личной безопасностью': avg_o,
                   'Среднее значение шкалы Проблемы становления идентичности': avg_ruvs,

                   'Среднее значение шкалы Проблемы, связанные с общением': avg_psp,
                   'Среднее значение шкалы Проблемы во взаимоотношениях с родителями': avg_ppvs,
                   'Среднее значение шкалы Проблемы, связанные с погруженностью в Интернет': avg_ip,

                   'Среднее значение фактора Проблемы, связанные со школой': avg_prp,
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

        dct_prefix = {'ОПО_Диапазон': 'ОПО',
                      'СОЛБ_Диапазон': 'СОЛБ',
                      'СИ_Диапазон': 'СИ',

                      'СО_Диапазон': 'СО',
                      'ВР_Диапазон': 'ВР',
                      'СПИ_Диапазон': 'СПИ',

                      'СШ_Диапазон': 'СШ',
                      }

        out_dct = create_list_on_level_pppr(base_df, out_dct, lst_sub, dct_prefix)

        """
                        Сохраняем в зависимости от необходимости делать своды по определенным колонкам
                        """
        if len(lst_svod_cols) == 0:
            return out_dct, part_df

        else:
            out_dct = create_result_ppp_regush(base_df, out_dct, lst_svod_cols)
            return out_dct, part_df

    except BadOrderPPPR:
        messagebox.showerror('Лахеcис',
                             f'При обработке вопросов теста Психологические проблемы подростков в реальной и виртуальной сфере Регуш обнаружены неправильные вопросы. Проверьте названия колонок с вопросами:\n'
                             f'{error_order_message[:5000]}\n'
                             f'Используйте при создании Яндекс-формы написание вопросов из руководства пользователя программы Лахесис.')
    except BadValuePPPR:
        messagebox.showerror('Лахеcис',
                             f'При обработке вопросов теста Психологические проблемы подростков в реальной и виртуальной сфере Регуш обнаружены неправильные варианты ответов. Проверьте ответы на указанных строках:\n'
                             f'{error_message[:5000]}\n'
                             f'Используйте при создании Яндекс-формы написание вариантов ответа из руководства пользователя программы Лахесис.')


    except BadCountColumnsPPPR:
        messagebox.showerror('Лахеcис',
                             f'Проверьте количество колонок с ответами на тест Психологические проблемы подростков в реальной и виртуальной сфере Регуш\n'
                             f'Должно быть 60 колонок с ответами')











