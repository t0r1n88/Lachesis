"""
Скрипт для обработки результатов теста Профессиональные установки подростков Андреева
"""

import pandas as pd
from tkinter import messagebox
from lachesis_support_functions import convert_to_int,round_mean,sort_name_class

class BadOrderPUP(Exception):
    """
    Исключение для обработки случая когда колонки не совпадают
    """
    pass

class BadValuePUP(Exception):
    """
    Исключение для неправильных значений в вариантах ответов
    """
    pass


class BadCountColumnsPUP(Exception):
    """
    Исключение для обработки случая если количество колонок не равно 24
    """
    pass


def processing_result_pup(row):
    """
Функция для вычисления итогового балла
"""

    # Создаем словарь для хранения данных
    dct_type = {'Уверенность в будущем выборе': 0, 'Нерешительность в выборе профессии': 0}
    lst_confidence = [1, 2, 4, 5, 7, 8, 9, 12, 13, 15, 17, 18, 19, 20, 22, 23]
    lst_indecision = [0, 3, 6, 10, 11, 14, 16, 21]
    for idx, value in enumerate(row):
        if idx in lst_confidence:
            dct_type['Уверенность в будущем выборе'] += value
        else:
            dct_type['Нерешительность в выборе профессии'] += value

    begin_str = (f'\nУверенность в будущем выборе: {dct_type["Уверенность в будущем выборе"]}\n'
                 f'Нерешительность в выборе профессии: {dct_type["Нерешительность в выборе профессии"]}')
    return begin_str






def calc_value_confidence(row):
    """
    Функция для подсчета уровня уверенности
    :param row: строка с ответами респондента
    :return:
    """
    value_confidence = 0 # счетчик уверенности
    lst_confidence = [1,2,4,5,7,8,9,12,13,15,17,18,19,20,22,23]


    for idx,value in enumerate(row):
        if idx in lst_confidence:
            value_confidence += value

    return value_confidence


def calc_level_confidence(value):
    """
    Функция для вычисления уровня уверенности
    :param value: числовое значение
    :return: строка с уровнем
    """
    if 0 <= value <= 53:
        return 'низкий'
    elif 54 <= value <= 66:
        return 'средний'
    elif 67 <= value:
        return 'высокий'


def calc_value_indecision(row):
    """
    Функция для подсчета уровня неуверенности
    :param row: строка с ответами респондента
    :return:
    """
    value_indecision = 0 # счетчик уверенности
    lst_indecision = [0,3,6,10,11,14,16,21]

    for idx,value in enumerate(row):
        if idx in lst_indecision:
            value_indecision += value

    return value_indecision


def calc_level_indecision(value):
    """
    Функция для вычисления уровня неуверенности
    :param value: числовое значение
    :return: строка с уровнем
    """
    if 0 <= value <= 12:
        return 'низкий'
    elif 13 <= value <= 19:
        return 'средний'
    elif 20 <= value:
        return 'высокий'



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
        scale_df = pd.pivot_table(df, index=f'Уровень_{scale}',
                                                  values=f'Значение_{scale}',
                                                  aggfunc='count')

        scale_df[f'{scale}% от общего'] = round(
            scale_df[f'Значение_{scale}'] / scale_df[f'Значение_{scale}'].sum(),3) * 100
        scale_df.rename(columns={f'Значение_{scale}':f'Количество_{scale}'},inplace=True)

        # # Создаем суммирующую строку
        scale_df.loc['Итого'] = scale_df.sum()


        base_df = base_df.join(scale_df)

    base_df = base_df.reset_index()
    base_df.rename(columns={'index':'Уровень'},inplace=True)
    return base_df


def calc_mean(df:pd.DataFrame,type_calc:str,lst_cat:list,val_cat):
    """
    Функция для создания сводных датафреймов

    :param df: датафрейм с данными
    :param type_calc:тип обработки Класс или Номер_класса
    :param lst_cat:список колонок по которым будет формироваться свод
    :param val_cat:значение по которому будет формиваться свод
    :return:датафрейм
    """
    if type_calc == 'Класс':
        calc_mean_df = pd.pivot_table(df, index=lst_cat,
                                           values=[val_cat],
                                           aggfunc=round_mean)
        calc_mean_df.reset_index(inplace=True)
        calc_mean_df.sort_values(by='Класс', key=lambda x: x.map(sort_name_class), inplace=True)  # сортируем
        return calc_mean_df
    else:
        calc_mean_df = pd.pivot_table(df, index=lst_cat,
                                           values=val_cat,
                                           aggfunc=round_mean)
        calc_mean_df.reset_index(inplace=True)
        return calc_mean_df



def calc_count(df:pd.DataFrame,type_calc:str,lst_cat:list,val_cat,col_cat,lst_cols:list):
    """
    Функция для создания сводных датафреймов

    :param df: датафрейм с данными
    :param type_calc:тип обработки Класс или Номер_класса
    :param lst_cat:список колонок по которым будет формироваться свод
    :param val_cat:значение по которому будет формиваться свод
    :param col_cat: колонка по которой будет формироваться свод
    :param lst_cols:список колонок для правильного порядка сводной таблицы
    :return:датафрейм
    """
    if type_calc == 'Класс':
        count_df = pd.pivot_table(df, index=lst_cat,
                                                 columns=col_cat,
                                                 values=val_cat,
                                                 aggfunc='count', margins=True, margins_name='Итого')

        count_df.reset_index(inplace=True)
        count_df = count_df.reindex(columns=lst_cols)

        count_df['% низкий от общего'] = round(
            count_df['низкий'] / count_df['Итого'], 2) * 100

        count_df['% средний от общего'] = round(
            count_df['средний'] / count_df['Итого'], 2) * 100

        count_df['% высокий от общего'] = round(
            count_df['высокий'] / count_df['Итого'], 2) * 100

        part_svod_df = count_df.iloc[:-1:]
        part_svod_df.sort_values(by='Класс', key=lambda x: x.map(sort_name_class), inplace=True)  # сортируем
        itog_svod_df = count_df.iloc[-1:]
        count_df = pd.concat([part_svod_df, itog_svod_df])

        return count_df
    else:
        count_df = pd.pivot_table(df, index=lst_cat,
                                  columns=col_cat,
                                  values=val_cat,
                                  aggfunc='count', margins=True, margins_name='Итого')

        count_df.reset_index(inplace=True)
        count_df = count_df.reindex(columns=lst_cols)

        count_df['% низкий от общего'] = round(
            count_df['низкий'] / count_df['Итого'], 2) * 100

        count_df['% средний от общего'] = round(
            count_df['средний'] / count_df['Итого'], 2) * 100

        count_df['% высокий от общего'] = round(
            count_df['высокий'] / count_df['Итого'], 2) * 100

        return count_df










def processing_pup(base_df: pd.DataFrame, answers_df: pd.DataFrame):
    """
    Функция для обработки теста Профессиональные установки подростков
    :param base_df:
    :param answers_df:
    :return:
    """
    try:
        out_answer_df = base_df.copy()  # делаем копию для последующего соединения с сырыми ответами
        if answers_df.shape[1] != 24:
            raise BadCountColumnsPUP


        lst_check_cols = ['Я слишком плохо знаю мир профессий','Выбор профессии не должен делаться под влиянием эмоций',
                          'Я могу отказаться от многих удовольствий ради престижной будущей профессии','Мне нужна поддержка и помощь в выборе профессии',
                          'Я чувствую, что уже пора готовиться к будущей профессии','Я верю, что стану первоклассным специалистом',
                          'Мне трудно сделать выбор между привлекательными профессиями','Я верю, что смогу развить свои способности ради будущей профессии',
                          'Я знаю, что найду профессию по себе','Я чувствую себя уверенно, когда знаю, что мой профессиональный выбор одобряют другие люди',
                          'Совершенно не знаю, на что ориентироваться при выборе профессии','Реклама многих профессий редко соответствует их реальному содержанию',
                          'Я надеюсь, что выбранная профессия позволит раскрыть мою индивидуальность','Я надеюсь, что моя профессия будет востребованной в будущем',
                          'Совершенно не знаю, с чего мне начать свой профессиональный путь','Я верю, что работа даст мне независимость от родителей',
                          'В выборе профессии я слишком поддаюсь внешним влияниям, советам, примерам','Я знаю, на какого профессионала я хочу стать похожим',
                          'Я надеюсь, что я буду с удовольствием заниматься выбранной профессией','Я приложу все усилия, чтобы сделать успешную карьеру',
                          'Я совсем не стремлюсь к взрослой и самостоятельной жизни','Я плохо представляю свое профессиональное будущее',
                          'Для меня важна не профессия, а карьера','В будущей профессии мне хотелось бы стать известным человеком'
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
            raise BadOrderPUP

        answers_df = answers_df.applymap(convert_to_int)  # приводим к инту
        # проверяем правильность
        valid_values = [1, 2, 3, 4, 5,6]
        # Проверяем, есть ли значения, отличающиеся от указанных в списке
        lst_error_answers = []  # список для хранения строк где найдены неправильные ответы

        for i in range(24):
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
            raise BadValuePUP

        base_df[f'Необработанное'] = answers_df.apply(processing_result_pup, axis=1)
        base_df[f'Значение_уверенности'] = answers_df.apply(calc_value_confidence, axis=1)
        base_df['Уровень_уверенности'] = base_df['Значение_уверенности'].apply(calc_level_confidence)

        base_df[f'Значение_нерешительности'] = answers_df.apply(calc_value_indecision, axis=1)
        base_df['Уровень_нерешительности'] = base_df['Значение_нерешительности'].apply(calc_level_indecision)

        # Создаем датафрейм для создания части в общий датафрейм
        part_df = pd.DataFrame(columns=['ПУП_Необработанное','ПУП_Значение_уверенности', 'ПУП_Уровень_уверенности', 'ПУП_Значение_нерешительности','ПУП_Уровень_нерешительности'])
        part_df['ПУП_Необработанное'] = base_df['Необработанное']
        part_df['ПУП_Значение_уверенности'] = base_df['Значение_уверенности']
        part_df['ПУП_Уровень_уверенности'] = base_df['Уровень_уверенности']
        part_df['ПУП_Значение_нерешительности'] = base_df['Значение_нерешительности']
        part_df['ПУП_Уровень_нерешительности'] = base_df['Уровень_нерешительности']

        base_df.sort_values(by='Значение_уверенности', ascending=False, inplace=True)  # сортируем
        out_answer_df = pd.concat([out_answer_df, answers_df], axis=1)  # Датафрейм для проверки

        # Создаем строку с описанием
        description_result = """
Шкала оценки результатов уверенности в будущем выборе
больше 67 баллов – высокая;
54-66 баллов – средняя;
53 и ниже баллов – низкая.

Шкала оценки результатов нерешительности в выборе профессии
больше 20 баллов – высокая;
13-19 баллов – средняя;
12 и ниже баллов – низкая.

Полученные результаты уверенности и неуверенности позволяют выявить психологическую готовность старшеклассников к переходу на следующий возрастной этап, связанный с выбором профессии и получением профессионального образования.      
        """
        # создаем описание результата
        base_df[f'Описание_результата'] = 'Профессиональные установки подростков.\nРезультат тестирования:\n' +base_df[
            f'Необработанное']+'\n' + description_result
        part_df['ПУП_Описание_результата'] = base_df[f'Описание_результата']


        # Общий свод сколько склонностей всего в процентном соотношении
        svod_all_df = count_all_scale(base_df, ['уверенности', 'нерешительности'],
                                      ['низкий',
                                       'средний',
                                       'высокий', 'Итого'])

        # формируем основной словарь
        out_dct = {'Списочный результат': base_df, 'Список для проверки': out_answer_df,
                   'Свод по уровням': svod_all_df,
                   }

        lst_level = ['низкий',
                     'средний',
                     'высокий']
        dct_conf = dict()


        for level in lst_level:
            temp_df = base_df[base_df['Уровень_уверенности'] == level]
            if temp_df.shape[0] != 0:
                if level == 'низкий':
                    level = 'низкая уверенность'
                elif level == 'средний':
                    level = 'средняя уверенность'
                elif level == 'высокий':
                    level = 'высокая уверенность'
                dct_conf[level] = temp_df
        out_dct.update(dct_conf)

        dct_indecision = dict()

        for level in lst_level:
            temp_df = base_df[base_df['Уровень_нерешительности'] == level]
            if temp_df.shape[0] != 0:
                if level == 'низкий':
                    level = 'низкая нерешительность'
                elif level == 'средний':
                    level = 'средняя нерешительность'
                elif level == 'высокий':
                    level = 'высокая нерешительность'

                dct_indecision[level] = temp_df
        out_dct.update(dct_indecision)


        lst_reindex_group_cols = ['Класс', 'низкий',
                     'средний',
                     'высокий','Итого']
        lst_reindex_group_sex_cols = ['Класс','Пол', 'низкий',
                     'средний',
                     'высокий','Итого']

        lst_reindex_course_cols = ['Номер_класса', 'низкий',
                     'средний',
                     'высокий','Итого']
        lst_reindex_course_sex_cols = ['Номер_класса','Пол','низкий',
                     'средний',
                     'высокий','Итого']


        """
              Обрабатываем Класс
              """

        # Уверенность
        svod_group_sop_df = calc_mean(base_df, 'Класс', ['Класс'], 'Значение_уверенности')
        svod_count_group_sop_df = calc_count(base_df, 'Класс', ['Класс'], 'Значение_уверенности', 'Уровень_уверенности',
                                             lst_reindex_group_cols)
        # Неуверенность
        svod_group_dp_df = calc_mean(base_df, 'Класс', ['Класс'], 'Значение_нерешительности')
        svod_count_group_dp_df = calc_count(base_df, 'Класс', ['Класс'], 'Значение_нерешительности', 'Уровень_нерешительности',
                                            lst_reindex_group_cols)

        """
                   Обрабатываем Класс Пол
                   """
        # Уверенность
        svod_group_sex_sop_df = calc_mean(base_df, 'Класс', ['Класс', 'Пол'], 'Значение_уверенности')
        svod_count_group_sex_sop_df = calc_count(base_df, 'Класс', ['Класс', 'Пол'], 'Значение_уверенности',
                                                 'Уровень_уверенности', lst_reindex_group_sex_cols)

        # Нерешительность
        svod_group_sex_dp_df = calc_mean(base_df, 'Класс', ['Класс', 'Пол'], 'Значение_нерешительности')
        svod_count_group_sex_dp_df = calc_count(base_df, 'Класс', ['Класс', 'Пол'], 'Значение_нерешительности',
                                                'Уровень_нерешительности', lst_reindex_group_sex_cols)


        """
            Обрабатываем Номер_класса
            """

        # Уверенность
        svod_course_sop_df = calc_mean(base_df, 'Номер_класса', ['Номер_класса'], 'Значение_уверенности')
        svod_count_course_sop_df = calc_count(base_df, 'Номер_класса', ['Номер_класса'], 'Значение_уверенности', 'Уровень_уверенности',
                                              lst_reindex_course_cols)
        # Нерешительность
        svod_course_dp_df = calc_mean(base_df, 'Номер_класса', ['Номер_класса'], 'Значение_нерешительности')
        svod_count_course_dp_df = calc_count(base_df, 'Номер_класса', ['Номер_класса'], 'Значение_нерешительности', 'Уровень_нерешительности',
                                             lst_reindex_course_cols)

        """
             Обрабатываем Номер_класса Пол
             """
        # Уверенность
        svod_course_sex_sop_df = calc_mean(base_df, 'Номер_класса', ['Номер_класса', 'Пол'], 'Значение_уверенности')
        svod_count_course_sex_sop_df = calc_count(base_df, 'Номер_класса', ['Номер_класса', 'Пол'],
                                                  'Значение_уверенности',
                                                  'Уровень_уверенности', lst_reindex_course_sex_cols)

        # Нерешительность
        svod_course_sex_dp_df = calc_mean(base_df, 'Номер_класса', ['Номер_класса', 'Пол'], 'Значение_нерешительности')
        svod_count_course_sex_dp_df = calc_count(base_df, 'Номер_класса', ['Номер_класса', 'Пол'], 'Значение_нерешительности',
                                                 'Уровень_нерешительности',
                                                 lst_reindex_course_sex_cols)





        svod_dct = {'Среднее Класс Ув':svod_group_sop_df,'Количество Класс Ув':svod_count_group_sop_df,
                    'Среднее Класс Нер': svod_group_dp_df, 'Количество Класс Нер': svod_count_group_dp_df,
                    'Среднее Класс Пол Ув': svod_group_sex_sop_df,'Количество Класс Пол Ув': svod_count_group_sex_sop_df,
                    'Среднее Класс Пол Нер': svod_group_sex_dp_df, 'Количество Класс Пол Нер': svod_count_group_sex_dp_df,
                    'Среднее Номер_класса Ув': svod_course_sop_df,'Количество Номер_класса Ув': svod_count_course_sop_df,
                    'Среднее Номер_класса Нер': svod_course_dp_df, 'Количество Номер_класса Нер': svod_count_course_dp_df,
                    'Среднее Номер_класса Пол Ув': svod_course_sex_sop_df,'Количество Номер_класса Пол Ув': svod_count_course_sex_sop_df,
                    'Среднее Номер_класса Пол Нер': svod_course_sex_dp_df,'Количество Номер_класса Пол Нер': svod_count_course_sex_dp_df,
                    }
        out_dct.update(svod_dct)

        return out_dct, part_df






    except BadOrderPUP:
        messagebox.showerror('Лахеcис',
                             f'При обработке вопросов теста Профессиональные установки подростков Андреева обнаружены неправильные вопросы. Проверьте названия колонок с вопросами:\n'
                             f'{error_order_message}\n'
                             f'Используйте при создании Яндекс-формы написание вопросов из руководства пользователя программы Лахесис.')
    except BadValuePUP:
        messagebox.showerror('Лахеcис',
                             f'При обработке вопросов теста Профессиональные установки подростков Андреева обнаружены неправильные варианты ответов. Проверьте ответы на указанных строках:\n'
                             f'{error_message}\n'
                             f'Используйте при создании Яндекс-формы написание вариантов ответа из руководства пользователя программы Лахесис.')


    except BadCountColumnsPUP:
        messagebox.showerror('Лахеcис',
                             f'Проверьте количество колонок с ответами на тест Профессиональные установки подростков Андреева\n'
                             f'Должно быть 24 колонки с ответами')


















