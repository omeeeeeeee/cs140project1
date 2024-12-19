# model.py
class Process:
    def __init__(self, name, arrival_time, bursts):
        self.name = name
        self.arrival_time = arrival_time
        self.bursts = bursts  # List of alternating CPU and I/O bursts
        self.remaining_burst_index = 0
        self.total_turnaround_time = 0
        self.total_waiting_time = 0
        self.queue_time = 0  # Tracks time in the current queue
        self.completed = False

class Queue:
    def __init__(self, time_allotment=None):
        self.processes = []
        self.time_allotment = time_allotment  # None for non-RR queues

    def enqueue(self, process):
        self.processes.append(process)

    def dequeue(self):
        return self.processes.pop(0) if self.processes else None

    def is_empty(self):
        return len(self.processes) == 0

class MLFQ:
    def __init__(self, q1_time_allotment, q2_time_allotment, context_switch_time):
        self.queues = [
            Queue(None), # Arriving processes
            Queue(q1_time_allotment),
            Queue(q2_time_allotment),
            Queue(None),  # SJF, no time allotment
            Queue(None) # Finished processes
        ]
        self.context_switch_time = context_switch_time
        self.time = 0
        self.cpu_process = None
        self.io_processes = []

    def add_process(self, process):
        self.queues[0].enqueue(process)
