"""
memory_manager.py - Memory Management for Mini OS
Algorithm: First Fit
Memory is divided into contiguous blocks, and the first sufficient space is selected.
"""

class MemoryBlock:
    """
    A contiguous block of memory.
    Address bounds are calculated as: $End = Start + Size - 1$
    """
    def __init__(self, start, size, process_id=None):
        self.start = start
        self.size = size
        self.process_id = process_id
        self.end = start + size - 1

    @property
    def is_free(self):
        return self.process_id is None

    def __repr__(self):
        status = "FREE" if self.is_free else f"P:{self.process_id}"
        return f"Block[{self.start}-{self.end}] size={self.size} ({status})"


class MemoryManager:
    """
    Memory management utilizing the First Fit algorithm.
    """

    def __init__(self, total_size=256):
        self.total_size = total_size
        self.blocks = [MemoryBlock(start=0, size=total_size)]
        self.allocation_log = []

    def allocate(self, process_id, size):
        """
        Allocate memory using First Fit:
        The first free block that satisfies $BlockSize >= RequestSize$ is selected.
        """
        for i, block in enumerate(self.blocks):
            if block.is_free and block.size >= size:
                if block.size > size:
                    remaining = MemoryBlock(
                        start=block.start + size,
                        size=block.size - size
                    )
                    self.blocks.insert(i + 1, remaining)

                block.size = size
                block.end = block.start + size - 1
                block.process_id = process_id

                msg = (f"[SUCCESS] Allocated: {process_id} <- {size} KB "
                       f"(Address {block.start}-{block.end})")
                self.allocation_log.append(msg)
                print(f"  {msg}")
                return True

        msg = f"[FAILED] Cannot allocate {size} KB to {process_id} - Insufficient contiguous memory"
        self.allocation_log.append(msg)
        print(f"  {msg}")
        return False

    def deallocate(self, process_id):
        """
        Deallocate memory for a specific process and merge contiguous free blocks.
        """
        freed = False
        for block in self.blocks:
            if block.process_id == process_id:
                block.process_id = None
                freed = True
                msg = f"[FREED] Deallocated: {process_id} ({block.size} KB freed)"
                self.allocation_log.append(msg)
                print(f"  {msg}")

        if freed:
            self._merge_free_blocks()
        else:
            print(f"  [WARN] Process '{process_id}' not found in memory.")

    def _merge_free_blocks(self):
        """Coalesce contiguous free memory blocks."""
        merged = True
        while merged:
            merged = False
            for i in range(len(self.blocks) - 1):
                if self.blocks[i].is_free and self.blocks[i + 1].is_free:
                    self.blocks[i].size += self.blocks[i + 1].size
                    self.blocks[i].end = self.blocks[i].start + self.blocks[i].size - 1
                    self.blocks.pop(i + 1)
                    merged = True
                    break

    def display(self, title="Memory Status"):
        """Display a graphical representation of the memory state."""
        print(f"\n  [ {title} ]")
        print(f"  {'='*55}")

        bar = ""
        legend = []
        bar_width = 50

        for block in self.blocks:
            ratio = block.size / self.total_size
            width = max(1, int(ratio * bar_width))
            if block.is_free:
                bar += "." * width
            else:
                char = block.process_id[-1] if block.process_id else "?"
                bar += char * width
                legend.append(f"{block.process_id}={char}")

        print(f"  |{bar[:bar_width]}|")
        print(f"  0{' ':>49}{self.total_size} KB")

        if legend:
            print(f"  Legend: {', '.join(legend)}, . = Free")

        print(f"\n  {'ID':<7} {'Start':<8} {'End':<8} {'Size':<9} {'Status'}")
        print(f"  {'-'*45}")
        used = 0
        for idx, block in enumerate(self.blocks):
            status = "Free" if block.is_free else f"Used ({block.process_id})"
            print(f"  {idx+1:<7} {block.start:<8} {block.end:<8} "
                  f"{block.size:<9} {status}")
            if not block.is_free:
                used += block.size

        free = self.total_size - used
        print(f"  {'-'*45}")
        print(f"  Total: {self.total_size} KB | "
              f"Used: {used} KB | "
              f"Free: {free} KB | "
              f"Utilization: {used/self.total_size*100:.1f}%")

    def fragmentation_report(self):
        """
        Report memory fragmentation metrics.
        Calculation: $FragmentationRate = (1 - LargestFree / TotalFree) * 100$
        """
        free_blocks = [b for b in self.blocks if b.is_free]
        total_free = sum(b.size for b in free_blocks)
        largest_free = max((b.size for b in free_blocks), default=0)

        print(f"\n  [ Fragmentation Report ]")
        print(f"  {'-'*33}")
        print(f"  Free Blocks         : {len(free_blocks)}")
        print(f"  Total Free Memory   : {total_free} KB")
        print(f"  Largest Free Block  : {largest_free} KB")
        if total_free > 0 and largest_free < total_free:
            frag = (1 - largest_free / total_free) * 100
            print(f"  Fragmentation Rate  : {frag:.1f}%  (Warning)")
        else:
            print(f"  Fragmentation Rate  : 0.0%  (Optimal)")

    def demo(self):
        """Execute a full simulation demo."""
        print(f"\n  Algorithm: First Fit | Total Memory: {self.total_size} KB")
        print(f"  Description: Allocates the first free block that is sufficiently large.\n")

        print(f"  -- Stage 1: Initial Allocation --")
        self.allocate("P1", 40)
        self.allocate("P2", 70)
        self.allocate("P3", 30)
        self.allocate("P4", 50)
        self.allocate("P5", 20)
        self.display("Post Initial Allocation")

        print(f"\n  -- Stage 2: Deallocation of P2 and P4 --")
        self.deallocate("P2")
        self.deallocate("P4")
        self.display("Post Deallocation of P2 and P4")
        self.fragmentation_report()

        print(f"\n  -- Stage 3: New Allocation (P6=25KB) --")
        self.allocate("P6", 25)
        self.display("Post Allocation of P6")

        print(f"\n  -- Stage 4: Out of Memory Allocation Attempt --")
        self.allocate("P7", 200)

        print(f"\n  [INFO] Memory Manager demo completed.")


if __name__ == "__main__":
    print("="*57)
    print("  Memory Manager Simulation - First Fit")
    print("="*57)
    mm = MemoryManager(total_size=256)
    mm.demo()
