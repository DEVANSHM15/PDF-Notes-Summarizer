
# 📄 DocuGemini AI

Chat with your PDF, DOCX, or PPTX documents using Google's Gemini AI, FAISS vector search, and a beautiful Streamlit interface.

---

## 🚀 Features

- 🧠 Ask questions based on uploaded documents
- 📄 Supports **PDF**, **DOCX**, and **PPTX**
- ⚡ Uses **Gemini 1.5 Flash** for fast, intelligent responses
- 🔍 Semantic document search with **FAISS** and **HuggingFace Embeddings**
- 🌓 Light/Dark mode toggle for better UX

---

## 🧰 Built With

| Tool | Description |
|------|-------------|
| ![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?logo=streamlit&logoColor=white) | Web App Framework |
| ![LangChain](https://img.shields.io/badge/LangChain-000000?logo=langchain&logoColor=white) | Document parsing and chunking |
| ![FAISS](https://img.shields.io/badge/FAISS-0077B5?logo=facebook&logoColor=white) | Vector similarity search |
| ![HuggingFace](https://img.shields.io/badge/HuggingFace-FFD21F?logo=huggingface&logoColor=black) | Embedding generation |
| ![Gemini](https://img.shields.io/badge/Google%20Gemini-4285F4?logo=google&logoColor=white) | Generative AI from Google |
| ![python-dotenv](https://img.shields.io/badge/python--dotenv-3466AF?logo=python&logoColor=white) | Environment variable management |

---

## 🛠️ Setup Instructions

### 1. Clone the Repo
```bash
git clone https://github.com/yourusername/docugemini.git
cd docugemini
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure API Key
Create a `.env` file in the root directory:
```env
GEMINI_API_KEY=your_google_generativeai_api_key
```

### 4. Run the App
```bash
streamlit run app.py
```

---

## 📸 Usage

1. Upload a **PDF**, **DOCX**, or **PPTX** document.
2. Ask a question about the content.
3. Get a contextual answer powered by Gemini AI.

---

---

## 📄 License

Licensed under the [MIT License](LICENSE).
