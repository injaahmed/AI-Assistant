import streamlit as st
import ollama
from PyPDF2 import PdfReader
from duckduckgo_search import DDGS

# Page title
st.title("Super AI Assistant")

# Sidebar
st.sidebar.title("AI Menu")

# Mode selection
mode = st.sidebar.selectbox(
    "Choose Mode",
    [
        "Normal Chat",
        "PDF Reader",
        "Coding Assistant",
        "Internet Search"
    ]
)

# Clear chat button
if st.sidebar.button("Clear Chat"):
    st.session_state.messages = []
    st.rerun()

# Memory
if "messages" not in st.session_state:
    st.session_state.messages = []

# Show old chats
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# PDF text
pdf_text = ""

# PDF upload
if mode == "PDF Reader":

    uploaded_file = st.file_uploader(
        "Upload PDF",
        type="pdf"
    )

    if uploaded_file:

        pdf_reader = PdfReader(uploaded_file)

        for page in pdf_reader.pages:
            text = page.extract_text()

            if text:
                pdf_text += text

        st.success("PDF Loaded Successfully!")

# User input
user = st.chat_input("Ask Something")

if user:

    # Show user message
    st.chat_message("user").write(user)

    # Save user message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": user
        }
    )

    # Default system prompt
    system_prompt = (
        "You are a helpful AI assistant. "
        "Give short and clear answers."
    )

    # Coding Assistant Mode
    if mode == "Coding Assistant":

        system_prompt = (
            "You are a coding assistant. "
            "Help with Python, C++, debugging, and programming."
        )

    # PDF Reader Mode
    elif mode == "PDF Reader":

        system_prompt = f"""
        Answer only using this PDF content:

        {pdf_text}

        Keep answers short and clear.
        """

    # Internet Search Mode
    elif mode == "Internet Search":

        search_results = ""

        with DDGS() as ddgs:

            results = ddgs.text(
                user,
                max_results=3
            )

            for result in results:

                search_results += (
                    result["title"] + "\n" +
                    result["body"] + "\n\n"
                )

        system_prompt = f"""
        Answer using these internet search results:

        {search_results}

        Give short and useful answers.
        """

    # AI response
    response = ollama.chat(
        model="phi3",
        messages=[
            {
                "role": "system",
                "content": system_prompt
            }
        ] + st.session_state.messages
    )

    # Get AI reply
    ai_reply = response["message"]["content"]

    # Show AI reply
    st.chat_message("assistant").write(ai_reply)

    # Save AI reply
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": ai_reply
        }
    )