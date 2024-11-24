class Task():
    # Class to store rows of tasks inside while parsing

    def __init__(self, csv_row : list[str]):
        self.number = csv_row[0]
        self.cores = csv_row[1]
        self.turns = csv_row[2]
        self.ram = csv_row[3]
        self.complete_in_turns = csv_row[4]
    