
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#     ___________    _____ __  ____      ____               _           __     ___  #
#    / ____/ ___/   <  / // / / __ \    / __ \_________    (_)__  _____/ /_   <  /  #
#   / /    \__ \    / / // /_/ / / /   / /_/ / ___/ __ \  / / _ \/ ___/ __/   / /   #
#  / /___ ___/ /   / /__  __/ /_/ /   / ____/ /  / /_/ / / /  __/ /__/ /_    / /    #
#  \____//____/   /_/  /_/  \____/   /_/   /_/   \____/_/ /\___/\___/\__/   /_/     #
#                                                    /___/                          #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# Members:
# Jakin Bacalla
# Naomi Amparo
# Ramon Comendador
# Shane Odhuno

#### PROJECT SPECS ####
# ASSUMPTIONS:
# All processes start in the highest priority queue with time allotments initialized accordingly.
# Context switching time is defined as an input from the user. 
# One process in the CPU can occur simultaneously with multiple I/Os. 
# At the time that a job consumes its entire time allotment, it is demoted to a lower priority queue. Otherwise, it stays in that queue. 
# Priority Boosting will not be implemented.

# ORDER OF OPERATIONS PER TIME STAMP:
# Enqueue the newly arriving process. 
# Enqueue the processes going back to the queue (returning from the CPU). 
# Enqueue the returning processes from I/O 
# Context switching into new process (if needed).
#### PROJECT SPECS ####

# ACRONYM LIST:
# MLFQ: Multi-Level Feedback Queue
# RR: Round Robin
# FCFS: First Come First Serve (i.e. First In, First Out)
# SJF: Shortest Job First
# CS: Context Switch
# RRQ: Round Robin Queue
# FCFSQ: First Come First Serve Queue
# SJF: Shortest Job First Queue

# Import helper funcs
from helpers import ( update_mlfq,
                     update_process_obj,
                     demote_process,
                     parse_input,
                     switch_processes)

# Initialize constants.
RR_TIME_QUANTUM = 4

RR_HIGH_PRIORITY = 1
FCFS_MEDIUM_PRIORITY = 2
SJF_LOW_PRIORITY = 3

NULL_QUEUE_PRIORITY = 0  # This is for processes that have completely finished.

class MLFQ:
    def __init__(self, rr_allotment, fcfs_allotment, context_switch_time):
        self.currentGlobalTime = 0 # Current time stamp
        self.recentRunningProcess = 0 # Process ID of most recently ran / running (?) process -- have to update 
        
        self.rrCPUQueue = [] # Round Robin CPU Queue -- have to update
        self.fcfsCPUQueue = [] # First Come First Serve CPU Queue -- have to update
        self.sjfCPUQueue = [] # Shortest Job First CPU Queue -- have to update
        
        self.rrIOQueue = [] # Round Robin IO Queue -- have to update
        self.fcfsIOQueue = [] # First Come First Serve IO Queue -- have to update
        self.sjfIOQueue = [] # Shortest Job First IO Queue -- have to update
        
        self.rrTimeQuantum = RR_TIME_QUANTUM # Round Robin Time Quantum
        self.rrTimeAllotment = rr_allotment # Round Robin Time Allotment
        self.fcfsTimeAllotment = fcfs_allotment # First Come First Serve Time Allotment
        
        # self.ioProcesses = [] # I/O Process Queue -- have to update
        self.contextSwitch = context_switch_time # Context switch time
        self.totalCSTime = 0 # Total time spent in context switch -- have to update

class Process:
    def __init__(self):
        self.processName = ""
        self.processID = 0
        self.arrivalTime = 0
        self.cpuTimes = [] # Update
        self.ioTimes = [] # Update
        self.usedTimeQuantum = 0 # Update
        self.usedTimeAllotment = 0 # Update
        self.totalBurstTime = 0 # Update
        self.totalIoTime = 0 # Added total I/O time (to be subtracted also in waiting time); update
        self.completionTime = 0
        self.turnaroundTime = 0 
        self.waitingTime = 0 
        self.processCSTime = 0 # Update
        self.currentQueue = RR_HIGH_PRIORITY  # All processes start at the Highest Queue: Round Robin.; update

def rr_scheduler(mlfq: MLFQ, process_list: list[Process], context_switch_time):
    rr_quantum = RR_TIME_QUANTUM
    
    # Enqueue arriving processes
    
    
    while True:
        
        # Add arriving processes to RRQ
        for process in process_list:
            if process.arrivalTime == mlfq.currentGlobalTime:
                mlfq.rrCPUQueue.append(process)
        
        # Run first process in CPU queue (run A)
        process = update_process_obj(first_process, 1, 0, 1, 0)
        
        # Update MLFQ state
        update_mlfq(mlfq, 1, 0, first_process)
        
        # Run first_process IO
        first_process = update_process_obj(first_process, 0, 1, 0, first_process.ioTimes[0])
        
        # Switch to second process
        switch_processes(first_process, mlfq, mlfq.contextSwitch)
        
        # Increment time stamp
        mlfq.currentGlobalTime += 1
        
    return mlfq, process_list

# def mlfq_scheduler(MLFQ: MLFQ, process_list: list[Process]):
#     """
#     Input: MLFQ and Process objects
#     Implements scheduling logic for all levels of MLFQ
#     """
    
#     # Run while 
    
    
#     return 0