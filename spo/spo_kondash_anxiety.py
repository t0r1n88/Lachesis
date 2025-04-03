"""
Скрипт для обработки результатов теста тревожности Кондаша
"""
from lachesis_support_functions import round_mean
import pandas as pd
from tkinter import messagebox



class BadOrderCondashAnxiety(Exception):
    """
    Исключение для обработки случая когда колонки не совпадают
    """
    pass


class BadValueCondashAnxiety(Exception):
    """
    Исключение для неправильных значений в вариантах ответов
    """
    pass



def count_all_scale(df:pd.DataFrame, lst_cols:list,lst_index:list):
    """
    Функция для подсчета уровней по всем шкалам
    :param df: датарфейм
    :param lst_cols: список колонок по которым нужно вести обработку
    :param lst_index: список индексов
    :return:датафрейм
    """
    base_df = pd.DataFrame(index=lst_index) # базовый датафрейм с индексами
    for scale in lst_cols:
        scale_df = pd.pivot_table(df, index=f'Уровень_{scale}_тревожности',
                                                  values=f'Значение_{scale}_тревожности',
                                                  aggfunc='count')

        scale_df[f'%{scale}_тревожности от общего'] = round(
            scale_df[f'Значение_{scale}_тревожности'] / scale_df[f'Значение_{scale}_тревожности'].sum(),3) * 100
        scale_df.rename(columns={f'Значение_{scale}_тревожности':f'Количество_{scale}_тревожности'},inplace=True)

        # # Создаем суммирующую строку
        scale_df.loc['Итого'] = scale_df.sum()


        base_df = base_df.join(scale_df)

    base_df = base_df.reset_index()
    base_df.rename(columns={'index':'Степень тревожности'},inplace=True)
    return base_df






def calc_level_all_condash_anxiety(ser:pd.Series):
    """
    Функция для подсчета уровня тревожности
    """
    row = ser.tolist() # превращаем в список
    group = int(row[0]) # курс
    sex = row[1] # пол
    value = row[2] # значение которое нужно обработать

    if group == 1:
        if sex == 'Женский':
            if 17 <= value <= 54:
                return 'Нормальный уровень тревожности'
            elif 55 <= value <= 73:
                return 'Несколько повышенный уровень тревожности'
            elif 74 <= value <= 90:
                return 'Высокий уровень тревожности'
            elif value > 90:
                return 'Очень высокий уровень тревожности'
            else:
                return 'Чрезмерное спокойствие'
        else:
            if 10 <= value <= 48:
                return 'Нормальный уровень тревожности'
            elif 49 <= value <= 67:
                return 'Несколько повышенный уровень тревожности'
            elif 68 <= value <= 86:
                return 'Высокий уровень тревожности'
            elif value > 86:
                return 'Очень высокий уровень тревожности'
            else:
                return 'Чрезмерное спокойствие'
    elif group == 2 or group == 3:
        if sex == 'Женский':
            if 35 <= value <= 62:
                return 'Нормальный уровень тревожности'
            elif 63 <= value <= 76:
                return 'Несколько повышенный уровень тревожности'
            elif 77 <= value <= 90:
                return 'Высокий уровень тревожности'
            elif value > 90:
                return 'Очень высокий уровень тревожности'
            else:
                return 'Чрезмерное спокойствие'
        else:
            if 23 <= value <= 47:
                return 'Нормальный уровень тревожности'
            elif 48 <= value <= 60:
                return 'Несколько повышенный уровень тревожности'
            elif 61 <= value <= 72:
                return 'Высокий уровень тревожности'
            elif value > 72:
                return 'Очень высокий уровень тревожности'
            else:
                return 'Чрезмерное спокойствие'
    else:
        return 'Для данного курса нет методики подсчета. Обрабатываются только 1,2,3 курсы.'

def calc_norm_all_condash_anxiety(ser:pd.Series):
    """
    Функция для подсчета уровня тревожности
    """
    row = ser.tolist() # превращаем в список
    group = int(row[0]) # курс
    sex = row[1] # пол

    if group == 1:
        if sex == 'Женский':
            return '17-73 баллов'

        else:
            return '10-67 баллов'

    elif group == 2 or group == 3:
        if sex == 'Женский':
            return '35-76 баллов'

        else:
            return '23-60 баллов'
    else:
        return 'Для данного курса нет методики подсчета. Обрабатываются только 1,2,3 курсы.'





def calc_level_study_condash_anxiety(ser:pd.Series):
    """
    Функция для подсчета учебной тревожности по шкале Кондаша
    """
    row = ser.tolist() # превращаем в список
    group = int(row[0]) # курс
    sex = row[1] # пол
    value = row[2] # значение которое нужно обработать

    if group == 1:
        if sex == 'Женский':
            if 2 <= value <= 14:
                return 'Нормальный уровень тревожности'
            elif 15 <= value <= 20:
                return 'Несколько повышенный уровень тревожности'
            elif 21 <= value <= 26:
                return 'Высокий уровень тревожности'
            elif value > 26:
                return 'Очень высокий уровень тревожности'
            else:
                return 'Чрезмерное спокойствие'
        else:
            if 1 <= value <= 13:
                return 'Нормальный уровень тревожности'
            elif 14 <= value <= 19:
                return 'Несколько повышенный уровень тревожности'
            elif 20 <= value <= 25:
                return 'Высокий уровень тревожности'
            elif value > 25:
                return 'Очень высокий уровень тревожности'
            else:
                return 'Чрезмерное спокойствие'
    elif group == 2 or group == 3:
        if sex == 'Женский':
            if 5 <= value <= 17:
                return 'Нормальный уровень тревожности'
            elif 18 <= value <= 23:
                return 'Несколько повышенный уровень тревожности'
            elif 24 <= value <= 30:
                return 'Высокий уровень тревожности'
            elif value > 30:
                return 'Очень высокий уровень тревожности'
            else:
                return 'Чрезмерное спокойствие'
        else:
            if 5 <= value <= 14:
                return 'Нормальный уровень тревожности'
            elif 15 <= value <= 19:
                return 'Несколько повышенный уровень тревожности'
            elif 20 <= value <= 24:
                return 'Высокий уровень тревожности'
            elif value > 24:
                return 'Очень высокий уровень тревожности'
            else:
                return 'Чрезмерное спокойствие'
    else:
        return 'Для данного курса нет методики подсчета. Обрабатываются только 1,2,3 курсы.'


def calc_norm_study_condash_anxiety(ser:pd.Series):
    """
    Функция для подсчета уровня тревожности
    """
    row = ser.tolist() # превращаем в список
    group = int(row[0]) # курс
    sex = row[1] # пол

    if group == 1:
        if sex == 'Женский':
            return '2-20 баллов'
        else:
            return '1-19 баллов'

    elif group == 2 or group == 3:
        if sex == 'Женский':
            return '5-23 баллов'
        else:
            return '5-19 баллов'
    else:
        return 'Для данного курса нет методики подсчета. Обрабатываются только 1,2,3 курсы.'


def calc_level_self_condash_anxiety(ser:pd.Series):
    """
    Функция для подсчета самоценочной тревожности
    """
    row = ser.tolist() # превращаем в список
    group = int(row[0]) # курс
    sex = row[1] # пол
    value = row[2] # значение которое нужно обработать

    if group == 1:
        if sex == 'Женский':
            if 6 <= value <= 19:
                return 'Нормальный уровень тревожности'
            elif 20 <= value <= 26:
                return 'Несколько повышенный уровень тревожности'
            elif 27 <= value <= 32:
                return 'Высокий уровень тревожности'
            elif value > 32:
                return 'Очень высокий уровень тревожности'
            else:
                return 'Чрезмерное спокойствие'
        else:
            if 1 <= value <= 17:
                return 'Нормальный уровень тревожности'
            elif 18 <= value <= 26:
                return 'Несколько повышенный уровень тревожности'
            elif 27 <= value <= 34:
                return 'Высокий уровень тревожности'
            elif value > 34:
                return 'Очень высокий уровень тревожности'
            else:
                return 'Чрезмерное спокойствие'
    elif group == 2 or group == 3:
        if sex == 'Женский':
            if 12 <= value <= 23:
                return 'Нормальный уровень тревожности'
            elif 24 <= value <= 29:
                return 'Несколько повышенный уровень тревожности'
            elif 30 <= value <= 34:
                return 'Высокий уровень тревожности'
            elif value > 34:
                return 'Очень высокий уровень тревожности'
            else:
                return 'Чрезмерное спокойствие'
        else:
            if 8 <= value <= 17:
                return 'Нормальный уровень тревожности'
            elif 18 <= value <= 22:
                return 'Несколько повышенный уровень тревожности'
            elif 23 <= value <= 27:
                return 'Высокий уровень тревожности'
            elif value > 27:
                return 'Очень высокий уровень тревожности'
            else:
                return 'Чрезмерное спокойствие'
    else:
        return 'Для данного курса нет методики подсчета. Обрабатываются только 1,2,3 курсы.'

def calc_norm_self_condash_anxiety(ser:pd.Series):
    """
    Функция для подсчета уровня тревожности
    """
    row = ser.tolist() # превращаем в список
    group = int(row[0]) # курс
    sex = row[1] # пол

    if group == 1:
        if sex == 'Женский':
            return '6-26 баллов'
        else:
            return '1-26 баллов'

    elif group == 2 or group == 3:
        if sex == 'Женский':
            return '12-29 баллов'
        else:
            return '8-22 баллов'
    else:
        return 'Для данного курса нет методики подсчета. Обрабатываются только 1,2,3 курсы.'


def calc_level_soc_condash_anxiety(ser:pd.Series):
    """
    Функция для подсчета межличностной тревожности
    """
    row = ser.tolist() # превращаем в список
    group = int(row[0]) # курс
    sex = row[1] # пол
    value = row[2] # значение которое нужно обработать

    if group == 1:
        if sex == 'Женский':
            if 4 <= value <= 19:
                return 'Нормальный уровень тревожности'
            elif 20 <= value <= 26:
                return 'Несколько повышенный уровень тревожности'
            elif 27 <= value <= 33:
                return 'Высокий уровень тревожности'
            elif value > 33:
                return 'Очень высокий уровень тревожности'
            else:
                return 'Чрезмерное спокойствие'
        else:
            if 3 <= value <= 17:
                return 'Нормальный уровень тревожности'
            elif 18 <= value <= 25:
                return 'Несколько повышенный уровень тревожности'
            elif 26 <= value <= 32:
                return 'Высокий уровень тревожности'
            elif value > 32:
                return 'Очень высокий уровень тревожности'
            else:
                return 'Чрезмерное спокойствие'
    elif group == 2 or group == 3:
        if sex == 'Женский':
            if 5 <= value <= 20:
                return 'Нормальный уровень тревожности'
            elif 21 <= value <= 28:
                return 'Несколько повышенный уровень тревожности'
            elif 29 <= value <= 36:
                return 'Высокий уровень тревожности'
            elif value > 36:
                return 'Очень высокий уровень тревожности'
            else:
                return 'Чрезмерное спокойствие'
        else:
            if 5 <= value <= 14:
                return 'Нормальный уровень тревожности'
            elif 15 <= value <= 19:
                return 'Несколько повышенный уровень тревожности'
            elif 20 <= value <= 23:
                return 'Высокий уровень тревожности'
            elif value > 23:
                return 'Очень высокий уровень тревожности'
            else:
                return 'Чрезмерное спокойствие'
    else:
        return 'Для данного курса нет методики подсчета. Обрабатываются только 1,2,3 курсы.'

def calc_norm_soc_condash_anxiety(ser:pd.Series):
    """
    Функция для подсчета уровня тревожности
    """
    row = ser.tolist() # превращаем в список
    group = int(row[0]) # курс
    sex = row[1] # пол

    if group == 1:
        if sex == 'Женский':
            return '4-26 баллов'
        else:
            return '3-25 баллов'

    elif group == 2 or group == 3:
        if sex == 'Женский':
            return '5-28 баллов'
        else:
            return '5-19 баллов'
    else:
        return 'Для данного курса нет методики подсчета. Обрабатываются только 1,2,3 курсы.'




def processing_kondash_anxiety(base_df: pd.DataFrame, answers_df: pd.DataFrame):
    """
    Проверка колонок и значений таблицы
    """
    try:
        out_answer_df = base_df.copy() # делаем копию для последующего соединения с сырыми ответами

        dct_replace_value = {'ситуация совершенно не кажется вам неприятной': 0,
                             'ситуация немного волнует, беспокоит вас': 1,
                             'ситуация достаточно неприятна и вызывает такое беспокойство, что вы предпочли бы избежать её': 2,
                             'ситуация очень неприятна и вызывает сильное беспокойство, тревогу, страх': 3,
                             'ситуация для вас крайне неприятна, если вы не можете перенести её и она вызывает у вас очень сильное беспокойство, очень сильный страх': 4}


        # Словарь с проверочными данными
        lst_check_cols =['Отвечать у доски','Пойти в дом к незнакомым людям','Участвовать в соревнованиях, конкурсах, в олимпиадах',
                         'Разговаривать с директором техникума, колледжа','Думать о своем будущем','Преподаватель смотрит по журналу, кого бы спросить',
                         'Тебя критикуют, в чем- то обвиняют','На тебя смотрят, когда ты что-нибудь делаешь (наблюдают за тобой во время работы, решения задачи)','Пишешь контрольную работу',
                         'После контрольной преподаватель называет отметки','На тебя не обращают внимания','У тебя что-то не получается',
                         'Ждешь родителей с родительского собрания','Тебе грозит неуспех, провал','Слышишь за своей спиной смех',
                         'Сдаешь экзамены в техникуме, колледже','На тебя сердятся (непонятно почему)','Выступать перед большой аудиторией',
                         'Предстоит важное, решающее дело','Не понимаешь объяснений преподавателя','С тобой не согласны, противоречат тебе',
                         'Сравниваешь себя с другими','Проверяют твои способности','На тебя смотрят как на маленького',
                         'На паре преподаватель неожиданно задает тебе вопрос','Замолчали, когда ты подошел','Оценивается твоя работа',
                         'Думаешь о своих делах','Тебе надо принять для себя решение','Не можешь справиться с домашним заданием']

        # Проверяем порядок колонок
        order_main_columns = lst_check_cols  # порядок колонок и названий как должно быть
        order_temp_df_columns = list(answers_df.columns)  # порядок колонок проверяемого файла
        error_order_lst = []  # список для несовпадающих пар
        # Сравниваем попарно колонки
        for main, temp in zip(order_main_columns, order_temp_df_columns):
            if main != temp:
                error_order_lst.append(f'На месте колонки {main} находится колонка {temp}')
        if len(error_order_lst) != 0:
            raise BadOrderCondashAnxiety

        answers_df.replace(dct_replace_value,inplace=True) # заменяем слова на цифры для подсчетов

        # Проверяем правильность замены слов на цифры
        valid_values = [0, 1, 2, 3,4]

        # Проверяем, есть ли значения, отличающиеся от указанных в списке
        mask = ~answers_df.isin(valid_values)

        # Получаем строки с отличающимися значениями
        result_check = answers_df[mask.any(axis=1)]
        if len(result_check) != 0:
            error_row =list(map(lambda x:x+2,result_check.index))
            error_row = list(map(str,error_row))
            error_message = ';'.join(error_row)
            raise BadValueCondashAnxiety



        # Колонки учебной тревожности
        lst_study_anxiety = ['Отвечать у доски','Разговаривать с директором техникума, колледжа',
                             'Преподаватель смотрит по журналу, кого бы спросить','Пишешь контрольную работу',
                             'После контрольной преподаватель называет отметки','Ждешь родителей с родительского собрания',
                             'Сдаешь экзамены в техникуме, колледже','Не понимаешь объяснений преподавателя',
                             'На паре преподаватель неожиданно задает тебе вопрос','Не можешь справиться с домашним заданием']

        # Колонки самооценки
        lst_self_anxiety = ['Участвовать в соревнованиях, конкурсах, в олимпиадах','Думать о своем будущем',
                            'У тебя что-то не получается','Тебе грозит неуспех, провал',
                            'Предстоит важное, решающее дело','Сравниваешь себя с другими',
                            'Проверяют твои способности','Оценивается твоя работа',
                            'Думаешь о своих делах','Тебе надо принять для себя решение']

        # Колонки межличностной тревожности
        lst_soc_anxiety = ['Пойти в дом к незнакомым людям','Тебя критикуют, в чем- то обвиняют',
                           'На тебя смотрят, когда ты что-нибудь делаешь (наблюдают за тобой во время работы, решения задачи)','На тебя не обращают внимания',
                           'Слышишь за своей спиной смех','На тебя сердятся (непонятно почему)','Выступать перед большой аудиторией',
                           'С тобой не согласны, противоречат тебе',
                           'На тебя смотрят как на маленького','Замолчали, когда ты подошел']

        # Считаем результат общая тревожность
        base_df['Значение_общей_тревожности'] = answers_df.sum(axis=1)
        base_df['Норма_общей_тревожности'] = base_df[['Курс', 'Пол']].apply(calc_norm_all_condash_anxiety,axis=1)
        base_df['Уровень_общей_тревожности'] = base_df[['Курс', 'Пол', 'Значение_общей_тревожности']].apply(calc_level_all_condash_anxiety,axis=1)

        # Считаем учебную тревожность в оригинале школьная
        base_df['Значение_учебной_тревожности'] = answers_df[lst_study_anxiety].sum(axis=1)
        base_df['Норма_учебной_тревожности'] = base_df[['Курс', 'Пол']].apply(calc_norm_study_condash_anxiety,axis=1)

        base_df['Уровень_учебной_тревожности'] = base_df[
            ['Курс', 'Пол', 'Значение_учебной_тревожности']].apply(calc_level_study_condash_anxiety,
                                                                                             axis=1)

        # Считаем самооценочную тревожность
        base_df['Значение_самооценочной_тревожности'] = answers_df[lst_self_anxiety].sum(axis=1)
        base_df['Норма_самоценочной_тревожности'] = base_df[['Курс', 'Пол']].apply(calc_norm_self_condash_anxiety,axis=1)

        base_df['Уровень_самооценочной_тревожности'] = base_df[
            ['Курс', 'Пол', 'Значение_самооценочной_тревожности']].apply(calc_level_self_condash_anxiety,
                                                                                             axis=1)
        # Считаем межличностную тревожность
        base_df['Значение_межличностной_тревожности'] = answers_df[lst_soc_anxiety].sum(axis=1)
        base_df['Норма_межличностной_тревожности'] = base_df[['Курс', 'Пол']].apply(calc_norm_soc_condash_anxiety,axis=1)

        base_df['Уровень_межличностной_тревожности'] = base_df[
            ['Курс', 'Пол', 'Значение_межличностной_тревожности']].apply(calc_level_soc_condash_anxiety,
                                                                                             axis=1)
        # Создаем датафрейм для создания части в общий датафрейм
        part_df = pd.DataFrame(columns=['Значение_общей_тревожности_Кондаш','Уровень_общей_тревожности_Кондаш',
                                        'Значение_учебной_тревожности_Кондаш','Уровень_учебной_тревожности_Кондаш',
                                        'Значение_самооценочной_тревожности_Кондаш','Уровень_самооценочной_тревожности_Кондаш',
                                        'Значение_межличностной_тревожности_Кондаш','Уровень_межличностной_тревожности_Кондаш'])

        part_df['Значение_общей_тревожности_Кондаш'] = base_df['Значение_общей_тревожности']
        part_df['Уровень_общей_тревожности_Кондаш'] = base_df['Уровень_общей_тревожности']
        part_df['Значение_учебной_тревожности_Кондаш'] = base_df['Значение_учебной_тревожности']
        part_df['Уровень_учебной_тревожности_Кондаш'] = base_df['Уровень_учебной_тревожности']
        part_df['Значение_самооценочной_тревожности_Кондаш'] = base_df['Значение_самооценочной_тревожности']
        part_df['Уровень_самооценочной_тревожности_Кондаш'] = base_df['Уровень_самооценочной_тревожности']
        part_df['Значение_межличностной_тревожности_Кондаш'] = base_df['Значение_межличностной_тревожности']
        part_df['Уровень_межличностной_тревожности_Кондаш'] = base_df['Уровень_межличностной_тревожности']




        base_df.sort_values(by='Значение_общей_тревожности',ascending=False,inplace=True) # сортируем

        # Делаем сводную таблицу средних значений.
        svod_all_df = pd.pivot_table(base_df,index=['Курс','Пол'],
                                     values=['Значение_общей_тревожности','Значение_учебной_тревожности','Значение_самооценочной_тревожности','Значение_межличностной_тревожности'],
                                     aggfunc=round_mean)
        svod_all_df.reset_index(inplace=True)

        all_result_df = svod_all_df[['Курс','Пол']] # выделяем базовые колонки

        # Начинаем собирать свод
        all_result_df['Значение_общей_тревожности'] = svod_all_df['Значение_общей_тревожности']
        all_result_df['Уровень_общей_тревожности'] = all_result_df[['Курс', 'Пол', 'Значение_общей_тревожности']].apply(calc_level_all_condash_anxiety,axis=1)

        all_result_df['Значение_учебной_тревожности'] = svod_all_df['Значение_учебной_тревожности']
        all_result_df['Уровень_учебной_тревожности'] = all_result_df[['Курс', 'Пол', 'Значение_учебной_тревожности']].apply(calc_level_study_condash_anxiety,axis=1)

        all_result_df['Значение_самооценочной_тревожности'] = svod_all_df['Значение_самооценочной_тревожности']
        all_result_df['Уровень_самооценочной_тревожности'] = all_result_df[
            ['Курс', 'Пол', 'Значение_самооценочной_тревожности']].apply(
            calc_level_self_condash_anxiety, axis=1)

        all_result_df['Значение_межличностной_тревожности'] = svod_all_df['Значение_межличностной_тревожности']
        all_result_df['Уровень_межличностной_тревожности'] = all_result_df[
            ['Курс', 'Пол', 'Значение_межличностной_тревожности']].apply(
            calc_level_soc_condash_anxiety, axis=1)


        # Делаем свод по количеству
        svod_all_count_df = pd.pivot_table(base_df,index=['Курс','Пол'],
                                     columns='Уровень_общей_тревожности',
                                     values='Значение_общей_тревожности',
                                     aggfunc='count',margins=True,margins_name='Итого')
        svod_all_count_df.reset_index(inplace=True)
        svod_all_count_df = svod_all_count_df.reindex(
            columns=['Курс','Пол', 'Нормальный уровень тревожности', 'Несколько повышенный уровень тревожности',
                     'Высокий уровень тревожности', 'Очень высокий уровень тревожности', 'Чрезмерное спокойствие',
                     'Итого'])

        # Добавляем колонки с процентами
        svod_all_count_df['% Нормальный уровень тревожности от общего'] = round(svod_all_count_df['Нормальный уровень тревожности'] / svod_all_count_df['Итого'],2)*100


        svod_all_count_df['% Несколько повышенный уровень тревожности от общего'] = round(svod_all_count_df['Несколько повышенный уровень тревожности'] / svod_all_count_df['Итого'],2)*100

        svod_all_count_df['% Высокий уровень тревожности от общего'] = round(svod_all_count_df['Высокий уровень тревожности'] / svod_all_count_df['Итого'],2)*100

        svod_all_count_df['% Очень высокий уровень тревожности от общего'] = round(svod_all_count_df['Очень высокий уровень тревожности'] / svod_all_count_df['Итого'],2)*100

        svod_all_count_df['% Чрезмерное спокойствие от общего'] = round(svod_all_count_df['Чрезмерное спокойствие'] / svod_all_count_df['Итого'],2)*100


        # свод по учебной тревожности
        svod_study_count_df = pd.pivot_table(base_df,index=['Курс','Пол'],
                                     columns='Уровень_учебной_тревожности',
                                     values='Значение_учебной_тревожности',
                                     aggfunc='count',margins=True,margins_name='Итого')
        svod_study_count_df.reset_index(inplace=True)
        svod_study_count_df = svod_study_count_df.reindex(
            columns=['Курс', 'Пол', 'Нормальный уровень тревожности', 'Несколько повышенный уровень тревожности',
                     'Высокий уровень тревожности', 'Очень высокий уровень тревожности', 'Чрезмерное спокойствие',
                     'Итого'])

        # Добавляем колонки с процентами
        svod_study_count_df['% Нормальный уровень тревожности от общего'] = round(svod_study_count_df['Нормальный уровень тревожности'] / svod_study_count_df['Итого'],2)

        svod_study_count_df['% Несколько повышенный уровень тревожности от общего'] = round(svod_study_count_df['Несколько повышенный уровень тревожности'] / svod_study_count_df['Итого'],2)*100

        svod_study_count_df['% Высокий уровень тревожности от общего'] = round(svod_study_count_df['Высокий уровень тревожности'] / svod_study_count_df['Итого'],2)*100

        svod_study_count_df['% Очень высокий уровень тревожности от общего'] = round(svod_study_count_df['Очень высокий уровень тревожности'] / svod_study_count_df['Итого'],2)*100

        svod_study_count_df['% Чрезмерное спокойствие от общего'] = round(svod_study_count_df['Чрезмерное спокойствие'] / svod_study_count_df['Итого'],2)*100


        # свод по самооценочной тревожности
        svod_self_count_df = pd.pivot_table(base_df,index=['Курс','Пол'],
                                     columns='Уровень_самооценочной_тревожности',
                                     values='Значение_самооценочной_тревожности',
                                     aggfunc='count',margins=True,margins_name='Итого')
        svod_self_count_df.reset_index(inplace=True)
        svod_self_count_df = svod_self_count_df.reindex(
            columns=['Курс', 'Пол', 'Нормальный уровень тревожности', 'Несколько повышенный уровень тревожности',
                     'Высокий уровень тревожности', 'Очень высокий уровень тревожности', 'Чрезмерное спокойствие',
                     'Итого'])

        svod_self_count_df['% Нормальный уровень тревожности от общего'] = round(
            svod_self_count_df['Нормальный уровень тревожности'] / svod_self_count_df['Итого'], 2)*100


        svod_self_count_df['% Несколько повышенный уровень тревожности от общего'] = round(
            svod_self_count_df['Несколько повышенный уровень тревожности'] / svod_self_count_df['Итого'], 2)*100

        svod_self_count_df['% Высокий уровень тревожности от общего'] = round(svod_self_count_df['Высокий уровень тревожности'] / svod_self_count_df['Итого'],
                                                          2)*100

        svod_self_count_df['% Очень высокий уровень тревожности от общего'] = round(
            svod_self_count_df['Очень высокий уровень тревожности'] / svod_self_count_df['Итого'], 2)*100

        svod_self_count_df['% Чрезмерное спокойствие от общего'] = round(
            svod_self_count_df['Чрезмерное спокойствие'] / svod_self_count_df['Итого'], 2)*100


        # свод по межличностной тревожности
        svod_soc_count_df = pd.pivot_table(base_df,index=['Курс','Пол'],
                                     columns='Уровень_межличностной_тревожности',
                                     values='Значение_межличностной_тревожности',
                                     aggfunc='count',margins=True,margins_name='Итого')
        svod_soc_count_df.reset_index(inplace=True)
        svod_soc_count_df = svod_soc_count_df.reindex(
            columns=['Курс', 'Пол', 'Нормальный уровень тревожности', 'Несколько повышенный уровень тревожности',
                     'Высокий уровень тревожности', 'Очень высокий уровень тревожности', 'Чрезмерное спокойствие',
                     'Итого'])

        svod_soc_count_df['% Нормальный уровень тревожности от общего'] = round(
            svod_soc_count_df['Нормальный уровень тревожности'] / svod_soc_count_df['Итого'], 2)*100


        svod_soc_count_df['% Несколько повышенный уровень тревожности от общего'] = round(
            svod_soc_count_df['Несколько повышенный уровень тревожности'] / svod_soc_count_df['Итого'], 2)*100

        svod_soc_count_df['% Высокий уровень тревожности от общего'] = round(svod_soc_count_df['Высокий уровень тревожности'] / svod_soc_count_df['Итого'], 2)*100

        svod_soc_count_df['% Очень высокий уровень тревожности от общего'] = round(
            svod_soc_count_df['Очень высокий уровень тревожности'] / svod_soc_count_df['Итого'], 2)*100

        svod_soc_count_df['% Чрезмерное спокойствие от общего'] = round(
            svod_soc_count_df['Чрезмерное спокойствие'] / svod_soc_count_df['Итого'], 2)*100


        out_answer_df = pd.concat([out_answer_df, answers_df], axis=1)


        # Делаем сводную таблицу средних значений.
        svod_all_group_df = pd.pivot_table(base_df, index=['Курс','Группа', 'Пол'],
                                     values=['Значение_общей_тревожности', 'Значение_учебной_тревожности',
                                             'Значение_самооценочной_тревожности',
                                             'Значение_межличностной_тревожности'],
                                     aggfunc=round_mean)
        svod_all_group_df.reset_index(inplace=True)
        all_result_group_df = svod_all_group_df[['Курс','Группа', 'Пол']]  # выделяем базовые колонки

        # Начинаем собирать свод
        all_result_group_df['Значение_общей_тревожности'] = svod_all_group_df['Значение_общей_тревожности']
        all_result_group_df['Уровень_общей_тревожности'] = all_result_group_df[
            ['Курс', 'Пол', 'Значение_общей_тревожности']].apply(
            calc_level_all_condash_anxiety,
            axis=1)

        all_result_group_df['Значение_учебной_тревожности'] = svod_all_group_df['Значение_учебной_тревожности']
        all_result_group_df['Уровень_учебной_тревожности'] = all_result_group_df[
            ['Курс', 'Пол', 'Значение_учебной_тревожности']].apply(
            calc_level_study_condash_anxiety,
            axis=1)

        all_result_group_df['Значение_самооценочной_тревожности'] = svod_all_group_df[
            'Значение_самооценочной_тревожности']
        all_result_group_df['Уровень_самооценочной_тревожности'] = all_result_group_df[
            ['Курс', 'Пол', 'Значение_самооценочной_тревожности']].apply(
            calc_level_self_condash_anxiety, axis=1)

        all_result_group_df['Значение_межличностной_тревожности'] = svod_all_group_df[
            'Значение_межличностной_тревожности']
        all_result_group_df['Уровень_межличностной_тревожности'] = all_result_group_df[
            ['Курс', 'Пол', 'Значение_межличностной_тревожности']].apply(
            calc_level_soc_condash_anxiety, axis=1)

        # Делаем свод по количеству
        svod_all_group_count_df = pd.pivot_table(base_df, index=['Группа', 'Пол'],
                                           columns='Уровень_общей_тревожности',
                                           values='Значение_общей_тревожности',
                                           aggfunc='count', margins=True, margins_name='Итого')
        svod_all_group_count_df.reset_index(inplace=True)
        svod_all_group_count_df = svod_all_group_count_df.reindex(
            columns=['Группа', 'Пол', 'Нормальный уровень тревожности', 'Несколько повышенный уровень тревожности',
                     'Высокий уровень тревожности', 'Очень высокий уровень тревожности', 'Чрезмерное спокойствие',
                     'Итого'])


        # Добавляем колонки с процентами
        svod_all_group_count_df['% Нормальный уровень тревожности от общего'] = round(
            svod_all_group_count_df['Нормальный уровень тревожности'] / svod_all_group_count_df['Итого'], 2)*100


        svod_all_group_count_df['% Несколько повышенный уровень тревожности от общего'] = round(
            svod_all_group_count_df['Несколько повышенный уровень тревожности'] / svod_all_group_count_df['Итого'], 2)*100

        svod_all_group_count_df['% Высокий уровень тревожности от общего'] = round(svod_all_group_count_df['Высокий уровень тревожности'] / svod_all_group_count_df['Итого'],
                                                         2)*100

        svod_all_group_count_df['% Очень высокий уровень тревожности от общего'] = round(
            svod_all_group_count_df['Очень высокий уровень тревожности'] / svod_all_group_count_df['Итого'], 2)*100

        svod_all_group_count_df['% Чрезмерное спокойствие от общего'] = round(
            svod_all_group_count_df['Чрезмерное спокойствие'] / svod_all_group_count_df['Итого'], 2)*100


        # свод по учебной тревожности
        svod_study_group_count_df = pd.pivot_table(base_df, index=['Группа', 'Пол'],
                                                   columns='Уровень_учебной_тревожности',
                                                   values='Значение_учебной_тревожности',
                                                   aggfunc='count', margins=True, margins_name='Итого')
        svod_study_group_count_df.reset_index(inplace=True)
        svod_study_group_count_df = svod_study_group_count_df.reindex(
            columns=['Группа', 'Пол', 'Нормальный уровень тревожности', 'Несколько повышенный уровень тревожности',
                     'Высокий уровень тревожности', 'Очень высокий уровень тревожности', 'Чрезмерное спокойствие',
                     'Итого'])

        # Добавляем колонки с процентами
        svod_study_group_count_df['% Нормальный уровень тревожности от общего'] = round(
            svod_study_group_count_df['Нормальный уровень тревожности'] / svod_study_group_count_df['Итого'], 2)*100


        svod_study_group_count_df['% Несколько повышенный уровень тревожности от общего'] = round(
            svod_study_group_count_df['Несколько повышенный уровень тревожности'] / svod_study_group_count_df['Итого'], 2)*100

        svod_study_group_count_df['% Высокий уровень тревожности от общего'] = round(
            svod_study_group_count_df['Высокий уровень тревожности'] / svod_study_group_count_df['Итого'], 2)*100

        svod_study_group_count_df['% Очень высокий уровень тревожности от общего'] = round(
            svod_study_group_count_df['Очень высокий уровень тревожности'] / svod_study_group_count_df['Итого'], 2)*100

        svod_study_group_count_df['% Чрезмерное спокойствие от общего'] = round(
            svod_study_group_count_df['Чрезмерное спокойствие'] / svod_study_group_count_df['Итого'], 2)*100


        # свод по самооценочной тревожности
        svod_self_group_count_df = pd.pivot_table(base_df, index=['Группа', 'Пол'],
                                                  columns='Уровень_самооценочной_тревожности',
                                                  values='Значение_самооценочной_тревожности',
                                                  aggfunc='count', margins=True, margins_name='Итого')
        svod_self_group_count_df.reset_index(inplace=True)
        svod_self_group_count_df = svod_self_group_count_df.reindex(
            columns=['Группа', 'Пол', 'Нормальный уровень тревожности', 'Несколько повышенный уровень тревожности',
                     'Высокий уровень тревожности', 'Очень высокий уровень тревожности', 'Чрезмерное спокойствие',
                     'Итого'])

        svod_self_group_count_df['% Нормальный уровень тревожности от общего'] = round(
            svod_self_group_count_df['Нормальный уровень тревожности'] / svod_self_group_count_df['Итого'], 2)*100


        svod_self_group_count_df['% Несколько повышенный уровень тревожности от общего'] = round(
            svod_self_group_count_df['Несколько повышенный уровень тревожности'] / svod_self_group_count_df['Итого'], 2)*100

        svod_self_group_count_df['% Высокий уровень тревожности от общего'] = round(
            svod_self_group_count_df['Высокий уровень тревожности'] / svod_self_group_count_df['Итого'],
            2)*100

        svod_self_group_count_df['% Очень высокий уровень тревожности от общего'] = round(
            svod_self_group_count_df['Очень высокий уровень тревожности'] / svod_self_group_count_df['Итого'], 2)*100

        svod_self_group_count_df['% Чрезмерное спокойствие от общего'] = round(
            svod_self_group_count_df['Чрезмерное спокойствие'] / svod_self_group_count_df['Итого'], 2)*100


        # свод по межличностной тревожности
        svod_soc_group_count_df = pd.pivot_table(base_df, index=['Группа', 'Пол'],
                                                 columns='Уровень_межличностной_тревожности',
                                                 values='Значение_межличностной_тревожности',
                                                 aggfunc='count', margins=True, margins_name='Итого')
        svod_soc_group_count_df.reset_index(inplace=True)
        svod_soc_group_count_df = svod_soc_group_count_df.reindex(
            columns=['Группа', 'Пол', 'Нормальный уровень тревожности', 'Несколько повышенный уровень тревожности',
                     'Высокий уровень тревожности', 'Очень высокий уровень тревожности', 'Чрезмерное спокойствие',
                     'Итого'])

        svod_soc_group_count_df['% Нормальный уровень тревожности от общего'] = round(
            svod_soc_group_count_df['Нормальный уровень тревожности'] / svod_soc_group_count_df['Итого'], 2)*100


        svod_soc_group_count_df['% Несколько повышенный уровень тревожности от общего'] = round(
            svod_soc_group_count_df['Несколько повышенный уровень тревожности'] / svod_soc_group_count_df['Итого'], 2)*100

        svod_soc_group_count_df['% Высокий уровень тревожности от общего'] = round(
            svod_soc_group_count_df['Высокий уровень тревожности'] / svod_soc_group_count_df['Итого'],
            2)*100

        svod_soc_group_count_df['% Очень высокий уровень тревожности от общего'] = round(
            svod_soc_group_count_df['Очень высокий уровень тревожности'] / svod_soc_group_count_df['Итого'], 2)*100

        svod_soc_group_count_df['% Чрезмерное спокойствие от общего'] = round(
            svod_soc_group_count_df['Чрезмерное спокойствие'] / svod_soc_group_count_df['Итого'], 2)*100

        # Общий свод сколько склонностей всего в процентном соотношении
        svod_all_df = count_all_scale(base_df, ['общей', 'учебной', 'самооценочной', 'межличностной' ],
                                      ['Нормальный уровень тревожности',
                                       'Несколько повышенный уровень тревожности',
                                       'Высокий уровень тревожности',
                                       'Очень высокий уровень тревожности',
                                       'Чрезмерное спокойствие', 'Итого'])





        # формируем словарь
        out_dct = {'Списочный результат':base_df,'Список для проверки':out_answer_df,
                   'Общий свод':svod_all_df,
                   'Курс_Ср_рез':all_result_df,'Курс_Кол_общ_трев':svod_all_count_df,
                   'Курс_Кол_учеб_трев':svod_study_count_df,'Курс_Кол_самооц_трев':svod_self_count_df,
                   'Курс_Кол_межлич_трев':svod_soc_count_df,
                   'Группа_Ср_рез':all_result_group_df,
                   'Группа_Кол_общ_трев':svod_all_group_count_df,
                   'Группа_Кол_учеб_трев':svod_study_group_count_df,
                   'Группа_Кол_сам_трев':svod_self_group_count_df,
                   'Группа_Кол_меж_трев':svod_soc_group_count_df,
                   }

        return out_dct, part_df
    except BadOrderCondashAnxiety:
        messagebox.showerror('Лахеcис',
                                 f'Названия колонок или их порядок для ответов на тест Шкалы тревожности Кондаша не совпадают с правильным!\n'
                                 f'{error_order_lst}')

    except BadValueCondashAnxiety:
        messagebox.showerror('Лахеcис',
                                 f'При обработке вопросов теста Шкалы тревожности Кондаша обнаружены неправильные варианты ответов. Проверьте ответы на указанных строках:\n'
                                 f'{error_message}\n'
                                 f'Используйте при создании Яндекс-формы написание вариантов ответа из руководства пользователя программы Лахесис.')






