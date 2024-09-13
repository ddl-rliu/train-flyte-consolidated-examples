import os

named_output = "model"
os.mkdir("/workflow/outputs/{}".format(named_output)) 

named_output = "processed_data"
with open("/workflow/outputs/{}".format(named_output), "w") as f:
    f.write("a,b,c\n1,2,3")