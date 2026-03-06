import streamlit as st
from langchain_community.document_loaders import PyPDFLoader
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA
import os

st.set_page_config(page_title="Агро-Ассистент", layout="wide")
st.title("🌱 Агент-Агроном (RAG-система)")

st.sidebar.header("Настройки")
api_key = st.sidebar.text_input("Введите ваш OpenAI API Key", type="password")

if api_key:
    os.environ["OPENAI_API_KEY"] = api_key
    uploaded_file = st.file_uploader("Загрузите PDF-книгу", type="pdf")
    if uploaded_file:
        with open("temp.pdf", "wb") as f:
            f.write(uploaded_file.getbuffer())
        with st.spinner("Изучаю книгу..."):
            loader = PyPDFLoader("temp.pdf")
            pages = loader.load_and_split()
            vectorstore = Chroma.from_documents(pages, OpenAIEmbeddings())
            qa = RetrievalQA.from_chain_type(
               llm=ChatOpenAI(model_name="gpt-4o"),
               chain_type="stuff",
               retriever=vectorstore.as_retriever()
            )
            st.success("Готово!")
        query = st.text_input("Ваш вопрос:")
        if query:
            response = qa.run(query)
            st.info(response)
else:
    st.warning("Введите API-ключ в меню слева")
