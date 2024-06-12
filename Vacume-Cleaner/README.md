# Clean the Wumpus cave

This program takes an input for the vacuum cleaner and checks if the mode is `CHECK PLAN` or `FIND PLAN`. If it's `CHECK PLAN`, it simulates the cleaner movements according to the plan. If it's `FIND PLAN`, then it takes care all the cases given starting position and orientation, given only starting position, and given none of the starting position/orientation and find the plan steps to clean the wumpus cave and for `CHECK PLAN` it takes into consideration all cases, given starting position and orientation, given only starting position, and given none of the starting position/orientation.  


## Usage

To run the program, use the following command:

py main.py <input_file> <output_file>
py main.py problem.txt solution.txt


## Input Format

The input file should contain the following:

- The first line contains `CHECK PLAN` or `FIND PLAN`.
- The second line contains the `PLAN STEPS` if the mode is `CHECK PLAN`, Accepted plan inputs are:
       - `M`, Moves one step in the facing direction.
       - `L`, Turns 90° to the Left.
       - `R`, Turns 90° to the Right.
- The next lines contain the grid itself, with `X` indicating a Walls and ` ` indicating squares, `^` for UP or `v` for DOWN or `<` for LEFT or `>` for RIGHT (Facing Directions). Or `S` for STARTING_POSITION


## Output Format

The output file will contain the following:

- If the mode is `CHECK PLAN`, the out put will be either `GOOD PLAN` or `BAD PLAN` in addition the position of each missed square.
- If the mode is `FIND PLAN`, the out put will be the Plan steps to clean the the wumpus cave.