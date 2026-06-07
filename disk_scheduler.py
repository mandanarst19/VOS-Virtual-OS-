class DiskRequest:
    def __init__(self, track, process_id=""):
        self.track = track
        self.process_id = process_id
        self.served = False
        self.wait_time = 0

class DiskScheduler:
    def __init__(self, head_position=50, max_track=199):
        self.head_position = head_position
        self.max_track = max_track

    def sstf(self, requests):
        queue = [DiskRequest(r[0], r[1]) if isinstance(r, tuple) else DiskRequest(r) for r in requests]

        current = self.head_position
        total_movement = 0
        order = []
        seek_sequence = [current]

        print("Incoming requests:")
        print(f"{'#':<5} {'Track':<8} {'Process'}")
        print("-" * 25)
        for i, req in enumerate(queue):
            print(f"{i+1:<5} {req.track:<8} {req.process_id or '-'}")

        print(f"\nInitial head position: {current}")
        print("=" * 50)
        print(f"{'Step':<8} {'From':<8} {'To':<10} {'Move':<8} {'Process'}")
        print("-" * 50)

        step = 1
        remaining = queue.copy()

        while remaining:
            nearest = min(remaining, key=lambda r: abs(r.track - current))
            movement = abs(nearest.track - current)
            total_movement += movement

            print(f"{step:<8} {current:<8} {nearest.track:<10} {movement:<8} {nearest.process_id or 'req-' + str(nearest.track)}")

            order.append(nearest.track)
            seek_sequence.append(nearest.track)

            for r in remaining:
                if r != nearest:
                    r.wait_time += 1

            current = nearest.track
            remaining.remove(nearest)
            step += 1

        self._print_results(order, total_movement, queue)
        self._print_seek_diagram(seek_sequence)

    def fcfs(self, requests):
        tracks = [r[0] if isinstance(r, tuple) else r for r in requests]
        current = self.head_position
        total_movement = 0
        order = []

        print("\nFCFS Comparison:")
        print("-" * 35)
        for track in tracks:
            movement = abs(track - current)
            total_movement += movement
            order.append(track)
            current = track

        print(f"Service order: {' -> '.join(map(str, order))}")
        print(f"Total movement (FCFS): {total_movement} tracks")
        return total_movement

    def _print_results(self, order, total_movement, queue):
        print("\n" + "=" * 50)
        print("SSTF Results")
        print("=" * 50)
        print(f"Service order: {' -> '.join(map(str, order))}")
        print(f"Total movement: {total_movement} tracks")
        if order:
            print(f"Average movement: {total_movement/len(order):.1f} tracks/request")

        starved = [r for r in queue if r.wait_time >= 3]
        if starved:
            print("\nStarvation Warning:")
            for r in starved:
                label = r.process_id or f"track-{r.track}"
                print(f"  {label} waited {r.wait_time} turns")
        else:
            print("\nNo Starvation detected.")

    def _print_seek_diagram(self, seek_sequence):
        print("\nSeek Diagram:")
        width = 50
        print(f"0{' '*(width-2)}{self.max_track}")
        print(f"|{'-'*width}|")

        for i, pos in enumerate(seek_sequence):
            scaled = int(pos / self.max_track * width)
            label = f"|{' '*scaled}*{' '*(width-scaled)}| <- {pos}"
            if i == 0:
                label += " (start)"
            print(label)

        print(f"|{'-'*width}|")

    def demo(self):
        print(f"\nSSTF Scheduling | Initial Head: {self.head_position}\n")

        requests = [
            (82,  "P1"),
            (170, "P2"),
            (43,  "P3"),
            (140, "P4"),
            (24,  "P5"),
            (16,  "P6"),
            (190, "P7"),
            (34,  "P8"),
        ]

        self.sstf(requests)

        print("\n" + "=" * 50)
        fcfs_movement = self.fcfs(requests)
        print("\nFinal Comparison:")
        print("-" * 35)
        print("SSTF: More efficient (less movement)")
        print(f"FCFS: {fcfs_movement} tracks")
        print("\nDisk Scheduler demo completed.")


if __name__ == "__main__":
    ds = DiskScheduler(head_position=50, max_track=199)
    ds.demo()
