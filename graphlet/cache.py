import os
import shutil
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
        # os.makedirs(filepath, exist_ok=True) # TODO: fix, only make the parent
        with open(filepath, "wb") as file:
            pickle.dump(item, file)


class PickleDeserializer(Deserializer):
    def __init__(self, parent_dir: str):
        self.parent_dir = parent_dir

    def deserialize(self, key: str) -> Any:
        filepath = os.path.join(self.parent_dir, key)
        if not os.path.exists(filepath):
            return None
        with open(filepath, "rb") as file:
            return pickle.load(file)


class Cache:
    def __init__(self, name: str, parent_dir: str = None, fetch_keys: bool = False):
        if parent_dir is None:
            prefix = os.path.join(".cache", name)
        elif parent_dir == "":
            prefix = os.path.join(name)
        else:
            prefix = os.path.join(parent_dir, name)

        self._prefix = prefix
        self.serializer = PickleSerializer(prefix)
        self.deserializer = PickleDeserializer(prefix)
        self.cache = {}
        self.keys = set()

        if fetch_keys:
            self.keys = self.fetch_keys()

    def fetch_keys(self) -> set[str]:
        keys = set()

        # Recursive function to fetch keys
        def traverse(directory, prefix=""):
            for name in os.listdir(directory):
                path = os.path.join(directory, name)
                if os.path.isfile(path):
                    keys.add(os.path.join(prefix, name))
                elif os.path.isdir(path):
                    traverse(path, os.path.join(prefix, name))

        traverse(self._prefix)
        return keys

    @property
    def prefix(self):
        return self._prefix

    def __getitem__(self, key: str) -> Any:
        if key in self.cache:
            return self.cache[key]

        return self.deserializer.deserialize(key)

    def __setitem__(self, key: str, value: Any):
        self.serializer.serialize(key, value)
        self.cache[key] = value
        self.keys.add(key)

    def __contains__(self, key: str):
        return key in self.keys

    def clear(self):
        self.keys.clear()
        self.cache.clear()
        shutil.rmtree(self._prefix)
        # remove everything from fs


if __name__ == "__main__":
    cache = Cache("test", fetch_keys=True)
    cache["a"] = 3
    cache["b"] = 5
    print(f"keys: {cache.keys}")
