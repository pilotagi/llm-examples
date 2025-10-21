import os
import streamlit as st
from langchain_openai import ChatOpenAI

st.title("🦜🔗 Langchain Quickstart App")

with st.sidebar:
    openai_api_key = st.text_input("OpenAI API Key", type="password")


def generate_response(input_text):
    os.environ["OPENAI_API_KEY"] = openai_api_key
    llm = ChatOpenAI(temperature=0.7, model="gpt-4o-mini")
    resp = llm.invoke(input_text)
    st.info(resp.content)


with st.form("my_form"):
    text = st.text_area("Enter text:", "What are 3 key advice for learning how to code?")
    submitted = st.form_submit_button("Submit")
    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
    elif submitted:
        generate_response(text)
