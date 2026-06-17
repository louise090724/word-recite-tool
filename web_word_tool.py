import streamlit as st 
import random 
import os 
# 数据文件 
FILE_PATH = "words.txt" 
# 初始化页面配置 
st.set_page_config(page_title="单词背诵打卡工具", layout="centered") 
# 加载单词 
def load_words(): word_list = [] if os.path.exists(FILE_PATH): with open(FILE_PATH, "r", encoding="utf-8") as f: lines = f.readlines() for line in lines: line = line.strip() if line and "||" in line: en, cn = line.split("||") word_list.append((en.strip(), cn.strip())) return word_list 
# 保存单词 
def save_word(en, cn): with open(FILE_PATH, "a", encoding="utf-8") as f: f.write(f"{en}||{cn}\n") 
  # 初始化会话状态（记录当前单词、已背诵列表） 
if "current_idx" not in st.session_state: st.session_state.current_idx = -1 if "finished" not in st.session_state: st.session_state.finished = [] 
# 主页面 
st.title("📚 英语单词背诵打卡工具") st.divider() 
# 1. 单词录入区域 
st.subheader("📝 添加新单词") col1, col2 = st.columns(2) with col1: en_input = st.text_input("英文单词") with col2: cn_input = st.text_input("中文释义") if st.button("✅ 添加单词"): if en_input.strip() and cn_input.strip(): save_word(en_input, cn_input) st.success("单词添加成功！") else: st.warning("单词和释义不能为空！") st.divider() 
# 2. 背诵区域 
st.subheader("🧠 开始背诵") word_list = load_words() un_finish = [i for i in range(len(word_list)) if i not in st.session_state.finished] 
# 功能按钮 
btn1, btn2, btn3 = st.columns(3) with btn1: random_btn = st.button("🎲 随机出题") with btn2: show_btn = st.button("👀 显示释义") with btn3: card_btn = st.button("✔️ 完成打卡") 
  # 随机出题 
if random_btn: if not word_list: st.warning("词库暂无单词，请先添加！") elif not un_finish: st.info("所有单词已背诵完成！") st.session_state.current_idx = -1 else: st.session_state.current_idx = random.choice(un_finish) 
# 展示当前单词 
current_idx = st.session_state.current_idx if current_idx != -1: en_text, _ = word_list[current_idx] st.markdown(f"### 单词：{en_text}") else: st.markdown("### 单词：请点击【随机出题】") 
# 显示释义 
if show_btn and current_idx != -1: _, cn_text = word_list[current_idx] st.markdown(f"### 释义：{cn_text}") elif show_btn and current_idx == -1: st.warning("请先随机出题！") 
# 完成打卡 
if card_btn: if current_idx == -1: st.warning("请先出题再打卡！") elif current_idx not in st.session_state.finished: st.session_state.finished.append(current_idx) st.success("打卡成功！") st.divider() 
# 3. 统计区域（核心数据展示） 
total = len(word_list) finish_num = len(st.session_state.finished) unfinish_num = total - finish_num st.info(f"📊 统计：总单词 {total} 个 | 已背诵 {finish_num} 个 | 未背诵 {unfinish_num} 个")
