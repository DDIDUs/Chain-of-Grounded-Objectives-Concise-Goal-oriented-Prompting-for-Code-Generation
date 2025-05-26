import os
import json
import subprocess
from datasets import load_dataset
import pandas as pd

def evaluate_by_difficulty(result_paths, output_table_path="summary.csv"):
    # 1. Load difficulty info
    tmp = load_dataset("livecodebench/code_generation", split="test")
    live_dict = {data['question_id']: data['difficulty'] for data in tmp}
    number = {'easy': 0, 'medium': 1, 'hard': 2}
    difficulty_keys = list(number.keys())

    summary_records = []

    for path in result_paths:
        if not os.path.exists(path):
            print(f"[!] File not found: {path}")
            continue

        print(f"\n=== Processing {path} ===")

        # Extract model and prompt
        parts = path.split('/')
        exp_name = parts[-2]  # e.g., llama3.1_70b_livecodebench_cgo
        model_parts = exp_name.split('_')
        if len(model_parts) < 3:
            print(f"[!] Unexpected experiment format: {exp_name}")
            continue

        model_name = '_'.join(model_parts[:2])      # llama3.1_70b
        prompt_name = model_parts[-1]               # cgo
        base_name = os.path.splitext(os.path.basename(path))[0]

        # Load result
        with open(path, "r") as f:
            test_results = json.load(f)

        # Split by difficulty
        new_results = [[] for _ in range(3)]
        for d in test_results:
            diff = live_dict.get(d['id'], None)
            if diff in number:
                new_results[number[diff]].append(d)

        # 결과 저장용 temp dict
        row = {"model": model_name, "prompt": prompt_name}

        for i, lst in zip(difficulty_keys, new_results):
            out_json = f"{model_name}_{prompt_name}_{i}.json"
            with open(out_json, 'w', encoding='utf-8') as json_file:
                json.dump(lst, json_file, ensure_ascii=False, indent=4)

            print(f"Evaluating {out_json} ...")
            result = subprocess.run([
                "python3", "run.py", "evaluator",
                f"--path={out_json}",
                "--gt_key=passed",
                "--exec_key=gold_tc_exec_result",
                "--filter_keys=[gen_tc_passed]",
                "--filter_weights=[1]",
                "-",
                "run",
                "--k=[1]",
                "--n=1"
            ], capture_output=True, text=True)

            # parse evaluator output
            for line in result.stdout.splitlines():
                if out_json in line:
                    try:
                        metrics = json.loads(line.split(":", 1)[1].strip())
                        for key in metrics:
                            row[f"{i}_{key}"] = round(metrics[key] * 100, 2)
                    except Exception as e:
                        print(f"[!] Failed to parse: {line}")
                    break

            os.remove(out_json)

        summary_records.append(row)

    df = pd.DataFrame(summary_records)
    print("\n=== Summary Table ===")
    print(df.to_string(index=False))
    df.to_csv(output_table_path, index=False)
    print(f"\nSaved summary to {output_table_path}")

    
if __name__ == "__main__":
    paths = [
        "results/llama3.1_70b_livecodebench_dp/results_merged_2.json",
        "results/llama3.1_70b_livecodebench_plan/results_merged_2.json",
        "results/llama3.1_70b_livecodebench_codecot/results_merged_2.json",
        "results/llama3.1_70b_livecodebench_zerocot/results_merged_2.json",
        "results/llama3.1_70b_livecodebench_pseudo/results_merged_2.json",
        "results/llama3.1_70b_livecodebench_cgo/results_merged_2.json",
    ]
    evaluate_by_difficulty(paths, output_table_path="llama_70b_diff_summary.csv")
