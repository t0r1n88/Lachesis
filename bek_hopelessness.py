"""
Скрипт для обработки результатов теста Шкала безадежности Бека
"""
from lachesis_support_functions import round_mean
import pandas as pd
from tkinter import messagebox


class BadOrderBekHopelessness(Exception):
    """
    Исключение для обработки случая когда колонки не совпадают
    """
    pass


class BadValueBekHopelessness(Exception):
    """
    Исключение для неправильных значений в вариантах ответов
    """
    pass


class BadCountColumnsBekHopelessness(Exception):
    """
    Исключение для обработки случая если количество колонок не равно 20
    """
    pass

def calc_value_hopelessness(row):
    """
    Функция для подсчета уровня безнадежности
    :param row: строка с ответами респондента
    :return:
    """
    value_hopelessness = 0 # счетчик безнадежности
    # обрабатываем
    if row[0] == 'НЕВЕРНО':
        value_hopelessness += 1
    if row[1] == 'ВЕРНО':
        value_hopelessness += 1
    if row[2] == 'НЕВЕРНО':
        value_hopelessness += 1
    if row[3] == 'ВЕРНО':
        value_hopelessness += 1
    if row[4] == 'НЕВЕРНО':
        value_hopelessness += 1

    if row[5] == 'НЕВЕРНО':
        value_hopelessness += 1
    if row[6] == 'ВЕРНО':
        value_hopelessness += 1
    if row[7] == 'НЕВЕРНО':
        value_hopelessness += 1
    if row[8] == 'ВЕРНО':
        value_hopelessness += 1
    if row[9] == 'НЕВЕРНО':
        value_hopelessness += 1

    if row[10] == 'ВЕРНО':
        value_hopelessness += 1
    if row[11] == 'ВЕРНО':
        value_hopelessness += 1
    if row[12] == 'НЕВЕРНО':
        value_hopelessness += 1
    if row[13] == 'ВЕРНО':
        value_hopelessness += 1
    if row[14] == 'НЕВЕРНО':
        value_hopelessness += 1

    if row[15] == 'ВЕРНО':
        value_hopelessness += 1
    if row[16] == 'ВЕРНО':
        value_hopelessness += 1
    if row[17] == 'ВЕРНО':
        value_hopelessness += 1
    if row[18] == 'НЕВЕРНО':
        value_hopelessness += 1
    if row[19] == 'ВЕРНО':
        value_hopelessness += 1

    return value_hopelessness

def calc_level_hopelessness(value):
    """
    Функция для вычисления уровня безнадежности
    :param value: числовое значение
    :return: строка с уровнем
    """
    if 0 <= value <= 3:
        return 'безнадёжность не выявлена'
    elif 4 <= value <= 8:
        return 'безнадежность лёгкая'
    elif 9 <= value <= 14:
        return 'безнадежность умеренная'
    elif value >= 15:
        return 'безнадежность тяжёлая'







def processing_bek_hopelessness(base_df: pd.DataFrame, answers_df: pd.DataFrame):
    out_answer_df = base_df.copy()  # делаем копию для последующего соединения с сырыми ответами
    if len(answers_df.columns) != 20:
        raise BadCountColumnsBekHopelessness


    # Словарь с проверочными данными
    lst_check_cols = ['Я жду будущего с надеждой и энтузиазмом',
                      'Мне пора сдаться, т.к. я ничего не могу изменить к лучшему',
                      'Когда дела идут плохо, мне помогает мысль, что так не может продолжаться всегда',
                      'Я не могу представить, на что будет похожа моя жизнь через 10 лет',
                      'У меня достаточно времени, чтобы завершить дела, которыми я больше всего хочу заниматься',
                      'В будущем, я надеюсь достичь успеха в том, что мне больше всего нравится',
                      'Будущее представляется мне во тьме',
                      'Я надеюсь получить в жизни больше хорошего, чем средний человек',
                      'У меня нет никаких просветов и нет причин верить, что они появятся в будущем',
                      'Мой прошлый опыт хорошо меня подготовил к будущему',
                      'Всё, что я вижу впереди - скорее, неприятности, чем радости',
                      'Я не надеюсь достичь того, чего действительно хочу',
                      'Когда я заглядываю в будущее, я надеюсь быть счастливее, чем я есть сейчас',
                      'Дела идут не так, как мне хочется',
                      'Я сильно верю в своё будущее',
                      'Я никогда не достигаю того, что хочу, поэтому глупо что-либо хотеть',
                      'Весьма маловероятно, что я получу реальное удовлетворение в будущем',
                      'Будущее представляется- мне расплывчатым и неопределённым',
                      'В будущем меня ждёт больше хороших дней, чем плохих',
                      'Бесполезно пытаться получить то, что я хочу, потому что, вероятно, я не добьюсь этого'
                      ]

    # Проверяем порядок колонок
    order_main_columns = lst_check_cols  # порядок колонок и названий как должно быть
    order_temp_df_columns = list(answers_df.columns)  # порядок колонок проверяемого файла
    error_order_lst = []  # список для несовпадающих пар
    # Сравниваем попарно колонки
    for main, temp in zip(order_main_columns, order_temp_df_columns):
        if main != temp:
            error_order_lst.append(f'На месте колонки {main} находится колонка {temp}')
    if len(error_order_lst) != 0:
        raise BadOrderBekHopelessness

    valid_values = ['ВЕРНО','НЕВЕРНО']

    # Проверяем, есть ли значения, отличающиеся от указанных в списке
    mask = ~answers_df.isin(valid_values)

    # Получаем строки с отличающимися значениями
    result_check = answers_df[mask.any(axis=1)]
    if len(result_check) != 0:
        error_row = list(map(lambda x: x + 2, result_check.index))
        error_row = list(map(str, error_row))
        error_message = ';'.join(error_row)
        raise BadValueBekHopelessness

    base_df['Значение_безнадежности'] = answers_df.apply(calc_value_hopelessness, axis=1)
    base_df['Уровень_безнадежности'] = base_df['Значение_безнадежности'].apply(calc_level_hopelessness)
    base_df.sort_values(by='Значение_безнадежности', ascending=False, inplace=True)  # сортируем


    # Делаем сводную таблицу по курсу
    svod_all_course_df = pd.pivot_table(base_df, index=['Выберите_свой_курс'],
                                 values=['Значение_безнадежности'],
                                 aggfunc=round_mean)
    svod_all_course_df.reset_index(inplace=True)
    svod_all_course_df['Уровень_безнадежности'] = svod_all_course_df['Значение_безнадежности'].apply(
        calc_level_hopelessness)  # считаем уровень
    svod_all_course_df.rename(columns={'Выберите_свой_курс': 'Курс'}, inplace=True)


    # делаем сводную по курсу
    svod_all_count_course_df = pd.pivot_table(base_df, index=['Выберите_свой_курс'],
                                              columns='Уровень_безнадежности',
                                              values='Значение_безнадежности',
                                              aggfunc='count', margins=True, margins_name='Итого')
    svod_all_count_course_df.reset_index(inplace=True)
    svod_all_count_course_df.rename(columns={'Выберите_свой_курс': 'Курс'}, inplace=True)
    if 'удовлетворительное эмоциональное состояние' in svod_all_count_course_df.columns:
        svod_all_count_course_df['% удовлетворительное эмоциональное состояние от общего'] = round(
            svod_all_count_course_df['удовлетворительное эмоциональное состояние'] / svod_all_count_course_df[
                'Итого'], 2)

    if 'безнадёжность не выявлена' in svod_all_count_course_df.columns:
        svod_all_count_course_df['% безнадёжность не выявлена  от общего'] = round(
            svod_all_count_course_df['безнадёжность не выявлена'] / svod_all_count_course_df['Итого'], 2)
    if 'безнадежность лёгкая' in svod_all_count_course_df.columns:
        svod_all_count_course_df['% безнадежность лёгкая от общего'] = round(
            svod_all_count_course_df['безнадежность лёгкая'] / svod_all_count_course_df['Итого'], 2)
    if 'безнадежность умеренная' in svod_all_count_course_df.columns:
        svod_all_count_course_df['% безнадежность умеренная от общего'] = round(
            svod_all_count_course_df['безнадежность умеренная'] / svod_all_count_course_df['Итого'], 2)
    if 'безнадежность тяжёлая' in svod_all_count_course_df.columns:
        svod_all_count_course_df['% безнадежность тяжёлая от общего'] = round(
            svod_all_count_course_df['безнадежность тяжёлая'] / svod_all_count_course_df['Итого'], 2)


    # Делаем сводную таблицу средних значений для курса и пола.
    svod_all_course_sex_df = pd.pivot_table(base_df, index=['Выберите_свой_курс', 'Выберите_свой_пол'],
                                 values=['Значение_безнадежности'],
                                 aggfunc=round_mean)
    svod_all_course_sex_df.reset_index(inplace=True)
    svod_all_course_sex_df['Уровень_безнадежности'] = svod_all_course_sex_df['Значение_безнадежности'].apply(
        calc_level_hopelessness)  # считаем уровень
    svod_all_course_sex_df.rename(columns={'Выберите_свой_курс': 'Курс', 'Выберите_свой_пол': 'Пол'}, inplace=True)




    # Делаем свод по количеству
    svod_all_count_course_sex_df = pd.pivot_table(base_df, index=['Выберите_свой_курс', 'Выберите_свой_пол'],
                                       columns='Уровень_безнадежности',
                                       values='Значение_безнадежности',
                                       aggfunc='count', margins=True, margins_name='Итого')
    svod_all_count_course_sex_df.reset_index(inplace=True)
    svod_all_count_course_sex_df.rename(columns={'Выберите_свой_курс': 'Курс', 'Выберите_свой_пол': 'Пол'}, inplace=True)
    if 'удовлетворительное эмоциональное состояние' in svod_all_count_course_sex_df.columns:
        svod_all_count_course_sex_df['% удовлетворительное эмоциональное состояние от общего'] = round(
            svod_all_count_course_sex_df['удовлетворительное эмоциональное состояние'] / svod_all_count_course_sex_df['Итого'], 2)

    if 'безнадёжность не выявлена' in svod_all_count_course_sex_df.columns:
        svod_all_count_course_sex_df['% безнадёжность не выявлена  от общего'] = round(
            svod_all_count_course_sex_df['безнадёжность не выявлена'] / svod_all_count_course_sex_df['Итого'], 2)
    if 'безнадежность лёгкая' in svod_all_count_course_sex_df.columns:
        svod_all_count_course_sex_df['% безнадежность лёгкая от общего'] = round(
            svod_all_count_course_sex_df['безнадежность лёгкая'] / svod_all_count_course_sex_df['Итого'], 2)
    if 'безнадежность умеренная' in svod_all_count_course_sex_df.columns:
        svod_all_count_course_sex_df['% безнадежность умеренная от общего'] = round(
            svod_all_count_course_sex_df['безнадежность умеренная'] / svod_all_count_course_sex_df['Итого'], 2)
    if 'безнадежность тяжёлая' in svod_all_count_course_sex_df.columns:
        svod_all_count_course_sex_df['% безнадежность тяжёлая от общего'] = round(
            svod_all_count_course_sex_df['безнадежность тяжёлая'] / svod_all_count_course_sex_df['Итого'], 2)

    # Датафрейм для проверки

    out_answer_df = pd.concat([out_answer_df, answers_df], axis=1)
    out_answer_df.rename(columns={'Выберите_свой_курс': 'Курс', 'Выберите_свой_пол': 'Пол'}, inplace=True)
    if 'Наименование_группы' in out_answer_df.columns:
        out_answer_df.rename(columns={'Наименование_группы': 'Группа'}, inplace=True)


    # Проверяем наличие колонки с наименованием группы
    if 'Наименование_группы' not in base_df.columns:
        # Заменяем
        base_df.rename(columns={'Выберите_свой_курс': 'Курс', 'Выберите_свой_пол': 'Пол'}, inplace=True)

        # формируем словарь
        out_dct = {'Списочный результат': base_df, 'Список для проверки': out_answer_df,
                   'Среднее по курсу': svod_all_course_df, 'Количество по курсу': svod_all_count_course_df,
                   'Среднее по курсу и полу': svod_all_course_sex_df, 'Количество по курсу и полу': svod_all_count_course_sex_df}

        return out_dct

    else:

        # Делаем сводную таблицу по группам
        svod_all_group_df = pd.pivot_table(base_df, index=['Наименование_группы'],
                                           values=['Значение_безнадежности'],
                                           aggfunc=round_mean)
        svod_all_group_df.reset_index(inplace=True)
        svod_all_group_df['Уровень_безнадежности'] = svod_all_group_df['Значение_безнадежности'].apply(
            calc_level_hopelessness)  # считаем уровень
        svod_all_group_df.rename(columns={'Наименование_группы': 'Группа'}, inplace=True)

        # делаем сводную по курсу
        svod_all_count_group_df = pd.pivot_table(base_df, index=['Наименование_группы'],
                                                 columns='Уровень_безнадежности',
                                                 values='Значение_безнадежности',
                                                 aggfunc='count', margins=True, margins_name='Итого')
        svod_all_count_group_df.reset_index(inplace=True)
        svod_all_count_group_df.rename(columns={'Наименование_группы': 'Группа'}, inplace=True)
        if 'удовлетворительное эмоциональное состояние' in svod_all_count_group_df.columns:
            svod_all_count_group_df['% удовлетворительное эмоциональное состояние от общего'] = round(
                svod_all_count_group_df['удовлетворительное эмоциональное состояние'] / svod_all_count_group_df[
                    'Итого'], 2)

        if 'безнадёжность не выявлена' in svod_all_count_group_df.columns:
            svod_all_count_group_df['% безнадёжность не выявлена  от общего'] = round(
                svod_all_count_group_df['безнадёжность не выявлена'] / svod_all_count_group_df['Итого'], 2)
        if 'безнадежность лёгкая' in svod_all_count_group_df.columns:
            svod_all_count_group_df['% безнадежность лёгкая от общего'] = round(
                svod_all_count_group_df['безнадежность лёгкая'] / svod_all_count_group_df['Итого'], 2)
        if 'безнадежность умеренная' in svod_all_count_group_df.columns:
            svod_all_count_group_df['% безнадежность умеренная от общего'] = round(
                svod_all_count_group_df['безнадежность умеренная'] / svod_all_count_group_df['Итого'], 2)
        if 'безнадежность тяжёлая' in svod_all_count_group_df.columns:
            svod_all_count_group_df['% безнадежность тяжёлая от общего'] = round(
                svod_all_count_group_df['безнадежность тяжёлая'] / svod_all_count_group_df['Итого'], 2)

        # Делаем сводную таблицу средних значений для группы и пола.
        svod_all_group_sex_df = pd.pivot_table(base_df, index=['Наименование_группы', 'Выберите_свой_пол'],
                                               values=['Значение_безнадежности'],
                                               aggfunc=round_mean)
        svod_all_group_sex_df.reset_index(inplace=True)
        svod_all_group_sex_df['Уровень_безнадежности'] = svod_all_group_sex_df['Значение_безнадежности'].apply(
            calc_level_hopelessness)  # считаем уровень
        svod_all_group_sex_df.rename(columns={'Наименование_группы': 'Группа', 'Выберите_свой_пол': 'Пол'},
                                     inplace=True)

        # Делаем свод по количеству для группы и пола
        svod_all_count_group_sex_df = pd.pivot_table(base_df, index=['Наименование_группы', 'Выберите_свой_пол'],
                                                     columns='Уровень_безнадежности',
                                                     values='Значение_безнадежности',
                                                     aggfunc='count', margins=True, margins_name='Итого')
        svod_all_count_group_sex_df.reset_index(inplace=True)
        svod_all_count_group_sex_df.rename(columns={'Наименование_группы': 'Группа', 'Выберите_свой_пол': 'Пол'},
                                           inplace=True)
        if 'удовлетворительное эмоциональное состояние' in svod_all_count_group_sex_df.columns:
            svod_all_count_group_sex_df['% удовлетворительное эмоциональное состояние от общего'] = round(
                svod_all_count_group_sex_df['удовлетворительное эмоциональное состояние'] /
                svod_all_count_group_sex_df['Итого'], 2)

        if 'безнадёжность не выявлена' in svod_all_count_group_sex_df.columns:
            svod_all_count_group_sex_df['% безнадёжность не выявлена  от общего'] = round(
                svod_all_count_group_sex_df['безнадёжность не выявлена'] / svod_all_count_group_sex_df['Итого'], 2)
        if 'безнадежность лёгкая' in svod_all_count_group_sex_df.columns:
            svod_all_count_group_sex_df['% безнадежность лёгкая от общего'] = round(
                svod_all_count_group_sex_df['безнадежность лёгкая'] / svod_all_count_group_sex_df['Итого'], 2)
        if 'безнадежность умеренная' in svod_all_count_group_sex_df.columns:
            svod_all_count_group_sex_df['% безнадежность умеренная от общего'] = round(
                svod_all_count_group_sex_df['безнадежность умеренная'] / svod_all_count_group_sex_df['Итого'], 2)
        if 'безнадежность тяжёлая' in svod_all_count_group_sex_df.columns:
            svod_all_count_group_sex_df['% безнадежность тяжёлая от общего'] = round(
                svod_all_count_group_sex_df['безнадежность тяжёлая'] / svod_all_count_group_sex_df['Итого'], 2)


        base_df.rename(columns={'Выберите_свой_курс': 'Курс', 'Выберите_свой_пол': 'Пол','Наименование_группы':'Группа'}, inplace=True)

        # формируем словарь
        out_dct = {'Списочный результат': base_df, 'Список для проверки': out_answer_df,
                   'Среднее по курсу': svod_all_course_df, 'Количество по курсу': svod_all_count_course_df,
                   'Среднее по курсу и полу': svod_all_course_sex_df,
                   'Количество по курсу и полу': svod_all_count_course_sex_df,
                   'Среднее по группам': svod_all_group_df, 'Количество по группам': svod_all_count_group_df,
                   'Среднее по группам и полам': svod_all_group_sex_df, 'Количество по группам и полам': svod_all_count_group_sex_df}

        return out_dct
