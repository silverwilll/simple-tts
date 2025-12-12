import streamlit as st
import edge_tts
import asyncio
import os

# --- 页面配置 ---
st.set_page_config(page_title="爸爸的语音助手", page_icon="🎙️")

# --- 样式调整 (大字号 + 界面优化) ---
st.markdown("""
    <style>
    /* 输入框文字变大 */
    .stTextArea textarea {
        font-size: 22px !important;
        line-height: 1.5 !important;
    }
    /* 按钮变大变绿 */
    .stButton button {
        font-size: 24px !important;
        width: 100%;
        background-color: #4CAF50;
        color: white;
        padding: 15px 0;
        border-radius: 10px;
    }
    /* 单选按钮文字变大 */
    .stRadio label {
        font-size: 20px !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 标题 ---
st.title("👴 爸爸的文字转语音工具")
st.write("请在下面的大框里写字，然后选择一个喜欢的声音。")

# --- 声音字典 (方便添加更多声音) ---
VOICES = {
    "👩 温柔女声 (晓晓)": "zh-CN-XiaoxiaoNeural",
    "👨 稳重男声 (云希)": "zh-CN-YunxiNeural",
    "🎙️ 新闻主播 (云扬 - 很有磁性)": "zh-CN-YunyangNeural"
}

# --- 核心功能函数 ---
async def generate_audio(text, voice_key, output_file):
    # 根据选择的中文名，获取对应的英文代码
    voice_id = VOICES[voice_key] 
    communicate = edge_tts.Communicate(text, voice_id)
    await communicate.save(output_file)

# --- 界面交互 ---

# 1. 布局：分两列，左边选声音，右边空着 (或者你可以把其他选项放右边)
#    但在手机上会自动变成上下排列，对老人家更友好
st.subheader("1. 先选一个读这一段的人：")
# 使用单选按钮，比下拉菜单更直观，一眼可见所有选项
selected_voice = st.radio(
    "声音列表", 
    options=list(VOICES.keys()), 
    index=0, # 默认选中第一个
    label_visibility="collapsed" # 隐藏自带的小标题，更简洁
)

st.subheader("2. 在这里输入文字：")
# 2. 输入框 (height=400 拉得更长了)
text_input = st.text_area(
    "输入框", 
    height=400, 
    placeholder="比如：今天天气真不错，我想去公园走走..."
)

# 3. 按钮
if st.button("开始生成语音 ▶️"):
    if text_input:
        with st.spinner('正在生成中，请稍等...'):
            output_filename = "speech.mp3"
            
            try:
                # 运行异步生成函数，传入用户选择的声音
                asyncio.run(generate_audio(text_input, selected_voice, output_filename))
                
                # 成功提示
                st.success("生成成功！点击下方播放 👇")
                
                # 读取音频
                audio_file = open(output_filename, 'rb')
                audio_bytes = audio_file.read()
                
                # 4. 音频播放器
                st.audio(audio_bytes, format='audio/mp3')
                
                # 5. 大号下载按钮
                st.download_button(
                    label="📥 点击下载这个音频",
                    data=audio_bytes,
                    file_name="爸爸的语音.mp3",
                    mime="audio/mp3"
                )
                
            except Exception as e:
                st.error(f"出错了，请检查网络: {e}")
    else:
        st.warning("⚠️ 还没写字呢，请先在上面的大框里输入文字。")