import os

try:
    named_output = "model"
    os.makedirs("/workflow/outputs/{}".format(named_output), exist_ok=True)
except:
    pass

for named_output in ["processed_data"] + [f"processed_data{i}" for i in range(2, 10)]:
    try:
        with open("/workflow/outputs/{}".format(named_output), "w") as f:
            f.write("a,b,c\n1,2,3")
    except:
        pass