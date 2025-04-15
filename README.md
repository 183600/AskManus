[English](README.md) | 中文 | [한국어](README_ko.md) | [日本語](README_ja.md)

[![GitHub stars](https://img.shields.io/github/stars/mannaandpoem/OpenManus?style=social)](https://github.com/mannaandpoem/OpenManus/stargazers)
&ensp;
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT) &ensp;
[![Discord Follow](https://dcbadge.vercel.app/api/server/DYn29wFk9z?style=flat)](https://discord.gg/DYn29wFk9z)

# 👋 AskManus

Based on OpenManus, this project provides:
- Installation scripts
- During user interactions, after a user inputs a message, the system may display command-line options for selection if necessary. Each option may include explanations if required .

## Installation Guide

Two installation methods are provided. **Method 2 (uv) is recommended** for faster installation and better dependency management.

### Method 1: Using Conda

1. Create a new conda environment:
```bash
conda create -n open_manus python=3.12
conda activate open_manus
```

2. Clone the repository:
```bash
git clone https://github.com/mannaandpoem/OpenManus.git
cd OpenManus
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

### Method 2: Using uv (Recommended)

1. Install uv (a fast Python package manager):
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

2. Clone the repository:
```bash
git clone https://github.com/mannaandpoem/OpenManus.git
cd OpenManus
```

3. Create and activate a virtual environment:
```bash
uv venv --python 3.12
source .venv/bin/activate  # For Unix/macOS
# For Windows:
# .venv\Scripts\activate
```

4. Install dependencies:
```bash
uv pip install -r requirements.txt
```

### Browser Automation Tools (Optional)
```bash
playwright install
```

## Configuration

To configure AskManus with an LLM API, follow these steps:

1. Create a `config.toml` file in the `config` directory (copy from the example):
```bash
cp config/config.example.toml config/config.toml
```

2. Edit `config/config.toml` to add API keys and custom settings:
```toml
# Global LLM configuration
[llm]
model = "gpt-4o"
base_url = "https://api.openai.com/v1"
api_key = "sk-..."  # Replace with your API key
max_tokens = 4096
temperature = 0.0

# Optional model-specific configurations
[llm.vision]
model = "gpt-4o"
base_url = "https://api.openai.com/v1"
api_key = "sk-..."  # Replace with your API key
```

## Quick Start

Run AskManus with a single command:
```bash
python main.py
```

Then input your queries via the terminal!

For the MCP tool version:
```bash
python run_mcp.py
```

For the experimental multi-agent version:
```bash
python run_flow.py
```

## Contribution Guidelines

Contributions of all kinds are welcome! Feel free to open an issue or submit a pull request.

**Note**: Before submitting a pull request, use `pre-commit run --all-files` to validate your changes .

## Community

## Star Count

[![Star History Chart](https://api.star-history.com/svg?repos=mannaandpoem/OpenManus&type=Date)](https://star-history.com/#mannaandpoem/OpenManus&Date)

## Acknowledgments

This project is built upon OpenManus. Special thanks to [OpenManus](https://github.com/anthropics/anthropic-quickstarts/tree/main/computer-use-demo) for foundational support!
