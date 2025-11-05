import os
import streamlit as st

from langchain_openai import ChatOpenAI
from langchain_community.tools import DuckDuckGoSearchRun
from langgraph.prebuilt import create_react_agent

with st.sidebar:
    openai_api_key = st.text_input("OpenAI API Key", key="langchain_search_api_key_openai", type="password")
    "[View the source code](https://github.com/streamlit/llm-examples/blob/main/pages/2_Chat_with_search.py)"
    "[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/streamlit/llm-examples?quickstart=1)"

st.title("🔎 LangChain - Chat with search")

"""
In this example, we're using a LangGraph ReAct agent with DuckDuckGo search to answer questions.
Try more LangChain 🤝 Streamlit Agent examples at [github.com/langchain-ai/streamlit-agent](https://github.com/langchain-ai/streamlit-agent).
"""

if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "assistant", "content": "Hi, I'm a chatbot who can search the web. How can I help you?"}
    ]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input(placeholder="Who won the Women's U.S. Open in 2018?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()

    os.environ["OPENAI_API_KEY"] = openai_api_key
    llm = ChatOpenAI(model="gpt-4o-mini", streaming=True)
    search = DuckDuckGoSearchRun(name="Search")

    # Create the ReAct agent using the new LangGraph API
    agent_executor = create_react_agent(llm, [search])

    with st.chat_message("assistant"):
        # Create a placeholder for streaming output
        response_placeholder = st.empty()
        full_response = ""

        # Stream the agent's response
        try:
            for chunk in agent_executor.stream(
                {"messages": [("user", prompt)]},
                stream_mode="values"
            ):
                # Get the last message from the agent
                if "messages" in chunk and len(chunk["messages"]) > 0:
                    last_message = chunk["messages"][-1]
                    # Check if it's an AI message
                    if hasattr(last_message, "content") and hasattr(last_message, "type"):
                        if last_message.type == "ai" and last_message.content:
                            full_response = last_message.content
                            response_placeholder.write(full_response)

            # Store the final response
            if full_response:
                st.session_state.messages.append({"role": "assistant", "content": full_response})
            else:
                # Fallback in case we didn't get a response
                fallback_msg = "I'm sorry, I couldn't process that request."
                response_placeholder.write(fallback_msg)
                st.session_state.messages.append({"role": "assistant", "content": fallback_msg})

        except Exception as e:
            error_msg = f"An error occurred: {str(e)}"
            response_placeholder.write(error_msg)
            st.session_state.messages.append({"role": "assistant", "content": error_msg})
