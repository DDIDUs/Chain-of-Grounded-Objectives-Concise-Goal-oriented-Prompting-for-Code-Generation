# Chain of Grounded Objectives

This repository provides a framework for evaluating and benchmarking large language models (LLMs) on code generation and reasoning tasks using a modular, chain-based approach. It supports flexible configuration, experiment management, and result summarization for various models and datasets.

## Features

- Modular experiment pipeline for LLM evaluation
- Support for multiple datasets (e.g., HumanEval, MBPP, LiveCodeBench)
- Easy configuration of models and experiments via YAML files
- Automated result aggregation and summarization
- Docker support for reproducible environments

## Directory Structure

- `run.py` — Main entry point for running generators and evaluators
- `main_result_summurize.py` — Aggregates and summarizes experiment results
- `configs/` — Experiment, model, and data source configuration files
- `data/` — Datasets (e.g., `mbpp_data.json`, `humaneval_data.json`)
- `process/` — Experiment scripts and processing utilities
- `third_party/expand_langchain/` — Core framework for chaining, evaluation, and generation
- `templates/` — Prompt and evaluation templates
- `api_keys.json` — API keys and endpoint configuration

## Installation

### Requirements

- Python 3.10+

### Setup

1. **Clone the repository**
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   pip install -e third_party/expand_langchain
   pip install vllm==0.6.2
   ```

3. **Configure API keys:**  
   Edit `api_keys.json` with your API keys and endpoints.

## Usage

### Running Experiments

You can run experiments using the provided shell scripts or directly via `run.py`:

```bash
python3 run.py generator --config_path=<path_to_config.yaml> run merge_json exit
```

Example (from a script):
```bash
bash process/llama3.1_8b/llama3.1_8b_live_test.sh
```

### Summarizing Results

After running experiments, aggregate results with:
```bash
python3 main_result_summurize.py
```

## Configuration

- **Model configs:** `configs/llm/*.yaml`
- **Data source configs:** `configs/source/*.yaml`
- **Experiment configs:** See subfolders in `configs/` for each model/benchmark

## API Keys

Edit `api_keys.json` to provide your keys and endpoints:
```json
{
  "OPEN_WEBUI_API_KEY": "sk-your_key",
  "OLLAMA_BASE_URL": "your_path",
  "VLLM_BASE_URL": "your_path",
  "OPENAI_API_KEY": "sk-your_key",
  "CODEEXEC_ENDPOINT": "http://localhost:5097/execute"
}
```

## License
