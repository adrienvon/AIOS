#!/bin/bash

# Cognitive Weaver Docker 启动脚本

set -e

echo "🚀 启动 Cognitive Weaver MOFA 版本..."

# 检查环境变量
if [ -z "$DEEPSEEK_API_KEY" ]; then
    echo "⚠️  警告: DEEPSEEK_API_KEY 未设置"
fi

# 初始化Dora
echo "📡 初始化 Dora 服务..."
dora up &
DORA_PID=$!

# 等待Dora启动
sleep 5

# 根据启动模式执行不同操作
case "$1" in
    "cognitive-weaver")
        echo "🧠 启动 Cognitive Weaver 完整版..."
        cd /app
        dora build cognitive_weaver_dataflow.yml
        dora start cognitive_weaver_dataflow.yml
        ;;
    "simple")
        echo "🧠 启动 Cognitive Weaver 简化版..."
        cd /app
        dora build cognitive_weaver_simple.yml
        dora start cognitive_weaver_simple.yml
        ;;
    "test")
        echo "🧪 运行测试..."
        cd /app
        python3 test_setup.py
        ;;
    "bash"|"shell")
        echo "💻 启动交互式Shell..."
        exec /bin/bash
        ;;
    *)
        echo "📖 用法:"
        echo "  docker run -it cognitive-weaver [cognitive-weaver|simple|test|bash]"
        echo ""
        echo "模式说明:"
        echo "  cognitive-weaver - 启动完整版数据流"
        echo "  simple          - 启动简化版数据流"
        echo "  test           - 运行系统测试"
        echo "  bash           - 启动交互式Shell"
        exec /bin/bash
        ;;
esac

# 清理
trap "kill $DORA_PID 2>/dev/null || true" EXIT

# 保持容器运行
wait
