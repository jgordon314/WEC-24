from Server import Server
from Task import Task
import csv 

def main():
    servers = get_server()
    tasks = get_tasks()

def get_server(): 
    server_list = []
    with open('Server.csv') as csvfile: 
        spamreader = csv.reader(csvfile)
        next(spamreader) # Skip header
        for row in spamreader: 
            server_list.append(Server(list(row)))
    return server_list

def get_tasks():
    task_list = []
    with open('Tasks.csv') as csvfile: 
        spamreader = csv.reader(csvfile)
        next(spamreader) # Skip header
        for row in spamreader: 
            task_list.append(Task(list(row)))
    return task_list


if __name__ == "__main__":
    main()