from Server import Server
from Task import Task
import csv 

def main():
    servers = get_server()
    tasks = get_tasks()

    print(servers)
    print(tasks)

def get_server(): 
    csv_table = []
    with open('Server.csv') as csvfile: 
        spamreader = csv.reader(csvfile)
        next(spamreader) # Skip header
        for row in spamreader: 
            csv_table.append(list(row))
    return csv_table

def get_tasks():
    csv_table = []
    with open('Tasks.csv') as csvfile: 
        spamreader = csv.reader(csvfile)
        next(spamreader) # Skip header
        for row in spamreader: 
            csv_table.append(list(row))
    return csv_table


if __name__ == "__main__":
    main()