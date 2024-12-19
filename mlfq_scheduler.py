class Process:
    def __init__(self, name, arrival_time, cpu_bursts, io_bursts):
        self.name = name
        self.arrival_time = arrival_time
        self.cpu_bursts = cpu_bursts  # List of CPU burst times
        self.io_bursts = io_bursts  # List of IO burst times
        self.turnaround_time = 0
        self.waiting_time = 0
        self.current_queue = 0  # Priority level (0 = highest priority)
        self.remaining_time = cpu_bursts[0] if cpu_bursts else 0
        self.completed = False

class Queue:
    def __init__(self, scheduling_algorithm, time_allotment=None):
        self.processes = []
        self.scheduling_algorithm = scheduling_algorithm  # RR, FCFS, SJF
        self.time_allotment = time_allotment

    def enqueue(self, process):
        self.processes.append(process)

    def dequeue(self):
        if self.scheduling_algorithm == "RR":
            return self.processes.pop(0)
        elif self.scheduling_algorithm == "FCFS":
            return self.processes.pop(0)
        elif self.scheduling_algorithm == "SJF":
            self.processes.sort(key=lambda p: p.remaining_time)
            return self.processes.pop(0)

    def is_empty(self):
        return len(self.processes) == 0

class Scheduler:
    def __init__(self, queues):
        self.queues = queues  # List of Queue objects
        self.current_time = 0
        self.completed_processes = []

    def add_process(self, process):
        self.queues[0].enqueue(process)

    def simulate(self):
        while any(queue.processes for queue in self.queues):
            for i, queue in enumerate(self.queues):
                if not queue.is_empty():
                    current_process = queue.dequeue()
                    time_slice = queue.time_allotment if queue.time_allotment else current_process.remaining_time
                    execution_time = min(time_slice, current_process.remaining_time)

                    # Simulate execution
                    self.current_time += execution_time
                    current_process.remaining_time -= execution_time

                    if current_process.remaining_time == 0:
                        self.complete_process(current_process)
                    else:
                        if i + 1 < len(self.queues):
                            self.queues[i + 1].enqueue(current_process)
                        else:
                            queue.enqueue(current_process)  # Stay in the same queue if no lower priority queue exists

    def complete_process(self, process):
        process.completed = True
        process.turnaround_time = self.current_time - process.arrival_time
        process.waiting_time = process.turnaround_time - sum(process.cpu_bursts)
        self.completed_processes.append(process)

class View:
    @staticmethod
    def display_simulation_state(time, queues):
        print(f"Time {time}")
        for i, queue in enumerate(queues):
            queue_processes = [p.name for p in queue.processes]
            print(f"Queue {i + 1}: {', '.join(queue_processes)}")

    @staticmethod
    def display_results(completed_processes):
        print("\nSummary")
        for process in completed_processes:
            print(f"Process {process.name}: Turnaround Time = {process.turnaround_time}, Waiting Time = {process.waiting_time}")

class Controller:
    def __init__(self):
        self.queues = [
            Queue("RR", time_allotment=8),
            Queue("RR", time_allotment=16),
            Queue("FCFS")
        ]
        self.scheduler = Scheduler(self.queues)

    def run(self):
        processes = self.get_user_input()
        for process in processes:
            self.scheduler.add_process(process)

        while any(queue.processes for queue in self.queues):
            View.display_simulation_state(self.scheduler.current_time, self.queues)
            self.scheduler.simulate()

        View.display_results(self.scheduler.completed_processes)

    def get_user_input(self):
        print("Enter process details (name, arrival time, CPU bursts, IO bursts):")
        processes = []
        while True:
            user_input = input("Process: ")
            if not user_input:
                break
            details = user_input.split(",")
            name = details[0]
            arrival_time = int(details[1])
            cpu_bursts = list(map(int, details[2::2]))
            io_bursts = list(map(int, details[3::2]))
            processes.append(Process(name, arrival_time, cpu_bursts, io_bursts))
        return processes

if __name__ == "__main__":
    controller = Controller()
    controller.run()
