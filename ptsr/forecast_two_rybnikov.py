"""
Скрипт для обработки результатов теста Методика оценки нервно-психической устойчивости «Прогноз-2»  В.Ю. Рыбников


"""
import pandas as pd
import re
from tkinter import messagebox
from lachesis_support_functions import round_mean,calc_count_scale,create_list_on_level


class BadOrderFTR(Exception):
    """
    Исключение для обработки случая когда колонки не совпадают
    """
    pass


class BadValueFTR(Exception):
    """
    Исключение для неправильных значений в вариантах ответов
    """
    pass

class BadCountColumnsFTR(Exception):
    """
    Исключение для обработки случая если количество колонок не равно 86
    """
    pass


def calc_value_sincerity(row):
    """
    Функция для подсчета значения шкалы Ригидность
    :param row: строка с ответами
    :return: число
    """
    lst_pr = [1,6,10,12,15,19,21,26,33,38,44,49,52,58,61]

    value_forward = 0 # счетчик прямых ответов

    for idx, value in enumerate(row):
        if idx +1 in lst_pr:
            if value == 'нет':
                value_forward += 1

    return value_forward

def calc_level_sincerity(value):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """
    if 0 <= value <= 4:
        return '0-4'
    elif 5 <= value <= 7:
        return '5-7'
    elif 8 <= value <= 9:
        return '8-9'
    elif 10 <= value <= 12:
        return '10-12'
    else:
        return '13-15'



def calc_value_npu(row):
    """
    Функция для подсчета значения шкалы Ригидность
    :param row: строка с ответами
    :return: число
    """
    lst_plus = [2,3,5,7,9,11,13,14,16,18,20,22,23,25,27,28,29,31,
                32,34,36,37,39,40,42,43,45,47,48,51,53,54,
                56,57,59,60,62,63,65,66,67,68,69,70,71,72,73,
                74,75,76,77,78,79,80,81,82,83,84,85,86
                ]
    lst_minus = [4,8,17,24,30,35,41,46,50,55,64]

    value_forward = 0 # счетчик прямых ответов

    for idx, value in enumerate(row):
        if idx +1 in lst_plus:
            if value == 'да':
                value_forward += 1
        elif idx + 1 in lst_minus:
            if value == 'нет':
                value_forward += 1
        else:
            continue

    return value_forward


def calc_sten_npu(value):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """
    if 0 <= value <= 1:
        return 10
    elif 2 <= value <= 3:
        return 9
    elif 4 <= value <= 5:
        return 8
    elif 6 <= value <= 9:
        return 7
    elif 10 <= value <= 15:
        return 6
    elif 16 <= value <= 20:
        return 5
    elif 21 <= value <= 28:
        return 4
    elif 29 <= value <= 34:
        return 3
    elif 35 <= value <= 40:
        return 2
    else:
        return 1


def calc_level_npu(value):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """
    if 1 <= value <= 2:
        return 'неудовлетворительная'
    elif 3 <= value <= 5:
        return 'удовлетворительная'
    elif 6 <= value <= 8:
        return 'хорошая'
    else:
        return 'высокая'

def calc_forecast_npu(value):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """
    if value == 'неудовлетворительная':
        return 'неблагоприятный'
    else:
        return 'благоприятный'


def calc_mean(df:pd.DataFrame,lst_cat:list,val_cat):
    """
    Функция для создания сводных датафреймов

    :param df: датафрейм с данными
    :param lst_cat:список колонок по которым будет формироваться свод
    :param val_cat:значение по которому будет формиваться свод
    :return:датафрейм
    """
    calc_mean_df = pd.pivot_table(df, index=lst_cat,
                                       values=val_cat,
                                       aggfunc=round_mean)
    calc_mean_df.reset_index(inplace=True)
    calc_mean_df.rename(columns={val_cat:'Среднее значение'},inplace=True)
    return calc_mean_df




def create_result_forecast_two_rybnikov(base_df:pd.DataFrame, out_dct:dict, lst_svod_cols:list):
    """
    Функция для подсчета результата если указаны колонки по которым нужно провести свод
    :param df: датафрейм с результатами
    :param out_dct: словарь с уже подсчитанными базовыми данными
    :param lst_svod_cols: список сводных колонок
    :return: словарь
    """
    lst_level = ['неудовлетворительная','удовлетворительная','хорошая','высокая']
    lst_sten = ['1','2','3','4','5','6','7','8','9','10']
    lst_forecast = ['неблагоприятный', 'благоприятный']
    lst_sinc = ['0-4', '5-7', '8-9', '10-12', '13-15']


    lst_reindex_one_level_cols = lst_svod_cols.copy()
    lst_reindex_one_level_cols.extend(['неудовлетворительная','удовлетворительная','хорошая','высокая',
                               'Итого'])  # Основная шкала

    lst_reindex_one_sten_cols = lst_svod_cols.copy()
    lst_reindex_one_sten_cols.extend(['1','2','3','4','5','6','7','8','9','10',
                               'Итого'])  # Стены

    lst_reindex_one_forecast_cols = lst_svod_cols.copy()
    lst_reindex_one_forecast_cols.extend(['неблагоприятный', 'благоприятный',
                               'Итого'])  # Прогноз

    lst_reindex_one_sinc_cols = lst_svod_cols.copy()
    lst_reindex_one_sinc_cols.extend(['0-4', '5-7', '8-9', '10-12', '13-15',
                               'Итого'])  # Прогноз


    svod_count_one_level_df = calc_count_scale(base_df, lst_svod_cols,
                                                    'Значение_НПУ',
                                                    'Уровень_НПУ',
                                                    lst_reindex_one_level_cols,lst_level)

    sten_df = base_df.copy() # делаем копию чтобы стены корректно подсчитались
    sten_df['Стен_НПУ'] = sten_df['Стен_НПУ'].astype(str)

    svod_count_one_sten_df = calc_count_scale(sten_df, lst_svod_cols,
                                                    'Значение_НПУ',
                                                    'Стен_НПУ',
                                                    lst_reindex_one_sten_cols,lst_sten)

    svod_count_one_forecast_df = calc_count_scale(base_df, lst_svod_cols,
                                                    'Значение_НПУ',
                                                    'Прогноз_НПУ',
                                                    lst_reindex_one_forecast_cols,lst_forecast)

    svod_count_one_sinc_df = calc_count_scale(base_df, lst_svod_cols,
                                                    'Значение_НПУ',
                                                    'Диапазон_Искренность',
                                                    lst_reindex_one_sinc_cols,lst_sinc)

    # Считаем среднее
    svod_mean_df = calc_mean(base_df, lst_svod_cols, 'Значение_НПУ')
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

    out_dct.update({f'Уровень {out_name}': svod_count_one_level_df,
                    f'Стен {out_name}': svod_count_one_sten_df,
                    f'Прогноз {out_name}': svod_count_one_forecast_df,
                    f'Искр {out_name}': svod_count_one_sinc_df,
                    f'Ср. {out_name}': svod_mean_df})

    if len(lst_svod_cols) == 1:
        return out_dct

    else:
        for idx, name_column in enumerate(lst_svod_cols):
            lst_reindex_column_level_cols = [lst_svod_cols[idx],'неудовлетворительная', 'удовлетворительная', 'хорошая', 'высокая',
                                                  'Итого']

            lst_reindex_column_sten_cols = [lst_svod_cols[idx],'1', '2', '3', '4', '5', '6', '7', '8', '9', '10',
                                                 'Итого']

            lst_reindex_column_forecast_cols = [lst_svod_cols[idx],'неблагоприятный', 'благоприятный',
                                                     'Итого']

            lst_reindex_column_sinc_cols = [lst_svod_cols[idx],'0-4', '5-7', '8-9', '10-12', '13-15',
                                                 'Итого']

            svod_count_column_level_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                          'Значение_НПУ',
                                                          'Уровень_НПУ',
                                                          lst_reindex_column_level_cols, lst_level)

            sten_df = base_df.copy()  # делаем копию чтобы стены корректно подсчитались
            sten_df['Стен_НПУ'] = sten_df['Стен_НПУ'].astype(str)

            svod_count_column_sten_df = calc_count_scale(sten_df, lst_svod_cols[idx],
                                                         'Значение_НПУ',
                                                         'Стен_НПУ',
                                                         lst_reindex_column_sten_cols, lst_sten)

            svod_count_column_forecast_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                             'Значение_НПУ',
                                                             'Прогноз_НПУ',
                                                             lst_reindex_column_forecast_cols, lst_forecast)

            svod_count_column_sinc_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                         'Значение_НПУ',
                                                         'Диапазон_Искренность',
                                                         lst_reindex_column_sinc_cols, lst_sinc)

            # Считаем среднее
            svod_mean_column_df = calc_mean(base_df, [lst_svod_cols[idx]], 'Значение_НПУ')

            # Готовим наименование
            name_column = lst_svod_cols[idx]
            name_column = re.sub(r'[\[\]\'+()<> :"?*|\\/]', '_', name_column)
            name_column = name_column[:15]

            out_dct.update({f'Уровень {name_column}': svod_count_column_level_df,
                            f'Стен {name_column}': svod_count_column_sten_df,
                            f'Прогноз {name_column}': svod_count_column_forecast_df,
                            f'Искр {name_column}': svod_count_column_sinc_df,
                            f'Ср. {name_column}': svod_mean_column_df})
        return out_dct









def processing_forecast_two_rybnikov(result_df: pd.DataFrame, answers_df: pd.DataFrame, lst_svod_cols:list):
    """
    Функция для обработки
    :param result_df: часть датафрейма с описательными колонками
    :param answers_df: часть датафрейма с ответами
    :param lst_svod_cols:  список с колонками по которым нужно делать свод
    """
    try:
        out_answer_df = result_df.copy()  # делаем копию для последующего соединения с сырыми ответами
        if len(answers_df.columns) != 86:  # проверяем количество колонок с вопросами
            raise BadCountColumnsFTR

        # очищаем названия колонок от возможных сочетаний .1 которые добавляет пандас при одинаковых колонках
        clean_df_lst = []
        for name_column in answers_df.columns:
            clean_name = re.sub(r'.\d+$', '', name_column)
            clean_df_lst.append(clean_name)

        answers_df.columns = clean_df_lst

        lst_check_cols = ['Бывало, что я бросал начатое дело, так как боялся, что не справлюсь с ним',
                          'Меня легко переспорить',
                          'Я избегаю поправлять людей, которые высказывают необоснованные утверждения',
                          'Люди проявляют ко мне столько сочувствия и симпатии, сколько я заслуживаю',
                          'Иногда я бываю, уверен, что другие люди знают, о чем я думаю',
                          'Бывали случаи, что я не сдерживал своих обещаний',
                          'Временами я бываю совершенно уверен в своей никчемности',
                          'У меня никогда не было столкновений с законом',
                          'Я часто запоминаю числа, не имеющие для меня никакого значения (например, номера автомашин и т.п.)',
                          'Иногда я говорю неправду',
                          'Я впечатлительнее большинства других людей',
                          'Мне приятно иметь среди своих знакомых значительных людей, это как бы придает мне вес в собственных глазах',
                          'Определенно судьба не благосклонна ко мне',
                          'Мне часто говорят, что я вспыльчив',
                          'Бывало, что я говорил о вещах, в которых не разбираюсь',
                          'Я легко теряю терпение с людьми',
                          'У меня отсутствуют враги, которые по-настоящему хотели бы причинить мне зло',
                          'Иногда мой слух настолько обостряется, что это мне даже мешает',
                          'Бывает, что я откладываю на завтра то, что можно сделать сегодня',
                          'Если бы люди не были настроены против меня, я достиг бы в жизни гораздо большего',
                          'В игре я предпочитаю выигрывать',
                          'Часто я перехожу на другую сторону улицы, чтобы избежать встречи с человеком, которого я не желаю видеть',
                          'Большую часть времени у меня такое чувство, будто я сделал что-то не то или даже плохое',
                          'Если кто-нибудь говорит глупость или как-нибудь иначе проявляет свое невежество, я стараюсь разъяснить ему его ошибку',
                          'Иногда у меня бывает чувство, что передо мной нагромоздилось столько трудностей, что одолеть их просто невозможно',
                          'В гостях я держусь за столом лучше, чем дома',
                          'В моей семье есть очень нервные люди',
                          'Если в моих неудачах кто-то виноват, я не оставляю его безнаказанным',
                          'Должен признать, что временами я волнуюсь из-за пустяков',
                          'Когда мне предлагают начать дискуссию или высказать мнение по вопросу, в котором я хорошо разбираюсь, я делаю это без робости',
                          'Я часто подшучиваю над друзьями',
                          'В течение жизни у меня несколько раз менялось отношение к моей профессии',
                          'Бывало, что при обсуждении некоторых вопросов я, особенно не задумываясь, соглашался с мнением других',
                          'Я часто работал под руководством людей, которые умели повернуть дело так, что все достижения в работе приписывались им, а виноватыми в ошибках оказывались другие',
                          'Я безо всякого страха вхожу в комнату, где другие уже собрались и разговаривают',
                          'Мне кажется, что по отношению именно ко мне особенно часто поступают несправедливо',
                          'Когда я нахожусь на высоком месте, у меня появляется желание прыгнуть вниз',
                          'Среди моих знакомых есть люди, которые мне не нравятся',
                          'Мои планы часто казались мне настолько трудно выполнимыми, что я должен был отказаться от них',
                          'Я часто бываю рассеянным и забывчивым',
                          'Приступы плохого настроения у меня бывают редко',
                          'Я бы предпочел работать с женщинами',
                          'Счастливей всего я бываю, когда я один',
                          'Иногда, когда я неважно себя чувствую, я бываю раздражительным',
                          'Часто я вижу сны, о которых лучше никому не рассказывать',
                          'Мои убеждения и взгляды непоколебимы',
                          'Я человек нервный и легковозбудимый',
                          'Меня очень раздражает, когда я забываю, куда кладу вещи',
                          'Бывает, что я сержусь',
                          'Работа, требующая пристального внимания, мне нравится',
                          'Иногда я бываю так взволнован, что не могу усидеть на месте',
                          'Бывает, что неприличная или даже непристойная шутка вызывает у меня смех',
                          'Иногда мне в голову приходят такие нехорошие мысли, что лучше о них никому не рассказывать',
                          'Иногда я принимаю валериану, элениум или другие успокаивающие средства',
                          'Человек я подвижный',
                          'Теперь мне трудно надеяться на то, что я чего-нибудь добьюсь в жизни',
                          'Иногда я чувствую, что близок к нервному срыву',
                          'Бывало, что я отвечал на письма не сразу после прочтения',
                          'Раз в неделю или чаще я бываю возбужденным и взволнованным',
                          'Мне очень трудно приспособиться к новым условиям жизни, работы или учебы. Переход к новым условиям жизни, работы или учебы кажется мне невыносимо трудным',
                          'Иногда случалось так, что я опаздывал на работу или свидание',
                          'Голова у меня болит часто',
                          'Я вел неправильный образ жизни',
                          'Алкогольные напитки я употребляю в умеренных количествах (или не употребляю вовсе)',
                          'Я часто предаюсь грустным размышлениям',
                          'По сравнению с другими семьями в моей очень мало любви и тепла',
                          'У меня часто бывают подъемы и спады настроения',
                          'Когда я нахожусь среди людей, я слышу очень странные вещи',
                          'Я считаю, что меня очень часто наказывали незаслуженно',
                          'Мне страшно смотреть вниз с большой высоты',
                          'Бывало, что я целыми днями или даже неделями ничего не мог делать, потому что никак не мог заставить себя взяться за работу',
                          'Я ежедневно выпиваю необычно много воды',
                          'У меня бывали периоды, когда я что-то делал, а потом не знал, что именно я делал',
                          'Когда я пытаюсь что-то сделать, то часто замечаю, что у меня дрожат руки',
                          'Думаю, что я человек обреченный',
                          'У меня бывают периоды такого сильного беспокойства, что я даже не могу усидеть на месте',
                          'Временами мне кажется, что моя голова работает медленнее',
                          'Мне кажется, что я все чувствую более остро, чем другие',
                          'Иногда совершенно безо всякой причины у меня вдруг наступает период необычайной веселости',
                          'Некоторые вещи настолько меня волнуют, что мне даже говорить о них трудно',
                          'Иногда меня подводят нервы',
                          'Часто у меня бывает такое ощущение, будто все вокруг нереально',
                          'Когда я слышу об успехах близкого знакомого, я начинаю чувствовать, что я неудачник',
                          'Бывает, что мне в голову приходят плохие, часто даже ужасные слова, и я никак не могу от них отвязаться',
                          'Иногда я стараюсь держаться подальше от того или иного человека, чтобы не сделать или не сказать чего-нибудь такого, о чем потом пожалею',
                          'Часто, даже когда все складывается для меня хорошо, я чувствую, что мне все безразлично',
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
            raise BadOrderFTR

        valid_values = ['да','нет']
        # Проверяем, есть ли значения, отличающиеся от указанных в списке
        lst_error_answers = []  # список для хранения строк где найдены неправильные ответы

        for i in range(86):
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
            raise BadValueFTR

        base_df = pd.DataFrame()

        base_df['Значение_Искренность'] = answers_df.apply(calc_value_sincerity,axis=1)
        base_df['Диапазон_Искренность'] = base_df['Значение_Искренность'].apply(calc_level_sincerity)

        base_df['Значение_НПУ'] = answers_df.apply(calc_value_npu, axis=1)
        base_df['Стен_НПУ'] = base_df['Значение_НПУ'].apply(calc_sten_npu)
        base_df['Уровень_НПУ'] = base_df['Стен_НПУ'].apply(calc_level_npu)
        base_df['Прогноз_НПУ'] = base_df['Уровень_НПУ'].apply(calc_forecast_npu)

        # Создаем датафрейм для создания части в общий датафрейм
        part_df = pd.DataFrame()
        part_df['ОНПУ_ПД_Р_Искренность'] = base_df['Значение_Искренность']
        part_df['ОНПУ_ПД_Р_Значение'] = base_df['Значение_НПУ']
        part_df['ОНПУ_ПД_Р_Стен'] = base_df['Стен_НПУ']
        part_df['ОНПУ_ПД_Р_Уровень'] = base_df['Уровень_НПУ']
        part_df['ОНПУ_ПД_Р_Прогноз'] = base_df['Прогноз_НПУ']

        # Соединяем анкетную часть с результатной
        base_df = pd.concat([result_df, base_df], axis=1)

        base_df.sort_values(by='Значение_НПУ', ascending=False, inplace=True)  # сортируем
        out_answer_df = pd.concat([out_answer_df, answers_df], axis=1)  # Датафрейм для проверки

        # Общий свод по уровням шкалы искренности всего в процентном соотношении
        base_svod_sinc_df = pd.DataFrame(
            index=['0-4','5-7','8-9','10-12','13-15'])

        svod_level_sinc_df = pd.pivot_table(base_df, index='Диапазон_Искренность',
                                       values='Значение_Искренность',
                                       aggfunc='count')

        svod_level_sinc_df['% от общего'] = round(
            svod_level_sinc_df['Значение_Искренность'] / svod_level_sinc_df[
                'Значение_Искренность'].sum(), 3) * 100

        base_svod_sinc_df = base_svod_sinc_df.join(svod_level_sinc_df)

        # # Создаем суммирующую строку
        base_svod_sinc_df.loc['Итого'] = svod_level_sinc_df.sum()
        base_svod_sinc_df.reset_index(inplace=True)
        base_svod_sinc_df.rename(columns={'index': 'Уровень', 'Значение_Искренность': 'Количество'},
                                inplace=True)

        # Общий свод по уровням общей шкалы всего в процентном соотношении
        base_svod_all_df = pd.DataFrame(
            index=['неудовлетворительная','удовлетворительная','хорошая','высокая'])

        svod_level_df = pd.pivot_table(base_df, index='Уровень_НПУ',
                                       values='Значение_НПУ',
                                       aggfunc='count')

        svod_level_df['% от общего'] = round(
            svod_level_df['Значение_НПУ'] / svod_level_df[
                'Значение_НПУ'].sum(), 3) * 100

        base_svod_all_df = base_svod_all_df.join(svod_level_df)

        # # Создаем суммирующую строку
        base_svod_all_df.loc['Итого'] = svod_level_df.sum()
        base_svod_all_df.reset_index(inplace=True)
        base_svod_all_df.rename(columns={'index': 'Уровень', 'Значение_НПУ': 'Количество'},
                                inplace=True)

        # Общий свод по уровням стенов всего в процентном соотношении
        base_svod_sten_df = pd.DataFrame(
            index=[1,2,3,4,5,6,7,8,9,10])

        svod_level_sten_df = pd.pivot_table(base_df, index='Стен_НПУ',
                                       values='Значение_НПУ',
                                       aggfunc='count')

        svod_level_sten_df['% от общего'] = round(
            svod_level_sten_df['Значение_НПУ'] / svod_level_sten_df[
                'Значение_НПУ'].sum(), 3) * 100

        base_svod_sten_df = base_svod_sten_df.join(svod_level_sten_df)

        # # Создаем суммирующую строку
        base_svod_sten_df.loc['Итого'] = svod_level_sten_df.sum()
        base_svod_sten_df.reset_index(inplace=True)
        base_svod_sten_df.rename(columns={'index': 'Уровень', 'Значение_НПУ': 'Количество'},
                                inplace=True)

        # Общий свод по уровням прогнозов всего в процентном соотношении
        base_svod_forecast_df = pd.DataFrame(
            index=['неблагоприятный','благоприятный'])

        svod_level_forecast_df = pd.pivot_table(base_df, index='Прогноз_НПУ',
                                       values='Значение_НПУ',
                                       aggfunc='count')

        svod_level_forecast_df['% от общего'] = round(
            svod_level_forecast_df['Значение_НПУ'] / svod_level_forecast_df[
                'Значение_НПУ'].sum(), 3) * 100

        base_svod_forecast_df = base_svod_forecast_df.join(svod_level_forecast_df)

        # # Создаем суммирующую строку
        base_svod_forecast_df.loc['Итого'] = svod_level_forecast_df.sum()
        base_svod_forecast_df.reset_index(inplace=True)
        base_svod_forecast_df.rename(columns={'index': 'Уровень', 'Значение_НПУ': 'Количество'},
                                inplace=True)

        # формируем основной словарь
        out_dct = {'Списочный результат': base_df, 'Список для проверки': out_answer_df,
                   'Свод Искренность': base_svod_sinc_df,
                   'Свод НПУ': base_svod_all_df,
                   'Свод Стен': base_svod_sten_df,
                   'Свод Прогноз': base_svod_forecast_df,
                   }

        lst_level = ['неудовлетворительная','удовлетворительная','хорошая','высокая']
        dct_level = dict()

        for level in lst_level:
            temp_df = base_df[base_df['Уровень_НПУ'] == level]
            if temp_df.shape[0] != 0:
                dct_level[level] = temp_df

        out_dct.update(dct_level)

        lst_sinc = ['0-4','5-7','8-9','10-12','13-15']


        dct_prefix = {'Диапазон_Искренность': 'Искр',
                      }

        out_dct = create_list_on_level(base_df, out_dct, lst_sinc, dct_prefix)



        """
                        Сохраняем в зависимости от необходимости делать своды по определенным колонкам
                        """
        if len(lst_svod_cols) == 0:
            return out_dct, part_df

        else:
            out_dct = create_result_forecast_two_rybnikov(base_df, out_dct, lst_svod_cols)

            return out_dct, part_df
    except BadOrderFTR:
        messagebox.showerror('Лахеcис',
                             f'При обработке вопросов теста Методика оценки нервно-психической устойчивости «Прогноз-2» Рыбников обнаружены неправильные вопросы. Проверьте названия колонок с вопросами:\n'
                             f'{error_order_message[:5000]}\n'
                             f'Используйте при создании Яндекс-формы написание вопросов из руководства пользователя программы Лахесис.')
    except BadValueFTR:
        messagebox.showerror('Лахеcис',
                             f'При обработке вопросов теста Методика оценки нервно-психической устойчивости «Прогноз-2» Рыбников обнаружены неправильные варианты ответов. Проверьте ответы на указанных строках:\n'
                             f'{error_message[:5000]}\n'
                             f'Используйте при создании Яндекс-формы написание вариантов ответа из руководства пользователя программы Лахесис.')


    except BadCountColumnsFTR:
        messagebox.showerror('Лахеcис',
                             f'Проверьте количество колонок с ответами на тест Методика оценки нервно-психической устойчивости «Прогноз-2» Рыбников\n'
                             f'Должно быть 9 колонок с ответами')



























