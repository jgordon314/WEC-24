import main
import random
import evaluator
import Server
import Task
import time

def test_given():
    assert main.test("given", "given") == None

def test_cracked():
    totalTime = 0
    totalPower = 0
    totalTasks = 0
    totalTurns = 0
    totalTasksCompleted = 0
    for w in range(0, 100):
        serverList = []
        taskList = []
        for x in range(0, random.randint(10, 100)):
            serverList.append(Server.Server([
                x,
                random.randint(10, 256),
                random.randint(0, 60),
                random.randint(0,2048)
            ]))
            for y in range(0, random.randint(1, 10)):
                taskList.append(Task.Task([
                    str(y + x*100 + 1),
                    random.randint(0, 100),
                    random.randint(0, 100),
                    random.randint(0, 1024),
                    -1 if random.randint(0, 4)==0 else random.randint(x, 100 * x) # -1 about 1/4 of the time
                ]))
        result = evaluator.eval(serverList, taskList)
        finalSimContents = result.simulation_file_contents[-1]
        totalTime += finalSimContents[1]
        totalPower += result.output_file_contents[-1][3]
        totalTurns += finalSimContents[2]
        for x in result.output_file_contents:
            totalTasks += 1
            totalTasksCompleted += x[2]
            
    print(f"Average completion rate: {(totalTasksCompleted/totalTasks * 100)}%")
    print(f"Average turns per completed task: {(totalTurns/totalTasksCompleted)}"%)
    print(f"Average power per completed task: %f"%(totalPower/totalTasksCompleted))
    print(f"Average runtime per total tasks: %f"%(totalTime/totalTasks))
        

        
if __name__ == "__main__":
    for x in [test_given, test_cracked]:
        print(x.__name__ + "\n")
        x()
        print("----------------------------------------------------")