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
    try:

        out_answer_df = base_df.copy()  # делаем копию для последующего соединения с сырыми ответами
        if len(answers_df.columns) != 20:
            raise BadCountColumnsBekHopelessness


        # Словарь для проверки вопросов
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
                error_order_message = ';'.join(error_order_lst)
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
        base_df['Значение_нормы'] = '0-8 баллов'
        base_df['Уровень_безнадежности'] = base_df['Значение_безнадежности'].apply(calc_level_hopelessness)


        # Создаем датафрейм для создания части в общий датафрейм
        part_df = pd.DataFrame(columns=['Значение_безнадежности_Бек','Уровень_безнадежности_Бек'])
        part_df['Значение_безнадежности_Бек'] = base_df['Значение_безнадежности']
        part_df['Уровень_безнадежности_Бек'] = base_df['Уровень_безнадежности']



        base_df.sort_values(by='Значение_безнадежности', ascending=False, inplace=True)  # сортируем


        # Делаем сводную таблицу по курсу
        svod_all_course_df = pd.pivot_table(base_df, index=['Курс'],
                                     values=['Значение_безнадежности'],
                                     aggfunc=round_mean)
        svod_all_course_df.reset_index(inplace=True)
        svod_all_course_df['Уровень_безнадежности'] = svod_all_course_df['Значение_безнадежности'].apply(
            calc_level_hopelessness)  # считаем уровень


        # делаем сводную по курсу
        svod_all_count_course_df = pd.pivot_table(base_df, index=['Курс'],
                                                  columns='Уровень_безнадежности',
                                                  values='Значение_безнадежности',
                                                  aggfunc='count', margins=True, margins_name='Итого')
        svod_all_count_course_df.reset_index(inplace=True)
        svod_all_count_course_df = svod_all_count_course_df.reindex(
            columns=['Курс', 'безнадёжность не выявлена', 'безнадежность лёгкая',
                     'безнадежность умеренная', 'безнадежность тяжёлая',
                     'Итого'])


        svod_all_count_course_df['% безнадёжность не выявлена  от общего'] = round(
            svod_all_count_course_df['безнадёжность не выявлена'] / svod_all_count_course_df['Итого'], 2)*100

        svod_all_count_course_df['% безнадежность лёгкая от общего'] = round(
            svod_all_count_course_df['безнадежность лёгкая'] / svod_all_count_course_df['Итого'], 2)*100

        svod_all_count_course_df['% безнадежность умеренная от общего'] = round(
            svod_all_count_course_df['безнадежность умеренная'] / svod_all_count_course_df['Итого'], 2)*100

        svod_all_count_course_df['% безнадежность тяжёлая от общего'] = round(
            svod_all_count_course_df['безнадежность тяжёлая'] / svod_all_count_course_df['Итого'], 2)*100



        # Делаем сводную таблицу средних значений для курса и пола.
        svod_all_course_sex_df = pd.pivot_table(base_df, index=['Курс', 'Пол'],
                                     values=['Значение_безнадежности'],
                                     aggfunc=round_mean)
        svod_all_course_sex_df.reset_index(inplace=True)
        svod_all_course_sex_df['Уровень_безнадежности'] = svod_all_course_sex_df['Значение_безнадежности'].apply(
            calc_level_hopelessness)  # считаем уровень

        # Делаем свод по количеству
        svod_all_count_course_sex_df = pd.pivot_table(base_df, index=['Курс', 'Пол'],
                                           columns='Уровень_безнадежности',
                                           values='Значение_безнадежности',
                                           aggfunc='count', margins=True, margins_name='Итого')
        svod_all_count_course_sex_df.reset_index(inplace=True)
        svod_all_count_course_sex_df = svod_all_count_course_sex_df.reindex(
            columns=['Курс', 'Пол', 'безнадёжность не выявлена', 'безнадежность лёгкая',
                     'безнадежность умеренная', 'безнадежность тяжёлая',
                     'Итого'])


        svod_all_count_course_sex_df['% безнадёжность не выявлена  от общего'] = round(
            svod_all_count_course_sex_df['безнадёжность не выявлена'] / svod_all_count_course_sex_df['Итого'], 2)*100

        svod_all_count_course_sex_df['% безнадежность лёгкая от общего'] = round(
            svod_all_count_course_sex_df['безнадежность лёгкая'] / svod_all_count_course_sex_df['Итого'], 2)*100

        svod_all_count_course_sex_df['% безнадежность умеренная от общего'] = round(
            svod_all_count_course_sex_df['безнадежность умеренная'] / svod_all_count_course_sex_df['Итого'], 2)*100

        svod_all_count_course_sex_df['% безнадежность тяжёлая от общего'] = round(
            svod_all_count_course_sex_df['безнадежность тяжёлая'] / svod_all_count_course_sex_df['Итого'], 2)*100


        # Датафрейм для проверки

        out_answer_df = pd.concat([out_answer_df, answers_df], axis=1)


        # Делаем сводную таблицу по группам
        svod_all_group_df = pd.pivot_table(base_df, index=['Группа'],
                                           values=['Значение_безнадежности'],
                                           aggfunc=round_mean)
        svod_all_group_df.reset_index(inplace=True)
        svod_all_group_df['Уровень_безнадежности'] = svod_all_group_df['Значение_безнадежности'].apply(
            calc_level_hopelessness)  # считаем уровень

        # делаем сводную по курсу
        svod_all_count_group_df = pd.pivot_table(base_df, index=['Группа'],
                                                 columns='Уровень_безнадежности',
                                                 values='Значение_безнадежности',
                                                 aggfunc='count', margins=True, margins_name='Итого')
        svod_all_count_group_df.reset_index(inplace=True)
        svod_all_count_group_df = svod_all_count_group_df.reindex(
            columns=['Группа', 'безнадёжность не выявлена', 'безнадежность лёгкая',
                     'безнадежность умеренная', 'безнадежность тяжёлая',
                     'Итого'])


        svod_all_count_group_df['% безнадёжность не выявлена  от общего'] = round(
            svod_all_count_group_df['безнадёжность не выявлена'] / svod_all_count_group_df['Итого'], 2)*100

        svod_all_count_group_df['% безнадежность лёгкая от общего'] = round(
            svod_all_count_group_df['безнадежность лёгкая'] / svod_all_count_group_df['Итого'], 2)*100

        svod_all_count_group_df['% безнадежность умеренная от общего'] = round(
            svod_all_count_group_df['безнадежность умеренная'] / svod_all_count_group_df['Итого'], 2)*100

        svod_all_count_group_df['% безнадежность тяжёлая от общего'] = round(
            svod_all_count_group_df['безнадежность тяжёлая'] / svod_all_count_group_df['Итого'], 2)*100


        # Делаем сводную таблицу средних значений для группы и пола.
        svod_all_group_sex_df = pd.pivot_table(base_df, index=['Группа', 'Пол'],
                                               values=['Значение_безнадежности'],
                                               aggfunc=round_mean)
        svod_all_group_sex_df.reset_index(inplace=True)
        svod_all_group_sex_df['Уровень_безнадежности'] = svod_all_group_sex_df['Значение_безнадежности'].apply(
            calc_level_hopelessness)  # считаем уровень

        # Делаем свод по количеству для группы и пола
        svod_all_count_group_sex_df = pd.pivot_table(base_df, index=['Группа', 'Пол'],
                                                     columns='Уровень_безнадежности',
                                                     values='Значение_безнадежности',
                                                     aggfunc='count', margins=True, margins_name='Итого')
        svod_all_count_group_sex_df.reset_index(inplace=True)
        svod_all_count_group_sex_df = svod_all_count_group_sex_df.reindex(
            columns=['Группа', 'Пол', 'безнадёжность не выявлена', 'безнадежность лёгкая',
                     'безнадежность умеренная', 'безнадежность тяжёлая',
                     'Итого'])

        svod_all_count_group_sex_df['% безнадёжность не выявлена  от общего'] = round(
            svod_all_count_group_sex_df['безнадёжность не выявлена'] / svod_all_count_group_sex_df['Итого'], 2)*100

        svod_all_count_group_sex_df['% безнадежность лёгкая от общего'] = round(
            svod_all_count_group_sex_df['безнадежность лёгкая'] / svod_all_count_group_sex_df['Итого'], 2)*100

        svod_all_count_group_sex_df['% безнадежность умеренная от общего'] = round(
            svod_all_count_group_sex_df['безнадежность умеренная'] / svod_all_count_group_sex_df['Итого'], 2)*100

        svod_all_count_group_sex_df['% безнадежность тяжёлая от общего'] = round(
            svod_all_count_group_sex_df['безнадежность тяжёлая'] / svod_all_count_group_sex_df['Итого'], 2)*100


        # Общий свод сколько склонностей всего в процентном соотношении
        base_svod_all_df = pd.DataFrame(index=['безнадёжность не выявлена','безнадежность лёгкая','безнадежность умеренная','безнадежность тяжёлая','Итого'])

        svod_all_df = pd.pivot_table(base_df, index='Уровень_безнадежности',
                                     values='Значение_безнадежности',
                                     aggfunc='count')

        svod_all_df['% от общего'] = round(
            svod_all_df['Значение_безнадежности'] / svod_all_df['Значение_безнадежности'].sum(), 3) * 100
        # # Создаем суммирующую строку
        svod_all_df.loc['Итого'] = svod_all_df.sum()

        base_svod_all_df =base_svod_all_df.join(svod_all_df)


        base_svod_all_df.reset_index(inplace=True)
        base_svod_all_df.rename(columns={'index': 'Уровень безнадежности', 'Значение_безнадежности': 'Количество'}, inplace=True)


        # формируем словарь
        out_dct = {'Списочный результат': base_df, 'Список для проверки': out_answer_df,
                   'Общий свод':base_svod_all_df,
                   'Среднее по группам': svod_all_group_df, 'Количество по группам': svod_all_count_group_df,
                   'Среднее по группам и полам': svod_all_group_sex_df,
                   'Количество по группам и полам': svod_all_count_group_sex_df,
                   'Среднее по курсу': svod_all_course_df, 'Количество по курсу': svod_all_count_course_df,
                   'Среднее по курсу и полу': svod_all_course_sex_df,'Количество по курсу и полу': svod_all_count_course_sex_df

                   }

        return out_dct, part_df

    except BadOrderBekHopelessness:
        messagebox.showerror('Лахеcис',
                             f'При обработке вопросов теста Шкала безнадежности Бека обнаружены неправильные вопросы. Проверьте названия колонок с вопросами:\n'
                             f'{error_order_message}\n'
                             f'Используйте при создании Яндекс-формы написание вопросов из руководства пользователя программы Лахесис.')
    except BadValueBekHopelessness:
        messagebox.showerror('Лахеcис',
                             f'При обработке вопросов теста Шкала безнадежности Бека обнаружены неправильные варианты ответов. Проверьте ответы на указанных строках:\n'
                             f'{error_message}\n'
                             f'Используйте при создании Яндекс-формы написание вариантов ответа из руководства пользователя программы Лахесис.')

    except BadCountColumnsBekHopelessness:
        messagebox.showerror('Лахеcис',
                             f'Проверьте количество колонок с ответами на тест Шкала безнадежности Бека\n'
                             f'Должно быть 20 колонок с вопросами'
                            )

