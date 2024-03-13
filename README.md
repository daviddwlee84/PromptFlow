# Prompt Flow

Playing some Prompt Flow stuff

## Getting Started

### Streamlit

```bash
pip install -r requirements.txt
```

```bash
# Optional
cp example.env .env
# Fill-in your keys
# ...
```

```bash
streamlit run Overview.py
```

### Prompt Flow

```bash
pf flow init --flow ./flows/simple_chat --type chat
```

## Todo

- [ ] Create flow
- [X] Call Prompt Flow scoring API

## Resources

- [microsoft/promptflow: Build high-quality LLM apps - from prototyping, testing to production deployment and monitoring.](https://github.com/microsoft/promptflow)
- [What is Azure Machine Learning prompt flow - Azure Machine Learning | Microsoft Learn](https://learn.microsoft.com/en-us/azure/machine-learning/prompt-flow/overview-what-is-prompt-flow?view=azureml-api-2)
- [Prompt flow for VS Code - Visual Studio Marketplace](https://marketplace.visualstudio.com/items?itemName=prompt-flow.prompt-flow)
- [Prompt flow — Prompt flow documentation](https://microsoft.github.io/promptflow/)
    - [Quick Start — Prompt flow documentation](https://microsoft.github.io/promptflow/how-to-guides/quick-start.html)

## Trouble Shooting

### `promptflow 0.1.0b7.post1 requires openai<0.28.0,>=0.27.8, but you have openai 1.13.3 which is incompatible.` / `AttributeError: module 'openai' has no attribute 'BadRequestError'`

- [v1.0.0 Migration Guide · openai/openai-python · Discussion #742](https://github.com/openai/openai-python/discussions/742)
- Prompt flow supports OpenAI 1.x since v1.1.0. This may introduce breaking change.
- [Frequency asked questions (FAQ) — Prompt flow documentation](https://microsoft.github.io/promptflow/how-to-guides/faq.html#openai-1-x-support)
