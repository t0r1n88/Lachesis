"""
Скрипт для обработки результатов Социально-психологическая самоаттестация коллектива (школьный вариант) Р.С. Немов
"""

import pandas as pd
import re
from tkinter import messagebox
from lachesis_support_functions import round_mean_two,calc_count_scale,create_union_svod, create_list_on_level

class BadOrderSPSKNSH(Exception):
    """
    Исключение для обработки случая когда колонки не совпадают
    """
    pass


class BadValueSPSKNSH(Exception):
    """
    Исключение для неправильных значений в вариантах ответов
    """
    pass

class BadCountColumnsSPSKNSH(Exception):
    """
    Исключение для обработки случая если количество колонок не равно 28
    """
    pass


def calc_level(value):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """

    if 3<= value:
        return f'высокий уровень ЭО'
    elif 2 <= value < 3:
        return f'средний уровень ЭО'
    else:
        return f'низкий уровень ЭО'

def create_result_school_spsk_nemov(base_df:pd.DataFrame, out_dct:dict, lst_svod_cols:list):
    """
    Функция для подсчета результата если указаны колонки по которым нужно провести свод
    :param df: датафрейм с результатами
    :param out_dct: словарь с уже подсчитанными базовыми данными
    :param lst_svod_cols: список сводных колонок
    :return: словарь
    """
    lst_level = ['высокий уровень ЭО', 'средний уровень ЭО', 'низкий уровень ЭО']

    lst_reindex_one_level_cols = lst_svod_cols.copy()
    lst_reindex_one_level_cols.extend(['высокий уровень ЭО', 'средний уровень ЭО', 'низкий уровень ЭО',
                                       'Итого'])  # Основная шкала
    svod_count_one_level_vcha_df = calc_count_scale(base_df, lst_svod_cols,
                                                    'ЭО_Значение',
                                                    'ЭО_Уровень',
                                                    lst_reindex_one_level_cols, lst_level)

    # Считаем среднее по субшкалам
    svod_mean_one_df = pd.pivot_table(base_df,
                                      index=lst_svod_cols,
                                      values=[
                                          'ЭО_Значение',
                                      ],
                                      aggfunc=round_mean_two)
    svod_mean_one_df.reset_index(inplace=True)

    # упорядочиваем колонки
    new_order_cols = lst_svod_cols.copy()
    new_order_cols.extend((['ЭО_Значение'
                            ]))
    svod_mean_one_df = svod_mean_one_df.reindex(columns=new_order_cols)

    dct_rename_cols_mean = {'ЭО_Значение': 'Ср. эталонность общности',
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
                    f'ЭО {out_name}': svod_count_one_level_vcha_df,
                    })

    if len(lst_svod_cols) == 1:
        return out_dct
    else:
        for idx, name_column in enumerate(lst_svod_cols):
            lst_reindex_column_level_cols = [lst_svod_cols[idx],'высокий уровень ЭО', 'средний уровень ЭО', 'низкий уровень ЭО',
                                                  'Итого']
            svod_count_column_level_vcha_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                               'ЭО_Значение',
                                                               'ЭО_Уровень',
                                                               lst_reindex_column_level_cols, lst_level)

            # Считаем среднее по субшкалам
            svod_mean_column_df = pd.pivot_table(base_df,
                                                 index=[lst_svod_cols[idx]],
                                                 values=[
                                                     'ЭО_Значение',
                                                 ],
                                                 aggfunc=round_mean_two)
            svod_mean_column_df.reset_index(inplace=True)

            # упорядочиваем колонки
            new_order_cols = [lst_svod_cols[idx]].copy()
            new_order_cols.extend((['ЭО_Значение'
                                    ]))
            svod_mean_column_df = svod_mean_column_df.reindex(columns=new_order_cols)

            dct_rename_cols_mean = {'ЭО_Значение': 'Ср. эталонность общности',
                                    }
            svod_mean_column_df.rename(columns=dct_rename_cols_mean, inplace=True)
            # Готовим наименование
            name_column = lst_svod_cols[idx]
            name_column = re.sub(r'[\[\]\'+()<> :"?*|\\/]', '_', name_column)
            name_column = name_column[:15]
            out_dct.update({f'Ср {name_column}': svod_mean_column_df,
                            f'ЭО {name_column}': svod_count_column_level_vcha_df,
                            })
        return out_dct




def processing_school_spskn_nemov(base_df: pd.DataFrame, answers_df: pd.DataFrame, lst_svod_cols:list):
    """
    Функция для обработки
    :param base_df: часть датафрейма с описательными колонками
    :param answers_df: часть датафрейма с ответами
    :param lst_svod_cols:  список с колонками по которым нужно делать свод
    """
    try:
        out_answer_df = base_df.copy()  # делаем копию для последующего соединения с сырыми ответами
        if len(answers_df.columns) != 28:  # проверяем количество колонок с вопросами
            raise BadCountColumnsSPSKNSH

        # очищаем названия колонок от возможных сочетаний .1 которые добавляет пандас при одинаковых колонках
        clean_df_lst = []
        for name_column in answers_df.columns:
            clean_name = re.sub(r'.\d+$', '', name_column)
            clean_df_lst.append(clean_name)

        answers_df.columns = clean_df_lst

        lst_check_cols = ['Свои слова подтверждают делом',
                          'Все вопросы решают сообща',
                          'Правильно понимают трудности, стоящие перед классом',
                          'Радуются успехам товарищей',
                          'Помогают новичкам, ребятам из младших классов',
                          'Не ссорятся, когда распределяют обязанности',
                          'Знают задачи, стоящие перед классом',
                          'Требовательны к себе и другим',
                          'Личные интересы подчиняют интересам коллектива',
                          'Принципиально оценивают успехи коллектива',

                          'Искренне огорчаются при неудаче товарища',
                          'К своим ребятам и новичкам из других школ предъявляют одинаковые требования',
                          'Самостоятельно выявляют и исправляют недостатки в работе',
                          'Знают итоги работы коллектива',
                          'Сознательно подчиняются дисциплине',
                          'Не остаются равнодушными, если задеты интересы класса',
                          'Одинаково оценивают общие неудачи',
                          'Уважают друг друга',
                          'Радуются успеху новичков и ребят из других классов',
                          'Если надо, принимают на себя обязанности других членов коллектива',

                          'Хорошо знают, чем занимаются учащиеся других классов',
                          'По-хозяйски относятся к общественному добру',
                          'Поддерживают принятые в классе традиции',
                          'Одинаково оценивают справедливость наказаний',
                          'Поддерживают друг друга в трудные минуты',
                          'Не хвастаются перед ребятами из других школ и классов',
                          'Действуют слаженно и организованно в сложных ситуациях',
                          'Хорошо знают, как обстоят дела друг у друга'
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
            raise BadOrderSPSKNSH

        # словарь для замены слов на числа
        dct_replace_value = {'никто': 0,
                             'меньшинство': 1,
                             'половина': 2,
                             'большинство': 3,
                             'все': 4,
                             }
        valid_values = [0,1, 2, 3, 4]
        answers_df.replace(dct_replace_value, inplace=True)  # заменяем слова на цифры для подсчетов
        # Проверяем, есть ли значения, отличающиеся от указанных в списке
        lst_error_answers = []  # список для хранения строк где найдены неправильные ответы

        for i in range(28):
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
            raise BadValueSPSKNSH

        base_df['ИП_Значение'] = answers_df.sum(axis=1)
        base_df['ЭО_Значение'] = round(base_df['ИП_Значение'] / 28,1)
        base_df['ЭО_Уровень'] = base_df['ЭО_Значение'].apply(calc_level)

        # Создаем датафрейм для создания части в общий датафрейм
        part_df = pd.DataFrame()
        part_df['СПСКНШ_ИП_Значение'] = base_df['ИП_Значение']
        part_df['СПСКНШ_ЭО_Значение'] = base_df['ЭО_Значение']
        part_df['СПСКНШ_ЭО_Уровень'] = base_df['ЭО_Уровень']

        base_df.sort_values(by='ЭО_Значение', ascending=True, inplace=True)  # сортируем
        out_answer_df = pd.concat([out_answer_df, answers_df], axis=1)  # Датафрейм для проверки

        # Делаем свод  по  шкалам
        dct_svod_sub = {'ЭО_Значение': 'ЭО_Уровень',
                        }

        dct_rename_svod_sub = {
            'ЭО_Значение': 'Уровень эталонности общности',
        }

        lst_sub = ['высокий уровень ЭО', 'средний уровень ЭО', 'низкий уровень ЭО']

        base_svod_sub_df = create_union_svod(base_df, dct_svod_sub, dct_rename_svod_sub, lst_sub)

        avg_psp = round(base_df['ЭО_Значение'].mean(), 2)

        avg_dct = {'Среднее значение эталонности общности': avg_psp,
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

        dct_prefix = {'ЭО_Уровень': 'ЭО',
                      }

        out_dct = create_list_on_level(base_df, out_dct, lst_sub, dct_prefix)

        """
                                Сохраняем в зависимости от необходимости делать своды по определенным колонкам
                                """
        if len(lst_svod_cols) == 0:
            return out_dct, part_df

        else:
            out_dct = create_result_school_spsk_nemov(base_df, out_dct, lst_svod_cols)
            return out_dct, part_df


    except BadOrderSPSKNSH:
        messagebox.showerror('Лахеcис',
                             f'При обработке вопросов теста Социально-психологическая самоаттестация коллектива (школьный вариант) Р.С. Немов обнаружены неправильные вопросы. Проверьте названия колонок с вопросами:\n'
                             f'{error_order_message[:5000]}\n'
                             f'Используйте при создании Яндекс-формы написание вопросов из руководства пользователя программы Лахесис.')
    except BadValueSPSKNSH:
        messagebox.showerror('Лахеcис',
                             f'При обработке вопросов теста Социально-психологическая самоаттестация коллектива (школьный вариант) Р.С. Немов обнаружены неправильные варианты ответов. Проверьте ответы на указанных строках:\n'
                             f'{error_message[:5000]}\n'
                             f'Используйте при создании Яндекс-формы написание вариантов ответа из руководства пользователя программы Лахесис.')


    except BadCountColumnsSPSKNSH:
        messagebox.showerror('Лахеcис',
                             f'Проверьте количество колонок с ответами на тест Социально-психологическая самоаттестация коллектива (школьный вариант) Р.С. Немов\n'
                             f'Должно быть 28 колонок с ответами')





