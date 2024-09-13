import os

named_output = "model"
os.makedirs("/workflow/outputs/{}".format(named_output), exist_ok=True)

for named_output in ["processed_data", "processed_data_out", "processed_data_out2"]:
    with open("/workflow/outputs/{}".format(named_output), "w") as f:
        f.write("a,b,c\n1,2,3")