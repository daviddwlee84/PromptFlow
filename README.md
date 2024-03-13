# Prompt Flow

Playing some Prompt Flow stuff

## Getting Started

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

## Todo

- [ ] Create flow
- [ ] Call Prompt Flow scoring API

## Resources

- [microsoft/promptflow: Build high-quality LLM apps - from prototyping, testing to production deployment and monitoring.](https://github.com/microsoft/promptflow)

## Trouble Shooting

### `promptflow 0.1.0b7.post1 requires openai<0.28.0,>=0.27.8, but you have openai 1.13.3 which is incompatible.` / `AttributeError: module 'openai' has no attribute 'BadRequestError'`

- [v1.0.0 Migration Guide · openai/openai-python · Discussion #742](https://github.com/openai/openai-python/discussions/742)
