"""
Функция для обработки результатов социометрического исследования
"""
import pandas as pd
import openpyxl
from collections import Counter
import time


def extract_answer_several_option(row:pd.Series):
    """
    Функция для извлечения ответов из колонок
    :param row:строка датафрейма с определенными колонками
    :return: строка значений разделенных точкой с запятой
    """
    temp_lst = row.tolist() # делаем список
    temp_lst = [value for value in temp_lst if pd.notna(value)] # отбрасываем незаполненное
    return ';'.join(temp_lst)


def count_value_in_column(df:pd.DataFrame,name_column:str):
    """
    Функция для подсчета сколько раз то или иное значение встречается в колонке
    :param col: серия
    :return: датафрейм
    """
    lst_count = []  # список для хранения значений которые были разделены точкой с запятой
    df[name_column] = df[name_column].astype(str)
    tmp_lst = df[name_column].tolist()
    for value_str in tmp_lst:
        lst_count.extend(value_str.split(';'))

    # Делаем частотную таблицу и сохраняем в словарь
    counts_df = pd.DataFrame.from_dict(dict(Counter(lst_count)), orient='index')
    counts_df = counts_df.reset_index()
    counts_df.columns = [name_column, 'Количество']
    counts_df.sort_values(by='Количество', ascending=False, inplace=True)

    counts_df['Доля в % от общего'] = round(
        counts_df[f'Количество'] / counts_df['Количество'].sum(), 2) * 100

    counts_df.loc['Итого'] = counts_df.sum(numeric_only=True)



    return counts_df




def generate_result_sociometry(data_file:str,quantity_descr_cols:int,end_folder:str):
    """
    Функция для генерации результатов социометрического исследования
    :param data_file: файл с данными из форм
    :param quantity_descr_cols: количество анкетных колонок
    :param end_folder: конечная папка
    """
    t = time.localtime()
    current_time = time.strftime('%H_%M_%S', t)
    dct_df = dict()  # словарь для хранения листовых датафреймов
    check_set_answer = set()  # множество для проверки есть ли такой вопрос или нет

    count_question = 1 # счетчик вопросов

    base_df = pd.read_excel(data_file,dtype=str) # исходный датафрейм
    # очищаем от лишних пробелов в начале и конце
    base_df = base_df.applymap(lambda x:x.strip() if isinstance(x,str) else x)

    descr_df = base_df.iloc[:,:quantity_descr_cols] # датафрейм с анкетными данными
    df = base_df.iloc[:,quantity_descr_cols:] # датафрейм с ответами
    lst_questions = [] # список для хранения самих вопросов
    # Находим все уникальные вопросы
    for name_column in df.columns:
        lst_answer = name_column.split(' / ')
        question = lst_answer[0]  # Вопрос
        if question not in lst_questions:
            lst_questions.append(question)

    for idx, name_question in enumerate(lst_questions,1):
        lst_columns_question = [col for col in df.columns if name_question in col] # список для хранения всех подвопросов
        descr_df[f'Вопрос_{idx}'] = df[lst_columns_question].apply(extract_answer_several_option, axis=1)

    descr_df.to_excel('data/dfd.xlsx',index=False)





    # for idx, name_column in enumerate(df.columns):
    #     lst_union_name_column = [name_column]  # список для хранения названий колонок относящихся к одному вопросу
    #
    #     # получаем последующую колонку
    #     if idx +1 == len(df.columns):
    #         # проверяем достижение предела
    #         cont_name_column = idx
    #     else:
    #         cont_name_column = idx+1
    #
    #     lst_answer = name_column.split(' / ')
    #     question = lst_answer[0]  # Вопрос
    #     if question not in check_set_answer: # если вопроса еще не было
    #         threshold = len(df.columns[cont_name_column:])  # сколько колонок осталось до конца датафрейма
    #         print(threshold)
    #         for temp_idx, temp_name_column in enumerate(df.columns[cont_name_column:]):
    #             temp_lst_question = temp_name_column.split(' / ')  # сплитим каждую последующую колонку пока вопрос равен предыдущему
    #             temp_question = temp_lst_question[0]  # вопрос в следующей колонке
    #             if question == temp_question:
    #                 lst_union_name_column.append(temp_name_column)  # добавляем название
    #                 if temp_idx + 1 == threshold:
    #                     break
    #             else:
    #                 check_set_answer.add(question)
    #                 print(len((lst_union_name_column)))
    #                 print(lst_union_name_column)
    #
    #                 count_question += 1
    #     else:
    #         continue
    #





















if __name__ == '__main__':
    main_file = 'data/Социометрия.xlsx'
    main_quantity_descr_cols = 2
    main_end_folder = 'data/Результат'
    generate_result_sociometry(main_file,main_quantity_descr_cols,main_end_folder)
    print('Lindy Booth')
