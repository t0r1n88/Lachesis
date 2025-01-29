"""
Скрипт для обработки тестов студентов СПО
"""
import pandas as pd
import openpyxl
from tkinter import messagebox
import re


class NotSameSize(Exception):
    """
    Исключение для проверки совпадают ли размеры таблицы с количеством колонок требуемых для выполнения тестов указанных в параметрах
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






def processing_kondash(base_df: pd.DataFrame, answers_df: pd.DataFrame, size: int, name_test):
    """
    Проверка колонок и значений таблицы
    """
    dct_replace_value = {'ситуация совершенно не кажется вам неприятной': 0,
                         'ситуация немного волнует, беспокоит вас': 1,
                         'ситуация достаточно неприятна и вызывает такое беспокойство, что вы предпочли бы избежать её': 2,
                         'ситуация очень неприятна и вызывает сильное беспокойство, тревогу, страх': 3,
                         'ситуация для вас крайне неприятна, если вы не можете перенести её и она вызывает у вас очень сильное беспокойство, очень сильный страх': 4}

    # множество значений для колонок теста ШТК
    set_variants_shtk = {'ситуация совершенно не кажется вам неприятной', 'ситуация немного волнует, беспокоит вас',
                         'ситуация достаточно неприятна и вызывает такое беспокойство, что вы предпочли бы избежать её',
                         'ситуация очень неприятна и вызывает сильное беспокойство, тревогу, страх',
                         'ситуация для вас крайне неприятна, если вы не можете перенести её и она вызывает у вас очень сильное беспокойство, очень сильный страх'}

    # Словарь с проверочными данными
    dct_check_table = {
        'ШТК': [{'Отвечать у доски': set_variants_shtk},
                {'Пойти в дом к незнакомым людям': set_variants_shtk},
                {'Участвовать в соревнованиях, конкурсах, в олимпиадах': set_variants_shtk},
                {'Разговаривать с директором техникума, колледжа': set_variants_shtk},
                {'Думать о своем будущем': set_variants_shtk},
                {'Преподаватель смотрит по журналу, кого бы спросить': set_variants_shtk},
                {'Тебя критикуют, в чем- то обвиняют': set_variants_shtk},
                {'На тебя смотрят, когда ты что-нибудь делаешь (наблюдают за тобой во время работы, решения задачи)': set_variants_shtk},
                {'Пишешь контрольную работу': set_variants_shtk},
                {'После контрольной учитель называет отметки': set_variants_shtk},
                {'На тебя не обращают внимания': set_variants_shtk},
                {'У тебя что-то не получается': set_variants_shtk},
                {'Ждешь родителей с родительского собрания': set_variants_shtk},
                {'Тебе грозит неуспех, провал': set_variants_shtk},
                {'Слышишь за своей спиной смех': set_variants_shtk},
                {'Сдаешь экзамены в техникуме, колледже': set_variants_shtk},
                {'На тебя сердятся (непонятно почему)': set_variants_shtk},
                {'Выступать перед большой аудиторией': set_variants_shtk},
                {'Предстоит важное, решающее дело': set_variants_shtk},
                {'Не понимаешь объяснений преподавателя': set_variants_shtk},
                {'С тобой не согласны, противоречат тебе': set_variants_shtk},
                {'Сравниваешь себя с другими': set_variants_shtk},
                {'Проверяют твои способности': set_variants_shtk},
                {'На тебя смотрят как на маленького': set_variants_shtk},
                {'На паре преподаватель неожиданно задает тебе вопрос': set_variants_shtk},
                {'Замолчали, когда ты подошел': set_variants_shtk},
                {'Оценивается твоя работа': set_variants_shtk},
                {'Думаешь о своих делах': set_variants_shtk},
                {'Тебе надо принять для себя решение': set_variants_shtk},
                {'Не можешь справиться с домашним заданием': set_variants_shtk},
                ]}
    answers_df.replace(dct_replace_value,inplace=True) # заменяем слова на цифры для подсчетов
    answers_df.to_excel('data/df.xlsx')
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
    base_df['Уровень_общей_тревожности'] = base_df[
        ['Выберите_свой_курс', 'Выберите_свой_пол', 'Значение_учебной_тревожности']].apply(calc_level_study_condash_anxiety,
                                                                                         axis=1)

    base_df.to_excel('data/dfd.xlsx')







def processing_bek(base_df: pd.DataFrame, answers_df: pd.DataFrame, size: int, name_test):
    pass


def generate_result_spo(params_spo: str, data_spo: str, end_folder: str, threshold_base: int):
    """
    Функция для генерации результатов комплексного теста на оценку состояния тревожности
    :param params_spo: какие тесты используются и в каком порядке
    :param data_spo: файл с данными
    :param end_folder: конечная папка
    :param threshold_base: количество колонок с вводными данными
    :return:
    """
    dct_tests = {'ШТК': (processing_kondash, 30), 'ШТБ': (processing_bek, 21),
                 }  # словарь с наименованием теста функцией для его обработки и количеством колонок

    params_df = pd.read_excel(params_spo, dtype=str, usecols='A',
                              header=None)  # считываем какие тесты нужно использовать
    params_df.dropna(inplace=True)  # удаляем пустые строки
    lst_used_test = params_df.iloc[:, 0].tolist()  # получаем список
    lst_used_test = [value for value in lst_used_test if value in dct_tests.keys()]  # отбираем только те что прописаны

    # создаем счетчик обработанных колонок
    threshold_finshed = threshold_base

    # Проверяем датафрейм на количество колонок
    df = pd.read_excel(data_spo, dtype=str)  # считываем датафрейм
    lst_name_cols = [col for col in df.columns if 'Unnamed' not in col]  # отбрасываем колонки без названия
    df = df[lst_name_cols]

    check_size_df = 0  # проверяем размер датафрейма чтобы он совпадал с количеством вопросов в тестах
    for name_test in lst_used_test:
        check_size_df += dct_tests[name_test][1]
    if check_size_df + threshold_base > df.shape[1]:
        raise NotSameSize

    base_df = df.iloc[:, :threshold_base]  # создаем датафрейм с данными не относящимися к тесту
    # делаем строковыми названия колонок
    base_df.columns = list(map(str, base_df.columns))

    # заменяем пробелы на нижнее подчеркивание и очищаем от пробельных символов в начале и конце
    base_df.columns = [column.strip().replace(' ', '_') for column in base_df.columns]

    # очищаем от всех символов кроме букв цифр
    base_df.columns = [re.sub(r'[^_\d\w]', '', column) for column in base_df.columns]

    # Создаем копию датафрейма с анкетными данными для передачи в функцию
    base_df_for_func = base_df.copy()
    # создаем копию для датафрейма с результатами
    result_df = base_df.copy()

    # Перебираем полученные названия тестов
    for name_test in lst_used_test:
        """
        запускаем функцию хранящуюся в словаре
        передаем туда датафрейм с анкетными данными, датафрейм с данными теста, количество колонок которое занимает данный тест
        получаем 2 датафрейма с результатами для данного теста которые добавляем в основные датафреймы
        """
        # получаем колонки относящиеся к тесту
        temp_df = df.iloc[:, threshold_finshed:threshold_finshed + dct_tests[name_test][1]]
        # обрабатываем и получаем датафреймы для добавления в основные таблицы
        temp_full_df, temp_result_df = dct_tests[name_test][0](base_df_for_func, temp_df,
                                                               dct_tests[name_test][1], name_test)

        base_df = pd.concat([base_df, temp_full_df],
                            axis=1)  # соединяем анкетные данные и вопросы вместе с результатами
        result_df = pd.concat([result_df, temp_result_df], axis=1)
        # увеличиваем предел обозначающий количество обработанных колонок
        threshold_finshed += dct_tests[name_test][1]








if __name__ == '__main__':
    main_params_spo = 'data/параметры для СПО.xlsx'
    main_spo_data = 'data/data.xlsx'
    main_end_folder = 'data/Результат'
    main_quantity_descr_cols = 2

    generate_result_spo(main_params_spo, main_spo_data, main_end_folder, main_quantity_descr_cols)

    print('Lindy Booth')
