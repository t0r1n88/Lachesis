"""
Скрипт для обработки результатов Опросник социальных аксиом (ОСА-31) Татарко, Лебедева
"""

import pandas as pd
import re
from tkinter import messagebox
from lachesis_support_functions import round_mean_two,calc_count_scale,create_union_svod, create_list_on_level

class BadOrderOSATL(Exception):
    """
    Исключение для обработки случая когда колонки не совпадают
    """
    pass


class BadValueOSATL(Exception):
    """
    Исключение для неправильных значений в вариантах ответов
    """
    pass

class BadCountColumnsOSATL(Exception):
    """
    Исключение для обработки случая если количество колонок не равно 31
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
    else:
        return f'4-5'



def calc_value_sc(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [8, 9, 13, 15, 18, 22, 31]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_pr:
            value_forward += value
    return round(value_forward/len(lst_pr),2)


def calc_value_cs(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [2, 10, 12, 20, 25]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_pr:
            value_forward += value
    return round(value_forward/len(lst_pr),2)


def calc_value_r(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [3, 11, 17, 23, 30]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_pr:
            value_forward += value
    return round(value_forward/len(lst_pr),2)


def calc_value_nu(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [2, 19, 24, 28, 29, 6]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_pr:
            value_forward += value
    return round(value_forward/len(lst_pr),2)



def calc_value_ss(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [4,5,7,14,21,26,27]
    lst_neg = [16]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_pr:
            if idx not in lst_neg:
                value_forward += value
            else:
                if value == 1:
                    value_forward += 5
                elif value == 2:
                    value_forward += 4
                elif value == 3:
                    value_forward += 3
                elif value == 4:
                    value_forward += 2
                else:
                    value_forward += 1


    return round(value_forward/len(lst_pr),2)


def create_result_osa_tatarko(base_df:pd.DataFrame, out_dct:dict, lst_svod_cols:list):
    """
    Функция для подсчета результата если указаны колонки по которым нужно провести свод
    :param df: датафрейм с результатами
    :param out_dct: словарь с уже подсчитанными базовыми данными
    :param lst_svod_cols: список сводных колонок
    :return: словарь
    """

    lst_level = ['1-1.99', '2-2.99', '3-3.99', '4-5']

    lst_reindex_one_level_cols = lst_svod_cols.copy()
    lst_reindex_one_level_cols.extend(['1-1.99', '2-2.99', '3-3.99', '4-5',
                                       'Итого'])  # Основная шкала

    # АД
    svod_count_one_level_z_df = calc_count_scale(base_df, lst_svod_cols,
                                                 'СЦ_Значение',
                                                 'СЦ_Диапазон',
                                                 lst_reindex_one_level_cols, lst_level)

    # АД
    svod_count_one_level_mo_df = calc_count_scale(base_df, lst_svod_cols,
                                                  'КС_Значение',
                                                  'КС_Диапазон',
                                                  lst_reindex_one_level_cols, lst_level)

    # АД
    svod_count_one_level_t_df = calc_count_scale(base_df, lst_svod_cols,
                                                 'Р_Значение',
                                                 'Р_Диапазон',
                                                 lst_reindex_one_level_cols, lst_level)

    # АД
    svod_count_one_level_s_df = calc_count_scale(base_df, lst_svod_cols,
                                                 'НУ_Значение',
                                                 'НУ_Диапазон',
                                                 lst_reindex_one_level_cols, lst_level)

    # АД
    svod_count_one_level_k_df = calc_count_scale(base_df, lst_svod_cols,
                                                 'СС_Значение',
                                                 'СС_Диапазон',
                                                 lst_reindex_one_level_cols, lst_level)


    # Считаем среднее по субшкалам
    svod_mean_one_df = pd.pivot_table(base_df,
                                      index=lst_svod_cols,
                                      values=['СЦ_Значение',
                                              'КС_Значение',
                                              'Р_Значение',
                                              'НУ_Значение',

                                              'СС_Значение',
                                              ],
                                      aggfunc=round_mean_two)
    svod_mean_one_df.reset_index(inplace=True)

    # упорядочиваем колонки
    new_order_cols = lst_svod_cols.copy()
    new_order_cols.extend((['СЦ_Значение',
                            'КС_Значение',
                            'Р_Значение',
                            'НУ_Значение',

                            'СС_Значение',
                            ]))
    svod_mean_one_df = svod_mean_one_df.reindex(columns=new_order_cols)

    dct_rename_cols_mean = {'СЦ_Значение': 'Ср. Социальный цинизм',
                            'КС_Значение': 'Ср. Контроль судьбы',
                            'Р_Значение': 'Ср. Религиозность',
                            'НУ_Значение': 'Ср. Награда за усилия',

                            'СС_Значение': 'Ср. Социальная сложность',
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
                    f'СЦ {out_name}': svod_count_one_level_z_df,
                    f'КС {out_name}': svod_count_one_level_mo_df,
                    f'Р {out_name}': svod_count_one_level_t_df,
                    f'НУ {out_name}': svod_count_one_level_s_df,

                    f'СС {out_name}': svod_count_one_level_k_df,
                    })

    if len(lst_svod_cols) == 1:
        return out_dct
    else:
        for idx, name_column in enumerate(lst_svod_cols):

            lst_reindex_column_level_cols = [lst_svod_cols[idx], '1-1.99', '2-2.99', '3-3.99', '4-5',
                                             'Итого']

            # АД
            svod_count_column_level_z_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                            'СЦ_Значение',
                                                            'СЦ_Диапазон',
                                                            lst_reindex_column_level_cols, lst_level)

            # АД
            svod_count_column_level_mo_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                             'КС_Значение',
                                                             'КС_Диапазон',
                                                             lst_reindex_column_level_cols, lst_level)

            # АД
            svod_count_column_level_t_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                            'Р_Значение',
                                                            'Р_Диапазон',
                                                            lst_reindex_column_level_cols, lst_level)

            # АД
            svod_count_column_level_s_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                            'НУ_Значение',
                                                            'НУ_Диапазон',
                                                            lst_reindex_column_level_cols, lst_level)

            # АД
            svod_count_column_level_k_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                            'СС_Значение',
                                                            'СС_Диапазон',
                                                            lst_reindex_column_level_cols, lst_level)

            # Считаем среднее по субшкалам
            svod_mean_column_df = pd.pivot_table(base_df,
                                                 index=[lst_svod_cols[idx]],
                                                 values=['СЦ_Значение',
                                                         'КС_Значение',
                                                         'Р_Значение',
                                                         'НУ_Значение',

                                                         'СС_Значение',
                                                         ],
                                                 aggfunc=round_mean_two)
            svod_mean_column_df.reset_index(inplace=True)

            # упорядочиваем колонки
            new_order_cols = [lst_svod_cols[idx]].copy()
            new_order_cols.extend((['СЦ_Значение',
                                    'КС_Значение',
                                    'Р_Значение',
                                    'НУ_Значение',

                                    'СС_Значение',
                                    ]))
            svod_mean_column_df = svod_mean_column_df.reindex(columns=new_order_cols)

            dct_rename_cols_mean = {'СЦ_Значение': 'Ср. Социальный цинизм',
                                    'КС_Значение': 'Ср. Контроль судьбы',
                                    'Р_Значение': 'Ср. Религиозность',
                                    'НУ_Значение': 'Ср. Награда за усилия',

                                    'СС_Значение': 'Ср. Социальная сложность',
                                    }
            svod_mean_column_df.rename(columns=dct_rename_cols_mean, inplace=True)

            # Готовим наименование
            name_column = lst_svod_cols[idx]
            name_column = re.sub(r'[\[\]\'+()<> :"?*|\\/]', '_', name_column)
            name_column = name_column[:15]

            out_dct.update({f'Ср {name_column}': svod_mean_column_df,
                            f'СЦ {name_column}': svod_count_column_level_z_df,
                            f'КС {name_column}': svod_count_column_level_mo_df,
                            f'Р {name_column}': svod_count_column_level_t_df,
                            f'НУ {name_column}': svod_count_column_level_s_df,

                            f'СС {name_column}': svod_count_column_level_k_df,
                            })
        return out_dct





def processing_osa_tatarko(base_df: pd.DataFrame, answers_df: pd.DataFrame, lst_svod_cols:list):
    """
    Функция для обработки
    :param base_df: часть датафрейма с описательными колонками
    :param answers_df: часть датафрейма с ответами
    :param lst_svod_cols:  список с колонками по которым нужно делать свод
    """
    try:
        count_descr_cols = base_df.shape[1] # количество анкетных колонок

        out_answer_df = base_df.copy()  # делаем копию для последующего соединения с сырыми ответами
        if len(answers_df.columns) != 31:  # проверяем количество колонок с вопросами
            raise BadCountColumnsOSATL

        # очищаем названия колонок от возможных сочетаний .1 которые добавляет пандас при одинаковых колонках
        clean_df_lst = []
        for name_column in answers_df.columns:
            clean_name = re.sub(r'.\d+$', '', name_column)
            clean_df_lst.append(clean_name)

        answers_df.columns = clean_df_lst

        lst_check_cols = ['Человек достигнет успеха, если он действительно старается',
                          'Успех человека в жизни зависит от судьбы',
                          'Религиозная вера помогает людям сделать правильный выбор в сложной жизненной ситуации',
                          'Поведение человека может противоречить его истинным чувствам',
                          'Поведение человека меняется в зависимости от социальных условий',
                          'Можно добиться успеха, идя к нему шаг за шагом',
                          'Люди внезапно могут потерять все, что имеют',
                          'Богатые люди становятся богаче, бедные люди становятся беднее',
                          'Занятие общественными делами приносит только проблемы',
                          'У людей нет способа улучшить свою судьбу',

                          'Религиозная вера способствует душевному здоровью',
                          'Люди, которых человек будет любить в своей жизни, предопределены судьбой',
                          'Различные социальные институты в обществе расположены к богатым',
                          'Каждый человек уникален',
                          'Власть и статус делают людей надменными',
                          'Многие вещи кажутся намного более сложными, чем они есть на самом деле',
                          'Религия делает людей более здоровыми',
                          'Люди, становясь богатыми и успешными, забывают тех, кто помогал им в жизни',
                          'Трудности можно преодолеть усердной работой и упорством',
                          'Все во Вселенной предопределено',

                          'Сильно отличающиеся мнения могут быть оба правильными',
                          'Возможность обогащения порождает у людей нечестность',
                          'Религия делает людей счастливее',
                          'Усердно работающие люди в итоге достигнут большего',
                          'Успехи и неудачи человека обусловлены судьбой',
                          'Для достижения цели важно видение разных путей к ней',
                          'В разных ситуациях люди могут вести себя абсолютно по-разному',
                          'Выносливость и решительность — ключ к достижению целей',
                          'Трудолюбивые люди хорошо вознаграждаются',
                          'Религия помогает людям делать правильный выбор в жизни',

                          'Люди с деньгами правят миром'
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
            raise BadOrderOSATL

        # словарь для замены слов на числа
        dct_replace_value = {'абсолютно не согласен': 1,
                             'не согласен': 2,
                             'не знаю': 3,
                             'согласен': 4,
                             'абсолютно согласен': 5,
                             }
        valid_values = [1,2,3,4,5]
        answers_df.replace(dct_replace_value, inplace=True)  # заменяем слова на цифры для подсчетов
        # Проверяем, есть ли значения, отличающиеся от указанных в списке
        lst_error_answers = []  # список для хранения строк где найдены неправильные ответы

        for i in range(31):
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
            raise BadValueOSATL

        base_df['СЦ_Значение'] = answers_df.apply(calc_value_sc, axis=1)
        base_df['СЦ_Диапазон'] = base_df['СЦ_Значение'].apply(calc_level)

        base_df['КС_Значение'] = answers_df.apply(calc_value_cs, axis=1)
        base_df['КС_Диапазон'] = base_df['КС_Значение'].apply(calc_level)

        base_df['Р_Значение'] = answers_df.apply(calc_value_r, axis=1)
        base_df['Р_Диапазон'] = base_df['Р_Значение'].apply(calc_level)

        base_df['НУ_Значение'] = answers_df.apply(calc_value_nu, axis=1)
        base_df['НУ_Диапазон'] = base_df['НУ_Значение'].apply(calc_level)

        base_df['СС_Значение'] = answers_df.apply(calc_value_ss, axis=1)
        base_df['СС_Диапазон'] = base_df['СС_Значение'].apply(calc_level)

        # Создаем датафрейм для создания части в общий датафрейм
        temp_df = base_df.copy()  # делаем копию
        part_df = temp_df.iloc[:, count_descr_cols:]
        part_df = part_df.add_prefix('ОСАТЛ_')

        out_answer_df = pd.concat([out_answer_df, answers_df], axis=1)  # Датафрейм для проверки

        base_df.sort_values(by='СЦ_Значение', ascending=False, inplace=True)  # сортируем

        # Делаем свод  по  шкалам
        dct_svod_sub = {'СЦ_Значение': 'СЦ_Диапазон',
                        'КС_Значение': 'КС_Диапазон',
                        'Р_Значение': 'Р_Диапазон',
                        'НУ_Значение': 'НУ_Диапазон',

                        'СС_Значение': 'СС_Диапазон',

                        }

        dct_rename_svod_sub = {'СЦ_Значение': 'Социальный цинизм',
                               'КС_Значение': 'Контроль судьбы',
                               'Р_Значение': 'Религиозность',
                               'НУ_Значение': 'Награда за усилия',

                               'СС_Значение': 'Социальная сложность',
                               }

        lst_sub = ['1-1.99', '2-2.99', '3-3.99', '4-5']

        base_svod_sub_df = create_union_svod(base_df, dct_svod_sub, dct_rename_svod_sub, lst_sub)

        avg_z = round(base_df['СЦ_Значение'].mean(), 2)
        avg_mo = round(base_df['КС_Значение'].mean(), 2)
        avg_t = round(base_df['Р_Значение'].mean(), 2)
        avg_s = round(base_df['НУ_Значение'].mean(), 2)

        avg_k = round(base_df['СС_Значение'].mean(), 2)

        avg_dct = {'Среднее значение шкалы Социальный цинизм': avg_z,
                   'Среднее значение шкалы Контроль судьбы': avg_mo,
                   'Среднее значение шкалы Религиозность': avg_t,
                   'Среднее значение шкалы Награда за усилия': avg_s,

                   'Среднее значение шкалы Социальная сложность': avg_k,
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
            'СЦ_Диапазон': 'СЦ',
            'КС_Диапазон': 'КС',
            'Р_Диапазон': 'Р',
            'НУ_Диапазон': 'НУ',

            'СС_Диапазон': 'СС',
        }

        out_dct = create_list_on_level(base_df, out_dct, lst_sub, dct_prefix)

        """
                        Сохраняем в зависимости от необходимости делать своды по определенным колонкам
                        """
        if len(lst_svod_cols) == 0:
            return out_dct, part_df

        else:
            out_dct = create_result_osa_tatarko(base_df, out_dct, lst_svod_cols)
            return out_dct, part_df



    except BadOrderOSATL:
        messagebox.showerror('Лахеcис',
                             f'При обработке вопросов теста Опросник социальных аксиом (ОСА-31) Татарко, Лебедева обнаружены неправильные вопросы. Проверьте названия колонок с вопросами:\n'
                             f'{error_order_message[:5000]}\n'
                             f'Используйте при создании Яндекс-формы написание вопросов из руководства пользователя программы Лахесис.')
    except BadValueOSATL:
        messagebox.showerror('Лахеcис',
                             f'При обработке вопросов теста Опросник социальных аксиом (ОСА-31) Татарко, Лебедева обнаружены неправильные варианты ответов. Проверьте ответы на указанных строках:\n'
                             f'{error_message[:5000]}\n'
                             f'Используйте при создании Яндекс-формы написание вариантов ответа из руководства пользователя программы Лахесис.')


    except BadCountColumnsOSATL:
        messagebox.showerror('Лахеcис',
                             f'Проверьте количество колонок с ответами на тест Опросник социальных аксиом (ОСА-31) Татарко, Лебедева\n'
                             f'Должно быть 31 колонка с ответами')





