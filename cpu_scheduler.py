"""
cpu_scheduler.py - CPU Management for Mini OS
Algorithm: Round Robin with Time Quantum
"""

from collections import deque


class Process:
    def __init__(self, pid, arrival, burst, priority=0):
        self.pid = pid
        self.arrival = arrival
        self.burst = burst
        self.priority = priority
        self.remaining = burst
        self.start_time = -1
        self.finish_time = 0
        self.waiting_time = 0
        self.turnaround_time = 0
        self.response_time = 0

    def __repr__(self):
        return (f"Process({self.pid}, arrival={self.arrival}, "
                f"burst={self.burst}, remaining={self.remaining})")


class CPUScheduler:
    def __init__(self, quantum=3):
        self.quantum = quantum

    def round_robin(self, processes):
        """
        Round Robin Algorithm:
        - Each process receives a maximum of $quantum$ units of CPU time.
        - If the process is not finished, it is moved to the back of the queue.
        - Wait Time calculation: $Wait = Turnaround - Burst$
        - Turnaround Time calculation: $TAT = Finish - Arrival$
        """
        procs = sorted(processes, key=lambda p: p.arrival)
        n = len(procs)

        print("\nInput Processes:")
        print(f"{'PID':<6} {'Arrival':<10} {'Burst':<8}")
        print("-" * 24)
        for p in procs:
            print(f"{p.pid:<6} {p.arrival:<10} {p.burst:<8}")

        print(f"\nTime Quantum: {self.quantum}")
        print("\n" + "=" * 55)
        print(f"{'Time':<8} {'PID':<8} {'Action':<20} {'Remaining'}")
        print("-" * 55)

        queue = deque()
        current_time = 0
        completed = 0
        gantt = []
        arrived = set()

        for p in procs:
            if p.arrival <= current_time:
                queue.append(p)
                arrived.add(p.pid)

        while completed < n:
            if not queue:
                current_time += 1
                for p in procs:
                    if p.pid not in arrived and p.arrival <= current_time:
                        queue.append(p)
                        arrived.add(p.pid)
                continue

            proc = queue.popleft()

            if proc.start_time == -1:
                proc.start_time = current_time

            exec_time = min(self.quantum, proc.remaining)
            gantt.append((proc.pid, current_time, current_time + exec_time))

            print(f"t={current_time:<7} {proc.pid:<8} "
                  f"exec {exec_time} units{'':<9} "
                  f"{proc.remaining} -> {proc.remaining - exec_time}")

            current_time += exec_time
            proc.remaining -= exec_time

            for p in procs:
                if p.pid not in arrived and p.arrival <= current_time:
                    queue.append(p)
                    arrived.add(p.pid)

            if proc.remaining == 0:
                proc.finish_time = current_time
                proc.turnaround_time = proc.finish_time - proc.arrival
                proc.waiting_time = proc.turnaround_time - proc.burst
                proc.response_time = proc.start_time - proc.arrival
                completed += 1
                print(f"{'':8} [Finished: {proc.pid}]")
            else:
                queue.append(proc)

        self._print_results(procs)
        self._print_gantt(gantt)

    def _print_results(self, processes):
        print("\n" + "=" * 65)
        print(f"Round Robin Results (Quantum = {self.quantum})")
        print("=" * 65)
        print(f"{'PID':<6} {'Arrival':<9} {'Burst':<7} {'Finish':<8} "
              f"{'TAT':<7} {'Wait':<7} {'Response'}")
        print("-" * 65)

        total_tat = total_wait = total_resp = 0

        for p in sorted(processes, key=lambda x: x.pid):
            print(f"{p.pid:<6} {p.arrival:<9} {p.burst:<7} "
                  f"{p.finish_time:<8} {p.turnaround_time:<7} "
                  f"{p.waiting_time:<7} {p.response_time}")
            total_tat += p.turnaround_time
            total_wait += p.waiting_time
            total_resp += p.response_time

        n = len(processes)
        print("-" * 65)
        print(f"{'Avg':<6} {'':<9} {'':<7} {'':<8} "
              f"{total_tat/n:<7.2f} {total_wait/n:<7.2f} {total_resp/n:.2f}")
        print("\nNote: TAT = Turnaround Time | Wait = Waiting Time")

    def _print_gantt(self, gantt):
        print("\nGantt Chart:")
        
        for pid, start, end in gantt:
            width = (end - start) * 2
            print(f"|{pid:^{width}}", end="")
        print("|")

        for pid, start, end in gantt:
            width = (end - start) * 2
            print(f"{start:<{width+1}}", end="")
        print(gantt[-1][2])
        print()
