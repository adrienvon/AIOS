import re
import json
from typing import List, Dict, Any, Set
from collections import defaultdict
from mofa.agent_build.base.base_agent import MofaAgent, run_agent

class KeywordExtractor:
    """智能关键词提取器"""
    
    def __init__(self):
        # 中文停用词
        self.stop_words = {
            '的', '了', '在', '是', '我', '有', '和', '就', '不', '人', '都', '一', '一个',
            '上', '也', '很', '到', '说', '要', '去', '你', '会', '着', '没有', '看', '好',
            '自己', '这', '那', '什么', '出', '就是', '他', '时候', '可以', '如果', '这个',
            '中', '么', '所', '只', '但', '又', '或', '为', '从', '而', '与', '及', '等'
        }
        
        # 中文关键词提取正则
        self.chinese_pattern = r'[\u4e00-\u9fff\w]+'
        
    def extract_keywords(self, content: str, file_path: str = '') -> List[Dict[str, Any]]:
        """从内容中提取关键词"""
        keywords = []
        lines = content.split('\n')
        
        for line_num, line in enumerate(lines):
            # 跳过已有链接的行
            if '[[' in line and ']]' in line:
                continue
                
            # 跳过标题、代码块等
            if line.strip().startswith('#') or line.strip().startswith('```'):
                continue
            
            # 提取当前行的关键词
            line_keywords = self._extract_line_keywords(line, line_num + 1, lines)
            keywords.extend(line_keywords)
        
        # 按频率分组关键词
        grouped_keywords = self._group_similar_keywords(keywords)
        
        return grouped_keywords
    
    def _extract_line_keywords(self, line: str, line_num: int, all_lines: List[str]) -> List[Dict[str, Any]]:
        """从单行中提取关键词"""
        keywords = []
        
        # 提取中文词汇
        matches = re.findall(self.chinese_pattern, line)
        
        for match in matches:
            # 过滤停用词和无意义词汇
            if self._is_valid_keyword(match):
                # 提取上下文
                context = self._get_context(all_lines, line_num - 1, match)
                
                keyword_info = {
                    'keyword': match,
                    'line_number': line_num,
                    'line_content': line.strip(),
                    'context': context,
                    'length': len(match)
                }
                
                keywords.append(keyword_info)
        
        return keywords
    
    def _is_valid_keyword(self, keyword: str) -> bool:
        """判断是否为有效关键词"""
        # 长度检查
        if len(keyword) < 2 or len(keyword) > 10:
            return False
        
        # 停用词检查
        if keyword in self.stop_words:
            return False
            
        # 数字检查
        if keyword.isdigit():
            return False
            
        # 单字符检查（除非是重要概念）
        if len(keyword) == 1:
            return False
        
        return True
    
    def _get_context(self, lines: List[str], line_index: int, keyword: str) -> str:
        """获取关键词的上下文"""
        start = max(0, line_index - 1)
        end = min(len(lines), line_index + 2)
        
        context_lines = lines[start:end]
        context = '\n'.join(context_lines)
        
        # 限制上下文长度
        if len(context) > 200:
            # 以关键词为中心截取
            keyword_pos = context.find(keyword)
            if keyword_pos != -1:
                start_pos = max(0, keyword_pos - 100)
                end_pos = min(len(context), keyword_pos + 100)
                context = context[start_pos:end_pos]
        
        return context.strip()
    
    def _group_similar_keywords(self, keywords: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """将相似的关键词分组"""
        # 按关键词文本分组
        keyword_groups = defaultdict(list)
        
        for kw in keywords:
            # 标准化关键词（转小写）
            normalized = kw['keyword'].lower()
            keyword_groups[normalized].append(kw)
        
        # 只保留出现多次的关键词
        grouped_results = []
        for keyword_text, occurrences in keyword_groups.items():
            if len(occurrences) >= 2:  # 至少出现2次
                group_info = {
                    'keyword': occurrences[0]['keyword'],  # 使用原始大小写
                    'occurrences': len(occurrences),
                    'contexts': [occ['context'] for occ in occurrences],
                    'line_numbers': [occ['line_number'] for occ in occurrences],
                    'lines': [occ['line_content'] for occ in occurrences]
                }
                grouped_results.append(group_info)
        
        # 按出现次数排序
        grouped_results.sort(key=lambda x: x['occurrences'], reverse=True)
        
        return grouped_results

@run_agent
def run(agent: MofaAgent):
    """
    关键词提取Agent主函数
    从文档内容中智能提取关键词
    """
    try:
        # 接收解析后的链接信息
        parsed_data = agent.receive_parameter('parsed_data')
        
        if isinstance(parsed_data, str):
            parsed_data = json.loads(parsed_data)
        
        file_path = parsed_data.get('file_path', '')
        file_name = parsed_data.get('file_name', '')
        
        # 获取原始文件内容（如果有的话）
        content = ''
        if 'content' in parsed_data:
            content = parsed_data['content']
        elif 'file_info' in parsed_data:
            content = parsed_data['file_info'].get('content', '')
        
        print(f"提取关键词: {file_path}")
        
        # 创建关键词提取器
        extractor = KeywordExtractor()
        
        # 提取关键词
        keywords = extractor.extract_keywords(content, file_path)
        
        if keywords:
            print(f"发现 {len(keywords)} 个关键词组")
            for kw in keywords[:5]:  # 显示前5个
                print(f"  - {kw['keyword']} (出现 {kw['occurrences']} 次)")
        else:
            print("未发现有效关键词")
        
        # 构建输出结果
        result = {
            'file_path': file_path,
            'file_name': file_name,
            'keywords': keywords,
            'keyword_count': len(keywords),
            'timestamp': parsed_data.get('timestamp'),
            'extracted_links': parsed_data.get('links', [])  # 保留链接信息
        }
        
        agent.send_output(
            agent_output_name='extracted_keywords',
            agent_result=result
        )
        
    except Exception as e:
        error_msg = f"关键词提取Agent错误: {str(e)}"
        print(error_msg)
        agent.send_output(
            agent_output_name='extracted_keywords',
            agent_result={'error': error_msg}
        )

def main():
    agent = MofaAgent(agent_name='cognitive-weaver-keyword-extractor')
    run(agent=agent)

if __name__ == "__main__":
    main()
