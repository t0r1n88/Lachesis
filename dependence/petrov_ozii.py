"""
Скрипт для обработки результатов теста Шкала оценки зависимости от Интернет-игр краткая форма, IGDS9-SF Петров, Черняк
"""

import pandas as pd
import re
from tkinter import messagebox
from lachesis_support_functions import round_mean_two,calc_count_scale,create_union_svod, create_list_on_level

class BadOrderOZIIPCH(Exception):
    """
    Исключение для обработки случая когда колонки не совпадают
    """
    pass


class BadValueOZIIPCH(Exception):
    """
    Исключение для неправильных значений в вариантах ответов
    """
    pass

class BadCountColumnsOZIIPCH(Exception):
    """
    Исключение для обработки случая если количество колонок не равно 9
    """
    pass


def calc_level(value):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """
    if 9<= value <= 18:
        return f'9-18'
    elif 19 <= value <= 28:
        return f'19-28'
    elif 29 <= value <= 38:
        return f'29-38'
    else:
        return f'39-45'


def create_result_ozii_pet_cher(base_df:pd.DataFrame, out_dct:dict, lst_svod_cols:list):
    """
    Функция для подсчета результата если указаны колонки по которым нужно провести свод
    :param df: датафрейм с результатами
    :param out_dct: словарь с уже подсчитанными базовыми данными
    :param lst_svod_cols: список сводных колонок
    :return: словарь
    """
    lst_level = ['9-18', '19-28', '29-38','39-45']

    lst_reindex_one_level_cols = lst_svod_cols.copy()
    lst_reindex_one_level_cols.extend(['9-18', '19-28', '29-38','39-45',
                                       'Итого'])  # Основная шкала

    svod_count_one_level_vcha_df = calc_count_scale(base_df, lst_svod_cols,
                                                    'ЗИИ_Значение',
                                                    'ЗИИ_Диапазон',
                                                    lst_reindex_one_level_cols, lst_level)

    # Считаем среднее по субшкалам
    svod_mean_one_df = pd.pivot_table(base_df,
                                      index=lst_svod_cols,
                                      values=[
                                              'ЗИИ_Значение',
                                              ],
                                      aggfunc=round_mean_two)
    svod_mean_one_df.reset_index(inplace=True)

    # упорядочиваем колонки
    new_order_cols = lst_svod_cols.copy()
    new_order_cols.extend(([ 'ЗИИ_Значение'
                            ]))
    svod_mean_one_df = svod_mean_one_df.reindex(columns=new_order_cols)

    dct_rename_cols_mean = {'ЗИИ_Значение': 'Ср. Зависимость от интернет-игр',
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
                    f'ЗИИ {out_name}': svod_count_one_level_vcha_df,
                    })

    if len(lst_svod_cols) == 1:
        return out_dct
    else:
        for idx, name_column in enumerate(lst_svod_cols):
            lst_reindex_column_level_cols = [lst_svod_cols[idx],'9-18', '19-28', '29-38','39-45',
                                                  'Итого']

            svod_count_column_level_vcha_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                               'ЗИИ_Значение',
                                                               'ЗИИ_Диапазон',
                                                               lst_reindex_column_level_cols, lst_level)

            # Считаем среднее по субшкалам
            svod_mean_column_df = pd.pivot_table(base_df,
                                              index=[lst_svod_cols[idx]],
                                              values=[
                                                  'ЗИИ_Значение',
                                              ],
                                              aggfunc=round_mean_two)
            svod_mean_column_df.reset_index(inplace=True)

            # упорядочиваем колонки
            new_order_cols = [lst_svod_cols[idx]].copy()
            new_order_cols.extend((['ЗИИ_Значение'
                                    ]))
            svod_mean_column_df = svod_mean_column_df.reindex(columns=new_order_cols)

            dct_rename_cols_mean = {'ЗИИ_Значение': 'Ср. Зависимость от интернет-игр',
                                    }
            svod_mean_column_df.rename(columns=dct_rename_cols_mean, inplace=True)
            # Готовим наименование
            name_column = lst_svod_cols[idx]
            name_column = re.sub(r'[\[\]\'+()<> :"?*|\\/]', '_', name_column)
            name_column = name_column[:15]
            out_dct.update({f'Ср {name_column}': svod_mean_column_df,
                            f'ЗИИ {name_column}': svod_count_column_level_vcha_df,
                            })
        return out_dct








def processing_ozii_pet_cher(base_df: pd.DataFrame, answers_df: pd.DataFrame, lst_svod_cols:list):
    """
    Функция для обработки
    :param base_df: часть датафрейма с описательными колонками
    :param answers_df: часть датафрейма с ответами
    :param lst_svod_cols:  список с колонками по которым нужно делать свод
    """
    try:
        out_answer_df = base_df.copy()  # делаем копию для последующего соединения с сырыми ответами
        if len(answers_df.columns) != 9:  # проверяем количество колонок с вопросами
            raise BadCountColumnsOZIIPCH

        # очищаем названия колонок от возможных сочетаний .1 которые добавляет пандас при одинаковых колонках
        clean_df_lst = []
        for name_column in answers_df.columns:
            clean_name = re.sub(r'.\d+$', '', name_column)
            clean_df_lst.append(clean_name)

        answers_df.columns = clean_df_lst

        lst_check_cols = ['Есть ли у Вас ощущение, что Ваше увлечение играми полностью поглощает Вас? (Например: Вы часто размышляете о том, как сыграли в прошлый раз, и с нетерпением ждете новой игровой сессии? Считаете ли вы, что компьютерные игры стали наиболее важным занятием в Вашей жизни?)',
                          'Испытываете ли Вы раздражение, тревогу или даже грусть, когда пытаетесь уменьшить количество времени, которое тратите на игры, или пытаетесь совсем бросить играть?',
                          'Испытываете ли Вы потребность тратить все больше времени за игрой для того, чтобы получить удовлетворение или удовольствие?',
                          'Преследуют ли Вас постоянные неудачи, когда Вы пытаетесь контролировать время, проводимое за играми, или пытаетесь бросить играть?',
                          'Утратили ли Вы Интерес к своим прежним хобби и прочим видам развлечений в результате увлечения компьютерными играми?',
                          'Продолжаете ли Вы играть тогда, когда знаете, что это приводит к проблемам между Вами и другими людьми?',
                          'Приходилось ли Вам когда — либо обманывать членов своей семьи, психотерапевта или других людей по поводу количества времени, которые Вы тратите на игры?',
                          'Играете ли Вы в игры для того, чтобы временно устраниться от проблем или избавиться от плохого настроения (например, беспомощность, чувство вины, тревожность)?',
                          'Страдают ли из — за Вашего увлечения играми важные отношения, работа, учеба или возможности Вашего карьерного роста?',
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
            raise BadOrderOZIIPCH

        # словарь для замены слов на числа
        dct_replace_value = {'никогда': 1,
                             'редко': 2,
                             'иногда': 3,
                             'часто': 4,
                             'очень часто': 5,
                             }
        valid_values = [1, 2, 3, 4, 5]
        answers_df.replace(dct_replace_value, inplace=True)  # заменяем слова на цифры для подсчетов
        # Проверяем, есть ли значения, отличающиеся от указанных в списке
        lst_error_answers = []  # список для хранения строк где найдены неправильные ответы

        for i in range(9):
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
            raise BadValueOZIIPCH

        base_df['ЗИИ_Значение'] = answers_df.sum(axis=1)
        base_df['ЗИИ_Диапазон'] = base_df['ЗИИ_Значение'].apply(calc_level)

    # Создаем датафрейм для создания части в общий датафрейм
        part_df = pd.DataFrame()

        # Основные шкалы

        part_df['ОЗИИПЧ_Значение'] = base_df['ЗИИ_Значение']
        part_df['ОЗИИПЧ_Диапазон'] = base_df['ЗИИ_Диапазон']

        out_answer_df = pd.concat([out_answer_df, answers_df], axis=1)  # Датафрейм для проверки

        base_df.sort_values(by='ЗИИ_Значение', ascending=False, inplace=True)  # сортируем

        # Делаем свод  по  шкалам
        dct_svod_sub = {'ЗИИ_Значение': 'ЗИИ_Диапазон',
                        }

        dct_rename_svod_sub = {
            'ЗИИ_Значение': 'Диапазон зависимости от интернет-игр',
        }

        lst_sub = ['9-18', '19-28', '29-38','39-45']

        base_svod_sub_df = create_union_svod(base_df, dct_svod_sub, dct_rename_svod_sub, lst_sub)

        avg_psp = round(base_df['ЗИИ_Значение'].mean(), 2)

        avg_dct = {'Среднее значение зависимости от интернет-игр': avg_psp,
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

        dct_prefix = {'ЗИИ_Диапазон': 'ЗИИ',
                      }

        out_dct = create_list_on_level(base_df, out_dct, lst_sub, dct_prefix)

        """
                                Сохраняем в зависимости от необходимости делать своды по определенным колонкам
                                """
        if len(lst_svod_cols) == 0:
            return out_dct, part_df

        else:
            out_dct = create_result_ozii_pet_cher(base_df, out_dct, lst_svod_cols)
            return out_dct, part_df


    except BadOrderOZIIPCH:
        messagebox.showerror('Лахеcис',
                             f'При обработке вопросов теста Шкала оценки зависимости от Интернет-игр краткая форма, IGDS9-SF Петров, Черняк обнаружены неправильные вопросы. Проверьте названия колонок с вопросами:\n'
                             f'{error_order_message[:5000]}\n'
                             f'Используйте при создании Яндекс-формы написание вопросов из руководства пользователя программы Лахесис.')
    except BadValueOZIIPCH:
        messagebox.showerror('Лахеcис',
                             f'При обработке вопросов теста Шкала оценки зависимости от Интернет-игр краткая форма, IGDS9-SF Петров, Черняк обнаружены неправильные варианты ответов. Проверьте ответы на указанных строках:\n'
                             f'{error_message[:5000]}\n'
                             f'Используйте при создании Яндекс-формы написание вариантов ответа из руководства пользователя программы Лахесис.')


    except BadCountColumnsOZIIPCH:
        messagebox.showerror('Лахеcис',
                             f'Проверьте количество колонок с ответами на тест Шкала оценки зависимости от Интернет-игр краткая форма, IGDS9-SF Петров, Черняк\n'
                             f'Должно быть 9 колонок с ответами')