import os
import json
import shutil
from datetime import datetime
from typing import List, Dict, Any
from mofa.agent_build.base.base_agent import MofaAgent, run_agent

class FileRewriter:
    """安全的文件重写器"""
    
    def __init__(self, backup_enabled: bool = True):
        self.backup_enabled = backup_enabled
    
    def create_backup(self, file_path: str) -> str:
        """创建文件备份"""
        if not self.backup_enabled:
            return ""
            
        backup_path = f"{file_path}.bak"
        try:
            shutil.copy2(file_path, backup_path)
            print(f"已创建备份: {backup_path}")
            return backup_path
        except Exception as e:
            print(f"创建备份失败 {file_path}: {e}")
            return ""
    
    def add_relationship_links(self, file_path: str, relationships: List[Dict[str, Any]]) -> bool:
        """在文件中添加关系链接"""
        try:
            # 创建备份
            backup_path = self.create_backup(file_path)
            
            # 读取原文件
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            lines = content.split('\n')
            modified = False
            
            # 为每个关系添加链接
            for rel in relationships:
                source = rel.get('source', '')
                target = rel.get('target', '')
                relationship_type = rel.get('relationship', '')
                
                if source and target and relationship_type:
                    # 在文件中查找并添加关系链接
                    for i, line in enumerate(lines):
                        if source in line and target in line:
                            # 检查是否已经有关系链接
                            if f'[[{relationship_type}]]' not in line:
                                # 在source和target之间插入关系链接
                                new_line = self._insert_relationship_link(line, source, target, relationship_type)
                                if new_line != line:
                                    lines[i] = new_line
                                    modified = True
                                    print(f"在第{i+1}行添加关系链接: {relationship_type}")
            
            # 如果有修改，写回文件
            if modified:
                new_content = '\n'.join(lines)
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f"文件已更新: {file_path}")
                return True
            else:
                print(f"无需修改文件: {file_path}")
                # 如果没有修改，删除备份
                if backup_path and os.path.exists(backup_path):
                    os.remove(backup_path)
                return False
                
        except Exception as e:
            print(f"文件重写失败 {file_path}: {e}")
            return False
    
    def _insert_relationship_link(self, line: str, source: str, target: str, relationship: str) -> str:
        """在行中插入关系链接"""
        # 查找source在line中的位置
        source_pos = line.find(source)
        target_pos = line.find(target)
        
        if source_pos == -1 or target_pos == -1:
            return line
        
        # 确保source在target之前
        if source_pos > target_pos:
            source_pos, target_pos = target_pos, source_pos
            source, target = target, source
        
        # 在source和target之间插入关系链接
        # 格式：source [[关系]] target
        before_target = line[:target_pos]
        after_target = line[target_pos:]
        
        # 检查是否已经有关系链接
        if f'[[{relationship}]]' in before_target:
            return line
        
        # 插入关系链接
        relationship_link = f" [[{relationship}]] "
        new_line = before_target + relationship_link + after_target
        
        return new_line
    
    def add_keyword_links(self, file_path: str, keywords: List[Dict[str, Any]]) -> bool:
        """为关键词添加双链链接"""
        try:
            # 创建备份
            backup_path = self.create_backup(file_path)
            
            # 读取原文件
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            modified_content = content
            
            # 为每个关键词添加链接
            for kw in keywords:
                keyword = kw.get('keyword', '')
                if keyword and len(keyword) > 1:
                    # 避免重复链接
                    if f'[[{keyword}]]' not in modified_content:
                        # 将关键词替换为链接格式
                        # 使用单词边界确保精确匹配
                        import re
                        pattern = r'\b' + re.escape(keyword) + r'\b'
                        replacement = f'[[{keyword}]]'
                        
                        new_content = re.sub(pattern, replacement, modified_content, count=1)
                        if new_content != modified_content:
                            modified_content = new_content
                            print(f"为关键词添加链接: {keyword}")
            
            # 如果有修改，写回文件
            if modified_content != content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(modified_content)
                print(f"关键词链接已添加到: {file_path}")
                return True
            else:
                print(f"无需为关键词添加链接: {file_path}")
                # 如果没有修改，删除备份
                if backup_path and os.path.exists(backup_path):
                    os.remove(backup_path)
                return False
                
        except Exception as e:
            print(f"关键词链接添加失败 {file_path}: {e}")
            return False

@run_agent
def run(agent: MofaAgent):
    """
    文件重写Agent主函数
    安全地修改文件，添加关系链接和关键词链接
    """
    try:
        # 接收AI推理结果
        ai_result = agent.receive_parameter('ai_result')
        
        if isinstance(ai_result, str):
            ai_result = json.loads(ai_result)
        
        file_path = ai_result.get('file_path', '')
        relationships = ai_result.get('relationships', [])
        keywords = ai_result.get('keywords', [])
        
        print(f"重写文件: {file_path}")
        
        if not os.path.exists(file_path):
            raise ValueError(f"文件不存在: {file_path}")
        
        # 创建文件重写器
        rewriter = FileRewriter(backup_enabled=True)
        
        updates_made = False
        
        # 添加关系链接
        if relationships:
            print(f"添加 {len(relationships)} 个关系链接")
            rel_updated = rewriter.add_relationship_links(file_path, relationships)
            updates_made = updates_made or rel_updated
        
        # 添加关键词链接
        if keywords:
            print(f"添加 {len(keywords)} 个关键词链接")
            kw_updated = rewriter.add_keyword_links(file_path, keywords)
            updates_made = updates_made or kw_updated
        
        # 构建输出结果
        result = {
            'file_path': file_path,
            'updates_made': updates_made,
            'relationships_added': len(relationships) if relationships else 0,
            'keywords_linked': len(keywords) if keywords else 0,
            'timestamp': datetime.now().isoformat(),
            'backup_created': True
        }
        
        if updates_made:
            print(f"文件更新完成: {file_path}")
        else:
            print(f"文件无需更新: {file_path}")
        
        agent.send_output(
            agent_output_name='file_updated',
            agent_result=result
        )
        
    except Exception as e:
        error_msg = f"文件重写Agent错误: {str(e)}"
        print(error_msg)
        agent.send_output(
            agent_output_name='file_updated',
            agent_result={'error': error_msg}
        )

def main():
    agent = MofaAgent(agent_name='cognitive-weaver-file-rewriter')
    run(agent=agent)

if __name__ == "__main__":
    main()
