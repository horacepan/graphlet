import networkx as nx
from node import Node
from cache import Cache


class Graph:
    def __init__(self):
        self.graph = nx.DiGraph()
        self.nodes = []

    def add(self, node: Node) -> Node:
        self.nodes.append(node)
        node.graph = self.graph
        return node

    def execute(self, cache: Cache):
        # iterate over nodes in topological order
        for node in nx.topological_sort(self.graph):
            if node.should_run(cache):
                node.execute(cache)

    def describe(self, cache: Cache):
        for node in nx.topological_sort(self.graph):
            print(f"- {node.describe(cache)}")


if __name__ == "__main__":

    class GetData1(Node):
        def outputs(self):
            return ["data1"]

        def execute(self, cache: Cache):
            cache["data1"] = [1, 2, 3]

    class GetData2(Node):
        def outputs(self):
            return ["data2"]

        def execute(self, cache: Cache):
            cache["data2"] = [1, 2, 3]

    class SumData(Node):
        def outputs(self):
            return ["sum"]

        def execute(self, cache: Cache):
            res = sum(x for x in (cache["data1"] + cache["data2"]))
            cache["sum"] = res
            breakpoint()

    cache = Cache("test_data")
    g = Graph()
    n1 = g.add(GetData1())
    n2 = g.add(GetData2())
    n3 = g.add(SumData()).after(n1, n2)
    g.describe()
    g.execute(cache)
