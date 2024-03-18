import subprocess

# Take input from the user
query = input("Please type in keywords:")
query = query.replace(' ', '/')

# Run the first subprocess and capture its output
p1 = subprocess.run(["python3", "query.py", query], text=True, capture_output=True)

# Print the output from p1
print(p1.stdout)

# Assuming you have a task_name variable set correctly
task_name = "ans3"

# Prepare the command for redirection in shell by joining them into a single string
command = f"python3 mapReduce2.py tf_idf.txt -n out > {task_name}.txt"

# Run the second command through the shell to handle redirection
p2 = subprocess.run(command, shell=True, text=True)

# Assuming p3 refers to your final subprocess call
# For example, let's run sort_ans.py as p3 and capture its output
p3 = subprocess.run(["python3", "sort_ans.py", f"{task_name}.txt"], text=True, capture_output=True)

# If you need to print output from p3 or handle it, you can do so here
print(p3.stdout)
