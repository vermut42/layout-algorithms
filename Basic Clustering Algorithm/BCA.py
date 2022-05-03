from cmath import inf
import numpy as np
import argparse


def vertices_area (vertices,graph_matrix):
    v_area = []
    for v in vertices:
        vertice = graph_matrix[v]
        v_area.append(sum(vertice))
    return(v_area)

def get_indices(list, element):
    list = []
    for i in range(len(list)):
        if list[i] == element:
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

    # формирование списка вершин
    vertices = []
    for index in range(len(graph_matrix)):
        vertices.append(index)

    # определение площадей всех вершин    
    v_area = vertices_area(vertices,graph_matrix)

    print(v_area.index(max(v_area)))
  
    vertices_run = vertices
    block = []
    while len(vertices_run) > 0:
   
        if len(block) == 0:
            v_area = vertices_area(vertices_run,graph_matrix)
            index_max = v_area.index(max(v_area))
            block.append(vertices[index_max])
            vertices_run.pop(index_max)
        
            print("Block",block)
            print("Actual list of vertices",vertices_run)
        elif len(block) < 3:
            for vertice in block:
                print(get_indices(graph_matrix[vertice],1))

 





        