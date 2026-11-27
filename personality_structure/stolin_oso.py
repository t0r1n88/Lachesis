"""
Скрипт для обработки результатов Опросник ксенофобских установок Гурина
"""

import pandas as pd
import re
from tkinter import messagebox
from lachesis_support_functions import round_mean_two,calc_count_scale,create_union_svod, create_list_on_level

class BadOrderOSOSP(Exception):
    """
    Исключение для обработки случая когда колонки не совпадают
    """
    pass


class BadValueOSOSP(Exception):
    """
    Исключение для неправильных значений в вариантах ответов
    """
    pass

class BadCountColumnsOSOSP(Exception):
    """
    Исключение для обработки случая если количество колонок не равно 57
    """
    pass


def calc_value_gs(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [2, 5, 23, 33, 37, 42, 46, 48, 52, 53, 57,
              6, 9, 13, 14, 16, 18, 30, 35, 38, 39, 41, 43, 44, 45, 49, 50, 56]
    lst_neg = [6, 9, 13, 14, 16, 18, 30, 35, 38, 39, 41, 43, 44, 45, 49, 50, 56]
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


def calc_percent_gs(value):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """
    result = 0

    if value == 0:
        result = 0
    elif value == 1:
        result = 0.67
    elif value ==2:
        result =3.00
    elif value ==3:
        result =5.33
    elif value ==4:
        result =6.33
    elif value ==5:
        result =9.00
    elif value ==6:
        result =13.00
    elif value ==7:
        result =16.00
    elif value ==8:
        result =21.33
    elif value ==9:
        result =26.67
    elif value ==10:
        result =32.33
    elif value ==11:
        result =38.33
    elif value ==12:
        result =49.00
    elif value ==13:
        result =55.33
    elif value ==14:
        result =62.67
    elif value ==15:
        result =69.33
    elif value ==16:
        result =74.33
    elif value ==17:
        result =80.00
    elif value ==18:
        result =85.00
    elif value ==19:
        result =88.00
    elif value ==20:
        result =90.67
    elif value ==21:
        result =93.33
    elif value ==22:
        result =96.00
    elif value ==23:
        result =96.67
    elif value ==24:
        result =98.00
    elif value ==25:
        result =98.33
    elif value ==26:
        result =98.67
    elif value ==27:
        result =99.67
    elif value ==28:
        result =100


    result = round(result)
    return f'{result}%'

def calc_level(value:str):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """
    value = value.replace('%','')

    result = int(value)

    if result <= 49:
        return f'признак не выражен'
    elif 50 <= result <= 74:
        return f'признак выражен'
    else:
        return f'признак ярко выражен'


def calc_value_su(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [2, 23, 53, 57,
              8, 13, 25, 27, 31, 35, 38, 39, 40, 41, 50]
    lst_neg = [8, 13, 25, 27, 31, 35, 38, 39, 40, 41, 50]
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

def calc_percent_su(value):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """
    result = 0

    if value == 0:
        result = 1.67
    elif value == 1:
        result =4.00
    elif value ==2:
        result =6.00
    elif value ==3:
        result =9.33
    elif value ==4:
        result =16.00
    elif value ==5:
        result =25.33
    elif value ==6:
        result =34.00
    elif value ==7:
        result =44.67
    elif value == 8:
        result =58.67
    elif value ==9:
        result =71.33
    elif value ==10:
        result =80.00
    elif value ==11:
        result =86.67
    elif value ==12:
        result =91.33
    elif value ==13:
        result =63.67
    elif value ==14:
        result =99.67
    else:
        result =100

    result = round(result)
    return f'{result}%'


def calc_value_as(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [12, 18, 28, 29, 37, 46, 48, 54,
              4, 9, 11, 16, 19, 24, 45, 56]
    lst_neg = [4, 9, 11, 16, 19, 24, 45, 56]
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

def calc_percent_as(value):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """
    result = 0

    if value == 0:
        result =0.33
    elif value == 1:
        result =3.67
    elif value ==2:
        result =9.00
    elif value ==3:
        result =16.00
    elif value ==4:
        result =21.67
    elif value ==5:
        result =28.00
    elif value ==6:
        result =37.33
    elif value ==7:
        result =47.00
    elif value ==8:
        result =58.33
    elif value ==9:
        result =69.67
    elif value ==10:
        result =77.33
    elif value ==11:
        result =86.00
    elif value ==12:
        result =90.67
    elif value ==13:
        result =96.67
    elif value ==14:
        result =98.33
    elif value ==15:
        result =99.67
    else:
        result =100

    result = round(result)
    return f'{result}%'





def processing_oso_stolin_pan(base_df: pd.DataFrame, answers_df: pd.DataFrame, lst_svod_cols:list):
    """
    Функция для обработки
    :param base_df: часть датафрейма с описательными колонками
    :param answers_df: часть датафрейма с ответами
    :param lst_svod_cols:  список с колонками по которым нужно делать свод
    """
    out_answer_df = base_df.copy()  # делаем копию для последующего соединения с сырыми ответами
    if len(answers_df.columns) != 57:  # проверяем количество колонок с вопросами
        raise BadCountColumnsOSOSP

    # очищаем названия колонок от возможных сочетаний .1 которые добавляет пандас при одинаковых колонках
    clean_df_lst = []
    for name_column in answers_df.columns:
        clean_name = re.sub(r'.\d+$', '', name_column)
        clean_df_lst.append(clean_name)

    answers_df.columns = clean_df_lst

    lst_check_cols = ['Думаю, что большинство моих знакомых относится ко мне с симпатией',
                      'Мои слова не так уж часто расходятся с делом',
                      'Думаю, что многие видят во мне что-то сходное с собой',
                      'Когда я пытаюсь себя оценить, я прежде всего вижу свои недостатки',
                      'Думаю, что как личность я вполне могу быть притягательным для других',
                      'Когда я вижу себя глазами любящего меня человека, меня неприятно поражает то, насколько мой образ далек от действительности',
                      'Мое «Я» всегда мне интересно',
                      'Я считаю, что иногда не грех пожалеть самого себя',
                      'В моей жизни есть или, по крайней мере, были люди, с которыми я был чрезвычайно близок',
                      'Собственное уважение мне еще надо заслужить',

                      'Бывало, и не раз, что я сам себя остро ненавидел',
                      'Я вполне доверяю своим внезапно возникшим желаниям',
                      'Я сам хотел во многом себя переделать',
                      'Мое собственное «Я» не представляется мне чем-то достойным глубокого внимания',
                      'Я искренне хочу, чтобы у меня было все хорошо в жизни',
                      'Если я и отношусь к кому-нибудь с укоризной, то прежде всего к самому себе',
                      'Случайному знакомому я скорее всего покажусь человеком приятным',
                      'Чаще всего я одобряю свои планы и поступки',
                      'Собственные слабости вызывают у меня что-то наподобие презрения',
                      'Если бы я раздвоился, то мне было бы довольно интересно общаться со своим двойником',

                      'Некоторые свои качества я ощущаю как посторонние, чужие мне',
                      'Вряд ли кто-либо сможет почувствовать свое сходство со мной',
                      'У меня достаточно способностей и энергии воплотить в жизнь задуманное',
                      'Часто я не без издевки подшучиваю над собой',
                      'Самое разумное, что может сделать человек в своей жизни — это подчиниться собственной судьбе',
                      'Посторонний человек, на первый взгляд, найдет во мне много отталкивающего',
                      'К сожалению, если я и сказал что-то, это не значит, что именно так и буду поступать',
                      'Свое отношение к самому себе можно назвать дружеским',
                      'Быть снисходительным к собственным слабостям вполне естественно',
                      'У меня не получается быть для любимого человека интересным длительное время',

                      'В глубине души я бы хотел, чтобы со мной произошло что-то катастрофическое',
                      'Вряд ли я вызываю симпатию у большинства моих знакомых',
                      'Мне бывает очень приятно увидеть себя глазами любящего меня человека',
                      'Когда у меня возникает какое-либо желание, я прежде всего спрашиваю себя, разумно ли это',
                      'Иногда мне кажется, что, если бы какой-то мудрый человек смог увидеть меня насквозь, он бы тут же понял, какое я ничтожество',
                      'Временами я сам собой восхищаюсь',
                      'Можно сказать, что я ценю себя достаточно высоко',
                      'В глубине души я никак не могу поверить, что я действительно взрослый человек',
                      'Без посторонней помощи я мало что могу сделать',
                      'Иногда я сам себя плохо понимаю',

                      'Мне очень мешает недостаток энергии, воли и целеустремленности',
                      'Думаю, что другие в целом оценивают меня достаточно высоко',
                      'В моей личности есть, наверное, что-то такое, что способно вызывать у других неприязнь',
                      'Большинство моих знакомых не принимают меня уж так всерьез',
                      'Сам у себя я довольно часто вызываю чувство раздражения',
                      'Я вполне могу сказать, что унижаю себя сам',
                      'Даже мои негативные черты не кажутся мне чужими',
                      'В целом, меня устраивает то, какой я есть',
                      'Вряд ли меня можно любить по-настоящему',
                      'Моим мечтам и планам не хватает реалистичности',

                      'Если бы мое второе «Я» существовало, то для меня это был бы самый скучный партнер по общению',
                      'Думаю, что мог бы найти общий язык с любым разумным и знающим человеком',
                      'То, что во мне происходит, как правило, мне понятно',
                      'Мои достоинства вполне перевешивают мои недостатки',
                      'Вряд ли найдется много людей, которые обвинят меня в отсутствии совести',
                      'Когда со мной случаются неприятности, как правило, я говорю: «И поделом тебе»',
                      'Я могу сказать, что в целом я контролирую свою судьбу'
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
        raise BadOrderOSOSP

    valid_values = ['да','нет']

    # Проверяем, есть ли значения, отличающиеся от указанных в списке
    lst_error_answers = []  # список для хранения строк где найдены неправильные ответы

    for i in range(57):
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
        raise BadValueOSOSP

    base_df['ГС_Сырое_Значение'] = answers_df.apply(calc_value_gs, axis=1)
    base_df['ГС_Накопленная_частота_%'] = base_df['ГС_Сырое_Значение'].apply(calc_percent_gs)
    base_df['ГС_Уровень'] = base_df['ГС_Накопленная_частота_%'].apply(calc_level)

    base_df['СУ_Сырое_Значение'] = answers_df.apply(calc_value_su, axis=1)
    base_df['СУ_Накопленная_частота_%'] = base_df['СУ_Сырое_Значение'].apply(calc_percent_su)
    base_df['СУ_Уровень'] = base_df['СУ_Накопленная_частота_%'].apply(calc_level)

    base_df['АС_Сырое_Значение'] = answers_df.apply(calc_value_as, axis=1)
    base_df['АС_Накопленная_частота_%'] = base_df['АС_Сырое_Значение'].apply(calc_percent_as)
    base_df['АС_Уровень'] = base_df['АС_Накопленная_частота_%'].apply(calc_level)




    base_df.to_excel('data/res.xlsx')





