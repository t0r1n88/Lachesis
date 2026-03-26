"""
Скрипт для обработки результатов Диагностика мотивации учения и эмоционального отношения к учению в средних и старших классах школы Прихожан
"""

import pandas as pd
import re
from tkinter import messagebox
from lachesis_support_functions import round_mean_two,calc_count_scale,create_union_svod, create_list_on_level

class BadOrderDMUAOUP(Exception):
    """
    Исключение для обработки случая когда колонки не совпадают
    """
    pass


class BadValueDMUAOUP(Exception):
    """
    Исключение для неправильных значений в вариантах ответов
    """
    pass

class NotReqColumnDMUAOUP(Exception):
    """
    Исключение для обработки случая когда нет обязательных колонок Пол
    """
    pass


class BadValueSexDMUAOUp(Exception):
    """
    Исключение для обработки случая когда в колонке Пол есть значения отличающиеся от Мужской или Женский
    """
    pass

class BadValueAgeDMUAOUP(Exception):
    """
    Исключение для обработки случая когда в колонке Возраст есть значения отличающиеся от
    """
    pass


class BadCountColumnsDMUAOUP(Exception):
    """
    Исключение для обработки случая если количество колонок не равно 40
    """
    pass

def calc_value_pa(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [2,6,10,14,18,22,26,30,34,38]
    lst_neg = [14,30,38]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_pr:
            if idx not in lst_neg:
                value_forward += value
            else:
                if value == 1:
                    value_forward += 4
                elif value == 2:
                    value_forward += 3
                elif value == 3:
                    value_forward += 2
                else:
                    value_forward += 1


    return value_forward


def calc_level_pa(row:pd.Series):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """
    sex,age, value = row

    if age == '10-11 лет':
        if sex == 'Женский':
            if 31<= value <=40:
                return f'высокий'
            elif 21<= value <=30:
                return f'средний'
            else:
                return f'низкий'
        else:
            if 28<= value <=40:
                return f'высокий'
            elif 22<= value <=27:
                return f'средний'
            else:
                return f'низкий'
    elif age == '12-14 лет':
        if sex == 'Женский':
            if 28<= value <=40:
                return f'высокий'
            elif 21<= value <=27:
                return f'средний'
            else:
                return f'низкий'
        else:
            if 27<= value <=40:
                return f'высокий'
            elif 19<= value <=26:
                return f'средний'
            else:
                return f'низкий'
    else:
        if sex == 'Женский':
            if 29<= value <=40:
                return f'высокий'
            elif 18<= value <=28:
                return f'средний'
            else:
                return f'низкий'
        else:
            if 31<= value <=40:
                return f'высокий'
            elif 21<= value <=30:
                return f'средний'
            else:
                return f'низкий'



def calc_value_md(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [4,8,12,16,20,24,28,32,36,40]
    lst_neg = [4,20,32]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_pr:
            if idx not in lst_neg:
                value_forward += value
            else:
                if value == 1:
                    value_forward += 4
                elif value == 2:
                    value_forward += 3
                elif value == 3:
                    value_forward += 2
                else:
                    value_forward += 1


    return value_forward


def calc_level_md(row:pd.Series):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """
    sex,age, value = row

    if age == '10-11 лет':
        if sex == 'Женский':
            if 32<= value <=40:
                return f'высокий'
            elif 22<= value <=31:
                return f'средний'
            else:
                return f'низкий'
        else:
            if 29<= value <=40:
                return f'высокий'
            elif 21<= value <=28:
                return f'средний'
            else:
                return f'низкий'
    elif age == '12-14 лет':
        if sex == 'Женский':
            if 31<= value <=40:
                return f'высокий'
            elif 23<= value <=30:
                return f'средний'
            else:
                return f'низкий'
        else:
            if 25<= value <=40:
                return f'высокий'
            elif 18<= value <=24:
                return f'средний'
            else:
                return f'низкий'
    else:
        if sex == 'Женский':
            if 31<= value <=40:
                return f'высокий'
            elif 22<= value <=30:
                return f'средний'
            else:
                return f'низкий'
        else:
            if 26<= value <=40:
                return f'высокий'
            elif 18<= value <=25:
                return f'средний'
            else:
                return f'низкий'


def calc_value_t(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [1,5,9,13,17,21,25,29,33,37]
    lst_neg = [1,9,25,33]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_pr:
            if idx not in lst_neg:
                value_forward += value
            else:
                if value == 1:
                    value_forward += 4
                elif value == 2:
                    value_forward += 3
                elif value == 3:
                    value_forward += 2
                else:
                    value_forward += 1


    return value_forward

def calc_level_t(row:pd.Series):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """
    sex,age, value = row

    if age == '10-11 лет':
        if sex == 'Женский':
            if 27<= value <=40:
                return f'высокий'
            elif 20<= value <=26:
                return f'средний'
            else:
                return f'низкий'
        else:
            if 24<= value <=40:
                return f'высокий'
            elif 17<= value <=23:
                return f'средний'
            else:
                return f'низкий'
    elif age == '12-14 лет':
        if sex == 'Женский':
            if 25<= value <=40:
                return f'высокий'
            elif 19<= value <=24:
                return f'средний'
            else:
                return f'низкий'
        else:
            if 26<= value <=40:
                return f'высокий'
            elif 19<= value <=25:
                return f'средний'
            else:
                return f'низкий'
    else:
        if sex == 'Женский':
            if 25<= value <=40:
                return f'высокий'
            elif 17<= value <=24:
                return f'средний'
            else:
                return f'низкий'
        else:
            if 23<= value <=40:
                return f'высокий'
            elif 16<= value <=22:
                return f'средний'
            else:
                return f'низкий'


def calc_value_g(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [3,7,11,15,19,23,27,31,35,39]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_pr:
            value_forward += value


    return value_forward



def calc_level_g(row:pd.Series):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """
    sex,age, value = row

    if age == '10-11 лет':
        if sex == 'Женский':
            if 21<= value <=40:
                return f'высокий'
            elif 14<= value <=20:
                return f'средний'
            else:
                return f'низкий'
        else:
            if 20<= value <=40:
                return f'высокий'
            elif 13<= value <=19:
                return f'средний'
            else:
                return f'низкий'
    elif age == '12-14 лет':
        if sex == 'Женский':
            if 20<= value <=40:
                return f'высокий'
            elif 14<= value <=19:
                return f'средний'
            else:
                return f'низкий'
        else:
            if 23<= value <=40:
                return f'высокий'
            elif 15<= value <=22:
                return f'средний'
            else:
                return f'низкий'
    else:
        if sex == 'Женский':
            if 21<= value <=40:
                return f'высокий'
            elif 14<= value <=20:
                return f'средний'
            else:
                return f'низкий'
        else:
            if 19<= value <=40:
                return f'высокий'
            elif 12<= value <=18:
                return f'средний'
            else:
                return f'низкий'

def calc_base_level(value):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """
    if 45<= value <= 60:
        return f'I уровень'
    elif 29 <= value <= 44:
        return f'II уровень'
    elif 13 <= value <= 28:
        return f'III уровень'
    elif -2 <= value <= 12:
        return f'IV уровень'
    else:
        return f'V уровень'


def create_result_dmuaou_prihogan(base_df:pd.DataFrame, out_dct:dict, lst_svod_cols:list):
    """
    Функция для подсчета результата если указаны колонки по которым нужно провести свод
    :param df: датафрейм с результатами
    :param out_dct: словарь с уже подсчитанными базовыми данными
    :param lst_svod_cols: список сводных колонок
    :return: словарь
    """
    lst_l = ['I уровень', 'II уровень', 'III уровень', 'IV уровень','V уровень']

    lst_reindex_one_level_l_cols = lst_svod_cols.copy()
    lst_reindex_one_level_l_cols.extend(['I уровень', 'II уровень', 'III уровень', 'IV уровень','V уровень',
                                       'Итого'])  # Основная шкала

    svod_count_one_level_l_df = calc_count_scale(base_df, lst_svod_cols,
                                                 'Итог_Значение',
                                                 'Итог_Уровень',
                                                 lst_reindex_one_level_l_cols, lst_l)

    lst_level = ['низкий', 'средний', 'высокий']

    lst_reindex_one_level_cols = lst_svod_cols.copy()
    lst_reindex_one_level_cols.extend(['низкий', 'средний', 'высокий',
                                       'Итого'])  # Основная шкала

    # АД
    svod_count_one_level_pa_df = calc_count_scale(base_df, lst_svod_cols,
                                                 'ПА_Значение',
                                                 'ПА_Уровень',
                                                 lst_reindex_one_level_cols, lst_level)
    # АВА
    svod_count_one_level_md_df = calc_count_scale(base_df, lst_svod_cols,
                                                 'МД_Значение',
                                                 'МД_Уровень',
                                                 lst_reindex_one_level_cols, lst_level)
    # АД
    svod_count_one_level_t_df = calc_count_scale(base_df, lst_svod_cols,
                                                 'Т_Значение',
                                                 'Т_Уровень',
                                                 lst_reindex_one_level_cols, lst_level)
    # АВА
    svod_count_one_level_g_df = calc_count_scale(base_df, lst_svod_cols,
                                                 'Г_Значение',
                                                 'Г_Уровень',
                                                 lst_reindex_one_level_cols, lst_level)

    # Считаем среднее по субшкалам
    svod_mean_one_df = pd.pivot_table(base_df,
                                      index=lst_svod_cols,
                                      values=['Итог_Значение',
                                              'ПА_Значение',
                                              'МД_Значение',
                                              'Т_Значение',
                                              'Г_Значение',
                                              ],
                                      aggfunc=round_mean_two)
    svod_mean_one_df.reset_index(inplace=True)

    # упорядочиваем колонки
    new_order_cols = lst_svod_cols.copy()
    new_order_cols.extend((['Итог_Значение',
                            'ПА_Значение',
                            'МД_Значение',
                            'Т_Значение',
                            'Г_Значение',
                            ]))
    svod_mean_one_df = svod_mean_one_df.reindex(columns=new_order_cols)

    dct_rename_cols_mean = {'Итог_Значение': 'Ср. Итоговое значение',
                            'ПА_Значение': 'Ср. Познавательная активность',
                            'МД_Значение': 'Ср. Мотивация Достижения',
                            'Т_Значение': 'Ср. Тревожность',
                            'Г_Значение': 'Ср. Гнев',
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
                    f'Итог {out_name}': svod_count_one_level_l_df,
                    f'ПА {out_name}': svod_count_one_level_pa_df,
                    f'МД {out_name}': svod_count_one_level_md_df,
                    f'Т {out_name}': svod_count_one_level_t_df,
                    f'Г {out_name}': svod_count_one_level_g_df,
                    })

    if len(lst_svod_cols) == 1:
        return out_dct

    else:
        for idx, name_column in enumerate(lst_svod_cols):
            lst_reindex_column_level_l_cols = [lst_svod_cols[idx], 'I уровень', 'II уровень', 'III уровень', 'IV уровень','V уровень',
                                             'Итого']
            # Ложь
            svod_count_column_level_l_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                         'Итог_Значение',
                                                         'Итог_Уровень',
                                                         lst_reindex_column_level_l_cols, lst_l)

            lst_reindex_column_level_cols = [lst_svod_cols[idx], 'низкий', 'средний', 'высокий',
                                             'Итого']

            # АД
            svod_count_column_level_pa_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                          'ПА_Значение',
                                                          'ПА_Уровень',
                                                          lst_reindex_column_level_cols, lst_level)
            # АВА
            svod_count_column_level_md_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                          'МД_Значение',
                                                          'МД_Уровень',
                                                          lst_reindex_column_level_cols, lst_level)
            # АД
            svod_count_column_level_t_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                         'Т_Значение',
                                                         'Т_Уровень',
                                                         lst_reindex_column_level_cols, lst_level)
            # АВА
            svod_count_column_level_g_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                         'Г_Значение',
                                                         'Г_Уровень',
                                                         lst_reindex_column_level_cols, lst_level)

            # Считаем среднее по субшкалам
            svod_mean_column_df = pd.pivot_table(base_df,
                                              index=[lst_svod_cols[idx]],
                                              values=['Итог_Значение',
                                                      'ПА_Значение',
                                                      'МД_Значение',
                                                      'Т_Значение',
                                                      'Г_Значение',
                                                      ],
                                              aggfunc=round_mean_two)
            svod_mean_column_df.reset_index(inplace=True)

            # упорядочиваем колонки
            new_order_cols = [lst_svod_cols[idx]].copy()
            new_order_cols.extend((['Итог_Значение',
                                    'ПА_Значение',
                                    'МД_Значение',
                                    'Т_Значение',
                                    'Г_Значение',
                                    ]))
            svod_mean_column_df = svod_mean_column_df.reindex(columns=new_order_cols)

            dct_rename_cols_mean = {'Итог_Значение': 'Ср. Итоговое значение',
                                    'ПА_Значение': 'Ср. Познавательная активность',
                                    'МД_Значение': 'Ср. Мотивация Достижения',
                                    'Т_Значение': 'Ср. Тревожность',
                                    'Г_Значение': 'Ср. Гнев',
                                    }
            svod_mean_column_df.rename(columns=dct_rename_cols_mean, inplace=True)

            name_column = lst_svod_cols[idx]
            name_column = re.sub(r'[\[\]\'+()<> :"?*|\\/]', '_', name_column)
            name_column = name_column[:15]
            out_dct.update({f'Ср {name_column}': svod_mean_column_df,
                            f'Итог {name_column}': svod_count_column_level_l_df,
                            f'ПА {name_column}': svod_count_column_level_pa_df,
                            f'МД {name_column}': svod_count_column_level_md_df,
                            f'Т {name_column}': svod_count_column_level_t_df,
                            f'Г {name_column}': svod_count_column_level_g_df,
                            })
        return out_dct














def processing_dmuaoup_prihogan(base_df: pd.DataFrame, answers_df: pd.DataFrame, lst_svod_cols:list):
    """
    Функция для обработки
    :param base_df: часть датафрейма с описательными колонками
    :param answers_df: часть датафрейма с ответами
    :param lst_svod_cols:  список с колонками по которым нужно делать свод
    """
    try:
        out_answer_df = base_df.copy()  # делаем копию для последующего соединения с сырыми ответами
        if len(answers_df.columns) != 40:  # проверяем количество колонок с вопросами
            raise BadCountColumnsDMUAOUP

        # очищаем названия колонок от возможных сочетаний .1 которые добавляет пандас при одинаковых колонках
        clean_df_lst = []
        for name_column in answers_df.columns:
            clean_name = re.sub(r'.\d+$', '', name_column)
            clean_df_lst.append(clean_name)

        answers_df.columns = clean_df_lst

        # Проверяем наличие колонок Пол и Возраст
        diff_req_cols = {'Пол', 'Возраст'}.difference(set(base_df.columns))
        if len(diff_req_cols) != 0:
            raise NotReqColumnDMUAOUP

        # на случай пустых
        base_df['Пол'].fillna('Не заполнено', inplace=True)
        # очищаем от лишних пробелов
        base_df['Пол'] = base_df['Пол'].apply(str.strip)

        base_df['Возраст'].fillna('Не заполнено', inplace=True)
        # очищаем от лишних пробелов
        base_df['Возраст'] = base_df['Возраст'].apply(str.strip)

        # Проверяем на пол
        diff_sex = set(base_df['Пол'].unique()).difference({'Мужской', 'Женский'})
        if len(diff_sex) != 0:
            raise BadValueSexDMUAOUp

        # Проверяем на возраст
        diff_age = set(base_df['Возраст'].unique()).difference({'10-11 лет', '12-14 лет','15-16 лет'})
        if len(diff_age) != 0:
            raise BadValueAgeDMUAOUP


        lst_check_cols = ['Я спокоен',
                          'Мне хочется узнать, понять, докопаться до сути',
                          'Я разъярен',
                          'Я падаю духом, сталкиваясь с трудностями в учебе',
                          'Я напряжен',
                          'Я испытываю любопытство',
                          'Мне хочется стукнуть кулаком по столу',
                          'Я стараюсь получать только хорошие и отличные оценки',
                          'Я раскован',
                          'Мне интересно',

                          'Я рассержен',
                          'Я прилагаю все силы, чтобы добиться успеха в учебе',
                          'Меня волнуют возможные неудачи',
                          'Мне кажется, что урок никогда не кончится',
                          'Мне хочется на кого-нибудь накричать',
                          'Я стараюсь все делать правильно',
                          'Я чувствую себя неудачником',
                          'Я чувствую себя исследователем',
                          'Мне хочется что-нибудь сломать',
                          'Я чувствую, что не справлюсь с заданиями',

                          'Я взвинчен',
                          'Я энергичен',
                          'Я взбешен',
                          'Я горжусь своими школьными успехами',
                          'Я чувствую себя совершенно свободно',
                          'Я чувствую, что у меня хорошо работает голова',
                          'Я раздражен',
                          'Я решаю самые трудные задачи',
                          'Мне не хватает уверенности в себе',
                          'Мне скучно',

                          'Мне хочется что-нибудь сломать',
                          'Я стараюсь не получить двойку',
                          'Я уравновешен',
                          'Мне нравится думать, решать',
                          'Я чувствую себя обманутым',
                          'Я стремлюсь показать свои способности и ум',
                          'Я боюсь',
                          'Я чувствую уныние и тоску',
                          'Меня многое приводит в ярость',
                          'Я хочу быть среди лучших',
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
            raise BadOrderDMUAOUP

        # словарь для замены слов на числа
        dct_replace_value = {'почти никогда': 1,
                             'иногда': 2,
                             'часто': 3,
                             'почти всегда': 4,
                             }
        valid_values = [1, 2, 3, 4]
        answers_df.replace(dct_replace_value, inplace=True)  # заменяем слова на цифры для подсчетов
        # Проверяем, есть ли значения, отличающиеся от указанных в списке
        lst_error_answers = []  # список для хранения строк где найдены неправильные ответы

        for i in range(40):
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
            raise BadValueDMUAOUP

        base_df['ПА_Значение'] = answers_df.apply(calc_value_pa, axis=1)
        base_df['ПА_Уровень'] = base_df[['Пол','Возраст','ПА_Значение']].apply(lambda x:calc_level_pa(x),axis=1)

        base_df['МД_Значение'] = answers_df.apply(calc_value_md, axis=1)
        base_df['МД_Уровень'] = base_df[['Пол','Возраст','МД_Значение']].apply(lambda x:calc_level_md(x),axis=1)

        base_df['Т_Значение'] = answers_df.apply(calc_value_t, axis=1)
        base_df['Т_Уровень'] = base_df[['Пол','Возраст','Т_Значение']].apply(lambda x:calc_level_t(x),axis=1)

        base_df['Г_Значение'] = answers_df.apply(calc_value_g, axis=1)
        base_df['Г_Уровень'] = base_df[['Пол','Возраст','Г_Значение']].apply(lambda x:calc_level_g(x),axis=1)

        base_df['Итог_Значение'] = base_df['ПА_Значение'] + base_df['МД_Значение'] + (-base_df['Т_Значение']) + (-base_df['Г_Значение'])
        base_df['Итог_Уровень'] = base_df['Итог_Значение'].apply(calc_base_level)

        # Создаем датафрейм для создания части в общий датафрейм
        part_df = pd.DataFrame()

        # Основные шкалы
        part_df['ДМУЭОУП_Итог_Значение'] = base_df['Итог_Значение']
        part_df['ДМУЭОУП_Итог_Уровень'] = base_df['Итог_Уровень']

        part_df['ДМУЭОУП_ПА_Значение'] = base_df['ПА_Значение']
        part_df['ДМУЭОУП_ПА_Уровень'] = base_df['ПА_Уровень']

        part_df['ДМУЭОУП_МД_Значение'] = base_df['МД_Значение']
        part_df['ДМУЭОУП_МД_Уровень'] = base_df['МД_Уровень']

        part_df['ДМУЭОУП_Т_Значение'] = base_df['Т_Значение']
        part_df['ДМУЭОУП_Т_Уровень'] = base_df['Т_Уровень']

        part_df['ДМУЭОУП_Г_Значение'] = base_df['Г_Значение']
        part_df['ДМУЭОУП_Г_Уровень'] = base_df['Г_Уровень']

        out_answer_df = pd.concat([out_answer_df, answers_df], axis=1)  # Датафрейм для проверки

        base_df.sort_values(by='Итог_Значение', ascending=True, inplace=True)  # сортируем

        # Делаем свод  по  шкалам
        dct_svod_l = {'Итог_Значение': 'Итог_Уровень',
                      }

        dct_rename_svod_l = {'Итог_Значение': 'Итог',
                             }

        lst_l = ['I уровень', 'II уровень', 'III уровень', 'IV уровень','V уровень']

        base_svod_l_df = create_union_svod(base_df, dct_svod_l, dct_rename_svod_l, lst_l)

        # Делаем свод  по  шкалам
        dct_svod_sub = {'ПА_Значение': 'ПА_Уровень',
                        'МД_Значение': 'МД_Уровень',
                        'Т_Значение': 'Т_Уровень',
                        'Г_Значение': 'Г_Уровень',
                        }

        dct_rename_svod_sub = {'ПА_Значение': 'Познавательная активность"',
                               'МД_Значение': 'Мотивация Достижения',
                               'Т_Значение': 'Тревожность',
                               'Г_Значение': 'Гнев',
                               }

        lst_sub = ['низкий', 'средний', 'высокий']

        base_svod_sub_df = create_union_svod(base_df, dct_svod_sub, dct_rename_svod_sub, lst_sub)

        avg_vcha = round(base_df['Итог_Значение'].mean(), 2)
        avg_o = round(base_df['ПА_Значение'].mean(), 2)
        avg_ruvs = round(base_df['МД_Значение'].mean(), 2)
        avg_t = round(base_df['Т_Значение'].mean(), 2)
        avg_g = round(base_df['Г_Значение'].mean(), 2)

        avg_dct = {'Среднее значение итогового балла': avg_vcha,
                   'Среднее значение шкалы Познавательная активность': avg_o,
                   'Среднее значение шкалы Мотивация Достижения': avg_ruvs,
                   'Среднее значение шкалы Тревожность': avg_t,
                   'Среднее значение шкалы Гнев': avg_g,
                   }

        avg_df = pd.DataFrame.from_dict(avg_dct, orient='index')
        avg_df = avg_df.reset_index()
        avg_df.columns = ['Показатель', 'Среднее значение']

        # формируем основной словарь
        out_dct = {'Списочный результат': base_df,
                   'Список для проверки': out_answer_df,
                   'Свод Итог': base_svod_l_df,
                   'Свод Шкалы': base_svod_sub_df,
                   'Среднее': avg_df,
                   }

        dct_l = {
            'Итог_Уровень': 'Итог',
        }

        out_dct = create_list_on_level(base_df, out_dct, lst_l, dct_l)

        dct_prefix = {
            'ПА_Уровень': 'ПА',
            'МД_Уровень': 'МД',
            'Т_Уровень': 'Т',
            'Г_Уровень': 'Г',
        }

        out_dct = create_list_on_level(base_df, out_dct, lst_sub, dct_prefix)
        """
                        Сохраняем в зависимости от необходимости делать своды по определенным колонкам
                        """
        if len(lst_svod_cols) == 0:
            return out_dct, part_df

        else:
            out_dct = create_result_dmuaou_prihogan(base_df, out_dct, lst_svod_cols)
            return out_dct, part_df

    except BadOrderDMUAOUP:
        messagebox.showerror('Лахеcис',
                             f'При обработке вопросов теста Диагностика мотивации учения и эмоционального отношения к учению Прихожан обнаружены неправильные вопросы. Проверьте названия колонок с вопросами:\n'
                             f'{error_order_message[:5000]}\n'
                             f'Используйте при создании Яндекс-формы написание вопросов из руководства пользователя программы Лахесис.')
    except BadValueDMUAOUP:
        messagebox.showerror('Лахеcис',
                             f'При обработке вопросов теста Диагностика мотивации учения и эмоционального отношения к учению Прихожан обнаружены неправильные варианты ответов. Проверьте ответы на указанных строках:\n'
                             f'{error_message[:5000]}\n'
                             f'Используйте при создании Яндекс-формы написание вариантов ответа из руководства пользователя программы Лахесис.')


    except BadCountColumnsDMUAOUP:
        messagebox.showerror('Лахеcис',
                             f'Проверьте количество колонок с ответами на тест Диагностика мотивации учения и эмоционального отношения к учению Прихожан\n'
                             f'Должно быть 40 колонок с ответами')

    except NotReqColumnDMUAOUP:
        messagebox.showerror('Лахеcис',
                             f'В таблице отсутствуют обязательные колонки {diff_req_cols}\n'
                             f'В таблице обязательно должны быть колонка с названием Пол и колонка с названием Возраст')

    except BadValueSexDMUAOUp:
        messagebox.showerror('Лахеcис',
                             f'В колонке Пол найдены значения отличающиеся от допустимых {diff_sex}\n'
                             f'Допускаются значения: Мужской и Женский\n'
                             f'Прочитайте страницу 1 и 2 файла инструкции к тесту Диагностика мотивации учения и эмоционального отношения к учению Прихожан')
    except BadValueAgeDMUAOUP:
        messagebox.showerror('Лахеcис',
                             f'В колонке Возраст найдены значения отличающиеся от допустимых {diff_age}\n'
                             f'Допускаются значения: 10-11 лет, 12-14 лет, 15-16 лет\n'
                             f'Прочитайте страницу 1 и 2 файла инструкции к тесту Диагностика мотивации учения и эмоционального отношения к учению Прихожан')



