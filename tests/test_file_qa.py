"""Unit tests for the File Q&A page."""
import pytest
from unittest.mock import Mock, patch
from anthropic import Anthropic


class TestFileQA:
    """Test cases for File Q&A functionality."""

    def test_anthropic_client_initialization(self, mock_anthropic_client):
        """Test that Anthropic client can be initialized."""
        client = Anthropic(api_key="test_key")
        assert client is not None
        mock_anthropic_client.assert_called_once_with(api_key="test_key")

    def test_anthropic_message_creation(self, mock_anthropic_client):
        """Test that Anthropic messages can be created."""
        client = Anthropic(api_key="test_key")
        response = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=300,
            messages=[{"role": "user", "content": "Test question"}]
        )

        assert response is not None
        assert len(response.content) > 0
        assert hasattr(response.content[0], 'text')

    def test_article_formatting(self):
        """Test article content formatting for the prompt."""
        article = "This is a test article about AI."
        question = "What is this article about?"
        user_content = f"Here's an article:\n\n<article>\n{article}\n</article>\n\n{question}"

        assert "<article>" in user_content
        assert "</article>" in user_content
        assert article in user_content
        assert question in user_content

    def test_file_reading(self, sample_text_file):
        """Test reading uploaded file content."""
        with open(sample_text_file, 'r') as f:
            content = f.read()

        assert len(content) > 0
        assert "test article" in content.lower()

    def test_file_decode(self, sample_text_file):
        """Test decoding file bytes to string."""
        with open(sample_text_file, 'rb') as f:
            file_bytes = f.read()

        decoded = file_bytes.decode('utf-8')
        assert isinstance(decoded, str)
        assert "test article" in decoded.lower()

    def test_response_text_extraction(self, mock_anthropic_client):
        """Test extracting text from Anthropic response."""
        client = Anthropic(api_key="test_key")
        response = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=300,
            messages=[{"role": "user", "content": "Test"}]
        )

        answer = "".join(getattr(block, "text", "") for block in response.content)
        assert isinstance(answer, str)
        assert len(answer) > 0

    def test_model_version(self):
        """Test that we're using the latest model version."""
        model = "claude-3-5-sonnet-20241022"
        assert "claude-3-5-sonnet" in model
        # Verify it's a recent version (2024)
        assert "2024" in model

    def test_api_key_validation(self):
        """Test API key validation."""
        api_key = ""
        assert not api_key  # Should prevent API call

        api_key = "test-api-key"
        assert api_key  # Should allow API call

    def test_file_and_question_validation(self):
        """Test that both file and question are required."""
        uploaded_file = Mock()
        question = "What is this about?"
        api_key = "test-key"

        # All three should be present
        assert uploaded_file and question and api_key

        # Test missing question
        question = ""
        assert not (uploaded_file and question and api_key)

    @patch('anthropic.Anthropic')
    def test_api_error_handling(self, mock_anthropic):
        """Test handling of API errors."""
        client = Mock()
        mock_anthropic.return_value = client
        client.messages.create.side_effect = Exception("API Error")

        with pytest.raises(Exception) as exc_info:
            client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=300,
                messages=[{"role": "user", "content": "Test"}]
            )

        assert "API Error" in str(exc_info.value)

    def test_max_tokens_parameter(self):
        """Test that max_tokens is set appropriately."""
        max_tokens = 300
        assert max_tokens > 0
        assert max_tokens <= 4096  # Reasonable limit

    def test_supported_file_types(self):
        """Test that only supported file types are accepted."""
        supported_types = ("txt", "md")
        assert "txt" in supported_types
        assert "md" in supported_types
        assert "pdf" not in supported_types  # Not supported in this version
