def simulate_scheduling():
    # Define the processes and their respective times
    processes = {
        'A': {'arrival': 0, 'burst': [4, 2, 4, 2], 'io': [4, 2]},
        'B': {'arrival': 0, 'burst': [2, 2], 'io': []},
        'C': {'arrival': 0, 'burst': [10], 'io': []},
        'D': {'arrival': 0, 'burst': [20], 'io': []}
    }

    # Initialize variables
    time = 0
    cpu = None
    io = []
    queues = [[], [], []]
    done = set()
    output = []

    # Function to print the current state
    def print_state():
        nonlocal time, cpu, io, queues
        state = f"At Time = {time}\n"
        if time == 0:
            state += "Arriving : [A, B, C, D]\n"
        state += f"Queues : {queues[0]};{queues[1]};{queues[2]}\n"
        state += f"CPU : {cpu if cpu else '[]'}\n"
        if io:
            state += f"I/O : {io}\n"
        output.append(state)

    # Main simulation loop
    while len(done) < 4:
        # Check for process completion
        if cpu and processes[cpu]['burst'][0] == 0:
            if len(processes[cpu]['burst']) == 1:
                done.add(cpu)
                output.append(f"{cpu} DONE\n")
            else:
                io.append(cpu)
                processes[cpu]['burst'].pop(0)
                processes[cpu]['io'].pop(0)
            cpu = None

        # Move processes from I/O to queues
        for p in io[:]:
            if processes[p]['io'][0] == 0:
                io.remove(p)
                queues[0].append(p)
                processes[p]['io'].pop(0)

        # Decrement burst and I/O times
        if cpu:
            processes[cpu]['burst'][0] -= 1
        for p in io:
            processes[p]['io'][0] -= 1

        # Assign CPU if available
        if not cpu and queues[0]:
            cpu = queues[0].pop(0)

        # Print the current state
        print_state()

        # Increment time
        time += 1

    # Calculate turn-around and waiting times
    turnaround_times = {}
    waiting_times = {}
    for p in processes:
        turnaround_times[p] = time - processes[p]['arrival']
        waiting_times[p] = turnaround_times[p] - sum(processes[p]['burst'])

    # Print the final results
    output.append("SIMULATION DONE\n")
    for p in processes:
        output.append(f"Turn-around time for Process {p} : {turnaround_times[p]} ms\n")
    avg_turnaround = sum(turnaround_times.values()) / len(turnaround_times)
    output.append(f"Average Turn-around time = {avg_turnaround} ms\n")
    for p in processes:
        output.append(f"Waiting time for Process {p} : {waiting_times[p]} ms\n")

    # Print the output
    for line in output:
        print(line)

# Run the simulation
simulate_scheduling()