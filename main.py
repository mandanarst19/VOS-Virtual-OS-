import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def check_modules():
    required = ["filesystem", "cli", "cpu_scheduler", "memory_manager", "disk_scheduler"]
    missing = []
    for module in required:
        try:
            __import__(module)
        except ImportError:
            missing.append(module + ".py")

    if missing:
        print("Error: The following modules were not found:")
        for m in missing:
            print(f"  - {m}")
        print("\nPlease ensure all files are in the same directory and try again.")
        return False
    return True


def run_demo_mode():
    from cpu_scheduler import CPUScheduler, Process
    from memory_manager import MemoryManager
    from disk_scheduler import DiskScheduler

    print("\n" + "╔" + "═"*55 + "╗")
    print("║" + "Mini OS - Full Demo Mode".center(55) + "║")
    print("╚" + "═"*55 + "╝")

    print("\n" + "█"*57)
    print("█" + "Part 1: CPU Scheduler - Round Robin".center(55) + "█")
    print("█"*57)
    
    processes = [
        Process("P1", arrival=0, burst=8),
        Process("P2", arrival=1, burst=4),
        Process("P3", arrival=2, burst=9),
        Process("P4", arrival=3, burst=5),
    ]
    scheduler = CPUScheduler(quantum=3)
    scheduler.round_robin(processes)

    input("\n[Enter] to continue to Memory Management...")

    print("\n" + "█"*57)
    print("█" + "Part 2: Memory Manager - First Fit".center(55) + "█")
    print("█"*57)
    
    mm = MemoryManager(total_size=256)
    mm.demo()

    input("\n[Enter] to continue to Disk Management...")

    print("\n" + "█"*57)
    print("█" + "Part 3: Disk Scheduler - SSTF".center(55) + "█")
    print("█"*57)
    
    ds = DiskScheduler(head_position=50, max_track=199)
    ds.demo()

    print("\n" + "═"*57)
    print("Demo completed successfully!")
    print("To run the interactive CLI, use:")
    print("python main.py --cli")
    print("═"*57 + "\n")


def run_cli_mode():
    from cli import CLI
    cli = CLI()
    cli.run()


def print_usage():
    print("""
╔══════════════════════════════════════════════╗
║           Mini OS - Usage Guide              ║
╠══════════════════════════════════════════════╣
║                                              ║
║  python main.py          Interactive CLI     ║
║  python main.py --cli    Interactive CLI     ║
║  python main.py --demo   Run algorithm demos ║
║  python main.py --help   Show this help      ║
║                                              ║
╚══════════════════════════════════════════════╝
""")


def main():
    if not check_modules():
        sys.exit(1)

    args = sys.argv[1:]

    if not args or "--cli" in args:
        run_cli_mode()
    elif "--demo" in args:
        run_demo_mode()
    elif "--help" in args or "-h" in args:
        print_usage()
    else:
        print(f"Unknown argument: {args[0]}")
        print_usage()
        sys.exit(1)


if __name__ == "__main__":
    main()
