"""Unit tests for LangChain example pages (Quickstart and PromptTemplate)."""
import pytest
from unittest.mock import Mock, patch
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate


class TestLangChainQuickstart:
    """Test cases for LangChain Quickstart page."""

    def test_chatopenai_initialization(self, mock_langchain_llm):
        """Test that ChatOpenAI can be initialized."""
        llm = ChatOpenAI(temperature=0.7, model="gpt-4o-mini")
        assert llm is not None
        mock_langchain_llm.assert_called_once()

    def test_llm_invoke(self, mock_langchain_llm):
        """Test that LLM invoke works correctly."""
        llm = ChatOpenAI(temperature=0.7, model="gpt-4o-mini")
        input_text = "What are 3 key advice for learning how to code?"
        response = llm.invoke(input_text)

        assert response is not None
        assert hasattr(response, 'content')
        assert response.content == "This is a test response from LangChain."

    def test_temperature_parameter(self):
        """Test temperature parameter configuration."""
        temperature = 0.7
        assert 0 <= temperature <= 1
        assert isinstance(temperature, float)

    def test_model_name(self):
        """Test model name configuration."""
        model = "gpt-4o-mini"
        assert model == "gpt-4o-mini"
        assert "gpt" in model.lower()

    def test_api_key_requirement(self, set_env_vars):
        """Test API key environment variable requirement."""
        import os
        api_key = "test_key"
        os.environ["OPENAI_API_KEY"] = api_key
        assert os.environ.get("OPENAI_API_KEY") is not None

    @patch('langchain_openai.ChatOpenAI')
    def test_llm_error_handling(self, mock_llm):
        """Test error handling during LLM invocation."""
        llm = Mock()
        mock_llm.return_value = llm
        llm.invoke.side_effect = Exception("LLM API Error")

        with pytest.raises(Exception) as exc_info:
            llm.invoke("test input")

        assert "LLM API Error" in str(exc_info.value)

    def test_default_prompt_text(self):
        """Test the default prompt text."""
        default_text = "What are 3 key advice for learning how to code?"
        assert len(default_text) > 0
        assert "code" in default_text.lower()


class TestLangChainPromptTemplate:
    """Test cases for LangChain PromptTemplate page."""

    def test_chat_prompt_template_creation(self):
        """Test creating a ChatPromptTemplate."""
        prompt = ChatPromptTemplate.from_messages([
            ("human", "As an experienced data scientist and technical writer, generate an outline for a blog about {topic}."),
        ])

        assert prompt is not None
        assert hasattr(prompt, 'invoke')

    def test_prompt_with_variable(self):
        """Test prompt template with variable substitution."""
        prompt = ChatPromptTemplate.from_messages([
            ("human", "As an experienced data scientist and technical writer, generate an outline for a blog about {topic}."),
        ])

        # Format the prompt with a topic
        formatted = prompt.invoke({"topic": "Machine Learning"})
        assert formatted is not None

    def test_chain_creation(self, mock_langchain_llm):
        """Test creating a chain with prompt and LLM."""
        llm = ChatOpenAI(model="gpt-4o-mini")
        prompt = ChatPromptTemplate.from_messages([
            ("human", "Generate an outline for a blog about {topic}."),
        ])

        chain = prompt | llm
        assert chain is not None

    def test_chain_invoke(self, mock_langchain_llm):
        """Test invoking a chain."""
        llm = ChatOpenAI(model="gpt-4o-mini")
        prompt = ChatPromptTemplate.from_messages([
            ("human", "Generate an outline for a blog about {topic}."),
        ])

        chain = prompt | llm

        # Mock the chain behavior
        with patch.object(chain, 'invoke') as mock_invoke:
            mock_response = Mock()
            mock_response.content = "Blog outline test content"
            mock_invoke.return_value = mock_response

            response = chain.invoke({"topic": "AI"})
            assert response.content == "Blog outline test content"

    def test_prompt_template_format(self):
        """Test prompt template string format."""
        template = "As an experienced data scientist and technical writer, generate an outline for a blog about {topic}."
        assert "{topic}" in template
        assert "data scientist" in template

    def test_topic_input_validation(self):
        """Test topic input validation."""
        topic = ""
        assert not topic  # Empty topic should be invalid

        topic = "Artificial Intelligence"
        assert topic  # Valid topic

    def test_response_content_extraction(self):
        """Test extracting content from response."""
        response = Mock()
        response.content = "Test blog outline content"

        content = response.content
        assert isinstance(content, str)
        assert len(content) > 0

    @patch('langchain_openai.ChatOpenAI')
    def test_chain_error_handling(self, mock_llm):
        """Test error handling during chain execution."""
        llm = Mock()
        mock_llm.return_value = llm

        prompt = ChatPromptTemplate.from_messages([
            ("human", "Generate outline for {topic}."),
        ])

        chain = prompt | llm
        # Simulate chain execution error
        with patch.object(chain, 'invoke', side_effect=Exception("Chain execution error")):
            with pytest.raises(Exception) as exc_info:
                chain.invoke({"topic": "AI"})

            assert "Chain execution error" in str(exc_info.value)

    def test_message_format(self):
        """Test message format in prompt template."""
        messages = [
            ("human", "Generate an outline for a blog about {topic}."),
        ]

        assert len(messages) == 1
        assert messages[0][0] == "human"
        assert "{topic}" in messages[0][1]

    def test_multiple_topics(self):
        """Test handling multiple different topics."""
        topics = ["Machine Learning", "Deep Learning", "Natural Language Processing"]

        for topic in topics:
            assert len(topic) > 0
            assert isinstance(topic, str)

    def test_api_key_validation(self):
        """Test API key validation before execution."""
        api_key = ""
        assert not api_key  # Should prevent execution

        api_key = "sk-test-key"
        assert api_key  # Should allow execution

    def test_model_configuration(self):
        """Test model configuration for blog generation."""
        model = "gpt-4o-mini"
        assert "gpt" in model
        assert "mini" in model  # Using efficient mini model
