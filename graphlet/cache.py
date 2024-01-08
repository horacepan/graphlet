import pandas as pd
import os
from typing import Any
import pickle
from abc import ABC, abstractmethod


class Serializer(ABC):
    @abstractmethod
    def serialize(self, item: Any):
        pass

class Deserializer:
    @abstractmethod
    def deserialize(self, item):
        pass

class PickleSerializer(Serializer):
    def __init__(self, parent_dir: str):
        self.parent_dir = parent_dir
        if not os.path.exists(parent_dir):
            os.makedirs(parent_dir)

    def serialize(self, key: str, item: Any):
        filepath = os.path.join(self.parent_dir, key)
        with open(filepath, 'wb') as file:
            pickle.dump(item, file)

class PickleDeserializer(Deserializer):
    def __init__(self, parent_dir: str):
        self.parent_dir = parent_dir

    def deserialize(self, key: str) -> Any:
        filepath = os.path.join(self.parent_dir, key)
        if not os.path.exists(filepath):
            return None
        with open(filepath, 'rb') as file:
            return pickle.load(file)

class SimpleCache:
    def __init__(self, name: str, parent_dir: str = None):
        if parent_dir is None:
            full_dir = os.path.join(".cache", name)
        elif parent_dir == "":
            full_dir = os.path.join(name)
        else:
            full_dir = os.path.join(parent_dir, name)

        self.serializer = PickleSerializer(name)
        self.deserializer = PickleDeserializer(name)
        self._cache = {}

    def __getitem__(self, key: str) -> Any:
        if key in self._cache:
            return self._cache[key]

        return self.deserializer.deserialize(key)

    def __setitem__(self, key: str, value: Any):
        self.serializer.serialize(key, value)

if __name__ == "__main__":
    df = pd.DataFrame({"a": [10, 20]})
    cache = SimpleCache("test")
