[English](README.md) | 中文 | [한국어](README_ko.md) | [日本語](README_ja.md)

&ensp;
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT) &ensp;
[![Discord Follow](https://dcbadge.vercel.app/api/server/uXjhv3Jp9s?style=flat)](https://discord.gg/uXjhv3Jp9s)

# 👋 AskManus

OpenManus 기반의 AI 에이전트로 다음 기능을 제공합니다:
- 설치 스크립트
- 사용자 대화 시, 사용자의 발화 후 필요한 경우 명령줄에 선택 옵션을 표시하며, 각 옵션에 설명이 필요한 경우 추가 설명 제공

## 설치 가이드

두 가지 설치 방법을 제공합니다. 더 빠른 설치 속도와 우수한 의존성 관리를 위해 방법 2(uv)를 권장합니다.

### 방법 1: conda 사용

1. 새로운 conda 환경 생성:

```bash
conda create -n open_manus python=3.12
conda activate open_manus
```

2. 저장소 복제:

```bash
git clone https://github.com/mannaandpoem/OpenManus.git
cd OpenManus
```

3. 의존성 설치:

```bash
pip install -r requirements.txt
```

### 방법 2: uv 사용 (권장)

1. uv(고속 Python 패키지 관리자) 설치:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

2. 저장소 복제:

```bash
git clone https://github.com/mannaandpoem/OpenManus.git
cd OpenManus
```

3. 가상 환경 생성 및 활성화:

```bash
uv venv --python 3.12
source .venv/bin/activate  # Unix/macOS 시스템
# Windows 시스템 사용:
# .venv\Scripts\activate
```

4. 의존성 설치:

```bash
uv pip install -r requirements.txt
```

### 브라우저 자동화 도구 (선택 사항)
```bash
playwright install
```

## 설정 설명

AskManus는 LLM API 사용을 위해 설정이 필요하며, 다음 단계로 설정할 수 있습니다:

1. `config` 디렉토리에 `config.toml` 파일 생성 (예제 파일 복사 가능):

```bash
cp config/config.example.toml config/config.toml
```

2. `config/config.toml` 편집하여 API 키와 사용자 정의 설정 추가:

```toml
# 전역 LLM 설정
[llm]
model = "gpt-4o"
base_url = "https://api.openai.com/v1"
api_key = "sk-..."  # 실제 API 키로 교체
max_tokens = 4096
temperature = 0.0

# 선택적 특정 LLM 모델 설정
[llm.vision]
model = "gpt-4o"
base_url = "https://api.openai.com/v1"
api_key = "sk-..."  # 실제 API 키로 교체
```

## 빠른 시작

한 줄 명령으로 AskManus 실행:

```bash
python main.py
```

터미널에 아이디어를 입력해 보세요!

MCP 도구 버전 사용 시 실행:
```bash
python run_mcp.py
```

불안정한 다중 에이전트 버전 체험:

```bash
python run_flow.py
```

## 기여 가이드

우리는 모든 친근한 제안과 가치 있는 기여를 환영합니다! 직접 issue를 생성하거나 pull request를 제출할 수 있습니다.

**주의**: pull request 제출 전 pre-commit 도구로 변경 사항을 확인하세요. `pre-commit run --all-files` 실행하여 검사를 수행합니다.

## 커뮤니케이션
- [Discord](https://discord.gg/uXjhv3Jp9s)
- [QQ 그룹](http://qm.qq.com/cgi-bin/qm/qr?_wv=1027&k=1XmdWxsfaDbgwq6oowemjjibzwml-bPO&authKey=1YifslbduQQmNTPH3XmXEPlH1zNM5wKd2djP3TIIXBr5UWPem5ULaNzS7mqBcOSe&noverify=0&group_code=725104480)

## 감사의 말

이 프로젝트는 OpenManus를 기반으로 하며, [OpenManus](https://github.com/anthropics/anthropic-quickstarts/tree/main/computer-use-demo)에 특별한 감사를 드립니다!
