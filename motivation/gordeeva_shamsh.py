"""
Скрипт для обработки результатов Методика Шкалы академической мотивации школьников Гордеева, Сычев, Гижицкий, Гавриченкова
"""

import pandas as pd
import re
from tkinter import messagebox
from lachesis_support_functions import round_mean_two,calc_count_scale,create_union_svod, create_list_on_level

class BadOrderSHAMSHG(Exception):
    """
    Исключение для обработки случая когда колонки не совпадают
    """
    pass


class BadValueSHAMSHG(Exception):
    """
    Исключение для неправильных значений в вариантах ответов
    """
    pass

class BadCountColumnsSHAMSHG(Exception):
    """
    Исключение для обработки случая если количество колонок не равно 32
    """
    pass


def calc_level(value):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """
    if 1<= value <2:
        return f'1-1,99'
    elif 2 <= value <3:
        return f'2-2,99'
    elif 3 <= value < 4:
        return f'3-3,99'
    else:
        return '4-5'


def calc_value_pm(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [1,9,17,25]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_pr:
            value_forward += value


    return round(value_forward/4,2)

def calc_value_md(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [2,10,18,26]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_pr:
            value_forward += value


    return round(value_forward/4,2)


def calc_value_msr(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [3,11,19,27]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_pr:
            value_forward += value


    return round(value_forward/4,2)


def calc_value_msu(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [4,12,20,28]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_pr:
            value_forward += value


    return round(value_forward/4,2)


def calc_value_im(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [5,13,21,29]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_pr:
            value_forward += value


    return round(value_forward/4,2)

def calc_value_mur(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [6,14,22,30]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_pr:
            value_forward += value


    return round(value_forward/4,2)


def calc_value_am(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [7,15,23,31]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_pr:
            value_forward += value


    return round(value_forward/4,2)


def calc_value_a(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [8,16,24,32]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_pr:
            value_forward += value


    return round(value_forward/4,2)


def create_result_shamsh_gordeeva(base_df:pd.DataFrame, out_dct:dict, lst_svod_cols:list):
    """
    Функция для подсчета результата если указаны колонки по которым нужно провести свод
    :param df: датафрейм с результатами
    :param out_dct: словарь с уже подсчитанными базовыми данными
    :param lst_svod_cols: список сводных колонок
    :return: словарь
    """

    lst_level = ['1-1,99', '2-2,99', '3-3,99','4-5']

    lst_reindex_one_level_cols = lst_svod_cols.copy()
    lst_reindex_one_level_cols.extend(['1-1,99', '2-2,99', '3-3,99','4-5',
                                       'Итого'])  # Основная шкала

    # АД
    svod_count_one_level_pm_df = calc_count_scale(base_df, lst_svod_cols,
                                                 'ПМ_Значение',
                                                 'ПМ_Диапазон',
                                                 lst_reindex_one_level_cols, lst_level)
    # АВА
    svod_count_one_level_md_df = calc_count_scale(base_df, lst_svod_cols,
                                                 'МД_Значение',
                                                 'МД_Диапазон',
                                                 lst_reindex_one_level_cols, lst_level)

    # АД
    svod_count_one_level_msr_df = calc_count_scale(base_df, lst_svod_cols,
                                                 'МСР_Значение',
                                                 'МСР_Диапазон',
                                                 lst_reindex_one_level_cols, lst_level)
    # АВА
    svod_count_one_level_msu_df = calc_count_scale(base_df, lst_svod_cols,
                                                 'МСУ_Значение',
                                                 'МСУ_Диапазон',
                                                 lst_reindex_one_level_cols, lst_level)

    # АД
    svod_count_one_level_im_df = calc_count_scale(base_df, lst_svod_cols,
                                                 'ИМ_Значение',
                                                 'ИМ_Диапазон',
                                                 lst_reindex_one_level_cols, lst_level)
    # АВА
    svod_count_one_level_mur_df = calc_count_scale(base_df, lst_svod_cols,
                                                 'МУР_Значение',
                                                 'МУР_Диапазон',
                                                 lst_reindex_one_level_cols, lst_level)

    # АД
    svod_count_one_level_am_df = calc_count_scale(base_df, lst_svod_cols,
                                                 'ЭМ_Значение',
                                                 'ЭМ_Диапазон',
                                                 lst_reindex_one_level_cols, lst_level)
    # АВА
    svod_count_one_level_a_df = calc_count_scale(base_df, lst_svod_cols,
                                                 'АМ_Значение',
                                                 'АМ_Диапазон',
                                                 lst_reindex_one_level_cols, lst_level)

    # Считаем среднее по субшкалам
    svod_mean_one_df = pd.pivot_table(base_df,
                                      index=lst_svod_cols,
                                      values=['ПМ_Значение',
                                              'МД_Значение',
                                              'МСР_Значение',
                                              'МСУ_Значение',

                                              'ИМ_Значение',
                                              'МУР_Значение',
                                              'ЭМ_Значение',
                                              'АМ_Значение',
                                              ],
                                      aggfunc=round_mean_two)
    svod_mean_one_df.reset_index(inplace=True)

    # упорядочиваем колонки
    new_order_cols = lst_svod_cols.copy()
    new_order_cols.extend((['ПМ_Значение',
                            'МД_Значение',
                            'МСР_Значение',
                            'МСУ_Значение',

                            'ИМ_Значение',
                            'МУР_Значение',
                            'ЭМ_Значение',
                            'АМ_Значение',
                            ]))
    svod_mean_one_df = svod_mean_one_df.reindex(columns=new_order_cols)

    dct_rename_cols_mean = {'ПМ_Значение': 'Ср. Познавательная мотивация',
                            'МД_Значение': 'Ср. Мотивация достижения',
                            'МСР_Значение': 'Ср. Мотивация саморазвития',
                            'МСУ_Значение': 'Ср. Мотивация самоуважения',

                            'ИМ_Значение': 'Ср. Интроецированная мотивация',
                            'МУР_Значение': 'Ср. Мотивация уважения родителями',
                            'ЭМ_Значение': 'Ср. Экстернальная мотивация',
                            'АМ_Значение': 'Ср. Амотивация',
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
                    f'ПМ {out_name}': svod_count_one_level_pm_df,
                    f'МД {out_name}': svod_count_one_level_md_df,
                    f'МСР {out_name}': svod_count_one_level_msr_df,
                    f'МСУ {out_name}': svod_count_one_level_msu_df,

                    f'ИМ {out_name}': svod_count_one_level_im_df,
                    f'МУР {out_name}': svod_count_one_level_mur_df,
                    f'ЭМ {out_name}': svod_count_one_level_am_df,
                    f'АМ {out_name}': svod_count_one_level_a_df,
                    })

    if len(lst_svod_cols) == 1:
        return out_dct

    else:
        for idx, name_column in enumerate(lst_svod_cols):
            lst_reindex_column_level_cols = [lst_svod_cols[idx], '1-1,99', '2-2,99', '3-3,99', '4-5',
                                             'Итого']


            svod_count_column_level_pm_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                             'ПМ_Значение',
                                                             'ПМ_Диапазон',
                                                             lst_reindex_column_level_cols, lst_level)
            # АВА
            svod_count_column_level_md_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                             'МД_Значение',
                                                             'МД_Диапазон',
                                                             lst_reindex_column_level_cols, lst_level)

            # АД
            svod_count_column_level_msr_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                              'МСР_Значение',
                                                              'МСР_Диапазон',
                                                              lst_reindex_column_level_cols, lst_level)
            # АВА
            svod_count_column_level_msu_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                              'МСУ_Значение',
                                                              'МСУ_Диапазон',
                                                              lst_reindex_column_level_cols, lst_level)

            # АД
            svod_count_column_level_im_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                             'ИМ_Значение',
                                                             'ИМ_Диапазон',
                                                             lst_reindex_column_level_cols, lst_level)
            # АВА
            svod_count_column_level_mur_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                              'МУР_Значение',
                                                              'МУР_Диапазон',
                                                              lst_reindex_column_level_cols, lst_level)

            # АД
            svod_count_column_level_am_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                             'ЭМ_Значение',
                                                             'ЭМ_Диапазон',
                                                             lst_reindex_column_level_cols, lst_level)
            # АВА
            svod_count_column_level_a_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                            'АМ_Значение',
                                                            'АМ_Диапазон',
                                                            lst_reindex_column_level_cols, lst_level)

            # Считаем среднее по субшкалам
            svod_mean_column_df = pd.pivot_table(base_df,
                                                 index=[lst_svod_cols[idx]],
                                                 values=['ПМ_Значение',
                                                         'МД_Значение',
                                                         'МСР_Значение',
                                                         'МСУ_Значение',

                                                         'ИМ_Значение',
                                                         'МУР_Значение',
                                                         'ЭМ_Значение',
                                                         'АМ_Значение',
                                                         ],
                                                 aggfunc=round_mean_two)
            svod_mean_column_df.reset_index(inplace=True)

            # упорядочиваем колонки
            new_order_cols = [lst_svod_cols[idx]].copy()
            new_order_cols.extend((['ПМ_Значение',
                                    'МД_Значение',
                                    'МСР_Значение',
                                    'МСУ_Значение',

                                    'ИМ_Значение',
                                    'МУР_Значение',
                                    'ЭМ_Значение',
                                    'АМ_Значение',
                                    ]))
            svod_mean_column_df = svod_mean_column_df.reindex(columns=new_order_cols)

            dct_rename_cols_mean = {'ПМ_Значение': 'Ср. Познавательная мотивация',
                                    'МД_Значение': 'Ср. Мотивация достижения',
                                    'МСР_Значение': 'Ср. Мотивация саморазвития',
                                    'МСУ_Значение': 'Ср. Мотивация самоуважения',

                                    'ИМ_Значение': 'Ср. Интроецированная мотивация',
                                    'МУР_Значение': 'Ср. Мотивация уважения родителями',
                                    'ЭМ_Значение': 'Ср. Экстернальная мотивация',
                                    'АМ_Значение': 'Ср. Амотивация',
                                    }
            svod_mean_column_df.rename(columns=dct_rename_cols_mean, inplace=True)
            # Готовим наименование
            name_column = lst_svod_cols[idx]
            name_column = re.sub(r'[\[\]\'+()<> :"?*|\\/]', '_', name_column)
            name_column = name_column[:15]

            out_dct.update({f'Ср {name_column}': svod_mean_column_df,
                            f'ПМ {name_column}': svod_count_column_level_pm_df,
                            f'МД {name_column}': svod_count_column_level_md_df,
                            f'МСР {name_column}': svod_count_column_level_msr_df,
                            f'МСУ {name_column}': svod_count_column_level_msu_df,

                            f'ИМ {name_column}': svod_count_column_level_im_df,
                            f'МУР {name_column}': svod_count_column_level_mur_df,
                            f'ЭМ {name_column}': svod_count_column_level_am_df,
                            f'АМ {name_column}': svod_count_column_level_a_df,
                            })
        return out_dct



def create_itog_values(row):
    """
    Функция для создания строки с итоговым стеном
    :param row: строка с результатами
    :return:
    """
    lst_out = list(map(str,row))
    return '-'.join(lst_out)






def processing_shamsh_gor(base_df: pd.DataFrame, answers_df: pd.DataFrame, lst_svod_cols:list):
    """
    Функция для обработки
    :param base_df: часть датафрейма с описательными колонками
    :param answers_df: часть датафрейма с ответами
    :param lst_svod_cols:  список с колонками по которым нужно делать свод
    """
    try:
        union_base_df = base_df.copy()  # делаем копию анкетной части чтобы потом соединить ее с ответной частью
        quantity_cols_base_df = base_df.shape[1]  # количество колонок в анкетной части

        out_answer_df = base_df.copy()  # делаем копию для последующего соединения с сырыми ответами
        if len(answers_df.columns) != 32:  # проверяем количество колонок с вопросами
            raise BadCountColumnsSHAMSHG

        # очищаем названия колонок от возможных сочетаний .1 которые добавляет пандас при одинаковых колонках
        clean_df_lst = []
        for name_column in answers_df.columns:
            clean_name = re.sub(r'.\d+$', '', name_column)
            clean_df_lst.append(clean_name)

        answers_df.columns = clean_df_lst

        lst_check_cols = ['Мне интересно учиться',
                          'Учёба доставляет мне удовольствие, я люблю решать трудные задачи',
                          'Потому что я получаю удовольствие, превосходя самого себя в учебных достижениях',
                          'Потому что я хочу доказать самому себе, что я способен успешно учиться в школе',
                          'Потому что мне стыдно плохо учиться',
                          'Я проявляю старание в учебе, чтобы заслужить уважение родителей',
                          'У меня нет другого выбора, если я буду прогуливать, у меня будут проблемы',
                          'Честно говоря, не знаю, мне кажется, что я здесь просто теряю время',
                          'Мне нравится учиться, потому что это интересно',
                          'Я чувствую удовлетворение, когда нахожусь в процессе решениях сложных учебных задач',

                          'Учеба дает мне возможность почувствовать удовлетворение в моем совершенствовании',
                          'Потому что когда я хорошо учусь, я чувствую себя значимым человеком',
                          'Потому что совесть заставляет меня учиться',
                          'Потому что хочу оправдать ожидания своих родителей',
                          'Чтобы избежать проблем с родителями и проблем после окончания школы',
                          'Раньше я понимал, зачем учусь, а теперь не уверен, стоит ли продолжать',
                          'Мне просто нравится учиться и узнавать новое',
                          'Мне нравится решать трудные задачи и прикладывать интеллектуальные усилия',
                          'Ради удовольствия, которое приносит мне достижение новых успехов в учебе',
                          'Чтобы доказать самому себе, что я умный человек',

                          'Потому что учиться – это моя обязанность, которой я не могу пренебречь',
                          'Чтобы получать хорошие оценки и чтобы меня любили и ценили мои родители',
                          'Потому что близкие меня будут осуждать, если я стану плохо учиться',
                          'Ходить-то я хожу, но не уверен, что в этом есть смысл',
                          'Я действительно получаю удовольствие от изучения нового материала на занятиях',
                          'Я просто люблю учиться, решать сложные задачи и чувствовать себя компетентным',
                          'Мне приятно осознавать, как растет моя компетентность и мои знания',
                          'Потому что я хочу показать самому себе, что я могу быть успешным в учебе',
                          'Потому что я должен подходить более ответственно к учебе в выпускном классе',
                          'Я стараюсь хорошо учиться, чтобы показать родителям, на что я способен',
                          'У меня нет выбора, иначе я не смогу в будущем иметь достаточно обеспеченную жизнь',
                          'Хожу по привычке, зачем, откровенно говоря, точно не знаю'
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
            raise BadOrderSHAMSHG

        # словарь для замены слов на числа
        dct_replace_value = {'совсем не соответствует': 1,
                             'скорее не соответствует': 2,
                             'нечто среднее': 3,
                             'скорее соответствует': 4,
                             'вполне соответствует': 5,
                             }
        valid_values = [1, 2, 3, 4, 5]
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
            raise BadValueSHAMSHG

        base_df['ПМ_Значение'] = answers_df.apply(calc_value_pm, axis=1)
        base_df['ПМ_Диапазон'] = base_df['ПМ_Значение'].apply(calc_level)

        base_df['МД_Значение'] = answers_df.apply(calc_value_md, axis=1)
        base_df['МД_Диапазон'] = base_df['МД_Значение'].apply(calc_level)

        base_df['МСР_Значение'] = answers_df.apply(calc_value_msr, axis=1)
        base_df['МСР_Диапазон'] = base_df['МСР_Значение'].apply(calc_level)

        base_df['МСУ_Значение'] = answers_df.apply(calc_value_msu, axis=1)
        base_df['МСУ_Диапазон'] = base_df['МСУ_Значение'].apply(calc_level)

        base_df['ИМ_Значение'] = answers_df.apply(calc_value_im, axis=1)
        base_df['ИМ_Диапазон'] = base_df['ИМ_Значение'].apply(calc_level)

        base_df['МУР_Значение'] = answers_df.apply(calc_value_mur, axis=1)
        base_df['МУР_Диапазон'] = base_df['МУР_Значение'].apply(calc_level)

        base_df['ЭМ_Значение'] = answers_df.apply(calc_value_am, axis=1)
        base_df['ЭМ_Диапазон'] = base_df['ЭМ_Значение'].apply(calc_level)

        base_df['АМ_Значение'] = answers_df.apply(calc_value_a, axis=1)
        base_df['АМ_Диапазон'] = base_df['АМ_Значение'].apply(calc_level)

        result_df = base_df.iloc[:, quantity_cols_base_df:]  # отсекаем часть с результатами чтобы упорядочить
        lst_stens = [column for column in result_df.columns if 'Значение' in column]
        result_df['Итог'] = result_df[lst_stens].apply(create_itog_values, axis=1)
        new_order_lst = ['Итог',
                         'ПМ_Значение', 'МД_Значение', 'МСР_Значение', 'МСУ_Значение',
                         'ИМ_Значение', 'МУР_Значение', 'ЭМ_Значение', 'АМ_Значение',

                         'ПМ_Диапазон', 'МД_Диапазон', 'МСР_Диапазон', 'МСУ_Диапазон',
                         'ИМ_Диапазон', 'МУР_Диапазон', 'ЭМ_Диапазон', 'АМ_Диапазон'

                         ]
        result_df = result_df.reindex(columns=new_order_lst)  # изменяем порядок
        base_df = pd.concat([union_base_df, result_df], axis=1)  # соединяем и перезаписываем base_df




        # Создаем датафрейм для создания части в общий датафрейм
        part_df = pd.DataFrame()

        # Основные шкалы
        part_df['ШАМШГСГГ_Итог_Значение'] = base_df['Итог']

        part_df['ШАМШГСГГ_ПМ_Значение'] = base_df['ПМ_Значение']
        part_df['ШАМШГСГГ_МД_Значение'] = base_df['МД_Значение']
        part_df['ШАМШГСГГ_МСР_Значение'] = base_df['МСР_Значение']
        part_df['ШАМШГСГГ_МСУ_Значение'] = base_df['МСУ_Значение']

        part_df['ШАМШГСГГ_ИМ_Значение'] = base_df['ИМ_Значение']
        part_df['ШАМШГСГГ_МУР_Значение'] = base_df['МУР_Значение']
        part_df['ШАМШГСГГ_ЭМ_Значение'] = base_df['ЭМ_Значение']
        part_df['ШАМШГСГГ_АМ_Значение'] = base_df['АМ_Значение']


        part_df['ШАМШГСГГ_ПМ_Диапазон'] = base_df['ПМ_Диапазон']
        part_df['ШАМШГСГГ_МД_Диапазон'] = base_df['МД_Диапазон']
        part_df['ШАМШГСГГ_МСР_Диапазон'] = base_df['МСР_Диапазон']
        part_df['ШАМШГСГГ_МСУ_Диапазон'] = base_df['МСУ_Диапазон']

        part_df['ШАМШГСГГ_ИМ_Диапазон'] = base_df['ИМ_Диапазон']
        part_df['ШАМШГСГГ_МУР_Диапазон'] = base_df['МУР_Диапазон']
        part_df['ШАМШГСГГ_ЭМ_Диапазон'] = base_df['ЭМ_Диапазон']
        part_df['ШАМШГСГГ_АМ_Диапазон'] = base_df['АМ_Диапазон']

        out_answer_df = pd.concat([out_answer_df, answers_df], axis=1)  # Датафрейм для проверки

        base_df.sort_values(by='ПМ_Значение', ascending=True, inplace=True)  # сортируем

        # Делаем свод  по  шкалам
        dct_svod_sub = {'ПМ_Значение': 'ПМ_Диапазон',
                        'МД_Значение': 'МД_Диапазон',
                        'МСР_Значение': 'МСР_Диапазон',
                        'МСУ_Значение': 'МСУ_Диапазон',

                        'ИМ_Значение': 'ИМ_Диапазон',
                        'МУР_Значение': 'МУР_Диапазон',
                        'ЭМ_Значение': 'ЭМ_Диапазон',
                        'АМ_Значение': 'АМ_Диапазон',
                        }

        dct_rename_svod_sub = {'ПМ_Значение': 'Познавательная мотивация',
                               'МД_Значение': 'Мотивация достижения',
                               'МСР_Значение': 'Мотивация саморазвития',
                               'МСУ_Значение': 'Мотивация самоуважения',

                               'ИМ_Значение': 'Интроецированная мотивация',
                               'МУР_Значение': 'Мотивация уважения родителями',
                               'ЭМ_Значение': 'Экстернальная мотивация',
                               'АМ_Значение': 'Амотивация',
                               }

        lst_sub = ['1-1,99', '2-2,99', '3-3,99','4-5']

        base_svod_sub_df = create_union_svod(base_df, dct_svod_sub, dct_rename_svod_sub, lst_sub)

        avg_pm = round(base_df['ПМ_Значение'].mean(), 2)
        avg_md = round(base_df['МД_Значение'].mean(), 2)
        avg_msr = round(base_df['МСР_Значение'].mean(), 2)
        avg_msu = round(base_df['МСУ_Значение'].mean(), 2)

        avg_im = round(base_df['ИМ_Значение'].mean(), 2)
        avg_mur = round(base_df['МУР_Значение'].mean(), 2)
        avg_am = round(base_df['ЭМ_Значение'].mean(), 2)
        avg_a = round(base_df['АМ_Значение'].mean(), 2)

        avg_dct = {'Среднее значение шкалы Познавательная мотивация': avg_pm,
                   'Среднее значение шкалы Мотивация достижения': avg_md,
                   'Среднее значение шкалы Мотивация саморазвития': avg_msr,
                   'Среднее значение шкалы Мотивация самоуважения': avg_msu,

                   'Среднее значение шкалы Интроецированная мотивация': avg_im,
                   'Среднее значение шкалы Мотивация уважения родителями': avg_mur,
                   'Среднее значение шкалы Экстернальная мотивация': avg_am,
                   'Среднее значение шкалы Амотивация': avg_a,
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

        dct_prefix = {
            'ПМ_Диапазон': 'ПМ',
            'МД_Диапазон': 'МД',
            'МСР_Диапазон': 'МСР',
            'МСУ_Диапазон': 'МСУ',

            'ИМ_Диапазон': 'ИМ',
            'МУР_Диапазон': 'МУР',
            'ЭМ_Диапазон': 'ЭМ',
            'АМ_Диапазон': 'АМ',
        }

        out_dct = create_list_on_level(base_df, out_dct, lst_sub, dct_prefix)

        """
                        Сохраняем в зависимости от необходимости делать своды по определенным колонкам
                        """
        if len(lst_svod_cols) == 0:
            return out_dct, part_df

        else:
            out_dct = create_result_shamsh_gordeeva(base_df, out_dct, lst_svod_cols)
            return out_dct, part_df


    except BadOrderSHAMSHG:
        messagebox.showerror('Лахеcис',
                             f'При обработке вопросов теста Шкалы академической мотивации школьников ШАМ-Ш Гордеева и др. обнаружены неправильные вопросы. Проверьте названия колонок с вопросами:\n'
                             f'{error_order_message[:5000]}\n'
                             f'Используйте при создании Яндекс-формы написание вопросов из руководства пользователя программы Лахесис.')
    except BadValueSHAMSHG:
        messagebox.showerror('Лахеcис',
                             f'При обработке вопросов теста Шкалы академической мотивации школьников ШАМ-Ш Гордеева и др. обнаружены неправильные варианты ответов. Проверьте ответы на указанных строках:\n'
                             f'{error_message[:5000]}\n'
                             f'Используйте при создании Яндекс-формы написание вариантов ответа из руководства пользователя программы Лахесис.')


    except BadCountColumnsSHAMSHG:
        messagebox.showerror('Лахеcис',
                             f'Проверьте количество колонок с ответами на тест Шкалы академической мотивации школьников ШАМ-Ш Гордеева и др.\n'
                             f'Должно быть 32 колонки с ответами')








