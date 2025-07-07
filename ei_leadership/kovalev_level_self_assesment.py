"""
Скрипт для обработки результатов теста уровень самооценки Ковалева
"""


import pandas as pd
import re
from tkinter import messagebox
from lachesis_support_functions import round_mean,create_union_svod


class BadOrderUSK(Exception):
    """
    Исключение для обработки случая когда колонки не совпадают
    """
    pass


class BadValueUSK(Exception):
    """
    Исключение для неправильных значений в вариантах ответов
    """
    pass

class BadCountColumnsUSK(Exception):
    """
    Исключение для обработки случая если количество колонок не равно 32
    """
    pass



def calc_value_usk(row):
    """
    Функция для подсчета значения уровня самооценки Ковалева
    :param row: строка с ответами
    :return: число
    """
    sum_row = sum(row) # получаем сумму
    return sum_row

def calc_level_usk(value):
    """
    Функция для подсчета уровня самооценки
    :param value:
    :return:
    """
    if 0 <= value <= 25:
        return 'высокий уровень самооценки'
    elif 26 <= value <= 45:
        return 'средний уровень самооценки'
    elif 46 <= value <= 128:
        return 'низкий уровень самооценки'


def calc_count_level(df:pd.DataFrame, lst_cat:list, val_cat, col_cat, lst_cols:list):
    """
    Функция для создания сводных датафреймов по субшкалам

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
    count_df['% низкий уровень самооценки от общего'] = round(
        count_df['низкий уровень самооценки'] / count_df['Итого'], 2) * 100
    count_df['% средний уровень самооценки от общего'] = round(
        count_df['средний уровень самооценки'] / count_df['Итого'], 2) * 100
    count_df['% высокий уровень самооценки от общего'] = round(
        count_df['высокий уровень самооценки'] / count_df['Итого'], 2) * 100

    return count_df



def create_result_usk(base_df:pd.DataFrame, out_dct:dict, lst_svod_cols:list):
    """
    Функция для подсчета результата если указаны колонки по которым нужно провести свод
    :param df: датафрейм с результатами
    :param out_dct: словарь с уже подсчитанными базовыми данными
    :param lst_svod_cols: список сводных колонок
    :return: словарь
    """
    lst_reindex_main_level_cols = lst_svod_cols.copy()
    lst_reindex_main_level_cols.extend( ['низкий уровень самооценки', 'средний уровень самооценки', 'высокий уровень самооценки',
                                   'Итого'])  # Основная шкала

    svod_count_one_level_usk_df = calc_count_level(base_df, lst_svod_cols,
                                                      'Значение_уровня_самооценки',
                                                      'Уровень_самооценки',
                                                  lst_reindex_main_level_cols)

    # Считаем среднее по субшкалам
    svod_mean_one_df = pd.pivot_table(base_df,
                                      index=lst_svod_cols,
                                      values=['Значение_уровня_самооценки',
                                              ],
                                      aggfunc=round_mean)
    svod_mean_one_df.reset_index(inplace=True)
    # упорядочиваем колонки
    new_order_cols = lst_svod_cols.copy()
    new_order_cols.extend((['Значение_уровня_самооценки',
                            ]))
    svod_mean_one_df = svod_mean_one_df.reindex(columns=new_order_cols)

    dct_rename_cols_mean = {'Значение_уровня_самооценки': 'Среднее уровня самооценки',
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
                    f'Свод {out_name}': svod_count_one_level_usk_df,
                    })

    if len(lst_svod_cols) == 1:
        return out_dct

    else:
        for idx, name_column in enumerate(lst_svod_cols):
            lst_reindex_main_column_cols = [lst_svod_cols[idx], 'низкий уровень самооценки', 'средний уровень самооценки', 'высокий уровень самооценки',
                                            'Итого']

            svod_count_column_level_usk_df = calc_count_level(base_df, lst_svod_cols[idx],
                                                           'Значение_уровня_самооценки',
                                                           'Уровень_самооценки',
                                                           lst_reindex_main_column_cols)

            # Считаем среднее по субшкалам
            svod_mean_column_df = pd.pivot_table(base_df,
                                              index=lst_svod_cols,
                                              values=['Значение_уровня_самооценки',
                                                      ],
                                              aggfunc=round_mean)
            svod_mean_column_df.reset_index(inplace=True)
            # упорядочиваем колонки
            new_order_cols = [lst_svod_cols[idx]].copy()

            new_order_cols.extend((['Значение_уровня_самооценки',
                                    ]))
            svod_mean_column_df = svod_mean_column_df.reindex(columns=new_order_cols)

            dct_rename_cols_mean = {'Значение_уровня_самооценки': 'Среднее уровня самооценки',
                                    }
            svod_mean_column_df.rename(columns=dct_rename_cols_mean, inplace=True)

            name_column = lst_svod_cols[idx]
            name_column = re.sub(r'[\[\]\'+()<> :"?*|\\/]', '_', name_column)
            name_column = name_column[:15]

            out_dct.update({f'Ср {name_column}': svod_mean_column_df,
                            f'Свод {name_column}': svod_count_column_level_usk_df,
                            })
        return out_dct












def processing_usk(result_df: pd.DataFrame, answers_df: pd.DataFrame, lst_svod_cols:list):
    """
    Функция для обработки
    :param result_df: часть датафрейма с описательными колонками
    :param answers_df: часть датафрейма с ответами
    :param lst_svod_cols:  список с колонками по которым нужно делать свод
    """
    try:
        out_answer_df = result_df.copy()  # делаем копию для последующего соединения с сырыми ответами
        if len(answers_df.columns) != 32:  # проверяем количество колонок с вопросами
            raise BadCountColumnsUSK

        # очищаем названия колонок от возможных сочетаний .1 которые добавляет пандас при одинаковых колонках
        clean_df_lst = []
        for name_column in answers_df.columns:
            clean_name = re.sub(r'.\d+$', '', name_column)
            clean_df_lst.append(clean_name)

        answers_df.columns = clean_df_lst

        # Словарь с проверочными данными
        lst_check_cols = ['Мне хочется, чтобы мои друзья подбадривали меня',
                          'Постоянно чувствую свою ответственность за работу (учебу)',
                          'Я беспокоюсь о своем будущем',
                          'Многие меня ненавидят',
                          'Я обладаю меньшей инициативой, нежели другие',
                          'Я беспокоюсь за свое психическое состояние',
                          'Я боюсь выглядеть глупцом',
                          'Внешний вид других куда лучше, чем мой',
                          'Я боюсь выступать с речью перед незнакомыми людьми',
                          'Я часто допускаю ошибки',
                          'Как жаль, что я не умею говорить, как следует с людьми',
                          'Как жаль, что мне не хватает уверенности в себе',
                          'Мне бы хотелось, чтобы мои действия ободрялись другими чаще',
                          'Я слишком скромен',
                          'Моя жизнь бесполезна',
                          'Многие неправильного мнения обо мне',
                          'Мне не с кем поделиться своими мыслями',
                          'Люди ждут от меня многого',
                          'Люди не особенно интересуются моими достижениями',
                          'Я слегка смущаюсь',
                          'Я чувствую, что многие люди не понимают меня',
                          'Я не чувствую себя в безопасности',
                          'Я часто понапрасну волнуюсь',
                          'Я чувствую себя неловко, когда вхожу в комнату, где уже сидят люди',
                          'Я чувствую себя скованным',
                          'Я чувствую, что люди говорят обо мне за моей спиной',
                          'Я уверен, что люди почти все принимают легче, чем я',
                          'Мне кажется, что со мной должна случиться какая-нибудь неприятность',
                          'Меня волнует мысль о том, как люди относятся ко мне',
                          'Как жаль, что я не так общителен',
                          'В спорах я высказываюсь только тогда, когда уверен в своей правоте',
                          'Я думаю о том, чего ждут от меня люди',

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
            raise BadOrderUSK

        # словарь для замены слов на числа
        dct_replace_value = {'никогда': 0,
                             'редко': 1,
                             'иногда': 2,
                             'часто': 3,
                             'очень часто': 4}

        valid_values = [0, 1, 2, 3, 4]
        answers_df.replace(dct_replace_value, inplace=True)  # заменяем слова на цифры для подсчетов

        # Проверяем, есть ли значения, отличающиеся от указанных в списке
        lst_error_answers = []  # список для хранения строк где найдены неправильные ответы

        for i in range(32):
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
            raise BadValueUSK

        base_df = pd.DataFrame()
        # Проводим подсчет
        base_df['Значение_уровня_самооценки'] = answers_df.apply(calc_value_usk, axis=1)
        base_df['Норма_уровня_самооценки'] = '0-45 баллов'
        base_df['Уровень_самооценки'] = base_df['Значение_уровня_самооценки'].apply(calc_level_usk)

        # Создаем датафрейм для создания части в общий датафрейм
        part_df = pd.DataFrame()
        part_df['УСК_Самооценка_Значение'] = base_df['Значение_уровня_самооценки']
        part_df['УСК_Самооценка_Уровень'] = base_df['Уровень_самооценки']

        out_answer_df = pd.concat([out_answer_df, answers_df], axis=1)  # Датафрейм для проверки

        # Соединяем анкетную часть с результатной
        base_df = pd.concat([result_df, base_df], axis=1)
        base_df.sort_values(by='Значение_уровня_самооценки', ascending=False, inplace=True)  # сортируем

        # формируем основной словарь
        out_dct = {'Списочный результат': base_df, 'Список для проверки': out_answer_df,
                   }

        # Делаем свод по интегральным показателям
        dct_svod_integral = {'Значение_уровня_самооценки': 'Уровень_самооценки',
                             }

        dct_rename_svod_integral = {'Значение_уровня_самооценки': 'Уровень самооценки',
                                    }

        lst_integral = ['низкий уровень самооценки', 'средний уровень самооценки', 'высокий уровень самооценки',
                        ]

        base_svod_integral_df = create_union_svod(base_df, dct_svod_integral, dct_rename_svod_integral, lst_integral)

        # считаем среднее
        avg_self_as = round(base_df['Значение_уровня_самооценки'].mean(), 2)

        avg_dct = {'Среднее значение уровня самооценки ': avg_self_as,

                   }

        avg_df = pd.DataFrame.from_dict(avg_dct, orient='index')
        avg_df = avg_df.reset_index()
        avg_df.columns = ['Показатель', 'Среднее значение']

        out_dct.update({'Свод': base_svod_integral_df,
                        'Среднее': avg_df}
                       )

        # Создаем листы со списками общему интеллекту
        dct_level = dict()
        for level in lst_integral:
            temp_df = base_df[base_df['Уровень_самооценки'] == level]
            if temp_df.shape[0] != 0:
                dct_level[level] = temp_df

        out_dct.update(dct_level)

        """
                    Сохраняем в зависимости от необходимости делать своды по определенным колонкам
                    """
        if len(lst_svod_cols) == 0:
            return out_dct, part_df
        else:
            out_dct = create_result_usk(base_df, out_dct, lst_svod_cols)

            return out_dct, part_df


    except BadOrderUSK:
        messagebox.showerror('Лахеcис',
                             f'При обработке вопросов теста Уровень самооценки Ковалев обнаружены неправильные вопросы. Проверьте названия колонок с вопросами:\n'
                             f'{error_order_message}\n'
                             f'Используйте при создании Яндекс-формы написание вопросов из руководства пользователя программы Лахесис.')
    except BadValueUSK:
        messagebox.showerror('Лахеcис',
                             f'При обработке вопросов теста Уровень самооценки Ковалев обнаружены неправильные варианты ответов. Проверьте ответы на указанных строках:\n'
                             f'{error_message}\n'
                             f'Используйте при создании Яндекс-формы написание вариантов ответа из руководства пользователя программы Лахесис.')

    except BadCountColumnsUSK:
        messagebox.showerror('Лахеcис',
                             f'Проверьте количество колонок с ответами на тест Уровень самооценки Ковалев\n'
                             f'Должно быть 32 колонки с вопросами'
                             )



