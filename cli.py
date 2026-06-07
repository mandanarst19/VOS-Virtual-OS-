from filesystem import VirtualFileSystem
import platform
import datetime

BANNER = """
======================================================
               Mini OS - Command Line
======================================================
Type 'help' to see available commands.
"""

HELP_TEXT = """
--- Directory Management ---
mkdir <name>           Create directory
rmdir <name>           Remove empty directory
cd <name>              Change directory (use .. for up, / for root)
ls                     List contents
ls -l                  List contents with details
pwd                    Print working directory
tree                   Show directory tree

--- File Management ---
touch <name>           Create file / update timestamp
rm <name>              Remove file
rename <old> <new>     Rename file or directory
write <name> <text>    Write text to file
cat <name>             Show file content

--- System ---
cpu                    Run CPU Scheduler simulation
mem                    Run Memory Manager simulation
disk                   Run Disk Scheduler simulation
sysinfo                Show system info
clear                  Clear screen
help                   Show this help message
exit                   Exit Mini OS
"""

class CLI:
    def __init__(self):
        self.fs = VirtualFileSystem()
        self.running = True
        self._setup_sample_structure()

    def _setup_sample_structure(self):
        self.fs.mkdir("home")
        self.fs.cd("home")
        self.fs.mkdir("user")
        self.fs.touch("readme.txt", "Welcome to Mini OS!")
        self.fs.cd("user")
        self.fs.mkdir("documents")
        self.fs.mkdir("downloads")
        self.fs.touch("notes.txt", "This is a note file.")
        self.fs.cd("..")
        self.fs.cd("..")

    def get_prompt(self):
        path = self.fs.get_current_path_str()
        return f"\nMiniOS:{path}> "

    def parse_command(self, raw_input):
        raw_input = raw_input.strip()
        if not raw_input:
            return None, [], ""

        parts = raw_input.split(maxsplit=1)
        command = parts[0].lower()
        args_str = parts[1] if len(parts) > 1 else ""
        args = args_str.split() if args_str else []

        return command, args, args_str

    def execute(self, command, args, args_str):
        if command == "mkdir":
            if not args:
                return "Usage: mkdir <name>"
            return self.fs.mkdir(args[0])

        elif command == "rmdir":
            if not args:
                return "Usage: rmdir <name>"
            return self.fs.rmdir(args[0])

        elif command == "cd":
            if not args:
                return self.fs.pwd()
            return self.fs.cd(args[0])

        elif command == "ls":
            show_details = "-l" in args
            return self.fs.ls(show_details)

        elif command == "pwd":
            return self.fs.pwd()

        elif command == "tree":
            return self.fs.tree()

        elif command == "touch":
            if not args:
                return "Usage: touch <name>"
            return self.fs.touch(args[0])

        elif command == "rm":
            if not args:
                return "Usage: rm <name>"
            return self.fs.rm(args[0])

        elif command == "rename":
            if len(args) < 2:
                return "Usage: rename <old_name> <new_name>"
            return self.fs.rename(args[0], args[1])

        elif command == "write":
            if len(args) < 2:
                return "Usage: write <name> <content>"
            filename = args[0]
            content = " ".join(args[1:])
            return self.fs.write(filename, content)

        elif command == "cat":
            if not args:
                return "Usage: cat <name>"
            return self.fs.cat(args[0])

        elif command == "cpu":
            return self._run_cpu()

        elif command == "mem":
            return self._run_memory()

        elif command == "disk":
            return self._run_disk()

        elif command == "sysinfo":
            return self._sysinfo()

        elif command == "clear":
            print("\033[2J\033[H", end="")
            print(BANNER)
            return ""

        elif command == "help":
            return HELP_TEXT

        elif command in ("exit", "quit", "bye"):
            self.running = False
            return "Exiting Mini OS. Goodbye!"

        else:
            return f"Command not found: '{command}'. Type 'help' for available commands."

    def _run_cpu(self):
        try:
            from cpu_scheduler import CPUScheduler, Process
            print("\n" + "="*50)
            print("  CPU Scheduler Simulation - Round Robin")
            print("="*50)
            processes = [
                Process("P1", arrival=0, burst=8),
                Process("P2", arrival=1, burst=4),
                Process("P3", arrival=2, burst=9),
                Process("P4", arrival=3, burst=5),
            ]
            scheduler = CPUScheduler(quantum=3)
            scheduler.round_robin(processes)
            return ""
        except ImportError:
            return "Error: cpu_scheduler.py not found."

    def _run_memory(self):
        try:
            from memory_manager import MemoryManager
            print("\n" + "="*50)
            print("  Memory Manager Simulation - First Fit")
            print("="*50)
            mm = MemoryManager(total_size=256)
            mm.demo()
            return ""
        except ImportError:
            return "Error: memory_manager.py not found."

    def _run_disk(self):
        try:
            from disk_scheduler import DiskScheduler
            print("\n" + "="*50)
            print("  Disk Scheduler Simulation - SSTF")
            print("="*50)
            ds = DiskScheduler(head_position=50)
            ds.demo()
            return ""
        except ImportError:
            return "Error: disk_scheduler.py not found."

    def _sysinfo(self):
        info = f"""
======================================
           System Info
======================================
  OS Version     : Mini OS v1.0
  Language       : Python 3
  Platform       : {platform.system():<22}
  Time           : {datetime.datetime.now().strftime('%Y-%m-%d %H:%M'):<22}
--------------------------------------
  CPU Scheduler  : Round Robin
  Memory Manager : First Fit
  Disk Scheduler : SSTF
======================================
"""
        return info

    def run(self):
        print(BANNER)
        while self.running:
            try:
                raw_input = input(self.get_prompt())
                result = self.parse_command(raw_input)

                if result is None or not result[0]:
                    continue

                command, args, args_str = result
                output = self.execute(command, args, args_str)

                if output:
                    print(output)

            except KeyboardInterrupt:
                print("\nType 'exit' to quit.")
            except EOFError:
                print("\nGoodbye!")
                break
            except Exception as e:
                print(f"\nSystem Error: {e}")
