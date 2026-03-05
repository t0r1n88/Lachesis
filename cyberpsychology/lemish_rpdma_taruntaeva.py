"""
Скрипт для обработки результатов теста Опросник Родительское посредничество детской медиаактивности Лемиш Адаптация П.И. Тарунтаева
"""

import pandas as pd
import re
from tkinter import messagebox
from lachesis_support_functions import round_mean_two,calc_count_scale,create_union_svod, create_list_on_level

class BadOrderRPDMALT(Exception):
    """
    Исключение для обработки случая когда колонки не совпадают
    """
    pass


class BadValueRPDMALT(Exception):
    """
    Исключение для неправильных значений в вариантах ответов
    """
    pass

class BadCountColumnsRPDMALT(Exception):
    """
    Исключение для обработки случая если количество колонок не равно 12
    """
    pass

def calc_value_osp(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [1,2,3,4]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_pr:
            value_forward += value
    return value_forward


def calc_value_isp(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [5,6,7,8]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_pr:
            value_forward += value
    return value_forward

def calc_value_ssi(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [9,10,11,12]
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
    if 12<= value <= 24:
        return f'12-24'
    elif 25 <= value <= 37:
        return f'25-37'
    elif 38 <= value <= 50:
        return f'38-50'
    else:
        return f'51-60'


def create_result_rpdma_lem_tarun(base_df:pd.DataFrame, out_dct:dict, lst_svod_cols:list):
    """
    Функция для подсчета результата если указаны колонки по которым нужно провести свод
    :param df: датафрейм с результатами
    :param out_dct: словарь с уже подсчитанными базовыми данными
    :param lst_svod_cols: список сводных колонок
    :return: словарь
    """
    lst_level = ['12-24', '25-37', '38-50', '51-60']

    lst_reindex_one_level_cols = lst_svod_cols.copy()
    lst_reindex_one_level_cols.extend(['12-24', '25-37', '38-50', '51-60',
                                       'Итого'])  # Основная шкала

    svod_count_one_level_vcha_df = calc_count_scale(base_df, lst_svod_cols,
                                                    'Сумма_Значение',
                                                    'Сумма_Диапазон',
                                                    lst_reindex_one_level_cols, lst_level)

    # Считаем среднее по субшкалам
    svod_mean_one_df = pd.pivot_table(base_df,
                                      index=lst_svod_cols,
                                      values=['ОСП_Значение',
                                              'ИСП_Значение',
                                              'ССИ_Значение',
                                              'Сумма_Значение',
                                              ],
                                      aggfunc=round_mean_two)
    svod_mean_one_df.reset_index(inplace=True)

    # упорядочиваем колонки
    new_order_cols = lst_svod_cols.copy()
    new_order_cols.extend((['ОСП_Значение', 'ИСП_Значение',
                            'ССИ_Значение','Сумма_Значение'
                            ]))
    svod_mean_one_df = svod_mean_one_df.reindex(columns=new_order_cols)

    dct_rename_cols_mean = {'ОСП_Значение': 'Ср. Ограничительная стратегия посредничества',
                            'ИСП_Значение': 'Ср. Инструктивная стратегия посредничества',
                            'ССИ_Значение': 'Ср. Стратегия совместного использования',
                            'Сумма_Значение': 'Ср. Общая сумма баллов',
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
                    f'Сумма {out_name}': svod_count_one_level_vcha_df,
                    })

    if len(lst_svod_cols) == 1:
        return out_dct
    else:
        for idx, name_column in enumerate(lst_svod_cols):
            lst_reindex_column_level_cols = [lst_svod_cols[idx],'12-24', '25-37', '38-50', '51-60',
                                                  'Итого']
            # ВЧА
            svod_count_column_level_vcha_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                            'Сумма_Значение',
                                                            'Сумма_Диапазон',
                                                            lst_reindex_column_level_cols, lst_level)

            # Считаем среднее по субшкалам
            svod_mean_column_df = pd.pivot_table(base_df,
                                              index=[lst_svod_cols[idx]],
                                              values=['ОСП_Значение',
                                                      'ИСП_Значение',
                                                      'ССИ_Значение',
                                                      'Сумма_Значение',
                                                      ],
                                              aggfunc=round_mean_two)
            svod_mean_column_df.reset_index(inplace=True)

            # упорядочиваем колонки
            new_order_cols = [lst_svod_cols[idx]].copy()
            new_order_cols.extend((['ОСП_Значение', 'ИСП_Значение',
                                    'ССИ_Значение', 'Сумма_Значение'
                                    ]))
            svod_mean_column_df = svod_mean_column_df.reindex(columns=new_order_cols)

            dct_rename_cols_mean = {'ОСП_Значение': 'Ср. Ограничительная стратегия посредничества',
                                    'ИСП_Значение': 'Ср. Инструктивная стратегия посредничества',
                                    'ССИ_Значение': 'Ср. Стратегия совместного использования',
                                    'Сумма_Значение': 'Ср. Общая сумма баллов',
                                    }
            svod_mean_column_df.rename(columns=dct_rename_cols_mean, inplace=True)

            # Готовим наименование
            name_column = lst_svod_cols[idx]
            name_column = re.sub(r'[\[\]\'+()<> :"?*|\\/]', '_', name_column)
            name_column = name_column[:15]
            out_dct.update({f'Ср {name_column}': svod_mean_column_df,
                            f'Сумма {name_column}': svod_count_column_level_vcha_df,
                            })
        return out_dct










def processing_rpdma_lem_tar(base_df: pd.DataFrame, answers_df: pd.DataFrame, lst_svod_cols:list):
    """
    Функция для обработки
    :param base_df: часть датафрейма с описательными колонками
    :param answers_df: часть датафрейма с ответами
    :param lst_svod_cols:  список с колонками по которым нужно делать свод
    """
    try:
        out_answer_df = base_df.copy()  # делаем копию для последующего соединения с сырыми ответами
        if len(answers_df.columns) != 12:  # проверяем количество колонок с вопросами
            raise BadCountColumnsRPDMALT

        # очищаем названия колонок от возможных сочетаний .1 которые добавляет пандас при одинаковых колонках
        clean_df_lst = []
        for name_column in answers_df.columns:
            clean_name = re.sub(r'.\d+$', '', name_column)
            clean_df_lst.append(clean_name)

        answers_df.columns = clean_df_lst

        lst_check_cols = ['Заранее предупреждаете, когда и сколько по времени ребенок может смотреть фильмы, мультфильмы, YouTube и т.д.',
                          'Обсуждаете с ребенком происходящее на экране во время просмотра',
                          'Вместе с ребенком смотрите фильмы, мультфильмы, YouTube и т.д., которые он выбрал сам и хочет, чтобы Вы к нему присоединились',
                          'Заранее предупреждаете ребенка, какие именно фильмы, мультфильмы, видео на YouTube и т.д. он может посмотреть',
                          'Обсуждаете с ребенком различные фильмы, мультфильмы, видео на YouTube и т.д. (в общем, а не в момент просмотра)',
                          'Вместе с ребенком смотрите фильмы, мультфильмы, YouTube и т.д., которые Вы выбрали сами, и хотите, чтобы ребенок к Вам присоединился',
                          'Заранее предупреждаете, когда и как долго ребенок может играть в игры, использовать различные приложения, веб-сайты и т.д.',
                          'Обсуждаете с ребенком происходящее на экране во время игры или при использовании приложения, веб-сайта и т.д.',
                          'Вместе с ребенком играете в игры, используете приложения, веб-сайты и т.д., которые выбрал ребенок и хочет, чтобы Вы присоединились к нему',
                          'Заранее предупреждаете, какие игры, приложения, веб-сайты и т.д. может использовать ребенок',
                          'Обсуждаете с ребенком различные игры, приложения, веб-сайты и т.д. (в общем, а не в момент просмотра)',
                          'Совместно с ребенком играете в игры, используете приложения, веб-сайты и т.д., которые выбрали Вы и хотите, чтобы ребенок к Вам присоединился',
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
            raise BadOrderRPDMALT

        # словарь для замены слов на числа
        dct_replace_value = {'всегда': 5,
                             'часто': 4,
                             'время от времени': 3,
                             'редко': 2,
                             'никогда': 1,
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
            raise BadValueRPDMALT

        base_df['ОСП_Значение'] = answers_df.apply(calc_value_osp, axis=1)
        base_df['ИСП_Значение'] = answers_df.apply(calc_value_isp, axis=1)
        base_df['ССИ_Значение'] = answers_df.apply(calc_value_ssi, axis=1)

        base_df['Сумма_Значение'] = answers_df.sum(axis=1)
        base_df['Сумма_Диапазон'] = base_df['Сумма_Значение'].apply(calc_level)

        # Создаем датафрейм для создания части в общий датафрейм
        part_df = pd.DataFrame()

        # Основные шкалы
        part_df['РПДМАЛТ_ОСП_Значение'] = base_df['ОСП_Значение']
        part_df['РПДМАЛТ_ИСП_Значение'] = base_df['ИСП_Значение']
        part_df['РПДМАЛТ_ССИ_Значение'] = base_df['ССИ_Значение']

        part_df['РПДМАЛТ_Сумма_Значение'] = base_df['Сумма_Значение']
        part_df['РПДМАЛТ_Сумма_Диапазон'] = base_df['Сумма_Диапазон']


        out_answer_df = pd.concat([out_answer_df, answers_df], axis=1)  # Датафрейм для проверки

        base_df.sort_values(by='Сумма_Значение', ascending=False, inplace=True)  # сортируем

        # Делаем свод  по  шкалам
        dct_svod_sub = {'Сумма_Значение': 'Сумма_Диапазон',
                        }

        dct_rename_svod_sub = {
            'Сумма_Значение': 'Диапазон Суммарного количества баллов',
            }

        lst_sub = ['12-24', '25-37', '38-50', '51-60']

        base_svod_sub_df = create_union_svod(base_df, dct_svod_sub, dct_rename_svod_sub, lst_sub)

        avg_vcha = round(base_df['ОСП_Значение'].mean(), 2)
        avg_o = round(base_df['ИСП_Значение'].mean(), 2)
        avg_ruvs = round(base_df['ССИ_Значение'].mean(), 2)

        avg_psp = round(base_df['Сумма_Значение'].mean(), 2)

        avg_dct = {'Среднее значение шкалы Ограничительная стратегия посредничества': avg_vcha,
                   'Среднее значение шкалы Инструктивная стратегия посредничества': avg_o,
                   'Среднее значение шкалы Стратегия совместного использования': avg_ruvs,

                   'Среднее значение Суммарный показатель': avg_psp,
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

        dct_prefix = {'Сумма_Диапазон': 'Сумма',
                      }

        out_dct = create_list_on_level(base_df, out_dct, lst_sub, dct_prefix)

        """
                        Сохраняем в зависимости от необходимости делать своды по определенным колонкам
                        """
        if len(lst_svod_cols) == 0:
            return out_dct, part_df

        else:
            out_dct = create_result_rpdma_lem_tarun(base_df, out_dct, lst_svod_cols)
            return out_dct, part_df


    except BadOrderRPDMALT:
        messagebox.showerror('Лахеcис',
                             f'При обработке вопросов теста Опросник Родительское посредничество детской медиаактивности Лемиш Тарунтаева обнаружены неправильные вопросы. Проверьте названия колонок с вопросами:\n'
                             f'{error_order_message[:5000]}\n'
                             f'Используйте при создании Яндекс-формы написание вопросов из руководства пользователя программы Лахесис.')
    except BadValueRPDMALT:
        messagebox.showerror('Лахеcис',
                             f'При обработке вопросов теста Опросник Родительское посредничество детской медиаактивности Лемиш Тарунтаева обнаружены неправильные варианты ответов. Проверьте ответы на указанных строках:\n'
                             f'{error_message[:5000]}\n'
                             f'Используйте при создании Яндекс-формы написание вариантов ответа из руководства пользователя программы Лахесис.')


    except BadCountColumnsRPDMALT:
        messagebox.showerror('Лахеcис',
                             f'Проверьте количество колонок с ответами на тест Опросник Родительское посредничество детской медиаактивности Лемиш Тарунтаева\n'
                             f'Должно быть 12 колонок с ответами')