#!/bin/bash

# Cognitive Weaver 快速部署脚本
# 一键启动容器化的Cognitive Weaver MOFA版本

set -e

echo "🧠 Cognitive Weaver MOFA 容器化部署"
echo "====================================="

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装，请先安装Docker"
    exit 1
fi

# 检查Docker Compose是否安装
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose未安装，请先安装Docker Compose"
    exit 1
fi

# 检查配置文件
if [ ! -f ".env.secret" ]; then
    echo "⚠️  配置文件不存在，从模板创建..."
    cp .env.example .env.secret
    echo "📝 请编辑 .env.secret 文件，添加您的API密钥"
    echo "   必需配置: DEEPSEEK_API_KEY"
    read -p "是否现在编辑配置文件? (y/n): " edit_config
    if [ "$edit_config" = "y" ]; then
        ${EDITOR:-nano} .env.secret
    fi
fi

# 选择运行模式
echo ""
echo "请选择运行模式:"
echo "1) 完整版 (推荐生产环境)"
echo "2) 简化版 (推荐测试)"
echo "3) 测试模式"
echo "4) 后台运行"
echo "5) 调试模式"

read -p "请输入选项 (1-5): " mode

case $mode in
    1)
        echo "🚀 启动完整版..."
        docker-compose run --rm cognitive-weaver cognitive-weaver
        ;;
    2)
        echo "🚀 启动简化版..."
        docker-compose run --rm cognitive-weaver simple
        ;;
    3)
        echo "🧪 运行测试..."
        docker-compose run --rm cognitive-weaver test
        ;;
    4)
        echo "🚀 后台启动..."
        docker-compose up -d
        echo "✅ 服务已在后台启动"
        echo "📊 查看状态: docker-compose ps"
        echo "📝 查看日志: docker-compose logs -f"
        echo "🛑 停止服务: docker-compose down"
        ;;
    5)
        echo "🔧 启动调试模式..."
        docker-compose run --rm cognitive-weaver bash
        ;;
    *)
        echo "❌ 无效选项"
        exit 1
        ;;
esac

echo ""
echo "🎉 部署完成！"
