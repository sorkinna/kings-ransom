# importing shutil module  
import shutil 
  
# Path 
path = "/home/nick/Desktop/players"
  
# Get the disk usage statistics 
# about the given path 
stat = shutil.disk_usage(path) 
  
# Print disk usage statistics 
print("Disk usage statistics:") 
print(stat)
