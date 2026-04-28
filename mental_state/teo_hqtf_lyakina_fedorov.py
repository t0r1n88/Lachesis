"""
Скрипт для обработки результатов Опросник хикикомори, HQ-25 Тео Лякина Федоров
"""

import pandas as pd
import re
from tkinter import messagebox
from lachesis_support_functions import round_mean_two,calc_count_scale,create_union_svod, create_list_on_level

class BadOrderHQTFLF(Exception):
    """
    Исключение для обработки случая когда колонки не совпадают
    """
    pass


class BadValueHQTFLF(Exception):
    """
    Исключение для неправильных значений в вариантах ответов
    """
    pass

class BadCountColumnsHQTFLF(Exception):
    """
    Исключение для обработки случая если количество колонок не равно 25
    """
    pass


def calc_level(value):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """
    if 0<= value <= 24:
        return f'0-24'
    elif 25 <= value <= 49:
        return f'25-49'
    elif 50 <= value <= 74:
        return f'50-74'
    else:
        return f'75-100'



def calc_value_ip(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [1,2,3,4,5,6,7,8,9,10,
              11,12,13,14,15,16,17,18,19,20,
              21,22,23,24,25]
    lst_neg = [4,15,25,22,7,10,21]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_pr:
            if idx not in lst_neg:
                value_forward += value
            else:
                if value == 0:
                    value_forward += 4
                elif value == 1:
                    value_forward += 3
                elif value == 2:
                    value_forward += 2
                elif value == 3:
                    value_forward += 1
                else:
                    value_forward += 0


    return value_forward


def calc_value_s(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [1,4,6,8,11,13,
              15,18,20,23,25]
    lst_neg = [4,15,25]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_pr:
            if idx not in lst_neg:
                value_forward += value
            else:
                if value == 0:
                    value_forward += 4
                elif value == 1:
                    value_forward += 3
                elif value == 2:
                    value_forward += 2
                elif value == 3:
                    value_forward += 1
                else:
                    value_forward += 0


    return value_forward


def calc_level_sub(value,quantity):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """

    result =round((value / quantity) * 100)

    if 0<= result <= 24:
        return f'0-24%'
    elif 25 <= result <= 49:
        return f'25-49%'
    elif 50 <= result <= 74:
        return f'50-74%'
    else:
        return f'75-100%'


def calc_value_i(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [2,5,9,12,16,19,22,24]
    lst_neg = [22]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_pr:
            if idx not in lst_neg:
                value_forward += value
            else:
                if value == 0:
                    value_forward += 4
                elif value == 1:
                    value_forward += 3
                elif value == 2:
                    value_forward += 2
                elif value == 3:
                    value_forward += 1
                else:
                    value_forward += 0


    return value_forward

def calc_value_ap(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [3,7,10,14,17,21]
    lst_neg = [7,10,21]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_pr:
            if idx not in lst_neg:
                value_forward += value
            else:
                if value == 0:
                    value_forward += 4
                elif value == 1:
                    value_forward += 3
                elif value == 2:
                    value_forward += 2
                elif value == 3:
                    value_forward += 1
                else:
                    value_forward += 0


    return value_forward


def create_result_hqtf_lyakina(base_df:pd.DataFrame, out_dct:dict, lst_svod_cols:list):
    """
    Функция для подсчета результата если указаны колонки по которым нужно провести свод
    :param df: датафрейм с результатами
    :param out_dct: словарь с уже подсчитанными базовыми данными
    :param lst_svod_cols: список сводных колонок
    :return: словарь
    """
    lst_l = ['0-24', '25-49', '50-74','75-100']

    lst_reindex_one_level_l_cols = lst_svod_cols.copy()
    lst_reindex_one_level_l_cols.extend(['0-24', '25-49', '50-74','75-100',
                                       'Итого'])  # Основная шкала

    # ИП
    svod_count_one_level_l_df = calc_count_scale(base_df, lst_svod_cols,
                                                 'ИП_Значение',
                                                 'ИП_Диапазон',
                                                 lst_reindex_one_level_l_cols, lst_l)

    lst_level = ['0-24%', '25-49%', '50-74%','75-100%']

    lst_reindex_one_level_cols = lst_svod_cols.copy()
    lst_reindex_one_level_cols.extend(['0-24%', '25-49%', '50-74%','75-100%',
                                       'Итого'])  # Основная шкала

    # АД
    svod_count_one_level_s_df = calc_count_scale(base_df, lst_svod_cols,
                                                 'С_Значение',
                                                 'С_Диапазон',
                                                 lst_reindex_one_level_cols, lst_level)
    # АВА
    svod_count_one_level_i_df = calc_count_scale(base_df, lst_svod_cols,
                                                 'И_Значение',
                                                 'И_Диапазон',
                                                 lst_reindex_one_level_cols, lst_level)

    svod_count_one_level_ap_df = calc_count_scale(base_df, lst_svod_cols,
                                                 'ЭП_Значение',
                                                 'ЭП_Диапазон',
                                                 lst_reindex_one_level_cols, lst_level)

    # Считаем среднее по субшкалам
    svod_mean_one_df = pd.pivot_table(base_df,
                                      index=lst_svod_cols,
                                      values=['ИП_Значение',
                                              'С_Значение',
                                              'И_Значение',
                                              'ЭП_Значение',
                                              ],
                                      aggfunc=round_mean_two)
    svod_mean_one_df.reset_index(inplace=True)

    # упорядочиваем колонки
    new_order_cols = lst_svod_cols.copy()
    new_order_cols.extend((['ИП_Значение',
                            'С_Значение',
                            'И_Значение',
                            'ЭП_Значение',
                            ]))
    svod_mean_one_df = svod_mean_one_df.reindex(columns=new_order_cols)

    dct_rename_cols_mean = {'ИП_Значение': 'Ср. Интегральный показатель',
                            'С_Значение': 'Ср. Социализация',
                            'И_Значение': 'Ср. Изоляция',
                            'ЭП_Значение': 'Ср. Эмоциональная поддержка',
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
                    f'ИП {out_name}': svod_count_one_level_l_df,
                    f'С {out_name}': svod_count_one_level_s_df,
                    f'И {out_name}': svod_count_one_level_i_df,
                    f'ЭП {out_name}': svod_count_one_level_ap_df,
                    })

    if len(lst_svod_cols) == 1:
        return out_dct

    else:
        for idx, name_column in enumerate(lst_svod_cols):
            lst_reindex_column_level_l_cols = [lst_svod_cols[idx], '0-24', '25-49', '50-74','75-100',
                                             'Итого']

            # Ложь
            svod_count_column_level_l_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                         'ИП_Значение',
                                                         'ИП_Диапазон',
                                                         lst_reindex_column_level_l_cols, lst_l)

            lst_reindex_column_level_cols = [lst_svod_cols[idx], '0-24%', '25-49%', '50-74%','75-100%',
                                             'Итого']

            # АД
            svod_count_column_level_s_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                            'С_Значение',
                                                            'С_Диапазон',
                                                            lst_reindex_column_level_cols, lst_level)
            # АВА
            svod_count_column_level_i_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                            'И_Значение',
                                                            'И_Диапазон',
                                                            lst_reindex_column_level_cols, lst_level)
            svod_count_column_level_ap_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                            'ЭП_Значение',
                                                            'ЭП_Диапазон',
                                                            lst_reindex_column_level_cols, lst_level)

            # Считаем среднее по субшкалам
            svod_mean_column_df = pd.pivot_table(base_df,
                                              index=[lst_svod_cols[idx]],
                                              values=['ИП_Значение',
                                                      'С_Значение',
                                                      'И_Значение',
                                                      'ЭП_Значение',
                                                      ],
                                              aggfunc=round_mean_two)
            svod_mean_column_df.reset_index(inplace=True)

            # упорядочиваем колонки
            new_order_cols = [lst_svod_cols[idx]].copy()
            new_order_cols.extend((['ИП_Значение',
                                    'С_Значение',
                                    'И_Значение',
                                    'ЭП_Значение',
                                    ]))
            svod_mean_column_df = svod_mean_column_df.reindex(columns=new_order_cols)

            dct_rename_cols_mean = {'ИП_Значение': 'Ср. Интегральный показатель',
                                    'С_Значение': 'Ср. Социализация',
                                    'И_Значение': 'Ср. Изоляция',
                                    'ЭП_Значение': 'Ср. Эмоциональная поддержка',
                                    }
            svod_mean_column_df.rename(columns=dct_rename_cols_mean, inplace=True)
            # Готовим наименование
            name_column = lst_svod_cols[idx]
            name_column = re.sub(r'[\[\]\'+()<> :"?*|\\/]', '_', name_column)
            name_column = name_column[:15]
            out_dct.update({f'Ср {name_column}': svod_mean_column_df,
                            f'ИП {name_column}': svod_count_column_level_l_df,
                            f'С {name_column}': svod_count_column_level_s_df,
                            f'И {name_column}': svod_count_column_level_i_df,
                            f'ЭП {name_column}': svod_count_column_level_ap_df,
                            })
        return out_dct








def processing_hqtf_lyak_fed(base_df: pd.DataFrame, answers_df: pd.DataFrame, lst_svod_cols:list):
    """
    Функция для обработки
    :param base_df: часть датафрейма с описательными колонками
    :param answers_df: часть датафрейма с ответами
    :param lst_svod_cols:  список с колонками по которым нужно делать свод
    """
    try:
        out_answer_df = base_df.copy()  # делаем копию для последующего соединения с сырыми ответами
        if len(answers_df.columns) != 25:  # проверяем количество колонок с вопросами
            raise BadCountColumnsHQTFLF

        # очищаем названия колонок от возможных сочетаний .1 которые добавляет пандас при одинаковых колонках
        clean_df_lst = []
        for name_column in answers_df.columns:
            clean_name = re.sub(r'.\d+$', '', name_column)
            clean_df_lst.append(clean_name)

        answers_df.columns = clean_df_lst
        lst_check_cols = ['Я держусь в стороне от людей',
                          'Я провожу большую часть своего времени дома',
                          'На самом деле нет никого, с кем я могу обсудить важные вещи',
                          'Мне нравится знакомиться с новыми людьми',
                          'Я запираюсь в своей комнате',
                          'Люди мешают мне',
                          'В моей жизни есть люди, которые пытаются понять меня',
                          'Я чувствую себя некомфортно в окружении людей',
                          'Я провожу большую часть своего времени в одиночестве',
                          'Я могу поделиться своими мыслями с несколькими людьми',

                          'Я не люблю быть на виду',
                          'Я редко встречаюсь с людьми лично',
                          'Мне трудно присоединяться к группам людей',
                          'Есть очень мало людей, с которыми я могу обсудить важные проблемы',
                          'Мне нравится находиться в социальных ситуациях',
                          'Я не живу по правилам и в соответствии с ценностями общества',
                          'В действительности, в моей жизни нет ни одного человека, кто имел бы для меня очень большое значение',
                          'Я избегаю разговоров с людьми',
                          'Я мало общаюсь с людьми вживую, по переписке и т.п.',
                          'Я предпочитаю быть наедине с собой, чем с другими людьми',

                          'У меня есть человек, кому я могу доверять и с кем я могу поделиться своими проблемами',
                          'Я редко провожу время в одиночестве',
                          'Мне не нравятся социальные взаимодействия',
                          'Я трачу очень мало времени на общение с другими людьми',
                          'Мне очень нравится находиться в окружении людей',
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
            raise BadOrderHQTFLF

        # словарь для замены слов на числа
        dct_replace_value = {'полностью не согласен': 0,
                             'скорее не согласен': 1,
                             'не могу согласиться или не согласиться': 2,
                             'скорее согласен': 3,
                             'полностью согласен': 4,
                             }
        valid_values = [0,1,2,3,4]
        answers_df.replace(dct_replace_value, inplace=True)  # заменяем слова на цифры для подсчетов
        # Проверяем, есть ли значения, отличающиеся от указанных в списке
        lst_error_answers = []  # список для хранения строк где найдены неправильные ответы

        for i in range(25):
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
            raise BadValueHQTFLF

        base_df['ИП_Значение'] = answers_df.apply(calc_value_ip,axis=1)
        base_df['ИП_Диапазон'] = base_df['ИП_Значение'].apply(calc_level)

        base_df['С_Значение'] = answers_df.apply(calc_value_s, axis=1)
        base_df['С_Диапазон'] = base_df['С_Значение'].apply(lambda x:calc_level_sub(x,44))

        base_df['И_Значение'] = answers_df.apply(calc_value_i, axis=1)
        base_df['И_Диапазон'] = base_df['И_Значение'].apply(lambda x:calc_level_sub(x,32))

        base_df['ЭП_Значение'] = answers_df.apply(calc_value_ap, axis=1)
        base_df['ЭП_Диапазон'] = base_df['ЭП_Значение'].apply(lambda x:calc_level_sub(x,24))

        # Создаем датафрейм для создания части в общий датафрейм
        part_df = pd.DataFrame()

        # Основные шкалы
        part_df['ОХЛФ_ИП_Значение'] = base_df['ИП_Значение']
        part_df['ОХЛФ_ИП_Диапазон'] = base_df['ИП_Диапазон']

        part_df['ОХЛФ_С_Значение'] = base_df['С_Значение']
        part_df['ОХЛФ_С_Диапазон'] = base_df['С_Диапазон']

        part_df['ОХЛФ_И_Значение'] = base_df['И_Значение']
        part_df['ОХЛФ_И_Диапазон'] = base_df['И_Диапазон']

        part_df['ОХЛФ_ЭП_Значение'] = base_df['ЭП_Значение']
        part_df['ОХЛФ_ЭП_Диапазон'] = base_df['ЭП_Диапазон']

        out_answer_df = pd.concat([out_answer_df, answers_df], axis=1)  # Датафрейм для проверки

        base_df.sort_values(by='ИП_Значение', ascending=False, inplace=True)  # сортируем

        # Делаем свод  по  шкалам
        dct_svod_l = {'ИП_Значение': 'ИП_Диапазон',
                      }

        dct_rename_svod_l = {'ИП_Значение': 'Интегральный показатель',
                             }

        lst_l = ['0-24', '25-49', '50-74','75-100']

        base_svod_l_df = create_union_svod(base_df, dct_svod_l, dct_rename_svod_l, lst_l)

        # Делаем свод  по  шкалам
        dct_svod_sub = {'С_Значение': 'С_Диапазон',
                        'И_Значение': 'И_Диапазон',
                        'ЭП_Значение': 'ЭП_Диапазон',
                        }

        dct_rename_svod_sub = {'С_Значение': 'Социализация"',
                               'И_Значение': 'Изоляция',
                               'ЭП_Значение': 'Эмоциональная поддержка',
                               }

        lst_sub = ['0-24%', '25-49%', '50-74%','75-100%']

        base_svod_sub_df = create_union_svod(base_df, dct_svod_sub, dct_rename_svod_sub, lst_sub)

        avg_vcha = round(base_df['ИП_Значение'].mean(), 2)
        avg_o = round(base_df['С_Значение'].mean(), 2)
        avg_ruvs = round(base_df['И_Значение'].mean(), 2)
        avg_ap = round(base_df['ЭП_Значение'].mean(), 2)

        avg_dct = {'Среднее значение интегрального показателя': avg_vcha,
                   'Среднее значение шкалы Социализация': avg_o,
                   'Среднее значение шкалы Изоляция': avg_ruvs,
                   'Среднее значение шкалы Эмоциональная поддержка': avg_ap,
                   }

        avg_df = pd.DataFrame.from_dict(avg_dct, orient='index')
        avg_df = avg_df.reset_index()
        avg_df.columns = ['Показатель', 'Среднее значение']
        # формируем основной словарь
        out_dct = {'Списочный результат': base_df,
                   'Список для проверки': out_answer_df,
                   'Свод ИП': base_svod_l_df,
                   'Свод Шкалы': base_svod_sub_df,
                   'Среднее': avg_df,
                   }

        dct_l = {
            'ИП_Диапазон': 'ИП',
        }

        out_dct = create_list_on_level(base_df, out_dct, lst_l, dct_l)

        dct_prefix = {
            'С_Диапазон': 'С',
            'И_Диапазон': 'И',
            'ЭП_Диапазон': 'ЭП',
        }

        out_dct = create_list_on_level(base_df, out_dct, lst_sub, dct_prefix)

        """
                        Сохраняем в зависимости от необходимости делать своды по определенным колонкам
                        """
        if len(lst_svod_cols) == 0:
            return out_dct, part_df

        else:
            out_dct = create_result_hqtf_lyakina(base_df, out_dct, lst_svod_cols)
            return out_dct, part_df

    except BadOrderHQTFLF:
        messagebox.showerror('Лахеcис',
                             f'При обработке вопросов теста Опросник хикикомори, HQ-25 Тео Лякина Федоров обнаружены неправильные вопросы. Проверьте названия колонок с вопросами:\n'
                             f'{error_order_message[:5000]}\n'
                             f'Используйте при создании Яндекс-формы написание вопросов из руководства пользователя программы Лахесис.')
    except BadValueHQTFLF:
        messagebox.showerror('Лахеcис',
                             f'При обработке вопросов теста Опросник хикикомори, HQ-25 Тео Лякина Федоров обнаружены неправильные варианты ответов. Проверьте ответы на указанных строках:\n'
                             f'{error_message[:5000]}\n'
                             f'Используйте при создании Яндекс-формы написание вариантов ответа из руководства пользователя программы Лахесис.')


    except BadCountColumnsHQTFLF:
        messagebox.showerror('Лахеcис',
                             f'Проверьте количество колонок с ответами на тест Опросник хикикомори, HQ-25 Тео Лякина Федоров\n'
                             f'Должно быть 25 колонок с ответами')







