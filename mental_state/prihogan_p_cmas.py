"""
Скрипт для обработки результатов теста Шкала явной тревожности для подростков CMAS А.М. Прихожан
"""

import pandas as pd
import re
from tkinter import messagebox
from lachesis_support_functions import round_mean_two,calc_count_scale,create_union_svod, create_list_on_level

class BadOrderCMASPP(Exception):
    """
    Исключение для обработки случая когда колонки не совпадают
    """
    pass


class BadValueCMASPP(Exception):
    """
    Исключение для неправильных значений в вариантах ответов
    """
    pass

class BadCountColumnsCMASPP(Exception):
    """
    Исключение для обработки случая если количество колонок не равно 65
    """
    pass

class NotReqColumn(Exception):
    """
    Исключение для обработки случая когда нет обязательных колонок Пол
    """
    pass

class BadValueSexCMASPP(Exception):
    """
    Исключение для обработки случая когда в колонке Пол есть значения отличающиеся от Мужской или Женский
    """
    pass

class BadValueAgeCMASPP(Exception):
    """
    Исключение для обработки случая когда в колонке Возраст есть значения отличающиеся от 13 лет, 14 лет, 15 лет, 16 лет
    """
    pass





def processing_p_cmas_prihog(base_df: pd.DataFrame, answers_df: pd.DataFrame, lst_svod_cols:list):
    """
    Функция для обработки
    :param base_df: часть датафрейма с описательными колонками
    :param answers_df: часть датафрейма с ответами
    :param lst_svod_cols:  список с колонками по которым нужно делать свод
    """
    out_answer_df = base_df.copy()  # делаем копию для последующего соединения с сырыми ответами
    if len(answers_df.columns) != 65:  # проверяем количество колонок с вопросами
        raise BadCountColumnsCMASPP

    # очищаем названия колонок от возможных сочетаний .1 которые добавляет пандас при одинаковых колонках
    clean_df_lst = []
    for name_column in answers_df.columns:
        clean_name = re.sub(r'.\d+$', '', name_column)
        clean_df_lst.append(clean_name)

    answers_df.columns = clean_df_lst


    # Проверяем наличие колонок Пол и Возраст
    diff_req_cols = {'Пол', 'Возраст'}.difference(set(base_df.columns))
    if len(diff_req_cols) != 0:
        raise NotReqColumn

    # на случай пустых
    base_df['Пол'].fillna('Не заполнено', inplace=True)
    # очищаем от лишних пробелов
    base_df['Пол'] = base_df['Пол'].apply(str.strip)

    base_df['Возраст'].fillna('Не заполнено', inplace=True)
    # очищаем от лишних пробелов
    base_df['Возраст'] = base_df['Возраст'].apply(str.strip)

    # Проверяем на пол
    diff_sex = set(base_df['Пол'].unique()).difference({'Мужской', 'Женский'})
    if len(diff_sex) != 0:
        raise BadValueSexCMASPP

    # Проверяем на возраст
    diff_age = set(base_df['Возраст'].unique()).difference({'13 лет', '14 лет', '15 лет', '16 лет'})
    if len(diff_age) != 0:
        raise BadValueAgeCMASPP

    lst_check_cols = ['Тебе трудно сосредоточиться на работе, выполнении задания',
                      'Ты можешь долго работать, не уставая',
                      'Тебя раздражает, если за тобой наблюдают, когда ты что-нибудь делаешь',
                      'Ты легко краснеешь',
                      'Не все люди, которых ты знаешь, тебе нравятся',
                      'Ты редко чувствуешь сильное сердцебиение',
                      'Временами ты чувствуешь, что ты хуже других',
                      'Ты очень редко смущаешься',
                      'Даже если все хорошо, ты ощущаешь какое-то беспокойство: вдруг произойдет что-то плохое',
                      'Иногда тебе хочется убежать, скрыться, хотя никаких видимых причин для этого нет',

                      'Нередко ты говоришь о том, в чем не разбираешься',
                      'Ты уверен, что ни в чем не хуже других',
                      'Ты часто чувствуешь, что другие люди недовольны тобой, осуждают тебя, хотя и не показывают этого',
                      'Ты почти ничего не боишься',
                      'Тебе нравится думать о своем будущем',
                      'Тебе очень трудно принять решение',
                      'Ты часто ловишь себя на том, что тебя что-то беспокоит, а что – непонятно',
                      'Ты всегда соблюдаешь правила',
                      'Тебя трудно разозлить, вывести из себя',
                      'Ты часто чувствуешь, что тебе трудно дышать',
                      '',
                      '',
                      '',
                      '',
                      '',
                      '',
                      '',
                      '',
                      '',
                      '',
                      ]