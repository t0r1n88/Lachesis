"""
Функция для обработки результатов социометрического исследования
"""
import pandas as pd
pd.options.mode.chained_assignment = None
import openpyxl
import numpy as np
import time
import copy
import re
import warnings
warnings.filterwarnings('ignore', category=UserWarning, module='openpyxl')
warnings.simplefilter(action='ignore', category=DeprecationWarning)
warnings.simplefilter(action='ignore', category=UserWarning)



class NotReqColumn(Exception):
    """
    Исключение для обработки случая когда нет обязательной колонки ФИО
    """
    pass

class BadQuantNegCols(Exception):
    """
    Исключение для обработки случая когда указан номер колонки с негативным вопросом большем чем есть вопросов в файле
    """
    pass





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
    if isinstance(value_str,str):
        lst_value = value_str.split(';')
        if lst_value != ['']:
            for value in lst_value:
                dct[fio][value] += 1


def calc_itog(row:pd.Series):
    """
    Функция для подсчета итоговой суммы в колонке Итого
    :param row: строка
    :return: значение
    """
    lst_value = row.tolist() # превращаем в список
    return sum([value for value in lst_value if isinstance(value,int)])


def calc_quantity_change(value):
    """
    Функция для подсчета количества выборов
    :param value: строка вида Значение1;Значение2
    """
    if isinstance(value,str):
        lst_value = value.split(';')
        if lst_value != ['']:
            return len(lst_value)
        else:
            return 0
    else:
        return 0


def check_negative_cols(quant_questions:int, negative_str:str):
    """
    Функция для проверки наличия колонок с негативными вопросами
    :param quant_questions: количество вопросов
    :param negative_str: строка с перечислением колонок или пустая
    :return: список или пустой список
    """
    result = re.findall(r'\d+', negative_str)
    out_lst = [] # список для хранения номеров колонок с негативными вопросами
    if result:
        for value in result:
            value_digit = int(value)
            if value_digit > quant_questions:
                raise BadQuantNegCols
            if value_digit == 0: # на случай если записан ноль
                out_lst.append(1)
            else:
                out_lst.append(value_digit-1)
        return out_lst
    else:
        return []






def generate_result_sociometry(data_file:str,quantity_descr_cols:int,negative_questions:str,end_folder:str):
    """
    Функция для генерации результатов социометрического исследования
    :param data_file: файл с данными из форм
    :param quantity_descr_cols: количество анкетных колонок
    :param negative_questions: строка с порядковыми номерам негативных вопросов
    :param end_folder: конечная папка
    """

    t = time.localtime()
    current_time = time.strftime('%H_%M_%S', t)
    checked_dct = dict()  # словарь для хранения проверочных датафреймов по каждому вопросу
    matrix_dct = dict()  # словарь для хранения матриц датафреймов по каждому вопросу
    lst_value_dct = [] # список для хранения словарей по каждому вопросу


    base_df = pd.read_excel(data_file,dtype=str) # исходный датафрейм
    # Проверяем наличие колонки ФИО
    diff_req_cols = {'ФИО'}.difference(set(base_df.columns))
    if len(diff_req_cols) != 0:
        raise NotReqColumn

    base_df = base_df[base_df['ФИО'].notna()] # удаляем незаполенные строки в колонке ФИО
    # очищаем от лишних пробелов в начале и конце
    base_df = base_df.applymap(lambda x:x.strip() if isinstance(x,str) else x)
    # Создаем файл с дубликатами
    dupl_df = base_df[base_df['ФИО'].duplicated(keep=False)]  # получаем дубликаты
    dupl_df.insert(0, '№ строки дубликата ', list(map(lambda x: x + 2, list(dupl_df.index))))
    dupl_df.replace(np.nan, None, inplace=True)  # для того чтобы в пустых ячейках ничего не отображалось

    dupl_df.to_excel(f'{end_folder}/Дубликаты {current_time}.xlsx',index=False)



    base_df.drop_duplicates(subset='ФИО',inplace=True) # удаляем дубликаты
    base_df.sort_values(by='ФИО',inplace=True) # сортируем по алфавиту
    # Создаем шаблон социоматрицы
    template_matrix_df = pd.DataFrame(index=base_df['ФИО'].tolist(),columns=base_df['ФИО'].tolist())

    lst_fio = base_df['ФИО'].tolist() # делаем список ФИО


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

    # проверяем и обрабатываем строку с колонками по которым нужно делать свод
    lst_negative_cols = check_negative_cols(len(lst_questions), negative_questions)
    lst_negative_cols.sort() # сортируем чтобы потом все шло по порядку

    ind_templ_dct = {f'Вопрос_{number}':0 for number in range(1,len(lst_questions)+1)}
    # В зависимости от того есть ли колонки с негативными ответами
    if len(lst_negative_cols) == 0:
        index_dct = {'Индекс групповой сплоченности':copy.deepcopy(ind_templ_dct),
                     'Индекс референтности группы':copy.deepcopy(ind_templ_dct)} # словарь для хранения групповых индексов
    elif len(lst_negative_cols) == len(lst_questions):
        index_dct = {'Индекс групповой конфликтности': copy.deepcopy(ind_templ_dct),
                     'Индекс референтности группы': copy.deepcopy(ind_templ_dct)
                     }  # словарь для хранения групповых индексов
    else:
        index_dct = {'Индекс групповой сплоченности':copy.deepcopy(ind_templ_dct),
                     'Индекс групповой конфликтности': copy.deepcopy(ind_templ_dct),
                     'Индекс референтности группы':copy.deepcopy(ind_templ_dct)} # словарь для хранения групповых индексов


    for idx, name_question in enumerate(lst_questions,1):
        lst_columns_question = [col for col in df.columns if name_question in col] # список для хранения всех подвопросов
        descr_df[f'Вопрос_{idx}'] = df[lst_columns_question].apply(extract_answer_several_option, axis=1)

        # Создаем датафрейм для обработки отдельного вопроса
        one_qustion_df = base_df.iloc[:,:quantity_descr_cols]
        one_qustion_df[f'Вопрос_{idx}'] = descr_df[f'Вопрос_{idx}']
        # Добавляем колонку с количеством выборов
        one_qustion_df['Количество_выборов'] = one_qustion_df[f'Вопрос_{idx}'].apply(calc_quantity_change)
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

        # Обрабатываем в зависимости от количества негативных вопросов
        if len(lst_negative_cols) == 0:
            one_matrix_df.loc['Получено выборов'] = sum_row
            one_matrix_df.loc['Получено взаимных выборов'] = change_row
            # Добавляем колонку с социометрическим индексом
            lst_soc_index = list(sum_row)
            lst_soc_index = list(map(lambda x:round(x/(len(base_df)-1),2),lst_soc_index))
            lst_soc_index.extend([None,None])
            one_matrix_df['Индекс социометрического статуса'] = lst_soc_index
            one_matrix_df['Индекс эмоциональной экспансивности'] = one_matrix_df[lst_fio].sum(axis=1) / (len(base_df) - 1)
            one_matrix_df['Коэффициент удовлетворенности'] = one_matrix_df[lst_fio].sum(axis=1)
            tmp_change_row = list(change_row) # делаем список для развертывания
            tmp_change_row.extend([None,None])
            one_matrix_df['DPf'] = tmp_change_row
            one_matrix_df['Коэффициент удовлетворенности'] = round(one_matrix_df['DPf'] / one_matrix_df['Коэффициент удовлетворенности'],2)
            one_matrix_df.drop(columns=['DPf'],inplace=True)

            one_matrix_df.loc['Получено выборов','Индекс эмоциональной экспансивности'] = None
            one_matrix_df.loc['Получено взаимных выборов','Индекс эмоциональной экспансивности'] = None
            one_matrix_df.loc['Получено взаимных выборов','Коэффициент удовлетворенности'] = None

        elif len(lst_negative_cols) == len(lst_questions):
            one_matrix_df.loc['Получено выборов'] = sum_row
            one_matrix_df.loc['Получено взаимных выборов'] = change_row

            # Добавляем колонку с социометрическим индексом
            lst_soc_index = list(sum_row)
            lst_soc_index = list(map(lambda x:round(x/(len(base_df)-1),2),lst_soc_index))
            lst_soc_index.extend([None,None])
            one_matrix_df['Индекс социометрического статуса'] = lst_soc_index
            one_matrix_df['Индекс эмоциональной экспансивности'] = one_matrix_df[lst_fio].sum(axis=1) / (len(base_df) - 1)
            one_matrix_df['Коэффициент удовлетворенности'] = one_matrix_df[lst_fio].sum(axis=1)
            tmp_change_row = list(change_row) # делаем список для развертывания
            tmp_change_row.extend([None,None])
            one_matrix_df['DPf'] = tmp_change_row
            one_matrix_df['Коэффициент удовлетворенности'] = round(one_matrix_df['DPf'] / one_matrix_df['Коэффициент удовлетворенности'],2)
            one_matrix_df.drop(columns=['DPf'],inplace=True)

            one_matrix_df.loc['Получено выборов','Индекс эмоциональной экспансивности'] = None
            one_matrix_df.loc['Получено взаимных выборов','Индекс эмоциональной экспансивности'] = None
            one_matrix_df.loc['Получено взаимных выборов','Коэффициент удовлетворенности'] = None
        else:
            one_matrix_df.loc['Получено выборов'] = sum_row
            one_matrix_df.loc['Получено взаимных выборов'] = change_row
            # Добавляем колонку с социометрическим индексом
            lst_soc_index = list(sum_row)
            lst_soc_index = list(map(lambda x:round(x/(len(base_df)-1),2),lst_soc_index))
            lst_soc_index.extend([None,None])
            one_matrix_df['Индекс социометрического статуса'] = lst_soc_index
            one_matrix_df['Индекс эмоциональной экспансивности'] = one_matrix_df[lst_fio].sum(axis=1) / (len(base_df) - 1)
            one_matrix_df['Коэффициент удовлетворенности'] = one_matrix_df[lst_fio].sum(axis=1)
            tmp_change_row = list(change_row) # делаем список для развертывания
            tmp_change_row.extend([None,None])
            one_matrix_df['DPf'] = tmp_change_row
            one_matrix_df['Коэффициент удовлетворенности'] = round(one_matrix_df['DPf'] / one_matrix_df['Коэффициент удовлетворенности'],2)
            one_matrix_df.drop(columns=['DPf'],inplace=True)

            one_matrix_df.loc['Получено выборов','Индекс эмоциональной экспансивности'] = None
            one_matrix_df.loc['Получено взаимных выборов','Индекс эмоциональной экспансивности'] = None
            one_matrix_df.loc['Получено взаимных выборов','Коэффициент удовлетворенности'] = None




        matrix_dct[idx] = one_matrix_df # добавляем в словарь для сохранения

        if len(lst_negative_cols) == 0:
            # Считаем индексы
            max_sum_mutual_change = (len(base_df)* (len(base_df)-1)) / 2 # максимально возможное число взаимных выборов
            cn_index = sum(change_row) / max_sum_mutual_change # Индекс групповой сплоченности
            index_dct['Индекс групповой сплоченности'][f'Вопрос_{idx}'] = round(cn_index,2)
            if sum(sum_row) !=0:
                index_dct['Индекс референтности группы'][f'Вопрос_{idx}'] = round(sum(change_row) / sum(sum_row),2)
            else:
                index_dct['Индекс референтности группы'][f'Вопрос_{idx}'] = 0
        elif len(lst_negative_cols) == len(lst_questions):
            # Считаем индексы
            max_sum_mutual_change = (len(base_df)* (len(base_df)-1)) / 2 # максимально возможное число взаимных выборов
            conf_index = sum(change_row) / max_sum_mutual_change # Индекс групповой конфликтности
            index_dct['Индекс групповой конфликтности'][f'Вопрос_{idx}'] = round(conf_index,2)
            if sum(sum_row) !=0:
                index_dct['Индекс референтности группы'][f'Вопрос_{idx}'] = round(sum(change_row) / sum(sum_row),2)
            else:
                index_dct['Индекс референтности группы'][f'Вопрос_{idx}'] = 0
        else:
            if idx-1 in lst_negative_cols:
                # Считаем индексы
                max_sum_mutual_change = (len(base_df) * (len(base_df) - 1)) / 2  # максимально возможное число взаимных выборов
                conf_index = sum(change_row) / max_sum_mutual_change  # Индекс групповой конфликтности
                index_dct['Индекс групповой сплоченности'][f'Вопрос_{idx}'] = None
                index_dct['Индекс групповой конфликтности'][f'Вопрос_{idx}'] = round(conf_index, 2)
                if sum(sum_row) != 0:
                    index_dct['Индекс референтности группы'][f'Вопрос_{idx}'] = round(sum(change_row) / sum(sum_row), 2)
                else:
                    index_dct['Индекс референтности группы'][f'Вопрос_{idx}'] = 0
            else:
                # Считаем индексы
                max_sum_mutual_change = (len(base_df) * (len(base_df) - 1)) / 2  # максимально возможное число взаимных выборов
                cn_index = sum(change_row) / max_sum_mutual_change  # Индекс групповой сплоченности
                index_dct['Индекс групповой сплоченности'][f'Вопрос_{idx}'] = round(cn_index, 2)
                index_dct['Индекс групповой конфликтности'][f'Вопрос_{idx}'] = None
                if sum(sum_row) != 0:
                    index_dct['Индекс референтности группы'][f'Вопрос_{idx}'] = round(sum(change_row) / sum(sum_row), 2)
                else:
                    index_dct['Индекс референтности группы'][f'Вопрос_{idx}'] = 0


    # Суммируем словари с ответами на отдельные вопросы для получения общего словаря
    for dct in lst_value_dct:
        for fio, value_dct in dct.items():
            for subfio,value in value_dct.items():
                result_dct[fio][subfio] +=value


    # Суммируем и сохраняем общую социоматрицу
    lst_matrix = [df for df in matrix_dct.values()]
    union_df = sum(lst_matrix)
    # Заполняем крестиками пересечения одинаковых ФИО
    for fio in lst_fio:
        union_df.loc[fio,fio] = 'X'


    if 0 < len(lst_negative_cols) < len(lst_questions):
        # Добавляем строки с суммами по отдельным негативным и позитивным выборам
        lst_positive_questions = []  # список для суммирующих строк выборов из позитивных вопросов
        lst_negative_questions = []  # список для суммирующих строк выборов из негативных вопросов

        lst_change_positive_questions = []  # список для суммирующих строк взаимных выборов из позитивных вопросов
        lst_change_negative_questions = []  # список для суммирующих строк взаимных выборов из негативных вопросов
        for idx,one_matrix_df in enumerate(lst_matrix,1):
            if idx-1 not in lst_negative_cols:
                lst_positive_questions.append(one_matrix_df.loc['Получено выборов',lst_fio])
                lst_change_positive_questions.append(one_matrix_df.loc['Получено взаимных выборов', lst_fio])
            else:
                lst_negative_questions.append(one_matrix_df.loc['Получено выборов',lst_fio])
                lst_change_negative_questions.append(one_matrix_df.loc['Получено взаимных выборов', lst_fio])

        union_df.loc['Получено положительных выборов'] = sum(lst_positive_questions)
        union_df.loc['Получено негативных выборов'] = sum(lst_negative_questions)

        union_df.loc['Получено взаимных положительных выборов'] = sum(lst_change_positive_questions)
        union_df.loc['Получено взаимных негативных выборов'] = sum(lst_change_negative_questions)

        lst_for_index = lst_fio.copy()
        lst_for_index.extend(['Получено выборов','Получено положительных выборов','Получено негативных выборов',
                              'Получено взаимных выборов','Получено взаимных положительных выборов','Получено взаимных негативных выборов'])
        union_df = union_df.reindex(lst_for_index)



        lst_pos_cols = []  # список для суммирующих строк выборов из позитивных вопросов
        lst_neg_cols = []  # список для суммирующих строк выборов из негативных вопросов

        # Добавляем колонки с подсчетом положительных и отрицательных
        for idx,one_matrix_df in enumerate(lst_matrix,1):
            if idx-1 not in lst_negative_cols:
                lst_pos_cols.append(one_matrix_df[lst_fio].sum(axis=1))
            else:
                lst_neg_cols.append(one_matrix_df[lst_fio].sum(axis=1))


        union_df['+ выборов'] = sum(lst_pos_cols)
        union_df['- выборов'] = sum(lst_neg_cols)

        lst_change_cols = list(range(1, len(lst_fio) + 1))  # цифры для названий колонок
        lst_change_cols.extend(['+ выборов', '- выборов'])
        union_df.drop(columns=['Индекс социометрического статуса', 'Индекс эмоциональной экспансивности','Коэффициент удовлетворенности'], inplace=True)

        union_df.columns = lst_change_cols
        # Подсчитываем колонку Итого
        union_df['Сделано выборов'] = union_df.apply(calc_itog, axis=1)

        # Добавляем подсчет общего экспансивного индекса
        union_df['+ИЭЭ'] = union_df['+ выборов'] / (len(lst_fio) - 1)
        union_df['-ИЭЭ'] = union_df['- выборов'] / (len(lst_fio) - 1)
        union_df['Общий ИЭЭ'] = union_df['Сделано выборов'] / (len(lst_fio) - 1)
        lst_union_aa = union_df['Общий ИЭЭ'].tolist()[:len(lst_fio)+1] # делаем список чтобы потом заменить значения для выборов
        lst_union_aa.extend([None,None,None,None,None])
        union_df['Общий ИЭЭ'] = lst_union_aa

        # Убираем показатели для строк с количеством выборов
        union_df.loc['Получено выборов','+ИЭЭ'] = None
        union_df.loc['Получено выборов','-ИЭЭ'] = None
        union_df.loc['Получено выборов','Общий ИЭЭ'] = None
        union_df.loc['Получено взаимных выборов','+ИЭЭ'] = None
        union_df.loc['Получено взаимных выборов','-ИЭЭ'] = None
        union_df.loc['Получено взаимных выборов','Общий ИЭЭ'] = None



        # Добавляем колонки с социометрическим индексом
        for idx, one_df in enumerate(lst_matrix, 1):
            if idx - 1 in lst_negative_cols:
                union_df[f'-ИСС Вопрос {idx}'] = one_df['Индекс социометрического статуса']
            else:
                union_df[f'+ИСС Вопрос {idx}'] = one_df['Индекс социометрического статуса']

        # Добавляем колонки с индексом эмоциональной экспансивности
        for idx, one_df in enumerate(lst_matrix, 1):
            if idx - 1 in lst_negative_cols:
                union_df[f'-ИЭЭ Вопрос {idx}'] = one_df['Индекс эмоциональной экспансивности']
            else:
                union_df[f'+ИЭЭ Вопрос {idx}'] = one_df['Индекс эмоциональной экспансивности']

        # Добавляем колонки с коэфициентом эмоциональной удовлетворенности
        for idx, one_df in enumerate(lst_matrix, 1):
            if idx - 1 in lst_negative_cols:
                union_df[f'-КУ Вопрос {idx}'] = one_df['Коэффициент удовлетворенности']
            else:
                union_df[f'+КУ Вопрос {idx}'] = one_df['Коэффициент удовлетворенности']

        # Создаем список (не матрицу) со всей статистикой
        stat_df = pd.DataFrame(index=lst_fio)
        stat_df['Сделано выборов'] = union_df.loc[lst_fio,'Сделано выборов']
        stat_df['Сделано + выборов'] = union_df.loc[lst_fio,'+ выборов']
        stat_df['Сделано - выборов'] = union_df.loc[lst_fio,'- выборов']

        stat_df['Получено выборов'] = list(union_df.loc['Получено выборов',list(range(1,len(lst_fio)+1))])
        stat_df['Получено + выборов'] = list(union_df.loc['Получено положительных выборов',list(range(1,len(lst_fio)+1))])
        stat_df['Получено - выборов'] = list(union_df.loc['Получено негативных выборов',list(range(1,len(lst_fio)+1))])

        stat_df['Получено взаимных выборов'] = list(union_df.loc['Получено взаимных выборов',list(range(1,len(lst_fio)+1))])
        stat_df['Получено взаимных + выборов'] = list(union_df.loc['Получено взаимных положительных выборов',list(range(1,len(lst_fio)+1))])
        stat_df['Получено взаимных - выборов'] = list(union_df.loc['Получено взаимных негативных выборов',list(range(1,len(lst_fio)+1))])

        stat_df['+ИЭЭ'] = union_df['+ИЭЭ']
        stat_df['-ИЭЭ'] = union_df['-ИЭЭ']

        stat_df.index.name = 'ФИО'
        union_df.index.name = 'ФИО'
        stat_df = pd.merge(stat_df,union_df.loc[lst_fio,'Общий ИЭЭ':],how='inner',left_index=True,right_index=True)

        stat_df.loc['Итого'] = 0 # добавляем строку для сумм выборов
        stat_df.loc['Итого','Сделано выборов'] = sum(stat_df['Сделано выборов'])
        stat_df.loc['Итого','Сделано + выборов'] = sum(stat_df['Сделано + выборов'])
        stat_df.loc['Итого','Сделано - выборов'] = sum(stat_df['Сделано - выборов'])

        stat_df.loc['Итого','Получено выборов'] = sum(stat_df['Получено выборов'])
        stat_df.loc['Итого','Получено + выборов'] = sum(stat_df['Получено + выборов'])
        stat_df.loc['Итого','Получено - выборов'] = sum(stat_df['Получено - выборов'])

        stat_df.loc['Итого','Получено взаимных выборов'] = sum(stat_df['Получено взаимных выборов'])
        stat_df.loc['Итого','Получено взаимных + выборов'] = sum(stat_df['Получено взаимных + выборов'])
        stat_df.loc['Итого','Получено взаимных - выборов'] = sum(stat_df['Получено взаимных - выборов'])

        for name_column in stat_df.columns[9:]:
            stat_df.loc['Итого',name_column] = None




    else:
        union_df.drop(columns=['Индекс социометрического статуса','Индекс эмоциональной экспансивности','Коэффициент удовлетворенности'], inplace=True)

        union_df.columns = range(1, len(lst_fio) +1)
        # Подсчитываем колонку Итого
        union_df['Сделано выборов'] = union_df.apply(calc_itog,axis=1)

        union_df['Общий ИЭЭ'] = union_df['Сделано выборов'] / (len(lst_fio) - 1)
        lst_union_aa = union_df['Общий ИЭЭ'].tolist()[:len(lst_fio)+1] # делаем список чтобы потом заменить значения для выборов
        lst_union_aa.extend([None])
        union_df['Общий ИЭЭ'] = lst_union_aa
        union_df.loc['Получено выборов','Общий ИЭЭ'] = None


        # Добавляем колонки с социометрическим индексом
        for idx,one_df in enumerate(lst_matrix,1):
            if idx-1 in lst_negative_cols:
                union_df[f'-ИСС Вопрос {idx}'] = one_df['Индекс социометрического статуса']
            else:
                union_df[f'+ИСС Вопрос {idx}'] = one_df['Индекс социометрического статуса']
        # Добавляем колонки с индексом эмоциональной экспансивности
        for idx, one_df in enumerate(lst_matrix, 1):
            if idx - 1 in lst_negative_cols:
                union_df[f'-ИЭЭ Вопрос {idx}'] = one_df['Индекс эмоциональной экспансивности']
            else:
                union_df[f'+ИЭЭ Вопрос {idx}'] = one_df['Индекс эмоциональной экспансивности']
        # Добавляем колонки с коэфициентом эмоциональной удовлетворенности
        for idx, one_df in enumerate(lst_matrix, 1):
            if idx - 1 in lst_negative_cols:
                union_df[f'-КУ Вопрос {idx}'] = one_df['Коэффициент удовлетворенности']
            else:
                union_df[f'+КУ Вопрос {idx}'] = one_df['Коэффициент удовлетворенности']


        # Создаем список (не матрицу) со всей статистикой
        stat_df = pd.DataFrame(index=lst_fio)
        stat_df['Сделано выборов'] = union_df.loc[lst_fio,'Сделано выборов']
        stat_df['Получено выборов'] = list(union_df.loc['Получено выборов',list(range(1,len(lst_fio)+1))])
        stat_df['Взаимных выборов'] = list(union_df.loc['Получено взаимных выборов',list(range(1,len(lst_fio)+1))])
        stat_df.index.name = 'ФИО'
        union_df.index.name = 'ФИО'
        stat_df = pd.merge(stat_df,union_df.loc[lst_fio,'Общий ИЭЭ':],how='inner',left_index=True,right_index=True)

        stat_df.loc['Итого'] = 0 # добавляем строку для сумм выборов
        stat_df.loc['Итого','Сделано выборов'] = sum(stat_df['Сделано выборов'])
        stat_df.loc['Итого','Получено выборов'] = sum(stat_df['Получено выборов'])
        stat_df.loc['Итого','Взаимных выборов'] = sum(stat_df['Взаимных выборов'])

        for name_column in stat_df.columns[3:]:
            stat_df.loc['Итого',name_column] = None






    # Создаем индекс с добавлением цифр
    lst_index_union = [] # список для хранения индекса с добавлением цифр
    for idx,value in enumerate(union_df.index,1):
        if value in  lst_fio:
            lst_index_union.append(f'{idx}. {value}')
        else:
            lst_index_union.append(value)

    union_df.index = lst_index_union
    union_df.to_excel(f'{end_folder}/Общая социоматрица {current_time}.xlsx',index=True)


    stat_df.to_excel(f'{end_folder}/Списочная статистика {current_time}.xlsx',index=True)


    index_df = pd.DataFrame.from_dict(index_dct, orient='index')
    index_df.to_excel(f'{end_folder}/Индексы {current_time}.xlsx',index=True)

    with pd.ExcelWriter(f'{end_folder}/Для проверки {current_time}.xlsx', engine='xlsxwriter') as writer:
        for name_sheet,out_df in checked_dct.items():
            out_df.to_excel(writer,sheet_name=str(name_sheet),index=False)

    with pd.ExcelWriter(f'{end_folder}/Социоматрицы отдельные {current_time}.xlsx', engine='xlsxwriter') as writer:
        for name_sheet,out_df in matrix_dct.items():
            # Заполняем крестиками пересечения одинаковых ФИО
            for fio in lst_fio:
                out_df.loc[fio, fio] = 'X'
            # Создаем индекс с добавлением цифр
            temp_lst_index_union = []  # список для хранения индекса с добавлением цифр
            for idx, value in enumerate(out_df.index, 1):
                if value in lst_fio:
                    temp_lst_index_union.append(f'{idx}. {value}')
                else:
                    temp_lst_index_union.append(value)
            out_df.index = temp_lst_index_union


            # Создаем колонки с добавлением цифр
            lst_one_cols  = list(range(1,len(lst_fio)+1)) # цифры для названий колонок
            lst_one_cols.extend(['Индекс социометрического статуса', 'Индекс эмоциональной экспансивности','Коэффициент удовлетворенности'])
            out_df.columns = lst_one_cols

            # Подсчитываем колонку Итого
            out_df['Сделано выборов'] = out_df.apply(calc_itog, axis=1)

            out_df.to_excel(writer,sheet_name=str(name_sheet),index=True)




















if __name__ == '__main__':
    main_file = 'data/Социометрия.xlsx'
    main_file = 'data/Социометрия негатив.xlsx'
    main_quantity_descr_cols = 1
    main_negative_questions = '2'
    main_end_folder = 'data/Результат'
    generate_result_sociometry(main_file,main_quantity_descr_cols,main_negative_questions,main_end_folder)
    print('Lindy Booth')
