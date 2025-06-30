"""
Скрипт для обработки результатов теста Самооценка психического состояния Айзенка
"""

import pandas as pd
import re
from tkinter import messagebox
from lachesis_support_functions import round_mean,create_svod_sub


class BadOrderASMS(Exception):
    """
    Исключение для обработки случая когда колонки не совпадают
    """
    pass


class BadValueASMS(Exception):
    """
    Исключение для неправильных значений в вариантах ответов
    """
    pass

class BadCountColumnsASMS(Exception):
    """
    Исключение для обработки случая если количество колонок не равно 40
    """
    pass


def calc_sub_value_anxiety(row):
    """
    Функция для подсчета значения субшкалы Тревожность
    :param row: строка с ответами
    :return: число
    """
    lst_pr = [1,2,3,4,5,6,7,8,9,10]

    value_forward = 0 # счетчик прямых ответов

    for idx, value in enumerate(row):
        if idx +1 in lst_pr:
            value_forward += value

    return value_forward

def calc_level_sub_anxiety(value):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """
    if 0 <= value <= 7:
        return 'низкий уровень тревожности'
    elif 8 <= value <= 14:
        return 'средний уровень тревожности'
    else:
        return 'высокий уровень тревожности'


def calc_sub_value_frust(row):
    """
    Функция для подсчета значения субшкалы Фрустрация
    :param row: строка с ответами
    :return: число
    """
    lst_pr = [11,12,13,14,15,16,17,18,19,20]

    value_forward = 0 # счетчик прямых ответов

    for idx, value in enumerate(row):
        if idx +1 in lst_pr:
            value_forward += value

    return value_forward

def calc_level_sub_frust(value):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """
    if 0 <= value <= 7:
        return 'высокий уровень самооценки'
    elif 8 <= value <= 14:
        return 'средний уровень самооценки'
    else:
        return 'низкий уровень самооценки'



def calc_sub_value_agres(row):
    """
    Функция для подсчета значения субшкалы Агрессивность
    :param row: строка с ответами
    :return: число
    """
    lst_pr = [21,22,23,24,25,26,27,28,29,30]

    value_forward = 0 # счетчик прямых ответов

    for idx, value in enumerate(row):
        if idx +1 in lst_pr:
            value_forward += value

    return value_forward

def calc_level_sub_agres(value):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """
    if 0 <= value <= 7:
        return 'низкий уровень агрессивности'
    elif 8 <= value <= 14:
        return 'средний уровень агрессивности'
    else:
        return 'высокий уровень агрессивности'


def calc_sub_value_rig(row):
    """
    Функция для подсчета значения субшкалы Ригидность
    :param row: строка с ответами
    :return: число
    """
    lst_pr = [31,32,33,34,35,36,37,38,39,40]

    value_forward = 0 # счетчик прямых ответов

    for idx, value in enumerate(row):
        if idx +1 in lst_pr:
            value_forward += value

    return value_forward

def calc_level_sub_rig(value):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """
    if 0 <= value <= 7:
        return 'низкий уровень ригидности'
    elif 8 <= value <= 14:
        return 'средний уровень ригидности'
    else:
        return 'высокий уровень ригидности'


def calc_count_level_sub_anxiety(df:pd.DataFrame, lst_cat:list, val_cat, col_cat, lst_cols:list):
    """
    Функция для создания сводных датафреймов по субшкалам

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
    count_df['% низкий уровень тревожности от общего'] = round(
        count_df['низкий уровень тревожности'] / count_df['Итого'], 2) * 100
    count_df['% средний уровень тревожности от общего'] = round(
        count_df['средний уровень тревожности'] / count_df['Итого'], 2) * 100
    count_df['% высокий уровень тревожности от общего'] = round(
        count_df['высокий уровень тревожности'] / count_df['Итого'], 2) * 100

    return count_df


def calc_count_level_sub_frust(df:pd.DataFrame, lst_cat:list, val_cat, col_cat, lst_cols:list):
    """
    Функция для создания сводных датафреймов по субшкалам

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
    count_df['% низкий уровень самооценки от общего'] = round(
        count_df['низкий уровень самооценки'] / count_df['Итого'], 2) * 100
    count_df['% средний уровень самооценки от общего'] = round(
        count_df['средний уровень самооценки'] / count_df['Итого'], 2) * 100
    count_df['% высокий уровень самооценки от общего'] = round(
        count_df['высокий уровень самооценки'] / count_df['Итого'], 2) * 100

    return count_df


def calc_count_level_sub_agres(df:pd.DataFrame, lst_cat:list, val_cat, col_cat, lst_cols:list):
    """
    Функция для создания сводных датафреймов по субшкалам

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
    count_df['% низкий уровень агрессивности от общего'] = round(
        count_df['низкий уровень агрессивности'] / count_df['Итого'], 2) * 100
    count_df['% средний уровень агрессивности от общего'] = round(
        count_df['средний уровень агрессивности'] / count_df['Итого'], 2) * 100
    count_df['% высокий уровень агрессивности от общего'] = round(
        count_df['высокий уровень агрессивности'] / count_df['Итого'], 2) * 100

    return count_df


def calc_count_level_sub_rig(df:pd.DataFrame, lst_cat:list, val_cat, col_cat, lst_cols:list):
    """
    Функция для создания сводных датафреймов по субшкалам

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
    count_df['% низкий уровень ригидности от общего'] = round(
        count_df['низкий уровень ригидности'] / count_df['Итого'], 2) * 100
    count_df['% средний уровень ригидности от общего'] = round(
        count_df['средний уровень ригидности'] / count_df['Итого'], 2) * 100
    count_df['% высокий уровень ригидности от общего'] = round(
        count_df['высокий уровень ригидности'] / count_df['Итого'], 2) * 100

    return count_df









def create_result_asms(base_df:pd.DataFrame, out_dct:dict, lst_svod_cols:list):
    """
    Функция для подсчета результата если указаны колонки по которым нужно провести свод
    :param df: датафрейм с результатами
    :param out_dct: словарь с уже подсчитанными базовыми данными
    :param lst_svod_cols: список сводных колонок
    :return: словарь
    """
    # Тревожность
    lst_reindex_anxiety_level_cols = lst_svod_cols.copy()
    lst_reindex_anxiety_level_cols.extend( ['низкий уровень тревожности', 'средний уровень тревожности', 'высокий уровень тревожности',
                                   'Итого'])

    # Тревожность
    lst_reindex_frust_level_cols = lst_svod_cols.copy()
    lst_reindex_frust_level_cols.extend( ['низкий уровень самооценки', 'средний уровень самооценки', 'высокий уровень самооценки',
                                   'Итого'])

    # Тревожность
    lst_reindex_agres_level_cols = lst_svod_cols.copy()
    lst_reindex_agres_level_cols.extend( ['низкий уровень агрессивности', 'средний уровень агрессивности', 'высокий уровень агрессивности',
                                   'Итого'])

    # Тревожность
    lst_reindex_rig_level_cols = lst_svod_cols.copy()
    lst_reindex_rig_level_cols.extend( ['низкий уровень ригидности', 'средний уровень ригидности', 'высокий уровень ригидности',
                                   'Итого'])

    # Субшкалы
    svod_count_one_level_anxiety_df = calc_count_level_sub_anxiety(base_df, lst_svod_cols,
                                                      'Значение_субшкалы_Тревожность',
                                                      'Уровень_субшкалы_Тревожность',
                                                      lst_reindex_anxiety_level_cols)

    svod_count_one_level_frust_df = calc_count_level_sub_frust(base_df, lst_svod_cols,
                                                          'Значение_субшкалы_Фрустрация',
                                                          'Уровень_субшкалы_Фрустрация',
                                                          lst_reindex_frust_level_cols)

    svod_count_one_level_agres_df = calc_count_level_sub_agres(base_df, lst_svod_cols,
                                                         'Значение_субшкалы_Агрессивность',
                                                         'Уровень_субшкалы_Агрессивность',
                                                         lst_reindex_agres_level_cols)

    svod_count_one_level_rig_df = calc_count_level_sub_rig(base_df, lst_svod_cols,
                                                         'Значение_субшкалы_Ригидность',
                                                         'Уровень_субшкалы_Ригидность',
                                                         lst_reindex_rig_level_cols)

    # Считаем среднее по субшкалам
    svod_mean_df = pd.pivot_table(base_df,
                                  index=lst_svod_cols,
                                  values=['Значение_субшкалы_Тревожность',
                                          'Значение_субшкалы_Фрустрация',
                                          'Значение_субшкалы_Агрессивность',
                                          'Значение_субшкалы_Ригидность',
                                          ],
                                  aggfunc=round_mean)
    svod_mean_df.reset_index(inplace=True)
    # упорядочиваем колонки
    new_order_cols = lst_svod_cols.copy()
    new_order_cols.extend((['Значение_субшкалы_Тревожность', 'Значение_субшкалы_Фрустрация',
                            'Значение_субшкалы_Агрессивность', 'Значение_субшкалы_Ригидность',
                            ]))
    svod_mean_df = svod_mean_df.reindex(columns=new_order_cols)

    dct_rename_cols_mean = {'Значение_субшкалы_Тревожность': 'Ср. Тревожность',
                            'Значение_субшкалы_Фрустрация': 'Ср. Фрустрация',
                            'Значение_субшкалы_Агрессивность': 'Ср. Агрессивность',
                            'Значение_субшкалы_Ригидность': 'Ср. Ригидность' }
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

    out_dct.update({f'Ср {out_name}': svod_mean_df,
                    f'Свод Трев {out_name}': svod_count_one_level_anxiety_df,
                    f'Свод Фрус {out_name}': svod_count_one_level_frust_df,
                    f'Свод Агрес {out_name}': svod_count_one_level_agres_df,
                    f'Свод Риг {out_name}': svod_count_one_level_rig_df})

    if len(lst_svod_cols) == 1:
        return out_dct








def processing_aizenk_self_mental_state(result_df: pd.DataFrame, answers_df: pd.DataFrame, lst_svod_cols:list):
    """
    Функция для обработки
    :param result_df: часть датафрейма с описательными колонками
    :param answers_df: часть датафрейма с ответами
    :param lst_svod_cols:  список с колонками по которым нужно делать свод
    """
    out_answer_df = result_df.copy()  # делаем копию для последующего соединения с сырыми ответами
    if len(answers_df.columns) != 40:  # проверяем количество колонок с вопросами
        raise BadCountColumnsASMS

    # очищаем названия колонок от возможных сочетаний .1 которые добавляет пандас при одинаковых колонках
    clean_df_lst = []
    for name_column in answers_df.columns:
        clean_name = re.sub(r'.\d+$', '', name_column)
        clean_df_lst.append(clean_name)

    answers_df.columns = clean_df_lst

    lst_check_cols =['Часто я не уверен в своих силах','Нередко мне кажется безысходным положение, из которого можно было бы найти выход',
                     'Я часто оставляю за собой последнее слово','Мне трудно менять свои привычки',
                     'Я часто из-за пустяков краснею','Неприятности меня сильно расстраивают, и я падаю духом',
                     'Нередко в разговоре я перебиваю собеседника','Я с трудом переключаюсь с одного дела на другое',
                     'Я часто просыпаюсь ночью','При крупных неприятностях я виню только себя',
                     'Меня легко рассердить','Я очень осторожен по отношению к переменам в своей жизни',
                     'Я легко впадаю в уныние','Несчастия и неудачи меня ничему не учат',
                     'Мне приходится часто делать замечания другим','В споре меня трудно переубедить',
                     'Меня волнуют даже воображаемые неприятности','Я часто отказываюсь от борьбы, считая ее бесполезной',
                     'Я хочу быть авторитетом для окружающих','Нередко у меня не выходят из головы мысли, от которых следовало бы избавиться',
                     'Меня пугают трудности, с которыми мне придется встретиться в жизни','Нередко я чувствую себя беззащитным',
                     'В любом деле я не довольствуюсь малым, а хочу добиться максимального успеха','Я легко сближаюсь с людьми',
                     'Я часто копаюсь в своих недостатках','Иногда у меня бывают состояния отчаяния',
                     'Мне трудно сдерживать себя, когда я сержусь','Я сильно переживаю, если в моей жизни что-то неожиданно меняется',
                     'Меня легко убедить','Я чувствую растерянность, когда у меня возникают трудности',
                     'Я предпочитаю руководить, а не подчиняться','Нередко я проявляю упрямство',
                     'В трудные минуты я иногда веду себя по-детски','В трудные минуты жизни иногда веду себя по-детски, хочу, чтобы меня пожалели',
                     'У меня резкая, грубоватая жестикуляция','Я неохотно иду на риск',
                     'Я с трудом переношу время ожидания','Я думаю, что никогда не смогу исправить свои недостатки',
                     'Я мстителен','Меня расстраивают даже незначительные нарушения моих планов',
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
        raise BadOrderASMS

    # словарь для замены слов на числа
    dct_replace_value = {'не подходит': 0,
                         'не совсем': 1,
                         'подходит': 2,
}

    valid_values = [0, 1, 2]
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
        raise BadValueASMS

    base_df = pd.DataFrame()

    # Тревожность
    base_df['Значение_субшкалы_Тревожность'] = answers_df.apply(calc_sub_value_anxiety, axis=1)
    base_df['Уровень_субшкалы_Тревожность'] = base_df['Значение_субшкалы_Тревожность'].apply(calc_level_sub_anxiety)

    # Фрустрация
    base_df['Значение_субшкалы_Фрустрация'] = answers_df.apply(calc_sub_value_frust, axis=1)
    base_df['Уровень_субшкалы_Фрустрация'] = base_df['Значение_субшкалы_Фрустрация'].apply(calc_level_sub_frust)

    # Агрессивность
    base_df['Значение_субшкалы_Агрессивность'] = answers_df.apply(calc_sub_value_agres, axis=1)
    base_df['Уровень_субшкалы_Агрессивность'] = base_df['Значение_субшкалы_Агрессивность'].apply(calc_level_sub_agres)

    # Ригидность
    base_df['Значение_субшкалы_Ригидность'] = answers_df.apply(calc_sub_value_rig, axis=1)
    base_df['Уровень_субшкалы_Ригидность'] = base_df['Значение_субшкалы_Ригидность'].apply(calc_level_sub_rig)

 # Создаем датафрейм для создания части в общий датафрейм
    part_df = pd.DataFrame()

    part_df['АСПС_Тревожность_Значение'] = base_df['Значение_субшкалы_Тревожность']
    part_df['АСПС_Тревожность_Уровень'] = base_df['Уровень_субшкалы_Тревожность']

    part_df['АСПС_Фрустрация_Значение'] = base_df['Значение_субшкалы_Фрустрация']
    part_df['АСПС_Фрустрация_Уровень'] = base_df['Уровень_субшкалы_Фрустрация']

    part_df['АСПС_Агрессивность_Значение'] = base_df['Значение_субшкалы_Агрессивность']
    part_df['АСПС_Агрессивность_Уровень'] = base_df['Уровень_субшкалы_Агрессивность']

    part_df['АСПС_Ригидность_Значение'] = base_df['Значение_субшкалы_Ригидность']
    part_df['АСПС_Ригидность_Уровень'] = base_df['Уровень_субшкалы_Ригидность']

    # Соединяем анкетную часть с результатной
    base_df = pd.concat([result_df, base_df], axis=1)
    base_df.sort_values(by='Значение_субшкалы_Тревожность', ascending=False, inplace=True)  # сортируем

    # Списки для субшкал
    lst_anxiety = ['низкий уровень тревожности','средний уровень тревожности','высокий уровень тревожности']
    lst_frust = ['низкий уровень самооценки','средний уровень самооценки','высокий уровень самооценки']
    lst_agres = ['низкий уровень агрессивности','средний уровень агрессивности','высокий уровень агрессивности']
    lst_rig = ['низкий уровень ригидности','средний уровень ригидности','высокий уровень ригидности']

    # считаем среднее значение по субшкалам
    avg_anxiety = round(base_df['Значение_субшкалы_Тревожность'].mean(), 2)
    avg_frust = round(base_df['Значение_субшкалы_Фрустрация'].mean(), 2)
    avg_agres = round(base_df['Значение_субшкалы_Агрессивность'].mean(), 2)
    avg_rig = round(base_df['Значение_субшкалы_Ригидность'].mean(), 2)

    avg_dct = {'Среднее значение субшкалы Тревожность': avg_anxiety,
               'Среднее значение субшкалы Фрустрация': avg_frust,
               'Среднее значение субшкалы Агрессивность': avg_agres,
               'Среднее значение субшкалы Ригидность': avg_rig,
               }

    avg_df = pd.DataFrame.from_dict(avg_dct, orient='index')
    avg_df = avg_df.reset_index()
    avg_df.columns = ['Показатель', 'Среднее значение']
    # формируем основной словарь
    out_dct = {'Списочный результат': base_df, 'Список для проверки': out_answer_df,
               'Среднее по субшкалам': avg_df,
               }



    base_svod_anxiety_df = create_svod_sub(base_df, lst_anxiety, 'Уровень_субшкалы_Тревожность',
                                      'Значение_субшкалы_Тревожность', 'count')
    base_svod_frust_df = create_svod_sub(base_df, lst_frust, 'Уровень_субшкалы_Фрустрация',
                                      'Значение_субшкалы_Фрустрация', 'count')
    base_svod_agres_df = create_svod_sub(base_df, lst_agres, 'Уровень_субшкалы_Агрессивность',
                                      'Значение_субшкалы_Агрессивность', 'count')
    base_svod_rig_df = create_svod_sub(base_df, lst_rig, 'Уровень_субшкалы_Ригидность',
                                      'Значение_субшкалы_Ригидность', 'count')
    # Тревожность
    out_dct.update({'Свод Тревожность':base_svod_anxiety_df})

    dct_anxiety = dict()
    for level in lst_anxiety:
        temp_df = base_df[base_df['Уровень_субшкалы_Тревожность'] == level]
        if temp_df.shape[0] != 0:
            dct_anxiety[level] = temp_df

    out_dct.update(dct_anxiety)

    # Фрустрация
    out_dct.update({'Свод Фрустрация':base_svod_frust_df})

    dct_frust = dict()
    for level in lst_frust:
        temp_df = base_df[base_df['Уровень_субшкалы_Фрустрация'] == level]
        if temp_df.shape[0] != 0:
            dct_frust[level] = temp_df

    out_dct.update(dct_frust)

    # Агрессивность
    out_dct.update({'Свод Агрессивность':base_svod_agres_df})

    dct_agres = dict()
    for level in lst_agres:
        temp_df = base_df[base_df['Уровень_субшкалы_Агрессивность'] == level]
        if temp_df.shape[0] != 0:
            dct_agres[level] = temp_df

    out_dct.update(dct_agres)

    # Ригидность
    out_dct.update({'Свод Ригидность':base_svod_rig_df})

    dct_rig = dict()
    for level in lst_rig:
        temp_df = base_df[base_df['Уровень_субшкалы_Ригидность'] == level]
        if temp_df.shape[0] != 0:
            dct_rig[level] = temp_df

    out_dct.update(dct_rig)

    """
        Сохраняем в зависимости от необходимости делать своды по определенным колонкам
        """
    if len(lst_svod_cols) == 0:
        return out_dct, part_df
    else:
        out_dct = create_result_asms(base_df, out_dct, lst_svod_cols)

        return out_dct, part_df





















