from copy import copy


class Net:
    def __init__(self):
        self.node_list: dict[str, Node] = dict()

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


class PathFinder:
    def __init__(self, node_from: Node, node_to: Node):
        self.node_from: Node = node_from
        self.node_to: Node = node_to
        self.path_list: list[Path] = list()
        self.has_arrived = False
        self.cost_of_travel = -1

    def build_routes_to_target(self):
        if not self.path_list:
            for edge in self.node_from.edge_list:
                path: Path = Path()
                path.add_start(edge.node_from)
                path.travel(edge)
                self.path_list.append(path)
                if edge.node_to == self.node_to:
                    self.has_arrived = True
        else:
            new_path_list: list[Path] = list()
            while self.path_list:
                path = self.path_list.pop()
                if path.last_node() == self.node_to:
                    self.has_arrived = True
                    new_path_list.append(path)
                else:
                    for edge in path.last_node().edge_list:
                        if edge.node_to not in path.node_traveled_list:
                            new_path = path.get_copy()
                            new_path.travel(edge)
                            new_path_list.append(new_path)
                            if edge.node_to == self.node_to:
                                self.has_arrived = True
            self.path_list = new_path_list

        if self.has_arrived:
            self.remove_unarrived_pathes()
            self.path_list.sort(key=lambda x: x.cost)
        else:
            self.build_routes_to_target()

    def remove_unarrived_pathes(self):
        for path in self.path_list:
            if path.last_node() != self.node_to:
                self.path_list.remove(path)


class Path:
    def __init__(self):
        self.node_traveled_list: list[Node] = list()
        self.step_list: list[str] = list()
        self.cost: int = 0

    def last_node(self) -> Node:
        return self.node_traveled_list[-1]

    def add_start(self, node: Node) -> None:
        self.node_traveled_list.append(node)

    def travel(self, edge: Edge) -> None:
        self.add_step(edge.node_to, edge.cost)

    def add_step(self, node: Node, cost: int) -> None:
        self.node_traveled_list.append(node)
        self.step_list.append(
            f"{self.node_traveled_list[-2].name}>{self.last_node().name}"
        )
        self.cost += cost

    def get_copy(self) -> "Path":
        new_path: Path = Path()
        new_path.node_traveled_list = copy(self.node_traveled_list)
        new_path.step_list = copy(self.step_list)
        new_path.cost = self.cost
        return new_path

    def __str__(self):
        return f"{', '.join(self.step_list)}, cost: {self.cost}"
