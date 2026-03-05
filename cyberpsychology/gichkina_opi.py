"""
Скрипт для обработки результатов теста Опросник поведения в интернете А.Е. Жичкина
"""

import pandas as pd
import re
from tkinter import messagebox
from lachesis_support_functions import round_mean_two,calc_count_scale,create_union_svod, create_list_on_level

class BadOrderOPIG(Exception):
    """
    Исключение для обработки случая когда колонки не совпадают
    """
    pass


class BadValueOPIG(Exception):
    """
    Исключение для неправильных значений в вариантах ответов
    """
    pass

class BadCountColumnsOPIG(Exception):
    """
    Исключение для обработки случая если количество колонок не равно 21
    """
    pass


def calc_value_ad(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [1,3,7,11,15,17]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_pr:
            if idx == 1:
                if value == 'Я часто ищу новые сайты, на которых я ни разу не был(а)':
                    value_forward += 1
            elif idx == 3:
                if value == 'В Интернете я часто знакомлюсь первым':
                    value_forward += 1
            elif idx == 7:
                if value == 'Общаясь в Интернете, я часто предлагаю свою тему для обсуждения':
                    value_forward += 1
            elif idx == 11:
                if value == 'В большинстве случаев я принимаю участие в обсуждении какого-либо вопроса в Интернете':
                    value_forward += 1
            elif idx == 15:
                if value == 'Общаясь в Интернете, я обычно стремлюсь произвести определенное впечатление на окружающих':
                    value_forward += 1
            elif idx == 17:
                if value == 'Обычно я выхожу в Интернет, заранее зная, зачем и что я там буду делать':
                    value_forward += 1


    return value_forward


def calc_level_ad(value):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """
    if value <= 2:
        return f'низкий уровень'
    elif 3 <= value <= 4:
        return f'средний уровень'
    else:
        return f'высокий уровень'



def calc_value_ava(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [2,4,8,9,12,14,18,20]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_pr:
            if idx == 2:
                if value == 'Мне нравится, что в Интернете каждый может вести себя так, как считает нужным':
                    value_forward += 1
            elif idx == 4:
                if value == 'Мне интересно читать чужие сообщения там, где я обычно общаюсь':
                    value_forward += 1
            elif idx == 8:
                if value == 'Мне часто бывают интересны темы, которые обсуждают в Интернете другие люди':
                    value_forward += 1
            elif idx == 9:
                if value == 'Мне нравится, что Интернет дает возможность познакомиться с самыми разными людьми':
                    value_forward += 1
            elif idx == 12:
                if value == 'На мой взгляд, все способы общения в Интернете (чаты, ICQ, конференции, почта) по-своему хороши':
                    value_forward += 1
            elif idx == 14:
                if value == 'Мне нравится, что в Интернете все время что-то изменяется':
                    value_forward += 1
            elif idx == 18:
                if value == 'По-моему, в Интернете каждый может найти место, где ему было бы интересно общаться':
                    value_forward += 1
            elif idx == 20:
                if value == 'Мне нравится, что в Интернете можно создать персонажа, который отличается от меня в реальной жизни':
                    value_forward += 1


    return value_forward

def calc_level_ava(value):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """
    if value <= 4:
        return f'низкий уровень'
    elif 5 <= value <= 7:
        return f'средний уровень'
    else:
        return f'высокий уровень'



def calc_value_iz(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [5,6,10,13,16,19,21]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_pr:
            if idx == 5:
                if value == 'Когда мне грустно или одиноко, я обычно выхожу в Интернет':
                    value_forward += 1
            elif idx == 6:
                if value == 'Когда я провожу в Интернете меньше времени, чем обычно, я чувствую себя подавленно':
                    value_forward += 1
            elif idx == 10:
                if value == 'Я чувствую, что мое увлечение Интернетом мешает моей учебе, работе или отношениям с людьми вне Интернета':
                    value_forward += 1
            elif idx == 13:
                if value == 'Многие мои знакомые не знают, сколько времени я на самом деле провожу в Интернете':
                    value_forward += 1
            elif idx == 16:
                if value == 'Я часто пытаюсь уменьшить количество времени, которое я провожу в Интернете':
                    value_forward += 1
            elif idx == 19:
                if value == 'Когда я не в Интернете, я часто думаю о том, что там происходит':
                    value_forward += 1
            elif idx == 21:
                if value == 'Я предпочитаю общаться с людьми или искать информацию через Интернет, а не в реальной жизни':
                    value_forward += 1


    return value_forward

def calc_level_iz(value):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """
    if value == 0:
        return f'низкий уровень'
    elif 1 <= value <= 2:
        return f'средний уровень'
    else:
        return f'высокий уровень'



def create_list_on_level_opig(base_df:pd.DataFrame, out_dct:dict, lst_level:list, dct_prefix:dict):
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
                if level == 'низкий уровень':
                    level = 'низкий'
                elif level == 'средний уровень':
                    level = 'средний'
                else:
                    level = 'высокий'
                dct_level[f'{dct_prefix[key]}. {level}'] = temp_df
        out_dct.update(dct_level)

    return out_dct


def create_result_opi_gichkova(base_df:pd.DataFrame, out_dct:dict, lst_svod_cols:list):
    """
    Функция для подсчета результата если указаны колонки по которым нужно провести свод
    :param df: датафрейм с результатами
    :param out_dct: словарь с уже подсчитанными базовыми данными
    :param lst_svod_cols: список сводных колонок
    :return: словарь
    """
    lst_level = ['низкий уровень', 'средний уровень', 'высокий уровень']

    lst_reindex_one_level_cols = lst_svod_cols.copy()
    lst_reindex_one_level_cols.extend(['низкий уровень', 'средний уровень', 'высокий уровень',
                                       'Итого'])  # Основная шкала

    # АД
    svod_count_one_level_k_df = calc_count_scale(base_df, lst_svod_cols,
                                                 'АД_Значение',
                                                 'АД_Уровень',
                                                 lst_reindex_one_level_cols, lst_level)
    # АВА
    svod_count_one_level_d_df = calc_count_scale(base_df, lst_svod_cols,
                                                 'АВА_Значение',
                                                 'АВА_Уровень',
                                                 lst_reindex_one_level_cols, lst_level)
    # ИЗ
    svod_count_one_level_s_df = calc_count_scale(base_df, lst_svod_cols,
                                                 'ИЗ_Значение',
                                                 'ИЗ_Уровень',
                                                 lst_reindex_one_level_cols, lst_level)

    # Считаем среднее по субшкалам
    svod_mean_one_df = pd.pivot_table(base_df,
                                      index=lst_svod_cols,
                                      values=['АД_Значение',
                                              'АВА_Значение',
                                              'ИЗ_Значение',
                                              ],
                                      aggfunc=round_mean_two)
    svod_mean_one_df.reset_index(inplace=True)

    # упорядочиваем колонки
    new_order_cols = lst_svod_cols.copy()
    new_order_cols.extend((['АД_Значение',
                            'АВА_Значение',
                            'ИЗ_Значение',
                            ]))
    svod_mean_one_df = svod_mean_one_df.reindex(columns=new_order_cols)

    dct_rename_cols_mean = {'АД_Значение': 'Ср. Активность в действии',
                            'АВА_Значение': 'Ср. Активность в восприятии альтернатив',
                            'ИЗ_Значение': 'Ср. Интернет-зависимость',
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
                    f'АД {out_name}': svod_count_one_level_k_df,
                    f'АВА {out_name}': svod_count_one_level_d_df,
                    f'ИЗ {out_name}': svod_count_one_level_s_df,
                    })

    if len(lst_svod_cols) == 1:
        return out_dct
    else:
        for idx, name_column in enumerate(lst_svod_cols):
            lst_reindex_column_level_cols = [lst_svod_cols[idx], 'низкий уровень', 'средний уровень', 'высокий уровень',
                                             'Итого']

            # АД
            svod_count_column_level_k_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                         'АД_Значение',
                                                         'АД_Уровень',
                                                         lst_reindex_column_level_cols, lst_level)
            # АВА
            svod_count_column_level_d_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                         'АВА_Значение',
                                                         'АВА_Уровень',
                                                         lst_reindex_column_level_cols, lst_level)
            # ИЗ
            svod_count_column_level_s_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                         'ИЗ_Значение',
                                                         'ИЗ_Уровень',
                                                         lst_reindex_column_level_cols, lst_level)

            # Считаем среднее по субшкалам
            svod_mean_column_df = pd.pivot_table(base_df,
                                              index=[lst_svod_cols[idx]],
                                              values=['АД_Значение',
                                                      'АВА_Значение',
                                                      'ИЗ_Значение',
                                                      ],
                                              aggfunc=round_mean_two)
            svod_mean_column_df.reset_index(inplace=True)

            # упорядочиваем колонки
            new_order_cols = [lst_svod_cols[idx]].copy()
            new_order_cols.extend((['АД_Значение',
                                    'АВА_Значение',
                                    'ИЗ_Значение',
                                    ]))
            svod_mean_column_df = svod_mean_column_df.reindex(columns=new_order_cols)

            dct_rename_cols_mean = {'АД_Значение': 'Ср. Активность в действии',
                                    'АВА_Значение': 'Ср. Активность в восприятии альтернатив',
                                    'ИЗ_Значение': 'Ср. Интернет-зависимость',
                                    }
            svod_mean_column_df.rename(columns=dct_rename_cols_mean, inplace=True)
            # Готовим наименование
            name_column = lst_svod_cols[idx]
            name_column = re.sub(r'[\[\]\'+()<> :"?*|\\/]', '_', name_column)
            name_column = name_column[:15]
            out_dct.update({f'Ср {name_column}': svod_mean_column_df,
                            f'АД {name_column}': svod_count_column_level_k_df,
                            f'АВА {name_column}': svod_count_column_level_d_df,
                            f'ИЗ {name_column}': svod_count_column_level_s_df,
                            })
        return out_dct











def processing_opi_gichkina(base_df: pd.DataFrame, answers_df: pd.DataFrame,lst_svod_cols:list):
    """
    Функция для обработки
    :param result_df: часть датафрейма с описательными колонками
    :param answers_df: часть датафрейма с ответами
    :param lst_svod_cols:  список с колонками по которым нужно делать свод
    """
    try:
        out_answer_df = base_df.copy()  # делаем копию для последующего соединения с сырыми ответами
        if answers_df.shape[1] != 21:
            raise BadCountColumnsOPIG
        # Переименовываем колонки
        answers_df.columns = [f'Вопрос_ №{i}' for i in range(1, 22)]

        valid_values= [['Я часто ищу новые сайты, на которых я ни разу не был(а)','Я предпочитаю ходить на те сайты, которые давно мне известны'],
                       ['Мне нравится, что в Интернете каждый может вести себя так, как считает нужным','Мне не нравится, что в Интернете многие люди ведут себя как хотят'],
                       ['В Интернете я часто знакомлюсь первым','Инициатива знакомства в Интернете, как правило, принадлежит не мне'],
                       ['Мне интересно читать чужие сообщения там, где я обычно общаюсь','Чужие сообщения в Интернете не вызывают у меня интереса'],
                       ['Когда мне грустно или одиноко, я обычно выхожу в Интернет','Я не чувствую необходимости выйти в Интернет тогда, когда у меня плохое настроение'],
                       ['Когда я провожу в Интернете меньше времени, чем обычно, я чувствую себя подавленно','Мое эмоциональное состояние не зависит от того, сколько времени я провожу в Интернете'],
                       ['Общаясь в Интернете, я часто предлагаю свою тему для обсуждения','Обычно, общаясь в Интернете, я не предлагаю своей темы для обсуждения'],
                       ['Мне часто бывают интересны темы, которые обсуждают в Интернете другие люди','Я не особенно интересуюсь темами, которые в Интернете обсуждают другие люди'],
                       ['Мне нравится, что Интернет дает возможность познакомиться с самыми разными людьми','Возможность знакомиться через Интернет с разными людьми мало меня интересует'],
                       ['Я чувствую, что мое увлечение Интернетом мешает моей учебе, работе или отношениям с людьми вне Интернета','Использование Интернета не мешает моим отношениям с людьми, учебе или работе'],

                       ['В большинстве случаев я принимаю участие в обсуждении какого-либо вопроса в Интернете','Обычно в Интернете я сохраняю молчаливую позицию'],
                       ['На мой взгляд, все способы общения в Интернете (чаты, ICQ, конференции, почта) по-своему хороши','По-моему, среди способов общения в Интернете много ненужных'],
                       ['Многие мои знакомые не знают, сколько времени я на самом деле провожу в Интернете','Большинство моих знакомых знает, сколько времени я провожу в Интернете'],
                       ['Мне нравится, что в Интернете все время что-то изменяется','Мне, скорее, безразлично то, что Интернет все время меняется'],
                       ['Общаясь в Интернете, я обычно стремлюсь произвести определенное впечатление на окружающих','Общаясь в Интернете, я обычно не задумываюсь о том, какое впечатление я произвожу на окружающих'],
                       ['Я часто пытаюсь уменьшить количество времени, которое я провожу в Интернете','Я не пытаюсь уменьшить количество времени, которое я провожу в Интернете'],
                       ['Обычно я выхожу в Интернет, заранее зная, зачем и что я там буду делать','Я часто выхожу в Интернет без какой-либо определенной цели'],
                       ['По-моему, в Интернете каждый может найти место, где ему было бы интересно общаться','На мой взгляд, в Интернете далеко не каждый может найти место, где ему было бы интересно общаться'],
                       ['Когда я не в Интернете, я часто думаю о том, что там происходит','Когда я не в Интернете, я редко думаю о нем'],
                       ['Мне нравится, что в Интернете можно создать персонажа, который отличается от меня в реальной жизни','Меня мало интересует возможность создания виртуальных личностей'],
                       ['Я предпочитаю общаться с людьми или искать информацию через Интернет, а не в реальной жизни','Я далеко не всегда прибегаю к помощи Интернета, когда мне нужно найти информацию или пообщаться'],
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
            raise BadValueOPIG

        base_df['АД_Значение'] = answers_df.apply(calc_value_ad, axis=1)
        base_df['АД_Уровень'] = base_df['АД_Значение'].apply(calc_level_ad)

        base_df['АВА_Значение'] = answers_df.apply(calc_value_ava, axis=1)
        base_df['АВА_Уровень'] = base_df['АВА_Значение'].apply(calc_level_ava)

        base_df['ИЗ_Значение'] = answers_df.apply(calc_value_iz, axis=1)
        base_df['ИЗ_Уровень'] = base_df['ИЗ_Значение'].apply(calc_level_iz)

        # Создаем датафрейм для создания части в общий датафрейм
        part_df = pd.DataFrame()

        # Основные шкалы
        part_df['ОПИЖ_АД_Значение'] = base_df['АД_Значение']
        part_df['ОПИЖ_АД_Уровень'] = base_df['АД_Уровень']

        part_df['ОПИЖ_АВА_Значение'] = base_df['АВА_Значение']
        part_df['ОПИЖ_АВА_Уровень'] = base_df['АВА_Уровень']

        part_df['ОПИЖ_ИЗ_Значение'] = base_df['ИЗ_Значение']
        part_df['ОПИЖ_ИЗ_Уровень'] = base_df['ИЗ_Уровень']

        out_answer_df = pd.concat([out_answer_df, answers_df], axis=1)  # Датафрейм для проверки

        base_df.sort_values(by='ИЗ_Значение', ascending=False, inplace=True)  # сортируем

        # Делаем свод  по  шкалам
        dct_svod_sub = {'АД_Значение': 'АД_Уровень',
                        'АВА_Значение': 'АВА_Уровень',
                        'ИЗ_Значение': 'ИЗ_Уровень',
                        }

        dct_rename_svod_sub = {'АД_Значение': 'Активность в действии',
                               'АВА_Значение': 'Активность в восприятии альтернатив',
                               'ИЗ_Значение': 'Интернет зависимость',
                               }

        lst_sub = ['низкий уровень', 'средний уровень', 'высокий уровень']

        base_svod_sub_df = create_union_svod(base_df, dct_svod_sub, dct_rename_svod_sub, lst_sub)

        avg_vcha = round(base_df['АД_Значение'].mean(), 2)
        avg_o = round(base_df['АВА_Значение'].mean(), 2)
        avg_ruvs = round(base_df['ИЗ_Значение'].mean(), 2)


        avg_dct = {'Среднее значение шкалы Активность в действии': avg_vcha,
                   'Среднее значение шкалы Активность в восприятии альтернатив': avg_o,
                   'Среднее значение шкалы Интернет-зависимость': avg_ruvs,
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

        dct_prefix = {'АД_Уровень': 'АД',
                      'АВА_Уровень': 'АВА',
                      'ИЗ_Уровень': 'ИЗ',
                      }

        out_dct = create_list_on_level_opig(base_df, out_dct, lst_sub, dct_prefix)
        """
                        Сохраняем в зависимости от необходимости делать своды по определенным колонкам
                        """
        if len(lst_svod_cols) == 0:
            return out_dct, part_df

        else:
            out_dct = create_result_opi_gichkova(base_df, out_dct, lst_svod_cols)
            return out_dct, part_df

    except BadValueOPIG:
        messagebox.showerror('Лахеcис',
                             f'При обработке вопросов теста Опросник поведения в интернете Жичкина обнаружены неправильные варианты ответов. Проверьте ответы на указанных строках:\n'
                             f'{error_message[:5000]}\n'
                             f'Используйте при создании Яндекс-формы написание вариантов ответа из руководства пользователя программы Лахесис.')


    except BadCountColumnsOPIG:
        messagebox.showerror('Лахеcис',
                             f'Проверьте количество колонок с ответами на тест Опросник поведения в интернете Жичкина\n'
                             f'Должно быть 21 колонка с ответами')




