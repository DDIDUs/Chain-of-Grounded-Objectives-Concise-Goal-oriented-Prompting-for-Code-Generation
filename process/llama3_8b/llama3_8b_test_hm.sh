#HumanEval
python3 run.py generator \
    --config_path=configs/LLaMA/LLaMA3/HumanEval/8B/llama3_8b_humaneval_cgo.yaml \
    - run \
    - merge_json \
    - exit
python3 run.py generator \
    --config_path=configs/LLaMA/LLaMA3/HumanEval/8B/llama3_8b_humaneval_plan.yaml \
    - run \
    - merge_json \
    - exit
python3 run.py generator \
    --config_path=configs/LLaMA/LLaMA3/HumanEval/8B/llama3_8b_humaneval_dp.yaml \
    - run \
    - merge_json \
    - exit
python3 run.py generator \
    --config_path=configs/LLaMA/LLaMA3/HumanEval/8B/llama3_8b_humaneval_codecot.yaml \
    - run \
    - merge_json \
    - exit
python3 run.py generator \
    --config_path=configs/LLaMA/LLaMA3/HumanEval/8B/llama3_8b_humaneval_zerocot.yaml \
    - run \
    - merge_json \
    - exit
python3 run.py generator \
    --config_path=configs/LLaMA/LLaMA3/HumanEval/8B/llama3_8b_humaneval_pseudo.yaml \
    - run \
    - merge_json \
    - exit

#MBPP
python3 run.py generator \
    --config_path=configs/LLaMA/LLaMA3/MBPP/8B/llama3_8b_mbpp_dp.yaml \
    - run \
    - merge_json \
    - exit
python3 run.py generator \
    --config_path=configs/LLaMA/LLaMA3/MBPP/8B/llama3_8b_mbpp_cgo.yaml \
    - run \
    - merge_json \
    - exit
python3 run.py generator \
    --config_path=configs/LLaMA/LLaMA3/MBPP/8B/llama3_8b_mbpp_codecot.yaml \
    - run \
    - merge_json \
    - exit
python3 run.py generator \
    --config_path=configs/LLaMA/LLaMA3/MBPP/8B/llama3_8b_mbpp_plan.yaml \
    - run \
    - merge_json \
    - exit
python3 run.py generator \
    --config_path=configs/LLaMA/LLaMA3/MBPP/8B/llama3_8b_mbpp_pseudo.yaml \
    - run \
    - merge_json \
    - exit
python3 run.py generator \
    --config_path=configs/LLaMA/LLaMA3/MBPP/8B/llama3_8b_mbpp_zerocot.yaml \
    - run \
    - merge_json \
    - exit