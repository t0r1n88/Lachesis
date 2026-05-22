"""
Скрипт для обработки результатов Шкала взаимной адаптации в браке Спаниер Полякова, Сорокова, Гаранян
"""

import pandas as pd
import re
from tkinter import messagebox
from lachesis_support_functions import round_mean_two,calc_count_scale,create_union_svod,create_list_on_level

class BadOrderVABPSG(Exception):
    """
    Исключение для обработки случая когда колонки не совпадают
    """
    pass


class BadValueVABPSG(Exception):
    """
    Исключение для неправильных значений в вариантах ответов
    """
    pass

class BadCountColumnsVABPSG(Exception):
    """
    Исключение для обработки случая если количество колонок не равно 28
    """
    pass


def calc_level_ip(value):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """
    if 0<=value <= 30:
        return f'0-30'
    elif 31<= value<= 60:
        return '31-60'
    elif 61<= value<= 90:
        return '61-90'
    elif 91<= value<= 120:
        return '91-120'
    else:
        return f'121-140'


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



def calc_value_ip(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [1,2,3,4,5,6,7,8,9,10,
              11,12,13,14,15,16,17,18,19,20,
              21,22,23,24,25,26,27,28]
    lst_neg = [18,19]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_pr:
            if idx not in lst_neg:
                value_forward += value
            else:
                if value == 0:
                    value_forward += 5
                elif value == 1:
                    value_forward += 4
                elif value == 2:
                    value_forward += 3
                elif value == 3:
                    value_forward += 2
                elif value == 4:
                    value_forward += 1
                else:
                    value_forward += 0

    return value_forward


def calc_value_sgp(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [1,2,3,4,5,6,7,8,9,10,
              11,12,13,14,15]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_pr:
            value_forward += value

    return value_forward


def calc_value_ub(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [16,17,18,19,20,
              21,22,28]
    lst_neg = [18,19]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_pr:
            if idx not in lst_neg:
                value_forward += value
            else:
                if value == 0:
                    value_forward += 5
                elif value == 1:
                    value_forward += 4
                elif value == 2:
                    value_forward += 3
                elif value == 3:
                    value_forward += 2
                elif value == 4:
                    value_forward += 1
                else:
                    value_forward += 0

    return value_forward

def calc_value_spp(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [23,24,25,26,27]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_pr:
            value_forward += value

    return value_forward


def create_result_vab_polyakova(base_df:pd.DataFrame, out_dct:dict, lst_svod_cols:list):
    """
    Функция для подсчета результата если указаны колонки по которым нужно провести свод
    :param df: датафрейм с результатами
    :param out_dct: словарь с уже подсчитанными базовыми данными
    :param lst_svod_cols: список сводных колонок
    :return: словарь
    """
    lst_l = ['0-30', '31-60', '61-90', '91-120','121-140']

    lst_reindex_one_level_l_cols = lst_svod_cols.copy()
    lst_reindex_one_level_l_cols.extend(['0-30', '31-60', '61-90', '91-120','121-140',
                                       'Итого'])  # Основная шкала

    # Ложь
    svod_count_one_level_ip_df = calc_count_scale(base_df, lst_svod_cols,
                                                 'ИП_Значение',
                                                 'ИП_Диапазон',
                                                 lst_reindex_one_level_l_cols, lst_l)

    lst_level = ['0-24%','25-49%','50-74%','75-100%']

    lst_reindex_one_level_cols = lst_svod_cols.copy()
    lst_reindex_one_level_cols.extend(['0-24%','25-49%','50-74%','75-100%',
                                       'Итого'])  # Основная шкала

    # АД
    svod_count_one_level_sgp_df = calc_count_scale(base_df, lst_svod_cols,
                                                 'СГП_Значение',
                                                 'СГП_Диапазон',
                                                 lst_reindex_one_level_cols, lst_level)
    # АВА
    svod_count_one_level_ub_df = calc_count_scale(base_df, lst_svod_cols,
                                                 'УБ_Значение',
                                                 'УБ_Диапазон',
                                                 lst_reindex_one_level_cols, lst_level)

    # АВА
    svod_count_one_level_spp_df = calc_count_scale(base_df, lst_svod_cols,
                                                 'СПП_Значение',
                                                 'СПП_Диапазон',
                                                 lst_reindex_one_level_cols, lst_level)

    # Считаем среднее по субшкалам
    svod_mean_one_df = pd.pivot_table(base_df,
                                      index=lst_svod_cols,
                                      values=['ИП_Значение',
                                              'СГП_Значение',
                                              'УБ_Значение',
                                              'СПП_Значение',
                                              ],
                                      aggfunc=round_mean_two)
    svod_mean_one_df.reset_index(inplace=True)

    # упорядочиваем колонки
    new_order_cols = lst_svod_cols.copy()
    new_order_cols.extend((['ИП_Значение',
                            'СГП_Значение',
                            'УБ_Значение',
                            'СПП_Значение',
                            ]))
    svod_mean_one_df = svod_mean_one_df.reindex(columns=new_order_cols)

    dct_rename_cols_mean = {'ИП_Значение': 'Ср. Интегральный показатель',
                            'СГП_Значение': 'Ср. Согласие в паре',
                            'УБ_Значение': 'Ср. Удовлетворенность браком',
                            'СПП_Значение': 'Ср. Сплоченность пары',
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
                    f'ИП {out_name}': svod_count_one_level_ip_df,
                    f'СГП {out_name}': svod_count_one_level_sgp_df,
                    f'УБ {out_name}': svod_count_one_level_ub_df,
                    f'СПП {out_name}': svod_count_one_level_spp_df,
                    })

    if len(lst_svod_cols) == 1:
        return out_dct
    else:
        for idx, name_column in enumerate(lst_svod_cols):
            lst_reindex_column_level_l_cols = [lst_svod_cols[idx], '0-30', '31-60', '61-90', '91-120','121-140',
                                             'Итого']

            lst_reindex_column_level_cols = [lst_svod_cols[idx], '0-24%','25-49%','50-74%','75-100%',
                                             'Итого']

            # Ложь
            svod_count_column_level_ip_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                             'ИП_Значение',
                                                             'ИП_Диапазон',
                                                             lst_reindex_column_level_l_cols, lst_l)

            # АД
            svod_count_column_level_sgp_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                              'СГП_Значение',
                                                              'СГП_Диапазон',
                                                              lst_reindex_column_level_cols, lst_level)
            # АВА
            svod_count_column_level_ub_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                             'УБ_Значение',
                                                             'УБ_Диапазон',
                                                             lst_reindex_column_level_cols, lst_level)

            # АВА
            svod_count_column_level_spp_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                              'СПП_Значение',
                                                              'СПП_Диапазон',
                                                              lst_reindex_column_level_cols, lst_level)

            # Считаем среднее по субшкалам
            svod_mean_column_df = pd.pivot_table(base_df,
                                                 index=[lst_svod_cols[idx]],
                                                 values=['ИП_Значение',
                                                         'СГП_Значение',
                                                         'УБ_Значение',
                                                         'СПП_Значение',
                                                         ],
                                                 aggfunc=round_mean_two)
            svod_mean_column_df.reset_index(inplace=True)

            # упорядочиваем колонки
            new_order_cols = [lst_svod_cols[idx]].copy()
            new_order_cols.extend((['ИП_Значение',
                                    'СГП_Значение',
                                    'УБ_Значение',
                                    'СПП_Значение',
                                    ]))
            svod_mean_column_df = svod_mean_column_df.reindex(columns=new_order_cols)

            dct_rename_cols_mean = {'ИП_Значение': 'Ср. Интегральный показатель',
                                    'СГП_Значение': 'Ср. Согласие в паре',
                                    'УБ_Значение': 'Ср. Удовлетворенность браком',
                                    'СПП_Значение': 'Ср. Сплоченность пары',
                                    }
            svod_mean_column_df.rename(columns=dct_rename_cols_mean, inplace=True)

            # Готовим наименование
            name_column = lst_svod_cols[idx]
            name_column = re.sub(r'[\[\]\'+()<> :"?*|\\/]', '_', name_column)
            name_column = name_column[:15]

            out_dct.update({f'Ср {name_column}': svod_mean_column_df,
                            f'ИП {name_column}': svod_count_column_level_ip_df,
                            f'СГП {name_column}': svod_count_column_level_sgp_df,
                            f'УБ {name_column}': svod_count_column_level_ub_df,
                            f'СПП {name_column}': svod_count_column_level_spp_df,
                            })

        return out_dct







def processing_vab_pol(base_df: pd.DataFrame, answers_df: pd.DataFrame, lst_svod_cols:list):
    """
    Функция для обработки
    :param base_df: часть датафрейма с описательными колонками
    :param answers_df: часть датафрейма с ответами
    :param lst_svod_cols:  список с колонками по которым нужно делать свод
    """
    try:
        count_descr_cols = base_df.shape[1] # количество анкетных колонок

        out_answer_df = base_df.copy()  # делаем копию для последующего соединения с сырыми ответами
        if len(answers_df.columns) != 28:  # проверяем количество колонок с вопросами
            raise BadCountColumnsVABPSG

        # очищаем названия колонок от возможных сочетаний .1 которые добавляет пандас при одинаковых колонках
        clean_df_lst = []
        for name_column in answers_df.columns:
            clean_name = re.sub(r'.\d+$', '', name_column)
            clean_df_lst.append(clean_name)

        answers_df.columns = clean_df_lst

        lst_check_cols = ['Решение финансовых вопросов',
                          'Развлечения',
                          'Религиозные вопросы',
                          'Способы выражения любви',
                          'Друзья',
                          'Сексуальные отношения',
                          'Приемлемые способы поведения',
                          'Философия жизни',
                          'Взаимоотношения с родителями',
                          'Цели, приоритеты, другие важные вещи',

                          'Количество времени, проводимого вместе',
                          'Принятие важных решений',
                          'Ведение хозяйства',
                          'Интересы и занятия на отдыхе',
                          'Вопросы карьеры',
                          'Как часто Вы обсуждаете или затрагиваете тему возможного развода, отделения друг от друга или завершения Ваших отношений?',
                          'Как часто Вы или Ваш партнер уходите из дома после ссоры?',
                          'В целом, как часто Вы склонны считать, что между Вами и Вашим партнером все хорошо?',
                          'Вы доверяете своему партнеру?',
                          'Вы когда-либо сожалели о том, что женились (вышли замуж) или о том, что стали жить вместе?',

                          'Как часто Вы ссоритесь с Вашим партнером?',
                          'Как часто Вы с Вашим партнером «действуете друг другу на нервы»?',
                          'Как много внешних (не связанных с внутренней жизнью семьи) интересов или занятий связывает Вас с Вашим партнером?',
                          'Вы увлеченно обмениваетесь мыслями',
                          'Вы смеетесь вместе',
                          'Вы спокойно что-нибудь обсуждаете',
                          'Вы вместе работаете над каким-либо делом',
                          'Следующая шкала отражает различные степени счастья в Ваших отношениях с партнером. Средняя отметка «счастлив» характеризует степень счастья в большинстве пар. Пожалуйста, с учетом разных сторон Вашего брака, оцените степень Вашего счастья. Выберите вариант, который точнее всего характеризует Ваше партнерство'
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
            raise BadOrderVABPSG


        dct_one_replace = {'никогда':0,
                            'реже одного раза в месяц':1,
                            'один/два раза в месяц':2,
                            'один/два раза в неделю':3,
                            'один раз в день':4,
                            'чаще, чем один раз в день':5,
        }

        answers_df[['Вы увлеченно обмениваетесь мыслями','Вы смеетесь вместе',
                    'Вы спокойно что-нибудь обсуждаете','Вы вместе работаете над каким-либо делом',]] = answers_df[['Вы увлеченно обмениваетесь мыслями','Вы смеетесь вместе',
                    'Вы спокойно что-нибудь обсуждаете','Вы вместе работаете над каким-либо делом',]].replace(dct_one_replace)



        # словарь для замены слов на числа
        dct_replace_value = {'всегда не соглашаемся друг с другом': 0,
                             'почти всегда не соглашаемся': 1,
                             'часто не соглашаемся': 2,
                             'иногда не соглашаемся': 3,
                             'почти всегда соглашаемся': 4,
                             'всегда соглашаемся друг с другом': 5,

                             'все время': 0,
                             'большую часть времени': 1,
                             'скорее часто, чем редко': 2,
                             'редко': 3,
                             'иногда': 4,
                             'никогда': 5,

                             'нет общих интересов': 0,
                             'очень немного общих интересов': 1,
                             'незначительная часть интересов общая': 2,
                             'большинство интересов общие': 3,
                             'все интересы общие': 4,

                             'чрезвычайно несчастлив': 0,
                             'очень несчастлив': 1,
                             'скорее несчастлив': 2,
                             'счастлив': 3,
                             'очень счастлив': 4,
                             'чрезвычайно счастлив': 5,
                             'мой брак - совершенство': 6,
                             }
        valid_values = [0,1,2,3,4,5,6]
        answers_df.replace(dct_replace_value, inplace=True)  # заменяем слова на цифры для подсчетов
        # Проверяем, есть ли значения, отличающиеся от указанных в списке
        lst_error_answers = []  # список для хранения строк где найдены неправильные ответы

        for i in range(28):
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
            raise BadValueVABPSG

        base_df['ИП_Значение'] = answers_df.apply(calc_value_ip, axis=1)
        base_df['ИП_Диапазон'] = base_df['ИП_Значение'].apply(calc_level_ip)

        base_df['СГП_Значение'] = answers_df.apply(calc_value_sgp, axis=1)
        base_df['СГП_Диапазон'] = base_df['СГП_Значение'].apply(lambda x: calc_level_sub(x, 75))

        base_df['УБ_Значение'] = answers_df.apply(calc_value_ub, axis=1)
        base_df['УБ_Диапазон'] = base_df['УБ_Значение'].apply(lambda x: calc_level_sub(x, 41))

        base_df['СПП_Значение'] = answers_df.apply(calc_value_spp, axis=1)
        base_df['СПП_Диапазон'] = base_df['СПП_Значение'].apply(lambda x: calc_level_sub(x, 24))

        # Создаем датафрейм для создания части в общий датафрейм
        temp_df = base_df.copy()  # делаем копию
        part_df = temp_df.iloc[:, count_descr_cols:]
        part_df = part_df.add_prefix('ВАБПСГ_')

        out_answer_df = pd.concat([out_answer_df, answers_df], axis=1)  # Датафрейм для проверки

        base_df.sort_values(by='ИП_Значение', ascending=True, inplace=True)  # сортируем

        # Делаем свод  по  шкалам
        dct_svod_l = {'ИП_Значение': 'ИП_Диапазон',
                      }

        dct_rename_svod_l = {'ИП_Значение': 'Интегральный показатель',
                             }

        lst_l = ['0-30', '31-60', '61-90', '91-120','121-140']

        base_svod_l_df = create_union_svod(base_df, dct_svod_l, dct_rename_svod_l, lst_l)

        # Делаем свод  по  шкалам
        dct_svod_sub = {'СГП_Значение': 'СГП_Диапазон',
                        'УБ_Значение': 'УБ_Диапазон',
                        'СПП_Значение': 'СПП_Диапазон',
                        }

        dct_rename_svod_sub = {'СГП_Значение': 'Согласие в паре',
                               'УБ_Значение': 'Удовлетворенность браком',
                               'СПП_Значение': 'Сплоченность пары',
                               }

        lst_sub = ['0-24%','25-49%','50-74%','75-100%']

        base_svod_sub_df = create_union_svod(base_df, dct_svod_sub, dct_rename_svod_sub, lst_sub)

        avg_ip = round(base_df['ИП_Значение'].mean(), 2)
        avg_sgp = round(base_df['СГП_Значение'].mean(), 2)
        avg_ub = round(base_df['УБ_Значение'].mean(), 2)
        avg_spp = round(base_df['СПП_Значение'].mean(), 2)

        avg_dct = {'Среднее значение Интегрального показателя': avg_ip,
                   'Среднее значение шкалы Согласие в паре': avg_sgp,
                   'Среднее значение шкалы Удовлетворенность браком': avg_ub,
                   'Среднее значение шкалы Сплоченность пары': avg_spp,
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
            'СГП_Диапазон': 'СГП',
            'УБ_Диапазон': 'УБ',
            'СПП_Диапазон': 'СПП',
        }

        out_dct = create_list_on_level(base_df, out_dct, lst_sub, dct_prefix)

        """
                        Сохраняем в зависимости от необходимости делать своды по определенным колонкам
                        """
        if len(lst_svod_cols) == 0:
            return out_dct, part_df

        else:
            out_dct = create_result_vab_polyakova(base_df, out_dct, lst_svod_cols)
            return out_dct, part_df


    except BadOrderVABPSG:
        messagebox.showerror('Лахеcис',
                             f'При обработке вопросов теста Шкала взаимной адаптации в браке Спаниер Полякова, Сорокова, Гаранян обнаружены неправильные вопросы. Проверьте названия колонок с вопросами:\n'
                             f'{error_order_message[:5000]}\n'
                             f'Используйте при создании Яндекс-формы написание вопросов из руководства пользователя программы Лахесис.')
    except BadValueVABPSG:
        messagebox.showerror('Лахеcис',
                             f'При обработке вопросов теста Шкала взаимной адаптации в браке Спаниер Полякова, Сорокова, Гаранян обнаружены неправильные варианты ответов. Проверьте ответы на указанных строках:\n'
                             f'{error_message[:5000]}\n'
                             f'Используйте при создании Яндекс-формы написание вариантов ответа из руководства пользователя программы Лахесис.')


    except BadCountColumnsVABPSG:
        messagebox.showerror('Лахеcис',
                             f'Проверьте количество колонок с ответами на тест Шкала взаимной адаптации в браке Спаниер Полякова, Сорокова, Гаранян\n'
                             f'Должно быть 28 колонок с ответами')











