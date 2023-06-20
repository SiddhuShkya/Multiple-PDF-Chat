import os
import streamlit as st
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import HuggingFaceInstructEmbeddings
from langchain.vectorstores import FAISS
from io import BytesIO

# streamlit run app.py

def get_pdf_text(docs):
    text = ""
    for pdf in docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text

def get_text_chunks(text):
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_text(text)
    return chunks

def get_vector_store(text_chunks):
    embeddings = HuggingFaceInstructEmbeddings(model_name="hkunlp/instructor-xl")
    vectorstore = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
    return vectorstore

def main():
    load_dotenv()
    st.set_page_config(page_title="Chat With PDFs", page_icon=":books:")
    st.header("Chat with PDFs :books:")
    st.text_input("Ask a question about your Docs:")
    with st.sidebar:
        st.subheader("Your documents")
        pdf_docs = st.file_uploader("upload your PDFs here and Click on 'Process'")
        if st.button("Process"):
            with st.spinner("Processing"):
                # Convert pdf_docs into a file-like object
                pdf_files = BytesIO(pdf_docs.read())
                # get pdf text
                raw_text = get_pdf_text([pdf_files])
                # get text chunks
                text_chunks = get_text_chunks(raw_text)
                # create vector store
                vector_store = get_vector_store(text_chunks)
                print("completed")

if __name__ == '__main__':
    main()
