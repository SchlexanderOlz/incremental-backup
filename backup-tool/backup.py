import os
import datetime
import pickle
import functools
from enum import Enum

class ChangeType(Enum):
    CREATED = 1
    DELETED = 2
    MODIFIED = 3


class Node:
    def __init__(self, last_changed: int, name: str, is_dir: bool = False):
        self.nodes: list[Node] = []

        self.last_changed: int = last_changed
        self.name: str = name
        self.is_dir: bool = is_dir

    def add(self, new: "Node"):
        new.name = new.name.removeprefix(self.name + "/")
        parts = new.name.split("/")

        if len(parts) > 1:
            for node in self.nodes:
                if not node.is_dir: continue
                if node.name == parts[0]:
                    new.name = "/".join(parts[1:])
                    node.add(new)
                    return

        node = Node(new.last_changed, parts[0], new.is_dir)
        self.nodes.append(node)
        if len(parts) == 1:
            print("Added node: {} at {}".format(node.name, self.name))
            return

        new.name = "/".join(parts[1:])
        node.add(new)
    
    def all(self) -> list["Node"]:
        nodes = [node for sublist in self.nodes for node in sublist.all()]
        nodes.extend(self.nodes)
        return nodes

    def get(self, name: str) -> type["Node"] | None:
        for node in self.nodes:
            name_split = name.split("/")
            if node.name.split("/")[0] == name_split[0]:
                if len(name_split) == 1:
                    return node
                else:
                    return node.get("/".join(name_split[1:]))
        return None

    def path_to(self, new: type["Node"]) -> str | None:
        for node in self.nodes:
            if node == new:
                return node.name

            if node.is_dir:
                path = node.path_to(new)
                if path:
                    return self.name + "/" + path
        return None


class Change:
    def __init__(self, change_type: int, node: Node, data: bytes | None = None):
        self.change_type = change_type
        self.node = node
        self.data = data


class Tree:
    def __init__(self, folder_dir: str):
        self.root = Node(os.path.getmtime(folder_dir), os.path.basename(folder_dir), True)
        self.load(folder_dir)

    def load(self, folder_dir: str):
        for a, dirs, files in os.walk(folder_dir):
            for dir in dirs:
                path = os.path.join(a, dir)

                self.root.add(Node(os.path.getmtime(path), path, True))

            for file in files:
                path = os.path.join(a, file)
                self.root.add(Node(os.path.getmtime(path), path))


    def diffs(self, old_tree: type["Tree"] | None) -> list[Change]:
        changes = []
        for i, node in enumerate(self.root.all()):
            path = self.root.path_to(node)
            try:
                found: Node | None = old_tree.root.get(path)
            except:
                found = None

            if not found:
                full_path = os.path.join(self.root.name, path)
                print("Creating file " + full_path)
                if os.path.isfile(full_path):
                    with open(full_path, "rb") as file:
                        data = file.read()
                    changes.append(Change(ChangeType.CREATED, node, data=data))
                    print(f"File {path} has been created")
                elif os.path.isdir(full_path):
                    changes.append(Change(ChangeType.CREATED, node))
                    print(f"Directory {path} has been created")

        if old_tree is None:
            return changes
        for _, old in enumerate(old_tree.root.all(), start=i):
            path = old_tree.root.path_to(old)
            found: Node | None = self.root.get(path)
            if not found:
                changes.append(Change(ChangeType.DELETED, old))
                print(f"File {path} has been deleted")
                continue

            if found.last_changed != old.last_changed:
                if found.is_dir:
                    data = None
                else:
                    with open(os.path.join(self.root.name, path), "rb") as file:
                        data = file.read()
                changes.append(Change(ChangeType.MODIFIED, found, data=data))
                print(f"File {path} has been changed")
        return changes


class Backup:
    def __init__(self, folder_dir: str, old: Tree | None = None):
        new = Tree(folder_dir)
        changes = new.diffs(old)

        self.tree: Tree = new
        self.changes = changes

    def dump(self) -> str:
        time = str(datetime.datetime.now().strftime("%Y%m%d%H%M%S"))
        with open(time, 'wb') as file:
            pickle.dump(self, file)
        return time

    @staticmethod
    def load_from_file(file: str, old: Tree | None = None):
        with open(file, 'rb') as file:
            backup = pickle.load(file)

        if old is not None:
            changes = backup.tree.diffs(old)
            backup.changes = changes
        return backup

    def restore(self, destination: str):
        for change in self.changes:
            print(change.node.name)
            print(change.node.is_dir)
            print(change.node.last_changed)
            print(change.change_type)
            print("-----")
        for change in self.changes:
            print(change.node.name)
            path = self.tree.root.path_to(change.node)
            if change.change_type == ChangeType.CREATED:
                if change.node.is_dir:
                    os.makedirs(os.path.join(destination, path), exist_ok=True)
                    continue

                with open(os.path.join(destination, path), "wb") as file:
                    file.write(change.data)
            elif change.change_type == ChangeType.MODIFIED:
                if change.node.is_dir:
                    os.makedirs(os.path.join(destination, path), exist_ok=True)
                    continue

                with open(os.path.join(destination, path), "wb") as file:
                    file.write(change.data)
            elif change.change_type == ChangeType.DELETED:
                print(destination)
                print(path)
                os.remove(os.path.join(destination, path))

class Restorer:
    def __init__(self, files: list[str]):
        self.files = files

        for file in files:
            if not os.path.exists(file):
                raise FileNotFoundError(f"File {file} not found")

        self.files.sort(key=self.extract_datetime_from_filename)
        self.backups = [Backup.load_from_file(file) for file in files]

    def extract_datetime_from_filename(self, filename: str) -> datetime:
        basename = os.path.basename(filename)
        datetime_str = basename.split('.')[0]
        return int(datetime_str)

    def restore(self, destination: str):
        for backup in self.backups:
            backup.restore(destination)
