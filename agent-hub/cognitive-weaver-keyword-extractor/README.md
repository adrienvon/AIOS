# Cognitive Weaver Keyword Extractor Agent

一个用于智能提取文档中关键概念的MOFA Agent。

## 功能特性

- **智能提取**：使用正则表达式和NLP技术提取中文关键词
- **停用词过滤**：自动过滤无意义的停用词
- **频率分析**：识别重复出现的重要概念
- **上下文保留**：为每个关键词保留上下文信息
- **分组聚合**：将相似的关键词进行分组

## 安装

```bash
pip install -e .
```

## 配置

### 输入参数

| 参数名 | 类型 | 必需 | 描述 |
|--------|------|------|------|
| `parsed_data` | object | 是 | 包含文件内容和解析信息的对象 |

### 输出参数

| 参数名 | 类型 | 描述 |
|--------|------|------|
| `extracted_keywords` | object | 提取的关键词信息，包含所有关键概念的详细数据 |

## 使用示例

在数据流配置中使用：

```yaml
nodes:
  - id: keyword-extractor
    path: cognitive-weaver-keyword-extractor
    outputs: [extracted_keywords]
    inputs:
      parsed_data: link-parser/parsed_links
```

## 输出格式

```json
{
  "file_path": "/path/to/file.md",
  "file_name": "file.md",
  "keywords": [
    {
      "keyword": "关键概念",
      "occurrences": 3,
      "contexts": ["上下文1...", "上下文2...", "上下文3..."],
      "line_numbers": [5, 12, 20],
      "lines": ["包含关键词的行1", "包含关键词的行2", "包含关键词的行3"]
    }
  ],
  "keyword_count": 1,
  "timestamp": 1234567890.123,
  "extracted_links": []
}
```
