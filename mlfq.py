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
# CS: Context Switch

# We start first by initializing the constants.

RR_TIME_QUANTUM = 4

RR_HIGH_PRIORITY = 1
FCFS_MEDIUM_PRIORITY = 2
SJF_LOW_PRIORITY = 3

NULL_QUEUE_PRIORITY = 0  # This is for processes that have completely finished.


class MLFQ:
    def __init__(self, rr_allotment, fcfs_allotment, context_switch_time):
        self.currentGlobalTime = 0
        self.recentRunningProcess = 0
        self.roundRobinQueue = []
        self.rrTimeQuantum = RR_TIME_QUANTUM
        self.rrTimeAllotment = rr_allotment
        self.firstComeFirstServeQueue = []
        self.fcfsTimeAllotment = fcfs_allotment
        self.shortestJobFirstQueue = []
        self.ioProcesses = []
        self.contextSwitch = context_switch_time
        self.totalCSTime = 0


# Each process has its own set of properties that identifies them.
# Luckily, for this project, we can assume that the user gives all of these
# details in advance through the set1.txt and set2.txt input files.


# We take advantage of this by incorporating as much up-front data as possible.
# In addition, since we are dealing with a split of CPU and I/O times, perhaps we could
# try placing these times in separate, array data structures to account for this?


class Process:
    def __init__(self):
        self.processName = ""
        self.processID = 0
        self.arrivalTime = 0
        self.cpuTimes = []
        self.ioTimes = []
        self.usedTimeQuantum = 0
        self.usedTimeAllotment = 0
        self.totalBurstTime = 0
        self.completionTime = 0
        self.turnaroundTime = 0
        self.waitingTime = 0
        self.processCSTime = 0
        self.currentQueue = RR_HIGH_PRIORITY  # All processes start at the Highest Queue: Round Robin.


def parse_input(file_content: str):
    lines = file_content.strip().split("\n")

    # The input can be divided into two halves, separated by a newline ("\n") in between.
    # The first lines will always be 4 integers, as instructed, so we extract and initialize them as so.

    num_processes = int(lines[0])
    rr_allotment = int(lines[1])
    fcfs_allotment = int(lines[2])
    context_switch_time = int(lines[3])

    # Extract CPU and I/O times. We can then take comfort in knowing that the succeeding lines are all just process details.
    process_lines = lines[5:]

    process_list = []

    # In addition, we also know that these details have a fixed pattern and are always separated by semicolons.
    for idx, process_line in enumerate(process_lines):
        parts = process_line.split(";")
        process_name = parts[0]
        arrival_time = int(parts[1])

        cpu_times = [int(parts[i]) for i in range(2, len(parts), 2)]
        io_times = [int(parts[i]) for i in range(3, len(parts), 2)]

        process = Process()
        process.processName = process_name
        process.processID = idx + 1
        process.arrivalTime = arrival_time
        process.cpuTimes = cpu_times
        process.ioTimes = io_times
        process.totalBurstTime = sum(cpu_times) + sum(io_times)

        process_list.append(process)

    # Sort processes by arrival time and then by process ID (alphabetical order).
    # We assume that the input file is already sorted at least by processName
    # (with hopefully the correct corresponding processID mappings).

    process_list.sort(key=lambda p: (p.arrivalTime, p.processID))

    return num_processes, rr_allotment, fcfs_allotment, context_switch_time, process_list



def print_mlfq_state(MLFQ: MLFQ, process_list: list[Process]):
    print(f"At Time = {MLFQ.currentGlobalTime}")
    
    done_processes = [p.processName for p in process_list if p.currentQueue == NULL_QUEUE_PRIORITY]
    if done_processes:
        print(f"{', '.join(done_processes)} DONE")

    arriving_processes = [p.processName for p in MLFQ.roundRobinQueue if p.arrivalTime == MLFQ.currentGlobalTime]
    if arriving_processes:
        print(f"Arriving: [{', '.join(arriving_processes)}]")

    round_robin_queue = [p.processName for p in MLFQ.roundRobinQueue]
    fcfs_queue = [p.processName for p in MLFQ.firstComeFirstServeQueue]
    sjf_queue = [p.processName for p in MLFQ.shortestJobFirstQueue]
    
    print(f"Queues: [{', '.join(round_robin_queue)}]; [{', '.join(fcfs_queue)}]; [{', '.join(sjf_queue)}]")

    if not MLFQ.roundRobinQueue and not MLFQ.firstComeFirstServeQueue and not MLFQ.shortestJobFirstQueue:
        print("CPU: []")
    elif MLFQ.recentRunningProcess:
        current_cpu_process = next((p.processName for p in process_list if p.processID == MLFQ.recentRunningProcess), None)
        print(f"CPU: {current_cpu_process}")
    else:
        print("CPU: []")

    if MLFQ.ioProcesses:
        io_processes = [p.processName for p in MLFQ.ioProcesses]
        print(f"I/O: [{', '.join(io_processes)}]")

    demoted_processes = [p.processName for p in process_list if p.currentQueue in [FCFS_MEDIUM_PRIORITY, SJF_LOW_PRIORITY]]
    if demoted_processes:
        print(f"{', '.join(demoted_processes)} DEMOTED")

    print("\n")
    
    
    
def print_simulation_summary(process_list: list[Process]):
    total_turnaround_time = 0
    process_list.sort(key=lambda p: (p.processName))

    print("SIMULATION DONE\n")

    # Calculate turnaround and waiting times for each process.
    for process in process_list:
        process.turnaroundTime = process.completionTime - process.arrivalTime

        # I do not know if we should consider context switches in the waiting time but I did just in case.
        process.waitingTime = process.completionTime - process.totalBurstTime - process.processCSTime
        total_turnaround_time += process.turnaroundTime

        print(f"Turn-around time for Process {process.processName} : " f"{process.completionTime} - {process.arrivalTime} = {process.turnaroundTime} ms")

    print()

    # Calculate and print average turnaround time.
    average_turnaround_time = total_turnaround_time / len(process_list)
    print(f"Average Turn-around time = {round(average_turnaround_time, 4)} ms\n")

    # Print waiting times.
    for process in process_list:
        print(f"Waiting time for Process {process.processName} : {process.waitingTime} ms")

    print()


# IMPORTANT: According to the sample input in the project specs it seems that
# (to give an example), if a process is in I/O in a higher priority queue when,
# at the same time, another process in a lower priority queue is just about to run next,
# then the lower priority process should actually be allowed to run its entire burst time.


# Essentially, it gets to run uninterrupted even if the process in the higher priority queue,
# let's say, wakes up earlier than when the lower priority process finishes its burst time.
# THIS IS NOT IMPLEMENTED HERE! Instead, all lower priority processes can get interrupted
# by higher ones at any time. I do not know which is correct so kindly verify HAHAHAHA


def run_mlfq_scheduler(MLFQ: MLFQ, process_list: list[Process]):
    while True:
        # Step 1: Add newly arriving processes to the highest priority queue: the Round Robin Queue.
        for process in process_list:
            if process.arrivalTime == MLFQ.currentGlobalTime and process not in MLFQ.roundRobinQueue:
                MLFQ.roundRobinQueue.append(process)

        if MLFQ.currentGlobalTime > 0:
            # Step 2: Handle IO processes, if any. Decrement I/O bursts per time step and check for CPU burst times.
            for process in MLFQ.ioProcesses:
                if process.ioTimes:
                    process.ioTimes[0] -= 1

            for process in MLFQ.ioProcesses:
                if process.ioTimes:
                    if process.ioTimes[0] == 0:
                        process.ioTimes.pop(0)
                        MLFQ.ioProcesses.remove(process)

                        if process.cpuTimes:
                            if process.currentQueue == RR_HIGH_PRIORITY:
                                MLFQ.roundRobinQueue.append(process)
                            elif process.currentQueue == FCFS_MEDIUM_PRIORITY:
                                MLFQ.firstComeFirstServeQueue.append(process)
                            elif process.currentQueue == SJF_LOW_PRIORITY:
                                MLFQ.shortestJobFirstQueue.append(process)

                        process.completionTime = MLFQ.currentGlobalTime
                        process.processCSTime = MLFQ.totalCSTime

            # Step 3: Process CPU bursts and handle queue transitions.
            # TODO: Also please don't forget to implement the actual algorithm for Shortest Job First!
            for current_queue in [MLFQ.roundRobinQueue, MLFQ.firstComeFirstServeQueue, MLFQ.shortestJobFirstQueue]:
                if current_queue:
                    current_process = current_queue[0]

                    # Decrement CPU bursts per time step. In addition,
                    # increment the time quantum and time allotment used by the current process so far.

                    if current_process.cpuTimes:
                        current_process.cpuTimes[0] -= 1
                        current_process.usedTimeQuantum += 1
                        current_process.usedTimeAllotment += 1

                        # If a CPU burst is done, it means that the process is either finished or going to I/O.
                        if current_process.cpuTimes[0] == 0:
                            current_process.cpuTimes.pop(0)
                            if current_process.ioTimes:
                                current_process.usedTimeQuantum = 0
                                current_process.usedTimeAllotment = 0
                                MLFQ.ioProcesses.append(current_process)
                            elif not current_process.cpuTimes:
                                current_process.currentQueue = NULL_QUEUE_PRIORITY
                                current_process.completionTime = MLFQ.currentGlobalTime
                                current_process.processCSTime = MLFQ.totalCSTime
                            current_queue.pop(0)

                        # If the Round Robin Time Allotment expires before the CPU burst is finished,
                        # then demote the process to the FCFS Queue.

                        elif current_process.currentQueue == RR_HIGH_PRIORITY and current_process.usedTimeAllotment == MLFQ.rrTimeAllotment:
                            current_process.currentQueue = FCFS_MEDIUM_PRIORITY
                            current_process.usedTimeAllotment = 0
                            current_process.usedTimeQuantum = 0  # Not really necessary
                            current_queue.pop(0)
                            MLFQ.firstComeFirstServeQueue.append(current_process)

                        # If the Round Robin Time Quantum expires before the CPU burst is finished,
                        # then switch out the process.

                        elif current_process.currentQueue == RR_HIGH_PRIORITY and current_process.usedTimeQuantum == MLFQ.rrTimeQuantum:
                            current_process.usedTimeQuantum = 0
                            current_queue.pop(0)
                            current_queue.append(current_process)

                        # If the FCFS Time Allotment expires before the CPU burst is finished,
                        # then demote the process to the SJF Queue.

                        elif current_process.currentQueue == FCFS_MEDIUM_PRIORITY and current_process.usedTimeAllotment == MLFQ.fcfsTimeAllotment:
                            current_process.currentQueue = SJF_LOW_PRIORITY
                            current_process.usedTimeAllotment = 0  # Not really necessary
                            current_process.usedTimeQuantum = 0  # Not really necessary
                            current_queue.pop(0)
                            MLFQ.shortestJobFirstQueue.append(current_process)

                    # Handle Context Switching between different processes.
                    if current_queue and MLFQ.recentRunningProcess != current_queue[0].processID:

                        if MLFQ.contextSwitch > 0:
                            MLFQ.recentRunningProcess = 0
                            print_mlfq_state(MLFQ, process_list)
                            MLFQ.currentGlobalTime += MLFQ.contextSwitch
                            MLFQ.totalCSTime += MLFQ.contextSwitch

                        MLFQ.recentRunningProcess = current_queue[0].processID

                    break  # Remember, queues can only be ran, one at a time, based on the priority order.

        else:
            MLFQ.recentRunningProcess = MLFQ.roundRobinQueue[0].processID

        # Print the current state of MLFQ.
        print_mlfq_state(MLFQ, process_list)

        # Increment global time.
        MLFQ.currentGlobalTime += 1

        # This stops the scheduler if at any point in time, except for at t = 0,
        # all three of the queues are empty at the same time. However, I do not know if
        # this should be the correct behavior according to the project specs as well as if it's safe.

        if not (MLFQ.roundRobinQueue or MLFQ.firstComeFirstServeQueue or MLFQ.shortestJobFirstQueue):
            print_simulation_summary(process_list)
            break


# Do we modularize this main function into sub functions as well?
# Also, is it possible for the input to be typed by the user via the terminal?
# I do not know if these features need to be implemented (neither of them have been yet).
# Regardless, I just wanted to give a heads up anyways just in case.


if __name__ == "__main__":
    # Parse set1.txt, use it to run the scheduler, and then output the results.
    with open("set1.txt", "r") as file:
        file_content = file.read()

    num_processes, rr_allotment, fcfs_allotment, context_switch_time, process_list = parse_input(file_content)
    first_MLFQ = MLFQ(rr_allotment, fcfs_allotment, context_switch_time)
    run_mlfq_scheduler(first_MLFQ, process_list)
    print()

    # Parse set2.txt, use it to run the scheduler, and then output the results.
    with open("set2.txt", "r") as file:
        file_content = file.read()

    num_processes, rr_allotment, fcfs_allotment, context_switch_time, process_list = parse_input(file_content)
    second_MLFQ = MLFQ(rr_allotment, fcfs_allotment, context_switch_time)
    run_mlfq_scheduler(second_MLFQ, process_list)
    print()
