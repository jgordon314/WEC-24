class Task():
    # Class to store rows of tasks inside while parsing

    def __init__(self, csv_row : list[str]):
        self.number = int(csv_row[0])
        self.cores = int(csv_row[1])
        self.turns = int(csv_row[2])
        self.ram = int(csv_row[3])
        self.complete_in_turns = int(csv_row[4])
        
        # Used for calculating total power used. 
        self.core_use = self.turns * self.cores

