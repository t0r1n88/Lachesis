"""
Скрипт для обработки результатов теста Степень увлеченности младших подростков компьютерными играми Гришина
"""

import pandas as pd
import re
from tkinter import messagebox
from lachesis_support_functions import round_mean_two,calc_count_scale,create_union_svod, create_list_on_level

class BadOrderSUMPKIG(Exception):
    """
    Исключение для обработки случая когда колонки не совпадают
    """
    pass


class BadValueSUMPKIG(Exception):
    """
    Исключение для неправильных значений в вариантах ответов
    """
    pass

class BadCountColumnsSUMPKIG(Exception):
    """
    Исключение для обработки случая если количество колонок не равно 22
    """
    pass


def calc_value_em(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [4,5,13,18,20]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_pr:
            value_forward += value
    return value_forward

def calc_value_sk(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [3,8,9,11,12,15,16,21,22]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_pr:
            value_forward += value
    return value_forward

def calc_value_cn(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [1,6,7]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_pr:
            value_forward += value
    return value_forward

def calc_value_ro(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [2,17]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_pr:
            value_forward += value
    return value_forward

def calc_value_po(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [10,14,19]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_pr:
            value_forward += value
    return value_forward


def calc_value(row):
    """
    Функция для подсчета значения
    :return: число
    """
    em,sk,cn,ro,po = row

    out_value = (0.21*em) + (0.43*sk) + (0.08 * ro) + (0.34*po) + 0.3
    return round(out_value,0)


def calc_level(value):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """
    if 6<= value <= 11:
        return f'естественный уровень'
    elif 12 <= value <= 21:
        return f'средний уровень'
    else:
        return f'зависимость'


def create_list_on_level_sumpki(base_df:pd.DataFrame, out_dct:dict, lst_level:list, dct_prefix:dict):
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
                if level == 'естественный уровень':
                    level = 'естественный'
                elif level == 'средний уровень':
                    level = 'средний'
                dct_level[f'{dct_prefix[key]}. {level}'] = temp_df
        out_dct.update(dct_level)

    return out_dct


def create_result_sumpki_grish(base_df:pd.DataFrame, out_dct:dict, lst_svod_cols:list):
    """
    Функция для подсчета результата если указаны колонки по которым нужно провести свод
    :param df: датафрейм с результатами
    :param out_dct: словарь с уже подсчитанными базовыми данными
    :param lst_svod_cols: список сводных колонок
    :return: словарь
    """
    lst_level = ['естественный уровень', 'средний уровень', 'зависимость']

    lst_reindex_one_level_cols = lst_svod_cols.copy()
    lst_reindex_one_level_cols.extend(['естественный уровень', 'средний уровень', 'зависимость',
                                       'Итого'])  # Основная шкала

    svod_count_one_level_vcha_df = calc_count_scale(base_df, lst_svod_cols,
                                                    'СУ_Значение',
                                                    'СУ_Уровень',
                                                    lst_reindex_one_level_cols, lst_level)

    # Считаем среднее по субшкалам
    svod_mean_one_df = pd.pivot_table(base_df,
                                      index=lst_svod_cols,
                                      values=['ЭО_Значение',
                                              'СК_Значение',
                                              'ЦН_Значение',
                                              'РО_Значение',
                                              'ПО_Значение',
                                              'СУ_Значение'
                                              ],
                                      aggfunc=round_mean_two)
    svod_mean_one_df.reset_index(inplace=True)

    # упорядочиваем колонки
    new_order_cols = lst_svod_cols.copy()
    new_order_cols.extend((['ЭО_Значение', 'СК_Значение', 'ЦН_Значение',
                            'РО_Значение', 'ПО_Значение', 'СУ_Значение'
                            ]))
    svod_mean_one_df = svod_mean_one_df.reindex(columns=new_order_cols)

    dct_rename_cols_mean = {'ЭО_Значение': 'Ср. Эмоциональное отношение к КИ',
                            'СК_Значение': 'Ср. Уровень самоконтроля',
                            'ЦН_Значение': 'Ср. Целевая направленность',
                            'РО_Значение': 'Ср. Родительского отношения',
                            'ПО_Значение': 'Ср. Уровня предпочтения  общения с героями КИ',
                            'СУ_Значение': 'Ср. Степень увлеченности',
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
                    f'СУ {out_name}': svod_count_one_level_vcha_df,
                    })

    if len(lst_svod_cols) == 1:
        return out_dct

    else:
        for idx, name_column in enumerate(lst_svod_cols):
            lst_reindex_column_level_cols = [lst_svod_cols[idx],'естественный уровень', 'средний уровень', 'зависимость',
                                                  'Итого']
            # ВЧА
            svod_count_column_level_vcha_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                            'СУ_Значение',
                                                            'СУ_Уровень',
                                                            lst_reindex_column_level_cols, lst_level)

            # Считаем среднее по субшкалам
            svod_mean_column_df = pd.pivot_table(base_df,
                                              index=[lst_svod_cols[idx]],
                                              values=['ЭО_Значение',
                                                      'СК_Значение',
                                                      'ЦН_Значение',
                                                      'РО_Значение',
                                                      'ПО_Значение',
                                                      'СУ_Значение'
                                                      ],
                                              aggfunc=round_mean_two)
            svod_mean_column_df.reset_index(inplace=True)

            # упорядочиваем колонки
            new_order_cols = [lst_svod_cols[idx]].copy()
            new_order_cols.extend((['ЭО_Значение', 'СК_Значение', 'ЦН_Значение',
                                    'РО_Значение', 'ПО_Значение', 'СУ_Значение'
                                    ]))
            svod_mean_column_df = svod_mean_column_df.reindex(columns=new_order_cols)

            dct_rename_cols_mean = {'ЭО_Значение': 'Ср. Эмоциональное отношение к КИ',
                                    'СК_Значение': 'Ср. Уровень самоконтроля',
                                    'ЦН_Значение': 'Ср. Целевая направленность',
                                    'РО_Значение': 'Ср. Родительского отношения',
                                    'ПО_Значение': 'Ср. Уровня предпочтения  общения с героями КИ',
                                    'СУ_Значение': 'Ср. Степень увлеченности',
                                    }
            svod_mean_column_df.rename(columns=dct_rename_cols_mean, inplace=True)
            # Готовим наименование
            name_column = lst_svod_cols[idx]
            name_column = re.sub(r'[\[\]\'+()<> :"?*|\\/]', '_', name_column)
            name_column = name_column[:15]
            out_dct.update({f'Ср {name_column}': svod_mean_column_df,
                            f'СУ {name_column}': svod_count_column_level_vcha_df,
                            })
        return out_dct





def processing_sumpki_gr(base_df: pd.DataFrame, answers_df: pd.DataFrame, lst_svod_cols:list):
    """
    Функция для обработки
    :param base_df: часть датафрейма с описательными колонками
    :param answers_df: часть датафрейма с ответами
    :param lst_svod_cols:  список с колонками по которым нужно делать свод
    """
    try:
        out_answer_df = base_df.copy()  # делаем копию для последующего соединения с сырыми ответами
        if len(answers_df.columns) != 22:  # проверяем количество колонок с вопросами
            raise BadCountColumnsSUMPKIG

        # очищаем названия колонок от возможных сочетаний .1 которые добавляет пандас при одинаковых колонках
        clean_df_lst = []
        for name_column in answers_df.columns:
            clean_name = re.sub(r'.\d+$', '', name_column)
            clean_df_lst.append(clean_name)

        answers_df.columns = clean_df_lst

        lst_check_cols = ['Играете ли вы в компьютерные игры?',
                          'Запрещают ли родители играть вам в компьютерные игры из-за того, что вы тратите на них слишком много времени?',
                          'Откладываете ли вы выполнение школьных домашних заданий, чтобы поиграть за компьютером?',
                          'Чувствуете ли вы себя раздраженным, если по каким-то причинам вам необходимо прекратить компьютерную игру?',
                          'Расстраиваетесь ли вы, если в течение дня вам не удается поиграть за компьютером?',
                          'Думаете ли вы о результатах, достигнутых в компьютерной игре?',
                          'Планируете ли вы повысить уровень своих результатов в игре?',
                          'Приходилось ли вам засиживаться за компьютерной игрой допоздна?',
                          'Чувствуете ли вы тягу к компьютерным играм?',
                          'Отказываетесь ли вы от общения с друзьями, чтобы поиграть за компьютером?',

                          'Случалось ли вам тратить на компьютерные игры деньги, которые были предназначены для других целей?',
                          'Приходилось ли вам играть за компьютером более 5 часов в день?',
                          'Предпочитаете ли вы компьютерную игру чтению интересной книги или просмотру фильма?',
                          'Играете ли вы с друзьями в компьютерные игры?',
                          'Замечаете ли вы, как летит время, пока вы играете в компьютерную игру',
                          'Как часто вы играли бы в компьютерные игры, если бы у вас была такая возможность?',
                          'Случалось ли вам скрывать от родителей, что вы играли за компьютером?',
                          'Используете ли вы компьютерную игру для того, чтобы уйти от проблем или от плохого настроения?',
                          'Обсуждаете ли вы результаты компьютерных игр с друзьями?',
                          'Злитесь ли вы, когда вас кто-то отвлекает от компьютерной игры?',
                          'Случалось ли вам уставать из-за того, что вы слишком долго играли за компьютером?',
                          'Стремитесь ли вы все свое свободное время играть за компьютером?',
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
            raise BadOrderSUMPKIG

        # словарь для замены слов на числа
        dct_replace_value = {'постоянно': 6,
                             'очень часто': 5,
                             'часто': 4,
                             'иногда': 3,
                             'редко': 2,
                             'никогда': 1,
                             }
        valid_values = [1, 2, 3, 4, 5, 6]
        answers_df.replace(dct_replace_value, inplace=True)  # заменяем слова на цифры для подсчетов
        # Проверяем, есть ли значения, отличающиеся от указанных в списке
        lst_error_answers = []  # список для хранения строк где найдены неправильные ответы

        for i in range(22):
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
            raise BadValueSUMPKIG

        base_df['ЭО_Значение'] = answers_df.apply(calc_value_em, axis=1)
        base_df['СК_Значение'] = answers_df.apply(calc_value_sk, axis=1)
        base_df['ЦН_Значение'] = answers_df.apply(calc_value_cn, axis=1)
        base_df['РО_Значение'] = answers_df.apply(calc_value_ro, axis=1)
        base_df['ПО_Значение'] = answers_df.apply(calc_value_po, axis=1)

        base_df['СУ_Значение'] = base_df[['ЭО_Значение','СК_Значение','ЦН_Значение','РО_Значение','ПО_Значение']].apply(calc_value,axis=1)
        base_df['СУ_Уровень'] = base_df['СУ_Значение'].apply(calc_level)

        # Создаем датафрейм для создания части в общий датафрейм
        part_df = pd.DataFrame()
        # Основные шкалы
        part_df['СУМПКИГ_ЭО_Значение'] = base_df['ЭО_Значение']
        part_df['СУМПКИГ_СК_Значение'] = base_df['СК_Значение']
        part_df['СУМПКИГ_ЦН_Значение'] = base_df['ЦН_Значение']
        part_df['СУМПКИГ_РО_Значение'] = base_df['РО_Значение']
        part_df['СУМПКИГ_ПО_Значение'] = base_df['ПО_Значение']

        part_df['СУМПКИГ_СУ_Значение'] = base_df['СУ_Значение']
        part_df['СУМПКИГ_СУ_Диапазон'] = base_df['СУ_Уровень']

        out_answer_df = pd.concat([out_answer_df, answers_df], axis=1)  # Датафрейм для проверки

        base_df.sort_values(by='СУ_Значение', ascending=False, inplace=True)  # сортируем

        # Делаем свод  по  шкалам
        dct_svod_sub = {'СУ_Значение': 'СУ_Уровень',
                        }

        dct_rename_svod_sub = {
            'СУ_Значение': 'Степень увлеченности КИ',
        }

        lst_sub = ['естественный уровень', 'средний уровень', 'зависимость']

        base_svod_sub_df = create_union_svod(base_df, dct_svod_sub, dct_rename_svod_sub, lst_sub)

        avg_vcha = round(base_df['ЭО_Значение'].mean(), 2)
        avg_o = round(base_df['СК_Значение'].mean(), 2)
        avg_ruvs = round(base_df['ЦН_Значение'].mean(), 2)
        avg_iika = round(base_df['РО_Значение'].mean(), 2)
        avg_np = round(base_df['ПО_Значение'].mean(), 2)

        avg_psp = round(base_df['СУ_Значение'].mean(), 2)

        avg_dct = {'Среднее значение Шкала уровня эмоционального отношения к компьютерным играм': avg_vcha,
                   'Среднее значение Шкала уровня самоконтроля в компьютерных играх,': avg_o,
                   'Среднее значение Шкала уровня целевой направленности на компьютерные игры': avg_ruvs,
                   'Среднее значение Шкала уровня родительского отношения к тому, что дети играют в КИ': avg_iika,
                   'Среднее значение Шкала уровня предпочтения общения с героями КИ реальному общению': avg_np,

                   'Среднее значение степени увлеченности КИ': avg_psp,
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

        dct_prefix = {'СУ_Уровень': 'СУ',
                      }

        out_dct = create_list_on_level_sumpki(base_df, out_dct, lst_sub, dct_prefix)

        """
                                Сохраняем в зависимости от необходимости делать своды по определенным колонкам
                                """
        if len(lst_svod_cols) == 0:
            return out_dct, part_df

        else:
            out_dct = create_result_sumpki_grish(base_df, out_dct, lst_svod_cols)
            return out_dct, part_df

    except BadOrderSUMPKIG:
        messagebox.showerror('Лахеcис',
                             f'При обработке вопросов теста Степень увлеченности младших подростков компьютерными играми Гришина обнаружены неправильные вопросы. Проверьте названия колонок с вопросами:\n'
                             f'{error_order_message[:5000]}\n'
                             f'Используйте при создании Яндекс-формы написание вопросов из руководства пользователя программы Лахесис.')
    except BadValueSUMPKIG:
        messagebox.showerror('Лахеcис',
                             f'При обработке вопросов теста Степень увлеченности младших подростков компьютерными играми Гришина обнаружены неправильные варианты ответов. Проверьте ответы на указанных строках:\n'
                             f'{error_message[:5000]}\n'
                             f'Используйте при создании Яндекс-формы написание вариантов ответа из руководства пользователя программы Лахесис.')


    except BadCountColumnsSUMPKIG:
        messagebox.showerror('Лахеcис',
                             f'Проверьте количество колонок с ответами на тест Степень увлеченности младших подростков компьютерными играми Гришина\n'
                             f'Должно быть 22 колонки с ответами')





