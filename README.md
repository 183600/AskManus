[English](README.md) | Chinese | [한국어](README_ko.md) | [日本語](README_ja.md)

&ensp;
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT) &ensp;
[![Discord Follow](https://dcbadge.vercel.app/api/server/uXjhv3Jp9s?style=flat)](https://discord.gg/uXjhv3Jp9s)

# 👋 AskManus

An AI Agent based on OpenManus, providing:
- Installation scripts
- During user conversations, after the user speaks, if necessary, several options will pop up in the command line for the user to choose from, and each option will include an explanation if needed.

## Installation Guide

We offer two installation methods. Method 2 (uv) is recommended as it provides faster installation speed and better dependency management.

### Method 1: Using conda

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
source .venv/bin/activate  # Unix/macOS systems
# For Windows systems, use:
# .venv\Scripts\activate
```

4. Install dependencies:

```bash
uv pip install -r requirements.txt
```

### Browser Automation Tool (Optional)
```bash
playwright install
```

## Configuration Instructions

AskManus requires configuration of the LLM API. Follow these steps to set it up:

1. Create a `config.toml` file in the `config` directory (you can copy from the example):

```bash
cp config/config.example.toml config/config.toml
```

2. Edit `config/config.toml` to add API keys and customize settings:

```toml
# Global LLM configuration
[llm]
model = "gpt-4o"
base_url = "https://api.openai.com/v1"
api_key = "sk-..."  # Replace with a real API key
max_tokens = 4096
temperature = 0.0

# Optional specific LLM model configuration
[llm.vision]
model = "gpt-4o"
base_url = "https://api.openai.com/v1"
api_key = "sk-..."  # Replace with a real API key
```

## Quick Start

Run AskManus with one command:

```bash
python main.py
```

Then input your ideas through the terminal!

To use the MCP tool version, run:
```bash
python run_mcp.py
```

To experience the unstable multi-agent version, run:

```bash
python run_flow.py
```

## Contribution Guidelines

We welcome any friendly suggestions and valuable contributions! You can directly create an issue or submit a pull request.

**Note**: Before submitting a pull request, please use the pre-commit tool to check your changes. Run `pre-commit run --all-files` to perform the checks.

## Communication
- [Discord](https://discord.gg/uXjhv3Jp9s)
- [QQ Group](http://qm.qq.com/cgi-bin/qm/qr?_wv=1027&k=1XmdWxsfaDbgwq6oowemjjibzwml-bPO&authKey=1YifslbduQQmNTPH3XmXEPlH1zNM5wKd2djP3TIIXBr5UWPem5ULaNzS7mqBcOSe&noverify=0&group_code=725104480)

## Acknowledgments

This project is based on OpenManus. Special thanks to [OpenManus](https://github.com/anthropics/anthropic-quickstarts/tree/main/computer-use-demo) for providing the foundational support for this project!
