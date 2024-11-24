import csv 

def main():
    csv_table = get_csv()
    print(csv_table)

def get_csv(): 
    csv_table = []
    with open('Server.csv') as csvfile: 
        spamreader = csv.reader(csvfile)
        for row in spamreader: 
            csv_table.append(list(row))
    return csv_table



if __name__ == "__main__":
    main()