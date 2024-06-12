import csv

class Station:
    # station object, node in graph, contains its short name and a local schedule
    def __init__(self, station_id, line_in):
        self.id = station_id
        self.schedule = {line_in.id: line_in}


class Line:
    # schedule object, contains line number, arrival time, departure time, distance to the next station
    # and the short name of the next station. Is saved in a schedule list of a station
    def __init__(self, line_id, stops, arrival_time, departure_time, distance, next_station, current_station):
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
        return self.cost < other.cost


def graph(filename):
    # function to build the graph. Returns a dictionary of stations

    stations = {}
    file = open(filename)
    # file = open('testschedule.csv')
    reader = csv.reader(file)

    # extract the header from the schedule
    header = []
    header = next(reader)

    # extract all rows from the file, add them to a list. This way we only have to read out the file once and can then
    # build the graph from the list

    rows = []
    for row in reader:
        #print(row)
        rows.append(row)

    file.close() # closes file, as we now have all infos extracted and don't need it anymore

    for i in range(len(rows)):
        # check if station already exists. We can assume and assure station uniqueness
        if rows[i][3].strip() in stations:
            # if the station exists already, add line information to existing station
            if i < len(rows)-1:
                # special cases: last station overall and last station of a line
                if rows[i][0] == rows[i+1][0]:
                    stations[rows[i][3].strip()].schedule[rows[i][0]] = Line(rows[i][0], rows[i][2], rows[i][5],rows[i][6],int(rows[i+1][7]) - int(rows[i][7]), rows[i+1][3].strip(), rows[i][3].strip())
                else:
                    stations[rows[i][3].strip()].schedule[rows[i][0]] = Line(rows[i][0], rows[i][2],rows[i][5], rows[i][6], 0, " ", rows[i][3].strip())
            else:
                stations[rows[i][3].strip()].schedule[rows[i][0]] = Line(rows[i][0], rows[i][2],rows[i][5], rows[i][6], 0, " ", rows[i][3].strip())
        else:
            # if station doesnt exist, append new station in station list
            if i < len(rows)-1:
                # special cases: last station overall and last station of a line
                if rows[i][0] == rows[i + 1][0]:
                    stations[rows[i][3].strip()] = Station(rows[i][3].strip(), Line(rows[i][0],rows[i][2], rows[i][5], rows[i][6], int(rows[i+1][7]) - int(rows[i][7]), rows[i+1][3].strip(), rows[i][3].strip()))
                else:
                    stations[rows[i][3].strip()] = Station(rows[i][3].strip(), Line(rows[i][0],rows[i][2], rows[i][5], rows[i][6], 0, " ", rows[i][3].strip()))
            else:
                stations[rows[i][3].strip()] = Station(rows[i][3].strip(), Line(rows[i][0],rows[i][2], rows[i][5], rows[i][6], 0, " ", rows[i][3].strip()))

    return stations

