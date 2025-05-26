bash process/llama3_8b/llama3_8b_test_hm.sh

bash process/llama3_8b/eval.sh

python3 main_result_summurize.py

python3 process/llama3_8b/calc_token_length.py