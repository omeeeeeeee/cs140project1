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

# Constants for scheduling.
RR_TIME_QUANTUM = 4
RR_HIGH_PRIORITY = 1
FCFS_MEDIUM_PRIORITY = 2
SJF_LOW_PRIORITY = 3
NULL_QUEUE_PRIORITY = 0  # For completed processes.

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
        self.currentQueue = RR_HIGH_PRIORITY

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
        
        if len(parts) < 2:
            #print(f"Skipping invalid process line: {process_line}")
            continue
        
        process_name = parts[0]
        
        try:
            arrival_time = int(parts[1])
        except ValueError:
            print(f"Invalid arrival time for process '{process_name}': {parts[1]}")
            continue
        
        cpu_times = []
        io_times = []
        
        for i in range(2, len(parts), 2):
            if i < len(parts):
                try:
                    cpu_times.append(int(parts[i]))
                except ValueError:
                    print(f"Invalid CPU time for process '{process_name}': {parts[i]}")
        
        for i in range(3, len(parts), 2):
            if i < len(parts):
                try:
                    io_times.append(int(parts[i]))
                except ValueError:
                    print(f"Invalid I/O time for process '{process_name}': {parts[i]}")

        process = Process()
        process.processName = process_name
        process.processID = idx + 1
        process.arrivalTime = arrival_time
        process.cpuTimes = cpu_times
        process.ioTimes = io_times
        process.totalBurstTime = sum(cpu_times) + sum(io_times)

        process_list.append(process)

    process_list.sort(key=lambda p: (p.arrivalTime, p.processID))
    return num_processes, rr_allotment, fcfs_allotment, context_switch_time, process_list
""" def print_mlfq_state(mlfq, process_list):
    print(f"At Time = {mlfq.currentGlobalTime}")

    # Print Round Robin Queue
    rr_queue = [p.processName for p in mlfq.roundRobinQueue]
    # Print FCFS Queue
    fcfs_queue = [p.processName for p in mlfq.firstComeFirstServeQueue]
    # Print SJF Queue
    sjf_queue = [p.processName for p in mlfq.shortestJobFirstQueue]

    # Format the queues as required
    print(f"Queues : {rr_queue};{fcfs_queue};{sjf_queue}")

    # Print CPU
    running_process = next((p for p in mlfq.roundRobinQueue + mlfq.firstComeFirstServeQueue + mlfq.shortestJobFirstQueue if p.processID == mlfq.recentRunningProcess), None)
    print(f"CPU : {running_process.processName if running_process else '[]'}")
    
    io_processes = [p.processName for p in mlfq.ioProcesses]
    print(f"I/O: {io_processes}")
    
    print() """

def print_mlfq_state(mlfq, process_list):
    print(f"At Time = {getattr(mlfq, 'currentGlobalTime', 0)}")

    rr_queue = [p.processName for p in getattr(mlfq, 'roundRobinQueue', [])]
    fcfs_queue = [p.processName for p in getattr(mlfq, 'firstComeFirstServeQueue', [])]
    sjf_queue = [p.processName for p in getattr(mlfq, 'shortestJobFirstQueue', [])]
    print(f"Queues: {rr_queue}; {fcfs_queue}; {sjf_queue}")

    running_process = next(
        (p for p in process_list if p.processID == getattr(mlfq, 'recentRunningProcess', None)), None
    )
    print(f"CPU: {running_process.processName if running_process else '[]'}")

    io_processes = [p.processName for p in getattr(mlfq, 'ioProcesses', [])]
    if io_processes:
        print(f"I/O: {io_processes}")


def print_simulation_summary(process_list):
    total_turnaround_time = 0
    print("\nSIMULATION DONE\n")

    for process in process_list:
        process.turnaroundTime = process.completionTime - process.arrivalTime
        process.waitingTime = process.turnaroundTime - process.totalBurstTime
        total_turnaround_time += process.turnaroundTime

        print(f"Turn-around time for Process {process.processName}: {process.turnaroundTime} ms")

    average_turnaround_time = total_turnaround_time / len(process_list)
    print(f"Average Turn-around time = {round(average_turnaround_time, 4)} ms\n")

    for process in process_list:
        print(f"Waiting time for Process {process.processName}: {process.waitingTime} ms")

def run_mlfq_scheduler(MLFQ, process_list):
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

                        MLFQ.recentRunningProcess = current_queue[0].processID

                    break  # Remember, queues can only be ran, one at a time, based on the priority order.

        else:
            MLFQ.recentRunningProcess = MLFQ.roundRobinQueue[0].processID

        # Print the current state of MLFQ.
        print_mlfq_state(MLFQ, process_list)

        # Increment global time.
        MLFQ.currentGlobalTime += 1

        # TODO: This stops the scheduler if at any point in time, except for at t = 0,
        # all three of the queues are empty at the same time. However, I do not know if
        # this should be the correct behavior according to the project specs.

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
    second_MLFQ = MLFQ(rr_allotment, fcfs_allotment, context_switch_time)
    run_mlfq_scheduler(second_MLFQ, process_list)

    # Parse set2.txt, use it to run the scheduler, and then output the results.
 
