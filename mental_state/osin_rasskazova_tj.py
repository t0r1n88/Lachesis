"""
Скрипт для обработки результатов Тест жизнестойкости Осин Рассказова
"""

import pandas as pd
import re
from tkinter import messagebox
from lachesis_support_functions import round_mean_two,calc_count_scale,create_union_svod, create_list_on_level

class BadOrderTJOR(Exception):
    """
    Исключение для обработки случая когда колонки не совпадают
    """
    pass


class BadValueTJOR(Exception):
    """
    Исключение для неправильных значений в вариантах ответов
    """
    pass

class BadCountColumnsTJOR(Exception):
    """
    Исключение для обработки случая если количество колонок не равно 24
    """
    pass

def calc_value_obj(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [1,2,3,4,5,6,7,8,9,10,
              11,12,13,14,15,16,17,18,19,20,
              21,22,23,24]
    lst_neg = [2, 4, 8, 15, 19, 21,
               1, 5, 10, 17, 18, 22,
               6, 9, 13, 14, 16]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_pr:
            if idx not in lst_neg:
                value_forward += value
            else:
                if value == 0:
                    value_forward += 3
                elif value == 1:
                    value_forward += 2
                elif value == 2:
                    value_forward += 1
                elif value == 3:
                    value_forward += 0
    return value_forward


def calc_level_obj(value):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """
    if 0<= value <= 39 :
        return f'низкий уровень'
    elif 40<= value <=61 :
        return f'средний уровень'
    else:
        return f'высокий уровень'


def calc_value_v(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [3, 11, 12, 20,
              2, 4, 8, 15, 19, 21]
    lst_neg = [2, 4, 8, 15, 19, 21]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_pr:
            if idx not in lst_neg:
                value_forward += value
            else:
                if value == 0:
                    value_forward += 3
                elif value == 1:
                    value_forward += 2
                elif value == 2:
                    value_forward += 1
                elif value == 3:
                    value_forward += 0
    return value_forward

def calc_level_v(value):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """
    if 0<= value <=17 :
        return f'низкий уровень'
    elif 18<= value <=26 :
        return f'средний уровень'
    else:
        return f'высокий уровень'


def calc_value_k(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [7, 23,
              1, 5, 10, 17, 18, 22]
    lst_neg = [1, 5, 10, 17, 18, 22]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_pr:
            if idx not in lst_neg:
                value_forward += value
            else:
                if value == 0:
                    value_forward += 3
                elif value == 1:
                    value_forward += 2
                elif value == 2:
                    value_forward += 1
                elif value == 3:
                    value_forward += 0
    return value_forward

def calc_level_k(value):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """
    if 0<= value <=12 :
        return f'низкий уровень'
    elif 13<= value <=20 :
        return f'средний уровень'
    else:
        return f'высокий уровень'


def calc_value_pr(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [24,
              6, 9, 13, 14, 16]
    lst_neg = [6, 9, 13, 14, 16]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_pr:
            if idx not in lst_neg:
                value_forward += value
            else:
                if value == 0:
                    value_forward += 3
                elif value == 1:
                    value_forward += 2
                elif value == 2:
                    value_forward += 1
                elif value == 3:
                    value_forward += 0
    return value_forward

def calc_level_pr(value):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """
    if 0<= value <=8 :
        return f'низкий уровень'
    elif 9<= value <=14 :
        return f'средний уровень'
    else:
        return f'высокий уровень'


def create_list_on_level_tj(base_df:pd.DataFrame, out_dct:dict, lst_level:list, dct_prefix:dict):
    """
    Функция для создания списков по уровням шкал
    :param base_df: датафрейм с результатами
    :param out_dct: словарь с датафреймами
    :param lst_level: список уровней по которым нужно сделать списки
    :param dct_prefix: префиксы для названий листов
    :return: обновлейнный out dct
    """
    for key,value in dct_prefix.items():
        dct_level = dict()
        for level in lst_level:
            temp_df = base_df[base_df[key] == level]
            if temp_df.shape[0] != 0:
                if level == 'низкий уровень':
                    level = 'низкий'
                elif level == 'средний уровень':
                    level = 'средний'
                else:
                    level = 'высокий'
                dct_level[f'{dct_prefix[key]}. {level}'] = temp_df
        out_dct.update(dct_level)

    return out_dct


def create_result_tj_osin_ras(base_df:pd.DataFrame, out_dct:dict, lst_svod_cols:list):
    """
    Функция для подсчета результата если указаны колонки по которым нужно провести свод
    :param df: датафрейм с результатами
    :param out_dct: словарь с уже подсчитанными базовыми данными
    :param lst_svod_cols: список сводных колонок
    :return: словарь
    """
    lst_l = ['высокий уровень','средний уровень','низкий уровень']

    lst_reindex_one_level_l_cols = lst_svod_cols.copy()
    lst_reindex_one_level_l_cols.extend(['высокий уровень','средний уровень','низкий уровень',
                                       'Итого'])  # Основная шкала

    svod_count_one_level_l_df = calc_count_scale(base_df, lst_svod_cols,
                                                 'ОБЖ_Значение',
                                                 'ОБЖ_Уровень',
                                                 lst_reindex_one_level_l_cols, lst_l)

    lst_level = ['высокий уровень', 'средний уровень', 'низкий уровень']

    lst_reindex_one_level_cols = lst_svod_cols.copy()
    lst_reindex_one_level_cols.extend(['высокий уровень', 'средний уровень', 'низкий уровень',
                                       'Итого'])  # Основная шкала

    # АД
    svod_count_one_level_v_df = calc_count_scale(base_df, lst_svod_cols,
                                                 'В_Значение',
                                                 'В_Уровень',
                                                 lst_reindex_one_level_cols, lst_level)
    svod_count_one_level_k_df = calc_count_scale(base_df, lst_svod_cols,
                                                 'К_Значение',
                                                 'К_Уровень',
                                                 lst_reindex_one_level_cols, lst_level)
    svod_count_one_level_pr_df = calc_count_scale(base_df, lst_svod_cols,
                                                 'ПР_Значение',
                                                 'ПР_Уровень',
                                                 lst_reindex_one_level_cols, lst_level)


    # Считаем среднее по субшкалам
    svod_mean_one_df = pd.pivot_table(base_df,
                                      index=lst_svod_cols,
                                      values=['ОБЖ_Значение',
                                              'В_Значение',
                                              'К_Значение',
                                              'ПР_Значение',
                                              ],
                                      aggfunc=round_mean_two)
    svod_mean_one_df.reset_index(inplace=True)

    # упорядочиваем колонки
    new_order_cols = lst_svod_cols.copy()
    new_order_cols.extend((['ОБЖ_Значение',
                            'В_Значение',
                            'К_Значение',
                            'ПР_Значение',
                            ]))
    svod_mean_one_df = svod_mean_one_df.reindex(columns=new_order_cols)

    dct_rename_cols_mean = {'ОБЖ_Значение': 'Ср. Жизнестойкость',
                            'В_Значение': 'Ср. Шкала Вовлеченность',
                            'К_Значение': 'Ср. Шкала Контроль',
                            'ПР_Значение': 'Ср. Шкала Принятие риска',
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
                    f'ОБЖ {out_name}': svod_count_one_level_l_df,
                    f'В {out_name}': svod_count_one_level_v_df,
                    f'К {out_name}': svod_count_one_level_k_df,
                    f'ПР {out_name}': svod_count_one_level_pr_df,
                    })

    if len(lst_svod_cols) == 1:
        return out_dct
    else:
        for idx, name_column in enumerate(lst_svod_cols):
            lst_reindex_column_level_l_cols = [lst_svod_cols[idx], 'высокий уровень', 'средний уровень', 'низкий уровень',
                                               'Итого']

            svod_count_column_level_l_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                            'ОБЖ_Значение',
                                                            'ОБЖ_Уровень',
                                                            lst_reindex_column_level_l_cols, lst_l)

            lst_level = ['высокий уровень', 'средний уровень', 'низкий уровень']

            lst_reindex_column_level_cols = [lst_svod_cols[idx], 'высокий уровень', 'средний уровень', 'низкий уровень',
                                             'Итого']

            # АД
            svod_count_column_level_v_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                            'В_Значение',
                                                            'В_Уровень',
                                                            lst_reindex_column_level_cols, lst_level)
            svod_count_column_level_k_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                            'К_Значение',
                                                            'К_Уровень',
                                                            lst_reindex_column_level_cols, lst_level)
            svod_count_column_level_pr_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                             'ПР_Значение',
                                                             'ПР_Уровень',
                                                             lst_reindex_column_level_cols, lst_level)

            # Считаем среднее по субшкалам
            svod_mean_column_df = pd.pivot_table(base_df,
                                                 index=[lst_svod_cols[idx]],
                                                 values=['ОБЖ_Значение',
                                                         'В_Значение',
                                                         'К_Значение',
                                                         'ПР_Значение',
                                                         ],
                                                 aggfunc=round_mean_two)
            svod_mean_column_df.reset_index(inplace=True)

            # упорядочиваем колонки
            new_order_cols = [lst_svod_cols[idx]].copy()
            new_order_cols.extend((['ОБЖ_Значение',
                                    'В_Значение',
                                    'К_Значение',
                                    'ПР_Значение',
                                    ]))
            svod_mean_column_df = svod_mean_column_df.reindex(columns=new_order_cols)

            dct_rename_cols_mean = {'ОБЖ_Значение': 'Ср. Жизнестойкость',
                                    'В_Значение': 'Ср. Шкала Вовлеченность',
                                    'К_Значение': 'Ср. Шкала Контроль',
                                    'ПР_Значение': 'Ср. Шкала Принятие риска',
                                    }
            svod_mean_column_df.rename(columns=dct_rename_cols_mean, inplace=True)

            # Готовим наименование
            name_column = lst_svod_cols[idx]
            name_column = re.sub(r'[\[\]\'+()<> :"?*|\\/]', '_', name_column)
            name_column = name_column[:15]

            out_dct.update({f'Ср {name_column}': svod_mean_column_df,
                            f'ОБЖ {name_column}': svod_count_column_level_l_df,
                            f'В {name_column}': svod_count_column_level_v_df,
                            f'К {name_column}': svod_count_column_level_k_df,
                            f'ПР {name_column}': svod_count_column_level_pr_df,
                            })
        return out_dct







def processing_tj_osin_ras(base_df: pd.DataFrame, answers_df: pd.DataFrame, lst_svod_cols:list):
    """
    Функция для обработки
    :param base_df: часть датафрейма с описательными колонками
    :param answers_df: часть датафрейма с ответами
    :param lst_svod_cols:  список с колонками по которым нужно делать свод
    """
    try:
        out_answer_df = base_df.copy()  # делаем копию для последующего соединения с сырыми ответами
        if len(answers_df.columns) != 24:  # проверяем количество колонок с вопросами
            raise BadCountColumnsTJOR

        # очищаем названия колонок от возможных сочетаний .1 которые добавляет пандас при одинаковых колонках
        clean_df_lst = []
        for name_column in answers_df.columns:
            clean_name = re.sub(r'.\d+$', '', name_column)
            clean_df_lst.append(clean_name)

        answers_df.columns = clean_df_lst

        lst_check_cols = ['Я часто не уверен в собственных решениях',
                          'Иногда мне кажется, что никому нет до меня дела',
                          'Я постоянно занят, и мне это нравится',
                          'Порой все, что я делаю, кажется мне бесполезным',
                          'Вечером я часто чувствую себя совершенно разбитым',
                          'Иногда меня пугают мысли о будущем',
                          'Я всегда уверен, что смогу воплотить в жизнь то, что задумал',
                          'Мне кажется, я не живу полной жизнью, а только играю роль',
                          'Мне кажется, если бы в прошлом у меня было меньше разочарований и невзгод, мне было бы сейчас легче жить на свете',
                          'Возникающие проблемы часто кажутся мне неразрешимыми',

                          'Когда кто-нибудь жалуется, что жизнь скучна, это значит, что он просто не умеет видеть интересное',
                          'Мне всегда есть чем заняться',
                          'Я часто сожалею о том, что уже сделано',
                          'Я довольно часто откладываю на завтра то, что трудноосуществимо, или то, в чем я не уверен',
                          'Мне кажется, жизнь проходит мимо меня',
                          'Мои мечты редко сбываются',
                          'Порой мне кажется, что все мои усилия тщетны',
                          'Мне не хватает упорства закончить начатое',
                          'Бывает, жизнь кажется мне скучной и бесцветной',
                          'Как правило, я работаю с удовольствием',

                          'Иногда я чувствую себя лишним даже в кругу друзей',
                          'Бывает, на меня наваливается столько проблем, что просто руки опускаются',
                          'Друзья уважают меня за упорство и непреклонность',
                          'Я охотно берусь воплощать новые идеи'
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
            raise BadOrderTJOR

        # словарь для замены слов на числа
        dct_replace_value = {'нет': 0,
                             'скорее нет': 1,
                             'скорее да': 2,
                             'да': 3,
                             }
        valid_values = [0, 1, 2, 3]
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
            raise BadValueTJOR

        base_df['ОБЖ_Значение'] = answers_df.apply(calc_value_obj, axis=1)
        base_df['ОБЖ_Уровень'] = base_df['ОБЖ_Значение'].apply(calc_level_obj)

        base_df['В_Значение'] = answers_df.apply(calc_value_v, axis=1)
        base_df['В_Уровень'] = base_df['В_Значение'].apply(calc_level_v)
        #
        base_df['К_Значение'] = answers_df.apply(calc_value_k, axis=1)
        base_df['К_Уровень'] = base_df['К_Значение'].apply(calc_level_k)
        #
        base_df['ПР_Значение'] = answers_df.apply(calc_value_pr, axis=1)
        base_df['ПР_Уровень'] = base_df['ПР_Значение'].apply(calc_level_pr)

        # Создаем датафрейм для создания части в общий датафрейм
        part_df = pd.DataFrame()

        # Основные шкалы
        part_df['ТЖОР_ОБЖ_Значение'] = base_df['ОБЖ_Значение']
        part_df['ТЖОР_ОБЖ_Уровень'] = base_df['ОБЖ_Уровень']

        part_df['ТЖОР_В_Значение'] = base_df['В_Значение']
        part_df['ТЖОР_В_Уровень'] = base_df['В_Уровень']

        part_df['ТЖОР_К_Значение'] = base_df['К_Значение']
        part_df['ТЖОР_К_Уровень'] = base_df['К_Уровень']

        part_df['ТЖОР_ПР_Значение'] = base_df['ПР_Значение']
        part_df['ТЖОР_ПР_Уровень'] = base_df['ПР_Уровень']

        out_answer_df = pd.concat([out_answer_df, answers_df], axis=1)  # Датафрейм для проверки

        base_df.sort_values(by='ОБЖ_Значение', ascending=True, inplace=True)  # сортируем

        # Делаем свод  по  шкалам
        dct_svod_l = {'ОБЖ_Значение': 'ОБЖ_Уровень',
                      }

        dct_rename_svod_l = {'ОБЖ_Значение': 'Жизнестойкость',
                             }

        lst_l = ['высокий уровень','средний уровень','низкий уровень']

        base_svod_l_df = create_union_svod(base_df, dct_svod_l, dct_rename_svod_l, lst_l)

        # Делаем свод  по  шкалам
        dct_svod_sub = {'В_Значение': 'В_Уровень',
                        'К_Значение': 'К_Уровень',
                        'ПР_Значение': 'ПР_Уровень',
                        }

        dct_rename_svod_sub = {'В_Значение': 'Шкала Вовлеченность',
                               'К_Значение': 'Шкала Контроль',
                               'ПР_Значение': 'Шкала Принятие риска',

                               }

        lst_sub = ['высокий уровень', 'средний уровень', 'низкий уровень']

        base_svod_sub_df = create_union_svod(base_df, dct_svod_sub, dct_rename_svod_sub, lst_sub)

        avg_obj = round(base_df['ОБЖ_Значение'].mean(), 2)
        avg_v = round(base_df['В_Значение'].mean(), 2)
        avg_k = round(base_df['К_Значение'].mean(), 2)
        avg_pr = round(base_df['ПР_Значение'].mean(), 2)

        avg_dct = {'Среднее значение Жизнестойкость': avg_obj,
                   'Среднее значение шкалы Вовлеченность': avg_v,
                   'Среднее значение шкалы Контроль': avg_k,
                   'Среднее значение шкалы Принятие риска': avg_pr,
                   }

        avg_df = pd.DataFrame.from_dict(avg_dct, orient='index')
        avg_df = avg_df.reset_index()
        avg_df.columns = ['Показатель', 'Среднее значение']

        # формируем основной словарь
        out_dct = {'Списочный результат': base_df,
                   'Список для проверки': out_answer_df,
                   'Свод ОБЖ': base_svod_l_df,
                   'Свод Шкалы': base_svod_sub_df,
                   'Среднее': avg_df,
                   }

        dct_l = {
            'ОБЖ_Уровень': 'ОБЖ',
        }

        out_dct = create_list_on_level_tj(base_df, out_dct, lst_l, dct_l)

        dct_prefix = {
            'В_Уровень': 'В',
            'К_Уровень': 'К',
            'ПР_Уровень': 'ПР'
        }

        out_dct = create_list_on_level_tj(base_df, out_dct, lst_sub, dct_prefix)

        """
                        Сохраняем в зависимости от необходимости делать своды по определенным колонкам
                        """
        if len(lst_svod_cols) == 0:
            return out_dct, part_df
        else:
            out_dct = create_result_tj_osin_ras(base_df, out_dct, lst_svod_cols)
            return out_dct, part_df


    except BadOrderTJOR:
        messagebox.showerror('Лахеcис',
                             f'При обработке вопросов теста жизнестойкости Осин Рассказова обнаружены неправильные вопросы. Проверьте названия колонок с вопросами:\n'
                             f'{error_order_message[:5000]}\n'
                             f'Используйте при создании Яндекс-формы написание вопросов из руководства пользователя программы Лахесис.')
    except BadValueTJOR:
        messagebox.showerror('Лахеcис',
                             f'При обработке вопросов теста жизнестойкости Осин Рассказова  обнаружены неправильные варианты ответов. Проверьте ответы на указанных строках:\n'
                             f'{error_message[:5000]}\n'
                             f'Используйте при создании Яндекс-формы написание вариантов ответа из руководства пользователя программы Лахесис.')


    except BadCountColumnsTJOR:
        messagebox.showerror('Лахеcис',
                             f'Проверьте количество колонок с ответами на Тест жизнестойкости Осин Рассказова\n'
                             f'Должно быть 24 колонки с ответами')












