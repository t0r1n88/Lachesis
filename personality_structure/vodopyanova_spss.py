"""
Скрипт для обработки результатов Стратегия преодоления стрессовых ситуаций, SACS Хобфолл С., 1994
Адаптация Н.Е. Водопьянова, Е.С. Старченкова

"""

import pandas as pd
import re
from tkinter import messagebox
from lachesis_support_functions import round_mean_two,calc_count_scale,create_union_svod, create_list_on_level

class BadOrderSPSSVS(Exception):
    """
    Исключение для обработки случая когда колонки не совпадают
    """
    pass


class BadValueSPSSVS(Exception):
    """
    Исключение для неправильных значений в вариантах ответов
    """
    pass

class BadCountColumnsSPSSVS(Exception):
    """
    Исключение для обработки случая если количество колонок не равно 54
    """
    pass


def calc_value_ad(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [1,10,19,28,37,46]
    lst_neg = [28,46]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_pr:
            if idx not in lst_neg:
                value_forward += value
            else:
                if value == 1:
                    value_forward += 5
                elif value == 2:
                    value_forward += 4
                elif value == 3:
                    value_forward += 3
                elif value == 4:
                    value_forward += 2
                elif value == 5:
                    value_forward += 1
    return value_forward

def calc_level_ad(value):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """
    if 6<= value <=17:
        return f'низкая степень'
    elif 18<= value <=22:
        return f'средняя степень'
    else:
        return f'высокая степень'

def calc_value_vsk(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [2,11,20,29,38,47]
    lst_neg = []
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_pr:
            if idx not in lst_neg:
                value_forward += value
            else:
                if value == 1:
                    value_forward += 5
                elif value == 2:
                    value_forward += 4
                elif value == 3:
                    value_forward += 3
                elif value == 4:
                    value_forward += 2
                elif value == 5:
                    value_forward += 1
    return value_forward


def calc_level_vsk(value):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """
    if 6<= value <=21:
        return f'низкая степень'
    elif 22<= value <=25 :
        return f'средняя степень'
    else:
        return f'высокая степень'

def calc_value_psp(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [3,12,21,30,39,48]
    lst_neg = []
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_pr:
            if idx not in lst_neg:
                value_forward += value
            else:
                if value == 1:
                    value_forward += 5
                elif value == 2:
                    value_forward += 4
                elif value == 3:
                    value_forward += 3
                elif value == 4:
                    value_forward += 2
                elif value == 5:
                    value_forward += 1
    return value_forward


def calc_level_psp(value):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """
    if 6<= value <=19:
        return f'низкая степень'
    elif 20<= value <=24 :
        return f'средняя степень'
    else:
        return f'высокая степень'



def calc_value_od(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [4,13,22,31,40,49]
    lst_neg = []
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_pr:
            if idx not in lst_neg:
                value_forward += value
            else:
                if value == 1:
                    value_forward += 5
                elif value == 2:
                    value_forward += 4
                elif value == 3:
                    value_forward += 3
                elif value == 4:
                    value_forward += 2
                elif value == 5:
                    value_forward += 1
    return value_forward


def calc_level_od(value):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """
    if 6<= value <=17:
        return f'низкая степень'
    elif 18<= value <=23 :
        return f'средняя степень'
    else:
        return f'высокая степень'


def calc_value_id(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [5,14,23,32,41,50]
    lst_neg = [50]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_pr:
            if idx not in lst_neg:
                value_forward += value
            else:
                if value == 1:
                    value_forward += 5
                elif value == 2:
                    value_forward += 4
                elif value == 3:
                    value_forward += 3
                elif value == 4:
                    value_forward += 2
                elif value == 5:
                    value_forward += 1
    return value_forward


def calc_level_id(value):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """
    if 6<= value <=15:
        return f'низкая степень'
    elif 16<= value <=19 :
        return f'средняя степень'
    else:
        return f'высокая степень'


def calc_value_i(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [6,15,24,33,42,51]
    lst_neg = []
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_pr:
            if idx not in lst_neg:
                value_forward += value
            else:
                if value == 1:
                    value_forward += 5
                elif value == 2:
                    value_forward += 4
                elif value == 3:
                    value_forward += 3
                elif value == 4:
                    value_forward += 2
                elif value == 5:
                    value_forward += 1
    return value_forward


def calc_level_i(value):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """
    if 6<= value <=12:
        return f'низкая степень'
    elif 13<= value <=17 :
        return f'средняя степень'
    else:
        return f'высокая степень'

def calc_value_nd(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [7,16,25,34,43,52]
    lst_neg = []
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_pr:
            if idx not in lst_neg:
                value_forward += value
            else:
                if value == 1:
                    value_forward += 5
                elif value == 2:
                    value_forward += 4
                elif value == 3:
                    value_forward += 3
                elif value == 4:
                    value_forward += 2
                elif value == 5:
                    value_forward += 1
    return value_forward


def calc_level_nd(value):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """
    if 6<= value <=16:
        return f'низкая степень'
    elif 17<= value <=23 :
        return f'средняя степень'
    else:
        return f'высокая степень'


def calc_value_asd(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [8,17,26,35,44,53]
    lst_neg = []
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_pr:
            if idx not in lst_neg:
                value_forward += value
            else:
                if value == 1:
                    value_forward += 5
                elif value == 2:
                    value_forward += 4
                elif value == 3:
                    value_forward += 3
                elif value == 4:
                    value_forward += 2
                elif value == 5:
                    value_forward += 1
    return value_forward


def calc_level_asd(value):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """
    if 6<= value <=14:
        return f'низкая степень'
    elif 15<= value <=19 :
        return f'средняя степень'
    else:
        return f'высокая степень'


def calc_value_agd(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [9,18,27,36,45,54]
    lst_neg = []
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_pr:
            if idx not in lst_neg:
                value_forward += value
            else:
                if value == 1:
                    value_forward += 5
                elif value == 2:
                    value_forward += 4
                elif value == 3:
                    value_forward += 3
                elif value == 4:
                    value_forward += 2
                elif value == 5:
                    value_forward += 1
    return value_forward


def calc_level_agd(value):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """
    if 6<= value <=13:
        return f'низкая степень'
    elif 14<= value <= 18 :
        return f'средняя степень'
    else:
        return f'высокая степень'





def processing_spss_vod_star(base_df: pd.DataFrame, answers_df: pd.DataFrame, lst_svod_cols:list):
    """
    Функция для обработки
    :param base_df: часть датафрейма с описательными колонками
    :param answers_df: часть датафрейма с ответами
    :param lst_svod_cols:  список с колонками по которым нужно делать свод
    """
    out_answer_df = base_df.copy()  # делаем копию для последующего соединения с сырыми ответами
    if len(answers_df.columns) != 54:  # проверяем количество колонок с вопросами
        raise BadCountColumnsSPSSVS

    # очищаем названия колонок от возможных сочетаний .1 которые добавляет пандас при одинаковых колонках
    clean_df_lst = []
    for name_column in answers_df.columns:
        clean_name = re.sub(r'.\d+$', '', name_column)
        clean_df_lst.append(clean_name)

    answers_df.columns = clean_df_lst

    lst_check_cols =['В любых сложных ситуациях вы не сдаетесь',
                     'Объединяетесь с другими людьми, чтобы вместе разрешить ситуацию',
                     'Советуетесь с друзьями или близкими о том, что бы они сделали, оказавшись в вашем положении',
                     'Вы всегда очень тщательно взвешиваете возможные варианты решений (лучше быть осторожным, чем подвергать себя риску)',
                     'Вы полагаетесь на свою интуицию',
                     'Как правило, вы откладываете решение возникшей проблемы в надежде, что она разрешится сама',
                     'Стараетесь держать все под контролем, хотя и не показываете этого другим',
                     'Вы полагаете, что иногда необходимо действовать столь быстро и решительно, чтобы застать других врасплох',
                     'Решая неприятные проблемы, выходите из себя и можете наломать немало дров',
                     'Когда кто-либо из близких поступает с вами несправедливо, вы пытаетесь вести себя так, чтобы они не почувствовали, что вы расстроены или обижены',

                     'Стараетесь помочь другим при решении ваших общих проблем',
                     'Не стесняетесь при необходимости обращаться к другим людям за помощью или поддержкой',
                     'Без необходимости не выкладываетесь полностью, предпочитая экономить свои силы',
                     'Вы часто удивляетесь, что наиболее правильным является то решение, которое первым пришло в голову',
                     'Иногда предпочитаете заняться чем угодно, лишь бы забыть о неприятном деле, которое нужно делать',
                     'Для достижения своих целей вам часто приходиться подыгрывать другим или подстраиваться под других людей (несколько кривить душой)',
                     'В определенных ситуациях вы ставите свои личные интересы превыше всего, даже если это пойдет во вред другим',
                     'Как правило, препятствия для решения ваших проблем или достижения желаемого сильно выводят вас из себя, можно сказать, что они просто бесят вас',
                     'Вы считаете, что в сложных ситуациях лучше действовать самому, чем ждать, когда ее будут решать другие',
                     'Находясь в трудной ситуации, вы раздумываете о том, как бы поступили в этом случае другие люди',

                     'В трудные минуты для вас очень важна эмоциональная поддержка близких людей',
                     'Считаете, что во всех случаях лучше семь раз отмерить, прежде чем отрезать',
                     'Вы часто проигрываете из-за того, что не полагаетесь на свои предчувствия',
                     'Вы не тратите свою энергию на разрешение того, что, возможно, само по себе рассеется',
                     'Позволяете другим людям думать, что они могут повлиять на вас, но на самом деле вы — крепкий орешек и никому не позволяете манипулировать собой',
                     'Считаете, что полезно демонстрировать свою власть и превосходство для укрепления собственного авторитета',
                     'Вас можно назвать вспыльчивым человеком',
                     'Вам бывает достаточно трудно ответить отказом на чьи-либо требования или просьбы',
                     'Вы полагаете, что в критических ситуациях лучше действовать сообща с другими',
                     'Вы считаете, что на душе может стать легче, если поделиться с другими своими переживаниями',

                     'Ничего не принимаете на веру, так как полагаете, что в любой ситуации могут быть «подводные камни»',
                     'Ваша интуиция вас никогда не подводит',
                     'В конфликтной ситуации убеждаете себя и других, что проблема не стоит и выеденного яйца',
                     'Иногда вам приходится немного манипулировать людьми (решать свои проблемы, невзирая на интересы других)',
                     'Бывает очень выгодно поставить другого человека в неловкое и зависимое положение',
                     'Вы считаете, что лучше решительно и быстро дать отпор тем, кто не согласен с вашим мнением, чем тянуть кота за хвост',
                     'Вы легко и спокойно можете защитить себя от несправедливых действий со стороны других, в случае необходимости сказать «нет» в ситуации эмоционального давления',
                     'Вы считаете, что общение с другими людьми обогатит ваш жизненный опыт',
                     'Вы полагаете, что поддержка других людей очень помогает вам в трудных ситуациях',
                     'В трудных ситуациях вы долго готовитесь и предпочитаете сначала успокоиться, а потом уже действовать',

                     'В сложных ситуациях лучше следовать первому импульсу, чем долго взвешивать возможные варианты',
                     'По возможности избегаете решительных действий, требующих большой напряженности и ответственности за последствия',
                     'Для достижения своих заветных целей не грех и немного полукавить',
                     'Ищете слабости других людей и используете их со своей выгодой',
                     'Грубость и глупости других людей часто приводят вас в ярость (выводят вас из себя)',
                     'Вы испытываете неловкость, когда вас хвалят или говорят комплименты',
                     'Считаете, что совместные усилия с другими принесут больше пользы в любых ситуациях (при решении любых задач)',
                     'Вы уверены, что в трудных ситуациях вы всегда найдете понимание и сочувствие со стороны близких людей',
                     'Вы полагаете, что во всех случаях нужно следовать принципу «тише едешь, дальше будешь»',
                     'Действие под влиянием первого порыва всегда хуже, чем трезвый расчет',

                     'В конфликтных ситуациях предпочитаете найти какие-либо важные и неотложные дела, позволяя другим заняться решением проблемы или надеясь, что время все расставит на свои места',
                     'Вы полагаете, что хитростью можно добиться порою больше, чем действуя напрямую',
                     'Цель оправдывает средства',
                     'В значимых и конфликтных ситуациях вы бываете агрессивны'
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
        raise BadOrderSPSSVS

    # словарь для замены слов на числа
    dct_replace_value = {'нет, это совсем не так': 1,
                         'скорее нет, чем да': 2,
                         'затрудняюсь ответить': 3,
                         'скорее да, чем нет': 4,
                         'да, совершенно верно': 5,
                         }
    valid_values = [1, 2, 3,4,5]
    answers_df.replace(dct_replace_value, inplace=True)  # заменяем слова на цифры для подсчетов
    # Проверяем, есть ли значения, отличающиеся от указанных в списке
    lst_error_answers = []  # список для хранения строк где найдены неправильные ответы

    for i in range(54):
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
        raise BadValueSPSSVS

    base_df['АД_Значение'] = answers_df.apply(calc_value_ad, axis=1)
    base_df['АД_Уровень'] = base_df['АД_Значение'].apply(calc_level_ad)

    base_df['ВСК_Значение'] = answers_df.apply(calc_value_vsk, axis=1)
    base_df['ВСК_Уровень'] = base_df['ВСК_Значение'].apply(calc_level_vsk)

    base_df['ПСП_Значение'] = answers_df.apply(calc_value_psp, axis=1)
    base_df['ПСП_Уровень'] = base_df['ПСП_Значение'].apply(calc_level_psp)

    base_df['ОД_Значение'] = answers_df.apply(calc_value_od, axis=1)
    base_df['ОД_Уровень'] = base_df['ОД_Значение'].apply(calc_level_od)

    base_df['ИД_Значение'] = answers_df.apply(calc_value_id, axis=1)
    base_df['ИД_Уровень'] = base_df['ИД_Значение'].apply(calc_level_id)

    base_df['И_Значение'] = answers_df.apply(calc_value_i, axis=1)
    base_df['И_Уровень'] = base_df['И_Значение'].apply(calc_level_i)

    base_df['НД_Значение'] = answers_df.apply(calc_value_nd, axis=1)
    base_df['НД_Уровень'] = base_df['НД_Значение'].apply(calc_level_nd)

    base_df['АСД_Значение'] = answers_df.apply(calc_value_asd, axis=1)
    base_df['АСД_Уровень'] = base_df['АСД_Значение'].apply(calc_level_asd)

    base_df['АГД_Значение'] = answers_df.apply(calc_value_agd, axis=1)
    base_df['АГД_Уровень'] = base_df['АГД_Значение'].apply(calc_level_agd)


    base_df.to_excel('data/res.xlsx')

