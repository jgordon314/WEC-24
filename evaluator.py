from Server import Server
from Task import Task
from Outputter import Outputter

def eval(servers : list[Server], tasks : list[Task], printData : bool):
    # Create the output files for the program
    outputter : Outputter = Outputter()

    turn = 1
    while True:
        # 1. Remove completed/failed tasks from the servers and put them in Output.csv. Update server resources available. 
        for server in servers:
            (completed, failed) = server.remove_completed_failed_tasks()
            for task in completed:
                outputter.add_output_row(turn, 1, task.core_use * server.watts_per_core, server.number)
            for task in failed:
                outputter.add_output_row(turn, 0, task.core_use * server.watts_per_core, server.number)

        # 2. Read the next row in Tasks.csv for a new task to send to a server
        if (len(tasks) != 0):
            task = tasks.pop(0)

            # 3. Once a task is read, it must be assigned to a server in the same turn or marked as failed.
            for server in servers:
                # 4a. Assign to server.
                if server.can_add_task(task):
                    # print(f"assigning {task.number} to {server.number}")
                    server.add_task(task)
                    task = None
                    break
            
            # 4b. If cannot be assigned to server, task fails and is written as a failure. 
            if task != None:
                # print(f"unable to add task {task.number} to server")
                outputter.add_output_row(turn, 0, 0, 0) # Failed task. 

        # Updating time tasks have ran.     
        for server in servers:
            server.decrement_turns_remaining()
            # for task in server.tasks:
                # print(task.turns)
        turn += 1

        # Checking to see if complete. 
        if (complete(servers, tasks)):
            # print(f"finished at {turn}")
            print(outputter.output_file_contents)
            print(outputter.simulation_file_contents)
            return outputter
    

def complete(servers: list[Server], tasks: list[Task]) -> bool:
    if len(tasks) != 0:
        return False
    for server in servers:
        if len(server.tasks) != 0:
            return False
    return True