import streamlit as st
import openai
import os

# Подхват ключа из Secret
openai.api_key = os.getenv("OPENAI_API_KEY")

st.set_page_config(page_title="EFM Translator", layout="centered")
st.title("EFM Translator — Переводчик")

# Ввод сообщений
a = st.text_area("Человек A", height=150)
b = st.text_area("Человек B", height=150)

# Формируем EFM-промпт
def efm_prompt(text):
    return f"""
Проанализируй сообщение по модели EFM:
1. Emotion: оценка эмоций
2. Fact: проверяемость фактов
3. Narrative: цель высказывания
4. Meta-context: контекст говорящего
5. Bias: влияние истории диалога

Текст:
{text}
"""

# Отправляем запрос
def analyze(text):
    if not text:
        return ""
    resp = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role":"user", "content": efm_prompt(text)}]
    )
    return resp.choices[0].message.content

# Кнопка анализа
if st.button("Проанализировать"):
    st.subheader("Интерпретация A")
    st.write(analyze(a))
    st.subheader("Интерпретация B")
    st.write(analyze(b))
