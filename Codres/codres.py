import re
import sys

class Block:
    """Класс блока."""

    def __init__(self, graph: dict, num_pins: int, square: int,  *args) -> None:
        self.graph = graph
        self.square = square
        self.num_pins = num_pins
        self.elements = []
        self.chains = []
        for arg in args:
            self.chains.extend(graph[arg])
            self.elements.append(arg)

    def add(self, *args) -> None:
        self.elements += args
        for arg in args:
            self.chains.extend(self.graph[arg])

    def del_e(self, *args) -> None:
        for arg in args:
            for c in self.graph[arg]:
                self.chains.remove(c)
            self.elements.remove(arg)

    def print_block(self):
        print(self.chains)
        print(self.elements)

    def block_t(self) -> set:
        return set(self.chains)

    def check_st(self) -> bool:
        """Проверка на ограничения."""

        return True if (len(self.chains) <= self.square
                        and len(self.block_t()) <= self.num_pins) else False

    def cut_graph(self) -> dict:
        """Обрезание изначального графа от Block."""

        cut_graph_res = self.graph.copy()

        for key in self.elements:
            cut_graph_res.pop(key, None)

        for chain_block in self.block_t():
            for element, chain_graph in cut_graph_res.items():
                if chain_block in chain_graph:
                    if "-" not in chain_block:
                        chain_graph.remove(chain_block)
                        chain_graph.add("-" + chain_block)
                        cut_graph_res[element] = chain_graph
        return cut_graph_res

    def cut_graph_virtual(self) -> dict:
        """Виртуальное обрезание изначального графа от Block."""

        cut_graph_res = self.graph.copy()

        for key in self.elements:
            cut_graph_res.pop(key, None)

        return cut_graph_res

    def con(self, block_2) -> set:
        """Конъюнкция двух блоков."""

        return self.block_t().intersection(block_2.block_t())

    def dis(self, block_2) -> set:
        """Дизъюнкция двух блоков."""

        return self.block_t().union(block_2.block_t()) - self.con(block_2)


def input_graph() -> dict:
    """Ввод графа."""

    graph = {}
    elements = int(input("Введите количество элементов:"))
    print("Если цепь периферийная, то она должна быть с '-' ")
    for element in range(1, elements+1):
        graph[element] = input(f"Введите цепи с которыми соединен элемент {element}:").split()

    print(graph)
    return graph


def len_periphery(chains: list) -> int:
    res = 0
    for chain in chains:
        res += 1 if "-" in chain else 0
    return res


def choice_a(graph: dict, T: int , S: int) -> int:
    a = dict()
    a_chain_max = len_periphery(graph[list(graph.keys())[0]])
    for buf_a, buf_a_chains in graph.items():
        if a_chain_max <= len_periphery(buf_a_chains):
            a_chain_max = len_periphery(buf_a_chains)
            a.setdefault(a_chain_max,  list()).append(buf_a)

    if len(a[max(a)]) > 1:
        con_dict = dict()
        for buf_a in a[max(a)]:
            A = Block(graph, T, S, buf_a)
            buf = Block(A.cut_graph_virtual(), T, S, *(set(graph.keys()).difference({buf_a})))
            con_dict.setdefault(len(A.con(buf)), list()).append(buf_a)
        return min(con_dict[min(con_dict.keys())])
    else:
        return a[max(a)][0]


def choice_b(graph: dict, block: Block, T: int , S: int) -> bool:
    if graph:
        con_max_dict = dict()
        con_max = 0
        for key in graph.keys() - block.elements:
            B = Block(block.cut_graph_virtual(), T, S, key)
            if con_max <= len(B.con(block)):
                con_max = len(B.con(block))
                con_max_dict.setdefault(con_max, list()).append(key)

        dis_min_dict = dict()
        dis_min = T
        for key in con_max_dict[max(con_max_dict.keys())]:
            P = Block(graph, T, S, key)
            if len(P.dis(block)) <= dis_min:
                dis_min = len(P.dis(block))
                dis_min_dict.setdefault(dis_min, list()).append(key)

        b = min(dis_min_dict[min(dis_min_dict.keys())])
        block.add(b)
        if not block.check_st():
            block.del_e(b)
            for buf_b in list(block.cut_graph_virtual().keys()):
                block.add(buf_b)
                if block.check_st():
                    return False
                else:
                    block.del_e(buf_b)
            return False
        return True
    return False


def codres(graph: dict, T: int, S: int) -> list:
    answer = []
    while graph:
        a = choice_a(graph, T, S)
        B = Block(graph, T, S, a)

        while choice_b(B.cut_graph_virtual(), B, T, S, ):
            pass
        answer.append(B.elements)
        graph = B.cut_graph()
    return answer


def read_file(name_file: str) -> list():
    with open(name_file) as f:
        return f.readlines()


def processing_file(file: list()) -> dict:
    data_file = {
        "T": None,
        "S": None,
        "G": dict(),
    }
    i = 0
    for line in file:
        if "T" in line:
            data_file["T"] = int(line.split()[-1])

        if "S" in line:
            data_file["S"] = int(line.split()[-1])

        if "G" in line:
            break
        i += 1

    for line in file[i+1:len(file)-1]:
        chain = re.compile("[-+]?\d+").findall(line)
        data_file["G"][int(chain[0])] = set(chain[1:])
    return data_file


def main():
    if sys.argv[1] == "-arm":
        T = int(input("Введите ограничение по T:"))
        S = int(input("Введите ограничение по S:"))
        G = input_graph()
        print(codres(G, T, S,))
    elif sys.argv[1] == "-f" and len(sys.argv) == 3:
        data = processing_file(read_file(sys.argv[2]))
        print(codres(data["G"], data["T"], data["S"], ))
    else:
        print("Неверный ключ")

if __name__ == '__main__':
    main()
