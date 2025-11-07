"""
Скрипт для обработки «Оценка коммуникативных и организаторских способностей» (КОС-1) Тест - опросник Б.А. Федоришина
"""

import pandas as pd
import re
from tkinter import messagebox
from lachesis_support_functions import round_mean_two, create_union_svod,create_list_on_level

class BadOrderKOSOne(Exception):
    """
    Исключение для обработки случая когда колонки не совпадают
    """
    pass


class BadValueKOSOne(Exception):
    """
    Исключение для неправильных значений в вариантах ответов
    """
    pass

class BadCountColumnsKOSOne(Exception):
    """
    Исключение для обработки случая если количество колонок не равно 40
    """
    pass

def calc_value_com_cos_one(row):
    """
    Функция для подсчета значения коммуникативных навыков КОС-1
    :param row: строка с ответами
    :return: число
    """
    value_forward = 0 # счетчик депрессии прямых ответов
    value_reverse = 0 # счетчик депрессии обратных ответов
    lst_forward = [1,5,9,13,17,21,25,29,33,37]  #  подсчет если значение Да
    lst_reverse = [3,7,11,15,19,23,27,31,35,39] # подсчет если значение Нет
    for idx, value in enumerate(row):
        if idx + 1 in lst_forward:
            # print(f'Прямой подсчет {idx +1}') # Для проверки корректности
            if value == 'Да':
                value_forward += 1
        elif idx +1 in lst_reverse:
            if value == 'Нет':
                value_reverse += 1
            # print(f'Обратный подсчет {idx +1}')# Для проверки корректности


    return (value_forward + value_reverse) * 0.05

def calc_est_com_cos_one(value):
    """
    Функция для подсчета оценки коммуникативных способностей КОС-1
    :param value:
    :return:
    """
    if 0.10 <= value <= 0.45:
        return 1
    elif 0.46 <= value <= 0.55:
        return 2
    elif 0.56 <= value <= 0.65:
        return 3
    elif 0.66 <= value <= 0.75:
        return 4
    elif 0.76 <= value <= 1:
        return 5



def calc_level_com_cos_one(value):
    """
    Функция для подсчета уровня коммуникативных способностей КОС-1
    :param value:
    :return:
    """
    if value == 1:
        return 'низкий'
    elif value == 2:
        return 'ниже среднего'
    elif value == 3:
        return 'средний'
    elif value == 4:
        return 'высокий'
    elif value == 5:
        return 'очень высокий'


def calc_value_org_cos_one(row):
    """
    Функция для подсчета значения коммуникативных навыков КОС-1
    :param row: строка с ответами
    :return: число
    """
    value_forward = 0 # счетчик депрессии прямых ответов
    value_reverse = 0 # счетчик депрессии обратных ответов
    lst_forward = [2,6,10,14,18,22,26,30,34,38]  #  подсчет если значение Да
    lst_reverse = [4,8,12,16,20,24,28,32,36,40] # подсчет если значение Нет
    for idx, value in enumerate(row):
        if idx + 1 in lst_forward:
            # print(f'Прямой подсчет {idx +1}') # Для проверки корректности
            if value == 'Да':
                value_forward += 1
        elif idx +1 in lst_reverse:
            if value == 'Нет':
                value_reverse += 1
            # print(f'Обратный подсчет {idx +1}')# Для проверки корректности


    return (value_forward + value_reverse) * 0.05


def calc_est_org_cos_one(value):
    """
    Функция для подсчета оценки организационных способностей КОС-1
    :param value:
    :return:
    """
    if 0.20 <= value <= 0.55:
        return 1
    elif 0.56 <= value <= 0.65:
        return 2
    elif 0.66 <= value <= 0.70:
        return 3
    elif 0.71 <= value <= 0.80:
        return 4
    elif 0.81 <= value <= 1:
        return 5



def calc_level_org_cos_one(value):
    """
    Функция для подсчета уровня организационных способностей КОС-1
    :param value:
    :return:
    """
    if value == 1:
        return 'низкий'
    elif value == 2:
        return 'ниже среднего'
    elif value == 3:
        return 'средний'
    elif value == 4:
        return 'высокий'
    elif value == 5:
        return 'очень высокий'


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
    count_df['% низкий от общего'] = round(
        count_df['низкий'] / count_df['Итого'], 2) * 100
    count_df['% ниже среднего от общего'] = round(
        count_df['ниже среднего'] / count_df['Итого'], 2) * 100
    count_df['% средний от общего'] = round(
        count_df['средний'] / count_df['Итого'], 2) * 100
    count_df['% высокий от общего'] = round(
        count_df['высокий'] / count_df['Итого'], 2) * 100
    count_df['% очень высокий от общего'] = round(
        count_df['очень высокий'] / count_df['Итого'], 2) * 100

    return count_df


def create_result_kos_one(base_df:pd.DataFrame, out_dct:dict, lst_svod_cols:list):
    """
    Функция для подсчета результата если указаны колонки по которым нужно провести свод
    :param df: датафрейм с результатами
    :param out_dct: словарь с уже подсчитанными базовыми данными
    :param lst_svod_cols: список сводных колонок
    :return: словарь
    """
    # Тревожность
    lst_reindex_one_level_cols = lst_svod_cols.copy()
    lst_reindex_one_level_cols.extend( ['низкий', 'ниже среднего', 'средний',
                    'высокий', 'очень высокий',
                                   'Итого'])

    # Субшкалы
    svod_count_one_level_kn_df = calc_count_level(base_df, lst_svod_cols,
                                                      'Значение_ком_навыков',
                                                      'Уровень_ком_навыков',
                                                       lst_reindex_one_level_cols)

    svod_count_one_level_on_df = calc_count_level(base_df, lst_svod_cols,
                                                          'Значение_орг_навыков',
                                                          'Уровень_орг_навыков',
                                                     lst_reindex_one_level_cols)

    # Считаем среднее по субшкалам
    svod_mean_one_df = pd.pivot_table(base_df,
                                      index=lst_svod_cols,
                                      values=['Значение_ком_навыков',
                                              'Значение_орг_навыков',
                                              ],
                                      aggfunc=round_mean_two)
    svod_mean_one_df.reset_index(inplace=True)
    # упорядочиваем колонки
    new_order_cols = lst_svod_cols.copy()
    new_order_cols.extend((['Значение_ком_навыков',
                            'Значение_орг_навыков',
                            ]))
    svod_mean_one_df = svod_mean_one_df.reindex(columns=new_order_cols)

    dct_rename_cols_mean = {'Значение_ком_навыков': 'Ср. Коммуникативные навыки',
                            'Значение_орг_навыков': 'Ср. Организационные навыки',
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
                    f'Свод КН {out_name}': svod_count_one_level_kn_df,
                    f'Свод ОН {out_name}': svod_count_one_level_on_df,
                    })

    if len(lst_svod_cols) == 1:
        return out_dct
    else:

        for idx, name_column in enumerate(lst_svod_cols):
            lst_reindex_main_column_cols = [lst_svod_cols[idx], 'низкий', 'ниже среднего', 'средний',
                        'высокий', 'очень высокий','Итого']

            # Субшкалы
            svod_count_column_level_kn_df = calc_count_level(base_df, lst_svod_cols[idx],
                                                          'Значение_ком_навыков',
                                                          'Уровень_ком_навыков',
                                                          lst_reindex_main_column_cols)

            svod_count_column_level_on_df = calc_count_level(base_df, lst_svod_cols[idx],
                                                          'Значение_орг_навыков',
                                                          'Уровень_орг_навыков',
                                                          lst_reindex_main_column_cols)

            # Считаем среднее по субшкалам
            svod_mean_column_df = pd.pivot_table(base_df,
                                              index=[lst_svod_cols[idx]],
                                              values=['Значение_ком_навыков',
                                                      'Значение_орг_навыков',
                                                      ],
                                              aggfunc=round_mean_two)
            svod_mean_column_df.reset_index(inplace=True)
            # упорядочиваем колонки
            new_order_cols = [lst_svod_cols[idx]].copy()
            new_order_cols.extend((['Значение_ком_навыков',
                                    'Значение_орг_навыков',
                                    ]))
            svod_mean_column_df = svod_mean_column_df.reindex(columns=new_order_cols)

            dct_rename_cols_mean = {'Значение_ком_навыков': 'Ср. Коммуникативные навыки',
                                    'Значение_орг_навыков': 'Ср. Организационные навыки',
                                    }
            svod_mean_column_df.rename(columns=dct_rename_cols_mean, inplace=True)

            name_column = lst_svod_cols[idx]
            name_column = re.sub(r'[\[\]\'+()<> :"?*|\\/]', '_', name_column)
            name_column = name_column[:15]
            out_dct.update({f'Ср {name_column}': svod_mean_column_df,
                            f'Свод КН {name_column}': svod_count_column_level_kn_df,
                            f'Свод ОН {name_column}': svod_count_column_level_on_df,
                            })
        return out_dct











def processing_kos_one(result_df: pd.DataFrame, answers_df: pd.DataFrame, lst_svod_cols:list):
    """
    Функция для обработки
    :param result_df: часть датафрейма с описательными колонками
    :param answers_df: часть датафрейма с ответами
    :param lst_svod_cols:  список с колонками по которым нужно делать свод
    """
    try:
        out_answer_df = result_df.copy()  # делаем копию для последующего соединения с сырыми ответами
        if len(answers_df.columns) != 40:  # проверяем количество колонок с вопросами
            raise BadCountColumnsKOSOne

        # очищаем названия колонок от возможных сочетаний .1 которые добавляет пандас при одинаковых колонках
        clean_df_lst = []
        for name_column in answers_df.columns:
            clean_name = re.sub(r'.\d+$', '', name_column)
            clean_df_lst.append(clean_name)

        answers_df.columns = clean_df_lst

        # Словарь с проверочными данными
        lst_check_cols = ['Много ли у вас друзей, с которыми вы постоянно общаетесь?',
                          'Часто ли вам удаётся склонить большинство своих друзей к принятию ими вашего мнения?',
                          'Долго ли вас беспокоит чувство обиды, причинённое вам кем-то из ваших друзей?',
                          'Всегда ли вам трудно ориентироваться в создавшейся критической ситуации?',
                          'Есть ли у вас стремление к установлению новых знакомств с разными людьми?',
                          'Нравится ли вам заниматься общественной работой?',
                          'Верно ли, что вам приятнее проще проводить время с книгами, за компьютером, чем с людьми?',
                          'Если возникли какие – либо помехи в осуществлении ваших планов, легко ли вы отступаете от них?',
                          'Легко ли вы устанавливаете контакты с людьми, которые значительно старше вас?',
                          'Любите ли вы придумывать и организовывать со своими друзьями различные игры и развлечения?',
                          'Трудно ли вы включаетесь в новую для вас компанию?',
                          'Часто ли вы откладываете на другие дни те дела, которые нужно было бы выполнить сегодня?',
                          'Легко ли вам удается устанавливать контакты с незнакомыми людьми?',
                          'Стремитесь ли вы добиваться, чтобы ваши друзья действовали в соответствии с вашим мнением?',
                          'Трудно ли вы осваиваетесь в новом коллективе?',
                          'Верно ли, что у вас не бывает конфликтов с друзьями из-за невыполнения ими своих обязанностей, обязательств?',
                          'Стремитесь ли вы при удобном случае познакомиться и побеседовать с новым человеком?',
                          'Часто ли в решении важных вопросов вы принимаете инициативу на себя?',
                          'Раздражают ли вас окружающие люди, и хочется ли вам побыть одному?',
                          'Правда ли, что вы обычно плохо ориентируетесь в незнакомой обстановке?',
                          'Нравится ли вам постоянно находиться среди людей?',
                          'Возникает ли у вас раздражение, если вам не удается закончить начатое дело?',
                          'Испытываете ли вы затруднения, неудобства или стеснение, если приходится проявлять инициативу, чтобы познакомиться с новым человеком?',
                          'Правда ли, что вы утомляетесь от частого общения с друзьями?',
                          'Любите ли вы участвовать в коллективных играх?',
                          'Часто ли вы проявляете инициативу при решении вопросов, затрагивающих интересы ваших друзей?',
                          'Правда ли, что вы чувствуете себя неуверенно среди мало знакомой компании?',
                          'Верно ли, что вы редко стремитесь к доказательству своей правоты?',
                          'Полагаете ли вы, что вам не доставляет особого труда внести оживление в малознакомую вам компанию?',
                          'Принимаете ли вы участие в общественной работе в школе, техникуме?',
                          'Стремитесь ли вы ограничить круг своих знакомых небольшим количеством человек?',
                          'Верно ли, что вы не стремитесь отстаивать своё мнение, если оно не сразу было принято вашими товарищами?',
                          'Чувствуете ли вы себя непринуждённо, попав в незнакомую компанию?',
                          'Охотно ли вы приступаете к организации различных мероприятий для своих знакомых и друзей?',
                          'Правда ли, что не чувствуете себя достаточно уверенным и спокойным, когда приходится говорить что-либо большой группе людей?',
                          'Всегда ли вы опаздываете на деловые свидания и встречи?',
                          'Верно ли, что у вас много друзей?',
                          'Часто ли, вы оказываетесь в центре внимания своих друзей?',
                          'Часто ли вы смущаетесь, чувствуете неловкость при общении с малознакомыми людьми?',
                          'Правда ли, что вы не очень уверенно чувствуете себя в окружении большой группы своих друзей?',
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
            raise BadOrderKOSOne

        valid_values = ['Да', 'Нет']

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
            raise BadValueKOSOne

        base_df = pd.DataFrame()

        # Коммуникативные новыки
        base_df['Значение_ком_навыков'] = answers_df.apply(calc_value_com_cos_one, axis=1)
        base_df['Норма_ком_навыков'] = '0,45-0,75'
        base_df['Оценка_ком_навыков'] = base_df['Значение_ком_навыков'].apply(calc_est_com_cos_one)
        base_df['Уровень_ком_навыков'] = base_df['Оценка_ком_навыков'].apply(calc_level_com_cos_one)

        # Организационные навыки
        base_df['Значение_орг_навыков'] = answers_df.apply(calc_value_org_cos_one, axis=1)
        base_df['Норма_орг_навыков'] = '0,56-0,80'
        base_df['Оценка_орг_навыков'] = base_df['Значение_орг_навыков'].apply(calc_est_org_cos_one)
        base_df['Уровень_орг_навыков'] = base_df['Оценка_орг_навыков'].apply(calc_level_org_cos_one)

        # Создаем датафрейм для создания части в общий датафрейм
        part_df = pd.DataFrame()
        part_df['КОС_один_КН_Значение'] = base_df['Значение_ком_навыков']
        part_df['КОС_один_КН_Уровень'] = base_df['Уровень_ком_навыков']
        part_df['КОС_один_ОН_Значение'] = base_df['Значение_орг_навыков']
        part_df['КОС_один_ОН_Уровень'] = base_df['Уровень_орг_навыков']

        out_answer_df = pd.concat([out_answer_df, answers_df], axis=1)  # Датафрейм для проверки

        # Соединяем анкетную часть с результатной
        base_df = pd.concat([result_df, base_df], axis=1)
        base_df.sort_values(by='Значение_ком_навыков', ascending=False, inplace=True)  # сортируем

        # формируем основной словарь
        out_dct = {'Списочный результат': base_df, 'Список для проверки': out_answer_df,
                   }

        # Делаем свод по интегральным показателям
        dct_svod_integral = {'Значение_ком_навыков': 'Уровень_ком_навыков',
                             'Значение_орг_навыков': 'Уровень_орг_навыков',
                             }

        dct_rename_svod_integral = {'Значение_ком_навыков': 'Ком.навыки',
                                    'Значение_орг_навыков': 'Орг.навыки',
                                    }

        lst_integral = ['низкий', 'ниже среднего', 'средний',
                        'высокий', 'очень высокий']

        base_svod_integral_df = create_union_svod(base_df, dct_svod_integral, dct_rename_svod_integral, lst_integral)

        # считаем среднее
        avg_kn = round(base_df['Значение_ком_навыков'].mean(), 2)
        avg_on = round(base_df['Значение_орг_навыков'].mean(), 2)

        avg_dct = {'Среднее значение Коммуникационные навыки ': avg_kn,
                   'Среднее значение Организационные навыки': avg_on,

                   }

        avg_df = pd.DataFrame.from_dict(avg_dct, orient='index')
        avg_df = avg_df.reset_index()
        avg_df.columns = ['Показатель', 'Среднее значение']

        out_dct.update({'Свод': base_svod_integral_df,
                        'Среднее': avg_df}
                       )

        dct_prefix = {'Уровень_ком_навыков': 'КН',
                      'Уровень_орг_навыков': 'ОН',
                      }

        out_dct = create_list_on_level(base_df, out_dct, lst_integral, dct_prefix)

        """
            Сохраняем в зависимости от необходимости делать своды по определенным колонкам
            """
        if len(lst_svod_cols) == 0:
            return out_dct, part_df
        else:
            out_dct = create_result_kos_one(base_df, out_dct, lst_svod_cols)

            return out_dct, part_df


    except BadOrderKOSOne:
        messagebox.showerror('Лахеcис',
                             f'При обработке вопросов теста Оценка коммуникативных и организаторских способностей КОС-1 обнаружены неправильные вопросы. Проверьте названия колонок с вопросами:\n'
                             f'{error_order_message[:5000]}\n'
                             f'Используйте при создании Яндекс-формы написание вопросов из руководства пользователя программы Лахесис.')
    except BadValueKOSOne:
        messagebox.showerror('Лахеcис',
                             f'При обработке вопросов теста Оценка коммуникативных и организаторских способностей КОС-1 обнаружены неправильные варианты ответов. Проверьте ответы на указанных строках:\n'
                             f'{error_message[:5000]}\n'
                             f'Используйте при создании Яндекс-формы написание вариантов ответа из руководства пользователя программы Лахесис.')

    except BadCountColumnsKOSOne:
        messagebox.showerror('Лахеcис',
                             f'Проверьте количество колонок с ответами на тест Оценка коммуникативных и организаторских способностей КОС-1\n'
                             f'Должно быть 40 колонок с вопросами'
                             )



