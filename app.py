import streamlit as st
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from io import BytesIO

def get_pdf_text(docs):
    text = ""
    for pdf in docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text


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
                # Pass a list containing the file-like object to the get_pdf_text function
                raw_text = get_pdf_text([pdf_files])
                # get text chunks
                st.write(raw_text)
 
if __name__ == '__main__':
    main()
