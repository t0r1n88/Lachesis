"""
Скрипт для обрабокти результатов теста профессиональный тип личности
"""
import pandas as pd
from tkinter import messagebox
from lachesis_support_functions import round_mean, sort_name_class
class BadValuePTL(Exception):
    """
    Исключение для неправильных значений в вариантах ответов
    """
    pass

class BadCountColumnsPTL(Exception):
    """
    Исключение для обработки случая если количество колонок не равно 30
    """
    pass


def calc_level_ptl(value):
    """
    Функция для подсчета уровня склонности к то или иной сфере
    """
    if value <= 4:
        return 'слабо выраженный тип'
    elif 5 <= value <= 7:
        return 'средне выраженный тип'
    elif 8 <= value <= 10:
        return 'ярко выраженный тип'


def calc_mean(df:pd.DataFrame,type_calc:str,lst_cat:list,val_cat):
    """
    Функция для создания сводных датафреймов

    :param df: датафрейм с данными
    :param type_calc:тип обработки Группа или Курс
    :param lst_cat:список колонок по которым будет формироваться свод
    :param val_cat:значение по которому будет формиваться свод
    :return:датафрейм
    """
    if type_calc == 'Группа':
        calc_mean_df = pd.pivot_table(df, index=lst_cat,
                                           values=[val_cat],
                                           aggfunc=round_mean)
        calc_mean_df.reset_index(inplace=True)
        calc_mean_df.rename(columns={val_cat: 'Среднее значение'}, inplace=True)

        return calc_mean_df
    else:
        calc_mean_df = pd.pivot_table(df, index=lst_cat,
                                           values=val_cat,
                                           aggfunc=round_mean)
        calc_mean_df.reset_index(inplace=True)
        calc_mean_df.rename(columns={val_cat:'Среднее значение'},inplace=True)
        return calc_mean_df



def calc_count_sphere_ptl(df:pd.DataFrame, type_calc:str, lst_cat:list, val_cat, col_cat):
    """
    Функция для создания сводных датафреймов

    :param df: датафрейм с данными
    :param type_calc:тип обработки Группа или Курс
    :param lst_cat:список колонок по которым будет формироваться свод
    :param val_cat:значение по которому будет формиваться свод
    :param col_cat: колонка по которой будет формироваться свод
    :return:датафрейм
    """
    if type_calc == 'Группа':
        count_df = pd.pivot_table(df, index=lst_cat,
                                                 columns=col_cat,
                                                 values=val_cat,
                                                 aggfunc='count', margins=True, margins_name='Итого')

        lst_sphere = count_df.columns[:-1]
        count_df.reset_index(inplace=True)

        for sphere in lst_sphere:
            count_df[f'% {sphere} от общего'] = round(
            count_df[f'{sphere}'] / count_df['Итого'], 2) * 100


        return count_df
    else:
        count_df = pd.pivot_table(df, index=lst_cat,
                                  columns=col_cat,
                                  values=val_cat,
                                  aggfunc='count', margins=True, margins_name='Итого')

        lst_sphere = count_df.columns[:-1]
        count_df.reset_index(inplace=True)

        for sphere in lst_sphere:
            count_df[f'% {sphere} от общего'] = round(
            count_df[f'{sphere}'] / count_df['Итого'], 2) * 100

        return count_df



def calc_count_level_ptl(df:pd.DataFrame, type_calc:str, lst_cat:list, val_cat, col_cat, lst_cols:list):
    """
    Функция для создания сводных датафреймов

    :param df: датафрейм с данными
    :param type_calc:тип обработки Группа или Курс
    :param lst_cat:список колонок по которым будет формироваться свод
    :param val_cat:значение по которому будет формиваться свод
    :param col_cat: колонка по которой будет формироваться свод
    :param lst_cols: список с колонками
    :return:датафрейм
    """
    if type_calc == 'Группа':
        count_df = pd.pivot_table(df, index=lst_cat,
                                                 columns=col_cat,
                                                 values=val_cat,
                                                 aggfunc='count', margins=True, margins_name='Итого')


        count_df.reset_index(inplace=True)
        count_df = count_df.reindex(columns=lst_cols)
        count_df['% слабо выраженный тип от общего'] = round(
            count_df['слабо выраженный тип'] / count_df['Итого'], 2) * 100
        count_df['% средне выраженный тип от общего'] = round(
            count_df['средне выраженный тип'] / count_df['Итого'], 2) * 100
        count_df['% ярко выраженный тип от общего'] = round(
            count_df['ярко выраженный тип'] / count_df['Итого'], 2) * 100

        return count_df
    else:
        count_df = pd.pivot_table(df, index=lst_cat,
                                  columns=col_cat,
                                  values=val_cat,
                                  aggfunc='count', margins=True, margins_name='Итого')

        count_df.reset_index(inplace=True)
        count_df = count_df.reindex(columns=lst_cols)
        count_df['% слабо выраженный тип от общего'] = round(
            count_df['слабо выраженный тип'] / count_df['Итого'], 2) * 100
        count_df['% средне выраженный тип от общего'] = round(
            count_df['средне выраженный тип'] / count_df['Итого'], 2) * 100
        count_df['% ярко выраженный тип от общего'] = round(
            count_df['ярко выраженный тип'] / count_df['Итого'], 2) * 100

        return count_df










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
            key,value = result.split(': ') # извлекаем ключ и значение
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
            key,value = result.split(': ') # извлекаем ключ и значение
            dct_result[key] = int(value)

    # возвращаем элемент с максимальным значением
    return dct_result[max(dct_result, key=dct_result.get)]


def processing_result_ptl(row):
    """
    Функция для подсчета результатов теста на определение профессионального типа личности
    :return:
    """
    # Создаем словарь для хранения данных
    dct_type = {'Реалистический': 0, 'Интеллектуальный': 0, 'Социальный': 0,
                'Офисный': 0,
                'Предпринимательский': 0,
                'Артистический': 0}
    dct_error = {}  # словарь для хранения ошибочных  значений, для того чтобы было легче находить ошибки при обновлении
    # 1
    if row[0] == 'Автомеханик':
        dct_type['Реалистический'] += 1
    elif row[0] == 'Физиотерапевт':
        dct_type['Социальный'] += 1
    else:
        dct_error[
            'Вопрос №1'] = f'Полученное значение-{row[0]} не совпадает с эталонными:[Автомеханик] или [Физиотерапевт]'

    # 2
    if row[1] == 'Специалист по защите информации':
        dct_type['Интеллектуальный'] += 1
    elif row[1] == 'Логистик':
        dct_type['Предпринимательский'] += 1
    else:
        dct_error[
            'Вопрос №2'] = f'Полученное значение-{row[1]} не совпадает с эталонными:[Специалист по защите информации] или [Логистик]'

    # 3
    if row[2] == 'Оператор связи':
        dct_type['Офисный'] += 1
    elif row[2] == 'Кинооператор':
        dct_type['Артистический'] += 1
    else:
        dct_error[
            'Вопрос №3'] = f'Полученное значение-{row[2]} не совпадает с эталонными:[Оператор связи] или [Кинооператор]'

    # 4
    if row[3] == 'Водитель':
        dct_type['Реалистический'] += 1
    elif row[3] == 'Продавец':
        dct_type['Социальный'] += 1
    else:
        dct_error['Вопрос №4'] = f'Полученное значение-{row[3]} не совпадает с эталонными:[Водитель] или [Продавец]'

    # 5
    if row[4] == 'Инженер-конструктор':
        dct_type['Интеллектуальный'] += 1
    elif row[4] == 'Менеджер по продажам':
        dct_type['Предпринимательский'] += 1
    else:
        dct_error[
            'Вопрос №5'] = f'Полученное значение-{row[4]} не совпадает с эталонными:[Инженер-конструктор] или [Менеджер по продажам]'

    # 6
    if row[5] == 'Диспетчер':
        dct_type['Офисный'] += 1
    elif row[5] == 'Дизайнер компьютерных программ':
        dct_type['Артистический'] += 1
    else:
        dct_error[
            'Вопрос №6'] = f'Полученное значение-{row[5]} не совпадает с эталонными:[Диспетчер] или [Дизайнер компьютерных программ]'

    # 7
    if row[6] == 'Ветеринар':
        dct_type['Реалистический'] += 1
    elif row[6] == 'Эколог':
        dct_type['Социальный'] += 1
    else:
        dct_error['Вопрос №7'] = f'Полученное значение-{row[6]} не совпадает с эталонными:[Ветеринар] или [Эколог]'

    # 8
    if row[7] == 'Биолог-исследователь':
        dct_type['Интеллектуальный'] += 1
    elif row[7] == 'Фермер':
        dct_type['Предпринимательский'] += 1
    else:
        dct_error[
            'Вопрос №8'] = f'Полученное значение-{row[7]} не совпадает с эталонными:[Биолог-исследователь] или [Фермер]'

    # 9
    if row[8] == 'Лаборант':
        dct_type['Офисный'] += 1
    elif row[8] == 'Дрессировщик':
        dct_type['Артистический'] += 1
    else:
        dct_error['Вопрос №9'] = f'Полученное значение-{row[8]} не совпадает с эталонными:[Лаборант] или [Дрессировщик]'

    # 10
    if row[9] == 'Агроном':
        dct_type['Реалистический'] += 1
    elif row[9] == 'Санитарный врач':
        dct_type['Социальный'] += 1
    else:
        dct_error[
            'Вопрос №10'] = f'Полученное значение-{row[9]} не совпадает с эталонными:[Агроном] или [Санитарный врач]'

    # 11
    if row[10] == 'Селекционер':
        dct_type['Интеллектуальный'] += 1
    elif row[10] == 'Заготовитель сельхозпродуктов':
        dct_type['Предпринимательский'] += 1
    else:
        dct_error[
            'Вопрос №11'] = f'Полученное значение-{row[10]} не совпадает с эталонными:[Селекционер] или [Заготовитель сельхозпродуктов]'

    # 12
    if row[11] == 'Микробиолог':
        dct_type['Офисный'] += 1
    elif row[11] == 'Ландшафтный дизайнер':
        dct_type['Артистический'] += 1
    else:
        dct_error[
            'Вопрос №12'] = f'Полученное значение-{row[11]} не совпадает с эталонными:[Микробиолог] или [Ландшафтный дизайнер]'

    # 13
    if row[12] == 'Массажист':
        dct_type['Реалистический'] += 1
    elif row[12] == 'Воспитатель':
        dct_type['Социальный'] += 1
    else:
        dct_error[
            'Вопрос №13'] = f'Полученное значение-{row[12]} не совпадает с эталонными:[Массажист] или [Воспитатель]'

    # 14
    if row[13] == 'Преподаватель':
        dct_type['Интеллектуальный'] += 1
    elif row[13] == 'Предприниматель':
        dct_type['Предпринимательский'] += 1
    else:
        dct_error[
            'Вопрос №14'] = f'Полученное значение-{row[13]} не совпадает с эталонными:[Преподаватель] или [Предприниматель]'

    # 15
    if row[14] == 'Администратор':
        dct_type['Офисный'] += 1
    elif row[14] == 'Режиссер театра и кино':
        dct_type['Артистический'] += 1
    else:
        dct_error[
            'Вопрос №15'] = f'Полученное значение-{row[14]} не совпадает с эталонными:[Администратор] или [Режиссер театра и кино]'

    # 16
    if row[15] == 'Официант':
        dct_type['Реалистический'] += 1
    elif row[15] == 'Врач':
        dct_type['Социальный'] += 1
    else:
        dct_error['Вопрос №16'] = f'Полученное значение-{row[15]} не совпадает с эталонными:[Официант] или [Врач]'

    # 17
    if row[16] == 'Психолог':
        dct_type['Интеллектуальный'] += 1
    elif row[16] == 'Торговый агент':
        dct_type['Предпринимательский'] += 1
    else:
        dct_error[
            'Вопрос №17'] = f'Полученное значение-{row[16]} не совпадает с эталонными:[Психолог] или [Торговый агент]'

    # 18
    if row[17] == 'Страховой агент':
        dct_type['Офисный'] += 1
    elif row[17] == 'Хореограф':
        dct_type['Артистический'] += 1
    else:
        dct_error[
            'Вопрос №18'] = f'Полученное значение-{row[17]} не совпадает с эталонными:[Страховой агент] или [Хореограф]'

    # 19
    if row[18] == 'Ювелир-гравер':
        dct_type['Реалистический'] += 1
    elif row[18] == 'Журналист':
        dct_type['Социальный'] += 1
    else:
        dct_error[
            'Вопрос №19'] = f'Полученное значение-{row[18]} не совпадает с эталонными:[Ювелир-гравер] или [Журналист]'

    # 20
    if row[19] == 'Искусствовед':
        dct_type['Интеллектуальный'] += 1
    elif row[19] == 'Продюсер':
        dct_type['Предпринимательский'] += 1
    else:
        dct_error[
            'Вопрос №20'] = f'Полученное значение-{row[19]} не совпадает с эталонными:[Искусствовед] или [Продюсер]'

    # 21
    if row[20] == 'Редактор':
        dct_type['Офисный'] += 1
    elif row[20] == 'Музыкант':
        dct_type['Артистический'] += 1
    else:
        dct_error['Вопрос №21'] = f'Полученное значение-{row[20]} не совпадает с эталонными:[Редактор] или [Музыкант]'

    # 22
    if row[21] == 'Дизайнер интерьера':
        dct_type['Реалистический'] += 1
    elif row[21] == 'Экскурсовод':
        dct_type['Социальный'] += 1
    else:
        dct_error[
            'Вопрос №22'] = f'Полученное значение-{row[21]} не совпадает с эталонными:[Дизайнер интерьера] или [Экскурсовод]'

    # 23
    if row[22] == 'Композитор':
        dct_type['Интеллектуальный'] += 1
    elif row[22] == 'Арт-директор':
        dct_type['Предпринимательский'] += 1
    else:
        dct_error[
            'Вопрос №23'] = f'Полученное значение-{row[22]} не совпадает с эталонными:[Композитор] или [Арт-директор]'

    # 24
    if row[23] == 'Музейный работник':
        dct_type['Офисный'] += 1
    elif row[23] == 'Актер театра и кино':
        dct_type['Артистический'] += 1
    else:
        dct_error[
            'Вопрос №24'] = f'Полученное значение-{row[23]} не совпадает с эталонными:[Музейный работник] или [Актер театра и кино]'

    # 25
    if row[24] == 'Верстальщик':
        dct_type['Реалистический'] += 1
    elif row[24] == 'Гид-переводчик':
        dct_type['Социальный'] += 1
    else:
        dct_error[
            'Вопрос №25'] = f'Полученное значение-{row[24]} не совпадает с эталонными:[Верстальщик] или [Гид-переводчик]'

    # 26
    if row[25] == 'Лингвист':
        dct_type['Интеллектуальный'] += 1
    elif row[25] == 'Антикризисный управляющий':
        dct_type['Предпринимательский'] += 1
    else:
        dct_error[
            'Вопрос №26'] = f'Полученное значение-{row[25]} не совпадает с эталонными:[Лингвист] или [Антикризисный управляющий]'

    # 27
    if row[26] == 'Корректор':
        dct_type['Офисный'] += 1
    elif row[26] == 'Художественный редактор':
        dct_type['Артистический'] += 1
    else:
        dct_error[
            'Вопрос №27'] = f'Полученное значение-{row[26]} не совпадает с эталонными:[Корректор] или [Художественный редактор]'

    # 28
    if row[27] == 'Наборщик текстов':
        dct_type['Реалистический'] += 1
    elif row[27] == 'Юрисконсульт':
        dct_type['Социальный'] += 1
    else:
        dct_error[
            'Вопрос №28'] = f'Полученное значение-{row[27]} не совпадает с эталонными:[Наборщик текстов] или [Юрисконсульт]'

    # 29
    if row[28] == 'Программист':
        dct_type['Интеллектуальный'] += 1
    elif row[28] == 'Брокер':
        dct_type['Предпринимательский'] += 1
    else:
        dct_error['Вопрос №29'] = f'Полученное значение-{row[28]} не совпадает с эталонными:[Программист] или [Брокер]'

    # 30
    if row[29] == 'Бухгалтер':
        dct_type['Офисный'] += 1
    elif row[29] == 'Литературный переводчик':
        dct_type['Артистический'] += 1
    else:
        dct_error[
            'Вопрос №30'] = f'Полученное значение-{row[29]} не совпадает с эталонными:[Бухгалтер] или [Литературный переводчик]'

        # проверяем на ошибки
    if len(dct_error) > 0:
        begin_str = 'Скопируйте правильные значения для указанных вопросов из квадратных скобок в вашу форму. \n'
        # создаем строку с результатами
        for sphere, value in dct_error.items():
            begin_str += f'{sphere} - {value};\n'
        return begin_str
    else:
        # сортируем по убыванию
        result_lst = sorted(dct_type.items(), key=lambda t: t[1], reverse=True)
        begin_str = '\n'
        # создаем строку с результатами
        for sphere, value in result_lst:
            begin_str += f'{sphere}: {value};\n'

        return begin_str




def processing_ptl(base_df: pd.DataFrame, answers_df: pd.DataFrame):
    """
        Функция для обработки результатов на определение профессионального типа личности
        """
    try:
        out_answer_df = base_df.copy()  # делаем копию для последующего соединения с сырыми ответами
        if answers_df.shape[1] != 30:
            raise BadCountColumnsPTL
        # Переименовываем колонки
        answers_df.columns = [f'Вопрос_ №{i}' for i in range(1, 31)]

        # проверяем правильность написания ответов
        valid_values = [['Автомеханик','Физиотерапевт'],
                        ['Специалист по защите информации','Логистик'],
                        ['Оператор связи','Кинооператор'],
                        ['Водитель','Продавец'],
                        ['Инженер-конструктор','Менеджер по продажам'],
                        ['Диспетчер','Дизайнер компьютерных программ'],
                        ['Ветеринар','Эколог'],
                        ['Биолог-исследователь','Фермер'],
                        ['Лаборант','Дрессировщик'],
                        ['Агроном','Санитарный врач'],
                        ['Селекционер','Заготовитель сельхозпродуктов'],
                        ['Микробиолог','Ландшафтный дизайнер'],
                        ['Массажист','Воспитатель'],
                        ['Преподаватель','Предприниматель'],
                        ['Администратор','Режиссер театра и кино'],
                        ['Официант','Врач'],
                        ['Психолог','Торговый агент'],
                        ['Страховой агент','Хореограф'],
                        ['Ювелир-гравер','Журналист'],
                        ['Искусствовед','Продюсер'],
                        ['Редактор','Музыкант'],
                        ['Дизайнер интерьера','Экскурсовод'],
                        ['Композитор','Арт-директор'],
                        ['Музейный работник','Актер театра и кино'],
                        ['Верстальщик','Гид-переводчик'],
                        ['Лингвист','Антикризисный управляющий'],
                        ['Корректор','Художественный редактор'],
                        ['Наборщик текстов','Юрисконсульт'],
                        ['Программист','Брокер'],
                        ['Бухгалтер','Литературный переводчик'],
                        ]
        lst_error_answers = [] # список для хранения строк где найдены неправильные ответы

        for idx,lst_values in enumerate(valid_values):
            mask = ~answers_df.iloc[:,idx].isin(lst_values) # проверяем на допустимые значения
            # Получаем строки с отличающимися значениями
            result_check = answers_df.iloc[:,idx][mask]

            if len(result_check) != 0:
                error_row = list(map(lambda x: x + 2, result_check.index))
                error_row = list(map(str, error_row))
                error_row_lst = [f'В {idx+1} вопросной колонке на строке {value}' for value in error_row]
                error_in_column = ','.join(error_row_lst)
                lst_error_answers.append(error_in_column)

        if len(lst_error_answers) !=0:
            error_message = ';'.join(lst_error_answers)
            raise BadValuePTL

        answers_df = answers_df.astype(str)

        base_df[f'Необработанное'] = answers_df.apply(processing_result_ptl, axis=1)
        base_df[f'Обработанное'] = base_df[f'Необработанное'].apply(
            extract_key_max_value)
        base_df[f'Максимум'] = base_df[f'Необработанное'].apply(
            extract_max_value)
        base_df[f'Уровень'] = base_df[f'Максимум'].apply(
            calc_level_ptl)


        # Создаем датафрейм для создания части в общий датафрейм
        part_df = pd.DataFrame(columns=['ПТЛ_Необработанное', 'ПТЛ_Обработанное','ПТЛ_Максимум','ПТЛ_Уровень'])
        part_df['ПТЛ_Необработанное'] = base_df['Необработанное']
        part_df['ПТЛ_Обработанное'] = base_df['Обработанное']
        part_df['ПТЛ_Максимум'] = base_df['Максимум']
        part_df['ПТЛ_Уровень'] = base_df['Уровень']

        base_df.sort_values(by='Максимум', ascending=False, inplace=True)  # сортируем
        out_answer_df = pd.concat([out_answer_df, answers_df], axis=1)  # Датафрейм для проверки

        description_result = """
Обработка результатов теста
8-10 баллов – ярко выраженный тип;
5-7 баллов – средне выраженный тип;
2-4 баллов – слабо выраженный тип.
Наибольшее количество баллов указывает на доминирующий тип. В чистом виде эти профессиональные типы встречаются редко – обычно можно говорить только о преобладающем типе личности. Выбирая профессию, необходимо учитывать свой профессиональный тип. Если профессия не соответствует вашему типу личности, работа будет даваться вам ценой значительного нервно-психического напряжения.
Интерпретация результатов теста
1. Реалистический тип (Р)
Люди, относящиеся к этому типу, предпочитают выполнять работу, требующую силы, ловкости, подвижности, хорошей координации движений, навыков практической работы. Результаты труда профессионалов этого типа ощутимы и реальны – их руками создан весь окружающий нас предметный мир. Люди реалистического типа охотнее делают, чем говорят, они настойчивы и уверены в себе, в работе предпочитают четкие и конкретные указания. Придерживаются традиционных ценностей, поэтому критически относятся к новым идеям.
Близкие типы: интеллектуальный и офисный.
Противоположный тип: социальный.
Хороший продавец и хороший ремонтник никогда не будут голодать. Шенк
2. Интеллектуальный (И)
Людей, относящихся к этому типу, отличают аналитические способности, рационализм, независимость и оригинальность мышления, умение точно формулировать и излагать свои мысли, решать логические задачи, генерировать новые идеи. Они часто выбирают научную и исследовательскую работу. Им нужна свобода для творчества. Работа способна увлечь их настолько, что стирается грань между рабочим временем и досугом. Мир идей для них может быть важнее, чем общение с людьми. Материальное благополучие для них обычно не на первом месте.
Близкие типы: реалистический и артистический.
Противоположный тип: предпринимательский.
Научная работа не подходит человеку, который обеими ногами стоит на земле и обеими руками тянется к долларам. М.Ларни
3. Социальный (С)
Люди, относящиеся к этому типу, предпочитают профессиональную деятельность, связанную с обучением, воспитанием, лечением, консультированием, обслуживанием. Люди этого типа гуманны, чувствительны, активны, ориентированы на социальные нормы, способны понять эмоциональное состояние другого человека. Для них характерно хорошее речевое развитие, живая мимика, интерес к людям, готовность прийти на помощь. Материальное благополучие для них обычно не на первом месте.
Близкие типы: артистический и предпринимательский.
Противоположный тип: реалистический.
Если больному после разговора с врачом не стало легче, то это не врач. В.Бехтерев
4. Офисный (О)
Люди этого типа обычно проявляют склонность к работе, связанной с обработкой и систематизацией информации, предоставленной в виде условных знаков, цифр, формул, текстов (ведение документации, установление количественных соотношений между числами и условными знаками). Они отличаются аккуратностью, пунктуальностью, практичностью, ориентированы на социальные нормы, предпочитают четко регламентированную работу. Материальное благополучие для них более значимо, чем для других типов. Склонны к работе, не связанной с широкими контактами и принятием ответственных решений.
Близкие типы: реалистический и предпринимательский.
Противоположный тип: артистический.
Офис может работать без шефа, но не без секретаря. Дж.Фонда
5. Предпринимательский (П)
Люди этого типа находчивы, практичны, быстро ориентируются в сложной обстановке, склонны к самостоятельному принятию решений, социально активны, готовы рисковать, ищут острые ощущения. Любят и умеют общаться. Имеют высокий уровень притязаний. Избегают занятий, требующих усидчивости, большой и длительной концентрации внимания. Для них значимо материальное благополучие. Предпочитают деятельность, требующую энергии, организаторских способностей, связанную с руководством, управлением и влиянием на людей.
Близкие типы: офисный и социальный.
Противоположный тип: исследовательский.
Специальность налетчика куда менее заманчива, чем смежные с ней профессии политика или биржевого спекулянта. О.Генри
6. Артистический (А)
Люди этого типа оригинальны, независимы в принятии решений, редко ориентируются на социальные нормы и одобрение, обладают необычным взглядом на жизнь, гибкостью мышления, эмоциональной чувствительностью.
Отношения с людьми строят, опираясь на свои ощущения, эмоции, воображение, интуицию. Они не выносят жесткой регламентации, предпочитая свободный график работы. Часто выбирают профессии, связанные с литературой, театром, кино, музыкой, изобразительным искусством.
Близкие типы: интеллектуальный и социальный.
Противоположный тип: офисный.
Только поэты и женщины умеют обращаться с деньгами так, как деньги того заслуживают. А.Боннар
                """

        # создаем описание результата
        base_df[f'Описание_результата'] = 'Профессиональный тип личности.\n' + base_df[
            f'Необработанное'] + description_result
        part_df['ПТЛ_Описание_результата'] = base_df[f'Описание_результата']

        # Общий свод по уровням склонности всего в процентном соотношении
        base_svod_all_df = pd.DataFrame(
            index=['слабо выраженный тип', 'средне выраженный тип',
                   'ярко выраженный тип',
                    'Итого'])

        svod_level_df = pd.pivot_table(base_df, index='Уровень',
                                       values='Максимум',
                                       aggfunc='count')

        svod_level_df['% от общего'] = round(
            svod_level_df['Максимум'] / svod_level_df['Максимум'].sum(), 3) * 100

        base_svod_all_df = base_svod_all_df.join(svod_level_df)

        # # Создаем суммирующую строку
        base_svod_all_df.loc['Итого'] = svod_level_df.sum()
        base_svod_all_df.reset_index(inplace=True)
        base_svod_all_df.rename(columns={'index': 'Уровень доминирующего типа', 'Максимум': 'Количество'}, inplace=True)

        # формируем основной словарь
        out_dct = {'Списочный результат': base_df, 'Список для проверки': out_answer_df,
                   'Свод по уровням': base_svod_all_df,
                   }

        lst_level = ['слабо выраженный тип', 'средне выраженный тип',
                   'ярко выраженный тип']
        dct_level = dict()

        for level in lst_level:
            temp_df = base_df[base_df['Уровень'] == level]
            if temp_df.shape[0] != 0:
                dct_level[level] = temp_df

        out_dct.update(dct_level)

        # Общий свод по сферам всего в процентном соотношении
        svod_sphere_df = pd.pivot_table(base_df, index='Обработанное',
                                        values='Максимум',
                                        aggfunc='count')

        svod_sphere_df['% от общего'] = round(
            svod_sphere_df['Максимум'] / svod_sphere_df['Максимум'].sum(), 3) * 100

        svod_sphere_df.sort_index(inplace=True)

        # # Создаем суммирующую строку
        svod_sphere_df.loc['Итого'] = svod_sphere_df.sum()
        svod_sphere_df.reset_index(inplace=True)
        svod_sphere_df.rename(columns={'index': 'Профессиональный тип', 'Максимум': 'Количество'},
                              inplace=True)

        # формируем списки по сферам деятельности
        lst_sphere = base_df['Обработанное'].unique()
        lst_sphere.sort()  # сортируем
        dct_sphere = {'Свод по типам': svod_sphere_df}  # словарь для хранения списков

        for sphere in lst_sphere:
            temp_df = base_df[base_df['Обработанное'] == sphere]
            dct_sphere[sphere] = temp_df

        out_dct.update(dct_sphere)

        """
            Своды 
            """
        lst_reindex_group_cols = ['Группа','слабо выраженный тип', 'средне выраженный тип',
                   'ярко выраженный тип','Итого']
        lst_reindex_group_sex_cols = ['Группа','Пол','слабо выраженный тип', 'средне выраженный тип',
                   'ярко выраженный тип','Итого']

        lst_reindex_course_cols = ['Курс','слабо выраженный тип', 'средне выраженный тип',
                   'ярко выраженный тип','Итого']
        lst_reindex_course_sex_cols = ['Курс','Пол','слабо выраженный тип', 'средне выраженный тип',
                   'ярко выраженный тип','Итого']

        # Своды по уровням
        # Группа
        svod_group_level_df = calc_mean(base_df, 'Группа', ['Группа', 'Уровень'], 'Максимум')
        svod_count_group_level_df = calc_count_level_ptl(base_df, 'Группа', ['Группа'], 'Максимум', 'Уровень',
                                                         lst_reindex_group_cols)

        # Группа Пол
        svod_group_level_sex_df = calc_mean(base_df, 'Группа', ['Группа', 'Уровень', 'Пол'], 'Максимум')
        svod_count_group_level_sex_df = calc_count_level_ptl(base_df, 'Группа', ['Группа', 'Пол'], 'Максимум', 'Уровень',
                                                             lst_reindex_group_sex_cols)

        # Курс
        svod_course_level_df = calc_mean(base_df, 'Курс', ['Курс', 'Уровень'], 'Максимум')
        svod_count_course_level_df = calc_count_level_ptl(base_df, 'Курс', ['Курс'], 'Максимум',
                                                           'Уровень', lst_reindex_course_cols)

        # Курс Пол
        svod_course_level_sex_df = calc_mean(base_df, 'Курс', ['Курс', 'Уровень', 'Пол'], 'Максимум')
        svod_count_course_level_sex_df = calc_count_level_ptl(base_df, 'Курс', ['Курс', 'Пол'],
                                                               'Максимум',
                                                               'Уровень', lst_reindex_course_sex_cols)

        # Своды по сферам
        # Группа
        svod_group_sphere_df = calc_mean(base_df, 'Группа', ['Группа', 'Обработанное'], 'Максимум')
        svod_count_group_sphere_df = calc_count_sphere_ptl(base_df, 'Группа', ['Группа'], 'Максимум', 'Обработанное')

        # Группа Пол
        svod_group_sphere_sex_df = calc_mean(base_df, 'Группа', ['Группа', 'Обработанное', 'Пол'], 'Максимум')
        svod_count_group_sphere_sex_df = calc_count_sphere_ptl(base_df, 'Группа', ['Группа', 'Пол'], 'Максимум',
                                                                'Обработанное')

        # Курс
        svod_course_sphere_df = calc_mean(base_df, 'Курс', ['Курс', 'Обработанное'], 'Максимум')
        svod_count_course_sphere_df = calc_count_sphere_ptl(base_df, 'Курс', ['Курс'], 'Максимум',
                                                             'Обработанное')

        # Курс Пол
        svod_course_sphere_sex_df = calc_mean(base_df, 'Курс', ['Курс', 'Обработанное', 'Пол'],
                                              'Максимум')
        svod_count_course_sphere_sex_df = calc_count_sphere_ptl(base_df, 'Курс', ['Курс', 'Пол'],
                                                                 'Максимум', 'Обработанное')

        svod_dct = {'Ср. Уровень Группа': svod_group_level_df, 'Кол. Уровень Группа': svod_count_group_level_df,
                    'Ср. Уровень Группа Пол': svod_group_level_sex_df,
                    'Кол. Уровень Группа Пол': svod_count_group_level_sex_df,
                    'Ср. Уровень Курс': svod_course_level_df,
                    'Кол. Уровень Курс': svod_count_course_level_df,
                    'Ср. Уровень Курс Пол': svod_course_level_sex_df,
                    'Кол. Уровень Курс Пол': svod_count_course_level_sex_df,

                    'Ср. Сфера Группа': svod_group_sphere_df, 'Кол. Сфера Группа': svod_count_group_sphere_df,
                    'Ср. Сфера Группа Пол': svod_group_sphere_sex_df,
                    'Кол. Сфера Группа Пол': svod_count_group_sphere_sex_df,
                    'Ср. Сфера Курс': svod_course_sphere_df,
                    'Кол. Сфера Курс': svod_count_course_sphere_df,
                    'Ср. Сфера Курс Пол': svod_course_sphere_sex_df,
                    'Кол. Сфера Курс Пол': svod_count_course_sphere_sex_df,

                    }
        out_dct.update(svod_dct)  # добавляем чтобы сохранить порядок

        return out_dct, part_df
    except BadValuePTL:
        messagebox.showerror('Лахеcис',
                             f'При обработке вопросов теста Профессиональный тип личности обнаружены неправильные варианты ответов. Проверьте ответы на указанных строках:\n'
                             f'{error_message}\n'
                             f'Используйте при создании Яндекс-формы написание вариантов ответа из руководства пользователя программы Лахесис.')


    except BadCountColumnsPTL:
        messagebox.showerror('Лахеcис',
                             f'Проверьте количество колонок с ответами на тест Профессиональный тип личности\n'
                             f'Должно быть 30 колонок с ответами')
