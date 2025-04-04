""""
Скрипт для обработки теста Карта интересов Голомштока в редакции Азбеля
"""
import pandas as pd
from tkinter import messagebox
from lachesis_support_functions import round_mean,sort_name_class


class BadOrderMIGA(Exception):
    """
    Исключение для обработки случая когда колонки не совпадают
    """
    pass


class BadValueMIGA(Exception):
    """
    Исключение для неправильных значений в вариантах ответов
    """
    pass


class BadCountColumnsMIGA(Exception):
    """
    Исключение для обработки случая если количество колонок не равно 144
    """
    pass

def calc_level_miga(value):
    """
    Функция для подсчета уровня склонности к то или иной сфере
    """
    if -12 <= value <= -6:
        return 'область деятельности активно отрицается'
    elif -5 <= value <= 0:
        return 'область деятельности интереса не вызывает'
    elif 1 <= value <= 4:
        return 'интерес выражен слабо'
    elif 5 <= value <= 7:
        return 'выраженный интерес'
    elif 8 <= value <= 12:
        return 'ярко выраженный интерес'






def calc_mean(df:pd.DataFrame,type_calc:str,lst_cat:list,val_cat):
    """
    Функция для создания сводных датафреймов

    :param df: датафрейм с данными
    :param type_calc:тип обработки Класс или Номер_класса
    :param lst_cat:список колонок по которым будет формироваться свод
    :param val_cat:значение по которому будет формиваться свод
    :return:датафрейм
    """
    if type_calc == 'Класс':
        calc_mean_df = pd.pivot_table(df, index=lst_cat,
                                           values=[val_cat],
                                           aggfunc=round_mean)
        calc_mean_df.reset_index(inplace=True)
        calc_mean_df.sort_values(by='Класс', key=lambda x: x.map(sort_name_class), inplace=True)  # сортируем
        calc_mean_df.rename(columns={val_cat: 'Среднее значение'}, inplace=True)

        return calc_mean_df
    else:
        calc_mean_df = pd.pivot_table(df, index=lst_cat,
                                           values=val_cat,
                                           aggfunc=round_mean)
        calc_mean_df.reset_index(inplace=True)
        calc_mean_df.rename(columns={val_cat:'Среднее значение'},inplace=True)
        return calc_mean_df



def calc_count_sphere_miga(df:pd.DataFrame, type_calc:str, lst_cat:list, val_cat, col_cat):
    """
    Функция для создания сводных датафреймов

    :param df: датафрейм с данными
    :param type_calc:тип обработки Класс или Номер_класса
    :param lst_cat:список колонок по которым будет формироваться свод
    :param val_cat:значение по которому будет формиваться свод
    :param col_cat: колонка по которой будет формироваться свод
    :return:датафрейм
    """
    if type_calc == 'Класс':
        count_df = pd.pivot_table(df, index=lst_cat,
                                                 columns=col_cat,
                                                 values=val_cat,
                                                 aggfunc='count', margins=True, margins_name='Итого')

        lst_sphere = count_df.columns[:-1]
        count_df.reset_index(inplace=True)

        for sphere in lst_sphere:
            count_df[f'% {sphere} от общего'] = round(
            count_df[f'{sphere}'] / count_df['Итого'], 2) * 100


        part_svod_df = count_df.iloc[:-1:]
        part_svod_df.sort_values(by='Класс', key=lambda x: x.map(sort_name_class), inplace=True)  # сортируем
        itog_svod_df = count_df.iloc[-1:]
        count_df = pd.concat([part_svod_df, itog_svod_df])

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



def calc_count_level_miga(df:pd.DataFrame, type_calc:str, lst_cat:list, val_cat, col_cat,lst_cols:list):
    """
    Функция для создания сводных датафреймов

    :param df: датафрейм с данными
    :param type_calc:тип обработки Класс или Номер_класса
    :param lst_cat:список колонок по которым будет формироваться свод
    :param val_cat:значение по которому будет формиваться свод
    :param col_cat: колонка по которой будет формироваться свод
    :param lst_cols: список с колонками
    :return:датафрейм
    """
    if type_calc == 'Класс':
        count_df = pd.pivot_table(df, index=lst_cat,
                                                 columns=col_cat,
                                                 values=val_cat,
                                                 aggfunc='count', margins=True, margins_name='Итого')


        count_df.reset_index(inplace=True)
        count_df = count_df.reindex(columns=lst_cols)
        count_df['% область деятельности активно отрицается от общего'] = round(
            count_df['область деятельности активно отрицается'] / count_df['Итого'], 2) * 100
        count_df['% область деятельности интереса не вызывает от общего'] = round(
            count_df['область деятельности интереса не вызывает'] / count_df['Итого'], 2) * 100
        count_df['% интерес выражен слабо от общего'] = round(
            count_df['интерес выражен слабо'] / count_df['Итого'], 2) * 100
        count_df['% выраженный интерес от общего'] = round(
            count_df['выраженный интерес'] / count_df['Итого'], 2) * 100
        count_df['% ярко выраженный интерес от общего'] = round(
            count_df['ярко выраженный интерес'] / count_df['Итого'], 2) * 100

        part_svod_df = count_df.iloc[:-1:]
        part_svod_df.sort_values(by='Класс', key=lambda x: x.map(sort_name_class), inplace=True)  # сортируем
        itog_svod_df = count_df.iloc[-1:]
        count_df = pd.concat([part_svod_df, itog_svod_df])

        return count_df
    else:
        count_df = pd.pivot_table(df, index=lst_cat,
                                  columns=col_cat,
                                  values=val_cat,
                                  aggfunc='count', margins=True, margins_name='Итого')

        count_df.reset_index(inplace=True)
        count_df = count_df.reindex(columns=lst_cols)
        count_df['% область деятельности активно отрицается от общего'] = round(
            count_df['область деятельности активно отрицается'] / count_df['Итого'], 2) * 100
        count_df['% область деятельности интереса не вызывает от общего'] = round(
            count_df['область деятельности интереса не вызывает'] / count_df['Итого'], 2) * 100
        count_df['% интерес выражен слабо от общего'] = round(
            count_df['интерес выражен слабо'] / count_df['Итого'], 2) * 100
        count_df['% выраженный интерес от общего'] = round(
            count_df['выраженный интерес'] / count_df['Итого'], 2) * 100
        count_df['% ярко выраженный интерес от общего'] = round(
            count_df['ярко выраженный интерес'] / count_df['Итого'], 2) * 100

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


def processing_result_miga(row):
    """
    Обработка результатов тестирования
    """
    dct_cols = {'Биология': [1, 25, 49, 73, 97, 121],
                'Физика': [2, 26, 50, 74, 98, 122],
                'Химия':[3,27,51,75,99,123],
                'География':[4,28,52,76,100,124],
                'Медицина':[5,29,53,77,101,125],
                'Техника и электроника':[6,30,54,78,102,126],
                'Строительство':[7,31,55,79,103,127],
                'Математика':[8,32,56,80,104,128],
                'Экономика':[9,33,57,81,105,129],
                'Иностранные языки':[10,34,58,82,106,130],
                'Транспорт':[11,35,59,83,107,131],
                'Авиация, морское дело':[12,36,60,84,108,132],
                'Военные специальности':[13,37,61,85,109,133],
                'История':[14,38,62,86,110,134],
                'Рабочие специальности':[15,39,63,87,111,135],
                'Журналистика':[16,40,64,88,112,136],
                'Юриспруденция':[17,41,65,89,113,137],
                'Педагогика':[18,42,66,90,114,138],
                'Сфера обслуживания, торговля':[19,43,67,91,115,139],
                'Физкультура и спорт':[20,44,68,92,116,140],
                'Музыка':[21,45,69,93,117,141],
                'Сценическое искусство':[22,46,70,94,118,142],
                'Изобразительное искусство':[23,47,71,95,119,143],
                'Экология':[24,48,72,96,120,144],
                }

    dct_answers = dict() # словарь для результатов

    for key, ind_cols in dct_cols.items():
        prepared_lst = list(map(lambda x:x-1,ind_cols))
        total = sum(row[i] for i in prepared_lst) # получаем сумму выбранных колонок
        dct_answers[key] = total

    result_lst = sorted(dct_answers.items(), key=lambda t: t[1], reverse=True)
    begin_str = ''
    # создаем строку с результатами
    for sphere, value in result_lst:
        begin_str += f'{sphere}: {value};\n'

    return begin_str








def processing_map_interests(base_df: pd.DataFrame, answers_df: pd.DataFrame):
    """
    Функция для обработки результатов тестирования Карта интересов Голомштока в редакции Азбеля
    :return:
    """
    out_answer_df = base_df.copy()  # делаем копию для последующего соединения с сырыми ответами
    if len(answers_df.columns) != 144:
        raise BadCountColumnsMIGA


    lst_check_cols = ['Изучать разнообразие животного и растительного мира','Проводить физические эксперименты',
                      'Разрабатывать новые технологии химического синтеза','Изучать месторождения полезных ископаемых',
                      'Разрабатывать новые методы диагностики и лечения различных болезней','Устанавливать и налаживать работу компьютерных программ',
                      'Следить за последовательностью и технологиями строительных работ','Решать задачки из книг типа «Математические игры», «Занимательная математика»',
                      'Планировать финансовую и производственную деятельность предприятия, фирмы','Помогать делать переводы документации',
                      'Управлять машиной, автобусом, трейлером и т. д.','Заниматься в секции парашютистов, в авиаклубе или заниматься в секции яхтсменов, аквалангистов',
                      'Заниматься в стрелковой секции','Заниматься в историческом клубе, разыгрывать ролевые игры по сюжетам исторических событий',
                      'Изучать устройство и режимы работы станков','Писать статьи, фельетоны, очерки в периодические издания и в Интернет',
                      'Оказывать юридическую помощь людям, консультируя их по вопросам законодательства','Организовывать для ребят игры и праздники',
                      'Консультировать людей при крупных покупках (автомобиль, заграничный тур и т. д.)','Тренировать команду спортсменов',
                      'Работать на музыкальных радиоканалах, составлять списки внесен для звучания в эфире','Сниматься в кино или играть на сцене',
                      'Делать интернет-сайты, веб-страницы','Разрабатывать мероприятия по охране численности редких растений и животных',
                      'Участвовать в биологических экспедициях, посещать биологические секции','Изучать законы природы, находить физические закономерности',
                      'Проводить опыты с различными веществами, следить за ходом химических реакций','Вести наблюдения за изменениями состояния атмосферы',
                      'Читать о том, как люди учились бороться с болезнями и изобретали новые лекарства','Находить и устранять причины сбоя в компьютерах, аппаратуре, приборах',
                      'Набрасывать эскизы или выполнять чертежи различных построек','Соревноваться в решении математических задач',
                      'Выступать посредником при заключении торговых сделок (искать покупателям продавцов и наоборот)','Проводить экскурсии на иностранном языке для гостей нашего города',
                      'Управлять пожарной машиной','Управлять самолетом МЧС или скоростным катером',
                      'Участвовать в военизированных учениях («Зарница», «Разведчик» и др.)','Посещать исторические музеи, изучать исторические памятники разных народов',
                      'Регулировать механизмы и заменять их в случае неисправности','Наблюдать и анализировать события, поступки людей, делать об этом репортажи',
                      'Искать и фиксировать следы на месте преступления','Заниматься репетиторством и преподавательской деятельностью',
                      'Изучать спрос покупателей на определенный товар','Читать специальные спортивные новости в газетах и на сайтах',
                      'Исполнять произведения на музыкальных инструментах с использованием различных техник игры','Изучать основы сценического искусства, творчество знаменитых мастеров сцены',
                      'Искать наиболее рациональное и эстетическое цветовое решение для интерьеров','Проводить наблюдения и контроль загрязнения окружающей среды',
                      'Изучать анатомию и физиологию животных','Собирать установки для проведения физических экспериментов',
                      'В лабораторных условиях определять степень загрязненности почвы химическими веществами','Создавать ландшафтные карты с помощью компьютерных геоинформационных систем',
                      'Интересоваться причинами и способами лечения болезни','Прокладывать сетевые кабели и кабели силового питания',
                      'Изучать новые технологии строительства','Изучать языки программирования на компьютере',
                      'Осуществлять финансовые расчеты между предприятиями','Читать литературу на иностранном языке или смотреть фильмы без перевода',
                      'Управлять современным поездом дальнего следования','Оказывать экстренную помощь людям на терпящих бедствие судах',
                      'Быть военным инженером или командиром','Обсуждать исторические и текущие политические события России и других стран',
                      'Подбирать цветовые оттенки, красить дома, расписывать стены','Добывать эксклюзивную информацию, передавать ее читателям и зрителям',
                      'Контролировать своевременную уплату налогов фирмами и физическими лицами','Обучать маленьких детей, играя с ними',
                      'Встречать и размещать пассажиров в салоне самолета','Тренироваться в профессиональном спортивном клубе',
                      'Играть в музыкальной группе или в оркестре, следуя указаниям дирижера','Вести концертные программы, объявлять зрителям новые номера программы',
                      'Создавать необычные модели одежды','Разрабатывать меры по снижению количества вредных производственных выбросов в окружающую среду',
                      'Разрабатывать средства борьбы с возбудителями заболеваний животных и растений','Изучать процессы взаимодействия элементарных частиц в ядерных реакторах',
                      'Брать на анализ химические пробы воды, продуктов питания, почвы и пр.','Вести разведку месторождений полезных ископаемых: нефти, газа, драгоценных металлов и др.',
                      'Тренироваться в навыках первой медицинской помощи','Проверять, испытывать, регулировать работу узлов автомобиля, самолета, корабля и т. д.',
                      'Готовить растворы, смеси для строительных работ','Разрабатывать программные алгоритмы для выполнения сложных расчетов',
                      'Вести финансовую документацию фирмы, предприятия','Изучать иностранные языки',
                      'Регулировать движение транспортных потоков на улицах города','Оказывать экстренную помощь людям «с воздуха» (например, управляя вертолетом МЧС)',
                      'Изучать устройство оружия, военной техники','Анализировать по книгам исторические факты',
                      'Обеспечивать в домах систему отопления, исправную работу водопровода','Редактировать тексты книг, статей, выступлений высокопоставленных лиц',
                      'Выдвигать обвинения преступникам, назначать им наказания в соответствии с законом','Готовить школьников к олимпиадным заданиям, конкурсам',
                      'Помогать подбирать людям наряды и украшения для торжественных церемоний','Сдавать спортивные нормативы',
                      'Выступать в качестве солиста перед публикой на концертах, в клубах','Подбирать актеров для съемки художественного фильма или рекламного клипа',
                      'Делать фотоснимки, монтировать фотографии с помощью компьютера','Заниматься мониторингом состояния воздуха на оживленных городских магистралях',
                      'Отбирать и заготавливать семена для посадки, высаживать растения в зимних садах','Моделировать на компьютере физические законы природы',
                      'Создавать новые синтетические вещества из нефтепродуктов и других полезных ископаемых','Изучать особенности флоры и фауны различных регионов',
                      'Осуществлять уход за человеком во время его выздоровления после болезни','Заниматься в технической или электротехнической секции (на пример, в авиа- или судомоделировании)',
                      'Изучать качества и условия применения строительных материалов','Писать компьютерные программы на основе анализа математических алгоритмов',
                      'Рассчитывать предполагаемый размер прибыли предприятия','Осуществлять перевод телепередач на русский язык',
                      'Консультировать людей по соблюдению правил дорожного движения','Изучать особенности управления яхтой в штормовую погоду',
                      'Предупреждать незаконное пересечение государственной границы иностранными гражданами','Разыскивать и собирать материалы, свидетельствующие о событиях прошлого',
                      'Обрабатывать и изготовлять металлические детали на фрезерном станке','Работать в средствах массовой информации, вести телепередачи',
                      'Выяснять у людей причины незаконных поступков, которые они скрывают','Организовывать походы для школьников',
                      'Разрабатывать рекламные акции для продвижения товара в магазинах города','Ездить в качестве участника на спортивные соревнования в другой город',
                      'Сочинять музыку для кинофильмов, телепередач, для известных исполнителей','Подготавливать и ставить трюки в кино',
                      'Придумывать оригинальные ювелирные изделия, украшения','Изучать взаимоотношения живых организмов с их средой обитания',
                      'Заниматься дрессировкой служебных собак или других животных','Читать книги тина «Занимательная физика», «Физики шутят» и т. п.',
                      'Управлять технологическими процессами производства лекарств','Участвовать в географических экспедициях',
                      'Работать врачом на станции «Скорой помощи»','Ремонтировать радиоприборы и различную аппаратуру',
                      'Продумывать планировку домов, этажей, квартир. Намечать план строительства','Отражать в виде чисел и формул какие-либо события, процессы или явления',
                      'Заключать сделки, договора на выполнение определенных работ','Изучать происхождение слов и различных словосочетаний в разных языках',
                      'Тренироваться водить машину или мотоцикл для подготовки к гонке','Изучать особенности управления легким самолетом в ветреную погоду',
                      'Жить согласно уставу, носить военную форму','Участвовать в археологических экспедициях, работать на раскопках',
                      'Делать из дерева различные предметы, мебель и пр.','Осуществлять литературную обработку статей в соответствии с жанровым своеобразием',
                      'Продумывать новые законы и поправки в кодексы, которые были бы удобны для применения','Руководить одной из секций в доме детского творчества',
                      'Помогать человеку улучшить внешность с помощью прически, макияжа, подбора красивой одежды и т. п.','Осуществлять честное и грамотное судейство на спортивных соревнованиях',
                      'Изучать творчество выдающихся композиторов, поэтов песен и исполнителей','Создавать творческие проекты, «раскручивать» исполнителей',
                      'Заниматься дизайном интерьеров','Следить за качеством воды, поступающей в городскую водопроводную сеть'
                      ]

    # Проверяем порядок колонок
    order_main_columns = lst_check_cols  # порядок колонок и названий как должно быть
    order_temp_df_columns = list(answers_df.columns)  # порядок колонок проверяемого файла
    error_order_lst = []  # список для несовпадающих пар
    # Сравниваем попарно колонки
    for main, temp in zip(order_main_columns, order_temp_df_columns):
        if main != temp:
            error_order_lst.append(f'На месте колонки {main} находится колонка {temp}')
            error_order_message = ';'.join(error_order_lst)
    if len(error_order_lst) != 0:
        raise BadOrderMIGA

    # словарь для замены слов на числа
    dct_replace_value = {'очень хотелось бы, нравится этим заниматься': 2,
                         'нравится, но не очень сильно': 1,
                         'затрудняюсь ответить': 0,
                         'не хотелось бы, не нравится': -1,
                         'очень не хотелось бы, совершенно не нравится': -2}

    valid_values = [-2, -1, 0, 1, 2]
    answers_df.replace(dct_replace_value, inplace=True)  # заменяем слова на цифры для подсчетов

    # Проверяем, есть ли значения, отличающиеся от указанных в списке
    mask = ~answers_df.isin(valid_values)

    # Получаем строки с отличающимися значениями
    result_check = answers_df[mask.any(axis=1)]
    if len(result_check) != 0:
        error_row = list(map(lambda x: x + 2, result_check.index))
        error_row = list(map(str, error_row))
        error_message = ';'.join(error_row)
        raise BadValueMIGA





    base_df[f'Необработанное'] = answers_df.apply(processing_result_miga, axis=1)
    base_df[f'Обработанное'] = base_df[f'Необработанное'].apply(
        extract_key_max_value)
    base_df[f'Максимум'] = base_df[f'Необработанное'].apply(
        extract_max_value)
    base_df[f'Уровень'] = base_df[f'Максимум'].apply(
        calc_level_miga)



    # Создаем датафрейм для создания части в общий датафрейм
    part_df = pd.DataFrame(columns=['КИ_Голомшток_Необработанное', 'КИ_Голомшток_Обработанное', 'КИ_Голомшток_Максимум','КИ_Голомшток_Уровень'])
    part_df['КИ_Голомшток_Необработанное'] = base_df['Необработанное']
    part_df['КИ_Голомшток_Обработанное'] = base_df['Обработанное']
    part_df['КИ_Голомшток_Максимум'] = base_df['Максимум']
    part_df['КИ_Голомшток_Уровень'] = base_df['Уровень']


    base_df.sort_values(by='Максимум', ascending=False, inplace=True)  # сортируем
    out_answer_df = pd.concat([out_answer_df, answers_df], axis=1)  # Датафрейм для проверки

    # Общий свод по уровням склонности всего в процентном соотношении
    base_svod_all_df = pd.DataFrame(
        index=['область деятельности активно отрицается', 'область деятельности интереса не вызывает', 'интерес выражен слабо',
               'выраженный интерес','ярко выраженный интерес', 'Итого'])

    svod_level_df = pd.pivot_table(base_df, index='Уровень',
                                 values='Максимум',
                                 aggfunc='count')

    svod_level_df['% от общего'] = round(
        svod_level_df['Максимум'] / svod_level_df['Максимум'].sum(), 3) * 100

    base_svod_all_df = base_svod_all_df.join(svod_level_df)

    # # Создаем суммирующую строку
    base_svod_all_df.loc['Итого'] = svod_level_df.sum()
    base_svod_all_df.reset_index(inplace=True)
    base_svod_all_df.rename(columns={'index': 'Уровень склонности', 'Максимум': 'Количество'}, inplace=True)

    # Создаем строку с описанием
    description_result = """
    Шкала оценки результатов
    от -12 до -6 баллов – сфера деятельности активно отрицается («Что угодно, только не это!»);;
    от-5 до 0 баллов – область деятельности интереса не вызывает;
    от 1 до 4 баллов – интерес выражен слабо;
    от 5 до 7 баллов – выраженный интерес;
    от 8 до 12 баллов – ярко выраженный интерес.
    """

    # создаем описание результата
    base_df[f'Описание_результата'] = 'Карта интересов Голомшток.\n'+description_result + base_df[
        f'Необработанное']
    part_df['КИ_Голомшток_Описание_результата'] = base_df[f'Описание_результата']

    # формируем основной словарь
    out_dct = {'Списочный результат': base_df, 'Список для проверки': out_answer_df,
               'Свод по уровням': base_svod_all_df,
               }



    lst_level = ['область деятельности активно отрицается', 'область деятельности интереса не вызывает', 'интерес выражен слабо',
               'выраженный интерес','ярко выраженный интерес']
    dct_level = dict()

    for level in lst_level:
        temp_df = base_df[base_df['Уровень'] == level]
        if temp_df.shape[0] !=0:
            if level == 'область деятельности активно отрицается':
                level = ' сфера активно отрицается'
            elif level == 'область деятельности интереса не вызывает':
                level = ' сфера интереса не вызывает'
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
    svod_sphere_df.rename(columns={'index': 'Предпочтительная сфера деятельности', 'Максимум': 'Количество'}, inplace=True)

    # формируем списки по сферам деятельности
    lst_sphere = base_df['Обработанное'].unique()
    lst_sphere.sort() # сортируем
    dct_sphere = {'Свод по сферам': svod_sphere_df} # словарь для хранения списков

    for sphere in lst_sphere:
        temp_df = base_df[base_df['Обработанное'] == sphere]
        dct_sphere[sphere] = temp_df


    out_dct.update(dct_sphere)
    """
    Своды 
    """
    lst_reindex_group_cols = ['Класс','область деятельности активно отрицается', 'область деятельности интереса не вызывает', 'интерес выражен слабо',
               'выраженный интерес','ярко выраженный интерес' ,'Итого']
    lst_reindex_group_sex_cols = ['Класс','Пол','область деятельности активно отрицается', 'область деятельности интереса не вызывает', 'интерес выражен слабо',
               'выраженный интерес','ярко выраженный интерес' ,'Итого']

    lst_reindex_course_cols = ['Номер_класса','область деятельности активно отрицается', 'область деятельности интереса не вызывает', 'интерес выражен слабо',
               'выраженный интерес','ярко выраженный интерес' ,'Итого']
    lst_reindex_course_sex_cols = ['Номер_класса','Пол','область деятельности активно отрицается', 'область деятельности интереса не вызывает', 'интерес выражен слабо',
               'выраженный интерес','ярко выраженный интерес' ,'Итого']


    # Своды по уровням
    # Класс
    svod_group_level_df = calc_mean(base_df, 'Класс', ['Класс', 'Уровень'], 'Максимум')
    svod_count_group_level_df = calc_count_level_miga(base_df, 'Класс', ['Класс'], 'Максимум', 'Уровень',
                                                      lst_reindex_group_cols)

    # Класс Пол
    svod_group_level_sex_df = calc_mean(base_df, 'Класс', ['Класс', 'Уровень', 'Пол'], 'Максимум')
    svod_count_group_level_sex_df = calc_count_level_miga(base_df, 'Класс', ['Класс', 'Пол'], 'Максимум', 'Уровень',
                                                          lst_reindex_group_sex_cols)

    # Номер_класса
    svod_course_level_df = calc_mean(base_df, 'Номер_класса', ['Номер_класса', 'Уровень'], 'Максимум')
    svod_count_course_level_df = calc_count_level_miga(base_df, 'Номер_класса', ['Номер_класса'], 'Максимум',
                                                       'Уровень', lst_reindex_course_cols)

    # Номер_класса Пол
    svod_course_level_sex_df = calc_mean(base_df, 'Номер_класса', ['Номер_класса', 'Уровень', 'Пол'], 'Максимум')
    svod_count_course_level_sex_df = calc_count_level_miga(base_df, 'Номер_класса', ['Номер_класса', 'Пол'],
                                                           'Максимум',
                                                           'Уровень', lst_reindex_course_sex_cols)


    # Своды по сферам
    # Класс
    svod_group_sphere_df = calc_mean(base_df,'Класс',['Класс','Обработанное'],'Максимум')
    svod_count_group_sphere_df = calc_count_sphere_miga(base_df, 'Класс', ['Класс'], 'Максимум', 'Обработанное')

    # Класс Пол
    svod_group_sphere_sex_df = calc_mean(base_df,'Класс',['Класс','Обработанное','Пол'],'Максимум')
    svod_count_group_sphere_sex_df = calc_count_sphere_miga(base_df, 'Класс', ['Класс', 'Пол'], 'Максимум', 'Обработанное')

    # Номер_класса
    svod_course_sphere_df = calc_mean(base_df,'Номер_класса',['Номер_класса','Обработанное'],'Максимум')
    svod_count_course_sphere_df = calc_count_sphere_miga(base_df, 'Номер_класса', ['Номер_класса'], 'Максимум', 'Обработанное')

    # Номер_класса Пол
    svod_course_sphere_sex_df = calc_mean(base_df,'Номер_класса',['Номер_класса','Обработанное','Пол'],'Максимум')
    svod_count_course_sphere_sex_df = calc_count_sphere_miga(base_df, 'Номер_класса', ['Номер_класса', 'Пол'], 'Максимум', 'Обработанное')








    svod_dct =  {'Ср. Уровень Класс':svod_group_level_df,'Кол. Уровень Класс':svod_count_group_level_df,
                 'Ср. Уровень Класс Пол':svod_group_level_sex_df,'Кол. Уровень Класс Пол':svod_count_group_level_sex_df,
                 'Ср. Уровень Номер_класса': svod_course_level_df, 'Кол. Уровень Номер_класса': svod_count_course_level_df,
                 'Ср. Уровень Номер_класса Пол': svod_course_level_sex_df, 'Кол. Уровень Номер_класса Пол': svod_count_course_level_sex_df,

                 'Ср. Сфера Класс':svod_group_sphere_df,'Кол. Сфера Класс':svod_count_group_sphere_df,
                 'Ср. Сфера Класс Пол':svod_group_sphere_sex_df,'Кол. Сфера Класс Пол':svod_count_group_sphere_sex_df,
                 'Ср. Сфера Номер_класса': svod_course_sphere_df, 'Кол. Сфера Номер_класса': svod_count_course_sphere_df,
                 'Ср. Сфера Номер_класса Пол': svod_course_sphere_sex_df, 'Кол. Сфера Номер_класса Пол': svod_count_course_sphere_sex_df,

                 }
    out_dct.update(svod_dct) # добавляем чтобы сохранить порядок

    return out_dct, part_df



