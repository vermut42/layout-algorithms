#### This script realize Feducci-Mattheises decomposition algorithm ####
#### Created on Python 3.8.9 / checked on Python 3.10.4
# v0.1    @ilyaShafeev  / 30 April, 2022 - main algorithm
# v0.1.1  @vermut42     / 30 April, 2022 - reading config file from command line

from cmath import inf
import numpy as np
import argparse


def area_balance_criterion(cells_area: np.ndarray, block_A: np.ndarray, balance_factor: float):
    '''
    Проверка на соответствие площади блока А фактору баланса, вычисление потери отклонения площади блока А
    '''
    max_V: float = np.max(cells_area)
    area_V: float = np.sum(cells_area)
    area_A: float = 0

    for i in block_A:
        area_A += cells_area[i]

    loss = abs(balance_factor - area_A/area_V)

    if(balance_factor * area_V - max_V <= area_A <= balance_factor * area_V + max_V):
        return area_A, loss
    else:
        return False


def cells_growth(graph_matrix, block_A_idx, block_B_idx, all_FS, all_TE, all_det_g, set_nodes):
    '''
    Расчет параметров вершин графа FS,TE,dg
    '''
    new_all_FS = np.array([x if(i in set_nodes) else 0 for (i, x) in enumerate(all_FS)])
    new_all_TE = np.array([x if(i in set_nodes) else 0 for (i, x) in enumerate(all_TE)])
    new_all_det_g = np.array([x if(i in set_nodes) else 0 for (i, x) in enumerate(all_det_g)])

    in_line_sum_A = np.zeros((graph_matrix.shape[1],))
    in_line_sum_B = np.zeros((graph_matrix.shape[1],))

    for node in block_A_idx:
        in_line_sum_A = np.add(in_line_sum_A, graph_matrix[node, :])

    for node in block_B_idx:
        in_line_sum_B = np.add(in_line_sum_B, graph_matrix[node, :])

    for i in range(graph_matrix.shape[0]):
        if(i in block_A_idx and i not in set_nodes):
            for k in range(graph_matrix.shape[1]):
                if(graph_matrix[i, k] == 1 and in_line_sum_A[k] == 1):
                    new_all_FS[i] += 1
                if(graph_matrix[i, k] == 1 and in_line_sum_B[k] == 0):
                    new_all_TE[i] += 1

        if(i in block_B_idx and i not in set_nodes):
            for k in range(graph_matrix.shape[1]):
                if(graph_matrix[i, k] == 1 and in_line_sum_B[k] == 1):
                    new_all_FS[i] += 1
                if(graph_matrix[i, k] == 1 and in_line_sum_A[k] == 0):
                    new_all_TE[i] += 1

    for idx in range(len(new_all_det_g)):
        if(idx not in set_nodes):
            new_all_det_g[idx] = new_all_FS[idx] - new_all_TE[idx]

    return new_all_FS, new_all_TE, new_all_det_g


def find_base_cell(balance_factor, cells_area, block_A, block_B, all_det_g, set_nodes):
    '''
    Поис базовой ячейки итерации
    '''
    first_order_sort = np.flip(np.sort(all_det_g))
    idx = 0

    set = False
    set_node = None
    set_block_A = None
    set_block_B = None

    for i in range(len(all_det_g)):
        cur_max_idx = np.where(first_order_sort[idx] == all_det_g)[0]
        min_area = inf

        for cur_max in cur_max_idx:
            if(cur_max in block_A and cur_max not in set_nodes):
                cur_max_A = np.where(block_A == cur_max)[0][0]

                new_block_A = np.delete(block_A, cur_max_A)
                area_balance = area_balance_criterion(cells_area, new_block_A, balance_factor)

                if((area_balance is not False)):
                    if(area_balance[1] <= min_area):
                        set_block_B = np.append(block_B, block_A[cur_max_A])
                        set_block_A = new_block_A

                        min_area = area_balance[1]
                        set_node = cur_max

                        set = True
                else:
                    first_order_sort = np.delete(first_order_sort, idx)
                    idx -= 1

            if(cur_max in block_B and cur_max not in set_nodes):
                cur_max_B = np.where(block_B == cur_max)[0][0]

                new_block_A = np.append(block_A, block_B[cur_max_B])
                area_balance = area_balance_criterion(cells_area, new_block_A, balance_factor)

                if((area_balance is not False)):
                    if(area_balance[1] <= min_area):
                        set_block_A = new_block_A
                        set_block_B = np.delete(block_B, cur_max_B)

                        min_area = area_balance[1]
                        set_node = cur_max

                        set = True
                else:
                    first_order_sort = np.delete(first_order_sort, idx)
                    idx -= 1
        idx += 1

        if(set):
            return set_block_A, set_block_B, set_node


def slice_cost(graph_matrix, block_A, block_B):
    '''
    Нохождение цены разреза между блоками
    '''
    cost = 0
    for x in range(graph_matrix.shape[1]):
        col = graph_matrix[:, x]
        if(1 in col[block_B] and 1 in col[block_A]):
            cost += 1
    return cost


def find_best(collect_G, collect_area):
    '''
    Нахождение лучшего решения за 1 проход
    '''
    max_G = np.where(collect_G == collect_G[np.argmax(collect_G)])[0]

    min_area = inf
    best = None
    out_area = None

    for _g in max_G:
        if(collect_area[_g][1] <= min_area):
            best = _g
            min_area = collect_area[_g][1]
            out_area = collect_area[_g][0]

    return collect_G[best], best, int(out_area)


if(__name__ == '__main__'):
    '''
    Формат файла:

    [ca]=2,4,1,4,5 // веса вершин
    [bf]=0.375 // фактор баланса
    [bA]=1,2 // вершины в блоке А
    [bB]=3,4,5 // вершина в блоке В

    Матрица инцидентности графа:
      v1,v2,v3,v4,v5
   e1 1, 1, 1, 1, 0
   e2 1, 1, 0, 0, 0
   e3 0, 1, 0, 0, 1
   e4 0, 0, 1, 0, 1
   e5 0, 0, 0, 1, 0
    '''
    parser = argparse.ArgumentParser(description='A tutorial of argparse!')
    parser.add_argument('--file')
    args = parser.parse_args()
    file = args.file
    with open(file) as f:

        lines = f.readlines()

        '''
        Параметры графа
        '''
        cells_area = np.array([int(x, base=10) for x in lines[0][5:].split(',')])
        balance_factor = float(lines[1][5:])
        block_A = [int(x, base=10)-1 for x in lines[2][5:].split(',')]
        block_B = [int(x, base=10)-1 for x in lines[3][5:].split(',')]
        lines = lines[4:]

        graph_matrix = np.empty((len(lines), len(lines[0].split(','))), dtype=np.int32)

        '''
        Внутрение параметры матрицы
        '''
        all_FS = np.zeros((len(lines),), dtype=np.int32)
        all_TE = np.zeros((len(lines),), dtype=np.int32)
        all_det_g = np.zeros((len(lines),), dtype=np.int32)

        for (i, y) in enumerate(lines):
            graph_matrix[i, :] = np.array([int(x, base=10) for x in y.split(',')])

        step = 0

        start_cost = 0
        set_nodes = np.array([], dtype=np.int32)
        collect_G = np.array([], dtype=np.int32)
        collect_area = np.empty((0, 2), dtype=np.int32)
        collect_silces = np.array([], dtype=np.int32)

        iteration = 0

        while(set_nodes.shape[0] != len(lines)):

            if(iteration == 0):
                start_cost = slice_cost(graph_matrix, block_A, block_B)

            print('\033[95m' + '\033[1m' + f'\n--------> Итерация i = {iteration+1}\n' + '\033[0m')

            all_FS, all_TE, all_det_g = cells_growth(graph_matrix, block_A, block_B, all_FS, all_TE, all_det_g, set_nodes)
            block_A, block_B, set_node = find_base_cell(balance_factor, cells_area, block_A, block_B, all_det_g, set_nodes)
            set_nodes = np.append(set_nodes, set_node)

            collect_G = np.append(collect_G, collect_G[-1] + all_det_g[set_node] if(collect_G.shape[0] > 0) else all_det_g[set_node])
            collect_silces = np.append(collect_silces, slice_cost(graph_matrix, block_A, block_B))

            '''
            Сохраняем реальное значение площади и потерю площади(|r - area(A)/area(V)|)
            '''
            area = area_balance_criterion(cells_area, block_A, balance_factor)
            add_area = np.empty((1, 2))
            add_area[0, :] = np.array([area[0], area[1]])
            collect_area = np.append(collect_area, add_area, axis=0)

            for i in range(len(all_FS)):
                print(f'Cell {i+1}: FS(Cell_{i+1}) = {all_FS[i]}   TE(Cell_{i+1}) = {all_TE[i]}   Δg(Cell_{i+1}) = {all_det_g[i]}')

            print(f'\nПосле итерации i = {iteration+1}: Компоненты A={(block_A+1).tolist()} и B={(block_B+1).tolist()}\nЗафиксированы ячейки: {(set_nodes+1).tolist()}')
            print(f'\nЦена разреза: {collect_silces[-1]}\n')
            iteration += 1

        _g, best, min_area = find_best(collect_G, collect_area)
        print(f'Лучший префикс прохода: Gm = {_g}, i={best+1}, area(A) = {min_area}, цена разреза уменьшилась с {start_cost} до {collect_silces[best]} \n')
