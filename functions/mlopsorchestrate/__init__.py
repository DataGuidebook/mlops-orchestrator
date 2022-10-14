import logging
import os

import azure.functions as func

from .devops.azdo.azdoprovider import AzureDevOpsProvider

if ("AZDO_PROJECT" in os.environ) and ("AZDO_ORGANIZATION" in os.environ):
    logging.debug("Initializing with Azure Devops")
    DEVOPS_CLIENT = AzureDevOpsProvider(
        organization=os.environ.get("AZDO_ORGANIZATION"),
        project=os.environ.get("AZDO_PROJECT"),
        devops_token=os.environ.get("AZDO_ACCESS_TOKEN")
    )
else:
    raise RuntimeError(
        "Please configure the service to work with Azure" +
        " DevOps by including AZDO_PROJECT and AZDO_ORGANIZATION in your" +
        " environment variables"
    )

PIPELINE_PATTERN = "{modelname}-deploy"


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    

    req_body = req.get_json()
    logging.info(req_body)
    # Get Pipeline Id based on model name
    mlflow_event = req_body.get("event")
    mlflow_model_name = req_body.get("model_name")
    mlflow_model_version = req_body.get("version")
    logging.info(f"{mlflow_model_name}:{mlflow_model_version} {mlflow_event}")

    # Sample event:
    # {'event': 'MODEL_VERSION_CREATED', 'event_timestamp': 1648995765580, 
    # 'text': "A test webhook trigger", 'version': '123',
    # 'model_name': 'mymodel', 'source_run_id': 'run12345', 
    # 'webhook_id': 'b1b1147f04824b49a101661ea40eaacd'}
    azdo_variables = {"MODEL_VERSION":{"value":mlflow_model_version, "isSecret":False}}
    logging.info("Attempting to get pipelineid")
    pipeline_id = DEVOPS_CLIENT.get_pipeline_id(pipeline_name=PIPELINE_PATTERN.format(modelname=mlflow_model_name))
    logging.info(f"Pipeline received: {pipeline_id}")
    logging.info("Attempting to execute pipeline")
    response = DEVOPS_CLIENT.run_pipeline(pipeline_id=pipeline_id, azdo_variables=azdo_variables)

    logging.info(response)

    return func.HttpResponse(
        "Received Web Hook",
        status_code=200
    )
