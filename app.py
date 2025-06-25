# ui/app.py
import streamlit as st
from local_chatbot import LocalChatbot

st.set_page_config(page_title="🧠 Local Chatbot", layout="wide")
st.title("🧠 Local Chatbot")
st.markdown("**All processing is done locally. Files and chats are encrypted.**")

if 'chatbot' not in st.session_state:
    st.session_state.chatbot = LocalChatbot()

if 'messages' not in st.session_state:
    st.session_state.messages = []

bot = st.session_state.chatbot

with st.sidebar:
    st.header("Model")
    models = bot.ollama.available_models
    if models:
        selected = st.selectbox("Choose a model", models)
        bot.ollama.current_model = selected
    else:
        st.warning("No models available.")
        download = st.text_input("Model to download", value="llama3")
        if st.button("Download Model"):
            if bot.ollama.download_model(download):
                st.success(f"Downloaded {download}")
                st.rerun()

    st.header("Documents")
    uploaded = st.file_uploader("Upload files", type=["pdf", "txt", "docx"], accept_multiple_files=True)
    if st.button("Process Files") and uploaded:
        total = sum(bot.upload_file(f) for f in uploaded)
        st.success(f"Processed {total} chunks from {len(uploaded)} file(s)")

    st.metric("Documents", bot.vdb.count_documents())

    st.header("Chat History")
    chats = bot.chatlog.load_all()
    name = st.selectbox("Load chat", ["New Chat"] + list(chats.keys()))
    if st.button("Load") and name != "New Chat":
        bot.chatlog.load(name)
        st.session_state.messages = bot.chatlog.current_chat
        st.rerun()
    new_name = st.text_input("Save as")
    if st.button("Save") and new_name:
        bot.chatlog.save(new_name)
        st.success("Saved")
    if st.button("Clear Chat"):
        bot.chatlog.clear()
        st.session_state.messages = []
        st.rerun()

for m in st.session_state.messages:
    with st.chat_message(m['role']):
        st.markdown(m['content'])

if prompt := st.chat_input("Ask something..."):
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = bot.chat(prompt)
        st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})
