class Outputter():
    # Class to store output results 

    def __init__(self, outputFileName : str = 'Output.csv',  simulationFileName : str = 'Simuation.csv'):
        self.output_file_name = outputFileName
        self.simulation_file_name = simulationFileName

        self.output_file_contents = []
        self.simulation_file_contents = []

    def add_output_row(self, turn: int, status: int, total_power: int, server_number: int):
        self.output_file_contents.append([turn, status, total_power, server_number])
    
    def add_simulation_row(self, update_type: str, timestamp: float, turn: int, server_task_number: int, action_cores, ram: int = 0):
        if (update_type == "Task"): 
            self.simulation_file_contents.append([update_type, timestamp, turn, server_task_number, action_cores])

        elif (update_type == "Server"):
            self.simulation_file_contents.append([update_type, timestamp, turn, server_task_number, action_cores, ram])

        else: 
            print("Tried to add simulation row for non-server and non-task.")