"""
Скрипт для обработки результатов теста Методика оценки нервно-психической устойчивости «Прогноз-2»  В.Ю. Рыбников


"""
import pandas as pd
import re
from tkinter import messagebox
from lachesis_support_functions import round_mean_two,calc_count_scale,create_list_on_level,create_union_svod


class BadOrderBPAQE(Exception):
    """
    Исключение для обработки случая когда колонки не совпадают
    """
    pass


class BadValueBPAQE(Exception):
    """
    Исключение для неправильных значений в вариантах ответов
    """
    pass

class BadCountColumnsBPAQE(Exception):
    """
    Исключение для обработки случая если количество колонок не равно 24
    """
    pass


def calc_value_fa(row):
    """
    Функция для подсчета значения шкалы Физическая агрессия
    :return: число
    """
    lst_pr = [1,4,7,10,13,16,22,24,19]
    lst_plus = [1,4,7,10,13,16,22,24]

    value_forward = 0 # счетчик прямых ответов

    for idx, value in enumerate(row):
        if idx +1 in lst_pr:
            if idx + 1 in lst_plus:
                value_forward += value
            else:
                if value == 1:
                    value_forward += 5
                elif value == 2:
                    value_forward += 4
                elif value == 3:
                    value_forward += 3
                elif value == 4:
                    value_forward += 2
                else:
                    value_forward += 1



    return value_forward


def calc_level_fa(value):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """
    if 9 <= value <= 19:
        return 'низкий уровень признака'
    elif 20 <= value <= 30:
        return 'средний уровень признака'
    else:
        return 'ярко выраженный признак'


def calc_value_wraith(row):
    """
    Функция для подсчета значения шкалы Гнев
    :return: число
    """
    lst_pr = [2,5,8,14,17,20,11]
    lst_plus = [2,5,8,14,17,20]

    value_forward = 0 # счетчик прямых ответов

    for idx, value in enumerate(row):
        if idx +1 in lst_pr:
            if idx + 1 in lst_plus:
                value_forward += value
            else:
                if value == 1:
                    value_forward += 5
                elif value == 2:
                    value_forward += 4
                elif value == 3:
                    value_forward += 3
                elif value == 4:
                    value_forward += 2
                else:
                    value_forward += 1



    return value_forward


def calc_level_wraith(value):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """
    if 7 <= value <= 14:
        return 'низкий уровень признака'
    elif 15 <= value <= 22:
        return 'средний уровень признака'
    else:
        return 'ярко выраженный признак'


def calc_value_hos(row):
    """
    Функция для подсчета значения шкалы Враждебность
    :return: число
    """
    lst_pr = [3,6,9,12,15,18,21,23]

    value_forward = 0 # счетчик прямых ответов

    for idx, value in enumerate(row):
        if idx +1 in lst_pr:
            value_forward += value

    return value_forward


def calc_level_hos(value):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """
    if 8 <= value <= 17:
        return 'низкий уровень признака'
    elif 18 <= value <= 27:
        return 'средний уровень признака'
    else:
        return 'ярко выраженный признак'



def create_list_on_level_bpaq(base_df:pd.DataFrame, out_dct:dict, lst_level:list, dct_prefix:dict):
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
                if level == 'низкий уровень признака':
                    level = 'низкий'
                elif level == 'средний уровень признака':
                    level = 'средний'
                else:
                    level = 'ярко выраженный'
                dct_level[f'{dct_prefix[key]}. {level}'] = temp_df
        out_dct.update(dct_level)

    return out_dct

def create_result_bass_perry_enikopolov(base_df:pd.DataFrame, out_dct:dict, lst_svod_cols:list):
    """
    Функция для подсчета результата если указаны колонки по которым нужно провести свод
    :param df: датафрейм с результатами
    :param out_dct: словарь с уже подсчитанными базовыми данными
    :param lst_svod_cols: список сводных колонок
    :return: словарь
    """
    lst_level = ['низкий уровень признака','средний уровень признака','ярко выраженный признак']

    lst_reindex_one_level_cols = lst_svod_cols.copy()
    lst_reindex_one_level_cols.extend(['низкий уровень признака','средний уровень признака','ярко выраженный признак',
                                       'Итого'])  # Основная шкала

    # Физическая агресивность
    svod_count_one_level_fa_df = calc_count_scale(base_df, lst_svod_cols,
                                               'ФА_Значение',
                                               'ФА_Уровень',
                                               lst_reindex_one_level_cols, lst_level)

    # Гнев
    svod_count_one_level_wraith_df = calc_count_scale(base_df, lst_svod_cols,
                                               'Гнев_Значение',
                                               'Гнев_Уровень',
                                               lst_reindex_one_level_cols, lst_level)

    # Враждебность
    svod_count_one_level_hos_df = calc_count_scale(base_df, lst_svod_cols,
                                               'Враждебность_Значение',
                                               'Враждебность_Уровень',
                                               lst_reindex_one_level_cols, lst_level)

    # Считаем среднее по субшкалам
    svod_mean_one_df = pd.pivot_table(base_df,
                                      index=lst_svod_cols,
                                      values=['ФА_Значение',
                                              'Гнев_Значение',
                                              'Враждебность_Значение',
                                              ],
                                      aggfunc=round_mean_two)
    svod_mean_one_df.reset_index(inplace=True)
    # упорядочиваем колонки
    new_order_cols = lst_svod_cols.copy()
    new_order_cols.extend((['ФА_Значение', 'Гнев_Значение',
                            'Враждебность_Значение',
                            ]))
    svod_mean_one_df = svod_mean_one_df.reindex(columns=new_order_cols)

    dct_rename_cols_mean = {'ФА_Значение': 'Ср. Физическая агрессивность',
                            'Гнев_Значение': 'Ср. Гнев',
                            'Враждебность_Значение': 'Ср. Враждебность',
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
                    f'ФА {out_name}': svod_count_one_level_fa_df,
                    f'Гнев {out_name}': svod_count_one_level_wraith_df,
                    f'Вр {out_name}': svod_count_one_level_hos_df,
              })

    if len(lst_svod_cols) == 1:
        return out_dct
    else:
        for idx, name_column in enumerate(lst_svod_cols):
            lst_reindex_column_level_cols = [lst_svod_cols[idx],'низкий уровень признака','средний уровень признака','ярко выраженный признак',
                                                  'Итого']

            # Физическая агресивность
            svod_count_column_level_fa_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                             'ФА_Значение',
                                                             'ФА_Уровень',
                                                             lst_reindex_column_level_cols, lst_level)

            # Гнев
            svod_count_column_level_wraith_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                                 'Гнев_Значение',
                                                                 'Гнев_Уровень',
                                                                 lst_reindex_column_level_cols, lst_level)

            # Враждебность
            svod_count_column_level_hos_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                              'Враждебность_Значение',
                                                              'Враждебность_Уровень',
                                                              lst_reindex_column_level_cols, lst_level)

            # Считаем среднее по субшкалам
            svod_mean_column_df = pd.pivot_table(base_df,
                                                 index=[lst_svod_cols[idx]],
                                                 values=['ФА_Значение',
                                                         'Гнев_Значение',
                                                         'Враждебность_Значение',
                                                         ],
                                                 aggfunc=round_mean_two)
            svod_mean_column_df.reset_index(inplace=True)
            # упорядочиваем колонки
            new_order_cols = [lst_svod_cols[idx]].copy()
            new_order_cols.extend((['ФА_Значение', 'Гнев_Значение',
                                    'Враждебность_Значение',
                                    ]))
            svod_mean_column_df = svod_mean_column_df.reindex(columns=new_order_cols)

            dct_rename_cols_mean = {'ФА_Значение': 'Ср. Физическая агрессивность',
                                    'Гнев_Значение': 'Ср. Гнев',
                                    'Враждебность_Значение': 'Ср. Враждебность',
                                    }
            svod_mean_column_df.rename(columns=dct_rename_cols_mean, inplace=True)

            # Готовим наименование
            name_column = lst_svod_cols[idx]
            name_column = re.sub(r'[\[\]\'+()<> :"?*|\\/]', '_', name_column)
            name_column = name_column[:15]

            out_dct.update({f'Ср {name_column}': svod_mean_column_df,
                            f'ФА {name_column}': svod_count_column_level_fa_df,
                            f'Гнев {name_column}': svod_count_column_level_wraith_df,
                            f'Вр {name_column}': svod_count_column_level_hos_df,
                            })
        return out_dct






def processing_bass_perry_enikopolov_agress(result_df: pd.DataFrame, answers_df: pd.DataFrame, lst_svod_cols:list):
    """
    Функция для обработки
    :param result_df: часть датафрейма с описательными колонками
    :param answers_df: часть датафрейма с ответами
    :param lst_svod_cols:  список с колонками по которым нужно делать свод
    """
    try:
        out_answer_df = result_df.copy()  # делаем копию для последующего соединения с сырыми ответами
        if len(answers_df.columns) != 24:  # проверяем количество колонок с вопросами
            raise BadCountColumnsBPAQE

        # очищаем названия колонок от возможных сочетаний .1 которые добавляет пандас при одинаковых колонках
        clean_df_lst = []
        for name_column in answers_df.columns:
            clean_name = re.sub(r'.\d+$', '', name_column)
            clean_df_lst.append(clean_name)

        answers_df.columns = clean_df_lst

        lst_check_cols = ['Иногда я не могу сдержать желание ударить другого человека',
                          'Я быстро вспыхиваю, но и быстро остываю',
                          'Бывает, что я просто схожу с ума от ревности',
                          'Если меня спровоцировать, я могу ударить другого человека',
                          'Я раздражаюсь, когда у меня что-то не получается',
                          'Временами мне кажется, что жизнь мне что-то не додала',
                          'Если кто-то ударит меня, я дам сдачи',
                          'Иногда я чувствую, что вот-вот взорвусь',
                          'Другим постоянно везет',
                          'Я дерусь чаще, чем окружающие',
                          'У меня спокойный характер',
                          'Я не понимаю, почему иной раз мне бывает так горько',
                          'Если для защиты моих прав мне надо применить физическую силу, я так и сделаю',
                          'Некоторые мои друзья считают, что я вспыльчив',
                          'Я знаю, что мои так называемые друзья сплетничают обо мне',
                          'Некоторые люди своим обращением ко мне могут довести меня до драки',
                          'Иногда я выхожу из себя без особой причины',
                          'Я не доверяю слишком доброжелательным людям',
                          'Я не могу представить себе причину, достаточную, чтобы ударить другого человека',
                          'Мне трудно сдерживать раздражение',
                          'Иногда мне кажется, что люди насмехаются надо мной за глаза',
                          'Бывало, что я угрожал своим знакомым',
                          'Если человек слишком мил со мной, значит он от меня что-то хочет',
                          'Иногда я настолько выходил из себя, что ломал вещи',
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
            raise BadOrderBPAQE

        # словарь для замены слов на числа
        dct_replace_value = {'очень на меня не похоже': 1,
                             'скорее не похоже на меня, чем похоже': 2,
                             'нечто среднее': 3,
                             'скорее похоже на меня, чем нет': 4,
                             'очень на меня похоже': 5
                             }

        valid_values = [1,2,3,4,5]
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
            raise BadValueBPAQE

        base_df = pd.DataFrame()

        base_df['ФА_Значение'] = answers_df.apply(calc_value_fa, axis=1)
        base_df['ФА_Уровень'] = base_df['ФА_Значение'].apply(calc_level_fa)

        base_df['Гнев_Значение'] = answers_df.apply(calc_value_wraith, axis=1)
        base_df['Гнев_Уровень'] = base_df['Гнев_Значение'].apply(calc_level_wraith)

        base_df['Враждебность_Значение'] = answers_df.apply(calc_value_hos, axis=1)
        base_df['Враждебность_Уровень'] = base_df['Враждебность_Значение'].apply(calc_level_hos)

        # Создаем датафрейм для создания части в общий датафрейм
        part_df = pd.DataFrame()
        part_df['УАВБП_Е_ФА_Значение'] = base_df['ФА_Значение']
        part_df['УАВБП_Е_ФА_Уровень'] = base_df['ФА_Уровень']

        part_df['УАВБП_Е_Гнев_Значение'] = base_df['Гнев_Значение']
        part_df['УАВБП_Е_Гнев_Уровень'] = base_df['Гнев_Уровень']

        part_df['УАВБП_Е_Вр_Значение'] = base_df['Враждебность_Значение']
        part_df['УАВБП_Е_Вр_Уровень'] = base_df['Враждебность_Уровень']


        out_answer_df = pd.concat([out_answer_df, answers_df], axis=1)  # Датафрейм для проверки
        # Соединяем анкетную часть с результатной
        base_df = pd.concat([result_df, base_df], axis=1)
        base_df.sort_values(by='ФА_Значение', ascending=False, inplace=True)  # сортируем

        # Делаем свод  по  шкалам
        dct_svod_sub = {'ФА_Значение': 'ФА_Уровень',
                        'Гнев_Значение': 'Гнев_Уровень',
                        'Враждебность_Значение': 'Враждебность_Уровень',
                        }

        dct_rename_svod_sub = {'ФА_Значение': 'Физическая агрессия',
                               'Гнев_Значение': 'Гнев',
                               'Враждебность_Значение': 'Враждебность',
                               }

        lst_sub = ['низкий уровень признака','средний уровень признака','ярко выраженный признак']

        base_svod_sub_df = create_union_svod(base_df, dct_svod_sub, dct_rename_svod_sub, lst_sub)

        # считаем среднее значение по шкалам
        avg_fa = round(base_df['ФА_Значение'].mean(), 2)
        avg_wraith = round(base_df['Гнев_Значение'].mean(), 2)
        avg_hos = round(base_df['Враждебность_Значение'].mean(), 2)

        avg_dct = {'Среднее значение шкалы Физическая агрессия': avg_fa,
                   'Среднее значение шкалы Гнев': avg_wraith,
                   'Среднее значение шкалы Враждебность': avg_hos,
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

        dct_prefix = {'ФА_Уровень': 'ФА',
                      'Гнев_Уровень': 'Гнев',
                      'Враждебность_Уровень': 'Вр',
                      }

        out_dct = create_list_on_level_bpaq(base_df, out_dct, lst_sub, dct_prefix)

        """
                        Сохраняем в зависимости от необходимости делать своды по определенным колонкам
                        """
        if len(lst_svod_cols) == 0:
            return out_dct, part_df

        else:
            out_dct = create_result_bass_perry_enikopolov(base_df, out_dct, lst_svod_cols)
            return out_dct, part_df


    except BadOrderBPAQE:
        messagebox.showerror('Лахеcис',
                             f'При обработке вопросов теста Опросник диагностики агрессии Басса-Перри Еникополов обнаружены неправильные вопросы. Проверьте названия колонок с вопросами:\n'
                             f'{error_order_message[:5000]}\n'
                             f'Используйте при создании Яндекс-формы написание вопросов из руководства пользователя программы Лахесис.')
    except BadValueBPAQE:
        messagebox.showerror('Лахеcис',
                             f'При обработке вопросов теста Опросник диагностики агрессии Басса-Перри Еникополов обнаружены неправильные варианты ответов. Проверьте ответы на указанных строках:\n'
                             f'{error_message[:5000]}\n'
                             f'Используйте при создании Яндекс-формы написание вариантов ответа из руководства пользователя программы Лахесис.')


    except BadCountColumnsBPAQE:
        messagebox.showerror('Лахеcис',
                             f'Проверьте количество колонок с ответами на тест Опросник диагностики агрессии Басса-Перри Еникополов\n'
                             f'Должно быть 24 колонки с ответами')











