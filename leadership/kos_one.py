"""
Скрипт для обработки «Оценка коммуникативных и организаторских способностей» (КОС) Тест - опросник Б.А. Федоришина
"""
import pandas as pd
from tkinter import messagebox
from lachesis_support_functions import round_mean

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