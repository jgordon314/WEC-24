from Server import Server
from Task import Task
from Outputter import Outputter
import time 

def eval(servers : list[Server], tasks : list[Task], printData : bool = False):
    # Create the output files for the program
    outputter : Outputter = Outputter()

    # Start timer 
    start = time.time()

    turn = 1
    while True:
        # 1. Remove completed/failed tasks from the servers and put them in Output.csv. Update server resources available. 
        for server in servers:
            (completed, failed) = server.remove_completed_failed_tasks()
            for task in completed:
                outputter.add_output_row(turn, task.number, 1, task.cumulative_core_use * server.watts_per_core, server.number)
                outputter.add_simulation_row("Task", time.time() - start, turn, task.number, "Completed")
            for task in failed:
                outputter.add_output_row(turn, task.number, 0, task.cumulative_core_use * server.watts_per_core, server.number)
                outputter.add_simulation_row("Task", time.time() - start, turn, task.number, "Failed")

        # Move any stored tasks into running. 
        move_stored_tasks_to_running(servers)

        # 2. Read the next row in Tasks.csv for a new task to send to a server
        if (len(tasks) != 0):
            task = tasks.pop(0)

            outputter.add_simulation_row("Task", time.time() - start, turn, task.number, "Read")

            # 3. Once a task is read, it must be assigned to a server in the same turn or marked as failed.
            if not add_task_to_servers(servers, task):
                # 4b. If cannot be assigned to server, task fails and is written as a failure. 
                outputter.add_output_row(turn, task.number, 0, 0, 0) # Failed task. 
                outputter.add_simulation_row("Task", time.time() - start, turn, task.number, "Failed")
        
        # Output status of every servrer. 
        for server in servers: 
            outputter.add_simulation_row("Server", time.time() - start, turn, server.number, server.cores_used, server.ram_used)

        # Updating time tasks have ran.     
        for server in servers:
            server.decrement_turns_remaining()
            # for task in server.tasks:
                # print(task.turns)
        turn += 1

        # Checking to see if complete. 
        if (complete(servers, tasks)):
            # print(f"finished at {turn}")
            if printData:
                print(outputter.output_file_contents)
                print(outputter.simulation_file_contents)
            return outputter

# Moves any tasks that are stored to now be running. 
def move_stored_tasks_to_running(servers: list[Server]) -> None:
    tasks_to_move = []
    for server in servers: 
        for task in server.stored_tasks:
            if server.can_move_stored_to_running(task):
                tasks_to_move.append(task)
    for task in tasks_to_move:
        if task in server.stored_tasks:
            server.move_stored_task_to_running(task)

# Adds a new task into the server (either for running or for storage). 
# Returns true if the task was added and false if the task was not added. 
def add_task_to_servers(servers: list[Server], task: Task) -> bool:
    for server in servers:
        # 4a. Assign to server.
        if server.can_run_task(task):
            # print(f"assigning {task.number} to {server.number}")
            server.run_task(task)
            return True
        elif server.can_store_task(task):
            server.store_task(task)
            return True
    return False

# Returns true if we are done handling all tasks. 
def complete(servers: list[Server], tasks: list[Task]) -> bool:
    if len(tasks) != 0:
        return False
    for server in servers:
        if len(server.running_tasks) != 0:
            return False
    return True