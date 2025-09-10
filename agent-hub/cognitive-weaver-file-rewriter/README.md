# Cognitive Weaver File Rewriter Agent

一个用于安全修改文件并添加关系链接的MOFA Agent。

## 功能特性

- **安全重写**：修改前自动创建备份文件
- **关系链接**：在概念间插入语义关系链接
- **关键词链接**：为重要概念添加双链格式
- **原子操作**：确保文件修改的完整性
- **错误恢复**：支持从备份恢复

## 安装

```bash
pip install -e .
```

## 配置

### 输入参数

| 参数名 | 类型 | 必需 | 描述 |
|--------|------|------|------|
| `ai_result` | object | 是 | 包含推理结果、关系和关键词的对象 |

### 输出参数

| 参数名 | 类型 | 描述 |
|--------|------|------|
| `file_updated` | object | 文件更新结果，包含更新统计和状态信息 |

## 使用示例

在数据流配置中使用：

```yaml
nodes:
  - id: file-rewriter
    path: cognitive-weaver-file-rewriter
    outputs: [file_updated]
    inputs:
      ai_result: ai-inference/inference_result
```

## 输出格式

```json
{
  "file_path": "/path/to/file.md",
  "updates_made": true,
  "relationships_added": 3,
  "keywords_linked": 5,
  "timestamp": "2024-01-01T12:00:00",
  "backup_created": true
}
```

## 备份机制

所有文件修改前都会自动创建`.bak`备份文件：
- `note.md` → `note.md.bak`
- 如果修改失败，可手动从备份恢复
- 如果无修改，自动删除空备份
