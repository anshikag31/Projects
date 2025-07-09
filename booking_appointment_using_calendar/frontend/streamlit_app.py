import streamlit as st
import requests

st.title("🤖 AI Calendar Booking Assistant")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Show chat history
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# Chat input
user_input = st.chat_input("Ask to book a meeting...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                res = requests.post("https://calendar-zo7z.onrender.com", json={"text": user_input})
                res.raise_for_status()
                reply = res.json().get("response", "⚠️ No response key in backend reply.")
            except Exception:
                reply = "❌ An error occurred while processing your request. Please check the backend logs."

            st.write(reply)
            st.session_state.messages.append({"role": "assistant", "content": reply})
