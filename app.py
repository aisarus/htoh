
import streamlit as st
import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

st.set_page_config(page_title="EFM Translator", layout="wide")
st.title("EFM Translator — Переводчик с человеческого на человеческий")
st.markdown("**Введите сообщения от двух людей, и модель попытается интерпретировать их через EFM (Emotion, Fact, Narrative, Meta-context, Bias).**")

col1, col2 = st.columns(2)
with col1:
    user_a_input = st.text_area("Человек A:", height=150)
with col2:
    user_b_input = st.text_area("Человек B:", height=150)

def efm_prompt(text):
    return f"""
Проанализируй следующее сообщение по пяти параметрам EFM:
1. Emotion (E): уровень выраженной эмоции (0.00 - 1.00)
2. Fact (F): насколько сообщение опирается на факты (0.00 - 1.00)
3. Narrative (N): цель сообщения
4. Meta-context (M): краткое описание положения говорящего
5. Bias (B): на что влияет история сообщений и взаимодействий

Выводи результат в табличной форме с пояснением.
Текст:
"""{text}"""
"""

def analyze_efm(text):
    if not text.strip():
        return "—"
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Ты — интерпретатор по модели EFM. Отвечай строго по структуре."},
            {"role": "user", "content": efm_prompt(text)}
        ],
        temperature=0.4
    )
    return response['choices'][0]['message']['content']

if st.button("Проанализировать"):
    col3, col4 = st.columns(2)
    with col3:
        st.subheader("Интерпретация A")
        st.markdown(analyze_efm(user_a_input))
    with col4:
        st.subheader("Интерпретация B")
        st.markdown(analyze_efm(user_b_input))
