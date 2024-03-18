import subprocess

# Take input from the user
query = input("Please type in keywords:")
query = query.replace(' ', '/')

# Run the first subprocess and capture its output
p1 = subprocess.run(["python3", "query.py", query], text=True, capture_output=True)

# Print the output from p1
out = p1.stdout
print(out)

# Assuming you have a task_name variable set correctly
task_name = "instance4"

# Prepare the command for redirection in shell by joining them into a single string
command = f"python3 mapReduce2.py tf_idf.txt -r emr -n out --output-dir=s3://cs230ans/{task_name} --instance-type c1.medium --num-core-instances 4" # 
# command = f"python3 mapReduce2.py < tf_idf.txt > ./ans/{task_name}.txt -n {out}" # --instance-type c1.medium --num-core-instances 4

# Run the second command through the shell to handle redirection
p2 = subprocess.run(command, shell=True, text=True)

# Assuming p3 refers to your final subprocess call
# For example, let's run sort_ans.py as p3 and capture its output
# download_command = f"aws s3 cp s3://cs230ans/{task_name}/part-00000 ./ans/{task_name}.txt --region us-east-2"
# p3 = subprocess.run(download_command, shell=True, text=True)

p4 = subprocess.run(["python3", "sort_ans.py", f"./ans/{task_name}.txt"], text=True, capture_output=True)

# If you need to print output from p3 or handle it, you can do so here
print()
print("Result:")
print(p4.stdout)
