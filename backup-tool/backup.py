import os


class Node:
    def __init__(self, last_changed: int, name: str, is_dir: bool = False, content: str | None = None):
        self.nodes: list[Node] = [] 

        self.last_changed: int = last_changed
        self.name: str = name
        self.is_dir: bool = is_dir

        self.file_content: str | None = content


class Backup:
    def __init__(self):
        self.root = None

    def backup(self, folder_dir: str):
        self.root = Node(os.path.getmtime(folder_dir), os.path.basename(folder_dir), True)

        def parse_dir(folder_dir: str, depth: Node):
            for a, dirs, files in os.walk(folder_dir):
                for file in files:
                    path = os.path.join(a, file)
                    depth.nodes.append(Node(os.path.getmtime(path), file, content=open(path, "r").read()))
                
                for dir in dirs:
                    path = os.path.join(a, dir)
                    root = Node(os.path.getmtime(path), path, True)
                    depth.nodes.append(root)
                    parse_dir(path, root)
                break

        parse_dir(folder_dir, self.root)

    def load(file: str):
        pass

    def dump(self):
        pass