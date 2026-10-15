#!/bin/bash

# 环境检测函数
check_environment() {
    # 检查Python是否安装
    if ! command -v python3 &> /dev/null; then
        echo "未检测到Python 3安装"
        read -p "是否要安装Python 3.12？[y/N] " choice
        case "$choice" in
            y|Y )
                echo "正在安装Python 3.12..."
                if [[ "$OSTYPE" == "linux-gnu"* ]]; then
                    sudo apt-get update && sudo apt-get install -y python3.12
                elif [[ "$OSTYPE" == "darwin"* ]]; then
                    brew install python@3.12
                else
                    echo "不支持的操作系统，请手动安装Python 3.12"
                    exit 1
                fi
                ;;
            * )
                echo "请先安装Python 3.12后再运行此脚本"
                exit 1
                ;;
        esac
    fi

    # 检查conda是否安装
    if ! command -v conda &> /dev/null; then
        echo "未检测到conda安装"
        read -p "是否要安装Miniconda？[y/N] " choice
        case "$choice" in
            y|Y )
                echo "正在安装Miniconda..."
                if [[ "$OSTYPE" == "linux-gnu"* ]]; then
                    wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
                    bash Miniconda3-latest-Linux-x86_64.sh
                elif [[ "$OSTYPE" == "darwin"* ]]; then
                    curl -O https://repo.anaconda.com/miniconda/Miniconda3-latest-MacOSX-x86_64.sh
                    bash Miniconda3-latest-MacOSX-x86_64.sh
                else
                    echo "不支持的操作系统，请手动安装Miniconda"
                    exit 1
                fi
                ;;
            * )
                echo "请先安装conda后再运行此脚本"
                exit 1
                ;;
        esac
    fi
}

# 执行环境检测
check_environment

# 创建conda环境
conda create -n open_manus python=3.12 -y
conda activate open_manus

# 克隆仓库
# git clone https://gitee.com/huspa/OpenManus.git
# cd OpenManus

# 安装依赖
pip install -r requirements.txt

# 配置GLM-4V-Flash API设置
mkdir -p config
cat > config/config.toml << 'EOF'
# 全局LLM配置
[llm]
model = "glm-4v-flash"
base_url = "https://open.bigmodel.cn/api/paas/v4/chat/completions"
api_key = "YOUR_API_KEY"
max_tokens = 4096
temperature = 0.0

# 视觉模型配置
[llm.vision]
model = "glm-4v-flash"
base_url = "https://open.bigmodel.cn/api/paas/v4/chat/completions"
api_key = "YOUR_API_KEY"
max_tokens = 4096
temperature = 0.0
EOF

# 可选: 安装浏览器自动化工具
playwright install

echo "AskManus已通过conda方式安装完成并将API设置成GLM-4V-Flash了"

echo -e "\n\n运行以下命令启动OpenManus:"
echo -e "\npython main.py"
echo -e "\n如需使用 MCP 工具版本，可运行："
echo -e "\npython run_mcp.py"
echo -e "\n如需体验不稳定的多智能体版本，可运行："
echo -e "\npython run_flow.py"
