"""
Скрипт для обработки результатов Опросник ксенофобских установок Гурина
"""

import pandas as pd
import re
from tkinter import messagebox
from lachesis_support_functions import round_mean_two,calc_count_scale,create_union_svod, create_list_on_level

class BadOrderOKUG(Exception):
    """
    Исключение для обработки случая когда колонки не совпадают
    """
    pass


class BadValueOKUG(Exception):
    """
    Исключение для неправильных значений в вариантах ответов
    """
    pass

class BadCountColumnsOKUG(Exception):
    """
    Исключение для обработки случая если количество колонок не равно 20
    """
    pass



def calc_value(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [1,2,3,4,5,6,7,8,9,10,
              11,12,13,14,15,16,17,18,19,20]
    lst_neg = [1,5,6,9,10,12,13,16,18,20]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_pr:
            if idx not in lst_neg:
                value_forward += value
            else:
                if value == 1:
                    value_forward += 7
                elif value == 2:
                    value_forward += 6
                elif value == 3:
                    value_forward += 5
                elif value == 4:
                    value_forward += 4
                elif value == 5:
                    value_forward += 3
                elif value == 6:
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
    if value <= 53:
        return 'преобладание положительных установок к иностранцам'
    elif 54 <= value <= 90:
        return 'сочетание положительных и негативных установок к иностранцам'
    else:
        return 'преобладание негативных (ксенофобских) установок к иностранцам'

def create_list_on_level_okug(base_df:pd.DataFrame,out_dct:dict,lst_level:list,dct_prefix:dict):
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
                if level == 'преобладание положительных установок к иностранцам':
                    level = 'положительные'
                elif level == 'сочетание положительных и негативных установок к иностранцам':
                    level = 'смешанные'
                else:
                    level = 'негативные'
                dct_level[f'{dct_prefix[key]}. {level}'] = temp_df
        out_dct.update(dct_level)

    return out_dct



def create_result_oku_gurina(base_df:pd.DataFrame, out_dct:dict, lst_svod_cols:list):
    """
    Функция для подсчета результата если указаны колонки по которым нужно провести свод
    :param df: датафрейм с результатами
    :param out_dct: словарь с уже подсчитанными базовыми данными
    :param lst_svod_cols: список сводных колонок
    :return: словарь
    """
    lst_level = ['преобладание положительных установок к иностранцам', 'сочетание положительных и негативных установок к иностранцам', 'преобладание негативных (ксенофобских) установок к иностранцам']

    lst_reindex_one_level_cols = lst_svod_cols.copy()
    lst_reindex_one_level_cols.extend(['преобладание положительных установок к иностранцам', 'сочетание положительных и негативных установок к иностранцам', 'преобладание негативных (ксенофобских) установок к иностранцам',
                                       'Итого'])  # Основная шкала
    svod_count_one_level_vcha_df = calc_count_scale(base_df, lst_svod_cols,
                                                    'ОКУ_Значение',
                                                    'ОКУ_Уровень',
                                                    lst_reindex_one_level_cols, lst_level)

    # Считаем среднее по субшкалам
    svod_mean_one_df = pd.pivot_table(base_df,
                                      index=lst_svod_cols,
                                      values=[
                                              'ОКУ_Значение',
                                              ],
                                      aggfunc=round_mean_two)
    svod_mean_one_df.reset_index(inplace=True)

    # упорядочиваем колонки
    new_order_cols = lst_svod_cols.copy()
    new_order_cols.extend(([ 'ОКУ_Значение'
                            ]))
    svod_mean_one_df = svod_mean_one_df.reindex(columns=new_order_cols)

    dct_rename_cols_mean = {'ОКУ_Значение': 'Ср. значение ксенофобских установок',
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
                    f'ОКУ {out_name}': svod_count_one_level_vcha_df,
                    })

    if len(lst_svod_cols) == 1:
        return out_dct
    else:
        for idx, name_column in enumerate(lst_svod_cols):
            lst_reindex_column_level_cols = [lst_svod_cols[idx],'преобладание положительных установок к иностранцам', 'сочетание положительных и негативных установок к иностранцам', 'преобладание негативных (ксенофобских) установок к иностранцам',
                                                  'Итого']
            svod_count_column_level_vcha_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                               'ОКУ_Значение',
                                                               'ОКУ_Уровень',
                                                               lst_reindex_column_level_cols, lst_level)

            # Считаем среднее по субшкалам
            svod_mean_column_df = pd.pivot_table(base_df,
                                                 index=[lst_svod_cols[idx]],
                                                 values=[
                                                     'ОКУ_Значение',
                                                 ],
                                                 aggfunc=round_mean_two)
            svod_mean_column_df.reset_index(inplace=True)

            # упорядочиваем колонки
            new_order_cols = [lst_svod_cols[idx]].copy()
            new_order_cols.extend((['ОКУ_Значение'
                                    ]))
            svod_mean_column_df = svod_mean_column_df.reindex(columns=new_order_cols)

            dct_rename_cols_mean = {'ОКУ_Значение': 'Ср. значение ксенофобских установок',
                                    }
            svod_mean_column_df.rename(columns=dct_rename_cols_mean, inplace=True)
            # Готовим наименование
            name_column = lst_svod_cols[idx]
            name_column = re.sub(r'[\[\]\'+()<> :"?*|\\/]', '_', name_column)
            name_column = name_column[:15]
            out_dct.update({f'Ср {name_column}': svod_mean_column_df,
                            f'ОКУ {name_column}': svod_count_column_level_vcha_df,
                            })
        return out_dct








def processing_oku_gurina(base_df: pd.DataFrame, answers_df: pd.DataFrame, lst_svod_cols:list):
    """
    Функция для обработки
    :param base_df: часть датафрейма с описательными колонками
    :param answers_df: часть датафрейма с ответами
    :param lst_svod_cols:  список с колонками по которым нужно делать свод
    """
    try:
        out_answer_df = base_df.copy()  # делаем копию для последующего соединения с сырыми ответами
        if len(answers_df.columns) != 20:  # проверяем количество колонок с вопросами
            raise BadCountColumnsOKUG

        # очищаем названия колонок от возможных сочетаний .1 которые добавляет пандас при одинаковых колонках
        clean_df_lst = []
        for name_column in answers_df.columns:
            clean_name = re.sub(r'.\d+$', '', name_column)
            clean_df_lst.append(clean_name)

        answers_df.columns = clean_df_lst

        lst_check_cols = ['Иностранцы должны иметь такие же права и социальные гарантии, как и местные жители',
                          'Следует запретить иностранцам селиться в одном месте',
                          'Большинство иностранцев нарушают местные правила и нормы',
                          'Следует применять к иностранцам более жесткие санкции и наказания, чем к местному населению, за совершение ими правонарушений',
                          'Следует сдерживать агрессию (оскорбления, провоцирование драк и др.) по отношению к иностранцам',
                          'Следует благоприятствовать развитию дружеских отношений к иностранцам',
                          'Иностранцы часто страдают опасными заболеваниями',
                          'Следует меньше общаться с иностранцами',
                          'Любой человек, независимо от его национальности, происхождения, имеет одинаковые права со всеми',
                          'Неверно мнение о том, что иностранцы могут быть угрозой для местного населения',

                          'Достаточно часты случаи, когда иностранцы вели себя агрессивно по отношению к местному населению',
                          'Среди иностранцев много интересных и незаурядных личностей',
                          'Все люди, независимо от их происхождения, национальности, могут найти общий язык между собой и жить в согласии',
                          'Тяжкие преступления (убийства, грабежи и т.д.) чаще всего совершают иностранцы',
                          'Враждебное отношение (оскорбление, унижение и т.д.) к иностранцам оправдано',
                          'Следует оказывать всестороннюю поддержку иностранцам',
                          'Зачастую иностранцы работают там, где могли бы работать местные жители',
                          'Между иностранцами и местным населением, где я живу, почти никогда не бывает конфликтов',
                          'Местные жители чаще всего враждебно настроены к иностранцам',
                          'Неправильно считать, что люди могут быть неполноценными (физически, интеллектуально, по экономическому статусу и т.д.) по признаку своей национальности, расы или религии'
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
            raise BadOrderOKUG

        # словарь для замены слов на числа
        dct_replace_value = {'1 – абсолютно не согласен': 1,
                             '2': 2,
                             '3': 3,
                             '4': 4,
                             '5': 5,
                             '6': 6,
                             '7 – абсолютно согласен': 7,
                             }
        valid_values = [1, 2, 3, 4,5,6,7]
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
            raise BadValueOKUG

        base_df['ОКУ_Значение'] = answers_df.apply(calc_value, axis=1)
        base_df['ОКУ_Уровень'] = base_df['ОКУ_Значение'].apply(calc_level)

        # Создаем датафрейм для создания части в общий датафрейм
        part_df = pd.DataFrame()
        part_df['ОКУГ_Значение'] = base_df['ОКУ_Значение']
        part_df['ОКУГ_Уровень'] = base_df['ОКУ_Уровень']


        base_df.sort_values(by='ОКУ_Значение', ascending=False, inplace=True)  # сортируем
        out_answer_df = pd.concat([out_answer_df, answers_df], axis=1)  # Датафрейм для проверки

        # Делаем свод  по  шкалам
        dct_svod_sub = {'ОКУ_Значение': 'ОКУ_Уровень',
                        }

        dct_rename_svod_sub = {'ОКУ_Значение': 'Степень выраженности ксенофобских установок',
                               }

        lst_sub = ['преобладание положительных установок к иностранцам', 'сочетание положительных и негативных установок к иностранцам', 'преобладание негативных (ксенофобских) установок к иностранцам']

        base_svod_sub_df = create_union_svod(base_df, dct_svod_sub, dct_rename_svod_sub, lst_sub)

        avg_vcha = round(base_df['ОКУ_Значение'].mean(), 2)

        avg_dct = {'Среднее значение выраженности ксенофобских установок': avg_vcha,
                   }

        avg_df = pd.DataFrame.from_dict(avg_dct, orient='index')
        avg_df = avg_df.reset_index()
        avg_df.columns = ['Показатель', 'Среднее значение']

        # формируем основной словарь
        out_dct = {'Списочный результат': base_df,
                   'Список для проверки': out_answer_df,
                   'Свод ОКУ': base_svod_sub_df,
                   'Среднее': avg_df,
                   }

        dct_prefix = {
            'ОКУ_Уровень': 'ОКУ',
        }

        out_dct = create_list_on_level_okug(base_df, out_dct, lst_sub, dct_prefix)

        """
                        Сохраняем в зависимости от необходимости делать своды по определенным колонкам
                        """
        if len(lst_svod_cols) == 0:
            return out_dct, part_df

        else:
            out_dct = create_result_oku_gurina(base_df, out_dct, lst_svod_cols)
            return out_dct, part_df

    except BadOrderOKUG:
        messagebox.showerror('Лахеcис',
                             f'При обработке вопросов теста Шкала оценки ксенофобских установок (ОКУ) Гурина обнаружены неправильные вопросы. Проверьте названия колонок с вопросами:\n'
                             f'{error_order_message[:5000]}\n'
                             f'Используйте при создании Яндекс-формы написание вопросов из руководства пользователя программы Лахесис.')
    except BadValueOKUG:
        messagebox.showerror('Лахеcис',
                             f'При обработке вопросов теста Шкала оценки ксенофобских установок (ОКУ) Гурина обнаружены неправильные варианты ответов. Проверьте ответы на указанных строках:\n'
                             f'{error_message[:5000]}\n'
                             f'Используйте при создании Яндекс-формы написание вариантов ответа из руководства пользователя программы Лахесис.')


    except BadCountColumnsOKUG:
        messagebox.showerror('Лахеcис',
                             f'Проверьте количество колонок с ответами на тест Шкала оценки ксенофобских установок (ОКУ) Гурина\n'
                             f'Должно быть 20 колонок с ответами')






