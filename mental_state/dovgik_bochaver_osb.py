"""
Скрипт для обработки результатов теста Опросник субъективного благополучия – WEMWBS Довжик Бочавер

"""
import pandas as pd
import re
from tkinter import messagebox
from lachesis_support_functions import round_mean_two,calc_count_scale,create_union_svod, create_list_on_level



class BadOrderOSBDB(Exception):
    """
    Исключение для обработки случая когда колонки не совпадают
    """
    pass


class BadValueOSBDB(Exception):
    """
    Исключение для неправильных значений в вариантах ответов
    """
    pass

class BadCountColumnsOSBDB(Exception):
    """
    Исключение для обработки случая если количество колонок не равно 14
    """
    pass


def calc_level(value):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """
    if 14 <= value <= 25:
        return '14-25'
    elif 26 <= value <= 36:
        return '26-36'
    elif 37 <= value <= 47:
        return '37-47'
    elif 48 <= value <= 58:
        return '48-58'
    else:
        return '59-70'


def create_result_osb_dov_boch(base_df:pd.DataFrame, out_dct:dict, lst_svod_cols:list):
    """
    Функция для подсчета результата если указаны колонки по которым нужно провести свод
    :param df: датафрейм с результатами
    :param out_dct: словарь с уже подсчитанными базовыми данными
    :param lst_svod_cols: список сводных колонок
    :return: словарь
    """
    lst_level = ['59-70', '48-58', '37-47','26-36','14-25']

    lst_reindex_one_level_cols = lst_svod_cols.copy()
    lst_reindex_one_level_cols.extend(['59-70', '48-58', '37-47','26-36','14-25',
                                       'Итого'])  # Основная шкала

    # АД
    svod_count_one_level_s_df = calc_count_scale(base_df, lst_svod_cols,
                                                 'ИП_Значение',
                                                 'ИП_Диапазон',
                                                 lst_reindex_one_level_cols, lst_level)

    # Считаем среднее по субшкалам
    svod_mean_one_df = pd.pivot_table(base_df,
                                      index=lst_svod_cols,
                                      values=['ИП_Значение',
                                              ],
                                      aggfunc=round_mean_two)
    svod_mean_one_df.reset_index(inplace=True)

    # упорядочиваем колонки
    new_order_cols = lst_svod_cols.copy()
    new_order_cols.extend((['ИП_Значение',
                            ]))
    svod_mean_one_df = svod_mean_one_df.reindex(columns=new_order_cols)
    dct_rename_cols_mean = {'ИП_Значение': 'Ср. Интегральный показатель',
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
                    f'ИП {out_name}': svod_count_one_level_s_df,
                    })

    if len(lst_svod_cols) == 1:
        return out_dct
    else:
        for idx, name_column in enumerate(lst_svod_cols):
            lst_reindex_column_level_cols = [lst_svod_cols[idx], '59-70', '48-58', '37-47','26-36','14-25',
                                             'Итого']

            # АД
            svod_count_column_level_s_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                            'ИП_Значение',
                                                            'ИП_Диапазон',
                                                            lst_reindex_column_level_cols, lst_level)

            # Считаем среднее по субшкалам
            svod_mean_column_df = pd.pivot_table(base_df,
                                                 index=[lst_svod_cols[idx]],
                                                 values=['ИП_Значение',
                                                         ],
                                                 aggfunc=round_mean_two)
            svod_mean_column_df.reset_index(inplace=True)

            # упорядочиваем колонки
            new_order_cols = [lst_svod_cols[idx]].copy()
            new_order_cols.extend((['ИП_Значение',
                                    ]))
            svod_mean_column_df = svod_mean_column_df.reindex(columns=new_order_cols)

            dct_rename_cols_mean = {'ИП_Значение': 'Ср. Интегральный показатель',
                                    }
            svod_mean_column_df.rename(columns=dct_rename_cols_mean, inplace=True)

            # Готовим наименование
            name_column = lst_svod_cols[idx]
            name_column = re.sub(r'[\[\]\'+()<> :"?*|\\/]', '_', name_column)
            name_column = name_column[:15]
            out_dct.update({f'Ср {name_column}': svod_mean_column_df,
                            f'ИП {name_column}': svod_count_column_level_s_df,
                            })
        return out_dct





def processing_osb_dov_boch(result_df: pd.DataFrame, answers_df: pd.DataFrame, lst_svod_cols:list):
    """
    Функция для обработки
    :param result_df: часть датафрейма с описательными колонками
    :param answers_df: часть датафрейма с ответами
    :param lst_svod_cols:  список с колонками по которым нужно делать свод
    """
    try:
        out_answer_df = result_df.copy()  # делаем копию для последующего соединения с сырыми ответами
        if len(answers_df.columns) != 14:  # проверяем количество колонок с вопросами
            raise BadCountColumnsOSBDB

        # очищаем названия колонок от возможных сочетаний .1 которые добавляет пандас при одинаковых колонках
        clean_df_lst = []
        for name_column in answers_df.columns:
            clean_name = re.sub(r'.\d+$', '', name_column)
            clean_df_lst.append(clean_name)

        answers_df.columns = clean_df_lst

        lst_check_cols = ['Я с оптимизмом смотрю в будущее',
                          'Я чувствую себя полезным(ой)',
                          'Я расслаблен(а)',
                          'Мне интересны другие люди',
                          'Я энергичен(на)',

                          'Я хорошо справляюсь с проблемами',
                          'Я мыслю ясно',
                          'Я доволен собой',
                          'Я чувствую свою близость другим людям',
                          'Я уверен в себе',
                          'Я способен составить свое собственное мнение о разных вещах',
                          'Я чувствую, что меня любят',
                          'Мне интересно новое',
                          'Мне весело'
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
            raise BadOrderOSBDB

        # словарь для замены слов на числа
        dct_replace_value = {'никогда': 1,
                             'редко': 2,
                             'иногда': 3,
                             'часто': 4,
                             'всегда': 5}

        valid_values = [1, 2, 3, 4, 5]
        answers_df.replace(dct_replace_value, inplace=True)  # заменяем слова на цифры для подсчетов
        # Проверяем, есть ли значения, отличающиеся от указанных в списке
        lst_error_answers = []  # список для хранения строк где найдены неправильные ответы

        for i in range(14):
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
            raise BadValueOSBDB

        base_df = pd.DataFrame()

        base_df['ИП_Значение'] = answers_df.sum(axis=1)
        base_df['ИП_Диапазон'] = base_df['ИП_Значение'].apply(
            calc_level)

        # Создаем датафрейм для создания части в общий датафрейм
        part_df = pd.DataFrame()
        part_df['ОСБДБ_Значение'] = base_df['ИП_Значение']
        part_df['ОСБДБ_Диапазон'] = base_df['ИП_Диапазон']

        # Соединяем анкетную часть с результатной
        base_df = pd.concat([result_df, base_df], axis=1)

        base_df.sort_values(by='ИП_Значение', ascending=True, inplace=True)  # сортируем
        out_answer_df = pd.concat([out_answer_df, answers_df], axis=1)  # Датафрейм для проверки

        # Делаем свод  по  шкалам
        dct_svod_sub = {'ИП_Значение': 'ИП_Диапазон',
                        }

        dct_rename_svod_sub = {'ИП_Значение': 'Диапазон интегрального показателя',
                               }

        lst_sub = ['59-70', '48-58', '37-47','26-36','14-25']

        base_svod_sub_df = create_union_svod(base_df, dct_svod_sub, dct_rename_svod_sub, lst_sub)

        avg_vcha = round(base_df['ИП_Значение'].mean(), 2)

        avg_dct = {'Среднее значение интегрального показателя': avg_vcha,
                   }

        avg_df = pd.DataFrame.from_dict(avg_dct, orient='index')
        avg_df = avg_df.reset_index()
        avg_df.columns = ['Показатель', 'Среднее значение']

        # формируем основной словарь
        out_dct = {'Списочный результат': base_df,
                   'Список для проверки': out_answer_df,
                   'Свод ИП': base_svod_sub_df,
                   'Среднее': avg_df,
                   }

        dct_prefix = {
            'ИП_Диапазон': 'ИП',
        }

        out_dct = create_list_on_level(base_df, out_dct, lst_sub, dct_prefix)

        """
                        Сохраняем в зависимости от необходимости делать своды по определенным колонкам
                        """
        if len(lst_svod_cols) == 0:
            return out_dct, part_df

        else:
            out_dct = create_result_osb_dov_boch(base_df, out_dct, lst_svod_cols)
            return out_dct, part_df


    except BadOrderOSBDB:
        messagebox.showerror('Лахеcис',
                             f'При обработке вопросов теста Опросник субъективного благополучия – WEMWBS Довжик Бочавер обнаружены неправильные вопросы. Проверьте названия колонок с вопросами:\n'
                             f'{error_order_message[:5000]}\n'
                             f'Используйте при создании Яндекс-формы написание вопросов из руководства пользователя программы Лахесис.')
    except BadValueOSBDB:
        messagebox.showerror('Лахеcис',
                             f'При обработке вопросов теста Опросник субъективного благополучия – WEMWBS Довжик Бочавер обнаружены неправильные варианты ответов. Проверьте ответы на указанных строках:\n'
                             f'{error_message[:5000]}\n'
                             f'Используйте при создании Яндекс-формы написание вариантов ответа из руководства пользователя программы Лахесис.')


    except BadCountColumnsOSBDB:
        messagebox.showerror('Лахеcис',
                             f'Проверьте количество колонок с ответами на тест Опросник субъективного благополучия – WEMWBS Довжик Бочавер\n'
                             f'Должно быть 14 колонок с ответами')