"""
Скрипт для обработки результатов теста Методика диагностики гейм-аддикции Н.В. Кочетков
"""

import pandas as pd
import re
from tkinter import messagebox
from lachesis_support_functions import round_mean_two,calc_count_scale,create_union_svod, create_list_on_level

class BadOrderDGAK(Exception):
    """
    Исключение для обработки случая когда колонки не совпадают
    """
    pass


class BadValueDGAK(Exception):
    """
    Исключение для неправильных значений в вариантах ответов
    """
    pass

class BadCountColumnsDGAK(Exception):
    """
    Исключение для обработки случая если количество колонок не равно 24
    """
    pass

def calc_value_a(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [1,9,17]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_pr:
            if idx != 17:
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
    return value_forward

def calc_value_r(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [2,10,18]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_pr:
            if idx != 10:
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
    return value_forward


def calc_value_v(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [3,11,19]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_pr:
            if idx == 3:
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
    return value_forward


def calc_value_emo(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [5,13,21]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_pr:
            if idx != 21:
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
    return value_forward

def calc_value_k(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [6,14,22]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_pr:
            value_forward += value
    return value_forward

def calc_value_p(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [7,15,23]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_pr:
            value_forward += value
    return value_forward


def calc_value_fp(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [4,8,12,16,20,24]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_pr:
            value_forward += value
    return value_forward


def calc_value_ip(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [10,11,17,19,21]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_pr:
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
        else:
            value_forward += value

    return value_forward




def calc_level(value):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """
    if 24<= value <= 48:
        return f'24-48'
    elif 49 <= value <= 73:
        return f'49-73'
    elif 74 <= value <= 98:
        return f'74-98'
    else:
        return f'99-120'



def create_result_dga_kochet(base_df:pd.DataFrame, out_dct:dict, lst_svod_cols:list):
    """
    Функция для подсчета результата если указаны колонки по которым нужно провести свод
    :param df: датафрейм с результатами
    :param out_dct: словарь с уже подсчитанными базовыми данными
    :param lst_svod_cols: список сводных колонок
    :return: словарь
    """
    lst_level = ['24-48', '49-73', '74-98','99-120']

    lst_reindex_one_level_cols = lst_svod_cols.copy()
    lst_reindex_one_level_cols.extend(['24-48', '49-73', '74-98','99-120',
                                       'Итого'])  # Основная шкала

    svod_count_one_level_vcha_df = calc_count_scale(base_df, lst_svod_cols,
                                                    'ИП_Значение',
                                                    'ИП_Диапазон',
                                                    lst_reindex_one_level_cols, lst_level)

    # Считаем среднее по субшкалам
    svod_mean_one_df = pd.pivot_table(base_df,
                                      index=lst_svod_cols,
                                      values=['А_Значение',
                                              'Р_Значение',
                                              'В_Значение',
                                              'МО_Значение',

                                              'Э_Значение',
                                              'К_Значение',
                                              'П_Значение',
                                              'ОИ_Значение',

                                              'ФП_Значение',
                                              'ИП_Значение',
                                              ],
                                      aggfunc=round_mean_two)
    svod_mean_one_df.reset_index(inplace=True)

    # упорядочиваем колонки
    new_order_cols = lst_svod_cols.copy()
    new_order_cols.extend((['А_Значение',
                          'Р_Значение',
                          'В_Значение',
                          'МО_Значение',

                          'Э_Значение',
                          'К_Значение',
                          'П_Значение',
                          'ОИ_Значение',

                          'ФП_Значение',
                          'ИП_Значение',
                                              ]))
    svod_mean_one_df = svod_mean_one_df.reindex(columns=new_order_cols)

    dct_rename_cols_mean = {'А_Значение': 'Ср. Аттракция',
                            'Р_Значение': 'Ср. Референтность',
                            'В_Значение': 'Ср. Власть',
                            'МО_Значение': 'Ср. Межличностные отношения',

                            'Э_Значение': 'Ср. Эмоциональный',
                            'К_Значение': 'Ср. Когнитивный',
                            'П_Значение': 'Ср. Поведенческий',
                            'ОИ_Значение': 'Ср. Отношение к игре',

                            'ФП_Значение': 'Ср. Физические проявления зависимости',
                            'ИП_Значение': 'Ср. Интегральный показатель',
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
                    f'ИП {out_name}': svod_count_one_level_vcha_df,
                    })

    if len(lst_svod_cols) == 1:
        return out_dct

    else:
        for idx, name_column in enumerate(lst_svod_cols):
            lst_reindex_column_level_cols = [lst_svod_cols[idx],'24-48', '49-73', '74-98','99-120',
                                                  'Итого']
            # ВЧА
            svod_count_column_level_vcha_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                            'ИП_Значение',
                                                            'ИП_Диапазон',
                                                            lst_reindex_column_level_cols, lst_level)

            # Считаем среднее по субшкалам
            svod_mean_column_df = pd.pivot_table(base_df,
                                              index=[lst_svod_cols[idx]],
                                              values=['А_Значение',
                                                      'Р_Значение',
                                                      'В_Значение',
                                                      'МО_Значение',

                                                      'Э_Значение',
                                                      'К_Значение',
                                                      'П_Значение',
                                                      'ОИ_Значение',

                                                      'ФП_Значение',
                                                      'ИП_Значение',
                                                      ],
                                              aggfunc=round_mean_two)
            svod_mean_column_df.reset_index(inplace=True)

            # упорядочиваем колонки
            new_order_cols = [lst_svod_cols[idx]].copy()
            new_order_cols.extend((['А_Значение',
                                    'Р_Значение',
                                    'В_Значение',
                                    'МО_Значение',

                                    'Э_Значение',
                                    'К_Значение',
                                    'П_Значение',
                                    'ОИ_Значение',

                                    'ФП_Значение',
                                    'ИП_Значение',
                                    ]))
            svod_mean_column_df = svod_mean_column_df.reindex(columns=new_order_cols)

            dct_rename_cols_mean = {'А_Значение': 'Ср. Аттракция',
                                    'Р_Значение': 'Ср. Референтность',
                                    'В_Значение': 'Ср. Власть',
                                    'МО_Значение': 'Ср. Межличностные отношения',

                                    'Э_Значение': 'Ср. Эмоциональный',
                                    'К_Значение': 'Ср. Когнитивный',
                                    'П_Значение': 'Ср. Поведенческий',
                                    'ОИ_Значение': 'Ср. Отношение к игре',

                                    'ФП_Значение': 'Ср. Физические проявления зависимости',
                                    'ИП_Значение': 'Ср. Интегральный показатель',
                                    }
            svod_mean_column_df.rename(columns=dct_rename_cols_mean, inplace=True)
            # Готовим наименование
            name_column = lst_svod_cols[idx]
            name_column = re.sub(r'[\[\]\'+()<> :"?*|\\/]', '_', name_column)
            name_column = name_column[:15]
            out_dct.update({f'Ср {name_column}': svod_mean_column_df,
                            f'ИП {name_column}': svod_count_column_level_vcha_df,
                            })
        return out_dct







def processing_dga_koch(base_df: pd.DataFrame, answers_df: pd.DataFrame, lst_svod_cols:list):
    """
    Функция для обработки
    :param base_df: часть датафрейма с описательными колонками
    :param answers_df: часть датафрейма с ответами
    :param lst_svod_cols:  список с колонками по которым нужно делать свод
    """
    try:
        out_answer_df = base_df.copy()  # делаем копию для последующего соединения с сырыми ответами
        if len(answers_df.columns) != 24:  # проверяем количество колонок с вопросами
            raise BadCountColumnsDGAK

        # очищаем названия колонок от возможных сочетаний .1 которые добавляет пандас при одинаковых колонках
        clean_df_lst = []
        for name_column in answers_df.columns:
            clean_name = re.sub(r'.\d+$', '', name_column)
            clean_df_lst.append(clean_name)

        answers_df.columns = clean_df_lst

        lst_check_cols = ['В Сети у меня много интересных друзей, с которыми я познакомился в играх',
                          'Мне интересно было бы узнать, что думают обо мне мои друзья по игре',
                          'Я хотел бы получить статус администратора или модератора чата (форума) игры или кого-то, кто может влиять на игровой процесс',
                          'Во время игры я могу забыть про еду и вспомнить про то, что я хочу есть, только по ее окончании',
                          'Неудачи в компьютерной игре вызывают у меня очень яркие эмоции',
                          'В любой игре я читаю информацию о ее тактике и характеристиках героев, снаряжения, техники',
                          'Если уж я играю, то, как правило, состою в каком-нибудь клане (гильдии, команде и т. п.)',
                          'После того, как я поиграю, мне бывает тяжело уснуть',
                          'Я слежу за праздниками в игре и отмечаю их со своими виртуальными друзьями',
                          'На самом деле большинству моих товарищей по игре безразлично мое мнение о них',

                          'Я не критикую действия разработчиков игры',
                          'У меня бывают боли в спине, руках или голове из-за того, что я много времени провожу за компьютером',
                          'Когда я нахожусь не в игре, я вспоминаю и переживаю события, которые были в ней накануне',
                          'Я смотрю видеоролики с прохождением игры',
                          'Я вкладываю в игру реальные деньги',
                          'Бывает так, что из-за игры мне не удается вовремя следить за собой (мыться, чистить зубы и т. п.)',
                          'Большая часть людей, с которыми я играю, мне малоинтересна',
                          'Я бы доверил друзьям, с которыми я познакомился в игре, решать важный для меня вопрос',
                          'Мне, в общем, все равно, кто является модератором, администратором или разработчиком игры',
                          'Мне снятся сны, в которых я продолжаю играть',
                          'Я не сажусь играть, если у меня плохое настроение',
                          'Я пишу в ЧаВо (FAQ) или викисловарь игры',
                          'Я стараюсь принимать участие во всех мероприятиях в игре (рейды, турниры, конкурсы)',
                          'Если я нахожусь не у компьютера, то на меня накатывает депрессия'
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
            raise BadOrderDGAK

        # словарь для замены слов на числа
        dct_replace_value = {'полностью не верно': 1,
                             'не верно': 2,
                             'затрудняюсь ответить': 3,
                             'верно': 4,
                             'полностью верно': 5,
                             }
        valid_values = [1, 2, 3, 4, 5]
        answers_df.replace(dct_replace_value, inplace=True)  # заменяем слова на цифры для подсчетов
        # Проверяем, есть ли значения, отличающиеся от указанных в списке
        lst_error_answers = []  # список для хранения строк где найдены неправильные ответы

        for i in range(24):
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
            raise BadValueDGAK

        base_df['А_Значение'] = answers_df.apply(calc_value_a, axis=1)
        base_df['Р_Значение'] = answers_df.apply(calc_value_r, axis=1)
        base_df['В_Значение'] = answers_df.apply(calc_value_v, axis=1)
        base_df['МО_Значение'] = base_df[['А_Значение','Р_Значение','В_Значение']].sum(axis=1)

        base_df['Э_Значение'] = answers_df.apply(calc_value_emo, axis=1)
        base_df['К_Значение'] = answers_df.apply(calc_value_k, axis=1)
        base_df['П_Значение'] = answers_df.apply(calc_value_p, axis=1)
        base_df['ОИ_Значение'] = base_df[['Э_Значение','К_Значение','П_Значение']].sum(axis=1)

        base_df['ФП_Значение'] = answers_df.apply(calc_value_fp, axis=1)

        base_df['ИП_Значение'] = answers_df.apply(calc_value_ip, axis=1)
        base_df['ИП_Диапазон'] = base_df['ИП_Значение'].apply(calc_level)

        # Создаем датафрейм для создания части в общий датафрейм
        part_df = pd.DataFrame()

        # Основные шкалы

        part_df['ДГА_А_Значение'] = base_df['А_Значение']
        part_df['ДГА_Р_Значение'] = base_df['Р_Значение']
        part_df['ДГА_В_Значение'] = base_df['В_Значение']
        part_df['ДГА_МО_Значение'] = base_df['МО_Значение']

        part_df['ДГА_Э_Значение'] = base_df['Э_Значение']
        part_df['ДГА_К_Значение'] = base_df['К_Значение']
        part_df['ДГА_П_Значение'] = base_df['П_Значение']
        part_df['ДГА_ОИ_Значение'] = base_df['ОИ_Значение']

        part_df['ДГА_ФП_Значение'] = base_df['ФП_Значение']

        part_df['ДГА_ИП_Значение'] = base_df['ИП_Значение']
        part_df['ДГА_ИП_Диапазон'] = base_df['ИП_Диапазон']

        out_answer_df = pd.concat([out_answer_df, answers_df], axis=1)  # Датафрейм для проверки

        base_df.sort_values(by='ИП_Значение', ascending=False, inplace=True)  # сортируем

        # Делаем свод  по  шкалам
        dct_svod_sub = {'ИП_Значение': 'ИП_Диапазон',
                        }

        dct_rename_svod_sub = {
            'ИП_Значение': 'Диапазон интегрального показателя',
        }

        lst_sub = ['24-48', '49-73', '74-98','99-120']

        base_svod_sub_df = create_union_svod(base_df, dct_svod_sub, dct_rename_svod_sub, lst_sub)

        avg_a = round(base_df['А_Значение'].mean(), 2)
        avg_r = round(base_df['Р_Значение'].mean(), 2)
        avg_v = round(base_df['В_Значение'].mean(), 2)
        avg_mo = round(base_df['МО_Значение'].mean(), 2)

        avg_emo = round(base_df['Э_Значение'].mean(), 2)
        avg_k = round(base_df['К_Значение'].mean(), 2)
        avg_p = round(base_df['П_Значение'].mean(), 2)
        avg_oi = round(base_df['ОИ_Значение'].mean(), 2)

        avg_fp = round(base_df['ФП_Значение'].mean(), 2)

        avg_ip = round(base_df['ИП_Значение'].mean(), 2)

        avg_dct = {'Среднее значение субкомпонента Аттракция': avg_a,
                   'Среднее значение субкомпонента Референтность': avg_r,
                   'Среднее значение субкомпонента Власть': avg_v,
                   'Среднее значение компонента Межличностные отношения': avg_mo,

                   'Среднее значение субкомпонента Эмоциональный': avg_emo,
                   'Среднее значение субкомпонента Когнитивный': avg_k,
                   'Среднее значение субкомпонента Поведенческий': avg_p,
                   'Среднее значение компонента Отношение к игре': avg_oi,

                   'Среднее значение компонента Физические проявления зависимости': avg_fp,
                   'Среднее значение интегрального показателя': avg_ip,
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

        dct_prefix = {'ИП_Диапазон': 'ИП',
                      }

        out_dct = create_list_on_level(base_df, out_dct, lst_sub, dct_prefix)

        """
                                Сохраняем в зависимости от необходимости делать своды по определенным колонкам
                                """
        if len(lst_svod_cols) == 0:
            return out_dct, part_df

        else:
            out_dct = create_result_dga_kochet(base_df, out_dct, lst_svod_cols)
            return out_dct, part_df

    except BadOrderDGAK:
        messagebox.showerror('Лахеcис',
                             f'При обработке вопросов теста Методика диагностики гейм-аддикции Кочетков обнаружены неправильные вопросы. Проверьте названия колонок с вопросами:\n'
                             f'{error_order_message[:5000]}\n'
                             f'Используйте при создании Яндекс-формы написание вопросов из руководства пользователя программы Лахесис.')
    except BadValueDGAK:
        messagebox.showerror('Лахеcис',
                             f'При обработке вопросов теста Методика диагностики гейм-аддикции Кочетков обнаружены неправильные варианты ответов. Проверьте ответы на указанных строках:\n'
                             f'{error_message[:5000]}\n'
                             f'Используйте при создании Яндекс-формы написание вариантов ответа из руководства пользователя программы Лахесис.')


    except BadCountColumnsDGAK:
        messagebox.showerror('Лахеcис',
                             f'Проверьте количество колонок с ответами на тест Методика диагностики гейм-аддикции Кочетков\n'
                             f'Должно быть 24 колонки с ответами')













