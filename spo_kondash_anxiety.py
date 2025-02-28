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
                return 'Нормальный'
            elif 55 <= value <= 73:
                return 'Несколько повышенный'
            elif 74 <= value <= 90:
                return 'Высокий'
            elif value > 90:
                return 'Очень высокий'
            else:
                return 'Чрезмерное спокойствие'
        else:
            if 10 <= value <= 48:
                return 'Нормальный'
            elif 49 <= value <= 67:
                return 'Несколько повышенный'
            elif 68 <= value <= 86:
                return 'Высокий'
            elif value > 86:
                return 'Очень высокий'
            else:
                return 'Чрезмерное спокойствие'
    elif group == 2:
        if sex == 'Женский':
            if 35 <= value <= 62:
                return 'Нормальный'
            elif 63 <= value <= 76:
                return 'Несколько повышенный'
            elif 77 <= value <= 90:
                return 'Высокий'
            elif value > 90:
                return 'Очень высокий'
            else:
                return 'Чрезмерное спокойствие'
        else:
            if 23 <= value <= 47:
                return 'Нормальный'
            elif 48 <= value <= 60:
                return 'Несколько повышенный'
            elif 61 <= value <= 72:
                return 'Высокий'
            elif value > 72:
                return 'Очень высокий'
            else:
                return 'Чрезмерное спокойствие'



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
                return 'Нормальный'
            elif 15 <= value <= 20:
                return 'Несколько повышенный'
            elif 21 <= value <= 26:
                return 'Высокий'
            elif value > 26:
                return 'Очень высокий'
            else:
                return 'Чрезмерное спокойствие'
        else:
            if 1 <= value <= 13:
                return 'Нормальный'
            elif 14 <= value <= 19:
                return 'Несколько повышенный'
            elif 20 <= value <= 25:
                return 'Высокий'
            elif value > 25:
                return 'Очень высокий'
            else:
                return 'Чрезмерное спокойствие'
    elif group == 2:
        if sex == 'Женский':
            if 5 <= value <= 17:
                return 'Нормальный'
            elif 18 <= value <= 23:
                return 'Несколько повышенный'
            elif 24 <= value <= 30:
                return 'Высокий'
            elif value > 30:
                return 'Очень высокий'
            else:
                return 'Чрезмерное спокойствие'
        else:
            if 5 <= value <= 14:
                return 'Нормальный'
            elif 15 <= value <= 19:
                return 'Несколько повышенный'
            elif 20 <= value <= 24:
                return 'Высокий'
            elif value > 24:
                return 'Очень высокий'
            else:
                return 'Чрезмерное спокойствие'

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
                return 'Нормальный'
            elif 20 <= value <= 26:
                return 'Несколько повышенный'
            elif 27 <= value <= 32:
                return 'Высокий'
            elif value > 32:
                return 'Очень высокий'
            else:
                return 'Чрезмерное спокойствие'
        else:
            if 1 <= value <= 17:
                return 'Нормальный'
            elif 18 <= value <= 26:
                return 'Несколько повышенный'
            elif 27 <= value <= 34:
                return 'Высокий'
            elif value > 34:
                return 'Очень высокий'
            else:
                return 'Чрезмерное спокойствие'
    elif group == 2:
        if sex == 'Женский':
            if 12 <= value <= 23:
                return 'Нормальный'
            elif 24 <= value <= 29:
                return 'Несколько повышенный'
            elif 30 <= value <= 34:
                return 'Высокий'
            elif value > 34:
                return 'Очень высокий'
            else:
                return 'Чрезмерное спокойствие'
        else:
            if 8 <= value <= 17:
                return 'Нормальный'
            elif 18 <= value <= 22:
                return 'Несколько повышенный'
            elif 23 <= value <= 27:
                return 'Высокий'
            elif value > 27:
                return 'Очень высокий'
            else:
                return 'Чрезмерное спокойствие'

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
                return 'Нормальный'
            elif 20 <= value <= 26:
                return 'Несколько повышенный'
            elif 27 <= value <= 33:
                return 'Высокий'
            elif value > 33:
                return 'Очень высокий'
            else:
                return 'Чрезмерное спокойствие'
        else:
            if 3 <= value <= 17:
                return 'Нормальный'
            elif 18 <= value <= 25:
                return 'Несколько повышенный'
            elif 26 <= value <= 32:
                return 'Высокий'
            elif value > 32:
                return 'Очень высокий'
            else:
                return 'Чрезмерное спокойствие'
    elif group == 2:
        if sex == 'Женский':
            if 5 <= value <= 20:
                return 'Нормальный'
            elif 21 <= value <= 28:
                return 'Несколько повышенный'
            elif 29 <= value <= 36:
                return 'Высокий'
            elif value > 36:
                return 'Очень высокий'
            else:
                return 'Чрезмерное спокойствие'
        else:
            if 5 <= value <= 14:
                return 'Нормальный'
            elif 15 <= value <= 19:
                return 'Несколько повышенный'
            elif 20 <= value <= 23:
                return 'Высокий'
            elif value > 23:
                return 'Очень высокий'
            else:
                return 'Чрезмерное спокойствие'




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
                         'После контрольной учитель называет отметки','На тебя не обращают внимания','У тебя что-то не получается',
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
                             'После контрольной учитель называет отметки','Ждешь родителей с родительского собрания',
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
        base_df['Уровень_общей_тревожности'] = base_df[['Выберите_свой_курс', 'Выберите_свой_пол', 'Значение_общей_тревожности']].apply(calc_level_all_condash_anxiety,axis=1)

        # Считаем учебную тревожность в оригинале школьная
        base_df['Значение_учебной_тревожности'] = answers_df[lst_study_anxiety].sum(axis=1)
        base_df['Уровень_учебной_тревожности'] = base_df[
            ['Выберите_свой_курс', 'Выберите_свой_пол', 'Значение_учебной_тревожности']].apply(calc_level_study_condash_anxiety,
                                                                                             axis=1)

        # Считаем самооценочную тревожность
        base_df['Значение_самооценочной_тревожности'] = answers_df[lst_self_anxiety].sum(axis=1)
        base_df['Уровень_самооценочной_тревожности'] = base_df[
            ['Выберите_свой_курс', 'Выберите_свой_пол', 'Значение_самооценочной_тревожности']].apply(calc_level_self_condash_anxiety,
                                                                                             axis=1)
        # Считаем межличностную тревожность
        base_df['Значение_межличностной_тревожности'] = answers_df[lst_soc_anxiety].sum(axis=1)
        base_df['Уровень_межличностной_тревожности'] = base_df[
            ['Выберите_свой_курс', 'Выберите_свой_пол', 'Значение_межличностной_тревожности']].apply(calc_level_soc_condash_anxiety,
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
        part_df['Значение_самооценочной_тревожности_Кондаш'] = base_df['Значение_общей_тревожности']
        part_df['Уровень_самооценочной_тревожности_Кондаш'] = base_df['Уровень_самооценочной_тревожности']
        part_df['Значение_межличностной_тревожности_Кондаш'] = base_df['Значение_межличностной_тревожности']
        part_df['Уровень_межличностной_тревожности_Кондаш'] = base_df['Уровень_межличностной_тревожности']




        base_df.sort_values(by='Значение_общей_тревожности',ascending=False,inplace=True) # сортируем

        # Делаем сводную таблицу средних значений.
        svod_all_df = pd.pivot_table(base_df,index=['Выберите_свой_курс','Выберите_свой_пол'],
                                     values=['Значение_общей_тревожности','Значение_учебной_тревожности','Значение_самооценочной_тревожности','Значение_межличностной_тревожности'],
                                     aggfunc=round_mean)
        svod_all_df.reset_index(inplace=True)

        all_result_df = svod_all_df[['Выберите_свой_курс','Выберите_свой_пол']] # выделяем базовые колонки

        # Начинаем собирать свод
        all_result_df['Значение_общей_тревожности'] = svod_all_df['Значение_общей_тревожности']
        all_result_df['Уровень_общей_тревожности'] = all_result_df[['Выберите_свой_курс', 'Выберите_свой_пол', 'Значение_общей_тревожности']].apply(calc_level_all_condash_anxiety,axis=1)

        all_result_df['Значение_учебной_тревожности'] = svod_all_df['Значение_учебной_тревожности']
        all_result_df['Уровень_учебной_тревожности'] = all_result_df[['Выберите_свой_курс', 'Выберите_свой_пол', 'Значение_учебной_тревожности']].apply(calc_level_study_condash_anxiety,axis=1)

        all_result_df['Значение_самооценочной_тревожности'] = svod_all_df['Значение_самооценочной_тревожности']
        all_result_df['Уровень_самооценочной_тревожности'] = all_result_df[
            ['Выберите_свой_курс', 'Выберите_свой_пол', 'Значение_самооценочной_тревожности']].apply(
            calc_level_self_condash_anxiety, axis=1)

        all_result_df['Значение_межличностной_тревожности'] = svod_all_df['Значение_межличностной_тревожности']
        all_result_df['Уровень_межличностной_тревожности'] = all_result_df[
            ['Выберите_свой_курс', 'Выберите_свой_пол', 'Значение_межличностной_тревожности']].apply(
            calc_level_soc_condash_anxiety, axis=1)

        all_result_df.rename(columns={'Выберите_свой_курс':'Курс','Выберите_свой_пол':'Пол'},inplace=True)

        # Делаем свод по количеству
        svod_all_count_df = pd.pivot_table(base_df,index=['Выберите_свой_курс','Выберите_свой_пол'],
                                     columns='Уровень_общей_тревожности',
                                     values='Значение_общей_тревожности',
                                     aggfunc='count',margins=True,margins_name='Итого')
        svod_all_count_df.reset_index(inplace=True)
        svod_all_count_df.rename(columns={'Выберите_свой_курс': 'Курс', 'Выберите_свой_пол': 'Пол'}, inplace=True)

        # Добавляем колонки с процентами
        if 'Нормальный' in svod_all_count_df.columns:
            svod_all_count_df['% Нормальный от общего'] = round(svod_all_count_df['Нормальный'] / svod_all_count_df['Итого'],2)

        if 'Несколько повышенный' in svod_all_count_df.columns:
            svod_all_count_df['% Несколько повышенный от общего'] = round(svod_all_count_df['Несколько повышенный'] / svod_all_count_df['Итого'],2)
        if 'Высокий' in svod_all_count_df.columns:
            svod_all_count_df['% Высокий от общего'] = round(svod_all_count_df['Высокий'] / svod_all_count_df['Итого'],2)
        if 'Очень высокий' in svod_all_count_df.columns:
            svod_all_count_df['% Очень высокий от общего'] = round(svod_all_count_df['Очень высокий'] / svod_all_count_df['Итого'],2)
        if 'Чрезмерное спокойствие' in svod_all_count_df.columns:
            svod_all_count_df['% Чрезмерное спокойствие от общего'] = round(svod_all_count_df['Чрезмерное спокойствие'] / svod_all_count_df['Итого'],2)

        # свод по учебной тревожности
        svod_study_count_df = pd.pivot_table(base_df,index=['Выберите_свой_курс','Выберите_свой_пол'],
                                     columns='Уровень_учебной_тревожности',
                                     values='Значение_учебной_тревожности',
                                     aggfunc='count',margins=True,margins_name='Итого')
        svod_study_count_df.reset_index(inplace=True)
        svod_study_count_df.rename(columns={'Выберите_свой_курс': 'Курс', 'Выберите_свой_пол': 'Пол'}, inplace=True)

        # Добавляем колонки с процентами
        if 'Нормальный' in svod_study_count_df.columns:
            svod_study_count_df['% Нормальный от общего'] = round(svod_study_count_df['Нормальный'] / svod_study_count_df['Итого'],2)

        if 'Несколько повышенный' in svod_study_count_df.columns:
            svod_study_count_df['% Несколько повышенный от общего'] = round(svod_study_count_df['Несколько повышенный'] / svod_study_count_df['Итого'],2)
        if 'Высокий' in svod_study_count_df.columns:
            svod_study_count_df['% Высокий от общего'] = round(svod_study_count_df['Высокий'] / svod_study_count_df['Итого'],2)
        if 'Очень высокий' in svod_study_count_df.columns:
            svod_study_count_df['% Очень высокий от общего'] = round(svod_study_count_df['Очень высокий'] / svod_study_count_df['Итого'],2)
        if 'Чрезмерное спокойствие' in svod_study_count_df.columns:
            svod_study_count_df['% Чрезмерное спокойствие от общего'] = round(svod_study_count_df['Чрезмерное спокойствие'] / svod_study_count_df['Итого'],2)

        # свод по самооценочной тревожности
        svod_self_count_df = pd.pivot_table(base_df,index=['Выберите_свой_курс','Выберите_свой_пол'],
                                     columns='Уровень_самооценочной_тревожности',
                                     values='Значение_самооценочной_тревожности',
                                     aggfunc='count',margins=True,margins_name='Итого')
        svod_self_count_df.reset_index(inplace=True)
        svod_self_count_df.rename(columns={'Выберите_свой_курс': 'Курс', 'Выберите_свой_пол': 'Пол'}, inplace=True)

        if 'Нормальный' in svod_self_count_df.columns:
            svod_self_count_df['% Нормальный от общего'] = round(
                svod_self_count_df['Нормальный'] / svod_self_count_df['Итого'], 2)

        if 'Несколько повышенный' in svod_self_count_df.columns:
            svod_self_count_df['% Несколько повышенный от общего'] = round(
                svod_self_count_df['Несколько повышенный'] / svod_self_count_df['Итого'], 2)
        if 'Высокий' in svod_self_count_df.columns:
            svod_self_count_df['% Высокий от общего'] = round(svod_self_count_df['Высокий'] / svod_self_count_df['Итого'],
                                                              2)
        if 'Очень высокий' in svod_self_count_df.columns:
            svod_self_count_df['% Очень высокий от общего'] = round(
                svod_self_count_df['Очень высокий'] / svod_self_count_df['Итого'], 2)
        if 'Чрезмерное спокойствие' in svod_self_count_df.columns:
            svod_self_count_df['% Чрезмерное спокойствие от общего'] = round(
                svod_self_count_df['Чрезмерное спокойствие'] / svod_self_count_df['Итого'], 2)

        # свод по межличностной тревожности
        svod_soc_count_df = pd.pivot_table(base_df,index=['Выберите_свой_курс','Выберите_свой_пол'],
                                     columns='Уровень_межличностной_тревожности',
                                     values='Значение_межличностной_тревожности',
                                     aggfunc='count',margins=True,margins_name='Итого')
        svod_soc_count_df.reset_index(inplace=True)
        svod_soc_count_df.rename(columns={'Выберите_свой_курс': 'Курс', 'Выберите_свой_пол': 'Пол'}, inplace=True)

        if 'Нормальный' in svod_soc_count_df.columns:
            svod_soc_count_df['% Нормальный от общего'] = round(
                svod_soc_count_df['Нормальный'] / svod_soc_count_df['Итого'], 2)

        if 'Несколько повышенный' in svod_soc_count_df.columns:
            svod_soc_count_df['% Несколько повышенный от общего'] = round(
                svod_soc_count_df['Несколько повышенный'] / svod_soc_count_df['Итого'], 2)
        if 'Высокий' in svod_soc_count_df.columns:
            svod_soc_count_df['% Высокий от общего'] = round(svod_soc_count_df['Высокий'] / svod_soc_count_df['Итого'], 2)
        if 'Очень высокий' in svod_soc_count_df.columns:
            svod_soc_count_df['% Очень высокий от общего'] = round(
                svod_soc_count_df['Очень высокий'] / svod_soc_count_df['Итого'], 2)
        if 'Чрезмерное спокойствие' in svod_soc_count_df.columns:
            svod_soc_count_df['% Чрезмерное спокойствие от общего'] = round(
                svod_soc_count_df['Чрезмерное спокойствие'] / svod_soc_count_df['Итого'], 2)

        out_answer_df = pd.concat([out_answer_df, answers_df], axis=1)
        out_answer_df.rename(columns={'Выберите_свой_курс':'Курс','Выберите_свой_пол':'Пол'},inplace=True)
        if 'Наименование_группы' in out_answer_df.columns:
            out_answer_df.rename(columns={'Наименование_группы': 'Группа'}, inplace=True)

        # Проверяем наличие колонки с наименованием группы
        if 'Наименование_группы' not in base_df.columns:
            # Заменяем
            base_df.rename(columns={'Выберите_свой_курс': 'Курс', 'Выберите_свой_пол': 'Пол'}, inplace=True)

            # формируем словарь
            out_dct = {'Средний результат':all_result_df,'Кол_общая_тревожность':svod_all_count_df,
                       'Кол_учеб_тревожность':svod_study_count_df,'Кол_самооц_тревожность':svod_self_count_df,
                       'Кол_межлич_тревожность':svod_soc_count_df,'Списочный результат':base_df,'Список для проверки':out_answer_df}

            return out_dct, part_df
        else:

            # Делаем сводную таблицу средних значений.
            svod_all_group_df = pd.pivot_table(base_df, index=['Выберите_свой_курс','Наименование_группы', 'Выберите_свой_пол'],
                                         values=['Значение_общей_тревожности', 'Значение_учебной_тревожности',
                                                 'Значение_самооценочной_тревожности',
                                                 'Значение_межличностной_тревожности'],
                                         aggfunc=round_mean)
            svod_all_group_df.reset_index(inplace=True)
            all_result_group_df = svod_all_group_df[['Выберите_свой_курс','Наименование_группы', 'Выберите_свой_пол']]  # выделяем базовые колонки

            # Начинаем собирать свод
            all_result_group_df['Значение_общей_тревожности'] = svod_all_group_df['Значение_общей_тревожности']
            all_result_group_df['Уровень_общей_тревожности'] = all_result_group_df[
                ['Выберите_свой_курс', 'Выберите_свой_пол', 'Значение_общей_тревожности']].apply(
                calc_level_all_condash_anxiety,
                axis=1)

            all_result_group_df['Значение_учебной_тревожности'] = svod_all_group_df['Значение_учебной_тревожности']
            all_result_group_df['Уровень_учебной_тревожности'] = all_result_group_df[
                ['Выберите_свой_курс', 'Выберите_свой_пол', 'Значение_учебной_тревожности']].apply(
                calc_level_study_condash_anxiety,
                axis=1)

            all_result_group_df['Значение_самооценочной_тревожности'] = svod_all_group_df[
                'Значение_самооценочной_тревожности']
            all_result_group_df['Уровень_самооценочной_тревожности'] = all_result_group_df[
                ['Выберите_свой_курс', 'Выберите_свой_пол', 'Значение_самооценочной_тревожности']].apply(
                calc_level_self_condash_anxiety, axis=1)

            all_result_group_df['Значение_межличностной_тревожности'] = svod_all_group_df[
                'Значение_межличностной_тревожности']
            all_result_group_df['Уровень_межличностной_тревожности'] = all_result_group_df[
                ['Выберите_свой_курс', 'Выберите_свой_пол', 'Значение_межличностной_тревожности']].apply(
                calc_level_soc_condash_anxiety, axis=1)

            all_result_group_df.rename(columns={'Выберите_свой_курс': 'Курс', 'Выберите_свой_пол': 'Пол','Наименование_группы':'Группа'}, inplace=True)




            # Делаем свод по количеству
            svod_all_group_count_df = pd.pivot_table(base_df, index=['Наименование_группы', 'Выберите_свой_пол'],
                                               columns='Уровень_общей_тревожности',
                                               values='Значение_общей_тревожности',
                                               aggfunc='count', margins=True, margins_name='Итого')
            svod_all_group_count_df.reset_index(inplace=True)
            svod_all_group_count_df.rename(columns={'Выберите_свой_пол': 'Пол','Наименование_группы':'Группа'}, inplace=True)


            # Добавляем колонки с процентами
            if 'Нормальный' in svod_all_group_count_df.columns:
                svod_all_group_count_df['% Нормальный от общего'] = round(
                    svod_all_group_count_df['Нормальный'] / svod_all_group_count_df['Итого'], 2)

            if 'Несколько повышенный' in svod_all_group_count_df.columns:
                svod_all_group_count_df['% Несколько повышенный от общего'] = round(
                    svod_all_group_count_df['Несколько повышенный'] / svod_all_group_count_df['Итого'], 2)
            if 'Высокий' in svod_all_group_count_df.columns:
                svod_all_group_count_df['% Высокий от общего'] = round(svod_all_group_count_df['Высокий'] / svod_all_group_count_df['Итого'],
                                                                 2)
            if 'Очень высокий' in svod_all_group_count_df.columns:
                svod_all_group_count_df['% Очень высокий от общего'] = round(
                    svod_all_group_count_df['Очень высокий'] / svod_all_group_count_df['Итого'], 2)
            if 'Чрезмерное спокойствие' in svod_all_group_count_df.columns:
                svod_all_group_count_df['% Чрезмерное спокойствие от общего'] = round(
                    svod_all_group_count_df['Чрезмерное спокойствие'] / svod_all_group_count_df['Итого'], 2)

            # свод по учебной тревожности
            svod_study_group_count_df = pd.pivot_table(base_df, index=['Наименование_группы', 'Выберите_свой_пол'],
                                                       columns='Уровень_учебной_тревожности',
                                                       values='Значение_учебной_тревожности',
                                                       aggfunc='count', margins=True, margins_name='Итого')
            svod_study_group_count_df.reset_index(inplace=True)
            svod_study_group_count_df.rename(columns={'Наименование_группы': 'Группа', 'Выберите_свой_пол': 'Пол'},
                                             inplace=True)

            # Добавляем колонки с процентами
            if 'Нормальный' in svod_study_group_count_df.columns:
                svod_study_group_count_df['% Нормальный от общего'] = round(
                    svod_study_group_count_df['Нормальный'] / svod_study_group_count_df['Итого'], 2)

            if 'Несколько повышенный' in svod_study_group_count_df.columns:
                svod_study_group_count_df['% Несколько повышенный от общего'] = round(
                    svod_study_group_count_df['Несколько повышенный'] / svod_study_group_count_df['Итого'], 2)
            if 'Высокий' in svod_study_group_count_df.columns:
                svod_study_group_count_df['% Высокий от общего'] = round(
                    svod_study_group_count_df['Высокий'] / svod_study_group_count_df['Итого'], 2)
            if 'Очень высокий' in svod_study_group_count_df.columns:
                svod_study_group_count_df['% Очень высокий от общего'] = round(
                    svod_study_group_count_df['Очень высокий'] / svod_study_group_count_df['Итого'], 2)
            if 'Чрезмерное спокойствие' in svod_study_group_count_df.columns:
                svod_study_group_count_df['% Чрезмерное спокойствие от общего'] = round(
                    svod_study_group_count_df['Чрезмерное спокойствие'] / svod_study_group_count_df['Итого'], 2)

            # свод по самооценочной тревожности
            svod_self_group_count_df = pd.pivot_table(base_df, index=['Наименование_группы', 'Выберите_свой_пол'],
                                                      columns='Уровень_самооценочной_тревожности',
                                                      values='Значение_самооценочной_тревожности',
                                                      aggfunc='count', margins=True, margins_name='Итого')
            svod_self_group_count_df.reset_index(inplace=True)
            svod_self_group_count_df.rename(columns={'Наименование_группы': 'Группа', 'Выберите_свой_пол': 'Пол'},
                                            inplace=True)

            if 'Нормальный' in svod_self_group_count_df.columns:
                svod_self_group_count_df['% Нормальный от общего'] = round(
                    svod_self_group_count_df['Нормальный'] / svod_self_group_count_df['Итого'], 2)

            if 'Несколько повышенный' in svod_self_group_count_df.columns:
                svod_self_group_count_df['% Несколько повышенный от общего'] = round(
                    svod_self_group_count_df['Несколько повышенный'] / svod_self_group_count_df['Итого'], 2)
            if 'Высокий' in svod_self_group_count_df.columns:
                svod_self_group_count_df['% Высокий от общего'] = round(
                    svod_self_group_count_df['Высокий'] / svod_self_group_count_df['Итого'],
                    2)
            if 'Очень высокий' in svod_self_group_count_df.columns:
                svod_self_group_count_df['% Очень высокий от общего'] = round(
                    svod_self_group_count_df['Очень высокий'] / svod_self_group_count_df['Итого'], 2)
            if 'Чрезмерное спокойствие' in svod_self_group_count_df.columns:
                svod_self_group_count_df['% Чрезмерное спокойствие от общего'] = round(
                    svod_self_group_count_df['Чрезмерное спокойствие'] / svod_self_group_count_df['Итого'], 2)

            # свод по межличностной тревожности
            svod_soc_group_count_df = pd.pivot_table(base_df, index=['Наименование_группы', 'Выберите_свой_пол'],
                                                     columns='Уровень_межличностной_тревожности',
                                                     values='Значение_межличностной_тревожности',
                                                     aggfunc='count', margins=True, margins_name='Итого')
            svod_soc_group_count_df.reset_index(inplace=True)
            svod_soc_group_count_df.rename(columns={'Наименование_группы': 'Группа', 'Выберите_свой_пол': 'Пол'}, inplace=True)

            if 'Нормальный' in svod_soc_group_count_df.columns:
                svod_soc_group_count_df['% Нормальный от общего'] = round(
                    svod_soc_group_count_df['Нормальный'] / svod_soc_group_count_df['Итого'], 2)

            if 'Несколько повышенный' in svod_soc_group_count_df.columns:
                svod_soc_group_count_df['% Несколько повышенный от общего'] = round(
                    svod_soc_group_count_df['Несколько повышенный'] / svod_soc_group_count_df['Итого'], 2)
            if 'Высокий' in svod_soc_group_count_df.columns:
                svod_soc_group_count_df['% Высокий от общего'] = round(
                    svod_soc_group_count_df['Высокий'] / svod_soc_group_count_df['Итого'],
                    2)
            if 'Очень высокий' in svod_soc_group_count_df.columns:
                svod_soc_group_count_df['% Очень высокий от общего'] = round(
                    svod_soc_group_count_df['Очень высокий'] / svod_soc_group_count_df['Итого'], 2)
            if 'Чрезмерное спокойствие' in svod_soc_group_count_df.columns:
                svod_soc_group_count_df['% Чрезмерное спокойствие от общего'] = round(
                    svod_soc_group_count_df['Чрезмерное спокойствие'] / svod_soc_group_count_df['Итого'], 2)

            # Заменяем
            base_df.rename(columns={'Выберите_свой_курс': 'Курс', 'Выберите_свой_пол': 'Пол'}, inplace=True)
            if 'Наименование_группы' in base_df.columns:
                base_df.rename(columns={'Наименование_группы': 'Группа'}, inplace=True)

            # формируем словарь
            out_dct = {'Списочный результат':base_df,'Список для проверки':out_answer_df,
                       'Средний результат':all_result_df,'Кол_общая_тревожность':svod_all_count_df,
                       'Кол_учеб_тревожность':svod_study_count_df,'Кол_самооц_тревожность':svod_self_count_df,
                       'Кол_межлич_тревожность':svod_soc_count_df,
                       'Групп_Ср_рез':all_result_group_df,
                       'Групп_Кол_общ_трев':svod_all_group_count_df,
                       'Групп_Кол_учеб_трев':svod_study_group_count_df,
                       'Групп_Кол_сам_трев':svod_self_group_count_df,
                       'Групп_Кол_меж_трев':svod_soc_group_count_df,
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







