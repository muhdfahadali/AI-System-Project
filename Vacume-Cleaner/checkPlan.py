def getStartingPoint(map):
    for row in range(len(map)):
        for col in range(len(map[0])):
            
            #If orientation is known 
            if map[row][col] in "<>^v":
                orientation = map[row][col]
                startingPos = (row, col)
                return orientation, startingPos 

            #If only starting point is known
            elif map[row][col] in "sS":
                orientation = None
                startingPos = (row, col)
                return orientation, startingPos 

    #If both orientation and starting point is unknown    
    orientation = None
    startingPos = None
    return orientation, startingPos 


def traversePlan(orientation,startingPos,plan,map):
    
    totalSquares = set()
    

    #get total no of squares from map except walls
    for row in range(len(map)):
        for col in range(len(map[0])):
            if map[row][col] != 'X' :
                totalSquares.add((row,col))

    #Check Plan if Orientation and Starting point both is known
    if (orientation != None) and (startingPos != None):

        #Add starating point to visited and cleared square
        visitedSquares = set()
        clearedPos = startingPos
        visitedSquares.add(clearedPos)
        
        #Traversing Plan
        for step in plan:
            #if step is move [M] than on the bases of orientation calculate next position and update visitedSquares
            if step == "M":
                if orientation == "^":
                    nextPos = (clearedPos[0]-1,clearedPos[1])
                elif orientation == "v":
                    nextPos = (clearedPos[0]+1,clearedPos[1])
                elif orientation == "<":
                    nextPos = (clearedPos[0],clearedPos[1]-1)
                elif orientation == ">":
                    nextPos = (clearedPos[0],clearedPos[1]+1)
                if (0 <= nextPos[0] < len(map) ) and (0 <= nextPos[1] < len(map[0])) and (map[nextPos[0]][nextPos[1]] != "X"):
                    clearedPos = nextPos
                    visitedSquares.add(clearedPos)

            #if step is turn Right [R] than turn 90 degree right and update orientation
            if step == "R":
                if orientation == "^":
                    orientation = ">"
                elif orientation == "v":
                    orientation = "<"
                elif orientation == "<":
                    orientation = "^"
                elif orientation == ">":
                    orientation = "v"
              
            #if step is turn left [L] than turn 90 degree left and update orientation
            if step == "L":
                if orientation == "^":
                    orientation = "<"
                elif orientation == "v":
                    orientation = ">"
                elif orientation == "<":
                    orientation = "v"
                elif orientation == ">":
                    orientation = "^"
                
        #Compare total and visited squares
        #last_visited = next(iter(visitedSquares))
        last_visited = list(visitedSquares)[-1]

        if totalSquares == visitedSquares:
            output = "GOOD PLAN"
            #return output,last_visited, None, None
            return output
        else:
            output = "BAD PLAN\n"
            dirtySquare = totalSquares - visitedSquares
            for square in dirtySquare:
                output += f"{square[1]}, {square[0]}\n"  # Corrected coordinate order
            #print("dirtySquare 1: ",output, dirtySquare)
            #return output, clearedPos, visitedSquares, dirtySquare
            return output
    #Check Plan if Orientation is unknown and Starting point is known
    elif (orientation == None) and (startingPos != None):

        orientations = ["^","<",">","v"] 
        totalDirtySquares = set()

        #Traversing Plan by using each orientation
        for orientation in orientations:
            dirtySquare = set()

            #Add starating point to visited and cleared square
            visitedSquares = set()
            clearedPos = startingPos
            visitedSquares.add(clearedPos)
            
            #Traversing Plan
            for step in plan:
                #if step is move [M] than on the bases of orientation calculate next position and update visitedSquares
                if step == "M":
                    if orientation == "^":
                        nextPos = (clearedPos[0]-1,clearedPos[1])
                    elif orientation == "v":
                        nextPos = (clearedPos[0]+1,clearedPos[1])
                    elif orientation == "<":
                        nextPos = (clearedPos[0],clearedPos[1]-1)
                    elif orientation == ">":
                        nextPos = (clearedPos[0],clearedPos[1]+1)
                    if (0 <= nextPos[0] < len(map) ) and (0 <= nextPos[1] < len(map[0])) and (map[nextPos[0]][nextPos[1]] != "X"):
                        clearedPos = nextPos
                        visitedSquares.add(clearedPos)

                #if step is turn Right [R] than turn 90 degree right and update orientation
                if step == "R":
                    if orientation == "^":
                        orientation = ">"
                    elif orientation == "v":
                        orientation = "<"
                    elif orientation == "<":
                        orientation = "^"
                    elif orientation == ">":
                        orientation = "v"
                
                #if step is turn left [L] than turn 90 degree left and update orientation
                if step == "L":
                    if orientation == "^":
                        orientation = "<"
                    elif orientation == "v":
                        orientation = ">"
                    elif orientation == "<":
                        orientation = "v"
                    elif orientation == ">":
                        orientation = "^"

            #Get dirty square which are not visited    
            dirtySquare = totalSquares - visitedSquares

            #Add dirty squares for each orientation to total dirty squares
            totalDirtySquares |= dirtySquare

        #Check total dirty squares equal to zero
        if len(totalDirtySquares) == 0:
            return "GOOD PLAN"
        else:
            output = "BAD PLAN\n"
            #return f"BAD PLAN \n {totalDirtySquares}"
            for square in totalDirtySquares:
                output += f"{square[1]}, {square[0]}\n"  # Corrected coordinate order
            return output
    #Check Plan if Orientation and Starting point both is known
    else:
        
        orientations = ["^","<",">","v"]
        totalDirtySquares = set()

        # Traverse every square as starting point
        
        for i in range(len(map)):
            for j in range(len(map[0])):
                if map[i][j] != "X":
                    startingPos = (i, j)
                    dirtySquare = set()
        
                    #Traversing Plan by using each orientation and for each square
                    for orientation in orientations:
                        
                        #Add starating point to visited and cleared square
                        visitedSquares = set()
                        clearedPos = startingPos
                        visitedSquares.add(clearedPos)
                        
                        #Traversing Plan
                        for step in plan:
                            #if step is move [M] than on the bases of orientation calculate next position and update visitedSquares
                            if step == "M":
                                if orientation == "^":
                                    nextPos = (clearedPos[0]-1,clearedPos[1])
                                elif orientation == "v":
                                    nextPos = (clearedPos[0]+1,clearedPos[1])
                                elif orientation == "<":
                                    nextPos = (clearedPos[0],clearedPos[1]-1)
                                elif orientation == ">":
                                    nextPos = (clearedPos[0],clearedPos[1]+1)
                                if (0 <= nextPos[0] < len(map) ) and (0 <= nextPos[1] < len(map[0])) and (map[nextPos[0]][nextPos[1]] != "X"):
                                    clearedPos = nextPos
                                    visitedSquares.add(clearedPos)

                            #if step is turn Right [R] than turn 90 degree right and update orientation
                            if step == "R":
                                if orientation == "^":
                                    orientation = ">"
                                elif orientation == "v":
                                    orientation = "<"
                                elif orientation == "<":
                                    orientation = "^"
                                elif orientation == ">":
                                    orientation = "v"
                            
                            #if step is turn left [L] than turn 90 degree left and update orientation
                            if step == "L":
                                if orientation == "^":
                                    orientation = "<"
                                elif orientation == "v":
                                    orientation = ">"
                                elif orientation == "<":
                                    orientation = "v"
                                elif orientation == ">":
                                    orientation = "^"
                            
                        #Get dirty square which are not visited    
                        dirtySquare |= totalSquares - visitedSquares

                    #Add dirty squares for each orientation to total dirty squares
                    totalDirtySquares |= dirtySquare
                        
        #Check total dirty squares equal to zero
        if len(totalDirtySquares) == 0:
            return "GOOD PLAN"
        else:
            output = "BAD PLAN\n"
            #return f"BAD PLAN \n {totalDirtySquares}"
            for square in totalDirtySquares:
                output += f"{square[1]}, {square[0]}\n"  # Corrected coordinate order
            return output
    

    
