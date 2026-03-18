"""
Скрипт для обработки результатов Шкала душевной боли, PAS-13 Холден Колачев Чистопольская и др.
"""

import pandas as pd
import re
from tkinter import messagebox
from lachesis_support_functions import round_mean_two,calc_count_scale,create_union_svod, create_list_on_level

class BadOrderPASKCH(Exception):
    """
    Исключение для обработки случая когда колонки не совпадают
    """
    pass


class BadValuePASKCH(Exception):
    """
    Исключение для неправильных значений в вариантах ответов
    """
    pass

class BadCountColumnsPASKCH(Exception):
    """
    Исключение для обработки случая если количество колонок не равно 13
    """
    pass

def calc_level(value):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """
    if 13<= value <= 28:
        return f'низкий ШДБ'
    elif 29 <= value <= 42:
        return f'умеренный ШДБ'
    elif 43 <= value <= 55:
        return f'повышенный ШДБ'
    else:
        return f'высокий ШДБ'



def create_list_on_level_pas(base_df:pd.DataFrame, out_dct:dict, lst_level:list, dct_prefix:dict):
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
                if level == 'низкий ШДБ':
                    level = 'низкий'
                elif level == 'умеренный ШДБ':
                    level = 'умеренный'
                elif level == 'повышенный ШДБ':
                    level = 'повышенный'
                else:
                    level = 'высокий'
                dct_level[f'{dct_prefix[key]}. {level}'] = temp_df
        out_dct.update(dct_level)

    return out_dct


def create_result_pas_kol_chist(base_df:pd.DataFrame, out_dct:dict, lst_svod_cols:list):
    """
    Функция для подсчета результата если указаны колонки по которым нужно провести свод
    :param df: датафрейм с результатами
    :param out_dct: словарь с уже подсчитанными базовыми данными
    :param lst_svod_cols: список сводных колонок
    :return: словарь
    """
    lst_level = ['низкий ШДБ', 'умеренный ШДБ', 'повышенный ШДБ', 'высокий ШДБ']

    lst_reindex_one_level_cols = lst_svod_cols.copy()
    lst_reindex_one_level_cols.extend(['низкий ШДБ', 'умеренный ШДБ', 'повышенный ШДБ', 'высокий ШДБ',
                                       'Итого'])  # Основная шкала
    svod_count_one_level_vcha_df = calc_count_scale(base_df, lst_svod_cols,
                                                    'ШДБ_Значение',
                                                    'ШДБ_Уровень',
                                                    lst_reindex_one_level_cols, lst_level)

    # Считаем среднее по субшкалам
    svod_mean_one_df = pd.pivot_table(base_df,
                                      index=lst_svod_cols,
                                      values=[
                                              'ШДБ_Значение',
                                              ],
                                      aggfunc=round_mean_two)
    svod_mean_one_df.reset_index(inplace=True)

    # упорядочиваем колонки
    new_order_cols = lst_svod_cols.copy()
    new_order_cols.extend(([ 'ШДБ_Значение'
                            ]))
    svod_mean_one_df = svod_mean_one_df.reindex(columns=new_order_cols)

    dct_rename_cols_mean = {'ШДБ_Значение': 'Ср. шкала душевной боли',
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
                    f'ШДБ {out_name}': svod_count_one_level_vcha_df,
                    })

    if len(lst_svod_cols) == 1:
        return out_dct
    else:
        for idx, name_column in enumerate(lst_svod_cols):
            lst_reindex_column_level_cols = [lst_svod_cols[idx],'низкий ШДБ', 'умеренный ШДБ', 'повышенный ШДБ', 'высокий ШДБ',
                                                  'Итого']
            svod_count_column_level_vcha_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                               'ШДБ_Значение',
                                                               'ШДБ_Уровень',
                                                               lst_reindex_column_level_cols, lst_level)

            # Считаем среднее по субшкалам
            svod_mean_column_df = pd.pivot_table(base_df,
                                                 index=[lst_svod_cols[idx]],
                                                 values=[
                                                     'ШДБ_Значение',
                                                 ],
                                                 aggfunc=round_mean_two)
            svod_mean_column_df.reset_index(inplace=True)

            # упорядочиваем колонки
            new_order_cols = [lst_svod_cols[idx]].copy()
            new_order_cols.extend((['ШДБ_Значение'
                                    ]))
            svod_mean_column_df = svod_mean_column_df.reindex(columns=new_order_cols)

            dct_rename_cols_mean = {'ШДБ_Значение': 'Ср. шкала душевной боли',
                                    }
            svod_mean_column_df.rename(columns=dct_rename_cols_mean, inplace=True)
            # Готовим наименование
            name_column = lst_svod_cols[idx]
            name_column = re.sub(r'[\[\]\'+()<> :"?*|\\/]', '_', name_column)
            name_column = name_column[:15]
            out_dct.update({f'Ср {name_column}': svod_mean_column_df,
                            f'ШДБ {name_column}': svod_count_column_level_vcha_df,
                            })
        return out_dct





def processing_pas_hol_kol(base_df: pd.DataFrame, answers_df: pd.DataFrame, lst_svod_cols:list):
    """
    Функция для обработки
    :param base_df: часть датафрейма с описательными колонками
    :param answers_df: часть датафрейма с ответами
    :param lst_svod_cols:  список с колонками по которым нужно делать свод
    """
    try:
        out_answer_df = base_df.copy()  # делаем копию для последующего соединения с сырыми ответами
        if len(answers_df.columns) != 13:  # проверяем количество колонок с вопросами
            raise BadCountColumnsPASKCH

        # очищаем названия колонок от возможных сочетаний .1 которые добавляет пандас при одинаковых колонках
        clean_df_lst = []
        for name_column in answers_df.columns:
            clean_name = re.sub(r'.\d+$', '', name_column)
            clean_df_lst.append(clean_name)

        answers_df.columns = clean_df_lst

        lst_check_cols = ['Я испытываю душевную боль',
                          'У меня щемит внутри',
                          'Моя душевная боль хуже любой физической боли',
                          'От этой боли хочется кричать',
                          'Из-за этой боли я живу как во тьме',
                          'Я не понимаю, почему я страдаю',
                          'Психологически я чувствую себя ужасно',
                          'Я испытываю боль из-за внутреннего чувства пустоты',
                          'У меня болит душа',
                          'Я не могу больше терпеть эту боль',
                          'Из-за этой боли моё состояние невыносимо',
                          'Из-за этой боли я словно разваливаюсь',
                          'Моя душевная боль влияет на всё, что я делаю',
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
            raise BadOrderPASKCH

        valid_values = [['никогда','иногда','часто','часто','всегда'],
                        ['никогда', 'иногда', 'часто', 'часто', 'всегда'],
                        ['никогда', 'иногда', 'часто', 'часто', 'всегда'],

                        ['никогда', 'иногда', 'часто', 'часто', 'всегда'],
                        ['никогда', 'иногда', 'часто', 'часто', 'всегда'],
                        ['никогда', 'иногда', 'часто', 'часто', 'всегда'],

                        ['никогда', 'иногда', 'часто', 'часто', 'всегда'],
                        ['никогда', 'иногда', 'часто', 'часто', 'всегда'],
                        ['никогда', 'иногда', 'часто', 'часто', 'всегда'],

                        ['абсолютно не согласен','не согласен','не уверен','согласен','абсолютно согласен'],
                        ['абсолютно не согласен','не согласен','не уверен','согласен','абсолютно согласен'],
                        ['абсолютно не согласен','не согласен','не уверен','согласен','абсолютно согласен'],
                        ['абсолютно не согласен','не согласен','не уверен','согласен','абсолютно согласен'],
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
            raise BadValuePASKCH

        # словарь для замены слов на числа
        dct_first_replace_value = {'никогда': 1,
                             'иногда': 2,
                             'часто': 3,
                             'очень часто': 4,
                             'всегда': 5,
                             }
        answers_df.replace(dct_first_replace_value, inplace=True)  # заменяем слова на цифры для подсчетов

        dct_second_replace_value = {'абсолютно не согласен': 1,
                             'не согласен': 2,
                             'не уверен': 3,
                             'согласен': 4,
                             'абсолютно согласен': 5,
                             }
        answers_df.replace(dct_second_replace_value, inplace=True)  # заменяем слова на цифры для подсчетов

        base_df['ШДБ_Значение'] = answers_df.sum(axis=1)
        base_df['ШДБ_Уровень'] = base_df['ШДБ_Значение'].apply(calc_level)

        # Создаем датафрейм для создания части в общий датафрейм
        part_df = pd.DataFrame()

        # Основные шкалы

        part_df['ШДБКЧ_Значение'] = base_df['ШДБ_Значение']
        part_df['ШДБКЧ_Диапазон'] = base_df['ШДБ_Уровень']

        out_answer_df = pd.concat([out_answer_df, answers_df], axis=1)  # Датафрейм для проверки
        base_df.sort_values(by='ШДБ_Значение', ascending=False, inplace=True)  # сортируем

        # Делаем свод  по  шкалам
        dct_svod_sub = {'ШДБ_Значение': 'ШДБ_Уровень',
                        }

        dct_rename_svod_sub = {
            'ШДБ_Значение': 'Уровень шкалы душевной боли',
        }

        lst_sub = ['низкий ШДБ', 'умеренный ШДБ', 'повышенный ШДБ', 'высокий ШДБ']

        base_svod_sub_df = create_union_svod(base_df, dct_svod_sub, dct_rename_svod_sub, lst_sub)

        avg_psp = round(base_df['ШДБ_Значение'].mean(), 2)

        avg_dct = {'Среднее значение шкалы душевной боли': avg_psp,
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

        dct_prefix = {'ШДБ_Уровень': 'ШДБ',
                      }

        out_dct = create_list_on_level_pas(base_df, out_dct, lst_sub, dct_prefix)

        """
                                Сохраняем в зависимости от необходимости делать своды по определенным колонкам
                                """
        if len(lst_svod_cols) == 0:
            return out_dct, part_df

        else:
            out_dct = create_result_pas_kol_chist(base_df, out_dct, lst_svod_cols)
            return out_dct, part_df


    except BadOrderPASKCH:
        messagebox.showerror('Лахеcис',
                             f'При обработке вопросов теста Шкала душевной боли, PAS-13 Холден Колачев Чистопольская и др. обнаружены неправильные вопросы. Проверьте названия колонок с вопросами:\n'
                             f'{error_order_message[:5000]}\n'
                             f'Используйте при создании Яндекс-формы написание вопросов из руководства пользователя программы Лахесис.')
    except BadValuePASKCH:
        messagebox.showerror('Лахеcис',
                             f'При обработке вопросов теста Шкала душевной боли, PAS-13 Холден Колачев Чистопольская и др. обнаружены неправильные варианты ответов. Проверьте ответы на указанных строках:\n'
                             f'{error_message[:5000]}\n'
                             f'Используйте при создании Яндекс-формы написание вариантов ответа из руководства пользователя программы Лахесис.')


    except BadCountColumnsPASKCH:
        messagebox.showerror('Лахеcис',
                             f'Проверьте количество колонок с ответами на тест Шкала душевной боли, PAS-13 Холден Колачев Чистопольская и др.\n'
                             f'Должно быть 13 колонок с ответами')




