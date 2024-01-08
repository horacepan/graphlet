from typing import Optional
import networkx as nx
from abc import ABC, abstractmethod
from cache import Cache


class Node(ABC):
    def __init__(self):
        self._graph: Optional[nx.DiGraph] = None

    def should_run(self, cache: Cache) -> bool:
        if not self.outputs():
            # node does not generate any artifacts, so it can always run
            return True

        # check that the node's outputs are not already in the cache
        return not all(output in cache for output in self.outputs())

    @abstractmethod
    def outputs(self) -> list[str]:
        pass

    @abstractmethod
    def execute(self, cache: Cache):
        pass

    def describe(self, cache: Cache):
        status = "uncached" if self.should_run(cache) else "cached"
        return (
            f"{self.__class__.__name__}({status})[outputs: {', '.join(self.outputs())}]"
        )

    def after(self, *parents: "Node") -> "Node":
        for parent in parents:
            # add edge from pnode to node
            self.graph.add_edge(parent, self)
        return self


if __name__ == "__main__":

    class Sample(Node):
        def outputs(self):
            return ["data1", "data2"]

        def execute(self, cache: Cache):
            cache["data1"] = [1, 2, 3]
            cache["data2"] = [4, 5]

    node = Sample()
    print(node.describe())
