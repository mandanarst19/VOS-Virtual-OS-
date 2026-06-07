import time

class FileNode:
    def __init__(self, name, is_dir=False, content=""):
        self.name = name
        self.is_dir = is_dir
        self.content = content
        self.children = {}
        self.created_at = time.strftime("%Y-%m-%d %H:%M:%S")
        self.modified_at = self.created_at
        self.size = len(content)

    def __repr__(self):
        return f"[{'DIR' if self.is_dir else 'FILE'}] {self.name}"

class VirtualFileSystem:
    def __init__(self):
        self.root = FileNode("/", is_dir=True)
        self.current_node = self.root
        self.current_path = ["/"]

    def get_current_path_str(self):
        if len(self.current_path) == 1:
            return "/"
        return "/" + "/".join(self.current_path[1:])

    def _find_node(self, name):
        return self.current_node.children.get(name)

    def mkdir(self, name):
        if not name:
            return "Error: Directory name required."
        if name in self.current_node.children:
            return f"Error: '{name}' already exists."
        if "/" in name:
            return "Error: Name cannot contain '/'."

        self.current_node.children[name] = FileNode(name, is_dir=True)
        return f"Directory '{name}' created."

    def rmdir(self, name):
        node = self._find_node(name)
        if not node:
            return f"Error: '{name}' not found."
        if not node.is_dir:
            return f"Error: '{name}' is a file."
        if node.children:
            return f"Error: Directory '{name}' is not empty."

        del self.current_node.children[name]
        return f"Directory '{name}' removed."

    def cd(self, name):
        if name == "..":
            if len(self.current_path) == 1:
                return "Error: Already at root."
            self.current_path.pop()
            self.current_node = self.root
            for part in self.current_path[1:]:
                self.current_node = self.current_node.children[part]
            return self.get_current_path_str()

        if name == "/":
            self.current_path = ["/"]
            self.current_node = self.root
            return "/"

        node = self._find_node(name)
        if not node:
            return f"Error: '{name}' not found."
        if not node.is_dir:
            return f"Error: '{name}' is a file."

        self.current_node = node
        self.current_path.append(name)
        return self.get_current_path_str()

    def ls(self, show_details=False):
        children = self.current_node.children
        if not children:
            return "Empty directory."

        lines = [f"Contents of {self.get_current_path_str()}:"]
        dirs = [n for n in children.values() if n.is_dir]
        files = [n for n in children.values() if not n.is_dir]

        for node in sorted(dirs, key=lambda x: x.name):
            if show_details:
                lines.append(f"  {node.name:<20} [DIR]   {node.created_at}")
            else:
                lines.append(f"  {node.name}/")

        for node in sorted(files, key=lambda x: x.name):
            if show_details:
                lines.append(f"  {node.name:<20} {node.size:>6} bytes   {node.modified_at}")
            else:
                lines.append(f"  {node.name}")

        lines.append(f"\nTotal: {len(dirs)} dirs, {len(files)} files")
        return "\n".join(lines)

    def pwd(self):
        return self.get_current_path_str()

    def touch(self, name, content=""):
        if not name:
            return "Error: File name required."
        if name in self.current_node.children:
            self.current_node.children[name].modified_at = time.strftime("%Y-%m-%d %H:%M:%S")
            return f"Updated timestamp for '{name}'."
        if "/" in name:
            return "Error: Name cannot contain '/'."

        self.current_node.children[name] = FileNode(name, is_dir=False, content=content)
        return f"File '{name}' created."

    def rm(self, name):
        node = self._find_node(name)
        if not node:
            return f"Error: '{name}' not found."
        if node.is_dir:
            return f"Error: '{name}' is a directory."

        del self.current_node.children[name]
        return f"File '{name}' removed."

    def rename(self, old_name, new_name):
        if not old_name or not new_name:
            return "Error: Names required."
        node = self._find_node(old_name)
        if not node:
            return f"Error: '{old_name}' not found."
        if new_name in self.current_node.children:
            return f"Error: '{new_name}' already exists."

        node.name = new_name
        self.current_node.children[new_name] = node
        del self.current_node.children[old_name]
        return f"Renamed '{old_name}' to '{new_name}'."

    def write(self, name, content):
        node = self._find_node(name)
        if not node:
            return f"Error: '{name}' not found."
        if node.is_dir:
            return f"Error: '{name}' is a directory."

        node.content = content
        node.size = len(content)
        node.modified_at = time.strftime("%Y-%m-%d %H:%M:%S")
        return f"Written {node.size} bytes to '{name}'."

    def cat(self, name):
        node = self._find_node(name)
        if not node:
            return f"Error: '{name}' not found."
        if node.is_dir:
            return f"Error: '{name}' is a directory."
        if not node.content:
            return "Empty file."

        return f"--- {name} ---\n{node.content}\n----------------"

    def tree(self, node=None, prefix="", is_last=True, first_call=True):
        if first_call:
            node = self.current_node
            lines = [self.get_current_path_str()]
            children = list(node.children.values())
            for i, child in enumerate(sorted(children, key=lambda x: (not x.is_dir, x.name))):
                lines.append(self.tree(child, prefix="", is_last=(i == len(children) - 1), first_call=False))
            return "\n".join(lines)
        
        connector = "`-- " if is_last else "|-- "
        line = f"{prefix}{connector}{node.name}"

        if node.is_dir:
            children = list(node.children.values())
            child_lines = [line]
            new_prefix = prefix + ("    " if is_last else "|   ")
            for i, child in enumerate(sorted(children, key=lambda x: (not x.is_dir, x.name))):
                child_lines.append(
                    self.tree(child, new_prefix, is_last=(i == len(children) - 1), first_call=False)
                )
            return "\n".join(child_lines)
        return line
