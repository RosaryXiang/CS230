import subprocess
import sys

# Take input from the user
query = input("Please type in keywords:")
query = query.replace(' ', '/')

p1 = subprocess.run(["python3", "query.py", query], text=True, capture_output=True)

out = p1.stdout
out = out.strip()
print(out)

# task_name = str(sys.argv[1])+"_pre_"+str(sys.argv[2])

command = f"python3 mapReduce2.py < tf_idf.txt > target.txt -n {out}" # 
# command = f"python3 mapReduce2.py < tf_idf.txt > ./ans/{task_name}.txt -n {out}" # --instance-type c1.medium --num-core-instances 4

print(command)
p2 = subprocess.run(command, shell=True, text=True)

# download_command = f"aws s3 cp s3://cs230ans/{task_name} ./ans/{task_name} --recursive --region us-east-2"
# p3 = subprocess.run(download_command, shell=True, text=True)

# add_command = f"find ./ans/{task_name} -type f -name \"part*\" | xargs cat >> target.txt"
# p5 = subprocess.run(add_command, shell=True, text=True)

p4 = subprocess.run(["python3", "sort_ans.py", "target.txt"], text=True, capture_output=True)

print()
print("Result:")
print(p4.stdout)
