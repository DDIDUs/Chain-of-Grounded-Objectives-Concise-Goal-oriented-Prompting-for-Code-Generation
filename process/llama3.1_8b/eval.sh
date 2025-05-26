for dir in results/llama3.1_8b_*/; do
    json_file="${dir}results_merged_2.json"
    if [ -f "$json_file" ]; then
        python3 run.py evaluator \
            --path="$json_file" \
            --gt_key=passed \
            --exec_key=gold_tc_exec_result_ratio \
            --filter_keys=[gen_tc_passed] \
            --filter_weights=[1] \
            - run \
            --k=[1] \
            --n=1 >> eval_log.txt 2>&1
    fi
done