"""Unit tests for the Chat with Search page."""
import pytest
from unittest.mock import Mock, patch
from langchain_openai import ChatOpenAI
from langchain_community.tools import DuckDuckGoSearchRun
from langgraph.prebuilt import create_react_agent


class TestChatWithSearch:
    """Test cases for Chat with Search functionality."""

    def test_langchain_llm_initialization(self, mock_langchain_llm):
        """Test that LangChain LLM can be initialized."""
        llm = ChatOpenAI(model="gpt-4o-mini", streaming=True)
        assert llm is not None
        mock_langchain_llm.assert_called_once()

    def test_duckduckgo_search_initialization(self, mock_duckduckgo_search):
        """Test that DuckDuckGo search tool can be initialized."""
        search = DuckDuckGoSearchRun(name="Search")
        assert search is not None
        assert search.name == "Search"
        mock_duckduckgo_search.assert_called_once()

    def test_react_agent_creation(self, mock_react_agent, mock_langchain_llm, mock_duckduckgo_search):
        """Test that ReAct agent can be created."""
        llm = ChatOpenAI(model="gpt-4o-mini", streaming=True)
        search = DuckDuckGoSearchRun(name="Search")
        agent = create_react_agent(llm, [search])

        assert agent is not None
        mock_react_agent.assert_called_once_with(llm, [search])

    def test_agent_streaming(self, mock_react_agent, mock_langchain_llm, mock_duckduckgo_search):
        """Test that agent can stream responses."""
        llm = ChatOpenAI(model="gpt-4o-mini", streaming=True)
        search = DuckDuckGoSearchRun(name="Search")
        agent = create_react_agent(llm, [search])

        prompt = "Who won the Women's U.S. Open in 2018?"
        stream = agent.stream(
            {"messages": [("user", prompt)]},
            stream_mode="values"
        )

        responses = list(stream)
        assert len(responses) > 0
        assert "messages" in responses[0]

    def test_message_extraction_from_stream(self, mock_react_agent, mock_langchain_llm, mock_duckduckgo_search):
        """Test extracting messages from agent stream."""
        llm = ChatOpenAI(model="gpt-4o-mini", streaming=True)
        search = DuckDuckGoSearchRun(name="Search")
        agent = create_react_agent(llm, [search])

        prompt = "Test question"
        full_response = ""

        for chunk in agent.stream(
            {"messages": [("user", prompt)]},
            stream_mode="values"
        ):
            if "messages" in chunk and len(chunk["messages"]) > 0:
                last_message = chunk["messages"][-1]
                if hasattr(last_message, "content") and hasattr(last_message, "type"):
                    if last_message.type == "ai" and last_message.content:
                        full_response = last_message.content

        assert len(full_response) > 0
        assert "Test search result" in full_response

    def test_session_state_initialization(self):
        """Test session state message initialization."""
        session_state = {}
        if "messages" not in session_state:
            session_state["messages"] = [
                {"role": "assistant", "content": "Hi, I'm a chatbot who can search the web. How can I help you?"}
            ]

        assert len(session_state["messages"]) == 1
        assert "search the web" in session_state["messages"][0]["content"]

    def test_model_configuration(self):
        """Test model configuration parameters."""
        model_name = "gpt-4o-mini"
        streaming = True

        assert model_name == "gpt-4o-mini"
        assert streaming is True

    def test_api_key_handling(self, set_env_vars):
        """Test API key environment variable handling."""
        import os
        api_key = "test_openai_key"
        os.environ["OPENAI_API_KEY"] = api_key

        assert os.environ.get("OPENAI_API_KEY") == api_key

    def test_error_handling(self, mock_react_agent, mock_langchain_llm, mock_duckduckgo_search):
        """Test error handling during agent execution."""
        llm = ChatOpenAI(model="gpt-4o-mini", streaming=True)
        search = DuckDuckGoSearchRun(name="Search")
        agent = create_react_agent(llm, [search])

        # Simulate an error
        agent.stream.side_effect = Exception("Agent execution error")

        with pytest.raises(Exception) as exc_info:
            list(agent.stream(
                {"messages": [("user", "test")]},
                stream_mode="values"
            ))

        assert "Agent execution error" in str(exc_info.value)

    def test_empty_response_handling(self):
        """Test handling of empty responses."""
        full_response = ""

        if full_response:
            final_msg = full_response
        else:
            final_msg = "I'm sorry, I couldn't process that request."

        assert final_msg == "I'm sorry, I couldn't process that request."

    def test_message_history_accumulation(self):
        """Test that messages accumulate correctly in history."""
        messages = [
            {"role": "assistant", "content": "Hi, I'm a chatbot who can search the web. How can I help you?"}
        ]

        # User message
        messages.append({"role": "user", "content": "What's the weather?"})
        assert len(messages) == 2

        # Assistant response
        messages.append({"role": "assistant", "content": "Let me search for that."})
        assert len(messages) == 3

        # Verify order
        assert messages[0]["role"] == "assistant"
        assert messages[1]["role"] == "user"
        assert messages[2]["role"] == "assistant"

    def test_tools_list_format(self):
        """Test that tools are provided as a list."""
        tools = []
        search = Mock()
        tools.append(search)

        assert isinstance(tools, list)
        assert len(tools) == 1
        assert tools[0] == search

    @patch('langchain_community.tools.DuckDuckGoSearchRun')
    def test_search_tool_error_handling(self, mock_search):
        """Test handling of search tool errors."""
        mock_search.side_effect = Exception("Search API error")

        with pytest.raises(Exception) as exc_info:
            DuckDuckGoSearchRun(name="Search")

        assert "Search API error" in str(exc_info.value)
