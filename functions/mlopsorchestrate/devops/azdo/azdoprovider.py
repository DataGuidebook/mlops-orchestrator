import logging

from ..provider import AbstractProvider, PipelineNotFound

import requests

class AzureDevOpsProvider(AbstractProvider):

    def __init__(self, organization:str , project:str, devops_token:str) -> None:
        super().__init__()
        self.organization = organization
        self.project = project
        self._devops_token = devops_token
        self._username = "accesstoken"
        self._root_endpoint = f"https://dev.azure.com/{self.organization}/{self.project}"


    def get_pipeline_id(self, pipeline_name=None, api_version="6.0-preview.1", **kwargs) -> str:
        """
        Get an Azure DevOps Pipeline Id.
        """
        url = f"{self._root_endpoint}/_apis/pipelines?api-version={api_version}"
        logging.info(url)
        

        results = requests.get(url, auth=(self._username, self._devops_token))
        logging.info(results.status_code)

        if results.status_code == 200:
            data = results.json()
            
            if data["count"] == 0:
                raise PipelineNotFound("There are no release definitions found.")
            else:
                candidate_releases = [r["id"] for r in data["value"] if r["name"] == pipeline_name]
                if len(candidate_releases) > 0:
                    return candidate_releases[0]
                else:
                    raise PipelineNotFound("There was no release definition found with the name '{}'".format(pipeline_name))
        else:
            raise Exception(results.content)

    def run_pipeline(self, pipeline_name=None, pipeline_id=None, api_version="6.0-preview.1", azdo_variables=None, **kwargs):
        """
        Execute an Azure DevOps pipeline based on its name or id. If calling by
        name, it will also execute `get_pipeline_id`.
        """
        if not pipeline_id:
            pipeline_id = self.get_pipeline_id(pipeline_name=pipeline_name, api_version=api_version)
        
        url = f"{self._root_endpoint}/_apis/pipelines/{pipeline_id}/runs?api-version={api_version}"

        data = {"variables":{}}
        if azdo_variables:
            # Must be in the form
            # "variables":{"my_variable_name":{"value":"anewvalue", "isSecret":bool}}
            data.update({"variables":azdo_variables})

        header = {"Content-Type":"application/json"}

        results = requests.post(url, auth=(self._username, self._devops_token), json=data, headers=header)

        output = dict()
        if results.status_code == 200:
            results_json = results.json()
            output["new_pipeline_id"] = results_json.get("id", "NotAssigned")
            output["new_pipeline_name"] = results_json.get("name", "NotAssigned")
            output["new_pipeline_url"] = results_json.get("url", "NotAssigned")
        else:
            raise Exception(results.json()["message"])
        
        return output