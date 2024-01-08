# Graphlet
![Graphlet Logo](assets/graphlet_logo.png)
Graphlet is a lightweight, Python library for defining computations in a graph-structured framework. It enables users to define workflows as a series of nodes, each representing a discrete computational task. Graphlet optimizes the development loop by skipping redundant computations, making it ideal for data processing and task automation in diverse applications.

## Installation
1) First, clone the graphlet repository to your local machine:
```
git clone https://github.com/yourusername/graphlet.git
cd graphlet
```

2) Setup a virtual environment
```
python3 -m venv venv
source venv/bin/activate
```

3) Install the package
```
pip install -r requirements.txt
pip install .
```

## Sample Usage
```
import numpy as np
from graphlet.graph import Graph
from graphlet.node import Node
from graphlet.cache import Cache


class Data(Node):
    def __init__(self, n: int):
        self.n = n

    def outputs(self) -> list[str]:
        return ["data"]

    def execute(self, cache: Cache):
        data = np.arange(self.n)
        cache["data"] = data


class Square(Node):
    def outputs(self) -> list[str]:
        return ["squared"]

    def execute(self, cache: Cache):
        data = cache["data"]
        squared = np.square(data)
        cache["squared"] = squared


class Aggregate(Node):
    def outputs(self) -> list[str]:
        return ["agg"]

    def execute(self, cache: Cache):
        agg = cache["squared"].sum()
        cache["agg"] = agg


cache = Cache("sample")
g = Graph()
fetch = g.add(Data(3))
square = g.add(Square()).after(fetch)
g.add(Aggregate()).after(square)
g.execute(cache)

# inspect contents of the cache
for k, v in cache.cache.items():
    print(f"{k}: {v}")
```
