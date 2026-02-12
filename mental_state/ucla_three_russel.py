"""
Скрипт для обработки результатов теста Шкала одиночества UCLA версия 3 Рассел Адаптация Ишмухаметов
"""

import pandas as pd
import re
from tkinter import messagebox
from lachesis_support_functions import round_mean_two,calc_count_scale,create_list_on_level,create_union_svod


class BadOrderUCLATI(Exception):
    """
    Исключение для обработки случая когда колонки не совпадают
    """
    pass


class BadValueUCLATI(Exception):
    """
    Исключение для неправильных значений в вариантах ответов
    """
    pass

class BadCountColumnsUCLATI(Exception):
    """
    Исключение для обработки случая если количество колонок не равно 20
    """
    pass


def calc_value_ucla_three(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [1,5,6,9,10,15,16,19,20]
    value_forward = 0  # результат
    for idx, value in enumerate(row):
        if idx +1 in lst_pr:
            if value == 4:
                value_forward += 1
            elif value == 3:
                value_forward += 2
            elif value == 2:
                value_forward += 3
            else:
                value_forward += 4
        else:
            value_forward += value

    return value_forward


def calc_level(value):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """
    if 20 <=value <= 34:
        return f'20-34'
    elif 35 <= value <= 49:
        return f'35-49'
    elif 50 <= value <= 64:
        return f'50-64'
    else:
        return f'65-80'



def create_list_on_level_ucla_three(base_df:pd.DataFrame, out_dct:dict, lst_level:list, dct_prefix:dict):
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


def create_result_ucla_three(base_df:pd.DataFrame, out_dct:dict, lst_svod_cols:list):
    """
    Функция для подсчета результата если указаны колонки по которым нужно провести свод
    :param df: датафрейм с результатами
    :param out_dct: словарь с уже подсчитанными базовыми данными
    :param lst_svod_cols: список сводных колонок
    :return: словарь
    """
    lst_level = ['20-34', '35-49', '50-64', '65-80']

    lst_reindex_one_level_cols = lst_svod_cols.copy()
    lst_reindex_one_level_cols.extend(['20-34', '35-49', '50-64', '65-80',
                                       'Итого'])  # Основная шкала

    svod_count_one_level_ucla_three_df = calc_count_scale(base_df, lst_svod_cols,
                                                   'ШО_Значение',
                                                   'ШО_Диапазон',
                                                   lst_reindex_one_level_cols, lst_level)

    # Считаем среднее по субшкалам
    svod_mean_one_df = pd.pivot_table(base_df,
                                      index=lst_svod_cols,
                                      values=['ШО_Значение',
                                              ],
                                      aggfunc=round_mean_two)
    svod_mean_one_df.reset_index(inplace=True)

    # упорядочиваем колонки
    new_order_cols = lst_svod_cols.copy()
    new_order_cols.extend((['ШО_Значение']))
    svod_mean_one_df = svod_mean_one_df.reindex(columns=new_order_cols)

    dct_rename_cols_mean = {'ШО_Значение': 'Среднее Шкала одиночества',
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
                    f'ШО {out_name}': svod_count_one_level_ucla_three_df,
                    })

    if len(lst_svod_cols) == 1:
        return out_dct

    else:
        for idx, name_column in enumerate(lst_svod_cols):
            lst_reindex_column_level_cols = [lst_svod_cols[idx],'20-34', '35-49', '50-64', '65-80',
                                                  'Итого']

            svod_count_column_level_ucla_three_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                               'ШО_Значение',
                                                               'ШО_Диапазон',
                                                               lst_reindex_column_level_cols, lst_level)

            # Считаем среднее по субшкалам
            svod_mean_column_df = pd.pivot_table(base_df,
                                              index=[lst_svod_cols[idx]],
                                              values=['ШО_Значение',
                                                      ],
                                              aggfunc=round_mean_two)
            svod_mean_column_df.reset_index(inplace=True)

            # упорядочиваем колонки
            new_order_cols = [lst_svod_cols[idx]].copy()
            new_order_cols.extend((['ШО_Значение']))
            svod_mean_column_df = svod_mean_column_df.reindex(columns=new_order_cols)

            dct_rename_cols_mean = {'ШО_Значение': 'Среднее Шкала одиночества',
                                    }
            svod_mean_column_df.rename(columns=dct_rename_cols_mean, inplace=True)
            # Готовим наименование
            name_column = lst_svod_cols[idx]
            name_column = re.sub(r'[\[\]\'+()<> :"?*|\\/]', '_', name_column)
            name_column = name_column[:15]
            out_dct.update({f'Ср {name_column}': svod_mean_column_df,
                            f'ШО {name_column}': svod_count_column_level_ucla_three_df,
                            })
        return out_dct








def processing_ucla_three_ish(base_df: pd.DataFrame, answers_df: pd.DataFrame, lst_svod_cols:list):
    """
    Функция для обработки
    :param base_df: часть датафрейма с описательными колонками
    :param answers_df: часть датафрейма с ответами
    :param lst_svod_cols:  список с колонками по которым нужно делать свод
    """
    try:
        out_answer_df = base_df.copy()  # делаем копию для последующего соединения с сырыми ответами
        if len(answers_df.columns) != 20:  # проверяем количество колонок с вопросами
            raise BadCountColumnsUCLATI

        # очищаем названия колонок от возможных сочетаний .1 которые добавляет пандас при одинаковых колонках
        clean_df_lst = []
        for name_column in answers_df.columns:
            clean_name = re.sub(r'.\d+$', '', name_column)
            clean_df_lst.append(clean_name)

        answers_df.columns = clean_df_lst

        lst_check_cols = ['Как часто Вы чувствуете себя "на одной волне" с окружающими людьми?',
                          'Как часто Вы чувствуете недостаток в дружеском общении?',
                          'Как часто Вы чувствуете, что нет никого, к кому можно обратиться?',
                          'Как часто Вы чувствуете себя одиноким?',
                          'Как часто Вы чувствуете себя частью группы друзей?',
                          'Как часто Вы чувствуете, что у Вас есть много общего с окружающими людьми?',
                          'Как часто Вы чувствуете, что Вы больше не испытываете близости к кому-либо?',
                          'Как часто Вы чувствуете, что окружающие Вас люди не разделяют Ваших интересов и идей?',
                          'Как часто Вы чувствуете себя открытым для общения и дружелюбным?',
                          'Как часто Вы чувствуете близость, единение с другими людьми?',

                          'Как часто Вы чувствуете себя покинутым?',
                          'Как часто Вы чувствуете, что Ваши отношения с другими поверхностны?',
                          'Как часто Вы чувствуете, что Вас никто не знает по-настоящему?',
                          'Как часто Вы чувствуете себя изолированным от других?',
                          'Как часто Вы чувствуете, что можете найти себе компанию, если Вы этого захотите?',
                          'Как часто Вы чувствуете, что есть люди, которые Вас действительно понимают?',
                          'Как часто Вы чувствуете стеснительность?',
                          'Как часто Вы чувствуете, что есть люди вокруг Вас, но не с Вами?',
                          'Как часто Вы чувствуете, что есть люди, с которыми Вы можете поговорить?',
                          'Как часто Вы чувствуете, что есть люди, к которым Вы можете обратиться?',
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
            raise BadOrderUCLATI

        # словарь для замены слов на числа
        dct_replace_value = {'часто': 4,
                             'иногда': 3,
                             'редко': 2,
                             'никогда': 1,
                             }
        valid_values = [1, 2, 3, 4]
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
            raise BadValueUCLATI

        base_df['ШО_Значение'] = answers_df.apply(calc_value_ucla_three, axis=1)
        base_df['ШО_Диапазон'] = base_df['ШО_Значение'].apply(calc_level)

        # Создаем датафрейм для создания части в общий датафрейм
        part_df = pd.DataFrame()
        part_df['ШО_3_И_Значение'] = base_df['ШО_Значение']
        part_df['ШО_3_И_Диапазон'] = base_df['ШО_Диапазон']

        out_answer_df = pd.concat([out_answer_df, answers_df], axis=1)  # Датафрейм для проверки
        base_df.sort_values(by='ШО_Значение', ascending=False, inplace=True)  # сортируем

        # Делаем свод  по  шкалам
        dct_svod_sub = {'ШО_Значение': 'ШО_Диапазон',
                        }

        dct_rename_svod_sub = {'ШО_Значение': 'Шкала одиночества',
                               }

        lst_sub = ['20-34', '35-49', '50-64', '65-80']
        base_svod_sub_df = create_union_svod(base_df, dct_svod_sub, dct_rename_svod_sub, lst_sub)

        # считаем среднее значение по шкалам
        avg_sho = round(base_df['ШО_Значение'].mean(), 2)

        avg_dct = {'Среднее значение шкалы одиночества': avg_sho,
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

        dct_prefix = {'ШО_Диапазон': 'ШО',
                      }

        out_dct = create_list_on_level_ucla_three(base_df, out_dct, lst_sub, dct_prefix)

        """
                        Сохраняем в зависимости от необходимости делать своды по определенным колонкам
                        """
        if len(lst_svod_cols) == 0:
            return out_dct, part_df

        else:
            out_dct = create_result_ucla_three(base_df, out_dct, lst_svod_cols)
            return out_dct, part_df
    except BadOrderUCLATI:
        messagebox.showerror('Лахеcис',
                             f'При обработке вопросов теста Шкала одиночества UCLA-3 Рассел Ишмухаметов обнаружены неправильные вопросы. Проверьте названия колонок с вопросами:\n'
                             f'{error_order_message[:5000]}\n'
                             f'Используйте при создании Яндекс-формы написание вопросов из руководства пользователя программы Лахесис.')
    except BadValueUCLATI:
        messagebox.showerror('Лахеcис',
                             f'При обработке вопросов теста Шкала одиночества UCLA-3 Рассел Ишмухаметов обнаружены неправильные варианты ответов. Проверьте ответы на указанных строках:\n'
                             f'{error_message[:5000]}\n'
                             f'Используйте при создании Яндекс-формы написание вариантов ответа из руководства пользователя программы Лахесис.')


    except BadCountColumnsUCLATI:
        messagebox.showerror('Лахеcис',
                             f'Проверьте количество колонок с ответами на тест Шкала одиночества UCLA-3 Рассел Ишмухаметов\n'
                             f'Должно быть 20 колонок с ответами')














