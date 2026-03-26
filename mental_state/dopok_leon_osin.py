"""
Скрипт для обработки результатов Дифференциальный опросник переживания одиночества (краткий вариант) ДОПО-3к Леонтьев Осин
"""

import pandas as pd
import re
from tkinter import messagebox
from lachesis_support_functions import round_mean_two,calc_count_scale,create_union_svod, create_list_on_level

class BadOrderDOPOKLO(Exception):
    """
    Исключение для обработки случая когда колонки не совпадают
    """
    pass


class BadValueDOPOKLO(Exception):
    """
    Исключение для неправильных значений в вариантах ответов
    """
    pass

class BadCountColumnsDOPOKLO(Exception):
    """
    Исключение для обработки случая если количество колонок не равно 24
    """
    pass

def calc_value_oo(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [1,4,5,6,10,14,16,21]
    lst_neg = [4,10]
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


def calc_value_zo(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [2,8,11,13,18,20,23]
    lst_neg = [13]
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

def calc_value_po(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [3,7,9,12,15,17,19,22,24]
    lst_neg = []
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


def create_result_dopok_leon_osin(base_df:pd.DataFrame, out_dct:dict, lst_svod_cols:list):
    """
    Функция для подсчета результата если указаны колонки по которым нужно провести свод
    :param df: датафрейм с результатами
    :param out_dct: словарь с уже подсчитанными базовыми данными
    :param lst_svod_cols: список сводных колонок
    :return: словарь
    """
    lst_level = ['0-24%', '25-49%', '50-74%','75-100%']

    lst_reindex_one_level_cols = lst_svod_cols.copy()
    lst_reindex_one_level_cols.extend(['0-24%', '25-49%', '50-74%','75-100%',
                                       'Итого'])  # Основная шкала

    # АД
    svod_count_one_level_k_df = calc_count_scale(base_df, lst_svod_cols,
                                                 'ОО_Значение',
                                                 'ОО_Диапазон',
                                                 lst_reindex_one_level_cols, lst_level)
    # АВА
    svod_count_one_level_d_df = calc_count_scale(base_df, lst_svod_cols,
                                                 'ЗО_Значение',
                                                 'ЗО_Диапазон',
                                                 lst_reindex_one_level_cols, lst_level)
    # ИЗ
    svod_count_one_level_s_df = calc_count_scale(base_df, lst_svod_cols,
                                                 'ПО_Значение',
                                                 'ПО_Диапазон',
                                                 lst_reindex_one_level_cols, lst_level)

    # Считаем среднее по субшкалам
    svod_mean_one_df = pd.pivot_table(base_df,
                                      index=lst_svod_cols,
                                      values=['ОО_Значение',
                                              'ЗО_Значение',
                                              'ПО_Значение',
                                              ],
                                      aggfunc=round_mean_two)
    svod_mean_one_df.reset_index(inplace=True)

    # упорядочиваем колонки
    new_order_cols = lst_svod_cols.copy()
    new_order_cols.extend((['ОО_Значение',
                            'ЗО_Значение',
                            'ПО_Значение',
                            ]))
    svod_mean_one_df = svod_mean_one_df.reindex(columns=new_order_cols)

    dct_rename_cols_mean = {'ОО_Значение': 'Ср. Общее переживание одиночества',
                            'ЗО_Значение': 'Ср. Зависимость от общения',
                            'ПО_Значение': 'Ср. Позитивное одиночество:',
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
                    f'ОО {out_name}': svod_count_one_level_k_df,
                    f'ЗО {out_name}': svod_count_one_level_d_df,
                    f'ПО {out_name}': svod_count_one_level_s_df,
                    })

    if len(lst_svod_cols) == 1:
        return out_dct
    else:
        for idx, name_column in enumerate(lst_svod_cols):
            lst_reindex_column_level_cols = [lst_svod_cols[idx], '0-24%', '25-49%', '50-74%','75-100%',
                                             'Итого']

            # АД
            svod_count_column_level_k_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                         'ОО_Значение',
                                                         'ОО_Диапазон',
                                                         lst_reindex_column_level_cols, lst_level)
            # АВА
            svod_count_column_level_d_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                         'ЗО_Значение',
                                                         'ЗО_Диапазон',
                                                         lst_reindex_column_level_cols, lst_level)
            # ИЗ
            svod_count_column_level_s_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                         'ПО_Значение',
                                                         'ПО_Диапазон',
                                                         lst_reindex_column_level_cols, lst_level)

            # Считаем среднее по субшкалам
            svod_mean_column_df = pd.pivot_table(base_df,
                                              index=[lst_svod_cols[idx]],
                                              values=['ОО_Значение',
                                                      'ЗО_Значение',
                                                      'ПО_Значение',
                                                      ],
                                              aggfunc=round_mean_two)
            svod_mean_column_df.reset_index(inplace=True)

            # упорядочиваем колонки
            new_order_cols = [lst_svod_cols[idx]].copy()
            new_order_cols.extend((['ОО_Значение',
                                    'ЗО_Значение',
                                    'ПО_Значение',
                                    ]))
            svod_mean_column_df = svod_mean_column_df.reindex(columns=new_order_cols)

            dct_rename_cols_mean = {'ОО_Значение': 'Ср. Общее переживание одиночества',
                                    'ЗО_Значение': 'Ср. Зависимость от общения',
                                    'ПО_Значение': 'Ср. Позитивное одиночество:',
                                    }
            svod_mean_column_df.rename(columns=dct_rename_cols_mean, inplace=True)
            # Готовим наименование
            name_column = lst_svod_cols[idx]
            name_column = re.sub(r'[\[\]\'+()<> :"?*|\\/]', '_', name_column)
            name_column = name_column[:15]
            out_dct.update({f'Ср {name_column}': svod_mean_column_df,
                            f'ОО {name_column}': svod_count_column_level_k_df,
                            f'ЗО {name_column}': svod_count_column_level_d_df,
                            f'ПО {name_column}': svod_count_column_level_s_df,
                            })
        return out_dct





def processing_dopok_leon_osin(base_df: pd.DataFrame, answers_df: pd.DataFrame, lst_svod_cols:list):
    """
    Функция для обработки
    :param base_df: часть датафрейма с описательными колонками
    :param answers_df: часть датафрейма с ответами
    :param lst_svod_cols:  список с колонками по которым нужно делать свод
    """
    try:
        out_answer_df = base_df.copy()  # делаем копию для последующего соединения с сырыми ответами
        if len(answers_df.columns) != 24:  # проверяем количество колонок с вопросами
            raise BadCountColumnsDOPOKLO

        # очищаем названия колонок от возможных сочетаний .1 которые добавляет пандас при одинаковых колонках
        clean_df_lst = []
        for name_column in answers_df.columns:
            clean_name = re.sub(r'.\d+$', '', name_column)
            clean_df_lst.append(clean_name)

        answers_df.columns = clean_df_lst
        lst_check_cols = ['Я чувствую себя одиноким',
                          'Когда рядом со мной никого нет, я испытываю скуку',
                          'Я люблю оставаться наедине с самим собой',
                          'Есть люди, с которыми я могу поговорить',
                          'Нет никого, к кому бы я мог обратиться',
                          'Мне трудно найти людей, с которыми можно было бы поделиться моими мыслями',
                          'В одиночестве приходят интересные идеи',
                          'Мне трудно быть вдали от людей',
                          'Бывают чувства, ощутить которые можно лишь наедине с собой',
                          'Есть люди, которые по-настоящему понимают меня',

                          'Я не люблю оставаться один',
                          'Чтобы понять какие-то важные вещи, человеку необходимо остаться одному',
                          'Когда я остаюсь один, я не испытываю неприятных чувств',
                          'Я чувствую себя покинутым',
                          'В одиночестве голова работает лучше',
                          'Люди вокруг меня, но не со мной',
                          'В одиночестве человек познает самого себя',
                          'Я плохо выношу отсутствие компании',
                          'В одиночестве я чувствую себя самим собой',
                          'Худшее, что можно сделать с человеком, – это оставить его одного',
                          'Мне кажется, что меня никто не понимает',
                          'Мне хорошо дома, когда я один',
                          'Когда я остаюсь один, я испытываю дискомфорт',
                          'В одиночестве каждый видит в себе то, что он есть на самом деле'
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
            raise BadOrderDOPOKLO

        # словарь для замены слов на числа
        dct_replace_value = {'не согласен': 1,
                             'скорее не согласен': 2,
                             'скорее согласен': 3,
                             'согласен': 4,
                             }
        valid_values = [1, 2, 3, 4]
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
            raise BadValueDOPOKLO

        base_df['ОО_Значение'] = answers_df.apply(calc_value_oo, axis=1)
        base_df['ОО_Диапазон'] = base_df['ОО_Значение'].apply(lambda x: calc_level_sub(x, 32))

        base_df['ЗО_Значение'] = answers_df.apply(calc_value_zo, axis=1)
        base_df['ЗО_Диапазон'] = base_df['ЗО_Значение'].apply(lambda x: calc_level_sub(x, 28))
        #
        base_df['ПО_Значение'] = answers_df.apply(calc_value_po, axis=1)
        base_df['ПО_Диапазон'] = base_df['ПО_Значение'].apply(lambda x: calc_level_sub(x, 36))

        # Создаем датафрейм для создания части в общий датафрейм
        part_df = pd.DataFrame()

        # Основные шкалы
        part_df['ДОПОКЛО_ОО_Значение'] = base_df['ОО_Значение']
        part_df['ДОПОКЛО_ОО_Диапазон'] = base_df['ОО_Диапазон']

        part_df['ДОПОКЛО_ЗО_Значение'] = base_df['ЗО_Значение']
        part_df['ДОПОКЛО_ЗО_Диапазон'] = base_df['ЗО_Диапазон']

        part_df['ДОПОКЛО_ПО_Значение'] = base_df['ПО_Значение']
        part_df['ДОПОКЛО_ПО_Диапазон'] = base_df['ПО_Диапазон']

        out_answer_df = pd.concat([out_answer_df, answers_df], axis=1)  # Датафрейм для проверки

        base_df.sort_values(by='ОО_Значение', ascending=False, inplace=True)  # сортируем

        # Делаем свод  по  шкалам
        dct_svod_sub = {'ОО_Значение': 'ОО_Диапазон',
                        'ЗО_Значение': 'ЗО_Диапазон',
                        'ПО_Значение': 'ПО_Диапазон',
                        }

        dct_rename_svod_sub = {'ОО_Значение': 'Общее переживание одиночества',
                               'ЗО_Значение': 'Зависимость от общения',
                               'ПО_Значение': 'Позитивное одиночество:',
                               }

        lst_sub = ['0-24%', '25-49%', '50-74%','75-100%']

        base_svod_sub_df = create_union_svod(base_df, dct_svod_sub, dct_rename_svod_sub, lst_sub)

        avg_vcha = round(base_df['ОО_Значение'].mean(), 2)
        avg_o = round(base_df['ЗО_Значение'].mean(), 2)
        avg_ruvs = round(base_df['ПО_Значение'].mean(), 2)

        avg_dct = {'Среднее значение шкалы Общее переживание одиночества': avg_vcha,
                   'Среднее значение шкалы Зависимость от общения': avg_o,
                   'Среднее значение шкалы Позитивное одиночество:': avg_ruvs,
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

        dct_prefix = {'ОО_Диапазон': 'ОО',
                      'ЗО_Диапазон': 'ЗО',
                      'ПО_Диапазон': 'ПО',
                      }

        out_dct = create_list_on_level(base_df, out_dct, lst_sub, dct_prefix)
        """
                        Сохраняем в зависимости от необходимости делать своды по определенным колонкам
                        """
        if len(lst_svod_cols) == 0:
            return out_dct, part_df

        else:
            out_dct = create_result_dopok_leon_osin(base_df, out_dct, lst_svod_cols)
            return out_dct, part_df

    except BadOrderDOPOKLO:
        messagebox.showerror('Лахеcис',
                             f'При обработке вопросов теста ДОПО-3к Леонтьев Осин обнаружены неправильные вопросы. Проверьте названия колонок с вопросами:\n'
                             f'{error_order_message[:5000]}\n'
                             f'Используйте при создании Яндекс-формы написание вопросов из руководства пользователя программы Лахесис.')
    except BadValueDOPOKLO:
        messagebox.showerror('Лахеcис',
                             f'При обработке вопросов теста ДОПО-3к Леонтьев Осин обнаружены неправильные варианты ответов. Проверьте ответы на указанных строках:\n'
                             f'{error_message[:5000]}\n'
                             f'Используйте при создании Яндекс-формы написание вариантов ответа из руководства пользователя программы Лахесис.')


    except BadCountColumnsDOPOKLO:
        messagebox.showerror('Лахеcис',
                             f'Проверьте количество колонок с ответами на тест ДОПО-3к Леонтьев Осин\n'
                             f'Должно быть 24 колонки с ответами')

