"""
Скрипт для обработки результатов теста уровень самооценки Ковалева
"""


import pandas as pd
from tkinter import messagebox
from lachesis_support_functions import round_mean


class BadOrderUSK(Exception):
    """
    Исключение для обработки случая когда колонки не совпадают
    """
    pass


class BadValueUSK(Exception):
    """
    Исключение для неправильных значений в вариантах ответов
    """
    pass

class BadCountColumnsUSK(Exception):
    """
    Исключение для обработки случая если количество колонок не равно 32
    """
    pass



def calc_value_usk(row):
    """
    Функция для подсчета значения уровня самооценки Ковалева
    :param row: строка с ответами
    :return: число
    """
    sum_row = sum(row) # получаем сумму
    return sum_row

def calc_level_usk(value):
    """
    Функция для подсчета уровня самооценки
    :param value:
    :return:
    """
    if 0 <= value <= 25:
        return 'Высокий уровень самооценки'
    elif 26 <= value <= 45:
        return 'Средний уровень самооценки'
    elif 46 <= value <= 128:
        return 'Низкий уровень самооценки'







def processing_usk(base_df: pd.DataFrame, answers_df: pd.DataFrame):
    """
    Функция для обработки
    :param base_df: часть датафрейма с описательными колонками
    :param answers_df: часть датафрейма с ответами
    :param size: количество колонок которое должно быть в answers_df
    :param name_test: название теста
    :param threshold_base: количество колонок
    :param end_folder: конечная папка для сохранения
    """
    try:

        out_answer_df = base_df.copy()  # делаем копию для последующего соединения с сырыми ответами
        if len(answers_df.columns) != 32:  # проверяем количество колонок с вопросами
            raise BadCountColumnsUSK

        # Словарь с проверочными данными
        lst_check_cols = ['Мне хочется, чтобы мои друзья подбадривали меня',
                          'Постоянно чувствую свою ответственность за работу (учебу)',
                          'Я беспокоюсь о своем будущем',
                          'Многие меня ненавидят',
                          'Я обладаю меньшей инициативой, нежели другие',
                          'Я беспокоюсь за свое психическое состояние',
                          'Я боюсь выглядеть глупцом',
                          'Внешний вид других куда лучше, чем мой',
                          'Я боюсь выступать с речью перед незнакомыми людьми',
                          'Я часто допускаю ошибки',
                          'Как жаль, что я не умею говорить, как следует с людьми',
                          'Как жаль, что мне не хватает уверенности в себе',
                          'Мне бы хотелось, чтобы мои действия ободрялись другими чаще',
                          'Я слишком скромен',
                          'Моя жизнь бесполезна',
                          'Многие неправильного мнения обо мне',
                          'Мне не с кем поделиться своими мыслями',
                          'Люди ждут от меня многого',
                          'Люди не особенно интересуются моими достижениями',
                          'Я слегка смущаюсь',
                          'Я чувствую, что многие люди не понимают меня',
                          'Я не чувствую себя в безопасности',
                          'Я часто понапрасну волнуюсь',
                          'Я чувствую себя неловко, когда вхожу в комнату, где уже сидят люди',
                          'Я чувствую себя скованным',
                          'Я чувствую, что люди говорят обо мне за моей спиной',
                          'Я уверен, что люди почти все принимают легче, чем я',
                          'Мне кажется, что со мной должна случиться какая-нибудь неприятность',
                          'Меня волнует мысль о том, как люди относятся ко мне',
                          'Как жаль, что я не так общителен',
                          'В спорах я высказываюсь только тогда, когда уверен в своей правоте',
                          'Я думаю о том, чего ждут от меня люди',

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
            raise BadOrderUSK

        # словарь для замены слов на числа
        dct_replace_value = {'никогда': 0,
                             'редко': 1,
                             'иногда': 2,
                             'часто': 3,
                             'очень часто': 4}

        valid_values = [0, 1, 2, 3, 4]
        answers_df.replace(dct_replace_value, inplace=True)  # заменяем слова на цифры для подсчетов

        # Проверяем, есть ли значения, отличающиеся от указанных в списке
        mask = ~answers_df.isin(valid_values)

        # Получаем строки с отличающимися значениями
        result_check = answers_df[mask.any(axis=1)]
        if len(result_check) != 0:
            error_row = list(map(lambda x: x + 2, result_check.index))
            error_row = list(map(str, error_row))
            error_message = ';'.join(error_row)
            raise BadValueUSK

        # Проводим подсчет
        base_df['Значение_уровня_самооценки'] = answers_df.apply(calc_value_usk, axis=1)
        base_df['Норма_уровня_самооценки'] = '0-45 баллов'
        base_df['Уровень_самооценки'] = base_df['Значение_уровня_самооценки'].apply(calc_level_usk)

        # Создаем датафрейм для создания части в общий датафрейм
        part_df = pd.DataFrame(columns=['Значение_самооценки_Ковалев','Уровень_самооценки_Ковалев'])
        part_df['Значение_самооценки_Ковалев'] = base_df['Значение_уровня_самооценки']
        part_df['Уровень_самооценки_Ковалев'] = base_df['Уровень_самооценки']

        base_df.sort_values(by='Значение_уровня_самооценки', ascending=False, inplace=True)  # сортируем


        # Среднее Курс
        mean_course_usk_df = pd.pivot_table(base_df, index=['Курс'],
                                            values=['Значение_уровня_самооценки'],
                                            aggfunc=round_mean)
        mean_course_usk_df.reset_index(inplace=True)
        mean_course_usk_df['Уровень_самооценки'] = mean_course_usk_df['Значение_уровня_самооценки'].apply(
            calc_level_usk)  # считаем уровень

        # Количество Курс
        count_course_usk_df = pd.pivot_table(base_df, index=['Курс'],
                                             columns='Уровень_самооценки',
                                             values='Значение_уровня_самооценки',
                                             aggfunc='count', margins=True, margins_name='Итого')
        count_course_usk_df.reset_index(inplace=True)

        if 'Низкий уровень самооценки' in count_course_usk_df.columns:
            count_course_usk_df['% Низкий уровень самооценки от общего'] = round(
                count_course_usk_df['Низкий уровень самооценки'] / count_course_usk_df['Итого'], 2) * 100

        if 'Средний уровень самооценки' in count_course_usk_df.columns:
            count_course_usk_df['% Средний уровень самооценки от общего'] = round(
                count_course_usk_df['Средний уровень самооценки'] /
                count_course_usk_df['Итого'], 2) * 100

        if 'Высокий уровень самооценки' in count_course_usk_df.columns:
            count_course_usk_df['% Высокий уровень самооценки от общего'] = round(
                count_course_usk_df['Высокий уровень самооценки'] /
                count_course_usk_df['Итого'], 2) * 100



        # Средняя Курс и Пол

        mean_course_sex_usk_df = pd.pivot_table(base_df, index=['Курс','Пол'],
                                            values=['Значение_уровня_самооценки'],
                                            aggfunc=round_mean)
        mean_course_sex_usk_df.reset_index(inplace=True)
        mean_course_sex_usk_df['Уровень_самооценки'] = mean_course_sex_usk_df['Значение_уровня_самооценки'].apply(
            calc_level_usk)  # считаем уровень

        # Количество Курс и Пол
        count_course_sex_usk_df = pd.pivot_table(base_df, index=['Курс','Пол'],
                                             columns='Уровень_самооценки',
                                             values='Значение_уровня_самооценки',
                                             aggfunc='count', margins=True, margins_name='Итого')
        count_course_sex_usk_df.reset_index(inplace=True)

        if 'Низкий уровень самооценки' in count_course_sex_usk_df.columns:
            count_course_sex_usk_df['% Низкий уровень самооценки от общего'] = round(
                count_course_sex_usk_df['Низкий уровень самооценки'] / count_course_sex_usk_df['Итого'], 2) * 100

        if 'Средний уровень самооценки' in count_course_sex_usk_df.columns:
            count_course_sex_usk_df['% Средний уровень самооценки от общего'] = round(
                count_course_sex_usk_df['Средний уровень самооценки'] /
                count_course_sex_usk_df['Итого'], 2) * 100

        if 'Высокий уровень самооценки' in count_course_sex_usk_df.columns:
            count_course_sex_usk_df['% Высокий уровень самооценки от общего'] = round(
                count_course_sex_usk_df['Высокий уровень самооценки'] /
                count_course_sex_usk_df['Итого'], 2) * 100

        """
        Обработка групп
        """
        # Средняя Группа
        mean_group_usk_df = pd.pivot_table(base_df, index=['Группа'],
                                            values=['Значение_уровня_самооценки'],
                                            aggfunc=round_mean)
        mean_group_usk_df.reset_index(inplace=True)
        mean_group_usk_df['Уровень_самооценки'] = mean_group_usk_df['Значение_уровня_самооценки'].apply(
            calc_level_usk)  # считаем уровень

        # Количество Группа и Пол
        count_group_usk_df = pd.pivot_table(base_df, index=['Группа'],
                                             columns='Уровень_самооценки',
                                             values='Значение_уровня_самооценки',
                                             aggfunc='count', margins=True, margins_name='Итого')
        count_group_usk_df.reset_index(inplace=True)

        if 'Низкий уровень самооценки' in count_group_usk_df.columns:
            count_group_usk_df['% Низкий уровень самооценки от общего'] = round(
                count_group_usk_df['Низкий уровень самооценки'] / count_group_usk_df['Итого'], 2) * 100

        if 'Средний уровень самооценки' in count_group_usk_df.columns:
            count_group_usk_df['% Средний уровень самооценки от общего'] = round(
                count_group_usk_df['Средний уровень самооценки'] /
                count_group_usk_df['Итого'], 2) * 100

        if 'Высокий уровень самооценки' in count_group_usk_df.columns:
            count_group_usk_df['% Высокий уровень самооценки от общего'] = round(
                count_group_usk_df['Высокий уровень самооценки'] /
                count_group_usk_df['Итого'], 2) * 100



        # Средняя Группа и Пол

        mean_group_sex_usk_df = pd.pivot_table(base_df, index=['Группа','Пол'],
                                            values=['Значение_уровня_самооценки'],
                                            aggfunc=round_mean)
        mean_group_sex_usk_df.reset_index(inplace=True)
        mean_group_sex_usk_df['Уровень_самооценки'] = mean_group_sex_usk_df['Значение_уровня_самооценки'].apply(
            calc_level_usk)  # считаем уровень

        # Количество Группа и Пол
        count_group_sex_usk_df = pd.pivot_table(base_df, index=['Группа','Пол'],
                                             columns='Уровень_самооценки',
                                             values='Значение_уровня_самооценки',
                                             aggfunc='count', margins=True, margins_name='Итого')
        count_group_sex_usk_df.reset_index(inplace=True)

        if 'Низкий уровень самооценки' in count_group_sex_usk_df.columns:
            count_group_sex_usk_df['% Низкий уровень самооценки от общего'] = round(
                count_group_sex_usk_df['Низкий уровень самооценки'] / count_group_sex_usk_df['Итого'], 2) * 100

        if 'Средний уровень самооценки' in count_group_sex_usk_df.columns:
            count_group_sex_usk_df['% Средний уровень самооценки от общего'] = round(
                count_group_sex_usk_df['Средний уровень самооценки'] /
                count_group_sex_usk_df['Итого'], 2) * 100

        if 'Высокий уровень самооценки' in count_group_sex_usk_df.columns:
            count_group_sex_usk_df['% Высокий уровень самооценки от общего'] = round(
                count_group_sex_usk_df['Высокий уровень самооценки'] /
                count_group_sex_usk_df['Итого'], 2) * 100

        out_answer_df = pd.concat([out_answer_df, answers_df], axis=1)

        # формируем словарь
        out_dct = {'Списочный результат': base_df, 'Список для проверки': out_answer_df,
                   'Среднее Группа': mean_group_usk_df, 'Количество Группа': count_group_usk_df,
                   'Среднее Группа Пол': mean_group_sex_usk_df, 'Количество Группа Пол': count_group_sex_usk_df,
                   'Среднее Курс': mean_course_usk_df, 'Количество Курс': count_course_usk_df,
                   'Среднее Курс Пол': mean_course_sex_usk_df, 'Количество Курс Пол': count_course_sex_usk_df,

                   }

        return out_dct, part_df

    except BadOrderUSK:
        messagebox.showerror('Лахеcис',
                             f'При обработке вопросов теста Уровень самооценки Ковалева обнаружены неправильные вопросы. Проверьте названия колонок с вопросами:\n'
                             f'{error_order_message}\n'
                             f'Используйте при создании Яндекс-формы написание вопросов из руководства пользователя программы Лахесис.')
    except BadValueUSK:
        messagebox.showerror('Лахеcис',
                             f'При обработке вопросов теста Уровень самооценки Ковалева обнаружены неправильные варианты ответов. Проверьте ответы на указанных строках:\n'
                             f'{error_message}\n'
                             f'Используйте при создании Яндекс-формы написание вариантов ответа из руководства пользователя программы Лахесис.')

    except BadCountColumnsUSK:
        messagebox.showerror('Лахеcис',
                             f'Проверьте количество колонок с ответами на тест Уровень самооценки Ковалева\n'
                             f'Должно быть 32 колонки с вопросами'
                             )
