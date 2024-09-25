import os
import datetime
import pickle
import functools
from enum import Enum

class ChangeType(Enum):
    """
    Enum representing the type of changes that can occur in a file or directory:
    - CREATED: File/Directory was created
    - DELETED: File/Directory was deleted
    - MODIFIED: File/Directory was modified
    """
    CREATED = 1
    DELETED = 2
    MODIFIED = 3


class Node:
    """
    A Node represents a file or directory in the filesystem.
    
    Attributes:
    - last_changed (int): Last modification time (timestamp).
    - name (str): Name or relative path of the file or directory.
    - is_dir (bool): Indicates if this node is a directory.
    - nodes (list[Node]): List of child nodes (used if this node is a directory).
    """
    def __init__(self, last_changed: int, name: str, is_dir: bool = False):
        self.nodes: list[Node] = []  # Stores child nodes if directory
        self.last_changed: int = last_changed  # Last modified time
        self.name: str = name  # Name of the file/directory
        self.is_dir: bool = is_dir  # True if this is a directory

    def add(self, new: "Node"):
        """
        Adds a new node (file or directory) to the tree structure. Recursively
        finds the correct place in the tree to insert this node.
        
        Args:
        - new (Node): Node representing a new file or directory.
        """
        new.name = new.name.removeprefix(self.name + "/")
        parts = new.name.split("/")

        if len(parts) > 1:
            for node in self.nodes:
                if not node.is_dir:
                    continue
                if node.name == parts[0]:
                    new.name = "/".join(parts[1:])
                    node.add(new)
                    return

        node = Node(new.last_changed, parts[0], new.is_dir)
        self.nodes.append(node)
        if len(parts) == 1:
            print(f"Added node: {node.name} at {self.name}")
            return

        new.name = "/".join(parts[1:])
        node.add(new)
    
    def all(self) -> list["Node"]:
        """
        Recursively returns all nodes (files and directories) under the current node.
        
        Returns:
        - list[Node]: List of all child nodes.
        """
        nodes = [node for sublist in self.nodes for node in sublist.all()]
        nodes.extend(self.nodes)
        return nodes

    def get(self, name: str) -> type["Node"] | None:
        """
        Searches for a node by name in the current directory tree.
        
        Args:
        - name (str): The name or path of the node to search for.
        
        Returns:
        - Node or None: Returns the node if found, otherwise None.
        """
        for node in self.nodes:
            name_split = name.split("/")
            if node.name.split("/")[0] == name_split[0]:
                if len(name_split) == 1:
                    return node
                else:
                    return node.get("/".join(name_split[1:]))
        return None

    def path_to(self, new: type["Node"]) -> str | None:
        """
        Recursively finds and returns the path to a specific node.
        
        Args:
        - new (Node): The node to find the path for.
        
        Returns:
        - str or None: The path to the node, or None if not found.
        """
        for node in self.nodes:
            if node == new:
                return node.name

            if node.is_dir:
                path = node.path_to(new)
                print(f"{node.name} at {path}")
                if path:
                    return node.name + "/" + path
        return None


class Change:
    """
    Represents a change in the file system.
    
    Attributes:
    - change_type (ChangeType): Type of change (CREATED, DELETED, MODIFIED).
    - node (Node): The file or directory node that was changed.
    - data (bytes): File data (for modified or created files).
    """
    def __init__(self, change_type: int, node: Node, data: bytes | None = None):
        self.change_type = change_type  # Type of change
        self.node = node  # Node that was changed
        self.data = data  # File data (only for files, not directories)


class Tree:
    """
    Represents the tree structure of a directory (with its files and subdirectories).
    
    Attributes:
    - root (Node): The root node of the directory tree.
    """
    def __init__(self, folder_dir: str):
        self.root = Node(os.path.getmtime(folder_dir), os.path.basename(folder_dir), True)  # Root directory
        self.load(folder_dir)  # Load all files and directories into the tree

    def load(self, folder_dir: str):
        """
        Loads the directory structure into the tree by walking through the filesystem.
        
        Args:
        - folder_dir (str): Path to the root directory.
        """
        for a, dirs, files in os.walk(folder_dir):
            for dir in dirs:
                path = os.path.join(a, dir)
                self.root.add(Node(os.path.getmtime(path), path, True))  # Add directories

            for file in files:
                path = os.path.join(a, file)
                self.root.add(Node(os.path.getmtime(path), path))  # Add files

    def diffs(self, old_tree: type["Tree"] | None) -> list[Change]:
        """
        Compares the current tree with an old tree and detects changes.
        
        Args:
        - old_tree (Tree or None): The previous state of the tree.
        
        Returns:
        - list[Change]: List of changes between the two trees.
        """
        changes = []
        for i, node in enumerate(self.root.all()):
            path = self.root.path_to(node)
            try:
                found: Node | None = old_tree.root.get(path)
            except:
                found = None

            if not found:
                full_path = os.path.join(self.root.name, path)
                print(f"Creating file {full_path}")
                if os.path.isfile(full_path):
                    with open(full_path, "rb") as file:
                        data = file.read()
                    changes.append(Change(ChangeType.CREATED, node, data=data))
                elif os.path.isdir(full_path):
                    changes.append(Change(ChangeType.CREATED, node))
                else:
                    with open(full_path, "rb") as file:
                        data = file.read()
                    changes.append(Change(ChangeType.CREATED, node, data=data))

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
    """
    Manages backups by creating snapshots of the filesystem and tracking changes.
    
    Attributes:
    - tree (Tree): Current state of the directory tree.
    - changes (list[Change]): List of changes since the last backup.
    """
    def __init__(self, folder_dir: str, old: Tree | None = None):
        new = Tree(folder_dir)
        changes = new.diffs(old)

        self.tree: Tree = new
        self.changes = changes

    def dump(self) -> str:
        """
        Dumps the backup data to a file using pickle.
        
        Returns:
        - str: The filename of the dumped backup.
        """
        time = str(datetime.datetime.now().strftime("%Y%m%d%H%M%S"))
        with open(time, 'wb') as file:
            pickle.dump(self, file)
        return time

    @staticmethod
    def load_from_file(file: str, old: Tree | None = None):
        """
        Loads a backup from a file and optionally compares it with an old tree.
        
        Args:
        - file (str): Path to the backup file.
        - old (Tree or None): Optional old tree to compare with.
        
        Returns:
        - Backup: Loaded backup with changes calculated.
        """
        with open(file, 'rb') as file:
            backup = pickle.load(file)

        if old is not None:
            changes = backup.tree.diffs(old)
            backup.changes = changes
        return backup

    def restore(self, destination: str):
        """
        Restores the backup to a destination directory.
        
        Args:
        - destination (str): Path to the directory where the backup will be restored.
        """
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
                os.makedirs(os.path.dirname(os.path.join(destination, path)), exist_ok=True)
                if change.node.is_dir:
                    continue

                with open(os.path.join(destination, path), "wb") as file:
                    file.write(change.data)
            elif change.change_type == ChangeType.MODIFIED:
                os.makedirs(os.path.dirname(os.path.join(destination, path)), exist_ok=True)
                if change.node.is_dir:
                    continue

                with open(os.path.join(destination, path), "wb") as file:
                    file.write(change.data)
            elif change.change_type == ChangeType.DELETED:
                print(destination)
                print(path)
                os.remove(os.path.join(destination, path))

class Restorer:
    """
    Restores a series of backups in chronological order. It manages multiple backup files,
    loading them, and then applying the changes to a destination directory.

    Attributes:
    - files (list[str]): List of file paths to the backup files.
    - backups (list[Backup]): Loaded Backup objects sorted by timestamp.
    """
    def __init__(self, files: list[str]):
        """
        Initializes the Restorer with a list of backup files. Ensures that each file exists,
        and then loads and sorts the backups based on the timestamp in the filenames.
        
        Args:
        - files (list[str]): List of backup file paths.

        Raises:
        - FileNotFoundError: If any file in the list does not exist.
        """
        self.files = files  # List of backup file paths

        # Ensure that all files exist
        for file in files:
            if not os.path.exists(file):
                raise FileNotFoundError(f"File {file} not found")

        # Sort the files based on their timestamp extracted from the filename
        self.files.sort(key=self.extract_datetime_from_filename)
        
        # Load the backups from each file
        self.backups = [Backup.load_from_file(file) for file in files]

    def extract_datetime_from_filename(self, filename: str) -> int:
        """
        Extracts the timestamp from the filename. Assumes that the filename is structured
        as "YYYYMMDDHHMMSS" and uses this to determine the order in which backups should
        be restored.

        Args:
        - filename (str): The name of the backup file.

        Returns:
        - int: The integer representation of the timestamp (e.g., "20230915083000").
        """
        basename = os.path.basename(filename)  # Extract the file's basename
        datetime_str = basename.split('.')[0]  # Extract the timestamp from the filename
        return int(datetime_str)  # Return the timestamp as an integer

    def restore(self, destination: str):
        """
        Restores all loaded backups to the destination directory. The backups are applied
        in chronological order, meaning earlier backups are applied first, followed by
        more recent ones.

        Args:
        - destination (str): The directory where the backup will be restored.
        """
        # Apply each backup in chronological order
        for backup in self.backups:
            backup.restore(destination)

