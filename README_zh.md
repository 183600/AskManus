[English](README.md) | 中文 | [한국어](README_ko.md) | [日本語](README_ja.md)

[![GitHub stars](https://img.shields.io/github/stars/mannaandpoem/OpenManus?style=social)](https://github.com/mannaandpoem/OpenManus/stargazers)
&ensp;
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT) &ensp;
[![Discord Follow](https://dcbadge.vercel.app/api/server/DYn29wFk9z?style=flat)](https://discord.gg/DYn29wFk9z)

# 👋 AskManus

一个基于OpenManus的AI Agent，提供：
- 安装脚本
- 用户对话时，用户说了一句话之后，如果有必要，会在命令行中弹出几个选项供用户选择，同时每个选项如果有必要，都会附带解释

## 安装指南

我们提供两种安装方式。推荐使用方式二（uv），因为它能提供更快的安装速度和更好的依赖管理。

### 方式一：使用 conda

1. 创建新的 conda 环境：

```bash
conda create -n open_manus python=3.12
conda activate open_manus
```

2. 克隆仓库：

```bash
git clone https://github.com/mannaandpoem/OpenManus.git
cd OpenManus
```

3. 安装依赖：

```bash
pip install -r requirements.txt
```

### 方式二：使用 uv（推荐）

1. 安装 uv（一个快速的 Python 包管理器）：

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

2. 克隆仓库：

```bash
git clone https://github.com/mannaandpoem/OpenManus.git
cd OpenManus
```

3. 创建并激活虚拟环境：

```bash
uv venv --python 3.12
source .venv/bin/activate  # Unix/macOS 系统
# Windows 系统使用：
# .venv\Scripts\activate
```

4. 安装依赖：

```bash
uv pip install -r requirements.txt
```

### 浏览器自动化工具（可选）
```bash
playwright install
```

## 配置说明

AskManus 需要配置使用的 LLM API，可按以下步骤设置：

1. 在 `config` 目录创建 `config.toml` 文件（可从示例复制）：

```bash
cp config/config.example.toml config/config.toml
```

2. 编辑 `config/config.toml` 添加 API 密钥和自定义设置：

```toml
# 全局 LLM 配置
[llm]
model = "gpt-4o"
base_url = "https://api.openai.com/v1"
api_key = "sk-..."  # 替换为真实 API 密钥
max_tokens = 4096
temperature = 0.0

# 可选特定 LLM 模型配置
[llm.vision]
model = "gpt-4o"
base_url = "https://api.openai.com/v1"
api_key = "sk-..."  # 替换为真实 API 密钥
```

## 快速启动

一行命令运行 AskManus：

```bash
python main.py
```

然后通过终端输入你的创意！

如需使用 MCP 工具版本，可运行：
```bash
python run_mcp.py
```

如需体验不稳定的多智能体版本，可运行：

```bash
python run_flow.py
```

## 贡献指南

我们欢迎任何友好的建议和有价值的贡献！可以直接创建 issue 或提交 pull request。

**注意**: 在提交 pull request 之前，请使用 pre-commit 工具检查您的更改。运行 `pre-commit run --all-files` 来执行检查。

## 交流群

## Star 数量

[![Star History Chart](https://api.star-history.com/svg?repos=mannaandpoem/OpenManus&type=Date)](https://star-history.com/#mannaandpoem/OpenManus&Date)

## 致谢

本项目基于OpenManus,特别感谢 [OpenManus](https://github.com/anthropics/anthropic-quickstarts/tree/main/computer-use-demo)为本项目提供的基础支持！

