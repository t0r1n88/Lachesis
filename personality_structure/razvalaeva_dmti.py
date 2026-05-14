"""
Скрипт для обработки результатов Опросник Тенденции в принятии решений DMTI Разваляева
"""

import pandas as pd
import re
from tkinter import messagebox
from lachesis_support_functions import round_mean_two,calc_count_scale,create_union_svod, create_list_on_level

class BadOrderDMTIR(Exception):
    """
    Исключение для обработки случая когда колонки не совпадают
    """
    pass


class BadValueDMTIR(Exception):
    """
    Исключение для неправильных значений в вариантах ответов
    """
    pass

class BadCountColumnsDMTIR(Exception):
    """
    Исключение для обработки случая если количество колонок не равно 20
    """
    pass



def calc_level(value):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """
    if 1.0<= value < 3 :
        return f'1-2.9'
    elif 3 <= value <5:
        return f'3-4.9'
    elif 5 <= value < 6:
        return f'5-5.9'
    else:
        return f'6-7'




def calc_value_ma(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [1,2,3,5,18]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_pr:
            value_forward += value

    return round(value_forward / len(lst_pr),1)

def calc_value_s(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [6,8,10,12,14,16]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_pr:
            value_forward += value

    return round(value_forward / len(lst_pr),1)

def calc_value_mi(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [4,7,9,11,13,15,17,19,20]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_pr:
            value_forward += value

    return round(value_forward / len(lst_pr),1)


def create_result_dmti_raz(base_df:pd.DataFrame, out_dct:dict, lst_svod_cols:list):
    """
    Функция для подсчета результата если указаны колонки по которым нужно провести свод
    :param df: датафрейм с результатами
    :param out_dct: словарь с уже подсчитанными базовыми данными
    :param lst_svod_cols: список сводных колонок
    :return: словарь
    """
    lst_level = ['1-2.9', '3-4.9', '5-5.9','6-7']

    lst_reindex_one_level_cols = lst_svod_cols.copy()
    lst_reindex_one_level_cols.extend(['1-2.9', '3-4.9', '5-5.9','6-7',
                                       'Итого'])  # Основная шкала

    # АД
    svod_count_one_level_ma_df = calc_count_scale(base_df, lst_svod_cols,
                                                 'МА_Значение',
                                                 'МА_Диапазон',
                                                 lst_reindex_one_level_cols, lst_level)
    svod_count_one_level_s_df = calc_count_scale(base_df, lst_svod_cols,
                                                 'С_Значение',
                                                 'С_Диапазон',
                                                 lst_reindex_one_level_cols, lst_level)
    svod_count_one_level_mi_df = calc_count_scale(base_df, lst_svod_cols,
                                                 'МИ_Значение',
                                                 'МИ_Диапазон',
                                                 lst_reindex_one_level_cols, lst_level)


    # Считаем среднее по субшкалам
    svod_mean_one_df = pd.pivot_table(base_df,
                                      index=lst_svod_cols,
                                      values=['МА_Значение',
                                              'С_Значение',
                                              'МИ_Значение',
                                              ],
                                      aggfunc=round_mean_two)
    svod_mean_one_df.reset_index(inplace=True)

    # упорядочиваем колонки
    new_order_cols = lst_svod_cols.copy()
    new_order_cols.extend((['МА_Значение',
                            'С_Значение',
                            'МИ_Значение',
                            ]))
    svod_mean_one_df = svod_mean_one_df.reindex(columns=new_order_cols)

    dct_rename_cols_mean = {'МА_Значение': 'Ср. Шкала Максимизация',
                            'С_Значение': 'Ср. Шкала Сатисфакция',
                            'МИ_Значение': 'Ср. Шкала Минимизация',
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
                    f'МА {out_name}': svod_count_one_level_ma_df,
                    f'С {out_name}': svod_count_one_level_s_df,
                    f'МИ {out_name}': svod_count_one_level_mi_df,
                    })

    if len(lst_svod_cols) == 1:
        return out_dct
    else:
        for idx, name_column in enumerate(lst_svod_cols):
            lst_reindex_column_level_cols = [lst_svod_cols[idx], '1-2.9', '3-4.9', '5-5.9','6-7',
                                             'Итого']

            # АД
            svod_count_column_level_ma_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                             'МА_Значение',
                                                             'МА_Диапазон',
                                                             lst_reindex_column_level_cols, lst_level)
            svod_count_column_level_s_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                            'С_Значение',
                                                            'С_Диапазон',
                                                            lst_reindex_column_level_cols, lst_level)
            svod_count_column_level_mi_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                             'МИ_Значение',
                                                             'МИ_Диапазон',
                                                             lst_reindex_column_level_cols, lst_level)

            # Считаем среднее по субшкалам
            svod_mean_column_df = pd.pivot_table(base_df,
                                                 index=[lst_svod_cols[idx]],
                                                 values=['МА_Значение',
                                                         'С_Значение',
                                                         'МИ_Значение',
                                                         ],
                                                 aggfunc=round_mean_two)
            svod_mean_column_df.reset_index(inplace=True)

            # упорядочиваем колонки
            new_order_cols = [lst_svod_cols[idx]].copy()
            new_order_cols.extend((['МА_Значение',
                                    'С_Значение',
                                    'МИ_Значение',
                                    ]))
            svod_mean_column_df = svod_mean_column_df.reindex(columns=new_order_cols)

            dct_rename_cols_mean = {'МА_Значение': 'Ср. Шкала Максимизация',
                                    'С_Значение': 'Ср. Шкала Сатисфакция',
                                    'МИ_Значение': 'Ср. Шкала Минимизация',
                                    }
            svod_mean_column_df.rename(columns=dct_rename_cols_mean, inplace=True)

            # Готовим наименование
            name_column = lst_svod_cols[idx]
            name_column = re.sub(r'[\[\]\'+()<> :"?*|\\/]', '_', name_column)
            name_column = name_column[:15]


            out_dct.update({f'Ср {name_column}': svod_mean_column_df,
                            f'МА {name_column}': svod_count_column_level_ma_df,
                            f'С {name_column}': svod_count_column_level_s_df,
                            f'МИ {name_column}': svod_count_column_level_mi_df,
                            })
        return out_dct










def processing_dmti_raz(base_df: pd.DataFrame, answers_df: pd.DataFrame, lst_svod_cols:list):
    """
    Функция для обработки
    :param base_df: часть датафрейма с описательными колонками
    :param answers_df: часть датафрейма с ответами
    :param lst_svod_cols:  список с колонками по которым нужно делать свод
    """
    try:
        quantity_cols_base_df = base_df.shape[1]  # количество колонок в анкетной части
        out_answer_df = base_df.copy()  # делаем копию для последующего соединения с сырыми ответами
        if len(answers_df.columns) != 20:  # проверяем количество колонок с вопросами
            raise BadCountColumnsDMTIR

        # очищаем названия колонок от возможных сочетаний .1 которые добавляет пандас при одинаковых колонках
        clean_df_lst = []
        for name_column in answers_df.columns:
            clean_name = re.sub(r'.\d+$', '', name_column)
            clean_df_lst.append(clean_name)

        answers_df.columns = clean_df_lst

        lst_check_cols = ['Вне зависимости от того, насколько я доволен своей работой, мне кажется правильным искать лучшие возможности',
                          'Вне зависимости от того, что я делаю, я предъявляю к себе самые высокие требования',
                          'Я никогда не довольствуюсь чем-то второсортным',
                          'Когда я выбираю из альтернатив, я останавливаюсь на первом варианте, который мне подходит',
                          'На работе или в учебе я всегда ставлю самые высокие цели',
                          'На работе или в учебе я склонен выбирать решения, которые гарантируют удовлетворяющие меня результаты',
                          'На работе или в учебе я ставлю цели, для достижения которых требуется минимальное усилие',
                          'Всякий раз, когда я делаю выбор, я пытаюсь представить все альтернативы, даже те, которые отсутствуют в данный момент',
                          'На работе или в учебе я согласен с любым выбором, который приносит минимальный результат',
                          'В любой области я пытаюсь достичь удовлетворяющих меня результатов',

                          'На работе или в учебе даже минимальный результат может меня устроить',
                          'На работе или в учебе я трачу время на то, чтобы выбрать решение, которое меня устраивает',
                          'Я всегда ставлю цели, для достижения которых требуется минимальное усилие',
                          'Когда я принимаю решения, я трачу время на то, чтобы выбрать приемлемую для себя альтернативу',
                          'Когда я должен принять решение, я выбираю вариант «по минимуму»',
                          'Когда передо мной встает новая задача, я трачу много времени на сбор информации о возможных путях ее решения',
                          'Когда на работе мне дают новое задание, я прилагаю не больше усилий, чем требуется',
                          'При выполнении рабочего задания я стремлюсь к максимальному результату, не считая потраченные силы и время',
                          'При выполнении любого задания я удовлетворяюсь результатом, который считаю достаточным на данный момент',
                          'При выполнения рабочего задания меня устроит результат, для достижения которого требуется минимум усилий'
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
            raise BadOrderDMTIR

        # словарь для замены слов на числа
        dct_replace_value = {'абсолютно не согласен': 1,
                             'не согласен': 2,
                             'скорее не согласен': 3,
                             'ни то, ни другое': 4,
                             'скорее согласен': 5,
                             'согласен': 6,
                             'полностью согласен': 7,
                             }
        valid_values = [1, 2, 3,4,5,6,7]
        answers_df.replace(dct_replace_value, inplace=True)  # заменяем слова на цифры для подсчетов
        # Проверяем, есть ли значения, отличающиеся от указанных в списке
        lst_error_answers = []  # список для хранения строк где найдены неправильные ответы

        for i in range(20):
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
            raise BadValueDMTIR

        base_df['МА_Значение'] = answers_df.apply(calc_value_ma, axis=1)
        base_df['МА_Диапазон'] = base_df['МА_Значение'].apply(calc_level)

        base_df['С_Значение'] = answers_df.apply(calc_value_s, axis=1)
        base_df['С_Диапазон'] = base_df['С_Значение'].apply(calc_level)

        base_df['МИ_Значение'] = answers_df.apply(calc_value_mi, axis=1)
        base_df['МИ_Диапазон'] = base_df['МИ_Значение'].apply(calc_level)



        # Создаем датафрейм для создания части в общий датафрейм
        temp_df = base_df.copy()  # делаем копию
        part_df = temp_df.iloc[:, quantity_cols_base_df:]
        part_df = part_df.add_prefix('ТПРР_')

        out_answer_df = pd.concat([out_answer_df, answers_df], axis=1)  # Датафрейм для проверки

        base_df.sort_values(by='МИ_Значение', ascending=False, inplace=True)  # сортируем

        # Делаем свод  по  шкалам
        dct_svod_sub = {'МА_Значение': 'МА_Диапазон',
                        'С_Значение': 'С_Диапазон',
                        'МИ_Значение': 'МИ_Диапазон',
                        }

        dct_rename_svod_sub = {'МА_Значение': 'Максимизация',
                               'С_Значение': 'Сатисфакция',
                               'МИ_Значение': 'Минимизация',
                               }

        lst_sub = ['1-2.9', '3-4.9', '5-5.9','6-7']

        base_svod_sub_df = create_union_svod(base_df, dct_svod_sub, dct_rename_svod_sub, lst_sub)

        avg_ma = round(base_df['МА_Значение'].mean(), 2)
        avg_s = round(base_df['С_Значение'].mean(), 2)
        avg_mi = round(base_df['МИ_Значение'].mean(), 2)

        avg_dct = {'Среднее значение шкалы Максимизация': avg_ma,
                   'Среднее значение шкалы Сатисфакция': avg_s,
                   'Среднее значение шкалы Минимизация': avg_mi,
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
            'МА_Диапазон': 'МА',
            'С_Диапазон': 'С',
            'МИ_Диапазон': 'МИ',
        }

        out_dct = create_list_on_level(base_df, out_dct, lst_sub, dct_prefix)

        """
                        Сохраняем в зависимости от необходимости делать своды по определенным колонкам
                        """
        if len(lst_svod_cols) == 0:
            return out_dct, part_df

        else:
            out_dct = create_result_dmti_raz(base_df, out_dct, lst_svod_cols)
            return out_dct, part_df

    except BadOrderDMTIR:
        messagebox.showerror('Лахеcис',
                             f'При обработке вопросов теста Опросник Тенденции в принятии решений DMTI Разваляева обнаружены неправильные вопросы. Проверьте названия колонок с вопросами:\n'
                             f'{error_order_message[:5000]}\n'
                             f'Используйте при создании Яндекс-формы написание вопросов из руководства пользователя программы Лахесис.')
    except BadValueDMTIR:
        messagebox.showerror('Лахеcис',
                             f'При обработке вопросов теста Опросник Тенденции в принятии решений DMTI Разваляева обнаружены неправильные варианты ответов. Проверьте ответы на указанных строках:\n'
                             f'{error_message[:5000]}\n'
                             f'Используйте при создании Яндекс-формы написание вариантов ответа из руководства пользователя программы Лахесис.')


    except BadCountColumnsDMTIR:
        messagebox.showerror('Лахеcис',
                             f'Проверьте количество колонок с ответами на тест Опросник Тенденции в принятии решений DMTI Разваляева\n'
                             f'Должно быть 20 колонок с ответами')











