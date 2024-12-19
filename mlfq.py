# main.py
from process_model import MLFQ
from process_view import SchedulerView
from process_controller import SchedulerController

if __name__ == "__main__":
    print("# Enter Scheduler Details #")
    num_processes = int(input())
    q1_allotment = int(input())
    q2_allotment = int(input())
    context_switch = int(input())

    process_inputs = []
    print(f"# Enter {num_processes} Process Details #")
    for _ in range(num_processes):
        process_inputs.append(input())

    # Initialize MVC components
    model = MLFQ(q1_allotment, q2_allotment, context_switch)
    view = SchedulerView()
    controller = SchedulerController(model, view)

    # Load processes and simulate
    controller.load_processes(process_inputs)
    controller.simulate()
