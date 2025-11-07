"""
Скрипт для обработки результатов теста Склонность к девиантному поведению Леуса
"""

import pandas as pd
import re
from tkinter import messagebox
from lachesis_support_functions import round_mean,create_union_svod,create_list_on_level

class BadOrderSDP(Exception):
    """
    Исключение для обработки случая когда колонки не совпадают
    """
    pass


class BadValueSDP(Exception):
    """
    Исключение для неправильных значений в вариантах ответов
    """
    pass

class BadCountColumnsSDP(Exception):
    """
    Исключение для обработки случая если количество колонок не равно 75
    """
    pass

def calc_level_sdp(value):
    """
    Функция для подсчета уровня склонности
    """
    if 0 <= value <= 10:
        return 'отсутствие признаков социально-психологической дезадаптации'
    elif 11 <= value <= 20:
        return 'легкая степень социально-психологической дезадаптации'
    elif 21 <= value <= 30:
        return 'выраженная социально-психологическая дезадаптация'



def calc_count_level(df:pd.DataFrame, lst_cat:list, val_cat, col_cat, lst_cols:list):
    """
    Функция для создания сводных датафреймов по шкалам

    :param df: датафрейм с данными
    :param lst_cat:список колонок по которым будет формироваться свод
    :param val_cat:значение по которому будет формироваться свод
    :param col_cat: колонка по которой будет формироваться свод
    :param lst_cols: список с колонками
    :return:датафрейм
    """
    count_df = pd.pivot_table(df, index=lst_cat,
                                             columns=col_cat,
                                             values=val_cat,
                                             aggfunc='count', margins=True, margins_name='Итого')


    count_df.reset_index(inplace=True)
    count_df = count_df.reindex(columns=lst_cols)
    count_df['% отсутствие признаков социально-психологической дезадаптации от общего'] = round(
        count_df['отсутствие признаков социально-психологической дезадаптации'] / count_df['Итого'], 2) * 100
    count_df['% легкая степень социально-психологической дезадаптации от общего'] = round(
        count_df['легкая степень социально-психологической дезадаптации'] / count_df['Итого'], 2) * 100
    count_df['% выраженная социально-психологическая дезадаптация от общего'] = round(
        count_df['выраженная социально-психологическая дезадаптация'] / count_df['Итого'], 2) * 100

    return count_df



def create_sdp_list_on_level(base_df:pd.DataFrame,out_dct:dict,lst_level:list,dct_prefix:dict):
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
                if level == 'отсутствие признаков социально-психологической дезадаптации':
                    level = 'отсутствует'
                elif level == 'легкая степень социально-психологической дезадаптации':
                    level = 'легкая'
                else:
                    level = 'выраженная'
                dct_level[f'{dct_prefix[key]}. {level}'] = temp_df
        out_dct.update(dct_level)

    return out_dct

def create_result_sdp(base_df:pd.DataFrame, out_dct:dict, lst_svod_cols:list):
    """
    Функция для подсчета результата если указаны колонки по которым нужно провести свод
    :param df: датафрейм с результатами
    :param out_dct: словарь с уже подсчитанными базовыми данными
    :param lst_svod_cols: список сводных колонок
    :return: словарь
    """
    lst_reindex_one_level_cols = lst_svod_cols.copy()
    lst_reindex_one_level_cols.extend( ['отсутствие признаков социально-психологической дезадаптации',
                                        'легкая степень социально-психологической дезадаптации', 'выраженная социально-психологическая дезадаптация',
                                                      'Итого'])

    # Субшкалы
    svod_count_one_level_sop_df = calc_count_level(base_df, lst_svod_cols,
                                                      'Значение_шкалы_СОП',
                                                      'Уровень_шкалы_СОП',
                                                      lst_reindex_one_level_cols)

    svod_count_one_level_dp_df = calc_count_level(base_df, lst_svod_cols,
                                                          'Значение_шкалы_ДП',
                                                          'Уровень_шкалы_ДП',
                                                          lst_reindex_one_level_cols)

    svod_count_one_level_zp_df = calc_count_level(base_df, lst_svod_cols,
                                                         'Значение_шкалы_ЗП',
                                                         'Уровень_шкалы_ЗП',
                                                         lst_reindex_one_level_cols)
    svod_count_one_level_ap_df = calc_count_level(base_df, lst_svod_cols,
                                                         'Значение_шкалы_АП',
                                                         'Уровень_шкалы_АП',
                                                         lst_reindex_one_level_cols)
    svod_count_one_level_sp_df = calc_count_level(base_df, lst_svod_cols,
                                                         'Значение_шкалы_СП',
                                                         'Уровень_шкалы_СП',
                                                         lst_reindex_one_level_cols)

    # Считаем среднее по субшкалам
    svod_mean_one_df = pd.pivot_table(base_df,
                                      index=lst_svod_cols,
                                      values=['Значение_шкалы_СОП',
                                              'Значение_шкалы_ДП',
                                              'Значение_шкалы_ЗП',
                                              'Значение_шкалы_АП',
                                              'Значение_шкалы_СП',
                                              ],
                                      aggfunc=round_mean)
    svod_mean_one_df.reset_index(inplace=True)
    # упорядочиваем колонки
    new_order_cols = lst_svod_cols.copy()
    new_order_cols.extend((['Значение_шкалы_СОП',
                            'Значение_шкалы_ДП',
                            'Значение_шкалы_ЗП',
                            'Значение_шкалы_АП',
                            'Значение_шкалы_СП',
                            ]))
    svod_mean_one_df = svod_mean_one_df.reindex(columns=new_order_cols)

    dct_rename_cols_mean = {'Значение_шкалы_СОП': 'Ср. СОП',
                            'Значение_шкалы_ДП': 'Ср. ДП',
                            'Значение_шкалы_ЗП': 'Ср. ЗП',
                            'Значение_шкалы_АП': 'Ср. АП',
                            'Значение_шкалы_СП': 'Ср. СП',
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
                    f'Свод СОП {out_name}': svod_count_one_level_sop_df,
                    f'Свод ДП {out_name}': svod_count_one_level_dp_df,
                    f'Свод ЗП {out_name}': svod_count_one_level_zp_df,
                    f'Свод АП {out_name}': svod_count_one_level_ap_df,
                    f'Свод СП {out_name}': svod_count_one_level_sp_df})
    if len(lst_svod_cols) == 1:
        return out_dct
    else:
        for idx, name_column in enumerate(lst_svod_cols):
            # Тревожность
            lst_reindex_column_level_cols = [lst_svod_cols[idx],'отсутствие признаков социально-психологической дезадаптации',
                                        'легкая степень социально-психологической дезадаптации', 'выраженная социально-психологическая дезадаптация',
                                             'Итого']

            # Субшкалы
            svod_count_column_level_sop_df = calc_count_level(base_df, lst_svod_cols[idx],
                                                              'Значение_шкалы_СОП',
                                                              'Уровень_шкалы_СОП',
                                                              lst_reindex_column_level_cols)

            svod_count_column_level_dp_df = calc_count_level(base_df, lst_svod_cols[idx],
                                                             'Значение_шкалы_ДП',
                                                             'Уровень_шкалы_ДП',
                                                             lst_reindex_column_level_cols)

            svod_count_column_level_zp_df = calc_count_level(base_df, lst_svod_cols[idx],
                                                             'Значение_шкалы_ЗП',
                                                             'Уровень_шкалы_ЗП',
                                                             lst_reindex_column_level_cols)
            svod_count_column_level_ap_df = calc_count_level(base_df, lst_svod_cols[idx],
                                                             'Значение_шкалы_АП',
                                                             'Уровень_шкалы_АП',
                                                             lst_reindex_column_level_cols)
            svod_count_column_level_sp_df = calc_count_level(base_df, lst_svod_cols[idx],
                                                             'Значение_шкалы_СП',
                                                             'Уровень_шкалы_СП',
                                                             lst_reindex_column_level_cols)

            # Считаем среднее по субшкалам
            svod_mean_column_df = pd.pivot_table(base_df,
                                                 index=[lst_svod_cols[idx]],
                                                 values=['Значение_шкалы_СОП',
                                                         'Значение_шкалы_ДП',
                                                         'Значение_шкалы_ЗП',
                                                         'Значение_шкалы_АП',
                                                         'Значение_шкалы_СП',
                                                         ],
                                                 aggfunc=round_mean)
            svod_mean_column_df.reset_index(inplace=True)
            # упорядочиваем колонки
            new_order_cols = [lst_svod_cols[idx]].copy()
            new_order_cols.extend((['Значение_шкалы_СОП',
                                    'Значение_шкалы_ДП',
                                    'Значение_шкалы_ЗП',
                                    'Значение_шкалы_АП',
                                    'Значение_шкалы_СП',
                                    ]))
            svod_mean_column_df = svod_mean_column_df.reindex(columns=new_order_cols)

            dct_rename_cols_mean = {'Значение_шкалы_СОП': 'Ср. СОП',
                                    'Значение_шкалы_ДП': 'Ср. ДП',
                                    'Значение_шкалы_ЗП': 'Ср. ЗП',
                                    'Значение_шкалы_АП': 'Ср. АП',
                                    'Значение_шкалы_СП': 'Ср. СП',
                                    }
            svod_mean_column_df.rename(columns=dct_rename_cols_mean, inplace=True)

            name_column = lst_svod_cols[idx]
            name_column = re.sub(r'[\[\]\'+()<> :"?*|\\/]', '_', name_column)
            name_column = name_column[:15]

            out_dct.update({f'Ср {name_column}': svod_mean_column_df,
                            f'Свод СОП {name_column}': svod_count_column_level_sop_df,
                            f'Свод ДП {name_column}': svod_count_column_level_dp_df,
                            f'Свод ЗП {name_column}': svod_count_column_level_zp_df,
                            f'Свод АП {name_column}': svod_count_column_level_ap_df,
                            f'Свод СП {name_column}': svod_count_column_level_sp_df})
        return out_dct






def processing_leus_sdp(result_df: pd.DataFrame, answers_df: pd.DataFrame, lst_svod_cols:list):
    """
    Функция для обработки
    :param result_df: часть датафрейма с описательными колонками
    :param answers_df: часть датафрейма с ответами
    :param lst_svod_cols:  список с колонками по которым нужно делать свод
    """
    try:
        out_answer_df = result_df.copy()  # делаем копию для последующего соединения с сырыми ответами
        if len(answers_df.columns) != 75:  # проверяем количество колонок с вопросами
            raise BadCountColumnsSDP

        # очищаем названия колонок от возможных сочетаний .1 которые добавляет пандас при одинаковых колонках
        clean_df_lst = []
        for name_column in answers_df.columns:
            clean_name = re.sub(r'.\d+$', '', name_column)
            clean_df_lst.append(clean_name)

        answers_df.columns = clean_df_lst

        lst_check_cols = ['Я всегда сдерживаю свои обещания', 'У меня бывают мысли, которыми я не хотел бы делиться',
                          'Разозлившись, я нередко выхожу из себя', 'Бывает, что я сплетничаю',
                          'Бывает, что я говорю о вещах, в которых ничего не смыслю', 'Я всегда говорю только правду',
                          'Я люблю прихвастнуть', 'Я никогда не опаздываю',
                          'Все свои привычки я считаю хорошими', 'Бывает, спорю и ссорюсь с родителями',
                          'Бывает, я перехожу улицу там, где мне удобно, а не там, где положено',
                          'Я всегда покупаю билет в транспорте',
                          'Бывает, мне хочется выругаться грубыми нецензурными словами',
                          'Среди моих знакомых есть люди, которые мне не нравятся',
                          'Я никогда не нарушаю правил общественного поведения', 'Я не хочу учиться и работать',
                          'Я могу уйти из дома жить в другое место', 'Меня забирали в полицию за плохое поведение',
                          'Я могу взять чужое, если мне надо или очень хочется',
                          'Состою на учете в подразделении по делам несовершеннолетних',
                          'Меня часто обижают окружающие (обзывают, бьют, отбирают деньги и вещи)',
                          'У меня есть судимые родственники и/или знакомые',
                          'У меня бывают сильные желания, которые обязательно надо исполнить',
                          'У меня бывает желание отомстить, восстановить справедливость',
                          'Я не верю окружающим', 'Хочу быть великим и всесильным',
                          'Я испытываю отчаяние, обиду, бессильный гнев',
                          'Я завидую своим одноклассникам, другим людям, взрослым',
                          'Если нельзя, но очень хочется – значит можно',
                          'Сильным и богатым людям необязательно соблюдать все правила и законы',
                          'Я курю', 'Я употребляю пиво и/или другие спиртные напитки',
                          'Я нюхал клей, растворители, пробовал наркотики, курительные смеси',
                          'Мои родители злоупотребляют спиртным',
                          'Мои друзья курят, употребляют спиртное',
                          'Люди пьют за компанию, для поддержания хорошего настроения',
                          'Пить и курить – это признаки взрослости',
                          'Я пью/курю из-за проблем в семье, школе, от одиночества',
                          'Дети и взрослые пьют и курят, потому что это модно и доступно',
                          'Дети пьют и курят из любопытства, по глупости',
                          'Удовольствие — это главное, к чему стоит стремиться в жизни',
                          'Мне необходимы сильные переживания и чувства',
                          'Я хотел бы попробовать спиртное, сигареты, наркотики, если бы этого никто не узнал',
                          'Вредное воздействие на человека алкоголя и табака сильно преувеличивают',
                          'Если в моей компании будет принято, то и я буду курить и пить пиво',
                          'Я редко жалею животных, людей',
                          'Я часто пререкаюсь или ругаюсь с учителями, одноклассниками', 'Я часто ссорюсь с родителями',
                          'Я не прощаю обиды', 'Если у меня плохое настроение, то я испорчу его еще кому-нибудь',
                          'Люблю посплетничать', 'Люблю, чтобы мне подчинялись',
                          'Предпочитаю споры решать дракой, а не словами',
                          'За компанию с друзьями могу что-нибудь сломать, приставать к посторонним',
                          'Часто испытываю раздражение, отвращение, злость, ярость, бешенство',
                          'У меня бывает желание что-то сломать, громко хлопнуть дверью, покричать, поругаться или подраться',
                          'В порыве гнева я могу накричать или ударить кого-то',
                          'Я охотно бы участвовал в каких-нибудь боевых действиях',
                          'Могу нарочно испортить чужую вещь, если мне что-то не нравится',
                          'Я хочу быть взрослым и сильным',
                          'Я чувствую, что меня никто не понимает, мной никто не интересуется',
                          'Я чувствую, что от меня ничего не зависит, безнадежность, беспомощность',
                          'Я могу причинить себе боль',
                          'Я бы взялся за опасное для жизни дело, если бы за это хорошо заплатили',
                          'Было бы лучше, если бы я умер', 'Я испытываю чувство вины перед окружающими, родителями',
                          'Я не люблю решать проблемы сам', 'У меня есть желания, которые никак не могут исполниться',
                          'Я не очень хороший человек', 'Я не всегда понимаю, что можно делать, а что нельзя',
                          'Я часто не могу решиться на какой-либо поступок',
                          'Когда я стою на мосту, то меня иногда так и тянет прыгнуть вниз',
                          'Я нуждаюсь в теплых, доверительных отношениях', 'Терпеть боль назло мне бывает даже приятно',
                          'Я испытываю потребность в острых ощущениях'
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
            raise BadOrderSDP

        # словарь для замены слов на числа
        dct_replace_value = {'да': 2,
                             'иногда': 1,
                             'нет': 0
                             }

        valid_values = [0, 1, 2]
        answers_df.replace(dct_replace_value, inplace=True)  # заменяем слова на цифры для подсчетов

        # Проверяем, есть ли значения, отличающиеся от указанных в списке
        lst_error_answers = []  # список для хранения строк где найдены неправильные ответы

        for i in range(75):
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
            raise BadValueSDP

        base_df = pd.DataFrame()

        base_df['Значение_шкалы_СОП'] = answers_df.iloc[:, :15].sum(axis=1)
        base_df['Уровень_шкалы_СОП'] = base_df['Значение_шкалы_СОП'].apply(calc_level_sdp)

        base_df['Значение_шкалы_ДП'] = answers_df.iloc[:, 15:30].sum(axis=1)
        base_df['Уровень_шкалы_ДП'] = base_df['Значение_шкалы_ДП'].apply(calc_level_sdp)

        base_df['Значение_шкалы_ЗП'] = answers_df.iloc[:, 30:45].sum(axis=1)
        base_df['Уровень_шкалы_ЗП'] = base_df['Значение_шкалы_ЗП'].apply(calc_level_sdp)

        base_df['Значение_шкалы_АП'] = answers_df.iloc[:, 45:60].sum(axis=1)
        base_df['Уровень_шкалы_АП'] = base_df['Значение_шкалы_АП'].apply(calc_level_sdp)

        base_df['Значение_шкалы_СП'] = answers_df.iloc[:, 60:75].sum(axis=1)
        base_df['Уровень_шкалы_СП'] = base_df['Значение_шкалы_СП'].apply(calc_level_sdp)

        # Создаем датафрейм для создания части в общий датафрейм
        part_df = pd.DataFrame()
        part_df['СДП_СОП_Значение'] = base_df['Значение_шкалы_СОП']
        part_df['СДП_СОП_Уровень'] = base_df['Уровень_шкалы_СОП']

        part_df['СДП_ДП_Значение'] = base_df['Значение_шкалы_ДП']
        part_df['СДП_ДП_Уровень'] = base_df['Уровень_шкалы_ДП']

        part_df['СДП_ЗП_Значение'] = base_df['Значение_шкалы_ЗП']
        part_df['СДП_ЗП_Уровень'] = base_df['Уровень_шкалы_ЗП']

        part_df['СДП_АП_Значение'] = base_df['Значение_шкалы_АП']
        part_df['СДП_АП_Уровень'] = base_df['Уровень_шкалы_АП']

        part_df['СДП_СП_Значение'] = base_df['Значение_шкалы_СП']
        part_df['СДП_СП_Уровень'] = base_df['Уровень_шкалы_СП']

        out_answer_df = pd.concat([out_answer_df, answers_df], axis=1)  # Датафрейм для проверки
        base_df = pd.concat([result_df, base_df], axis=1)


        base_df.sort_values(by='Значение_шкалы_СОП', ascending=False, inplace=True)  # сортируем


        # Делаем свод  по  шкалам
        dct_svod_sub = {'Значение_шкалы_СОП': 'Уровень_шкалы_СОП',
                        'Значение_шкалы_ДП': 'Уровень_шкалы_ДП',
                        'Значение_шкалы_ЗП': 'Уровень_шкалы_ЗП',
                        'Значение_шкалы_АП': 'Уровень_шкалы_АП',
                        'Значение_шкалы_СП': 'Уровень_шкалы_СП',
                        }

        dct_rename_svod_sub = {'Значение_шкалы_СОП': 'СОП',
                               'Значение_шкалы_ДП': 'ДП',
                               'Значение_шкалы_ЗП': 'ЗП',
                               'Значение_шкалы_АП': 'АП',
                               'Значение_шкалы_СП': 'СП',
                               }

        # Списки для шкал
        lst_level = ['отсутствие признаков социально-психологической дезадаптации', 'легкая степень социально-психологической дезадаптации',
                     'выраженная социально-психологическая дезадаптация']


        base_svod_sub_df = create_union_svod(base_df, dct_svod_sub, dct_rename_svod_sub, lst_level)

        # считаем среднее значение по шкалам
        avg_sop = round(base_df['Значение_шкалы_СОП'].mean(), 2)
        avg_dp = round(base_df['Значение_шкалы_ДП'].mean(), 2)
        avg_zp = round(base_df['Значение_шкалы_ЗП'].mean(), 2)
        avg_ap = round(base_df['Значение_шкалы_АП'].mean(), 2)
        avg_sp = round(base_df['Значение_шкалы_СП'].mean(), 2)

        avg_dct = {'Среднее значение шкалы Социально обусловленное поведение': avg_sop,
                   'Среднее значение шкалы Делинквентное (допротивоправное) поведение': avg_dp,
                   'Среднее значение шкалы Зависимое (аддиктивное) поведение': avg_zp,
                   'Среднее значение шкалы Агрессивное поведение': avg_ap,
                   'Среднее значение шкалы Самоповреждающее (аутоагрессивное) поведение': avg_sp,
                   }

        avg_df = pd.DataFrame.from_dict(avg_dct, orient='index')
        avg_df = avg_df.reset_index()
        avg_df.columns = ['Показатель', 'Среднее значение']

        # формируем основной словарь
        out_dct = {'Списочный результат': base_df, 'Список для проверки': out_answer_df,
                   'Свод по шкалам': base_svod_sub_df,
                   'Среднее по шкалам': avg_df,
                   }

        # Делаем списки
        dct_prefix = {'Уровень_шкалы_СОП': 'СОП',
                      'Уровень_шкалы_ДП': 'ДП',
                      'Уровень_шкалы_ЗП': 'ЗП',
                      'Уровень_шкалы_АП': 'АП',
                      'Уровень_шкалы_СП': 'СП',
                      }

        out_dct = create_sdp_list_on_level(base_df, out_dct, lst_level, dct_prefix)

        """
            Сохраняем в зависимости от необходимости делать своды по определенным колонкам
            """
        if len(lst_svod_cols) == 0:
            return out_dct, part_df
        else:
            out_dct = create_result_sdp(base_df, out_dct, lst_svod_cols)

            return out_dct, part_df

    except BadOrderSDP:
        messagebox.showerror('Лахеcис',
                             f'При обработке вопросов теста Склонность к девиантному поведению Леус обнаружены неправильные вопросы. Проверьте названия колонок с вопросами:\n'
                             f'{error_order_message[:5000]}\n'
                             f'Используйте при создании Яндекс-формы написание вопросов из руководства пользователя программы Лахесис.')
    except BadValueSDP:
        messagebox.showerror('Лахеcис',
                             f'При обработке вопросов теста Склонность к девиантному поведению Леус обнаружены неправильные варианты ответов. Проверьте ответы на указанных строках:\n'
                             f'{error_message[:5000]}\n'
                             f'Используйте при создании Яндекс-формы написание вариантов ответа из руководства пользователя программы Лахесис.')


    except BadCountColumnsSDP:
        messagebox.showerror('Лахеcис',
                             f'Проверьте количество колонок с ответами на тест Склонность к девиантному поведению Леус\n'
                             f'Должно быть 75 колонок с ответами')













