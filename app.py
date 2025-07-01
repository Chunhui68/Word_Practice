# 初始设置和样式
import streamlit as st  # 引入 Streamlit，用于快速搭建交互式网页
import pandas as pd # 引入 pandas，用于读取和操作表格数据
import random # 引入 random，用于打乱、随机抽样
import base64 # 引入 base64，用于把图片编码为 base64 字符串

# === 页面基础配置 ===
st.set_page_config(
    page_title="安安识字",            # 浏览器标签页标题
    page_icon="icon.png",            # 标签页图标
    layout="centered"                # 整体布局居中
)

# === 注入全局 CSS，去除顶部空白，并放大字体 ===
st.markdown(
    """
    <style>
    /* 整个内容容器上方内边距设为 0 */
      .block-container { padding-top: 0rem !important; }
    /* 主视图最外层也去掉一点空 */
      .appview-container .main { padding-top: 0rem !important; }
    /* 如果还有多余 margin，请一并清零 */
      header, footer { margin-top: 0 !important; }

    /* —— 收紧“字”标题（h1）和下方信息之间的距离 —— */
        div.stMarkdown h1 {
        margin-bottom: 0rem !important;   /* 默认可能是 1rem~1.5rem，改小一点 */
    }
      
    /* 下方“字库：… 完成：…”那行也是 Markdown，给它一点上边距 */
        div.stMarkdown + div.stMarkdown {
        margin-top: 0rem !important;
    }

    /* —— 收紧拼音选项和“提交”按钮之间的距离 —— */
    /* radio 外层 div（占位符）和下面按钮间隙 */
        div[role="radiogroup"] {
        margin-bottom: 0rem !important;
    }
      
    /* 针对提交按钮自身上边距 */
        button[data-testid="stButton"] {
        margin-top: 0rem !important;
    }
    
    /* —— 全局字体放大 —— */
    html, body, [class*="css"] {
        font-size: 28px !important;    /* 根据需要改成 22px / 24px ... */
    }

    /* —— 特别放大 pinyin 单选项的文字 —— */
    /* Streamlit 的 radio option 会把文本包在 <label><span> 里： */
    div[role="radiogroup"] label span {
        font-size: 36px !important;    /* 这里就是拼音选项的字号 */
        font-weight: 700 !important;
    }

    /* —— 如果你还有其它想单独调大的，比如标题 h3 —— */
    div.stMarkdown h3 {
        font-size: 28px !important;
        font-weight: 700 !important;
    }

    /* —— 放大示例词标题 h5 —— */
      div.stMarkdown h5 {
          font-size: 28px !important;
    }

    /* 把所有 stButton 里的按钮字体放大到 80px */
      div.stButton > button {
        font-size: 100px !important;
        line-height: 1 !important;
        font-weight: 700 !important;
        padding: 0.1em 0.2em !important;

    </style>
    """,
    unsafe_allow_html=True,
)

# 加载数据
@st.cache_data
def load_data():
    df = pd.read_csv("wordbank_part_1.csv")
    return df

df = load_data()
all_pinyins = list(set(df["pinyin"].tolist()))

# 会话状态初始化
if 'correct_count' not in st.session_state:
    st.session_state.correct_count = 0
if 'index' not in st.session_state:
    st.session_state.index = 0
if 'feedback' not in st.session_state:
    st.session_state.feedback = ""
if 'answered_correctly' not in st.session_state:
    st.session_state.answered_correctly = False
if "show_options" not in st.session_state:
    st.session_state.show_options = False
if "wrong_chars" not in st.session_state:
    st.session_state.wrong_chars = []
if 'show_pinyin' not in st.session_state:
    st.session_state.show_pinyin = True
if 'had_error' not in st.session_state:
    st.session_state.had_error = False

# 辅助函数
def check_answer(correct_pinyin, user_choice):
    return correct_pinyin == user_choice

def update_question():
    st.session_state.index += 1
    st.session_state.feedback = ""
    st.session_state.answered_correctly = False

# 把 icon.png 读成 base64 字符串
def get_base64_icon(path: str) -> str:
    with open(path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

icon_b64 = get_base64_icon("icon.png")

# 页面布局
#st.markdown("<div style='margin-top: -500px;'></div>", unsafe_allow_html=True)

st.markdown(
    f"""
    <div style="display: flex; align-items: center; margin-bottom: 0px;">
      <img src="data:image/png;base64,{icon_b64}" width="120" style="margin-right: 16px;" />
      <h1 style="margin: 0; line-height: 1;">安安识字</h1>
    </div>
    """,
    unsafe_allow_html=True,
)


st.markdown(f"字库：{len(df)} &nbsp;&nbsp; 完成：{st.session_state.index}", unsafe_allow_html=True)

# 题目显示逻辑
if st.session_state.index >= len(df):
    st.success("你完成了全部题目，共 {} 题，答对了 {} 题".format(len(df), st.session_state.correct_count))
    if st.button("重新开始"):
        st.session_state.index = 0
        st.session_state.feedback = ""
        st.session_state.answered_correctly = False
        st.session_state.wrong_chars = []
        st.session_state.had_error = False
        st.session_state.correct_count = 0
        st.stop()

# 侧边栏设置
with st.sidebar:
    if st.button("拼音"):
        st.session_state.show_pinyin = not st.session_state.show_pinyin

    st.markdown("#### ❌ 错字表")
    wrong_chars = st.session_state.get("wrong_chars", [])

    if wrong_chars:
        for char in wrong_chars:
            pinyin = df.loc[df["character"] == char, "pinyin"].values[0]
            if st.session_state.show_pinyin:
                st.markdown(f"{char} ({pinyin})")
            else:
                st.markdown(f"{char}")
    else:
        st.markdown("暂无错字")

if "show_pinyin" not in st.session_state:
    st.session_state.show_pinyin = True

if st.session_state.index >= len(df):
    st.stop()

row = df.iloc[st.session_state.index]
character = row["character"]
correct_pinyin = row["pinyin"]

key_options = f"options_{st.session_state.index}"
if key_options not in st.session_state:
    distractors = [p for p in all_pinyins if p != correct_pinyin]
    random_options = random.sample(distractors, 3)
    random_options.append(correct_pinyin)
    random.shuffle(random_options)
    st.session_state[key_options] = random_options

options = st.session_state[key_options]

examples = row["examples"].split("|")

# 交互逻辑
# 点击汉字本身来显示拼音选项
if not st.session_state.show_options:
    # 用 st.button 把 character 变成按钮
    if st.button(f"## {character}", key="char_btn"):
        st.session_state.show_options = True
        st.rerun()
else:
    # 已经点击过，就静态地显示汉字
    st.markdown(f"## {character}")

    # 紧凑显示拼音选项
    choice = st.radio(
        "请选择正确的拼音：", 
        options, 
        key=f"q_{st.session_state.index}",
        horizontal=True
    )
    
    # 减小选项与提交按钮的间距
    # st.markdown("<div style='height: 2px'></div>", unsafe_allow_html=True)

# 答题处理
if st.session_state.show_options:
    if st.button("提交"):
        if check_answer(correct_pinyin, choice):
            st.success("✅ 正确！")
            st.session_state.answered_correctly = True
            if not st.session_state.had_error:
                st.session_state.correct_count += 1
            example_text = "、".join(examples)
            st.markdown(f"##### 示例词：<span style='font-size:40px;'>{example_text}</span>", unsafe_allow_html=True)

        else:
            st.warning("❌ 错误，请再试一次。")
            st.session_state.answered_correctly = False
            st.session_state.had_error = True

if st.session_state.answered_correctly:
    if st.button("下一题"):
        if st.session_state.had_error:
            if character not in st.session_state.wrong_chars:
                st.session_state.wrong_chars.append(character)
        st.session_state.had_error = False
        update_question()
        st.session_state.show_options = False
        st.rerun()
