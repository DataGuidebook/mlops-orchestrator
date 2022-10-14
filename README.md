# MLOps Orchestrator
Automate Model, Pipeline, and Endpoint Deployments with MLFlow, Databricks, and Azure ML

## Quickstart

1. Create a virtual environment called .venv in the root
  ```python
  python -m virtualenv .venv
  ```
1. Change `functions/local.settings.rename` to `functions/local.settings.json` and provide:
  * `AZDO_ACCESS_TOKEN`
  * `AZDO_PROJECT`
  * `AZDO_ORGANIZATION`
1. Use VS Code to [deploy the Python function app](https://learn.microsoft.com/en-us/azure/azure-functions/create-first-function-vs-code-python#publish-the-project-to-azure)
