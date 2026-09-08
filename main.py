import os
import streamlit as st

try:
    from dotenv import load_dotenv
except ModuleNotFoundError:
    def load_dotenv():
        return False

try:
    import google.generativeai as genai
except ModuleNotFoundError:
    genai = None


load_dotenv()
api_key = os.getenv("GEMINI_API_KEY") or st.secrets.get("GEMINI_API_KEY")

model = None
if api_key and genai:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(
        model_name="gemini-3.6-flash",
        system_instruction="""Bạn là một gia sư AI, chuyên giải thích khái niệm kỹ thuật
cho sinh viên công nghệ thông tin theo mảng AI engineering. Luôn:
- Giải thích cặn kẽ, có ví dụ cụ thể
- Liên hệ với dự án thực tế nếu phù hợp
- Tránh dùng thuật ngữ mà không giải thích"""
    )

st.set_page_config(page_title="Study AI", page_icon="🎓")
st.title("🎓 Study AI — Trợ lý học tập")

if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.messages.append({
        "role": "assistant",
        "content": "Chào bạn! Mình là Study AI. Hãy hỏi mình về các khái niệm kỹ thuật trong AI engineering nhé."
    })

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

question = st.chat_input("Nhập câu hỏi...")
if question:
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.write(question)

    with st.chat_message("assistant"):
        if not model:
            reply = "Chưa tìm thấy GEMINI_API_KEY. Hãy tạo file .env và thêm: GEMINI_API_KEY=your_key_here"
        else:
            with st.spinner("Đang suy nghĩ..."):
                try:
                    reply = model.generate_content(question).text
                except Exception as error:
                    reply = f"Mình chưa thể trả lời lúc này. Chi tiết: {error}"
        st.write(reply)
    st.session_state.messages.append({"role": "assistant", "content": reply})