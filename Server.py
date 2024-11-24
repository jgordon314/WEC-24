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

        self.tasks : set[Task] = set()

    def can_add_task(self, task : Task):
        # print(f"trying to add {task.number} with {task.cores} cores and {task.ram} ram to server with {self.max_cores - self.cores_used} cores and {self.max_ram - self.ram_used} ram]")
        return (task.cores + self.cores_used <= self.max_cores) and (task.ram + self.ram_used <= self.max_ram)
    
    # Adds a task into the server. 
    # Pre: can_add_task(task) == true 
    def add_task(self, task : Task):
        self.cores_used += task.cores
        self.ram_used += task.ram
        self.tasks.add(task)
    
    # Removes a task from the server. Requires the server to have this task. 
    def remove_task(self, task: Task):
        self.cores_used -= task.cores
        self.ram_used -= task.ram
        self.tasks.remove(task)
    
    # Finds all completed and failed tasks and removes them. 
    def remove_completed_failed_tasks(self) -> tuple[set[Task], set[Task]]:
        complete_tasks: set[Task] = set()
        failed_tasks: set[Task] = set()
        tasks_to_remove: set[Task] = set()
        
        for task in self.tasks:
            if task.turns <= 0:
                complete_tasks.add(task)
                tasks_to_remove.add(task)
                self.ram_used -= task.ram
                self.cores_used -= task.cores
            elif task.complete_in_turns <= 0:
                failed_tasks.add(task)
                tasks_to_remove.add(task)
                self.ram_used -= task.ram
                self.cores_used -= task.cores
        
        # Remove all tasks that are complete. 
        self.tasks = self.tasks.difference(tasks_to_remove)

        return (complete_tasks, failed_tasks)

    # Returns the power used by all tasks in the current turn. 
    def get_power_use(self):
        return self.watts_per_core * self.cores_used

    # Decrements each task done by one turn. 
    #   Tasks completed as a result will have their ram and memory removed. 
    def decrement_turns_remaining(self):
        # Go through all tasks and decrement them. 
        for task in self.tasks:
            task.turns -= 1
            task.complete_in_turns -= 1