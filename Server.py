from Task import Task

class Server() :
    # Class to store server data inside while parsing
    
    def __init__(self, csv_row : list[str]):
        self.number = int(csv_row[0])
        self.max_cores = int(csv_row[1])
        self.watts_per_core = int(csv_row[2])
        self.max_ram = int(csv_row[3])

        self.cores_used = 0
        self.ram_used = 0

        self.running_tasks : set[Task] = set()
        self.stored_tasks : set[Task] = set()

    def can_run_task(self, task : Task):
        # print(f"trying to add {task.number} with {task.cores} cores and {task.ram} ram to server with {self.max_cores - self.cores_used} cores and {self.max_ram - self.ram_used} ram]")
        return (task.cores + self.cores_used <= self.max_cores) and (task.ram + self.ram_used <= self.max_ram)
    
    def can_store_task(self, task : Task):
        return task.ram + self.ram_used <= self.max_ram
    
    # Checks to see if can move a task that was stored to now be running.
    #   Assumes the task is in the server.
    def can_move_stored_to_running(self, task: Task):
        return task.cores + self.cores_used <= self.max_cores

    # Adds a task into the server. 
    # Pre: can_run_task(task) == true 
    def run_task(self, task : Task):
        self.cores_used += task.cores
        self.ram_used += task.ram
        self.running_tasks.add(task)
    
    # Stores a task in the server RAM. 
    # Pre: can_store_task(task) == true 
    def store_task(self, task: Task):
        self.ram_used += task.ram
        self.stored_tasks.add(task)

    # Moves a task that was previously stored to now be running.
    # Pre: can_move_stored_to_running(task) == true 
    def move_stored_task_to_running(self, task: Task):
        self.cores_used += task.cores
        self.stored_tasks.remove(task)
        self.running_tasks.add(task)

    # Removes a task from the server. Requires the server to have this task. 
    def remove_task(self, task: Task):
        self.cores_used -= task.cores
        self.ram_used -= task.ram
        self.running_tasks.remove(task)
    
    # Finds all completed and failed tasks and removes them. 
    def remove_completed_failed_tasks(self) -> tuple[set[Task], set[Task]]:
        complete_tasks: set[Task] = set()
        failed_tasks: set[Task] = set()
        running_tasks_to_remove: set[Task] = set()
        stored_tasks_to_remove : set[Task] = set()

        for task in self.running_tasks:
            if task.turns <= 0:
                complete_tasks.add(task)
                running_tasks_to_remove.add(task)
                self.ram_used -= task.ram
                self.cores_used -= task.cores
            elif task.complete_in_turns <= 0:
                failed_tasks.add(task)
                running_tasks_to_remove.add(task)
                self.ram_used -= task.ram
                self.cores_used -= task.cores
        for task in self.stored_tasks:
            if task.complete_in_turns < task.turns:
                failed_tasks.add(task)
                stored_tasks_to_remove.add(task)
                self.ram_used -= task.ram

        # Remove all tasks that are complete or failed. 
        self.running_tasks = self.running_tasks.difference(running_tasks_to_remove)
        self.stored_tasks = self.stored_tasks.difference(stored_tasks_to_remove)

        return (complete_tasks, failed_tasks)

    # Returns the power used by all tasks in the current turn. 
    def get_power_use(self):
        return self.watts_per_core * self.cores_used

    # Decrements each task done by one turn. 
    #   Tasks completed as a result will have their ram and memory removed. 
    def decrement_turns_remaining(self):
        # Go through all tasks and decrement them. 
        for task in self.running_tasks:
            task.turns -= 1
            task.complete_in_turns -= 1
        for task in self.stored_tasks:
            task.complete_in_turns -= 1