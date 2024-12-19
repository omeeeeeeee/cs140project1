# view.py
class SchedulerView:
    @staticmethod
    def display_time(time):
        print(f"\nAt Time = {time} ms")

    @staticmethod
    def display_event(event):
        print(event)

    @staticmethod
    def display_queue_state(queues):
        for i, queue in enumerate(queues):
            queue_state = [p.name for p in queue.processes]
            print(f"Queue Q{i + 1}: {queue_state if queue_state else '[]'}")

    @staticmethod
    def display_cpu_state(cpu_process):
        print(f"CPU: {cpu_process.name if cpu_process else '[]'}")

    @staticmethod
    def display_io_state(io_processes):
        io_state = [p.name for p in io_processes]
        print(f"I/O: {', '.join(io_state) if io_state else '[]'}")

    @staticmethod
    def display_statistics(finished_processes):
        print("\nSimulation Completed!")
        for process in finished_processes:
            print(f"Turnaround Time for {process.name}: {process.total_turnaround_time} ms")
        avg_turnaround = sum(p.total_turnaround_time for p in finished_processes) / len(finished_processes)
        print(f"Average Turnaround Time: {avg_turnaround:.2f} ms")
