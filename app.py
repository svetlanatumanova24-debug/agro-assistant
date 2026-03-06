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
uploaded_file = st.file_uploader("Загрузите PDF-книгу по агрономии", type="pdf")

else:
st.warning("Сначала введите API-ключ в поле слева.")
