"""
Скрипт для обработки результатов теста ДДО
"""
import pandas as pd
from tkinter import messagebox
from lachesis_support_functions import round_mean, sort_name_class


class BadValueDDO(Exception):
    """
    Исключение для неправильных значений в вариантах ответов
    """
    pass


class BadCountColumnsDDO(Exception):
    """
    Исключение для обработки случая если количество колонок не равно 30
    """
    pass


def extract_key_max_value(cell: str) -> str:
    """
    Функция для извлечения ключа с максимальным значением
    :param cell: строка формата ключ - значение;
    :return: ключ словаря в формате строки
    """
    # проверяем если некорректное значение
    if 'Скопируйте правильные значения для указанных вопросов из квадратных скобок' in cell:
        return cell
    dct_result = {}
    cell = cell.replace('\n', '')  # убираем переносы
    lst_temp = cell.split(';')  # сплитим по точке с запятой
    for result in lst_temp:
        # отбрасываем пустую строку
        if result:
            key, value = result.split(' - ')  # извлекаем ключ и значение
            dct_result[key] = int(value)

    # возвращаем элемент с максимальным значением
    return max(dct_result, key=dct_result.get)


def extract_max_value(cell: str):
    """
    Функция для извлечения значения ключа с максимальным значением , ха звучит странно
    :param cell: строка формата ключ - значение;
    :return: ключ словаря в формате строки
    """
    # проверяем если некорректное значение
    if 'Скопируйте правильные значения для указанных вопросов из квадратных скобок' in cell:
        return 0
    dct_result = {}
    cell = cell.replace('\n', '')  # убираем переносы
    lst_temp = cell.split(';')  # сплитим по точке с запятой
    for result in lst_temp:
        # отбрасываем пустую строку
        if result:
            key, value = result.split(' - ')  # извлекаем ключ и значение
            dct_result[key] = int(value)

    # возвращаем элемент с максимальным значением
    return dct_result[max(dct_result, key=dct_result.get)]


def create_out_str_ddo(x, dct_desciprion, dct_prof):
    """
    Функция для создания выходной строки ДДО
    """
    return f'{dct_desciprion.get(x, "Проверьте правильность написания ответа в форме,в колонке ДДО_Обработанный_результат указаны несовпадающие значения")}\nРекомендуемые профессии:\n{dct_prof.get(x, "Проверьте правильность написания ответа в форме,в колонке ДДО_Обработанный_результат указаны несовпадающие значения")}'


def processing_result_ddo(row):
    """
    Обработка результатов тестирования ДДО
    """

    # # Создаем словарь для хранения данных
    dct_type = {'Человек-природа': 0, 'Человек-техника': 0, 'Человек-другой человек': 0, 'Человек-знаковая система': 0,
                'Человек-художественный образ': 0, 'Сам человек': 0}
    # # 1
    if row[0] == 'Выращивать и дрессировать служебных собак для поиска наркотиков':
        dct_type['Человек-природа'] += 1
    elif row[0] == 'Разрабатывать новые модели электронной бытовой техники':
        dct_type['Человек-техника'] += 1
    # 2
    if row[1] == 'Спасать людей после аварии и землетрясения':
        dct_type['Человек-другой человек'] += 1
    elif row[1] == 'Заверять документы, оформлять доверенности, договоры':
        dct_type['Человек-знаковая система'] += 1
    #
    # 3
    if row[2] == 'Петь в музыкальной группе':
        dct_type['Человек-художественный образ'] += 1
    elif row[2] == 'Интенсивно тренироваться, совершенствоваться и добиваться новых спортивных результатов':
        dct_type['Сам человек'] += 1

    # # 4
    if row[3] == 'Налаживать работу компьютеров и оборудования':
        dct_type['Человек-техника'] += 1
    elif row[3] == 'Рассказывать о товаре, убеждать людей приобретать его':
        dct_type['Человек-другой человек'] += 1
    #
    # 5
    if row[4] == 'Переводить научные тексты':
        dct_type['Человек-знаковая система'] += 1
    elif row[4] == 'Писать рассказы, сценарии, фельетоны':
        dct_type['Человек-художественный образ'] += 1
    # 6
    if row[5] == 'Тренировать свой организм, чтобы он выдерживал воздействие больших физических нагрузок':
        dct_type['Сам человек'] += 1
    elif row[
        5] == 'Разрабатывать мероприятия по охране редких растений':
        dct_type['Человек-природа'] += 1

    # # 7
    if row[6] == 'Ремонтировать оргтехнику, компьютеры, телефоны':
        dct_type['Человек-техника'] += 1
    elif row[
        6] == 'Исправлять смысловые и стилистические ошибки в готовящихся к печати текстах':
        dct_type['Человек-знаковая система'] += 1

    # 8
    if row[7] == 'Заниматься флористикой, оформлять помещения цветами':
        dct_type['Человек-художественный образ'] += 1
    elif row[7] == 'Анализировать состояние растений и животных в загрязненных условиях среды':
        dct_type['Человек-природа'] += 1

    # 9
    if row[8] == 'Управлять автомобилем, автобусом, трейлером, локомотивом поезда':
        dct_type['Человек-техника'] += 1
    elif row[8] == 'Микшировать музыку или корректировать фотоснимки с помощью компьютера':
        dct_type['Человек-художественный образ'] += 1

    # 10
    if row[
        9] == 'Ежедневно тренировать свои атлетические навыки в спортивном зале, в бассейне, на стадионе, корте и т. д.':
        dct_type['Сам человек'] += 1
    elif row[9] == 'Отлаживать работу спортивного автомобиля и заменять механизмы в случае неисправности':
        dct_type['Человек-техника'] += 1

    # 11
    if row[10] == 'Давать людям консультации по туристическим маршрутам других городов и стран':
        dct_type['Человек-другой человек'] += 1
    elif row[10] == 'Оформлять витрины универмагов; заниматься оформлением концертов и шоу':
        dct_type['Человек-художественный образ'] += 1

    # 12
    if row[11] == 'Разводить декоративных рыб и ухаживать за аквариумами в офисах':
        dct_type['Человек-природа'] += 1
    elif row[11] == 'Оказывать людям медицинскую помощь':
        dct_type['Человек-другой человек'] += 1

    # 13
    if row[12] == 'Упорядочивать документацию фирмы и подготавливать новую (договора, счета, ведомости, доверенности)':
        dct_type['Человек-знаковая система'] += 1
    elif row[
        12] == 'Вырабатывать навыки красивой походки и пластичных движений для профессионального выступления на подиуме':
        dct_type['Сам человек'] += 1

    # 14
    if row[13] == 'Изучать генетику, выводить новые сорта растений':
        dct_type['Человек-природа'] += 1
    elif row[13] == 'Работать в фондах архивов, находить необходимые документы':
        dct_type['Человек-знаковая система'] += 1

    # 15
    if row[14] == 'Сопровождать людей в сложных туристических походах в роли инструктора':
        dct_type['Человек-другой человек'] += 1
    elif row[14] == 'Придумывать и отрабатывать сложные акробатические трюки, спортивные номера':
        dct_type['Сам человек'] += 1

    # 16
    if row[15] == 'Лечить кошек, собак, лошадей и пр.':
        dct_type['Человек-природа'] += 1
    elif row[15] == 'Осуществлять сборку компьютеров':
        dct_type['Человек-техника'] += 1

    # 17
    if row[16] == 'Искать нужных людей, проводить подбор персонала в различные фирмы':
        dct_type['Человек-другой человек'] += 1
    elif row[16] == 'Проводить финансовый анализ рынка ценных бумаг':
        dct_type['Человек-знаковая система'] += 1

    # 18
    if row[17] == 'Играть на сцене, сниматься в кино, ставить трюки':
        dct_type['Человек-художественный образ'] += 1
    elif row[17] == 'Тренировать и репетировать красивые и точные движения перед спортивным выступлением':
        dct_type['Сам человек'] += 1

    # 19
    if row[18] == 'Налаживать работу медицинского лазера, ультразвуковой аппаратуры':
        dct_type['Человек-техника'] += 1
    elif row[18] == 'Преподавать различные предметы в школе, техникуме, институте и т. д.':
        dct_type['Человек-другой человек'] += 1

    # 20
    if row[19] == 'Рассчитывать экономный путь транспортировки товара до потребителя':
        dct_type['Человек-знаковая система'] += 1
    elif row[19] == 'Оформлять иллюстрациями сайты, книги, журналы':
        dct_type['Человек-художественный образ'] += 1

    # 21
    if row[19] == 'Осуществлять постоянную психологическую и физическую подготовку к соревнованиям, турнирам':
        dct_type['Сам человек'] += 1
    elif row[19] == 'Участвовать в экспедициях, посвященных изучению природных явлений':
        dct_type['Человек-природа'] += 1

    # 22
    if row[19] == 'Строить дома по планам, делать разводку электричества в соответствии с проектом':
        dct_type['Человек-техника'] += 1
    elif row[19] == 'Работать с финансовыми законами и кодексами':
        dct_type['Человек-знаковая система'] += 1

    # 23
    if row[19] == 'Проектировать садово-парковые зоны, оформлять участки с помощью растений':
        dct_type['Человек-художественный образ'] += 1
    elif row[19] == 'Анализировать молекулярный состав крови':
        dct_type['Человек-природа'] += 1

    # 24
    if row[19] == 'Проектировать новое производственное оборудование, дома':
        dct_type['Человек-техника'] += 1
    elif row[19] == 'Производить архитектурно восстановительные работы исторических мест':
        dct_type['Человек-художественный образ'] += 1

    # 25
    if row[19] == 'Оттачивать мастерство выполнения спортивного упражнения, превозмогая усталость и страх':
        dct_type['Сам человек'] += 1
    elif row[19] == 'Разрабатывать новые модели спортивных тренажеров, велосипедов и другое спортивное оборудование':
        dct_type['Человек-техника'] += 1

    # 26
    if row[19] == 'Организовывать праздники, выступать в роли тамады':
        dct_type['Человек-знаковая система'] += 1
    elif row[19] == 'Вести концертные программы, объявлять зрителям имена выступающих и названия номеров':
        dct_type['Человек-художественный образ'] += 1

    # 27
    if row[19] == 'Изучать жизнь организмов с помощью электронного микроскопа':
        dct_type['Человек-природа'] += 1
    elif row[19] == 'Оказывать людям психологическую помощь, работая на телефоне доверия':
        dct_type['Человек-другой человек'] += 1

    # 28
    if row[19] == 'Обрабатывать, анализировать и обобщать социологические данные':
        dct_type['Человек-знаковая система'] += 1
    elif row[19] == 'Профессионально работать над красотой своей фигуры и внешности':
        dct_type['Сам человек'] += 1

    # 29
    if row[19] == 'Разрабатывать средства защиты растений от вредителей и вирусов':
        dct_type['Человек-природа'] += 1
    elif row[19] == 'Писать компьютерные программы':
        dct_type['Человек-знаковая система'] += 1

    # 30
    if row[19] == 'Консультировать людей в фитнес-зале, в бассейне, на спортивной площадке':
        dct_type['Человек-другой человек'] += 1
    elif row[19] == 'Тренировать общую выносливость и совершенствовать отдельные спортивные или артистические навыки':
        dct_type['Сам человек'] += 1

    # сортируем по убыванию
    result_lst = sorted(dct_type.items(), key=lambda t: t[1], reverse=True)
    begin_str = '\n'
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
        if answers_df.shape[1] != 30:
            raise BadCountColumnsDDO
        # Переименовываем колонки
        answers_df.columns = [f'Вопрос_ №{i}' for i in range(1, 31)]

        valid_values = ['Выращивать и дрессировать служебных собак для поиска наркотиков',
                        'Разрабатывать новые модели электронной бытовой техники',
                        'Спасать людей после аварии и землетрясения',
                        'Заверять документы, оформлять доверенности, договоры',
                        'Петь в музыкальной группе',
                        'Интенсивно тренироваться, совершенствоваться и добиваться новых спортивных результатов',
                        'Налаживать работу компьютеров и оборудования',
                        'Рассказывать о товаре, убеждать людей приобретать его',
                        'Переводить научные тексты', 'Писать рассказы, сценарии, фельетоны',
                        'Тренировать свой организм, чтобы он выдерживал воздействие больших физических нагрузок',
                        'Разрабатывать мероприятия по охране редких растений',
                        'Ремонтировать оргтехнику, компьютеры, телефоны',
                        'Исправлять смысловые и стилистические ошибки в готовящихся к печати текстах',
                        'Заниматься флористикой, оформлять помещения цветами',
                        'Анализировать состояние растений и животных в загрязненных условиях среды',
                        'Управлять автомобилем, автобусом, трейлером, локомотивом поезда',
                        'Микшировать музыку или корректировать фотоснимки с помощью компьютера',
                        'Ежедневно тренировать свои атлетические навыки в спортивном зале, в бассейне, на стадионе, корте и т. д.',
                        'Отлаживать работу спортивного автомобиля и заменять механизмы в случае неисправности',

                        'Давать людям консультации по туристическим маршрутам других городов и стран',
                        'Оформлять витрины универмагов; заниматься оформлением концертов и шоу',
                        'Разводить декоративных рыб и ухаживать за аквариумами в офисах',
                        'Оказывать людям медицинскую помощь',
                        'Упорядочивать документацию фирмы и подготавливать новую (договора, счета, ведомости, доверенности)',
                        'Вырабатывать навыки красивой походки и пластичных движений для профессионального выступления на подиуме',
                        'Изучать генетику, выводить новые сорта растений',
                        'Работать в фондах архивов, находить необходимые документы',
                        'Сопровождать людей в сложных туристических походах в роли инструктора',
                        'Придумывать и отрабатывать сложные акробатические трюки, спортивные номера',
                        'Лечить кошек, собак, лошадей и пр.', 'Осуществлять сборку компьютеров',
                        'Искать нужных людей, проводить подбор персонала в различные фирмы',
                        'Проводить финансовый анализ рынка ценных бумаг',
                        'Играть на сцене, сниматься в кино, ставить трюки',
                        'Тренировать и репетировать красивые и точные движения перед спортивным выступлением',
                        'Налаживать работу медицинского лазера, ультразвуковой аппаратуры',
                        'Преподавать различные предметы в школе, техникуме, институте и т. д.',
                        'Рассчитывать экономный путь транспортировки товара до потребителя',
                        'Оформлять иллюстрациями сайты, книги, журналы',

                        'Осуществлять постоянную психологическую и физическую подготовку к соревнованиям, турнирам',
                        'Участвовать в экспедициях, посвященных изучению природных явлений',
                        'Строить дома по планам, делать разводку электричества в соответствии с проектом',
                        'Работать с финансовыми законами и кодексами',
                        'Проектировать садово-парковые зоны, оформлять участки с помощью растений',
                        'Анализировать молекулярный состав крови',
                        'Проектировать новое производственное оборудование, дома',
                        'Производить архитектурно восстановительные работы исторических мест',
                        'Оттачивать мастерство выполнения спортивного упражнения, превозмогая усталость и страх',
                        'Разрабатывать новые модели спортивных тренажеров, велосипедов и другое спортивное оборудование',
                        'Организовывать праздники, выступать в роли тамады',
                        'Вести концертные программы, объявлять зрителям имена выступающих и названия номеров',
                        'Изучать жизнь организмов с помощью электронного микроскопа',
                        'Оказывать людям психологическую помощь, работая на телефоне доверия',
                        'Обрабатывать, анализировать и обобщать социологические данные',
                        'Профессионально работать над красотой своей фигуры и внешности',
                        'Разрабатывать средства защиты растений от вредителей и вирусов',
                        'Писать компьютерные программы',
                        'Консультировать людей в фитнес-зале, в бассейне, на спортивной площадке',
                        'Тренировать общую выносливость и совершенствовать отдельные спортивные или артистические навыки',
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
            'Человек-природа': 'ветеринар, агроном, гидролог, овощевод, геолог, полевод, егерь, механизатор и т.п.',
            'Человек-техника': 'Водитель, слесарь-ремонтник, наладчик, сталевар, токарь, слесарь-механик, ткач, столяр, пекарь, кондитер,проходчик, шахтер и т.п.',
            'Человек-другой человек': 'Продавец, медсестра, секретарь, бортпроводник, учитель, воспитатель, няня, преподаватель, врач, официант, администратор и т.п.',
            'Человек-знаковая система': 'Программист, кассир, делопроизводитель, бухгалтер, чертежник, корректор, экономист, радист, наборщик и т.п.',
            'Человек-художественный образ': 'Парикмахер, модельер, чеканщик, маляр, гравер, резчик по камню, фотограф, актер, художник, музыкант и т.п.',
            'Сам человек': 'Спортсмен, тренер, модель, и т.п.',
        }

        dct_desciprion = \
            {'Человек-природа': """Человек-природа.\n
Она объединяет все профессии, представители которых имеют дело с объектами, явлениями и процессами живой и неживой природы (предмет труда- земля, вода, растения и животные). Представителей этих профессий объединяет одно очень важное качество – любовь к природе. 
Их любовь не созерцательная, которой обладают все люди, а деятельная, связанная с познанием ее законов и применением их. Поэтому, выбирая профессию данного типа, очень важно разобраться, как именно Вы относитесь к природе: как к мастерской, где Вы будете работать, или как к месту отдыха, где хорошо погулять, подышать свежим воздухом. 
Особенность объектов труда этого типа состоит в том, что они сложны, изменчивы, нестандартны. И растения, и животные, и микроорганизмы развиваются без всяких выходных и праздников, так что специалисту необходимо всегда быть готовым к непредвиденным событиям.

Желательно иметь следующие качества:
-Наблюдательность
-Пространственное воображение
-Потребность в двигательной активности
-Физическая выносливость
-Организаторские способности
-Аналитические способности
        """,
             'Человек-техника': """Человек-техника.\n
Особенность технических объектов в том, что они, как правило, могут быть точно
измерены по многим признакам. При их обработке, преобразовании, перемещении
или оценке от работника требуется точность, определенность действий. Техника как
предмет труда представляет широкие возможности для новаторства, выдумки,
творчества, поэтому важное значение приобретает такое качество, как практическое
мышление. Техническая фантазия, способность мысленно соединять и разъединять
технические объекты и их части — важные условия для успеха в данной области.

Желательно иметь следующие качества:
-Техническое мышление
-Переключение и концентрация внимания
-Пространственное воображение
-Оперативная память
-Хорошая реакция и координация движений
-Устойчивость нервной системы к внешним раздражителям
-Переносимость однообразия и монотонности

        """, 'Человек-другой человек': """Человек-другой человек.\n
Главное содержание труда в профессиях типа «человек-человек» сводится к
взаимодействию между людьми. Если не наладится это взаимодействие, значит, не
наладится и работа. Качества, необходимые для работы с людьми: устойчивое,
хорошее настроение в процессе работы с людьми, потребность в общении,
способность мысленно ставить себя на место другого человека, быстро понимать
намерения, помыслы, настроение людей, умение разбираться в человеческих
взаимоотношениях, хорошая память (умение держать в уме имена и особенности
многих людей), терпение.

Желательно иметь следующие качества:
-Коммуникативные и организаторские способности
-Эмпатические способности
-Эмоциональная устойчивость
-Устойчивость и распределение внимания
-Доброжелательность
-Самообладание, выдержка
        """, 'Человек-знаковая система': """Человек-знаковая система.\n
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

Желательно иметь следующие качества:
-Устойчивость, концентрация, переключение и распределение внимания
-Абстрактное мышление
-Образная память
-Отсутствие выраженной экстраверсии и повышенного нейротизма
-Аккуратность
-Усидчивость

""", 'Человек-художественный образ': """Человек-художественный образ.\n
Важнейшие требования, которые предъявляют профессии, связанные с изобразительной, музыкальной, литературно-художественной, актерско-сценической деятельностью человека—
 Желательно иметь следующие качества:
-Наглядно-образное мышление
-Образная память
-Творческое воображение
-Эмоциональная лабильность
-Специальные способности (художественные, музыкальные)
""",
'Сам человек': """Сам человек.\n
Деятельность в этой области предполагает совершенствование своей внешности, тренировку различных спортивных навыков, а также осуществление психологической и физической подготовки к соревнованиям, турнирам, выступлениям.
Желательно иметь следующие качества:
-Коммуникативные и организаторские способности
-Усидчивость
-Работоспособность, физическая выносливость
-Двигательная память
-Наглядно-образное мышление
""",
             }

        base_df[f'Необработанное'] = answers_df.apply(processing_result_ddo, axis=1)
        # обрабатываем результаты и получаем ключ с максимальным значением
        base_df[f'Обработанное'] = base_df[f'Необработанное'].apply(
            extract_key_max_value)
        base_df[f'Максимум'] = base_df[f'Необработанное'].apply(extract_max_value)
        base_df[f'Описание_результата'] = base_df[f'Обработанное'].apply(
            lambda x: create_out_str_ddo(x, dct_desciprion, dct_prof))

        # Создаем датафрейм для создания части в общий датафрейм
        part_df = pd.DataFrame(columns=['ДДО_Необработанное', 'ДДО_Обработанное', 'ДДО_Максимум'])
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
            svod_all_df['Максимум'] / svod_all_df['Максимум'].sum(), 3) * 100
        # # Создаем суммирующую строку
        svod_all_df.loc['Итого'] = svod_all_df.sum()
        svod_all_df['Максимум'] = svod_all_df['Максимум'].astype(int)
        svod_all_df.reset_index(inplace=True)
        svod_all_df.rename(columns={'Обработанное': 'Тип', 'Максимум': 'Количество'}, inplace=True)

        """
                Обрабатываем Класс
                """
        # Среднее по Класс
        svod_group_df = pd.pivot_table(base_df, index=['Класс', 'Обработанное'],
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
            columns=['Класс', 'Человек-природа', 'Человек-техника',
                     'Человек-другой человек', 'Человек-знаковые системы',
                     'Человек-художественный образ',
                     'Итого'])
        svod_count_group_df['% Человек-природа от общего'] = round(
            svod_count_group_df['Человек-природа'] / svod_count_group_df['Итого'], 2) * 100
        svod_count_group_df['% Человек-техника от общего'] = round(
            svod_count_group_df['Человек-техника'] / svod_count_group_df['Итого'], 2) * 100
        svod_count_group_df['% Человек-другой человек от общего'] = round(
            svod_count_group_df['Человек-другой человек'] / svod_count_group_df['Итого'], 2) * 100
        svod_count_group_df['% Человек-знаковые системы от общего'] = round(
            svod_count_group_df['Человек-знаковые системы'] / svod_count_group_df['Итого'], 2) * 100
        svod_count_group_df['% Человек-художественный образ от общего'] = round(
            svod_count_group_df['Человек-художественный образ'] / svod_count_group_df['Итого'], 2) * 100

        part_svod_df = svod_count_group_df.iloc[:-1:]
        part_svod_df.sort_values(by='Класс', key=lambda x: x.map(sort_name_class), inplace=True)  # сортируем
        itog_svod_df = svod_count_group_df.iloc[-1:]
        svod_count_group_df = pd.concat([part_svod_df, itog_svod_df])

        # Среднее по Класс Пол
        svod_group_sex_df = pd.pivot_table(base_df, index=['Класс', 'Пол', 'Обработанное'],
                                           values=['Максимум'],
                                           aggfunc=round_mean)
        svod_group_sex_df.reset_index(inplace=True)

        svod_group_sex_df.sort_values(by='Класс', key=lambda x: x.map(sort_name_class), inplace=True)  # сортируем

        # Количество Класс Пол
        svod_count_group_sex_df = pd.pivot_table(base_df, index=['Класс', 'Пол'],
                                                 columns='Обработанное',
                                                 values='Максимум',
                                                 aggfunc='count', margins=True, margins_name='Итого')
        svod_count_group_sex_df.reset_index(inplace=True)
        svod_count_group_sex_df = svod_count_group_sex_df.reindex(
            columns=['Класс', 'Человек-природа', 'Человек-техника',
                     'Человек-другой человек', 'Человек-знаковые системы',
                     'Человек-художественный образ',
                     'Итого'])
        svod_count_group_sex_df['% Человек-природа от общего'] = round(
            svod_count_group_sex_df['Человек-природа'] / svod_count_group_sex_df['Итого'], 2) * 100
        svod_count_group_sex_df['% Человек-техника от общего'] = round(
            svod_count_group_sex_df['Человек-техника'] / svod_count_group_sex_df['Итого'], 2) * 100
        svod_count_group_sex_df['% Человек-другой человек от общего'] = round(
            svod_count_group_sex_df['Человек-другой человек'] / svod_count_group_sex_df['Итого'], 2) * 100
        svod_count_group_sex_df['% Человек-знаковые системы от общего'] = round(
            svod_count_group_sex_df['Человек-знаковые системы'] / svod_count_group_sex_df['Итого'], 2) * 100
        svod_count_group_sex_df['% Человек-художественный образ от общего'] = round(
            svod_count_group_sex_df['Человек-художественный образ'] / svod_count_group_sex_df['Итого'], 2) * 100

        part_svod_df = svod_count_group_sex_df.iloc[:-1:]
        part_svod_df.sort_values(by='Класс', key=lambda x: x.map(sort_name_class), inplace=True)  # сортируем
        itog_svod_df = svod_count_group_sex_df.iloc[-1:]
        svod_count_group_sex_df = pd.concat([part_svod_df, itog_svod_df])

        """
                Обрабатываем Номер_класса
                """
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
            columns=['Номер_класса', 'Человек-природа', 'Человек-техника',
                     'Человек-другой человек', 'Человек-знаковые системы',
                     'Человек-художественный образ',
                     'Итого'])
        svod_count_course_df['% Человек-природа от общего'] = round(
            svod_count_course_df['Человек-природа'] / svod_count_course_df['Итого'], 2) * 100
        svod_count_course_df['% Человек-техника от общего'] = round(
            svod_count_course_df['Человек-техника'] / svod_count_course_df['Итого'], 2) * 100
        svod_count_course_df['% Человек-другой человек от общего'] = round(
            svod_count_course_df['Человек-другой человек'] / svod_count_course_df['Итого'], 2) * 100
        svod_count_course_df['% Человек-знаковые системы от общего'] = round(
            svod_count_course_df['Человек-знаковые системы'] / svod_count_course_df['Итого'], 2) * 100
        svod_count_course_df['% Человек-художественный образ от общего'] = round(
            svod_count_course_df['Человек-художественный образ'] / svod_count_course_df['Итого'], 2) * 100

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
            columns=['Номер_класса', 'Человек-природа', 'Человек-техника',
                     'Человек-другой человек', 'Человек-знаковые системы',
                     'Человек-художественный образ',
                     'Итого'])
        svod_count_course_sex_df['% Человек-природа от общего'] = round(
            svod_count_course_sex_df['Человек-природа'] / svod_count_course_sex_df['Итого'], 2) * 100
        svod_count_course_sex_df['% Человек-техника от общего'] = round(
            svod_count_course_sex_df['Человек-техника'] / svod_count_course_sex_df['Итого'], 2) * 100
        svod_count_course_sex_df['% Человек-другой человек от общего'] = round(
            svod_count_course_sex_df['Человек-другой человек'] / svod_count_course_sex_df['Итого'], 2) * 100
        svod_count_course_sex_df['% Человек-знаковые системы от общего'] = round(
            svod_count_course_sex_df['Человек-знаковые системы'] / svod_count_course_sex_df['Итого'], 2) * 100
        svod_count_course_sex_df['% Человек-художественный образ от общего'] = round(
            svod_count_course_sex_df['Человек-художественный образ'] / svod_count_course_sex_df['Итого'], 2) * 100

        # формируем словарь
        out_dct = {'Списочный результат': base_df, 'Список для проверки': out_answer_df,
                   'Общий свод': svod_all_df,
                   'Среднее Класс': svod_group_df, 'Количество Класс': svod_count_group_df,
                   'Среднее Класс Пол': svod_group_sex_df, 'Количество Класс Пол': svod_count_group_sex_df,
                   'Среднее Номер_класса': svod_course_df, 'Количество Номер_класса': svod_count_course_df,
                   'Среднее Номер_класса Пол': svod_course_sex_df,
                   'Количество Номер_класса Пол': svod_count_course_sex_df,
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
