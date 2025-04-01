"""
Скрипт для обработки результатов теста ДДО
"""
import pandas as pd
from tkinter import messagebox
from lachesis_support_functions import round_mean,sort_name_class

class BadValueDDO(Exception):
    """
    Исключение для неправильных значений в вариантах ответов
    """
    pass

class BadCountColumnsDDO(Exception):
    """
    Исключение для обработки случая если количество колонок не равно 20
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


def create_out_str_ddo(x,dct_desciprion,dct_prof):
    """
    Функция для создания выходной строки ДДО
    """
    return f'{dct_desciprion.get(x, "Проверьте правильность написания ответа в форме,в колонке ДДО_Обработанный_результат указаны несовпадающие значения")}\nРекомендуемые профессии:\n{dct_prof.get(x, "Проверьте правильность написания ответа в форме,в колонке ДДО_Обработанный_результат указаны несовпадающие значения")}'




def processing_result_ddo(row):
    """
    Обработка результатов тестирования ДДО
    """
    # Создаем словарь для хранения данных
    # Создаем словарь для хранения данных
    dct_type = {'Человек-природа': 0, 'Человек-техника': 0, 'Человек-человек': 0, 'Человек-знаковые системы': 0,
                'Человек-художественный образ': 0}
    dct_error = {}  # словарь для хранения ошибочных  значений, для того чтобы было легче находить ошибки при обновлении
    # 1
    if row[0] == 'Ухаживать за животными':
        dct_type['Человек-природа'] += 1
    elif row[0] == 'Обслуживать машины, приборы (следить, регулировать)':
        dct_type['Человек-техника'] += 1
    else:
        dct_error[
            'Вопрос №1'] = f'Полученное значение-{row[0]} не совпадает с эталонными:[Ухаживать за животными] или [Обслуживать машины, приборы (следить, регулировать)]'
    # 2
    if row[1] == 'Помогать больным':
        dct_type['Человек-человек'] += 1
    elif row[1] == 'Составлять таблицы, схемы, компьютерные программы':
        dct_type['Человек-знаковые системы'] += 1
    else:
        dct_error[
            'Вопрос №2'] = f'Полученное значение-{row[1]} не совпадает с эталонными:[Помогать больным] или [Составлять таблицы, схемы, компьютерные программы]'

    # 3
    if row[2] == 'Следить за качеством книжных иллюстраций, плакатов, художественных открыток, музыкальных записей':
        dct_type['Человек-художественный образ'] += 1
    elif row[2] == 'Следить за состоянием и развитием растений':
        dct_type['Человек-природа'] += 1
    else:
        dct_error[
            'Вопрос №3'] = f'Полученное значение-{row[2]} не совпадает с эталонными:[Следить за качеством книжных иллюстраций, плакатов, художественных открыток, музыкальных записей] или [Следить за состоянием и развитием растений]'

    # 4
    if row[3] == 'Обрабатывать материалы (дерево, ткань, металл, пластмассу и т.п.)':
        dct_type['Человек-техника'] += 1
    elif row[3] == 'Доводить товары до потребителя, рекламировать, продавать':
        dct_type['Человек-человек'] += 1
    else:
        dct_error[
            'Вопрос №4'] = f'Полученное значение-{row[3]} не совпадает с эталонными:[Обрабатывать материалы (дерево, ткань, металл, пластмассу и т.п.)] или [Доводить товары до потребителя, рекламировать, продавать]'

    # 5
    if row[4] == 'Обсуждать научно-популярные книги, статьи':
        dct_type['Человек-знаковые системы'] += 1
    elif row[4] == 'Обсуждать художественные книги (или пьесы, концерты)':
        dct_type['Человек-художественный образ'] += 1
    else:
        dct_error[
            'Вопрос №5'] = f'Полученное значение-{row[4]} не совпадает с эталонными:[Обсуждать научно-популярные книги, статьи] или [Обсуждать художественные книги (или пьесы, концерты)]'

    # 6
    if row[5] == 'Выращивать молодняк (животных какой-либо породы)':
        dct_type['Человек-природа'] += 1
    elif row[
        5] == 'Тренировать товарищей (или младших) для выполнения и закрепления каких-либо навыков (трудовых, учебных, спортивных)':
        dct_type['Человек-человек'] += 1
    else:
        dct_error[
            'Вопрос №6'] = f'Полученное значение-{row[5]} не совпадает с эталонными:[Выращивать молодняк (животных какой-либо породы)] или [Тренировать товарищей (или младших) для выполнения и закрепления каких-либо навыков (трудовых, учебных, спортивных)]'

    # 7
    if row[6] == 'Копировать рисунки, изображения (или настраивать музыкальные инструменты)':
        dct_type['Человек-художественный образ'] += 1
    elif row[
        6] == 'Управлять какой-либо машиной (грузовым, подъемным или транспортным средством) - подъемным краном, трактором, тепловозом и др.':
        dct_type['Человек-техника'] += 1
    else:
        dct_error[
            'Вопрос №7'] = f'Полученное значение-{row[6]} не совпадает с эталонными:[Копировать рисунки, изображения (или настраивать музыкальные инструменты)] или [Управлять какой-либо машиной (грузовым, подъемным или транспортным средством) - подъемным краном, трактором, тепловозом и др.]'

    # 8
    if row[7] == 'Сообщать, разъяснять людям нужные им сведения (в справочном бюро, на экскурсии и т.д.)':
        dct_type['Человек-человек'] += 1
    elif row[7] == 'Оформлять выставки, витрины (или участвовать в подготовке пьес, концертов)':
        dct_type['Человек-художественный образ'] += 1
    else:
        dct_error[
            'Вопрос №8'] = f'Полученное значение-{row[7]} не совпадает с эталонными:[Сообщать, разъяснять людям нужные им сведения (в справочном бюро, на экскурсии и т.д.)] или [Оформлять выставки, витрины (или участвовать в подготовке пьес, концертов)]'

    # 9
    if row[8] == 'Ремонтировать вещи, изделия (одежду, технику), жилище':
        dct_type['Человек-техника'] += 1
    elif row[8] == 'Искать и исправлять ошибки в текстах, таблицах, рисунках':
        dct_type['Человек-знаковые системы'] += 1
    else:
        dct_error[
            'Вопрос №9'] = f'Полученное значение-{row[8]} не совпадает с эталонными:[Ремонтировать вещи, изделия (одежду, технику), жилище] или [Искать и исправлять ошибки в текстах, таблицах, рисунках]'

    # 10
    if row[9] == 'Лечить животных':
        dct_type['Человек-природа'] += 1
    elif row[9] == 'Выполнять вычисления, расчёты':
        dct_type['Человек-знаковые системы'] += 1
    else:
        dct_error[
            'Вопрос №10'] = f'Полученное значение-{row[9]} не совпадает с эталонными:[Лечить животных] или [Выполнять вычисления, расчёты]'

    # 11
    if row[10] == 'Выводить новые сорта растений':
        dct_type['Человек-природа'] += 1
    elif row[10] == 'Конструировать, новые виды промышленных изделий (машины, одежду, дома, продукты питания и т.п.)':
        dct_type['Человек-техника'] += 1
    else:
        dct_error[
            'Вопрос №11'] = f'Полученное значение-{row[10]} не совпадает с эталонными:[Выводить новые сорта растений] или [Конструировать, новые виды промышленных изделий (машины, одежду, дома, продукты питания и т.п.)]'

    # 12
    if row[11] == 'Разбирать споры, ссоры между людьми, убеждать, разъяснять, наказывать, поощрять':
        dct_type['Человек-человек'] += 1
    elif row[11] == 'Разбираться в чертежах, схемах, таблицах (проверять, уточнять, приводить в порядок)':
        dct_type['Человек-знаковые системы'] += 1
    else:
        dct_error[
            'Вопрос №12'] = f'Полученное значение-{row[11]} не совпадает с эталонными:[Разбирать споры, ссоры между людьми, убеждать, разъяснять, наказывать, поощрять] или [Разбираться в чертежах, схемах, таблицах (проверять, уточнять, приводить в порядок)]'

    # 13
    if row[12] == 'Наблюдать, изучать работу коллективов художественной самодеятельности':
        dct_type['Человек-художественный образ'] += 1
    elif row[12] == 'Наблюдать, изучать жизнь микробов':
        dct_type['Человек-природа'] += 1
    else:
        dct_error[
            'Вопрос №13'] = f'Полученное значение-{row[12]} не совпадает с эталонными:[Наблюдать, изучать работу коллективов художественной самодеятельности] или [Наблюдать, изучать жизнь микробов]'

    # 14
    if row[13] == 'Обслуживать, налаживать медицинские приборы, аппараты':
        dct_type['Человек-техника'] += 1
    elif row[13] == 'Оказывать людям медицинскую помощь при ранениях, ушибах, ожогах и т.п.':
        dct_type['Человек-человек'] += 1
    else:
        dct_error[
            'Вопрос №14'] = f'Полученное значение-{row[13]} не совпадает с эталонными:[Обслуживать, налаживать медицинские приборы, аппараты] или [Оказывать людям медицинскую помощь при ранениях, ушибах, ожогах и т.п.]'

    # 15
    if row[14] == 'Художественно описывать, изображать события (наблюдаемые и представляемые)':
        dct_type['Человек-знаковые системы'] += 1
    elif row[14] == 'Составлять точные описания-отчеты о наблюдаемых явлениях, событиях, измеряемых объектах и др.':
        dct_type['Человек-художественный образ'] += 1
    else:
        dct_error[
            'Вопрос №15'] = f'Полученное значение-{row[14]} не совпадает с эталонными:[Художественно описывать, изображать события (наблюдаемые и представляемые)] или [Составлять точные описания-отчеты о наблюдаемых явлениях, событиях, измеряемых объектах и др.]'

    # 16
    if row[15] == 'Делать лабораторные анализы в больнице':
        dct_type['Человек-природа'] += 1
    elif row[15] == 'Принимать, осматривать больных, беседовать с ними, назначать лечение':
        dct_type['Человек-человек'] += 1
    else:
        dct_error[
            'Вопрос №16'] = f'Полученное значение-{row[15]} не совпадает с эталонными:[Делать лабораторные анализы в больнице] или [Принимать, осматривать больных, беседовать с ними, назначать лечение]'

    # 17
    if row[16] == 'Красить или расписывать стены помещений, поверхность изделий':
        dct_type['Человек-техника'] += 1
    elif row[16] == 'Осуществлять монтаж или сборку машин, приборов':
        dct_type['Человек-техника'] += 1
    else:
        dct_error[
            'Вопрос №17'] = f'Полученное значение-{row[16]} не совпадает с эталонными:[Красить или расписывать стены помещений, поверхность изделий] или [Осуществлять монтаж или сборку машин, приборов]'

    # 18
    if row[
        17] == 'Организовывать культпоходы сверстников или младших в театры, музеи, экскурсии, туристические походы и т.п.':
        dct_type['Человек-человек'] += 1
    elif row[17] == 'Играть на сцене, принимать участие в концертах':
        dct_type['Человек-художественный образ'] += 1
    else:
        dct_error[
            'Вопрос №18'] = f'Полученное значение-{row[17]} не совпадает с эталонными:[Организовывать культпоходы сверстников или младших в театры, музеи, экскурсии, туристические походы и т.п.] или [Играть на сцене, принимать участие в концертах]'

    # 19
    if row[18] == 'Изготовлять по чертежам детали, изделия (машины, одежду), строить здания':
        dct_type['Человек-техника'] += 1
    elif row[18] == 'Заниматься черчением, копировать чертежи, карты':
        dct_type['Человек-знаковые системы'] += 1
    else:
        dct_error[
            'Вопрос №19'] = f'Полученное значение-{row[18]} не совпадает с эталонными:[Изготовлять по чертежам детали, изделия (машины, одежду), строить здания] или [Заниматься черчением, копировать чертежи, карты]'

    # 20
    if row[19] == 'Вести борьбу с болезнями растений, с вредителями леса, сада':
        dct_type['Человек-природа'] += 1
    elif row[19] == 'Работать на устройствах с клавиатурой, ноутбуке и др.)':
        dct_type['Человек-знаковые системы'] += 1
    else:
        dct_error[
            'Вопрос №20'] = f'Полученное значение-{row[19]} не совпадает с эталонными:[Вести борьбу с болезнями растений, с вредителями леса, сада] или [Работать на устройствах с клавиатурой, ноутбуке и др.)]'

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







def processing_ddo(base_df: pd.DataFrame, answers_df: pd.DataFrame):
    """
        Фугкция для обработки данных ДДО
        :return:
        """
    try:
        out_answer_df = base_df.copy()  # делаем копию для последующего соединения с сырыми ответами
        if answers_df.shape[1] != 20:
            raise BadCountColumnsDDO
        # Переименовываем колонки
        answers_df.columns = [f'Вопрос_ №{i}' for i in range(1, 21)]

        valid_values = ['Ухаживать за животными','Обслуживать машины, приборы (следить, регулировать)',
                        'Помогать больным','Составлять таблицы, схемы, компьютерные программы',
                        'Следить за качеством книжных иллюстраций, плакатов, художественных открыток, музыкальных записей','Следить за состоянием и развитием растений',
                        'Обрабатывать материалы (дерево, ткань, металл, пластмассу и т.п.)','Доводить товары до потребителя, рекламировать, продавать',
                        'Обсуждать научно-популярные книги, статьи','Обсуждать художественные книги (или пьесы, концерты)',
                        'Выращивать молодняк (животных какой-либо породы)','Тренировать товарищей (или младших) для выполнения и закрепления каких-либо навыков (трудовых, учебных, спортивных)',
                        'Копировать рисунки, изображения (или настраивать музыкальные инструменты)','Управлять какой-либо машиной (грузовым, подъемным или транспортным средством) - подъемным краном, трактором, тепловозом и др.',
                        'Сообщать, разъяснять людям нужные им сведения (в справочном бюро, на экскурсии и т.д.)','Оформлять выставки, витрины (или участвовать в подготовке пьес, концертов)',
                        'Ремонтировать вещи, изделия (одежду, технику), жилище','Искать и исправлять ошибки в текстах, таблицах, рисунках',
                        'Лечить животных','Выполнять вычисления, расчёты',
                        'Выводить новые сорта растений','Конструировать, новые виды промышленных изделий (машины, одежду, дома, продукты питания и т.п.)',
                        'Разбирать споры, ссоры между людьми, убеждать, разъяснять, наказывать, поощрять','Разбираться в чертежах, схемах, таблицах (проверять, уточнять, приводить в порядок)',
                        'Наблюдать, изучать работу коллективов художественной самодеятельности','Наблюдать, изучать жизнь микробов',
                        'Обслуживать, налаживать медицинские приборы, аппараты','Оказывать людям медицинскую помощь при ранениях, ушибах, ожогах и т.п.',
                        'Художественно описывать, изображать события (наблюдаемые и представляемые)','Составлять точные описания-отчеты о наблюдаемых явлениях, событиях, измеряемых объектах и др.',
                        'Делать лабораторные анализы в больнице','Принимать, осматривать больных, беседовать с ними, назначать лечение',
                        'Красить или расписывать стены помещений, поверхность изделий','Осуществлять монтаж или сборку машин, приборов',
                        'Организовывать культпоходы сверстников или младших в театры, музеи, экскурсии, туристические походы и т.п.','Играть на сцене, принимать участие в концертах',
                        'Изготовлять по чертежам детали, изделия (машины, одежду), строить здания','Заниматься черчением, копировать чертежи, карты',
                        'Вести борьбу с болезнями растений, с вредителями леса, сада','Работать на устройствах с клавиатурой, ноутбуке и др.)',
                        ]

        # Проверяем, есть ли значения, отличающиеся от указанных в списке
        mask = ~answers_df.isin(valid_values)

        # Получаем строки с отличающимися значениями
        result_check = answers_df[mask.any(axis=1)]
        if len(result_check) != 0:
            error_row = list(map(lambda x: x + 2, result_check.index))
            error_row = list(map(str, error_row))
            error_message = ';'.join(error_row)
            raise BadValueDDO

        # Создаем словари для создания текста письма
        dct_prof = {
            'Человек-природа': 'Тракторист, рыбовод, зоотехник, агроном, садовник, ветеринар, животновод, геолог, биолог, почвовед и т.д.',
            'Человек-техника': 'Водитель, токарь, инженер, слесарь, радиотехник, швея, электрик, механик, монтажник и т.п.',
            'Человек-человек': 'Продавец, медсестра, секретарь, бортпроводник, учитель, воспитатель, няня, преподаватель, врач, официант, администратор и т.п.',
            'Человек-знаковые системы': 'Наборщик, кассир, делопроизводитель, бухгалтер, программист, чертежник, корректор, экономист, радист, оператор ПЭВМ, машинистка, наборщик и т.п.',
            'Человек-художественный образ': 'Парикмахер, модельер, чеканщик, маляр, гравер, резчик по камню, фотограф, актер, художник, музыкант и т.п.'}

        dct_desciprion = \
            {'Человек-природа': """Человек-природа.\n
        Представителей этих профессий объединяет одно очень важное качество — любовь к
        природе. Но любовь не созерцательная. Которой обладают практически все люди,
        считая природу наиболее благоприятной средой для отдыха, а деятельная связанная с
        познанием ее законов и применением их. Одно дело — любить животных и растения,
        играть с ними, радоваться им. И совсем другое — регулярно, день за днем ухаживать
        за ними, наблюдать, лечить, выгуливать, не считаясь с личным временем и планами.
        Специалист должен не просто все знать о живых организмах, но и прогнозировать
        возможные изменения в них и принимать меры. От человека требуется инициатива и
        самостоятельность в решении конкретных задач, заботливость, терпение и
        дальновидность.\n
        Человек, работающий в сфере «человек-природа», должен быть спокойным и уравновешенным.""",
             'Человек-техника': """Человек-техника.\n
        Особенность технических объектов в том, что они, как правило, могут быть точно
        измерены по многим признакам. При их обработке, преобразовании, перемещении
        или оценке от работника требуется точность, определенность действий. Техника как
        предмет труда представляет широкие возможности для новаторства, выдумки,
        творчества, поэтому важное значение приобретает такое качество, как практическое
        мышление. Техническая фантазия, способность мысленно соединять и разъединять
        технические объекты и их части — важные условия для успеха в данной области.
        """, 'Человек-человек': """Человек-человек.\n
        Главное содержание труда в профессиях типа «человек-человек» сводится к
        взаимодействию между людьми. Если не наладится это взаимодействие, значит, не
        наладится и работа. Качества, необходимые для работы с людьми: устойчивое,
        хорошее настроение в процессе работы с людьми, потребность в общении,
        способность мысленно ставить себя на место другого человека, быстро понимать
        намерения, помыслы, настроение людей, умение разбираться в человеческих
        взаимоотношениях, хорошая память (умение держать в уме имена и особенности
        многих людей), терпение.
        """, 'Человек-знаковые системы': """Человек-знаковая система.\n
        Мы встречаемся со знаками значительно чаще, чем обычно представляем себе. Это
        цифры. Коды, условные знаки, естественные или искусственные языки, чертежи,
        таблицы формулы. В любом случае человек воспринимает знак как символ реального
        объекта или явления. Поэтому специалисту, который работает со знаками, важно
        уметь, с одной стороны, абстрагироваться от реальных физических, химически,
        механических свойств предметов, а с другой —представлять и воспринимать
        характеристики реальных явлений или объектов, стоящих за знаками. Чтобы успешно
        работать в какой-нибудь профессии данного типа, необходимо уметь мысленно
        погружаться в мир, казалось бы, сухих обозначений и сосредотачиваться на
        сведениях, которые они несут в себе. Особые требования профессии этого типа
        предъявляют к вниманию.
        """, 'Человек-художественный образ': """Человек-художественный образ.\n
        Важнейшие требования, которые предъявляют профессии, связанные с изобразительной, музыкальной, литературно-художественной, актерско-сценической деятельностью человека—
        Наличие способности к искусствам, творческое воображение, образное мышление, талант, трудолюбие.
        """}

        base_df[f'Необработанное'] = answers_df.apply(processing_result_ddo, axis=1)
        # обрабатываем результаты и получаем ключ с максимальным значением
        base_df[f'Обработанное'] = base_df[f'Необработанное'].apply(
            extract_key_max_value)
        base_df[f'Максимум'] = base_df[f'Необработанное'].apply(extract_max_value)
        base_df[f'Описание_результата'] = base_df[f'Обработанное'].apply(lambda x:create_out_str_ddo(x,dct_desciprion,dct_prof))

        # Создаем датафрейм для создания части в общий датафрейм
        part_df = pd.DataFrame(columns=['ДДО_Необработанное', 'ДДО_Обработанное','ДДО_Максимум'])
        part_df['ДДО_Необработанное'] = base_df['Необработанное']
        part_df['ДДО_Обработанное'] = base_df['Обработанное']
        part_df['ДДО_Максимум'] = base_df['Максимум']
        part_df['ДДО_Описание_результата'] = base_df[f'Описание_результата']

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
                Обрабатываем Группа
                """
        # Среднее по Группа
        svod_group_df = pd.pivot_table(base_df, index=['Группа', 'Обработанное'],
                                       values=['Максимум'],
                                       aggfunc=round_mean)
        svod_group_df.reset_index(inplace=True)

        svod_group_df.sort_values(by='Группа', key=lambda x: x.map(sort_name_class), inplace=True)  # сортируем

        # Количество Группа
        svod_count_group_df = pd.pivot_table(base_df, index=['Группа'],
                                                 columns='Обработанное',
                                                 values='Максимум',
                                                 aggfunc='count', margins=True, margins_name='Итого')
        svod_count_group_df.reset_index(inplace=True)
        svod_count_group_df = svod_count_group_df.reindex(
            columns=['Группа', 'Человек-природа', 'Человек-техника',
                 'Человек-человек', 'Человек-знаковые системы',
                 'Человек-художественный образ',
                 'Итого'])
        svod_count_group_df['% Человек-природа от общего'] = round(
            svod_count_group_df['Человек-природа'] / svod_count_group_df['Итого'], 2) * 100
        svod_count_group_df['% Человек-техника от общего'] = round(
            svod_count_group_df['Человек-техника'] / svod_count_group_df['Итого'], 2) * 100
        svod_count_group_df['% Человек-человек от общего'] = round(
            svod_count_group_df['Человек-человек'] / svod_count_group_df['Итого'], 2) * 100
        svod_count_group_df['% Человек-знаковые системы от общего'] = round(
            svod_count_group_df['Человек-знаковые системы'] / svod_count_group_df['Итого'], 2) * 100
        svod_count_group_df['% Человек-художественный образ от общего'] = round(
            svod_count_group_df['Человек-художественный образ'] / svod_count_group_df['Итого'], 2) * 100

        part_svod_df = svod_count_group_df.iloc[:-1:]
        part_svod_df.sort_values(by='Группа', key=lambda x: x.map(sort_name_class), inplace=True)  # сортируем
        itog_svod_df = svod_count_group_df.iloc[-1:]
        svod_count_group_df = pd.concat([part_svod_df, itog_svod_df])

        # Среднее по Группа Пол
        svod_group_sex_df = pd.pivot_table(base_df, index=['Группа', 'Пол', 'Обработанное'],
                                           values=['Максимум'],
                                           aggfunc=round_mean)
        svod_group_sex_df.reset_index(inplace=True)

        svod_group_sex_df.sort_values(by='Группа', key=lambda x: x.map(sort_name_class), inplace=True)  # сортируем

        # Количество Группа Пол
        svod_count_group_sex_df = pd.pivot_table(base_df, index=['Группа', 'Пол'],
                                                 columns='Обработанное',
                                                 values='Максимум',
                                                 aggfunc='count', margins=True, margins_name='Итого')
        svod_count_group_sex_df.reset_index(inplace=True)
        svod_count_group_sex_df = svod_count_group_sex_df.reindex(
            columns=['Группа', 'Человек-природа', 'Человек-техника',
                 'Человек-человек', 'Человек-знаковые системы',
                 'Человек-художественный образ',
                 'Итого'])
        svod_count_group_sex_df['% Человек-природа от общего'] = round(
            svod_count_group_sex_df['Человек-природа'] / svod_count_group_sex_df['Итого'], 2) * 100
        svod_count_group_sex_df['% Человек-техника от общего'] = round(
            svod_count_group_sex_df['Человек-техника'] / svod_count_group_sex_df['Итого'], 2) * 100
        svod_count_group_sex_df['% Человек-человек от общего'] = round(
            svod_count_group_sex_df['Человек-человек'] / svod_count_group_sex_df['Итого'], 2) * 100
        svod_count_group_sex_df['% Человек-знаковые системы от общего'] = round(
            svod_count_group_sex_df['Человек-знаковые системы'] / svod_count_group_sex_df['Итого'], 2) * 100
        svod_count_group_sex_df['% Человек-художественный образ от общего'] = round(
            svod_count_group_sex_df['Человек-художественный образ'] / svod_count_group_sex_df['Итого'], 2) * 100

        part_svod_df = svod_count_group_sex_df.iloc[:-1:]
        part_svod_df.sort_values(by='Группа', key=lambda x: x.map(sort_name_class), inplace=True)  # сортируем
        itog_svod_df = svod_count_group_sex_df.iloc[-1:]
        svod_count_group_sex_df = pd.concat([part_svod_df, itog_svod_df])

        """
                Обрабатываем Курс
                """
        # Среднее по Курс
        svod_course_df = pd.pivot_table(base_df, index=['Курс', 'Обработанное'],
                                        values=['Максимум'],
                                        aggfunc=round_mean)
        svod_course_df.reset_index(inplace=True)

        # Количество Курс
        svod_count_course_df = pd.pivot_table(base_df, index=['Курс'],
                                              columns='Обработанное',
                                              values='Максимум',
                                              aggfunc='count', margins=True, margins_name='Итого')
        svod_count_course_df.reset_index(inplace=True)
        svod_count_course_df = svod_count_course_df.reindex(
            columns=['Курс', 'Человек-природа', 'Человек-техника',
                     'Человек-человек', 'Человек-знаковые системы',
                     'Человек-художественный образ',
                     'Итого'])
        svod_count_course_df['% Человек-природа от общего'] = round(
            svod_count_course_df['Человек-природа'] / svod_count_course_df['Итого'], 2) * 100
        svod_count_course_df['% Человек-техника от общего'] = round(
            svod_count_course_df['Человек-техника'] / svod_count_course_df['Итого'], 2) * 100
        svod_count_course_df['% Человек-человек от общего'] = round(
            svod_count_course_df['Человек-человек'] / svod_count_course_df['Итого'], 2) * 100
        svod_count_course_df['% Человек-знаковые системы от общего'] = round(
            svod_count_course_df['Человек-знаковые системы'] / svod_count_course_df['Итого'], 2) * 100
        svod_count_course_df['% Человек-художественный образ от общего'] = round(
            svod_count_course_df['Человек-художественный образ'] / svod_count_course_df['Итого'], 2) * 100

        # Среднее по Курс Пол
        svod_course_sex_df = pd.pivot_table(base_df, index=['Курс', 'Пол', 'Обработанное'],
                                            values=['Максимум'],
                                            aggfunc=round_mean)
        svod_course_sex_df.reset_index(inplace=True)

        # Количество Курс Пол
        svod_count_course_sex_df = pd.pivot_table(base_df, index=['Курс', 'Пол'],
                                                  columns='Обработанное',
                                                  values='Максимум',
                                                  aggfunc='count', margins=True, margins_name='Итого')
        svod_count_course_sex_df.reset_index(inplace=True)
        svod_count_course_sex_df = svod_count_course_sex_df.reindex(
            columns=['Курс', 'Человек-природа', 'Человек-техника',
                     'Человек-человек', 'Человек-знаковые системы',
                     'Человек-художественный образ',
                     'Итого'])
        svod_count_course_sex_df['% Человек-природа от общего'] = round(
            svod_count_course_sex_df['Человек-природа'] / svod_count_course_sex_df['Итого'], 2) * 100
        svod_count_course_sex_df['% Человек-техника от общего'] = round(
            svod_count_course_sex_df['Человек-техника'] / svod_count_course_sex_df['Итого'], 2) * 100
        svod_count_course_sex_df['% Человек-человек от общего'] = round(
            svod_count_course_sex_df['Человек-человек'] / svod_count_course_sex_df['Итого'], 2) * 100
        svod_count_course_sex_df['% Человек-знаковые системы от общего'] = round(
            svod_count_course_sex_df['Человек-знаковые системы'] / svod_count_course_sex_df['Итого'], 2) * 100
        svod_count_course_sex_df['% Человек-художественный образ от общего'] = round(
            svod_count_course_sex_df['Человек-художественный образ'] / svod_count_course_sex_df['Итого'], 2) * 100

        # формируем словарь
        out_dct = {'Списочный результат': base_df, 'Список для проверки': out_answer_df,
                   'Общий свод':svod_all_df,
                   'Среднее Группа': svod_group_df,'Количество Группа': svod_count_group_df,
                   'Среднее Группа Пол': svod_group_sex_df,'Количество Группа Пол': svod_count_group_sex_df,
                   'Среднее Курс': svod_course_df, 'Количество Курс': svod_count_course_df,
                   'Среднее Курс Пол': svod_course_sex_df, 'Количество Курс Пол': svod_count_course_sex_df,
                   }

        return out_dct, part_df
    except BadValueDDO:
        messagebox.showerror('Лахеcис',
                             f'При обработке вопросов теста Дифференциально-диагностический опросник обнаружены неправильные варианты ответов. Проверьте ответы на указанных строках:\n'
                             f'{error_message}\n'
                             f'Используйте при создании Яндекс-формы написание вариантов ответа из руководства пользователя программы Лахесис.')


    except BadCountColumnsDDO:
        messagebox.showerror('Лахеcис',
                             f'Проверьте количество колонок с ответами на тест Дифференциально-диагностический опросник\n'
                             f'Должно быть 20 колонок с ответами')
