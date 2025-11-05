"""Pytest configuration and fixtures for testing Streamlit LLM examples."""
import os
import pytest
from unittest.mock import Mock, MagicMock, patch


@pytest.fixture
def mock_openai_client():
    """Mock OpenAI client for testing."""
    with patch('openai.OpenAI') as mock:
        client = Mock()
        mock.return_value = client

        # Mock chat completions response
        completion = Mock()
        completion.choices = [Mock()]
        completion.choices[0].message = Mock()
        completion.choices[0].message.role = "assistant"
        completion.choices[0].message.content = "This is a test response from GPT."

        client.chat.completions.create.return_value = completion

        yield mock


@pytest.fixture
def mock_anthropic_client():
    """Mock Anthropic client for testing."""
    with patch('anthropic.Anthropic') as mock:
        client = Mock()
        mock.return_value = client

        # Mock messages response
        response = Mock()
        content_block = Mock()
        content_block.text = "This is a test response from Claude."
        response.content = [content_block]

        client.messages.create.return_value = response

        yield mock


@pytest.fixture
def mock_langchain_llm():
    """Mock LangChain ChatOpenAI for testing."""
    with patch('langchain_openai.ChatOpenAI') as mock:
        llm = Mock()
        mock.return_value = llm

        # Mock invoke response
        response = Mock()
        response.content = "This is a test response from LangChain."
        llm.invoke.return_value = response

        yield mock


@pytest.fixture
def mock_duckduckgo_search():
    """Mock DuckDuckGo search tool for testing."""
    with patch('langchain_community.tools.DuckDuckGoSearchRun') as mock:
        search = Mock()
        search.name = "Search"
        mock.return_value = search

        yield mock


@pytest.fixture
def mock_react_agent():
    """Mock LangGraph ReAct agent for testing."""
    with patch('langgraph.prebuilt.create_react_agent') as mock:
        agent = Mock()
        mock.return_value = agent

        # Mock stream response
        message = Mock()
        message.type = "ai"
        message.content = "Test search result: The answer is 42."

        agent.stream.return_value = [
            {"messages": [message]}
        ]

        yield mock


@pytest.fixture
def set_env_vars():
    """Set environment variables for testing."""
    os.environ["OPENAI_API_KEY"] = "test_key"
    os.environ["ANTHROPIC_API_KEY"] = "test_key"
    yield
    # Cleanup
    os.environ.pop("OPENAI_API_KEY", None)
    os.environ.pop("ANTHROPIC_API_KEY", None)


@pytest.fixture
def sample_text_file(tmp_path):
    """Create a sample text file for testing file upload."""
    file_path = tmp_path / "test_article.txt"
    content = "This is a test article about AI and machine learning."
    file_path.write_text(content)
    return file_path
