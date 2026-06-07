# 🖥️ Mini OS

> Operating Systems Laboratory Final Project  
> Implementation Language: Python 3  

---

## 📁 Project Structure

mini_os/
├── main.py              # Entry point - Run CLI or Demo
├── cli.py               # Command Line Interface (CLI)
├── filesystem.py        # Virtual File System
├── cpu_scheduler.py     # CPU Management - Round Robin
├── memory_manager.py    # Memory Management - First Fit
├── disk_scheduler.py    # Disk Management - SSTF
└── README.md            # This file


---

## ▶️ How to Run

```bash
# Interactive CLI environment
python main.py

# Full demo of all algorithms (suitable for presentation)
python main.py --demo

# Help
python main.py --help
```

**Requirements:** Python 3.6 or higher — No external libraries required.

---

## Part 1: File System and CLI

### 1.1 File System Architecture (`filesystem.py`)

The file system is implemented as an **n-ary tree** in memory.

#### Data Structure

FileNode
├── name          File or directory name
├── is_dir        Type (file or directory)
├── content       File content (string)
├── children      Children dictionary (only for directories)
├── created_at    Creation time
├── modified_at   Last modified time
└── size          Size in bytes


**Reason for choosing a dictionary for `children`:**  
$O(1)$ search by name, similar to an inode table in real systems.

#### Implemented Commands

| Command | Function | Complexity |
|-------|---------|---------|
| `mkdir <name>` | Create directory | $O(1)$ |
| `rmdir <name>` | Remove empty directory | $O(1)$ |
| `cd <name>` | Change directory | $O(1)$ |
| `cd ..` | Go to parent directory | $O(depth)$ |
| `ls` | List contents | $O(n)$ |
| `ls -l` | Detailed list | $O(n)$ |
| `pwd` | Print working directory | $O(1)$ |
| `tree` | Recursive tree view | $O(n)$ |
| `touch <name>` | Create file | $O(1)$ |
| `rm <name>` | Remove file | $O(1)$ |
| `rename <old> <new>` | Rename item | $O(1)$ |
| `write <name> <text>` | Write to file | $O(1)$ |
| `cat <name>` | Read file | $O(1)$ |

#### Sample Run

MiniOS:/> mkdir projects
✅ Directory 'projects' created.

MiniOS:/> cd projects
📂 Changed directory to: /projects

MiniOS:/projects> touch main.py
✅ File 'main.py' created.

MiniOS:/projects> write main.py print("Hello World")
✅ Content written to 'main.py' (20 bytes).

MiniOS:/projects> tree
📂 /projects
└── 📄 main.py


---

### 1.2 CLI Environment (`cli.py`)

The CLI is a **REPL Loop** (Read-Eval-Print Loop):

┌─────────────────────────────────┐
│  1. Get user input (Read)       │
│  2. Parse command (Eval)        │
│  3. Execute and display (Print) │
│  4. Return to step 1 (Loop)     │
└─────────────────────────────────┘


**CLI Features:**
- Dynamic prompt showing the current path: `MiniOS:/home/user>`
- Error handling with `try/except`
- Support for `Ctrl+C` without exiting
- Integration with CPU, Memory, and Disk modules

---

## Part 2: Operating System Algorithms

---

### 2.1 CPU Management - Round Robin (`cpu_scheduler.py`)

#### Algorithm Explanation

Round Robin is one of the most widely used CPU scheduling algorithms.  
Each process gets a maximum of **one time quantum** from the CPU.  
If the process does not finish, it returns to the **end of the queue**.

Ready Queue:
┌────┬────┬────┬────┐
│ P1 │ P2 │ P3 │ P4 │  ← Waiting processes
└────┴────┴────┴────┘
         ↓ quantum=3
    CPU executes
         ↓
    [Finished?] → Yes → Exit
         ↓ No
    Returns to the end of the queue


#### Input Parameters

```python
Process("P1", arrival=0, burst=8)   # P1: Arrives at t=0, needs 8 CPU units
Process("P2", arrival=1, burst=4)
Process("P3", arrival=2, burst=9)
Process("P4", arrival=3, burst=5)
CPUScheduler(quantum=3)             # Each process gets 3 CPU units
```

#### Output and Results

Gantt Chart:
|  P1  |  P2  |  P3  |  P4  |  P1  |P2|  P3  | P4 | P1 |  P3  |
0      3      6      9      12     15 16     19   21   23     26

Results Table:
PID   Burst   TAT    Wait   Response
P1    8       23     15     0
P2    4       15     11     2
P3    9       24     15     4
P4    5       18     13     6
Average:  TAT=20  Wait=13.5  Response=3.0


#### Calculation Equations

$$Turnaround Time (TAT) = Finish Time - Arrival Time$$
$$Waiting Time = TAT - Burst Time$$
$$Response Time = Start Time - Arrival Time$$

#### Reason for choosing Round Robin

| Metric | Round Robin | FCFS | SJF |
|-------|------------|------|-----|
| Fairness | ✅ Excellent | ❌ Poor | ❌ Poor |
| Starvation | ✅ None | ✅ None | ❌ Yes |
| Response Time | ✅ Short | ❌ Long | ✅ Short |
| Best For | Time-sharing | Batch | Batch |

Round Robin is the **best choice for interactive systems** because no process waits longer than the `quantum`.

---

### 2.2 Memory Management - First Fit (`memory_manager.py`)

#### Algorithm Explanation

Memory is maintained as a **list of blocks**.  
In First Fit allocation, the **first free block that is large enough** is selected.

Memory before allocation:
┌─────────────────────────────────┐
│           256 KB Free            │
└─────────────────────────────────┘

After allocating P1=40KB, P2=70KB, P3=30KB:
┌──────┬───────────┬───────┬────────┐
│  P1  │    P2     │  P3   │  Free  │
│ 40KB │   70KB    │ 30KB  │ 116KB  │
└──────┴───────────┴───────┴────────┘
 0    39 40       109 110  139 140  255


#### Implemented Operations

**1. Allocate:**
```python
def allocate(self, process_id, size):
    for block in self.blocks:
        if block.is_free and block.size >= size:
            # Split the block into two parts
            # Part 1: Allocated to the process
            # Part 2: Remaining free space
```

**2. Deallocate + Coalescing:**
```python
def deallocate(self, process_id):
    # Free the block
    block.process_id = None
    # Merge adjacent free blocks
    self._merge_free_blocks()
```

**3. Coalescing Free Blocks:**  
After deallocation, adjacent free blocks are merged to prevent **External Fragmentation**.

#### Sample Run and Fragmentation

After deallocating P2 and P4:
┌──────┬───────────┬───────┬──────────┬───────┬────────┐
│  P1  │  Free(70) │  P3   │ Free(50) │  P5   │ Free(46)│
└──────┴───────────┴───────┴──────────┴───────┴────────┘

Fragmentation Report:
Number of free blocks : 3
Total free memory     : 166 KB
Largest free block    : 70 KB
Fragmentation rate    : 57.8% ⚠️

→ First Fit selects the first sufficient block (70KB) for P6=25KB


#### Memory Allocation Algorithms Comparison

| Algorithm | Speed | Fragmentation | Description |
|----------|------|---------------|-------|
| **First Fit** | ✅ Fast | Medium | First sufficient block |
| Best Fit | ❌ Slow | ✅ Less | Smallest sufficient block |
| Worst Fit | ❌ Slow | ❌ More | Largest available block |

**Reason for choosing First Fit:** Fastest algorithm with acceptable practical performance.

---

### 2.3 Disk Management - SSTF (`disk_scheduler.py`)

#### Algorithm Explanation

SSTF (Shortest Seek Time First) selects the **closest track** to the current disk head position at each step.

Requests: 82, 170, 43, 140, 24, 16, 190, 34
Initial head position: 50

Step 1: Closest to 50  → 43  (Distance=7)
Step 2: Closest to 43  → 34  (Distance=9)
Step 3: Closest to 34  → 24  (Distance=10)
Step 4: Closest to 24  → 16  (Distance=8)
Step 5: Closest to 16  → 82  (Distance=66)
...


#### Head Movement Diagram

0                                              199
|────────────────────────────────────────────────|
|            ●                                    | ← 50 (Start)
|          ●                                      | ← 43
|        ●                                        | ← 34
|      ●                                          | ← 24
|    ●                                            | ← 16
|                    ●                            | ← 82
|                               ●                 | ← 140
|                                        ●        | ← 170
|                                             ●   | ← 190


#### SSTF vs FCFS Comparison

SSTF Order: 43 → 34 → 24 → 16 → 82 → 140 → 170 → 190
Total SSTF movement: 208 tracks  ✅

FCFS Order: 82 → 170 → 43 → 140 → 24 → 16 → 190 → 34
Total FCFS movement: 798 tracks  ❌ (Almost 4 times more!)


#### Note: Starvation in SSTF

SSTF can cause **Starvation**:  
If requests close to the head keep arriving, distant requests will never be serviced.  
Our system measures and reports the number of waiting turns to monitor this.

---

## Conclusion

| Component | Algorithm | Reason for Selection |
|-----|---------|-------------|
| CPU | Round Robin | Fair, no starvation, suitable for time-sharing |
| Memory | First Fit | Fastest allocation with high practical efficiency |
| Disk | SSTF | Minimizes total head movement, increases disk lifespan |

---

## References

- Silberschatz, A., Galvin, P. B., & Gagne, G. — *Operating System Concepts* (10th Ed.)
- Tanenbaum, A. S. — *Modern Operating Systems* (4th Ed.)