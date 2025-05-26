# Chain of Grounded Objectives

Official implementation of the paper 'Chain-of-Grounded-Objectives: Concise-Goal-oriented-Prompting-for-Code-Generation'.

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
