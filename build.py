import PyInstaller.__main__
import os
import streamlit
import sys

# 1. 自动判断系统分隔符
separator = ';' if sys.platform.startswith('win') else ':'

# 获取 streamlit 库的安装路径
streamlit_path = os.path.dirname(streamlit.__file__)
print(f"Streamlit location: {streamlit_path}")

# 2. 构建数据路径字符串
streamlit_data = f'{streamlit_path}{separator}streamlit'
app_data = f'app.py{separator}.'

# 开始打包
PyInstaller.__main__.run([
    'run.py',
    '--name=爸的语音助手',
    '--onefile',
    #'--windowed',
    '--clean',
    
    # --- 关键修改：强制复制 streamlit 的元数据 ---
    '--copy-metadata=streamlit',
    # ----------------------------------------

    # 包含数据文件
    f'--add-data={streamlit_data}',
    f'--add-data={app_data}',
    
    # 隐藏导入
    '--hidden-import=streamlit',
    '--hidden-import=edge_tts',
    '--hidden-import=asyncio',
])