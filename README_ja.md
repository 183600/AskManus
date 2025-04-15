[English](README.md) | 中文 | [한국어](README_ko.md) | [日本語](README_ja.md)

&ensp;
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT) &ensp;
[![Discord Follow](https://dcbadge.vercel.app/api/server/uXjhv3Jp9s?style=flat)](https://discord.gg/uXjhv3Jp9s)

# 👋 AskManus

OpenManusを基にしたAIエージェントで、以下の機能を提供します：
• インストールスクリプト
• ユーザーとの対話時に、ユーザーが発言した後、必要に応じてコマンドラインに選択肢を表示し、各選択肢には必要に応じて説明が付きます

## インストールガイド

2つのインストール方法を提供しています。方法2（uv）を推奨します。より高速なインストール速度と優れた依存関係管理を提供するためです。

### 方法1：condaを使用

1. 新しいconda環境を作成：

```bash
conda create -n open_manus python=3.12
conda activate open_manus
```

2. リポジトリをクローン：

```bash
git clone https://github.com/mannaandpoem/OpenManus.git
cd OpenManus
```

3. 依存関係をインストール：

```bash
pip install -r requirements.txt
```

### 方法2：uvを使用（推奨）

1. uv（高速なPythonパッケージマネージャー）をインストール：

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

2. リポジトリをクローン：

```bash
git clone https://github.com/mannaandpoem/OpenManus.git
cd OpenManus
```

3. 仮想環境を作成して有効化：

```bash
uv venv --python 3.12
source .venv/bin/activate  # Unix/macOSシステム
# Windowsシステムでは：
# .venv\Scripts\activate
```

4. 依存関係をインストール：

```bash
uv pip install -r requirements.txt
```

### ブラウザ自動化ツール（オプション）
```bash
playwright install
```

## 設定説明

AskManusは使用するLLM APIの設定が必要です。以下の手順で設定できます：

1. `config`ディレクトリに`config.toml`ファイルを作成（サンプルからコピー可）：

```bash
cp config/config.example.toml config/config.toml
```

2. `config/config.toml`を編集してAPIキーとカスタム設定を追加：

```toml
# グローバルLLM設定
[llm]
model = "gpt-4o"
base_url = "https://api.openai.com/v1"
api_key = "sk-..."  # 実際のAPIキーに置き換えてください
max_tokens = 4096
temperature = 0.0

# オプションの特定LLMモデル設定
[llm.vision]
model = "gpt-4o"
base_url = "https://api.openai.com/v1"
api_key = "sk-..."  # 実際のAPIキーに置き換えてください
```

## クイックスタート

AskManusを実行：

```bash
python main.py
```

その後、ターミナルからアイデアを入力してください！

MCPツールバージョンを使用する場合は、以下を実行：
```bash
python run_mcp.py
```

不安定なマルチエージェントバージョンを体験する場合は、以下を実行：

```bash
python run_flow.py
```

## 貢献ガイド

友好的な提案や価値ある貢献を歓迎します！直接issueを作成するかpull requestを提出してください。

**注意**: pull requestを提出する前に、pre-commitツールで変更をチェックしてください。`pre-commit run --all-files`を実行してチェックを行います。

## 交流
• [Discord](https://discord.gg/uXjhv3Jp9s)
• [QQグループ](http://qm.qq.com/cgi-bin/qm/qr?_wv=1027&k=1XmdWxsfaDbgwq6oowemjjibzwml-bPO&authKey=1YifslbduQQmNTPH3XmXEPlH1zNM5wKd2djP3TIIXBr5UWPem5ULaNzS7mqBcOSe&noverify=0&group_code=725104480)

## 謝辞

このプロジェクトはOpenManusを基にしており、[OpenManus](https://github.com/anthropics/anthropic-quickstarts/tree/main/computer-use-demo)に特別な感謝を申し上げます。
