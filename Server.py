class Server() :
    # Class to store server data inside while parsing
    
    def __init__(self, csv_row : list[str]):
        self.number = csv_row[0]
        self.cores = csv_row[1]
        self.watts = csv_row[2]
        self.ram = csv_row[3]