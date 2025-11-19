"""
Функция для обработки результатов социометрического исследования
"""
import pandas as pd
import openpyxl
from collections import Counter
import time
import copy
from collections import defaultdict

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
    checked_dct = dict()  # словарь для хранения проверочных датафреймов по каждому вопросу
    matrix_dct = dict()  # словарь для хранения матриц датафреймов по каждому вопросу
    lst_value_dct = [] # список для хранения словарей по каждому вопросу




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

    result_dct = copy.deepcopy(template_dct) # словарь в котором будут слаживаться результаты по всем вопросам

    descr_df = base_df.iloc[:,:quantity_descr_cols] # датафрейм с анкетными данными в который будут записываться данные по всем вопросам
    df = base_df.iloc[:,quantity_descr_cols:] # датафрейм с ответами
    lst_questions = [] # список для хранения самих вопросов
    # Находим все уникальные вопросы
    for name_column in df.columns:
        lst_answer = name_column.split(' / ')
        question = lst_answer[0]  # Вопрос
        if question not in lst_questions:
            lst_questions.append(question)

    ind_templ_dct = {f'Вопрос_{number}':0 for number in range(1,len(lst_questions)+1)}
    index_dct = {'Индекс групповой сплоченности (Сn)':copy.deepcopy(ind_templ_dct)} # словарь для хранения групповых индексов


    for idx, name_question in enumerate(lst_questions,1):
        lst_columns_question = [col for col in df.columns if name_question in col] # список для хранения всех подвопросов
        descr_df[f'Вопрос_{idx}'] = df[lst_columns_question].apply(extract_answer_several_option, axis=1)

        # Создаем датафрейм для обработки отдельного вопроса
        one_qustion_df = base_df.iloc[:,:quantity_descr_cols]
        one_qustion_df[f'Вопрос_{idx}'] = descr_df[f'Вопрос_{idx}']
        checked_dct[idx] = one_qustion_df

        # считаем отдельную колонку
        one_dct = copy.deepcopy(template_dct)
        one_qustion_df[['ФИО',f'Вопрос_{idx}']].apply(lambda x: calc_anwers(x,one_dct),axis=1)
        lst_value_dct.append(one_dct) # добавляем в список
        # заполняем социоматрицу на отдельный вопрос
        one_matrix_df = template_matrix_df.copy()
        for key,value_dct in one_dct.items():
            for subkey,value in value_dct.items():
                one_matrix_df.loc[key,subkey] = value

        change_dct = {key:{} for key in one_dct.keys()}

        for fio,value_dct in one_dct.items():
            for subfio,value in value_dct.items():
                if fio != subfio:
                    if one_dct[subfio][fio] == 1 and value_dct[subfio] == 1:
                        change_dct[fio][subfio] = 1
                        change_dct[subfio][fio] = 1

        change_row = [len(value) for key,value in change_dct.items()]
        # считаем количество выборов
        sum_row = one_matrix_df.sum()
        one_matrix_df.loc['Кол-во выборов'] = sum_row
        one_matrix_df.loc['Кол-взаимных выборов'] = change_row

        matrix_dct[idx] = one_matrix_df # добавляем в словарь для сохранения

        # Считаем индексы
        max_sum_mutual_change = (len(base_df)* (len(base_df)-1)) / 2 # максимально возможное число взаимных выборов
        cn_index = sum(change_row) / max_sum_mutual_change # Индекс групповой сплоченности
        index_dct['Индекс групповой сплоченности (Сn)'][f'Вопрос_{idx}'] = cn_index





    with pd.ExcelWriter(f'{end_folder}/Для проверки {current_time}.xlsx', engine='xlsxwriter') as writer:
        for name_sheet,out_df in checked_dct.items():
            out_df.to_excel(writer,sheet_name=str(name_sheet),index=False)

    with pd.ExcelWriter(f'{end_folder}/Социоматрицы отдельные {current_time}.xlsx', engine='xlsxwriter') as writer:
        for name_sheet,out_df in matrix_dct.items():
            out_df.to_excel(writer,sheet_name=str(name_sheet),index=True)

    # Суммируем словари с ответами на отдельные вопросы для получения общего словаря
    for dct in lst_value_dct:
        for fio, value_dct in dct.items():
            for subfio,value in value_dct.items():
                result_dct[fio][subfio] +=value


    # Суммируем и сохраняем общую социоматрицу
    lst_matrix = [df for df in matrix_dct.values()]
    result = sum(lst_matrix)
    result.to_excel(f'{end_folder}/Общая социоматрица {current_time}.xlsx',index=True)

    index_df = pd.DataFrame.from_dict(index_dct, orient='index')
    index_df.to_excel(f'{end_folder}/Индексы {current_time}.xlsx',index=True)




















if __name__ == '__main__':
    main_file = 'data/Социометрия.xlsx'
    main_quantity_descr_cols = 2
    main_end_folder = 'data/Результат'
    generate_result_sociometry(main_file,main_quantity_descr_cols,main_end_folder)
    print('Lindy Booth')
