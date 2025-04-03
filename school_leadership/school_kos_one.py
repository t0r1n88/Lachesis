"""
Скрипт для обработки «Оценка коммуникативных и организаторских способностей» (КОС) Тест - опросник Б.А. Федоришина
"""
import pandas as pd
from tkinter import messagebox
from lachesis_support_functions import round_mean_two, sort_name_class

class BadOrderKOSOne(Exception):
    """
    Исключение для обработки случая когда колонки не совпадают
    """
    pass


class BadValueKOSOne(Exception):
    """
    Исключение для неправильных значений в вариантах ответов
    """
    pass

class BadCountColumnsKOSOne(Exception):
    """
    Исключение для обработки случая если количество колонок не равно 40
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
        scale_df = pd.pivot_table(df, index=f'Уровень_{scale}_навыков',
                                                  values=f'Значение_{scale}_навыков',
                                                  aggfunc='count')

        scale_df[f'{scale}_навыки % от общего'] = round(
            scale_df[f'Значение_{scale}_навыков'] / scale_df[f'Значение_{scale}_навыков'].sum(),3) * 100
        scale_df.rename(columns={f'Значение_{scale}_навыков':f'Количество_{scale}'},inplace=True)

        # # Создаем суммирующую строку
        scale_df.loc['Итого'] = scale_df.sum()


        base_df = base_df.join(scale_df)

    base_df = base_df.reset_index()
    base_df.rename(columns={'index':'Уровень навыков'},inplace=True)
    return base_df





def calc_value_com_cos_one(row):
    """
    Функция для подсчета значения коммуникативных навыков КОС-1
    :param row: строка с ответами
    :return: число
    """
    value_forward = 0 # счетчик депрессии прямых ответов
    value_reverse = 0 # счетчик депрессии обратных ответов
    lst_forward = [1,5,9,13,17,21,25,29,33,37]  #  подсчет если значение Да
    lst_reverse = [3,7,11,15,19,23,27,31,35,39] # подсчет если значение Нет
    for idx, value in enumerate(row):
        if idx + 1 in lst_forward:
            # print(f'Прямой подсчет {idx +1}') # Для проверки корректности
            if value == 'Да':
                value_forward += 1
        elif idx +1 in lst_reverse:
            if value == 'Нет':
                value_reverse += 1
            # print(f'Обратный подсчет {idx +1}')# Для проверки корректности


    return (value_forward + value_reverse) * 0.05

def calc_est_com_cos_one(value):
    """
    Функция для подсчета оценки коммуникативных способностей КОС-1
    :param value:
    :return:
    """
    if 0.10 <= value <= 0.45:
        return 1
    elif 0.46 <= value <= 0.55:
        return 2
    elif 0.56 <= value <= 0.65:
        return 3
    elif 0.66 <= value <= 0.75:
        return 4
    elif 0.76 <= value <= 1:
        return 5



def calc_level_com_cos_one(value):
    """
    Функция для подсчета уровня коммуникативных способностей КОС-1
    :param value:
    :return:
    """
    if value == 1:
        return 'Низкий'
    elif value == 2:
        return 'Ниже среднего'
    elif value == 3:
        return 'Средний'
    elif value == 4:
        return 'Высокий'
    elif value == 5:
        return 'Очень высокий'


def calc_value_org_cos_one(row):
    """
    Функция для подсчета значения коммуникативных навыков КОС-1
    :param row: строка с ответами
    :return: число
    """
    value_forward = 0 # счетчик депрессии прямых ответов
    value_reverse = 0 # счетчик депрессии обратных ответов
    lst_forward = [2,6,10,14,18,22,26,30,34,38]  #  подсчет если значение Да
    lst_reverse = [4,8,12,16,20,24,28,32,36,40] # подсчет если значение Нет
    for idx, value in enumerate(row):
        if idx + 1 in lst_forward:
            # print(f'Прямой подсчет {idx +1}') # Для проверки корректности
            if value == 'Да':
                value_forward += 1
        elif idx +1 in lst_reverse:
            if value == 'Нет':
                value_reverse += 1
            # print(f'Обратный подсчет {idx +1}')# Для проверки корректности


    return (value_forward + value_reverse) * 0.05


def calc_est_org_cos_one(value):
    """
    Функция для подсчета оценки организационных способностей КОС-1
    :param value:
    :return:
    """
    if 0.20 <= value <= 0.55:
        return 1
    elif 0.56 <= value <= 0.65:
        return 2
    elif 0.66 <= value <= 0.70:
        return 3
    elif 0.71 <= value <= 0.80:
        return 4
    elif 0.81 <= value <= 1:
        return 5



def calc_level_org_cos_one(value):
    """
    Функция для подсчета уровня организационных способностей КОС-1
    :param value:
    :return:
    """
    if value == 1:
        return 'Низкий'
    elif value == 2:
        return 'Ниже среднего'
    elif value == 3:
        return 'Средний'
    elif value == 4:
        return 'Высокий'
    elif value == 5:
        return 'Очень высокий'






def processing_kos(base_df: pd.DataFrame, answers_df: pd.DataFrame,):
    """
    Функция для обработки
    :param base_df: часть датафрейма с описательными колонками
    :param answers_df: часть датафрейма с ответами
    """
    try:
        out_answer_df = base_df.copy()  # делаем копию для последующего соединения с сырыми ответами
        if len(answers_df.columns) != 40:  # проверяем количество колонок с вопросами
            raise BadCountColumnsKOSOne

        # Словарь с проверочными данными
        lst_check_cols = ['Много ли у вас друзей, с которыми вы постоянно общаетесь?',
                          'Часто ли вам удаётся склонить большинство своих друзей к принятию ими вашего мнения?',
                          'Долго ли вас беспокоит чувство обиды, причинённое вам кем-то из ваших друзей?',
                          'Всегда ли вам трудно ориентироваться в создавшейся критической ситуации?',
                          'Есть ли у вас стремление к установлению новых знакомств с разными людьми?',
                          'Нравится ли вам заниматься общественной работой?',
                          'Верно ли, что вам приятнее проще проводить время с книгами, за компьютером, чем с людьми?',
                          'Если возникли какие – либо помехи в осуществлении ваших планов, легко ли вы отступаете от них?',
                          'Легко ли вы устанавливаете контакты с людьми, которые значительно старше вас?',
                          'Любите ли вы придумывать и организовывать со своими друзьями различные игры и развлечения?',
                          'Трудно ли вы включаетесь в новую для вас компанию?',
                          'Часто ли вы откладываете на другие дни те дела, которые нужно было бы выполнить сегодня?',
                          'Легко ли вам удается устанавливать контакты с незнакомыми людьми?',
                          'Стремитесь ли вы добиваться, чтобы ваши друзья действовали в соответствии с вашим мнением?',
                          'Трудно ли вы осваиваетесь в новом коллективе?',
                          'Верно ли, что у вас не бывает конфликтов с друзьями из-за невыполнения ими своих обязанностей, обязательств?',
                          'Стремитесь ли вы при удобном случае познакомиться и побеседовать с новым человеком?',
                          'Часто ли в решении важных вопросов вы принимаете инициативу на себя?',
                          'Раздражают ли вас окружающие люди, и хочется ли вам побыть одному?',
                          'Правда ли, что вы обычно плохо ориентируетесь в незнакомой обстановке?',
                          'Нравится ли вам постоянно находиться среди людей?',
                          'Возникает ли у вас раздражение, если вам не удается закончить начатое дело?',
                          'Испытываете ли вы затруднения, неудобства или стеснение, если приходится проявлять инициативу, чтобы познакомиться с новым человеком?',
                          'Правда ли, что вы утомляетесь от частого общения с друзьями?',
                          'Любите ли вы участвовать в коллективных играх?',
                          'Часто ли вы проявляете инициативу при решении вопросов, затрагивающих интересы ваших друзей?',
                          'Правда ли, что вы чувствуете себя неуверенно среди мало знакомой компании?',
                          'Верно ли, что вы редко стремитесь к доказательству своей правоты?',
                          'Полагаете ли вы, что вам не доставляет особого труда внести оживление в малознакомую вам компанию?',
                          'Принимаете ли вы участие в общественной работе в школе, техникуме?',
                          'Стремитесь ли вы ограничить круг своих знакомых небольшим количеством человек?',
                          'Верно ли, что вы не стремитесь отстаивать своё мнение, если оно не сразу было принято вашими товарищами?',
                          'Чувствуете ли вы себя непринуждённо, попав в незнакомую компанию?',
                          'Охотно ли вы приступаете к организации различных мероприятий для своих знакомых и друзей?',
                          'Правда ли, что не чувствуете себя достаточно уверенным и спокойным, когда приходится говорить что-либо большой группе людей?',
                          'Всегда ли вы опаздываете на деловые свидания и встречи?',
                          'Верно ли, что у вас много друзей?',
                          'Часто ли, вы оказываетесь в центре внимания своих друзей?',
                          'Часто ли вы смущаетесь, чувствуете неловкость при общении с малознакомыми людьми?',
                          'Правда ли, что вы не очень уверенно чувствуете себя в окружении большой группы своих друзей?',
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
            raise BadOrderKOSOne

        valid_values = ['Да','Нет']

        # Проверяем, есть ли значения, отличающиеся от указанных в списке
        mask = ~answers_df.isin(valid_values)

        # Получаем строки с отличающимися значениями
        result_check = answers_df[mask.any(axis=1)]
        if len(result_check) != 0:
            error_row = list(map(lambda x: x + 2, result_check.index))
            error_row = list(map(str, error_row))
            error_message = ';'.join(error_row)
            raise BadValueKOSOne

        # Коммуникативные новыки
        base_df['Значение_ком_навыков'] = answers_df.apply(calc_value_com_cos_one, axis=1)
        base_df['Норма_ком_навыков'] = '0,45-0,75'
        base_df['Оценка_ком_навыков'] = base_df['Значение_ком_навыков'].apply(calc_est_com_cos_one)
        base_df['Уровень_ком_навыков'] = base_df['Оценка_ком_навыков'].apply(calc_level_com_cos_one)

        # Организационные навыки
        base_df['Значение_орг_навыков'] = answers_df.apply(calc_value_org_cos_one, axis=1)
        base_df['Норма_орг_навыков'] = '0,56-0,80'
        base_df['Оценка_орг_навыков'] = base_df['Значение_орг_навыков'].apply(calc_est_org_cos_one)
        base_df['Уровень_орг_навыков'] = base_df['Оценка_орг_навыков'].apply(calc_level_org_cos_one)

        # Создаем датафрейм для создания части в общий датафрейм
        part_df = pd.DataFrame(columns=['Значение_ком_навыков_КОС_один','Уровень_ком_навыков_КОС_один','Значение_орг_навыков_КОС_один','Уровень_орг_навыков_КОС_один'])
        part_df['Значение_ком_навыков_КОС_один'] = base_df['Значение_ком_навыков']
        part_df['Уровень_ком_навыков_КОС_один'] = base_df['Уровень_ком_навыков']
        part_df['Значение_орг_навыков_КОС_один'] = base_df['Значение_орг_навыков']
        part_df['Уровень_орг_навыков_КОС_один'] = base_df['Уровень_орг_навыков']


        base_df.sort_values(by='Значение_ком_навыков', ascending=False, inplace=True)  # сортируем

        """
        Делаем свод по курсам
        """
        # Коммуникативные навыки
        # Среднее Номер_класса
        mean_course_com_cos_one_df = pd.pivot_table(base_df, index=['Номер_класса'],
                                            values=['Значение_ком_навыков'],
                                            aggfunc=round_mean_two)
        mean_course_com_cos_one_df.reset_index(inplace=True)
        mean_course_com_cos_one_df['Уровень_ком_навыков'] = mean_course_com_cos_one_df['Значение_ком_навыков'].apply(
            calc_level_com_cos_one)  # считаем уровень

        # Количество Номер_класса
        count_course_com_cos_one_df = pd.pivot_table(base_df, index=['Номер_класса'],
                                             columns='Уровень_ком_навыков',
                                             values='Значение_ком_навыков',
                                             aggfunc='count', margins=True, margins_name='Итого')
        count_course_com_cos_one_df.reset_index(inplace=True)
        count_course_com_cos_one_df = count_course_com_cos_one_df.reindex(
            columns=['Номер_класса', 'Низкий', 'Ниже среднего', 'Средний',
                     'Высокий', 'Очень высокий', 'Итого'])

        count_course_com_cos_one_df['% Низкий уровень ком.навыков от общего'] = round(
            count_course_com_cos_one_df['Низкий'] / count_course_com_cos_one_df['Итого'], 2) * 100

        count_course_com_cos_one_df['% Ниже среднего уровень ком.навыков от общего'] = round(
            count_course_com_cos_one_df['Ниже среднего'] / count_course_com_cos_one_df['Итого'], 2) * 100

        count_course_com_cos_one_df['% Средний уровень ком.навыков от общего'] = round(
            count_course_com_cos_one_df['Средний'] /
            count_course_com_cos_one_df['Итого'], 2) * 100

        count_course_com_cos_one_df['% Высокий уровень ком.навыков от общего'] = round(
            count_course_com_cos_one_df['Высокий'] /
            count_course_com_cos_one_df['Итого'], 2) * 100
        count_course_com_cos_one_df['% Очень высокий ком.навыков от общего'] = round(
            count_course_com_cos_one_df['Очень высокий'] /
            count_course_com_cos_one_df['Итого'], 2) * 100


        # Средняя Номер_класса и Пол

        mean_course_sex_com_cos_one_df = pd.pivot_table(base_df, index=['Номер_класса','Пол'],
                                            values=['Значение_ком_навыков'],
                                            aggfunc=round_mean_two)
        mean_course_sex_com_cos_one_df.reset_index(inplace=True)
        mean_course_sex_com_cos_one_df['Уровень_ком_навыков'] = mean_course_sex_com_cos_one_df['Значение_ком_навыков'].apply(
            calc_level_com_cos_one)  # считаем уровень

        # Количество Номер_класса и Пол
        count_course_sex_com_cos_one_df = pd.pivot_table(base_df, index=['Номер_класса','Пол'],
                                             columns='Уровень_ком_навыков',
                                             values='Значение_ком_навыков',
                                             aggfunc='count', margins=True, margins_name='Итого')
        count_course_sex_com_cos_one_df.reset_index(inplace=True)
        count_course_sex_com_cos_one_df = count_course_sex_com_cos_one_df.reindex(
            columns=['Номер_класса','Пол', 'Низкий', 'Ниже среднего', 'Средний',
                     'Высокий', 'Очень высокий', 'Итого'])

        count_course_sex_com_cos_one_df['% Низкий уровень ком.навыков от общего'] = round(
            count_course_sex_com_cos_one_df['Низкий'] / count_course_sex_com_cos_one_df['Итого'], 2) * 100

        count_course_sex_com_cos_one_df['% Ниже среднего уровень ком.навыков от общего'] = round(
            count_course_sex_com_cos_one_df['Ниже среднего'] / count_course_sex_com_cos_one_df['Итого'], 2) * 100

        count_course_sex_com_cos_one_df['% Средний уровень ком.навыков от общего'] = round(
            count_course_sex_com_cos_one_df['Средний'] /
            count_course_sex_com_cos_one_df['Итого'], 2) * 100

        count_course_sex_com_cos_one_df['% Высокий уровень ком.навыков от общего'] = round(
            count_course_sex_com_cos_one_df['Высокий'] /
            count_course_sex_com_cos_one_df['Итого'], 2) * 100
        count_course_sex_com_cos_one_df['% Очень высокий ком.навыков от общего'] = round(
            count_course_sex_com_cos_one_df['Очень высокий'] /
            count_course_sex_com_cos_one_df['Итого'], 2) * 100


        # Организационные навыки
        # Среднее Номер_класса
        mean_course_org_cos_one_df = pd.pivot_table(base_df, index=['Номер_класса'],
                                                    values=['Значение_орг_навыков'],
                                                    aggfunc=round_mean_two)
        mean_course_org_cos_one_df.reset_index(inplace=True)
        mean_course_org_cos_one_df['Уровень_орг_навыков'] = mean_course_org_cos_one_df['Значение_орг_навыков'].apply(
            calc_level_org_cos_one)  # считаем уровень

        # Количество Номер_класса
        count_course_org_cos_one_df = pd.pivot_table(base_df, index=['Номер_класса'],
                                                     columns='Уровень_орг_навыков',
                                                     values='Значение_орг_навыков',
                                                     aggfunc='count', margins=True, margins_name='Итого')
        count_course_org_cos_one_df.reset_index(inplace=True)
        count_course_org_cos_one_df = count_course_org_cos_one_df.reindex(
            columns=['Номер_класса', 'Низкий', 'Ниже среднего', 'Средний',
                     'Высокий', 'Очень высокий', 'Итого'])

        count_course_org_cos_one_df['% Низкий уровень орг.навыков от общего'] = round(
            count_course_org_cos_one_df['Низкий'] / count_course_org_cos_one_df['Итого'], 2) * 100

        count_course_org_cos_one_df['% Ниже среднего уровень орг.навыков от общего'] = round(
            count_course_org_cos_one_df['Ниже среднего'] / count_course_org_cos_one_df['Итого'], 2) * 100

        count_course_org_cos_one_df['% Средний уровень орг.навыков от общего'] = round(
            count_course_org_cos_one_df['Средний'] /
            count_course_org_cos_one_df['Итого'], 2) * 100

        count_course_org_cos_one_df['% Высокий уровень орг.навыков от общего'] = round(
            count_course_org_cos_one_df['Высокий'] /
            count_course_org_cos_one_df['Итого'], 2) * 100
        count_course_org_cos_one_df['% Очень высокий орг.навыков от общего'] = round(
            count_course_org_cos_one_df['Очень высокий'] /
            count_course_org_cos_one_df['Итого'], 2) * 100

        # Средняя Номер_класса и Пол

        mean_course_sex_org_cos_one_df = pd.pivot_table(base_df, index=['Номер_класса', 'Пол'],
                                                        values=['Значение_орг_навыков'],
                                                        aggfunc=round_mean_two)
        mean_course_sex_org_cos_one_df.reset_index(inplace=True)
        mean_course_sex_org_cos_one_df['Уровень_орг_навыков'] = mean_course_sex_org_cos_one_df[
            'Значение_орг_навыков'].apply(
            calc_level_org_cos_one)  # считаем уровень

        # Количество Номер_класса и Пол
        count_course_sex_org_cos_one_df = pd.pivot_table(base_df, index=['Номер_класса', 'Пол'],
                                                         columns='Уровень_орг_навыков',
                                                         values='Значение_орг_навыков',
                                                         aggfunc='count', margins=True, margins_name='Итого')
        count_course_sex_org_cos_one_df.reset_index(inplace=True)
        count_course_sex_org_cos_one_df = count_course_sex_org_cos_one_df.reindex(
            columns=['Номер_класса', 'Пол', 'Низкий', 'Ниже среднего', 'Средний',
                     'Высокий', 'Очень высокий', 'Итого'])

        count_course_sex_org_cos_one_df['% Низкий уровень орг.навыков от общего'] = round(
            count_course_sex_org_cos_one_df['Низкий'] / count_course_sex_org_cos_one_df['Итого'], 2) * 100

        count_course_sex_org_cos_one_df['% Ниже среднего уровень орг.навыков от общего'] = round(
            count_course_sex_org_cos_one_df['Ниже среднего'] / count_course_sex_org_cos_one_df['Итого'], 2) * 100

        count_course_sex_org_cos_one_df['% Средний уровень орг.навыков от общего'] = round(
            count_course_sex_org_cos_one_df['Средний'] /
            count_course_sex_org_cos_one_df['Итого'], 2) * 100

        count_course_sex_org_cos_one_df['% Высокий уровень орг.навыков от общего'] = round(
            count_course_sex_org_cos_one_df['Высокий'] /
            count_course_sex_org_cos_one_df['Итого'], 2) * 100
        count_course_sex_org_cos_one_df['% Очень высокий орг.навыков от общего'] = round(
            count_course_sex_org_cos_one_df['Очень высокий'] /
            count_course_sex_org_cos_one_df['Итого'], 2) * 100


        """
        Своды по группам
        """
        # Коммуникативные навыки
        # Среднее Класс
        mean_group_com_cos_one_df = pd.pivot_table(base_df, index=['Класс'],
                                            values=['Значение_ком_навыков'],
                                            aggfunc=round_mean_two)
        mean_group_com_cos_one_df.reset_index(inplace=True)
        mean_group_com_cos_one_df['Уровень_ком_навыков'] = mean_group_com_cos_one_df['Значение_ком_навыков'].apply(
            calc_level_com_cos_one)  # считаем уровень
        mean_group_com_cos_one_df.sort_values(by='Класс', key=lambda x: x.map(sort_name_class), inplace=True)  # сортируем

        # Количество Класс
        count_group_com_cos_one_df = pd.pivot_table(base_df, index=['Класс'],
                                             columns='Уровень_ком_навыков',
                                             values='Значение_ком_навыков',
                                             aggfunc='count', margins=True, margins_name='Итого')
        count_group_com_cos_one_df.reset_index(inplace=True)
        count_group_com_cos_one_df = count_group_com_cos_one_df.reindex(
            columns=['Класс', 'Низкий', 'Ниже среднего', 'Средний',
                     'Высокий', 'Очень высокий', 'Итого'])

        count_group_com_cos_one_df['% Низкий уровень ком.навыков от общего'] = round(
            count_group_com_cos_one_df['Низкий'] / count_group_com_cos_one_df['Итого'], 2) * 100

        count_group_com_cos_one_df['% Ниже среднего уровень ком.навыков от общего'] = round(
            count_group_com_cos_one_df['Ниже среднего'] / count_group_com_cos_one_df['Итого'], 2) * 100

        count_group_com_cos_one_df['% Средний уровень ком.навыков от общего'] = round(
            count_group_com_cos_one_df['Средний'] /
            count_group_com_cos_one_df['Итого'], 2) * 100

        count_group_com_cos_one_df['% Высокий уровень ком.навыков от общего'] = round(
            count_group_com_cos_one_df['Высокий'] /
            count_group_com_cos_one_df['Итого'], 2) * 100
        count_group_com_cos_one_df['% Очень высокий ком.навыков от общего'] = round(
            count_group_com_cos_one_df['Очень высокий'] /
            count_group_com_cos_one_df['Итого'], 2) * 100

        part_svod_df = count_group_com_cos_one_df.iloc[:-1:]
        part_svod_df.sort_values(by='Класс', key=lambda x: x.map(sort_name_class), inplace=True)  # сортируем
        itog_svod_df = count_group_com_cos_one_df.iloc[-1:]
        count_group_com_cos_one_df = pd.concat([part_svod_df, itog_svod_df])


        # Средняя Класс и Пол

        mean_group_sex_com_cos_one_df = pd.pivot_table(base_df, index=['Класс','Пол'],
                                            values=['Значение_ком_навыков'],
                                            aggfunc=round_mean_two)
        mean_group_sex_com_cos_one_df.reset_index(inplace=True)
        mean_group_sex_com_cos_one_df['Уровень_ком_навыков'] = mean_group_sex_com_cos_one_df['Значение_ком_навыков'].apply(
            calc_level_com_cos_one)  # считаем уровень
        mean_group_sex_com_cos_one_df.sort_values(by='Класс', key=lambda x: x.map(sort_name_class), inplace=True)  # сортируем

        # Количество Класс и Пол
        count_group_sex_com_cos_one_df = pd.pivot_table(base_df, index=['Класс','Пол'],
                                             columns='Уровень_ком_навыков',
                                             values='Значение_ком_навыков',
                                             aggfunc='count', margins=True, margins_name='Итого')
        count_group_sex_com_cos_one_df.reset_index(inplace=True)
        count_group_sex_com_cos_one_df = count_group_sex_com_cos_one_df.reindex(
            columns=['Класс','Пол', 'Низкий', 'Ниже среднего', 'Средний',
                     'Высокий', 'Очень высокий', 'Итого'])

        count_group_sex_com_cos_one_df['% Низкий уровень ком.навыков от общего'] = round(
            count_group_sex_com_cos_one_df['Низкий'] / count_group_sex_com_cos_one_df['Итого'], 2) * 100

        count_group_sex_com_cos_one_df['% Ниже среднего уровень ком.навыков от общего'] = round(
            count_group_sex_com_cos_one_df['Ниже среднего'] / count_group_sex_com_cos_one_df['Итого'], 2) * 100

        count_group_sex_com_cos_one_df['% Средний уровень ком.навыков от общего'] = round(
            count_group_sex_com_cos_one_df['Средний'] /
            count_group_sex_com_cos_one_df['Итого'], 2) * 100

        count_group_sex_com_cos_one_df['% Высокий уровень ком.навыков от общего'] = round(
            count_group_sex_com_cos_one_df['Высокий'] /
            count_group_sex_com_cos_one_df['Итого'], 2) * 100
        count_group_sex_com_cos_one_df['% Очень высокий ком.навыков от общего'] = round(
            count_group_sex_com_cos_one_df['Очень высокий'] /
            count_group_sex_com_cos_one_df['Итого'], 2) * 100

        part_svod_df = count_group_sex_com_cos_one_df.iloc[:-1:]
        part_svod_df.sort_values(by='Класс', key=lambda x: x.map(sort_name_class), inplace=True)  # сортируем
        itog_svod_df = count_group_sex_com_cos_one_df.iloc[-1:]
        count_group_sex_com_cos_one_df = pd.concat([part_svod_df, itog_svod_df])


        # Организационные навыки
        # Среднее Класс
        mean_group_org_cos_one_df = pd.pivot_table(base_df, index=['Класс'],
                                                    values=['Значение_орг_навыков'],
                                                    aggfunc=round_mean_two)
        mean_group_org_cos_one_df.reset_index(inplace=True)
        mean_group_org_cos_one_df['Уровень_орг_навыков'] = mean_group_org_cos_one_df['Значение_орг_навыков'].apply(
            calc_level_org_cos_one)  # считаем уровень

        mean_group_org_cos_one_df.sort_values(by='Класс', key=lambda x: x.map(sort_name_class), inplace=True)  # сортируем

        # Количество Класс
        count_group_org_cos_one_df = pd.pivot_table(base_df, index=['Класс'],
                                                     columns='Уровень_орг_навыков',
                                                     values='Значение_орг_навыков',
                                                     aggfunc='count', margins=True, margins_name='Итого')
        count_group_org_cos_one_df.reset_index(inplace=True)
        count_group_org_cos_one_df = count_group_org_cos_one_df.reindex(
            columns=['Класс', 'Низкий', 'Ниже среднего', 'Средний',
                     'Высокий', 'Очень высокий', 'Итого'])

        count_group_org_cos_one_df['% Низкий уровень орг.навыков от общего'] = round(
            count_group_org_cos_one_df['Низкий'] / count_group_org_cos_one_df['Итого'], 2) * 100

        count_group_org_cos_one_df['% Ниже среднего уровень орг.навыков от общего'] = round(
            count_group_org_cos_one_df['Ниже среднего'] / count_group_org_cos_one_df['Итого'], 2) * 100

        count_group_org_cos_one_df['% Средний уровень орг.навыков от общего'] = round(
            count_group_org_cos_one_df['Средний'] /
            count_group_org_cos_one_df['Итого'], 2) * 100

        count_group_org_cos_one_df['% Высокий уровень орг.навыков от общего'] = round(
            count_group_org_cos_one_df['Высокий'] /
            count_group_org_cos_one_df['Итого'], 2) * 100
        count_group_org_cos_one_df['% Очень высокий орг.навыков от общего'] = round(
            count_group_org_cos_one_df['Очень высокий'] /
            count_group_org_cos_one_df['Итого'], 2) * 100

        # Средняя Класс и Пол

        mean_group_sex_org_cos_one_df = pd.pivot_table(base_df, index=['Класс', 'Пол'],
                                                        values=['Значение_орг_навыков'],
                                                        aggfunc=round_mean_two)
        mean_group_sex_org_cos_one_df.reset_index(inplace=True)
        mean_group_sex_org_cos_one_df['Уровень_орг_навыков'] = mean_group_sex_org_cos_one_df[
            'Значение_орг_навыков'].apply(
            calc_level_org_cos_one)  # считаем уровень
        mean_group_sex_org_cos_one_df.sort_values(by='Класс', key=lambda x: x.map(sort_name_class), inplace=True)  # сортируем

        # Количество Класс и Пол
        count_group_sex_org_cos_one_df = pd.pivot_table(base_df, index=['Класс', 'Пол'],
                                                         columns='Уровень_орг_навыков',
                                                         values='Значение_орг_навыков',
                                                         aggfunc='count', margins=True, margins_name='Итого')
        count_group_sex_org_cos_one_df.reset_index(inplace=True)
        count_group_sex_org_cos_one_df = count_group_sex_org_cos_one_df.reindex(
            columns=['Класс', 'Пол', 'Низкий', 'Ниже среднего', 'Средний',
                     'Высокий', 'Очень высокий', 'Итого'])

        count_group_sex_org_cos_one_df['% Низкий уровень орг.навыков от общего'] = round(
            count_group_sex_org_cos_one_df['Низкий'] / count_group_sex_org_cos_one_df['Итого'], 2) * 100

        count_group_sex_org_cos_one_df['% Ниже среднего уровень орг.навыков от общего'] = round(
            count_group_sex_org_cos_one_df['Ниже среднего'] / count_group_sex_org_cos_one_df['Итого'], 2) * 100

        count_group_sex_org_cos_one_df['% Средний уровень орг.навыков от общего'] = round(
            count_group_sex_org_cos_one_df['Средний'] /
            count_group_sex_org_cos_one_df['Итого'], 2) * 100

        count_group_sex_org_cos_one_df['% Высокий уровень орг.навыков от общего'] = round(
            count_group_sex_org_cos_one_df['Высокий'] /
            count_group_sex_org_cos_one_df['Итого'], 2) * 100
        count_group_sex_org_cos_one_df['% Очень высокий орг.навыков от общего'] = round(
            count_group_sex_org_cos_one_df['Очень высокий'] /
            count_group_sex_org_cos_one_df['Итого'], 2) * 100

        part_svod_df = count_group_sex_org_cos_one_df.iloc[:-1:]
        part_svod_df.sort_values(by='Класс', key=lambda x: x.map(sort_name_class), inplace=True)  # сортируем
        itog_svod_df = count_group_sex_org_cos_one_df.iloc[-1:]
        count_group_sex_org_cos_one_df = pd.concat([part_svod_df, itog_svod_df])



        out_answer_df = pd.concat([out_answer_df, answers_df], axis=1)

        # Общий свод сколько склонностей всего в процентном соотношении
        svod_all_df = count_all_scale(base_df, ['ком', 'орг'],
                                      ['Низкий',
                                       'Ниже среднего',
                                       'Средний',
                                       'Высокий',
                                       'Очень высокий',
                                        'Итого'])




        # формируем словарь
        out_dct = {'Списочный результат': base_df, 'Список для проверки': out_answer_df,
                   'Общий свод': svod_all_df,
                   'Среднее Класс Ком': mean_group_com_cos_one_df, 'Количество Класс Ком': count_group_com_cos_one_df,
                   'Среднее Класс Орг': mean_group_org_cos_one_df, 'Количество Класс Орг': count_group_org_cos_one_df,
                   'Среднее Класс Пол Ком': mean_group_sex_com_cos_one_df, 'Количество Класс Пол Ком': count_group_sex_com_cos_one_df,
                   'Среднее Класс Пол Орг': mean_group_sex_org_cos_one_df, 'Количество Класс Пол Орг': count_group_sex_org_cos_one_df,
                   'Среднее Номер_класса Ком': mean_course_com_cos_one_df, 'Количество Номер_класса Ком': count_course_com_cos_one_df,
                   'Среднее Номер_класса Орг': mean_course_org_cos_one_df, 'Количество Номер_класса Орг': count_course_org_cos_one_df,
                   'Среднее Номер_класса Пол Ком': mean_course_sex_com_cos_one_df, 'Количество Номер_класса Пол Ком': count_course_sex_com_cos_one_df,
                   'Среднее Номер_класса Пол Орг': mean_course_sex_org_cos_one_df, 'Количество Номер_класса Пол Орг': count_course_sex_org_cos_one_df

                   }
        return out_dct, part_df





    except BadOrderKOSOne:
        messagebox.showerror('Лахеcис',
                             f'При обработке вопросов теста Оценка коммуникативных и организаторских способностей КОС-1 обнаружены неправильные вопросы. Проверьте названия колонок с вопросами:\n'
                             f'{error_order_message}\n'
                             f'Используйте при создании Яндекс-формы написание вопросов из руководства пользователя программы Лахесис.')
    except BadValueKOSOne:
        messagebox.showerror('Лахеcис',
                             f'При обработке вопросов теста Оценка коммуникативных и организаторских способностей КОС-1 обнаружены неправильные варианты ответов. Проверьте ответы на указанных строках:\n'
                             f'{error_message}\n'
                             f'Используйте при создании Яндекс-формы написание вариантов ответа из руководства пользователя программы Лахесис.')

    except BadCountColumnsKOSOne:
        messagebox.showerror('Лахеcис',
                             f'Проверьте количество колонок с ответами на тест Оценка коммуникативных и организаторских способностей КОС-1\n'
                             f'Должно быть 40 колонок с вопросами'
                             )