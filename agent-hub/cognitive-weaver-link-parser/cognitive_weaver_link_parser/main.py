import re
import json
from typing import List, Dict, Any
from mofa.agent_build.base.base_agent import MofaAgent, run_agent

class LinkParser:
    """Obsidian双链链接解析器"""
    
    def __init__(self):
        # Obsidian双链格式：[[目标]] 或 [[目标|显示文本]]
        self.link_pattern = r'\[\[([^\]]+)\]\]'
        self.context_window = 100  # 上下文窗口大小
    
    def extract_links(self, content: str) -> List[Dict[str, Any]]:
        """提取文档中的所有双链链接"""
        links = []
        lines = content.split('\n')
        
        for line_num, line in enumerate(lines):
            # 跳过已经有关系链接的行
            if '[[' in line and ']]' in line:
                # 检查是否已经是关系链接格式
                if self._is_relationship_link(line):
                    continue
                
                # 提取当前行的链接
                line_links = re.findall(self.link_pattern, line)
                
                for link_text in line_links:
                    # 处理 [[目标|显示文本]] 格式
                    if '|' in link_text:
                        target, display = link_text.split('|', 1)
                    else:
                        target = link_text
                        display = link_text
                    
                    # 提取上下文
                    context = self._extract_context(lines, line_num, link_text)
                    
                    link_info = {
                        'target': target.strip(),
                        'display': display.strip(),
                        'line_number': line_num + 1,
                        'line_content': line.strip(),
                        'context': context,
                        'full_link': f'[[{link_text}]]'
                    }
                    
                    links.append(link_info)
        
        return links
    
    def _is_relationship_link(self, line: str) -> bool:
        """检查是否已经是关系链接格式"""
        # 检查是否包含关系类型的关键词
        relationship_keywords = [
            '支撑观点', '反驳观点', '举例说明', '对比分析',
            '因果关系', '补充说明', '相关概念', '发展历程'
        ]
        
        for keyword in relationship_keywords:
            if f'[[{keyword}]]' in line:
                return True
        return False
    
    def _extract_context(self, lines: List[str], line_num: int, link_text: str) -> str:
        """提取链接的上下文"""
        # 获取前后几行作为上下文
        start_line = max(0, line_num - 2)
        end_line = min(len(lines), line_num + 3)
        
        context_lines = lines[start_line:end_line]
        context = '\n'.join(context_lines)
        
        # 限制上下文长度
        if len(context) > self.context_window * 2:
            # 以当前行为中心，截取上下文
            current_line = lines[line_num]
            before_context = context[:context.find(current_line)][-self.context_window:]
            after_context = context[context.find(current_line) + len(current_line):][:self.context_window]
            context = before_context + current_line + after_context
        
        return context.strip()

@run_agent
def run(agent: MofaAgent):
    """
    链接解析Agent主函数
    解析Obsidian文档中的双链链接
    """
    try:
        # 接收文件信息
        file_info = agent.receive_parameter('file_info')
        
        if isinstance(file_info, str):
            file_info = json.loads(file_info)
        
        file_path = file_info.get('file_path', '')
        content = file_info.get('content', '')
        
        print(f"解析文件链接: {file_path}")
        
        # 创建解析器
        parser = LinkParser()
        
        # 提取链接
        links = parser.extract_links(content)
        
        if links:
            print(f"发现 {len(links)} 个链接")
            for link in links:
                print(f"  - {link['full_link']} (行 {link['line_number']})")
        else:
            print("未发现链接")
        
        # 构建输出结果
        result = {
            'file_path': file_path,
            'file_name': file_info.get('file_name', ''),
            'links': links,
            'link_count': len(links),
            'timestamp': file_info.get('timestamp')
        }
        
        agent.send_output(
            agent_output_name='parsed_links',
            agent_result=result
        )
        
    except Exception as e:
        error_msg = f"链接解析Agent错误: {str(e)}"
        print(error_msg)
        agent.send_output(
            agent_output_name='parsed_links',
            agent_result={'error': error_msg}
        )

def main():
    agent = MofaAgent(agent_name='cognitive-weaver-link-parser')
    run(agent=agent)

if __name__ == "__main__":
    main()
