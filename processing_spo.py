"""
Скрипт для обработки тестов студентов СПО
"""
import pandas as pd
import openpyxl
from tkinter import messagebox



class NotSameSize(Exception):
    """
    Исключение для проверки совпадают ли размеры таблицы с количеством колонок требуемых для выполнения тестов указанных в параметрах
    """
    pass


def generate_result_spo(params_spo:str, data_spo:str,end_folder:str,quantity_descr_cols:int):
    """
    Функция для генерации результатов комплексного теста на оценку состояния тревожности
    :param params_spo: какие тесты используются и в каком порядке
    :param data_spo: файл с данными
    :param end_folder: конечная папка
    :param quantity_descr_cols: количество колонок с вводными данными
    :return:
    """
    params_df = pd.read_excel(params_spo,dtype=str,usecols='A',header=None) # считываем какие тесты нужно использовать
    dct_tests = {'ШТК':30,'ШТБ':21} # словарь с наименованием теста и количеством вопросов в нем
    params_df.dropna(inplace=True) # удаляем пустые строки
    lst_used_test = params_df.iloc[:,0].tolist() # получаем список
    lst_used_test = [value for value in lst_used_test if value in dct_tests.keys()] # отбираем только те что прописаны

    df = pd.read_excel(data_spo,dtype=str) # считываем датафрейм
    lst_name_cols = [col for col in df.columns if 'Unnamed' not in col] # отбрасываем колонки без названия
    df = df[lst_name_cols]

    check_size_df = 0 # проверяем размер датафрейма чтобы он совпадал с количеством вопросов в тестах
    for name_test in lst_used_test:
        check_size_df += dct_tests[name_test]
    if check_size_df + quantity_descr_cols > df.shape[1]:
        raise NotSameSize

    # множество значений для колонок теста ШТК
    set_variants_shtk = {'ситуация совершенно не кажется вам неприятной','ситуация немного волнует, беспокоит вас',
                         'ситуация достаточно неприятна и вызывает такое беспокойство, что вы предпочли бы избежать её',
                         'ситуация очень неприятна и вызывает сильное беспокойство, тревогу, страх',
                         'ситуация для вас крайне неприятна, если вы не можете перенести её и она вызывает у вас очень сильное беспокойство, очень сильный страх'}

    # Словарь с проверочными данными
    dct_check_table = {'ШТК':[{'Отвечать у доски':set_variants_shtk},{'Пойти в дом к незнакомым людям':set_variants_shtk},
                              {'Участвовать в соревнованиях, конкурсах, в олимпиадах':set_variants_shtk},{'Разговаривать с директором техникума, колледжа':set_variants_shtk},
                              {'Думать о своем будущем':set_variants_shtk},{'Преподаватель смотрит по журналу, кого бы спросить':set_variants_shtk},
                              {'Тебя критикуют, в чем- то обвиняют':set_variants_shtk},{'На тебя смотрят, когда ты что-нибудь делаешь (наблюдают за тобой во время работы, решения задачи)':set_variants_shtk},
                              {'Пишешь контрольную работу':set_variants_shtk},{'После контрольной учитель называет отметки':set_variants_shtk},
                              {'На тебя не обращают внимания':set_variants_shtk},{'У тебя что-то не получается':set_variants_shtk},
                              {'Ждешь родителей с родительского собрания':set_variants_shtk},{'Тебе грозит неуспех, провал':set_variants_shtk},
                              {'Слышишь за своей спиной смех':set_variants_shtk},{'Сдаешь экзамены в техникуме, колледже':set_variants_shtk},
                              {'На тебя сердятся (непонятно почему)':set_variants_shtk},{'Выступать перед большой аудиторией':set_variants_shtk},
                              {'Предстоит важное, решающее дело':set_variants_shtk},{'Не понимаешь объяснений преподавателя':set_variants_shtk},
                              {'С тобой не согласны, противоречат тебе':set_variants_shtk},{'Сравниваешь себя с другими':set_variants_shtk},
                              {'Проверяют твои способности':set_variants_shtk},{'На тебя смотрят как на маленького':set_variants_shtk},
                              {'На уроке преподаватель неожиданно задает тебе вопрос':set_variants_shtk},{'Замолчали, когда ты подошел':set_variants_shtk},
                              {'Оценивается твоя работа': set_variants_shtk}, {'Думаешь о своих делах': set_variants_shtk},
                              {'Тебе надо принять для себя решение': set_variants_shtk}, {'Не можешь справиться с домашним заданием': set_variants_shtk},
                              ]}

    # Проверяем колонки в файле с данными

































if __name__ == '__main__':
    main_params_spo = 'data/параметры для СПО.xlsx'
    main_spo_data = 'data/data.xlsx'
    main_end_folder = 'data/Результат'
    main_quantity_descr_cols = 2

    generate_result_spo(main_params_spo,main_spo_data,main_end_folder,main_quantity_descr_cols)

    print('Lindy Booth')