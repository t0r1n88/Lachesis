"""
Функция для обработки результатов социометрического исследования
"""
import pandas as pd
pd.options.mode.chained_assignment = None
import numpy as np
import time
import copy
import re
import warnings
warnings.filterwarnings('ignore', category=UserWarning, module='openpyxl')
warnings.simplefilter(action='ignore', category=DeprecationWarning)
warnings.simplefilter(action='ignore', category=UserWarning)
import itertools
import networkx as nx
import matplotlib.pyplot as plt
from scipy.spatial import distance
import os
from tkinter import messagebox
from collections import Counter


class NotReqColumn(Exception):
    """
    Исключение для обработки случая когда нет обязательной колонки ФИО
    """
    pass

class BadQuantNegCols(Exception):
    """
    Исключение для обработки случая когда указан номер колонки с негативным вопросом большем чем есть вопросов в файле
    """
    pass





def extract_answer_several_option(row:pd.Series):
    """
    Функция для извлечения ответов из колонок
    :param row:строка датафрейма с определенными колонками
    :return: строка значений разделенных точкой с запятой
    """
    temp_lst = row.tolist() # делаем список
    temp_lst = [value for value in temp_lst if pd.notna(value)] # отбрасываем незаполненное
    return ';'.join(temp_lst)


def calc_answers(row:pd.Series, dct:dict,miss_dct:dict,chosen_miss_dct:dict):
    """
    Функция для извлечения данных из строки формата Значение1;Значение2 в словарь
    :param row: колонка ФИО и колонка с ответами
    :param dct: словарь который нужно заполнить
    :param miss_dct: словарь для тех кто не тестировался
    :param chosen_miss_dct: словарь для учета тех кто выбрал отсутствующих
    :return: словарь
    """
    fio, value_str = row.tolist()
    if isinstance(value_str,str):
        lst_value = value_str.split(';')
        if lst_value != ['']:
            for value in lst_value:
                if value in dct.keys():
                    dct[fio][value] += 1
                else:
                    if fio not in chosen_miss_dct:
                        chosen_miss_dct[fio] = dict() # создаем словарь для данного ключа
                        chosen_miss_dct[fio][value] = 1
                    else:
                        chosen_miss_dct[fio][value] = 1

                    if value not in miss_dct:
                        miss_dct[value] = 1
                    else:
                        miss_dct[value] += 1

def calc_answers_not_yandex(row:pd.Series, dct:dict,miss_dct:dict,chosen_miss_dct:dict):
    """
    Функция для извлечения данных из строки формата Значение1,Значение2 в словарь
    :param row: колонка ФИО и колонка с ответами
    :param dct: словарь который нужно заполнить
    :param miss_dct: словарь для тех кто не тестировался
    :param chosen_miss_dct: словарь для учета тех кто выбрал отсутствующих
    :return: словарь
    """
    fio, value_str = row.tolist()
    if isinstance(value_str,str):
        lst_value = value_str.split(',')
        if lst_value != ['']:
            for value in lst_value:
                value = value.strip()
                if value in dct.keys():
                    dct[fio][value] += 1
                else:
                    if fio not in chosen_miss_dct:
                        chosen_miss_dct[fio] = dict() # создаем словарь для данного ключа
                        chosen_miss_dct[fio][value] = 1
                    else:
                        chosen_miss_dct[fio][value] = 1

                    if value not in miss_dct:
                        miss_dct[value] = 1
                    else:
                        miss_dct[value] += 1


def calc_itog(row:pd.Series):
    """
    Функция для подсчета итоговой суммы в колонке Итого
    :param row: строка
    :return: значение
    """
    lst_value = row.tolist() # превращаем в список
    return sum([value for value in lst_value if isinstance(value,int)])


def calc_quantity_change(row):
    """
    Функция для подсчета количества выборов
    :param row: строка вида Значение1;Значение2
    """
    fio, value = row

    if isinstance(value,str):
        lst_value = value.split(';')
        if lst_value != ['']:
            lst_value = [name for name in lst_value if name != fio]  # отбрасываем фио если человек выбрал себя
            return len(lst_value)
        else:
            return 0
    else:
        return 0

def calc_quantity_change_not_yandex(row):
    """
    Функция для подсчета количества выборов из неяндексовских форм
    :param row: строка ФИО, список значений разделенных запятыми
    """
    fio,value = row
    if isinstance(value,str):
        lst_value = value.split(',')
        if lst_value != ['']:
            lst_value = [name for name in lst_value if name != fio] # отбрасываем фио если человек выбрал себя
            return len(lst_value)
        else:
            return 0
    else:
        return 0


def check_negative_cols(quant_questions:int, negative_str:str):
    """
    Функция для проверки наличия колонок с негативными вопросами
    :param quant_questions: количество вопросов
    :param negative_str: строка с перечислением колонок или пустая
    :return: список или пустой список
    """
    result = re.findall(r'\d+', negative_str)
    out_lst = [] # список для хранения номеров колонок с негативными вопросами
    if result:
        for value in result:
            value_digit = int(value)
            if value_digit > quant_questions:
                raise BadQuantNegCols
            if value_digit == 0: # на случай если записан ноль
                out_lst.append(1)
            else:
                out_lst.append(value_digit-1)
        return out_lst
    else:
        return []


 # Функция для проверки и устранения перекрытий
def avoid_overlap(pos, min_distance=1.5):
    """
    Устраняет перекрытия узлов, отодвигая их друг от друга
    """
    nodes = list(pos.keys())
    n = len(nodes)
    new_pos = pos.copy()

    max_iterations = 100
    for iteration in range(max_iterations):
        overlap_found = False
        for i in range(n):
            for j in range(i + 1, n):
                node_i = nodes[i]
                node_j = nodes[j]
                dist = distance.euclidean(new_pos[node_i], new_pos[node_j])

                if dist < min_distance:
                    overlap_found = True
                    # Вычисляем вектор отталкивания
                    dx = new_pos[node_i][0] - new_pos[node_j][0]
                    dy = new_pos[node_i][1] - new_pos[node_j][1]

                    # Нормализуем и увеличиваем расстояние
                    if dist == 0:
                        dx, dy = 1, 1  # Случайное направление если узлы в одной точке
                    else:
                        dx, dy = dx / dist, dy / dist

                    # Сдвигаем узлы
                    shift = (min_distance - dist) / 2
                    new_pos[node_i] = (new_pos[node_i][0] + dx * shift,
                                       new_pos[node_i][1] + dy * shift)
                    new_pos[node_j] = (new_pos[node_j][0] - dx * shift,
                                       new_pos[node_j][1] - dy * shift)

        if not overlap_found:
            break

    return new_pos


# ВАРИАНТ 1: Spring layout с увеличенными расстояниями
def layout_spring_no_overlap(G):
    pos = nx.spring_layout(G, k=5, iterations=200, scale=10)
    pos = avoid_overlap(pos, min_distance=2.0)
    return pos

# ВАРИАНТ 2: Кластерное позиционирование с большими расстояниями
def layout_clustered_no_overlap(G):
    degrees = dict(G.degree())
    clusters = {}
    for node, degree in degrees.items():
        if degree not in clusters:
            clusters[degree] = []
        clusters[degree].append(node)

    pos = {}
    x_pos = 0
    for degree, nodes in sorted(clusters.items(), reverse=True):
        y_pos = 0
        for i, node in enumerate(nodes):
            pos[node] = (x_pos + i * 0.3, y_pos - i * 2.0)  # Увеличиваем расстояния
        x_pos += 4  # Увеличиваем расстояние между кластерами

    pos = avoid_overlap(pos, min_distance=1.8)
    return pos

# ВАРИАНТ 3: Shell layout (концентрические круги)
def layout_shell_no_overlap(G):
    degrees = dict(G.degree())
    sorted_nodes = sorted(degrees.items(), key=lambda x: x[1], reverse=True)

    # Разбиваем на 2 концентрических круга
    core_nodes = [node for node, deg in sorted_nodes if deg >= 2]
    peripheral_nodes = [node for node, deg in sorted_nodes if deg < 2]

    pos = {}

    # Ядро - внутренний круг
    if core_nodes:
        core_pos = nx.circular_layout(core_nodes, scale=3)
        pos.update(core_pos)

    # Периферия - внешний круг
    if peripheral_nodes:
        peripheral_pos = nx.circular_layout(peripheral_nodes, scale=6)
        pos.update(peripheral_pos)

    pos = avoid_overlap(pos, min_distance=2.0)
    return pos

# ВАРИАНТ 4: Grid layout (сетка)
def layout_grid_no_overlap(G):
    nodes = list(G.nodes())
    n = len(nodes)

    # Вычисляем размер сетки
    cols = int(np.ceil(np.sqrt(n)))
    rows = int(np.ceil(n / cols))

    pos = {}
    for i, node in enumerate(nodes):
        row = i // cols
        col = i % cols
        pos[node] = (col * 3, -row * 3)  # Увеличиваем шаг сетки

    return pos

# ВАРИАНТ 5: Kamada-Kawai layout (оптимизированный)
def layout_kamada_kawai_no_overlap(G):
    try:
        pos = nx.kamada_kawai_layout(G, scale=10)
        pos = avoid_overlap(pos, min_distance=2.0)
        return pos
    except:
        return layout_spring_no_overlap(G)

# ВАРИАНТ 6: Спиральное расположение
def layout_spiral_no_overlap(G):
    nodes = list(G.nodes())
    n = len(nodes)
    pos = {}

    for i, node in enumerate(nodes):
        # Спиральная формула
        theta = i * 2 * np.pi / (n * 0.8)  # Увеличиваем шаг
        r = 2 + theta * 0.5  # Радиус увеличивается
        x = r * np.cos(theta)
        y = r * np.sin(theta)
        pos[node] = (x, y)

    pos = avoid_overlap(pos, min_distance=2.0)
    return pos


# ВАРИАНТ 7: Центральность по степени с постепенным размещением (как описано в требовании)
def layout_centrality_no_overlap(G):
    """
       Располагает узлы по принципу центральности:
       1. Сначала в центр помещают тех, кто получил наибольшее число выборов
       2. Затем отображают их выборы и тех, кто их выбрал
       3. Постепенно переходят ко всем оставшимся узлам
       """
    # Вычисляем входящую степень (популярность) для каждого узла
    # Исключаем петли (самовыборы) из расчета популярности
    in_degrees = {}
    for node in G.nodes():
        # Считаем только входящие связи от других узлов (не от себя)
        incoming = list(G.predecessors(node))
        # Убираем самого себя, если есть петля
        if node in incoming:
            incoming.remove(node)
        in_degrees[node] = len(incoming)

    # Сортируем узлы по убыванию популярности
    sorted_nodes = sorted(in_degrees.items(), key=lambda x: x[1], reverse=True)


    # Создаем множество уже размещенных узлов
    placed_nodes = set()
    pos = {}

    # Параметры размещения
    center_radius = 1.0
    layer_distance = 3.0

    # Шаг 1: Размещаем самых популярных в центре
    max_in_degree = sorted_nodes[0][1] if sorted_nodes else 0

    # Берем узлы с максимальной или близкой к максимальной популярностью
    top_popular = []
    for node, deg in sorted_nodes:
        if deg >= max_in_degree * 0.8:  # Берем узлы с популярностью от 80% от максимума
            top_popular.append(node)
        if len(top_popular) >= 5:  # Ограничиваем количество центральных узлов
            break


    if top_popular:
        if len(top_popular) == 1:
            # Один самый популярный - в самый центр
            pos[top_popular[0]] = (0, 0)
            placed_nodes.add(top_popular[0])
        else:
            # Несколько популярных - размещаем по кругу в центре
            angles = np.linspace(0, 2 * np.pi, len(top_popular), endpoint=False)
            for i, node in enumerate(top_popular):
                angle = angles[i]
                x = center_radius * np.cos(angle) * 0.7  # Уменьшаем радиус для тесной группы
                y = center_radius * np.sin(angle) * 0.7
                pos[node] = (x, y)
                placed_nodes.add(node)

    # Шаг 2: Размещаем тех, кто выбрал центральных узлов и кого выбрали центральные
    current_radius = center_radius + layer_distance
    layer_nodes = []

    # Собираем все узлы, связанные с центральными (исключая петли)
    for center_node in top_popular:
        # Те, кого выбрал центральный узел (исходящие связи)
        for successor in G.successors(center_node):
            if successor != center_node:  # Исключаем петли
                if successor not in placed_nodes and successor not in layer_nodes:
                    layer_nodes.append(successor)

        # Те, кто выбрал центральный узел (входящие связи)
        for predecessor in G.predecessors(center_node):
            if predecessor != center_node:  # Исключаем петли
                if predecessor not in placed_nodes and predecessor not in layer_nodes:
                    layer_nodes.append(predecessor)

    # Удаляем дубликаты (если узел связан с несколькими центральными)
    layer_nodes = list(dict.fromkeys(layer_nodes))


    # Размещаем узлы первого слоя
    if layer_nodes:
        angles = np.linspace(0, 2 * np.pi, len(layer_nodes), endpoint=False)
        # Добавляем случайное смещение для лучшего распределения
        angle_offset = np.random.random() * 2 * np.pi

        for i, node in enumerate(layer_nodes):
            angle = angles[i] + angle_offset
            x = current_radius * np.cos(angle)
            y = current_radius * np.sin(angle)
            pos[node] = (x, y)
            placed_nodes.add(node)

    # Шаг 3: Размещаем остальные узлы по слоям
    remaining_nodes = [node for node in G.nodes() if node not in placed_nodes]

    # Сортируем оставшиеся узлы по степени центральности
    remaining_sorted = sorted([(node, in_degrees[node]) for node in remaining_nodes],
                              key=lambda x: x[1], reverse=True)


    if remaining_sorted:
        current_radius += layer_distance
        # Разбиваем на группы по степени популярности
        groups = []
        current_group = []
        current_deg = None

        for node, deg in remaining_sorted:
            if current_deg is None or abs(deg - current_deg) <= 1:
                current_group.append(node)
                current_deg = deg
            else:
                if current_group:
                    groups.append(current_group)
                current_group = [node]
                current_deg = deg

        if current_group:
            groups.append(current_group)

        # Размещаем группы по слоям
        for group in groups:
            if not group:
                continue

            angles = np.linspace(0, 2 * np.pi, len(group), endpoint=False)
            # Разное смещение для каждой группы
            angle_offset = np.random.random() * 2 * np.pi

            for i, node in enumerate(group):
                angle = angles[i] + angle_offset
                x = current_radius * np.cos(angle)
                y = current_radius * np.sin(angle)
                pos[node] = (x, y)
                placed_nodes.add(node)

            # Увеличиваем радиус для следующей группы
            current_radius += layer_distance * 0.7

    # Проверяем, что все узлы размещены
    if len(pos) < G.number_of_nodes():
        # Размещаем оставшиеся узлы случайным образом
        for node in G.nodes():
            if node not in pos:
                x = np.random.uniform(-current_radius, current_radius)
                y = np.random.uniform(-current_radius, current_radius)
                pos[node] = (x, y)

    # Применяем алгоритм устранения перекрытий с большим расстоянием
    pos = avoid_overlap(pos, min_distance=3.0)

    # Центрируем граф
    if pos:
        # Находим центр масс
        avg_x = sum(x for x, y in pos.values()) / len(pos)
        avg_y = sum(y for x, y in pos.values()) / len(pos)

        # Сдвигаем все точки так, чтобы центр масс был в (0, 0)
        for node in pos:
            x, y = pos[node]
            pos[node] = (x - avg_x, y - avg_y)

    return pos


def analyze_mutual_pairs(G):
    """
    Анализирует и возвращает информацию о взаимных парах
    """
    mutual_pairs = []
    nodes_in_mutual = set()

    for u in G.nodes():
        for v in G.nodes():
            if u != v and u not in nodes_in_mutual and v not in nodes_in_mutual:
                if G.has_edge(u, v) and G.has_edge(v, u):
                    mutual_pairs.append((u, v))
                    nodes_in_mutual.add(u)
                    nodes_in_mutual.add(v)

    # Группы (по 3 и более взаимосвязанных узлов)
    groups = []
    visited = set()

    for node in G.nodes():
        if node not in visited:
            # Ищем связанную компоненту
            component = set([node])
            stack = [node]

            while stack:
                current = stack.pop()
                for neighbor in G.neighbors(current):
                    if neighbor not in component and G.has_edge(neighbor, current):
                        component.add(neighbor)
                        stack.append(neighbor)

            if len(component) >= 3:
                groups.append(list(component))
                visited.update(component)

    return {
        'mutual_pairs': mutual_pairs,
        'mutual_groups': groups,
        'total_mutual_connections': len(mutual_pairs) * 2,
        'nodes_in_mutual_pairs': list(nodes_in_mutual)
    }


def analyze_all_groups(G):
    """
    Детальный анализ различных типов групп в социограмме

    Возвращает:
    - mutual_pairs: взаимные пары (A↔B)
    - cliques: полностью взаимосвязанные группы (каждый с каждым)
    - dense_groups: группы с плотными связями (>75% возможных связей)
    - star_centers: звездообразные структуры (один популярный в центре)
    - chains: цепочки взаимных выборов
    - isolates: изолированные узлы
    """

    # 1. ВЗАИМНЫЕ ПАРЫ (2 узла)
    mutual_pairs = []
    nodes_in_mutual = set()

    # Проходим по всем уникальным парам узлов
    nodes = list(G.nodes())
    for i in range(len(nodes)):
        for j in range(i + 1, len(nodes)):
            u = nodes[i]
            v = nodes[j]
            if u == v:
                continue  # Пропускаем петли

            # Проверяем взаимность
            if G.has_edge(u, v) and G.has_edge(v, u):
                # Сортируем для уникальности
                pair_tuple = tuple(sorted([u, v]))
                if pair_tuple not in nodes_in_mutual:
                    nodes_in_mutual.add(pair_tuple)
                    mutual_pairs.append((u, v))



    # 2. КЛИКИ (полностью взаимосвязанные группы)
    cliques = []

    # Конвертируем в неориентированный граф ТОЛЬКО с взаимными связями
    G_mutual_undirected = nx.Graph()
    for node in G.nodes():
        G_mutual_undirected.add_node(node)

    for u, v in G.edges():
        if G.has_edge(v, u):  # Только взаимные связи
            G_mutual_undirected.add_edge(u, v)

    # Находим все клики размера 3 и более
    if G_mutual_undirected.number_of_edges() > 0:
        # Используем алгоритм поиска клик
        for clique in nx.find_cliques(G_mutual_undirected):
            if len(clique) >= 3:
                # Проверяем, что это действительно клика (все связи взаимны)
                is_valid_clique = True
                for u, v in itertools.combinations(clique, 2):
                    if not (G.has_edge(u, v) and G.has_edge(v, u)):
                        is_valid_clique = False
                        break

                if is_valid_clique:
                    # Сортируем для единообразия
                    cliques.append(sorted(clique))

    # Убираем дубликаты (клики могут находиться несколько раз)
    unique_cliques = []
    for clique in cliques:
        clique_set = set(clique)
        if not any(clique_set == set(unique) for unique in unique_cliques):
            unique_cliques.append(clique)
    cliques = unique_cliques

    # 3. ПЛОТНЫЕ ГРУППЫ (dense_groups)
    dense_groups = []
    density_threshold = 0.75  # Минимальная плотность связей (75%)

    # Находим сильно связные компоненты в графе взаимных связей
    for component in nx.connected_components(G_mutual_undirected):
        component = list(component)
        if len(component) >= 3:
            # Создаем подграф для этого компонента
            subgraph = G_mutual_undirected.subgraph(component)

            # Вычисляем плотность (отношение реальных связей к максимально возможным)
            n = len(component)
            max_possible_edges = n * (n - 1) / 2
            actual_edges = subgraph.number_of_edges()
            density = actual_edges / max_possible_edges if max_possible_edges > 0 else 0

            if density >= density_threshold:
                # Дополнительно проверяем взаимность всех связей
                all_mutual = True
                for u, v in itertools.combinations(component, 2):
                    if subgraph.has_edge(u, v):
                        if not (G.has_edge(u, v) and G.has_edge(v, u)):
                            all_mutual = False
                            break

                if all_mutual:
                    dense_groups.append({
                        'nodes': sorted(component),
                        'density': round(density, 2),
                        'size': n,
                        'edges': actual_edges
                    })

    # 4. ЗВЕЗДООБРАЗНЫЕ СТРУКТУРЫ (star_centers)
    star_centers = []
    min_star_rays = 3  # Минимальное количество "лучей" звезды

    for node in G.nodes():
        # Находим всех, кого выбрал этот узел (исходящие)
        outgoing = set(G.successors(node))

        # Находим всех, кто выбрал этот узел (входящие)
        incoming = set(G.predecessors(node))

        # Взаимные связи с этим узлом
        mutual_with_node = outgoing.intersection(incoming)

        # Односторонние исходящие связи (узел выбрал, но ему не ответили)
        one_way_out = outgoing - incoming

        # Односторонние входящие связи (выбрали узел, но он не ответил)
        one_way_in = incoming - outgoing

        # Классифицируем тип звезды
        if len(mutual_with_node) >= min_star_rays-1:
            # Звезда с взаимными связями (популярный лидер)
            star_type = "Звезда с взаимными связями (2 и более взаимных связи)"
        elif len(one_way_in) >= min_star_rays:
            # Звезда, куда стекаются выборы (популярный, но не отвечает)
            star_type = "Звезда, которого выбирают (популярный, но не отвечает-выбран 3 и более раз)"
        elif len(one_way_out) >= min_star_rays:
            # Звезда, которая раздает выборы (активный, но непопулярный)
            star_type = "Звезда, которая раздает выборы (активный, но непопулярный - сделал 3 и более выборов)"
        else:
            continue

        star_centers.append({
            'center': node,
            'type': star_type,
            'mutual_connections': sorted(list(mutual_with_node)),
            'one_way_incoming': sorted(list(one_way_in)),
            'one_way_outgoing': sorted(list(one_way_out)),
            'total_connections': len(outgoing.union(incoming))
        })

    # 5. ЦЕПОЧКИ (chains) взаимных выборов
    chains = []

    # Находим все простые пути в графе взаимных связей длиной 3 и более
    G_mutual_directed = nx.DiGraph()
    for u, v in G.edges():
        if G.has_edge(v, u):  # Только взаимные связи
            G_mutual_directed.add_edge(u, v)
            G_mutual_directed.add_edge(v, u)

    visited_chains = set()

    for start_node in G_mutual_directed.nodes():
        # Ищем пути длиной от 3 до 5 узлов
        for end_node in G_mutual_directed.nodes():
            if start_node != end_node:
                try:
                    # Находим все простые пути между start и end
                    all_paths = list(nx.all_simple_paths(G_mutual_directed,
                                                         start_node, end_node,
                                                         cutoff=4))

                    for path in all_paths:
                        if len(path) >= 3:
                            # Создаем ключ для уникальности (сортируем)
                            path_key = tuple(sorted(path))
                            if path_key not in visited_chains:
                                # Проверяем, что это действительно цепочка взаимных выборов
                                is_valid_chain = True
                                for i in range(len(path) - 1):
                                    if not (G.has_edge(path[i], path[i + 1]) and
                                            G.has_edge(path[i + 1], path[i])):
                                        is_valid_chain = False
                                        break

                                if is_valid_chain:
                                    chains.append({
                                        'path': path,
                                        'length': len(path),
                                        'nodes': path
                                    })
                                    visited_chains.add(path_key)
                except:
                    continue

    # 6. ИЗОЛИРОВАННЫЕ УЗЛЫ (isolates)
    isolates = []

    for node in G.nodes():
        # Узел считается изолированным, если у него нет взаимных связей
        has_mutual = False
        for neighbor in G.neighbors(node):
            if G.has_edge(neighbor, node):
                has_mutual = True
                break

        if not has_mutual and G.degree(node) == 0:
            # Полная изоляция - нет никаких связей
            isolates.append({
                'node': node,
                'type': 'Полностью изолирован (никого не выбрал и никто не выбрал)',
                'outgoing': list(G.successors(node)),
                'incoming': list(G.predecessors(node))
            })
        elif not has_mutual:
            # Частичная изоляция - есть связи, но не взаимные
            isolates.append({
                'node': node,
                'type': 'Частичная изоляция - есть связи, но не взаимные',
                'outgoing': list(G.successors(node)),
                'incoming': list(G.predecessors(node))
            })

    # 7. СТАТИСТИКА ПО СВЯЗЯМ
    # ДОПОЛНИТЕЛЬНО: считаем петли отдельно
    loops = []
    for node in G.nodes():
        if G.has_edge(node, node):  # Петля
            loops.append(node)


    total_edges = G.number_of_edges()
    mutual_edges = sum(1 for u, v in G.edges() if G.has_edge(v, u)) - len(loops) # отнимаем количество петель
    one_way_edges = total_edges - mutual_edges

    # Собираем полную статистику
    return {
        'mutual_pairs': mutual_pairs,
        'cliques': cliques,
        'dense_groups': dense_groups,
        'star_centers': star_centers,
        'chains': chains,
        'isolates': isolates,
        'loops': loops,
        'statistics': {
            'total_nodes': G.number_of_nodes(),
            'total_edges': total_edges,
            'mutual_edges': mutual_edges,
            'one_way_edges': one_way_edges,
            'mutual_ratio': mutual_edges / total_edges if total_edges > 0 else 0,
            'avg_degree': round(total_edges / G.number_of_nodes(),2) ,
            'density': nx.density(G)
        }
    }

# Функция для сохранения детального отчета
def save_detailed_group_analysis(analysis, save_path):
    """
    Сохраняет детальный анализ групп в текстовый файл
    """
    with open(save_path, 'w', encoding='utf-8') as f:

        # Статистика
        stats = analysis['statistics']
        f.write("ОБЩАЯ СТАТИСТИКА:\n")
        f.write("-" * 40 + "\n")
        f.write(f"Всего узлов (ответивших): {stats['total_nodes']}\n")
        f.write(f"Всего связей (сделанных и полученных выборов): {stats['total_edges']}\n")
        f.write(f"Взаимных связей (выборов): {stats['mutual_edges']} ({stats['mutual_ratio']:.1%})\n")
        f.write(f"Односторонних связей (выборов): {stats['one_way_edges']}\n")
        f.write(f"Среднее количество входящих и исходящих связей (выборов): {stats['avg_degree']:.2f}\n")
        f.write(f"Плотность графа (доля связей (выборов) от максимально возможных в группе): {stats['density']:.4f}\n\n")

        # Взаимные пары
        f.write("ВЗАИМНЫЕ ПАРЫ (диады):\n")
        f.write("-" * 40 + "\n")
        if analysis['mutual_pairs']:
            for i, (u, v) in enumerate(analysis['mutual_pairs'], 1):
                f.write(f"{i}. {u} ↔ {v}\n")
        else:
            f.write("Нет взаимных пар\n")
        f.write(f"Всего: {len(analysis['mutual_pairs'])} пар\n\n")

        # Клики
        f.write("КЛИКИ (полностью взаимосвязанные группы - триады,тетрады и т.д.):\n")
        f.write("-" * 40 + "\n")
        if analysis['cliques']:
            for i, clique in enumerate(analysis['cliques'], 1):
                f.write(f"{i}. Размер {len(clique)}: {', '.join(clique)}\n")
        else:
            f.write("Нет клик размера ≥3\n")
        f.write(f"Всего: {len(analysis['cliques'])} клик\n\n")

        # # Плотные группы
        # f.write("ПЛОТНЫЕ ГРУППЫ (плотность ≥ 75%):\n")
        # f.write("-" * 40 + "\n")
        # if analysis['dense_groups']:
        #     for i, group in enumerate(analysis['dense_groups'], 1):
        #         f.write(f"{i}. Размер {group['size']}, Плотность {group['density']}: "
        #                 f"{', '.join(group['nodes'])}\n")
        # else:
        #     f.write("Нет плотных групп\n")
        # f.write(f"Всего: {len(analysis['dense_groups'])} групп\n\n")

        # Звездообразные структуры
        f.write("ЗВЕЗДООБРАЗНЫЕ СТРУКТУРЫ (≥3 связи):\n")
        f.write("-" * 40 + "\n")
        if analysis['star_centers']:
            for i, star in enumerate(analysis['star_centers'], 1):
                f.write(f"{i}. Центр: {star['center']} ({star['type']})\n")
                f.write(f"   Всего связей: {star['total_connections']}\n")
                if star['mutual_connections']:
                    f.write(f"   Взаимные: {', '.join(star['mutual_connections'])}\n")
                if star['one_way_incoming']:
                    f.write(f"   Входящие (не взаимные): {', '.join(star['one_way_incoming'])}\n")
                if star['one_way_outgoing']:
                    f.write(f"   Исходящие (не взаимные): {', '.join(star['one_way_outgoing'])}\n")
                f.write("\n")
        else:
            f.write("Нет звездообразных структур\n")
        f.write(f"Всего: {len(analysis['star_centers'])} структур\n\n")

        # # Цепочки
        # f.write("ЦЕПОЧКИ ВЗАИМНЫХ ВЫБОРОВ (длина ≥3):\n")
        # f.write("-" * 40 + "\n")
        # if analysis['chains']:
        #     for i, chain in enumerate(analysis['chains'], 1):
        #         f.write(f"{i}. Длина {chain['length']}: {' → '.join(chain['path'])}\n")
        # else:
        #     f.write("Нет цепочек\n")
        # f.write(f"Всего: {len(analysis['chains'])} цепочек\n\n")

        # Изолированные узлы
        f.write("ИЗОЛИРОВАННЫЕ УЗЛЫ (нет взаимных выборов):\n")
        f.write("-" * 40 + "\n")
        if analysis['isolates']:
            for i, isolate in enumerate(analysis['isolates'], 1):
                f.write(f"{i}. {isolate['node']} ({isolate['type']})\n")
                if isolate['outgoing']:
                    f.write(f"   Исходящие: {', '.join(isolate['outgoing'])}\n")
                if isolate['incoming']:
                    f.write(f"   Входящие: {', '.join(isolate['incoming'])}\n")
                f.write("\n")
        else:
            f.write("Нет изолированных узлов\n")
        f.write(f"Всего: {len(analysis['isolates'])} узлов\n")

        # Петли (случаи когда человек выбрал сам себя)
        # f.write("Петли (выбор самого себя):\n")
        # f.write("-" * 40 + "\n")
        # if analysis['loops']:
        #     for i, loop in enumerate(analysis['loops'], 1):
        #         f.write(f"{i}. {loop}")
        #         f.write("\n")
        # else:
        #     f.write("Нет петель (нет выборов самого себя)\n")
        # f.write(f"Всего: {len(analysis['loops'])} узлов\n")


def get_meaningful_metrics_with_names(G):
    """
    Расширенные метрики с идентификацией конкретных людей
    """
    metrics = {}

    # 1. ПОПУЛЯРНОСТЬ (входящие степени) - КТО популярен
    in_degrees = dict(G.in_degree())

    metrics['popularity'] = {
        'max_in_degree': max(in_degrees.values()),
        'max_in_degree_nodes': [node for node, deg in in_degrees.items()
                                if deg == max(in_degrees.values())],

        'min_in_degree': min(in_degrees.values()),
        'min_in_degree_nodes': [node for node, deg in in_degrees.items()
                                if deg == min(in_degrees.values())],

        'avg_in_degree': np.mean(list(in_degrees.values())),
        'std_in_degree': np.std(list(in_degrees.values())),

        # Топ-5 самых популярных
        'top_5_popular': sorted(in_degrees.items(), key=lambda x: x[1], reverse=True)[:5],
        # Весь список
        'list_popular':sorted(in_degrees.items(), key=lambda x: x[1], reverse=True)[:1000],

        # Распределение популярности
        'popularity_distribution': dict(Counter(in_degrees.values())),

        # Классификация по популярности
        'highly_popular': [(node, deg) for node, deg in in_degrees.items()
                           if deg > np.mean(list(in_degrees.values())) + np.std(list(in_degrees.values()))],
        'unpopular': [(node, deg) for node, deg in in_degrees.items()
                      if deg < np.mean(list(in_degrees.values())) - np.std(list(in_degrees.values()))]
    }

    # 2. АКТИВНОСТЬ (исходящие степени) - КТО активен
    out_degrees = dict(G.out_degree())

    metrics['activity'] = {
        'max_out_degree': max(out_degrees.values()),
        'max_out_degree_nodes': [node for node, deg in out_degrees.items()
                                 if deg == max(out_degrees.values())],

        'min_out_degree': min(out_degrees.values()),
        'min_out_degree_nodes': [node for node, deg in out_degrees.items()
                                 if deg == min(out_degrees.values())],

        'avg_out_degree': np.mean(list(out_degrees.values())),
        'std_out_degree': np.std(list(out_degrees.values())),

        # Топ-5 самых активных
        'top_5_active': sorted(out_degrees.items(), key=lambda x: x[1], reverse=True)[:5],
        # Общий список активных
        'list_active': sorted(out_degrees.items(), key=lambda x: x[1], reverse=True)[:1000],

        # Распределение активности
        'activity_distribution': dict(Counter(out_degrees.values())),

        # Классификация по активности
        'highly_active': [(node, deg) for node, deg in out_degrees.items()
                          if deg > np.mean(list(out_degrees.values())) + np.std(list(out_degrees.values()))],
        'passive': [(node, deg) for node, deg in out_degrees.items()
                    if deg < np.mean(list(out_degrees.values())) - np.std(list(out_degrees.values()))]
    }

    # 3. БАЛАНС (разница входящих-исходящих) - КТО в какой категории
    balance_data = []
    for node in G.nodes():
        in_deg = in_degrees[node]
        out_deg = out_degrees[node]
        diff = in_deg - out_deg
        balance_data.append({
            'node': node,
            'in_degree': in_deg,
            'out_degree': out_deg,
            'balance': diff
        })

    # Сортируем по балансу
    balance_data_sorted = sorted(balance_data, key=lambda x: x['balance'], reverse=True)

    metrics['balance'] = {
        # Количественные показатели
        'balanced_nodes_count': sum(1 for item in balance_data if item['balance'] == 0),
        'popular_nodes_count': sum(1 for item in balance_data if item['balance'] > 1),
        'active_nodes_count': sum(1 for item in balance_data if item['balance'] < -1),
        'slightly_popular_count': sum(1 for item in balance_data if 0 < item['balance'] <= 1),
        'slightly_active_count': sum(1 for item in balance_data if -1 <= item['balance'] < 0),

        # Конкретные люди в каждой категории
        'balanced_nodes': [(item['node'], item['in_degree'], item['out_degree'])
                           for item in balance_data if item['balance'] == 0],

        'popular_nodes': [(item['node'], item['in_degree'], item['out_degree'], item['balance'])
                          for item in balance_data if item['balance'] > 1],
        'popular_nodes_sorted': sorted([(item['node'], item['balance'])
                                        for item in balance_data if item['balance'] > 1],
                                       key=lambda x: x[1], reverse=True)[:10],  # Топ-10 популярных

        'active_nodes': [(item['node'], item['in_degree'], item['out_degree'], item['balance'])
                         for item in balance_data if item['balance'] < -1],
        'active_nodes_sorted': sorted([(item['node'], abs(item['balance']))
                                       for item in balance_data if item['balance'] < -1],
                                      key=lambda x: x[1], reverse=True)[:10],  # Топ-10 активных

        # Экстремальные случаи
        'most_popular': balance_data_sorted[0] if balance_data_sorted else None,  # Самый популярный
        'most_active': balance_data_sorted[-1] if balance_data_sorted else None,  # Самый активный
        'most_balanced': next((item for item in balance_data if item['balance'] == 0), None),

        # Статистика баланса
        'avg_balance': np.mean([item['balance'] for item in balance_data]),
        'std_balance': np.std([item['balance'] for item in balance_data]),
        'max_positive_balance': max(item['balance'] for item in balance_data),
        'max_negative_balance': min(item['balance'] for item in balance_data)
    }

    # 4. СОЦИОМЕТРИЧЕСКИЕ СТАТУСЫ
    metrics['sociometric_status'] = {
        # "Звезды" - высокие входящие и исходящие
        'stars': [(node, in_deg, out_deg) for node, in_deg, out_deg in
                  [(n, in_degrees[n], out_degrees[n]) for n in G.nodes()]
                  if in_deg > metrics['popularity']['avg_in_degree'] and
                  out_deg > metrics['activity']['avg_out_degree']],

        # "Лидеры" - высокие входящие, средние исходящие
        'leaders': [(node, in_deg, out_deg) for node, in_deg, out_deg in
                    [(n, in_degrees[n], out_degrees[n]) for n in G.nodes()]
                    if in_deg > metrics['popularity']['avg_in_degree'] + metrics['popularity']['std_in_degree'] and
                    abs(in_deg - out_deg) <= 2],

        # "Изолированные" - низкие входящие и исходящие
        'isolated': [(node, in_deg, out_deg) for node, in_deg, out_deg in
                     [(n, in_degrees[n], out_degrees[n]) for n in G.nodes()]
                     if in_deg < 2 and out_deg < 2],

        # "Связные" - средние показатели, но много взаимных связей
        'connectors': [(node, in_deg, out_deg) for node, in_deg, out_deg in
                       [(n, in_degrees[n], out_degrees[n]) for n in G.nodes()]
                       if abs(in_deg - out_deg) <= 1 and
                       in_deg >= metrics['popularity']['avg_in_degree']],

        # "Проблемные" - высокие исходящие, но низкие входящие
        'problematic': [(node, in_deg, out_deg) for node, in_deg, out_deg in
                        [(n, in_degrees[n], out_degrees[n]) for n in G.nodes()]
                        if out_deg > in_deg * 2 and out_deg > 3]
    }

    # 5. ВЗАИМНОСТЬ - кто во взаимных связях
    mutual_pairs = []
    mutual_nodes = set()

    for u in G.nodes():
        for v in G.nodes():
            if u != v and G.has_edge(u, v) and G.has_edge(v, u):
                pair = tuple(sorted([u, v]))
                if pair not in mutual_pairs:
                    mutual_pairs.append(pair)
                    mutual_nodes.add(u)
                    mutual_nodes.add(v)

    metrics['reciprocity'] = {
        'mutual_pairs_count': len(mutual_pairs),
        'mutual_pairs': mutual_pairs[:20],  # Первые 20 пар
        'nodes_in_mutual': list(mutual_nodes),
        'nodes_not_in_mutual': [node for node in G.nodes() if node not in mutual_nodes],

        # Список по с количеством взаимных связей
        'mutual_by_node': sorted(
            [(node, sum(1 for v in G.nodes()
                        if node != v and G.has_edge(node, v) and G.has_edge(v, node)))
             for node in G.nodes()],
            key=lambda x: x[1], reverse=True
        )
    }

    # 6. СВОДНАЯ ИНФОРМАЦИЯ
    metrics['summary'] = {
        'total_nodes': G.number_of_nodes(),
        'total_edges': G.number_of_edges(),
        'density': nx.density(G),

        'key_individuals': {
            'most_popular_person': metrics['balance']['most_popular']['node'] if metrics['balance'][
                'most_popular'] else None,
            'most_popular_score': metrics['balance']['most_popular']['balance'] if metrics['balance'][
                'most_popular'] else None,

            'most_active_person': metrics['balance']['most_active']['node'] if metrics['balance'][
                'most_active'] else None,
            'most_active_score': abs(metrics['balance']['most_active']['balance']) if metrics['balance'][
                'most_active'] else None,

            'central_person': metrics['popularity']['top_5_popular'][0][0] if metrics['popularity'][
                'top_5_popular'] else None,

            'isolated_persons': [node for node, in_deg, out_deg in metrics['sociometric_status']['isolated']]
        }
    }

    return metrics


def save_detailed_metrics_report(metrics, save_path, question_num=None, G=None):
    """
    Сохраняет детальный отчет с именами людей в файл
    """
    with open(save_path, 'a', encoding='utf-8') as f:
        # Вспомогательная функция для записи
        def write_line(text=""):
            f.write(text + "\n")

        write_line("=" * 70)
        write_line(f"Индивидуальные метрики - ВОПРОС {question_num}")
        write_line("=" * 70)

        # 1. САМЫЕ ВАЖНЫЕ ЛЮДИ
        write_line("\nКЛЮЧЕВЫЕ ФИГУРЫ КОЛЛЕКТИВА:")
        write_line("-" * 40)

        # if metrics['balance']['most_popular']:
        #     mp = metrics['balance']['most_popular']
        #     write_line(f"САМЫЙ ПОПУЛЯРНЫЙ: {mp['node']}")
        #     write_line(f"   • Получает выборов: {mp['in_degree']}")
        #     write_line(f"   • Делает выборов: {mp['out_degree']}")
        #     write_line(f"   • Баланс: +{mp['balance']} (намного больше получает, чем отдает)")
        #
        # if metrics['balance']['most_active']:
        #     ma = metrics['balance']['most_active']
        #     write_line(f"\nСАМЫЙ АКТИВНЫЙ: {ma['node']}")
        #     write_line(f"   • Получает выборов: {ma['in_degree']}")
        #     write_line(f"   • Делает выборов: {ma['out_degree']}")
        #     write_line(f"   • Баланс: {ma['balance']} (намного больше отдает, чем получает)")

        # 2. ТОП-5 ПОПУЛЯРНЫХ
        write_line("\nТОП-5 САМЫХ ПОПУЛЯРНЫХ:")
        write_line("-" * 40)
        for i, (node, degree) in enumerate(metrics['popularity']['top_5_popular'], 1):
            out_deg = dict(G.out_degree())[node] if G else 0
            balance = degree - out_deg
            balance_desc = "(сбалансирован)" if balance == 0 else f"(баланс: {balance:+d})"
            write_line(f"{i:2d}. {node:30} | Выборов получил: {degree:2d} {balance_desc}")

        # 3. ТОП-5 АКТИВНЫХ
        write_line("\n ТОП-5 САМЫХ АКТИВНЫХ:")
        write_line("-" * 40)
        for i, (node, degree) in enumerate(metrics['activity']['top_5_active'], 1):
            in_deg = dict(G.in_degree())[node] if G else 0
            balance = in_deg - degree
            balance_desc = "(сбалансирован)" if balance == 0 else f"(баланс: {balance:+d})"
            write_line(f"{i:2d}. {node:30} | Выборов сделал: {degree:2d} {balance_desc}")

        # 4. САМЫЕ НЕПОПУЛЯРНЫЕ
        if metrics['popularity']['min_in_degree_nodes']:
            write_line("\n САМЫЕ НЕПОПУЛЯРНЫЕ:")
            write_line("-" * 40)
            for node in metrics['popularity']['min_in_degree_nodes']:
                in_deg = metrics['popularity']['min_in_degree']
                out_deg = dict(G.out_degree())[node] if G else 0
                write_line(f"• {node:30} | Получил: {in_deg} выборов | Сделал: {out_deg} выборов")

        # 5. САМЫЕ ПАССИВНЫЕ
        if metrics['activity']['min_out_degree_nodes']:
            write_line("\n САМЫЕ ПАССИВНЫЕ:")
            write_line("-" * 40)
            for node in metrics['activity']['min_out_degree_nodes']:
                out_deg = metrics['activity']['min_out_degree']
                in_deg = dict(G.in_degree())[node] if G else 0
                write_line(f"• {node:30} | Сделал: {out_deg} выборов | Получил: {in_deg} выборов")

        # Общие списки по популярности и активности
        if metrics['popularity']['list_popular']:
            write_line("\n ОБЩИЙ СПИСОК ПОПУЛЯРНОСТИ:")
            write_line("-" * 40)
            for i, (node, degree) in enumerate(metrics['popularity']['list_popular'], 1):
                out_deg = dict(G.out_degree())[node] if G else 0
                balance = degree - out_deg
                balance_desc = "(сбалансирован)" if balance == 0 else f"(баланс: {balance:+d})"
                write_line(f"{i:2d}. {node:30} | Выборов получил: {degree:2d} {balance_desc}")

        if metrics['activity']['list_active']:
            write_line("\n ОБЩИЙ СПИСОК АКТИВНОСТИ:")
            write_line("-" * 40)
            for i, (node, degree) in enumerate(metrics['activity']['list_active'], 1):
                in_deg = dict(G.in_degree())[node] if G else 0
                balance = in_deg - degree
                balance_desc = "(сбалансирован)" if balance == 0 else f"(баланс: {balance:+d})"
                write_line(f"{i:2d}. {node:30} | Выборов сделал: {degree:2d} {balance_desc}")



        # # 6. ИЗОЛИРОВАННЫЕ (если есть)
        # if metrics['sociometric_status']['isolated']:
        #     write_line("\n ИЗОЛИРОВАННЫЕ УЧАСТНИКИ:")
        #     write_line("-" * 40)
        #     for node, in_deg, out_deg in metrics['sociometric_status']['isolated']:
        #         write_line(f"• {node:30} | Получил: {in_deg:2d} | Сделал: {out_deg:2d}")

        # 7. СТАТИСТИКА БАЛАНСА
        write_line("\n СТАТИСТИКА БАЛАНСА:")
        write_line("-" * 40)
        balance = metrics['balance']
        total = metrics['summary']['total_nodes']

        categories = [
            ("Сбалансированные", balance['balanced_nodes_count']),
            ("Популярные (+2 и более)", balance['popular_nodes_count']),
            ("Активные (-2 и более)", balance['active_nodes_count']),
            ("Слегка популярные (+1)", balance['slightly_popular_count']),
            ("Слегка активные (-1)", balance['slightly_active_count'])
        ]

        for name, count in categories:
            percentage = count / total * 100 if total > 0 else 0
            write_line(f"{name:25}: {count:3d} чел. ({percentage:5.1f}%)")

        # 8. ВЗАИМНЫЕ СВЯЗИ
        write_line(f"\n ВЗАИМНЫЕ СВЯЗИ:")
        write_line("-" * 40)
        recip = metrics['reciprocity']
        write_line(f"Всего взаимных пар: {recip['mutual_pairs_count']}")
        write_line(f"Участников во взаимных связях: {len(recip['nodes_in_mutual'])} из {total}")
        write_line(f"Без взаимных связей: {len(recip['nodes_not_in_mutual'])} из {total}")

        # # Показать несколько взаимных пар
        # if recip['mutual_pairs']:
        #     write_line("\nПримеры взаимных пар:")
        #     for i, (u, v) in enumerate(recip['mutual_pairs'][:10], 1):
        #         write_line(f"{i:2d}. {u:25} ↔ {v:25}")
            # if recip['mutual_pairs_count'] > 10:
            #     write_line(f"... и ещё {recip['mutual_pairs_count'] - 10} пар")

        # 9. ТОП УЧАСТНИКОВ ВО ВЗАИМНЫХ СВЯЗЯХ
        if recip['mutual_by_node']:
            write_line("\n ОБЩИЙ СПИСОК ПО ВЗАИМНЫМ СВЯЗЯМ:")
            write_line("-" * 40)
            for i, (node, count) in enumerate(recip['mutual_by_node'], 1):
                write_line(f"{i:2d}. {node:30} | {count:2d} взаимных связей")

        # 10. РАСПРЕДЕЛЕНИЕ ПОПУЛЯРНОСТИ
        write_line("\n РАСПРЕДЕЛЕНИЕ ПОПУЛЯРНОСТИ (получено выборов):")
        write_line("-" * 40)
        pop = metrics['popularity']
        write_line(f"Средняя популярность: {pop['avg_in_degree']:.2f} выборов на человека")
        write_line(f"Разброс (стандартное отклонение): {pop['std_in_degree']:.2f}")
        write_line(f"Максимум: {pop['max_in_degree']} выборов")
        write_line(f"Минимум: {pop['min_in_degree']} выборов")

        # 11. РАСПРЕДЕЛЕНИЕ АКТИВНОСТИ
        write_line("\n РАСПРЕДЕЛЕНИЕ АКТИВНОСТИ (сделано выборов):")
        write_line("-" * 40)
        act = metrics['activity']
        write_line(f"Средняя активность: {act['avg_out_degree']:.2f} выборов на человека")
        write_line(f"Разброс (стандартное отклонение): {act['std_out_degree']:.2f}")
        write_line(f"Максимум: {act['max_out_degree']} выборов")
        write_line(f"Минимум: {act['min_out_degree']} выборов")

        # # 12. ТИП КОЛЛЕКТИВА
        # write_line(f"\n ТИП КОЛЛЕКТИВА:")
        # write_line("-" * 40)
        #
        # avg_in = metrics['popularity']['avg_in_degree']
        # avg_out = metrics['activity']['avg_out_degree']
        # std_in = metrics['popularity']['std_in_degree']
        # std_out = metrics['activity']['std_out_degree']
        #
        # # Определение типа
        # if std_in < 2 and balance['balanced_nodes_count'] > total * 0.4:
        #     collective_type = "ДЕМОКРАТИЧЕСКИЙ"
        #     description = "равномерное распределение, много сбалансированных участников"
        # elif std_in > 3 and metrics['balance']['most_popular']['balance'] > 5:
        #     collective_type = "ИЕРАРХИЧЕСКИЙ"
        #     description = "явный лидер, сильные различия в популярности"
        # elif metrics['balance']['active_nodes_count'] > total * 0.3:
        #     collective_type = "КОММУНИКАТИВНЫЙ"
        #     description = "много активных участников, высокая социальная активность"
        # elif len(recip['nodes_in_mutual']) > total * 0.7:
        #     collective_type = "СПЛОЧЕННЫЙ"
        #     description = "много взаимных связей, высокая взаимность"
        # elif std_in < 1.5 and std_out < 1.5:
        #     collective_type = "ОДНОРОДНЫЙ"
        #     description = "мало различий между участниками"
        # else:
        #     collective_type = "СМЕШАННЫЙ ТИП"
        #     description = "разнообразная социальная структура"
        #
        # write_line(f"Тип: {collective_type}")
        # write_line(f"Описание: {description}")
        #
        # # 13. РЕКОМЕНДАЦИИ
        # write_line("\n РЕКОМЕНДАЦИИ ДЛЯ РУКОВОДИТЕЛЯ:")
        # write_line("-" * 40)
        #
        # recommendations = []
        #
        # # Анализ для рекомендаций
        # if metrics['balance']['popular_nodes_count'] > total * 0.3:
        #     recommendations.append("  Много популярных участников - возможна конкуренция за внимание")
        #     recommendations.append("   → Разделить роли и зоны ответственности")
        #
        # if metrics['balance']['active_nodes_count'] < 3:
        #     recommendations.append(" Мало активных инициаторов")
        #     recommendations.append("   → Проводить тренинги по коммуникации, поощрять инициативу")
        #
        # if len(recip['nodes_not_in_mutual']) > total * 0.4:
        #     recommendations.append(" Много участников без взаимных связей")
        #     recommendations.append("   → Организовать командные мероприятия, парную работу")
        #
        # if metrics['sociometric_status']['isolated']:
        #     isolated_names = ", ".join([node for node, _, _ in metrics['sociometric_status']['isolated'][:5]])
        #     recommendations.append(f" Вовлекать изолированных в общие проекты")
        #     recommendations.append(f"   → Особое внимание: {isolated_names}")
        #
        # if std_in > 3:
        #     recommendations.append("  Большой разброс в популярности")
        #     recommendations.append("   → Равномерно распределять внимание, избегать 'любимчиков'")
        #
        # if metrics['activity']['min_out_degree'] == 0:
        #     recommendations.append(" Есть участники, которые никого не выбрали")
        #     recommendations.append("   → Выяснить причины пассивности, индивидуальные беседы")
        #
        # if not recommendations:
        #     recommendations.append(" Коллектив сбалансированный, особых проблем не выявлено")
        #     recommendations.append("   → Поддерживать текущую атмосферу, продолжать командную работу")
        #
        # for rec in recommendations:
        #     write_line(rec)

        # write_line("-" * 40)
        #
        # hr_recommendations = []
        #
        # if metrics['balance']['most_popular']:
        #     mp = metrics['balance']['most_popular']
        #     hr_recommendations.append(f"• Неформальный лидер: {mp['node']}")
        #     hr_recommendations.append(f"  Использовать его влияние для внедрения изменений")
        #
        # if metrics['sociometric_status']['connectors']:
        #     connectors = metrics['sociometric_status']['connectors'][:3]
        #     conn_names = ", ".join([node for node, _, _ in connectors])
        #     hr_recommendations.append(f"• Потенциальные 'связные': {conn_names}")
        #     hr_recommendations.append(f"  Могут помочь в коммуникации между группами")
        #
        # if metrics['sociometric_status']['problematic']:
        #     problematic = metrics['sociometric_status']['problematic'][:3]
        #     prob_names = ", ".join([node for node, _, _ in problematic])
        #     hr_recommendations.append(f"• Требуют внимания: {prob_names}")
        #     hr_recommendations.append(f"  Много инициативы, но мало отклика - возможна фрустрация")
        #
        # if not hr_recommendations:
        #     hr_recommendations.append("• Особого внимания не требуется")
        #     hr_recommendations.append("  Социальная структура коллектива в норме")
        #
        # for hr_rec in hr_recommendations:
        #     write_line(hr_rec)

        # # 15. ИТОГИ
        # write_line("\n" + "=" * 70)
        # write_line("КРАТКИЕ ИТОГИ:")
        # write_line("=" * 70)

        # # Самые важные цифры
        # summary_points = [
        #     f"• Участников: {total}",
        #     f"• Всего выборов: {metrics['summary']['total_edges']}",
        #     f"• Взаимных связей: {recip['mutual_pairs_count'] * 2} ({metrics.get('statistics', {}).get('mutual_ratio', 0) * 100:.1f}%)",
        #     f"• Самый популярный: {metrics['balance']['most_popular']['node'] if metrics['balance']['most_popular'] else 'нет'}",
        #     f"• Самый активный: {metrics['balance']['most_active']['node'] if metrics['balance']['most_active'] else 'нет'}",
        #     f"• Тип коллектива: {collective_type}"
        # ]
        #
        # for point in summary_points:
        #     write_line(point)


# Функция для определения категорий узлов по популярности
def get_node_categories(G):
    """
    Определяет категории узлов по количеству полученных выборов:
    I - группа «лидеров» (звёзд), набравших максимальное число выборов.
    II - референтная группа (предпочитаемых), набравших выборов выше среднего.
    III - группа «пренебрегаемых», набравших выборов ниже среднего.
    IV - группа «оттесненных» (изолированных), набравших 1-2 выборов.
    V - группа «изолированных» (отверженные), не получивших ни одного выбора.
    """
    # Вычисляем входящие степени (популярность) без учета петель
    in_degrees = {}
    for node in G.nodes():
        incoming = list(G.predecessors(node))
        # Убираем самого себя, если есть петля
        if node in incoming:
            incoming.remove(node)
        in_degrees[node] = len(incoming)

    # Статистика для определения категорий
    degrees_list = list(in_degrees.values())
    max_degree = max(degrees_list) if degrees_list else 0
    avg_degree = np.mean(degrees_list) if degrees_list else 0

    # Определяем пороги для категорий
    categories = {
        'I': {'name': 'Лидеры (звезды)', 'color': 5, 'description': 'Максимальное число выборов'},
        'II': {'name': 'Предпочитаемые', 'color': 4, 'description': 'Выше среднего'},
        'III': {'name': 'Пренебрегаемые', 'color': 3, 'description': 'Ниже среднего'},
        'IV': {'name': 'Оттесненные', 'color': 2, 'description': '1-2 выбора'},
        'V': {'name': 'Изолированные', 'color': 1, 'description': '0 выборов'}
    }

    # Распределяем узлы по категориям
    node_categories = {}
    for node, degree in in_degrees.items():
        if degree == max_degree and max_degree > 0:
            category = 'I'
        elif degree > avg_degree and degree > 0:
            category = 'II'
        elif degree < avg_degree and degree > 2:
            category = 'III'
        elif 1 <= degree <= 2:
            category = 'IV'
        else:  # degree == 0
            category = 'V'
        node_categories[node] = category

    # Статистика по категориям
    category_stats = {}
    for cat_id, cat_info in categories.items():
        nodes_in_cat = [node for node, cat in node_categories.items() if cat == cat_id]
        category_stats[cat_id] = {
            'name': cat_info['name'],
            'color_value': cat_info['color'],
            'count': len(nodes_in_cat),
            'nodes': nodes_in_cat,
            'description': cat_info['description']
        }

    return node_categories, category_stats, in_degrees








def create_sociograms(lst_graphs:list,end_folder:str,dct_missing_person:dict,dct_chosen_missng:dict):
    """
    Функция для создания и сохранения социограмм
    :param lst_graphs:список из словарей для каждого вопроса с отношениями
    :param dct_missing_person: словарь для отметки количества выборов отсутствующих
    :param dct_chosen_missng: словарь для хранения кто выбрал отсутствующих
    :param end_folder:конечная папка
    """
    # Создаем сокращенные имена
    for idx,dct_graph in enumerate(lst_graphs,1):
        # Создаем папку
        finish_path = f'{end_folder}/Вопрос_{idx}'
        if not os.path.exists(finish_path):
            os.makedirs(finish_path)
        if len(dct_missing_person[str(idx)]) != 0: # сохраняем списки тех не тестировался но кого выбрали
            miss_df = pd.DataFrame.from_dict(dct_missing_person[str(idx)],orient='index',columns=['Количество выборов'])
            miss_df = miss_df.reset_index()
            miss_df.columns = ['ФИО','Количество выборов']
            miss_df.sort_values(by='ФИО',inplace=True)
            # Делаем файл с тем кто выбрал
            rows = []
            for key1, inner_dict in dct_chosen_missng[str(idx)].items():
                for key2, value in inner_dict.items():
                    rows.append({
                        'Кто выбрал': key1,
                        'Кого выбрали': key2,
                        'Для подсчета': value
                    })

            missing_stat_link_df = pd.DataFrame(rows)

            with pd.ExcelWriter(f'{finish_path}/Выборы отсутствующих Вопрос_{idx}.xlsx', engine='xlsxwriter') as writer:
                missing_stat_link_df.to_excel(writer,sheet_name='Выбравшие',index=False)
                miss_df.to_excel(writer,sheet_name='Количество',index=False)


        # Создаем сокращенные имена
        short_names = {}
        check_dupl_set = set() # для проверки совпадения
        for i, name in enumerate(dct_graph.keys()):
            parts = name.split()
            first_part = parts[0] # Фамилия
            if len(parts) == 1:
                short_names[name] = first_part
            elif len(parts) == 2:
                out_name = f'{first_part} {parts[1][:3]}.'
                if out_name not in check_dupl_set:
                    short_names[name] = out_name
                    check_dupl_set.add(out_name)
                else:
                    short_names[name] = f'{out_name}_{i}'
                    check_dupl_set.add(f'{out_name}_{i}')
            elif len(parts) == 3:
                out_name = f'{first_part} '
                for part in parts[1:]:
                    out_name += f'{part[0]}.'

                if out_name not in check_dupl_set:
                    short_names[name] = out_name
                    check_dupl_set.add(out_name)
                else:
                    out_name = f'{first_part} {parts[1][:3]}.{parts[2][0]}.'
                    if out_name not in check_dupl_set:
                        short_names[name] = out_name
                        check_dupl_set.add(out_name)
                    else:
                        short_names[name] = f'{out_name}_{i}'
                        check_dupl_set.add(f'{out_name}_{i}')
            else:
                out_name = f'{first_part} '
                for part in parts[1:]:
                    out_name += f'{part[0]}.'

                if out_name not in check_dupl_set:
                    short_names[name] = out_name
                    check_dupl_set.add(out_name)
                else:
                    short_names[name] = f'{out_name}_{i}'
                    check_dupl_set.add(f'{out_name}_{i}')

        # Создаем ориентированный граф
        G = nx.DiGraph()
        G.add_nodes_from(short_names.values())

        # Добавляем ребра
        all_choices = []
        for person_from, choices in dct_graph.items():
            for person_to, choice in choices.items():
                if choice == 1 and person_from != person_to:
                    from_short = short_names[person_from]
                    to_short = short_names[person_to]
                    all_choices.append((from_short, to_short))

        for choice in all_choices:
            from_node, to_node = choice
            reverse_choice = (to_node, from_node)
            if reverse_choice in all_choices:
                G.add_edge(from_node, to_node, weight=2)
            else:
                G.add_edge(from_node, to_node, weight=1)

        detailed_analysis = analyze_all_groups(G)

        # Получаем категории узлов
        node_categories, category_stats, in_degrees = get_node_categories(G)

        # Сохраняем отчет
        save_detailed_group_analysis(detailed_analysis, f'{finish_path}/Анализ_Вопрос_{idx}.txt')

        # Индивидуальные метрики
        # Получаем расширенные метрики
        detailed_metrics = get_meaningful_metrics_with_names(G)

        # Выводим отчет
        save_detailed_metrics_report(
            metrics=detailed_metrics,
            save_path=f'{finish_path}/Анализ_Вопрос_{idx}.txt',
            question_num=idx,
            G=G  # Передаем граф для дополнительных расчетов
        )


        # Создаем варианты позиционирования
        layout_options = {
            1: ("Пружинная раскладка", layout_spring_no_overlap),
            2: ("Кластерное расположение", layout_clustered_no_overlap),
            3: ("Концентрические круги", layout_shell_no_overlap),
            4: ("Сетка", layout_grid_no_overlap),
            5: ("Камада-Каваи", layout_kamada_kawai_no_overlap),
            6: ("Спиральное", layout_spiral_no_overlap),
            7: ("Центрированное", layout_centrality_no_overlap)
        }

        # Создаем все варианты отображения для вопроса
        for selected_option in layout_options.keys():
            layout_name, layout_func = layout_options[selected_option]
            pos = layout_func(G)

            # Создаем рисунок с увеличенным размером
            plt.figure(figsize=(16, 12))

            # Определяем стили для ребер
            edge_colors = []
            edge_widths = []
            for edge in G.edges():
                weight = G[edge[0]][edge[1]]['weight']
                if weight == 2:
                    edge_colors.append('green')
                    edge_widths.append(3.0)
                else:
                    edge_colors.append('blue')
                    edge_widths.append(1.5)

            # Получаем значения категорий для цветов
            node_category_values = [category_stats[node_categories[node]]['color_value'] for node in G.nodes()]

            # Размеры узлов также могут зависеть от категории
            node_sizes = []
            for node in G.nodes():
                category = node_categories[node]
                if category == 'I':
                    size = 1200  # Лидеры - самые большие
                elif category == 'II':
                    size = 1000  # Предпочитаемые - большие
                elif category == 'III':
                    size = 800  # Пренебрегаемые - средние
                elif category == 'IV':
                    size = 600  # Оттесненные - маленькие
                else:  # 'V'
                    size = 400  # Изолированные - самые маленькие
                node_sizes.append(size)

            # Создаем цветовую карту с 5 дискретными цветами
            cmap = plt.cm.get_cmap('RdYlBu', 5)  # 5 дискретных цветов

            # Рисуем узлы с обводкой для лучшей видимости
            nodes = nx.draw_networkx_nodes(
                G, pos,
                node_size=node_sizes,
                node_color=node_category_values,
                cmap=cmap,
                vmin=0.5,  # Минимальное значение для дискретных цветов
                vmax=5.5,  # Максимальное значение для дискретных цветов
                edgecolors='black',
                linewidths=3,
                alpha=0.9
            )

            # Рисуем подписи узлов с фоном для читаемости
            label_pos = {}
            for node, (x, y) in pos.items():
                label_pos[node] = (x, y - 0.3)  # Сдвигаем подписи немного вниз

            for node, (x, y) in label_pos.items():
                plt.text(x, y, node, fontsize=9, fontweight='bold',
                         ha='center', va='center',
                         bbox=dict(boxstyle="round,pad=0.3", facecolor='white',
                                   alpha=0.8, edgecolor='none'))

            # Рисуем ребра
            for i, (u, v) in enumerate(G.edges()):
                nx.draw_networkx_edges(
                    G, pos,
                    edgelist=[(u, v)],
                    edge_color=[edge_colors[i]],
                    width=[edge_widths[i]],
                    arrows=True,
                    arrowsize=25,
                    arrowstyle='->',
                    connectionstyle='arc3,rad=0.2',
                    alpha=0.8
                )

            # Создаем кастомную цветовую шкалу - ПРАВИЛЬНЫЙ СПОСОБ
            from matplotlib.colors import BoundaryNorm
            from matplotlib.cm import ScalarMappable

            # Границы для категорий
            bounds = [0.5, 1.5, 2.5, 3.5, 4.5, 5.5]

            # Названия категорий для легенды
            category_labels = [
                'V: Изолированные (0 выборов)',
                'IV: Оттесненные (1-2 выбора)',
                'III: Пренебрегаемые (ниже среднего)',
                'II: Предпочитаемые (выше среднего)',
                'I: Лидеры (максимум выборов)'
            ]

            # Создаем нормализацию для дискретных цветов
            norm = BoundaryNorm(bounds, cmap.N)

            # Создаем ScalarMappable для цветовой шкалы
            sm = ScalarMappable(cmap=cmap, norm=norm)
            sm.set_array([])  # Пустой массив, так как данные уже отрисованы

            # Добавляем цветовую шкалу с кастомными метками
            ax = plt.gca()  # Получаем текущие оси
            cbar = plt.colorbar(sm, ax=ax, shrink=0.8, pad=0.02)

            # Устанавливаем кастомные метки
            cbar.set_ticks([1, 2, 3, 4, 5])
            cbar.set_ticklabels(category_labels)
            cbar.ax.tick_params(labelsize=9)
            cbar.set_label('Категории популярности', fontsize=11, fontweight='bold')

            # Особое оформление для варианта с центральностью
            if selected_option == 7:
                # Добавляем пояснительную аннотацию
                plt.figtext(0.02, 0.02,
                            'Структура графа:\n• В центре - самые популярные\n• Первый круг - их выборы\n• Внешние круги - остальные',
                            fontsize=10, bbox=dict(boxstyle="round,pad=0.5", facecolor='lightyellow', alpha=0.8))

                plt.title(
                    f'Социограмма группы - {layout_name}\n(Сначала самые популярные, затем их связи, затем остальные)\n'
                    f'Зеленые стрелки: взаимные выборы | Синие стрелки: обычные выборы',
                    size=14, pad=20)

            else:
                plt.title(
                    f'Социограмма группы - {layout_name}\nЗеленые стрелки: взаимные выборы | Синие стрелки: обычные выборы',
                    size=14, pad=20)

            plt.axis('off')

            # Сохраняем с высоким качеством
            plt.savefig(f'{finish_path}/{layout_options[selected_option][0]}.png',dpi=300, bbox_inches='tight',
                        facecolor='white', edgecolor='none',
                        transparent=False)

            plt.close('all') # очищаем от старых графиков



            # Создаем список связей
            lst_stat_link = []

            for u, v in G.edges():
                weight = G[u][v].get('weight', 1)  # Безопасное получение веса
                if weight == 2:
                    lst_stat_link.append(['ВЗАИМНЫЙ',u,'↔',v])
                else:
                    lst_stat_link.append(['ОДНОСТОРОННИЙ',u,'→',v])

            stat_link_df = pd.DataFrame(data=lst_stat_link,columns=['Тип выбора ','Сделавший выбор','Направление','Выбранный'])

            stat_link_df.to_excel(f'{finish_path}/Список связей Вопрос_{idx}.xlsx',index=False)




def generate_result_sociometry(data_file:str,quantity_descr_cols:int,negative_questions:str,end_folder:str,checkbox_not_yandex:str):
    """
    Функция для генерации результатов социометрического исследования
    :param data_file: файл с данными из форм
    :param quantity_descr_cols: количество анкетных колонок
    :param negative_questions: строка с порядковыми номерам негативных вопросов
    :param end_folder: конечная папка
    :param checkbox_not_yandex: определяет структуру файла с ответами. Значения Yes No если Yes то ответы разделены
    запятыми и находятся в одной колонке вопроса. Если No то это яндекс форма где каждый ответ это отдельная колонка
    """
    try:
        t = time.localtime()
        current_time = time.strftime('%H_%M_%S', t)
        checked_dct = dict()  # словарь для хранения проверочных датафреймов по каждому вопросу
        matrix_dct = dict()  # словарь для хранения матриц датафреймов по каждому вопросу
        lst_value_dct = [] # список для хранения словарей по каждому вопросу
        dct_chosen_missing = dict() # словарь для хранения выборов не тестировавшихся
        dct_missing_person = dict() # словарь для хранения словарей с выборами тех кто не прошел тестирование


        base_df = pd.read_excel(data_file,dtype=str) # исходный датафрейм
        # Проверяем наличие колонки ФИО
        diff_req_cols = {'ФИО'}.difference(set(base_df.columns))
        if len(diff_req_cols) != 0:
            raise NotReqColumn

        base_df = base_df[base_df['ФИО'].notna()] # удаляем незаполенные строки в колонке ФИО
        # очищаем от лишних пробелов в начале и конце
        base_df = base_df.applymap(lambda x:x.strip() if isinstance(x,str) else x)
        # Создаем файл с дубликатами
        dupl_df = base_df[base_df['ФИО'].duplicated(keep=False)]  # получаем дубликаты
        dupl_df.insert(0, '№ строки дубликата ', list(map(lambda x: x + 2, list(dupl_df.index))))
        dupl_df.replace(np.nan, None, inplace=True)  # для того чтобы в пустых ячейках ничего не отображалось

        dupl_df.to_excel(f'{end_folder}/Дубликаты {current_time}.xlsx',index=False)


        base_df.drop_duplicates(subset='ФИО',inplace=True) # удаляем дубликаты
        base_df.sort_values(by='ФИО',inplace=True) # сортируем по алфавиту
        # Создаем шаблон социоматрицы
        template_matrix_df = pd.DataFrame(index=base_df['ФИО'].tolist(),columns=base_df['ФИО'].tolist())

        lst_fio = base_df['ФИО'].tolist() # делаем список ФИО


        # создаем словарь где вида {ФИО:{ФИО:0}}
        template_dct = {}
        for fio in base_df['ФИО'].tolist():
            template_dct[fio] = {key:0 for key in base_df['ФИО'].tolist()}

        result_dct = copy.deepcopy(template_dct) # словарь в котором будут слаживаться результаты по всем вопросам

        descr_df = base_df.iloc[:,:quantity_descr_cols] # датафрейм с анкетными данными в который будут записываться данные по всем вопросам
        df = base_df.iloc[:,quantity_descr_cols:] # датафрейм с ответами
        lst_questions = [] # список для хранения самих вопросов
        # Находим все уникальные вопросы и отсутсвующих в случае если используется яндекс форма
        for name_column in df.columns:
            lst_answer = name_column.split(' / ')
            question = lst_answer[0]  # Вопрос
            if question not in lst_questions:
                lst_questions.append(question)

        # проверяем и обрабатываем строку с колонками по которым нужно делать свод
        lst_negative_cols = check_negative_cols(len(lst_questions), negative_questions)
        lst_negative_cols.sort() # сортируем чтобы потом все шло по порядку

        ind_templ_dct = {f'Вопрос_{number}':0 for number in range(1,len(lst_questions)+1)}
        # В зависимости от того есть ли колонки с негативными ответами
        if len(lst_negative_cols) == 0:
            index_dct = {'Индекс групповой сплоченности':copy.deepcopy(ind_templ_dct),
                         'Индекс референтности группы':copy.deepcopy(ind_templ_dct)} # словарь для хранения групповых индексов
        elif len(lst_negative_cols) == len(lst_questions):
            index_dct = {'Индекс групповой конфликтности': copy.deepcopy(ind_templ_dct),
                         'Индекс референтности группы': copy.deepcopy(ind_templ_dct)
                         }  # словарь для хранения групповых индексов
        else:
            index_dct = {'Индекс групповой сплоченности':copy.deepcopy(ind_templ_dct),
                         'Индекс групповой конфликтности': copy.deepcopy(ind_templ_dct),
                         'Индекс референтности группы':copy.deepcopy(ind_templ_dct)} # словарь для хранения групповых индексов

        # Делаем список пропущ

        for idx, name_question in enumerate(lst_questions,1):
            if checkbox_not_yandex == 'No':
                lst_columns_question = [col for col in df.columns if name_question in col] # список для хранения всех подвопросов
                descr_df[f'Вопрос_{idx}'] = df[lst_columns_question].apply(extract_answer_several_option, axis=1)

                # Создаем датафрейм для обработки отдельного вопроса
                one_qustion_df = base_df.iloc[:,:quantity_descr_cols]
                one_qustion_df[f'Вопрос_{idx}'] = descr_df[f'Вопрос_{idx}']
                # Добавляем колонку с количеством выборов
                one_qustion_df['Количество_выборов'] = one_qustion_df[['ФИО',f'Вопрос_{idx}']].apply(calc_quantity_change,axis=1)
                checked_dct[idx] = one_qustion_df

                # считаем отдельную колонку
                one_dct = copy.deepcopy(template_dct)

                missing_dct = dict() # словарь для тех кто не
                chosen_missing_dct = dict() # словарь для отслеживания выборов не тестировавшихся

                one_qustion_df[['ФИО',f'Вопрос_{idx}']].apply(lambda x: calc_answers(x, one_dct,missing_dct,chosen_missing_dct), axis=1)
                lst_value_dct.append(one_dct) # добавляем в список
                dct_missing_person[f'{idx}'] = missing_dct
                dct_chosen_missing[f'{idx}'] = chosen_missing_dct
            else:
                # Обработка не яндексовских форм
                # Создаем датафрейм для обработки отдельного вопроса
                descr_df[f'Вопрос_{idx}'] = df[name_question] # присваиваем колонку
                one_qustion_df = base_df.iloc[:, :quantity_descr_cols]
                one_qustion_df[f'Вопрос_{idx}'] = descr_df[f'Вопрос_{idx}']
                # Добавляем колонку с количеством выборов
                one_qustion_df['Количество_выборов'] = one_qustion_df[['ФИО',f'Вопрос_{idx}']].apply(calc_quantity_change_not_yandex,axis=1)
                checked_dct[idx] = one_qustion_df

                # считаем отдельную колонку
                one_dct = copy.deepcopy(template_dct)
                missing_dct = dict()  # словарь для тех кто не тестировался
                chosen_missing_dct = dict() # словарь для отслеживания выборов не тестировавшихся

                one_qustion_df[['ФИО',f'Вопрос_{idx}']].apply(lambda x: calc_answers_not_yandex(x, one_dct,missing_dct,chosen_missing_dct), axis=1)
                lst_value_dct.append(one_dct) # добавляем в список
                dct_missing_person[f'{idx}'] = missing_dct
                dct_chosen_missing[f'{idx}'] = chosen_missing_dct


            # заполняем социоматрицу на отдельный вопрос
            one_matrix_df = template_matrix_df.copy()
            for key,value_dct in one_dct.items():
                for subkey,value in value_dct.items():
                    if key != subkey:
                        one_matrix_df.loc[key,subkey] = value

            # считаем взаимные выборы
            change_dct = {key:{} for key in one_dct.keys()}

            for fio,value_dct in one_dct.items():
                for subfio,value in value_dct.items():
                    if fio != subfio:
                        if one_dct[subfio][fio] == 1 and value_dct[subfio] == 1:
                            change_dct[fio][subfio] = 1
                            change_dct[subfio][fio] = 1

            change_row = [len(value) for key,value in change_dct.items()]
            # считаем количество выборов
            sum_row = one_matrix_df.sum()

            # Обрабатываем в зависимости от количества негативных вопросов
            if len(lst_negative_cols) == 0:
                one_matrix_df.loc['Получено выборов'] = sum_row
                one_matrix_df.loc['Получено взаимных выборов'] = change_row
                # Добавляем колонку с социометрическим индексом
                lst_soc_index = list(sum_row)
                lst_soc_index = list(map(lambda x:round(x/(len(base_df)-1),2),lst_soc_index))
                lst_soc_index.extend([None,None])
                one_matrix_df['Индекс социометрического статуса'] = lst_soc_index
                one_matrix_df['Индекс эмоциональной экспансивности'] = round(one_matrix_df[lst_fio].sum(axis=1) / (len(base_df) - 1),2)
                one_matrix_df['Коэффициент удовлетворенности'] = one_matrix_df[lst_fio].sum(axis=1)
                tmp_change_row = list(change_row) # делаем список для развертывания
                tmp_change_row.extend([None,None])
                one_matrix_df['DPf'] = tmp_change_row
                one_matrix_df['Коэффициент удовлетворенности'] = round(one_matrix_df['DPf'] / one_matrix_df['Коэффициент удовлетворенности'],2)
                one_matrix_df.drop(columns=['DPf'],inplace=True)

                one_matrix_df.loc['Получено выборов','Индекс эмоциональной экспансивности'] = None
                one_matrix_df.loc['Получено взаимных выборов','Индекс эмоциональной экспансивности'] = None
                one_matrix_df.loc['Получено взаимных выборов','Коэффициент удовлетворенности'] = None

            elif len(lst_negative_cols) == len(lst_questions):
                one_matrix_df.loc['Получено выборов'] = sum_row
                one_matrix_df.loc['Получено взаимных выборов'] = change_row

                # Добавляем колонку с социометрическим индексом
                lst_soc_index = list(sum_row)
                lst_soc_index = list(map(lambda x:round(x/(len(base_df)-1),2),lst_soc_index))
                lst_soc_index.extend([None,None])
                one_matrix_df['Индекс социометрического статуса'] = lst_soc_index
                one_matrix_df['Индекс эмоциональной экспансивности'] = round(one_matrix_df[lst_fio].sum(axis=1) / (len(base_df) - 1),2)
                one_matrix_df['Коэффициент удовлетворенности'] = one_matrix_df[lst_fio].sum(axis=1)
                tmp_change_row = list(change_row) # делаем список для развертывания
                tmp_change_row.extend([None,None])
                one_matrix_df['DPf'] = tmp_change_row
                one_matrix_df['Коэффициент удовлетворенности'] = round(one_matrix_df['DPf'] / one_matrix_df['Коэффициент удовлетворенности'],2)
                one_matrix_df.drop(columns=['DPf'],inplace=True)

                one_matrix_df.loc['Получено выборов','Индекс эмоциональной экспансивности'] = None
                one_matrix_df.loc['Получено взаимных выборов','Индекс эмоциональной экспансивности'] = None
                one_matrix_df.loc['Получено взаимных выборов','Коэффициент удовлетворенности'] = None
            else:
                one_matrix_df.loc['Получено выборов'] = sum_row
                one_matrix_df.loc['Получено взаимных выборов'] = change_row
                # Добавляем колонку с социометрическим индексом
                lst_soc_index = list(sum_row)
                lst_soc_index = list(map(lambda x:round(x/(len(base_df)-1),2),lst_soc_index))
                lst_soc_index.extend([None,None])
                one_matrix_df['Индекс социометрического статуса'] = lst_soc_index
                one_matrix_df['Индекс эмоциональной экспансивности'] = round(one_matrix_df[lst_fio].sum(axis=1) / (len(base_df) - 1),2)
                one_matrix_df['Коэффициент удовлетворенности'] = one_matrix_df[lst_fio].sum(axis=1)
                tmp_change_row = list(change_row) # делаем список для развертывания
                tmp_change_row.extend([None,None])
                one_matrix_df['DPf'] = tmp_change_row
                one_matrix_df['Коэффициент удовлетворенности'] = round(one_matrix_df['DPf'] / one_matrix_df['Коэффициент удовлетворенности'],2)
                one_matrix_df.drop(columns=['DPf'],inplace=True)

                one_matrix_df.loc['Получено выборов','Индекс эмоциональной экспансивности'] = None
                one_matrix_df.loc['Получено взаимных выборов','Индекс эмоциональной экспансивности'] = None
                one_matrix_df.loc['Получено взаимных выборов','Коэффициент удовлетворенности'] = None




            matrix_dct[idx] = one_matrix_df # добавляем в словарь для сохранения

            if len(lst_negative_cols) == 0:
                # Считаем индексы
                max_sum_mutual_change = (len(base_df)* (len(base_df)-1)) / 2 # максимально возможное число взаимных выборов
                cn_index = sum(change_row) / max_sum_mutual_change # Индекс групповой сплоченности
                index_dct['Индекс групповой сплоченности'][f'Вопрос_{idx}'] = round(cn_index,2)
                if sum(sum_row) !=0:
                    index_dct['Индекс референтности группы'][f'Вопрос_{idx}'] = round(sum(change_row) / sum(sum_row),2)
                else:
                    index_dct['Индекс референтности группы'][f'Вопрос_{idx}'] = 0
            elif len(lst_negative_cols) == len(lst_questions):
                # Считаем индексы
                max_sum_mutual_change = (len(base_df)* (len(base_df)-1)) / 2 # максимально возможное число взаимных выборов
                conf_index = sum(change_row) / max_sum_mutual_change # Индекс групповой конфликтности
                index_dct['Индекс групповой конфликтности'][f'Вопрос_{idx}'] = round(conf_index,2)
                if sum(sum_row) !=0:
                    index_dct['Индекс референтности группы'][f'Вопрос_{idx}'] = round(sum(change_row) / sum(sum_row),2)
                else:
                    index_dct['Индекс референтности группы'][f'Вопрос_{idx}'] = 0
            else:
                if idx-1 in lst_negative_cols:
                    # Считаем индексы
                    max_sum_mutual_change = (len(base_df) * (len(base_df) - 1)) / 2  # максимально возможное число взаимных выборов
                    conf_index = sum(change_row) / max_sum_mutual_change  # Индекс групповой конфликтности
                    index_dct['Индекс групповой сплоченности'][f'Вопрос_{idx}'] = None
                    index_dct['Индекс групповой конфликтности'][f'Вопрос_{idx}'] = round(conf_index, 2)
                    if sum(sum_row) != 0:
                        index_dct['Индекс референтности группы'][f'Вопрос_{idx}'] = round(sum(change_row) / sum(sum_row), 2)
                    else:
                        index_dct['Индекс референтности группы'][f'Вопрос_{idx}'] = 0
                else:
                    # Считаем индексы
                    max_sum_mutual_change = (len(base_df) * (len(base_df) - 1)) / 2  # максимально возможное число взаимных выборов
                    cn_index = sum(change_row) / max_sum_mutual_change  # Индекс групповой сплоченности
                    index_dct['Индекс групповой сплоченности'][f'Вопрос_{idx}'] = round(cn_index, 2)
                    index_dct['Индекс групповой конфликтности'][f'Вопрос_{idx}'] = None
                    if sum(sum_row) != 0:
                        index_dct['Индекс референтности группы'][f'Вопрос_{idx}'] = round(sum(change_row) / sum(sum_row), 2)
                    else:
                        index_dct['Индекс референтности группы'][f'Вопрос_{idx}'] = 0


        # Суммируем словари с ответами на отдельные вопросы для получения общего словаря
        for dct in lst_value_dct:
            for fio, value_dct in dct.items():
                for subfio,value in value_dct.items():
                    result_dct[fio][subfio] +=value


        # Суммируем и сохраняем общую социоматрицу
        lst_matrix = [df for df in matrix_dct.values()]
        union_df = sum(lst_matrix)
        # Заполняем крестиками пересечения одинаковых ФИО
        for fio in lst_fio:
            union_df.loc[fio,fio] = 'X'


        if 0 < len(lst_negative_cols) < len(lst_questions):
            # Добавляем строки с суммами по отдельным негативным и позитивным выборам
            lst_positive_questions = []  # список для суммирующих строк выборов из позитивных вопросов
            lst_negative_questions = []  # список для суммирующих строк выборов из негативных вопросов

            lst_change_positive_questions = []  # список для суммирующих строк взаимных выборов из позитивных вопросов
            lst_change_negative_questions = []  # список для суммирующих строк взаимных выборов из негативных вопросов
            for idx,one_matrix_df in enumerate(lst_matrix,1):
                if idx-1 not in lst_negative_cols:
                    lst_positive_questions.append(one_matrix_df.loc['Получено выборов',lst_fio])
                    lst_change_positive_questions.append(one_matrix_df.loc['Получено взаимных выборов', lst_fio])
                else:
                    lst_negative_questions.append(one_matrix_df.loc['Получено выборов',lst_fio])
                    lst_change_negative_questions.append(one_matrix_df.loc['Получено взаимных выборов', lst_fio])

            union_df.loc['Получено положительных выборов'] = sum(lst_positive_questions)
            union_df.loc['Получено негативных выборов'] = sum(lst_negative_questions)

            union_df.loc['Получено взаимных положительных выборов'] = sum(lst_change_positive_questions)
            union_df.loc['Получено взаимных негативных выборов'] = sum(lst_change_negative_questions)

            lst_for_index = lst_fio.copy()
            lst_for_index.extend(['Получено выборов','Получено положительных выборов','Получено негативных выборов',
                                  'Получено взаимных выборов','Получено взаимных положительных выборов','Получено взаимных негативных выборов'])
            union_df = union_df.reindex(lst_for_index)



            lst_pos_cols = []  # список для суммирующих строк выборов из позитивных вопросов
            lst_neg_cols = []  # список для суммирующих строк выборов из негативных вопросов

            # Добавляем колонки с подсчетом положительных и отрицательных
            for idx,one_matrix_df in enumerate(lst_matrix,1):
                if idx-1 not in lst_negative_cols:
                    lst_pos_cols.append(one_matrix_df[lst_fio].sum(axis=1))
                else:
                    lst_neg_cols.append(one_matrix_df[lst_fio].sum(axis=1))


            union_df['+ выборов'] = sum(lst_pos_cols)
            union_df['- выборов'] = sum(lst_neg_cols)

            lst_change_cols = list(range(1, len(lst_fio) + 1))  # цифры для названий колонок
            lst_change_cols.extend(['+ выборов', '- выборов'])
            union_df.drop(columns=['Индекс социометрического статуса', 'Индекс эмоциональной экспансивности','Коэффициент удовлетворенности'], inplace=True)

            union_df.columns = lst_change_cols
            # Подсчитываем колонку Итого
            union_df['Сделано выборов'] = union_df.apply(calc_itog, axis=1)

            # Добавляем подсчет общего экспансивного индекса
            union_df['+ИЭЭ'] = round(union_df['+ выборов'] / (len(lst_fio) - 1),2)
            union_df['-ИЭЭ'] = round(union_df['- выборов'] / (len(lst_fio) - 1),2)
            union_df['Общий ИЭЭ'] = round(union_df['Сделано выборов'] / (len(lst_fio) - 1),2)
            lst_union_aa = union_df['Общий ИЭЭ'].tolist()[:len(lst_fio)+1] # делаем список чтобы потом заменить значения для выборов
            lst_union_aa.extend([None,None,None,None,None])
            union_df['Общий ИЭЭ'] = lst_union_aa

            # Убираем показатели для строк с количеством выборов
            union_df.loc['Получено выборов','+ИЭЭ'] = None
            union_df.loc['Получено выборов','-ИЭЭ'] = None
            union_df.loc['Получено выборов','Общий ИЭЭ'] = None
            union_df.loc['Получено взаимных выборов','+ИЭЭ'] = None
            union_df.loc['Получено взаимных выборов','-ИЭЭ'] = None
            union_df.loc['Получено взаимных выборов','Общий ИЭЭ'] = None



            # Добавляем колонки с социометрическим индексом
            for idx, one_df in enumerate(lst_matrix, 1):
                if idx - 1 in lst_negative_cols:
                    union_df[f'-ИСС Вопрос {idx}'] = one_df['Индекс социометрического статуса']
                else:
                    union_df[f'+ИСС Вопрос {idx}'] = one_df['Индекс социометрического статуса']

            # Добавляем колонки с индексом эмоциональной экспансивности
            for idx, one_df in enumerate(lst_matrix, 1):
                if idx - 1 in lst_negative_cols:
                    union_df[f'-ИЭЭ Вопрос {idx}'] = one_df['Индекс эмоциональной экспансивности']
                else:
                    union_df[f'+ИЭЭ Вопрос {idx}'] = one_df['Индекс эмоциональной экспансивности']

            # Добавляем колонки с коэфициентом эмоциональной удовлетворенности
            for idx, one_df in enumerate(lst_matrix, 1):
                if idx - 1 in lst_negative_cols:
                    union_df[f'-КУ Вопрос {idx}'] = one_df['Коэффициент удовлетворенности']
                else:
                    union_df[f'+КУ Вопрос {idx}'] = one_df['Коэффициент удовлетворенности']

            # Создаем список (не матрицу) со всей статистикой
            stat_df = pd.DataFrame(index=lst_fio)
            stat_df['Сделано выборов'] = union_df.loc[lst_fio,'Сделано выборов']
            stat_df['Сделано + выборов'] = union_df.loc[lst_fio,'+ выборов']
            stat_df['Сделано - выборов'] = union_df.loc[lst_fio,'- выборов']

            stat_df['Получено выборов'] = list(union_df.loc['Получено выборов',list(range(1,len(lst_fio)+1))])
            stat_df['Получено + выборов'] = list(union_df.loc['Получено положительных выборов',list(range(1,len(lst_fio)+1))])
            stat_df['Получено - выборов'] = list(union_df.loc['Получено негативных выборов',list(range(1,len(lst_fio)+1))])

            stat_df['Получено взаимных выборов'] = list(union_df.loc['Получено взаимных выборов',list(range(1,len(lst_fio)+1))])
            stat_df['Получено взаимных + выборов'] = list(union_df.loc['Получено взаимных положительных выборов',list(range(1,len(lst_fio)+1))])
            stat_df['Получено взаимных - выборов'] = list(union_df.loc['Получено взаимных негативных выборов',list(range(1,len(lst_fio)+1))])

            stat_df['+ИЭЭ'] = union_df['+ИЭЭ']
            stat_df['-ИЭЭ'] = union_df['-ИЭЭ']

            stat_df.index.name = 'ФИО'
            union_df.index.name = 'ФИО'
            stat_df = pd.merge(stat_df,union_df.loc[lst_fio,'Общий ИЭЭ':],how='inner',left_index=True,right_index=True)

            stat_df.loc['Итого'] = 0 # добавляем строку для сумм выборов
            stat_df.loc['Итого','Сделано выборов'] = sum(stat_df['Сделано выборов'])
            stat_df.loc['Итого','Сделано + выборов'] = sum(stat_df['Сделано + выборов'])
            stat_df.loc['Итого','Сделано - выборов'] = sum(stat_df['Сделано - выборов'])

            stat_df.loc['Итого','Получено выборов'] = sum(stat_df['Получено выборов'])
            stat_df.loc['Итого','Получено + выборов'] = sum(stat_df['Получено + выборов'])
            stat_df.loc['Итого','Получено - выборов'] = sum(stat_df['Получено - выборов'])

            stat_df.loc['Итого','Получено взаимных выборов'] = sum(stat_df['Получено взаимных выборов'])
            stat_df.loc['Итого','Получено взаимных + выборов'] = sum(stat_df['Получено взаимных + выборов'])
            stat_df.loc['Итого','Получено взаимных - выборов'] = sum(stat_df['Получено взаимных - выборов'])

            for name_column in stat_df.columns[9:]:
                stat_df.loc['Итого',name_column] = None




        else:
            union_df.drop(columns=['Индекс социометрического статуса','Индекс эмоциональной экспансивности','Коэффициент удовлетворенности'], inplace=True)

            union_df.columns = range(1, len(lst_fio) +1)
            # Подсчитываем колонку Итого
            union_df['Сделано выборов'] = union_df.apply(calc_itog,axis=1)

            union_df['Общий ИЭЭ'] = round(union_df['Сделано выборов'] / (len(lst_fio) - 1),2)
            lst_union_aa = union_df['Общий ИЭЭ'].tolist()[:len(lst_fio)+1] # делаем список чтобы потом заменить значения для выборов
            lst_union_aa.extend([None])
            union_df['Общий ИЭЭ'] = lst_union_aa
            union_df.loc['Получено выборов','Общий ИЭЭ'] = None


            # Добавляем колонки с социометрическим индексом
            for idx,one_df in enumerate(lst_matrix,1):
                if idx-1 in lst_negative_cols:
                    union_df[f'-ИСС Вопрос {idx}'] = one_df['Индекс социометрического статуса']
                else:
                    union_df[f'+ИСС Вопрос {idx}'] = one_df['Индекс социометрического статуса']
            # Добавляем колонки с индексом эмоциональной экспансивности
            for idx, one_df in enumerate(lst_matrix, 1):
                if idx - 1 in lst_negative_cols:
                    union_df[f'-ИЭЭ Вопрос {idx}'] = one_df['Индекс эмоциональной экспансивности']
                else:
                    union_df[f'+ИЭЭ Вопрос {idx}'] = one_df['Индекс эмоциональной экспансивности']
            # Добавляем колонки с коэфициентом эмоциональной удовлетворенности
            for idx, one_df in enumerate(lst_matrix, 1):
                if idx - 1 in lst_negative_cols:
                    union_df[f'-КУ Вопрос {idx}'] = one_df['Коэффициент удовлетворенности']
                else:
                    union_df[f'+КУ Вопрос {idx}'] = one_df['Коэффициент удовлетворенности']


            # Создаем список (не матрицу) со всей статистикой
            stat_df = pd.DataFrame(index=lst_fio)
            stat_df['Сделано выборов'] = union_df.loc[lst_fio,'Сделано выборов']
            stat_df['Получено выборов'] = list(union_df.loc['Получено выборов',list(range(1,len(lst_fio)+1))])
            stat_df['Взаимных выборов'] = list(union_df.loc['Получено взаимных выборов',list(range(1,len(lst_fio)+1))])
            stat_df.index.name = 'ФИО'
            union_df.index.name = 'ФИО'
            stat_df = pd.merge(stat_df,union_df.loc[lst_fio,'Общий ИЭЭ':],how='inner',left_index=True,right_index=True)

            stat_df.loc['Итого'] = 0 # добавляем строку для сумм выборов
            stat_df.loc['Итого','Сделано выборов'] = sum(stat_df['Сделано выборов'])
            stat_df.loc['Итого','Получено выборов'] = sum(stat_df['Получено выборов'])
            stat_df.loc['Итого','Взаимных выборов'] = sum(stat_df['Взаимных выборов'])

            for name_column in stat_df.columns[3:]:
                stat_df.loc['Итого',name_column] = None






        # Создаем индекс с добавлением цифр
        lst_index_union = [] # список для хранения индекса с добавлением цифр
        for idx,value in enumerate(union_df.index,1):
            if value in  lst_fio:
                lst_index_union.append(f'{idx}. {value}')
            else:
                lst_index_union.append(value)

        union_df.index = lst_index_union
        union_df.to_excel(f'{end_folder}/Общая социоматрица {current_time}.xlsx',index=True)


        stat_df.to_excel(f'{end_folder}/Списочная статистика {current_time}.xlsx',index=True)


        index_df = pd.DataFrame.from_dict(index_dct, orient='index')
        index_df.to_excel(f'{end_folder}/Индексы {current_time}.xlsx',index=True)

        with pd.ExcelWriter(f'{end_folder}/Для проверки {current_time}.xlsx', engine='xlsxwriter') as writer:
            for name_sheet,out_df in checked_dct.items():
                out_df.to_excel(writer,sheet_name=str(name_sheet),index=False)

        with pd.ExcelWriter(f'{end_folder}/Социоматрицы отдельные {current_time}.xlsx', engine='xlsxwriter') as writer:
            for name_sheet,out_df in matrix_dct.items():
                # Заполняем крестиками пересечения одинаковых ФИО
                for fio in lst_fio:
                    out_df.loc[fio, fio] = 'X'
                # Создаем индекс с добавлением цифр
                temp_lst_index_union = []  # список для хранения индекса с добавлением цифр
                for idx, value in enumerate(out_df.index, 1):
                    if value in lst_fio:
                        temp_lst_index_union.append(f'{idx}. {value}')
                    else:
                        temp_lst_index_union.append(value)
                out_df.index = temp_lst_index_union


                # Создаем колонки с добавлением цифр
                lst_one_cols  = list(range(1,len(lst_fio)+1)) # цифры для названий колонок
                lst_one_cols.extend(['Индекс социометрического статуса', 'Индекс эмоциональной экспансивности','Коэффициент удовлетворенности'])
                out_df.columns = lst_one_cols

                # Подсчитываем колонку Итого
                out_df['Сделано выборов'] = out_df.apply(calc_itog, axis=1)

                out_df.to_excel(writer,sheet_name=str(name_sheet),index=True)

        # Создаем и сохраняем социограммы и выборы тех кто не тестировался

        create_sociograms(lst_value_dct,end_folder,dct_missing_person,dct_chosen_missing)
    except NotReqColumn:
        messagebox.showerror('Лахеcис',
                             f'При обработке файла с выборами социометрии обнаружено отсутствие обязательной колонки:\n'
                             f'{diff_req_cols}\n В таблице с выборами обязательно должна быть колонка с названием ФИО')
    except PermissionError:
        messagebox.showerror('Лахеcис',
                                 f'Закройте все файлы созданные программой Лахесис и запустите повторно обработку')
    except OSError:
        messagebox.showerror('Лахеcис',
                             f'Слишком длинный путь к создаваемым файлам. Выберите более короткий путь сохранения (прямо на диске C)')

    except KeyError:
        messagebox.showerror('Лахеcис',
                             f'Проверьте структуру файла с выборами. Если вы использовали Яндекс форму, то чекбокс типа обрабатываемого файла должен быть пустым(галочки не должно стоять).\n'
                             f'Если файл создан с помощью гугл формы или других средств, то есть для каждого вопроса выборы тестируемого находятся в одной ячейке\n'
                             f'и разделены запятой, то чекбокс типа обрабатываемого файла должен быть нажат(галочка должна стоять)')
    else:
        messagebox.showinfo('Лахеcис',
                                'Данные успешно обработаны')





















if __name__ == '__main__':
    main_file = 'data/Социометрия.xlsx'
    main_file = 'data/Социометрия негатив.xlsx'
    # main_file = 'data/Социометрия смеш.xlsx'
    main_file = 'data/Группа 110 н.xlsx'
    main_file = 'data/Социометрия смеш.xlsx'

    # main_file = 'data/Социометрия Гугл.xlsx'
    main_quantity_descr_cols = 2
    # main_quantity_descr_cols = 1
    main_negative_questions = '2,4'
    # main_negative_questions = '2'
    main_end_folder = 'data/Результат'
    main_checkbox_not_yandex = 'No'
    # main_checkbox_not_yandex = 'Yes'
    generate_result_sociometry(main_file,main_quantity_descr_cols,main_negative_questions,main_end_folder,main_checkbox_not_yandex)
    print('Lindy Booth')
