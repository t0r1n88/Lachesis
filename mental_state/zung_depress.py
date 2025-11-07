"""
Скрипт для обработки результатов теста Шкала депрессии Цунга
"""

from lachesis_support_functions import round_mean,create_union_svod
import pandas as pd
import re
from tkinter import messagebox


class BadOrderZungDepress(Exception):
    """
    Исключение для обработки случая когда колонки не совпадают
    """
    pass


class BadValueZungDepress(Exception):
    """
    Исключение для неправильных значений в вариантах ответов
    """
    pass

class BadCountColumnsZungDepress(Exception):
    """
    Исключение для обработки случая если количество колонок не равно 20
    """
    pass


def calc_value_zung_depress(row):
    """
    Функция для подсчета значения депрессии Цунга
    :param row: строка с ответами
    :return: число
    """
    value_depress_forward = 0 # счетчик депрессии прямых ответов
    value_depress_reverse = 0 # счетчик депрессии обратных ответов
    lst_forward = [0,2,3,6,7,8,9,12,14,18] # список ответов которые нужно считать простым сложением
    lst_reverse = [1,4,5,10,11,13,15,16,17,19] # обратный подсчет
    for idx, value in enumerate(row):
        if idx in lst_forward:
            value_depress_forward += value
        elif idx in lst_reverse:
            if value == 1:
                value_depress_reverse += 4
            elif value == 2:
                value_depress_reverse += 3
            elif value == 3:
                value_depress_reverse += 2
            elif value == 4:
                value_depress_reverse += 1

    return value_depress_forward + value_depress_reverse





def calc_level_zung_depress(value):
    """
    Функция для подсчета уровня депрессии по шкале Цунга
    :param value:
    :return:
    """
    if 0 <= value <= 50:
        return 'депрессия не выявлена'
    elif 51 <= value <= 59:
        return 'легкая депрессия ситуативного или невротического генеза'
    elif 60 <= value <= 69:
        return 'субдепрессивное состояние или маскированная депрессия'
    else:
        return 'истинное депрессивное состояние'


def create_zung_list_on_level(base_df:pd.DataFrame, out_dct:dict, lst_level:list, dct_prefix:dict):
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
                if level == 'депрессия не выявлена':
                    level = 'не выявлена'
                elif level == 'легкая депрессия ситуативного или невротического генеза':
                    level = 'легкая'
                elif level == 'субдепрессивное состояние или маскированная депрессия':
                    level = 'субдепрессивное'
                else:
                    level = 'истинно депрессивное'
                dct_level[f'{dct_prefix[key]} {level}'] = temp_df
        out_dct.update(dct_level)

    return out_dct


def calc_count_level(df:pd.DataFrame, lst_cat:list, val_cat, col_cat, lst_cols:list):
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
    count_df['% депрессия не выявлена от общего'] = round(
        count_df['депрессия не выявлена'] / count_df['Итого'], 2) * 100
    count_df['% легкая депрессия ситуативного или невротического генеза от общего'] = round(
        count_df['легкая депрессия ситуативного или невротического генеза'] / count_df['Итого'], 2) * 100
    count_df['% субдепрессивное состояние или маскированная депрессия от общего'] = round(
        count_df['субдепрессивное состояние или маскированная депрессия'] / count_df['Итого'], 2) * 100
    count_df['% истинное депрессивное состояние от общего'] = round(
        count_df['истинное депрессивное состояние'] / count_df['Итого'], 2) * 100

    return count_df


def create_result_zung_depress(base_df:pd.DataFrame, out_dct:dict, lst_svod_cols:list):
    """
    Функция для подсчета результата если указаны колонки по которым нужно провести свод
    :param df: датафрейм с результатами
    :param out_dct: словарь с уже подсчитанными базовыми данными
    :param lst_svod_cols: список сводных колонок
    :return: словарь
    """
    lst_reindex_one_level_cols = lst_svod_cols.copy()
    lst_reindex_one_level_cols.extend( ['депрессия не выявлена', 'легкая депрессия ситуативного или невротического генеза', 'субдепрессивное состояние или маскированная депрессия',
                                        'истинное депрессивное состояние','Итого'])

    svod_count_one_level_depress_df = calc_count_level(base_df, lst_svod_cols,
                                                       'Значение_уровня_депрессии',
                                                       'Уровень_депрессии',
                                                       lst_reindex_one_level_cols)

    # Считаем среднее по субшкалам
    svod_mean_one_df = pd.pivot_table(base_df,
                                      index=lst_svod_cols,
                                      values=['Значение_уровня_депрессии',
                                              ],
                                      aggfunc=round_mean)
    svod_mean_one_df.reset_index(inplace=True)
    # упорядочиваем колонки
    new_order_cols = lst_svod_cols.copy()
    new_order_cols.extend((['Значение_уровня_депрессии',
                            ]))
    svod_mean_one_df = svod_mean_one_df.reindex(columns=new_order_cols)

    dct_rename_cols_mean = {'Значение_уровня_депрессии': 'Ср. Депрессия',
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
                    f'Свод {out_name}': svod_count_one_level_depress_df})
    if len(lst_svod_cols) == 1:
        return out_dct
    else:
        for idx, name_column in enumerate(lst_svod_cols):
            lst_reindex_column_level_cols = [lst_svod_cols[idx],'депрессия не выявлена', 'легкая депрессия ситуативного или невротического генеза', 'субдепрессивное состояние или маскированная депрессия',
                                        'истинное депрессивное состояние',
                                             'Итого']
            svod_count_column_level_depress_df = calc_count_level(base_df, lst_svod_cols[idx],
                                                                  'Значение_уровня_депрессии',
                                                                  'Уровень_депрессии',
                                                                  lst_reindex_column_level_cols)

            # Считаем среднее по субшкалам
            svod_mean_column_df = pd.pivot_table(base_df,
                                                 index=[lst_svod_cols[idx]],
                                                 values=['Значение_уровня_депрессии',
                                                         ],
                                                 aggfunc=round_mean)
            svod_mean_column_df.reset_index(inplace=True)
            # упорядочиваем колонки
            new_order_cols = [lst_svod_cols[idx]].copy()
            new_order_cols.extend((['Значение_уровня_депрессии',
                                    ]))
            svod_mean_column_df = svod_mean_column_df.reindex(columns=new_order_cols)

            dct_rename_cols_mean = {'Значение_уровня_депрессии': 'Ср. Депрессия',
                                    }
            svod_mean_column_df.rename(columns=dct_rename_cols_mean, inplace=True)

            name_column = lst_svod_cols[idx]
            name_column = re.sub(r'[\[\]\'+()<> :"?*|\\/]', '_', name_column)
            name_column = name_column[:15]

            out_dct.update({f'Ср {name_column}': svod_mean_column_df,
                            f'Свод {name_column}': svod_count_column_level_depress_df})
        return out_dct



def processing_zung_depress(base_df: pd.DataFrame, answers_df: pd.DataFrame,lst_svod_cols:list):
    """
    Функция для обработки
    :param base_df: часть датафрейма с описательными колонками
    :param answers_df: часть датафрейма с ответами
    :param lst_svod_cols:  список с колонками по которым нужно делать свод
    """
    try:
        out_answer_df = base_df.copy()  # делаем копию для последующего соединения с сырыми ответами
        if len(answers_df.columns) != 20:  # проверяем количество колонок
            raise BadCountColumnsZungDepress

        # очищаем названия колонок от возможных сочетаний .1 которые добавляет пандас при одинаковых колонках
        clean_df_lst = []
        for name_column in answers_df.columns:
            clean_name = re.sub(r'.\d+$', '', name_column)
            clean_df_lst.append(clean_name)

        answers_df.columns = clean_df_lst

        # Словарь с проверочными данными
        lst_check_cols = ['Я чувствую подавленность, тоску',
                          'Утром я чувствую себя лучше всего',
                          'У меня бывают периоды плача или близости к слезам',
                          'У меня плохой ночной сон',
                          'Аппетит у меня не хуже обычного',
                          'Мне приятно смотреть на привлекательных людей, разговаривать с ними, находиться рядом',
                          'Я замечаю, что теряю вес',
                          'Меня беспокоят запоры',
                          'Сердце бьется быстрее, чем обычно',
                          'Я устаю без всяких причин',
                          'Я мыслю так же ясно, как всегда',
                          'Мне легко делать то, что я умею',
                          'Чувствую беспокойство и не могу усидеть на месте',
                          'У меня есть надежды на будущее',
                          'Я более раздражителен, чем обычно',
                          'Мне легко принимать решения',
                          'Я чувствую, что полезен и необходим',
                          'Я живу достаточно полной жизнью',
                          'Я чувствую, что другим людям станет лучше, если я умру',
                          'Меня до сих пор радует то, что радовало всегда'
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
            raise BadOrderZungDepress

        # словарь для замены слов на числа
        dct_replace_value = {'никогда или изредка': 1,
                             'иногда': 2,
                             'часто': 3,
                             'почти всегда или постоянно': 4}

        valid_values = [1, 2, 3, 4]
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
            raise BadValueZungDepress

        # Проводим подсчет
        base_df['Значение_уровня_депрессии'] = answers_df.apply(calc_value_zung_depress, axis=1)
        base_df['Значение_нормы'] = '0-50 баллов'
        base_df['Уровень_депрессии'] = base_df['Значение_уровня_депрессии'].apply(calc_level_zung_depress)

        # Создаем датафрейм для создания части в общий датафрейм
        part_df = pd.DataFrame()
        part_df['ШДЦ_Депрессия_Значение'] = base_df['Значение_уровня_депрессии']
        part_df['ШДЦ_Депрессия_Уровень'] = base_df['Уровень_депрессии']

        out_answer_df = pd.concat([out_answer_df, answers_df], axis=1)

        base_df.sort_values(by='Значение_уровня_депрессии', ascending=False, inplace=True)  # сортируем

        # Делаем свод  по  шкалам
        dct_svod_sub = {'Значение_уровня_депрессии': 'Уровень_депрессии',
                        }

        dct_rename_svod_sub = {'Значение_уровня_депрессии': 'Депрессия',
                               }

        # Списки для шкал
        lst_level = ['депрессия не выявлена', 'легкая депрессия ситуативного или невротического генеза',
                     'субдепрессивное состояние или маскированная депрессия', 'истинное депрессивное состояние']

        base_svod_sub_df = create_union_svod(base_df, dct_svod_sub, dct_rename_svod_sub, lst_level)

     # считаем среднее значение по шкалам
        avg_depress = round(base_df['Значение_уровня_депрессии'].mean(), 2)

        avg_dct = {'Среднее значение уровня депрессии': avg_depress,
                   }

        avg_df = pd.DataFrame.from_dict(avg_dct, orient='index')
        avg_df = avg_df.reset_index()
        avg_df.columns = ['Показатель', 'Среднее значение']

        # формируем основной словарь
        out_dct = {'Списочный результат': base_df, 'Список для проверки': out_answer_df,
                   'Свод': base_svod_sub_df,
                   'Среднее': avg_df,
                   }

        # Делаем списки
        dct_prefix = {'Уровень_депрессии': '',
                      }

        out_dct = create_zung_list_on_level(base_df, out_dct, lst_level, dct_prefix)
        """
            Сохраняем в зависимости от необходимости делать своды по определенным колонкам
            """
        if len(lst_svod_cols) == 0:
            return out_dct, part_df
        else:
            out_dct = create_result_zung_depress(base_df, out_dct, lst_svod_cols)

            return out_dct, part_df

    except BadOrderZungDepress:
        messagebox.showerror('Лахеcис',
                             f'При обработке вопросов теста Шкала депрессии Цунга обнаружены неправильные вопросы. Проверьте названия колонок с вопросами:\n'
                             f'{error_order_message}\n'
                             f'Используйте при создании Яндекс-формы написание вопросов из руководства пользователя программы Лахесис.')
    except BadValueZungDepress:
        messagebox.showerror('Лахеcис',
                             f'При обработке вопросов теста Шкала депрессии Цунга обнаружены неправильные варианты ответов. Проверьте ответы на указанных строках:\n'
                             f'{error_message[:5000]}\n'
                             f'Используйте при создании Яндекс-формы написание вариантов ответа из руководства пользователя программы Лахесис.')

    except BadCountColumnsZungDepress:
        messagebox.showerror('Лахеcис',
                             f'Проверьте количество колонок с ответами на тест Шкала депрессии Цунга\n'
                             f'Должно быть 20 колонок с вопросами'
                             )
