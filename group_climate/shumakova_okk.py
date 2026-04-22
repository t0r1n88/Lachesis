"""
Скрипт для обработки результатов Опросник Климат в классе Петрова Щебланова
"""

import pandas as pd
import re
from tkinter import messagebox
from lachesis_support_functions import round_mean_two,calc_count_scale,create_union_svod, create_list_on_level

class BadOrderOKKSSS(Exception):
    """
    Исключение для обработки случая когда колонки не совпадают
    """
    pass


class BadValueOKKSSS(Exception):
    """
    Исключение для неправильных значений в вариантах ответов
    """
    pass

class BadCountColumnsOKKSSS(Exception):
    """
    Исключение для обработки случая если количество колонок не равно 39
    """
    pass

class NotReqColumnOKKSSS(Exception):
    """
    Исключение для обработки случая когда нет обязательных колонок Пол И ФИО
    """
    pass

class BadValueAgeOKKSSS(Exception):
    """
    Исключение для обработки случая когда в колонке Пол есть значения отличающиеся от 5-6. 7-8. 9-10 классов
    """
    pass


def calc_level(value):
    """
    Функция для подсчета уровня
    :param value: значение
    :return:
    """
    if value == 1:
        return 'очень низкий'
    elif  2<=value <=3 :
        return 'ниже среднего'
    elif  4<=value <=6 :
        return 'средний'
    elif  7<=value <=8 :
        return 'выше среднего'
    else:
        return 'очень высокий'




def calc_value_pu(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [5,6,7,11,21,22,23,34,35,36]
    lst_neg = [34]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_pr:
            if idx not in lst_neg:
                value_forward += value
            else:
                if value == 0:
                    value_forward += 3
                elif value == 1:
                    value_forward += 2
                elif value == 2:
                    value_forward += 1
                elif value == 3:
                    value_forward += 0


    return value_forward


def calc_pu_sten(value):
    """
    Функция для подсчета Стена
    """
    if  0<= value <= 9 :
        return 1
    elif 10 <=value <= 13:
        return 2
    elif 14<=value <= 16 :
        return 3
    elif 17<=value <= 19 :
        return 4
    elif 20<=value <=22 :
        return 5
    elif 23<=value <=25 :
        return 6
    elif 26<=value <=28 :
        return 7
    elif value ==29 :
        return 8
    else:
        return 9



def calc_value_sto(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [3,4,8,9,19,24,25,33,37]
    lst_neg = [3,19,24,37]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_pr:
            if idx not in lst_neg:
                value_forward += value
            else:
                if value == 0:
                    value_forward += 3
                elif value == 1:
                    value_forward += 2
                elif value == 2:
                    value_forward += 1
                elif value == 3:
                    value_forward += 0


    return value_forward


def calc_sto_sten(value):
    """
    Функция для подсчета Стена
    """
    if  value == 0 :
        return 1
    elif  1<=value <=3 :
        return 2
    elif 4<=value <=6  :
        return 3
    elif 7<=value <=9  :
        return 4
    elif 10<=value <=11 :
        return 5
    elif 12<=value <=14 :
        return 6
    elif 15<=value <=17 :
        return 7
    elif 18<=value <=19:
        return 8
    else:
        return 9


def calc_value_ork(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [13,14,15,18,27,29,39]
    lst_neg = [27]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_pr:
            if idx not in lst_neg:
                value_forward += value
            else:
                if value == 0:
                    value_forward += 3
                elif value == 1:
                    value_forward += 2
                elif value == 2:
                    value_forward += 1
                elif value == 3:
                    value_forward += 0


    return value_forward

def calc_ork_sten(row:pd.Series):
    """
    Функция для подсчета Стена
    """
    age,value = row
    if age == '5–6 классы':
        if  0<= value <=1  :
            return 1
        elif  2<=value <=4 :
            return 2
        elif 5<=value <=8  :
            return 3
        elif 9<=value <=10  :
            return 4
        elif 11<=value <=13 :
            return 5
        elif 14<=value <=15 :
            return 6
        elif 16<=value <=17 :
            return 7
        elif value == 18:
            return 8
        else:
            return 9
    elif age == '7–8 классы':
        if  value == 0  :
            return 1
        elif  1<=value <= 4 :
            return 2
        elif 5<=value <= 7 :
            return 3
        elif 8<=value <= 9 :
            return 4
        elif 10<=value <=12 :
            return 5
        elif 13<=value <=14 :
            return 6
        elif 15<=value <=16 :
            return 7
        elif 17<=value <=18 :
            return 8
        else:
            return 9
    else:
        if  value == 0  :
            return 1
        elif  1<=value <=2 :
            return 2
        elif 3<=value <=5  :
            return 3
        elif 6<=value <=7  :
            return 4
        elif 8<=value <=10 :
            return 5
        elif 11<=value <=12 :
            return 6
        elif 13<=value <=14 :
            return 7
        elif 15<=value <=17 :
            return 8
        else:
            return 9



def calc_value_spo(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [2,10,16,17,20,26]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_pr:
            value_forward += value


    return value_forward

def calc_spo_sten(value):
    """
    Функция для подсчета Стена
    """

    if  0<= value <=1:
        return 1
    elif  value == 2:
        return 2
    elif 3<=value <= 4:
        return 3
    elif value ==5:
        return 4
    elif 6<=value <=7:
        return 5
    elif value ==8:
        return 6
    elif 9<=value <= 11:
        return 7
    elif 12 <=value <=13:
        return 8
    else:
        return 9


def calc_value_dshs(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [1,28,38]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_pr:
            value_forward += value


    return value_forward

def calc_dshs_sten(value):
    """
    Функция для подсчета Стена
    """

    if  0<= value <=1:
        return 1
    elif  value == 2:
        return 2
    elif value == 3:
        return 3
    elif value ==4:
        return 4
    elif value ==5:
        return 5
    elif value ==6 :
        return 6
    elif value ==7:
        return 7
    elif value ==8 :
        return 8
    else:
        return 9


def calc_value_vou(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [12,30,31,32]
    lst_neg = [12,30]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_pr:
            if idx not in lst_neg:
                value_forward += value
            else:
                if value == 0:
                    value_forward += 3
                elif value == 1:
                    value_forward += 2
                elif value == 2:
                    value_forward += 1
                elif value == 3:
                    value_forward += 0


    return value_forward

def calc_vou_sten(value):
    """
    Функция для подсчета Стена
    """

    if  0<= value <= 3:
        return 1
    elif  value ==4:
        return 2
    elif 5<=value <=6:
        return 3
    elif value ==7  :
        return 4
    elif value ==8:
        return 5
    elif value ==9 :
        return 6
    elif value ==10 :
        return 7
    elif value ==11:
        return 8
    else:
        return 9

def create_itog_stens(row):
    """
    Функция для создания строки с итоговым стеном
    :param row: строка с результатами
    :return:
    """
    lst_out = list(map(str,row))
    return '-'.join(lst_out)



def create_result_okk_shumakova(base_df:pd.DataFrame, out_dct:dict, lst_svod_cols:list):
    """
    Функция для подсчета результата если указаны колонки по которым нужно провести свод
    :param df: датафрейм с результатами
    :param out_dct: словарь с уже подсчитанными базовыми данными
    :param lst_svod_cols: список сводных колонок
    :return: словарь
    """
    lst_level = ['очень низкий', 'ниже среднего', 'средний','выше среднего','очень высокий']

    lst_reindex_one_level_cols = lst_svod_cols.copy()
    lst_reindex_one_level_cols.extend(['очень низкий', 'ниже среднего', 'средний','выше среднего','очень высокий',
                                       'Итого'])  # Основная шкала

    # АД
    svod_count_one_level_pu_df = calc_count_scale(base_df, lst_svod_cols,
                                                 'ПУ_Стен',
                                                 'ПУ_Уровень',
                                                 lst_reindex_one_level_cols, lst_level)
    # АВА
    svod_count_one_level_sto_df = calc_count_scale(base_df, lst_svod_cols,
                                                 'СТО_Стен',
                                                 'СТО_Уровень',
                                                 lst_reindex_one_level_cols, lst_level)

    svod_count_one_level_ork_df = calc_count_scale(base_df, lst_svod_cols,
                                                 'ОРК_Стен',
                                                 'ОРК_Уровень',
                                                 lst_reindex_one_level_cols, lst_level)

    # АД
    svod_count_one_level_spo_df = calc_count_scale(base_df, lst_svod_cols,
                                                 'СПО_Стен',
                                                 'СПО_Уровень',
                                                 lst_reindex_one_level_cols, lst_level)
    # АВА
    svod_count_one_level_dshs_df = calc_count_scale(base_df, lst_svod_cols,
                                                 'ДШС_Стен',
                                                 'ДШС_Уровень',
                                                 lst_reindex_one_level_cols, lst_level)

    svod_count_one_level_vou_df = calc_count_scale(base_df, lst_svod_cols,
                                                 'ВОУ_Стен',
                                                 'ВОУ_Уровень',
                                                 lst_reindex_one_level_cols, lst_level)

    # Считаем среднее по субшкалам
    svod_mean_one_df = pd.pivot_table(base_df,
                                      index=lst_svod_cols,
                                      values=['ПУ_Стен',
                                              'СТО_Стен',
                                              'ОРК_Стен',

                                              'СПО_Стен',
                                              'ДШС_Стен',
                                              'ВОУ_Стен',
                                              ],
                                      aggfunc=round_mean_two)
    svod_mean_one_df.reset_index(inplace=True)

    # упорядочиваем колонки
    new_order_cols = lst_svod_cols.copy()
    new_order_cols.extend((['ПУ_Стен',
                            'СТО_Стен',
                            'ОРК_Стен',

                            'СПО_Стен',
                            'ДШС_Стен',
                            'ВОУ_Стен',
                            ]))
    svod_mean_one_df = svod_mean_one_df.reindex(columns=new_order_cols)

    dct_rename_cols_mean = {'ПУ_Стен': 'Ср. стен Поддерживающий учитель',
                            'СТО_Стен': 'Ср. стен Сотрудничество с одноклассниками',
                            'ОРК_Стен': 'Ср. стен Организация работы в классе',

                            'СПО_Стен': 'Ср. стен Соперничество с одноклассниками',
                            'ДШС_Стен': 'Ср. стен Давление школьной среды',
                            'ВОУ_Стен': 'Ср. стен Вовлеченность одноклассников в учебу',
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
                    f'ПУ {out_name}': svod_count_one_level_pu_df,
                    f'СТО {out_name}': svod_count_one_level_sto_df,
                    f'ОРК {out_name}': svod_count_one_level_ork_df,

                    f'СПО {out_name}': svod_count_one_level_spo_df,
                    f'ДШС {out_name}': svod_count_one_level_dshs_df,
                    f'ВОУ {out_name}': svod_count_one_level_vou_df,
                    })

    if len(lst_svod_cols) == 1:
        return out_dct
    else:
        for idx, name_column in enumerate(lst_svod_cols):
            lst_reindex_column_level_cols = [lst_svod_cols[idx], 'очень низкий', 'ниже среднего', 'средний','выше среднего','очень высокий',
                                             'Итого']


            # АД
            svod_count_column_level_pu_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                            'ПУ_Стен',
                                                            'ПУ_Уровень',
                                                            lst_reindex_column_level_cols, lst_level)
            # АВА
            svod_count_column_level_sto_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                            'СТО_Стен',
                                                            'СТО_Уровень',
                                                            lst_reindex_column_level_cols, lst_level)
            svod_count_column_level_ork_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                            'ОРК_Стен',
                                                            'ОРК_Уровень',
                                                            lst_reindex_column_level_cols, lst_level)

            # АД
            svod_count_column_level_spo_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                            'СПО_Стен',
                                                            'СПО_Уровень',
                                                            lst_reindex_column_level_cols, lst_level)
            # АВА
            svod_count_column_level_dshs_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                            'ДШС_Стен',
                                                            'ДШС_Уровень',
                                                            lst_reindex_column_level_cols, lst_level)
            svod_count_column_level_vou_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                            'ВОУ_Стен',
                                                            'ВОУ_Уровень',
                                                            lst_reindex_column_level_cols, lst_level)

            # Считаем среднее по субшкалам
            svod_mean_column_df = pd.pivot_table(base_df,
                                              index=[lst_svod_cols[idx]],
                                              values=['ПУ_Стен',
                                                      'СТО_Стен',
                                                      'ОРК_Стен',

                                                      'СПО_Стен',
                                                      'ДШС_Стен',
                                                      'ВОУ_Стен',
                                                      ],
                                              aggfunc=round_mean_two)
            svod_mean_column_df.reset_index(inplace=True)

            # упорядочиваем колонки
            new_order_cols = [lst_svod_cols[idx]].copy()
            new_order_cols.extend((['ПУ_Стен',
                                    'СТО_Стен',
                                    'ОРК_Стен',

                                    'СПО_Стен',
                                    'ДШС_Стен',
                                    'ВОУ_Стен',
                                    ]))
            svod_mean_column_df = svod_mean_column_df.reindex(columns=new_order_cols)

            dct_rename_cols_mean = {'ПУ_Стен': 'Ср. стен Поддерживающий учитель',
                                    'СТО_Стен': 'Ср. стен Сотрудничество с одноклассниками',
                                    'ОРК_Стен': 'Ср. стен Организация работы в классе',

                                    'СПО_Стен': 'Ср. стен Соперничество с одноклассниками',
                                    'ДШС_Стен': 'Ср. стен Давление школьной среды',
                                    'ВОУ_Стен': 'Ср. стен Вовлеченность одноклассников в учебу',
                                    }
            svod_mean_column_df.rename(columns=dct_rename_cols_mean, inplace=True)

            # Готовим наименование
            name_column = lst_svod_cols[idx]
            name_column = re.sub(r'[\[\]\'+()<> :"?*|\\/]', '_', name_column)
            name_column = name_column[:15]
            out_dct.update({f'Ср {name_column}': svod_mean_column_df,
                            f'ПУ {name_column}': svod_count_column_level_pu_df,
                            f'СТО {name_column}': svod_count_column_level_sto_df,
                            f'ОРК {name_column}': svod_count_column_level_ork_df,

                            f'СПО {name_column}': svod_count_column_level_spo_df,
                            f'ДШС {name_column}': svod_count_column_level_dshs_df,
                            f'ВОУ {name_column}': svod_count_column_level_vou_df,
                            })
        return out_dct












def processing_okk_shum(base_df: pd.DataFrame, answers_df: pd.DataFrame, lst_svod_cols:list):
    """
    Функция для обработки
    :param base_df: часть датафрейма с описательными колонками
    :param answers_df: часть датафрейма с ответами
    :param lst_svod_cols:  список с колонками по которым нужно делать свод
    """
    try:
        # Проверяем наличие колонок Пол
        diff_req_cols = {'Возраст'}.difference(set(base_df.columns))
        if len(diff_req_cols) != 0:
            raise NotReqColumnOKKSSS

        # Проверяем на пол
        diff_sex = set(base_df['Возраст'].unique()).difference({'5-6 классы', '7-8 классы','9-10 классы'})
        if len(diff_sex) != 0:
            raise BadValueAgeOKKSSS

        union_base_df = base_df.copy()  # делаем копию для последующего соединения с сырыми ответами
        out_answer_df = base_df.copy()  # делаем копию для последующего соединения с сырыми ответами
        quantity_cols_base_df = base_df.shape[1]  # количество колонок в анкетной части
        if len(answers_df.columns) != 39:  # проверяем количество колонок с вопросами
            raise BadCountColumnsOKKSSS

        # очищаем названия колонок от возможных сочетаний .1 которые добавляет пандас при одинаковых колонках
        clean_df_lst = []
        for name_column in answers_df.columns:
            clean_name = re.sub(r'.\d+$', '', name_column)
            clean_df_lst.append(clean_name)

        answers_df.columns = clean_df_lst
        lst_check_cols = ['В школе нам задают слишком много домашних заданий',
                          'В нашем классе каждый старается быть лучше других учеников',
                          'Большинству учащихся доставляет удовольствие совместная работа с одноклассниками',
                          'Если у кого-то из нашего класса возникли трудности, никто не придет ему на помощь',
                          'У нас есть учителя, которые заботятся также и о самых слабых учениках',
                          'Многие учителя стараются помочь нам продвигаться вперед',
                          'У нас можно обсуждать с учителями вопросы, которые не относятся к материалу занятий',
                          'У нас каждый должен пробиваться сам, на поддержку надежды мало',
                          'У нас есть различные группы учеников, которые не хотят иметь дело друг с другом',
                          'У нас каждый видит в одноклассниках только конкурентов',

                          'У нас в классе ученики задают много вопросов и размышляют на уроках',
                          'Если мы не учимся в выходные дни, мы не занимаемся уроками',
                          'Мы часто пытаемся затянуть урок вопросами и надуманными проблемами',
                          'У нас редко бывает на занятиях настолько тихо, чтобы можно было спокойно работать',
                          'Большинство учеников мало интересуются занятиями',
                          'Лучших учеников у нас часто пренебрежительно называют карьеристами',
                          'У нас легко можно стать аутсайдером, если не делать того, что класс считает правильным',
                          'У нас нередко бывает, что весь класс смеется над одним учеником',
                          'Если у нас кто-нибудь что-то не понял, одноклассники ему объяснят',
                          'В классе нельзя нарушать общий порядок, иначе одноклассники будут на тебя косо смотреть',

                          'Некоторые учителя всегда приходят к нам на уроки с новыми идеями',
                          'Большинство учителей стараются сделать уроки как можно более интересными',
                          'Учителя знают сильные стороны учеников и поощряют их развитие',
                          'Если у кого-то из учеников возникают проблемы с выполнением задания, ему охотно помогают одноклассники',
                          'У нас каждый больше всего любит работать в одиночку',
                          'Многие ученики завидуют, если у кого-то результаты лучше, чем у них',
                          'Большинство моих одноклассников сосредоточенно и серьезно работают на уроках',
                          'У нас на уроках предъявляются высокие требования',
                          'Учителям часто нелегко поддерживать у нас на уроках тишину и порядок',
                          'Иногда мы заранее планируем, как сорвать урок или разозлить учителя',

                          'Нельзя позволить себе заболеть, так как отстанешь от других',
                          'Многие из моих одноклассников отдают учебе в школе много сил',
                          'Я считаю, что в нашем классе ученики плохо сотрудничают друг с другом',
                          'На слабых учеников учителя обращают мало внимания',
                          'Большинство учителей заботятся о том, чтобы учеба в школе доставляла нам радость',
                          'Большинство учителей стараются учитывать, что нужно каждому ученику',
                          'Ученики часто помогают друг другу в учебе и других делах',
                          'В школе от нас требуют слишком много',
                          'Некоторые ученики всегда мешают занятиям, когда другие хотят работать'
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
            raise BadOrderOKKSSS

        # словарь для замены слов на числа
        dct_replace_value = {'совершенно не верно': 0,
                             'скорее не верно': 1,
                             'скорее верно': 2,
                             'совершенно верно': 3,
                             }
        valid_values = [0, 1, 2, 3]
        answers_df.replace(dct_replace_value, inplace=True)  # заменяем слова на цифры для подсчетов
        # Проверяем, есть ли значения, отличающиеся от указанных в списке
        lst_error_answers = []  # список для хранения строк где найдены неправильные ответы

        for i in range(39):
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
            raise BadValueOKKSSS

        base_df['ПУ_Значение'] = answers_df.apply(calc_value_pu, axis=1)
        base_df['ПУ_Стен'] = base_df['ПУ_Значение'].apply(calc_pu_sten)
        base_df['ПУ_Уровень'] = base_df['ПУ_Стен'].apply(calc_level)

        base_df['СТО_Значение'] = answers_df.apply(calc_value_sto, axis=1)
        base_df['СТО_Стен'] = base_df['СТО_Значение'].apply(calc_sto_sten)
        base_df['СТО_Уровень'] = base_df['СТО_Стен'].apply(calc_level)

        base_df['ОРК_Значение'] = answers_df.apply(calc_value_ork, axis=1)
        base_df['ОРК_Стен'] = base_df[['Возраст','ОРК_Значение']].apply(calc_ork_sten,axis=1)
        base_df['ОРК_Уровень'] = base_df['ОРК_Стен'].apply(calc_level)


        base_df['СПО_Значение'] = answers_df.apply(calc_value_spo, axis=1)
        base_df['СПО_Стен'] = base_df['СПО_Значение'].apply(calc_spo_sten)
        base_df['СПО_Уровень'] = base_df['СПО_Стен'].apply(calc_level)

        base_df['ДШС_Значение'] = answers_df.apply(calc_value_dshs, axis=1)
        base_df['ДШС_Стен'] = base_df['ДШС_Значение'].apply(calc_dshs_sten)
        base_df['ДШС_Уровень'] = base_df['ДШС_Стен'].apply(calc_level)

        base_df['ВОУ_Значение'] = answers_df.apply(calc_value_vou, axis=1)
        base_df['ВОУ_Стен'] = base_df['ВОУ_Значение'].apply(calc_vou_sten)
        base_df['ВОУ_Уровень'] = base_df['ВОУ_Стен'].apply(calc_level)

        # Упорядочиваем
        result_df = base_df.iloc[:, quantity_cols_base_df:]  # отсекаем часть с результатами чтобы упорядочить
        lst_stens = [column for column in result_df.columns if 'Стен' in column]
        result_df['Итоговые_стены'] = result_df[lst_stens].apply(create_itog_stens, axis=1)

        new_order_lst = ['Итоговые_стены',
                         'ПУ_Стен', 'СТО_Стен', 'ОРК_Стен',
                         'СПО_Стен', 'ДШС_Стен', 'ВОУ_Стен',

                         'ПУ_Уровень', 'СТО_Уровень', 'ОРК_Уровень',
                         'СПО_Уровень', 'ДШС_Уровень', 'ВОУ_Уровень',

                         'ПУ_Значение', 'СТО_Значение', 'ОРК_Значение',
                         'СПО_Значение', 'ДШС_Значение', 'ВОУ_Значение'
                         ]
        result_df = result_df.reindex(columns=new_order_lst)  # изменяем порядок
        base_df = pd.concat([union_base_df, result_df], axis=1)  # соединяем и перезаписываем base_df

        base_df.to_excel('data/res.xlsx')





        # Создаем датафрейм для создания части в общий датафрейм
        part_df = pd.DataFrame()

        # Основные шкалы
        part_df['ОККШЩС_Итоговые_стены'] = base_df['Итоговые_стены']

        part_df['ОККШЩС_ПУ_Стен'] = base_df['ПУ_Стен']
        part_df['ОККШЩС_СТО_Стен'] = base_df['СТО_Стен']
        part_df['ОККШЩС_ОРК_Стен'] = base_df['ОРК_Стен']

        part_df['ОККШЩС_СПО_Стен'] = base_df['СПО_Стен']
        part_df['ОККШЩС_ДШС_Стен'] = base_df['ДШС_Стен']
        part_df['ОККШЩС_ВОУ_Стен'] = base_df['ВОУ_Стен']


        part_df['ОККШЩС_ПУ_Уровень'] = base_df['ПУ_Уровень']
        part_df['ОККШЩС_СТО_Уровень'] = base_df['СТО_Уровень']
        part_df['ОККШЩС_ОРК_Уровень'] = base_df['ОРК_Уровень']

        part_df['ОККШЩС_СПО_Уровень'] = base_df['СПО_Уровень']
        part_df['ОККШЩС_ДШС_Уровень'] = base_df['ДШС_Уровень']
        part_df['ОККШЩС_ВОУ_Уровень'] = base_df['ВОУ_Уровень']


        part_df['ОККШЩС_ПУ_Значение'] = base_df['ПУ_Значение']
        part_df['ОККШЩС_СТО_Значение'] = base_df['СТО_Значение']
        part_df['ОККШЩС_ОРК_Значение'] = base_df['ОРК_Значение']

        part_df['ОККШЩС_СПО_Значение'] = base_df['СПО_Значение']
        part_df['ОККШЩС_ДШС_Значение'] = base_df['ДШС_Значение']
        part_df['ОККШЩС_ВОУ_Значение'] = base_df['ВОУ_Значение']

        out_answer_df = pd.concat([out_answer_df, answers_df], axis=1)  # Датафрейм для проверки

        # Делаем свод  по  шкалам
        dct_svod_sub = {'ПУ_Стен': 'ПУ_Уровень',
                        'СТО_Стен': 'СТО_Уровень',
                        'ОРК_Стен': 'ОРК_Уровень',

                        'СПО_Стен': 'СПО_Уровень',
                        'ДШС_Стен': 'ДШС_Уровень',
                        'ВОУ_Стен': 'ВОУ_Уровень',
                        }

        dct_rename_svod_sub = {
            'ПУ_Стен': 'Уровень шкалы Поддерживающий учитель',
            'СТО_Стен': 'Уровень шкалы Сотрудничество с одноклассниками',
            'ОРК_Стен': 'Уровень шкалы Организация работы в классе',

            'СПО_Стен': 'Уровень шкалы Соперничество с одноклассниками',
            'ДШС_Стен': 'Уровень шкалы Давление школьной среды',
            'ВОУ_Стен': 'Уровень шкалы Вовлеченность одноклассников в учебу',
        }

        lst_sub = ['очень низкий', 'ниже среднего', 'средний','выше среднего','очень высокий']

        base_svod_sub_df = create_union_svod(base_df, dct_svod_sub, dct_rename_svod_sub, lst_sub)

        avg_pu = round(base_df['ПУ_Стен'].mean(), 2)
        avg_sto = round(base_df['СТО_Стен'].mean(), 2)
        avg_ork = round(base_df['ОРК_Стен'].mean(), 2)

        avg_spo = round(base_df['СПО_Стен'].mean(), 2)
        avg_dshs = round(base_df['ДШС_Стен'].mean(), 2)
        avg_vou = round(base_df['ВОУ_Стен'].mean(), 2)

        avg_dct = {'Средний стен шкалы Поддерживающий учитель ': avg_pu,
                   'Среднее стен шкалы Сотрудничество с одноклассниками': avg_sto,
                   'Среднее стен шкалы Организация работы в классе': avg_ork,

                   'Среднее стен шкалы Соперничество с одноклассниками': avg_spo,
                   'Среднее стен шкалы Давление школьной среды': avg_dshs,
                   'Среднее стен шкалы Вовлеченность одноклассников в учебу': avg_vou,
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
            'ПУ_Уровень': 'ПУ',
            'СТО_Уровень': 'СТО',
            'ОРК_Уровень': 'ОРК',

            'СПО_Уровень': 'СПО',
            'ДШС_Уровень': 'ДШС',
            'ВОУ_Уровень': 'ВОУ',
        }

        out_dct = create_list_on_level(base_df, out_dct, lst_sub, dct_prefix)

        """
                        Сохраняем в зависимости от необходимости делать своды по определенным колонкам
                        """
        if len(lst_svod_cols) == 0:
            return out_dct, part_df
        else:
            out_dct = create_result_okk_shumakova(base_df, out_dct, lst_svod_cols)
            return out_dct, part_df



    except NotReqColumnOKKSSS:
        messagebox.showerror('Лахеcис',
                             f'При обработке вопросов теста Опросник Климат в классе Шумакова Щебланова Сорокова обнаружено отсутствие обязательных колонок:\n'
                             f'{diff_req_cols}\n В таблице с ответами обязательно должна быть колонка с названием Возраст'
                             f'Используйте при создании Яндекс-формы написание вопросов из руководства пользователя программы Лахесис.')
    except BadValueAgeOKKSSS:
        messagebox.showerror('Лахеcис',
                             f'При обработке вопросов теста Опросник Климат в классе Шумакова Щебланова Сорокова в колонке Пол обнаружены значения отличающиеся от допустимых:\n'
                             f'{diff_sex}\n В колонке Пол допустимы только значения Мужской и Женский.'
                             f'Используйте при создании Яндекс-формы написание вопросов из руководства пользователя программы Лахесис.')
    except BadOrderOKKSSS:
        messagebox.showerror('Лахеcис',
                             f'При обработке вопросов теста Опросник Климат в классе Шумакова Щебланова Сорокова обнаружены неправильные вопросы. Проверьте названия колонок с вопросами:\n'
                             f'{error_order_message[:5000]}\n'
                             f'Используйте при создании Яндекс-формы написание вопросов из руководства пользователя программы Лахесис.')
    except BadValueOKKSSS:
        messagebox.showerror('Лахеcис',
                             f'При обработке вопросов теста Опросник Климат в классе Шумакова Щебланова Сорокова обнаружены неправильные варианты ответов. Проверьте ответы на указанных строках:\n'
                             f'{error_message[:5000]}\n'
                             f'Используйте при создании Яндекс-формы написание вариантов ответа из руководства пользователя программы Лахесис.')


    except BadCountColumnsOKKSSS:
        messagebox.showerror('Лахеcис',
                             f'Проверьте количество колонок с ответами на тест Опросник Климат в классе Шумакова Щебланова Сорокова\n'
                             f'Должно быть 39 колонок с ответами')








