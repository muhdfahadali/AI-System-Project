import subprocess

for i in range(20):
    input_file = f"example-problems/problem_f_{i:02d}.txt"
    output_file = f"solutions/solution_f_{i:02d}.txt"
    print(i)
    command = f"python main.py {input_file} {output_file}"
    subprocess.run(command, shell=True)
