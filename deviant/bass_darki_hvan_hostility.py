"""
Скрипт для обработки результатов теста Опросник враждебности Басса-Дарки, BDHI Хван


"""
import pandas as pd
import re
from tkinter import messagebox
from lachesis_support_functions import round_mean,calc_count_scale,create_list_on_level


class BadOrderBHDI(Exception):
    """
    Исключение для обработки случая когда колонки не совпадают
    """
    pass


class BadValueBHDI(Exception):
    """
    Исключение для неправильных значений в вариантах ответов
    """
    pass

class BadCountColumnsBHDI(Exception):
    """
    Исключение для обработки случая если количество колонок не равно 75
    """
    pass

def calc_value_fa(row):
    """
    Функция для подсчета значения шкалы Физическая агрессия
    :return: число
    """
    lst_pr = [1,25,33,48,55,62,68,9,17,41]
    lst_plus = [1,25,33,48,55,62,68]

    value_forward = 0 # счетчик прямых ответов

    for idx, value in enumerate(row):
        if idx +1 in lst_pr:
            if idx + 1 in lst_plus:
                if value == 'да':
                    value_forward += 1
            else:
                if value == 'нет':
                    value_forward += 1

    return value_forward * 10



def calc_value_ka(row):
    """
    Функция для подсчета значения шкалы Косвенная агрессия
    :return: число
    """
    lst_pr = [2,18,34,42,56,63,10,26,49]
    lst_plus = [2,18,34,42,56,63]

    value_forward = 0 # счетчик прямых ответов

    for idx, value in enumerate(row):
        if idx +1 in lst_pr:
            if idx + 1 in lst_plus:
                if value == 'да':
                    value_forward += 1
            else:
                if value == 'нет':
                    value_forward += 1

    return value_forward * 8


def calc_value_r(row):
    """
    Функция для подсчета значения шкалы Раздражение
    :return: число
    """
    lst_pr = [3,19,27,43,50,57,64,72,11,35,69]
    lst_plus = [3,19,27,43,50,57,64,72]

    value_forward = 0 # счетчик прямых ответов

    for idx, value in enumerate(row):
        if idx +1 in lst_pr:
            if idx + 1 in lst_plus:
                if value == 'да':
                    value_forward += 1
            else:
                if value == 'нет':
                    value_forward += 1

    return value_forward * 11


def calc_value_n(row):
    """
    Функция для подсчета значения шкалы Негативизм
    :return: число
    """
    lst_pr = [4,12,20,23,36]

    value_forward = 0 # счетчик прямых ответов

    for idx, value in enumerate(row):
        if idx +1 in lst_pr:
            if value == 'да':
                value_forward += 1

    return value_forward * 20


def calc_value_o(row):
    """
    Функция для подсчета значения шкалы Обида
    :return: число
    """
    lst_pr = [5,13,21,29,37,51,58,44]
    lst_plus = [5,13,21,29,37,51,58]

    value_forward = 0 # счетчик прямых ответов

    for idx, value in enumerate(row):
        if idx +1 in lst_pr:
            if idx + 1 in lst_plus:
                if value == 'да':
                    value_forward += 1
            else:
                if value == 'нет':
                    value_forward += 1

    return value_forward * 9


def calc_value_p(row):
    """
    Функция для подсчета значения шкалы Подозрительность
    :return: число
    """
    lst_pr = [6,14,22,30,38,45,52,59,65,70]
    lst_plus = [6,14,22,30,38,45,52,59]

    value_forward = 0 # счетчик прямых ответов

    for idx, value in enumerate(row):
        if idx +1 in lst_pr:
            if idx + 1 in lst_plus:
                if value == 'да':
                    value_forward += 1
            else:
                if value == 'нет':
                    value_forward += 1

    return value_forward * 10


def calc_value_va(row):
    """
    Функция для подсчета значения шкалы Вербальная агрессия
    :return: число
    """
    lst_pr = [7,15,23,31,46,53,60,71,73,39,74,75]
    lst_plus = [7,15,23,31,46,53,60,71,73]

    value_forward = 0 # счетчик прямых ответов

    for idx, value in enumerate(row):
        if idx +1 in lst_pr:
            if idx + 1 in lst_plus:
                if value == 'да':
                    value_forward += 1
            else:
                if value == 'нет':
                    value_forward += 1

    return value_forward * 13


def calc_value_us(row):
    """
    Функция для подсчета значения шкалы Угрызение совести
    :return: число
    """
    lst_pr = [8,16,24,32,40,47,54,61,67]

    value_forward = 0 # счетчик прямых ответов

    for idx, value in enumerate(row):
        if idx +1 in lst_pr:
            if value == 'да':
                value_forward += 1

    return value_forward * 11


def calc_sten_first(value):
    """
    Функция для подсчета стена для КА ВА Н ЧВ
    :param value:
    :return:
    """
    if 0 <= value <= 19:
        return 1
    elif 20 <= value <= 30:
        return 2
    elif 31 <= value <= 41:
        return 3
    elif 42 <= value <= 52:
        return 4
    elif 53 <= value <= 63:
        return 5
    elif 64 <= value <= 74:
        return 6
    elif 75 <= value <= 85:
        return 7
    elif 86 <= value <= 96:
        return 8
    else:
        return 9

def calc_level_first(value):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """
    if 1 <= value <= 2:
        return 'низкий'
    elif 3 <= value <= 4:
        return 'средний'
    elif 5 <= value <= 6:
        return 'повышенный'
    elif value == 7:
        return 'высокий'
    else:
        return 'очень высокий'




def calc_sten_host(value):
    """
    Функция для подсчета стена для Враждебность
    :param value:
    :return:
    """
    if value == 0:
        return 1
    elif 0.1 <= value <= 14.99:
        return 2
    elif 15 <= value <= 25.99:
        return 3
    elif 26 <= value <= 36.99:
        return 4
    elif 37 <= value <= 47.99:
        return 5
    elif 48 <= value <= 58.99:
        return 6
    elif 59 <= value <= 69.99:
        return 7
    elif 70 <= value <= 80.99:
        return 8
    elif 81 <= value <= 92.99:
        return 9
    else:
        return 10

def calc_level_host(value):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """
    if 1 <= value <= 2:
        return 'низкий'
    elif 3 <= value <= 4:
        return 'средний'
    elif 5 <= value <= 6:
        return 'повышенный'
    elif value == 7:
        return 'высокий'
    else:
        return 'очень высокий'






def processing_bass_darki_hvan_hostility(result_df: pd.DataFrame, answers_df: pd.DataFrame, lst_svod_cols:list):
    """
    Функция для обработки
    :param result_df: часть датафрейма с описательными колонками
    :param answers_df: часть датафрейма с ответами
    :param lst_svod_cols:  список с колонками по которым нужно делать свод
    """
    out_answer_df = result_df.copy()  # делаем копию для последующего соединения с сырыми ответами
    if len(answers_df.columns) != 75:  # проверяем количество колонок с вопросами
        raise BadCountColumnsBHDI

    # очищаем названия колонок от возможных сочетаний .1 которые добавляет пандас при одинаковых колонках
    clean_df_lst = []
    for name_column in answers_df.columns:
        clean_name = re.sub(r'.\d+$', '', name_column)
        clean_df_lst.append(clean_name)

    answers_df.columns = clean_df_lst

    lst_check_cols = ['Временами я не могу справиться с желанием причинить вред другим','Иногда сплетничаю о людях, которых не люблю',
                      'Я легко раздражаюсь, но быстро успокаиваюсь','Если меня не попросят по-хорошему, я не выполню',
                      'Я не всегда получаю то, что мне положено','Я не знаю, что люди говорят обо мне за моей спиной',
                      'Если я не одобряю поведение друзей, я даю им это почувствовать','Когда мне случалось обмануть кого-нибудь, я испытывал мучительные угрызения совести',
                      'Мне кажется, что я не способен ударить человека','Я никогда не раздражаюсь настолько, чтобы кидаться предметами',
                      'Я всегда снисходителен к чужим недостаткам','Если мне не нравится установленное правило, мне хочется нарушить его',
                      'Другие умеют почти всегда пользоваться благоприятными обстоятельствами','Я держусь настороженно с людьми, которые относятся ко мне несколько более дружественно, чем я ожидал',
                      'Я часто бываю не согласен с людьми','Иногда мне на ум приходят мысли, которых я стыжусь',
                      'Если кто-нибудь первым ударит меня, я не отвечу ему','Когда я раздражаюсь, я хлопаю дверьми',
                      'Я гораздо более раздражителен, чем кажется','Если кто-то воображает себя начальником, я всегда поступаю ему наперекор',
                      'Меня немного огорчает моя судьба','Я думаю, что многие люди не любят меня',
                      'Я не могу удержаться от спора, если люди не согласны со мной','Люди, увиливающие от работы, должны испытывать чувство вины',
                      'Тот, кто оскорбляет меня и мою семью, напрашивается на драку','Я не способен на грубые шутки',
                      'Меня охватывает ярость, когда надо мной насмехаются','Когда люди строят из себя начальников, я делаю все, чтобы они не зазнавались',
                      'Почти каждую неделю я вижу кого-нибудь, кто мне не нравится','Довольно многие люди завидуют мне',
                      'Я требую, чтобы люди уважали меня','Меня угнетает то, что я мало делаю для своих родителей',
                      'Люди, которые постоянно изводят вас, стоят того, чтобы их "щелкнули по носу"','Я никогда не бываю мрачен от злости',
                      'Если ко мне относятся хуже, чем я того заслуживаю, я не расстраиваюсь','Если кто-то выводит меня из себя, я не обращаю внимания',
                      'Хотя я и не показываю этого, меня иногда гложет зависть','Иногда мне кажется, что надо мной смеются',
                      'Даже если я злюсь, я не прибегаю к "сильным" выражениям','Мне хочется, чтобы мои грехи были прощены',
                      'Я редко даю сдачи, даже если кто-нибудь ударит меня','Когда получается не, по-моему, я иногда обижаюсь',
                      'Иногда люди раздражают меня одним своим присутствием','Нет людей, которых бы я по-настоящему ненавидел',
                      'Мой принцип: "Никогда не доверять "чужакам"','Если кто-нибудь раздражает меня, я готов сказать, что я о нем думаю',
                      'Я делаю много такого, о чем впоследствии жалею','Если я разозлюсь, я могу ударить кого-нибудь',
                      'С детства я никогда не проявлял вспышек гнева','Я часто чувствую себя как пороховая бочка, готовая взорваться',
                      'Если бы все знали, что я чувствую, меня бы считали человеком, с которым нелегко работать','Я всегда думаю о том, какие тайные причины заставляют людей делать что-нибудь приятное для меня',
                      'Когда на меня кричат, я начинаю кричать в ответ','Неудачи огорчают меня',
                      'Я дерусь не реже и не чаще, чем другие','Я могу вспомнить случаи, когда я был настолько зол, что хватал попавшуюся мне под руку вещь и ломал ее',
                      'Иногда я чувствую, что готов первым начать драку','Иногда я чувствую, что жизнь поступает со мной несправедливо',
                      'Раньше я думал, что большинство людей говорит правду, но теперь я в это не верю','Я ругаюсь только со злости',
                      'Когда я поступаю неправильно, меня мучает совесть','Если для защиты своих прав мне нужно применить физическую силу, я применяю ее',
                      'Иногда я выражаю свой гнев тем, что стучу кулаком по столу','Я бываю грубоват по отношению к людям, которые мне не нравятся',
                      'У меня нет врагов, которые бы хотели мне навредить','Я не умею поставить человека на место, даже если он того заслуживает',
                      'Я часто думаю, что жил неправильно','Я знаю людей, которые способны довести меня до драки',
                      'Я не огорчаюсь из-за мелочей','Мне редко приходит в голову, что люди пытаются разозлить или оскорбить меня',
                      'Я часто только угрожаю людям, хотя и не собираюсь приводить угрозы в исполнение','В последнее время я стал занудой',
                      'В споре я часто повышаю голос','Я стараюсь обычно скрывать свое плохое отношение к людям',
                      'Я лучше соглашусь с чем-либо, чем стану спорить'
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
        raise BadOrderBHDI

    valid_values = ['да', 'нет']
    # Проверяем, есть ли значения, отличающиеся от указанных в списке
    lst_error_answers = []  # список для хранения строк где найдены неправильные ответы

    for i in range(75):
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
        raise BadValueBHDI

    base_df = pd.DataFrame()

    base_df['ФА_Значение'] = answers_df.apply(calc_value_fa, axis=1)
    base_df['ФА_Стен'] = base_df['ФА_Значение'].apply(calc_sten_first)
    base_df['ФА_Уровень'] = base_df['ФА_Стен'].apply(calc_level_first)


    base_df['КА_Значение'] = answers_df.apply(calc_value_ka, axis=1)
    base_df['Р_Значение'] = answers_df.apply(calc_value_r, axis=1)

    base_df['Н_Значение'] = answers_df.apply(calc_value_n, axis=1)
    base_df['Н_Стен'] = base_df['Н_Значение'].apply(calc_sten_first)
    base_df['Н_Уровень'] = base_df['Н_Стен'].apply(calc_level_first)

    base_df['О_Значение'] = answers_df.apply(calc_value_o, axis=1)
    base_df['П_Значение'] = answers_df.apply(calc_value_p, axis=1)

    base_df['ВА_Значение'] = answers_df.apply(calc_value_va, axis=1)
    base_df['ВА_Стен'] = base_df['ВА_Значение'].apply(calc_sten_first)
    base_df['ВА_Уровень'] = base_df['ВА_Стен'].apply(calc_level_first)

    base_df['ЧВ_Значение'] = answers_df.apply(calc_value_us, axis=1)
    base_df['ЧВ_Стен'] = base_df['ЧВ_Значение'].apply(calc_sten_first)
    base_df['ЧВ_Уровень'] = base_df['ЧВ_Стен'].apply(calc_level_first)

    base_df['Враждебность_Значение'] = round(base_df[['О_Значение','П_Значение']].sum(axis=1) / 2,2)
    base_df['Враждебность_Стен'] = base_df['Враждебность_Значение'].apply(calc_sten_host)
    base_df['Враждебность_Уровень'] = base_df['Враждебность_Стен'].apply(calc_level_host)





    base_df.to_excel('data.xlsx')






