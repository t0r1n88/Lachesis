"""
Скрипт для обработки результатов Опросник по выявлению рисков буллинга в образовательной среде для обучающихся 5-11 классов НИЦМП
"""

import pandas as pd
import re
from tkinter import messagebox
from lachesis_support_functions import round_mean_two,calc_count_scale,create_union_svod, create_list_on_level

class BadOrderOVRBN(Exception):
    """
    Исключение для обработки случая когда колонки не совпадают
    """
    pass


class BadValueOVRBN(Exception):
    """
    Исключение для неправильных значений в вариантах ответов
    """
    pass

class BadCountColumnsOVRBN(Exception):
    """
    Исключение для обработки случая если количество колонок не равно 17
    """
    pass


def calc_value(row):
    """
    Фнукция подсчета значения
    :param row:
    :return:
    """
    value = 0 # сумматор

    # 1
    if row[0] == 'Никогда':
        value += 0
    elif row[0] == 'Редко (раз в месяц или реже)':
        value += 1
    elif row[0] == 'Иногда (раз в неделю)':
        value += 2
    else:
        value +=3

    # 2
    if row[1] == 'Такого не бывает':
        value += 0
    elif row[1] == 'Бывает, но редко':
        value += 1
    elif row[1] == 'Бывает иногда':
        value += 2
    else:
        value += 3

    # 3
    if row[2] == 'Нет, такого не бывает':
        value += 0
    elif row[2] == 'Бывает, но очень редко':
        value += 1
    elif row[2] == 'Бывает время от времени':
        value += 2
    else:
        value += 3

    # 4
    if row[3] == 'Нет таких учеников':
        value += 0
    elif row[3] == 'Есть один такой ученик':
        value += 1
    elif row[3] == 'Есть несколько таких учеников':
        value += 2
    else:
        value += 3

    # 5
    if row[4] == 'Никогда':
        value += 0
    elif row[4] == 'Редко (раз в месяц или реже)':
        value += 1
    elif row[4] == 'Иногда (раз в неделю)':
        value += 2
    else:
        value += 3

    # 6
    if row[5] == 'Нет, такого не бывает':
        value += 0
    elif row[5] == 'Бывает, но редко':
        value += 1
    elif row[5] == 'Бывает иногда':
        value += 2
    else:
        value += 3

    # 7
    if row[6] == 'Нет, таких учеников нет':
        value += 0
    elif row[6] == 'Есть один такой ученик':
        value += 1
    elif row[6] == 'Есть несколько таких учеников':
        value += 2
    else:
        value += 3

    # 8
    if row[7] == 'Никогда':
        value += 0
    elif row[7] == 'Редко (раз в месяц или реже)':
        value += 1
    elif row[7] == 'Иногда (раз в неделю)':
        value += 2
    else:
        value += 3

    # 9
    if row[8] == 'Всегда, когда это нужно':
        value += 0
    elif row[8] == 'Часто':
        value += 1
    elif row[8] == 'Иногда':
        value += 2
    else:
        value += 3

    # 10
    if row[9] == 'Да, все знают':
        value += 0
    elif row[9] == 'Большинство знает':
        value += 1
    elif row[9] == 'Немногие знают':
        value += 2
    else:
        value += 3

    # 11
    if row[10] == 'Очень дружелюбная':
        value += 0
    elif row[10] == 'В целом хорошая':
        value += 1
    elif row[10] == 'Бывает по-разному':
        value += 2
    else:
        value += 3

    # 12
    if row[11] == 'Очень высокий, все всегда готовы помочь друг другу':
        value += 0
    elif row[11] == 'Средний, помощь оказывается, но не всегда':
        value += 1
    elif row[11] == 'Низкий, каждый сам за себя':
        value += 2
    else:
        value += 3

    # 13
    if row[12] == 'Очень открыто, эти темы регулярно обсуждаются':
        value += 0
    elif row[12] == 'Иногда обсуждаются, но не очень глубоко':
        value += 1
    elif row[12] == 'Редко, эти темы считаются табу':
        value += 2
    else:
        value += 3

    # 14
    if row[13] == 'Никогда':
        value += 0
    elif row[13] == 'Редко (раз в месяц или реже)':
        value += 1
    elif row[13] == 'Иногда (раз в неделю)':
        value += 2
    else:
        value += 3

    # 15
    if row[14] == 'Никогда':
        value += 0
    elif row[14] == 'Не обращаю на такие вещи внимания':
        value += 1
    elif row[14] == 'Видел пару раз':
        value += 2
    else:
        value += 3

    # 16
    if row[15] == 'Учителя активно участвуют и эффективно решают проблемы':
        value += 0
    elif row[15] == 'Учителя пытаются помочь, но не всегда эффективно':
        value += 1
    elif row[15] == 'Учителя редко вмешиваются в конфликты между учениками':
        value += 2
    else:
        value += 3

    # 17
    if row[16] == 'Очень комфортно, я всегда свободно выражаю свое мнение':
        value += 0
    elif row[16] == 'В целом комфортно, но иногда я сомневаюсь':
        value += 1
    elif row[16] == 'Не очень комфортно, я часто боюсь высказываться':
        value += 2
    else:
        value += 3


    return value



def calc_level(value):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """
    if 0<= value <= 17:
        return f'низкий уровень риска'
    elif 18 <= value <= 34:
        return f'средний уровень риска'
    else:
        return f'высокий уровень риска'


def create_result_ovrb_nicmp(base_df:pd.DataFrame, out_dct:dict, lst_svod_cols:list):
    """
    Функция для подсчета результата если указаны колонки по которым нужно провести свод
    :param df: датафрейм с результатами
    :param out_dct: словарь с уже подсчитанными базовыми данными
    :param lst_svod_cols: список сводных колонок
    :return: словарь
    """
    lst_level = ['низкий уровень риска','средний уровень риска','высокий уровень риска']

    lst_reindex_one_level_cols = lst_svod_cols.copy()
    lst_reindex_one_level_cols.extend(['низкий уровень риска','средний уровень риска','высокий уровень риска',
                                       'Итого'])  # Основная шкала
    svod_count_one_level_vcha_df = calc_count_scale(base_df, lst_svod_cols,
                                                    'РБ_Значение',
                                                    'РБ_Уровень',
                                                    lst_reindex_one_level_cols, lst_level)

    # Считаем среднее по субшкалам
    svod_mean_one_df = pd.pivot_table(base_df,
                                      index=lst_svod_cols,
                                      values=[
                                              'РБ_Значение',
                                              ],
                                      aggfunc=round_mean_two)
    svod_mean_one_df.reset_index(inplace=True)

    # упорядочиваем колонки
    new_order_cols = lst_svod_cols.copy()
    new_order_cols.extend(([ 'РБ_Значение'
                            ]))
    svod_mean_one_df = svod_mean_one_df.reindex(columns=new_order_cols)

    dct_rename_cols_mean = {'РБ_Значение': 'Ср. риск буллинга',
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
                    f'РБ {out_name}': svod_count_one_level_vcha_df,
                    })

    if len(lst_svod_cols) == 1:
        return out_dct

    else:
        for idx, name_column in enumerate(lst_svod_cols):
            lst_reindex_column_level_cols = [lst_svod_cols[idx],'низкий уровень риска','средний уровень риска','высокий уровень риска',
                                                  'Итого']
            svod_count_column_level_vcha_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                               'РБ_Значение',
                                                               'РБ_Уровень',
                                                               lst_reindex_column_level_cols, lst_level)

            # Считаем среднее по субшкалам
            svod_mean_column_df = pd.pivot_table(base_df,
                                                 index=[lst_svod_cols[idx]],
                                                 values=[
                                                     'РБ_Значение',
                                                 ],
                                                 aggfunc=round_mean_two)
            svod_mean_column_df.reset_index(inplace=True)

            # упорядочиваем колонки
            new_order_cols = [lst_svod_cols[idx]].copy()
            new_order_cols.extend((['РБ_Значение'
                                    ]))
            svod_mean_column_df = svod_mean_column_df.reindex(columns=new_order_cols)

            dct_rename_cols_mean = {'РБ_Значение': 'Ср. риск буллинга',
                                    }
            svod_mean_column_df.rename(columns=dct_rename_cols_mean, inplace=True)
            # Готовим наименование
            name_column = lst_svod_cols[idx]
            name_column = re.sub(r'[\[\]\'+()<> :"?*|\\/]', '_', name_column)
            name_column = name_column[:15]
            out_dct.update({f'Ср {name_column}': svod_mean_column_df,
                            f'РБ {name_column}': svod_count_column_level_vcha_df,
                            })
        return out_dct






def processing_school_ovrb_nicmp(base_df: pd.DataFrame, answers_df: pd.DataFrame, lst_svod_cols:list):
    """
    Функция для обработки
    :param base_df: часть датафрейма с описательными колонками
    :param answers_df: часть датафрейма с ответами
    :param lst_svod_cols:  список с колонками по которым нужно делать свод
    """
    try:
        out_answer_df = base_df.copy()  # делаем копию для последующего соединения с сырыми ответами
        if len(answers_df.columns) != 17:  # проверяем количество колонок с вопросами
            raise BadCountColumnsOVRBN

        # очищаем названия колонок от возможных сочетаний .1 которые добавляет пандас при одинаковых колонках
        clean_df_lst = []
        for name_column in answers_df.columns:
            clean_name = re.sub(r'.\d+$', '', name_column)
            clean_df_lst.append(clean_name)

        answers_df.columns = clean_df_lst
        lst_check_cols = ['Как часто в вашем классе кто-то обзывает или дразнит других учеников?',
                          'Бывает ли, что кого-то из одноклассников, намеренно не принимают в общие дела?',
                          'Случается ли, что кто-то из учеников забирает или портит вещи одноклассников?',
                          'Есть ли в классе ученики, которых другие боятся?',
                          'Как часто в вашем классе происходят драки или толкание?',
                          'Распространяют ли ученики вашего класса слухи или сплетни друг о друге?',
                          'Есть ли в вашем классе ученики, которые всегда остаются одни, с которыми никто не общается?',
                          'Насколько часто ученики вашего класса сталкиваются с кибербуллингом (оскорблениями, угрозами или распространением слухов в интернете)?',
                          'Как часто в вашем классе кто-то встает на защиту тех, кого обижают?',
                          'Знают ли ученики вашего класса, к кому обратиться в школе, если кого-то обижают?',

                          'Как бы вы оценили общую атмосферу в вашем классе?',
                          'Как вы оцениваете уровень взаимопомощи между учениками в вашем классе?',
                          'Насколько открыто в вашем классе обсуждаются проблемы отношений между учениками?',
                          'Случаются ли в вашей школе конфликты и драки между учащимися?',
                          'Замечали ли вы, что кого-то из учащихся вашей школы публично оскорбляли и унижали?',
                          'Как вы оцениваете роль учителей в предотвращении и разрешении конфликтов между учениками?',
                          'Насколько комфортно вы чувствуете себя, выражая свое мнение в классе, даже если оно отличается от мнения большинства?',
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
            raise BadOrderOVRBN


        valid_values = [['Никогда','Редко (раз в месяц или реже)','Иногда (раз в неделю)','Часто (почти каждый день)'],
                        ['Такого не бывает','Бывает, но редко','Бывает иногда','Бывает часто'],
                        ['Нет, такого не бывает','Бывает, но очень редко','Бывает время от времени','Да, это частое явление'],
                        ['Нет таких учеников','Есть один такой ученик','Есть несколько таких учеников','Многие ученики кого-то боятся'],
                        ['Никогда','Редко (раз в месяц или реже)','Иногда (раз в неделю)','Часто (почти каждый день)'],

                        ['Нет, такого не бывает','Бывает, но редко','Бывает иногда','Да, это происходит часто'],
                        ['Нет, таких учеников нет','Есть один такой ученик','Есть несколько таких учеников','Да, многие ученики остаются одни'],
                        ['Никогда','Редко (раз в месяц или реже)','Иногда (раз в неделю)','Часто (почти каждый день)'],
                        ['Всегда, когда это нужно','Часто','Иногда','Редко или никогда'],
                        ['Да, все знают','Большинство знает','Немногие знают','Никто не знает'],

                        ['Очень дружелюбная','В целом хорошая','Бывает по-разному','Часто напряженная или недружелюбная'],
                        ['Очень высокий, все всегда готовы помочь друг другу','Средний, помощь оказывается, но не всегда','Низкий, каждый сам за себя','Очень низкий, все друг против друга'],
                        ['Очень открыто, эти темы регулярно обсуждаются','Иногда обсуждаются, но не очень глубоко','Редко, эти темы считаются табу','Никогда не обсуждаются'],
                        ['Никогда','Редко (раз в месяц или реже)','Иногда (раз в неделю)','Часто (почти каждый день)'],
                        ['Никогда','Не обращаю на такие вещи внимания','Видел пару раз','Да, такое происходит часто'],

                        ['Учителя активно участвуют и эффективно решают проблемы','Учителя пытаются помочь, но не всегда эффективно',
                         'Учителя редко вмешиваются в конфликты между учениками','Учителя игнорируют проблемы между учениками'],
                        ['Очень комфортно, я всегда свободно выражаю свое мнение','В целом комфортно, но иногда я сомневаюсь',
                         'Не очень комфортно, я часто боюсь высказываться','Совсем некомфортно, я никогда не высказываю свое мнение']
                        ]

        lst_error_answers = []  # список для хранения строк где найдены неправильные ответы

        for idx, lst_values in enumerate(valid_values):
            mask = ~answers_df.iloc[:, idx].isin(lst_values)  # проверяем на допустимые значения
            # Получаем строки с отличающимися значениями
            result_check = answers_df.iloc[:, idx][mask]

            if len(result_check) != 0:
                error_row = list(map(lambda x: x + 2, result_check.index))
                error_row = list(map(str, error_row))
                error_row_lst = [f'В {idx + 1} вопросной колонке на строке {value}' for value in error_row]
                error_in_column = ','.join(error_row_lst)
                lst_error_answers.append(error_in_column)

        if len(lst_error_answers) != 0:
            error_message = ';'.join(lst_error_answers)
            raise BadValueOVRBN

        base_df['РБ_Значение'] = answers_df.apply(calc_value, axis=1)
        base_df['РБ_Уровень'] = base_df['РБ_Значение'].apply(calc_level)

        # Создаем датафрейм для создания части в общий датафрейм
        part_df = pd.DataFrame()

        # Основные шкалы

        part_df['ОВРБ_Значение'] = base_df['РБ_Значение']
        part_df['ОВРБ_Уровень'] = base_df['РБ_Уровень']

        out_answer_df = pd.concat([out_answer_df, answers_df], axis=1)  # Датафрейм для проверки
        base_df.sort_values(by='РБ_Значение', ascending=False, inplace=True)  # сортируем

        # Делаем свод  по  шкалам
        dct_svod_sub = {'РБ_Значение': 'РБ_Уровень',
                        }

        dct_rename_svod_sub = {
            'РБ_Значение': 'Уровень риска буллинга',
        }

        lst_sub = ['низкий уровень риска','средний уровень риска','высокий уровень риска']

        base_svod_sub_df = create_union_svod(base_df, dct_svod_sub, dct_rename_svod_sub, lst_sub)

        avg_psp = round(base_df['РБ_Значение'].mean(), 2)

        avg_dct = {'Среднее значение риска буллинга': avg_psp,
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

        dct_prefix = {'РБ_Уровень': 'РБ',
                      }

        out_dct = create_list_on_level(base_df, out_dct, lst_sub, dct_prefix)

        """
                                Сохраняем в зависимости от необходимости делать своды по определенным колонкам
                                """
        if len(lst_svod_cols) == 0:
            return out_dct, part_df

        else:
            out_dct = create_result_ovrb_nicmp(base_df, out_dct, lst_svod_cols)
            return out_dct, part_df


    except BadOrderOVRBN:
        messagebox.showerror('Лахеcис',
                             f'При обработке вопросов тестаОпросник по выявлению рисков буллинга в образовательной среде для обучающихся 5-11 классов НИЦМП обнаружены неправильные вопросы. Проверьте названия колонок с вопросами:\n'
                             f'{error_order_message[:5000]}\n'
                             f'Используйте при создании Яндекс-формы написание вопросов из руководства пользователя программы Лахесис.')
    except BadValueOVRBN:
        messagebox.showerror('Лахеcис',
                             f'При обработке вопросов теста Опросник по выявлению рисков буллинга в образовательной среде для обучающихся 5-11 классов НИЦМП обнаружены неправильные варианты ответов. Проверьте ответы на указанных строках:\n'
                             f'{error_message[:5000]}\n'
                             f'Используйте при создании Яндекс-формы написание вариантов ответа из руководства пользователя программы Лахесис.')


    except BadCountColumnsOVRBN:
        messagebox.showerror('Лахеcис',
                             f'Проверьте количество колонок с ответами на тест Опросник по выявлению рисков буллинга в образовательной среде для обучающихся 5-11 классов НИЦМП\n'
                             f'Должно быть 17 колонок с ответами')






