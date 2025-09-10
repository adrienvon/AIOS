import os
from pathlib import Path

# 获取项目根目录
package_root = os.path.abspath(os.path.dirname(__file__))
agent_config_dir_path = str(Path(package_root).parent)
