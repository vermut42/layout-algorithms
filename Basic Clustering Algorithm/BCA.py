from cmath import inf
import numpy as np
import argparse


def area (graph_matrix):
    cells_area = []
    for row in graph_matrix:
        cells_area.append(sum(row))
    return(cells_area)

def get_indices(lst, el):
    list = []
    for i in range(len(lst)):
        if lst[i] == el:
            list.append(i)
    return list



if(__name__ == '__main__'):
    '''
    Формат файла:

    Матрица смежности графа:
      v1,v2,v3,v4,v5
   v1 1, 1, 1, 1, 0
   v2 1, 1, 0, 0, 0
   v3 0, 1, 0, 0, 1
   v4 0, 0, 1, 0, 1
   v5 0, 0, 0, 1, 0
    '''
    parser = argparse.ArgumentParser(description='A tutorial of argparse!')
    parser.add_argument('--file')
    parser.add_argument('--area')
    args = parser.parse_args()
    file = args.file
#    area_max = args.area_max
    with open(file) as f:

        lines = f.readlines()

        '''
        Параметры графа
        '''

        graph_matrix = np.empty((len(lines), len(lines[0].split(','))), dtype=np.int32)

        for (i, y) in enumerate(lines):
            graph_matrix[i, :] = np.array([int(x, base=10) for x in y.split(',')])

    print(graph_matrix)

    cells_area = area(graph_matrix)
    print(cells_area)
    print(cells_area.index(max(cells_area)))
    vertices = []
    for index in range(1,len(cells_area)+1):
        vertices.append(index)
    print(vertices)

    step = 1
    b = []
    while len(vertices) > 0:
        if len(b) == 0:
            index_max = cells_area.index(max(cells_area))
        vertices.pop(index_max)
        b.append(vertices[index_max])
        print("Block",b)
        print("Vertices",vertices)
 





        
