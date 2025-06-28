
import streamlit as st
import pandas as pd
import random

st.set_page_config(page_title="安安识字", page_icon="icon.png", layout="centered")

@st.cache_data
def load_data():
    df = pd.read_csv("wordbank_part_1.csv")
    return df

df = load_data()
all_pinyins = list(set(df["pinyin"].tolist()))

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

def check_answer(correct_pinyin, user_choice):
    return correct_pinyin == user_choice

def update_question():
    st.session_state.index += 1
    st.session_state.feedback = ""
    st.session_state.answered_correctly = False

st.markdown("<div style='margin-top: -150px;'></div>", unsafe_allow_html=True)

col1, col2 = st.columns([3, 8])
with col1:
    st.image("icon.png", width=120)
with col2:
    st.markdown("### 安安识字")

st.markdown(f"字库：{len(df)} &nbsp;&nbsp; 完成：{st.session_state.index}", unsafe_allow_html=True)

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

with st.sidebar:
    if st.button("拼音"):
        st.session_state.show_pinyin = not st.session_state.show_pinyin

    st.markdown("### ❌ 错字表")
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

st.markdown(f"### 请选择拼音： **{character}**")

if not st.session_state.show_options:
    if st.button("👉 请选择拼音"):
        st.session_state.show_options = True
        st.rerun()
else:
    st.markdown("&nbsp;", unsafe_allow_html=True)

placeholder = st.empty()

if st.session_state.show_options:
    with placeholder.container():
        choice = st.radio(" ", options, key=f"q_{st.session_state.index}")
        st.markdown("<div style='height: 20px'></div>", unsafe_allow_html=True)
else:
    with placeholder.container():
        st.markdown("<div style='height: 140px'></div>", unsafe_allow_html=True)

if st.session_state.show_options:
    if st.button("提交"):
        if check_answer(correct_pinyin, choice):
            st.success("✅ 正确！")
            st.session_state.answered_correctly = True
            if not st.session_state.had_error:
                st.session_state.correct_count += 1
            example_text = "、".join(examples)
            st.markdown(f"#### 示例词：<span style='font-size:18px;'>{example_text}</span>", unsafe_allow_html=True)

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






