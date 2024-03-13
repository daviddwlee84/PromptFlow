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

Chat Example

```bash
pf flow init --flow ./flows/simple_chat --type chat
```

```powershell
# Azure OpenAI
# https://stackoverflow.com/questions/72236557/how-do-i-read-a-env-file-from-a-ps1-script
# https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_environment_variables?view=powershell-7.4
# https://stackoverflow.com/questions/7760013/why-does-continue-behave-like-break-in-a-foreach-object
# Load .env and set environment variable in Powershell
Get-Content .env | foreach {
    $name, $value = $_.split('=')
    if ([string]::IsNullOrWhiteSpace($name) -or $name.Contains('#')) {
        return
    }
    Set-Content env:\$name $value
}

pf connection create --file ./flows/simple_chat/azure_openai.yaml --set api_key=$env:AZURE_OPENAI_KEY api_base=$env:AZURE_OPENAI_ENDPOINT/openai/deployments/$env:AZURE_OPENAI_DEPLOYMENT_NAME/chat/completions?api-version=$env:AZURE_OPENAI_VERSION --set api_version=$env:AZURE_OPENAI_VERSION --name open_ai_connection
```

```powershell
pf flow test --flow ./flows/simple_chat --interactive
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

### pf.flow.test failed with UserErrorException: Exception: OpenAI API hits NotFoundError: Error code: 404 - {'error': {'code': 'DeploymentNotFound', 'message': 'The API deployment for this resource does not exist. If you created the deployment within the last 5 minutes, please wait a moment and try again.'}} [Error reference: https://platform.openai.com/docs/guides/error-codes/api-errors]

Basically your connection config are not set correctly

Seems the `azure_openai.yaml` is just a template, you don't need to change the file.
