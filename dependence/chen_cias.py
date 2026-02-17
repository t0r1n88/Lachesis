"""
Скрипт для обработки результатов теста Шкала интернет-зависимости Чена, CIAS Малыгин
"""

import pandas as pd
import re
from tkinter import messagebox
from lachesis_support_functions import round_mean_two,calc_count_scale,create_list_on_level,create_union_svod



class BadOrderCIASCM(Exception):
    """
    Исключение для обработки случая когда колонки не совпадают
    """
    pass


class BadValueCIASCM(Exception):
    """
    Исключение для неправильных значений в вариантах ответов
    """
    pass

class BadCountColumnsCIASCM(Exception):
    """
    Исключение для обработки случая если количество колонок не равно 26
    """
    pass



def calc_level(value):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """
    if 26<= value <= 42:
        return f'отсутствие ИЗП'
    elif 43 <= value <= 64:
        return f'склонность к ИЗП'
    else:
        return f'наличие ИЗП'

def calc_value_cs(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [11,14,19,20,22]
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
    lst_pr = [2,4,5,10,16]
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
    lst_pr = [3,6,9,24]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_pr:
            value_forward += value


    return value_forward

def calc_value_vpsz(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [7,12,13,15,17,18,21]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_pr:
            value_forward += value


    return value_forward


def calc_value_uv(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [1,8,23,25,26]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_pr:
            value_forward += value


    return value_forward


def create_list_on_level_cias(base_df:pd.DataFrame, out_dct:dict, lst_level:list, dct_prefix:dict):
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
                dct_level[f'{dct_prefix[key]}. {level}'] = temp_df
        out_dct.update(dct_level)

    return out_dct


def create_result_cias_chen(base_df:pd.DataFrame, out_dct:dict, lst_svod_cols:list):
    """
    Функция для подсчета результата если указаны колонки по которым нужно провести свод
    :param df: датафрейм с результатами
    :param out_dct: словарь с уже подсчитанными базовыми данными
    :param lst_svod_cols: список сводных колонок
    :return: словарь
    """
    lst_level = ['отсутствие ИЗП', 'склонность к ИЗП', 'наличие ИЗП']

    lst_reindex_one_level_cols = lst_svod_cols.copy()
    lst_reindex_one_level_cols.extend(['отсутствие ИЗП', 'склонность к ИЗП', 'наличие ИЗП',
                                       'Итого'])  # Основная шкала

    # ВЧА
    svod_count_one_level_vcha_df = calc_count_scale(base_df, lst_svod_cols,
                                                   'ИЗ_Значение',
                                                   'ИЗ_Уровень',
                                                   lst_reindex_one_level_cols, lst_level)

    # Считаем среднее по субшкалам
    svod_mean_one_df = pd.pivot_table(base_df,
                                      index=lst_svod_cols,
                                      values=['КС_Значение',
                                              'СО_Значение',
                                              'Т_Значение',
                                              'ВПСЗ_Значение',

                                              'УВ_Значение',
                                              'КСИЗ_Значение',
                                              'ПИЗ_Значение',
                                              'ИЗ_Значение',
                                              ],
                                      aggfunc=round_mean_two)
    svod_mean_one_df.reset_index(inplace=True)

    # упорядочиваем колонки
    new_order_cols = lst_svod_cols.copy()
    new_order_cols.extend((['КС_Значение', 'СО_Значение',
                            'Т_Значение','ВПСЗ_Значение',
                            'УВ_Значение','КСИЗ_Значение',
                            'ПИЗ_Значение','ИЗ_Значение',
                            ]))
    svod_mean_one_df = svod_mean_one_df.reindex(columns=new_order_cols)

    dct_rename_cols_mean = {'КС_Значение': 'Ср. Компульсивные симптомы',
                            'СО_Значение': 'Ср. Симптомы отмены',
                            'Т_Значение': 'Ср. Толерантности',
                            'ВПСЗ_Значение': 'Ср. Внутриличностных проблем и проблем, связанных со здоровьем',

                            'УВ_Значение': 'Ср. Управление временем',
                            'КСИЗ_Значение': 'Ср. Ключевые симптомы интернет-зависимости',
                            'ПИЗ_Значение': 'Ср. Проблемы, связанные с интернет-зависимостью',
                            'ИЗ_Значение': 'Ср. Интернет зависимость',
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
                    f'ИЗ {out_name}': svod_count_one_level_vcha_df,
                    })

    if len(lst_svod_cols) == 1:
        return out_dct
    else:
        for idx, name_column in enumerate(lst_svod_cols):
            lst_reindex_column_level_cols = [lst_svod_cols[idx],'отсутствие ИЗП', 'склонность к ИЗП', 'наличие ИЗП',
                                                  'Итого']
            # ВЧА
            svod_count_column_level_vcha_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                            'ИЗ_Значение',
                                                            'ИЗ_Уровень',
                                                            lst_reindex_column_level_cols, lst_level)

            # Считаем среднее по субшкалам
            svod_mean_column_df = pd.pivot_table(base_df,
                                              index=[lst_svod_cols[idx]],
                                              values=['КС_Значение',
                                                      'СО_Значение',
                                                      'Т_Значение',
                                                      'ВПСЗ_Значение',

                                                      'УВ_Значение',
                                                      'КСИЗ_Значение',
                                                      'ПИЗ_Значение',
                                                      'ИЗ_Значение',
                                                      ],
                                              aggfunc=round_mean_two)
            svod_mean_column_df.reset_index(inplace=True)

            # упорядочиваем колонки
            new_order_cols = [lst_svod_cols[idx]].copy()
            new_order_cols.extend((['КС_Значение', 'СО_Значение',
                                    'Т_Значение', 'ВПСЗ_Значение',
                                    'УВ_Значение', 'КСИЗ_Значение',
                                    'ПИЗ_Значение', 'ИЗ_Значение',
                                    ]))
            svod_mean_column_df = svod_mean_column_df.reindex(columns=new_order_cols)

            dct_rename_cols_mean = {'КС_Значение': 'Ср. Компульсивные симптомы',
                                    'СО_Значение': 'Ср. Симптомы отмены',
                                    'Т_Значение': 'Ср. Толерантности',
                                    'ВПСЗ_Значение': 'Ср. Внутриличностных проблем и проблем, связанных со здоровьем',

                                    'УВ_Значение': 'Ср. Управление временем',
                                    'КСИЗ_Значение': 'Ср. Ключевые симптомы интернет-зависимости',
                                    'ПИЗ_Значение': 'Ср. Проблемы, связанные с интернет-зависимостью',
                                    'ИЗ_Значение': 'Ср. Интернет зависимость',
                                    }
            svod_mean_column_df.rename(columns=dct_rename_cols_mean, inplace=True)
            # Готовим наименование
            name_column = lst_svod_cols[idx]
            name_column = re.sub(r'[\[\]\'+()<> :"?*|\\/]', '_', name_column)
            name_column = name_column[:15]
            out_dct.update({f'Ср {name_column}': svod_mean_column_df,
                            f'ИЗ {name_column}': svod_count_column_level_vcha_df,
                            })
        return out_dct










def processing_cias_chen_mal(base_df: pd.DataFrame, answers_df: pd.DataFrame, lst_svod_cols:list):
    """
    Функция для обработки
    :param base_df: часть датафрейма с описательными колонками
    :param answers_df: часть датафрейма с ответами
    :param lst_svod_cols:  список с колонками по которым нужно делать свод
    """
    try:
        out_answer_df = base_df.copy()  # делаем копию для последующего соединения с сырыми ответами
        if len(answers_df.columns) != 26:  # проверяем количество колонок с вопросами
            raise BadCountColumnsCIASCM

        # очищаем названия колонок от возможных сочетаний .1 которые добавляет пандас при одинаковых колонках
        clean_df_lst = []
        for name_column in answers_df.columns:
            clean_name = re.sub(r'.\d+$', '', name_column)
            clean_df_lst.append(clean_name)

        answers_df.columns = clean_df_lst

        lst_check_cols = ['Мне не раз говорили, что я провожу слишком много времени в Интернете',
                          'Я чувствую себя некомфортно, когда я не бываю в Интернете в течение определенного периода времени',
                          'Я замечаю, что все больше и больше времени провожу в сети',
                          'Я чувствую беспокойство и раздражение, когда Интернет отключен или недоступен',
                          'Я чувствую себя полным сил, пребывая онлайн, несмотря на чувствовавшуюся ранее усталость',
                          'Я остаюсь в сети в течение более длительного периода времени, чем намеревался, хотя я и планировал только «зайти на минутку»',
                          'Хотя использование Интернета негативно влияет на мои отношения с другими людьми, количество времени, потраченного на Интернет, остается неизменным',
                          'Несколько раз (>1) я спал менее четырех часов из-за того, что «завис» в Интернете',
                          'За последний семестр (или за последние 6 месяцев) я стал гораздо больше времени проводить в сети',
                          'Я переживаю или расстраиваюсь, если приходится прекратить пользоваться Интернетом на определенный период времени',

                          'Мне не удается преодолеть желание войти в сеть',
                          'Я отмечаю, что я выхожу в Интернет вместо личной встречи с друзьями',
                          'У меня болит спина или я испытываю другого рода физический дискомфорт после сидения в Интернете',
                          'Мысль зайти в сеть приходит мне первой, когда я просыпаюсь утром',
                          'Пребывание в Интернете привело к возникновению у меня определенных неприятностей в школе или на работе',
                          'Пребывая вне сети в течение определенного периода времени, я ощущаю, что упускаю что-то',
                          'Мое общение с членами семьи сокращается из-за использования Интернета',
                          'Я меньше отдыхаю из-за использования Интернета',
                          'Даже когда я отключаюсь от Интернета после выполненной работы, у меня не получается справиться с желанием войти в сеть снова',
                          'Моя жизнь была бы безрадостной, если бы не было Интернета',
                          'Пребывание в Интернете негативно повлияло на мое физическое самочувствие',
                          'Я стараюсь тратить меньше времени в Интернете, но безуспешно',
                          'Для меня становится обычным спать меньше, чтобы провести больше времени в Интернете',
                          'Мне необходимо проводить все больше времени в Интернете, чтобы получать то же удовлетворение, что и раньше',
                          'Иногда у меня не получается поесть в нужное время из-за того, что я сижу в Интернете',
                          'Я чувствую себя усталым днем из-за того, что ночью сидел в Интернете',
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
            raise BadOrderCIASCM

        # словарь для замены слов на числа
        dct_replace_value = {'полностью подходит': 4,
                             'частично подходит': 3,
                             'слабо подходит': 2,
                             'совсем не подходит': 1,
                             }
        valid_values = [1, 2, 3, 4]
        answers_df.replace(dct_replace_value, inplace=True)  # заменяем слова на цифры для подсчетов
        # Проверяем, есть ли значения, отличающиеся от указанных в списке
        lst_error_answers = []  # список для хранения строк где найдены неправильные ответы

        for i in range(26):
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
            raise BadValueCIASCM

        # Субшкалы
        base_df['КС_Значение'] = answers_df.apply(calc_value_cs, axis=1)
        base_df['СО_Значение'] = answers_df.apply(calc_value_so, axis=1)
        base_df['Т_Значение'] = answers_df.apply(calc_value_t, axis=1)
        base_df['ВПСЗ_Значение'] = answers_df.apply(calc_value_vpsz, axis=1)
        base_df['УВ_Значение'] = answers_df.apply(calc_value_uv, axis=1)

        # Интегральные шкалы
        base_df['КСИЗ_Значение'] = base_df['КС_Значение'] + base_df['СО_Значение'] + base_df['Т_Значение']
        base_df['ПИЗ_Значение'] = base_df['ВПСЗ_Значение'] +  base_df['УВ_Значение']
        base_df['ИЗ_Значение'] = answers_df.sum(axis=1)
        base_df['ИЗ_Уровень'] = base_df['ИЗ_Значение'].apply(calc_level)

        # Создаем датафрейм для создания части в общий датафрейм
        part_df = pd.DataFrame()

        # Основные шкалы
        part_df['ШИЗЧМ_ИЗ_Значение'] = base_df['ИЗ_Значение']
        part_df['ШИЗЧМ_ИЗ_Уровень'] = base_df['ИЗ_Уровень']
        part_df['ШИЗЧМ_ПИЗ_Значение'] = base_df['ПИЗ_Значение']
        part_df['ШИЗЧМ_КСИЗ_Значение'] = base_df['КСИЗ_Значение']

        # Субшкалы
        part_df['ШИЗЧМ_КС_Значение'] = base_df['КС_Значение']
        part_df['ШИЗЧМ_СО_Значение'] = base_df['СО_Значение']
        part_df['ШИЗЧМ_Т_Значение'] = base_df['Т_Значение']
        part_df['ШИЗЧМ_ВПСЗ_Значение'] = base_df['ВПСЗ_Значение']
        part_df['ШИЗЧМ_УВ_Значение'] = base_df['УВ_Значение']

        out_answer_df = pd.concat([out_answer_df, answers_df], axis=1)  # Датафрейм для проверки

        base_df.sort_values(by='ИЗ_Значение', ascending=False, inplace=True)  # сортируем

        # Делаем свод  по  шкалам
        dct_svod_sub = {'ИЗ_Значение': 'ИЗ_Уровень',
                        }

        dct_rename_svod_sub = {'ИЗ_Значение': 'Интернет зависимость',
                               }

        lst_sub = ['отсутствие ИЗП', 'склонность к ИЗП', 'наличие ИЗП']

        base_svod_sub_df = create_union_svod(base_df, dct_svod_sub, dct_rename_svod_sub, lst_sub)

        avg_vcha = round(base_df['КС_Значение'].mean(), 2)
        avg_o = round(base_df['СО_Значение'].mean(), 2)
        avg_ruvs = round(base_df['Т_Значение'].mean(), 2)

        avg_psp = round(base_df['ВПСЗ_Значение'].mean(), 2)
        avg_ppvs = round(base_df['УВ_Значение'].mean(), 2)
        avg_ip = round(base_df['КСИЗ_Значение'].mean(), 2)

        avg_ppbd = round(base_df['ПИЗ_Значение'].mean(), 2)

        avg_prp = round(base_df['ИЗ_Значение'].mean(), 2)

        avg_dct = {'Среднее значение шкалы Компульсивные симптомы': avg_vcha,
                   'Среднее значение шкалы Симптомы отмены': avg_o,
                   'Среднее значение шкалы Толерантности': avg_ruvs,

                   'Среднее значение шкалы Внутриличностных проблем и проблем, связанных со здоровьем': avg_psp,
                   'Среднее значение шкалы Управления временем': avg_ppvs,
                   'Среднее значение шкалы Ключевые симптомы интернет-зависимости': avg_ip,

                   'Среднее значение шкалы Проблемы, связанные с интернет-зависимостью': avg_ppbd,

                   'Среднее значение интернет зависимости': avg_prp,
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

        dct_prefix = {'ИЗ_Уровень': 'ИЗ',
                      }

        out_dct = create_list_on_level_cias(base_df, out_dct, lst_sub, dct_prefix)

        """
                        Сохраняем в зависимости от необходимости делать своды по определенным колонкам
                        """
        if len(lst_svod_cols) == 0:
            return out_dct, part_df

        else:
            out_dct = create_result_cias_chen(base_df, out_dct, lst_svod_cols)
            return out_dct, part_df


    except BadOrderCIASCM:
        messagebox.showerror('Лахеcис',
                             f'При обработке вопросов теста Шкала интернет-зависимости Чена, CIAS Малыгин обнаружены неправильные вопросы. Проверьте названия колонок с вопросами:\n'
                             f'{error_order_message[:5000]}\n'
                             f'Используйте при создании Яндекс-формы написание вопросов из руководства пользователя программы Лахесис.')
    except BadValueCIASCM:
        messagebox.showerror('Лахеcис',
                             f'При обработке вопросов теста Шкала интернет-зависимости Чена, CIAS Малыгин обнаружены неправильные варианты ответов. Проверьте ответы на указанных строках:\n'
                             f'{error_message[:5000]}\n'
                             f'Используйте при создании Яндекс-формы написание вариантов ответа из руководства пользователя программы Лахесис.')


    except BadCountColumnsCIASCM:
        messagebox.showerror('Лахеcис',
                             f'Проверьте количество колонок с ответами на тест Шкала интернет-зависимости Чена, CIAS Малыгин\n'
                             f'Должно быть 26 колонок с ответами')
















