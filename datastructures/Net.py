from copy import copy


class Net:
    def __init__(self):
        self.node_list: dict[str, Node] = dict()
        self.distance_dict: dict[str, dict[str, Path]] = dict()

    def add_node(self, node: "Node"):
        if node not in self.node_list:
            self.node_list[node.name] = node
            return True
        return False

    def add_edge(
        self, node_name_from: str, node_name_to: str, value: int, cost: int
    ):
        node_from = self.get_node(node_name_from)
        node_to = self.get_node(node_name_to)
        node_from.add_edge(Edge(node_from, node_to, value, cost))
        node_to.add_edge(Edge(node_to, node_from, value, cost))

    def get_node(self, node_name: str) -> "Node":
        return self.node_list[node_name]

    def calculate_path_list(self):
        self._initialize_distance_dict()
        self._fill_distance_dict_initial_edges()
        self._fill_distance_dict_derive_all()

    def _initialize_distance_dict(self):
        for node_name in self.node_list.keys():
            self.distance_dict[node_name] = dict()

    def _fill_distance_dict_initial_edges(self):
        for node in self.node_list.values():
            for edge in node.edge_list:
                path: Path = Path(edge.node_from)
                path.travel(edge)
                self.distance_dict[edge.node_from.name][
                    edge.node_to.name
                ] = path

    def _fill_distance_dict_derive_all(self):
        is_ready = False

        while not is_ready:
            is_ready = True
            for node_from_path_dict in self.distance_dict.values():
                node_from_path_list: list[Path] = [
                    path
                    for path in node_from_path_dict.values()
                    if path is not None
                ]
                new_path_list = Net.generate_connecting_path_list(
                    node_from_path_list
                )
                if new_path_list:
                    for path in new_path_list:
                        existing_path = self.distance_dict[
                            path.start().name
                        ].get(path.end().name, None)
                        if (
                            existing_path == None
                            or existing_path.cost > path.cost
                        ):
                            self.distance_dict[path.start().name][
                                path.end().name
                            ] = path
                            is_ready = False

    @classmethod
    def generate_connecting_path_list(
        cls, path_list: list["Path"]
    ) -> list["Path"]:
        if len(path_list) <= 1:
            return None

        new_path_list: list[Path] = list()
        for path_end_1 in path_list:
            for path_end_2 in path_list:
                if path_end_1 != path_end_2:
                    new_path = path_end_1.get_copy(True)
                    for i, node in enumerate(path_end_2.node_list[1:]):
                        new_path.add_step(node, path_end_2.cost_list[i - 1])
                        new_path_list.append(new_path)
        return new_path_list


class Node:
    def __init__(self, name: str, value: int = 0, cost: int = 0):
        self.name: str = name
        self.value: int = value
        self.cost: int = cost
        self.edge_list: list[Edge] = list()

    def add_edge(self, edge: "Edge") -> bool:
        if edge not in self.edge_list:
            self.edge_list.append(edge)
            return True
        return False


class Edge:
    def __init__(
        self, from_node: Node, to_node: Node, value: int = 0, cost: int = 0
    ):
        self.node_from: Node = from_node
        self.node_to: Node = to_node
        self.value: int = value
        self.cost: int = cost

    def __eq__(self, other: Node) -> bool:
        if not isinstance(other, Edge):
            return NotImplemented

        return (
            self.node_from == other.node_from and self.node_to == other.node_to
        )


class Path:
    def __init__(self, start_node=None):
        self.node_list: list[Node] = list()
        self.cost_list: list[int] = list()
        self.cost: int = 0
        if start_node is not None:
            self.add_start(start_node)

    def add_start(self, node: Node) -> None:
        self.node_list.append(node)

    def start(self) -> Node:
        return self.node_list[0]

    def end(self) -> Node:
        return self.node_list[-1]

    def travel(self, edge: Edge) -> None:
        self.add_step(edge.node_to, edge.cost)

    def add_step(self, node: Node, cost: int) -> None:
        self.node_list.append(node)
        self.cost_list.append(cost)
        self.cost += cost

    def get_copy(self, reversed: bool = False) -> "Path":
        new_path: Path = Path()
        new_path.node_list = copy(self.node_list)
        new_path.cost_list = copy(self.cost_list)
        new_path.cost = self.cost
        if reversed:
            new_path.node_list.reverse()
            new_path.cost_list.reverse()
        return new_path

    def get_combination(self, other: "Path") -> "Path":
        new: Path = self.get_copy(True)
        for i, node in enumerate(other.node_list):
            if node != new.end():
                new.add_step(node, other.cost_list[i - 1])
        return new

    def __eq__(self, other: "Path") -> bool:
        if not isinstance(other, Path):
            return NotImplemented

        return self.node_list == other.node_list

    def __str__(self):
        line_list: list = list()
        for i in range(len(self.node_list) - 1):
            line_list.append(
                f"{self.node_list[i].name}>{self.node_list[i+1].name} ({self.cost_list[i]})"
            )
        return f"{' - '.join(line_list)}, total: {self.cost}"


def main():
    net: Net = Net()

    node_a: Node = Node("A", 1, 0)
    node_b: Node = Node("B", 2, 0)
    node_c: Node = Node("C", 3, 0)
    node_d: Node = Node("D", 4, 0)
    node_e: Node = Node("E", 5, 0)

    edge_ab: Edge = Edge(node_a, node_b, 0, 1)
    edge_bc: Edge = Edge(node_b, node_c, 0, 2)
    edge_bd: Edge = Edge(node_b, node_d, 0, 3)
    edge_ae: Edge = Edge(node_a, node_e, 0, 5)

    print("path abc")
    path_abc = Path(node_a)
    path_abc.travel(edge_ab)
    path_abc.travel(edge_bc)
    print(path_abc)
    print(f"copy: {path_abc.get_copy()}")
    print(f"reversed copy: {path_abc.get_copy(True)}")
    print()

    print("path ae")
    path_ae = Path(node_a)
    path_ae.travel(edge_ae)
    print(path_ae)
    print()

    path_new = path_abc.get_combination(path_ae)
    print(f"combination: {path_new}")
    print()

    net.add_node(node_a)
    net.add_node(node_b)
    net.add_node(node_c)
    net.add_node(node_d)
    net.add_node(node_e)

    net.add_edge("A", "B", 0, 1)
    net.add_edge("B", "C", 0, 2)
    net.add_edge("B", "D", 0, 3)
    net.add_edge("A", "E", 0, 5)

    net.calculate_path_list()

    print(net)


if __name__ == "__main__":
    main()
