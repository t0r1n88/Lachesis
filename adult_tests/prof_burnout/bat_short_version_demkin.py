"""
Скрипт для обработки результатов теста BAT краткая версия Демкин
"""

import pandas as pd
import re
from tkinter import messagebox
from lachesis_support_functions import round_mean,create_svod_sub

class BadOrderSBATD(Exception):
    """
    Исключение для обработки случая когда колонки не совпадают
    """
    pass


class BadValueSBATD(Exception):
    """
    Исключение для неправильных значений в вариантах ответов
    """
    pass

class BadCountColumnsSBATD(Exception):
    """
    Исключение для обработки случая если количество колонок не равно 12
    """
    pass


def calc_level_exhaustion(value):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """
    if 1.0 <= value <= 1.66:
        return 'низкий уровень'
    elif 1.67 <= value <= 2.99:
        return 'средний уровень'
    elif 3.0 <= value <= 3.99:
        return 'высокий уровень'
    else:
        return 'очень высокий уровень'


def calc_level_distance(value):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """
    if value == 1.0:
        return 'низкий уровень'
    elif 1.01 <= value <= 2.65:
        return 'средний уровень'
    elif 2.66 <= value <= 3.99:
        return 'высокий уровень'
    else:
        return 'очень высокий уровень'


def calc_level_cog_problem(value):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """
    if 1.0 <=value <= 1.66:
        return 'низкий уровень'
    elif 1.67 <= value <= 2.33:
        return 'средний уровень'
    elif 2.34 <= value <= 3.32:
        return 'высокий уровень'
    else:
        return 'очень высокий уровень'

def calc_level_emo_problem(value):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """
    if value == 1.0:
        return 'низкий уровень'
    elif 1.01 <= value <= 2.0:
        return 'средний уровень'
    elif 2.01 <= value <= 3.0:
        return 'высокий уровень'
    else:
        return 'очень высокий уровень'


def calc_level_burnout(value):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """
    if 1.0 <=value <= 1.50:
        return 'низкий уровень'
    elif 1.51 <= value <= 2.35:
        return 'средний уровень'
    elif 2.36 <= value <= 3.17:
        return 'высокий уровень'
    else:
        return 'очень высокий уровень'

def calc_count_level_bat_short(df:pd.DataFrame, lst_cat:list, val_cat, col_cat, lst_cols:list):
    """
    Функция для создания сводных датафреймов

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
    count_df['% низкий уровень от общего'] = round(
        count_df['низкий уровень'] / count_df['Итого'], 2) * 100
    count_df['% средний уровень от общего'] = round(
        count_df['средний уровень'] / count_df['Итого'], 2) * 100
    count_df['% высокий уровень от общего'] = round(
        count_df['высокий уровень'] / count_df['Итого'], 2) * 100
    count_df['% очень высокий уровень от общего'] = round(
        count_df['очень высокий уровень'] / count_df['Итого'], 2) * 100

    return count_df






def create_result_sbatd(base_df:pd.DataFrame, out_dct:dict, lst_svod_cols:list):
    """
    Функция для подсчета результата если указаны колонки по которым нужно провести свод
    :param df: датафрейм с результатами
    :param out_dct: словарь с уже подсчитанными базовыми данными
    :param lst_svod_cols: список сводных колонок
    :return: словарь
    """
    # Шкала
    lst_reindex_main_level_cols = lst_svod_cols.copy()
    lst_reindex_main_level_cols.extend(['низкий уровень', 'средний уровень',
           'высокий уровень', 'очень высокий уровень','Итого'])


    svod_count_one_level_df = calc_count_level_bat_short(base_df, lst_svod_cols, 'Значение_профессионального_выгорания',
                                                    'Уровень_профессионального_выгорания',
                                                         lst_reindex_main_level_cols)

    svod_count_one_level_exhaustion_df = calc_count_level_bat_short(base_df, lst_svod_cols, 'Значение_Истощение',
                                                    'Уровень_Истощение',
                                                         lst_reindex_main_level_cols)
    svod_count_one_level_distance_df = calc_count_level_bat_short(base_df, lst_svod_cols, 'Значение_Дистанцирование',
                                                    'Уровень_Дистанцирование',
                                                         lst_reindex_main_level_cols)
    svod_count_one_level_cog_problem_df = calc_count_level_bat_short(base_df, lst_svod_cols, 'Значение_Когнитивные_проблемы',
                                                    'Уровень_Когнитивные_проблемы',
                                                         lst_reindex_main_level_cols)
    svod_count_one_level_emo_problem_df = calc_count_level_bat_short(base_df, lst_svod_cols, 'Значение_Эмоциональные_проблемы',
                                                    'Уровень_Эмоциональные_проблемы',
                                                         lst_reindex_main_level_cols)

    svod_mean_df = pd.pivot_table(base_df,
                                  index=lst_svod_cols,
                                  values=['Значение_профессионального_выгорания',
                                          'Значение_Истощение',
                                          'Значение_Дистанцирование',
                                          'Значение_Когнитивные_проблемы',
                                          'Значение_Эмоциональные_проблемы'],
                                  aggfunc=round_mean)

    svod_mean_df.reset_index(inplace=True)
    new_order_cols = lst_svod_cols.copy()
    new_order_cols.extend(['Значение_профессионального_выгорания', 'Значение_Истощение',
                           'Значение_Дистанцирование','Значение_Когнитивные_проблемы','Значение_Эмоциональные_проблемы'])
    svod_mean_df = svod_mean_df.reindex(columns=new_order_cols)
    dct_rename_cols_mean = {'Значение_профессионального_выгорания': 'Ср. профессионального выгорания',
                            'Значение_Истощение': 'Ср. истощения',
                            'Значение_Дистанцирование': 'Ср. дистанцирования',
                            'Значение_Когнитивные_проблемы': 'Ср. когнитивных проблем',
                            'Значение_Эмоциональные_проблемы': 'Ср. эмоциональных проблем'}

    svod_mean_df.rename(columns=dct_rename_cols_mean, inplace=True)

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

    out_dct.update({f'Свод {out_name}': svod_count_one_level_df,
                    f'Ср. {out_name}': svod_mean_df,
                    f'Свод Истощение {out_name}': svod_count_one_level_exhaustion_df,
                    f'Свод Дис-ние {out_name}': svod_count_one_level_distance_df,
                    f'Свод КП {out_name}': svod_count_one_level_cog_problem_df,
                    f'Свод ЭП {out_name}': svod_count_one_level_emo_problem_df,
                     })

    if len(lst_svod_cols) == 1:
        return out_dct
    else:
        for idx, name_column in enumerate(lst_svod_cols):
            lst_reindex_main_level_cols = [lst_svod_cols[idx], 'низкий уровень', 'средний уровень',
           'высокий уровень', 'очень высокий уровень','Итого']  # Основная шкала

            svod_count_column_level_df = calc_count_level_bat_short(base_df, [lst_svod_cols[idx]],
                                                                    'Значение_профессионального_выгорания',
                                                                    'Уровень_профессионального_выгорания',
                                                                    lst_reindex_main_level_cols)

            svod_count_column_level_exhaustion_df = calc_count_level_bat_short(base_df, [lst_svod_cols[idx]],
                                                                               'Значение_Истощение',
                                                                               'Уровень_Истощение',
                                                                               lst_reindex_main_level_cols)
            svod_count_column_level_distance_df = calc_count_level_bat_short(base_df, [lst_svod_cols[idx]],
                                                                             'Значение_Дистанцирование',
                                                                             'Уровень_Дистанцирование',
                                                                             lst_reindex_main_level_cols)
            svod_count_column_level_cog_problem_df = calc_count_level_bat_short(base_df, [lst_svod_cols[idx]],
                                                                                'Значение_Когнитивные_проблемы',
                                                                                'Уровень_Когнитивные_проблемы',
                                                                                lst_reindex_main_level_cols)
            svod_count_column_level_emo_problem_df = calc_count_level_bat_short(base_df, [lst_svod_cols[idx]],
                                                                                'Значение_Эмоциональные_проблемы',
                                                                                'Уровень_Эмоциональные_проблемы',
                                                                                lst_reindex_main_level_cols)

            svod_mean_column_df = pd.pivot_table(base_df,
                                          index=[lst_svod_cols[idx]],
                                          values=['Значение_профессионального_выгорания',
                                                  'Значение_Истощение',
                                                  'Значение_Дистанцирование',
                                                  'Значение_Когнитивные_проблемы',
                                                  'Значение_Эмоциональные_проблемы'],
                                          aggfunc=round_mean)

            svod_mean_column_df.reset_index(inplace=True)
            new_order_cols = [lst_svod_cols[idx]].copy()

            new_order_cols.extend(['Значение_профессионального_выгорания', 'Значение_Истощение',
                                   'Значение_Дистанцирование', 'Значение_Когнитивные_проблемы',
                                   'Значение_Эмоциональные_проблемы'])
            svod_mean_column_df = svod_mean_column_df.reindex(columns=new_order_cols)
            dct_rename_cols_mean = {'Значение_профессионального_выгорания': 'Ср. профессионального выгорания',
                                    'Значение_Истощение': 'Ср. истощения',
                                    'Значение_Дистанцирование': 'Ср. дистанцирования',
                                    'Значение_Когнитивные_проблемы': 'Ср. когнитивных проблем',
                                    'Значение_Эмоциональные_проблемы': 'Ср. эмоциональных проблем'}

            svod_mean_column_df.rename(columns=dct_rename_cols_mean, inplace=True)

            name_column = lst_svod_cols[idx]
            name_column = re.sub(r'[\[\]\'+()<> :"?*|\\/]', '_', name_column)
            name_column = name_column[:15]

            out_dct.update({f'Свод {name_column}': svod_count_column_level_df,
                            f'Ср. {name_column}': svod_mean_column_df,
                            f'Свод Истощение {name_column}': svod_count_column_level_exhaustion_df,
                            f'Свод Дис-ние {name_column}': svod_count_column_level_distance_df,
                            f'Свод КП {name_column}': svod_count_column_level_cog_problem_df,
                            f'Свод ЭП {name_column}': svod_count_column_level_emo_problem_df,
                            })
        return out_dct














def processing_short_bat_demkin(result_df: pd.DataFrame, answers_df: pd.DataFrame, lst_svod_cols:list):
    """
    Функция для обработки
    :param result_df: часть датафрейма с описательными колонками
    :param answers_df: часть датафрейма с ответами
    :param lst_svod_cols:  список с колонками по которым нужно делать свод
    """
    try:
        out_answer_df = result_df.copy()  # делаем копию для последующего соединения с сырыми ответами
        if len(answers_df.columns) != 12:  # проверяем количество колонок с вопросами
            raise BadCountColumnsSBATD

        # очищаем названия колонок от возможных сочетаний .1 которые добавляет пандас при одинаковых колонках
        clean_df_lst = []
        for name_column in answers_df.columns:
            clean_name = re.sub(r'.\d+$', '', name_column)
            clean_df_lst.append(clean_name)

        answers_df.columns = clean_df_lst

        lst_check_cols = ['На работе я чувствую себя морально истощенным','Все, что я делаю на работе, требует больших усилий','После рабочего дня мне трудно восстановить свои силы',
                          'Я изо всех сил пытаюсь проявить хоть какой-то энтузиазм в своей работе','Я испытываю сильное отвращение к своей работе','Я цинично отношусь к тому, что моя работа значит для других',
                          'На работе мне трудно концентрироваться на задаче','Когда я работаю, мне трудно сосредоточиться','Я совершаю ошибки в своей работе, потому что мои мысли заняты другими вещами',
                          'На работе я чувствую, что не могу контролировать свои эмоции','Я не узнаю себя по тому, как эмоционально реагирую на все на работе','На работе я могу непреднамеренно слишком остро реагировать'
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
            raise BadOrderSBATD

        # словарь для замены слов на числа
        dct_replace_value = {'никогда': 1,
                             'редко': 2,
                             'иногда': 3,
                             'часто': 4,
                             'всегда': 5,
                             }

        valid_values = [1, 2, 3, 4, 5]
        answers_df.replace(dct_replace_value, inplace=True)  # заменяем слова на цифры для подсчетов
        # Проверяем, есть ли значения, отличающиеся от указанных в списке
        lst_error_answers = []  # список для хранения строк где найдены неправильные ответы

        for i in range(12):
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
            raise BadValueSBATD


        base_df = pd.DataFrame()
        base_df['Значение_Истощение'] = round(answers_df.iloc[:,0:3].sum(axis=1) / 3,2)
        base_df['Уровень_Истощение'] = base_df['Значение_Истощение'].apply(calc_level_exhaustion)

        base_df['Значение_Дистанцирование'] = round(answers_df.iloc[:,3:6].sum(axis=1)/3,2)
        base_df['Уровень_Дистанцирование'] = base_df['Значение_Дистанцирование'].apply(calc_level_distance)

        base_df['Значение_Когнитивные_проблемы'] = round(answers_df.iloc[:,6:9].sum(axis=1)/3,2)
        base_df['Уровень_Когнитивные_проблемы'] = base_df['Значение_Когнитивные_проблемы'].apply(calc_level_cog_problem)

        base_df['Значение_Эмоциональные_проблемы'] = round(answers_df.iloc[:,9:12].sum(axis=1)/3,2)
        base_df['Уровень_Эмоциональные_проблемы'] = base_df['Значение_Эмоциональные_проблемы'].apply(calc_level_emo_problem)

        base_df['Значение_профессионального_выгорания'] = round(answers_df.sum(axis=1)/12,2)
        base_df['Уровень_профессионального_выгорания'] = base_df['Значение_профессионального_выгорания'].apply(calc_level_burnout)

        # Создаем датафрейм для создания части в общий датафрейм
        part_df = pd.DataFrame()
        part_df['БАТКД_Значение_профессионального_выгорания'] = base_df['Значение_профессионального_выгорания']
        part_df['БАТКД_Уровень_профессионального_выгорания'] = base_df['Уровень_профессионального_выгорания']

        part_df['БАТКД_Значение_И'] = base_df['Значение_Истощение']
        part_df['БАТКД_Уровень_И'] = base_df['Уровень_Истощение']

        part_df['БАТКД_Значение_Д'] = base_df['Значение_Дистанцирование']
        part_df['БАТКД_Уровень_Д'] = base_df['Уровень_Дистанцирование']

        part_df['БАТКД_КП'] = base_df['Значение_Когнитивные_проблемы']
        part_df['БАТКД_КП'] = base_df['Уровень_Когнитивные_проблемы']

        part_df['БАТКД_ЭП'] = base_df['Значение_Эмоциональные_проблемы']
        part_df['БАТКД_ЭП'] = base_df['Уровень_Эмоциональные_проблемы']

        new_order_cols = ['Значение_профессионального_выгорания','Уровень_профессионального_выгорания',
                          'Значение_Истощение','Уровень_Истощение',
                          'Значение_Дистанцирование','Уровень_Дистанцирование',
                          'Значение_Когнитивные_проблемы','Уровень_Когнитивные_проблемы',
                          'Значение_Эмоциональные_проблемы','Уровень_Эмоциональные_проблемы',
                          ]

        base_df = base_df.reindex(columns=new_order_cols)
        # Соединяем анкетную часть с результатной
        base_df = pd.concat([result_df, base_df], axis=1)

        base_df.sort_values(by='Значение_профессионального_выгорания', ascending=False, inplace=True)  # сортируем
        out_answer_df = pd.concat([out_answer_df, answers_df], axis=1)  # Датафрейм для проверки

        # Общий свод по уровням общей шкалы всего в процентном соотношении
        base_svod_all_df = pd.DataFrame(
            index=['низкий уровень', 'средний уровень',
                   'высокий уровень','очень высокий уровень'])

        svod_level_df = pd.pivot_table(base_df, index='Уровень_профессионального_выгорания',
                                       values='Значение_профессионального_выгорания',
                                       aggfunc='count')

        svod_level_df['% от общего'] = round(
            svod_level_df['Значение_профессионального_выгорания'] / svod_level_df[
                'Значение_профессионального_выгорания'].sum(), 3) * 100

        base_svod_all_df = base_svod_all_df.join(svod_level_df)

        # # Создаем суммирующую строку
        base_svod_all_df.loc['Итого'] = svod_level_df.sum()
        base_svod_all_df.reset_index(inplace=True)
        base_svod_all_df.rename(columns={'index': 'Уровень', 'Значение_профессионального_выгорания': 'Количество'},
                                inplace=True)
        # формируем основной словарь
        out_dct = {'Списочный результат': base_df, 'Список для проверки': out_answer_df,
                   'Свод Общий': base_svod_all_df,
                   }

        lst_level = ['низкий уровень', 'средний уровень',
                   'высокий уровень','очень высокий уровень']
        dct_level = dict()

        for level in lst_level:
            temp_df = base_df[base_df['Уровень_профессионального_выгорания'] == level]
            if temp_df.shape[0] != 0:
                dct_level[level] = temp_df

        out_dct.update(dct_level)

        # Свод по шкалам
        base_svod_exhaustion = create_svod_sub(base_df, lst_level, 'Уровень_Истощение',
                            'Значение_Истощение', 'count')
        base_svod_distance = create_svod_sub(base_df, lst_level, 'Уровень_Дистанцирование',
                            'Значение_Дистанцирование', 'count')
        base_svod_cog_problem = create_svod_sub(base_df, lst_level, 'Уровень_Когнитивные_проблемы',
                            'Значение_Когнитивные_проблемы', 'count')
        base_svod_emo_problem = create_svod_sub(base_df, lst_level, 'Уровень_профессионального_выгорания',
                            'Значение_Эмоциональные_проблемы', 'count')


     # считаем среднее значение по  шкале субшкалам

        avg_all = round(base_df['Значение_профессионального_выгорания'].mean(),2)
        avg_exhaustion = round(base_df['Значение_Истощение'].mean(),2)
        avg_distance= round(base_df['Значение_Дистанцирование'].mean(),2)
        avg_cog_problem = round(base_df['Значение_Когнитивные_проблемы'].mean(),2)
        avg_emo_problem= round(base_df['Значение_Эмоциональные_проблемы'].mean(),2)

        avg_dct = {'Среднее значение профессионального выгорания':avg_all,
                   'Среднее значение Истощение': avg_exhaustion,
                   'Среднее значение Дистанцирование': avg_distance,
                   'Среднее значение Когнитивные проблемы': avg_cog_problem,
                   'Среднее значение Эмоциональные проблемы': avg_emo_problem,
                   }

        avg_df = pd.DataFrame.from_dict(avg_dct, orient='index')
        avg_df = avg_df.reset_index()
        avg_df.columns = ['Показатель','Среднее значение']

        out_dct.update({'Свод Истощение':base_svod_exhaustion,
                        'Свод Дистанцирование': base_svod_distance,
                        'Свод Когнитивные проблемы':base_svod_cog_problem,
                        'Свод Эмоциональные проблемы':base_svod_emo_problem,
                        'Среднее по субшкалам':avg_df}
                       )

        if len(lst_svod_cols) == 0:
            return out_dct, part_df
        else:
            out_dct = create_result_sbatd(base_df, out_dct, lst_svod_cols)

            return out_dct, part_df

    except BadOrderSBATD:
        messagebox.showerror('Лахеcис',
                             f'При обработке вопросов теста BAT краткая версия Демкин обнаружены неправильные вопросы. Проверьте названия колонок с вопросами:\n'
                             f'{error_order_message}\n'
                             f'Используйте при создании Яндекс-формы написание вопросов из руководства пользователя программы Лахесис.')
    except BadValueSBATD:
        messagebox.showerror('Лахеcис',
                             f'При обработке вопросов теста BAT краткая версия Демкин обнаружены неправильные варианты ответов. Проверьте ответы на указанных строках:\n'
                             f'{error_message}\n'
                             f'Используйте при создании Яндекс-формы написание вариантов ответа из руководства пользователя программы Лахесис.')


    except BadCountColumnsSBATD:
        messagebox.showerror('Лахеcис',
                             f'Проверьте количество колонок с ответами на тест BAT краткая версия Демкин\n'
                             f'Должно быть 12 колонок с ответами')


















