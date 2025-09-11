# Cognitive Weaver MOFA 容器化部署
# 基于现有的MOFA Dockerfile进行扩展

FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

# 配置阿里云镜像源
RUN sed -i 's|http://archive.ubuntu.com/ubuntu/|http://mirrors.aliyun.com/ubuntu/|g' /etc/apt/sources.list

# 安装基础系统依赖
RUN apt-get update && \
    apt-get install -y software-properties-common && \
    add-apt-repository ppa:deadsnakes/ppa && \
    apt-get update && \
    apt-get install -y vim wget lsof curl uuid-dev python3.10 python3.10-distutils python3.10-venv git && \
    apt-get install -y python3-pip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# 设置Python 3.10为默认版本
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.10 1

# 安装Rust环境 (Dora-rs需要)
RUN apt-get update && apt-get install -y curl && \
    curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y && \
    /root/.cargo/bin/rustup default stable

ENV PATH="/root/.cargo/bin:${PATH}"

# 验证Rust安装
RUN rustc --version && cargo --version

# 安装Dora-rs和MOFA框架
RUN cargo install dora-cli --locked && \
    pip3 install dora-rs

# 安装MOFA框架和基础依赖
RUN pip3 install --upgrade pip --index-url https://pypi.org/simple && \
    pip install --upgrade --ignore-installed blinker && \
    pip3 install uv && \
    uv pip install --system mofa-ai

# 创建项目目录
WORKDIR /app

# 复制项目文件
COPY . .

# 安装Cognitive Weaver相关依赖
RUN pip3 install watchdog>=3.0.0 && \
    pip3 install openai>=1.0.0 && \
    pip3 install pyyaml && \
    pip3 install python-dotenv

# 安装Cognitive Weaver Agent组件
RUN if [ -d "../agent-hub/cognitive-weaver-file-monitor" ]; then \
    pip3 install -e ../agent-hub/cognitive-weaver-file-monitor; \
    fi && \
    if [ -d "../agent-hub/cognitive-weaver-link-parser" ]; then \
    pip3 install -e ../agent-hub/cognitive-weaver-link-parser; \
    fi && \
    if [ -d "../agent-hub/cognitive-weaver-keyword-extractor" ]; then \
    pip3 install -e ../agent-hub/cognitive-weaver-keyword-extractor; \
    fi && \
    if [ -d "../agent-hub/cognitive-weaver-file-rewriter" ]; then \
    pip3 install -e ../agent-hub/cognitive-weaver-file-rewriter; \
    fi

# 创建数据目录
RUN mkdir -p /app/data /app/logs /app/vault

# 设置环境变量
ENV PYTHONPATH=/app:$PYTHONPATH
ENV DORA_LOG_LEVEL=INFO

# 暴露端口 (如果需要Web界面)
EXPOSE 8000 8080

# 启动脚本
COPY docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh

# 健康检查
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD python3 test_setup.py || exit 1

ENTRYPOINT ["/docker-entrypoint.sh"]
CMD ["cognitive-weaver"]
