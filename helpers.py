       
from mlfq_2 import ( MLFQ, 
                    Process, 
                    RR_HIGH_PRIORITY, 
                    FCFS_MEDIUM_PRIORITY, 
                    SJF_LOW_PRIORITY )

def update_mlfq(mlfq: MLFQ, run_cpu: bool, run_io: bool, process: Process):
    """
    Update state of MLFQ based on current level and running process
    """
    # Update recent running process
    mlfq.recentRunningProcess = process.processName
    
    # Update CPU queues
    if run_cpu:
        if process.currentQueue == RR_HIGH_PRIORITY:
            # Update RRQ CPU Queue
            mlfq.rrCPUQueue.pop(mlfq.rrCPUQueue.index(process.processName))
        elif process.currentQueue == FCFS_MEDIUM_PRIORITY:
            # Update FCFS CPU Queue
            mlfq.fcfsCPUQueue.pop(mlfq.fcfsCPUQueue.index(process.processName))
        elif process.currentQueue == SJF_LOW_PRIORITY:
            # Update SJF CPU Queue
            mlfq.sjfCPUQueue.pop(mlfq.sjfCPUQueue.index(process.processName))
            
    # Update IO queues
    elif run_io:
        if process.currentQueue == RR_HIGH_PRIORITY:
            # Update RRQ IO Queue
            mlfq.rrIOQueue.pop(mlfq.rrIOQueue.index(process.processName))
        elif process.currentQueue == FCFS_MEDIUM_PRIORITY:
            # Update FCFS IO Queue
            mlfq.fcfsIOQueue.pop(mlfq.fcfsIOQueue.index(process.processName))
        elif process.currentQueue == SJF_LOW_PRIORITY:
            # Update SJF IO Queue
            mlfq.sjfIOQueue.pop(mlfq.sjfIOQueue.index(process.processName))
        
    return mlfq

def switch_processes(first_process: Process, mlfq: MLFQ, context_switch_time: int):
    """
    Handle context switches
    Update CS time of process and MLFQ 
    """
    
    # Q: Do we need the second process?
    first_process.processCSTime += context_switch_time
    mlfq.totalCSTime += context_switch_time
    
    return first_process, mlfq
    

def demote_process(process: Process):
    """
    Updates current queue of process when demoted
    """
    proc_curr_queue = process.currentQueue
    
    if proc_curr_queue == RR_HIGH_PRIORITY:
        proc_curr_queue = FCFS_MEDIUM_PRIORITY
        
    elif proc_curr_queue == FCFS_MEDIUM_PRIORITY:
        proc_curr_queue = SJF_LOW_PRIORITY
        
    return process
        
def update_process_obj(process: Process, 
                       run_cpu: bool, 
                       run_io: bool, 
                       cpu_time_spent: int, 
                       io_time_spent: int):
    
    """
    Updates process object
    """
    
    process_cpu_time_list = process.cpuTimes
    process_io_time_list = process.ioTimes
    
    # If running in CPU
    if run_cpu:
        # Update CPU time list
        if process_cpu_time_list[0] == 0:
            process_cpu_time_list.pop(0)
        
        process_cpu_time_list[0] -= cpu_time_spent
        
        # Update used time allotment
        process.usedTimeAllotment += cpu_time_spent
        
        # Update total burst time of process 
        process.totalBurstTime += cpu_time_spent
    
    # If running in I/O    
    elif run_io:
        # Update IO time list
        if process_io_time_list[0] == 0:
            process_io_time_list.pop(0)
            
        process_io_time_list[0] -= io_time_spent
        
        # Update total IO time
        process.totalIoTime += io_time_spent
        
    return process

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