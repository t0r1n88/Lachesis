"""
Скрипт для обработки результатов теста Склонность к девиантному поведению Леуса
"""

import pandas as pd
from tkinter import messagebox
from lachesis_support_functions import round_mean,round_mean_two

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
        return calc_mean_df
    else:
        calc_mean_df = pd.pivot_table(df, index=lst_cat,
                                           values=val_cat,
                                           aggfunc=round_mean)
        calc_mean_df.reset_index(inplace=True)
        return calc_mean_df



def calc_count(df:pd.DataFrame,type_calc:str,lst_cat:list,val_cat,col_cat,lst_cols:list):
    """
    Функция для создания сводных датафреймов

    :param df: датафрейм с данными
    :param type_calc:тип обработки Группа или Курс
    :param lst_cat:список колонок по которым будет формироваться свод
    :param val_cat:значение по которому будет формиваться свод
    :param col_cat: колонка по которой будет формироваться свод
    :param lst_cols:список колонок для правильного порядка сводной таблицы
    :return:датафрейм
    """
    if type_calc == 'Группа':
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
    else:
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


def count_all_scale(df:pd.DataFrame, lst_cols:list,lst_index:list):
    """
    Функция для подсчета уровней по всем шкалам
    :param df: датарфейм
    :param lst_cols: список колонок по которым нужно вести обработку
    :param lst_index: список индексов
    :return:датафрейм
    """
    base_df = pd.DataFrame(index=lst_index) # базовый датафрейм с индексами
    for scale in lst_cols:
        scale_df = pd.pivot_table(df, index=f'Уровень_шкалы_{scale}',
                                                  values=f'Значение_шкалы_{scale}',
                                                  aggfunc='count')

        scale_df[f'{scale}% от общего'] = round(
            scale_df[f'Значение_шкалы_{scale}'] / scale_df[f'Значение_шкалы_{scale}'].sum(),3) * 100
        scale_df.rename(columns={f'Значение_шкалы_{scale}':f'Количество_{scale}'},inplace=True)

        # # Создаем суммирующую строку
        scale_df.loc['Итого'] = scale_df.sum()


        base_df = base_df.join(scale_df)

    base_df = base_df.reset_index()
    base_df.rename(columns={'index':'Степень дезадаптации'},inplace=True)
    return base_df






def processing_leus_sdp(base_df: pd.DataFrame, answers_df: pd.DataFrame):
    """
    Функция для обработки
    :param base_df: часть датафрейма с описательными колонками
    :param answers_df: часть датафрейма с ответами
    """
    try:
        out_answer_df = base_df.copy()  # делаем копию для последующего соединения с сырыми ответами
        if len(answers_df.columns) != 75:  # проверяем количество колонок с вопросами
            raise BadCountColumnsSDP

        lst_check_cols = ['Я всегда сдерживаю свои обещания','У меня бывают мысли, которыми я не хотел бы делиться',
                          'Разозлившись, я нередко выхожу из себя','Бывает, что я сплетничаю',
                          'Бывает, что я говорю о вещах, в которых ничего не смыслю','Я всегда говорю только правду',
                          'Я люблю прихвастнуть','Я никогда не опаздываю',
                          'Все свои привычки я считаю хорошими','Бывает, спорю и ссорюсь с родителями',
                          'Бывает, я перехожу улицу там, где мне удобно, а не там, где положено','Я всегда покупаю билет в транспорте',
                          'Бывает, мне хочется выругаться грубыми нецензурными словами','Среди моих знакомых есть люди, которые мне не нравятся',
                          'Я никогда не нарушаю правил общественного поведения','Я не хочу учиться и работать',
                          'Я могу уйти из дома жить в другое место','Меня забирали в полицию за плохое поведение',
                          'Я могу взять чужое, если мне надо или очень хочется','Состою на учете в подразделении по делам несовершеннолетних',
                          'Меня часто обижают окружающие (обзывают, бьют, отбирают деньги и вещи)','У меня есть судимые родственники и/или знакомые',
                          'У меня бывают сильные желания, которые обязательно надо исполнить','У меня бывает желание отомстить, восстановить справедливость',
                          'Я не верю окружающим','Хочу быть великим и всесильным',
                          'Я испытываю отчаяние, обиду, бессильный гнев','Я завидую своим одноклассникам, другим людям, взрослым',
                          'Если нельзя, но очень хочется – значит можно','Сильным и богатым людям необязательно соблюдать все правила и законы',
                          'Я курю','Я употребляю пиво и/или другие спиртные напитки',
                          'Я нюхал клей, растворители, пробовал наркотики, курительные смеси','Мои родители злоупотребляют спиртным',
                          'Мои друзья курят, употребляют спиртное','Люди пьют за компанию, для поддержания хорошего настроения',
                          'Пить и курить – это признаки взрослости','Я пью/курю из-за проблем в семье, школе, от одиночества',
                          'Дети и взрослые пьют и курят, потому что это модно и доступно','Дети пьют и курят из любопытства, по глупости',
                          'Удовольствие — это главное, к чему стоит стремиться в жизни','Мне необходимы сильные переживания и чувства',
                          'Я хотел бы попробовать спиртное, сигареты, наркотики, если бы этого никто не узнал','Вредное воздействие на человека алкоголя и табака сильно преувеличивают',
                          'Если в моей компании будет принято, то и я буду курить и пить пиво','Я редко жалею животных, людей',
                          'Я часто пререкаюсь или ругаюсь с учителями, одноклассниками','Я часто ссорюсь с родителями',
                          'Я не прощаю обиды','Если у меня плохое настроение, то я испорчу его еще кому-нибудь',
                          'Люблю посплетничать','Люблю, чтобы мне подчинялись',
                          'Предпочитаю споры решать дракой, а не словами','За компанию с друзьями могу что-нибудь сломать, приставать к посторонним',
                          'Часто испытываю раздражение, отвращение, злость, ярость, бешенство','У меня бывает желание что-то сломать, громко хлопнуть дверью, покричать, поругаться или подраться',
                          'В порыве гнева я могу накричать или ударить кого-то','Я охотно бы участвовал в каких-нибудь боевых действиях',
                          'Могу нарочно испортить чужую вещь, если мне что-то не нравится','Я хочу быть взрослым и сильным',
                          'Я чувствую, что меня никто не понимает, мной никто не интересуется','Я чувствую, что от меня ничего не зависит, безнадежность, беспомощность',
                          'Я могу причинить себе боль','Я бы взялся за опасное для жизни дело, если бы за это хорошо заплатили',
                          'Было бы лучше, если бы я умер','Я испытываю чувство вины перед окружающими, родителями',
                          'Я не люблю решать проблемы сам','У меня есть желания, которые никак не могут исполниться',
                          'Я не очень хороший человек','Я не всегда понимаю, что можно делать, а что нельзя',
                          'Я часто не могу решиться на какой-либо поступок','Когда я стою на мосту, то меня иногда так и тянет прыгнуть вниз',
                          'Я нуждаюсь в теплых, доверительных отношениях','Терпеть боль назло мне бывает даже приятно',
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

        base_df['Норма_СДП'] = '0-10 баллов'
        base_df['Значение_шкалы_СОП'] =answers_df.iloc[:,:15].sum(axis=1)
        base_df['Уровень_шкалы_СОП'] = base_df['Значение_шкалы_СОП'].apply(calc_level_sdp)

        base_df['Значение_шкалы_ДП'] =answers_df.iloc[:,15:30].sum(axis=1)
        base_df['Уровень_шкалы_ДП'] = base_df['Значение_шкалы_ДП'].apply(calc_level_sdp)

        base_df['Значение_шкалы_ЗП'] =answers_df.iloc[:,30:45].sum(axis=1)
        base_df['Уровень_шкалы_ЗП'] = base_df['Значение_шкалы_ЗП'].apply(calc_level_sdp)

        base_df['Значение_шкалы_АП'] =answers_df.iloc[:,45:60].sum(axis=1)
        base_df['Уровень_шкалы_АП'] = base_df['Значение_шкалы_АП'].apply(calc_level_sdp)

        base_df['Значение_шкалы_СП'] =answers_df.iloc[:,60:75].sum(axis=1)
        base_df['Уровень_шкалы_СП'] = base_df['Значение_шкалы_СП'].apply(calc_level_sdp)

        # Создаем датафрейм для создания части в общий датафрейм
        part_df = pd.DataFrame(columns=['СДП_Значение_шкалы_СОП', 'СДП_Уровень_шкалы_СОП',
                                        'СДП_Значение_шкалы_ДП', 'СДП_Уровень_шкалы_ДП',
                                        'СДП_Значение_шкалы_ЗП', 'СДП_Уровень_шкалы_ЗП',
                                        'СДП_Значение_шкалы_АП', 'СДП_Уровень_шкалы_АП',
                                        'СДП_Значение_шкалы_СП', 'СДП_Уровень_шкалы_СП',
                                        ])
        part_df['СДП_Значение_шкалы_СОП'] = base_df['Значение_шкалы_СОП']
        part_df['СДП_Уровень_шкалы_СОП'] = base_df['Уровень_шкалы_СОП']

        part_df['СДП_Значение_шкалы_ДП'] = base_df['Значение_шкалы_ДП']
        part_df['СДП_Уровень_шкалы_ДП'] = base_df['Уровень_шкалы_ДП']

        part_df['СДП_Значение_шкалы_ЗП'] = base_df['Значение_шкалы_ЗП']
        part_df['СДП_Уровень_шкалы_ЗП'] = base_df['Уровень_шкалы_ЗП']

        part_df['СДП_Значение_шкалы_АП'] = base_df['Значение_шкалы_АП']
        part_df['СДП_Уровень_шкалы_АП'] = base_df['Уровень_шкалы_АП']

        part_df['СДП_Значение_шкалы_СП'] = base_df['Значение_шкалы_СП']
        part_df['СДП_Уровень_шкалы_СП'] = base_df['Уровень_шкалы_СП']

        base_df.sort_values(by='Значение_шкалы_СОП', ascending=False, inplace=True)  # сортируем
        out_answer_df = pd.concat([out_answer_df, answers_df], axis=1)  # Датафрейм для проверки

        #Общий свод сколько склонностей всего в процентном соотношении
        svod_all_df = count_all_scale(base_df,['СОП','ДП','ЗП','АП','СП',],['отсутствие признаков социально-психологической дезадаптации', 'легкая степень социально-психологической дезадаптации',
                 'выраженная социально-психологическая дезадаптация','Итого'])

        lst_reindex_group_cols = ['Группа', 'отсутствие признаков социально-психологической дезадаптации', 'легкая степень социально-психологической дезадаптации',
                 'выраженная социально-психологическая дезадаптация','Итого']
        lst_reindex_group_sex_cols = ['Группа','Пол', 'отсутствие признаков социально-психологической дезадаптации', 'легкая степень социально-психологической дезадаптации',
                 'выраженная социально-психологическая дезадаптация','Итого']

        lst_reindex_course_cols = ['Курс', 'отсутствие признаков социально-психологической дезадаптации', 'легкая степень социально-психологической дезадаптации',
                 'выраженная социально-психологическая дезадаптация','Итого']
        lst_reindex_course_sex_cols = ['Курс','Пол','отсутствие признаков социально-психологической дезадаптации', 'легкая степень социально-психологической дезадаптации',
                 'выраженная социально-психологическая дезадаптация','Итого']

        """
            Обрабатываем Группа
            """

        # СОП
        svod_group_sop_df = calc_mean(base_df,'Группа',['Группа'],'Значение_шкалы_СОП')
        svod_count_group_sop_df = calc_count(base_df,'Группа',['Группа'],'Значение_шкалы_СОП','Уровень_шкалы_СОП',lst_reindex_group_cols)
        # ДП
        svod_group_dp_df = calc_mean(base_df,'Группа',['Группа'],'Значение_шкалы_ДП')
        svod_count_group_dp_df = calc_count(base_df,'Группа',['Группа'],'Значение_шкалы_ДП','Уровень_шкалы_ДП',lst_reindex_group_cols)

        # ЗП
        svod_group_zp_df = calc_mean(base_df,'Группа',['Группа'],'Значение_шкалы_ЗП')
        svod_count_group_zp_df = calc_count(base_df,'Группа',['Группа'],'Значение_шкалы_ЗП','Уровень_шкалы_ЗП',lst_reindex_group_cols)

        # АП
        svod_group_ap_df = calc_mean(base_df,'Группа',['Группа'],'Значение_шкалы_АП')
        svod_count_group_ap_df = calc_count(base_df,'Группа',['Группа'],'Значение_шкалы_АП','Уровень_шкалы_АП',lst_reindex_group_cols)

        # СП
        svod_group_sp_df = calc_mean(base_df,'Группа',['Группа'],'Значение_шкалы_СП')
        svod_count_group_sp_df = calc_count(base_df,'Группа',['Группа'],'Значение_шкалы_СП','Уровень_шкалы_СП',lst_reindex_group_cols)

        """
            Обрабатываем Группа Пол
            """
        # СОП
        svod_group_sex_sop_df = calc_mean(base_df,'Группа',['Группа','Пол'],'Значение_шкалы_СОП')
        svod_count_group_sex_sop_df = calc_count(base_df,'Группа',['Группа','Пол'],'Значение_шкалы_СОП','Уровень_шкалы_СОП',lst_reindex_group_sex_cols)

        # ДП
        svod_group_sex_dp_df = calc_mean(base_df,'Группа',['Группа','Пол'],'Значение_шкалы_ДП')
        svod_count_group_sex_dp_df = calc_count(base_df,'Группа',['Группа','Пол'],'Значение_шкалы_ДП','Уровень_шкалы_ДП',lst_reindex_group_sex_cols)

        # ЗП
        svod_group_sex_zp_df = calc_mean(base_df,'Группа',['Группа','Пол'],'Значение_шкалы_ЗП')
        svod_count_group_sex_zp_df = calc_count(base_df,'Группа',['Группа','Пол'],'Значение_шкалы_ЗП','Уровень_шкалы_ЗП',lst_reindex_group_sex_cols)

        # АП
        svod_group_sex_ap_df = calc_mean(base_df,'Группа',['Группа','Пол'],'Значение_шкалы_АП')
        svod_count_group_sex_ap_df = calc_count(base_df,'Группа',['Группа','Пол'],'Значение_шкалы_АП','Уровень_шкалы_АП',lst_reindex_group_sex_cols)

        # СП
        svod_group_sex_sp_df = calc_mean(base_df,'Группа',['Группа','Пол'],'Значение_шкалы_СП')
        svod_count_group_sex_sp_df = calc_count(base_df,'Группа',['Группа','Пол'],'Значение_шкалы_СП','Уровень_шкалы_СП',lst_reindex_group_sex_cols)

        """
            Обрабатываем Курс
            """

        # СОП
        svod_course_sop_df = calc_mean(base_df, 'Курс', ['Курс'], 'Значение_шкалы_СОП')
        svod_count_course_sop_df = calc_count(base_df, 'Курс', ['Курс'], 'Значение_шкалы_СОП', 'Уровень_шкалы_СОП',
                                              lst_reindex_course_cols)
        # ДП
        svod_course_dp_df = calc_mean(base_df, 'Курс', ['Курс'], 'Значение_шкалы_ДП')
        svod_count_course_dp_df = calc_count(base_df, 'Курс', ['Курс'], 'Значение_шкалы_ДП', 'Уровень_шкалы_ДП',
                                             lst_reindex_course_cols)

        # ЗП
        svod_course_zp_df = calc_mean(base_df, 'Курс', ['Курс'], 'Значение_шкалы_ЗП')
        svod_count_course_zp_df = calc_count(base_df, 'Курс', ['Курс'], 'Значение_шкалы_ЗП', 'Уровень_шкалы_ЗП',
                                             lst_reindex_course_cols)

        # АП
        svod_course_ap_df = calc_mean(base_df, 'Курс', ['Курс'], 'Значение_шкалы_АП')
        svod_count_course_ap_df = calc_count(base_df, 'Курс', ['Курс'], 'Значение_шкалы_АП', 'Уровень_шкалы_АП',
                                             lst_reindex_course_cols)

        # СП
        svod_course_sp_df = calc_mean(base_df, 'Курс', ['Курс'], 'Значение_шкалы_СП')
        svod_count_course_sp_df = calc_count(base_df, 'Курс', ['Курс'], 'Значение_шкалы_СП', 'Уровень_шкалы_СП',
                                             lst_reindex_course_cols)

        """
            Обрабатываем Курс Пол
            """
        # СОП
        svod_course_sex_sop_df = calc_mean(base_df, 'Курс', ['Курс', 'Пол'], 'Значение_шкалы_СОП')
        svod_count_course_sex_sop_df = calc_count(base_df, 'Курс', ['Курс', 'Пол'], 'Значение_шкалы_СОП',
                                                  'Уровень_шкалы_СОП', lst_reindex_course_sex_cols)

        # ДП
        svod_course_sex_dp_df = calc_mean(base_df, 'Курс', ['Курс', 'Пол'], 'Значение_шкалы_ДП')
        svod_count_course_sex_dp_df = calc_count(base_df, 'Курс', ['Курс', 'Пол'], 'Значение_шкалы_ДП', 'Уровень_шкалы_ДП',
                                                 lst_reindex_course_sex_cols)

        # ЗП
        svod_course_sex_zp_df = calc_mean(base_df, 'Курс', ['Курс', 'Пол'], 'Значение_шкалы_ЗП')
        svod_count_course_sex_zp_df = calc_count(base_df, 'Курс', ['Курс', 'Пол'], 'Значение_шкалы_ЗП', 'Уровень_шкалы_ЗП',
                                                 lst_reindex_course_sex_cols)

        # АП
        svod_course_sex_ap_df = calc_mean(base_df, 'Курс', ['Курс', 'Пол'], 'Значение_шкалы_АП')
        svod_count_course_sex_ap_df = calc_count(base_df, 'Курс', ['Курс', 'Пол'], 'Значение_шкалы_АП', 'Уровень_шкалы_АП',
                                                 lst_reindex_course_sex_cols)

        # СП
        svod_course_sex_sp_df = calc_mean(base_df, 'Курс', ['Курс', 'Пол'], 'Значение_шкалы_СП')
        svod_count_course_sex_sp_df = calc_count(base_df, 'Курс', ['Курс', 'Пол'], 'Значение_шкалы_СП', 'Уровень_шкалы_СП',
                                                 lst_reindex_course_sex_cols)

        out_dct = {'Списочный результат': base_df, 'Список для проверки': out_answer_df,
                   'Общий свод':svod_all_df,
                   'Среднее Группа СОП':svod_group_sop_df,'Количество Группа СОП':svod_count_group_sop_df,
                   'Среднее Группа ДП':svod_group_dp_df,'Количество Группа ДП':svod_count_group_dp_df,
                   'Среднее Группа ЗП':svod_group_zp_df,'Количество Группа ЗП':svod_count_group_zp_df,
                   'Среднее Группа АП':svod_group_ap_df,'Количество Группа АП':svod_count_group_ap_df,
                   'Среднее Группа СП':svod_group_sp_df,'Количество Группа СП':svod_count_group_sp_df,

                   'Среднее Группа Пол СОП':svod_group_sex_sop_df,'Количество Группа Пол СОП':svod_count_group_sex_sop_df,
                   'Среднее Группа Пол ДП':svod_group_sex_dp_df,'Количество Группа Пол ДП':svod_count_group_sex_dp_df,
                   'Среднее Группа Пол ЗП':svod_group_sex_zp_df,'Количество Группа Пол ЗП':svod_count_group_sex_zp_df,
                   'Среднее Группа Пол АП':svod_group_sex_ap_df,'Количество Группа Пол АП':svod_count_group_sex_ap_df,
                   'Среднее Группа Пол СП':svod_group_sex_sp_df,'Количество Группа Пол СП':svod_count_group_sex_sp_df,


                   'Среднее Курс СОП': svod_course_sop_df, 'Количество Курс СОП': svod_count_course_sop_df,
                   'Среднее Курс ДП': svod_course_dp_df, 'Количество Курс ДП': svod_count_course_dp_df,
                   'Среднее Курс ЗП': svod_course_zp_df, 'Количество Курс ЗП': svod_count_course_zp_df,
                   'Среднее Курс АП': svod_course_ap_df, 'Количество Курс АП': svod_count_course_ap_df,
                   'Среднее Курс СП': svod_course_sp_df, 'Количество Курс СП': svod_count_course_sp_df,

                   'Среднее Курс Пол СОП': svod_course_sex_sop_df, 'Количество Курс Пол СОП': svod_count_course_sex_sop_df,
                   'Среднее Курс Пол ДП': svod_course_sex_dp_df, 'Количество Курс Пол ДП': svod_count_course_sex_dp_df,
                   'Среднее Курс Пол ЗП': svod_course_sex_zp_df, 'Количество Курс Пол ЗП': svod_count_course_sex_zp_df,
                   'Среднее Курс Пол АП': svod_course_sex_ap_df, 'Количество Курс Пол АП': svod_count_course_sex_ap_df,
                   'Среднее Курс Пол СП': svod_course_sex_sp_df, 'Количество Курс Пол СП': svod_count_course_sex_sp_df,

                   }

        return out_dct, part_df
    except BadOrderSDP:
        messagebox.showerror('Лахеcис',
                             f'При обработке вопросов теста Склонность к девиантному поведению Леус обнаружены неправильные вопросы. Проверьте названия колонок с вопросами:\n'
                             f'{error_order_message}\n'
                             f'Используйте при создании Яндекс-формы написание вопросов из руководства пользователя программы Лахесис.')
    except BadValueSDP:
        messagebox.showerror('Лахеcис',
                             f'При обработке вопросов теста Склонность к девиантному поведению Леус обнаружены неправильные варианты ответов. Проверьте ответы на указанных строках:\n'
                             f'{error_message}\n'
                             f'Используйте при создании Яндекс-формы написание вариантов ответа из руководства пользователя программы Лахесис.')


    except BadCountColumnsSDP:
        messagebox.showerror('Лахеcис',
                             f'Проверьте количество колонок с ответами на тест Склонность к девиантному поведению Леус\n'
                             f'Должно быть 75 колонок с ответами')








