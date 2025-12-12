import PyInstaller.__main__
import os
import streamlit

# 获取 streamlit 库的安装路径，因为我们需要把它的网页素材也打包进去
streamlit_path = os.path.dirname(streamlit.__file__)

print(f"Streamlit location: {streamlit_path}")

# 开始打包
PyInstaller.__main__.run([
    'run.py',                       # 我们的启动脚本
    '--name=爸的语音助手',           # 生成 exe 的名字
    '--onefile',                    # 打包成单个文件
    '--windowed',                   # 不显示黑色命令行窗口(如果报错想看日志，去掉这一行)
    '--clean',                      # 清理缓存
    
    # 下面这两行非常关键：把 app.py 和 streamlit 的库文件塞进去
    f'--add-data={streamlit_path};streamlit',
    '--add-data=app.py;.',          
    
    # 如果你有 bgm.mp3，把下面这行前面的 # 去掉
    # '--add-data=bgm.mp3;.',
    
    # 包含必要的隐藏导入
    '--hidden-import=streamlit',
    '--hidden-import=edge_tts',
    '--hidden-import=asyncio',
])