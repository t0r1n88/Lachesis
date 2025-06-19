"""
Скрипт для обработки результатов теста Профессиональное выгорание методика Н. Е. Водопьяновой на основе модели К. Маслач и С. Джексон
"""
import pandas as pd
import re
from tkinter import messagebox
from lachesis_support_functions import round_mean




class BadOrderVODPB(Exception):
    """
    Исключение для обработки случая когда колонки не совпадают
    """
    pass


class BadValueVODPB(Exception):
    """
    Исключение для неправильных значений в вариантах ответов
    """
    pass

class BadCountColumnsVODPB(Exception):
    """
    Исключение для обработки случая если количество колонок не равно 22
    """
    pass


def calc_sub_value_em_attrition(row):
    """
    Функция для подсчета значения субшкалы Эмоциональное истощение
    :param row: строка с ответами
    :return: число
    """
    lst_pr = [1,2,3,6,8,13,14,16,20]

    value_forward = 0 # счетчик прямых ответов
    value_reverse = 0 # счетчик обратных ответов
    lst_forward = [1,2,3,8,13,14,16,20]  # список ответов которые нужно считать простым сложением
    lst_reverse = [6] # обратный подсчет

    for idx, value in enumerate(row):
        if idx +1 in lst_pr:
            if idx + 1 in lst_forward:
                # print(f'Прямой подсчет {idx +1}') # Для проверки корректности
                value_forward += value
            elif idx +1 in lst_reverse:
                # print(f'Обратный подсчет {idx +1}')# Для проверки корректности
                if value == 6:
                    value_reverse += 0
                elif value == 5:
                    value_reverse += 1
                elif value == 4:
                    value_reverse += 2
                elif value == 3:
                    value_reverse += 3
                elif value == 2:
                    value_reverse += 4
                elif value == 1:
                    value_reverse += 5
                elif value == 0:
                    value_reverse += 6

    return value_forward + value_reverse


def calc_level_sub_em_attrition(value):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """
    if 0 <= value <= 15:
        return 'низкий уровень'
    elif 16 <= value <= 24:
        return 'средний уровень'
    else:
        return 'высокий уровень'



def calc_sub_value_depers(row):
    """
    Функция для подсчета значения субшкалы Деперсонализация
    :param row: строка с ответами
    :return: число
    """
    lst_pr = [5,10,11,15,22]

    value_forward = 0 # счетчик прямых ответов

    for idx, value in enumerate(row):
        if idx +1 in lst_pr:
            value_forward += value

    return value_forward


def calc_level_sub_depers(value):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """
    if 0 <= value <= 5:
        return 'низкий уровень'
    elif 6 <= value <= 10:
        return 'средний уровень'
    else:
        return 'высокий уровень'



def calc_sub_value_reduc(row):
    """
    Функция для подсчета значения субшкалы Редукция персональных достижений
    :param row: строка с ответами
    :return: число
    """
    lst_pr = [4,7,9,12,17,18,19,21]

    value_forward = 0 # счетчик прямых ответов

    for idx, value in enumerate(row):
        if idx +1 in lst_pr:
            value_forward += value

    return value_forward


def calc_level_sub_reduc(value):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """
    if 37 <= value:
        return 'низкий уровень'
    elif 31 <= value <= 36:
        return 'средний уровень'
    else:
        return 'высокий уровень'


def calc_level_burnout(row:pd.Series):
    """
    Функция для подсчета уровня выгорания
    :param row: значения трех субшкал
    """
    lst_sub_value = row.tolist()
    em_level = lst_sub_value[0]
    depers_level = lst_sub_value[1]
    reduc_level = lst_sub_value[2]

    if em_level == 'высокий уровень' and depers_level == 'высокий уровень' and reduc_level == 'высокий уровень':
        return 'высокий уровень выгорания'
    else:
        if lst_sub_value.count('высокий уровень') == 2:
            return 'пограничное выгорание'
        else:
            return 'уровень выгорания в пределах нормы'





def calc_count_level_vpbp(df:pd.DataFrame, lst_cat:list, val_cat, col_cat, lst_cols:list):
    """
    Функция для создания сводных датафреймов

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
    count_df['% уровень выгорания в пределах нормы от общего'] = round(
        count_df['уровень выгорания в пределах нормы'] / count_df['Итого'], 2) * 100
    count_df['% пограничное выгорание от общего'] = round(
        count_df['пограничное выгорание'] / count_df['Итого'], 2) * 100
    count_df['% высокий уровень выгорания от общего'] = round(
        count_df['высокий уровень выгорания'] / count_df['Итого'], 2) * 100

    return count_df


def calc_count_level_sub_vpbp(df:pd.DataFrame, lst_cat:list, val_cat, col_cat, lst_cols:list):
    """
    Функция для создания сводных датафреймов по субшкалам

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
    count_df['% низкий уровень от общего'] = round(
        count_df['низкий уровень'] / count_df['Итого'], 2) * 100
    count_df['% средний уровень от общего'] = round(
        count_df['средний уровень'] / count_df['Итого'], 2) * 100
    count_df['% высокий уровень от общего'] = round(
        count_df['высокий уровень'] / count_df['Итого'], 2) * 100

    return count_df



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













def processing_vod_prof_burnout(base_df: pd.DataFrame, answers_df: pd.DataFrame,lst_svod_cols:list):
    """
    Функция для обработки
    :param base_df: часть датафрейма с описательными колонками
    :param answers_df: часть датафрейма с ответами
    :param lst_svod_cols:  список с колонками по которым нужно делать свод
    """
    try:
        out_answer_df = base_df.copy()  # делаем копию для последующего соединения с сырыми ответами
        if len(answers_df.columns) != 22:  # проверяем количество колонок с вопросами
            raise BadCountColumnsVODPB

        lst_check_cols = ['К концу рабочей недели я чувствую себя эмоционально опустошенным(ой).',
                          'К концу рабочего дня я чувствую себя как выжатый лимон.',
                          'Я чувствую себя усталым(ой), когда встаю утром и должен (должна) идти на работу.',
                          'Результаты моей работы не стоят тех усилий, которые я затрачиваю.',
                          'Меня раздражают люди, которые долго и много говорят о своих страхах.',
                          'Я чувствую себя энергичным(ой) и эмоционально воодушевленным(ой).',
                          'При разговоре с агрессивными учениками я умею находить нужные слова, снижающие их агрессию.',
                          'Я чувствую угнетенность и апатию.',
                          'Мне нравится успокаивать недоверчивых учеников и помогать им.',
                          'В последнее время я стал(а) более черствым(ой) (бесчувственным) по отношению к ученикам.',
                          'Ученики, с которыми мне приходится работать, не интересны для меня. Они скорее утомляют, чем радуют меня.',
                          'У меня много планов на будущее, и я верю в их осуществление.',
                          'У меня все больше жизненных разочарований.',
                          'Я чувствую равнодушие и потерю интереса ко многому, что радовало меня раньше.',
                          'Мне безразлично, что думают и чувствуют ученики. Я предпочитаю формальное, без лишних эмоций общение с ними.',
                          'Мне хочется уединиться и отдохнуть от всего и всех.',
                          'Я легко могу создать атмосферу доброжелательности и доверия на уроке.',
                          'Я разговариваю без напряжения с любым учеником или родителем (независимо от их амбиций, эмоционального состояния и культуры общения).',
                          'Я доволен (довольна) своими жизненными успехами (достижениями).',
                          'Я чувствую себя на пределе возможностей.',
                          'Я смогу еще много сделать в своей жизни.',
                          'Я проявляю к другим людям больше внимания и заботы, чем получаю от них в ответ признательности и благодарности.',
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
            raise BadOrderVODPB

        # словарь для замены слов на числа
        dct_replace_value = {'никогда': 0,
                             'очень редко': 1,
                             'редко': 2,
                             'иногда': 3,
                             'часто': 4,
                             'очень часто': 5,
                             'ежедневно': 6}

        valid_values = [0,1, 2, 3, 4, 5, 6]
        answers_df.replace(dct_replace_value, inplace=True)  # заменяем слова на цифры для подсчетов
        # Проверяем, есть ли значения, отличающиеся от указанных в списке
        lst_error_answers = []  # список для хранения строк где найдены неправильные ответы

        for i in range(22):
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
            raise BadValueVODPB

        # Субшкала Эмоциональное истощение
        base_df['Значение_субшкалы_Эмоциональное_истощение'] = answers_df.apply(calc_sub_value_em_attrition, axis=1)
        base_df['Норма_Эмоциональное_истощение'] = '0-24 балла'
        base_df['Уровень_субшкалы_Эмоциональное_истощение'] = base_df['Значение_субшкалы_Эмоциональное_истощение'].apply(calc_level_sub_em_attrition)

        # Субшкала Деперсонализация
        base_df['Значение_субшкалы_Деперсонализация'] = answers_df.apply(calc_sub_value_depers, axis=1)
        base_df['Норма_Деперсонализация'] = '0-10 баллов'
        base_df['Уровень_субшкалы_Деперсонализация'] = base_df['Значение_субшкалы_Деперсонализация'].apply(calc_level_sub_depers)

        # Субшкала Редукция персональных достижений
        base_df['Значение_субшкалы_Редукция_персональных_достижений'] = answers_df.apply(calc_sub_value_reduc, axis=1)
        base_df['Норма_Редукция_персональных_достижений'] = '31 и более баллов'
        base_df['Уровень_субшкалы_Редукция_персональных_достижений'] = base_df['Значение_субшкалы_Редукция_персональных_достижений'].apply(calc_level_sub_reduc)

        # Итоговая шкала
        base_df['Уровень_выгорания'] = base_df[['Уровень_субшкалы_Эмоциональное_истощение','Уровень_субшкалы_Деперсонализация','Уровень_субшкалы_Редукция_персональных_достижений']].apply(
            lambda x:calc_level_burnout(x),axis=1)

        # Создаем датафрейм для создания части в общий датафрейм
        part_df = pd.DataFrame()

        part_df['ПВПВ_Уровень_выгорания'] = base_df['Уровень_выгорания']

        part_df['ПВПВ_ЭИ_Значение'] = base_df['Значение_субшкалы_Эмоциональное_истощение']
        part_df['ПВПВ_ЭИ_Уровень'] = base_df['Уровень_субшкалы_Эмоциональное_истощение']

        part_df['ПВПВ_ДП_Значение'] = base_df['Значение_субшкалы_Деперсонализация']
        part_df['ПВПВ_ДП_Уровень'] = base_df['Уровень_субшкалы_Деперсонализация']

        part_df['ПВПВ_РПД_Значение'] = base_df['Значение_субшкалы_Редукция_персональных_достижений']
        part_df['ПВПВ_РПД_Уровень'] = base_df['Уровень_субшкалы_Редукция_персональных_достижений']

        base_df.sort_values(by='Значение_субшкалы_Эмоциональное_истощение', ascending=False, inplace=True)  # сортируем
        out_answer_df = pd.concat([out_answer_df, answers_df], axis=1)  # Датафрейм для проверки

        # Общий свод по уровням общей шкалы всего в процентном соотношении
        base_svod_all_df = pd.DataFrame(
            index=['уровень выгорания в пределах нормы', 'пограничное выгорание',
                   'высокий уровень выгорания'])

        svod_level_df = pd.pivot_table(base_df, index='Уровень_выгорания',
                                       values='Значение_субшкалы_Эмоциональное_истощение',
                                       aggfunc='count')

        svod_level_df['% от общего'] = round(
            svod_level_df['Значение_субшкалы_Эмоциональное_истощение'] / svod_level_df['Значение_субшкалы_Эмоциональное_истощение'].sum(), 3) * 100

        base_svod_all_df = base_svod_all_df.join(svod_level_df)

        # # Создаем суммирующую строку
        base_svod_all_df.loc['Итого'] = svod_level_df.sum()
        base_svod_all_df.reset_index(inplace=True)
        base_svod_all_df.rename(columns={'index': 'Уровень', 'Значение_субшкалы_Эмоциональное_истощение': 'Количество'}, inplace=True)
        # формируем основной словарь
        out_dct = {'Списочный результат': base_df, 'Список для проверки': out_answer_df,
                   'Свод Общий': base_svod_all_df,
                   }

        lst_level = ['уровень выгорания в пределах нормы', 'пограничное выгорание',
                   'высокий уровень выгорания']
        dct_level = dict()

        for level in lst_level:
            temp_df = base_df[base_df['Уровень_выгорания'] == level]
            if temp_df.shape[0] != 0:
                if level == 'уровень выгорания в пределах нормы':
                    level = 'нормальный уровень'
                dct_level[level] = temp_df

        out_dct.update(dct_level)

        # Свод по уровням субшкалы Эмоциональное истощение всего в процентном соотношении
        base_svod_em_df = pd.DataFrame(
            index=['низкий уровень', 'средний уровень',
                   'высокий уровень'])

        svod_level_em_df = pd.pivot_table(base_df, index='Уровень_субшкалы_Эмоциональное_истощение',
                                       values='Значение_субшкалы_Эмоциональное_истощение',
                                       aggfunc='count')

        svod_level_em_df['% от общего'] = round(
            svod_level_em_df['Значение_субшкалы_Эмоциональное_истощение'] / svod_level_em_df[
                'Значение_субшкалы_Эмоциональное_истощение'].sum(), 3) * 100

        base_svod_em_df = base_svod_em_df.join(svod_level_em_df)

        # # Создаем суммирующую строку
        base_svod_em_df.loc['Итого'] = svod_level_em_df.sum()
        base_svod_em_df.reset_index(inplace=True)
        base_svod_em_df.rename(columns={'index': 'Уровень', 'Значение_субшкалы_Эмоциональное_истощение': 'Количество'},
                                inplace=True)

        # Свод по уровням субшкалы Деперсонализация всего в процентном соотношении
        base_svod_depers_df = pd.DataFrame(
            index=['низкий уровень', 'средний уровень',
                   'высокий уровень'])

        svod_level_depers_df = pd.pivot_table(base_df, index='Уровень_субшкалы_Деперсонализация',
                                       values='Значение_субшкалы_Эмоциональное_истощение',
                                       aggfunc='count')

        svod_level_depers_df['% от общего'] = round(
            svod_level_depers_df['Значение_субшкалы_Эмоциональное_истощение'] / svod_level_depers_df[
                'Значение_субшкалы_Эмоциональное_истощение'].sum(), 3) * 100

        base_svod_depers_df = base_svod_depers_df.join(svod_level_depers_df)

        # # Создаем суммирующую строку
        base_svod_depers_df.loc['Итого'] = svod_level_depers_df.sum()
        base_svod_depers_df.reset_index(inplace=True)
        base_svod_depers_df.rename(columns={'index': 'Уровень', 'Значение_субшкалы_Эмоциональное_истощение': 'Количество'},
                                inplace=True)

        # Свод по уровням субшкалы Редукция_персональных_достижений всего в процентном соотношении
        base_svod_reduc_df = pd.DataFrame(
            index=['низкий уровень', 'средний уровень',
                   'высокий уровень'])

        svod_level_reduc_df = pd.pivot_table(base_df, index='Уровень_субшкалы_Редукция_персональных_достижений',
                                       values='Значение_субшкалы_Эмоциональное_истощение',
                                       aggfunc='count')

        svod_level_reduc_df['% от общего'] = round(
            svod_level_reduc_df['Значение_субшкалы_Эмоциональное_истощение'] / svod_level_reduc_df[
                'Значение_субшкалы_Эмоциональное_истощение'].sum(), 3) * 100

        base_svod_reduc_df = base_svod_reduc_df.join(svod_level_reduc_df)

        # # Создаем суммирующую строку
        base_svod_reduc_df.loc['Итого'] = svod_level_reduc_df.sum()
        base_svod_reduc_df.reset_index(inplace=True)
        base_svod_reduc_df.rename(columns={'index': 'Уровень', 'Значение_субшкалы_Эмоциональное_истощение': 'Количество'},
                                inplace=True)

        # считаем среднее значение по субшкалам
        avg_em = round(base_df['Значение_субшкалы_Эмоциональное_истощение'].mean(),1)
        avg_depers = round(base_df['Значение_субшкалы_Деперсонализация'].mean(),1)
        avg_reduc = round(base_df['Значение_субшкалы_Редукция_персональных_достижений'].mean(),1)

        avg_dct = {'Среднее значение субшкалы Эмоциональное истощение':avg_em,
                   'Среднее значение субшкалы Деперсонализация': avg_depers,
                   'Среднее значение субшкалы Редукция персональных достижений': avg_reduc,
                   }

        avg_df = pd.DataFrame.from_dict(avg_dct, orient='index')
        avg_df = avg_df.reset_index()
        avg_df.columns = ['Показатель','Среднее значение']

        out_dct.update({'Свод ЭИ':base_svod_em_df,'Свод ДП':base_svod_depers_df,'Свод РПД':base_svod_reduc_df,
                        'Среднее по субшкалам':avg_df}
                       )

        """
            Сохраняем в зависимости от необходимости делать своды по определенным колонкам
            """
        if len(lst_svod_cols) == 0:
            return out_dct, part_df

        elif len(lst_svod_cols) == 1:
            lst_reindex_main_level_cols = [lst_svod_cols[0],'уровень выгорания в пределах нормы', 'пограничное выгорание',
                   'высокий уровень выгорания','Итого'] # Основная шкала

            lst_reindex_sub_level_cols = [lst_svod_cols[0],'низкий уровень', 'средний уровень',
                   'высокий уровень','Итого'] # Субшкалы

            # основная шкала
            svod_count_one_level_df = calc_count_level_vpbp(base_df, lst_svod_cols, 'Значение_субшкалы_Эмоциональное_истощение', 'Уровень_выгорания',
                                                            lst_reindex_main_level_cols)

            # Субшкалы
            svod_count_one_level_em_df = calc_count_level_sub_vpbp(base_df, lst_svod_cols, 'Значение_субшкалы_Эмоциональное_истощение', 'Уровень_субшкалы_Эмоциональное_истощение',
                                                            lst_reindex_sub_level_cols)

            svod_count_one_level_depers_df = calc_count_level_sub_vpbp(base_df, lst_svod_cols, 'Значение_субшкалы_Эмоциональное_истощение', 'Уровень_субшкалы_Деперсонализация',
                                                            lst_reindex_sub_level_cols)

            svod_count_one_level_reduc_df = calc_count_level_sub_vpbp(base_df, lst_svod_cols, 'Значение_субшкалы_Эмоциональное_истощение', 'Уровень_субшкалы_Редукция_персональных_достижений',
                                                            lst_reindex_sub_level_cols)


            # очищаем название колонки по которой делали свод
            name_one = lst_svod_cols[0]
            name_one = re.sub(r'[\[\]\'+()<> :"?*|\\/]', '_', name_one)
            name_one = name_one[:15]

            # Считаем среднее по субшкалам
            svod_mean_em_df = calc_mean(base_df, [lst_svod_cols[0]], 'Значение_субшкалы_Эмоциональное_истощение')
            svod_mean_depers_df = calc_mean(base_df, [lst_svod_cols[0]], 'Значение_субшкалы_Деперсонализация')
            svod_mean_reduc_df = calc_mean(base_df, [lst_svod_cols[0]], 'Значение_субшкалы_Редукция_персональных_достижений')




            out_dct.update({f'Свод {name_one}':svod_count_one_level_df,
                            f'Свод ЭИ {name_one}':svod_count_one_level_em_df,
                            f'Свод ДП {name_one}':svod_count_one_level_depers_df,
                            f'Свод РПД {name_one}':svod_count_one_level_reduc_df,
                            f'Ср. ЭИ {name_one}':svod_mean_em_df,
                            f'Ср. ДП {name_one}':svod_mean_depers_df,
                            f'Ср. РПД {name_one}':svod_mean_reduc_df,})



            return out_dct, part_df

        elif len(lst_svod_cols) == 2:
            lst_reindex_main_level_cols = [lst_svod_cols[0],lst_svod_cols[1], 'уровень выгорания в пределах нормы', 'пограничное выгорание',
                                           'высокий уровень выгорания', 'Итого']  # Основная шкала

            lst_reindex_sub_level_cols = [lst_svod_cols[0],lst_svod_cols[1], 'низкий уровень', 'средний уровень',
                                          'высокий уровень', 'Итого']  # Субшкалы

            # первая колонка
            lst_reindex_first_mail_level_cols = [lst_svod_cols[0],'уровень выгорания в пределах нормы', 'пограничное выгорание',
                   'высокий уровень выгорания','Итого'] # Основная шкала

            lst_reindex_first_sub_level_cols = [lst_svod_cols[0],'низкий уровень', 'средний уровень',
                   'высокий уровень','Итого'] # Субшкалы

            # вторая колонка
            lst_reindex_second_mail_level_cols = [lst_svod_cols[1],'уровень выгорания в пределах нормы', 'пограничное выгорание',
                   'высокий уровень выгорания','Итого'] # Основная шкала

            lst_reindex_second_sub_level_cols = [lst_svod_cols[1],'низкий уровень', 'средний уровень',
                   'высокий уровень','Итого'] # Субшкалы




            # основная шкала
            svod_count_two_level_df = calc_count_level_vpbp(base_df, lst_svod_cols,
                                                            'Значение_субшкалы_Эмоциональное_истощение',
                                                            'Уровень_выгорания',
                                                            lst_reindex_main_level_cols)

            # Субшкалы
            svod_count_two_level_em_df = calc_count_level_sub_vpbp(base_df, lst_svod_cols,
                                                                   'Значение_субшкалы_Эмоциональное_истощение',
                                                                   'Уровень_субшкалы_Эмоциональное_истощение',
                                                                   lst_reindex_sub_level_cols)

            svod_count_two_level_depers_df = calc_count_level_sub_vpbp(base_df, lst_svod_cols,
                                                                       'Значение_субшкалы_Эмоциональное_истощение',
                                                                       'Уровень_субшкалы_Деперсонализация',
                                                                       lst_reindex_sub_level_cols)

            svod_count_two_level_reduc_df = calc_count_level_sub_vpbp(base_df, lst_svod_cols,
                                                                      'Значение_субшкалы_Эмоциональное_истощение',
                                                                      'Уровень_субшкалы_Редукция_персональных_достижений',
                                                                      lst_reindex_sub_level_cols)


            # первая колонка
            # основная шкала
            svod_count_first_level_df = calc_count_level_vpbp(base_df, [lst_svod_cols[0]], 'Значение_субшкалы_Эмоциональное_истощение', 'Уровень_выгорания',
                                                            lst_reindex_first_mail_level_cols)

            # Субшкалы
            svod_count_first_level_em_df = calc_count_level_sub_vpbp(base_df, [lst_svod_cols[0]], 'Значение_субшкалы_Эмоциональное_истощение', 'Уровень_субшкалы_Эмоциональное_истощение',
                                                            lst_reindex_first_sub_level_cols)

            svod_count_first_level_depers_df = calc_count_level_sub_vpbp(base_df, [lst_svod_cols[0]], 'Значение_субшкалы_Эмоциональное_истощение', 'Уровень_субшкалы_Деперсонализация',
                                                            lst_reindex_first_sub_level_cols)

            svod_count_first_level_reduc_df = calc_count_level_sub_vpbp(base_df, [lst_svod_cols[0]], 'Значение_субшкалы_Эмоциональное_истощение', 'Уровень_субшкалы_Редукция_персональных_достижений',
                                                            lst_reindex_first_sub_level_cols)



            # Вторая колонка
            svod_count_second_level_df = calc_count_level_vpbp(base_df, [lst_svod_cols[1]], 'Значение_субшкалы_Эмоциональное_истощение', 'Уровень_выгорания',
                                                            lst_reindex_second_mail_level_cols)

            # Субшкалы
            svod_count_second_level_em_df = calc_count_level_sub_vpbp(base_df, [lst_svod_cols[1]], 'Значение_субшкалы_Эмоциональное_истощение', 'Уровень_субшкалы_Эмоциональное_истощение',
                                                            lst_reindex_second_sub_level_cols)

            svod_count_second_level_depers_df = calc_count_level_sub_vpbp(base_df, [lst_svod_cols[1]], 'Значение_субшкалы_Эмоциональное_истощение', 'Уровень_субшкалы_Деперсонализация',
                                                            lst_reindex_second_sub_level_cols)

            svod_count_second_level_reduc_df = calc_count_level_sub_vpbp(base_df, [lst_svod_cols[1]], 'Значение_субшкалы_Эмоциональное_истощение', 'Уровень_субшкалы_Редукция_персональных_достижений',
                                                            lst_reindex_second_sub_level_cols)


            # Считаем среднее по субшкалам
            svod_mean_em_df = calc_mean(base_df, lst_svod_cols, 'Значение_субшкалы_Эмоциональное_истощение')
            svod_mean_depers_df = calc_mean(base_df, lst_svod_cols, 'Значение_субшкалы_Деперсонализация')
            svod_mean_reduc_df = calc_mean(base_df, lst_svod_cols, 'Значение_субшкалы_Редукция_персональных_достижений')

            # Считаем среднее по субшкалам
            svod_mean_first_em_df = calc_mean(base_df, [lst_svod_cols[0]], 'Значение_субшкалы_Эмоциональное_истощение')
            svod_mean_first_depers_df = calc_mean(base_df, [lst_svod_cols[0]], 'Значение_субшкалы_Деперсонализация')
            svod_mean_first_reduc_df = calc_mean(base_df, [lst_svod_cols[0]], 'Значение_субшкалы_Редукция_персональных_достижений')

            svod_mean_second_em_df = calc_mean(base_df, [lst_svod_cols[1]], 'Значение_субшкалы_Эмоциональное_истощение')
            svod_mean_second_depers_df = calc_mean(base_df, [lst_svod_cols[1]], 'Значение_субшкалы_Деперсонализация')
            svod_mean_second_reduc_df = calc_mean(base_df, [lst_svod_cols[1]], 'Значение_субшкалы_Редукция_персональных_достижений')









            # очищаем название колонки по которой делали свод
            name_one = lst_svod_cols[0]
            name_one = re.sub(r'[\[\]\'+()<> :"?*|\\/]', '_', name_one)
            name_one = name_one[:15]

            name_two = lst_svod_cols[1]
            name_two = re.sub(r'[\[\]\'+()<> :"?*|\\/]', '_', name_two)
            name_two = name_two[:15]



            out_dct.update({f'Свод {name_one[:10]}_{name_two[:10]}': svod_count_two_level_df,
                            f'Свод ЭИ {name_one[:10]}_{name_two[:10]}': svod_count_two_level_em_df,
                            f'Свод ДП {name_one[:10]}_{name_two[:10]}': svod_count_two_level_depers_df,
                            f'Свод РПД {name_one[:10]}_{name_two[:10]}': svod_count_two_level_reduc_df,

                            f'Ср. ЭИ {name_one[:10]}_{name_two[:10]}':svod_mean_em_df,
                            f'Ср. ДП {name_one[:10]}_{name_two[:10]}':svod_mean_depers_df,
                            f'Ср. РПД {name_one[:10]}_{name_two[:10]}':svod_mean_reduc_df,


                            f'Свод {name_one}':svod_count_first_level_df,
                            f'Свод ЭИ {name_one}':svod_count_first_level_em_df,
                            f'Свод ДП {name_one}':svod_count_first_level_depers_df,
                            f'Свод РПД {name_one}':svod_count_first_level_reduc_df,

                            f'Ср. ЭИ {name_one}': svod_mean_first_em_df,
                            f'Ср. ДП {name_one}': svod_mean_first_depers_df,
                            f'Ср. РПД {name_one}': svod_mean_first_reduc_df,

                            f'Свод {name_two}': svod_count_second_level_df,
                            f'Свод ЭИ {name_two}': svod_count_second_level_em_df,
                            f'Свод ДП {name_two}': svod_count_second_level_depers_df,
                            f'Свод РПД {name_two}': svod_count_second_level_reduc_df,

                            f'Ср. ЭИ {name_two}': svod_mean_second_em_df,
                            f'Ср. ДП {name_two}': svod_mean_second_depers_df,
                            f'Ср. РПД {name_two}': svod_mean_second_reduc_df,

                            })

            return out_dct, part_df
    except BadOrderVODPB:
        messagebox.showerror('Лахеcис',
                             f'При обработке вопросов теста Профессиональное выгорание педагогов Водопьянова обнаружены неправильные вопросы. Проверьте названия колонок с вопросами:\n'
                             f'{error_order_message}\n'
                             f'Используйте при создании Яндекс-формы написание вопросов из руководства пользователя программы Лахесис.')
    except BadValueVODPB:
        messagebox.showerror('Лахеcис',
                             f'При обработке вопросов теста Профессиональное выгорание педагогов Водопьянова обнаружены неправильные варианты ответов. Проверьте ответы на указанных строках:\n'
                             f'{error_message}\n'
                             f'Используйте при создании Яндекс-формы написание вариантов ответа из руководства пользователя программы Лахесис.')


    except BadCountColumnsVODPB:
        messagebox.showerror('Лахеcис',
                             f'Проверьте количество колонок с ответами на тест Профессиональное выгорание педагогов Водопьянова\n'
                             f'Должно быть 22 колонки с ответами')








































