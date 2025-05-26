import json
import os
import numpy as np
import pandas as pd
from transformers import AutoTokenizer

humaneval_8b_paths = [
    'results/llama3_8b_humaneval_cgo/results_merged_2.json',
    'results/llama3_8b_humaneval_plan/results_merged_2.json',
    'results/llama3_8b_humaneval_codecot/results_merged_2.json',
    'results/llama3_8b_humaneval_zerocot/results_merged_2.json',
    'results/llama3_8b_humaneval_pseudo/results_merged_2.json',
]

KEY_MAP = {
    "cgo": lambda d, t: len(t.tokenize(d['cgo'][-1])),
    "plan": lambda d, t: len(t.tokenize(d['plan'][-1])),
    "cot": lambda d, t: len(t.tokenize(d['cot'][-1])),
    "code_raw": lambda d, t: len(t.tokenize(d['code_raw'][-1])),
    "pseudo+requirements": lambda d, t: len(t.tokenize(d['pseudo'][-1])) + len(t.tokenize(d['requirements'][-1]))
}

def get_model_name(path):
    if "llama3.1" in path:
        size = "8B" if "8b" in path else "70B"
        return f"meta-llama/Meta-Llama-3.1-{size}-Instruct"
    else:
        size = "8B" if "8b" in path else "70B"
        return f"meta-llama/Meta-Llama-3-{size}-Instruct"

def extract_key(path):
    if "pseudo" in path:
        return "pseudo+requirements"
    elif "plan" in path:
        return "plan"
    elif "codecot" in path:
        return "cot"
    elif "zerocot" in path:
        return "code_raw"
    elif "cgo" in path:
        return "cgo"
    else:
        raise ValueError(f"Unknown strategy in path: {path}")

def extract_benchmark(path):
    if "humaneval" in path:
        return "HumanEval"
    elif "live" in path:
        return "LiveCodeBench"
    else:
        return "Unknown"

def extract_model(path):
    if "8b" in path:
        return "LLaMA3-8B"
    elif "70b" in path:
        return "LLaMA3-70B"
    else:
        return "UnknownModel"

def compute_avg_token_length(path):
    model_name = get_model_name(path)
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    key = extract_key(path)

    with open(path, "r") as f:
        data = json.load(f)
        lengths = [KEY_MAP[key](entry, tokenizer) for entry in data]

    return np.mean(lengths)

def compute_all(paths):
    records = []
    for path in paths:
        avg_len = compute_avg_token_length(path)
        record = {
            "Benchmark": extract_benchmark(path),
            "Model": extract_model(path),
            "Prompt": extract_key(path),
            "AvgTokenLen": avg_len
        }
        records.append(record)
    return records

all_paths = (
    humaneval_8b_paths
)

results = compute_all(all_paths)
df = pd.DataFrame(results)
pivot_df = df.pivot_table(index=["Benchmark", "Model"], columns="Prompt", values="AvgTokenLen")
os.makedirs('avg_tokens', exist_ok=True)
pivot_df.to_csv("avg_tokens/llama3_8b_token_length.csv", float_format="%.2f")

print(pivot_df)
