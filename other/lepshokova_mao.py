"""
Скрипт для обработки результатов Адаптированная и модифицированная методика аккультурационных ожиданий Берри Лепшокова Татарко
"""

import pandas as pd
import re
from tkinter import messagebox
from lachesis_support_functions import round_mean_two,calc_count_scale,create_union_svod,create_list_on_level

class BadOrderMAOLT(Exception):
    """
    Исключение для обработки случая когда колонки не совпадают
    """
    pass


class BadValueMAOLT(Exception):
    """
    Исключение для неправильных значений в вариантах ответов
    """
    pass

class BadCountColumnsMAOLT(Exception):
    """
    Исключение для обработки случая если количество колонок не равно 27
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
        return f'3- 3.99'
    else:
        return f'4-5'


def calc_value_i(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [5, 11, 12, 16, 20, 23, 27]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_pr:
            value_forward += value


    return round(value_forward / len(lst_pr),2)


def calc_value_a(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [3, 6, 7, 8, 17, 18, 21]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_pr:
            value_forward += value


    return round(value_forward / len(lst_pr),2)


def calc_value_s(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [2, 10, 13, 14, 19, 24]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_pr:
            value_forward += value


    return round(value_forward / len(lst_pr),2)

def calc_value_isk(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [1, 4, 9, 15, 22, 25, 26]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_pr:
            value_forward += value


    return round(value_forward / len(lst_pr),2)

def create_result_mao_lepshokova(base_df:pd.DataFrame, out_dct:dict, lst_svod_cols:list):
    """
    Функция для подсчета результата если указаны колонки по которым нужно провести свод
    :param df: датафрейм с результатами
    :param out_dct: словарь с уже подсчитанными базовыми данными
    :param lst_svod_cols: список сводных колонок
    :return: словарь
    """

    lst_level = ['1-1.99', '2-2.99', '3- 3.99', '4-5']

    lst_reindex_one_level_cols = lst_svod_cols.copy()
    lst_reindex_one_level_cols.extend(['1-1.99', '2-2.99', '3- 3.99', '4-5',
                                       'Итого'])  # Основная шкала

    # АД
    svod_count_one_level_z_df = calc_count_scale(base_df, lst_svod_cols,
                                                 'И_Значение',
                                                 'И_Диапазон',
                                                 lst_reindex_one_level_cols, lst_level)

    # АД
    svod_count_one_level_mo_df = calc_count_scale(base_df, lst_svod_cols,
                                                 'А_Значение',
                                                 'А_Диапазон',
                                                 lst_reindex_one_level_cols, lst_level)

    # АД
    svod_count_one_level_t_df = calc_count_scale(base_df, lst_svod_cols,
                                                 'С_Значение',
                                                 'С_Диапазон',
                                                 lst_reindex_one_level_cols, lst_level)

    # АД
    svod_count_one_level_s_df = calc_count_scale(base_df, lst_svod_cols,
                                                 'Иск_Значение',
                                                 'Иск_Диапазон',
                                                 lst_reindex_one_level_cols, lst_level)


    # Считаем среднее по субшкалам
    svod_mean_one_df = pd.pivot_table(base_df,
                                      index=lst_svod_cols,
                                      values=['И_Значение',
                                              'А_Значение',
                                              'С_Значение',
                                              'Иск_Значение',
                                              ],
                                      aggfunc=round_mean_two)
    svod_mean_one_df.reset_index(inplace=True)

    # упорядочиваем колонки
    new_order_cols = lst_svod_cols.copy()
    new_order_cols.extend((['И_Значение',
                            'А_Значение',
                            'С_Значение',
                            'Иск_Значение',
                            ]))
    svod_mean_one_df = svod_mean_one_df.reindex(columns=new_order_cols)

    dct_rename_cols_mean = {'И_Значение': 'Ср. Интеграция (мультикультурализм)',
                            'А_Значение': 'Ср. Ассимиляция (плавильный котел)',
                            'С_Значение': 'Ср. Сегрегация',
                            'Иск_Значение': 'Ср. Исключение',
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
                    f'И {out_name}': svod_count_one_level_z_df,
                    f'А {out_name}': svod_count_one_level_mo_df,
                    f'С {out_name}': svod_count_one_level_t_df,
                    f'Иск {out_name}': svod_count_one_level_s_df,
                    })

    if len(lst_svod_cols) == 1:
        return out_dct
    else:
        for idx, name_column in enumerate(lst_svod_cols):

            lst_reindex_column_level_cols = [lst_svod_cols[idx], '1-1.99', '2-2.99', '3- 3.99', '4-5',
                                             'Итого']

            # АД
            svod_count_column_level_z_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                            'И_Значение',
                                                            'И_Диапазон',
                                                            lst_reindex_column_level_cols, lst_level)

            # АД
            svod_count_column_level_mo_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                             'А_Значение',
                                                             'А_Диапазон',
                                                             lst_reindex_column_level_cols, lst_level)

            # АД
            svod_count_column_level_t_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                            'С_Значение',
                                                            'С_Диапазон',
                                                            lst_reindex_column_level_cols, lst_level)

            # АД
            svod_count_column_level_s_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                            'Иск_Значение',
                                                            'Иск_Диапазон',
                                                            lst_reindex_column_level_cols, lst_level)

            # Считаем среднее по субшкалам
            svod_mean_column_df = pd.pivot_table(base_df,
                                                 index=[lst_svod_cols[idx]],
                                                 values=['И_Значение',
                                                         'А_Значение',
                                                         'С_Значение',
                                                         'Иск_Значение',
                                                         ],
                                                 aggfunc=round_mean_two)
            svod_mean_column_df.reset_index(inplace=True)

            # упорядочиваем колонки
            new_order_cols = [lst_svod_cols[idx]].copy()
            new_order_cols.extend((['И_Значение',
                                    'А_Значение',
                                    'С_Значение',
                                    'Иск_Значение',
                                    ]))
            svod_mean_column_df = svod_mean_column_df.reindex(columns=new_order_cols)

            dct_rename_cols_mean = {'И_Значение': 'Ср. Интеграция (мультикультурализм)',
                                    'А_Значение': 'Ср. Ассимиляция (плавильный котел)',
                                    'С_Значение': 'Ср. Сегрегация',
                                    'Иск_Значение': 'Ср. Исключение',
                                    }
            svod_mean_column_df.rename(columns=dct_rename_cols_mean, inplace=True)

            # Готовим наименование
            name_column = lst_svod_cols[idx]
            name_column = re.sub(r'[\[\]\'+()<> :"?*|\\/]', '_', name_column)
            name_column = name_column[:15]

            out_dct.update({f'Ср {name_column}': svod_mean_column_df,
                            f'И {name_column}': svod_count_column_level_z_df,
                            f'А {name_column}': svod_count_column_level_mo_df,
                            f'С {name_column}': svod_count_column_level_t_df,
                            f'Иск {name_column}': svod_count_column_level_s_df,
                            })
        return out_dct









def processing_mao_lepsh(base_df: pd.DataFrame, answers_df: pd.DataFrame, lst_svod_cols:list):
    """
    Функция для обработки
    :param base_df: часть датафрейма с описательными колонками
    :param answers_df: часть датафрейма с ответами
    :param lst_svod_cols:  список с колонками по которым нужно делать свод
    """
    try:
        count_descr_cols = base_df.shape[1] # количество анкетных колонок

        out_answer_df = base_df.copy()  # делаем копию для последующего соединения с сырыми ответами
        if len(answers_df.columns) != 27:  # проверяем количество колонок с вопросами
            raise BadCountColumnsMAOLT

        # очищаем названия колонок от возможных сочетаний .1 которые добавляет пандас при одинаковых колонках
        clean_df_lst = []
        for name_column in answers_df.columns:
            clean_name = re.sub(r'.\d+$', '', name_column)
            clean_df_lst.append(clean_name)

        answers_df.columns = clean_df_lst

        lst_check_cols = ['Мигрантам не следует участвовать в деятельности как российских организаций, так и своих этнических групп',
                          'Мигрантам следует участвовать только в тех видах деятельности, где участвуют члены их этнической группы',
                          'Мигрантам следует участвовать в тех видах деятельности, где участвуют только русские',
                          'Я считаю, что мигрантам не важно как поддерживать свои культурные традиции, так и усваивать русские',
                          'Я считаю, что мигранты должны как сохранять свои культурные традиции, так и осваивать русские',
                          'Я считаю, что мигранты должны осваивать русские культурные традиции и не поддерживать собственные',
                          'Мигрантам следует дружить только с россиянами',
                          'Мигрантам важнее владеть в совершенстве русским языком, чем родным',
                          'Мигрантам не следует дружить ни с людьми своей национальности, ни с русскими',
                          'Мигранты должны иметь друзей только своей национальности',

                          'Мигрантам следует участвовать в тех видах деятельности, где участвуют и россияне, и представители их этнической групп',
                          'Мигрантам следует иметь друзей и своей национальности, и русских',
                          'Мигрантам лучше заключать браки только с представителями своего народа и не заключать их с русскими',
                          'Я считаю, что мигранты должны работать там, где работают представители их этнической группы, а не работать там, где работают русские',
                          'Мигрантам здесь не следует заключать браки ни с русскими, ни с представителями своего народа',
                          'Лучше всего если мигранты будут жить среди русских, соблюдая нормы поведения, принятые в русской культуре, но при этом сохраняя нормы поведения, принятые и в их культуре',
                          'Мигрантам следует здесь жить среди русских в соответствии нормами поведения русской культуры, а не в этнических районах',
                          'Лучше, если мигранты будут работать здесь среди русских, а не среди представителей своей этнической группы',
                          'Я считаю, что мигранты должны учить своих детей в специальных национальных школах для мигрантов, а не в школах, где обучаются русские дети',
                          'Я считаю, что мигранты здесь могут заключать браки, как с русскими, так и с представителями своего народа',

                          'Мигрантам лучше заключать браки с русскими, чем с представителями своего народа',
                          'Я считаю, что мигрантам здесь не следует учить своих детей, ни в российских общеобразовательных школах, ни в национальных',
                          'Лучше всего, если мигранты будут учить своих детей в общеобразовательных школах в поликультурных классах, в которых учатся как русские, так и дети мигрантов',
                          'Мигрантам следует жить в этнических районах в соответствии со своими культурными нормами поведения, а не среди русских',
                          'Я считаю, что мигрантам здесь вообще не следует работать — ни среди русских, ни среди представителей своего народа',
                          'Я считаю, что мигрантам вообще не следует жить здесь — ни в этнических районах, ни среди русских',
                          'Лучше, если будут образовываться смешанные трудовые коллективы, в которых работают и русские и мигранты',
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
            raise BadOrderMAOLT

        # словарь для замены слов на числа
        dct_replace_value = {'абсолютно не согласен': 1,
                             'скорее не согласен': 2,
                             'не знаю, не уверен': 3,
                             'согласен': 4,
                             'абсолютно согласен': 5,
                             }
        valid_values = [1,2,3,4,5]
        answers_df.replace(dct_replace_value, inplace=True)  # заменяем слова на цифры для подсчетов
        # Проверяем, есть ли значения, отличающиеся от указанных в списке
        lst_error_answers = []  # список для хранения строк где найдены неправильные ответы

        for i in range(27):
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
            raise BadValueMAOLT

        base_df['И_Значение'] = answers_df.apply(calc_value_i, axis=1)
        base_df['И_Диапазон'] = base_df['И_Значение'].apply(calc_level)

        base_df['А_Значение'] = answers_df.apply(calc_value_a, axis=1)
        base_df['А_Диапазон'] = base_df['А_Значение'].apply(calc_level)

        base_df['С_Значение'] = answers_df.apply(calc_value_s, axis=1)
        base_df['С_Диапазон'] = base_df['С_Значение'].apply(calc_level)

        base_df['Иск_Значение'] = answers_df.apply(calc_value_isk, axis=1)
        base_df['Иск_Диапазон'] = base_df['Иск_Значение'].apply(calc_level)

        # Создаем датафрейм для создания части в общий датафрейм
        temp_df = base_df.copy()  # делаем копию
        part_df = temp_df.iloc[:, count_descr_cols:]
        part_df = part_df.add_prefix('МАОЛТ_')

        out_answer_df = pd.concat([out_answer_df, answers_df], axis=1)  # Датафрейм для проверки

        base_df.sort_values(by='Иск_Значение', ascending=False, inplace=True)  # сортируем

        # Делаем свод  по  шкалам
        dct_svod_sub = {'И_Значение': 'И_Диапазон',
                        'А_Значение': 'А_Диапазон',
                        'С_Значение': 'С_Диапазон',
                        'Иск_Значение': 'Иск_Диапазон',


                        }

        dct_rename_svod_sub = {'И_Значение': 'Интеграция (мультикультурализм)',
                               'А_Значение': 'Ассимиляция (плавильный котел)',
                               'С_Значение': 'Сегрегация',
                               'Иск_Значение': 'Исключение',

                               }

        lst_sub = ['1-1.99', '2-2.99', '3- 3.99', '4-5']

        base_svod_sub_df = create_union_svod(base_df, dct_svod_sub, dct_rename_svod_sub, lst_sub)

        avg_z = round(base_df['И_Значение'].mean(), 2)
        avg_mo = round(base_df['А_Значение'].mean(), 2)
        avg_t = round(base_df['С_Значение'].mean(), 2)
        avg_s = round(base_df['Иск_Значение'].mean(), 2)


        avg_dct = {'Среднее значение шкалы Интеграция (мультикультурализм)': avg_z,
                   'Среднее значение шкалы Ассимиляция (плавильный котел)': avg_mo,
                   'Среднее значение шкалы Сегрегация': avg_t,
                   'Среднее значение шкалы Исключение': avg_s,
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
            'И_Диапазон': 'И',
            'А_Диапазон': 'А',
            'С_Диапазон': 'С',
            'Иск_Диапазон': 'Иск',

        }

        out_dct = create_list_on_level(base_df, out_dct, lst_sub, dct_prefix)

        """
                        Сохраняем в зависимости от необходимости делать своды по определенным колонкам
                        """
        if len(lst_svod_cols) == 0:
            return out_dct, part_df

        else:
            out_dct = create_result_mao_lepshokova(base_df, out_dct, lst_svod_cols)
            return out_dct, part_df



    except BadOrderMAOLT:
        messagebox.showerror('Лахеcис',
                             f'При обработке вопросов теста Методика аккультурационных ожиданий Берри Лепшокова Татарко обнаружены неправильные вопросы. Проверьте названия колонок с вопросами:\n'
                             f'{error_order_message[:5000]}\n'
                             f'Используйте при создании Яндекс-формы написание вопросов из руководства пользователя программы Лахесис.')
    except BadValueMAOLT:
        messagebox.showerror('Лахеcис',
                             f'При обработке вопросов теста Методика аккультурационных ожиданий Берри Лепшокова Татарко обнаружены неправильные варианты ответов. Проверьте ответы на указанных строках:\n'
                             f'{error_message[:5000]}\n'
                             f'Используйте при создании Яндекс-формы написание вариантов ответа из руководства пользователя программы Лахесис.')


    except BadCountColumnsMAOLT:
        messagebox.showerror('Лахеcис',
                             f'Проверьте количество колонок с ответами на тест Методика аккультурационных ожиданий Берри Лепшокова Татарко\n'
                             f'Должно быть 27 колонок с ответами')