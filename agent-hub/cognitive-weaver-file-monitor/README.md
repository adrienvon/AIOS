# Cognitive Weaver File Monitor Agent

一个用于监控Obsidian vault中Markdown文件变化的MOFA Agent。

## 功能特性

- **实时文件监控**：使用watchdog监控文件系统变化
- **Markdown文件过滤**：只处理.md文件的变化
- **内容提取**：自动读取变化文件的内容
- **递归监控**：支持监控子目录中的文件
- **错误处理**：包含完善的错误处理机制

## 安装

```bash
pip install -e .
```

## 配置

### 输入参数

| 参数名 | 类型 | 必需 | 描述 |
|--------|------|------|------|
| `vault_path` | string | 是 | Obsidian vault的根目录路径 |

### 输出参数

| 参数名 | 类型 | 描述 |
|--------|------|------|
| `file_changed` | object | 文件变化信息，包含文件路径、内容、时间戳等 |

## 使用示例

在数据流配置中使用：

```yaml
nodes:
  - id: file-monitor
    path: cognitive-weaver-file-monitor
    outputs: [file_changed]
    inputs:
      vault_path: terminal-input/vault_path
```

## 输出格式

```json
{
  "file_path": "/path/to/file.md",
  "file_name": "file.md", 
  "content": "文件内容...",
  "timestamp": 1234567890.123
}
```
