import json
import re
import pandas as pd
from collections import defaultdict
import os

with open("eval_log.txt", "r") as f:
    lines = f.readlines()

data = defaultdict(lambda: defaultdict(dict))

for line in lines:
    if ':' not in line:
        continue
    path, json_part = line.strip().split(":", 1)
    try:
        metrics = json.loads(json_part)
    except json.JSONDecodeError:
        continue

    match = re.search(r"results/([^/]+)/", path)
    if match:
        name = match.group(1)
        parts = name.split("_")
        if len(parts) < 3:
            continue
        model = "_".join(parts[:-2])
        benchmark = parts[-2]
        method = parts[-1]

        for k, v in metrics.items():
            try:
                if k == "naive":
                    k_new = "pass@1"
                elif k == "pass-ratio":
                    k_new = "pass-ratio@1"
                else:
                    k_new = k

                v = round(v * 100, 2)
                col = f"{benchmark}_{k_new}"
                data[model][method][col] = v
            except TypeError:
                continue  

os.makedirs("main_results", exist_ok=True)

for model, method_data in data.items():
    df = pd.DataFrame.from_dict(method_data, orient="index").reset_index()
    df.rename(columns={"index": "Method"}, inplace=True)
    df.to_csv(f"main_results/{model}.csv", index=False)
    os.remove("eval_log.txt")
    print(f"Saved: main_results/{model}.csv")
