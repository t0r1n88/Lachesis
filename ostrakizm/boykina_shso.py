"""
Скрипт для обработки результатов теста Шкала субъективного остракизма Бойкина Вариант для школьников
"""
import pandas as pd
import re
from tkinter import messagebox
from lachesis_support_functions import round_mean,create_union_svod,create_list_on_level

class BadOrderSHSO(Exception):
    """
    Исключение для обработки случая когда колонки не совпадают
    """
    pass


class BadValueSHSO(Exception):
    """
    Исключение для неправильных значений в вариантах ответов
    """
    pass

class BadCountColumnsSHSO(Exception):
    """
    Исключение для обработки случая если количество колонок не равно 14
    """
    pass


def calc_sub_value_ig(row):
    """
    Функция для подсчета значения субшкалы Игнорирование
    :param row: строка с ответами
    :return: число
    """
    lst_pr = [1, 2, 4, 7, 10]

    value_forward = 0 # счетчик прямых ответов
    value_reverse = 0 # счетчик обратных ответов
    lst_forward = [1, 2, 4,7, 10]  # список ответов которые нужно считать простым сложением
    lst_reverse = [] # обратный подсчет

    for idx, value in enumerate(row):
        if idx +1 in lst_pr:
            if idx + 1 in lst_forward:
                # print(f'Прямой подсчет {idx +1}') # Для проверки корректности
                value_forward += value
            elif idx +1 in lst_reverse:
                # print(f'Обратный подсчет {idx +1}')# Для проверки корректности
                if value == 5:
                    value_reverse += 1
                elif value == 4:
                    value_reverse += 2
                elif value == 3:
                    value_reverse += 3
                elif value == 2:
                    value_reverse += 4
                elif value == 1:
                    value_reverse += 5

    return round((value_forward + value_reverse) /5,1)

def calc_level_sub_ig(value):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """
    if 1 <= value <= 1.3:
        return 'низкий уровень социального остракизма'
    elif 1.4 <= value <= 2:
        return 'средний уровень социального остракизма'
    elif 2.1 <= value <= 5:
        return 'высокий уровень социального остракизма'



def calc_sub_value_isk(row):
    """
    Функция для подсчета значения субшкалы Исключение
    :return: число
    """
    lst_pr = [5, 8, 9, 12, 13]

    value_forward = 0 # счетчик прямых ответов
    value_reverse = 0 # счетчик обратных ответов
    lst_forward = []  # список ответов которые нужно считать простым сложением
    lst_reverse = [5, 8, 9, 12, 13] # обратный подсчет

    for idx, value in enumerate(row):
        if idx +1 in lst_pr:
            if idx + 1 in lst_forward:
                # print(f'Прямой подсчет {idx +1}') # Для проверки корректности
                value_forward += value
            elif idx +1 in lst_reverse:
                # print(f'Обратный подсчет {idx +1}')# Для проверки корректности
                if value == 5:
                    value_reverse += 1
                elif value == 4:
                    value_reverse += 2
                elif value == 3:
                    value_reverse += 3
                elif value == 2:
                    value_reverse += 4
                elif value == 1:
                    value_reverse += 5

    return round((value_forward + value_reverse) /5,1)

def calc_level_sub_isk(value):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """
    if 1 <= value <= 2.3:
        return 'низкий уровень социального остракизма'
    elif 2.4 <= value <= 3.4:
        return 'средний уровень социального остракизма'
    elif 3.5 <= value <= 5:
        return 'высокий уровень социального остракизма'



def calc_sub_value_ot(row):
    """
    Функция для подсчета значения субшкалы Отвержение
    :return: число
    """
    lst_pr = [3, 6, 11, 14]

    value_forward = 0 # счетчик прямых ответов
    value_reverse = 0 # счетчик обратных ответов
    lst_forward = [6, 11, 14]  # список ответов которые нужно считать простым сложением
    lst_reverse = [3] # обратный подсчет

    for idx, value in enumerate(row):
        if idx +1 in lst_pr:
            if idx + 1 in lst_forward:
                # print(f'Прямой подсчет {idx +1}') # Для проверки корректности
                value_forward += value
            elif idx +1 in lst_reverse:
                # print(f'Обратный подсчет {idx +1}')# Для проверки корректности
                if value == 5:
                    value_reverse += 1
                elif value == 4:
                    value_reverse += 2
                elif value == 3:
                    value_reverse += 3
                elif value == 2:
                    value_reverse += 4
                elif value == 1:
                    value_reverse += 5

    return round((value_forward + value_reverse) /4,1)

def calc_level_sub_ot(value):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """
    if 1 <= value <= 1.6:
        return 'низкий уровень социального остракизма'
    elif 1.7 <= value <= 2.5:
        return 'средний уровень социального остракизма'
    elif 2.6 <= value <= 5:
        return 'высокий уровень социального остракизма'



def create_boykina_list_on_level(base_df:pd.DataFrame,out_dct:dict,lst_level:list,dct_prefix:dict):
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
                if level == 'низкий уровень социального остракизма':
                    level = 'низкий уровень'
                elif level == 'средний уровень социального остракизма':
                    level = 'средний уровень'
                else:
                    level = 'высокий уровень'
                dct_level[f'{dct_prefix[key]}. {level}'] = temp_df
        out_dct.update(dct_level)

    return out_dct

def calc_count_level(df:pd.DataFrame, lst_cat:list, val_cat, col_cat, lst_cols:list):
    """
    Функция для создания сводных датафреймов по шкалам

    :param df: датафрейм с данными
    :param lst_cat:список колонок по которым будет формироваться свод
    :param val_cat:значение по которому будет формироваться свод
    :param col_cat: колонка по которой будет формироваться свод
    :param lst_cols: список с колонками
    :return:датафрейм
    """
    count_df = pd.pivot_table(df, index=lst_cat,
                                             columns=col_cat,
                                             values=val_cat,
                                             aggfunc='count', margins=True, margins_name='Итого')


    count_df.reset_index(inplace=True)
    count_df = count_df.reindex(columns=lst_cols)
    count_df['% низкий уровень социального остракизма от общего'] = round(
        count_df['низкий уровень социального остракизма'] / count_df['Итого'], 2) * 100
    count_df['% средний уровень социального остракизма от общего'] = round(
        count_df['средний уровень социального остракизма'] / count_df['Итого'], 2) * 100
    count_df['% высокий уровень социального остракизма от общего'] = round(
        count_df['высокий уровень социального остракизма'] / count_df['Итого'], 2) * 100

    return count_df

def create_result_shso(base_df:pd.DataFrame, out_dct:dict, lst_svod_cols:list):
    """
    Функция для подсчета результата если указаны колонки по которым нужно провести свод
    :param df: датафрейм с результатами
    :param out_dct: словарь с уже подсчитанными базовыми данными
    :param lst_svod_cols: список сводных колонок
    :return: словарь
    """
    lst_reindex_one_level_cols = lst_svod_cols.copy()
    lst_reindex_one_level_cols.extend( ['низкий уровень социального остракизма', 'средний уровень социального остракизма', 'высокий уровень социального остракизма',
                                                      'Итого'])

    # Субшкалы
    svod_count_one_level_ig_df = calc_count_level(base_df, lst_svod_cols,
                                                      'Значение_субшкалы_Игнорирование',
                                                      'Уровень_субшкалы_Игнорирование',
                                                      lst_reindex_one_level_cols)

    svod_count_one_level_is_df = calc_count_level(base_df, lst_svod_cols,
                                                          'Значение_субшкалы_Исключение',
                                                          'Уровень_субшкалы_Исключение',
                                                          lst_reindex_one_level_cols)

    svod_count_one_level_ot_df = calc_count_level(base_df, lst_svod_cols,
                                                         'Значение_субшкалы_Отвержение',
                                                         'Уровень_субшкалы_Отвержение',
                                                         lst_reindex_one_level_cols)

    # Считаем среднее по субшкалам
    svod_mean_one_df = pd.pivot_table(base_df,
                                      index=lst_svod_cols,
                                      values=['Значение_субшкалы_Игнорирование',
                                              'Значение_субшкалы_Исключение',
                                              'Значение_субшкалы_Отвержение',
                                              ],
                                      aggfunc=round_mean)
    svod_mean_one_df.reset_index(inplace=True)
    # упорядочиваем колонки
    new_order_cols = lst_svod_cols.copy()
    new_order_cols.extend((['Значение_субшкалы_Игнорирование',
                            'Значение_субшкалы_Исключение',
                            'Значение_субшкалы_Отвержение',
                            ]))
    svod_mean_one_df = svod_mean_one_df.reindex(columns=new_order_cols)

    dct_rename_cols_mean = {'Значение_субшкалы_Игнорирование': 'Ср. Игнор',
                            'Значение_субшкалы_Исключение': 'Ср. Искл',
                            'Значение_субшкалы_Отвержение': 'Ср. Отв',
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
                    f'Свод Игнор {out_name}': svod_count_one_level_ig_df,
                    f'Свод Искл {out_name}': svod_count_one_level_is_df,
                    f'Свод Отв {out_name}': svod_count_one_level_ot_df})

    if len(lst_svod_cols) == 1:
        return out_dct
    else:
        for idx, name_column in enumerate(lst_svod_cols):
            # Тревожность
            lst_reindex_column_level_cols = [lst_svod_cols[idx],'низкий уровень социального остракизма', 'средний уровень социального остракизма', 'высокий уровень социального остракизма',
                                             'Итого']
            svod_count_column_level_ig_df = calc_count_level(base_df, lst_svod_cols[idx],
                                                             'Значение_субшкалы_Игнорирование',
                                                             'Уровень_субшкалы_Игнорирование',
                                                             lst_reindex_column_level_cols)

            svod_count_column_level_is_df = calc_count_level(base_df, lst_svod_cols[idx],
                                                             'Значение_субшкалы_Исключение',
                                                             'Уровень_субшкалы_Исключение',
                                                             lst_reindex_column_level_cols)

            svod_count_column_level_ot_df = calc_count_level(base_df, lst_svod_cols[idx],
                                                             'Значение_субшкалы_Отвержение',
                                                             'Уровень_субшкалы_Отвержение',
                                                             lst_reindex_column_level_cols)

            # Считаем среднее по субшкалам
            svod_mean_column_df = pd.pivot_table(base_df,
                                                 index=[lst_svod_cols[idx]],
                                                 values=['Значение_субшкалы_Игнорирование',
                                                         'Значение_субшкалы_Исключение',
                                                         'Значение_субшкалы_Отвержение',
                                                         ],
                                                 aggfunc=round_mean)
            svod_mean_column_df.reset_index(inplace=True)
            # упорядочиваем колонки
            new_order_cols = [lst_svod_cols[idx]].copy()
            new_order_cols.extend((['Значение_субшкалы_Игнорирование',
                                    'Значение_субшкалы_Исключение',
                                    'Значение_субшкалы_Отвержение',
                                    ]))
            svod_mean_column_df = svod_mean_column_df.reindex(columns=new_order_cols)

            dct_rename_cols_mean = {'Значение_субшкалы_Игнорирование': 'Ср. Игнор',
                                    'Значение_субшкалы_Исключение': 'Ср. Искл',
                                    'Значение_субшкалы_Отвержение': 'Ср. Отв',
                                    }
            svod_mean_column_df.rename(columns=dct_rename_cols_mean, inplace=True)
            name_column = lst_svod_cols[idx]
            name_column = re.sub(r'[\[\]\'+()<> :"?*|\\/]', '_', name_column)
            name_column = name_column[:15]

            out_dct.update({f'Ср {name_column}': svod_mean_column_df,
                            f'Свод Игнор {name_column}': svod_count_column_level_ig_df,
                            f'Свод Искл {name_column}': svod_count_column_level_is_df,
                            f'Свод Отв {name_column}': svod_count_column_level_ot_df})
        return out_dct






def processing_boykina_shso(result_df: pd.DataFrame, answers_df: pd.DataFrame,lst_svod_cols:list):
    """
    Функция для обработки
    :param result_df: часть датафрейма с описательными колонками
    :param answers_df: часть датафрейма с ответами
    :param lst_svod_cols:  список с колонками по которым нужно делать свод
    """
    try:
        out_answer_df = result_df.copy()  # делаем копию для последующего соединения с сырыми ответами
        if len(answers_df.columns) != 14:  # проверяем количество колонок с вопросами
            raise BadCountColumnsSHSO

        # очищаем названия колонок от возможных сочетаний .1 которые добавляет пандас при одинаковых колонках
        clean_df_lst = []
        for name_column in answers_df.columns:
            clean_name = re.sub(r'.\d+$', '', name_column)
            clean_df_lst.append(clean_name)

        answers_df.columns = clean_df_lst

        lst_check_cols = ['В основном, другие относятся ко мне как к невидимке',
                          'В основном, другие смотрят сквозь меня, будто я не существую',
                          'В основном, другие отвергают мои предложения',
                          'В основном, другие игнорируют меня во время разговора',
                          'В основном, другие приглашают меня на выходные',
                          'В основном, другие отказывают мне, когда я что-либо спрашиваю',
                          'В основном, другие игнорируют меня',
                          'В основном, другие проводят время со мной у меня дома',
                          'В основном, другие приглашают меня стать членом их клуба, организации, группы',
                          'В основном, другие игнорируют мои приветствия при встрече',
                          'В основном, другие не стесняются писать мне в соцсети, что не пойдут со мной на встречу',
                          'В основном, другие всячески стараются привлечь моё внимание',
                          'В основном, другие приглашают меня присоединиться к ним в хобби, провести вместе выходные или сходить куда-нибудь',
                          'В основном, другие часто противоречат мне в большой компании',
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
            raise BadOrderSHSO

        # словарь для замены слов на числа
        dct_replace_value = {'всегда': 5,
                             'часто': 4,
                             'иногда': 3,
                             'редко': 2,
                             'никогда': 1}

        valid_values = [1, 2, 3, 4, 5]
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
            raise BadValueSHSO

        base_df = pd.DataFrame()

        # Субшкала Игнорирование
        base_df['Значение_субшкалы_Игнорирование'] = answers_df.apply(calc_sub_value_ig, axis=1)
        base_df['Норма_Игнорирование'] = '1,4-2 балла'
        base_df['Уровень_субшкалы_Игнорирование'] = base_df['Значение_субшкалы_Игнорирование'].apply(
            calc_level_sub_ig)

        # Субшкала Исключение
        base_df['Значение_субшкалы_Исключение'] = answers_df.apply(calc_sub_value_isk, axis=1)
        base_df['Норма_Исключение'] = '2,4-3,4 баллов'
        base_df['Уровень_субшкалы_Исключение'] = base_df['Значение_субшкалы_Исключение'].apply(
            calc_level_sub_isk)

        # Субшкала Отвержение
        base_df['Значение_субшкалы_Отвержение'] = answers_df.apply(calc_sub_value_ot, axis=1)
        base_df['Норма_Отвержение'] = '1,7-2,5 баллов'
        base_df['Уровень_субшкалы_Отвержение'] = base_df['Значение_субшкалы_Отвержение'].apply(
            calc_level_sub_ot)

        # Создаем датафрейм для создания части в общий датафрейм
        part_df = pd.DataFrame()

        part_df['ШСО_Игнор_Значение'] = base_df['Значение_субшкалы_Игнорирование']
        part_df['ШСО_Игнор_Уровень'] = base_df['Уровень_субшкалы_Игнорирование']

        part_df['ШСО_Искл_Значение'] = base_df['Значение_субшкалы_Исключение']
        part_df['ШСО_Искл_Уровень'] = base_df['Уровень_субшкалы_Исключение']

        part_df['ШСО_Отв_Значение'] = base_df['Значение_субшкалы_Отвержение']
        part_df['ШСО_Отв_Уровень'] = base_df['Уровень_субшкалы_Отвержение']

        out_answer_df = pd.concat([out_answer_df, answers_df], axis=1)  # Датафрейм для проверки

        # Соединяем анкетную часть с результатной
        base_df = pd.concat([result_df, base_df], axis=1)
        base_df.sort_values(by='Значение_субшкалы_Игнорирование', ascending=False, inplace=True)  # сортируем

        # формируем основной словарь
        out_dct = {'Списочный результат': base_df, 'Список для проверки': out_answer_df,
                   }

        # Делаем свод  по  шкалам
        dct_svod_sub = {'Значение_субшкалы_Игнорирование': 'Уровень_субшкалы_Игнорирование',
                        'Значение_субшкалы_Исключение': 'Уровень_субшкалы_Исключение',
                        'Значение_субшкалы_Отвержение': 'Уровень_субшкалы_Отвержение',
                        }

        dct_rename_svod_sub = {'Значение_субшкалы_Игнорирование': 'Игнорирование',
                               'Значение_субшкалы_Исключение': 'Исключение',
                               'Значение_субшкалы_Отвержение': 'Отвержение',
                               }

        # Списки для шкал
        lst_level = ['низкий уровень социального остракизма', 'средний уровень социального остракизма', 'высокий уровень социального остракизма']

        base_svod_sub_df = create_union_svod(base_df, dct_svod_sub, dct_rename_svod_sub, lst_level)

        # считаем среднее значение по шкалам
        avg_ig = round(base_df['Значение_субшкалы_Игнорирование'].mean(), 2)
        avg_is = round(base_df['Значение_субшкалы_Исключение'].mean(), 2)
        avg_ot = round(base_df['Значение_субшкалы_Отвержение'].mean(), 2)

        avg_dct = {'Среднее значение шкалы Игнорирование': avg_ig,
                   'Среднее значение шкалы Исключение': avg_is,
                   'Среднее значение шкалы Отвержение': avg_ot,
                   }

        avg_df = pd.DataFrame.from_dict(avg_dct, orient='index')
        avg_df = avg_df.reset_index()
        avg_df.columns = ['Показатель', 'Среднее значение']

        # формируем основной словарь
        out_dct = {'Списочный результат': base_df, 'Список для проверки': out_answer_df,
                   'Свод по шкалам': base_svod_sub_df,
                   'Среднее по шкалам': avg_df,
                   }


        # Делаем списки
        dct_prefix = {'Уровень_субшкалы_Игнорирование': 'Игнор',
                      'Уровень_субшкалы_Исключение': 'Искл',
                      'Уровень_субшкалы_Отвержение': 'Отв',
                      }

        out_dct = create_boykina_list_on_level(base_df, out_dct, lst_level, dct_prefix)

        """
            Сохраняем в зависимости от необходимости делать своды по определенным колонкам
            """
        if len(lst_svod_cols) == 0:
            return out_dct, part_df
        else:
            out_dct = create_result_shso(base_df, out_dct, lst_svod_cols)

            return out_dct, part_df

    except BadOrderSHSO:
        messagebox.showerror('Лахеcис',
                             f'При обработке вопросов теста Шкала субъективного остракизма Бойкина обнаружены неправильные вопросы. Проверьте названия колонок с вопросами:\n'
                             f'{error_order_message}\n'
                             f'Используйте при создании Яндекс-формы написание вопросов из руководства пользователя программы Лахесис.')
    except BadValueSHSO:
        messagebox.showerror('Лахеcис',
                             f'При обработке вопросов теста Шкала субъективного остракизма Бойкина обнаружены неправильные варианты ответов. Проверьте ответы на указанных строках:\n'
                             f'{error_message}\n'
                             f'Используйте при создании Яндекс-формы написание вариантов ответа из руководства пользователя программы Лахесис.')


    except BadCountColumnsSHSO:
        messagebox.showerror('Лахеcис',
                             f'Проверьте количество колонок с ответами на тест Шкала субъективного остракизма Бойкина\n'
                             f'Должно быть 14 колонок с ответами')

