from collections import deque

class Process:
    def __init__(self, pid, arrival_time, bursts):
        self.pid = pid
        self.arrival_time = arrival_time
        self.bursts = bursts  # List of alternating CPU and I/O bursts
        self.current_burst = 0  # Index of the current burst
        self.queue_level = 0  # Start at the highest-priority queue
        self.wait_time = 0  # Time spent waiting for CPU
        self.remaining_time = bursts[0]  # Remaining time in the current CPU burst

    def is_cpu_burst(self):
        return self.current_burst % 2 == 0  # Even indices are CPU bursts

# Initialize queues
num_queues = 3
cpu_queues = [deque() for _ in range(num_queues)]  # CPU queues for each priority level
io_queue = deque()  # I/O wait queue
time_slices = [2, 4, 8]  # Time slices for each queue

# Sample processes with alternating CPU and I/O bursts
processes = [
    Process(pid=1, arrival_time=0, bursts=[5, 3, 4]),  # CPU 5 -> I/O 3 -> CPU 4
    Process(pid=2, arrival_time=2, bursts=[3, 2, 6]),  # CPU 3 -> I/O 2 -> CPU 6
    Process(pid=3, arrival_time=4, bursts=[4, 5]),     # CPU 4 -> I/O 5
]

# Track unarrived processes
unarrived_processes = sorted(processes, key=lambda p: p.arrival_time)

current_time = 0
while any(queue for queue in cpu_queues) or io_queue or unarrived_processes:
    # Add newly arrived processes to the highest-priority queue
    while unarrived_processes and unarrived_processes[0].arrival_time <= current_time:
        arriving_process = unarrived_processes.pop(0)
        cpu_queues[0].append(arriving_process)

    # Handle I/O operations
    if io_queue:
        for process in list(io_queue):  # Iterate over a copy to allow modifications
            process.remaining_time -= 1
            if process.remaining_time <= 0:
                # Move to the next burst (CPU burst)
                process.current_burst += 1
                if process.current_burst < len(process.bursts):
                    process.remaining_time = process.bursts[process.current_burst]
                    cpu_queues[process.queue_level].append(process)
                io_queue.remove(process)

    # Check if all CPU queues are empty
    if not any(queue for queue in cpu_queues):
        # Advance time to the next event (process arrival or I/O completion)
        if unarrived_processes:
            current_time = unarrived_processes[0].arrival_time
        elif io_queue:
            current_time += 1  # Advance by 1 unit for ongoing I/O
        continue

    # Execute processes from the highest-priority non-empty CPU queue
    for level in range(num_queues):
        if cpu_queues[level]:
            process = cpu_queues[level].popleft()
            time_slice = time_slices[level]

            # Simulate process execution
            execution_time = min(time_slice, process.remaining_time)
            process.remaining_time -= execution_time
            current_time += execution_time

            # Check if CPU burst is complete
            if process.remaining_time > 0:
                # Not finished; demote or stay in the same queue
                if level < num_queues - 1:
                    process.queue_level += 1
                    cpu_queues[process.queue_level].append(process)
                else:
                    cpu_queues[level].append(process)
            else:
                # Move to the next burst (I/O or terminate)
                process.current_burst += 1
                if process.current_burst < len(process.bursts):
                    if process.is_cpu_burst():
                        process.remaining_time = process.bursts[process.current_burst]
                        cpu_queues[process.queue_level].append(process)
                    else:
                        process.remaining_time = process.bursts[process.current_burst]
                        io_queue.append(process)
                else:
                    print(f"Process {process.pid} completed at time {current_time}")

            # Exit loop to re-evaluate queue priorities
            break
