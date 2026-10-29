"""
Скрипт для обработки результатов Многомерная шкала школьной вовлеченности, MSES Фомина Моросанова

"""

import pandas as pd
import re
from tkinter import messagebox
from lachesis_support_functions import round_mean_two,calc_count_scale,create_union_svod, create_list_on_level

class BadOrderMSHSHVFM(Exception):
    """
    Исключение для обработки случая когда колонки не совпадают
    """
    pass


class BadValueMSHSHVFM(Exception):
    """
    Исключение для неправильных значений в вариантах ответов
    """
    pass

class BadCountColumnsMSHSHVFM(Exception):
    """
    Исключение для обработки случая если количество колонок не равно 37
    """
    pass

def calc_level_scale(value,count):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """
    result = round((value / (count*5)) * 100)

    return f'{result}%'


def calc_level_procent(value:str):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """
    try:
        value = int(value.replace('%',''))
        if 20 <= value <= 39:
            return '20-39%'
        elif 40<= value <= 59:
            return '40-59%'
        elif 60 <= value <= 79:
            return '60-79%'
        else:
            return '80-100%'

    except:
        return 'ошибочное значение'


def calc_value_v_p(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [1,2,3,4]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_pr:
            value_forward += value


    return value_forward


def calc_value_v_k(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [5,6,7,8,9]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_pr:
            value_forward += value


    return value_forward


def calc_value_v_a(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [10,11,12,13,14]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_pr:
            value_forward += value


    return value_forward


def calc_value_v_s(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [15,16,17,18,19]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_pr:
            value_forward += value


    return value_forward

def calc_value_b_p(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [20,21,22,23,24,25,26,27]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_pr:
            value_forward += value


    return value_forward

def calc_value_b_k(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [28,29]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_pr:
            value_forward += value


    return value_forward

def calc_value_b_a(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [30,31,32,33]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_pr:
            value_forward += value


    return value_forward

def calc_value_b_s(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [34,35,36,37]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_pr:
            value_forward += value


    return value_forward


def create_itog_stens(row):
    """
    Функция для создания строки с итоговым стеном
    :param row: строка с результатами
    :return:
    """
    lst_out = list(map(str,row))
    return '-'.join(lst_out)


def create_result_mshshv_fom_mor(base_df:pd.DataFrame, out_dct:dict, lst_svod_cols:list):
    """
    Функция для подсчета результата если указаны колонки по которым нужно провести свод
    :param df: датафрейм с результатами
    :param out_dct: словарь с уже подсчитанными базовыми данными
    :param lst_svod_cols: список сводных колонок
    :return: словарь
    """
    lst_level = ['20-39%', '40-59%', '60-79%', '80-100%']
    lst_reindex_one_level_cols = lst_svod_cols.copy()
    lst_reindex_one_level_cols.extend(
        ['20-39%', '40-59%', '60-79%', '80-100%',
         'Итого'])  # Основная шкала

    # Конфликтность
    svod_count_one_level_k_df = calc_count_scale(base_df, lst_svod_cols,
                                                 'В_П_Значение',
                                                 'В_П_Диапазон_Пр',
                                                 lst_reindex_one_level_cols, lst_level)
    # Дистанцирование
    svod_count_one_level_d_df = calc_count_scale(base_df, lst_svod_cols,
                                                 'В_К_Значение',
                                                 'В_К_Диапазон_Пр',
                                                 lst_reindex_one_level_cols, lst_level)
    # Самоконтроль
    svod_count_one_level_s_df = calc_count_scale(base_df, lst_svod_cols,
                                                 'В_Э_Значение',
                                                 'В_Э_Диапазон_Пр',
                                                 lst_reindex_one_level_cols, lst_level)
    # ПСП
    svod_count_one_level_psp_df = calc_count_scale(base_df, lst_svod_cols,
                                                   'В_С_Значение',
                                                   'В_С_Диапазон_Пр',
                                                   lst_reindex_one_level_cols, lst_level)


    # ПО
    svod_count_one_level_po_df = calc_count_scale(base_df, lst_svod_cols,
                                                  'Б_П_Значение',
                                                  'Б_П_Диапазон_Пр',
                                                  lst_reindex_one_level_cols, lst_level)
    # БИ
    svod_count_one_level_bi_df = calc_count_scale(base_df, lst_svod_cols,
                                                  'Б_К_Значение',
                                                  'Б_К_Диапазон_Пр',
                                                  lst_reindex_one_level_cols, lst_level)
    # ПРП
    svod_count_one_level_prp_df = calc_count_scale(base_df, lst_svod_cols,
                                                   'Б_Э_Значение',
                                                   'Б_Э_Диапазон_Пр',
                                                   lst_reindex_one_level_cols, lst_level)
    # ПП
    svod_count_one_level_pp_df = calc_count_scale(base_df, lst_svod_cols,
                                                  'Б_С_Значение',
                                                  'Б_С_Диапазон_Пр',
                                                  lst_reindex_one_level_cols, lst_level)

    # Считаем среднее по субшкалам
    svod_mean_one_df = pd.pivot_table(base_df,
                                      index=lst_svod_cols,
                                      values=[
                                              'В_П_Значение',
                                              'В_К_Значение',
                                              'В_Э_Значение',
                                              'В_С_Значение',

                                              'Б_П_Значение',
                                              'Б_К_Значение',
                                              'Б_Э_Значение',
                                              'Б_С_Значение',
                                              ],
                                      aggfunc=round_mean_two)
    svod_mean_one_df.reset_index(inplace=True)

    # упорядочиваем колонки
    new_order_cols = lst_svod_cols.copy()
    new_order_cols.extend(([
        'В_П_Значение',
        'В_К_Значение',
        'В_Э_Значение',
        'В_С_Значение',

        'Б_П_Значение',
        'Б_К_Значение',
        'Б_Э_Значение',
        'Б_С_Значение',
                            ]))
    svod_mean_one_df = svod_mean_one_df.reindex(columns=new_order_cols)

    dct_rename_cols_mean = {
                            'В_П_Значение': 'Ср. Вовлеченность Поведенческая',
                            'В_К_Значение': 'Ср. Вовлеченность Когнитивная',
                            'В_Э_Значение': 'Ср. Вовлеченность Эмоциональная',
                            'В_С_Значение': 'Ср. Вовлеченность Социальная',

                            'Б_П_Значение': 'Ср. Безучастность Поведенческая',
                            'Б_К_Значение': 'Ср. Безучастность Когнитивная',
                            'Б_Э_Значение': 'Ср. Безучастность Эмоциональная',
                            'Б_С_Значение': 'Ср. Безучастность Социальная',
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
                    f'В_П {out_name}': svod_count_one_level_k_df,
                    f'В_К {out_name}': svod_count_one_level_d_df,
                    f'В_Э {out_name}': svod_count_one_level_s_df,
                    f'В_С {out_name}': svod_count_one_level_psp_df,

                    f'Б_П {out_name}': svod_count_one_level_po_df,
                    f'Б_К {out_name}': svod_count_one_level_bi_df,
                    f'Б_Э {out_name}': svod_count_one_level_prp_df,
                    f'Б_С {out_name}': svod_count_one_level_pp_df,
                    })

    if len(lst_svod_cols) == 1:
        return out_dct
    else:
        for idx, name_column in enumerate(lst_svod_cols):


            lst_reindex_column_level_cols = [lst_svod_cols[idx],'20-39%', '40-59%', '60-79%', '80-100%',
                                                  'Итого']

            # Конфликтность
            svod_count_column_level_k_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                            'В_П_Значение',
                                                            'В_П_Диапазон_Пр',
                                                            lst_reindex_column_level_cols, lst_level)
            # Дистанцирование
            svod_count_column_level_d_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                            'В_К_Значение',
                                                            'В_К_Диапазон_Пр',
                                                            lst_reindex_column_level_cols, lst_level)
            # Самоконтроль
            svod_count_column_level_s_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                            'В_Э_Значение',
                                                            'В_Э_Диапазон_Пр',
                                                            lst_reindex_column_level_cols, lst_level)
            # ПСП
            svod_count_column_level_psp_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                              'В_С_Значение',
                                                              'В_С_Диапазон_Пр',
                                                              lst_reindex_column_level_cols, lst_level)

            # ПО
            svod_count_column_level_po_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                             'Б_П_Значение',
                                                             'Б_П_Диапазон_Пр',
                                                             lst_reindex_column_level_cols, lst_level)
            # БИ
            svod_count_column_level_bi_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                             'Б_К_Значение',
                                                             'Б_К_Диапазон_Пр',
                                                             lst_reindex_column_level_cols, lst_level)
            # ПРП
            svod_count_column_level_prp_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                              'Б_Э_Значение',
                                                              'Б_Э_Диапазон_Пр',
                                                              lst_reindex_column_level_cols, lst_level)
            # ПП
            svod_count_column_level_pp_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                             'Б_С_Значение',
                                                             'Б_С_Диапазон_Пр',
                                                             lst_reindex_column_level_cols, lst_level)

            # Считаем среднее по субшкалам
            svod_mean_column_df = pd.pivot_table(base_df,
                                                 index=[lst_svod_cols[idx]],
                                                 values=[
                                                     'В_П_Значение',
                                                     'В_К_Значение',
                                                     'В_Э_Значение',
                                                     'В_С_Значение',

                                                     'Б_П_Значение',
                                                     'Б_К_Значение',
                                                     'Б_Э_Значение',
                                                     'Б_С_Значение',
                                                 ],
                                                 aggfunc=round_mean_two)
            svod_mean_column_df.reset_index(inplace=True)

            # упорядочиваем колонки
            new_order_cols = [lst_svod_cols[idx]].copy()
            new_order_cols.extend(([
                'В_П_Значение',
                'В_К_Значение',
                'В_Э_Значение',
                'В_С_Значение',

                'Б_П_Значение',
                'Б_К_Значение',
                'Б_Э_Значение',
                'Б_С_Значение',
            ]))
            svod_mean_column_df = svod_mean_column_df.reindex(columns=new_order_cols)

            dct_rename_cols_mean = {
                'В_П_Значение': 'Ср. Вовлеченность Поведенческая',
                'В_К_Значение': 'Ср. Вовлеченность Когнитивная',
                'В_Э_Значение': 'Ср. Вовлеченность Эмоциональная',
                'В_С_Значение': 'Ср. Вовлеченность Социальная',

                'Б_П_Значение': 'Ср. Безучастность Поведенческая',
                'Б_К_Значение': 'Ср. Безучастность Когнитивная',
                'Б_Э_Значение': 'Ср. Безучастность Эмоциональная',
                'Б_С_Значение': 'Ср. Безучастность Социальная',
            }
            svod_mean_column_df.rename(columns=dct_rename_cols_mean, inplace=True)

            # Готовим наименование
            name_column = lst_svod_cols[idx]
            name_column = re.sub(r'[\[\]\'+()<> :"?*|\\/]', '_', name_column)
            name_column = name_column[:15]


            out_dct.update({f'Ср {name_column}': svod_mean_column_df,
                            f'В_П {name_column}': svod_count_column_level_k_df,
                            f'В_К {name_column}': svod_count_column_level_d_df,
                            f'В_Э {name_column}': svod_count_column_level_s_df,
                            f'В_С {name_column}': svod_count_column_level_psp_df,

                            f'Б_П {name_column}': svod_count_column_level_po_df,
                            f'Б_К {name_column}': svod_count_column_level_bi_df,
                            f'Б_Э {name_column}': svod_count_column_level_prp_df,
                            f'Б_С {name_column}': svod_count_column_level_pp_df,
                            })
        return out_dct


def processing_mshshv_fom_mor(base_df: pd.DataFrame, answers_df: pd.DataFrame, lst_svod_cols:list):
    """
    Функция для обработки
    :param base_df: часть датафрейма с описательными колонками
    :param answers_df: часть датафрейма с ответами
    :param lst_svod_cols:  список с колонками по которым нужно делать свод
    """
    try:
        out_answer_df = base_df.copy()  # делаем копию для последующего соединения с сырыми ответами
        union_base_df = base_df.copy()  # делаем копию анкетной части чтобы потом соединить ее с ответной частью
        quantity_cols_base_df = base_df.shape[1]  # количество колонок в анкетной части

        if len(answers_df.columns) != 37:  # проверяем количество колонок с вопросами
            raise BadCountColumnsMSHSHVFM

        # очищаем названия колонок от возможных сочетаний .1 которые добавляет пандас при одинаковых колонках
        clean_df_lst = []
        for name_column in answers_df.columns:
            clean_name = re.sub(r'.\d+$', '', name_column)
            clean_df_lst.append(clean_name)

        answers_df.columns = clean_df_lst

        lst_check_cols = ['В школе всегда стараюсь изо всех сил',
                          'Я активно работаю на уроках',
                          'Когда мне что-то непонятно – задаю вопросы',
                          'Принимаю участие в школьных мероприятиях (например, в кружках, спортивных соревнованиях, школьных праздниках)',
                          'Обдумываю, как буду выполнять домашнюю работу',
                          'Я проверяю свою самостоятельную работу, прежде чем сдать ее учителю',
                          'Я продолжаю искать решение, даже когда «застреваю» на каком-то вопросе при выполнении учебной работы',
                          'В школе я усердно учусь, несмотря на возникающие проблемы / трудности',
                          'Стараюсь понять, что я сделал неправильно, когда вижу свои ошибки в выполненном задании',
                          'Хорошая успеваемость в школе важна для моего будущего',

                          'Мне весело в школе',
                          'Я счастлив в школе',
                          'Я горжусь своей школой',
                          'Мне интересно, что мы изучаем в школе',
                          'Я помогаю друзьям, когда им трудно',
                          'Мне нравится участвовать в школьных делах со сверстниками',
                          'С одноклассниками мы учимся друг у друга, когда занимаемся вместе',
                          'Легко завожу новых друзей в школе',
                          'Мне нравится проводить время со сверстниками в школе',
                          'Во время работы в классе обычно «валяю дурака»',

                          'Нахожу способы опоздать в школу',
                          'Нахожу причины, чтобы выйти из класса во время урока',
                          'Нарушаю правила поведения в школе',
                          'В школе у меня проблемы с поведением',
                          'Я не выполняю домашнюю работу',
                          'Я часто отвлекаюсь на уроках',
                          'На уроках в школе я невнимателен',
                          'Если я не понимаю задачу, я сразу сдаюсь',
                          'Выполнить домашнюю работу быстро для меня важнее, чем сделать ее правильно',
                          'Я нервничаю в школе',

                          'Я перегружен в школе',
                          'В школе чувствую себя некомфортно',
                          'Школа меня раздражает',
                          'У меня нет друзей в школе',
                          'В школе на меня не обращают внимания',
                          'Отношения с одноклассниками не очень важны для меня',
                          'В школе мне ни до кого нет дела'
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
            raise BadOrderMSHSHVFM

        # словарь для замены слов на числа
        dct_replace_value = {'совсем на меня не похоже': 1,
                             'скорее не похоже': 2,
                             'нечто среднее': 3,
                             'скорее похоже': 4,
                             'очень на меня похоже': 5
                             }
        valid_values = [1,2,3,4,5]
        answers_df.replace(dct_replace_value, inplace=True)  # заменяем слова на цифры для подсчетов
        # Проверяем, есть ли значения, отличающиеся от указанных в списке
        lst_error_answers = []  # список для хранения строк где найдены неправильные ответы

        for i in range(37):
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
            raise BadValueMSHSHVFM

        base_df['В_П_Значение'] = answers_df.apply(calc_value_v_p, axis=1)
        base_df['В_П_Процент'] = base_df['В_П_Значение'].apply(lambda x: calc_level_scale(x, 4))
        base_df['В_П_Диапазон_Пр'] = base_df['В_П_Процент'].apply(calc_level_procent)

        base_df['В_К_Значение'] = answers_df.apply(calc_value_v_k, axis=1)
        base_df['В_К_Процент'] = base_df['В_К_Значение'].apply(lambda x: calc_level_scale(x, 5))
        base_df['В_К_Диапазон_Пр'] = base_df['В_К_Процент'].apply(calc_level_procent)

        base_df['В_Э_Значение'] = answers_df.apply(calc_value_v_a, axis=1)
        base_df['В_Э_Процент'] = base_df['В_Э_Значение'].apply(lambda x: calc_level_scale(x, 5))
        base_df['В_Э_Диапазон_Пр'] = base_df['В_Э_Процент'].apply(calc_level_procent)

        base_df['В_С_Значение'] = answers_df.apply(calc_value_v_s, axis=1)
        base_df['В_С_Процент'] = base_df['В_С_Значение'].apply(lambda x: calc_level_scale(x, 5))
        base_df['В_С_Диапазон_Пр'] = base_df['В_С_Процент'].apply(calc_level_procent)

        base_df['Б_П_Значение'] = answers_df.apply(calc_value_b_p, axis=1)
        base_df['Б_П_Процент'] = base_df['Б_П_Значение'].apply(lambda x: calc_level_scale(x, 8))
        base_df['Б_П_Диапазон_Пр'] = base_df['Б_П_Процент'].apply(calc_level_procent)

        base_df['Б_К_Значение'] = answers_df.apply(calc_value_b_k, axis=1)
        base_df['Б_К_Процент'] = base_df['Б_К_Значение'].apply(lambda x: calc_level_scale(x, 2))
        base_df['Б_К_Диапазон_Пр'] = base_df['Б_К_Процент'].apply(calc_level_procent)

        base_df['Б_Э_Значение'] = answers_df.apply(calc_value_b_a, axis=1)
        base_df['Б_Э_Процент'] = base_df['Б_Э_Значение'].apply(lambda x: calc_level_scale(x, 4))
        base_df['Б_Э_Диапазон_Пр'] = base_df['Б_Э_Процент'].apply(calc_level_procent)

        base_df['Б_С_Значение'] = answers_df.apply(calc_value_b_s, axis=1)
        base_df['Б_С_Процент'] = base_df['Б_С_Значение'].apply(lambda x: calc_level_scale(x, 4))
        base_df['Б_С_Диапазон_Пр'] = base_df['Б_С_Процент'].apply(calc_level_procent)

        # Упорядочиваем
        result_df = base_df.iloc[:, quantity_cols_base_df:]  # отсекаем часть с результатами чтобы упорядочить
        lst_stens = [column for column in result_df.columns if 'Процент' in column]
        result_df['Проценты_по_шкалам'] = result_df[lst_stens].apply(create_itog_stens, axis=1)

        new_order_lst = ['Проценты_по_шкалам',
                         'В_П_Процент', 'В_К_Процент', 'В_Э_Процент', 'В_С_Процент',
                         'Б_П_Процент', 'Б_К_Процент', 'Б_Э_Процент', 'Б_С_Процент',

                         'В_П_Диапазон_Пр', 'В_К_Диапазон_Пр', 'В_Э_Диапазон_Пр', 'В_С_Диапазон_Пр',
                         'Б_П_Диапазон_Пр', 'Б_К_Диапазон_Пр', 'Б_Э_Диапазон_Пр', 'Б_С_Диапазон_Пр',

                         'В_П_Значение', 'В_К_Значение', 'В_Э_Значение', 'В_С_Значение',
                         'Б_П_Значение', 'Б_К_Значение', 'Б_Э_Значение', 'Б_С_Значение',
                         ]
        result_df = result_df.reindex(columns=new_order_lst)  # изменяем порядок
        base_df = pd.concat([union_base_df, result_df], axis=1)  # соединяем и перезаписываем base_df

        # Создаем датафрейм для создания части в общий датафрейм
        part_df = pd.DataFrame()
        # Общая тревожность
        part_df['МШШВФМ_Проценты_по_шкалам'] = base_df['Проценты_по_шкалам']
        part_df['МШШВФМ_В_П_Процент'] = base_df['В_П_Процент']
        part_df['МШШВФМ_В_К_Процент'] = base_df['В_К_Процент']
        part_df['МШШВФМ_В_Э_Процент'] = base_df['В_Э_Процент']
        part_df['МШШВФМ_В_С_Процент'] = base_df['В_С_Процент']

        part_df['МШШВФМ_Б_П_Процент'] = base_df['Б_П_Процент']
        part_df['МШШВФМ_Б_К_Процент'] = base_df['Б_К_Процент']
        part_df['МШШВФМ_Б_Э_Процент'] = base_df['Б_Э_Процент']
        part_df['МШШВФМ_Б_С_Процент'] = base_df['Б_С_Процент']

        part_df['МШШВФМ_В_П_Диапазон'] = base_df['В_П_Диапазон_Пр']
        part_df['МШШВФМ_В_К_Диапазон'] = base_df['В_К_Диапазон_Пр']
        part_df['МШШВФМ_В_Э_Диапазон'] = base_df['В_Э_Диапазон_Пр']
        part_df['МШШВФМ_В_С_Диапазон'] = base_df['В_С_Диапазон_Пр']

        part_df['МШШВФМ_Б_П_Диапазон'] = base_df['Б_П_Диапазон_Пр']
        part_df['МШШВФМ_Б_К_Диапазон'] = base_df['Б_К_Диапазон_Пр']
        part_df['МШШВФМ_Б_Э_Диапазон'] = base_df['Б_Э_Диапазон_Пр']
        part_df['МШШВФМ_Б_С_Диапазон'] = base_df['Б_С_Диапазон_Пр']

        part_df['МШШВФМ_В_П_Значение'] = base_df['В_П_Значение']
        part_df['МШШВФМ_В_К_Значение'] = base_df['В_К_Значение']
        part_df['МШШВФМ_В_Э_Значение'] = base_df['В_Э_Значение']
        part_df['МШШВФМ_В_С_Значение'] = base_df['В_С_Значение']

        part_df['МШШВФМ_Б_П_Значение'] = base_df['Б_П_Значение']
        part_df['МШШВФМ_Б_К_Значение'] = base_df['Б_К_Значение']
        part_df['МШШВФМ_Б_Э_Значение'] = base_df['Б_Э_Значение']
        part_df['МШШВФМ_Б_С_Значение'] = base_df['Б_С_Значение']

        out_answer_df = pd.concat([out_answer_df, answers_df], axis=1)  # Датафрейм для проверки

        base_df.sort_values(by='Б_П_Значение', inplace=True, ascending=False)

        # Делаем свод  по  шкалам
        dct_svod_sub = {'В_П_Значение': 'В_П_Диапазон_Пр',
                        'В_К_Значение': 'В_К_Диапазон_Пр',
                        'В_Э_Значение': 'В_Э_Диапазон_Пр',
                        'В_С_Значение': 'В_С_Диапазон_Пр',

                        'Б_П_Значение': 'Б_П_Диапазон_Пр',
                        'Б_К_Значение': 'Б_К_Диапазон_Пр',
                        'Б_Э_Значение': 'Б_Э_Диапазон_Пр',
                        'Б_С_Значение': 'Б_С_Диапазон_Пр',
                        }

        dct_rename_svod_sub = {'В_П_Значение': 'В_П',
                               'В_К_Значение': 'В_К',
                               'В_Э_Значение': 'В_Э',
                               'В_С_Значение': 'В_С',

                               'Б_П_Значение': 'Б_П',
                               'Б_К_Значение': 'Б_К',
                               'Б_Э_Значение': 'Б_Э',
                               'Б_С_Значение': 'Б_С',
                               }

        lst_sub = ['20-39%', '40-59%', '60-79%', '80-100%']

        base_svod_sub_df = create_union_svod(base_df, dct_svod_sub, dct_rename_svod_sub, lst_sub)

        # считаем среднее значение по шкалам
        avg_ip = round(base_df['В_П_Значение'].mean(), 2)
        avg_k = round(base_df['В_К_Значение'].mean(), 2)
        avg_d = round(base_df['В_Э_Значение'].mean(), 2)
        avg_s = round(base_df['В_С_Значение'].mean(), 2)

        avg_po = round(base_df['Б_П_Значение'].mean(), 2)
        avg_bi = round(base_df['Б_К_Значение'].mean(), 2)
        avg_prp = round(base_df['Б_Э_Значение'].mean(), 2)
        avg_pp = round(base_df['Б_С_Значение'].mean(), 2)

        avg_dct = {'Среднее значение шкалы Вовлеченность Поведенческая': avg_ip,
                   'Среднее значение шкалы Вовлеченность Когнитивная': avg_k,
                   'Среднее значение шкалы Вовлеченность Эмоциональная': avg_d,
                   'Среднее значение шкалы Вовлеченность Социальная': avg_s,

                   'Среднее значение шкалы Безучастность Поведенческая': avg_po,
                   'Среднее значение шкалы Безучастность Когнитивная': avg_bi,
                   'Среднее значение шкалы Безучастность Эмоциональная': avg_prp,
                   'Среднее значение шкалы Безучастность Социальная': avg_pp,
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

        dct_prefix = {'В_П_Диапазон_Пр': 'В_П',
                      'В_К_Диапазон_Пр': 'В_К',
                      'В_Э_Диапазон_Пр': 'В_Э',
                      'В_С_Диапазон_Пр': 'В_С',

                      'Б_П_Диапазон_Пр': 'Б_П',
                      'Б_К_Диапазон_Пр': 'Б_К',
                      'Б_Э_Диапазон_Пр': 'Б_Э',
                      'Б_С_Диапазон_Пр': 'Б_С',

                      }

        out_dct = create_list_on_level(base_df, out_dct, lst_sub, dct_prefix)
        """
                        Сохраняем в зависимости от необходимости делать своды по определенным колонкам
                        """
        if len(lst_svod_cols) == 0:
            return out_dct, part_df
        else:
            out_dct = create_result_mshshv_fom_mor(base_df, out_dct, lst_svod_cols)
            return out_dct, part_df


    except BadOrderMSHSHVFM:
        messagebox.showerror('Лахеcис',
                             f'При обработке вопросов теста Многомерная шкала школьной вовлеченности, MSES Фомина Моросанова обнаружены неправильные вопросы. Проверьте названия колонок с вопросами:\n'
                             f'{error_order_message[:5000]}\n'
                             f'Используйте при создании Яндекс-формы написание вопросов из руководства пользователя программы Лахесис.')
    except BadValueMSHSHVFM:
        messagebox.showerror('Лахеcис',
                             f'При обработке вопросов теста Многомерная шкала школьной вовлеченности, MSES Фомина Моросанова обнаружены неправильные варианты ответов. Проверьте ответы на указанных строках:\n'
                             f'{error_message[:5000]}\n'
                             f'Используйте при создании Яндекс-формы написание вариантов ответа из руководства пользователя программы Лахесис.')


    except BadCountColumnsMSHSHVFM:
        messagebox.showerror('Лахеcис',
                             f'Проверьте количество колонок с ответами на тест Многомерная шкала школьной вовлеченности, MSES Фомина Моросанова\n'
                             f'Должно быть 37 колонок с ответами')








