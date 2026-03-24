"""
Скрипт для обработки результатов Диагностический опросник для выявления склонности к различным формам девиантного поведения для учащихся общеобразовательных учреждений ВМедА
"""

import pandas as pd
import re
from tkinter import messagebox
from lachesis_support_functions import round_mean_two,calc_count_scale,create_union_svod, create_list_on_level

class BadOrderDAPPS(Exception):
    """
    Исключение для обработки случая когда колонки не совпадают
    """
    pass


class BadValueDAPPS(Exception):
    """
    Исключение для неправильных значений в вариантах ответов
    """
    pass

class BadCountColumnsDAPPS(Exception):
    """
    Исключение для обработки случая если количество колонок не равно 48
    """
    pass


def calc_ip_sten(value):
    """
    Функция для подсчета Стена
    :return:
    """

    if  89<= value:
        return 1
    elif  83<= value <= 88 :
        return 2
    elif 68<= value <=82 :
        return 3
    elif  54<= value <=67 :
        return 4
    elif 45<=value <=53 :
        return 5
    elif  33<= value <= 44:
        return 6
    elif 26<=value <=32 :
        return 7
    elif  19<= value <=25 :
        return 8
    elif 15<= value <=18 :
        return 9
    else:
        return 10


def calc_value_adp(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [3,6,10,11,13,16,20,22,23,24,
              26,29,31,32,33,37,38,39,42,45,46,48]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_pr:
            value_forward += value

    return value_forward


def calc_adp_sten(value):
    """
    Функция для подсчета Стена
    :return:
    """

    if  38<= value:
        return 1
    elif  31<= value <=37 :
        return 2
    elif 26<= value <=30 :
        return 3
    elif  19<= value <=25 :
        return 4
    elif 13<=value <=18 :
        return 5
    elif  8<= value <=12 :
        return 6
    elif 6<=value <=7 :
        return 7
    elif  4<= value <=5 :
        return 8
    elif 2<= value <=3 :
        return 9
    else:
        return 10


def calc_value_dp(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [2,5,8,12,14,15,17,
              18,19,21,27,28,35,40]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_pr:
            value_forward += value

    return value_forward

def calc_dp_sten(value):
    """
    Функция для подсчета Стена
    :return:
    """

    if  33<= value:
        return 1
    elif  27<= value <=32 :
        return 2
    elif 23<= value <=26 :
        return 3
    elif  18<= value <=22 :
        return 4
    elif 15<=value <=17 :
        return 5
    elif  11<= value <=14 :
        return 6
    elif 8<=value <=10 :
        return 7
    elif  5<= value <=7 :
        return 8
    elif 3<= value <= 4:
        return 9
    else:
        return 10


def calc_value_sr(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [4,9,25,30,34,36,44,47]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_pr:
            value_forward += value

    return value_forward


def calc_sr_sten(value):
    """
    Функция для подсчета Стена
    :return:
    """

    if  16<= value:
        return 1
    elif  13<= value <=15 :
        return 2
    elif 10<= value <=12 :
        return 3
    elif  7<= value <=9 :
        return 4
    elif 5<=value <=6 :
        return 5
    elif value ==4 :
        return 6
    elif value ==3 :
        return 7
    elif value ==2 :
        return 8
    elif value ==1 :
        return 9
    else:
        return 10





def calc_level(value):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """
    if 1<= value <= 2:
        return f'высокая склонность к ДП'
    elif 3 <= value <= 8:
        return f'значительная предрасположенность к ДП'
    else:
        return f'низкая склонность к ДП'

def create_itog_stens(row):
    """
    Функция для создания строки с итоговым стеном
    :param row: строка с результатами
    :return:
    """
    lst_out = list(map(str,row))
    return '-'.join(lst_out)



def create_list_on_level_dapp_school(base_df:pd.DataFrame, out_dct:dict, lst_level:list, dct_prefix:dict):
    """
    Функция для создания списков по уровням шкал
    :param base_df: датафрейм с результатами
    :param out_dct: словарь с датафреймами
    :param lst_level: список уровней по которым нужно сделать списки
    :param dct_prefix: префиксы для названий листов
    :return: обновлейнный out dct
    """
    for key,value in dct_prefix.items():
        dct_level = dict()
        for level in lst_level:
            temp_df = base_df[base_df[key] == level]
            if temp_df.shape[0] != 0:
                if level == 'низкая склонность к ДП':
                    level = 'низкая'
                elif level == 'значительная предрасположенность к ДП':
                    level = 'значительная'
                else:
                    level = 'высокая'
                dct_level[f'{dct_prefix[key]}. {level}'] = temp_df
        out_dct.update(dct_level)

    return out_dct


def create_result_dapp_school(base_df:pd.DataFrame, out_dct:dict, lst_svod_cols:list):
    """
    Функция для подсчета результата если указаны колонки по которым нужно провести свод
    :param df: датафрейм с результатами
    :param out_dct: словарь с уже подсчитанными базовыми данными
    :param lst_svod_cols: список сводных колонок
    :return: словарь
    """
    lst_level = ['низкая склонность к ДП', 'значительная предрасположенность к ДП', 'высокая склонность к ДП']
    lst_reindex_one_level_cols = lst_svod_cols.copy()
    lst_reindex_one_level_cols.extend(['низкая склонность к ДП', 'значительная предрасположенность к ДП', 'высокая склонность к ДП',
                                       'Итого'])  # Основная шкала

    # АД
    svod_count_one_level_k_df = calc_count_scale(base_df, lst_svod_cols,
                                                 'ИП_Стен',
                                                 'ИП_Уровень',
                                                 lst_reindex_one_level_cols, lst_level)
    # АВА
    svod_count_one_level_d_df = calc_count_scale(base_df, lst_svod_cols,
                                                 'АДП_Стен',
                                                 'АДП_Уровень',
                                                 lst_reindex_one_level_cols, lst_level)
    # ИЗ
    svod_count_one_level_s_df = calc_count_scale(base_df, lst_svod_cols,
                                                 'ДП_Стен',
                                                 'ДП_Уровень',
                                                 lst_reindex_one_level_cols, lst_level)
    # ИЗ
    svod_count_one_level_pa_df = calc_count_scale(base_df, lst_svod_cols,
                                                  'СР_Стен',
                                                  'СР_Уровень',
                                                  lst_reindex_one_level_cols, lst_level)

    # Считаем среднее по субшкалам
    svod_mean_one_df = pd.pivot_table(base_df,
                                      index=lst_svod_cols,
                                      values=['ИП_Значение',
                                              'АДП_Значение',
                                              'ДП_Значение',

                                              'СР_Значение',
                                              ],
                                      aggfunc=round_mean_two)
    svod_mean_one_df.reset_index(inplace=True)

    # упорядочиваем колонки
    new_order_cols = lst_svod_cols.copy()
    new_order_cols.extend((['ИП_Значение',
                            'АДП_Значение',
                            'ДП_Значение',

                            'СР_Значение',
                            ]))
    svod_mean_one_df = svod_mean_one_df.reindex(columns=new_order_cols)

    dct_rename_cols_mean = {'ИП_Значение': 'Ср. Интегральный показатель',
                            'АДП_Значение': 'Ср. Аддитивное поведение',
                            'ДП_Значение': 'Ср. Делинквентное поведение',
                            'СР_Значение': 'Ср. Суицидальный риск',
                            }
    svod_mean_one_df.rename(columns=dct_rename_cols_mean, inplace=True)

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

    out_dct.update({f'Ср. {out_name}': svod_mean_one_df,
                    f'ИП {out_name}': svod_count_one_level_k_df,
                    f'АДП {out_name}': svod_count_one_level_d_df,
                    f'ДП {out_name}': svod_count_one_level_s_df,

                    f'СР {out_name}': svod_count_one_level_pa_df
                    })

    if len(lst_svod_cols) == 1:
        return out_dct
    else:
        for idx, name_column in enumerate(lst_svod_cols):
            lst_reindex_column_level_cols = [lst_svod_cols[idx], 'низкая склонность к ДП', 'значительная предрасположенность к ДП', 'высокая склонность к ДП',
                                             'Итого']

            # АД
            svod_count_column_level_k_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                            'ИП_Стен',
                                                            'ИП_Уровень',
                                                            lst_reindex_column_level_cols, lst_level)
            # АВА
            svod_count_column_level_d_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                            'АДП_Стен',
                                                            'АДП_Уровень',
                                                            lst_reindex_column_level_cols, lst_level)
            # ИЗ
            svod_count_column_level_s_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                            'ДП_Стен',
                                                            'ДП_Уровень',
                                                            lst_reindex_column_level_cols, lst_level)
            # ИЗ
            svod_count_column_level_pa_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                             'СР_Стен',
                                                             'СР_Уровень',
                                                             lst_reindex_column_level_cols, lst_level)

            # Считаем среднее по субшкалам
            svod_mean_column_df = pd.pivot_table(base_df,
                                              index=[lst_svod_cols[idx]],
                                              values=['ИП_Значение',
                                                      'АДП_Значение',
                                                      'ДП_Значение',

                                                      'СР_Значение',
                                                      ],
                                              aggfunc=round_mean_two)
            svod_mean_column_df.reset_index(inplace=True)

            # упорядочиваем колонки
            new_order_cols = [lst_svod_cols[idx]].copy()
            new_order_cols.extend((['ИП_Значение',
                                    'АДП_Значение',
                                    'ДП_Значение',

                                    'СР_Значение',
                                    ]))
            svod_mean_column_df = svod_mean_column_df.reindex(columns=new_order_cols)

            dct_rename_cols_mean = {'ИП_Значение': 'Ср. Интегральный показатель',
                                    'АДП_Значение': 'Ср. Аддитивное поведение',
                                    'ДП_Значение': 'Ср. Делинквентное поведение',
                                    'СР_Значение': 'Ср. Суицидальный риск',
                                    }
            svod_mean_column_df.rename(columns=dct_rename_cols_mean, inplace=True)
            # Готовим наименование
            name_column = lst_svod_cols[idx]
            name_column = re.sub(r'[\[\]\'+()<> :"?*|\\/]', '_', name_column)
            name_column = name_column[:15]
            out_dct.update({f'Ср. {name_column}': svod_mean_column_df,
                            f'ИП {name_column}': svod_count_column_level_k_df,
                            f'АДП {name_column}': svod_count_column_level_d_df,
                            f'ДП {name_column}': svod_count_column_level_s_df,

                            f'СР {name_column}': svod_count_column_level_pa_df,
                            })
        return out_dct








def processing_dap_p_school(base_df: pd.DataFrame, answers_df: pd.DataFrame, lst_svod_cols:list):
    """
    Функция для обработки
    :param base_df: часть датафрейма с описательными колонками
    :param answers_df: часть датафрейма с ответами
    :param lst_svod_cols:  список с колонками по которым нужно делать свод
    """
    try:
        out_answer_df = base_df.copy()  # делаем копию для последующего соединения с сырыми ответами
        union_base_df = base_df.copy()  # делаем копию анкетной части чтобы потом соединить ее с ответной частью
        quantity_cols_base_df = base_df.shape[1]  # количество колонок в анкетной части

        if len(answers_df.columns) != 48:  # проверяем количество колонок с вопросами
            raise BadCountColumnsDAPPS

        # очищаем названия колонок от возможных сочетаний .1 которые добавляет пандас при одинаковых колонках
        clean_df_lst = []
        for name_column in answers_df.columns:
            clean_name = re.sub(r'.\d+$', '', name_column)
            clean_df_lst.append(clean_name)

        answers_df.columns = clean_df_lst

        lst_check_cols = ['Я хорошо понял инструкцию к данной методике',
                          'Люди, с которыми я пытаюсь находиться в дружеских отношениях, очень часто причиняют мне боль',
                          '«За компанию» с товарищами я могу принять большое количество алкоголя',
                          'Я считаю, что в некоторых ситуациях жизнь может потерять ценность для человека',
                          'Я бываю излишне груб (а) с окружающими',
                          'Мои друзья рассказывали, что в некоторых ситуациях они испытывали необычные состояния: видели красочные и интересные видения, слышали странные звуки и др.',
                          'Думаю, что самым трудным предметом для меня будет—производственное обучение',
                          'Среди моих друзей были такие, которые вели такой образ жизни, что мне приходилось скрывать свою дружбу от родителей',
                          'Мне кажется, окружающие плохо понимают меня, не ценят и недолюбливают',
                          'В последнее время я замечаю, что стал (а) много курить. Это помогает мне отвлечься от проблем и хлопот',

                          'Бывало, что по утрам у меня дрожали руки и голова просто «раскалывалась»',
                          'Я всегда стремился (лась) к дружбе с ребятами, которые были старше меня по возрасту',
                          'Не могу заставить себя бросить курить, хотя знаю, что это вредно',
                          'В состоянии агрессии я способен (а) на многое',
                          'Среди моих близких родственников (отец, мать, братья, сестры) были судимые лица',
                          'Часто я испытывал чувство невесомости тела, отрешенности от окружающего мира, нереальности происходящего',
                          'На подрастающее поколение влияет так много обстоятельств, что усилия родителей и педагогов по их воспитанию оказываются бесполезными',
                          'Если кто-нибудь виноват в моих неприятностях, я найду способ отплатить ему тем же',
                          'Приятели, с которыми я дружу, не нравятся моим родителям',
                          'Я считаю, что можно оправдать людей, выбравших добровольную смерть',

                          'Я привык (ла) считать, что «око за око, зуб за зуб»',
                          'Я всегда раз в неделю выпиваю',
                          'Если кто-то причинил мне зло, я отплачу ему тем же',
                          'Бывало, что я слышал (а) голоса внутри моей головы, звучание собственных мыслей',
                          'Смысл жизни не всегда бывает ясен, иногда его можно потерять',
                          'У меня есть друзья, которые любят смотреть «мультики» после приема разных веществ',
                          'В районе, где я проживаю, есть молодежные тусовки, которые активно враждуют между собой',
                          'В последнее время, чтобы не сорваться, я вынужден (а) принимать успокоительные средства',
                          'Я пыталась (лся) освободиться от некоторых пагубных привычек',
                          'Я не осуждаю людей, которые совершают попытки уйти из жизни',

                          'Употребляя алкоголь, я часто превышал свою норму',
                          'Мои родители и родственники высказывали опасения в связи с моими выпивками',
                          'В последнее время я часто испытывал (а) стресс, поэтому принимал (а) успокоительные средства',
                          'Выбор добровольной смерти человеком в обычной жизни, безусловно, может быть оправдан',
                          'В нашей школе был принят «ритуал прописки» новичков, и я активно в нем участвовал',
                          'В последнее время у меня подавленное состояние, будущее кажется мне безнадежным',
                          'У меня были неприятности во время учебы в связи с употреблением алкоголя',
                          'Мне неприятно вспоминать и говорить о некоторых случаях, которые были связаны с употреблением алкоголя',
                          'Мои друзья умеют хорошо «расслабиться» и получить удовольствие',
                          'Можно согласиться, с тем, что я не очень-то склонен выполнять многие законы, считаю их неразумными',

                          'Среди моих близких друзей были такие, которые часто уходили из дома, бродяжничали и т.д.',
                          'Я считаю, что мой отец злоупотреблял (злоупотребляет) алкоголем',
                          'Я люблю играть в азартные игры. Они дают возможность «встряхнуться», «поймать свой шанс»',
                          'Я понимаю людей, которые не хотят жить дальше, если их предают родные и близкие',
                          'Я не осуждаю друзей, которые курят «травку»',
                          'Нет ничего предосудительного в том, что люди пытаются испытать на себе некоторые необычные состояния',
                          'В нашей семье были случаи добровольного ухода из жизни (или попытки ухода)',
                          'С некоторыми своими привычками я уже не смогу справиться'
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
            raise BadOrderDAPPS

        # словарь для замены слов на числа
        dct_replace_value = {'нет, это совсем не так': 0,
                             'пожалуй, так': 1,
                             'верно': 2,
                             'совершенно верно': 3,
                             }
        valid_values = [0,1,2,3]
        answers_df.replace(dct_replace_value, inplace=True)  # заменяем слова на цифры для подсчетов
        # Проверяем, есть ли значения, отличающиеся от указанных в списке
        lst_error_answers = []  # список для хранения строк где найдены неправильные ответы

        for i in range(48):
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
            raise BadValueDAPPS


        base_df['ИП_Значение'] = answers_df.sum(axis=1)
        base_df['ИП_Стен'] = base_df['ИП_Значение'].apply(calc_ip_sten)
        base_df['ИП_Уровень'] = base_df['ИП_Стен'].apply(calc_level)

        base_df['АДП_Значение'] = answers_df.apply(calc_value_adp,axis=1)
        base_df['АДП_Стен'] = base_df['АДП_Значение'].apply(calc_adp_sten)
        base_df['АДП_Уровень'] = base_df['АДП_Стен'].apply(calc_level)

        base_df['ДП_Значение'] = answers_df.apply(calc_value_dp,axis=1)
        base_df['ДП_Стен'] = base_df['ДП_Значение'].apply(calc_dp_sten)
        base_df['ДП_Уровень'] = base_df['ДП_Стен'].apply(calc_level)

        base_df['СР_Значение'] = answers_df.apply(calc_value_sr,axis=1)
        base_df['СР_Стен'] = base_df['СР_Значение'].apply(calc_sr_sten)
        base_df['СР_Уровень'] = base_df['СР_Стен'].apply(calc_level)

        # Упорядочиваем
        result_df = base_df.iloc[:, quantity_cols_base_df:]  # отсекаем часть с результатами чтобы упорядочить
        lst_stens = [column for column in result_df.columns if 'Стен' in column]
        result_df['Итоговые_стены'] = result_df[lst_stens].apply(create_itog_stens, axis=1)

        new_order_lst = ['Итоговые_стены', 'ИП_Стен', 'АДП_Стен',
                         'ДП_Стен', 'СР_Стен',

                         'ИП_Уровень', 'АДП_Уровень', 'ДП_Уровень', 'СР_Уровень',

                         'ИП_Значение', 'АДП_Значение', 'ДП_Значение', 'СР_Значение',
                         ]
        result_df = result_df.reindex(columns=new_order_lst)  # изменяем порядок
        base_df = pd.concat([union_base_df, result_df], axis=1)  # соединяем и перезаписываем base_df

        # Создаем датафрейм для создания части в общий датафрейм
        part_df = pd.DataFrame()
        # Общая тревожность
        part_df['ДАППВМА_Итоговые_стены'] = base_df['Итоговые_стены']
        part_df['ДАППВМА_ИП_Стен'] = base_df['ИП_Стен']
        part_df['ДАППВМА_АДП_Стен'] = base_df['АДП_Стен']
        part_df['ДАППВМА_ДП_Стен'] = base_df['ДП_Стен']
        part_df['ДАППВМА_СР_Стен'] = base_df['СР_Стен']

        part_df['ДАППВМА_ИП_Уровень'] = base_df['ИП_Уровень']
        part_df['ДАППВМА_АДП_Уровень'] = base_df['АДП_Уровень']
        part_df['ДАППВМА_ДП_Уровень'] = base_df['ДП_Уровень']
        part_df['ДАППВМА_СР_Уровень'] = base_df['СР_Уровень']

        part_df['ДАППВМА_ИП_Значение'] = base_df['ИП_Значение']
        part_df['ДАППВМА_АДП_Значение'] = base_df['АДП_Значение']
        part_df['ДАППВМА_ДП_Значение'] = base_df['ДП_Значение']
        part_df['ДАППВМА_СР_Значение'] = base_df['СР_Значение']

        out_answer_df = pd.concat([out_answer_df, answers_df], axis=1)  # Датафрейм для проверки

        base_df.sort_values(by='ИП_Значение', inplace=True, ascending=False)

        # Делаем свод  по  шкалам
        dct_svod_sub = {'ИП_Стен': 'ИП_Уровень',
                        'АДП_Стен': 'АДП_Уровень',
                        'ДП_Стен': 'ДП_Уровень',
                        'СР_Стен': 'СР_Уровень',
                        }

        dct_rename_svod_sub = {'ИП_Стен': 'Интегральный показатель девиантного поведения',
                               'АДП_Стен': 'Аддитивное поведение',
                               'ДП_Стен': 'Делинквентное поведение',
                               'СР_Стен': 'Суицидальный риск',
                               }

        lst_sub = ['низкая склонность к ДП', 'значительная предрасположенность к ДП', 'высокая склонность к ДП']

        base_svod_sub_df = create_union_svod(base_df, dct_svod_sub, dct_rename_svod_sub, lst_sub)

        # считаем среднее значение по шкалам
        avg_ip = round(base_df['ИП_Значение'].mean(), 2)
        avg_k = round(base_df['АДП_Значение'].mean(), 2)
        avg_d = round(base_df['ДП_Значение'].mean(), 2)
        avg_s = round(base_df['СР_Значение'].mean(), 2)

        avg_dct = {'Среднее значение интегрального показателя': avg_ip,
                   'Среднее значение шкалы Аддитивное поведение': avg_k,
                   'Среднее значение шкалы Делинквентное поведение': avg_d,
                   'Среднее значение шкалы Суицидальный риск': avg_s,
                   }

        avg_df = pd.DataFrame.from_dict(avg_dct, orient='index')
        avg_df = avg_df.reset_index()
        avg_df.columns = ['Показатель', 'Среднее значение']

        # формируем основной словарь
        out_dct = {'Списочный результат': base_df,
                   'Список для проверки': out_answer_df,
                   'Свод Шкалы': base_svod_sub_df,
                   'Среднее': avg_df,
                   }

        dct_prefix = {'ИП_Уровень': 'ИП',
                      'АДП_Уровень': 'АДП',
                      'ДП_Уровень': 'ДП',
                      'СР_Уровень': 'СР',
                      }

        out_dct = create_list_on_level_dapp_school(base_df, out_dct, lst_sub, dct_prefix)
        """
                        Сохраняем в зависимости от необходимости делать своды по определенным колонкам
                        """
        if len(lst_svod_cols) == 0:
            return out_dct, part_df

        else:
            out_dct = create_result_dapp_school(base_df, out_dct, lst_svod_cols)
            return out_dct, part_df

    except BadOrderDAPPS:
        messagebox.showerror('Лахеcис',
                             f'При обработке вопросов теста ДАП-П для школьников обнаружены неправильные вопросы. Проверьте названия колонок с вопросами:\n'
                             f'{error_order_message[:5000]}\n'
                             f'Используйте при создании Яндекс-формы написание вопросов из руководства пользователя программы Лахесис.')
    except BadValueDAPPS:
        messagebox.showerror('Лахеcис',
                             f'При обработке вопросов теста ДАП-П для школьников обнаружены неправильные варианты ответов. Проверьте ответы на указанных строках:\n'
                             f'{error_message[:5000]}\n'
                             f'Используйте при создании Яндекс-формы написание вариантов ответа из руководства пользователя программы Лахесис.')


    except BadCountColumnsDAPPS:
        messagebox.showerror('Лахеcис',
                             f'Проверьте количество колонок с ответами на тест ДАП-П для школьников\n'
                             f'Должно быть 48 колонок с ответами')












