import os
import traceback

import streamlit as st
from openai import OpenAI


st.set_page_config(page_title="EFM Translator Debug", layout="wide")


# --- Diagnostics Sidebar ---
st.sidebar.title("🛠️ Диагностика")

# 1. Проверяем существование ключа
api_key = os.getenv("OPENAI_API_KEY")
st.sidebar.write("API key loaded:", "✅" if api_key else "❌")

# 2. Версия библиотеки
try:
    from openai import __version__ as openai_version
except (ImportError, AttributeError):
    openai_version = "unknown"
st.sidebar.write("openai lib version:", openai_version)

# 3. Если ключ есть — пробуем получить список моделей
client = None
if api_key:
    try:
        client = OpenAI(api_key=api_key)
        models = client.models.list()
        st.sidebar.write(
            "Models available:",
            [m.id for m in models.data][:5],
            "…" if len(models.data) > 5 else "",
        )
    except Exception as e:
        st.sidebar.write("Error listing models:", e)
        client = None

# Останавливаем, если нет ключа
if not api_key:
    st.sidebar.error("Добавьте OPENAI_API_KEY в Secrets и перезапустите")
    st.stop()

if client is None:
    st.sidebar.error("Не удалось инициализировать OpenAI клиент")
    st.stop()

# --- Main UI ---
st.title("🪲 EFM Translator — Debug-версия")

col1, col2 = st.columns(2)
with col1:
    text_a = st.text_area("Человек A:", height=150)
with col2:
    text_b = st.text_area("Человек B:", height=150)

def make_prompt(msg: str) -> str:
    return f"""
Проанализируй сообщение по модели EFM:

1. Emotion: эмоции
2. Fact: факты
3. Narrative: цель
4. Meta-context: контекст
5. Bias: предвзятость

Текст:
\"\"\"{msg}\"\"\"
"""

def analyze(msg: str) -> str:
    if not msg.strip():
        return ""
    try:
        resp = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Ты — анализатор по модели EFM. Строго по пунктам."},
                {"role": "user",   "content": make_prompt(msg)}
            ],
            temperature=0.4
        )
        return resp.choices[0].message.content
    except Exception as e:
        tb = traceback.format_exc()
        return f"❗ Ошибка при вызове OpenAI API:\n{e}\n\nTraceback:\n{tb}"

if st.button("Проанализировать"):
    st.subheader("Интерпретация A")
    st.text(analyze(text_a))
    st.subheader("Интерпретация B")
    st.text(analyze(text_b))
