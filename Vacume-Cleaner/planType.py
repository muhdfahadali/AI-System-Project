import sys

#Get the type of problem from the input string
def getType(problem):
    mode = problem.split("\n")[0]
    if mode == "CHECK PLAN":
        return "CHECK_PLAN"
    elif mode == "FIND PLAN":
        return "FIND_PLAN"
    else:
        return "Problem UnIdentified"


def getMap(problem):
    mode = getType(problem)
    
    #If mode is CHECK PLAN then extract Plan and Map
    if mode == "CHECK_PLAN":

        #Extract plan from the problem
        plan = problem.split("\n")[1]
        
        #Extract map from the problem
        map_str = problem.split("\n")[2:]
        
        #Convert map to 2D Array
        map=[]
        for i in map_str:
            map.append(list(i))

        return mode,plan,map
    
    #If mode is CHECK PLAN then extract Map
    elif mode == "FIND_PLAN":

        #Extract plan from the problem
        plan = None

        #Extract map from the problem
        map_str = problem.split("\n")[1:]
        
        #Convert map to 2D Array
        map=[]
        for i in map_str:
            map.append(list(i))

        return mode,plan,map
    
    #Un Identified Problem no mode, plan and map
    else:
        mode = None
        plan = None
        map  = None
        return mode,plan,map
    