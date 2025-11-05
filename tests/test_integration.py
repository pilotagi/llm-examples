"""Integration tests for Streamlit LLM examples."""
import pytest
import os
from pathlib import Path
from unittest.mock import Mock, patch
import importlib.util


class TestStreamlitPagesIntegration:
    """Integration tests for Streamlit pages."""

    @pytest.fixture
    def project_root(self):
        """Get project root directory."""
        return Path(__file__).parent.parent

    def test_chatbot_file_exists(self, project_root):
        """Test that Chatbot.py exists."""
        chatbot_path = project_root / "Chatbot.py"
        assert chatbot_path.exists()
        assert chatbot_path.is_file()

    def test_file_qa_page_exists(self, project_root):
        """Test that File Q&A page exists."""
        page_path = project_root / "pages" / "1_File_Q&A.py"
        assert page_path.exists()
        assert page_path.is_file()

    def test_chat_with_search_page_exists(self, project_root):
        """Test that Chat with Search page exists."""
        page_path = project_root / "pages" / "2_Chat_with_search.py"
        assert page_path.exists()
        assert page_path.is_file()

    def test_langchain_quickstart_page_exists(self, project_root):
        """Test that LangChain Quickstart page exists."""
        page_path = project_root / "pages" / "3_Langchain_Quickstart.py"
        assert page_path.exists()
        assert page_path.is_file()

    def test_langchain_prompt_template_page_exists(self, project_root):
        """Test that LangChain PromptTemplate page exists."""
        page_path = project_root / "pages" / "4_Langchain_PromptTemplate.py"
        assert page_path.exists()
        assert page_path.is_file()

    def test_requirements_file_exists(self, project_root):
        """Test that requirements.txt exists and has content."""
        req_path = project_root / "requirements.txt"
        assert req_path.exists()

        with open(req_path, 'r') as f:
            content = f.read()

        assert len(content) > 0
        assert "streamlit" in content
        assert "langchain" in content
        assert "openai" in content
        assert "anthropic" in content

    def test_requirements_versions_pinned(self, project_root):
        """Test that requirements have version pins."""
        req_path = project_root / "requirements.txt"

        with open(req_path, 'r') as f:
            lines = f.readlines()

        for line in lines:
            line = line.strip()
            if line and not line.startswith('#'):
                assert "==" in line, f"Version not pinned for: {line}"

    def test_all_imports_available(self):
        """Test that all required imports are available."""
        imports = [
            "streamlit",
            "openai",
            "anthropic",
            "langchain",
            "langchain_openai",
            "langchain_community",
            "langchain_core",
            "langgraph",
        ]

        for module_name in imports:
            try:
                __import__(module_name)
            except ImportError:
                pytest.fail(f"Required module {module_name} is not installed")

    def test_openai_import_structure(self):
        """Test OpenAI import structure."""
        from openai import OpenAI
        assert OpenAI is not None

    def test_anthropic_import_structure(self):
        """Test Anthropic import structure."""
        from anthropic import Anthropic
        assert Anthropic is not None

    def test_langchain_imports(self):
        """Test LangChain imports."""
        from langchain_openai import ChatOpenAI
        from langchain_core.prompts import ChatPromptTemplate
        from langchain_community.tools import DuckDuckGoSearchRun

        assert ChatOpenAI is not None
        assert ChatPromptTemplate is not None
        assert DuckDuckGoSearchRun is not None

    def test_langgraph_imports(self):
        """Test LangGraph imports."""
        from langgraph.prebuilt import create_react_agent

        assert create_react_agent is not None

    def test_python_syntax_chatbot(self, project_root):
        """Test that Chatbot.py has valid Python syntax."""
        chatbot_path = project_root / "Chatbot.py"

        with open(chatbot_path, 'r') as f:
            code = f.read()

        try:
            compile(code, str(chatbot_path), 'exec')
        except SyntaxError as e:
            pytest.fail(f"Syntax error in Chatbot.py: {e}")

    def test_python_syntax_all_pages(self, project_root):
        """Test that all pages have valid Python syntax."""
        pages_dir = project_root / "pages"
        python_files = list(pages_dir.glob("*.py"))

        assert len(python_files) > 0, "No Python files found in pages directory"

        for file_path in python_files:
            with open(file_path, 'r') as f:
                code = f.read()

            try:
                compile(code, str(file_path), 'exec')
            except SyntaxError as e:
                pytest.fail(f"Syntax error in {file_path.name}: {e}")

    def test_streamlit_import_in_all_files(self, project_root):
        """Test that all page files import streamlit."""
        all_files = [project_root / "Chatbot.py"]
        all_files.extend(list((project_root / "pages").glob("*.py")))

        for file_path in all_files:
            with open(file_path, 'r') as f:
                content = f.read()

            assert "import streamlit" in content, f"{file_path.name} doesn't import streamlit"

    def test_api_key_inputs_present(self, project_root):
        """Test that API key inputs are present in pages."""
        # Chatbot should have OpenAI API key input
        with open(project_root / "Chatbot.py", 'r') as f:
            content = f.read()
        assert "openai_api_key" in content

        # File Q&A should have Anthropic API key input
        with open(project_root / "pages" / "1_File_Q&A.py", 'r') as f:
            content = f.read()
        assert "anthropic_api_key" in content

    def test_models_configuration(self, project_root):
        """Test that models are configured correctly."""
        # Check Chatbot uses gpt-4o-mini
        with open(project_root / "Chatbot.py", 'r') as f:
            content = f.read()
        assert "gpt-4o-mini" in content

        # Check File Q&A uses claude-3-5-sonnet-20241022
        with open(project_root / "pages" / "1_File_Q&A.py", 'r') as f:
            content = f.read()
        assert "claude-3-5-sonnet-20241022" in content

    def test_session_state_usage(self, project_root):
        """Test that session state is used for message history."""
        files_to_check = [
            project_root / "Chatbot.py",
            project_root / "pages" / "2_Chat_with_search.py",
        ]

        for file_path in files_to_check:
            with open(file_path, 'r') as f:
                content = f.read()
            assert "st.session_state" in content, f"{file_path.name} doesn't use session state"

    def test_no_deprecated_langchain_apis(self, project_root):
        """Test that deprecated LangChain APIs are not used."""
        with open(project_root / "pages" / "2_Chat_with_search.py", 'r') as f:
            content = f.read()

        # Should NOT use deprecated initialize_agent
        assert "initialize_agent" not in content

        # Should use new create_react_agent
        assert "create_react_agent" in content

    def test_gitignore_exists(self, project_root):
        """Test that .gitignore exists."""
        gitignore_path = project_root / ".gitignore"
        assert gitignore_path.exists()

    def test_readme_exists(self, project_root):
        """Test that README exists."""
        readme_path = project_root / "README.md"
        assert readme_path.exists()

    @pytest.mark.parametrize("dependency", [
        "streamlit==1.51.0",
        "langchain==1.0.3",
        "langchain-openai==1.0.2",
        "langchain-community==0.4.1",
        "openai==2.7.1",
        "anthropic==0.72.0",
    ])
    def test_key_dependencies_versions(self, project_root, dependency):
        """Test that key dependencies have correct versions."""
        req_path = project_root / "requirements.txt"

        with open(req_path, 'r') as f:
            content = f.read()

        assert dependency in content, f"Expected dependency {dependency} not found in requirements.txt"
