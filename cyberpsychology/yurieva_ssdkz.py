"""
Скрипт для обработки результатов теста Способ скрининговой диагностики компьютерной зависимости Л.Н. Юрьева, Т.Ю. Больбот
"""

import pandas as pd
import re
from tkinter import messagebox
from lachesis_support_functions import round_mean_two,calc_count_scale,create_union_svod, create_list_on_level

class BadOrderSSDKZYB(Exception):
    """
    Исключение для обработки случая когда колонки не совпадают
    """
    pass


class BadValueSSDKZYB(Exception):
    """
    Исключение для неправильных значений в вариантах ответов
    """
    pass

class BadCountColumnsSSDKZYB(Exception):
    """
    Исключение для обработки случая если количество колонок не равно 11
    """
    pass


def calc_value(row):
    """
    Функция для подсчета значения
    :return: число
    """
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx != 4:
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


def calc_level(value):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """
    if value <= 15:
        return f'отсутствие КЗ'
    elif 16 <= value <= 22:
        return f'стадия увлеченности'
    elif 23 <= value <= 37:
        return f'риск КЗ'
    else:
        return f'наличие КЗ'


def create_result_ssdkz_yur_bol(base_df:pd.DataFrame, out_dct:dict, lst_svod_cols:list):
    """
    Функция для подсчета результата если указаны колонки по которым нужно провести свод
    :param df: датафрейм с результатами
    :param out_dct: словарь с уже подсчитанными базовыми данными
    :param lst_svod_cols: список сводных колонок
    :return: словарь
    """

    lst_level = ['отсутствие КЗ', 'стадия увлеченности', 'риск КЗ','наличие КЗ']

    lst_reindex_one_level_cols = lst_svod_cols.copy()
    lst_reindex_one_level_cols.extend(['отсутствие КЗ', 'стадия увлеченности', 'риск КЗ','наличие КЗ',
                                       'Итого'])  # Основная шкала

    svod_count_one_level_vcha_df = calc_count_scale(base_df, lst_svod_cols,
                                                    'КЗ_Значение',
                                                    'КЗ_Уровень',
                                                    lst_reindex_one_level_cols, lst_level)

    # Считаем среднее по субшкалам
    svod_mean_one_df = pd.pivot_table(base_df,
                                      index=lst_svod_cols,
                                      values=[
                                          'КЗ_Значение',
                                      ],
                                      aggfunc=round_mean_two)
    svod_mean_one_df.reset_index(inplace=True)

    # упорядочиваем колонки
    new_order_cols = lst_svod_cols.copy()
    new_order_cols.extend((['КЗ_Значение'
                            ]))
    svod_mean_one_df = svod_mean_one_df.reindex(columns=new_order_cols)

    dct_rename_cols_mean = {'КЗ_Значение': 'Ср. Компьютерная зависимость',
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
                    f'КЗ {out_name}': svod_count_one_level_vcha_df,
                    })

    if len(lst_svod_cols) == 1:
        return out_dct

    else:
        for idx, name_column in enumerate(lst_svod_cols):
            lst_reindex_column_level_cols = [lst_svod_cols[idx],'отсутствие КЗ', 'стадия увлеченности', 'риск КЗ','наличие КЗ',
                                                  'Итого']

            svod_count_column_level_vcha_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                               'КЗ_Значение',
                                                               'КЗ_Уровень',
                                                               lst_reindex_column_level_cols, lst_level)

            # Считаем среднее по субшкалам
            svod_mean_column_df = pd.pivot_table(base_df,
                                              index=[lst_svod_cols[idx]],
                                              values=[
                                                  'КЗ_Значение',
                                              ],
                                              aggfunc=round_mean_two)
            svod_mean_column_df.reset_index(inplace=True)

            # упорядочиваем колонки
            new_order_cols = [lst_svod_cols[idx]].copy()
            new_order_cols.extend((['КЗ_Значение'
                                    ]))
            svod_mean_column_df = svod_mean_column_df.reindex(columns=new_order_cols)

            dct_rename_cols_mean = {'КЗ_Значение': 'Ср. Компьютерная зависимость',
                                    }
            svod_mean_column_df.rename(columns=dct_rename_cols_mean, inplace=True)

            # Готовим наименование
            name_column = lst_svod_cols[idx]
            name_column = re.sub(r'[\[\]\'+()<> :"?*|\\/]', '_', name_column)
            name_column = name_column[:15]
            out_dct.update({f'Ср {name_column}': svod_mean_column_df,
                            f'КЗ {name_column}': svod_count_column_level_vcha_df,
                            })
        return out_dct








def processing_ssdkz_yur_bol(base_df: pd.DataFrame, answers_df: pd.DataFrame, lst_svod_cols:list):
    """
    Функция для обработки
    :param base_df: часть датафрейма с описательными колонками
    :param answers_df: часть датафрейма с ответами
    :param lst_svod_cols:  список с колонками по которым нужно делать свод
    """
    try:
        out_answer_df = base_df.copy()  # делаем копию для последующего соединения с сырыми ответами
        if len(answers_df.columns) != 11:  # проверяем количество колонок с вопросами
            raise BadCountColumnsSSDKZYB

        # очищаем названия колонок от возможных сочетаний .1 которые добавляет пандас при одинаковых колонках
        clean_df_lst = []
        for name_column in answers_df.columns:
            clean_name = re.sub(r'.\d+$', '', name_column)
            clean_df_lst.append(clean_name)

        answers_df.columns = clean_df_lst

        lst_check_cols = ['Как часто Вы ощущаете оживление, удовольствие, удовлетворение или облегчение, находясь за компьютером (в сети)?',
                          'Как часто Вы предвкушаете пребывание за компьютером (в сети), думая и размышляя о том, как окажетесь за компьютером, откроете определенный сайт, найдете определенную информацию, заведете новые знакомства?',
                          'Как часто Вам необходимо все больше времени проводить за компьютером (в сети) или тратить все больше денег для того, чтобы получить те же ощущения?',
                          'Как часто Вам удается самостоятельно прекратить работу за компьютером (в сети)?',
                          'Как часто Вы чувствуете нервозность, снижение настроения, раздражительность или пустоту вне компьютера (вне сети)?',
                          'Как часто Вы ощущаете потребность вернуться за компьютер (в сеть) для улучшения настроения или ухода от жизненных проблем?',
                          'Как часто Вы пренебрегаете семейными, общественными обязанностями и учебой из-за частой работы за компьютером (пребывания в сети)?',
                          'Как часто Вам приходится лгать, скрывать от родителей или преподавателей количество времени, проводимого за компьютером (в сети)?',
                          'Как часто существует актуализация или угроза потери дружеских и/или семейных отношений, изменений финансовой стабильности, успехов в учебе в связи с частой работой за компьютером (пребыванием в сети)?',
                          'Как часто Вы отмечаете физические симптомы, такие как: онемение и боли в кисти руки, боли в спине, сухость в глазах, головные боли; пренебрежение личной гигиеной, употребление пищи около компьютера?',
                          'Как часто Вы отмечаете нарушения сна или изменения режима сна в связи с частой работой за компьютером (в сети)?',
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
            raise BadOrderSSDKZYB

        # словарь для замены слов на числа
        dct_replace_value = {'очень часто': 4,
                             'часто': 3,
                             'редко': 2,
                             'никогда': 1,
                             }
        valid_values = [1, 2, 3, 4]
        answers_df.replace(dct_replace_value, inplace=True)  # заменяем слова на цифры для подсчетов
        # Проверяем, есть ли значения, отличающиеся от указанных в списке
        lst_error_answers = []  # список для хранения строк где найдены неправильные ответы

        for i in range(11):
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
            raise BadValueSSDKZYB

        base_df['КЗ_Значение'] = answers_df.apply(calc_value, axis=1)
        base_df['КЗ_Уровень'] = base_df['КЗ_Значение'].apply(calc_level)

        # Создаем датафрейм для создания части в общий датафрейм
        part_df = pd.DataFrame()

        # Основные шкалы

        part_df['ССДКЗЮБ_Значение'] = base_df['КЗ_Значение']
        part_df['ССДКЗЮБ_Уровень'] = base_df['КЗ_Уровень']

        out_answer_df = pd.concat([out_answer_df, answers_df], axis=1)  # Датафрейм для проверки

        base_df.sort_values(by='КЗ_Значение', ascending=False, inplace=True)  # сортируем

        # Делаем свод  по  шкалам
        dct_svod_sub = {'КЗ_Значение': 'КЗ_Уровень',
                        }

        dct_rename_svod_sub = {
            'КЗ_Значение': 'Уровень компьютерной зависимости',
        }

        lst_sub = ['отсутствие КЗ', 'стадия увлеченности', 'риск КЗ','наличие КЗ']

        base_svod_sub_df = create_union_svod(base_df, dct_svod_sub, dct_rename_svod_sub, lst_sub)

        avg_psp = round(base_df['КЗ_Значение'].mean(), 2)

        avg_dct = {'Среднее значение Компьютерной зависимости': avg_psp,
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

        dct_prefix = {'КЗ_Уровень': 'КЗ',
                      }

        out_dct = create_list_on_level(base_df, out_dct, lst_sub, dct_prefix)

        """
                        Сохраняем в зависимости от необходимости делать своды по определенным колонкам
                        """
        if len(lst_svod_cols) == 0:
            return out_dct, part_df
        else:
            out_dct = create_result_ssdkz_yur_bol(base_df, out_dct, lst_svod_cols)
            return out_dct, part_df


    except BadOrderSSDKZYB:
        messagebox.showerror('Лахеcис',
                             f'При обработке вопросов теста Способ скрининговой диагностики компьютерной зависимости Юрьева, Больбот обнаружены неправильные вопросы. Проверьте названия колонок с вопросами:\n'
                             f'{error_order_message[:5000]}\n'
                             f'Используйте при создании Яндекс-формы написание вопросов из руководства пользователя программы Лахесис.')
    except BadValueSSDKZYB:
        messagebox.showerror('Лахеcис',
                             f'При обработке вопросов теста Способ скрининговой диагностики компьютерной зависимости Юрьева, Больбот обнаружены неправильные варианты ответов. Проверьте ответы на указанных строках:\n'
                             f'{error_message[:5000]}\n'
                             f'Используйте при создании Яндекс-формы написание вариантов ответа из руководства пользователя программы Лахесис.')


    except BadCountColumnsSSDKZYB:
        messagebox.showerror('Лахеcис',
                             f'Проверьте количество колонок с ответами на тест Способ скрининговой диагностики компьютерной зависимости Юрьева, Больбот\n'
                             f'Должно быть 11 колонок с ответами')