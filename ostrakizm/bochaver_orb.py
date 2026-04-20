"""
Скрипт для обработки результатов Опросник риска буллинга А.А. Бочавер и др.
"""

import pandas as pd
import re
from tkinter import messagebox
from lachesis_support_functions import round_mean_two,calc_count_scale,create_union_svod, create_list_on_level

class BadOrderBORB(Exception):
    """
    Исключение для обработки случая когда колонки не совпадают
    """
    pass


class BadValueBORB(Exception):
    """
    Исключение для неправильных значений в вариантах ответов
    """
    pass

class BadCountColumnsBORB(Exception):
    """
    Исключение для обработки случая если количество колонок не равно 48
    """
    pass

def calc_value_nb(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [1,3,7,11,12,16,20,31,33,34,36,46,
              8,21,32,35]
    lst_neg = [8,21,32,35]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_pr:
            if idx not in lst_neg:
                if value == 'да':
                    value_forward += 1
            else:
                if value == 'нет':
                    value_forward += 1
    return value_forward


def calc_value_b(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [15,17,26,27,41,47,
              19,25,28,44,48]
    lst_neg = [19,25,28,44,48]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_pr:
            if idx not in lst_neg:
                if value == 'да':
                    value_forward += 1
            else:
                if value == 'нет':
                    value_forward += 1
    return value_forward


def calc_value_ro(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [4,22,37,39,43,
              2,5,6,38,42]
    lst_neg = [2,5,6,38,42]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_pr:
            if idx not in lst_neg:
                if value == 'да':
                    value_forward += 1
            else:
                if value == 'нет':
                    value_forward += 1
    return value_forward


def calc_value_rp(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [9,10,13,14,18,23,24,29,30,40,45]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_pr:
            if value == 'да':
                value_forward += 1
    return value_forward



def calc_level_sub(value,quantity):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """

    result =round((value / quantity) * 100)

    if 0<= result <= 24:
        return f'0-24%'
    elif 25 <= result <= 49:
        return f'25-49%'
    elif 50 <= result <= 74:
        return f'50-74%'
    else:
        return f'75-100%'


def count_group_result(df:pd.DataFrame):
    """
    Для подсчета внутри группы
    :param df:
    :return:
    """
    return round(df.sum() / len(df),2)


def create_result_orb_bochaver(base_df:pd.DataFrame, out_dct:dict, lst_svod_cols:list):
    """
    Функция для подсчета результата если указаны колонки по которым нужно провести свод
    :param df: датафрейм с результатами
    :param out_dct: словарь с уже подсчитанными базовыми данными
    :param lst_svod_cols: список сводных колонок
    :return: словарь
    """



    lst_level = ['0-24%', '25-49%', '50-74%','75-100%']
    lst_reindex_one_level_cols = lst_svod_cols.copy()
    lst_reindex_one_level_cols.extend(['0-24%', '25-49%', '50-74%','75-100%',
                                       'Итого'])  # Основная шкала

    # АД
    svod_count_one_level_nb_df = calc_count_scale(base_df, lst_svod_cols,
                                                 'ИО_НБ_Значение',
                                                 'ИО_НБ_Диапазон',
                                                 lst_reindex_one_level_cols, lst_level)
    # АВА
    svod_count_one_level_b_df = calc_count_scale(base_df, lst_svod_cols,
                                                 'ИО_Б_Значение',
                                                 'ИО_Б_Диапазон',
                                                 lst_reindex_one_level_cols, lst_level)

    svod_count_one_level_ro_df = calc_count_scale(base_df, lst_svod_cols,
                                                 'ИО_РО_Значение',
                                                 'ИО_РО_Диапазон',
                                                 lst_reindex_one_level_cols, lst_level)
    svod_count_one_level_rp_df = calc_count_scale(base_df, lst_svod_cols,
                                                 'ИО_РО_Диапазон',
                                                 'ИО_РП_Диапазон',
                                                 lst_reindex_one_level_cols, lst_level)

    # Считаем среднее по субшкалам
    svod_mean_one_df = pd.pivot_table(base_df,
                                      index=lst_svod_cols,
                                      values=['ИО_НБ_Значение',
                                              'ИО_Б_Значение',
                                              'ИО_РО_Значение',
                                              'ИО_РП_Значение',
                                              ],
                                      aggfunc=round_mean_two)
    svod_mean_one_df.reset_index(inplace=True)

    # упорядочиваем колонки
    new_order_cols = lst_svod_cols.copy()
    new_order_cols.extend((['ИО_НБ_Значение',
                            'ИО_Б_Значение',
                            'ИО_РО_Значение',
                            'ИО_РП_Значение',
                            ]))
    svod_mean_one_df = svod_mean_one_df.reindex(columns=new_order_cols)

    dct_rename_cols_mean = {'ИО_НБ_Значение': 'Небезопасность',
                            'ИО_Б_Значение': 'Благополучие',
                            'ИО_РО_Значение': 'Разобщенность',
                            'ИО_РП_Значение': 'Равноправие',
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

    out_dct.update({
                    f'ГО {out_name}': svod_mean_one_df,
                    f'НБ {out_name}': svod_count_one_level_nb_df,
                    f'Б {out_name}': svod_count_one_level_b_df,
                    f'РО {out_name}': svod_count_one_level_ro_df,
                    f'РП {out_name}': svod_count_one_level_rp_df,
                    })


    if len(lst_svod_cols) == 1:
        dct_prefix = {'ИО_НБ_Диапазон': 'НБ',
                      'ИО_Б_Диапазон': 'Б',
                      'ИО_РО_Диапазон': 'РО',
                      'ИО_РП_Диапазон': 'РП',
                      }

        out_dct = create_list_on_level(base_df, out_dct, lst_level, dct_prefix)
        return out_dct
    else:
        for idx, name_column in enumerate(lst_svod_cols):
            lst_reindex_column_level_cols = [lst_svod_cols[idx], '0-24%', '25-49%', '50-74%','75-100%',
                                             'Итого']

            # АД
            svod_count_column_level_nb_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                            'ИО_НБ_Значение',
                                                            'ИО_НБ_Диапазон',
                                                            lst_reindex_column_level_cols, lst_level)
            # АВА
            svod_count_column_level_b_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                            'ИО_Б_Значение',
                                                            'ИО_Б_Диапазон',
                                                            lst_reindex_column_level_cols, lst_level)
            svod_count_column_level_ro_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                            'ИО_РО_Значение',
                                                            'ИО_РО_Диапазон',
                                                            lst_reindex_column_level_cols, lst_level)
            svod_count_column_level_rp_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                            'ИО_РП_Значение',
                                                            'ИО_РП_Диапазон',
                                                            lst_reindex_column_level_cols, lst_level)

            # Считаем среднее по субшкалам
            svod_mean_column_df = pd.pivot_table(base_df,
                                              index=[lst_svod_cols[idx]],
                                              values=['ИО_НБ_Значение',
                                                      'ИО_Б_Значение',
                                                      'ИО_РО_Значение',
                                                      'ИО_РП_Значение',
                                                      ],
                                              aggfunc=round_mean_two)
            svod_mean_column_df.reset_index(inplace=True)

            # упорядочиваем колонки
            new_order_cols = [lst_svod_cols[idx]].copy()
            new_order_cols.extend((['ИО_НБ_Значение',
                                    'ИО_Б_Значение',
                                    'ИО_РО_Значение',
                                    'ИО_РП_Значение',
                                    ]))
            svod_mean_column_df = svod_mean_column_df.reindex(columns=new_order_cols)

            dct_rename_cols_mean = {'ИО_НБ_Значение': 'Небезопасность',
                                    'ИО_Б_Значение': 'Благополучие',
                                    'ИО_РО_Значение': 'Разобщенность',
                                    'ИО_РП_Значение': 'Равноправие',
                                    }
            svod_mean_column_df.rename(columns=dct_rename_cols_mean, inplace=True)

            # Готовим наименование
            name_column = lst_svod_cols[idx]
            name_column = re.sub(r'[\[\]\'+()<> :"?*|\\/]', '_', name_column)
            name_column = name_column[:15]
            out_dct.update({f'ГО {name_column}': svod_mean_column_df,
                            f'НБ {name_column}': svod_count_column_level_nb_df,
                            f'Б {name_column}': svod_count_column_level_b_df,
                            f'РО {name_column}': svod_count_column_level_ro_df,
                            f'РП {name_column}': svod_count_column_level_rp_df,
                            })
        dct_prefix = {'ИО_НБ_Диапазон': 'НБ',
                      'ИО_Б_Диапазон': 'Б',
                      'ИО_РО_Диапазон': 'РО',
                      'ИО_РП_Диапазон': 'РП',
                      }

        out_dct = create_list_on_level(base_df, out_dct, lst_level, dct_prefix)

        return out_dct







def processing_school_orb_bochaver(base_df: pd.DataFrame, answers_df: pd.DataFrame, lst_svod_cols:list):
    """
    Функция для обработки
    :param base_df: часть датафрейма с описательными колонками
    :param answers_df: часть датафрейма с ответами
    :param lst_svod_cols:  список с колонками по которым нужно делать свод
    """
    try:
        out_answer_df = base_df.copy()  # делаем копию для последующего соединения с сырыми ответами
        if len(answers_df.columns) != 48:  # проверяем количество колонок с вопросами
            raise BadCountColumnsBORB

        # очищаем названия колонок от возможных сочетаний .1 которые добавляет пандас при одинаковых колонках
        clean_df_lst = []
        for name_column in answers_df.columns:
            clean_name = re.sub(r'.\d+$', '', name_column)
            clean_df_lst.append(clean_name)

        answers_df.columns = clean_df_lst

        lst_check_cols = ['В вашем классе принято мешать друг другу, лезть, приставать',
                          'В вашем классе принято вместе развлекаться после уроков',
                          'В вашем классе принято шутить над кем-нибудь так, чтобы смеялся весь класс',
                          'В вашем классе принято драться',
                          'В вашем классе принято ходить друг к другу в гости',
                          'В вашем классе принято заступаться за своих',
                          'В вашем классе принято обзываться',
                          'В вашем классе принято не мешать друг другу заниматься, чем захочется',
                          'В вашем классе есть кто-то кого все уважают',
                          'В вашем классе есть кто-то кого все боятся',

                          'В вашем классе есть кто-то над кем все смеются',
                          'В вашем классе есть кто-то кем часто недовольны учителя',
                          'В вашем классе есть кто-то на кого хочется быть похожим',
                          'В вашем классе есть кто-то с кем лучше не спорить',
                          'В вашем классе есть кто-то кто никогда не прогуливает',
                          'В вашем классе есть кто-то с кем даже учитель не может справиться',
                          'Как к вам в классе обращаются обычно учителя? По имени',
                          'Как к вам в классе обращаются обычно учителя? По имени и отчеству',
                          'Как к вам в классе обращаются обычно учителя? По фамилии',
                          'Как к вам в классе обращаются обычно учителя? По прозвищам',

                          'Когда в школе происходит драка, вы удивляетесь',
                          'Когда в школе происходит драка, вы не обращаете внимания, это обычное дело',
                          'Когда в школе происходит драка, вы присоединяетесь, встав на чью-то сторону',
                          'Когда в школе происходит драка, вы много это потом обсуждаете между собой в классе',
                          'Ценные вещи стараюсь не носить в школу вообще',
                          'Ценные вещи спокойно оставляю в классе',
                          'Ценные вещи можно оставить в коридоре',
                          'Ценные вещи был случай, что украли',
                          'Ценные вещи оставляю в раздевалке',
                          'Вызов к директору – это хотят за что-то похвалить',

                          'В вашей школе мат, ругательства звучат на переменах в личных разговорах',
                          'В вашей школе мат, ругательства не приняты вообще',
                          'В вашей школе курят в туалетах, под лестницами',
                          'В вашей школе стены, мебель исписанные, испачканные',
                          'Если кто-то начинает орать, драться, класс «встает на уши»; что нужно, чтобы это прекратилось? Кто-то из учеников должен сказать «хватит»',
                          'Если кто-то начинает орать, драться, класс «встает на уши»; что нужно, чтобы это прекратилось? Должен прийти директор',
                          'Если кто-то начинает орать, драться, класс «встает на уши»; что нужно, чтобы это прекратилось? Это прекратится, когда все устанут',
                          'В школе вам в целом нравится, приятно, интересно',
                          'В школе вам в целом не нравится, плохо, никто ни с кем не дружит',
                          'Перемену я провожу захожу к друзьям в другие классы',

                          'Когда ваш класс едет куда-то с учителями это обычная ситуация',
                          'Когда ваш класс едет куда-то с учителями вам это нравится, это весело',
                          'Когда ваш класс едет куда-то с учителями вы стараетесь не ездить',
                          'Когда ваш класс едет куда-то с учителями учителям это сложно, они каждый говорят, что это «в последний раз»',
                          'Ваш класс имеет репутацию отличников',
                          'Ваш класс имеет репутацию хулиганов',
                          'Ваш класс имеет репутацию самого обычного, ничем не отличающегося от других классов в школе',
                          'Ваш класс имеет репутацию класса, в котором никто не хочет быть классным руководителем'
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
            raise BadOrderBORB

        valid_values = ['да','нет']
        # Проверяем, есть ли значения, отличающиеся от указанных в списке
        lst_error_answers = []  # список для хранения строк где найдены неправильные ответы

        for i in range(48):
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
            raise BadValueBORB
        base_df['ИО_НБ_Значение'] = answers_df.apply(calc_value_nb, axis=1)
        base_df['ИО_НБ_Диапазон'] = base_df['ИО_НБ_Значение'].apply(lambda x:calc_level_sub(x,16))

        base_df['ИО_Б_Значение'] = answers_df.apply(calc_value_b, axis=1)
        base_df['ИО_Б_Диапазон'] = base_df['ИО_Б_Значение'].apply(lambda x: calc_level_sub(x, 11))

        base_df['ИО_РО_Значение'] = answers_df.apply(calc_value_ro, axis=1)
        base_df['ИО_РО_Диапазон'] = base_df['ИО_РО_Значение'].apply(lambda x: calc_level_sub(x, 10))

        base_df['ИО_РП_Значение'] = answers_df.apply(calc_value_rp, axis=1)
        base_df['ИО_РП_Диапазон'] = base_df['ИО_РП_Значение'].apply(lambda x: calc_level_sub(x, 11))

        if len(lst_svod_cols) == 0:
            base_df['ГО_НБ_Значение'] = round(base_df['ИО_НБ_Значение'].sum() / len(base_df), 2)
            base_df['ГО_Б_Значение'] = round(base_df['ИО_Б_Значение'].sum() / len(base_df), 2)
            base_df['ГО_РО_Значение'] = round(base_df['ИО_РО_Значение'].sum() / len(base_df), 2)
            base_df['ГО_РП_Значение'] = round(base_df['ИО_РП_Значение'].sum() / len(base_df), 2)

            # Создаем датафрейм для отображения группового значения
            group_cols = lst_svod_cols.copy()
            group_cols.extend(['ГО_НБ_Значение','ГО_Б_Значение','ГО_РО_Значение','ГО_РП_Значение'])
            group_result_df = base_df[group_cols]
            group_result_df = group_result_df.head(1)
            group_result_df.columns = ['Небезопасность','Благополучие','Разобщенность','Равноправие']




            # Создаем датафрейм для создания части в общий датафрейм
            part_df = pd.DataFrame()

            part_df['ОРББ_ГО_НБ_Значение'] = base_df['ГО_НБ_Значение']
            part_df['ОРББ_ГО_Б_Значение'] = base_df['ГО_Б_Значение']
            part_df['ОРББ_ГО_РО_Значение'] = base_df['ГО_РО_Значение']
            part_df['ОРББ_ГО_РП_Значение'] = base_df['ГО_РП_Значение']


            part_df['ОРББ_ИО_НБ_Значение'] = base_df['ИО_НБ_Значение']
            part_df['ОРББ_ИО_НБ_Диапазон'] = base_df['ИО_НБ_Диапазон']

            part_df['ОРББ_ИО_Б_Значение'] = base_df['ИО_Б_Значение']
            part_df['ОРББ_ИО_Б_Диапазон'] = base_df['ИО_Б_Диапазон']

            part_df['ОРББ_ИО_РО_Значение'] = base_df['ИО_РО_Значение']
            part_df['ОРББ_ИО_РО_Диапазон'] = base_df['ИО_РО_Диапазон']

            part_df['ОРББ_ИО_РП_Значение'] = base_df['ИО_РП_Значение']
            part_df['ОРББ_ИО_РП_Диапазон'] = base_df['ИО_РП_Диапазон']

            out_answer_df = pd.concat([out_answer_df, answers_df], axis=1)  # Датафрейм для проверки

            # Соединяем анкетную часть с результатной
            base_df.sort_values(by='ИО_НБ_Значение', ascending=False, inplace=True)  # сортируем


            # Делаем свод  по  шкалам
            dct_svod_sub = {'ИО_НБ_Значение': 'ИО_НБ_Диапазон',
                            'ИО_Б_Значение': 'ИО_Б_Диапазон',
                            'ИО_РО_Значение': 'ИО_РО_Диапазон',
                            'ИО_РП_Значение': 'ИО_РП_Диапазон',
                            }

            dct_rename_svod_sub = {'ИО_НБ_Значение': 'ИО диапазона в % шкалы Небезопасность',
                                   'ИО_Б_Значение': 'ИО диапазона в % шкалы Благополучие',
                                   'ИО_РО_Значение': 'ИО диапазона в % шкалы Разобщенность',
                                   'ИО_РП_Значение': 'ИО диапазона в % шкалы Равноправие',
                                   }

            lst_sub = ['0-24%', '25-49%', '50-74%','75-100%']

            base_svod_sub_df = create_union_svod(base_df, dct_svod_sub, dct_rename_svod_sub, lst_sub)

            # Делаем свод  по  шкалам
            dct_svod_pr_sub = {'ИО_НБ_Значение': 'ИО_НБ_Диапазон',
                            'ИО_РО_Значение': 'ИО_РО_Диапазон',
                            }

            dct_rename_svod_pr_sub = {'ИО_НБ_Значение': 'ИО диапазона в % шкалы Небезопасность',
                                   'ИО_РО_Значение': 'ИО диапазона в % шкалы Разобщенность',
                                   }

            base_svod_sub_pr_df = create_union_svod(base_df, dct_svod_pr_sub, dct_rename_svod_pr_sub, lst_sub)


            dct_svod_apr_sub = {
                            'ИО_Б_Значение': 'ИО_Б_Диапазон',
                            'ИО_РП_Значение': 'ИО_РП_Диапазон',
                            }

            dct_rename_svod_apr_sub = {
                                   'ИО_Б_Значение': 'ИО диапазона в % шкалы Благополучие',
                                   'ИО_РП_Значение': 'ИО диапазона в % шкалы Равноправие',
                                   }

            base_svod_sub_apr_df = create_union_svod(base_df, dct_svod_apr_sub, dct_rename_svod_apr_sub, lst_sub)


            # формируем основной словарь
            out_dct = {'Списочный результат': base_df,
                       'Список для проверки': out_answer_df,
                       'ГО': group_result_df,
                       'Свод Предикторы': base_svod_sub_pr_df,
                       'Свод Антипредикторы': base_svod_sub_apr_df,
                       'Свод Шкалы': base_svod_sub_df,
                       }

            dct_prefix = {'ИО_НБ_Диапазон': 'НБ',
                          'ИО_Б_Диапазон': 'Б',
                          'ИО_РО_Диапазон': 'РО',
                          'ИО_РП_Диапазон': 'РП',
                          }

            out_dct = create_list_on_level(base_df, out_dct, lst_sub, dct_prefix)

            return out_dct, part_df
        else:
            # Высчитываем по отдельности для каждой группы
            group_result_df = pd.pivot_table(base_df, index=lst_svod_cols,
                                             values=['ИО_НБ_Значение','ИО_Б_Значение','ИО_РО_Значение','ИО_РП_Значение'],
                                             aggfunc=count_group_result)

            group_result_df = group_result_df.reindex(columns=['ИО_НБ_Значение','ИО_Б_Значение','ИО_РО_Значение','ИО_РП_Значение'])

            group_result_df = group_result_df.reset_index()

            group_result_df.rename(columns={'ИО_НБ_Значение': 'ГО_НБ_Значение',
                                            'ИО_Б_Значение': 'ГО_Б_Значение',
                                            'ИО_РО_Значение': 'ГО_РО_Значение',
                                            'ИО_РП_Значение': 'ГО_РП_Значение',}, inplace=True)

            base_df = base_df.merge(group_result_df, how='inner', on=lst_svod_cols)


            # Создаем датафрейм для создания части в общий датафрейм
            part_df = pd.DataFrame()

            part_df['ОРББ_ГО_НБ_Значение'] = base_df['ГО_НБ_Значение']
            part_df['ОРББ_ГО_Б_Значение'] = base_df['ГО_Б_Значение']
            part_df['ОРББ_ГО_РО_Значение'] = base_df['ГО_РО_Значение']
            part_df['ОРББ_ГО_РП_Значение'] = base_df['ГО_РП_Значение']


            part_df['ОРББ_ИО_НБ_Значение'] = base_df['ИО_НБ_Значение']
            part_df['ОРББ_ИО_НБ_Диапазон'] = base_df['ИО_НБ_Диапазон']

            part_df['ОРББ_ИО_Б_Значение'] = base_df['ИО_Б_Значение']
            part_df['ОРББ_ИО_Б_Диапазон'] = base_df['ИО_Б_Диапазон']

            part_df['ОРББ_ИО_РО_Значение'] = base_df['ИО_РО_Значение']
            part_df['ОРББ_ИО_РО_Диапазон'] = base_df['ИО_РО_Диапазон']

            part_df['ОРББ_ИО_РП_Значение'] = base_df['ИО_РП_Значение']
            part_df['ОРББ_ИО_РП_Диапазон'] = base_df['ИО_РП_Диапазон']

            out_answer_df = pd.concat([out_answer_df, answers_df], axis=1)  # Датафрейм для проверки

            # Соединяем анкетную часть с результатной
            base_df.sort_values(by='ИО_НБ_Значение', ascending=False, inplace=True)  # сортируем

            # Делаем свод  по  шкалам
            dct_svod_sub = {'ИО_НБ_Значение': 'ИО_НБ_Диапазон',
                            'ИО_Б_Значение': 'ИО_Б_Диапазон',
                            'ИО_РО_Значение': 'ИО_РО_Диапазон',
                            'ИО_РП_Значение': 'ИО_РП_Диапазон',
                            }

            dct_rename_svod_sub = {'ИО_НБ_Значение': 'ИО диапазона в % шкалы Небезопасность',
                                   'ИО_Б_Значение': 'ИО диапазона в % шкалы Благополучие',
                                   'ИО_РО_Значение': 'ИО диапазона в % шкалы Разобщенность',
                                   'ИО_РП_Значение': 'ИО диапазона в % шкалы Равноправие',
                                   }

            lst_sub = ['0-24%', '25-49%', '50-74%','75-100%']

            base_svod_sub_df = create_union_svod(base_df, dct_svod_sub, dct_rename_svod_sub, lst_sub)

            # Делаем свод  по  шкалам
            dct_svod_pr_sub = {'ИО_НБ_Значение': 'ИО_НБ_Диапазон',
                            'ИО_РО_Значение': 'ИО_РО_Диапазон',
                            }

            dct_rename_svod_pr_sub = {'ИО_НБ_Значение': 'ИО диапазона в % шкалы Небезопасность',
                                   'ИО_РО_Значение': 'ИО диапазона в % шкалы Разобщенность',
                                   }

            base_svod_sub_pr_df = create_union_svod(base_df, dct_svod_pr_sub, dct_rename_svod_pr_sub, lst_sub)


            dct_svod_apr_sub = {
                            'ИО_Б_Значение': 'ИО_Б_Диапазон',
                            'ИО_РП_Значение': 'ИО_РП_Диапазон',
                            }

            dct_rename_svod_apr_sub = {
                                   'ИО_Б_Значение': 'ИО диапазона в % шкалы Благополучие',
                                   'ИО_РП_Значение': 'ИО диапазона в % шкалы Равноправие',
                                   }

            base_svod_sub_apr_df = create_union_svod(base_df, dct_svod_apr_sub, dct_rename_svod_apr_sub, lst_sub)


            # формируем основной словарь
            out_dct = {'Списочный результат': base_df,
                       'Список для проверки': out_answer_df,
                       'Свод Предикторы': base_svod_sub_pr_df,
                       'Свод Антипредикторы': base_svod_sub_apr_df,
                       'Свод Шкалы': base_svod_sub_df,
                       }



            out_dct = create_result_orb_bochaver(base_df, out_dct, lst_svod_cols)

            return out_dct, part_df

    except BadOrderBORB:
        messagebox.showerror('Лахеcис',
                             f'При обработке вопросов теста Опросник риска буллинга Бочавер обнаружены неправильные вопросы. Проверьте названия колонок с вопросами:\n'
                             f'{error_order_message[:5000]}\n'
                             f'Используйте при создании Яндекс-формы написание вопросов из руководства пользователя программы Лахесис.')
    except BadValueBORB:
        messagebox.showerror('Лахеcис',
                             f'При обработке вопросов теста Опросник риска буллинга Бочавер обнаружены неправильные варианты ответов. Проверьте ответы на указанных строках:\n'
                             f'{error_message[:5000]}\n'
                             f'Используйте при создании Яндекс-формы написание вариантов ответа из руководства пользователя программы Лахесис.')


    except BadCountColumnsBORB:
        messagebox.showerror('Лахеcис',
                             f'Проверьте количество колонок с ответами на тест Опросник риска буллинга Бочавер\n'
                             f'Должно быть 48 колонок с ответами')










