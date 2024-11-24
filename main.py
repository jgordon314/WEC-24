from Server import Server
from Task import Task
import csv 
from evaluator import eval

# Parses values from provided CSVs and runs simulation. 
def run(serverFileName : str = 'Server.csv',  taskFileName : str = 'Tasks.csv', printData : bool = False):
    servers = get_server(serverFileName)
    tasks = get_tasks(taskFileName)
    output = eval(servers, tasks, printData)
    output.write_results()

# Parse servers CSV file. 
def get_server(fileName) -> list[Server]: 
    server_list = []
    with open(fileName) as csvfile: 
        spamreader = csv.reader(csvfile)
        next(spamreader) # Skip header
        for row in spamreader: 
            server_list.append(Server(list(row)))
    return server_list

# Parse tasks CSV file. 
def get_tasks(fileName) -> list[Task]:
    task_list = []
    with open(fileName) as csvfile: 
        spamreader = csv.reader(csvfile)
        next(spamreader) # Skip header
        for row in spamreader: 
            task_list.append(Task(list(row)))
    return task_list

# Used for testing in test.py. 
def test(serverFileName : str, taskFileName : str) : 
    return run("testServers\\" + serverFileName + ".csv", "testTasks\\" + taskFileName + ".csv", True)

# Main. 
def main() : 
    run()
    
if __name__ == "__main__":
    main()