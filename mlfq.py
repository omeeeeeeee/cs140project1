# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#     ___________    _____ __  ____      ____               _           __     ___  #
#    / ____/ ___/   <  / // / / __ \    / __ \_________    (_)__  _____/ /_   <  /  #
#   / /    \__ \    / / // /_/ / / /   / /_/ / ___/ __ \  / / _ \/ ___/ __/   / /   #
#  / /___ ___/ /   / /__  __/ /_/ /   / ____/ /  / /_/ / / /  __/ /__/ /_    / /    #
#  \____//____/   /_/  /_/  \____/   /_/   /_/   \____/_/ /\___/\___/\__/   /_/     #
#                                                    /___/                          #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


# ACRONYM LIST:
# MLFQ: Multi-Level Feedback Queue
# RR: Round Robin
# FCFS: First Come First Serve (i.e. First In, First Out)
# SJF: Shortest Job First

# Initialize the constants.
RR_TIME_QUANTUM = 4

RR_HIGH_PRIORITY = 1
FCFS_MEDIUM_PRIORITY = 2
SJF_LOW_PRIORITY = 3

NULL_QUEUE_PRIORITY = 0  # This is for processes that have completely finished.


class MLFQ:
    def __init__(self, rr_allotment, fcfs_allotment, context_switch_time):
        self.currentGlobalTime = 0
        self.recentRunningProcess = 0

        self.roundRobinQueue = []  # This should be a Queue Data Structure.
        self.rrTimeQuantum = RR_TIME_QUANTUM
        self.rrTimeAllotment = rr_allotment

        self.firstComeFirstServeQueue = []  # This should be a Queue Data Structure.
        self.fcfsTimeAllotment = fcfs_allotment

        self.shortestJobFirstQueue = []  # This should be a Queue Data Structure.

        self.ioProcesses = []
        self.contextSwitch = context_switch_time


# Each process has its own set of properties that identifies them.
# Luckily, for this project, we can assume that the user gives, in advance,
# all of these details through the set1.txt and set2.txt input files.


# We take advantage of this by incorporating as much up-front data as possible.
# In addition, since we are dealing with a split of CPU and I/O times,
# perhaps we could try placing these times in an array data structure to account for this?


class Process:
    def __init__(self):
        self.processName = ""
        self.processID = 0

        self.arrivalTime = 0

        self.cpuTimes = []
        self.ioTimes = []

        self.remainingTimeQuantum = 0
        self.remainingTimeAllotment = 0

        self.totalBurstTime = 0

        self.completionTime = 0
        self.turnaroundTime = 0
        self.waitingTime = 0

        self.currentQueue = RR_HIGH_PRIORITY  # All processes start at the Highest Queue: Round Robin.


# The input can be divided into two halves, separated by a newline (/n) in between.
# The first lines will always be 4 integers, as instructed, so we extract and initialize them as so.

# We can then take comfort in knowing that the succeeding lines are all just process details.
# In addition, we also know that these details have a fixed pattern and are separated by semicolons.


def parse_input(file_content):
    lines = file_content.strip().split("\n")

    num_processes = int(lines[0])
    rr_allotment = int(lines[1])
    fcfs_allotment = int(lines[2])
    context_switch_time = int(lines[3])
    process_lines = lines[5:]

    process_list = []

    for idx, process_line in enumerate(process_lines):
        parts = process_line.split(";")
        process_name = parts[0]
        arrival_time = int(parts[1])

        # Extract CPU and I/O times
        cpu_times = [int(parts[i]) for i in range(2, len(parts), 2)]
        io_times = [int(parts[i]) for i in range(3, len(parts), 2)]

        process = Process()
        process.processName = process_name
        process.processID = idx + 1
        process.arrivalTime = arrival_time
        process.cpuTimes = cpu_times
        process.ioTimes = io_times
        process.totalBurstTime = sum(cpu_times)

        process_list.append(process)

    # Sort processes by arrival time and then by process ID (alphabetical order)
    process_list.sort(key=lambda p: (p.arrivalTime, p.processID))

    return num_processes, rr_allotment, fcfs_allotment, context_switch_time, process_list


# This is a placeholder.
def run_rr_scheduler(MLFQ, process_list):
    pass


# This is a placeholder.
def run_fcfs_scheduler(MLFQ, process_list):
    pass


# This is a placeholder.
def run_sjf_scheduler(MLFQ, process_list):
    pass


# This is a placeholder. Don't do anything to this yet.
def run_mlfq_scheduler(MLFQ, process_list):
    pass

    # POSSIBLE HIGH-LEVEL IMPLEMENTATION:

    # 1.) At each time step, starting from "currentGlobalTime = 0", first check for any newly arriving processes based on these conditions:
    #   1.1. If "currentGlobalTime = arrivalTime" and "processID is NOT in roundRobinQueue"
    #   1.2. If 1.1. is TRUE, then we enqueue the processes (in order of "processID") to the "roundRobinQueue".
    #        We also set "recentRunningProcess" to the value at the start of the queue/s. Remember, queue priority is important here.

    # 2.) At each time step, starting from "currentGlobalTime = 0" (and assuming that the process is NOT in "ioProcesses"), we both decrement "cpuTimes[i]"
    #   (where "i" is the current CPU sub-burst time of the process) by 1 as well as increment the "remainingTimeQuantum"
    #   and the "remainingTimeAllotment" by 1 and then check then for any of these conditions:

    #   2.1.) If "cpuTimes[i] > 0" and "remainingTimeAllotment" is equal to either the "rrTimeAllotment" or the "fcfsTimeAllotment",
    #       then we have to dequeue the process and enqueue it to the lower priority queue.

    #   2.2.) If "cpuTimes[i] > 0" and "remainingTimeQuantum" is equal to "rrTimeQuantum",
    #       then we have to dequeue the process and re-enqueue it to the same priority queue.

    #   2.3.) If "cpuTimes[i]" is equal to 0,
    #       then we have to dequeue the process. We can then either:
    #       2.3.1.) Append the process to the "ioProcesses". Then, we dequeue it from "ioProcesses" if "ioTimes[i]" = 0 and then we can either:
    #           2.3.1.1.) Re-enqueue it to its priority queue if isn't finished yet.
    #           2.3.1.1.) Set its "currentQueue" to NULL_QUEUE_PRIORITY if it just finised.
    #       2.3.2.) Or, directly and simply set its "currentQueue" to NULL_QUEUE_PRIORITY if it has finished already.

    # REMINDER: If a dequeue from a CPU queue has occurred, and then the new process at queue[0] is NOT the same
    # as the previous one (i.e. "queue[0] is NOT equal to recentRunningProcess"),
    # and "contextSwitch > 0", then a Context Switch has to occur first.


if __name__ == "__main__":
    # Parse set1.txt
    with open("set1.txt", "r") as file:
        file_content = file.read()

    num_processes, rr_allotment, fcfs_allotment, context_switch_time, process_list = parse_input(file_content)
    first_MLFQ = MLFQ(rr_allotment, fcfs_allotment, context_switch_time)
    run_mlfq_scheduler(first_MLFQ, process_list)

    # Parse set2_test.txt
    with open("set2.txt", "r") as file:
        file_content = file.read()

    num_processes, rr_allotment, fcfs_allotment, context_switch_time, process_list = parse_input(file_content)
    second_MLFQ = MLFQ(rr_allotment, fcfs_allotment, context_switch_time)
    run_mlfq_scheduler(second_MLFQ, process_list)
