"""
Скрипт для обработки результатов Опросник проблемного использования социальных сетей Сирота, Московченко, Ялтонский, Ялтонская
"""

import pandas as pd
import re
from tkinter import messagebox
from lachesis_support_functions import round_mean_two,calc_count_scale,create_union_svod, create_list_on_level

class BadOrderPISSS(Exception):
    """
    Исключение для обработки случая когда колонки не совпадают
    """
    pass


class BadValuePISSS(Exception):
    """
    Исключение для неправильных значений в вариантах ответов
    """
    pass

class BadCountColumnsPISSS(Exception):
    """
    Исключение для обработки случая если количество колонок не равно 15
    """
    pass


def calc_level(value):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """
    if 3<= value <= 7:
        return f'3-7'
    elif 8 <= value <= 13:
        return f'8-13'
    elif 14 <= value <= 17:
        return f'14-17'
    else:
        return f'18-21'




def calc_value_poo(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [1,2,3]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_pr:
            value_forward += value
    return value_forward

def calc_value_ra(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [4,5,6]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_pr:
            value_forward += value
    return value_forward

def calc_value_kp(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [7,8,9]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_pr:
            value_forward += value
    return value_forward


def calc_value_ki(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [10,11,12]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_pr:
            value_forward += value
    return value_forward

def calc_value_np(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [13,14,15]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_pr:
            value_forward += value
    return value_forward


def create_result_piss_sirota(base_df:pd.DataFrame, out_dct:dict, lst_svod_cols:list):
    """
    Функция для подсчета результата если указаны колонки по которым нужно провести свод
    :param df: датафрейм с результатами
    :param out_dct: словарь с уже подсчитанными базовыми данными
    :param lst_svod_cols: список сводных колонок
    :return: словарь
    """

    lst_level = ['3-7', '8-13', '14-17', '18-21']

    lst_reindex_one_level_cols = lst_svod_cols.copy()
    lst_reindex_one_level_cols.extend(['3-7', '8-13', '14-17', '18-21',
                                       'Итого'])  # Основная шкала

    # АД
    svod_count_one_level_z_df = calc_count_scale(base_df, lst_svod_cols,
                                                 'ПОО_Значение',
                                                 'ПОО_Диапазон',
                                                 lst_reindex_one_level_cols, lst_level)

    # АД
    svod_count_one_level_mo_df = calc_count_scale(base_df, lst_svod_cols,
                                                  'РЭ_Значение',
                                                  'РЭ_Диапазон',
                                                  lst_reindex_one_level_cols, lst_level)

    # АД
    svod_count_one_level_t_df = calc_count_scale(base_df, lst_svod_cols,
                                                 'КП_Значение',
                                                 'КП_Диапазон',
                                                 lst_reindex_one_level_cols, lst_level)

    # АД
    svod_count_one_level_s_df = calc_count_scale(base_df, lst_svod_cols,
                                                 'КИ_Значение',
                                                 'КИ_Диапазон',
                                                 lst_reindex_one_level_cols, lst_level)

    # АД
    svod_count_one_level_k_df = calc_count_scale(base_df, lst_svod_cols,
                                                 'НП_Значение',
                                                 'НП_Диапазон',
                                                 lst_reindex_one_level_cols, lst_level)

    # Считаем среднее по субшкалам
    svod_mean_one_df = pd.pivot_table(base_df,
                                      index=lst_svod_cols,
                                      values=['ПОО_Значение',
                                              'РЭ_Значение',
                                              'КП_Значение',
                                              'КИ_Значение',

                                              'НП_Значение',
                                              ],
                                      aggfunc=round_mean_two)
    svod_mean_one_df.reset_index(inplace=True)

    # упорядочиваем колонки
    new_order_cols = lst_svod_cols.copy()
    new_order_cols.extend((['ПОО_Значение',
                            'РЭ_Значение',
                            'КП_Значение',
                            'КИ_Значение',

                            'НП_Значение',
                            ]))
    svod_mean_one_df = svod_mean_one_df.reindex(columns=new_order_cols)

    dct_rename_cols_mean = {'ПОО_Значение': 'Ср. Предпочтение онлайн-общения',
                            'РЭ_Значение': 'Ср. Регуляция эмоций',
                            'КП_Значение': 'Ср. Когнитивная поглощенность',
                            'КИ_Значение': 'Ср. Компульсивное использование',

                            'НП_Значение': 'Ср. Негативные последствия',
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
                    f'ПОО {out_name}': svod_count_one_level_z_df,
                    f'РЭ {out_name}': svod_count_one_level_mo_df,
                    f'КП {out_name}': svod_count_one_level_t_df,
                    f'КИ {out_name}': svod_count_one_level_s_df,

                    f'НП {out_name}': svod_count_one_level_k_df,
                    })

    if len(lst_svod_cols) == 1:
        return out_dct
    else:
        for idx, name_column in enumerate(lst_svod_cols):

            lst_reindex_column_level_cols = [lst_svod_cols[idx], '3-7', '8-13', '14-17', '18-21',
                                             'Итого']
            # АД
            svod_count_column_level_z_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                            'ПОО_Значение',
                                                            'ПОО_Диапазон',
                                                            lst_reindex_column_level_cols, lst_level)

            # АД
            svod_count_column_level_mo_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                             'РЭ_Значение',
                                                             'РЭ_Диапазон',
                                                             lst_reindex_column_level_cols, lst_level)

            # АД
            svod_count_column_level_t_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                            'КП_Значение',
                                                            'КП_Диапазон',
                                                            lst_reindex_column_level_cols, lst_level)

            # АД
            svod_count_column_level_s_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                            'КИ_Значение',
                                                            'КИ_Диапазон',
                                                            lst_reindex_column_level_cols, lst_level)

            # АД
            svod_count_column_level_k_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                            'НП_Значение',
                                                            'НП_Диапазон',
                                                            lst_reindex_column_level_cols, lst_level)

            # Считаем среднее по субшкалам
            svod_mean_column_df = pd.pivot_table(base_df,
                                                 index=[lst_svod_cols[idx]],
                                                 values=['ПОО_Значение',
                                                         'РЭ_Значение',
                                                         'КП_Значение',
                                                         'КИ_Значение',

                                                         'НП_Значение',
                                                         ],
                                                 aggfunc=round_mean_two)
            svod_mean_column_df.reset_index(inplace=True)

            # упорядочиваем колонки
            new_order_cols = [lst_svod_cols[idx]].copy()
            new_order_cols.extend((['ПОО_Значение',
                                    'РЭ_Значение',
                                    'КП_Значение',
                                    'КИ_Значение',

                                    'НП_Значение',
                                    ]))
            svod_mean_column_df = svod_mean_column_df.reindex(columns=new_order_cols)

            dct_rename_cols_mean = {'ПОО_Значение': 'Ср. Предпочтение онлайн-общения',
                                    'РЭ_Значение': 'Ср. Регуляция эмоций',
                                    'КП_Значение': 'Ср. Когнитивная поглощенность',
                                    'КИ_Значение': 'Ср. Компульсивное использование',

                                    'НП_Значение': 'Ср. Негативные последствия',
                                    }
            svod_mean_column_df.rename(columns=dct_rename_cols_mean, inplace=True)

            # Готовим наименование
            name_column = lst_svod_cols[idx]
            name_column = re.sub(r'[\[\]\'+()<> :"?*|\\/]', '_', name_column)
            name_column = name_column[:15]

            out_dct.update({f'Ср {name_column}': svod_mean_column_df,
                            f'ПОО {name_column}': svod_count_column_level_z_df,
                            f'РЭ {name_column}': svod_count_column_level_mo_df,
                            f'КП {name_column}': svod_count_column_level_t_df,
                            f'КИ {name_column}': svod_count_column_level_s_df,

                            f'НП {name_column}': svod_count_column_level_k_df,
                            })
        return out_dct







def processing_piss_sirota(base_df: pd.DataFrame, answers_df: pd.DataFrame, lst_svod_cols:list):
    """
    Функция для обработки
    :param base_df: часть датафрейма с описательными колонками
    :param answers_df: часть датафрейма с ответами
    :param lst_svod_cols:  список с колонками по которым нужно делать свод
    """
    try:
        count_descr_cols = base_df.shape[1] # количество анкетных колонок

        out_answer_df = base_df.copy()  # делаем копию для последующего соединения с сырыми ответами
        if len(answers_df.columns) != 15:  # проверяем количество колонок с вопросами
            raise BadCountColumnsPISSS

        # очищаем названия колонок от возможных сочетаний .1 которые добавляет пандас при одинаковых колонках
        clean_df_lst = []
        for name_column in answers_df.columns:
            clean_name = re.sub(r'.\d+$', '', name_column)
            clean_df_lst.append(clean_name)

        answers_df.columns = clean_df_lst

        lst_check_cols = ['Я предпочитаю общение в социальных сетях общению лицом к лицу',
                          'Общение в социальных сетях для меня более комфортно, чем общение в реальной жизни',
                          'Я предпочитаю общаться с людьми в социальных сетях, а не в реальности',
                          'Я заходил(а) в социальную сеть, чтобы с кем-то поговорить, когда мне было одиноко',
                          'Я заходил(а) в социальную сеть, чтобы мне стало лучше, когда я чувствовал(а) себя плохо',
                          'Я заходил(а) в социальную сеть, чтобы мне стало лучше, когда расстраивался/лась',
                          'Если я некоторое время не захожу в социальную сеть, меня начинают терзать мысли, что надо зайти',
                          'Если бы я потерял(а) доступ к социальным сетям, я не знал(а) бы что делать.',
                          'Я поглощен(а) навязчивыми мыслями о том, что нужно зайти в социальную сеть, даже когда не сижу в Интернете.',
                          'Мне сложно контролировать, сколько времени я провожу в социальных сетях',

                          'Я считаю, что мне нелегко контролировать мое пребывание в социальных сетях',
                          'Мне тяжело противостоять непреодолимому желанию зайти в социальную сеть, когда я занят чем-то вне Интернета',
                          'Социальные сети усложнили мне жизнь',
                          'Из-за того, что я проводил(ла) много времени в социальных сетях, я пренебрегал(ла) своей социальной жизнью и различными мероприятиями',
                          'Пользование социальными сетями привело к проблемам в моей жизни'

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
            raise BadOrderPISSS

        answers_df = answers_df.astype(str)

        # словарь для замены слов на числа
        dct_replace_value = {'1 – полностью не согласен': 1,
                             '2': 2,
                             '3': 3,
                             '4- нейтрально': 4,
                             '5': 5,
                             '6': 6,
                             '7- полностью согласен': 7,
                             }
        valid_values = [1,2,3,4,5,6,7]
        answers_df.replace(dct_replace_value, inplace=True)  # заменяем слова на цифры для подсчетов
        # Проверяем, есть ли значения, отличающиеся от указанных в списке
        lst_error_answers = []  # список для хранения строк где найдены неправильные ответы

        for i in range(15):
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
            raise BadValuePISSS

        base_df['ПОО_Значение'] = answers_df.apply(calc_value_poo, axis=1)
        base_df['ПОО_Диапазон'] = base_df['ПОО_Значение'].apply(calc_level)

        base_df['РЭ_Значение'] = answers_df.apply(calc_value_ra, axis=1)
        base_df['РЭ_Диапазон'] = base_df['РЭ_Значение'].apply(calc_level)

        base_df['КП_Значение'] = answers_df.apply(calc_value_kp, axis=1)
        base_df['КП_Диапазон'] = base_df['КП_Значение'].apply(calc_level)

        base_df['КИ_Значение'] = answers_df.apply(calc_value_ki, axis=1)
        base_df['КИ_Диапазон'] = base_df['КИ_Значение'].apply(calc_level)

        base_df['НП_Значение'] = answers_df.apply(calc_value_np, axis=1)
        base_df['НП_Диапазон'] = base_df['НП_Значение'].apply(calc_level)

        # Создаем датафрейм для создания части в общий датафрейм
        temp_df = base_df.copy()  # делаем копию
        part_df = temp_df.iloc[:, count_descr_cols:]
        part_df = part_df.add_prefix('ПИСССМЯЯ_')

        out_answer_df = pd.concat([out_answer_df, answers_df], axis=1)  # Датафрейм для проверки

        base_df.sort_values(by='НП_Значение', ascending=False, inplace=True)  # сортируем

        # Делаем свод  по  шкалам
        dct_svod_sub = {'ПОО_Значение': 'ПОО_Диапазон',
                        'РЭ_Значение': 'РЭ_Диапазон',
                        'КП_Значение': 'КП_Диапазон',
                        'КИ_Значение': 'КИ_Диапазон',

                        'НП_Значение': 'НП_Диапазон',

                        }

        dct_rename_svod_sub = {'ПОО_Значение': 'Предпочтение онлайн-общения',
                               'РЭ_Значение': 'Регуляция эмоций',
                               'КП_Значение': 'Когнитивная поглощенность',
                               'КИ_Значение': 'Компульсивное использование',

                               'НП_Значение': 'Негативные последствия',
                               }

        lst_sub = ['3-7', '8-13', '14-17', '18-21']

        base_svod_sub_df = create_union_svod(base_df, dct_svod_sub, dct_rename_svod_sub, lst_sub)

        avg_z = round(base_df['ПОО_Значение'].mean(), 2)
        avg_mo = round(base_df['РЭ_Значение'].mean(), 2)
        avg_t = round(base_df['КП_Значение'].mean(), 2)
        avg_s = round(base_df['КИ_Значение'].mean(), 2)

        avg_k = round(base_df['НП_Значение'].mean(), 2)

        avg_dct = {'Среднее значение шкалы Предпочтение онлайн-общения': avg_z,
                   'Среднее значение шкалы Регуляция эмоций': avg_mo,
                   'Среднее значение шкалы Когнитивная поглощенность': avg_t,
                   'Среднее значение шкалы Компульсивное использование': avg_s,

                   'Среднее значение шкалы Негативные последствия': avg_k,
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

        dct_prefix = {
            'ПОО_Диапазон': 'ПОО',
            'РЭ_Диапазон': 'РЭ',
            'КП_Диапазон': 'КП',
            'КИ_Диапазон': 'КИ',

            'НП_Диапазон': 'НП',
        }

        out_dct = create_list_on_level(base_df, out_dct, lst_sub, dct_prefix)

        """
                        Сохраняем в зависимости от необходимости делать своды по определенным колонкам
                        """
        if len(lst_svod_cols) == 0:
            return out_dct, part_df

        else:
            out_dct = create_result_piss_sirota(base_df, out_dct, lst_svod_cols)
            return out_dct, part_df


    except BadOrderPISSS:
        messagebox.showerror('Лахеcис',
                             f'При обработке вопросов теста Опросник проблемного использования социальных сетей Сирота, Московченко, Ялтонский, Ялтонская обнаружены неправильные вопросы. Проверьте названия колонок с вопросами:\n'
                             f'{error_order_message[:5000]}\n'
                             f'Используйте при создании Яндекс-формы написание вопросов из руководства пользователя программы Лахесис.')
    except BadValuePISSS:
        messagebox.showerror('Лахеcис',
                             f'При обработке вопросов теста Опросник проблемного использования социальных сетей Сирота, Московченко, Ялтонский, Ялтонская обнаружены неправильные варианты ответов. Проверьте ответы на указанных строках:\n'
                             f'{error_message[:5000]}\n'
                             f'Используйте при создании Яндекс-формы написание вариантов ответа из руководства пользователя программы Лахесис.')


    except BadCountColumnsPISSS:
        messagebox.showerror('Лахеcис',
                             f'Проверьте количество колонок с ответами на тест Опросник проблемного использования социальных сетей Сирота, Московченко, Ялтонский, Ялтонская\n'
                             f'Должно быть 15 колонок с ответами')


