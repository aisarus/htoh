import os
import streamlit as st
from openai import OpenAI

# Проверяем, что ключ задан
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    st.error("❌ Не найден OPENAI_API_KEY. Добавьте ключ в Secrets и перезапустите приложение.")
    st.stop()

# Инициализируем клиент (openai-python v1+)
client = OpenAI(api_key=OPENAI_API_KEY)

# UI
st.set_page_config(page_title="EFM Translator", layout="wide")
st.title("EFM Translator — Переводчик с человеческого на человеческий")
st.markdown("**Введите два сообщения от людей, а модель проинтерпретирует их через EFM.**")

col1, col2 = st.columns(2)
with col1:
    user_a = st.text_area("Человек A:", height=150)
with col2:
    user_b = st.text_area("Человек B:", height=150)

def efm_prompt(text: str) -> str:
    return f"""
Проанализируй это сообщение по пяти параметрам EFM:
1. Emotion (E): уровень эмоций (0.00–1.00)
2. Fact (F): доля фактов (0.00–1.00)
3. Narrative (N): цель (например просьба, провокация, утешение)
4. Meta-context (M): контекст положения говорящего
5. Bias (B): влияние предыдущей истории

Выводи в табличной форме с краткими пояснениями.

Текст:
{text}
"""

def analyze_efm(text: str) -> str:
    if not text.strip():
        return "—"
    res = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Ты — интерпретатор по модели EFM. Отвечай строго по структуре."},
            {"role": "user",   "content": efm_prompt(text)}
        ],
        temperature=0.4
    )
    return res.choices[0].message.content

if st.button("Проанализировать"):
    with st.spinner("Анализируем…"):
        c1, c2 = st.columns(2)
        with c1:
            st.subheader("Интерпретация A")
            st.markdown(analyze_efm(user_a))
        with c2:
            st.subheader("Интерпретация B")
            st.markdown(analyze_efm(user_b))
