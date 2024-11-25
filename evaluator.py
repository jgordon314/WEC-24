from Server import Server
from Task import Task
from Outputter import Outputter
import time 

def eval(servers : list[Server], tasks : list[Task], printData : bool = False):
    global tasksToSkip
    # Create the output files for the program
    outputter : Outputter = Outputter()

    # Start timer 
    start = time.time()

    def getTime(task : Task) -> int:
        return task.turns
    
    orderedTasks = tasks.copy()
    orderedTasks.sort(key=getTime, reverse=True)
    tasksToSkip = orderedTasks[0:(int(len(orderedTasks)/2 - 1))]
    
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
        set_stored_tasks_to_running(servers)

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
def set_stored_tasks_to_running(servers: list[Server]) -> None:
    def getForServer(server: Server) -> list[Task]:
        def powerset(set : list[Task]) -> list[list[Task]] :
            if len(set) == 0:
                return []
            addedSet = [[set[0]]]
            for y in powerset(set[1:]):
                addedSet.append(y.copy())
                y.append(set[0])
                addedSet.append(y)
            return addedSet
        
        def score(tasks: list[Task]):
            totalTime = 0
            for task in tasks:
                totalTime += task.complete_in_turns
            return totalTime
        #sort the tasks into a list
        allTasks = []
        for task in server.running_tasks:
            allTasks.append(task)
        for task in server.stored_tasks:
            allTasks.append(task)
        if(len(allTasks) == 0):
            return []
        
        pSet = powerset(allTasks)
        maxLen = 0
        for x in pSet:
            if len(x) > maxLen:
                maxLen = len(x)
        pSet = [x for x in pSet if len(x) == maxLen]
        # gets a list of all the possible combinations of tasks where as many tasks are running as possible
        
        pSet.sort(key=score) # sorted now by lowest total run time
        return pSet[0]        
            
                
    for server in servers:
        server.setRunning(getForServer(server))

# Adds a new task into the server (either for running or for storage). 
# Returns true if the task was added and false if the task was not added. 
def add_task_to_servers(servers: list[Server], task: Task) -> bool:
    def getPower(server : Server) -> int:
            return server.watts_per_core
        
    def tooFull(servers : list[Server]) -> bool:
        full = 0
        total = 0
        for x in servers:
            total = x.max_cores 
            full = x.cores_used
        return full / total >= 0.8
    
    if(tooFull(servers)):
        if task in tasksToSkip:
            return False
        
    if(task.complete_in_turns > task.number and task.complete_in_turns != -1):
        return False
        
    
    
    # Look in order of servers sorted by least power consumed to most
    servers.sort(key=getPower)
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