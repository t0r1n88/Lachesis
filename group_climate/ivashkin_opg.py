"""
Скрипт для обработки результатов Определение привлекательности для школьника группы одноклассников Ивашкин
"""

import pandas as pd
import re
from tkinter import messagebox
from lachesis_support_functions import round_mean_two,calc_count_scale,create_union_svod,create_list_on_level

class BadOrderOPSGOI(Exception):
    """
    Исключение для обработки случая когда колонки не совпадают
    """
    pass


class BadValueOPSGOI(Exception):
    """
    Исключение для неправильных значений в вариантах ответов
    """
    pass

class BadCountColumnsOPSGOI(Exception):
    """
    Исключение для обработки случая если количество колонок не равно 5
    """
    pass

def calc_value(row):
    """
    Функция для подсчета значения шкалы Самочувствие
    :param row: строка с ответами
    :return: число
    """
    value_pos = 0
    # 1
    if row[0] == 'Считаю себя активным, полноправным членом класса':
        value_pos += 5
    elif row[0] == 'Участвую в большинстве дел класса, но часть одноклассников делают это активнее меня':
        value_pos += 4
    elif row[0] == 'Участвую примерно в половине дел класса':
        value_pos += 3
    elif row[0] == 'Не чувствую привязанности к классу и в его делах участвую редко':
        value_pos += 2
    elif row[0] == 'Делами класса не интересуюсь и участвовать в них не желаю':
        value_pos += 1

    # 2
    if row[1] == 'Очень хотел бы':
        value_pos += 1
    elif row[1] == 'Скорее всего перешел бы, чем остался':
        value_pos += 2
    elif row[1] == 'Не вижу никакой разницы':
        value_pos += 3
    elif row[1] == 'Скорее всего остался бы в своем классе':
        value_pos += 4
    elif row[1] == 'Очень хотел бы остаться в своем классе':
        value_pos += 5
    # 3
    if row[2] == 'Лучше, чем в других классах':
        value_pos += 3
    elif row[2] == 'Такие же, как в других классах':
        value_pos += 2
    elif row[2] == 'Хуже, чем в других классах':
        value_pos += 1

    # 4
    if row[3] == 'Лучше, чем в других классах':
        value_pos += 3
    elif row[3] == 'Такие же, как в других классах':
        value_pos += 2
    elif row[3] == 'Хуже, чем в других классах':
        value_pos += 1

    # 5
    if row[4] == 'Лучше, чем в других классах':
        value_pos += 3
    elif row[4] == 'Такое же, как в других классах':
        value_pos += 2
    elif row[4] == 'Хуже, чем в других классах':
        value_pos += 1



    return value_pos


def calc_level(value):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """
    if  5 <=value <= 8:
        return f'от 5 до 8'
    elif 9 <= value <= 12:
        return f'от 9 до 12'
    elif 13 <= value <= 16:
        return f'от 13 до 16'
    else:
        return f'от 17 до 19'


def calc_level_all(value):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """
    if 5 <= value < 8:
        return f'5-7.99'
    elif 8 <= value < 12:
        return f'8-11.99'
    elif 12 <= value < 16:
        return f'12-15.99'
    else:
        return f'16-19'



def create_union_svod_opg(base_df:pd.DataFrame,dct_svod_integral:dict,dct_rename_svod_integral:dict,lst_integral:list):
    """
    Функция для создания объединенного свода по шкалам с одинаковыми названиями уровней
    :param base_df: датафрейм с результатам подсчетов
    :param dct_svod_integral: словарь где ключ это название колонки с значением шкалы а значение это название колонки с уровнем значения шкалы
    :param dct_rename_svod_integral: словарь для переименования колонок ключ это значение шкалы а значение это то как будет называться колонка в своде
    :param lst_integral:  список уровней
    :return: датафрейм
    """
    # общий датафрейм
    base_svod_df = pd.DataFrame(
        index=lst_integral)

    for key,value in dct_svod_integral.items():
        svod_level_df = pd.pivot_table(base_df, index=value,
                                       values=key,
                                       aggfunc='count')

        svod_level_df[f'{dct_rename_svod_integral[key]} % от общего'] = round(
            svod_level_df[key] / svod_level_df[
                key].sum(), 3) * 100

        base_svod_df = base_svod_df.join(svod_level_df)

        # # Создаем суммирующую строку
    base_svod_df.loc['Итого'] = base_svod_df.sum()
    base_svod_df.reset_index(inplace=True)
    # Переименовываем
    base_svod_df.rename(columns=dct_rename_svod_integral,inplace=True)
    base_svod_df.rename(columns={'index': 'Вариант ответа'},inplace=True)

    return base_svod_df


def create_list_on_level_first(base_df:pd.DataFrame,out_dct:dict,lst_level:list,dct_prefix:dict):
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
                if level == 'Делами класса не интересуюсь и участвовать в них не желаю':
                    level = '1'
                elif level == 'Не чувствую привязанности к классу и в его делах участвую редко':
                    level = '2'
                elif level == 'Участвую примерно в половине дел класса':
                    level = '3'
                elif level == 'Участвую в большинстве дел класса, но часть одноклассников делают это активнее меня':
                    level = '4'
                else:
                    level = '5'
                dct_level[f'{dct_prefix[key]}. {level}'] = temp_df
        out_dct.update(dct_level)

    return out_dct


def create_list_on_level_second(base_df:pd.DataFrame,out_dct:dict,lst_level:list,dct_prefix:dict):
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
                if level == 'Очень хотел бы':
                    level = '1'
                elif level == 'Скорее всего перешел бы, чем остался':
                    level = '2'
                elif level == 'Не вижу никакой разницы':
                    level = '3'
                elif level == 'Скорее всего остался бы в своем классе':
                    level = '4'
                else:
                    level = '5'
                dct_level[f'{dct_prefix[key]}. {level}'] = temp_df
        out_dct.update(dct_level)

    return out_dct


def create_list_on_level_other(base_df:pd.DataFrame,out_dct:dict,lst_level:list,dct_prefix:dict):
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
                if level == 'Хуже, чем в других классах':
                    level = '1'
                elif level == 'Такие же, как в других классах':
                    level = '2'
                elif level == 'Лучше, чем в других классах':
                    level = '3'
                dct_level[f'{dct_prefix[key]}. {level}'] = temp_df
        out_dct.update(dct_level)

    return out_dct


def count_group_result(df:pd.DataFrame):
    """
    Для подсчета внутри группы
    :param df:
    :return:
    """
    return round(df.sum() / len(df),2)



def create_result_opg_ivashkin(base_df:pd.DataFrame, out_dct:dict, lst_svod_cols:list):
    """
    Функция для подсчета результата если указаны колонки по которым нужно провести свод
    :param df: датафрейм с результатами
    :param out_dct: словарь с уже подсчитанными базовыми данными
    :param lst_svod_cols: список сводных колонок
    :return: словарь
    """

    lst_level_sj = ['от 5 до 8', 'от 9 до 12', 'от 13 до 16', 'от 17 до 19']
    lst_reindex_one_level_sj_cols = lst_svod_cols.copy()
    lst_reindex_one_level_sj_cols.extend(['от 5 до 8', 'от 9 до 12', 'от 13 до 16', 'от 17 до 19',
                                       'Итого'])  # Основная шкала

    svod_count_one_level_sj_df = calc_count_scale(base_df, lst_svod_cols,
                                                    'ИО_Значение',
                                                    'ИО_Диапазон',
                                                    lst_reindex_one_level_sj_cols, lst_level_sj)


    lst_t_sub = ['5-7.99','8-11.99','12-15.99','16-19']

    lst_reindex_one_level_t_cols = lst_svod_cols.copy()
    lst_reindex_one_level_t_cols.extend(['5-7.99','8-11.99','12-15.99','16-19',
                                          'Итого'])  # Основная шкала

    svod_count_one_level_t_df = calc_count_scale(base_df, lst_svod_cols,
                                                  'ГО_Значение',
                                                  'ГО_Диапазон',
                                                  lst_reindex_one_level_t_cols, lst_t_sub)

    # Считаем среднее по субшкалам
    svod_mean_one_df = pd.pivot_table(base_df,
                                      index=lst_svod_cols,
                                      values=[
                                          'ИО_Значение'
                                      ],
                                      aggfunc=round_mean_two)
    svod_mean_one_df.reset_index(inplace=True)

    # упорядочиваем колонки
    new_order_cols = lst_svod_cols.copy()
    new_order_cols.extend((['ИО_Значение'
                            ]))
    svod_mean_one_df = svod_mean_one_df.reindex(columns=new_order_cols)

    dct_rename_cols_mean = {'ИО_Значение': 'Ср. значение Индивидуальная оценка уровня привлекательности класса для школьника',
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
                    f'ИО {out_name}': svod_count_one_level_sj_df,
                    f'ГО {out_name}': svod_count_one_level_t_df,
                    })

    if len(lst_svod_cols) == 1:
        dct_prefix = {'ИО_Диапазон': 'ИО',
                      }

        out_dct = create_list_on_level(base_df, out_dct, lst_level_sj, dct_prefix)

        dct_prefix_oo = {'ГО_Диапазон': 'ГО',
                         }
        out_dct = create_list_on_level(base_df, out_dct, lst_t_sub, dct_prefix_oo)

        return out_dct
    else:
        for idx, name_column in enumerate(lst_svod_cols):
            lst_reindex_column_io_level_cols = [lst_svod_cols[idx],'от 5 до 8', 'от 9 до 12', 'от 13 до 16', 'от 17 до 19',
                                   'Итого']  # Основная шкала

            lst_reindex_column_oo_level_cols = [lst_svod_cols[idx],'5-7.99','8-11.99','12-15.99','16-19',
                                   'Итого']  # Основная шкала

            svod_count_column_level_io_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                          'ИО_Значение',
                                                          'ИО_Диапазон',
                                                          lst_reindex_column_io_level_cols, lst_level_sj)

            svod_count_column_level_oo_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                          'ГО_Значение',
                                                          'ГО_Диапазон',
                                                          lst_reindex_column_oo_level_cols, lst_t_sub)

            # Считаем среднее по субшкалам
            svod_mean_column_df = pd.pivot_table(base_df,
                                                 index=[lst_svod_cols[idx]],
                                                 values=[
                                                     'ИО_Значение'
                                                 ],
                                                 aggfunc=round_mean_two)
            svod_mean_column_df.reset_index(inplace=True)

            # упорядочиваем колонки
            new_order_cols = [lst_svod_cols[idx]].copy()
            new_order_cols.extend((['ИО_Значение'
                                    ]))
            svod_mean_column_df = svod_mean_column_df.reindex(columns=new_order_cols)

            dct_rename_cols_mean = {
                'ИО_Значение': 'Ср. значение Индивидуальная оценка уровня привлекательности класса для школьника',
            }
            svod_mean_column_df.rename(columns=dct_rename_cols_mean, inplace=True)
            name_column = lst_svod_cols[idx]
            name_column = re.sub(r'[\[\]\'+()<> :"?*|\\/]', '_', name_column)
            name_column = name_column[:15]

            out_dct.update({f'Ср {name_column}': svod_mean_column_df,
                            f'ИО {name_column}': svod_count_column_level_io_df,
                            f'ГО {name_column}': svod_count_column_level_oo_df,
                            })
        dct_prefix = {'ИО_Диапазон': 'ИО',
                      }

        out_dct = create_list_on_level(base_df, out_dct, lst_level_sj, dct_prefix)

        dct_prefix_oo = {'ГО_Диапазон': 'ГО',
                         }
        out_dct = create_list_on_level(base_df, out_dct, lst_t_sub, dct_prefix_oo)

        return out_dct













def processing_opsgo_ivashkin(base_df: pd.DataFrame, answers_df: pd.DataFrame, lst_svod_cols:list):
    """
    Функция для обработки
    :param base_df: часть датафрейма с описательными колонками
    :param answers_df: часть датафрейма с ответами
    :param lst_svod_cols:  список с колонками по которым нужно делать свод
    """
    try:
        out_answer_df = base_df.copy()  # делаем копию для последующего соединения с сырыми ответами
        if len(answers_df.columns) != 5:  # проверяем количество колонок с вопросами
            raise BadCountColumnsOPSGOI

        # очищаем названия колонок от возможных сочетаний .1 которые добавляет пандас при одинаковых колонках
        clean_df_lst = []
        for name_column in answers_df.columns:
            clean_name = re.sub(r'.\d+$', '', name_column)
            clean_df_lst.append(clean_name)

        answers_df.columns = clean_df_lst
        lst_check_cols = ['Как вы оцениваете свою принадлежность классу?',
                          'Хотели бы вы перейти в другой класс, если бы предоставилась такая возможность?',
                          'Взаимоотношения учащихся в вашем классе',
                          'Взаимоотношения учеников вашего класса с учителями',
                          'Отношение одноклассников к учебе'
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
            raise BadOrderOPSGOI

        valid_values = [['Считаю себя активным, полноправным членом класса','Участвую в большинстве дел класса, но часть одноклассников делают это активнее меня',
                         'Участвую примерно в половине дел класса','Не чувствую привязанности к классу и в его делах участвую редко','Делами класса не интересуюсь и участвовать в них не желаю'],
                        ['Очень хотел бы','Скорее всего перешел бы, чем остался','Не вижу никакой разницы',
                         'Скорее всего остался бы в своем классе','Очень хотел бы остаться в своем классе'],
                        ['Лучше, чем в других классах','Такие же, как в других классах','Хуже, чем в других классах'],
                        ['Лучше, чем в других классах','Такие же, как в других классах','Хуже, чем в других классах'],
                        ['Лучше, чем в других классах','Такое же, как в других классах','Хуже, чем в других классах'],
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
            raise BadValueOPSGOI

        base_df['ИО_Значение'] = answers_df.apply(calc_value, axis=1)
        base_df['ИО_Диапазон'] = base_df['ИО_Значение'].apply(calc_level)

        if len(lst_svod_cols) == 0:
            base_df['ГО_Значение'] = round(base_df['ИО_Значение'].sum() / len(base_df), 1)
            base_df['ГО_Диапазон'] = base_df['ГО_Значение'].apply(calc_level_all)

            # Создаем датафрейм для создания части в общий датафрейм
            part_df = pd.DataFrame()

            part_df['ОПШГОИ_ИО_Значение'] = base_df['ИО_Значение']
            part_df['ОПШГОИ_ИО_Диапазон'] = base_df['ИО_Диапазон']
            part_df['ОПШГОИ_ГО_Значение'] = base_df['ГО_Значение']
            part_df['ОПШГОИ_ГО_Диапазон'] = base_df['ГО_Диапазон']

            out_answer_df = pd.concat([out_answer_df, answers_df], axis=1)  # Датафрейм для проверки

            # Соединяем анкетную часть с результатной
            base_df.sort_values(by='ИО_Значение', ascending=True, inplace=True)  # сортируем

            # Делаем свод  по  шкалам
            dct_svod_sub = {'ИО_Значение': 'ИО_Диапазон',
                            }

            dct_rename_svod_sub = {'ИО_Значение': 'Индивидуальная оценка уровня привлекательности класса для школьника',
                                   }

            lst_sub = ['от 5 до 8', 'от 9 до 12', 'от 13 до 16', 'от 17 до 19']

            base_svod_sub_df = create_union_svod(base_df, dct_svod_sub, dct_rename_svod_sub, lst_sub)

            # делаем копию датафрейма с ответами чтобы сделать сводные таблицы
            temp_answers_df = out_answer_df.copy()

            temp_answers_df['Счетчик'] = 1
            temp_answers_df['Третий'] = 1
            temp_answers_df['Четвертый'] = 1
            temp_answers_df['Пятый'] = 1


            # Первый вопрос
            dct_svod_first = {'Счетчик': 'Как вы оцениваете свою принадлежность классу?',
                            }

            dct_rename_svod_first = {'Счетчик': 'Как вы оцениваете свою принадлежность классу?',
                                   }

            lst_first = ['Делами класса не интересуюсь и участвовать в них не желаю',
                       'Не чувствую привязанности к классу и в его делах участвую редко',
                       'Участвую примерно в половине дел класса', 'Участвую в большинстве дел класса, но часть одноклассников делают это активнее меня',
                       'Считаю себя активным, полноправным членом класса']

            base_svod_first_df = create_union_svod_opg(temp_answers_df, dct_svod_first, dct_rename_svod_first, lst_first)

            # Второй вопрос
            dct_svod_second = {'Счетчик': 'Хотели бы вы перейти в другой класс, если бы предоставилась такая возможность?',
                            }

            dct_rename_svod_second = {'Счетчик': 'Хотели бы вы перейти в другой класс, если бы предоставилась такая возможность?',
                                   }

            lst_second = ['Очень хотел бы',
                       'Скорее всего перешел бы, чем остался',
                       'Не вижу никакой разницы', 'Скорее всего остался бы в своем классе',
                       'Очень хотел бы остаться в своем классе']

            base_svod_second_df = create_union_svod_opg(temp_answers_df, dct_svod_second, dct_rename_svod_second, lst_second)

            # 3,4,5 вопросы
            dct_svod_other = {'Третий': 'Взаимоотношения учащихся в вашем классе',
                              'Четвертый': 'Взаимоотношения учеников вашего класса с учителями',
                              'Пятый': 'Отношение одноклассников к учебе',
                            }

            dct_rename_svod_other = {'Третий': 'Взаимоотношения учащихся в вашем классе',
                                     'Четвертый': 'Взаимоотношения учеников вашего класса с учителями',
                                     'Пятый': 'Отношение одноклассников к учебе',

                                   }

            lst_other = ['Хуже, чем в других классах',
                       'Такие же, как в других классах',
                       'Лучше, чем в других классах',
                       ]

            base_svod_other_df = create_union_svod_opg(temp_answers_df, dct_svod_other, dct_rename_svod_other, lst_other)

            avg_vcha = round(base_df['ИО_Значение'].mean(), 2)

            avg_dct = {'Среднее значение Индивидуальная оценка уровня привлекательности класса для школьника': avg_vcha,
                       }

            avg_df = pd.DataFrame.from_dict(avg_dct, orient='index')
            avg_df = avg_df.reset_index()
            avg_df.columns = ['Показатель', 'Среднее значение']

            # формируем основной словарь
            out_dct = {'Списочный результат': base_df,
                       'Список для проверки': out_answer_df,
                       'Свод ИО': base_svod_sub_df,
                       '1_вопрос': base_svod_first_df,
                       '2_вопрос': base_svod_second_df,
                       '345_вопросы': base_svod_other_df,
                       'Среднее': avg_df,
                       }

            dct_prefix = {'ИО_Диапазон': 'ИО',
                          }

            out_dct = create_list_on_level(base_df, out_dct, lst_sub, dct_prefix)

            temp_answers_df.drop(columns=['Счетчик','Третий','Четвертый','Пятый'],inplace=True)


            dct_prefix_first = {'Как вы оцениваете свою принадлежность классу?': 'Первый',
                          }

            out_dct = create_list_on_level_first(temp_answers_df, out_dct, lst_first, dct_prefix_first)

            dct_prefix_second = {'Хотели бы вы перейти в другой класс, если бы предоставилась такая возможность?': 'Второй',
                          }

            out_dct = create_list_on_level_second(temp_answers_df, out_dct, lst_second, dct_prefix_second)

            dct_prefix_other = {'Взаимоотношения учащихся в вашем классе': 'Третий',
                                'Взаимоотношения учеников вашего класса с учителями': 'Четвертый',
                                'Отношение одноклассников к учебе': 'Пятый',
                          }

            out_dct = create_list_on_level_other(temp_answers_df, out_dct, lst_other, dct_prefix_other)

            return out_dct, part_df

        else:
            # Высчитываем по отдельности для каждой группы
            group_result_df = pd.pivot_table(base_df, index=lst_svod_cols,
                                             values=['ИО_Значение'],
                                             aggfunc=count_group_result)

            group_result_df = group_result_df.reset_index()
            group_result_df.rename(columns={'ИО_Значение': 'ГО_Значение'}, inplace=True)
            base_df['Порядок'] = range(1,len(base_df) + 1)  # сохраняем порядок
            base_df = base_df.merge(group_result_df, how='inner', on=lst_svod_cols)
            base_df = base_df.sort_values('Порядок').drop(columns=['Порядок'])  # восстанавливаем порядок
            base_df = base_df.reset_index(drop=True)
            base_df['ГО_Диапазон'] = base_df['ГО_Значение'].apply(calc_level_all)


            # Создаем датафрейм для создания части в общий датафрейм
            part_df = pd.DataFrame()

            part_df['ОПШГОИ_ИО_Значение'] = base_df['ИО_Значение']
            part_df['ОПШГОИ_ИО_Диапазон'] = base_df['ИО_Диапазон']
            part_df['ОПШГОИ_ГО_Значение'] = base_df['ГО_Значение']
            part_df['ОПШГОИ_ГО_Диапазон'] = base_df['ГО_Диапазон']

            out_answer_df = pd.concat([out_answer_df, answers_df], axis=1)  # Датафрейм для проверки

            # Соединяем анкетную часть с результатной
            base_df.sort_values(by='ИО_Значение', ascending=True, inplace=True)  # сортируем

            # Делаем свод  по  шкалам
            dct_svod_sub = {'ИО_Значение': 'ИО_Диапазон',
                            }

            dct_rename_svod_sub = {'ИО_Значение': 'Индивидуальная оценка уровня привлекательности класса для школьника',
                                   }

            lst_sub = ['от 5 до 8', 'от 9 до 12', 'от 13 до 16', 'от 17 до 19']

            base_svod_sub_df = create_union_svod(base_df, dct_svod_sub, dct_rename_svod_sub, lst_sub)


            dct_svod_t_sub = {'ГО_Значение': 'ГО_Диапазон',
                            }
            dct_rename_svod_t_sub = {'ГО_Значение': 'Групповая оценка уровня привлекательности класса',
                                   }
            lst_t_sub = ['5-7.99', '8-11.99', '12-15.99', '16-19']

            base_svod_t_sub_df = create_union_svod(base_df, dct_svod_t_sub, dct_rename_svod_t_sub, lst_t_sub)


            # делаем копию датафрейма с ответами, чтобы сделать сводные таблицы
            temp_answers_df = out_answer_df.copy()

            temp_answers_df['Счетчик'] = 1
            temp_answers_df['Третий'] = 1
            temp_answers_df['Четвертый'] = 1
            temp_answers_df['Пятый'] = 1

            # Первый вопрос
            dct_svod_first = {'Счетчик': 'Как вы оцениваете свою принадлежность классу?',
                              }

            dct_rename_svod_first = {'Счетчик': 'Как вы оцениваете свою принадлежность классу?',
                                     }

            lst_first = ['Делами класса не интересуюсь и участвовать в них не желаю',
                         'Не чувствую привязанности к классу и в его делах участвую редко',
                         'Участвую примерно в половине дел класса',
                         'Участвую в большинстве дел класса, но часть одноклассников делают это активнее меня',
                         'Считаю себя активным, полноправным членом класса']

            base_svod_first_df = create_union_svod_opg(temp_answers_df, dct_svod_first, dct_rename_svod_first, lst_first)

            # Второй вопрос
            dct_svod_second = {'Счетчик': 'Хотели бы вы перейти в другой класс, если бы предоставилась такая возможность?',
                               }

            dct_rename_svod_second = {
                'Счетчик': 'Хотели бы вы перейти в другой класс, если бы предоставилась такая возможность?',
                }

            lst_second = ['Очень хотел бы',
                          'Скорее всего перешел бы, чем остался',
                          'Не вижу никакой разницы', 'Скорее всего остался бы в своем классе',
                          'Очень хотел бы остаться в своем классе']

            base_svod_second_df = create_union_svod_opg(temp_answers_df, dct_svod_second, dct_rename_svod_second,
                                                        lst_second)

            # 3,4,5 вопросы
            dct_svod_other = {'Третий': 'Взаимоотношения учащихся в вашем классе',
                              'Четвертый': 'Взаимоотношения учеников вашего класса с учителями',
                              'Пятый': 'Отношение одноклассников к учебе',
                              }

            dct_rename_svod_other = {'Третий': 'Взаимоотношения учащихся в вашем классе',
                                     'Четвертый': 'Взаимоотношения учеников вашего класса с учителями',
                                     'Пятый': 'Отношение одноклассников к учебе',

                                     }

            lst_other = ['Хуже, чем в других классах',
                         'Такие же, как в других классах',
                         'Лучше, чем в других классах',
                         ]

            base_svod_other_df = create_union_svod_opg(temp_answers_df, dct_svod_other, dct_rename_svod_other, lst_other)

            avg_vcha = round(base_df['ИО_Значение'].mean(), 2)

            avg_dct = {'Среднее значение Индивидуальная оценка уровня привлекательности класса для школьника': avg_vcha,
                       }

            avg_df = pd.DataFrame.from_dict(avg_dct, orient='index')
            avg_df = avg_df.reset_index()
            avg_df.columns = ['Показатель', 'Среднее значение']

            # формируем основной словарь
            out_dct = {'Списочный результат': base_df,
                       'Список для проверки': out_answer_df,
                       'Свод ИО': base_svod_sub_df,
                       'Свод ГО': base_svod_t_sub_df,
                       '1_вопрос': base_svod_first_df,
                       '2_вопрос': base_svod_second_df,
                       '345_вопросы': base_svod_other_df,
                       'Среднее': avg_df,
                       }

            dct_prefix = {'ИО_Диапазон': 'ИО',
                          }

            out_dct = create_list_on_level(base_df, out_dct, lst_sub, dct_prefix)

            temp_answers_df.drop(columns=['Счетчик', 'Третий', 'Четвертый', 'Пятый'], inplace=True)

            dct_prefix_first = {'Как вы оцениваете свою принадлежность классу?': 'Первый',
                                }

            out_dct = create_list_on_level_first(temp_answers_df, out_dct, lst_first, dct_prefix_first)

            dct_prefix_second = {'Хотели бы вы перейти в другой класс, если бы предоставилась такая возможность?': 'Второй',
                                 }

            out_dct = create_list_on_level_second(temp_answers_df, out_dct, lst_second, dct_prefix_second)

            dct_prefix_other = {'Взаимоотношения учащихся в вашем классе': 'Третий',
                                'Взаимоотношения учеников вашего класса с учителями': 'Четвертый',
                                'Отношение одноклассников к учебе': 'Пятый',
                                }

            out_dct = create_list_on_level_other(temp_answers_df, out_dct, lst_other, dct_prefix_other)

            out_dct = create_result_opg_ivashkin(base_df, out_dct, lst_svod_cols)
            return out_dct, part_df


    except BadOrderOPSGOI:
        messagebox.showerror('Лахеcис',
                             f'При обработке вопросов теста Определение привлекательности для школьника группы одноклассников Ивашкин обнаружены неправильные вопросы. Проверьте названия колонок с вопросами:\n'
                             f'{error_order_message[:5000]}\n'
                             f'Используйте при создании Яндекс-формы написание вопросов из руководства пользователя программы Лахесис.')
    except BadValueOPSGOI:
        messagebox.showerror('Лахеcис',
                             f'При обработке вопросов теста ИОпределение привлекательности для школьника группы одноклассников Ивашкин обнаружены неправильные варианты ответов. Проверьте ответы на указанных строках:\n'
                             f'{error_message[:5000]}\n'
                             f'Используйте при создании Яндекс-формы написание вариантов ответа из руководства пользователя программы Лахесис.')


    except BadCountColumnsOPSGOI:
        messagebox.showerror('Лахеcис',
                             f'Проверьте количество колонок с ответами на тест Определение привлекательности для школьника группы одноклассников Ивашкин\n'
                             f'Должно быть 5 колонок с ответами')


