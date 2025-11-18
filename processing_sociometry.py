"""
Функция для обработки результатов социометрического исследования
"""
import pandas as pd
import openpyxl
from collections import Counter
import time
import copy

def extract_answer_several_option(row:pd.Series):
    """
    Функция для извлечения ответов из колонок
    :param row:строка датафрейма с определенными колонками
    :return: строка значений разделенных точкой с запятой
    """
    temp_lst = row.tolist() # делаем список
    temp_lst = [value for value in temp_lst if pd.notna(value)] # отбрасываем незаполненное
    return ';'.join(temp_lst)


def calc_anwers(row:pd.Series, dct:dict):
    """
    Функция для извлечения данных из строки формата Значение1;Значение2 в словарь
    :param row: колонка ФИО и колонка с ответами
    :param dct: словарь котороый нужно заполнить
    :return: словарь
    """
    fio, value_str = row.tolist()
    lst_value = value_str.split(';')
    for value in lst_value:
        dct[fio][value] += 1










def generate_result_sociometry(data_file:str,quantity_descr_cols:int,end_folder:str):
    """
    Функция для генерации результатов социометрического исследования
    :param data_file: файл с данными из форм
    :param quantity_descr_cols: количество анкетных колонок
    :param end_folder: конечная папка
    """
    t = time.localtime()
    current_time = time.strftime('%H_%M_%S', t)




    base_df = pd.read_excel(data_file,dtype=str) # исходный датафрейм
    # очищаем от лишних пробелов в начале и конце
    base_df = base_df.applymap(lambda x:x.strip() if isinstance(x,str) else x)
    base_df.drop_duplicates(subset='ФИО',inplace=True) # удаляем дубликаты
    base_df.sort_values(by='ФИО',inplace=True) # сортируем по алфавиту
    # Создаем шаблон социоматрицы
    template_matrix_df = pd.DataFrame(index=base_df['ФИО'].tolist(),columns=base_df['ФИО'].tolist())




    # создаем словарь где вида {ФИО:{ФИО:0}}
    template_dct = {}
    for fio in base_df['ФИО'].tolist():
        template_dct[fio] = {key:0 for key in base_df['ФИО'].tolist()}

    descr_df = base_df.iloc[:,:quantity_descr_cols] # датафрейм с анкетными данными в который будут записываться данные по всем вопросам
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

        # Создаем датафрейм для обработки отдельного вопроса
        one_qustion_df = base_df.iloc[:,:quantity_descr_cols]
        one_qustion_df[f'Вопрос_{idx}'] = descr_df[f'Вопрос_{idx}']
        # считаем отдельную колонку
        one_dct = copy.deepcopy(template_dct)
        one_qustion_df[['ФИО',f'Вопрос_{idx}']].apply(lambda x: calc_anwers(x,one_dct),axis=1)
        one_matrix_df = template_matrix_df.copy()
        for key,value_dct in one_dct.items():
            print(key)
            for subkey,value in value_dct.items():
                one_matrix_df.loc[key,subkey] = value

        one_matrix_df.to_excel('data/mat.xlsx')
        raise ZeroDivisionError
















if __name__ == '__main__':
    main_file = 'data/Социометрия.xlsx'
    main_quantity_descr_cols = 2
    main_end_folder = 'data/Результат'
    generate_result_sociometry(main_file,main_quantity_descr_cols,main_end_folder)
    print('Lindy Booth')
