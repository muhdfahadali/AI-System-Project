import sys

class VacuumCleaner:
    
        #Intializing orientation, starting point, map and variables to keep traks of plan    def __init__(self, map):
        def __init__(self, map):
            self.orientation = None     
            self.row = None             
            self.col = None             
            self.plan = []             
            self.map = map
            self.stack = []             
            self.uncleanSquares = []   

        #Move one step forward according to orientation of vacuum cleaner
        def moveForward(self):
            if self.orientation == "^":
                self.row -= 1
            elif self.orientation == ">":
                self.col += 1
            elif self.orientation == "v":
                self.row += 1
            elif self.orientation == "<":
                self.col -= 1
            self.plan.append("M")

        #Turn 90 degree right and add R to plan
        def turnRight(self):
            orientations = {"^": ">", ">": "v", "v": "<", "<": "^"}
            self.orientation = orientations[self.orientation]
            self.plan.append("R")

        #Turn 90 degree left and add L to plan
        def turnLeft(self):
            orientations = {"^": "<", ">": "^", "v": ">", "<": "v"}
            self.orientation = orientations[self.orientation]
            self.plan.append("L")


        def findPlan(self):
            
            uncleanedSquares = []
            for row in range(len(self.map)):
                for col in range(len(self.map[0])):
                    if self.map[row][col] == " ":
                        uncleanedSquares.append((row, col))
           
            while True:

                #Assign starting position to currentSquare
                currentSquare = self.map[self.row][self.col]
                if currentSquare in [" ","^","S",">","<","v"]:
                    #Mark the square as cleaned
                    self.map[self.row][self.col] = "."  
                
                uncleanedNeighbors = self.getUncleanedNeighbors()
                
                #Traverse each uncleaned square using robor orientation and move forward function
                if uncleanedNeighbors:
                    self.stack.append((self.row, self.col))
                    neighborRow, neighborCol = uncleanedNeighbors[0]
                    self.roboOrientation(neighborRow, neighborCol)
                    self.moveForward()
                    
                # If the stack is empty, all squares are cleaned
                else:
                    if not self.stack:  
                        break
                    if(len(uncleanedSquares) == 0):
                        break
                    prev_cell = self.stack.pop()
                    self.roboOrientation(prev_cell[0],prev_cell[1])
                    self.moveForward()
            
            self.uncleanSquares = []
            for row in range(len(self.map)):
                for col in range(len(self.map[0])):
                    if self.map[row][col] == " ":
                        self.uncleanSquares.append((row, col))

        def getUncleanedNeighbors(self):

            #get the cordinates of the uncleared neighbours 
            neighbors = []
            for NRow, NCol in [(-1, 0), (0, 1), (1, 0), (0, -1)]:
                neighborRow = self.row + NRow
                neighborCol = self.col + NCol
                if (
                    0 <= neighborRow < len(self.map) and
                    0 <= neighborCol < len(self.map[0]) and
                    self.map[neighborRow][neighborCol] == " "
                ):
                    neighbors.append((neighborRow, neighborCol))
            return neighbors

        def roboOrientation(self, targetRow, targetCol):

            #Turn robo right till the robo face towards target row and column
            if targetRow < self.row:
                while self.orientation != "^":
                    self.turnRight()
            elif targetRow > self.row:
                while self.orientation != "v":
                    self.turnRight()
            elif targetCol < self.col:
                while self.orientation != "<":
                    self.turnRight()
            elif targetCol > self.col:
                while self.orientation != ">":
                    self.turnRight()

#Change three time right turn with left turn
def reducePlan(plan):
    
    i = 0
    while i < len(plan) - 2:
        if plan[i] == 'R' and plan[i + 1] == 'R' and plan[i + 2] == 'R':
            plan[i:i + 3] = ['L']
            i += 1
        else:
            i += 1
    return plan

def getStartingPoint(problem):
    
    #Remove leading/trailing whitespaces and newlines
    lines = problem.strip().split("\n")

    #Extract map from the problem
    map = [list(line) for line in lines[1:-1]]

    #Find orientation and starting position
    orientation = None
    startingPos = None

    for row in range(len(map)):
        for col in range(len(map[row])):
            square = map[row][col]

            #If orientation is known
            if square in ['^', '>', 'v', '<']:
                orientation = square
                startingPos = (row, col)
                break

            #If orientation is not known
            # Suppose orientation = "^"
            elif square == 'S':
                orientation = None  
                startingPos = (row, col)
                break
            # Both starting position and orientation is unknown
            # Suppose the orientation is "^" and the starting position is the first uncleaned room encounter on the map
            # else:
            #     orientation = "^"
            #     for row in range(len(map)):
            #         for col in range(len(map[row])):
            #             square = map[row][col]
            #             if square == " ":
            #                 startingPos = (row, col)
            #                 return orientation, startingPos, map

    return orientation, startingPos, map





    # for row in range(len(map)):
    #     for col in range(len(map[0])):
    #         print("map[row][col] : ",map[row][col])
    #         #If orientation is known 
    #         if map[row][col] in ["<",">","^","v"]:
    #             orientation = map[row][col]
    #             startingPos = (row, col)
    #             return orientation, startingPos, map 

    #         #If only starting point is known
    #         elif map[row][col] in "S":
    #             print("here")
    #             startingPos = (row, col)
    #             orientation = None
    #             return None, startingPos, map 


    #         # Both starting position and orientation is unknown
    #         else:
    #             print("herea")
    #             return None, None, map
