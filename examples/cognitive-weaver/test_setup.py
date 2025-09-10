# Cognitive Weaver测试脚本

import os
import sys
import time
import subprocess
from pathlib import Path

def test_cognitive_weaver():
    """测试Cognitive Weaver MOFA版本"""
    
    print("🚀 开始测试Cognitive Weaver MOFA版本")
    
    # 检查依赖
    print("\n📋 检查依赖...")
    required_agents = [
        "cognitive-weaver-file-monitor",
        "cognitive-weaver-link-parser", 
        "cognitive-weaver-keyword-extractor",
        "cognitive-weaver-file-rewriter"
    ]
    
    for agent in required_agents:
        try:
            # 直接尝试导入模块来检查是否安装
            import_name = agent.replace("-", "_")
            __import__(import_name)
            print(f"  ✅ {agent} - 已安装")
        except ImportError:
            print(f"  ❌ {agent} - 未安装或有问题")
        except Exception as e:
            print(f"  ⚠️  {agent} - 检查失败: {e}")
    
    # 检查配置文件
    print("\n📝 检查配置文件...")
    env_file = Path(".env.secret")
    if env_file.exists():
        print("  ✅ .env.secret - 已存在")
    else:
        print("  ⚠️  .env.secret - 不存在，请复制.env.example并配置")
    
    # 检查数据流文件
    print("\n📊 检查数据流配置...")
    dataflow_files = [
        "cognitive_weaver_dataflow.yml",
        "cognitive_weaver_simple.yml"
    ]
    
    for file in dataflow_files:
        if Path(file).exists():
            print(f"  ✅ {file} - 已存在")
        else:
            print(f"  ❌ {file} - 不存在")
    
    # 测试建议
    print("\n💡 测试建议:")
    print("1. 确保所有Agent都已正确安装")
    print("2. 配置.env.secret文件中的API密钥")
    print("3. 运行简化版本进行快速测试:")
    print("   dora build cognitive_weaver_simple.yml")
    print("   dora start cognitive_weaver_simple.yml")
    print("4. 在另一个终端运行: terminal-input")
    
    print("\n🎉 测试完成!")

if __name__ == "__main__":
    test_cognitive_weaver()
