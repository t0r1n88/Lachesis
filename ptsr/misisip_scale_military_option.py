"""
Скрипт для обработки результатов теста Миссисипская шкала посттравматического стрессового расстройства (Mississippi Scale for PTSD, CMS) военный вариант
"""
import pandas as pd
import re
from tkinter import messagebox
from lachesis_support_functions import round_mean,calc_count_scale



class BadOrderMSMO(Exception):
    """
    Исключение для обработки случая когда колонки не совпадают
    """
    pass


class BadValueMSMO(Exception):
    """
    Исключение для неправильных значений в вариантах ответов
    """
    pass

class BadCountColumnsMSMO(Exception):
    """
    Исключение для обработки случая если количество колонок не равно 35
    """
    pass


def calc_value_ptsr(row):
    """
    Функция для подсчета значения субшкалы Эмоциональное истощение
    :param row: строка с ответами
    :return: число
    """

    value_forward = 0 # счетчик прямых ответов
    value_reverse = 0 # счетчик обратных ответов
    lst_forward = [1,3,4,5,7,8,9,10,12,13,14,15,16,18,20,21,23,25,26,28,29,31,32,33,35]  # список ответов которые нужно считать простым сложением
    lst_reverse = [2,6,11,17,19,22,24,27,30,34] # обратный подсчет

    for idx, value in enumerate(row):
        if idx + 1 in lst_forward:
            # print(f'Прямой подсчет {idx +1}') # Для проверки корректности
            value_forward += value
        elif idx +1 in lst_reverse:
            # print(f'Обратный подсчет {idx +1}')# Для проверки корректности
            if value == 5:
                value_reverse += 1
            elif value == 4:
                value_reverse += 2
            elif value == 3:
                value_reverse += 3
            elif value == 2:
                value_reverse += 4
            elif value == 1:
                value_reverse += 5

    return value_forward + value_reverse


def calc_level_ptsr(value):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """
    if 35 <= value <= 96:
        return 'хороший уровень адаптации'
    elif 97 <= value <= 111:
        return 'нарушение адаптации'
    else:
        return 'посттравматическое стрессовое расстройство'


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



def create_result_msmo(base_df:pd.DataFrame, out_dct:dict, lst_svod_cols:list):
    """
    Функция для подсчета результата если указаны колонки по которым нужно провести свод
    :param df: датафрейм с результатами
    :param out_dct: словарь с уже подсчитанными базовыми данными
    :param lst_svod_cols: список сводных колонок
    :return: словарь
    """
    lst_level = ['хороший уровень адаптации', 'нарушение адаптации','посттравматическое стрессовое расстройство']
    lst_reindex_main_level_cols = lst_svod_cols.copy()
    lst_reindex_main_level_cols.extend(['хороший уровень адаптации', 'нарушение адаптации',
               'посттравматическое стрессовое расстройство',
                               'Итого'])  # Основная шкала

    svod_count_one_level_df = calc_count_scale(base_df, lst_svod_cols,
                                                    'Значение_шкалы_ПТСР',
                                                    'Уровень_шкалы_ПТСР',
                                                    lst_reindex_main_level_cols,lst_level)

    # Считаем среднее
    svod_mean_df = calc_mean(base_df, lst_svod_cols, 'Значение_шкалы_ПТСР')
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
            lst_reindex_column_level_cols = [lst_svod_cols[idx],'хороший уровень адаптации', 'нарушение адаптации',
               'посттравматическое стрессовое расстройство',
                               'Итого']

            svod_count_column_level_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                       'Значение_шкалы_ПТСР',
                                                       'Уровень_шкалы_ПТСР',
                                                       lst_reindex_column_level_cols, lst_level)

            # Считаем среднее
            svod_mean_column_df = calc_mean(base_df, [lst_svod_cols[idx]], 'Значение_шкалы_ПТСР')
            # Готовим наименование
            name_column = lst_svod_cols[idx]
            name_column = re.sub(r'[\[\]\'+()<> :"?*|\\/]', '_', name_column)
            name_column = name_column[:15]
            out_dct.update({f'Свод {name_column}': svod_count_column_level_df,
                            f'Ср. {name_column}': svod_mean_column_df})

        return out_dct









def processing_misisip_scale_military_option(result_df: pd.DataFrame, answers_df: pd.DataFrame, lst_svod_cols:list):
    """
    Функция для обработки
    :param result_df: часть датафрейма с описательными колонками
    :param answers_df: часть датафрейма с ответами
    :param lst_svod_cols:  список с колонками по которым нужно делать свод
    """
    try:
        out_answer_df = result_df.copy()  # делаем копию для последующего соединения с сырыми ответами
        if len(answers_df.columns) != 35:  # проверяем количество колонок с вопросами
            raise BadCountColumnsMSMO

        # очищаем названия колонок от возможных сочетаний .1 которые добавляет пандас при одинаковых колонках
        clean_df_lst = []
        for name_column in answers_df.columns:
            clean_name = re.sub(r'.\d+$', '', name_column)
            clean_df_lst.append(clean_name)

        answers_df.columns = clean_df_lst

        lst_check_cols = ['До службы в армии у меня было больше друзей чем сейчас','У меня нет чувства вины за то, что я делал во время службы в армии',
                          'Если кто-то выведет меня из терпения, я скорее всего не сдержусь (применю физическую силу)','Если случается что-то, напоминающее мне о прошлом, это выводит меня из равновесия и причиняет мне боль',
                          'Люди, которые очень хорошо меня знают, меня боятся','Я способен вступать в эмоционально близкие отношения с другими людьми',
                          'Мне снятся по ночам кошмары о том, что было в действительности на войне','Когда я думаю о некоторых вещах, которые я делал в армии, мне просто не хочется жить',
                          'Внешне я выгляжу бесчувственным','Последнее время я чувствую, что хочу покончить с собой',
                          'Я хорошо засыпаю, нормально сплю и просыпаюсь только тогда, когда надо вставать','Я всё время задаю себе вопрос, почему я ещё жив, в то время как другие погибли на войне',
                          'В определённых ситуациях я чувствую себя так, как будто я снова в армии','Мои сны настолько реальны, что я просыпаюсь в холодном поту и заставляю себя больше не спать',
                          'Я чувствую, что больше не могу','Вещи, которые вызывают у других людей смех или слёзы, меня не трогают',
                          'Меня по-прежнему радуют те же вещи, что и раньше','Мои фантазии реалистичны и вызывают страх',
                          'Я обнаружил, что мне не трудно работать после демобилизации','Мне трудно сосредоточиться',
                          'Я беспричинно плачу','Мне нравится быть в обществе других людей',
                          'Меня пугают мои стремления и желания','Я легко засыпаю',
                          'От неожиданного шума я легко вздрагиваю','Никто, даже члены моей семьи, не понимают, что я чувствую',
                          'Я лёгкий, спокойный, уравновешенный человек','Я чувствую, что о каких-то вещах, которые я делал в армии, я не смогу рассказать кому-либо, потому что этого никому не понять',
                          'Временами я употребляю алкоголь или снотворное, чтобы помочь себе заснуть или забыть о тех вещах, которые случились со мной, когда я служил в армии','Я не испытываю дискомфорта, когда нахожусь в толпе',
                          'Я теряю самообладание и взрываюсь из-за мелочей','Я боюсь засыпать',
                          'Я пытаюсь избегать всего, что могло бы напомнить мне о том, что случилось со мной в армии','Моя память такая же хорошая, как и раньше',
                          'Я испытываю трудности в проявлении своих чувств, даже по отношению к близким людям']

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
            raise BadOrderMSMO

        # словарь для замены слов на числа
        dct_replace_value = {'совершенно неверно': 1,
                             'иногда неверно': 2,
                             'до некоторой степени верно': 3,
                             'верно': 4,
                             'совершенно верно': 5}


        valid_values = [1, 2, 3, 4, 5]
        answers_df.replace(dct_replace_value, inplace=True)  # заменяем слова на цифры для подсчетов
        # Проверяем, есть ли значения, отличающиеся от указанных в списке
        lst_error_answers = []  # список для хранения строк где найдены неправильные ответы

        for i in range(35):
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
            raise BadValueMSMO

        base_df = pd.DataFrame()

        # Субшкала Эмоциональное истощение
        base_df['Значение_шкалы_ПТСР'] = answers_df.apply(calc_value_ptsr, axis=1)
        base_df['Уровень_шкалы_ПТСР'] = base_df['Значение_шкалы_ПТСР'].apply(
            calc_level_ptsr)

        # Создаем датафрейм для создания части в общий датафрейм
        part_df = pd.DataFrame()
        part_df['МШ_ПТСР_В_Значение'] = base_df['Значение_шкалы_ПТСР']
        part_df['МШ_ПТСР_В_Уровень'] = base_df['Уровень_шкалы_ПТСР']

        # Соединяем анкетную часть с результатной
        base_df = pd.concat([result_df, base_df], axis=1)

        base_df.sort_values(by='Значение_шкалы_ПТСР', ascending=False, inplace=True)  # сортируем
        out_answer_df = pd.concat([out_answer_df, answers_df], axis=1)  # Датафрейм для проверки

        # Общий свод по уровням общей шкалы всего в процентном соотношении
        base_svod_all_df = pd.DataFrame(
            index=['хороший уровень адаптации', 'нарушение адаптации',
                   'посттравматическое стрессовое расстройство'])

        svod_level_df = pd.pivot_table(base_df, index='Уровень_шкалы_ПТСР',
                                       values='Значение_шкалы_ПТСР',
                                       aggfunc='count')

        svod_level_df['% от общего'] = round(
            svod_level_df['Значение_шкалы_ПТСР'] / svod_level_df[
                'Значение_шкалы_ПТСР'].sum(), 3) * 100

        base_svod_all_df = base_svod_all_df.join(svod_level_df)

        # # Создаем суммирующую строку
        base_svod_all_df.loc['Итого'] = svod_level_df.sum()
        base_svod_all_df.reset_index(inplace=True)
        base_svod_all_df.rename(columns={'index': 'Уровень', 'Значение_шкалы_ПТСР': 'Количество'},
                                inplace=True)
        # формируем основной словарь
        out_dct = {'Списочный результат': base_df, 'Список для проверки': out_answer_df,
                   'Свод Общий': base_svod_all_df,
                   }

        lst_level = ['хороший уровень адаптации', 'нарушение адаптации',
                   'посттравматическое стрессовое расстройство']
        dct_level = dict()

        for level in lst_level:
            temp_df = base_df[base_df['Уровень_шкалы_ПТСР'] == level]
            if temp_df.shape[0] != 0:
                if level == 'посттравматическое стрессовое расстройство':
                    level = 'ПТСР'
                dct_level[level] = temp_df

        out_dct.update(dct_level)

        """
                        Сохраняем в зависимости от необходимости делать своды по определенным колонкам
                        """
        if len(lst_svod_cols) == 0:
            return out_dct, part_df

        else:
            out_dct = create_result_msmo(base_df, out_dct, lst_svod_cols)

            return out_dct, part_df

    except BadOrderMSMO:
        messagebox.showerror('Лахеcис',
                             f'При обработке вопросов теста Миссисипская шкала ПТСР военный вариант обнаружены неправильные вопросы. Проверьте названия колонок с вопросами:\n'
                             f'{error_order_message}\n'
                             f'Используйте при создании Яндекс-формы написание вопросов из руководства пользователя программы Лахесис.')
    except BadValueMSMO:
        messagebox.showerror('Лахеcис',
                             f'При обработке вопросов теста Миссисипская шкала ПТСР военный вариант обнаружены неправильные варианты ответов. Проверьте ответы на указанных строках:\n'
                             f'{error_message}\n'
                             f'Используйте при создании Яндекс-формы написание вариантов ответа из руководства пользователя программы Лахесис.')


    except BadCountColumnsMSMO:
        messagebox.showerror('Лахеcис',
                             f'Проверьте количество колонок с ответами на тест Миссисипская шкала ПТСР военный вариант\n'
                             f'Должно быть 35 колонок с ответами')



















