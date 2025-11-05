# 🎈 Streamlit + LLM Examples App

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/streamlit/llm-examples?quickstart=1)

Starter examples for building LLM apps with Streamlit.

## Overview of the App

This app showcases a growing collection of LLM minimum working examples.

Current examples include:

- Chatbot
- File Q&A
- Langchain Quickstart
- Langchain PromptTemplate
- LangChain Search

## Demo App

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://llm-examples.streamlit.app/)

## Recent Updates (2025)

### Dependency Upgrades

All dependencies have been upgraded to the latest versions:

- **Streamlit**: 1.51.0
- **LangChain**: 1.0.3 (migrated from deprecated APIs)
- **OpenAI**: 2.7.1
- **Anthropic**: 0.72.0 (using Claude 3.5 Sonnet 20241022)
- **LangGraph**: Latest (replaced deprecated initialize_agent)

### Breaking Changes Fixed

- Migrated from deprecated `initialize_agent` to new `create_react_agent` from LangGraph
- Updated to latest Claude model version
- Fixed all compatibility issues with LangChain 1.0+

### Testing

Comprehensive test suite added with 80+ tests covering:

- Unit tests for all pages
- Integration tests for file structure and syntax
- API compatibility validation
- No deprecated API usage

Run tests:
```bash
pip install -r requirements-test.txt
pytest tests/
```

See `tests/README.md` for detailed testing documentation.

## Get an OpenAI API key

You can get your own OpenAI API key by following the following instructions:

1. Go to https://platform.openai.com/account/api-keys.
2. Click on the `+ Create new secret key` button.
3. Next, enter an identifier name (optional) and click on the `Create secret key` button.

## Enter the OpenAI API key in Streamlit Community Cloud

To set the OpenAI API key as an environment variable in Streamlit apps, do the following:

1. At the lower right corner, click on `< Manage app` then click on the vertical "..." followed by clicking on `Settings`.
2. This brings the **App settings**, next click on the `Secrets` tab and paste the API key into the text box as follows:

```sh
OPENAI_API_KEY='xxxxxxxxxx'
```
