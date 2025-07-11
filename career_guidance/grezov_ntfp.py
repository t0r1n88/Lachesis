"""
Скрипт для обработки результатов теста Наемный труд, фриланс предпринимательство Грецов
"""

import pandas as pd
import re
from tkinter import messagebox
from lachesis_support_functions import convert_to_int,round_mean,create_union_svod,calc_count_scale

class BadOrderNTFP(Exception):
    """
    Исключение для обработки случая когда колонки не совпадают
    """
    pass

class BadValueNTFP(Exception):
    """
    Исключение для неправильных значений в вариантах ответов
    """
    pass


class BadCountColumnsNTFP(Exception):
    """
    Исключение для обработки случая если количество колонок не равно 24
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




def processing_result_ntfp(row):
    """
Функция для вычисления итогового балла  результатов теста Наемный труд, фриланс, предпринимательство
"""

    # Создаем словарь для хранения данных
    dct_type = {'Наемный труд': 0, 'Фриланс': 0, 'Предпринимательство': 0}
    # 1
    dct_type['Наемный труд'] += row[0]

    # 2
    dct_type['Фриланс'] += row[1]

    # 3
    dct_type['Предпринимательство'] += row[2]

    # 4
    dct_type['Наемный труд'] += row[3]

    # 5
    dct_type['Фриланс'] += row[4]

    # 6
    dct_type['Предпринимательство'] += row[5]

    # 7
    dct_type['Наемный труд'] += row[6]

    # 8
    dct_type['Фриланс'] += row[7]

    # 9
    dct_type['Предпринимательство'] += row[8]

    # 10
    dct_type['Наемный труд'] += row[9]

    # 11
    dct_type['Фриланс'] += row[10]

    # 12
    dct_type['Предпринимательство'] += row[11]

    # 13
    dct_type['Наемный труд'] += row[12]

    # 14
    dct_type['Фриланс'] += row[13]

    # 15
    dct_type['Предпринимательство'] += row[14]

    # 16
    dct_type['Наемный труд'] += row[15]

    # 17
    dct_type['Фриланс'] += row[16]

    # 18
    dct_type['Предпринимательство'] += row[17]

    # 19
    dct_type['Наемный труд'] += row[18]

    # 20
    dct_type['Фриланс'] += row[19]

    # 21
    dct_type['Предпринимательство'] += row[20]

    # 22
    dct_type['Наемный труд'] += row[21]

    # 23
    dct_type['Фриланс'] += row[22]

    # 24
    dct_type['Предпринимательство'] += row[23]

    # сортируем по убыванию
    result_lst = sorted(dct_type.items(), key=lambda t: t[1], reverse=True)
    begin_str = '\n'
    # создаем строку с результатами
    for sphere, value in result_lst:
        begin_str += f'{sphere}: {value};\n'

    # добавляем описание
    return begin_str



def calc_level_ntfp(row):
    """
    Функция для подсчета уровня склонности
    """
    if row[0] == 'Наемный труд':
        if 0 <= row[1] <= 7:
            return 'низкая'
        elif 8 <=  row[1] <= 14:
            return 'ниже среднего'
        elif 15 <=  row[1] <= 23:
            return 'средняя'
        elif 24 <=  row[1] <= 33:
            return 'выше среднего'
        elif 34 <=  row[1]:
            return 'высокая'
    else:
        if 0 <= row[1] <= 8:
            return 'низкая'
        elif 9 <=  row[1] <= 16:
            return 'ниже среднего'
        elif 17 <=  row[1] <= 25:
            return 'средняя'
        elif 26 <=  row[1] <= 34:
            return 'выше среднего'
        elif 35 <=  row[1]:
            return 'высокая'



def create_result_grezov_ntfp(base_df:pd.DataFrame, out_dct:dict, lst_svod_cols:list):
    """
    Функция для подсчета результата если указаны колонки по которым нужно провести свод
    :param df: датафрейм с результатами
    :param out_dct: словарь с уже подсчитанными базовыми данными
    :param lst_svod_cols: список сводных колонок
    :return: словарь
    """
    lst_level = ['низкая', 'ниже среднего', 'средняя', 'выше среднего', 'высокая']
    lst_sphere = ['Наемный труд', 'Фриланс', 'Предпринимательство']

    lst_reindex_one_level_cols = lst_svod_cols.copy()
    lst_reindex_one_level_cols.extend( ['низкая', 'ниже среднего','средняя','выше среднего', 'высокая',
                                                      'Итого'])

    lst_reindex_one_sphere_cols = lst_svod_cols.copy()
    lst_reindex_one_sphere_cols.extend( ['Наемный труд', 'Фриланс', 'Предпринимательство','Итого'])

    svod_count_one_level_df = calc_count_scale(base_df, lst_svod_cols,
                                               'Значение_ведущего_типа',
                                               'Уровень_выраженности',
                                               lst_reindex_one_level_cols, lst_level)

    svod_count_one_sphere_df = calc_count_scale(base_df, lst_svod_cols,
                                                'Значение_ведущего_типа',
                                                'Ведущий_тип',
                                                lst_reindex_one_sphere_cols, lst_sphere)

    # Считаем среднее по субшкалам
    svod_mean_one_df = pd.pivot_table(base_df,
                                      index=lst_svod_cols,
                                      values=['Значение_ведущего_типа',
                                              ],
                                      aggfunc=round_mean)
    svod_mean_one_df.reset_index(inplace=True)
    # упорядочиваем колонки
    new_order_cols = lst_svod_cols.copy()
    new_order_cols.extend((['Значение_ведущего_типа',
                            ]))
    svod_mean_one_df = svod_mean_one_df.reindex(columns=new_order_cols)

    dct_rename_cols_mean = {'Значение_ведущего_типа': 'Среднее значение ведущего типа',
                            }
    svod_mean_one_df.rename(columns=dct_rename_cols_mean, inplace=True)

    # очищаем название колонки по которой делали свод
    out_name_lst = []

    for name_col in lst_svod_cols:
        name = re.sub(r'[\[\]\'+()<> :"?*|\\/]', '_', name_col)
        if len(lst_svod_cols) == 1:
            out_name_lst.append(name[:14])
        elif len(lst_svod_cols) == 2:
            out_name_lst.append(name[:7])
        else:
            out_name_lst.append(name[:4])

    out_name = ' '.join(out_name_lst)
    if len(out_name) > 14:
        out_name = out_name[:14]

    out_dct.update({f'Ср {out_name}': svod_mean_one_df,
                    f'Уровень {out_name}': svod_count_one_level_df,
                    f'Тип {out_name}': svod_count_one_sphere_df,
                    })

    if len(lst_svod_cols) == 1:
        return out_dct
    else:
        for idx, name_column in enumerate(lst_svod_cols):
            lst_reindex_column_level_cols = [lst_svod_cols[idx], 'низкая', 'ниже среднего','средняя','выше среднего', 'высокая',
                                             'Итого']

            lst_reindex_column_sphere_cols = [lst_svod_cols[idx], 'Наемный труд', 'Фриланс', 'Предпринимательство','Итого']

            svod_count_column_level_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                          'Значение_ведущего_типа',
                                                          'Уровень_выраженности',
                                                          lst_reindex_column_level_cols, lst_level)

            svod_count_column_sphere_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                           'Значение_ведущего_типа',
                                                           'Ведущий_тип',
                                                           lst_reindex_column_sphere_cols, lst_sphere)

            # Считаем среднее по субшкалам
            svod_mean_column_df = pd.pivot_table(base_df,
                                                 index=[lst_svod_cols[idx]],
                                                 values=['Значение_ведущего_типа',
                                                         ],
                                                 aggfunc=round_mean)
            svod_mean_column_df.reset_index(inplace=True)
            # упорядочиваем колонки
            new_order_cols = [lst_svod_cols[idx]].copy()
            new_order_cols.extend((['Значение_ведущего_типа',
                                    ]))
            svod_mean_column_df = svod_mean_column_df.reindex(columns=new_order_cols)

            dct_rename_cols_mean = {'Значение_ведущего_типа': 'Среднее значение ведущего типа',
                                    }
            svod_mean_column_df.rename(columns=dct_rename_cols_mean, inplace=True)


            name_column = lst_svod_cols[idx]
            name_column = re.sub(r'[\[\]\'+()<> :"?*|\\/]', '_', name_column)
            name_column = name_column[:15]

            out_dct.update({f'Ср {name_column}': svod_mean_column_df,
                            f'Уровень {name_column}': svod_count_column_level_df,
                            f'Тип {name_column}': svod_count_column_sphere_df,
                            })
        return out_dct







def processing_grezov_ntfp(base_df: pd.DataFrame, answers_df: pd.DataFrame,lst_svod_cols:list):
    """
    Функция для обработки
    :param base_df: часть датафрейма с описательными колонками
    :param answers_df: часть датафрейма с ответами
    :param lst_svod_cols:  список с колонками по которым нужно делать свод
    """
    try:
        out_answer_df = base_df.copy()  # делаем копию для последующего соединения с сырыми ответами
        if answers_df.shape[1] != 24:
            raise BadCountColumnsNTFP

        # очищаем названия колонок от возможных сочетаний .1 которые добавляет пандас при одинаковых колонках
        clean_df_lst = []
        for name_column in answers_df.columns:
            clean_name = re.sub(r'.\d+$', '', name_column)
            clean_df_lst.append(clean_name)

        answers_df.columns = clean_df_lst

        lst_check_cols = ['В любой работе мне важны стабильность, предсказуемость',
                          'Я желаю сам выбирать, какие именно рабочие заказы буду выполнять',
                          'Я хочу иметь свое собственное дело, а не работать на кого-то',
                          'Я считаю, что важная составляющая работы — социальные гарантии (выплата больничных, будущая пенсия и т. п.)',
                          'Я согласен, что надо мной будет начальство, но хотел бы сам выбирать, под чьим именно руководством трудиться',
                          'Терпеть не могу, когда кто-то указывает мне, как нужно делать работу',
                          'Хочется четко представлять свои функциональные обязанности, всегда знать, что именно я должен делать',
                          'Сделать карьеру для меня — это не самому стать начальником, а быть таким специалистом, за которым начальники будут охотиться и сами предлагать хорошие деньги',
                          'Для меня принципиально важно, чтобы надо мной не было начальников; в работе хочу быть предоставлен самому себе',
                          'Готов смириться с относительно меньшими перспективами карьерного роста в обмен на то, что моя работа будет спокойной и стабильной',
                          'Я готов работать в режиме резкого изменения загруженности: «то густо, то пусто»',
                          'Для меня принципиально важно воплощать в жизнь то, что я задумал, пусть даже на это потребуется гораздо больше времени и сил, чем предполагает обычный рабочий день',
                          'Я предпочел бы, чтобы не я сам, а работодатель заботился о поиске заказов и о том, как организовать мой труд',
                          'Согласен, что содержание и график моей работы могут резко меняться в зависимости от того, какой заказ удалось получить',
                          'Я готов вкладывать в развитие дела личные финансовые средства, даже если рискую их потерять',
                          'Я готов вести себя в четком соответствии с теми правилами, которые заданы моим работодателем',
                          'Я согласен обойтись без постоянной гарантированной зарплаты, а получать деньги лишь за то, что фактически выполнил',
                          'Полагаю, что лучше рисковать — «либо заработаю много, либо потеряю все», — нежели довольствоваться небольшой, но гарантированной зарплатой',
                          'Я не желаю заниматься чем-либо, выходящим за рамки моей основной работы',
                          'Я готов смириться с тем, что у меня долго вообще не будет заработков, если не удалось найти заказы',
                          'Полагаю, что у меня хорошие способности к управлению другими людьми и решению неожиданных проблем',
                          'Для меня предпочтительнее работать за гарантированную зарплату, а не подвергать себя рискам, связанным с собственным бизнесом',
                          'Готов работать на начальника, но не согласен, чтобы он «монополизировал» меня; пусть лучше у меня будет сразу несколько начальников',
                          'Считаю, что иметь собственный бизнес — это важный показатель жизненного успеха человека'
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
            raise BadOrderNTFP

        answers_df = answers_df.applymap(convert_to_int)  # приводим к инту
        # проверяем правильность
        valid_values = [0, 1, 2, 3, 4, 5]
        # Проверяем, есть ли значения, отличающиеся от указанных в списке
        lst_error_answers = []  # список для хранения строк где найдены неправильные ответы

        for i in range(24):
            mask = ~answers_df.iloc[:, i].isin(valid_values)  # проверяем на допустимые значения
            result_check = answers_df.iloc[:, i][mask]
            if len(result_check) != 0:
                error_row = list(map(lambda x: x + 2, result_check.index))
                error_row = list(map(str, error_row))
                error_row_lst = [f'В {i + 1} вопросной колонке на строке {value}' for value in error_row]
                error_in_column = ','.join(error_row_lst)
                lst_error_answers.append(error_in_column)

        if len(lst_error_answers) != 0:
            error_message = ';'.join(lst_error_answers)
            raise BadValueNTFP

        # Создаем колонку для результатов первичного подсчета
        base_df[f'Распределение'] = answers_df.apply(processing_result_ntfp, axis=1)
        base_df[f'Ведущий_тип'] = base_df[f'Распределение'].apply(
            extract_key_max_value)
        base_df[f'Значение_ведущего_типа'] = base_df[f'Распределение'].apply(
            extract_max_value)
        base_df[f'Уровень_выраженности'] = base_df[['Ведущий_тип', 'Значение_ведущего_типа']].apply(lambda x: calc_level_ntfp(x), axis=1)

        # Создаем датафрейм для создания части в общий датафрейм
        part_df = pd.DataFrame()
        part_df['НТФП_Распределение'] = base_df['Распределение']
        part_df['НТФП_Ведущий_тип'] = base_df['Ведущий_тип']
        part_df['НТФП_Тип_Значение'] = base_df['Значение_ведущего_типа']
        part_df['НТФП_Тип_Уровень'] = base_df['Уровень_выраженности']

        base_df.sort_values(by='Значение_ведущего_типа', ascending=False, inplace=True)  # сортируем
        out_answer_df = pd.concat([out_answer_df, answers_df], axis=1)  # Датафрейм для проверки

        # Создаем строку с описанием
        description_result = """
        Шкала оценки результатов шкалы склонности к Наемному труду
        34-40 баллов – высокая;
        24-33 баллов – выше среднего;
        15-23 баллов – средняя;
        8-14 баллов – ниже среднего;
        0-7 баллов – низкая склонность.
    
        Шкала оценки результатов шкалы склонности к Фрилансу, Предпринимательству
        35-40 баллов – высокая;
        26-34 баллов – выше среднего;
        17-25 баллов – средняя;
        9-16 баллов – ниже среднего;
        0-8 баллов – низкая склонность.
    
    
        Если баллы превышают средние показатели по всем трем шкалам — скорее всего, это говорит о том, что твои представления об идеальной работе внутренне противоречивы, трудно совместимы между собой (к примеру, желание иметь полную личную свободу в трудовых отношениях сочетается с требованием высокого уровня социальных гарантий, а стремление самому выбирать заказы — с тем, чтобы их искал и предлагал на выбор начальник). 
        В реальности найти работу, которая отвечала бы такому набору требований, вряд ли удастся, все равно придется идти на компромиссы...
        Если же баллы по всем трем шкалам оказываются ниже средних, это значит, что у тебя, видимо, просто не сформирована мотивация к трудовой деятельности. Получается, что тебе, по твоим собственным представлениям, не подходит вообще никакая работа. 
    
        Наемный труд.
        Самый распространенный вариант. Чаще всего под словами «искать работу», «устроиться на работу» подразумевают именно наемный труд. Сотрудник оформляется в штат организации и поддерживает трудовые отношения с ней на постоянной основе. С одной стороны, такой вариант трудоустройства самый стабильный, так как обеспечивает социальные гарантии (как минимум это больничные и выплаты в пенсионный фонд, но многие организации предоставляют сотрудникам различные дополнительные льготы — транспорт, бесплатные обеды, добровольное медицинское страхование и т. п.). Мы говорим, разумеется, об официальном трудоустройстве с заключением договора согласно Трудовому кодексу. От тех работодателей, которые не соблюдают предусмотренные законом процедуры, лучше держаться в стороне. Обычно именно тот, кто предоставляет работу, озабочен и обустройством рабочего места, поиском заказчиков, поставками материалов и т. п. У исполнителя голова обо всем этом не болит, его задача — четко выполнять возложенные на него обязанности. Но, с другой стороны, степень личной свободы таких работников минимальна. По сути, они продают свое время, усилия и готовность выполнять определенный труд, а распоряжается всем этим работодатель.
         Над таким работником, каких бы карьерных высот он ни достиг, все равно будет вышестоящий начальник. То, что такой сотрудник создает в рабочее время, будь то материальный предмет или продукт интеллектуальной деятельности, тоже принадлежит работодателю. Возможности для карьерного роста зависят от конкретного рабочего места, уровня подготовки и опыта работника, но в целом работники, особенно начинающие, склонны завышать свои ожидания, в реальности «звездную» карьеру с помощью наемного труда делают очень и очень немногие. 
        Нужно помнить, что заработная плата наемного работника в коммерческих организациях обычно оказывается заметно ниже того дохода, который его труд приносит работодателю. Ведь такая организация направлена на получение прибыли, а значит расходы в том числе и на оплату труда, должны быть меньше, чем сумма, за которую можно продать произведенные товары или услуги. 
        Некоторым такая ситуация субъективно некомфортна: дескать, я вынужден работать «на дядю», значительную долю прибыли от моего труда получает кто-то другой. Это так и есть, но ведь предприниматель получает эту прибыль тоже не просто так, а решает все связанные с работой организационные вопросы, обеспечивает условия для нее, а также берет на себя неизбежные в предпринимательской деятельности риски. Если ты готов лично заниматься этим — становись предпринимателем сам.
    
        Фриланс.
        Слово «фрилансер» происходит от средневекового английского термина, дословно обозначающего «свободное копье». Так называли воинов-наемников, не состоявших на постоянной службе в какой-либо армии, а готовых предложить свои услуги любому, кто заплатит за них. На рынке труда так называют тех, кто, не оформляя постоянные трудовые отношения с каким-либо работодателем, ищет и выполняет разовые заказы.
        Главный плюс такой работы — это высокая степень личной свободы. Человек сам волен определять, за что ему браться, когда и как выполнять работу. Необходимо лишь выдать нужный результат к согласованному с заказчиком сроку, а то, как его достигнуть, — личное дело работника. Часто такая работа подразумевает и возможность трудиться в режиме удаленного доступа, то есть необязательно физически находиться там, где указал работодатель, а можно, к примеру, путешествовать с ноутбуком по стране и миру, по ходу дела выполняя работу (скажем, редактируя тексты, создавая веб-страницы или обрабатывая статистические данные) и отсылая результаты заказчику через Интернет.
        Важно подчеркнуть, что обратная сторона личной свободы фрилансера — это высокий уровень самоорганизованности, умение спланировать и осуществить труд без контроля извне. Он ведь не обязан являться на работу по раз и навсегда заведенному расписанию, и начальник не контролирует, чтобы он занимался делом. У многих людей в таких условиях возникает соблазн действовать по принципу «раз конкретно сегодня работу можно и не выполнять — значит, сделаю как-нибудь потом». Но это «потом» зачастую так и не настает, в результате заказы в срок не исполняются, а новые найти становится почти невозможно (ведь для фрилансера важнее всего репутация, никто не хочет иметь дело с ненадежным исполнителем).
        Минусы работы фрилансера — нестабильность, почти полное отсутствие социальных гарантий и чаще всего — резкая неравномерность загруженности во времени. Пока есть заказы, и ты в состоянии их выполнить — ты, что называется, на коне. А если заказы закончились или, скажем, ты не можешь выполнять их из-за болезни — все, источников средств к существованию нет, придется искать другую работу или же довольствоваться нищенскими социальными пособиями. Заказы поступают, как правило, неравномерно: порой их так много, что фрилансер на пределе сил трудится по 14–16 часов в день, а потом их почти нет. Соответственно, нестабилен и доход (поэтому, кстати, фрилансерам сложно получить банковский кредит). Есть риск столкнуться с мошенничеством: нередки ситуации, когда получить деньги за уже выполненную работу не удается. 
        Однако все это окупается тем, что компетентные и востребованные специалисты, услуги которых нужны сразу нескольким организациям, в свободном плаванье имеют шансы заработать в два-три раза больше, чем если бы они оформили постоянные трудовые отношения с каким-то одним работодателем.
        Важно понимать, что фриланс в отличие от построения собственного бизнеса — чаще всего все равно работа не на развитие своего дела, а, как говорится, «на дядю». Человек продает свое рабочее время и компетентность, а кто-то, скорее всего, строит на этом свой бизнес, по сути, перепродавая результаты труда дальше. В этом плане отличие фриланса от обычного наемного труда заключается лишь в отсутствии постоянных трудовых отношений с одним конкретным работодателем.
    
        Предпринимательство.
        Это самостоятельная, осуществляемая на свой риск деятельность, направленная на систематическое получение дохода, то есть на создание и развитие собственного бизнеса. Она либо осуществляется непосредственно самим человеком (индивидуальное предпринимательство), либо подразумевает образование организации, так называемого юридического лица.
        Потенциально именно этот путь самый доходный, но он же связан с максимальными рисками. Начальства как такового у предпринимателя нет, он предоставлен сам себе и трудится на себя, начиная с выбора того, что вообще сделать предметом бизнеса (вариантов много, самые частые: оказание услуг, производство, продажи) и заканчивая поиском клиентов. Однако не следует путать отсутствие начальства и свободу в принятии решений со вседозволенностью и отсутствием обязательств. 
        У любого предпринимателя обязательства все равно возникают, и их неисполнение чревато серьезными неприятностями — начиная с материальных убытков и заканчивая уголовным наказанием. В принципе, предпринимательство возможно и в такой форме: человек единолично создает какой-либо продукт или оказывает услугу и сам реализует их, однако сколько-нибудь серьезный профессиональный рост в этой сфере предполагает привлечение наемных работников и организацию их деятельности.
        Для достижения успеха в предпринимательстве важно не только уметь хорошо делать то дело, которое открываешь, но и быть эффективным управленцем. Вообще говоря, вникать в детали производства хозяину и необязательно, некоторые владельцы бизнеса полностью передают решение всех таких вопросов подчиненным наемным работникам, оставляя за собой функции общего управления. 
        Важнейшие личностные качества бизнесмена — устойчивость к стрессам, умение принимать решения (в том числе и связанные с разумным риском) даже в условиях недостатка информации, уверенность в себе и настойчивость, готовность мобилизовать свои усилия в нужный момент, организовать деятельность самого себя и подчиненных, наладить взаимопонимание с людьми и управлять ими. 
        Подчеркнем важность понимания экономических и юридических механизмов управления бизнесом, так как без этого даже лучшие начинания почти гарантированно обречены на провал.
        Социальное страхование предприниматели (разумеется, те, кто официально оформил свою деятельность) имеют, но в очень ограниченном объеме — в этом смысле они защищены меньше, чем большинство наемных работников. Индивидуальный предприниматель отвечает по взятым на себя обязательствам личным имуществом.
        Если же бизнес подразумевает создание юридического лица — формы ответственности зависят от целого ряда нюансов, но они в любом случае существуют и оказываются довольно жесткими.
        Вообще, заниматься предпринимательством намного сложнее, чем быть наемным работником: приходится решать массу разнородных проблем, принимать ответственные решения, идти на риски, вступать в отношения жесткой конкуренции с другими бизнесменами. Но если это соответствует твоим личностным качествам и желанию, то попробовать себя на этом пути, несомненно, стоит. 
        С одной стороны, в случае успеха такая деятельность приведет к большему благосостоянию и более высокому статусу в обществе, чем наемный труд. А с другой стороны, скучать на этом пути в любом случае не придется…
        
                """
        # создаем описание результата
        base_df[f'Описание_результата'] = 'Наемный труд, фриланс, предпринимательство.\nРезультат тестирования:\n' + \
                                          base_df[
                                              f'Распределение'] + description_result
        part_df['НТФП_Описание_результата'] = base_df[f'Описание_результата']

        # Делаем свод по уровню
        dct_svod_level = {'Значение_ведущего_типа': 'Уровень_выраженности',
                          }
        dct_rename_svod_level = {'Значение_ведущего_типа': 'Количество',
                                 }
        # Списки для шкал
        lst_level = ['низкая', 'ниже среднего',
                     'средняя',
                     'выше среднего','высокая'
                     ]
        base_svod_level_df = create_union_svod(base_df, dct_svod_level, dct_rename_svod_level, lst_level)

        # Делаем свод по сфере
        dct_svod_sphere = {'Значение_ведущего_типа': 'Ведущий_тип',
                           }

        dct_rename_svod_sphere = {'Значение_ведущего_типа': 'Количество',
                                  }

        # Списки для шкал
        lst_sphere = ['Наемный труд', 'Фриланс', 'Предпринимательство']

        base_svod_sphere_df = create_union_svod(base_df, dct_svod_sphere, dct_rename_svod_sphere, lst_sphere)

        # считаем среднее значение
        avg_main = round(base_df['Значение_ведущего_типа'].mean(), 2)

        avg_dct = {'Среднее значение Ведущий тип': avg_main,
                   }

        avg_df = pd.DataFrame.from_dict(avg_dct, orient='index')
        avg_df = avg_df.reset_index()
        avg_df.columns = ['Показатель', 'Среднее значение']

        # формируем основной словарь
        out_dct = {'Списочный результат': base_df, 'Список для проверки': out_answer_df,
                   'Среднее': avg_df,
                   'Свод по уровням': base_svod_level_df,
                   }

        # Листы по уровням
        dct_level = dict()
        for level in lst_level:
            temp_df = base_df[base_df['Уровень_выраженности'] == level]
            if temp_df.shape[0] != 0:
                dct_level[level] = temp_df
        out_dct.update(dct_level)

        # Добавляем свод по сферам
        out_dct.update({
            'Свод по типам': base_svod_sphere_df,
        })
        # Листы по сферам
        dct_sphere = dict()
        for sphere in lst_sphere:
            temp_df = base_df[base_df['Ведущий_тип'] == sphere]
            if temp_df.shape[0] != 0:
                dct_sphere[sphere] = temp_df
        out_dct.update(dct_sphere)

        """
                            Сохраняем в зависимости от необходимости делать своды по определенным колонкам
                            """
        if len(lst_svod_cols) == 0:
            return out_dct, part_df
        else:
            out_dct = create_result_grezov_ntfp(base_df, out_dct, lst_svod_cols)

            return out_dct, part_df

    except BadOrderNTFP:
        messagebox.showerror('Лахеcис',
                             f'При обработке вопросов теста Наемный труд, фриланс, предпринимательство Грецов обнаружены неправильные вопросы. Проверьте названия колонок с вопросами:\n'
                             f'{error_order_message}\n'
                             f'Используйте при создании Яндекс-формы написание вопросов из руководства пользователя программы Лахесис.')
    except BadValueNTFP:
        messagebox.showerror('Лахеcис',
                             f'При обработке вопросов теста Наемный труд, фриланс, предпринимательство Грецов обнаружены неправильные варианты ответов. Проверьте ответы на указанных строках:\n'
                             f'{error_message}\n'
                             f'Используйте при создании Яндекс-формы написание вариантов ответа из руководства пользователя программы Лахесис.')


    except BadCountColumnsNTFP:
        messagebox.showerror('Лахеcис',
                             f'Проверьте количество колонок с ответами на тест Наемный труд, фриланс, предпринимательство Грецов\n'
                             f'Должно быть 24 колонки с ответами')





