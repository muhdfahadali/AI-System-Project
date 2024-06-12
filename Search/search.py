import copy
import csv
import graph
import heapq
from helper_file import CsvWriter

class problem:
    def __init__(self, pnr, fr, to, stt, cf):
        self.id = pnr
        self.startnode = fr
        self.endnode = to
        # we get the starttime as a string and have to convert it into the time format
        self.starttime = stt
        self.costfunction = cf

    @staticmethod
    def cost(linear: str) -> []:
        values = linear.split()
        costs_value = [0, 0, 0, 0, 0, 0]
        costs = ["stops", "changes", "price", "arrivaltime", "distance", "duration"]
        if values[0] != "linear":
            i = costs.index(values[0])
            costs_value[i] = 1
            return costs_value
        symbols = set("+*-/")
        index = 1
        word = None
        word_value = 0
        for i in range(1, len(values)):
            value = values[i]
            if value not in symbols and value not in costs:
                word_value = int(value)
            elif value in costs:
                i = costs.index(value)
                costs_value[i] = word_value
                word_value = 0
            else:
                continue

        return costs_value

    @staticmethod
    def time_to_sec(times: []) -> int:
        hours = times[0].strip().strip('\'')
        minutes = times[1].strip().strip('\'')
        seconds = times[2].strip().strip('\'')

        return (((int(hours) * 60) + int(minutes)) * 60) + int(seconds)

    @staticmethod
    def duration_counter(arrivaltime: str, departuretime: str):
        arr_l = arrivaltime.split(':')
        dep_l = departuretime.split(':')
        day_lowest = 0  # in sec
        day_heighest = 86400  # in sec

        arr_time_sec = problem.time_to_sec(arr_l)
        dep_time_sec = problem.time_to_sec(dep_l)

        if arr_time_sec < dep_time_sec:
            duration = (day_heighest - dep_time_sec) + (arr_time_sec - day_lowest)
            return duration
        else:
            return arr_time_sec - dep_time_sec

    @staticmethod
    def day_change(arrivaltime: str, departuretime: str):
        arr_l = arrivaltime.split(':')
        dep_l = departuretime.split(':')


        arr_time_sec = problem.time_to_sec(arr_l)
        dep_time_sec = problem.time_to_sec(dep_l)

        if arr_time_sec < dep_time_sec:
            return 1
        else:
            return 0

    @staticmethod
    def arrivaltime (day: int, arrivaltime: str):
        if day == 0:
            return arrivaltime.strip().strip('\'')
        elif day < 10:
            return '0' + str(day) + ':' + arrivaltime.strip().strip('\'')
        else:
            return str(day) + ':' + arrivaltime.strip().strip('\'')

class solution:
    def __init__(self, pn, time, stnode):
        self.pnr = pn
        self.currentnode = stnode
        self.currentline = ' '
        self.prevline = ' '
        self.route = {}
        self.rnr = 0
        self.cost = 0
        self.visited = {stnode}
        self.day = 0
        self.currenttime = time
        self.done = False

        # route format: list of (line nr, station nr)

class dnode:
    def __init__(self, id, lin, nlin, cos, pre, da, arrival):
        self.id = id
        self.line = lin
        self.nextline = nlin
        self.cost = cos
        self.prev = pre
        self.day = da
        self.arrivaltime = arrival
        self.lines = {}

class dline:
    def __init__(self, lid, co, sid, nid, sol):
        self.id = lid
        self.cost = co
        self.station = sid
        self.nextStation = nid
        self.solution = sol

    def __lt__(self, other):
        return self.cost < other.cost


def dsearch(problem, network):

    'initialisation'
    # extract cost multipliers
    costs = problem.cost(problem.costfunction)

    stops = costs[0]
    changes = costs[1]
    price = costs[2]
    arrivaltime = costs[3]
    distance = costs[4]
    duration = costs[5]

    # initialise lists, dicts and heap
    visitednodes = {}
    routelines = []

    workedlines = []

    lineheap = []

    line = ' '
    cost = 0
    prev = ' '

    # initialise connections from the startnode
    # we make special abbrivated dijkstra nodes for the dijkstra network
    # in case a node a several possible incoming routes with the same cost, we save several possible solutions
    initsolution = solution(problem.id, problem.starttime, problem.startnode)
    visitednodes[problem.startnode] = dnode(problem.startnode, line, ' ', cost, prev, 0, problem.starttime)

    for x in network[problem.startnode].schedule:
        w = network[problem.startnode].schedule[x]
        if w.nextStation != ' ':
            worksolution = copy.deepcopy(initsolution)
            linecost = visitednodes[problem.startnode].cost + stops*1  + price*1

            'time cost calculations'
            linecost += duration*problem.duration_counter(network[w.nextStation].schedule[w.id].arrival, w.departure)

            linecost += arrivaltime*problem.duration_counter(w.departure, problem.starttime)
            linecost += arrivaltime*problem.duration_counter(network[w.nextStation].schedule[w.id].arrival, w.departure)

            day = problem.day_change(w.departure, problem.starttime)

            # we make special dijkstra lines, like with the nodes
            # in each line, a solution object is saved. Since we look at each line at most once, this allows us to
            # build the solution on the fly
            worksolution.day = day
            worksolution.cost = linecost
            worksolution.currentline = w.id
            worksolution.currenttime = network[w.nextStation].schedule[w.id].arrival
            worksolution.visited.add(problem.startnode)
            worksolution.route[0] = (w.id, [w.stop])
            worksolution.route[0][1].append(network[w.nextStation].schedule[w.id].stop)

            newline = dline(w.id, linecost, w.currentStation, w.nextStation, worksolution)

            visitednodes[problem.startnode].lines[w.id] = newline

            heapq.heappush(lineheap, newline)

            network[problem.startnode].schedule[x].cost = linecost
            workedlines.append(newline)

    while(True):

        'Dijkstra loop'

        # pop a line with lowest cost from the heap, and get the line from the actual network
        workline = heapq.heappop(lineheap)
        netline = network[workline.station].schedule[workline.id]

        if netline.nextStation == problem.endnode:
            'if the line reaches the goal, we can directly use the solution saved in the workline object'

            solved = workline.solution

            # if we are only interested in the arrival time, we change the cost to the right format
            if arrivaltime == 1 and duration == 0 and price == 0 and distance == 0 and stops == 0 and changes == 0:
                solved.cost = problem.arrivaltime(solved.day, solved.currenttime)
                # print("Solution found for: " + problem.id + ", Cost: " + solved.cost)
            else:
                # print("Solution found for: " + problem.id + ", Cost: " + str(solved.cost))
                pass

            for x in workedlines:
                'reset the cost of all network schedule objects, just to be save'
                network[x.station].schedule[x.id].cost = 0

            return solved

        elif netline.nextStation not in workline.solution.visited:

            'Dijkstra update if a specific line between to nodes in the network has not been used yet'
            # set the line in the network to visited, so that we don't use it again
            #network[workline.station].schedule[workline.id].visited = True

            for x in network[netline.nextStation].schedule:

                # extract all lines to consider from the schedule of the next station
                w = network[netline.nextStation].schedule[x]

                if w.nextStation != ' ':

                    # calculation of the simple costs
                    newcost = workline.cost + stops + price * 1

                    if w.id != workline.id:
                        newcost += changes + price * 1

                    'time management'
                    # calculates duration (on train) and travel time (incl. waiting times)

                    traveltime = problem.duration_counter(network[w.nextStation].schedule[x].arrival, w.departure)
                    traveltime += problem.duration_counter(w.departure, network[netline.nextStation].schedule[workline.id].arrival)

                    newcost += duration * traveltime
                    newcost += arrivaltime * traveltime

                    if newcost < w.cost or w.cost == 0:

                        worksolution = copy.deepcopy(workline.solution)
                        # update the line object in the network with the lowest cost
                        network[netline.nextStation].schedule[x].cost = newcost
                        # counting days in case of waiting and traveling time having day changes
                        newday = workline.solution.day
                        newday += problem.day_change(w.departure, network[netline.nextStation].schedule[workline.id].arrival)
                        newday += problem.day_change(network[w.nextStation].schedule[w.id].arrival, w.departure)

                        # copy and update the solution and add it to a new line object, which is pushed to the heap
                        worksolution.visited.add(w.currentStation)
                        worksolution.currenttime = network[w.nextStation].schedule[w.id].arrival
                        worksolution.day = newday
                        worksolution.cost = newcost

                        if worksolution.currentline != w.id:
                            worksolution.rnr += 1
                            worksolution.route[worksolution.rnr] = (w.id, [w.stop])
                            worksolution.route[worksolution.rnr][1].append(network[w.nextStation].schedule[w.id].stop)
                        else:
                            worksolution.route[worksolution.rnr][1].append(network[w.nextStation].schedule[w.id].stop)

                        worksolution.prevline = worksolution.currentline
                        worksolution.currentline = w.id

                        newline = dline(w.id, newcost, w.currentStation, w.nextStation, worksolution)

                        'node and line update'
                        if netline.nextStation not in visitednodes:
                            # if we haven't visited a station yet, or come across a lower cost, we simply reinit it
                            newnode = dnode(netline.nextStation, workline.id, newline, newcost, netline.currentStation, newday, network[netline.nextStation].schedule[netline.id].arrival)
                            visitednodes[netline.nextStation] = newnode

                        visitednodes[netline.nextStation].lines[workline.id] = newline

                        heapq.heappush(lineheap, newline)
                        workedlines.append(newline)


def main():
    network = graph.graph()

    problems = []

    file = open('priceproblem1.csv')
    reader = csv.reader(file)

    #extract the header from the problem file
    header = []
    header = next(reader)

    rows = []
    for row in reader:
        rows.append(row)

    file.close()

    for x in rows:
        # add all problems from `problems.csv`
        problems.append(problem(x[0], x[2], x[3], x[4], x[5]))

    for x in problems:
        # we only have to take the first solution from the search
        # write one solution at a time on `solutions.csv`
        solution = dsearch(x, network)
        CsvWriter.WriteCsvFile(solution)

    print("Execution complete. Please check solutions.csv for answers!")


if __name__ == "__main__":
    main()