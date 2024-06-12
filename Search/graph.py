import csv

class Station:
    def __init__(self, station_id, line_in):
        # Initialize a Station object with a unique ID and an initial line in its schedule
        self.id = station_id
        self.schedule = {line_in.id: line_in}

class Line:
    def __init__(self, line_id, stops, arrival_time, departure_time, distance, next_station, current_station):
        # Initialize a Line object with schedule information
        self.id = line_id
        self.cost = 0
        self.stop = stops
        self.arrival = arrival_time
        self.departure = departure_time
        self.distance = distance
        self.nextStation = next_station
        self.currentStation = current_station
        self.day = 0
        self.visited = False

    def __lt__(self, other):
        # Implement less than comparison for Line objects based on their cost attribute
        return self.cost < other.cost

def Graph(filename):
    
    # Build a graph of stations and their schedules from a CSV file
    stations = {}  
    
    # Dictionary to store stations
    file = open(filename)  
    
    reader = csv.reader(file) 

    header = []   
    header = next(reader)  
    
    rows = []  
    for row in reader:
        rows.append(row)

    file.close()  

    for i in range(len(rows)):

        # Check if the station already exists
        if rows[i][3].strip() in stations:
            
            # Add line information to an existing station
            if i < len(rows)-1:
                
                # Special cases: last station overall and last station of a line
                if rows[i][0] == rows[i+1][0]:
                    stations[rows[i][3].strip()].schedule[rows[i][0]] = Line(rows[i][0], rows[i][2], rows[i][5], rows[i][6], int(rows[i+1][7]) - int(rows[i][7]), rows[i+1][3].strip(), rows[i][3].strip())
                else:
                    stations[rows[i][3].strip()].schedule[rows[i][0]] = Line(rows[i][0], rows[i][2],rows[i][5], rows[i][6], 0, " ", rows[i][3].strip())
            else:
                
                stations[rows[i][3].strip()].schedule[rows[i][0]] = Line(rows[i][0], rows[i][2],rows[i][5], rows[i][6], 0, " ", rows[i][3].strip())
        else:
            
            # If the station doesn't exist, append a new station in the station list
            if i < len(rows)-1:
                
                # Special cases: last station overall and last station of a line
                if rows[i][0] == rows[i + 1][0]:
                    stations[rows[i][3].strip()] = Station(rows[i][3].strip(), Line(rows[i][0],rows[i][2], rows[i][5], rows[i][6], int(rows[i+1][7]) - int(rows[i][7]), rows[i+1][3].strip(), rows[i][3].strip()))
                else:
                    stations[rows[i][3].strip()] = Station(rows[i][3].strip(), Line(rows[i][0],rows[i][2], rows[i][5], rows[i][6], 0, " ", rows[i][3].strip()))
            else:
                stations[rows[i][3].strip()] = Station(rows[i][3].strip(), Line(rows[i][0],rows[i][2], rows[i][5], rows[i][6], 0, " ", rows[i][3].strip()))

    return stations
