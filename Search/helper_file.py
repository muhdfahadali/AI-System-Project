import csv
import heapq
from pathlib import Path

class CsvWriter:

    def GetFormattedConnections(connections_dict: {}) -> str:

        #Formats connections from the given dictionary and returns a formatted string.
        formatted_connections = ""
        sorted_keys = sorted(connections_dict.keys())
        for key in sorted_keys:
            conn = connections_dict[key]
            train_number = conn[0].strip().strip('\'')
            line_number = conn[1]
            conn_format = "{} : {} -> {} ; ".format(train_number, line_number[0], line_number[-1])
            formatted_connections = formatted_connections + conn_format

        conn_format_line = len(formatted_connections) - 2
        return formatted_connections[:conn_format_line]

    def PrepareCsvData(solution) -> {}:
        
        #Prepares a dictionary with data for writing to a CSV file.
        row_data = {}
        row_data["ProblemNumber"] = solution.pnr
        row_data["Connection"] = CsvWriter.GetFormattedConnections(solution.route)
        row_data["Cost"] = solution.cost
        return row_data

    def WriteCsvFile1(solution):

        #Writes solution data to a CSV file.
        file_data = CsvWriter.PrepareCsvData(solution)
        file_name = 'solutions.csv'
        field_names = ['ProblemNumber', 'Connection', 'Cost']

        if Path(file_name).is_file():
            with open(file_name, 'a', newline='') as csv_file:
                csv_writer = csv.DictWriter(csv_file, fieldnames=field_names)
                csv_writer.writerow(file_data)
        else:
            with open(file_name, 'w', newline='') as csv_file:
                csv_writer = csv.DictWriter(csv_file, fieldnames=field_names)
                csv_writer.writeheader()
                csv_writer.writerow(file_data)

class ObjectHeap:
    def initialize(self, initial=None, key=lambda x: x):

        #Initializes a heap with the given initial data and a key function.
        self.key = key
        self.index = 0
        if initial:
            self.data = [(key(item), i, item) for i, item in enumerate(initial)]
            self.index = len(self.data)
            heapq.heapify(self.data)
        else:
            self.data = []

    def push_item(self, item):
        
        #Pushes an item onto the heap.
        heapq.heappush(self.data, (self.key(item), self.index, item))
        self.index += 1

    def pop_item(self):
        
        #Pops the smallest item from the heap and returns it.
        return heapq.heappop(self.data)[2]
