# CS 140 Project 1
# Good luck guys

from collections import deque

class Process:
  def __init__(self, pid, arrival_time, burst_sequence):
    self.pid = pid
    self.arrival_time = arrival_time
    self.burst_sequence = burst_sequence
    self.current_burst_index = 0  # Index of the current burst in the sequence
    self.remaining_time = burst_sequence[0] # Remaining time for the current burst
    self.queue_level = 0  # Start in the highest-priority queue
    self.is_waiting_io = False  # Whether the process is in an I/O phase

  def is_complete(self):
    return self.current_burst_index >= len(self.burst_sequence)

# Initialize queues
num_queues = 3
queues = [deque() for _ in range(num_queues)]
time_slices = [2, 4, 8]

# Sample processes with alternating CPU and I/O bursts
processes = [
  Process(pid=1, arrival_time=0, burst_sequence=[5, 3, 4, 2]),
  Process(pid=2, arrival_time=1, burst_sequence=[6, 2, 3, 1]),
  Process(pid=3, arrival_time=3, burst_sequence=[4, 6, 5]),
]

# Add processes to the highest-priority queue initially
for process in processes:
  queues[0].append(process)

current_time = 0
while any(queue for queue in queues):
  for level in range(num_queues):
    if queues[level]:
      process = queues[level].popleft()
      time_slice = time_slices[level]

      # Simulate process execution
      execution_time = min(time_slice, process.remaining_time)
      process.remaining_time -= execution_time
      current_time += execution_time

      # Check if process is complete
      if process.remaining_time > 0:
        if level < num_queues - 1:
          process.queue_level += 1
          queues[process.queue_level].append(process)
        else:
          queues[level].append(process)
      else:
        print(f"Process {process.pid} completed at time {current_time}")

      # Exit loop to re-evaluate queue priorities
      break



