import os
import streamlit as st
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import (
    PyPDFLoader,
    UnstructuredWordDocumentLoader,
    UnstructuredPowerPointLoader,
)
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash-latest")

# Page config
st.set_page_config(page_title="DocuGemini AI", page_icon="📄", layout="wide")

# Theme toggle
dark_mode = st.sidebar.toggle("🌗 Dark Mode", value=False)

# CSS styling
base_bg = "#0e1117" if dark_mode else "#f9fafc"
text_color = "#f0f0f0" if dark_mode else "#1a1a1a"
answer_bg = "#1e2632" if dark_mode else "#edf4ff"
border_color = "#4b8ef6"

st.markdown(f"""
    <style>
        .main {{
            background-color: {base_bg};
        }}
        .title-container {{
            text-align: center;
            padding: 1rem;
            margin-bottom: 1rem;
            color: {text_color};
        }}
        .file-uploader {{
            padding: 1rem;
            border: 2px dashed #c7c7c7;
            border-radius: 10px;
            background-color: #ffffff;
        }}
        .question-box {{
            padding: 1.5rem;
            background-color: #ffffff;
            border-radius: 15px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.05);
            margin-top: 1rem;
        }}
        .answer-box {{
            background-color: {answer_bg};
            color: {text_color};
            padding: 1rem;
            border-left: 5px solid {border_color};
            border-radius: 10px;
            font-size: 1.1rem;
            margin: 0.5rem 0;
        }}
    </style>
""", unsafe_allow_html=True)

# Title
st.markdown(f'<div class="title-container"><h1>📄 DocuGemini: AI Notes Assistant</h1><p style="color:gray;">Chat with your PDF, PPTX, or DOCX using Gemini AI</p></div>', unsafe_allow_html=True)

# Session state to store chat and vectorstore
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "db" not in st.session_state:
    st.session_state.db = None

# Upload section
st.markdown('<div class="file-uploader">', unsafe_allow_html=True)
uploaded_file = st.file_uploader("Upload your notes (PDF, DOCX, PPTX)", type=["pdf", "docx", "pptx"])
st.markdown('</div>', unsafe_allow_html=True)

if uploaded_file:
    file_path = os.path.join("temp", uploaded_file.name)
    os.makedirs("temp", exist_ok=True)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getvalue())

    if uploaded_file.type == "application/pdf":
        loader = PyPDFLoader(file_path)
    elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        loader = UnstructuredWordDocumentLoader(file_path)
    elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.presentationml.presentation":
        loader = UnstructuredPowerPointLoader(file_path)
    else:
        st.error("Unsupported file type.")
        st.stop()

    documents = loader.load()
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    texts = text_splitter.split_documents(documents)

    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    db = FAISS.from_documents(texts, embeddings)

    st.session_state.db = db
    st.success("✅ Document processed! You can now ask questions below.")

# Chat interface
if st.session_state.db:
    st.markdown('<div class="question-box">', unsafe_allow_html=True)

    question = st.text_input("Ask a question about your document:", key="chat_input")

    if question:
        with st.spinner("💬 Gemini is thinking..."):
            docs = st.session_state.db.similarity_search(question)
            input_text = "".join([doc.page_content for doc in docs])

            history_prompt = ""
            for q, a in st.session_state.chat_history:
                history_prompt += f"Q: {q}\nA: {a}\n"

            full_prompt = (
                f"{history_prompt}"
                f"Context:\n{input_text}\n\n"
                f"Q: {question}\nA:"
            )

            response = model.generate_content(full_prompt)
            answer = response.text

            st.session_state.chat_history.append((question, answer))

    # Display chat history
    for q, a in st.session_state.chat_history:
        st.markdown(f"**You:** {q}")
        st.markdown(f'<div class="answer-box">{a}</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown(f"<center><small style='color:{text_color};'>Built with ❤️ using Streamlit and Gemini</small></center>", unsafe_allow_html=True)
