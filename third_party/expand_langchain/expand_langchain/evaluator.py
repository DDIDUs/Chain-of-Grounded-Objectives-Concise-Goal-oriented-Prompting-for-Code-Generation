import json
from collections import defaultdict
from math import comb
from pathlib import Path
from typing import List, Optional

import ast
import re
import numpy as np
from pydantic import BaseModel


class Evaluator(BaseModel):
    path: Path
    gt_key: str
    exec_key: str
    filter_keys: List[str] = []
    filter_weights: List[float] = []

    data: List[dict] = None

    def __init__(self, **data):
        super().__init__(**data)

        with open(self.path, "r") as f:
            self.data = json.load(f)

    def pass_ratio_at_n(self, key):
        total_p = []
        for datum in self.data:
            datum_point = []
            def extract_asserts(code_string, entry):
                assert_pattern = re.compile(r"assert .*?\n")
                a = code_string.replace('candidate', entry)
                asserts = assert_pattern.findall(a)
                return asserts
            if "def check(candidate)" in datum['gold_tc']:
                test_len = len(extract_asserts(datum['gold_tc'], datum['entry_point']))
            else:
                test_len = len(eval(datum['gold_tc']))
            test_results = datum[key][-1].count("Test Failed")
            total_p.append(((test_len-test_results)/test_len)**2)
        pass_ratio = np.mean(total_p)
        return pass_ratio
    
    def pass_ratio_at_n_plus(self, key):
        def count_inputs_elements(code_str: str) -> int:
            match = re.search(r"inputs\s*=\s*(\[[^\n]*\])", code_str)
            if not match:
                return 0
            try:
                inputs_code = match.group(1)
                safe_globals = {"inf": float("inf"), "nan": float("nan"), "__builtins__": {}}
                inputs_list = eval(inputs_code, safe_globals)
                return len(inputs_list)
            except Exception:
                return 0

        total_ratios = []

        for datum in self.data:
            test_case_count = count_inputs_elements(datum.get('plus_tc', ''))
            result_summary = datum.get(key, [])
            last_result = result_summary[-1] if result_summary else ""

            failed_count = 0
            passed_count = 0

            if last_result == "Compile Failed" or "Timeout Failed" in last_result:
                failed_count = test_case_count
            elif "Failed" in last_result:
                failed_count = last_result.count("Failed")
                matches = re.findall(r'count:\s*(\d+)', last_result)
                if matches:
                    try:
                        total_count = int(matches[-1])
                        passed_count = total_count + 1 - failed_count
                    except ValueError:
                        passed_count = 0
                else:
                    passed_count = 0
            else:
                passed_count = test_case_count

            if test_case_count > 0:
                pass_ratio_squared = (passed_count / test_case_count) ** 2
                total_ratios.append(pass_ratio_squared)

        return np.mean(total_ratios) if total_ratios else 0.0
            
    def _load_results(self, key):
        l = []
        for datum in self.data:
            passed = datum[key]
            if isinstance(passed, list):
                if isinstance(passed[0], bool):
                    l.append([[int(p)] for p in passed])
                elif isinstance(passed[0], list):
                    if len(passed[0]) == 0:
                        l.append([0 for p in passed])
                    else:
                        l.append([np.mean(p) for p in passed])
                else:
                    raise ValueError("Invalid format")
            else:
                l.append([[passed]])

        return np.array(l)

    def _run_fixed_k(
        self,
        k,
        n,
    ):
        metrics = {}

        gt_results = self._load_results(self.gt_key)  
        gt_results = gt_results.reshape(len(gt_results), -1)
        naive_pass_rate = pass_at_k(gt_results, k)
        metrics["naive"] = naive_pass_rate
        pass_ratio = self.pass_ratio_at_n(self.exec_key)
        metrics["pass-ratio"] = pass_ratio
        
        if "livecodebench" not in str(self.path):
            gt_results = self._load_results('passed_plus')  
            gt_results = gt_results.reshape(len(gt_results), -1)
            naive_pass_rate = pass_at_k(gt_results, k)
            metrics['plus_naive'] = naive_pass_rate
            pass_ratio = self.pass_ratio_at_n_plus('gold_tc_exec_result_plus_ratio')
            metrics["plus_ratio"] = pass_ratio
        return metrics

    def run(
        self,
        k: List[int],
        n: int,
    ):
        results = {}
        for _k in k:
            results[f"{self.path}"] = self._run_fixed_k(_k, n)

        return results


def probability(n, c, k):
    return 1 - comb(n - c, k) / comb(n, k)


def naive_pass_at_k(
    gt_results: List[List[int]],
    k: int,
):
    num_correct = [sum(x) for x in gt_results]
    num_samples = [len(x) for x in gt_results]
    probs = np.array([probability(n, c, k) for n, c in zip(num_samples, num_correct)])
    return probs.mean()


def pass_at_k_with_scores_per_problem(gt_results, pass_at_k, scores):
    score_mapping = defaultdict(int)
    score_count = defaultdict(int)
    for score, gt_result in zip(scores, gt_results):
        score = int(score)
        score_mapping[score] += gt_result                               # Gen_TC 테스트 결과에 대응되는 GT 결과
        score_count[score] += 1                                         # Gen_TC 테스트 결과
    score_sorted = sorted(score_count.keys(), reverse=True)
    cumsum = 0
    correct_so_far = 0
    for score in score_sorted:
        cumsum += score_count[score]
        if cumsum > pass_at_k:
            if correct_so_far:
                return 1
            else:
                n = score_count[score]
                k = score_mapping[score]
                x = pass_at_k + score_count[score] - cumsum

                if k == n:
                    return 1
                else:
                    return 1 - comb(n - k, x) / comb(n, x)
        if score_mapping[score] > 0:
            correct_so_far = 1
        if cumsum == pass_at_k:
            return correct_so_far


def pass_at_k_with_scores(
    gt_results: List[List[int]],
    k: int,
    scores: List[List[float]],
):
    prob_results = []
    for _scores, _gt_results in zip(scores, gt_results):
        prob_results.append(pass_at_k_with_scores_per_problem(_gt_results, k, _scores))

    return np.mean(prob_results)


def pass_at_k(
    gt_results: List[List[int]],
    k: int,
    scores: Optional[List[List[float]]] = None,
):
    if scores is None:
        return naive_pass_at_k(gt_results, k)
    else:
        return pass_at_k_with_scores(gt_results, k, scores)
