from Task import Task

class Server() :
    # Class to store server data inside while parsing
    
    def __init__(self, csv_row : list[str]):
        self.number = csv_row[0]
        self.max_cores = csv_row[1]
        self.watts_per_core = csv_row[2]
        self.max_ram = csv_row[3]

        self.cores_used = 0
        self.ram_used = 0

        self.tasks : set[Task] = set()

    def can_add_task(self, task : Task):
        return (task.cores + self.cores_used <= self.max_cores) and (task.ram + self.ram_used > self.max_ram)
    
    # Adds a task into the server. 
    #   Returns true if the task was able to be added, otherwise return false. 
    def add_task(self, task : Task):
        if self.can_add_task(task):
            self.cores_used += task.cores
            self.ram_used += task.ram
            self.tasks.add(task)
            return True
        else:
            return False
    
    # Removes a task from the server. Requires the server to have this task. 
    def remove_task(self, task: Task):
        self.cores_used -= task.cores
        self.ram_used -= task.ram
        self.tasks.remove(task)
    
    # Returns the power used by all tasks in the current turn. 
    def get_power_use(self):
        return self.watts_per_core * self.cores_used

    # Decrements each task done by one turn. 
    #   Tasks completed as a result will have their ram and memory removed. 
    def update(self):
        
        complete_tasks: set[Task] = set()

        # Go through all tasks and decrement them. 
        for task in self.tasks:
            task.turns -= 1
            if task.turns == 0:
                complete_tasks.add(task)
                self.ram_used -= task.ram
                self.cores_used -= task.cores

        # Remove all tasks that are complete. 
        self.tasks = self.tasks.difference(complete_tasks)