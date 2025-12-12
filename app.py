import streamlit as st
import edge_tts
import asyncio
import os

# --- 页面配置 ---
st.set_page_config(page_title="爸爸的语音助手", page_icon="🎙️")

# --- 样式调整 (让字号更大，适合长辈) ---
st.markdown("""
    <style>
    .stTextArea textarea {
        font-size: 20px !important;
    }
    .stButton button {
        font-size: 20px !important;
        width: 100%;
        background-color: #4CAF50;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 标题 ---
st.title("👴 爸爸的文字转语音工具")
st.write("在下面输入文字，点一下按钮，就能变成声音。")

# --- 核心功能函数 ---
async def generate_audio(text, output_file):
    # 使用微软的 'zh-CN-XiaoxiaoNeural' (女声) 或 'zh-CN-YunxiNeural' (男声)
    # 这里默认选了晓晓，声音很亲切
    voice = 'zh-CN-XiaoxiaoNeural' 
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(output_file)

# --- 界面交互 ---
# 1. 输入框
text_input = st.text_area("输入您想说的话：", height=150, placeholder="比如：今天天气真不错，我想去公园走走。")

# 2. 按钮
if st.button("开始生成语音"):
    if text_input:
        with st.spinner('正在生成中，请稍等...'):
            output_filename = "speech.mp3"
            
            # 运行异步生成函数
            try:
                asyncio.run(generate_audio(text_input, output_filename))
                
                # 成功提示
                st.success("生成成功！点击下方播放或下载 👇")
                
                # 3. 音频播放器 (自带下载功能)
                audio_file = open(output_filename, 'rb')
                audio_bytes = audio_file.read()
                st.audio(audio_bytes, format='audio/mp3')
                
                # 额外的显眼下载按钮 (可选，方便老人直接点)
                st.download_button(
                    label="📥 点击这里下载音频文件",
                    data=audio_bytes,
                    file_name="爸爸的语音.mp3",
                    mime="audio/mp3"
                )
                
            except Exception as e:
                st.error(f"出错了: {e}")
    else:
        st.warning("请先在框里输入文字哦！")