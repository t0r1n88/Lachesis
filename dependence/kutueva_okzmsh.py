"""
Скрипт для обработки результатов теста для младших школьников на определение компьютерной зависимости О.Л. Кутуева
"""

import pandas as pd
import re
from tkinter import messagebox
from lachesis_support_functions import round_mean_two,calc_count_scale,create_union_svod, create_list_on_level

class BadOrderOKZMSHK(Exception):
    """
    Исключение для обработки случая когда колонки не совпадают
    """
    pass


class BadValueOKZMSHK(Exception):
    """
    Исключение для неправильных значений в вариантах ответов
    """
    pass

class BadCountColumnsOKZMSHK(Exception):
    """
    Исключение для обработки случая если количество колонок не равно 8
    """
    pass


def calc_value(row):
    """
    Фнукция подсчета значения
    :param row:
    :return:
    """
    value = 0
    # 1
    if row[0] == 'только когда нечего делать':
        value += 1
    elif row[0] == 'один раз в два дня':
        value += 2
    elif row[0] == 'ежедневно':
        value += 3
    # 2
    if row[1] == 'не более часа':
        value += 1
    elif row[1] == '1–2 часа (увлекаюсь игрой)':
        value += 2
    elif row[1] == 'более 2–3 часов':
        value += 3
    # 3
    if row[2] == 'выключаю сам по собственной воле':
        value += 1
    elif row[2] == 'бывает по-разному, иногда могу выключить компьютер сам':
        value += 2
    elif row[2] == 'пока не выключат родители — сам не выключаю, или выключаю, когда он перегревается, или когда начинаю засыпать, или когда начинает болеть спина, или когда сливаются цвета':
        value += 3
    # 4
    if row[3] == 'вряд ли буду сидеть за компьютером':
        value += 1
    elif row[3] == 'зависит от настроения и желания, возможно, на компьютер':
        value += 2
    elif row[3] == 'конечно, на компьютер':
        value += 3
    # 5
    if row[4] == 'нет, никогда такого не было':
        value += 1
    elif row[4] == 'пару раз, возможно, и случалось, но мероприятие не было таким уж важным':
        value += 2
    elif row[4] == 'да, было такое':
        value += 3
    # 6
    if row[5] == 'почти совсем не вспоминаю, может быть, очень редко':
        value += 1
    elif row[5] == 'могу пару раз вспомнить в течение дня':
        value += 2
    elif row[5] == 'почти все время думаю об этом':
        value += 3
    # 7
    if row[6] == 'компьютер не занимает какое-то особое место в моей жизни':
        value += 1
    elif row[6] == 'большую роль, но и других интересных вещей в жизни много, которые тоже для меня много значат':
        value += 2
    elif row[6] == 'Компьютер для меня все':
        value += 3
    # 8
    if row[7] == 'точно не садишься за компьютер':
        value += 1
    elif row[7] == 'каждый раз бывает по-разному, иногда садишься за компьютер':
        value += 2
    elif row[7] == 'идешь к компьютеру и включаешь его':
        value += 3

    return value

def calc_level(value):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """
    if 8<= value <= 12:
        return f'отсутствие КЗ'
    elif 13 <= value <= 18:
        return f'склонность к КЗ'
    else:
        return f'наличие КЗ'



def create_result_okzmsh_kut(base_df:pd.DataFrame, out_dct:dict, lst_svod_cols:list):
    """
    Функция для подсчета результата если указаны колонки по которым нужно провести свод
    :param df: датафрейм с результатами
    :param out_dct: словарь с уже подсчитанными базовыми данными
    :param lst_svod_cols: список сводных колонок
    :return: словарь
    """

    lst_level = ['отсутствие КЗ', 'склонность к КЗ', 'наличие КЗ']

    lst_reindex_one_level_cols = lst_svod_cols.copy()
    lst_reindex_one_level_cols.extend(['отсутствие КЗ', 'склонность к КЗ', 'наличие КЗ',
                                       'Итого'])  # Основная шкала

    svod_count_one_level_vcha_df = calc_count_scale(base_df, lst_svod_cols,
                                                    'КЗ_Значение',
                                                    'КЗ_Уровень',
                                                    lst_reindex_one_level_cols, lst_level)

    # Считаем среднее по субшкалам
    svod_mean_one_df = pd.pivot_table(base_df,
                                      index=lst_svod_cols,
                                      values=[
                                              'КЗ_Значение',
                                              ],
                                      aggfunc=round_mean_two)
    svod_mean_one_df.reset_index(inplace=True)

    # упорядочиваем колонки
    new_order_cols = lst_svod_cols.copy()
    new_order_cols.extend(([ 'КЗ_Значение'
                            ]))
    svod_mean_one_df = svod_mean_one_df.reindex(columns=new_order_cols)

    dct_rename_cols_mean = {'КЗ_Значение': 'Ср. Компьютерная зависимость',
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
                    f'КЗ {out_name}': svod_count_one_level_vcha_df,
                    })

    if len(lst_svod_cols) == 1:
        return out_dct
    else:
        for idx, name_column in enumerate(lst_svod_cols):
            lst_reindex_column_level_cols = [lst_svod_cols[idx],'отсутствие КЗ', 'склонность к КЗ', 'наличие КЗ',
                                                  'Итого']

            svod_count_column_level_vcha_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                               'КЗ_Значение',
                                                               'КЗ_Уровень',
                                                               lst_reindex_column_level_cols, lst_level)

            # Считаем среднее по субшкалам
            svod_mean_column_df = pd.pivot_table(base_df,
                                              index=[lst_svod_cols[idx]],
                                              values=[
                                                  'КЗ_Значение',
                                              ],
                                              aggfunc=round_mean_two)
            svod_mean_column_df.reset_index(inplace=True)

            # упорядочиваем колонки
            new_order_cols = [lst_svod_cols[idx]].copy()
            new_order_cols.extend((['КЗ_Значение'
                                    ]))
            svod_mean_column_df = svod_mean_column_df.reindex(columns=new_order_cols)

            dct_rename_cols_mean = {'КЗ_Значение': 'Ср. Компьютерная зависимость',
                                    }
            svod_mean_column_df.rename(columns=dct_rename_cols_mean, inplace=True)

            # Готовим наименование
            name_column = lst_svod_cols[idx]
            name_column = re.sub(r'[\[\]\'+()<> :"?*|\\/]', '_', name_column)
            name_column = name_column[:15]
            out_dct.update({f'Ср {name_column}': svod_mean_column_df,
                            f'КЗ {name_column}': svod_count_column_level_vcha_df,
                            })
        return out_dct








def processing_okzmsh_kut(base_df: pd.DataFrame, answers_df: pd.DataFrame, lst_svod_cols:list):
    """
    Функция для обработки
    :param base_df: часть датафрейма с описательными колонками
    :param answers_df: часть датафрейма с ответами
    :param lst_svod_cols:  список с колонками по которым нужно делать свод
    """
    try:
        out_answer_df = base_df.copy()  # делаем копию для последующего соединения с сырыми ответами
        if len(answers_df.columns) != 8:  # проверяем количество колонок с вопросами
            raise BadCountColumnsOKZMSHK

        # очищаем названия колонок от возможных сочетаний .1 которые добавляет пандас при одинаковых колонках
        clean_df_lst = []
        for name_column in answers_df.columns:
            clean_name = re.sub(r'.\d+$', '', name_column)
            clean_df_lst.append(clean_name)

        answers_df.columns = clean_df_lst

        lst_check_cols = ['Часто ли ты проводишь время за компьютером?',
                          'Какое количество времени за один подход ты посвящаешь компьютеру?',
                          'В каком случае ты решаешь выключить компьютер?',
                          'Когда у тебя появляется свободное время, на что ты его тратишь?',
                          'Пропускал ли ты какие-то важные мероприятия или учебу ради игры в компьютерные игры?',
                          'Насколько часто ты думаешь о том, чем занимаешься, сидя за компьютером, например, об играх:',
                          'Чем для тебя является компьютер? Какую роль в твоей жизни он играет?',
                          'Когда ты приходишь домой, то первым делом:',
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
            raise BadOrderOKZMSHK


        valid_values = [['ежедневно','один раз в два дня','только когда нечего делать'],
                        ['более 2–3 часов','1–2 часа (увлекаюсь игрой)','не более часа'],
                        ['пока не выключат родители — сам не выключаю, или выключаю, когда он перегревается, или когда начинаю засыпать, или когда начинает болеть спина, или когда сливаются цвета',
                         'бывает по-разному, иногда могу выключить компьютер сам','выключаю сам по собственной воле'],
                        ['конечно, на компьютер','зависит от настроения и желания, возможно, на компьютер','вряд ли буду сидеть за компьютером'],

                        ['да, было такое','пару раз, возможно, и случалось, но мероприятие не было таким уж важным','нет, никогда такого не было'],
                        ['почти все время думаю об этом','могу пару раз вспомнить в течение дня','почти совсем не вспоминаю, может быть, очень редко'],
                        ['Компьютер для меня все','большую роль, но и других интересных вещей в жизни много, которые тоже для меня много значат','компьютер не занимает какое-то особое место в моей жизни'],
                        ['идешь к компьютеру и включаешь его','каждый раз бывает по-разному, иногда садишься за компьютер','точно не садишься за компьютер']
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
            raise BadValueOKZMSHK

        base_df['КЗ_Значение'] = answers_df.apply(calc_value, axis=1)
        base_df['КЗ_Уровень'] = base_df['КЗ_Значение'].apply(calc_level)

        # Создаем датафрейм для создания части в общий датафрейм
        part_df = pd.DataFrame()

        # Основные шкалы

        part_df['ОКЗМШК_Значение'] = base_df['КЗ_Значение']
        part_df['ОКЗМШК_Уровень'] = base_df['КЗ_Уровень']

        out_answer_df = pd.concat([out_answer_df, answers_df], axis=1)  # Датафрейм для проверки

        base_df.sort_values(by='КЗ_Значение', ascending=False, inplace=True)  # сортируем

        # Делаем свод  по  шкалам
        dct_svod_sub = {'КЗ_Значение': 'КЗ_Уровень',
                        }

        dct_rename_svod_sub = {
            'КЗ_Значение': 'Уровень компьютерной зависимости',
        }

        lst_sub = ['отсутствие КЗ', 'склонность к КЗ', 'наличие КЗ']

        base_svod_sub_df = create_union_svod(base_df, dct_svod_sub, dct_rename_svod_sub, lst_sub)

        avg_psp = round(base_df['КЗ_Значение'].mean(), 2)

        avg_dct = {'Среднее значение Компьютерной зависимости': avg_psp,
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

        dct_prefix = {'КЗ_Уровень': 'КЗ',
                      }

        out_dct = create_list_on_level(base_df, out_dct, lst_sub, dct_prefix)

        """
                        Сохраняем в зависимости от необходимости делать своды по определенным колонкам
                        """
        if len(lst_svod_cols) == 0:
            return out_dct, part_df
        else:
            out_dct = create_result_okzmsh_kut(base_df, out_dct, lst_svod_cols)
            return out_dct, part_df


    except BadOrderOKZMSHK:
        messagebox.showerror('Лахеcис',
                             f'При обработке вопросов теста для младших школьников на определение компьютерной зависимости Кутуева обнаружены неправильные вопросы. Проверьте названия колонок с вопросами:\n'
                             f'{error_order_message[:5000]}\n'
                             f'Используйте при создании Яндекс-формы написание вопросов из руководства пользователя программы Лахесис.')
    except BadValueOKZMSHK:
        messagebox.showerror('Лахеcис',
                             f'При обработке вопросов теста для младших школьников на определение компьютерной зависимости Кутуева обнаружены неправильные варианты ответов. Проверьте ответы на указанных строках:\n'
                             f'{error_message[:5000]}\n'
                             f'Используйте при создании Яндекс-формы написание вариантов ответа из руководства пользователя программы Лахесис.')


    except BadCountColumnsOKZMSHK:
        messagebox.showerror('Лахеcис',
                             f'Проверьте количество колонок с ответами на тест для младших школьников на определение компьютерной зависимости Кутуева\n'
                             f'Должно быть 8 колонок с ответами')

