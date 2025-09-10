import os
import time
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from mofa.agent_build.base.base_agent import MofaAgent, run_agent

class MarkdownFileHandler(FileSystemEventHandler):
    """监控Markdown文件变化的处理器"""
    
    def __init__(self, agent):
        self.agent = agent
        
    def on_modified(self, event):
        if not event.is_directory and event.src_path.endswith('.md'):
            print(f"检测到文件变化: {event.src_path}")
            self.send_file_change(event.src_path)
    
    def on_created(self, event):
        if not event.is_directory and event.src_path.endswith('.md'):
            print(f"检测到新文件: {event.src_path}")
            self.send_file_change(event.src_path)
    
    def send_file_change(self, file_path):
        """发送文件变化信息"""
        try:
            # 读取文件内容
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            file_info = {
                'file_path': file_path,
                'file_name': os.path.basename(file_path),
                'content': content,
                'timestamp': time.time()
            }
            
            self.agent.send_output(
                agent_output_name='file_changed',
                agent_result=file_info
            )
            print(f"已发送文件变化: {file_path}")
            
        except Exception as e:
            print(f"读取文件失败 {file_path}: {e}")

@run_agent
def run(agent: MofaAgent):
    """
    文件监控Agent主函数
    监控Obsidian vault中的Markdown文件变化
    """
    try:
        # 获取监控路径
        vault_path = agent.receive_parameter('vault_path')
        print(f"开始监控路径: {vault_path}")
        
        if not os.path.exists(vault_path):
            raise ValueError(f"路径不存在: {vault_path}")
        
        # 创建文件处理器
        event_handler = MarkdownFileHandler(agent)
        
        # 创建观察者
        observer = Observer()
        observer.schedule(event_handler, vault_path, recursive=True)
        
        # 启动监控
        observer.start()
        print(f"文件监控已启动，监控路径: {vault_path}")
        
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()
            print("文件监控已停止")
        
        observer.join()
        
    except Exception as e:
        error_msg = f"文件监控Agent错误: {str(e)}"
        print(error_msg)
        agent.send_output(
            agent_output_name='file_changed',
            agent_result={'error': error_msg}
        )

def main():
    agent = MofaAgent(agent_name='cognitive-weaver-file-monitor')
    run(agent=agent)

if __name__ == "__main__":
    main()
