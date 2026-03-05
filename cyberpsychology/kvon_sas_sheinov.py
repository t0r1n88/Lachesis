"""
Скрипт для обработки результатов теста Шкала зависимости от смартфона SAS Квон Адаптация В.П. Шейнов

"""

import pandas as pd
import re
from tkinter import messagebox
from lachesis_support_functions import round_mean_two,calc_count_scale,create_list_on_level,create_union_svod


class BadOrderSASKSH(Exception):
    """
    Исключение для обработки случая когда колонки не совпадают
    """
    pass


class BadValueSASKSH(Exception):
    """
    Исключение для неправильных значений в вариантах ответов
    """
    pass

class BadCountColumnsSASKSH(Exception):
    """
    Исключение для обработки случая если количество колонок не равно 33
    """
    pass



def calc_value_npg(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [1,2,3,4,5]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_pr:
            value_forward += value
    return value_forward


def calc_value_po(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [6,7,8,9,10,11,12,13]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_pr:
            value_forward += value
    return value_forward


def calc_value_so(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [14,15,16,17,18,19]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_pr:
            value_forward += value
    return value_forward

def calc_value_ko(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [20,21,22,23,24,25,26]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_pr:
            value_forward += value
    return value_forward


def calc_value_chp(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [27,28,29,30]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_pr:
            value_forward += value
    return value_forward

def calc_value_t(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [31,32,33]
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
    if value <= 20:
        return f'0-20'
    elif 21 <= value <= 40:
        return f'21-40'
    elif 41 <= value <= 60:
        return f'41-60'
    elif 61 <= value <= 80:
        return f'61-80'
    else:
        return f'81-99'


def create_result_sas_kvan_sheinov(base_df:pd.DataFrame, out_dct:dict, lst_svod_cols:list):
    """
    Функция для подсчета результата если указаны колонки по которым нужно провести свод
    :param df: датафрейм с результатами
    :param out_dct: словарь с уже подсчитанными базовыми данными
    :param lst_svod_cols: список сводных колонок
    :return: словарь
    """

    lst_level = ['0-20', '21-40', '41-60','61-80','81-99']

    lst_reindex_one_level_cols = lst_svod_cols.copy()
    lst_reindex_one_level_cols.extend(['0-20', '21-40', '41-60','61-80','81-99',
                                       'Итого'])  # Основная шкала

    svod_count_one_level_vcha_df = calc_count_scale(base_df, lst_svod_cols,
                                                    'ИП_Значение',
                                                    'ИП_Диапазон',
                                                    lst_reindex_one_level_cols, lst_level)

    # Считаем среднее по субшкалам
    svod_mean_one_df = pd.pivot_table(base_df,
                                      index=lst_svod_cols,
                                      values=['НПЖ_Значение',
                                              'ПО_Значение',
                                              'СО_Значение',
                                              'КО_Значение',
                                              'ЧП_Значение',
                                              'Т_Значение',
                                              'ИП_Значение',
                                              ],
                                      aggfunc=round_mean_two)
    svod_mean_one_df.reset_index(inplace=True)

    # упорядочиваем колонки
    new_order_cols = lst_svod_cols.copy()
    new_order_cols.extend((['НПЖ_Значение', 'ПО_Значение', 'СО_Значение',
                            'КО_Значение', 'ЧП_Значение','Т_Значение', 'ИП_Значение'
                            ]))
    svod_mean_one_df = svod_mean_one_df.reindex(columns=new_order_cols)

    dct_rename_cols_mean = {'НПЖ_Значение': 'Ср. Нарушение повседневной жизни',
                            'ПО_Значение': 'Ср. Положительные ожидания',
                            'СО_Значение': 'Ср. Симптомы отмены',
                            'КО_Значение': 'Ср. Киберотношения',
                            'ЧП_Значение': 'Ср. Чрезмерное пользование',
                            'Т_Значение': 'Ср. Толерантность',

                            'ИП_Значение': 'Ср. Интегральный показатель зависимости',
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
            lst_reindex_column_level_cols = [lst_svod_cols[idx],'0-20', '21-40', '41-60','61-80','81-99',
                                                  'Итого']

            # ВЧА
            svod_count_column_level_vcha_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                            'ИП_Значение',
                                                            'ИП_Диапазон',
                                                            lst_reindex_column_level_cols, lst_level)

            # Считаем среднее по субшкалам
            svod_mean_column_df = pd.pivot_table(base_df,
                                              index=[lst_svod_cols[idx]],
                                              values=['НПЖ_Значение',
                                                      'ПО_Значение',
                                                      'СО_Значение',
                                                      'КО_Значение',
                                                      'ЧП_Значение',
                                                      'Т_Значение',
                                                      'ИП_Значение',
                                                      ],
                                              aggfunc=round_mean_two)
            svod_mean_column_df.reset_index(inplace=True)

            # упорядочиваем колонки
            new_order_cols = [lst_svod_cols[idx]].copy()
            new_order_cols.extend((['НПЖ_Значение', 'ПО_Значение', 'СО_Значение',
                                    'КО_Значение', 'ЧП_Значение', 'Т_Значение', 'ИП_Значение'
                                    ]))
            svod_mean_column_df = svod_mean_column_df.reindex(columns=new_order_cols)

            dct_rename_cols_mean = {'НПЖ_Значение': 'Ср. Нарушение повседневной жизни',
                                    'ПО_Значение': 'Ср. Положительные ожидания',
                                    'СО_Значение': 'Ср. Симптомы отмены',
                                    'КО_Значение': 'Ср. Киберотношения',
                                    'ЧП_Значение': 'Ср. Чрезмерное пользование',
                                    'Т_Значение': 'Ср. Толерантность',

                                    'ИП_Значение': 'Ср. Интегральный показатель зависимости',
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





def processing_sas_kvon_shein(base_df: pd.DataFrame, answers_df: pd.DataFrame, lst_svod_cols:list):
    """
    Функция для обработки
    :param base_df: часть датафрейма с описательными колонками
    :param answers_df: часть датафрейма с ответами
    :param lst_svod_cols:  список с колонками по которым нужно делать свод
    """
    try:
        out_answer_df = base_df.copy()  # делаем копию для последующего соединения с сырыми ответами
        if len(answers_df.columns) != 33:  # проверяем количество колонок с вопросами
            raise BadCountColumnsSASKSH

        # очищаем названия колонок от возможных сочетаний .1 которые добавляет пандас при одинаковых колонках
        clean_df_lst = []
        for name_column in answers_df.columns:
            clean_name = re.sub(r'.\d+$', '', name_column)
            clean_df_lst.append(clean_name)

        answers_df.columns = clean_df_lst

        lst_check_cols = ['Бывает, что не удается выполнить запланированную работу из-за использования смартфона',
                          'Из-за использования смартфона бывает трудно сосредоточиться на занятиях, выполнять задания или при иной работе',
                          'Бывает головокружение или помутнение зрения из-за чрезмерного использования смартфона',
                          'Бывает ощущение боли в запястьях или шее при использовании смартфона',
                          'Бывает чувство усталости и недостаток сна из-за чрезмерного использования смартфона',
                          'Пользование смартфоном дает мне чувство спокойствия или уюта',
                          'Пользование смартфоном дает мне чувство приятного возбуждения',
                          'Пользование смартфоном дает мне чувство уверенности',
                          'Смартфон дает возможность избавиться от стресса',
                          'Нет ничего веселее, чем пользоваться смартфоном',

                          'Моя жизнь была бы пустой без смартфона',
                          'Используя смартфон, чувствую себя максимально свободным',
                          'Использование смартфона —это самое интересное',
                          'Не смогу находиться без смартфона',
                          'Испытываю нетерпение и раздражение, когда не держу в руках смартфон',
                          'Помню о смартфоне, даже когда не пользуюсь им',
                          'Никогда не откажусь от использования смартфона, даже когда он будет сильно осложнять мою повседневную жизнь',
                          'Раздражаюсь, когда не пользуюсь смартфоном',
                          'Захватываю смартфон в туалет, даже когда очень спешу туда',
                          'Чувствую себя отлично, знакомясь с новыми людьми с помощью смартфона',

                          'Чувствую, что мои отношения с виртуальными друзьями более близкие, чем с друзьями из реальной жизни',
                          'Невозможность пользоваться смартфоном была бы такой же болезненной, как потеря друга',
                          'Мои виртуальные друзья понимают меня лучше, чем мои реальные друзья',
                          'Постоянно проверяю смартфон, чтобы не пропустить информацию в социальных сетях',
                          'Как только проснусь, проверяю сайты социальных сетей',
                          'Предпочитаю разговаривать с друзьями по смартфону, чем тусоваться с ними или с членами моей семьи',
                          'Предпочитаю поиск информации через смартфон, нежели спросить кого-то',
                          'Батареи моего телефона не хватало на день, даже когда он был новым',
                          'Использую свой смартфон дольше, чем планировал',
                          'Чувствую желание снова использовать смартфон сразу после того, как отключился от него',
                          'Всегда думаю, что должен сократить время пользования смартфоном',
                          'Попытки сократить время использования моего смартфона постоянно терпят неудачу',
                          'Люди вокруг меня говорят мне, что я слишком часто использую смартфон',
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
            raise BadOrderSASKSH

        # словарь для замены слов на числа
        dct_replace_value = {'уверенное да': 3,
                             'скорее да, чем нет': 2,
                             'скорее нет, чем да': 1,
                             'уверенное нет': 0,
                             }
        valid_values = [0, 1, 2, 3]
        answers_df.replace(dct_replace_value, inplace=True)  # заменяем слова на цифры для подсчетов
        # Проверяем, есть ли значения, отличающиеся от указанных в списке
        lst_error_answers = []  # список для хранения строк где найдены неправильные ответы

        for i in range(33):
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
            raise BadValueSASKSH

        base_df['НПЖ_Значение'] = answers_df.apply(calc_value_npg, axis=1)
        base_df['ПО_Значение'] = answers_df.apply(calc_value_po, axis=1)
        base_df['СО_Значение'] = answers_df.apply(calc_value_so, axis=1)
        base_df['КО_Значение'] = answers_df.apply(calc_value_ko, axis=1)
        base_df['ЧП_Значение'] = answers_df.apply(calc_value_chp, axis=1)
        base_df['Т_Значение'] = answers_df.apply(calc_value_t, axis=1)

        base_df['ИП_Значение'] = answers_df.sum(axis=1)
        base_df['ИП_Диапазон'] = base_df['ИП_Значение'].apply(calc_level)

        # Создаем датафрейм для создания части в общий датафрейм
        part_df = pd.DataFrame()

        # Основные шкалы

        part_df['ШЗСКШ_НПЖ_Значение'] = base_df['НПЖ_Значение']
        part_df['ШЗСКШ_ПО_Значение'] = base_df['ПО_Значение']
        part_df['ШЗСКШ_СО_Значение'] = base_df['СО_Значение']
        part_df['ШЗСКШ_КО_Значение'] = base_df['КО_Значение']
        part_df['ШЗСКШ_ЧП_Значение'] = base_df['ЧП_Значение']
        part_df['ШЗСКШ_Т_Значение'] = base_df['Т_Значение']

        part_df['ШЗСКШ_ИП_Значение'] = base_df['ИП_Значение']
        part_df['ШЗСКШ_ИП_Диапазон'] = base_df['ИП_Диапазон']

        out_answer_df = pd.concat([out_answer_df, answers_df], axis=1)  # Датафрейм для проверки

        base_df.sort_values(by='ИП_Значение', ascending=False, inplace=True)  # сортируем

        # Делаем свод  по  шкалам
        dct_svod_sub = {'ИП_Значение': 'ИП_Диапазон',
                        }

        dct_rename_svod_sub = {
            'ИП_Значение': 'Диапазон интегрального показателя зависимости',
        }

        lst_sub = ['0-20', '21-40', '41-60','61-80','81-99']

        base_svod_sub_df = create_union_svod(base_df, dct_svod_sub, dct_rename_svod_sub, lst_sub)

        avg_vcha = round(base_df['НПЖ_Значение'].mean(), 2)
        avg_o = round(base_df['ПО_Значение'].mean(), 2)
        avg_ruvs = round(base_df['СО_Значение'].mean(), 2)
        avg_iika = round(base_df['КО_Значение'].mean(), 2)
        avg_np = round(base_df['ЧП_Значение'].mean(), 2)
        avg_br = round(base_df['Т_Значение'].mean(), 2)

        avg_psp = round(base_df['ИП_Значение'].mean(), 2)

        avg_dct = {'Среднее значение шкалы Нарушение повседневной жизни': avg_vcha,
                   'Среднее значение шкалы Положительные ожидания': avg_o,
                   'Среднее значение шкалы Симптомы отмены': avg_ruvs,
                   'Среднее значение шкалы Киберотношения': avg_iika,
                   'Среднее значение шкалы Чрезмерное пользование': avg_np,
                   'Среднее значение шкалы Толерантность': avg_br,

                   'Среднее значение Интегральный показатель зависимости': avg_psp,
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
            out_dct = create_result_sas_kvan_sheinov(base_df, out_dct, lst_svod_cols)
            return out_dct, part_df

    except BadOrderSASKSH:
        messagebox.showerror('Лахеcис',
                             f'При обработке вопросов теста Шкала зависимости от смартфона SAS Квон Шейнов обнаружены неправильные вопросы. Проверьте названия колонок с вопросами:\n'
                             f'{error_order_message[:5000]}\n'
                             f'Используйте при создании Яндекс-формы написание вопросов из руководства пользователя программы Лахесис.')
    except BadValueSASKSH:
        messagebox.showerror('Лахеcис',
                             f'При обработке вопросов теста Шкала зависимости от смартфона SAS Квон Шейнов обнаружены неправильные варианты ответов. Проверьте ответы на указанных строках:\n'
                             f'{error_message[:5000]}\n'
                             f'Используйте при создании Яндекс-формы написание вариантов ответа из руководства пользователя программы Лахесис.')


    except BadCountColumnsSASKSH:
        messagebox.showerror('Лахеcис',
                             f'Проверьте количество колонок с ответами на тест Шкала зависимости от смартфона SAS Квон Шейнов\n'
                             f'Должно быть 33 колонки с ответами')



