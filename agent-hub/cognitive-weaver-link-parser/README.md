# Cognitive Weaver Link Parser Agent

一个用于解析Obsidian文档中双链链接的MOFA Agent。

## 功能特性

- **双链识别**：识别`[[目标]]`和`[[目标|显示文本]]`格式的链接
- **上下文提取**：提取链接周围的上下文信息
- **关系链接过滤**：跳过已处理的关系链接
- **详细信息**：提供链接的行号、内容等详细信息

## 安装

```bash
pip install -e .
```

## 配置

### 输入参数

| 参数名 | 类型 | 必需 | 描述 |
|--------|------|------|------|
| `file_info` | object | 是 | 包含文件路径、内容等信息的对象 |

### 输出参数

| 参数名 | 类型 | 描述 |
|--------|------|------|
| `parsed_links` | object | 解析后的链接信息，包含所有链接的详细数据 |

## 使用示例

在数据流配置中使用：

```yaml
nodes:
  - id: link-parser
    path: cognitive-weaver-link-parser
    outputs: [parsed_links]
    inputs:
      file_info: file-monitor/file_changed
```

## 输出格式

```json
{
  "file_path": "/path/to/file.md",
  "file_name": "file.md",
  "links": [
    {
      "target": "目标笔记",
      "display": "显示文本", 
      "line_number": 5,
      "line_content": "这是包含[[目标笔记|显示文本]]的行",
      "context": "周围的上下文内容...",
      "full_link": "[[目标笔记|显示文本]]"
    }
  ],
  "link_count": 1,
  "timestamp": 1234567890.123
}
```
