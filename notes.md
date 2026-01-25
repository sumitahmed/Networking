📘 IPC USING PYTHON (netpack) — NOTES & EXPLANATION
🔹 Aim of the Program

To demonstrate Inter-Process Communication (IPC) using Queue and Multiprocessing in Python with the help of the netpack library.

🔹 Files Used
1️⃣ 2_IPC.py → Main / Driver Program

This is the main file

It:

creates shared resources (Queue)

creates processes

starts processes

This is the file we run

2️⃣ IPC_methods.py → Helper Functions

Contains functions used by child processes

Does NOT run on its own

Functions are executed only when called from 2_IPC.py

3️⃣ netpack.so → Networking & IPC Library

Precompiled Linux shared object

Provides:

Queue creation

Process creation

Read / write operations

Built for Python 3.10 on Linux

🔹 Code Breakdown (Step-by-Step)
📌 File: 2_IPC.py
1️⃣ Import required modules
import netpack as npk
import IPC_methods as ipc


netpack → provides IPC & multiprocessing utilities

IPC_methods → contains user-defined functions executed by processes

2️⃣ Create a Queue (Shared Memory)
Q = npk.create_queue()


Queue is used for data sharing between processes

Ensures safe communication (FIFO)

3️⃣ Create a list of data
val_list = list(range(5))


Data to be written into the queue

Values: [0, 1, 2, 3, 4]

4️⃣ Select experiment set
flag = 1


flag = 1 → SET-1 (Write & Read using two processes)

flag = 2 → SET-2 (Write-Read & Read-Write)

5️⃣ Create Processes (SET-1)
P1 = npk.create_process(ipc.write_to, [Q, val_list])
P2 = npk.create_process(ipc.read_from, [Q])


P1 → writes data into Queue

P2 → reads data from Queue

Both run concurrently

6️⃣ Start the processes
npk.start_process(P1)
npk.start_process(P2)


OS schedules both processes

Output order may vary slightly due to multiprocessing

7️⃣ Main process ends
print("Main ends")


Parent process finishes

Child processes continue execution

📌 File: IPC_methods.py
1️⃣ Write Process Function
def write_to(container, arr):


Writes elements of arr into Queue

Uses write_queue() from netpack

Prints written values

2️⃣ Read Process Function
def read_from(container):


Reads data from Queue

Stops when Queue becomes empty

Prints read values

🔴 Important Note

IPC_methods.py contains only function definitions.
So running it directly:

python3 IPC_methods.py


will produce no output — this is expected behavior.

🔹 Execution Flow (Important for Viva)
2_IPC.py
 ├── create Queue
 ├── create processes
 │    ├── Process P1 → write_to()
 │    └── Process P2 → read_from()
 ├── start processes
 └── Main process ends

🔹 Sample Output Explanation
Main ends
P1 has been started
P2 has been started
Printing from P1 & write Data = 0
...
Printing from P2 & read Data = 4


Main ends appears early → parent process exits

Writing happens first (P1)

Reading happens after slight delay (P2)

Order is controlled by OS scheduler

🔹 How to Run the Program (IMPORTANT)
✅ Method 1: Linux (Ubuntu / WSL Ubuntu 22.04)
1️⃣ Open terminal
cd path/to/Networking

2️⃣ Make sure Python version is correct
python3 --version


Must be:

Python 3.10.x

3️⃣ Run the program
python3 2_IPC.py


✔ This automatically imports netpack and IPC_methods
✔ No need to type import manually

❌ WRONG Way (Do NOT do this)
python3
>>> import netpack


❌ This only tests imports
❌ Does NOT run the program logic

🔹 Running in WSL (Special Notes)

Must use Ubuntu 22.04

Python 3.10 is mandatory

VS Code must be opened from Ubuntu 22.04 terminal:

code .


Check:

lsb_release -a
python3 --version

🔹 Common Mistakes (and Fixes)
Mistake	Reason	Fix
_PyUnicode_Ready error	Python version mismatch	Use Python 3.10
No output from IPC_methods.py	Only functions defined	Run 2_IPC.py
Using cat file.py	Prints code only	Use python3 file.py