```korean
[English](README.md) | 中文 | [한국어](README_ko.md) | [日本語](README_ja.md)

[![GitHub stars](https://img.shields.io/github/stars/mannaandpoem/OpenManus?style=social)](https://github.com/mannaandpoem/OpenManus/stargazers)
&ensp;
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT) &ensp;
[![Discord Follow](https://dcbadge.vercel.app/api/server/DYn29wFk9z?style=flat)](https://discord.gg/DYn29wFk9z)

# 👋 AskManus

OpenManus를 기반으로 제공되는 기능:
- 설치 스크립트
- 사용자가 문장을 입력한 후 필요한 경우 명령행에 몇 가지 옵션을 표시하며, 각 옵션은 필요한 경우 설명을 포함합니다

## 설치 가이드

두 가지 설치 방법을 제공합니다. 방법 이(_uv)를 권장합니다. 설치 속도와 의존성 관리가 더 우수합니다.

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

### 방법 2: uv 사용(권장)

1. uv(빠른 Python 패키지 관리자) 설치:

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
source .venv/bin/activate  # Unix/macOS
# Windows 시스템은:
# .venv\Scripts\activate
```

4. 의존성 설치:

```bash
uv pip install -r requirements.txt
```

### 브라우저 자동화 도구(선택사항)
```bash
playwright install
```

## 구성 설명

AskManus는 LLM API 설정이 필요합니다. 다음 단계를 따라 설정하세요:

1. `config` 디렉토리에 `config.toml` 파일 생성(예시 복사):

```bash
cp config/config.example.toml config/config.toml
```

2. `config/config.toml` 편집하여 API 키 및 설정 추가:

```toml
# 전역 LLM 설정
[llm]
model = "gpt-4o"
base_url = "https://api.openai.com/v1"
api_key = "sk-..."  # 실제 키로 변경
max_tokens = 4096
temperature = 0.0

# 특정 LLM 모델 설정(선택)
[llm.vision]
model = "gpt-4o"
base_url = "https://api.openai.com/v1"
api_key = "sk-..."  # 실제 키로 변경
```

## 빠른 시작

단일 명령으로 AskManus 실행:

```bash
python main.py
```

터미널에 아이디어를 입력하세요!

MCP 도구 버전 사용 시:
```bash
python run_mcp.py
```

불안정한 다중 에이전트 버전 경험 시:
```bash
python run_flow.py
```

## 기여 가이드

친절한 제안과 소중한 기여를 환영합니다! 이슈 생성 또는 Pull Request 제출 가능합니다.

**참고**: Pull Request 제출 전 `pre-commit run --all-files`로 검사를 완료하세요.

## 커뮤니티

## Star 수

[![Star History Chart](https://api.star-history.com/svg?repos=mannaandpoem/OpenManus&type=Date)](https://star-history.com/#mannaandpoem/OpenManus&Date)

## 감사의 말

이 프로젝트는 OpenManus 기반으로 구축되었으며, [OpenManus](https://github.com/anthropics/anthropic-quickstarts/tree/main/computer-use-demo)의 지원에 깊이 감사드립니다!
