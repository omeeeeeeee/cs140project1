from process_model import Process

# controller.py
class SchedulerController:
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def load_processes(self, process_inputs):
        for input_line in process_inputs:
            name, arrival, *bursts = input_line.split(';')
            arrival = int(arrival)
            bursts = list(map(int, bursts))
            self.model.add_process(Process(name, arrival, bursts))

    def simulate(self):
        while not all(queue.is_empty() for queue in self.model.queues) or self.model.cpu_process:
            self.view.display_time(self.model.time)

            # Handle arriving processes, enqueue them
            self.handle_arrivals()

            # Process CPU and I/O bursts
            self.handle_cpu()
            self.handle_io()

            # Print queue and CPU states
            self.view.display_queue_state(self.model.queues)
            self.view.display_cpu_state(self.model.cpu_process)
            self.view.display_io_state(self.model.io_processes)

            # Increment time
            self.model.time += 1

        self.view.display_statistics(self.model.finished_processes)

    def handle_arrivals(self):
        while self.model.queues[0].processes and self.model.queues[0].processes[0].arrival_time == self.model.time:
            process = self.model.queues[0].dequeue()
            self.model.queues[1].enqueue(process)

    def handle_cpu(self):
        pass

    def handle_io(self):
        # Logic for I/O bursts
        pass
