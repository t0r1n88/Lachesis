"""
Скрипт для обработки результатов теста ценностные ориентиры в карьере
"""
import pandas as pd
from tkinter import messagebox
from lachesis_support_functions import convert_to_int,round_mean,sort_name_class

class BadValueCok(Exception):
    """
    Исключение для неправильных значений в вариантах ответов
    """
    pass

class BadCountColumnsCok(Exception):
    """
    Исключение для обработки случая если количество колонок не равно 41
    """
    pass




def extract_key_max_value(cell:str) ->str:
    """
    Функция для извлечения ключа с максимальным значением
    :param cell: строка формата ключ - значение;
    :return: ключ словаря в формате строки
    """
    # проверяем если некорректное значение
    if 'Скопируйте правильные значения для указанных вопросов из квадратных скобок' in cell:
        return cell
    dct_result = {}
    cell = cell.replace('\n','') # убираем переносы
    lst_temp = cell.split(';') # сплитим по точке с запятой
    for result in lst_temp:
        # отбрасываем пустую строку
        if result:
            key,value = result.split(' - ') # извлекаем ключ и значение
            dct_result[key] = int(value)

    # возвращаем элемент с максимальным значением
    return max(dct_result, key=dct_result.get)

def extract_max_value(cell:str):
    """
    Функция для извлечения значения ключа с максимальным значением , ха звучит странно
    :param cell: строка формата ключ - значение;
    :return: ключ словаря в формате строки
    """
    # проверяем если некорректное значение
    if 'Скопируйте правильные значения для указанных вопросов из квадратных скобок' in cell:
        return 0
    dct_result = {}
    cell = cell.replace('\n','') # убираем переносы
    lst_temp = cell.split(';') # сплитим по точке с запятой
    for result in lst_temp:
        # отбрасываем пустую строку
        if result:
            key,value = result.split(' - ') # извлекаем ключ и значение
            dct_result[key] = int(value)

    # возвращаем элемент с максимальным значением
    return dct_result[max(dct_result, key=dct_result.get)]

def processing_result_cok(row):
    """
Функция для вычисления итогового балла  результатов теста Диагностика ценностных ориентаций в карьере
"""

    # Создаем словарь для хранения данных
    dct_type = {'Профессиональная компетентность': 0, 'Менеджмент': 0, 'Автономия (независимость)': 0,
                'Стабильность работы': 0,
                'Стабильность места жительства': 0, 'Служение': 0, 'Вызов': 0,
                'Интеграция стилей жизни': 0, 'Предпринимательство': 0}
    dct_error = {}  # словарь для хранения ошибочных  значений, для того чтобы было легче находить ошибки при обновлении
    # 1
    dct_type['Профессиональная компетентность'] += row[0]

    # 2
    dct_type['Менеджмент'] += row[1]

    # 3
    dct_type['Автономия (независимость)'] += row[2]

    # 4
    dct_type['Стабильность работы'] += row[3]

    # 5
    dct_type['Служение'] += row[4]

    # 6
    dct_type['Вызов'] += row[5]

    # 7
    dct_type['Интеграция стилей жизни'] += row[6]

    # 8
    dct_type['Предпринимательство'] += row[7]

    # 9
    dct_type['Профессиональная компетентность'] += row[8]

    # 10
    dct_type['Менеджмент'] += row[9]

    # 11
    dct_type['Автономия (независимость)'] += row[10]

    # 12
    dct_type['Стабильность работы'] += row[11]

    # 13
    dct_type['Служение'] += row[12]

    # 14
    dct_type['Вызов'] += row[13]

    # 15
    dct_type['Интеграция стилей жизни'] += row[14]

    # 16
    dct_type['Предпринимательство'] += row[15]

    # 17
    dct_type['Профессиональная компетентность'] += row[16]

    # 18
    dct_type['Менеджмент'] += row[17]

    # 19
    dct_type['Автономия (независимость)'] += row[18]

    # 20
    dct_type['Стабильность места жительства'] += row[19]

    # 21
    dct_type['Служение'] += row[20]

    # 22
    dct_type['Вызов'] += row[21]

    # 23
    dct_type['Интеграция стилей жизни'] += row[22]

    # 24
    dct_type['Предпринимательство'] += row[23]

    # 25
    dct_type['Профессиональная компетентность'] += row[24]

    # 26
    dct_type['Менеджмент'] += row[25]

    # 27
    dct_type['Автономия (независимость)'] += row[26]

    # 28
    dct_type['Стабильность места жительства'] += row[27]

    # 29
    dct_type['Служение'] += row[28]

    # 30
    dct_type['Вызов'] += row[29]

    # 31
    dct_type['Интеграция стилей жизни'] += row[30]

    # 32
    dct_type['Предпринимательство'] += row[31]

    # 33
    dct_type['Профессиональная компетентность'] += row[32]

    # 34
    dct_type['Менеджмент'] += row[33]

    # 35
    dct_type['Автономия (независимость)'] += row[34]

    # 36
    dct_type['Стабильность работы'] += row[35]

    # 37
    dct_type['Служение'] += row[36]

    # 38
    dct_type['Вызов'] += row[37]

    # 39
    dct_type['Интеграция стилей жизни'] += row[38]

    # 40
    dct_type['Предпринимательство'] += row[39]

    # 41
    dct_type['Стабильность места жительства'] += row[40]

    # Делим на 5 результаты
    for key, value in dct_type.items():
        dct_type[key] = round(dct_type[key] / 5)
    # Сортируем
    result_lst = sorted(dct_type.items(), key=lambda t: t[1], reverse=True)

    begin_str = ''
    # создаем строку с результатами
    for sphere, value in result_lst:
        begin_str += f'{sphere} - {value};\n'

    return begin_str




def processing_cok(base_df: pd.DataFrame, answers_df: pd.DataFrame):
    """
    Функция для обработки теста ценностных ориентиров в карьере
    :param base_df:
    :param answers_df:
    :return:
    """
    try:
        out_answer_df = base_df.copy()  # делаем копию для последующего соединения с сырыми ответами
        if answers_df.shape[1] != 41:
            raise BadCountColumnsCok
        # Переименовываем колонки
        answers_df.columns = [f'Вопрос_ №{i}' for i in range(1, 42)]

        answers_df = answers_df.applymap(convert_to_int) # приводим к инту

        # проверяем правильность
        valid_values = [1, 2, 3, 4,5,6,7,8,9,10]
        # Проверяем, есть ли значения, отличающиеся от указанных в списке
        mask = ~answers_df.isin(valid_values)

        # Получаем строки с отличающимися значениями
        result_check = answers_df[mask.any(axis=1)]
        if len(result_check) != 0:
            error_row = list(map(lambda x: x + 2, result_check.index))
            error_row = list(map(str, error_row))
            error_message = ';'.join(error_row)
            raise BadValueCok

        # Создаем колонку для результатов первичного подсчета
        base_df[f'Необработанное'] = answers_df.apply(processing_result_cok, axis=1)
        base_df[f'Обработанное'] = base_df[f'Необработанное'].apply(
            extract_key_max_value)
        base_df[f'Максимум'] = base_df[f'Необработанное'].apply(
            extract_max_value)

        # Создаем датафрейм для создания части в общий датафрейм
        part_df = pd.DataFrame(columns=['ЦОК_Необработанное', 'ЦОК_Обработанное','ЦОК_Максимум'])
        part_df['ЦОК_Необработанное'] = base_df['Необработанное']
        part_df['ЦОК_Обработанное'] = base_df['Обработанное']
        part_df['ЦОК_Максимум'] = base_df['Максимум']

        base_df.sort_values(by='Максимум', ascending=False, inplace=True)  # сортируем
        out_answer_df = pd.concat([out_answer_df, answers_df], axis=1)  # Датафрейм для проверки

        """
            Обрабатываем Класс
            """
        # Среднее по Класс
        svod_group_df = pd.pivot_table(base_df, index=['Класс','Обработанное'],
                                           values=['Максимум'],
                                           aggfunc=round_mean)
        svod_group_df.reset_index(inplace=True)

        svod_group_df.sort_values(by='Класс', key=lambda x: x.map(sort_name_class), inplace=True)  # сортируем

        # Количество Класс
        svod_count_group_df = pd.pivot_table(base_df, index=['Класс'],
                                                 columns='Обработанное',
                                                 values='Максимум',
                                                 aggfunc='count', margins=True, margins_name='Итого')
        svod_count_group_df.reset_index(inplace=True)
        svod_count_group_df = svod_count_group_df.reindex(
            columns=['Класс', 'Профессиональная компетентность', 'Менеджмент',
                     'Автономия (независимость)', 'Стабильность работы',
                     'Стабильность места жительства', 'Служение',
                     'Вызов', 'Интеграция стилей жизни',
                     'Предпринимательство',
                     'Итого'])
        svod_count_group_df['% Профессиональная компетентность от общего'] = round(
            svod_count_group_df['Профессиональная компетентность'] / svod_count_group_df['Итого'], 2) * 100
        svod_count_group_df['% Менеджмент от общего'] = round(
            svod_count_group_df['Менеджмент'] / svod_count_group_df['Итого'], 2) * 100
        svod_count_group_df['% Автономия (независимость) от общего'] = round(
            svod_count_group_df['Автономия (независимость)'] / svod_count_group_df['Итого'], 2) * 100
        svod_count_group_df['% Стабильность работы от общего'] = round(
            svod_count_group_df['Стабильность работы'] / svod_count_group_df['Итого'], 2) * 100
        svod_count_group_df['% Стабильность места жительства от общего'] = round(
            svod_count_group_df['Стабильность места жительства'] / svod_count_group_df['Итого'], 2) * 100
        svod_count_group_df['% Служение от общего'] = round(
            svod_count_group_df['Служение'] / svod_count_group_df['Итого'], 2) * 100
        svod_count_group_df['% Вызов от общего'] = round(
            svod_count_group_df['Вызов'] / svod_count_group_df['Итого'], 2) * 100
        svod_count_group_df['% Интеграция стилей жизни от общего'] = round(
            svod_count_group_df['Интеграция стилей жизни'] / svod_count_group_df['Итого'], 2) * 100
        svod_count_group_df['% Предпринимательство от общего'] = round(
            svod_count_group_df['Предпринимательство'] / svod_count_group_df['Итого'], 2) * 100
        part_svod_df = svod_count_group_df.iloc[:-1:]
        part_svod_df.sort_values(by='Класс', key=lambda x: x.map(sort_name_class), inplace=True)  # сортируем
        itog_svod_df = svod_count_group_df.iloc[-1:]
        svod_count_group_df = pd.concat([part_svod_df, itog_svod_df])

        # Среднее по Класс Пол
        svod_group_sex_df = pd.pivot_table(base_df, index=['Класс','Пол','Обработанное'],
                                           values=['Максимум'],
                                           aggfunc=round_mean)
        svod_group_sex_df.reset_index(inplace=True)

        svod_group_sex_df.sort_values(by='Класс', key=lambda x: x.map(sort_name_class), inplace=True)  # сортируем

        # Количество Класс Пол
        svod_count_group_sex_df = pd.pivot_table(base_df, index=['Класс','Пол'],
                                                 columns='Обработанное',
                                                 values='Максимум',
                                                 aggfunc='count', margins=True, margins_name='Итого')
        svod_count_group_sex_df.reset_index(inplace=True)
        svod_count_group_sex_df = svod_count_group_sex_df.reindex(
            columns=['Класс','Пол', 'Профессиональная компетентность', 'Менеджмент',
                     'Автономия (независимость)', 'Стабильность работы',
                     'Стабильность места жительства', 'Служение',
                     'Вызов', 'Интеграция стилей жизни',
                     'Предпринимательство',
                     'Итого'])
        svod_count_group_sex_df['% Профессиональная компетентность от общего'] = round(
            svod_count_group_sex_df['Профессиональная компетентность'] / svod_count_group_sex_df['Итого'], 2) * 100
        svod_count_group_sex_df['% Менеджмент от общего'] = round(
            svod_count_group_sex_df['Менеджмент'] / svod_count_group_sex_df['Итого'], 2) * 100
        svod_count_group_sex_df['% Автономия (независимость) от общего'] = round(
            svod_count_group_sex_df['Автономия (независимость)'] / svod_count_group_sex_df['Итого'], 2) * 100
        svod_count_group_sex_df['% Стабильность работы от общего'] = round(
            svod_count_group_sex_df['Стабильность работы'] / svod_count_group_sex_df['Итого'], 2) * 100
        svod_count_group_sex_df['% Стабильность места жительства от общего'] = round(
            svod_count_group_sex_df['Стабильность места жительства'] / svod_count_group_sex_df['Итого'], 2) * 100
        svod_count_group_sex_df['% Служение от общего'] = round(
            svod_count_group_sex_df['Служение'] / svod_count_group_sex_df['Итого'], 2) * 100
        svod_count_group_sex_df['% Вызов от общего'] = round(
            svod_count_group_sex_df['Вызов'] / svod_count_group_sex_df['Итого'], 2) * 100
        svod_count_group_sex_df['% Интеграция стилей жизни от общего'] = round(
            svod_count_group_sex_df['Интеграция стилей жизни'] / svod_count_group_sex_df['Итого'], 2) * 100
        svod_count_group_sex_df['% Предпринимательство от общего'] = round(
            svod_count_group_sex_df['Предпринимательство'] / svod_count_group_sex_df['Итого'], 2) * 100
        part_svod_df = svod_count_group_sex_df.iloc[:-1:]
        part_svod_df.sort_values(by='Класс', key=lambda x: x.map(sort_name_class), inplace=True)  # сортируем
        itog_svod_df = svod_count_group_sex_df.iloc[-1:]
        svod_count_group_sex_df = pd.concat([part_svod_df, itog_svod_df])

        """
            Обрабатываем Номер_класса
            """
        # Среднее по Номер_класса
        svod_course_df = pd.pivot_table(base_df, index=['Номер_класса', 'Обработанное'],
                                        values=['Максимум'],
                                        aggfunc=round_mean)
        svod_course_df.reset_index(inplace=True)

        # Количество Номер_класса
        svod_count_course_df = pd.pivot_table(base_df, index=['Номер_класса'],
                                              columns='Обработанное',
                                              values='Максимум',
                                              aggfunc='count', margins=True, margins_name='Итого')
        svod_count_course_df.reset_index(inplace=True)
        svod_count_course_df = svod_count_course_df.reindex(
            columns=['Номер_класса', 'Профессиональная компетентность', 'Менеджмент',
                     'Автономия (независимость)', 'Стабильность работы',
                     'Стабильность места жительства', 'Служение',
                     'Вызов', 'Интеграция стилей жизни',
                     'Предпринимательство',
                     'Итого'])
        svod_count_course_df['% Профессиональная компетентность от общего'] = round(
            svod_count_course_df['Профессиональная компетентность'] / svod_count_course_df['Итого'], 2) * 100
        svod_count_course_df['% Менеджмент от общего'] = round(
            svod_count_course_df['Менеджмент'] / svod_count_course_df['Итого'], 2) * 100
        svod_count_course_df['% Автономия (независимость) от общего'] = round(
            svod_count_course_df['Автономия (независимость)'] / svod_count_course_df['Итого'], 2) * 100
        svod_count_course_df['% Стабильность работы от общего'] = round(
            svod_count_course_df['Стабильность работы'] / svod_count_course_df['Итого'], 2) * 100
        svod_count_course_df['% Стабильность места жительства от общего'] = round(
            svod_count_course_df['Стабильность места жительства'] / svod_count_course_df['Итого'], 2) * 100
        svod_count_course_df['% Служение от общего'] = round(
            svod_count_course_df['Служение'] / svod_count_course_df['Итого'], 2) * 100
        svod_count_course_df['% Вызов от общего'] = round(
            svod_count_course_df['Вызов'] / svod_count_course_df['Итого'], 2) * 100
        svod_count_course_df['% Интеграция стилей жизни от общего'] = round(
            svod_count_course_df['Интеграция стилей жизни'] / svod_count_course_df['Итого'], 2) * 100
        svod_count_course_df['% Предпринимательство от общего'] = round(
            svod_count_course_df['Предпринимательство'] / svod_count_course_df['Итого'], 2) * 100

        # Среднее по Номер_класса Пол
        svod_course_sex_df = pd.pivot_table(base_df, index=['Номер_класса', 'Пол', 'Обработанное'],
                                            values=['Максимум'],
                                            aggfunc=round_mean)
        svod_course_sex_df.reset_index(inplace=True)

        # Количество Номер_класса Пол
        svod_count_course_sex_df = pd.pivot_table(base_df, index=['Номер_класса', 'Пол'],
                                                  columns='Обработанное',
                                                  values='Максимум',
                                                  aggfunc='count', margins=True, margins_name='Итого')
        svod_count_course_sex_df.reset_index(inplace=True)
        svod_count_course_sex_df = svod_count_course_sex_df.reindex(
            columns=['Номер_класса', 'Пол', 'Профессиональная компетентность', 'Менеджмент',
                     'Автономия (независимость)', 'Стабильность работы',
                     'Стабильность места жительства', 'Служение',
                     'Вызов', 'Интеграция стилей жизни',
                     'Предпринимательство',
                     'Итого'])
        svod_count_course_sex_df['% Профессиональная компетентность от общего'] = round(
            svod_count_course_sex_df['Профессиональная компетентность'] / svod_count_course_sex_df['Итого'], 2) * 100
        svod_count_course_sex_df['% Менеджмент от общего'] = round(
            svod_count_course_sex_df['Менеджмент'] / svod_count_course_sex_df['Итого'], 2) * 100
        svod_count_course_sex_df['% Автономия (независимость) от общего'] = round(
            svod_count_course_sex_df['Автономия (независимость)'] / svod_count_course_sex_df['Итого'], 2) * 100
        svod_count_course_sex_df['% Стабильность работы от общего'] = round(
            svod_count_course_sex_df['Стабильность работы'] / svod_count_course_sex_df['Итого'], 2) * 100
        svod_count_course_sex_df['% Стабильность места жительства от общего'] = round(
            svod_count_course_sex_df['Стабильность места жительства'] / svod_count_course_sex_df['Итого'], 2) * 100
        svod_count_course_sex_df['% Служение от общего'] = round(
            svod_count_course_sex_df['Служение'] / svod_count_course_sex_df['Итого'], 2) * 100
        svod_count_course_sex_df['% Вызов от общего'] = round(
            svod_count_course_sex_df['Вызов'] / svod_count_course_sex_df['Итого'], 2) * 100
        svod_count_course_sex_df['% Интеграция стилей жизни от общего'] = round(
            svod_count_course_sex_df['Интеграция стилей жизни'] / svod_count_course_sex_df['Итого'], 2) * 100
        svod_count_course_sex_df['% Предпринимательство от общего'] = round(
            svod_count_course_sex_df['Предпринимательство'] / svod_count_course_sex_df['Итого'], 2) * 100

        # Общий свод сколько склонностей всего в процентном соотношении
        svod_all_df = pd.pivot_table(base_df, index=['Обработанное'],
                                                  values='Максимум',
                                                  aggfunc='count')

        svod_all_df['% от общего'] = round(
            svod_all_df['Максимум'] / svod_all_df['Максимум'].sum(),3) * 100
        # # Создаем суммирующую строку
        svod_all_df.loc['Итого'] = svod_all_df.sum()
        svod_all_df['Максимум'] = svod_all_df['Максимум'].astype(int)
        svod_all_df.reset_index(inplace=True)
        svod_all_df.rename(columns={'Обработанное':'Ценностная ориентация','Максимум':'Количество'},inplace=True)

        """
            Создаем колонку с описанием результата
            """
        description_result = """
        По каждой из девяти карьерных ориентаций подсчитывается количество баллов. Таким образом определяется ведущая карьерная ориентация - количество набранных для этого баллов должно быть не менее пяти. Иногда ведущей не становится ни одна карьерная ориентация - в таком случае карьера не является центральной в жизни личности.
    
        1) Профессиональная компетентность -быть профессионалом, мастером в своем деле.
        Эта ориентация связана с наличием способностей и талантов в определенной области.
        Люди с такой ориентацией хотят быть мастерами своего дела, они бывают особенно счастливы, когда достигают успеха в профессиональной сфере, но быстро теряют интерес к работе, которая не позволяет развивать их способности. Вряд ли их заинтересует даже значительно более высокая должность, если она не связана с их профессиональными компетенциями. Они ищут признания своих талантов, что должно выражаться в статусе, соответствующем их мастерству. Они готовы управлять другими в пределах своей компетенции, но управление не представляет для них особого интереса. Поэтому многие из этой категории отвергают работу руководителя, управление рассматривают как необходимое условие для продвижения в своей профессиональной сфере.
        2) Менеджмент - Управлять – людьми, проектами, бизнес-процессами и т.п.
        Для этих людей первостепенное значение имеет ориентация личности на интеграцию усилий других людей, полнота ответственности за конечный результат и соединение различных функций организации. С возрастом и опытом эта карьерная ориентация проявляется сильнее. Возможности для лидерства, высокого дохода, повышенных уровней ответственности и вклад в успех своей организации являются ключевыми ценностями и мотивами. Самое главное для них – управление: людьми, проектами, любыми бизнес-процессами – это в целом не имеет принципиального значения. Центральное понятие их профессионального развития – власть, осознание того, что от них зависит принятие ключевых решений. Причем для них не является принципиальным управление собственным проектом или целым бизнесом, скорее наоборот, они в большей степени ориентированы на построение карьеры в наемном менеджменте, но при условии, что им будут делегированы значительные полномочия. Человек с такой ориентацией будет считать, что не достиг цели своей карьеры, пока не займет должность, на которой будет управлять различными сторонами деятельности предприятия.
        3) Автономия (независимость) – Главное в работе – это свобода и независимость.
        Первичная забота личности с такой ориентацией –освобождение от организационных правил, предписаний и ограничений. Они испытывают трудности, связанные с установленными правилами, процедурами, рабочим днем, дисциплиной, формой одежды и т.д. Они любят выполнять работу своим способом, темпом и по собственным стандартам. Они не любят, когда работа вмешивается в их частную жизнь, поэтому предпочитают делать независимую карьеру собственным путем. Они скорее выберут низкосортную работу, чем откажутся от автономии и независимости. Для них первоочередная задача развития карьеры – получить возможность работать самостоятельно, самому решать, как, когда и что делать для достижения тех или иных целей. Карьера для них – это, прежде всего, способ реализации их свободы, поэтому любые рамки и строгое подчинение оттолкнут их даже от внешне привлекательной вакансии. Такой человек может работать в организации, которая обеспечивает достаточную степень свободы.
        4) Стабильность работы - стабильная, надежная работа на длительное время.
        Эти люди испытывают потребность в безопасности, защите и возможности прогнозирования и будут искать постоянную работу с минимальной вероятностью увольнения. Эти люди отождествляют свою работу со своей карьерой. Их потребность в безопасности и стабильности ограничивает выбор вариантов	карьеры.
        Авантюрные или краткосрочные проекты и только становящиеся на ноги компании их, скорее всего, не привлекают. Они очень ценят социальные гарантии, которые может предложить работодатель, и, как правило, их выбор места работы связан именно с длительным контрактом и стабильным положением компании на рынке. Такие люди ответственность за управление своей карьерой перекладывают на нанимателя. Часто данная ценностная ориентация сочетается с невысоким уровнем притязаний.
        5) Стабильность места жительства - Главное – жить в своем городе (минимум переездов, командировок).
        Важнее остаться на одном месте жительства, чем получить повышение или новую работу на новой местности. Переезд для таких людей неприемлем, и даже частые командировки являются для них негативным фактором при рассмотрении	предложения о работе.
        6) Служение - Воплощать в работе свои идеалы и ценности.
        Данная ценностная ориентация характерна для людей, занимающихся делом по причине желания реализовать в своей работе главные ценности. Они часто ориентированы больше на ценности, чем на требующиеся в данном виде работы способности. Они стремятся приносить пользу людям, обществу, для них очень важно видеть конкретные плоды своей работы, даже если они и не выражены в материальном эквиваленте. Основной тезис построения их карьеры – получить возможность максимально эффективно использовать их таланты и опыт для реализации общественно	важной цели. Люди, ориентированные на служение, общительны и часто консервативны. Человек с такой ориентацией не будет работать в организации, которая враждебна его целям и ценностям.
        7) Вызов - Сделать   невозможное – возможным, решать   уникальные   задачи.
        Эти люди считают успехом преодоление непреодолимых препятствий, решение неразрешимых проблем или просто выигрыш. Они ориентированы на то, чтобы “бросать вызов”. Для одних людей вызов представляет более трудная работа, для других это — конкуренция и межличностные отношения. Они ориентированы на решение заведомо сложных задач, преодоление препятствий ради победы в конкурентной борьбе. Они чувствуют себя преуспевающими только тогда, когда постоянно вовлечены в решение трудных проблем или в ситуацию соревнования. Карьера для них – это постоянный вызов их профессионализму, и они всегда готовы его принять. Социальная ситуация чаще всего рассматривается с позиции “выигрыша – проигрыша”. Процесс борьбы и победа более важна для них, чем конкретная область деятельности или квалификация. Новизна, разнообразие и вызов имеют для них очень большую ценность, и, если все идет слишком просто, им становиться скучно.
        8) Интеграция стилей жизни - Сохранение гармонии между сложившейся личной жизнью и карьерой.
        Для людей этой категории карьера должна ассоциироваться с общим стилем жизни, уравновешивая потребности человека, семьи и карьеры. Они хотят, чтобы организационные отношения отражали бы уважение к их личным и семейным проблемам.
        Выбирать и поддерживать определенный образ жизни для них важнее, чем добиваться успеха в карьере. Развитие карьеры их привлекает только в том случае, если она не нарушает привычный им стиль жизни и окружение. Для них важно, чтобы все было уравновешено – карьера, семья, личные интересы и т.п. Жертвовать   чем-то   одним   ради   другого   им    явно    не    свойственно. Такие люди обычно в своем поведении проявляют конформность (тенденция изменять свое поведение в зависимости от влияния других людей с тем, чтобы оно соответствовало мнению окружающих)
        9) Предпринимательство – Создавать новые организации, товары, услуги.
        Этим людям нравится создавать новые организации, товары или услуги, которые могут быть отождествлены с их усилиями. Работать на других – это не их, они – предприниматели по духу, и цель их карьеры – создать что-то новое, организовать свое дело, воплотить в жизнь идею, всецело принадлежащую только им. Вершина карьеры в их понимании – собственный бизнес.
        """
        # создаем описание результата
        base_df[f'Описание_результата'] = 'Диагностика ценностных ориентаций в карьере.\n' + base_df[
            f'Необработанное'] + description_result
        part_df['ЦОК_Описание_результата'] = base_df[f'Описание_результата']

        # формируем словарь
        out_dct = {'Списочный результат': base_df, 'Список для проверки': out_answer_df,
                   'Общий свод':svod_all_df,
                   'Среднее Класс': svod_group_df,'Количество Класс': svod_count_group_df,
                   'Среднее Класс Пол': svod_group_sex_df,'Количество Класс Пол': svod_count_group_sex_df,
                   'Среднее Номер_класса': svod_course_df, 'Количество Номер_класса': svod_count_course_df,
                   'Среднее Номер_класса Пол': svod_course_sex_df, 'Количество Номер_класса Пол': svod_count_course_sex_df,
                   }

        return out_dct, part_df
    except BadValueCok:
        messagebox.showerror('Лахеcис',
                             f'При обработке вопросов теста Ценностные ориентиры карьеры обнаружены неправильные варианты ответов. Проверьте ответы на указанных строках:\n'
                             f'{error_message}\n'
                             f'Используйте при создании Яндекс-формы написание вариантов ответа из руководства пользователя программы Лахесис.')


    except BadCountColumnsCok:
        messagebox.showerror('Лахеcис',
                             f'Проверьте количество колонок с ответами на тест Ценностные ориентиры карьеры\n'
                             f'Должно быть 41 колонка с ответами')

