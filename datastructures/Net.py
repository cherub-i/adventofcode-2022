from copy import copy


class Net:
    def __init__(self):
        self.node_list: dict[str, Node] = dict()
        self.distance_dict: dict[str, dict[str, int]] = dict()

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
        for node_name_outer, node_outer in self.node_list.items():
            self.distance_dict[node_name_outer] = dict()
            for node_name_innner in self.node_list.keys():
                self.distance_dict[node_name_outer][node_name_innner] = -1
            for edge in node_outer.edge_list:
                self.distance_dict[edge.node_from.name][
                    edge.node_to.name
                ] = edge.cost

        is_ready = False
        while not is_ready:
            is_ready = True
            for (
                node_from_name,
                node_from_path_dict,
            ) in self.distance_dict.items():
                node_from_connection_list: list[tuple[str, int]] = list()
                for to_node_name, cost in node_from_path_dict.items():
                    if cost > 0:
                        node_from_connection_list.append((to_node_name, cost))
                for node_from_connection in node_from_connection_list:
                    for connection_to in node_from_connection_list:
                        if node_from_connection != connection_to:
                            new_from = node_from_connection[0]
                            new_to = connection_to[0]
                            new_distance = (
                                node_from_connection[1] + connection_to[1]
                            )
                            if self.distance_dict[new_from][new_to] == -1:
                                self.distance_dict[new_from][
                                    new_to
                                ] = new_distance
                                is_ready = False


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
    def __init__(self):
        self.node_list: list[Node] = list()
        self.step_list: list[str] = list()
        self.cost: int = 0

    def last_node(self) -> Node:
        return self.node_list[-1]

    def add_start(self, node: Node) -> None:
        self.node_list.append(node)

    def travel(self, edge: Edge) -> None:
        self.add_step(edge.node_to, edge.cost)

    def add_step(self, node: Node, cost: int) -> None:
        self.node_list.append(node)
        self.step_list.append(
            f"{self.node_list[-2].name}>{self.last_node().name}"
        )
        self.cost += cost

    def get_copy(self) -> "Path":
        new_path: Path = Path()
        new_path.node_list = copy(self.node_list)
        new_path.step_list = copy(self.step_list)
        new_path.cost = self.cost
        return new_path

    def __str__(self):
        return f"{', '.join(self.step_list)}, cost: {self.cost}"
