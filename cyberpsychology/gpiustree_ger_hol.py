"""
Скрипт для обработки результатов теста Общая шкала проблемного использования интернета -3 GPIUS3 Герасимова Холмогорова
"""

import pandas as pd
import re
from tkinter import messagebox
from lachesis_support_functions import round_mean_two,calc_count_scale,create_list_on_level,create_union_svod


class BadOrderGPIUSTGH(Exception):
    """
    Исключение для обработки случая когда колонки не совпадают
    """
    pass


class BadValueGPIUSTGH(Exception):
    """
    Исключение для неправильных значений в вариантах ответов
    """
    pass

class BadCountColumnsGPIUSTGH(Exception):
    """
    Исключение для обработки случая если количество колонок не равно 14
    """
    pass



def calc_value_poo(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [1,3,12]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_pr:
            value_forward += value
    return value_forward

def calc_value_rn(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [4,5,7]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_pr:
            value_forward += value
    return value_forward

def calc_value_kp(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [2,8,10]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_pr:
            value_forward += value
    return value_forward

def calc_value_ki(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [6,9,11]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_pr:
            value_forward += value
    return value_forward

def calc_value_np(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [13,14]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_pr:
            value_forward += value
    return value_forward


def calc_level(value):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """
    if 14<= value <= 34:
        return f'14-34'
    elif 35 <= value <= 55:
        return f'35-55'
    elif 56 <= value <= 76:
        return f'56-76'
    else:
        return f'77-98'



def create_list_on_level_gpiust(base_df:pd.DataFrame, out_dct:dict, lst_level:list, dct_prefix:dict):
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


def create_result_gpiust_ger_hol(base_df:pd.DataFrame, out_dct:dict, lst_svod_cols:list):
    """
    Функция для подсчета результата если указаны колонки по которым нужно провести свод
    :param df: датафрейм с результатами
    :param out_dct: словарь с уже подсчитанными базовыми данными
    :param lst_svod_cols: список сводных колонок
    :return: словарь
    """
    lst_level = ['14-34', '35-55', '56-76', '77-98']

    lst_reindex_one_level_cols = lst_svod_cols.copy()
    lst_reindex_one_level_cols.extend(['14-34', '35-55', '56-76', '77-98',
                                       'Итого'])  # Основная шкала

    svod_count_one_level_vcha_df = calc_count_scale(base_df, lst_svod_cols,
                                                    'Сумма_Значение',
                                                    'Сумма_Диапазон',
                                                    lst_reindex_one_level_cols, lst_level)

    # Считаем среднее по субшкалам
    svod_mean_one_df = pd.pivot_table(base_df,
                                      index=lst_svod_cols,
                                      values=['ПОО_Значение',
                                              'РН_Значение',
                                              'КП_Значение',
                                              'КИ_Значение',
                                              'НП_Значение',
                                              'Сумма_Значение',
                                              ],
                                      aggfunc=round_mean_two)
    svod_mean_one_df.reset_index(inplace=True)

    # упорядочиваем колонки
    new_order_cols = lst_svod_cols.copy()
    new_order_cols.extend((['ПОО_Значение', 'РН_Значение','КП_Значение',
                            'КИ_Значение', 'НП_Значение', 'Сумма_Значение'
                            ]))
    svod_mean_one_df = svod_mean_one_df.reindex(columns=new_order_cols)

    dct_rename_cols_mean = {'ПОО_Значение': 'Ср. Предпочтение онлайн-общения',
                            'РН_Значение': 'Ср. Регуляция настроения',
                            'КП_Значение': 'Ср. Когнитивная поглощенность',
                            'КИ_Значение': 'Ср. Компульсивное использование',
                            'НП_Значение': 'Ср. Негативные последствия',
                            'Сумма_Значение': 'Ср. Общая сумма баллов',
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
                    f'Сумма {out_name}': svod_count_one_level_vcha_df,
                    })

    if len(lst_svod_cols) == 1:
        return out_dct

    else:
        for idx, name_column in enumerate(lst_svod_cols):
            lst_reindex_column_level_cols = [lst_svod_cols[idx],'14-34', '35-55', '56-76', '77-98',
                                                  'Итого']
            # ВЧА
            svod_count_column_level_vcha_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                            'Сумма_Значение',
                                                            'Сумма_Диапазон',
                                                            lst_reindex_column_level_cols, lst_level)

            # Считаем среднее по субшкалам
            svod_mean_column_df = pd.pivot_table(base_df,
                                              index=[lst_svod_cols[idx]],
                                              values=['ПОО_Значение',
                                                      'РН_Значение',
                                                      'КП_Значение',
                                                      'КИ_Значение',
                                                      'НП_Значение',
                                                      'Сумма_Значение',
                                                      ],
                                              aggfunc=round_mean_two)
            svod_mean_column_df.reset_index(inplace=True)

            # упорядочиваем колонки
            new_order_cols = [lst_svod_cols[idx]].copy()
            new_order_cols.extend((['ПОО_Значение', 'РН_Значение', 'КП_Значение',
                                    'КИ_Значение', 'НП_Значение', 'Сумма_Значение'
                                    ]))
            svod_mean_column_df = svod_mean_column_df.reindex(columns=new_order_cols)

            dct_rename_cols_mean = {'ПОО_Значение': 'Ср. Предпочтение онлайн-общения',
                                    'РН_Значение': 'Ср. Регуляция настроения',
                                    'КП_Значение': 'Ср. Когнитивная поглощенность',
                                    'КИ_Значение': 'Ср. Компульсивное использование',
                                    'НП_Значение': 'Ср. Негативные последствия',
                                    'Сумма_Значение': 'Ср. Общая сумма баллов',
                                    }
            svod_mean_column_df.rename(columns=dct_rename_cols_mean, inplace=True)

            # Готовим наименование
            name_column = lst_svod_cols[idx]
            name_column = re.sub(r'[\[\]\'+()<> :"?*|\\/]', '_', name_column)
            name_column = name_column[:15]
            out_dct.update({f'Ср {name_column}': svod_mean_column_df,
                            f'Сумма {name_column}': svod_count_column_level_vcha_df,
                            })
        return out_dct







def processing_gpiust_ger_hol(base_df: pd.DataFrame, answers_df: pd.DataFrame, lst_svod_cols:list):
    """
    Функция для обработки
    :param base_df: часть датафрейма с описательными колонками
    :param answers_df: часть датафрейма с ответами
    :param lst_svod_cols:  список с колонками по которым нужно делать свод
    """
    try:
        out_answer_df = base_df.copy()  # делаем копию для последующего соединения с сырыми ответами
        if len(answers_df.columns) != 14:  # проверяем количество колонок с вопросами
            raise BadCountColumnsGPIUSTGH

        # очищаем названия колонок от возможных сочетаний .1 которые добавляет пандас при одинаковых колонках
        clean_df_lst = []
        for name_column in answers_df.columns:
            clean_name = re.sub(r'.\d+$', '', name_column)
            clean_df_lst.append(clean_name)

        answers_df.columns = clean_df_lst

        lst_check_cols = ['Для меня более комфортно социальное взаимодействие online, чем лицом к лицу',
                          'Когда я не бываю online какое-то время, то меня начинает беспокоить мысль о выходе в сеть',
                          'Я предпочитаю общаться с людьми online, чем лицом к лицу',
                          'Я использую социальные сети, чтобы почувствовать себя лучше, когда мне грустно',
                          'Я использую социальные сети, чтобы поговорить с другими, когда чувствую себя в изоляции',
                          'Мне сложно контролировать количество времени, проводимого online',
                          'Я использую социальные сети, чтобы почувствовать себя лучше, когда расстраиваюсь',
                          'Я буду чувствовать себя потерянно, если не смогу быть online',
                          'Мне трудно контролировать мое пребывание в сети',
                          'Я навязчиво думаю о выходе в сеть, когда я offline',
                          'Когда я offline, мне сложно сопротивляться желанию выйти в сеть',
                          'Я предпочитаю социальные взаимодействия online, чем общение лицом к лицу',
                          'Мое использование социальных сетей создало проблемы в моей жизни',
                          'Мое использование социальных сетей создало трудности в управлении жизнью'
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
            raise BadOrderGPIUSTGH

        # словарь для замены слов на числа
        dct_replace_value = {'полностью согласен': 7,
                             'согласен': 6,
                             'скорее согласен': 5,
                             'ни то ни другое': 4,
                             'скорее не согласен': 3,
                             'не согласен': 2,
                             'полностью не согласен': 1,
                             }
        valid_values = [1, 2, 3, 4,5,6,7]
        answers_df.replace(dct_replace_value, inplace=True)  # заменяем слова на цифры для подсчетов
        # Проверяем, есть ли значения, отличающиеся от указанных в списке
        lst_error_answers = []  # список для хранения строк где найдены неправильные ответы

        for i in range(14):
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
            raise BadValueGPIUSTGH

        base_df['ПОО_Значение'] = answers_df.apply(calc_value_poo, axis=1)
        base_df['РН_Значение'] = answers_df.apply(calc_value_rn, axis=1)
        base_df['КП_Значение'] = answers_df.apply(calc_value_kp, axis=1)
        base_df['КИ_Значение'] = answers_df.apply(calc_value_ki, axis=1)
        base_df['НП_Значение'] = answers_df.apply(calc_value_np, axis=1)

        base_df['Сумма_Значение'] = answers_df.sum(axis=1)
        base_df['Сумма_Диапазон'] = base_df['Сумма_Значение'].apply(calc_level)

        # Создаем датафрейм для создания части в общий датафрейм
        part_df = pd.DataFrame()
        # Основные шкалы
        part_df['ОШПИИГХ_ПОО_Значение'] = base_df['ПОО_Значение']
        part_df['ОШПИИГХ_РН_Значение'] = base_df['РН_Значение']
        part_df['ОШПИИГХ_КП_Значение'] = base_df['КП_Значение']
        part_df['ОШПИИГХ_КИ_Значение'] = base_df['КИ_Значение']
        part_df['ОШПИИГХ_НП_Значение'] = base_df['НП_Значение']

        part_df['ОШПИИГХ_Сумма_Значение'] = base_df['Сумма_Значение']
        part_df['ОШПИИГХ_Сумма_Диапазон'] = base_df['Сумма_Диапазон']

        out_answer_df = pd.concat([out_answer_df, answers_df], axis=1)  # Датафрейм для проверки

        base_df.sort_values(by='Сумма_Значение', ascending=False, inplace=True)  # сортируем

        # Делаем свод  по  шкалам
        dct_svod_sub = {'Сумма_Значение': 'Сумма_Диапазон',
                        }

        dct_rename_svod_sub = {
            'Сумма_Значение': 'Диапазон Суммы баллов',
            }

        lst_sub = ['14-34', '35-55', '56-76', '77-98']

        base_svod_sub_df = create_union_svod(base_df, dct_svod_sub, dct_rename_svod_sub, lst_sub)

        avg_vcha = round(base_df['ПОО_Значение'].mean(), 2)
        avg_o = round(base_df['РН_Значение'].mean(), 2)
        avg_ruvs = round(base_df['КП_Значение'].mean(), 2)
        avg_iika = round(base_df['КИ_Значение'].mean(), 2)
        avg_np = round(base_df['НП_Значение'].mean(), 2)

        avg_psp = round(base_df['Сумма_Значение'].mean(), 2)

        avg_dct = {'Среднее значение шкалы Предпочтение онлайн-общения': avg_vcha,
                   'Среднее значение шкалы Регуляция настроения': avg_o,
                   'Среднее значение шкалы Когнитивная поглощенность': avg_ruvs,
                   'Среднее значение шкалы Компульсивное использование': avg_iika,
                   'Среднее значение шкалы Негативные последствия ': avg_np,

                   'Среднее значение Общая сумма баллов': avg_psp,
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

        dct_prefix = {'Сумма_Диапазон': 'Сумма',
                      }

        out_dct = create_list_on_level_gpiust(base_df, out_dct, lst_sub, dct_prefix)

        """
                                Сохраняем в зависимости от необходимости делать своды по определенным колонкам
                                """
        if len(lst_svod_cols) == 0:
            return out_dct, part_df

        else:
            out_dct = create_result_gpiust_ger_hol(base_df, out_dct, lst_svod_cols)
            return out_dct, part_df


    except BadOrderGPIUSTGH:
        messagebox.showerror('Лахеcис',
                             f'При обработке вопросов теста Общая шкала проблемного использования интернета-3 (GPIUS3) Герасимова, Холмогорова обнаружены неправильные вопросы. Проверьте названия колонок с вопросами:\n'
                             f'{error_order_message[:5000]}\n'
                             f'Используйте при создании Яндекс-формы написание вопросов из руководства пользователя программы Лахесис.')
    except BadValueGPIUSTGH:
        messagebox.showerror('Лахеcис',
                             f'При обработке вопросов теста Общая шкала проблемного использования интернета-3 (GPIUS3) Герасимова, Холмогорова обнаружены неправильные варианты ответов. Проверьте ответы на указанных строках:\n'
                             f'{error_message[:5000]}\n'
                             f'Используйте при создании Яндекс-формы написание вариантов ответа из руководства пользователя программы Лахесис.')


    except BadCountColumnsGPIUSTGH:
        messagebox.showerror('Лахеcис',
                             f'Проверьте количество колонок с ответами на тест Общая шкала проблемного использования интернета-3 (GPIUS3) Герасимова, Холмогорова\n'
                             f'Должно быть 14 колонок с ответами')









