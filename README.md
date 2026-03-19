# ms-foundry-hosted-agent

This repository shows a minimal Microsoft Foundry hosted agent setup:

- `agent/` contains the source agent manifest and Python code which will be run on Hosted Agent. You can also run locally.

The repository is intentionally small, but there is one important detail: after you run `azd ai agent init`, the deployable agent code lives under `my-hosted-agent/`.

## Repository layout

```text
.
|- agent/
|  |- agent.yaml
|  |- main.py
|  |- requirements.txt
|- test/
|  \- test-response.ps1
\- .env.example
```

## Prerequisites

- Python 3.12
- PowerShell on Windows
- Azure CLI
- Azure Developer CLI (`azd`)
- The `azure.ai.agents` `azd` extension
- An Azure subscription with access to Microsoft Foundry and the model you want to deploy

Recommended versions:

```powershell
az version
azd version
```

If `azd` is outdated, update it before provisioning:

```powershell
winget upgrade Microsoft.Azd
```

Install the required tooling if needed:

```powershell
winget install Microsoft.Azd
winget install Microsoft.AzureCLI
azd extension add azure.ai.agents
```

## 1. Create the local Python environment

From the repository root:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r .\agent\requirements.txt
```

This installs the local dependencies required by `agent/main.py`.

## 2. Create the local `.env` file

The real `.env` file is ignored by git. Start from the sample file:

```powershell
Copy-Item .\.env.example .\.env
```

Then replace the placeholder values in `.env`.

Expected variables:

- `AZURE_OPENAI_ENDPOINT`: Azure OpenAI endpoint from your Foundry resource
- `AZURE_OPENAI_CHAT_DEPLOYMENT_NAME`: model deployment name, for example `gpt-5.1`
- `AZURE_AI_PROJECT_ENDPOINT`: Azure AI Foundry project endpoint

Copy the relevant values into the root `.env` file.

## 3. Authenticate for local development

The local Python app uses `DefaultAzureCredential`, so Azure CLI sign-in is the simplest option:

```powershell
az login
```

If you use multiple subscriptions, set the one you want before running the agent:

```powershell
az account set --subscription "<your-subscription-name-or-id>"
```

## 4. Run the agent locally

Start the local server from the repository root:

```powershell
python .\agent\main.py
```

The agent listens on `http://localhost:8088`.

In another PowerShell terminal, send a test prompt:

```powershell
.\test\test-response.ps1
```

You can also pass a custom prompt:

```powershell
.\test\test-response.ps1 -Prompt "How do I deploy a Microsoft Foundry hosted agent?"
```

## 5. Recreate the `azd` project from scratch

You need to run the following commands from the repository root.

```powershell
mkdir my-hosted-agent
cd .\my-hosted-agent
azd init -t https://github.com/Azure-Samples/azd-ai-starter-basic
azd ai agent init -m ..\agent\agent.yaml
```

During `azd ai agent init`, you will be prompted for:

- Azure subscription
- Azure location
- model SKU
- model deployment name
- container CPU and memory
- minimum and maximum replica count

Typical values for this sample:

- Environment name: any unique name such as `myagent-dev`
- Region: a Foundry-supported region such as `eastus2`
- Model deployment name: `gpt-5.1`
- Memory: `2Gi`
- CPU: `1`
- Min replicas: `1`
- Max replicas: `3`

After initialization, the generated deployable source is placed under:

```text
my-hosted-agent/src/agent
```

## 6. Provision and deploy to Azure

From `my-hosted-agent/`:

```powershell
azd up
```

This command packages the agent, provisions Azure resources, and deploys the hosted agent.

For this sample, `azd up` creates or configures the following core resources:

- Resource group
- Log Analytics workspace
- Application Insights
- Microsoft Foundry account
- Microsoft Foundry project
- Azure OpenAI model deployment
- Azure Container Registry
- Foundry hosted agent capability host

At the end of a successful deployment, `azd` prints:

- the agent playground URL in the Azure AI Foundry portal
- the hosted agent endpoint URL

## 7. Clean up Azure resources

When you are done, remove the deployed resources to avoid unnecessary cost:

```powershell
cd .\my-hosted-agent
azd down
```

## Notes

- `.env` is for local development only and should not contain production secrets.
- `agent/agent.yaml` is the manifest used as input to `azd ai agent init`.
- `my-hosted-agent/azure.yaml` is the generated `azd` project definition used for deployment.
- `test/test-response.ps1` targets the local server, not the Azure hosted endpoint.