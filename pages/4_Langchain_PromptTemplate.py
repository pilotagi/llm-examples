import os
import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

st.title("🦜🔗 Langchain - Blog Outline Generator App")

openai_api_key = st.sidebar.text_input("OpenAI API Key", type="password")


def blog_outline(topic):
    os.environ["OPENAI_API_KEY"] = openai_api_key
    llm = ChatOpenAI(model="gpt-4o-mini")
    prompt = ChatPromptTemplate.from_messages([
        ("human", "As an experienced data scientist and technical writer, generate an outline for a blog about {topic}."),
    ])
    chain = prompt | llm
    response = chain.invoke({"topic": topic})
    return st.info(response.content)


with st.form("myform"):
    topic_text = st.text_input("Enter prompt:", "")
    submitted = st.form_submit_button("Submit")
    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
    elif submitted:
        blog_outline(topic_text)
