# 容器化部署指南

## 🐳 **是的，可以使用同一个容器！**

Cognitive Weaver + MOFA项目完全可以在单一容器中运行，所有组件都兼容并且资源需求合理。

## 📦 **快速部署**

### 方式1: Docker Compose (推荐)

```bash
# 1. 配置环境变量
cp .env.example .env.secret
# 编辑 .env.secret 添加API密钥

# 2. 设置Obsidian vault路径
export OBSIDIAN_VAULT_PATH=/path/to/your/obsidian/vault

# 3. 启动服务
docker-compose up -d

# 4. 查看日志
docker-compose logs -f cognitive-weaver
```

### 方式2: 直接Docker

```bash
# 构建镜像
docker build -t cognitive-weaver .

# 运行容器
docker run -d \
  --name cognitive-weaver \
  -v /path/to/obsidian/vault:/app/vault \
  -v cognitive-weaver-data:/app/data \
  -e DEEPSEEK_API_KEY=your_api_key \
  cognitive-weaver
```

## 🎛️ **运行模式**

### 完整版模式
```bash
docker run -it cognitive-weaver cognitive-weaver
```

### 简化版模式 (推荐测试)
```bash
docker run -it cognitive-weaver simple
```

### 测试模式
```bash
docker run -it cognitive-weaver test
```

### 调试模式
```bash
docker run -it cognitive-weaver bash
```

## 🔧 **配置说明**

### 环境变量

| 变量名 | 说明 | 必需 |
|--------|------|------|
| `DEEPSEEK_API_KEY` | DeepSeek API密钥 | ✅ |
| `OPENAI_API_KEY` | OpenAI API密钥 | ❌ |
| `DORA_LOG_LEVEL` | 日志级别 | ❌ |
| `OBSIDIAN_VAULT_PATH` | Obsidian vault路径 | ✅ |

### 数据卷挂载

| 容器路径 | 说明 | 类型 |
|----------|------|------|
| `/app/vault` | Obsidian vault目录 | 必需 |
| `/app/data` | 知识图谱数据 | 持久化 |
| `/app/logs` | 系统日志 | 持久化 |

## 🚀 **性能优化**

### 资源配置
- **内存**: 推荐2GB，最小512MB
- **CPU**: 推荐1核，最小0.25核
- **存储**: 根据vault大小，推荐10GB+

### 缓存优化
```bash
# 启用Redis缓存
docker-compose --profile caching up -d
```

### 监控
```bash
# 启用监控
docker-compose --profile monitoring up -d
# 访问 http://localhost:9090
```

## 🔍 **故障排查**

### 检查容器状态
```bash
docker-compose ps
docker-compose logs cognitive-weaver
```

### 进入容器调试
```bash
docker-compose exec cognitive-weaver bash
# 或
docker exec -it cognitive-weaver bash
```

### 重启服务
```bash
docker-compose restart cognitive-weaver
```

### 完全重新部署
```bash
docker-compose down -v
docker-compose up --build -d
```

## 📊 **优势总结**

### ✅ **统一容器的优势**

1. **简化部署**: 一个容器包含所有组件
2. **资源高效**: 共享系统资源，无重复overhead
3. **网络简单**: 组件间通信无需跨容器
4. **管理便捷**: 单一容器生命周期管理
5. **开发友好**: 统一的调试和测试环境

### 🎯 **适用场景**

- ✅ **单机部署**
- ✅ **开发测试环境**
- ✅ **小规模生产环境**
- ✅ **个人使用**
- ✅ **快速原型验证**

### 🔄 **未来扩展**

如果后续需要分布式部署，可以考虑：
- 微服务拆分 (每个Agent一个容器)
- Kubernetes编排
- 负载均衡和高可用

但对于当前项目规模，**单一容器是最佳选择**！
