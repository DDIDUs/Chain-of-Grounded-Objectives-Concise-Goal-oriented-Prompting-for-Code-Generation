python3 run.py generator \
    --config_path=configs/LLaMA/LLaMA3.1/LiveCodeBench/70B/llama3.1_70b_livecodebench_cgo.yaml \
    - run \
    - merge_json \
    - exit
python3 run.py generator \
    --config_path=configs/LLaMA/LLaMA3.1/LiveCodeBench/70B/llama3.1_70b_livecodebench_plan.yaml \
    - run \
    - merge_json \
    - exit
python3 run.py generator \
    --config_path=configs/LLaMA/LLaMA3.1/LiveCodeBench/70B/llama3.1_70b_livecodebench_dp.yaml \
    - run \
    - merge_json \
    - exit
python3 run.py generator \
    --config_path=configs/LLaMA/LLaMA3.1/LiveCodeBench/70B/llama3.1_70b_livecodebench_codecot.yaml \
    - run \
    - merge_json \
    - exit
python3 run.py generator \
    --config_path=configs/LLaMA/LLaMA3.1/LiveCodeBench/70B/llama3.1_70b_livecodebench_zerocot.yaml \
    - run \
    - merge_json \
    - exit
python3 run.py generator \
    --config_path=configs/LLaMA/LLaMA3.1/LiveCodeBench/70B/llama3.1_70b_livecodebench_pseudo.yaml \
    - run \
    - merge_json \
    - exit