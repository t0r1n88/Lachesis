"""
Скрипт для обрабокти результатов теста профессиональный тип личности
"""
import pandas as pd
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
        begin_str = ''
        # создаем строку с результатами
        for sphere, value in result_lst:
            begin_str += f'{sphere} - {value};\n'

        return begin_str




def processing_ptl(base_df: pd.DataFrame, answers_df: pd.DataFrame):
    """
        Функция для обработки результатов на определение профессионального типа личности
        """
    out_answer_df = base_df.copy()  # делаем копию для последующего соединения с сырыми ответами
    if answers_df.shape[1] != 30:
        raise BadCountColumnsPTL
    # Переименовываем колонки
    answers_df.columns = [f'Вопрос_ №{i}' for i in range(1, 31)]

    # проверяем правильность написания ответов
    valid_values = ['Автомеханик','Физиотерапевт',
                    'Специалист по защите информации','Логистик',
                    'Оператор связи','Кинооператор',
                    'Водитель','Продавец',
                    'Инженер-конструктор','Менеджер по продажам',
                    'Диспетчер','Дизайнер компьютерных программ',
                    'Ветеринар','Эколог',
                    'Биолог-исследователь','Фермер',
                    'Лаборант','Дрессировщик',
                    'Агроном','Санитарный врач',
                    'Селекционер','Заготовитель сельхозпродуктов',
                    'Микробиолог','Ландшафтный дизайнер',
                    'Массажист','Воспитатель',
                    'Преподаватель','Предприниматель',
                    'Администратор','Режиссер театра и кино',
                    'Официант','Врач',
                    'Психолог','Торговый агент',
                    'Страховой агент','Хореограф',
                    'Ювелир-гравер','Журналист',
                    'Искусствовед','Продюсер',
                    'Редактор','Музыкант',
                    'Дизайнер интерьера','Экскурсовод',
                    'Композитор','Арт-директор',
                    'Музейный работник','Актер театра и кино',
                    'Верстальщик','Гид-переводчик',
                    'Лингвист','Антикризисный управляющий',
                    'Корректор','Художественный редактор',
                    'Наборщик текстов','Юрисконсульт',
                    'Программист','Брокер',
                    'Бухгалтер','Литературный переводчик',
                    ]
    # Проверяем, есть ли значения, отличающиеся от указанных в списке
    mask = ~answers_df.isin(valid_values)

    # Получаем строки с отличающимися значениями
    result_check = answers_df[mask.any(axis=1)]
    if len(result_check) != 0:
        error_row = list(map(lambda x: x + 2, result_check.index))
        error_row = list(map(str, error_row))
        error_message = ';'.join(error_row)
        raise BadValuePTL

    answers_df = answers_df.astype(str)

    base_df[f'Необработанное'] = answers_df.apply(processing_result_ptl, axis=1)
    base_df[f'Обработанное'] = base_df[f'Необработанное'].apply(
        extract_key_max_value)
    base_df[f'Максимум'] = base_df[f'Необработанное'].apply(
        extract_max_value)

    # Создаем датафрейм для создания части в общий датафрейм
    part_df = pd.DataFrame(columns=['ПТЛ_Необработанное', 'ПТЛ_Обработанное','ПТЛ_Максимум'])
    part_df['ПТЛ_Необработанное'] = base_df['Необработанное']
    part_df['ПТЛ_Обработанное'] = base_df['Обработанное']
    part_df['ПТЛ_Максимум'] = base_df['Максимум']

    base_df.sort_values(by='Максимум', ascending=False, inplace=True)  # сортируем
    out_answer_df = pd.concat([out_answer_df, answers_df], axis=1)  # Датафрейм для проверки

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
    svod_all_df.rename(columns={'Обработанное':'Тип','Максимум':'Количество'},inplace=True)






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
        columns=['Класс', 'Реалистический', 'Интеллектуальный',
             'Социальный', 'Офисный',
             'Предпринимательский', 'Артистический',
             'Итого'])
    svod_count_group_df['% Реалистический от общего'] = round(
        svod_count_group_df['Реалистический'] / svod_count_group_df['Итого'], 2) * 100
    svod_count_group_df['% Интеллектуальный от общего'] = round(
        svod_count_group_df['Интеллектуальный'] / svod_count_group_df['Итого'], 2) * 100
    svod_count_group_df['% Социальный от общего'] = round(
        svod_count_group_df['Социальный'] / svod_count_group_df['Итого'], 2) * 100
    svod_count_group_df['% Офисный от общего'] = round(
        svod_count_group_df['Офисный'] / svod_count_group_df['Итого'], 2) * 100
    svod_count_group_df['% Предпринимательский от общего'] = round(
        svod_count_group_df['Предпринимательский'] / svod_count_group_df['Итого'], 2) * 100
    svod_count_group_df['% Артистический от общего'] = round(
        svod_count_group_df['Артистический'] / svod_count_group_df['Итого'], 2) * 100

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
        columns=['Класс','Пол', 'Реалистический', 'Интеллектуальный',
                 'Социальный', 'Офисный',
                 'Предпринимательский', 'Артистический',
                 'Итого'])
    svod_count_group_sex_df['% Реалистический от общего'] = round(
        svod_count_group_sex_df['Реалистический'] / svod_count_group_sex_df['Итого'], 2) * 100
    svod_count_group_sex_df['% Интеллектуальный от общего'] = round(
        svod_count_group_sex_df['Интеллектуальный'] / svod_count_group_sex_df['Итого'], 2) * 100
    svod_count_group_sex_df['% Социальный от общего'] = round(
        svod_count_group_sex_df['Социальный'] / svod_count_group_sex_df['Итого'], 2) * 100
    svod_count_group_sex_df['% Офисный от общего'] = round(
        svod_count_group_sex_df['Офисный'] / svod_count_group_sex_df['Итого'], 2) * 100
    svod_count_group_sex_df['% Предпринимательский от общего'] = round(
        svod_count_group_sex_df['Предпринимательский'] / svod_count_group_sex_df['Итого'], 2) * 100
    svod_count_group_sex_df['% Артистический от общего'] = round(
        svod_count_group_sex_df['Артистический'] / svod_count_group_sex_df['Итого'], 2) * 100

    part_svod_df = svod_count_group_sex_df.iloc[:-1:]
    part_svod_df.sort_values(by='Класс', key=lambda x: x.map(sort_name_class), inplace=True)  # сортируем
    itog_svod_df = svod_count_group_sex_df.iloc[-1:]
    svod_count_group_sex_df = pd.concat([part_svod_df, itog_svod_df])


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
        columns=['Номер_класса', 'Реалистический', 'Интеллектуальный',
                 'Социальный', 'Офисный',
                 'Предпринимательский', 'Артистический',
                 'Итого'])
    svod_count_course_df['% Реалистический от общего'] = round(
        svod_count_course_df['Реалистический'] / svod_count_course_df['Итого'], 2) * 100
    svod_count_course_df['% Интеллектуальный от общего'] = round(
        svod_count_course_df['Интеллектуальный'] / svod_count_course_df['Итого'], 2) * 100
    svod_count_course_df['% Социальный от общего'] = round(
        svod_count_course_df['Социальный'] / svod_count_course_df['Итого'], 2) * 100
    svod_count_course_df['% Офисный от общего'] = round(
        svod_count_course_df['Офисный'] / svod_count_course_df['Итого'], 2) * 100
    svod_count_course_df['% Предпринимательский от общего'] = round(
        svod_count_course_df['Предпринимательский'] / svod_count_course_df['Итого'], 2) * 100
    svod_count_course_df['% Артистический от общего'] = round(
        svod_count_course_df['Артистический'] / svod_count_course_df['Итого'], 2) * 100

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
        columns=['Номер_класса', 'Пол', 'Реалистический', 'Интеллектуальный',
                 'Социальный', 'Офисный',
                 'Предпринимательский', 'Артистический',
                 'Итого'])
    svod_count_course_sex_df['% Реалистический от общего'] = round(
        svod_count_course_sex_df['Реалистический'] / svod_count_course_sex_df['Итого'], 2) * 100
    svod_count_course_sex_df['% Интеллектуальный от общего'] = round(
        svod_count_course_sex_df['Интеллектуальный'] / svod_count_course_sex_df['Итого'], 2) * 100
    svod_count_course_sex_df['% Социальный от общего'] = round(
        svod_count_course_sex_df['Социальный'] / svod_count_course_sex_df['Итого'], 2) * 100
    svod_count_course_sex_df['% Офисный от общего'] = round(
        svod_count_course_sex_df['Офисный'] / svod_count_course_sex_df['Итого'], 2) * 100
    svod_count_course_sex_df['% Предпринимательский от общего'] = round(
        svod_count_course_sex_df['Предпринимательский'] / svod_count_course_sex_df['Итого'], 2) * 100
    svod_count_course_sex_df['% Артистический от общего'] = round(
        svod_count_course_sex_df['Артистический'] / svod_count_course_sex_df['Итого'], 2) * 100

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
    if 'ФИО' in base_df.columns:
        base_df[f'Описание_результата'] = base_df['ФИО'] + '.' + ' \nПрофессиональный тип личности.\n' + \
                                                 base_df[
                                                     f'Необработанное'] + description_result
        part_df['ПТЛ_Описание_результата'] = base_df[f'Описание_результата']
    else:
        base_df[f'Описание_результата'] = 'Профессиональный тип личности.\n' + base_df[
            f'Необработанное'] + description_result
        part_df['ПТЛ_Описание_результата'] = base_df[f'Описание_результата']



    # формируем словарь
    out_dct = {'Списочный результат': base_df, 'Список для проверки': out_answer_df,
               'Общий свод':svod_all_df,
               'Среднее Класс': svod_group_df,'Количество Класс': svod_count_group_df,
               'Среднее Класс Пол': svod_group_sex_df,'Количество Класс Пол': svod_count_group_sex_df,
               'Среднее Номер_класса': svod_course_df, 'Количество Номер_класса': svod_count_course_df,
               'Среднее Номер_класса Пол': svod_course_sex_df, 'Количество Номер_класса Пол': svod_count_course_sex_df,
               }

    return out_dct, part_df


















    # if answers_df.shape[1] != size:
    #     raise WrongNumberColumn
    #
    # answers_df.columns = [f'{name_test}_Вопрос_ №_{i}' for i in range(1, answers_df.shape[1] + 1)]
    #
    # answers_df = answers_df.astype(str)
    #
    # answers_df = answers_df.applymap(lambda x: x.strip())
    # answers_df[f'{name_test}_Необработанный_результат'] = answers_df.apply(processing_result_ptl, axis=1)
    # answers_df[f'{name_test}_Обработанный_результат'] = answers_df[f'{name_test}_Необработанный_результат'].apply(
    #     extract_key_max_value)
    # answers_df[f'{name_test}_Числовое_значение_результата'] = answers_df[f'{name_test}_Необработанный_результат'].apply(
    #     extract_max_value)
    #
    # # Создаем датафрейм для данных отчета
    # report_df = answers_df.iloc[::, size + 1:]
    #
    # # Создаем датафрейм в который будем заносить итоговые результаты
    # finish_report_df = report_df[f'{name_test}_Обработанный_результат'].value_counts().to_frame()
    #
    # # получаем процента
    # finish_report_df['Доля_от_общего_количества'] = round(
    #     (finish_report_df[f'{name_test}_Обработанный_результат'] / report_df.shape[0]) * 100, 2)
    #
    # finish_report_df = finish_report_df.reset_index()
    #
    # finish_report_df.columns = ['Категория', 'Количество', 'Доля в % от общего количества']
    #
    # # соединяем после обработки
    # df = pd.concat([base_df, answers_df], axis=1)
    #
    # description_result = """
    # Обработка результатов теста
    # 8-10 баллов – ярко выраженный тип;
    # 5-7 баллов – средне выраженный тип;
    # 2-4 баллов – слабо выраженный тип.
    # Наибольшее количество баллов указывает на доминирующий тип. В чистом виде эти профессиональные типы встречаются редко – обычно можно говорить только о преобладающем типе личности. Выбирая профессию, необходимо учитывать свой профессиональный тип. Если профессия не соответствует вашему типу личности, работа будет даваться вам ценой значительного нервно-психического напряжения.
    # Интерпретация результатов теста
    # 1. Реалистический тип (Р)
    # Люди, относящиеся к этому типу, предпочитают выполнять работу, требующую силы, ловкости, подвижности, хорошей координации движений, навыков практической работы. Результаты труда профессионалов этого типа ощутимы и реальны – их руками создан весь окружающий нас предметный мир. Люди реалистического типа охотнее делают, чем говорят, они настойчивы и уверены в себе, в работе предпочитают четкие и конкретные указания. Придерживаются традиционных ценностей, поэтому критически относятся к новым идеям.
    # Близкие типы: интеллектуальный и офисный.
    # Противоположный тип: социальный.
    # Хороший продавец и хороший ремонтник никогда не будут голодать. Шенк
    # 2. Интеллектуальный (И)
    # Людей, относящихся к этому типу, отличают аналитические способности, рационализм, независимость и оригинальность мышления, умение точно формулировать и излагать свои мысли, решать логические задачи, генерировать новые идеи. Они часто выбирают научную и исследовательскую работу. Им нужна свобода для творчества. Работа способна увлечь их настолько, что стирается грань между рабочим временем и досугом. Мир идей для них может быть важнее, чем общение с людьми. Материальное благополучие для них обычно не на первом месте.
    # Близкие типы: реалистический и артистический.
    # Противоположный тип: предпринимательский.
    # Научная работа не подходит человеку, который обеими ногами стоит на земле и обеими руками тянется к долларам. М.Ларни
    # 3. Социальный (С)
    # Люди, относящиеся к этому типу, предпочитают профессиональную деятельность, связанную с обучением, воспитанием, лечением, консультированием, обслуживанием. Люди этого типа гуманны, чувствительны, активны, ориентированы на социальные нормы, способны понять эмоциональное состояние другого человека. Для них характерно хорошее речевое развитие, живая мимика, интерес к людям, готовность прийти на помощь. Материальное благополучие для них обычно не на первом месте.
    # Близкие типы: артистический и предпринимательский.
    # Противоположный тип: реалистический.
    # Если больному после разговора с врачом не стало легче, то это не врач. В.Бехтерев
    # 4. Офисный (О)
    # Люди этого типа обычно проявляют склонность к работе, связанной с обработкой и систематизацией информации, предоставленной в виде условных знаков, цифр, формул, текстов (ведение документации, установление количественных соотношений между числами и условными знаками). Они отличаются аккуратностью, пунктуальностью, практичностью, ориентированы на социальные нормы, предпочитают четко регламентированную работу. Материальное благополучие для них более значимо, чем для других типов. Склонны к работе, не связанной с широкими контактами и принятием ответственных решений.
    # Близкие типы: реалистический и предпринимательский.
    # Противоположный тип: артистический.
    # Офис может работать без шефа, но не без секретаря. Дж.Фонда
    # 5. Предпринимательский (П)
    # Люди этого типа находчивы, практичны, быстро ориентируются в сложной обстановке, склонны к самостоятельному принятию решений, социально активны, готовы рисковать, ищут острые ощущения. Любят и умеют общаться. Имеют высокий уровень притязаний. Избегают занятий, требующих усидчивости, большой и длительной концентрации внимания. Для них значимо материальное благополучие. Предпочитают деятельность, требующую энергии, организаторских способностей, связанную с руководством, управлением и влиянием на людей.
    # Близкие типы: офисный и социальный.
    # Противоположный тип: исследовательский.
    # Специальность налетчика куда менее заманчива, чем смежные с ней профессии политика или биржевого спекулянта. О.Генри
    # 6. Артистический (А)
    # Люди этого типа оригинальны, независимы в принятии решений, редко ориентируются на социальные нормы и одобрение, обладают необычным взглядом на жизнь, гибкостью мышления, эмоциональной чувствительностью.
    # Отношения с людьми строят, опираясь на свои ощущения, эмоции, воображение, интуицию. Они не выносят жесткой регламентации, предпочитая свободный график работы. Часто выбирают профессии, связанные с литературой, театром, кино, музыкой, изобразительным искусством.
    # Близкие типы: интеллектуальный и социальный.
    # Противоположный тип: офисный.
    # Только поэты и женщины умеют обращаться с деньгами так, как деньги того заслуживают. А.Боннар
    # """
    # if 'ФИО' in df.columns:
    #     df[f'{name_test}_Описание_результата'] = df['ФИО'] + '.' + ' \nОпределение профессионального типа личности.\n' + \
    #                                              df[
    #                                                  f'{name_test}_Необработанный_результат'] + description_result
    # else:
    #     df[f'{name_test}_Описание_результата'] = 'Определение профессионального типа личности.\n' + df[
    #         f'{name_test}_Необработанный_результат'] + description_result
    #
    # # Создаем сокращенный вариант
    # send_df = df.iloc[:, :threshold_base]
    # # Добавляем колонки с результатами
    # send_df[f'{name_test}_Необработанный_результат'] = df[f'{name_test}_Необработанный_результат']
    # send_df[f'{name_test}_Обработанный_результат'] = df[f'{name_test}_Обработанный_результат']
    # send_df[f'{name_test}_Числовое_значение_результата'] = df[f'{name_test}_Числовое_значение_результата']
    # send_df[f'{name_test}_Описание_результата'] = df[f'{name_test}_Описание_результата']
    # # создаем датафреймы для возврата в основную функцию
    # out_full_df = df.iloc[:, threshold_base:]  # датафрейм с вопросами и результатами без анкетных данных
    # out_result_df = send_df.iloc[:, threshold_base:]
    # # Сортировка
    # df.sort_values(by=f'{name_test}_Числовое_значение_результата', ascending=False, inplace=True)
    # send_df.sort_values(by=f'{name_test}_Числовое_значение_результата', ascending=False, inplace=True)
    #
    #
    # finish_path = f'{end_folder}/ПТЛ'
    # if not os.path.exists(finish_path):
    #     os.makedirs(finish_path)
    #
    # df.to_excel(f'{finish_path}/Полная таблица {name_test}.xlsx',
    #             index=False,
    #             engine='xlsxwriter')
    # send_df.to_excel(f'{finish_path}/Краткая таблица {name_test}.xlsx',
    #                  index=False, engine='xlsxwriter')
    # finish_report_df.to_excel(f'{finish_path}/Сводка {name_test}.xlsx',
    #                           index=False, engine='xlsxwriter')
    #
    # return out_full_df, out_result_df

