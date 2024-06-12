import sys
import checkPlan as cPlan
import findPlan as fPlan
import planType as ptype
import copy

class WumpusCave:
    def __init__(self,problem):
        
        #Extract problem from the input
        self.problem = problem

        #Extract Mode, Plan and map from problem
        self.mode,self.plan,self.map = ptype.getMap(self.problem)

    def solver(self):
        if self.mode == "CHECK_PLAN":
            
            #Get starting point and orientation from problem
            orientation,startingPos = cPlan.getStartingPoint(self.map)
            
            #Traverse given plan on the map
            result= cPlan.traversePlan(orientation,startingPos,self.plan,self.map)
            
            return result
        
        elif self.mode == "FIND_PLAN":
            
            #Get starting point and orientation from problem
            orientation, starting_pos, map = fPlan.getStartingPoint(self.problem)
            #Passing the Orientation map and starting point to vacuumCleaner class
            print("starting_pos : ",starting_pos)
            vacuumCleaner = fPlan.VacuumCleaner(map)
            vacuumCleaner.orientation = orientation
            if starting_pos:
                vacuumCleaner.row, vacuumCleaner.col = starting_pos
            plan=[]
            totalSquares= set()
            if orientation == None and starting_pos == None:  
                for row in range(len(map)):
                    for col in range(len(map[0])):
                        if map[row][col] == ' ':
                            totalSquares.add((row,col))
                for pos in totalSquares:
                    startingPos = pos
                    orientations = ["v"]
            
                    for orient in orientations:
                        orientation, starting_pos, map = fPlan.getStartingPoint(self.problem)
                        vacuumCleaner = fPlan.VacuumCleaner(map)
                        vacuumCleaner.orientation = orient
                        vacuumCleaner.row, vacuumCleaner.col = startingPos
                        vacuumCleaner.findPlan()
                        plan = plan + vacuumCleaner.plan
                fplan = [step for sublist in plan for step in sublist]
                vacuumCleaner.plan = fPlan.reducePlan(fplan)             
                print("all_plan : ")
            elif orientation == None:
                orientations = ["^","v","<",">"]
                all_plan = {}
                for orient in orientations:
                    orientation, starting_pos, map = fPlan.getStartingPoint(self.problem)
                    vacuumCleaner = fPlan.VacuumCleaner(map)
                    vacuumCleaner.orientation = orient
                    vacuumCleaner.row, vacuumCleaner.col = starting_pos
                    vacuumCleaner.findPlan()
                    all_plan[orient] = vacuumCleaner.plan,vacuumCleaner.orientation
                
                    all_plan[orient] = vacuumCleaner.plan,vacuumCleaner.orientation
                
                print("all_plan : ",all_plan)
                

                longest_key = max(all_plan, key=lambda k: len(all_plan[k][0]))
                print("longest_list : ",longest_key)
                
                longest_list = all_plan[longest_key]
                #result_plan = ''.join(longest_list)
                print("longest_list : ",longest_list)


            else:
               vacuumCleaner.findPlan()

            return vacuumCleaner.plan

        
        else:
            #Input format is not correct
            print("Incorrect input format") 
       



if  __name__ == '__main__':
    
    #Checking if there is Input and Output file argument given on the execution
    if len(sys.argv) < 3:
        print("Use Command: python main.py <input_file_name> <output_file_name>")
        sys.exit(1)

    #Assignning File name to Variables
    inputfile = sys.argv[1]
    outputfile = sys.argv[2]

    #Getting the problem from the input file
    try:
        with open(inputfile, "r") as file:
            problem = file.read()
    except FileNotFoundError:
            print(f"Error: file <{inputfile}> not found!")
            sys.exit(1)

    #Solving the problem 
    wc = WumpusCave(problem)
    result = wc.solver()
    result = ''.join(result)
    with open(outputfile,'w') as file:
        file.write(result)