"""
Скрипт для обработки результатов теста Опросник мотивации к достижению цели, к успеху Элерс Котик
"""

import pandas as pd
import re
from tkinter import messagebox
from lachesis_support_functions import calc_count_scale,round_mean

class BadOrderKMT(Exception):
    """
    Исключение для обработки случая когда колонки не совпадают
    """
    pass


class BadValueKMT(Exception):
    """
    Исключение для неправильных значений в вариантах ответов
    """
    pass

class BadCountColumnsKMT(Exception):
    """
    Исключение для обработки случая если количество колонок не равно 41
    """
    pass

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


def calc_motiv_value(row):
    """
    Фнукция подсчета значения мотивации к успеху
    :param row:
    :return:
    """
    key_lst = ['да','да',
               'да','да',
               'нет','да',
               'да','да',
               'да','да',
               'да','да',
               'да','нет',
               'нет','нет',
               'да','да',
               'нет','да',
               'да','да',
               'да','да',
               'да','нет',
               'да','нет',
               'да','нет',
               'нет','да',

               ]

    differences_count = sum(x == y for x, y in zip(list(row), key_lst)) # считаем количество отличий
    return differences_count


def calc_level_motiv(value:int):
    """
    Уровень мотивации к успеху
    :param value: значение
    :return:
    """
    if value <= 10:
        return 'низкий уровень мотивации к цели, успеху'
    elif 11<= value <=16:
        return 'средний уровень мотивации к цели,успеху'
    elif 17<= value <=20:
        return 'умеренно высокий уровень мотивации к цели,успеху'
    else:
        return 'слишком высокий уровень мотивации к цели,успеху'


def create_result_kmt(base_df:pd.DataFrame, out_dct:dict, lst_svod_cols:list):
    """
    Функция для подсчета результата если указаны колонки по которым нужно провести свод
    :param df: датафрейм с результатами
    :param out_dct: словарь с уже подсчитанными базовыми данными
    :param lst_svod_cols: список сводных колонок
    :return: словарь
    """
    lst_level = ['низкий уровень мотивации к цели, успеху','средний уровень мотивации к цели,успеху','умеренно высокий уровень мотивации к цели,успеху',
                 'слишком высокий уровень мотивации к цели,успеху']
    lst_reindex_main_level_cols = lst_svod_cols.copy()
    lst_reindex_main_level_cols.extend(['низкий уровень мотивации к цели, успеху','средний уровень мотивации к цели,успеху','умеренно высокий уровень мотивации к цели,успеху',
                 'слишком высокий уровень мотивации к цели,успеху',
                               'Итого'])  # Основная шкала

    svod_count_one_level_df = calc_count_scale(base_df, lst_svod_cols,
                                               'Значение_Мотивация',
                                               'Уровень_Мотивация',
                                               lst_reindex_main_level_cols, lst_level)

    # Считаем среднее
    svod_mean_df = calc_mean(base_df, lst_svod_cols, 'Значение_Мотивация')
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

    out_dct.update({f'Свод {out_name}': svod_count_one_level_df,
                    f'Ср. {out_name}': svod_mean_df})

    if len(lst_svod_cols) == 1:
        return out_dct
    else:
        for idx, name_column in enumerate(lst_svod_cols):
            lst_reindex_column_level_cols = [lst_svod_cols[idx],'низкий уровень мотивации к цели, успеху','средний уровень мотивации к цели,успеху','умеренно высокий уровень мотивации к цели,успеху',
                 'слишком высокий уровень мотивации к цели,успеху',
                               'Итого']

            svod_count_column_level_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                       'Значение_Мотивация',
                                                       'Уровень_Мотивация',
                                                       lst_reindex_column_level_cols, lst_level)

            # Считаем среднее
            svod_mean_column_df = calc_mean(base_df, [lst_svod_cols[idx]], 'Значение_Мотивация')
            # Готовим наименование
            name_column = lst_svod_cols[idx]
            name_column = re.sub(r'[\[\]\'+()<> :"?*|\\/]', '_', name_column)
            name_column = name_column[:15]
            out_dct.update({f'Свод {name_column}': svod_count_column_level_df,
                            f'Ср. {name_column}': svod_mean_column_df})

        return out_dct







def processing_kotik_motiv_target(result_df: pd.DataFrame, answers_df: pd.DataFrame,lst_svod_cols:list):
    """
    Функция для обработки
    :param base_df: часть датафрейма с описательными колонками
    :param answers_df: часть датафрейма с ответами
    :param lst_svod_cols:  список с колонками по которым нужно делать свод
    """
    try:
        out_answer_df = result_df.copy()  # делаем копию для последующего соединения с сырыми ответами
        if len(answers_df.columns) != 41:  # проверяем количество колонок с вопросами
            raise BadCountColumnsKMT

        lst_check_cols = ['Когда имеется выбор между двумя вариантами, его лучше сделать быстрее, чем отложить на определенное время',
                          'Я легко раздражаюсь, когда замечаю, что не могу на все 100% выполнить задание',
                          'Когда я работаю, это выглядит так, будто я все ставлю на карту',
                          'Когда возникает проблемная ситуация, я чаще всего принимаю решение одним из последних',
                          'Когда у меня два дня подряд нет дела, я теряю покой',
                          'В некоторые дни мои успехи ниже среднего',
                          'По отношению к себе я более строг, чем по отношению к другим',
                          'Я более доброжелателен, чем другие',
                          'Когда я отказываюсь от трудного задания, я потом сурово осуждаю себя, так как знаю, что в нем я добился бы успеха',
                          'В процессе работы я нуждаюсь в небольших паузах для отдыха',
                          'Усердие – это не основная моя черта',
                          'Мои достижения в труде не всегда одинаковы',
                          'Меня больше привлекает другая работа, чем та, которой я занят',
                          'Порицание стимулирует меня сильнее, чем похвала',
                          'Я знаю, что мои коллеги считают меня дельным человеком',
                          'Препятствия делают мои решения более твердыми',
                          'У меня легко вызвать честолюбие',
                          'Когда я работаю без вдохновения, это обычно заметно',
                          'При выполнении работы я не рассчитываю на помощь других',
                          'Иногда я откладываю то, что должен был сделать сейчас',
                          'Нужно полагаться только на самого себя',
                          'В жизни мало вещей, более важных, чем деньги',
                          'Всегда, когда мне предстоит выполнить важное задание, я ни о чем другом не думаю',
                          'Я менее честолюбив, чем многие другие',
                          'В конце отпуска я обычно радуюсь, что скоро выйду на работу',
                          'Когда я расположен к работе, я делаю лучше и квалифицированнее, чем другие',
                          'Мне проще и легче общаться с людьми, которые могут упорно работать',
                          'Когда у меня нет дел, я чувствую, что мне не по себе',
                          'Мне приходится выполнять ответственную работу чаще, чем другим',
                          'Когда мне приходится принимать решение, я стараюсь делать это как можно лучше',
                          'Мои друзья иногда считают меня ленивым',
                          'Мои успехи в какой-то мере зависят от моих коллег',
                          'Бессмысленно противодействовать воле руководителя',
                          'Иногда не знаешь, какую работу придется выполнять',
                          'Когда что-то не ладиться, я нетерпелив',
                          'Я обычно обращаю мало внимания на свои достижения',
                          'Когда я работаю вместе с другими, моя работа дает большие результаты, чем работы других',
                          'Многое, за что я берусь, я не довожу до конца',
                          'Я завидую людям, которые не загружены работой',
                          'Я не завидую тем, кто стремится к власти и положению',
                          'Когда я уверен, что стою на правильном пути, для доказательства своей правоты я иду вплоть до крайних мер',
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
            raise BadOrderKMT

        valid_values = ['да', 'нет']
        # Проверяем, есть ли значения, отличающиеся от указанных в списке
        lst_error_answers = []  # список для хранения строк где найдены неправильные ответы

        for i in range(41):
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
            raise BadValueKMT

        base_df = pd.DataFrame()
        # Основные шкалы
        lst_motiv = [2, 3, 4, 5, 6, 7, 8, 9, 10, 14, 15, 16, 17, 18, 19, 20, 21, 22, 24, 25, 26, 27, 28, 29, 30, 31, 32, 36, 37, 38, 39, 41]
        lst_motiv = list(map(lambda x: x - 1, lst_motiv))
        base_df['Значение_Мотивация'] =answers_df.take(lst_motiv,axis=1).apply(calc_motiv_value,axis=1)
        base_df['Уровень_Мотивация'] = base_df['Значение_Мотивация'].apply(calc_level_motiv)  # Уровень Мотивации
        # Создаем датафрейм для создания части в общий датафрейм
        part_df = pd.DataFrame()
        # Общая тревожность
        part_df['МДЦУ_Мотивация_цель_Значение'] = base_df['Значение_Мотивация']
        part_df['МДЦУ_Мотивация_цель_Уровень'] = base_df['Уровень_Мотивация']
        # Соединяем анкетную часть с результатной
        base_df = pd.concat([result_df, base_df], axis=1)

        out_answer_df = pd.concat([out_answer_df, answers_df], axis=1)  # Датафрейм для проверки

        base_df.sort_values(by='Значение_Мотивация', ascending=False, inplace=True)  # сортируем

        # Общий свод по уровням общей шкалы всего в процентном соотношении
        base_svod_all_df = pd.DataFrame(
            index=['низкий уровень мотивации к цели, успеху', 'средний уровень мотивации к цели,успеху',
                   'умеренно высокий уровень мотивации к цели,успеху','слишком высокий уровень мотивации к цели,успеху'])

        svod_level_df = pd.pivot_table(base_df, index='Уровень_Мотивация',
                                       values='Значение_Мотивация',
                                       aggfunc='count')

        svod_level_df['% от общего'] = round(
            svod_level_df['Значение_Мотивация'] / svod_level_df[
                'Значение_Мотивация'].sum(), 3) * 100

        base_svod_all_df = base_svod_all_df.join(svod_level_df)
        # # Создаем суммирующую строку
        base_svod_all_df.loc['Итого'] = svod_level_df.sum()
        base_svod_all_df.reset_index(inplace=True)
        base_svod_all_df.rename(columns={'index': 'Уровень', 'Значение_Мотивация': 'Количество'},
                                inplace=True)

        # формируем основной словарь
        out_dct = {'Списочный результат': base_df, 'Список для проверки': out_answer_df,
                   'Свод Общий': base_svod_all_df,
                   }

        lst_level = ['низкий уровень мотивации к цели, успеху', 'средний уровень мотивации к цели,успеху',
                   'умеренно высокий уровень мотивации к цели,успеху','слишком высокий уровень мотивации к цели,успеху']
        dct_level = dict()

        for level in lst_level:
            temp_df = base_df[base_df['Уровень_Мотивация'] == level]
            if temp_df.shape[0] != 0:
                if level == 'низкий уровень мотивации к цели, успеху':
                    level = 'низкий'
                elif level == 'средний уровень мотивации к цели,успеху':
                    level = 'средний'
                elif level == 'умеренно высокий уровень мотивации к цели,успеху':
                    level = 'умеренно высокий'
                else:
                    level = 'слишком высокий'

                dct_level[level] = temp_df

        out_dct.update(dct_level)

        """
                Сохраняем в зависимости от необходимости делать своды по определенным колонкам
                """
        if len(lst_svod_cols) == 0:
            return out_dct, part_df

        else:
            out_dct = create_result_kmt(base_df, out_dct, lst_svod_cols)

            return out_dct, part_df
    except BadOrderKMT:
        messagebox.showerror('Лахеcис',
                             f'При обработке вопросов теста Опросник мотивации к достижению цели, к успеху Элерс Котик обнаружены неправильные вопросы. Проверьте названия колонок с вопросами:\n'
                             f'{error_order_message}\n'
                             f'Используйте при создании Яндекс-формы написание вопросов из руководства пользователя программы Лахесис.')
    except BadValueKMT:
        messagebox.showerror('Лахеcис',
                             f'При обработке вопросов теста Опросник мотивации к достижению цели, к успеху Элерс Котик обнаружены неправильные варианты ответов. Проверьте ответы на указанных строках:\n'
                             f'{error_message}\n'
                             f'Используйте при создании Яндекс-формы написание вариантов ответа из руководства пользователя программы Лахесис.')


    except BadCountColumnsKMT:
        messagebox.showerror('Лахеcис',
                             f'Проверьте количество колонок с ответами на тест Опросник мотивации к достижению цели, к успеху Элерс Котик\n'
                             f'Должно быть 41 колонка с ответами')












