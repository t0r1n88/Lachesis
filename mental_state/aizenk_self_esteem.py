"""
Скрипт для обработки результатов теста Методика «Самооценки психических состояний» Г. Айзенка
"""

import pandas as pd
import re
from tkinter import messagebox
from lachesis_support_functions import round_mean,create_union_svod,create_list_on_level


class BadOrderSPSA(Exception):
    """
    Исключение для обработки случая когда колонки не совпадают
    """
    pass


class BadValueSPSA(Exception):
    """
    Исключение для неправильных значений в вариантах ответов
    """
    pass

class BadCountColumnsSPSA(Exception):
    """
    Исключение для обработки случая если количество колонок не равно 40
    """
    pass


def calc_sub_value_anxiety(row):
    """
    Функция для подсчета значения шкалы Тревожность
    :param row: строка с ответами
    :return: число
    """
    lst_pr = [1,2,3,4,5,6,7,8,9,10]

    value_forward = 0 # счетчик прямых ответов

    for idx, value in enumerate(row):
        if idx +1 in lst_pr:
            value_forward += value

    return value_forward

def calc_level(value):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """
    if 0 <= value <= 7:
        return 'низкий уровень'
    elif 8 <= value <= 14:
        return 'средний уровень'
    else:
        return 'высокий уровень'

def calc_sub_value_frust(row):
    """
    Функция для подсчета значения шкалы Фрустрация
    :param row: строка с ответами
    :return: число
    """
    lst_pr = [11,12,13,14,15,16,17,18,19,20]

    value_forward = 0 # счетчик прямых ответов

    for idx, value in enumerate(row):
        if idx +1 in lst_pr:
            value_forward += value

    return value_forward


def calc_sub_value_agres(row):
    """
    Функция для подсчета значения шкалы Агрессивность
    :param row: строка с ответами
    :return: число
    """
    lst_pr = [21,22,23,24,25,26,27,28,29,30]

    value_forward = 0 # счетчик прямых ответов

    for idx, value in enumerate(row):
        if idx +1 in lst_pr:
            value_forward += value

    return value_forward

def calc_sub_value_rig(row):
    """
    Функция для подсчета значения шкалы Ригидность
    :param row: строка с ответами
    :return: число
    """
    lst_pr = [31,32,33,34,35,36,37,38,39,40]

    value_forward = 0 # счетчик прямых ответов

    for idx, value in enumerate(row):
        if idx +1 in lst_pr:
            value_forward += value

    return value_forward

def calc_count_level_sub(df:pd.DataFrame, lst_cat:list, val_cat, col_cat, lst_cols:list):
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
    count_df['% низкий уровень от общего'] = round(
        count_df['низкий уровень'] / count_df['Итого'], 2) * 100
    count_df['% средний уровень от общего'] = round(
        count_df['средний уровень'] / count_df['Итого'], 2) * 100
    count_df['% высокий уровень от общего'] = round(
        count_df['высокий уровень'] / count_df['Итого'], 2) * 100

    return count_df




def create_result_spspg(base_df:pd.DataFrame, out_dct:dict, lst_svod_cols:list):
    """
    Функция для подсчета результата если указаны колонки по которым нужно провести свод
    :param df: датафрейм с результатами
    :param out_dct: словарь с уже подсчитанными базовыми данными
    :param lst_svod_cols: список сводных колонок
    :return: словарь
    """
    # Тревожность
    lst_reindex_one_level_cols = lst_svod_cols.copy()
    lst_reindex_one_level_cols.extend( ['низкий уровень', 'средний уровень', 'высокий уровень',
                                   'Итого'])


    # Субшкалы
    svod_count_one_level_anxiety_df = calc_count_level_sub(base_df, lst_svod_cols,
                                                      'Значение_шкалы_Тревожность',
                                                      'Уровень_шкалы_Тревожность',
                                                      lst_reindex_one_level_cols)

    svod_count_one_level_frust_df = calc_count_level_sub(base_df, lst_svod_cols,
                                                          'Значение_шкалы_Фрустрация',
                                                          'Уровень_шкалы_Фрустрация',
                                                          lst_reindex_one_level_cols)

    svod_count_one_level_agres_df = calc_count_level_sub(base_df, lst_svod_cols,
                                                         'Значение_шкалы_Агрессивность',
                                                         'Уровень_шкалы_Агрессивность',
                                                         lst_reindex_one_level_cols)

    svod_count_one_level_rig_df = calc_count_level_sub(base_df, lst_svod_cols,
                                                         'Значение_шкалы_Ригидность',
                                                         'Уровень_шкалы_Ригидность',
                                                         lst_reindex_one_level_cols)

    # Считаем среднее по шкалам
    svod_mean_df = pd.pivot_table(base_df,
                                  index=lst_svod_cols,
                                  values=['Значение_шкалы_Тревожность',
                                          'Значение_шкалы_Фрустрация',
                                          'Значение_шкалы_Агрессивность',
                                          'Значение_шкалы_Ригидность',
                                          ],
                                  aggfunc=round_mean)
    svod_mean_df.reset_index(inplace=True)
    # упорядочиваем колонки
    new_order_cols = lst_svod_cols.copy()
    new_order_cols.extend((['Значение_шкалы_Тревожность', 'Значение_шкалы_Фрустрация',
                            'Значение_шкалы_Агрессивность', 'Значение_шкалы_Ригидность',
                            ]))
    svod_mean_df = svod_mean_df.reindex(columns=new_order_cols)

    dct_rename_cols_mean = {'Значение_шкалы_Тревожность': 'Ср. Тревожность',
                            'Значение_шкалы_Фрустрация': 'Ср. Фрустрация',
                            'Значение_шкалы_Агрессивность': 'Ср. Агрессивность',
                            'Значение_шкалы_Ригидность': 'Ср. Ригидность' }
    svod_mean_df.rename(columns=dct_rename_cols_mean, inplace=True)

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

    out_dct.update({f'Ср {out_name}': svod_mean_df,
                    f'Свод Трев {out_name}': svod_count_one_level_anxiety_df,
                    f'Свод Фрус {out_name}': svod_count_one_level_frust_df,
                    f'Свод Агрес {out_name}': svod_count_one_level_agres_df,
                    f'Свод Риг {out_name}': svod_count_one_level_rig_df})

    if len(lst_svod_cols) == 1:
        return out_dct
    else:
        for idx, name_column in enumerate(lst_svod_cols):
            # Тревожность
            lst_reindex_column_level_cols =[lst_svod_cols[idx],'низкий уровень', 'средний уровень', 'высокий уровень',
                 'Итого']

            # Субшкалы
            svod_count_column_level_anxiety_df = calc_count_level_sub(base_df, lst_svod_cols[idx],
                                                                           'Значение_шкалы_Тревожность',
                                                                           'Уровень_шкалы_Тревожность',
                                                                           lst_reindex_column_level_cols)

            svod_count_column_level_frust_df = calc_count_level_sub(base_df, lst_svod_cols[idx],
                                                                       'Значение_шкалы_Фрустрация',
                                                                       'Уровень_шкалы_Фрустрация',
                                                                       lst_reindex_column_level_cols)

            svod_count_column_level_agres_df = calc_count_level_sub(base_df, lst_svod_cols[idx],
                                                                       'Значение_шкалы_Агрессивность',
                                                                       'Уровень_шкалы_Агрессивность',
                                                                       lst_reindex_column_level_cols)

            svod_count_column_level_rig_df = calc_count_level_sub(base_df, lst_svod_cols[idx],
                                                                   'Значение_шкалы_Ригидность',
                                                                   'Уровень_шкалы_Ригидность',
                                                                   lst_reindex_column_level_cols)

            # Считаем среднее по шкалам
            svod_mean_column_df = pd.pivot_table(base_df,
                                          index=[lst_svod_cols[idx]],
                                          values=['Значение_шкалы_Тревожность',
                                                  'Значение_шкалы_Фрустрация',
                                                  'Значение_шкалы_Агрессивность',
                                                  'Значение_шкалы_Ригидность',
                                                  ],
                                          aggfunc=round_mean)
            svod_mean_column_df.reset_index(inplace=True)
            # упорядочиваем колонки
            new_order_cols = [lst_svod_cols[idx]].copy()
            new_order_cols.extend((['Значение_шкалы_Тревожность', 'Значение_шкалы_Фрустрация',
                                    'Значение_шкалы_Агрессивность', 'Значение_шкалы_Ригидность',
                                    ]))
            svod_mean_column_df = svod_mean_column_df.reindex(columns=new_order_cols)

            dct_rename_cols_mean = {'Значение_шкалы_Тревожность': 'Ср. Тревожность',
                                    'Значение_шкалы_Фрустрация': 'Ср. Фрустрация',
                                    'Значение_шкалы_Агрессивность': 'Ср. Агрессивность',
                                    'Значение_шкалы_Ригидность': 'Ср. Ригидность'}
            svod_mean_column_df.rename(columns=dct_rename_cols_mean, inplace=True)

            name_column = lst_svod_cols[idx]
            name_column = re.sub(r'[\[\]\'+()<> :"?*|\\/]', '_', name_column)
            name_column = name_column[:15]

            out_dct.update({f'Ср {name_column}': svod_mean_column_df,
                             f'Свод Трев {name_column}': svod_count_column_level_anxiety_df,
                            f'Свод Фрус {name_column}': svod_count_column_level_frust_df,
                            f'Свод Агрес {name_column}': svod_count_column_level_agres_df,
                            f'Свод Риг {name_column}': svod_count_column_level_rig_df})

        return out_dct







def processing_aizenk_sps(result_df: pd.DataFrame, answers_df: pd.DataFrame, lst_svod_cols:list):
    """
    Функция для обработки
    :param result_df: часть датафрейма с описательными колонками
    :param answers_df: часть датафрейма с ответами
    :param lst_svod_cols:  список с колонками по которым нужно делать свод
    """
    try:
        out_answer_df = result_df.copy()  # делаем копию для последующего соединения с сырыми ответами
        if len(answers_df.columns) != 40:  # проверяем количество колонок с вопросами
            raise BadCountColumnsSPSA

        # очищаем названия колонок от возможных сочетаний .1 которые добавляет пандас при одинаковых колонках
        clean_df_lst = []
        for name_column in answers_df.columns:
            clean_name = re.sub(r'.\d+$', '', name_column)
            clean_df_lst.append(clean_name)

        answers_df.columns = clean_df_lst

        lst_check_cols = ['Не чувствую в себе уверенности',
                          'Часто из-за пустяков краснею',
                          'Мой сон беспокоен',
                          'Легко впадаю в уныние',
                          'Беспокоюсь о только воображаемых еще неприятностях',
                          'Меня пугают трудности',
                          'Люблю копаться в своих недостатках',
                          'Меня легко убедить',
                          'Я мнительный',
                          'Я с трудом переношу время ожидания',

                          'Нередко мне кажутся безвыходными положения, из которых все-таки можно найти выход',
                          'Неприятности меня сильно расстраивают, я падаю духом',
                          'При больших неприятностях я склонен без достаточных оснований винить себя',
                          'Несчастья и неудачи ничему меня не учат',
                          'Я часто отказываюсь от борьбы, считая ее бесплодной',
                          'Я нередко чувствую себя беззащитным',
                          'Иногда у меня бывает состояние отчаяния',
                          'Я чувствую растерянность перед трудностями',
                          'В трудные минуты жизни иногда веду себя по-детски, хочу чтобы пожалели',
                          'Считаю недостатки своего характера неисправимыми',

                          'Оставляю за собой последнее слово',
                          'Нередко в разговоре перебиваю собеседника',
                          'Меня легко рассердить',
                          'Люблю делать замечания другим',
                          'Хочу быть авторитетом для других',
                          'Не довольствуюсь малым, хочу наибольшего',
                          'Когда разгневаюсь, плохо себя сдерживаю',
                          'Предпочитаю лучше руководить, чем подчиняться',
                          'У меня резкая, грубоватая жестикуляция',
                          'Я мстителен',

                          'Мне трудно менять привычки',
                          'Нелегко переключать внимание',
                          'Очень настороженно отношусь ко всему новому',
                          'Меня трудно переубедить',
                          'Нередко у меня не выходит из головы мысль, от которой следовало бы освободиться',
                          'Нелегко сближаюсь с людьми',
                          'Меня расстраивают даже незначительные нарушения плана',
                          'Нередко я проявляю упрямство',
                          'Неохотно иду на риск',
                          'Резко переживаю отклонения от принятого мною режима дня',
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
            raise BadOrderSPSA

        # словарь для замены слов на числа
        dct_replace_value = {'нет, это мне совсем не подходит': 0,
                             'такое состояние у меня иногда бывает': 1,
                             'да, это состояние мне присуще часто': 2,
    }

        valid_values = [0, 1, 2]
        answers_df.replace(dct_replace_value, inplace=True)  # заменяем слова на цифры для подсчетов
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
            raise BadValueSPSA

        base_df = pd.DataFrame()

        # Тревожность
        base_df['Значение_шкалы_Тревожность'] = answers_df.apply(calc_sub_value_anxiety, axis=1)
        base_df['Уровень_шкалы_Тревожность'] = base_df['Значение_шкалы_Тревожность'].apply(calc_level)

        # Фрустрация
        base_df['Значение_шкалы_Фрустрация'] = answers_df.apply(calc_sub_value_frust, axis=1)
        base_df['Уровень_шкалы_Фрустрация'] = base_df['Значение_шкалы_Фрустрация'].apply(calc_level)

        # Агрессивность
        base_df['Значение_шкалы_Агрессивность'] = answers_df.apply(calc_sub_value_agres, axis=1)
        base_df['Уровень_шкалы_Агрессивность'] = base_df['Значение_шкалы_Агрессивность'].apply(calc_level)

        # Ригидность
        base_df['Значение_шкалы_Ригидность'] = answers_df.apply(calc_sub_value_rig, axis=1)
        base_df['Уровень_шкалы_Ригидность'] = base_df['Значение_шкалы_Ригидность'].apply(calc_level)

        # Создаем датафрейм для создания части в общий датафрейм
        part_df = pd.DataFrame()

        part_df['СПСА_Тревожность_Значение'] = base_df['Значение_шкалы_Тревожность']
        part_df['СПСА_Тревожность_Уровень'] = base_df['Уровень_шкалы_Тревожность']

        part_df['СПСА_Фрустрация_Значение'] = base_df['Значение_шкалы_Фрустрация']
        part_df['СПСА_Фрустрация_Уровень'] = base_df['Уровень_шкалы_Фрустрация']

        part_df['СПСА_Агрессивность_Значение'] = base_df['Значение_шкалы_Агрессивность']
        part_df['СПСА_Агрессивность_Уровень'] = base_df['Уровень_шкалы_Агрессивность']

        part_df['СПСА_Ригидность_Значение'] = base_df['Значение_шкалы_Ригидность']
        part_df['СПСА_Ригидность_Уровень'] = base_df['Уровень_шкалы_Ригидность']

        out_answer_df = pd.concat([out_answer_df, answers_df], axis=1)  # Датафрейм для проверки

        # Соединяем анкетную часть с результатной
        base_df = pd.concat([result_df, base_df], axis=1)
        base_df.sort_values(by='Значение_шкалы_Тревожность', ascending=False, inplace=True)  # сортируем

        # считаем среднее значение по шкалам
        avg_anxiety = round(base_df['Значение_шкалы_Тревожность'].mean(), 2)
        avg_frust = round(base_df['Значение_шкалы_Фрустрация'].mean(), 2)
        avg_agres = round(base_df['Значение_шкалы_Агрессивность'].mean(), 2)
        avg_rig = round(base_df['Значение_шкалы_Ригидность'].mean(), 2)

        avg_dct = {'Среднее значение шкалы Тревожность': avg_anxiety,
                   'Среднее значение шкалы Фрустрация': avg_frust,
                   'Среднее значение шкалы Агрессивность': avg_agres,
                   'Среднее значение шкалы Ригидность': avg_rig,
                   }

        avg_df = pd.DataFrame.from_dict(avg_dct, orient='index')
        avg_df = avg_df.reset_index()
        avg_df.columns = ['Показатель', 'Среднее значение']

        # Делаем свод  по  шкалам
        dct_svod_sub = {'Значение_шкалы_Тревожность': 'Уровень_шкалы_Тревожность',
                        'Значение_шкалы_Фрустрация': 'Уровень_шкалы_Фрустрация',
                        'Значение_шкалы_Агрессивность': 'Уровень_шкалы_Агрессивность',
                        'Значение_шкалы_Ригидность': 'Уровень_шкалы_Ригидность',
                        }

        dct_rename_svod_sub = {'Значение_шкалы_Тревожность': 'Тревожность',
                               'Значение_шкалы_Фрустрация': 'Фрустрация',
                               'Значение_шкалы_Агрессивность': 'Агрессивность',
                               'Значение_шкалы_Ригидность': 'Ригидность',
                               }

        # Списки для шкал
        lst_level = ['низкий уровень', 'средний уровень', 'высокий уровень']

        base_svod_sub_df = create_union_svod(base_df, dct_svod_sub, dct_rename_svod_sub, lst_level)
        # формируем основной словарь
        out_dct = {'Списочный результат': base_df, 'Список для проверки': out_answer_df,
                   'Свод по шкалам': base_svod_sub_df,
                   'Среднее по шкалам': avg_df,
                   }

        dct_prefix = {'Уровень_шкалы_Тревожность': 'Т',
                      'Уровень_шкалы_Фрустрация': 'Ф',
                      'Уровень_шкалы_Агрессивность': 'А',
                      'Уровень_шкалы_Ригидность': 'Р',
                      }

        out_dct = create_list_on_level(base_df, out_dct, lst_level, dct_prefix)

        """
            Сохраняем в зависимости от необходимости делать своды по определенным колонкам
            """
        if len(lst_svod_cols) == 0:
            return out_dct, part_df
        else:
            out_dct = create_result_spspg(base_df, out_dct, lst_svod_cols)

            return out_dct, part_df



    except BadOrderSPSA:
        messagebox.showerror('Лахеcис',
                             f'При обработке вопросов теста Самооценки психических состояний Айзенк обнаружены неправильные вопросы. Проверьте названия колонок с вопросами:\n'
                             f'{error_order_message[:5000]}\n'
                             f'Используйте при создании Яндекс-формы написание вопросов из руководства пользователя программы Лахесис.')
    except BadValueSPSA:
        messagebox.showerror('Лахеcис',
                             f'При обработке вопросов теста Самооценки психических состояний Айзенк обнаружены неправильные варианты ответов. Проверьте ответы на указанных строках:\n'
                             f'{error_message[:5000]}\n'
                             f'Используйте при создании Яндекс-формы написание вариантов ответа из руководства пользователя программы Лахесис.')


    except BadCountColumnsSPSA:
        messagebox.showerror('Лахеcис',
                             f'Проверьте количество колонок с ответами на тест Самооценки психических состояний Айзенк\n'
                             f'Должно быть 40 колонок с ответами')