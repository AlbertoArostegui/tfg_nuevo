from pydantic.v1 import BaseModel
from langchain.tools import Tool
import urllib.parse
import requests
from requests.auth import HTTPBasicAuth
from dotenv import dotenv_values
from typing import List
from json_processing import jira_json_processing
import settings

jira_base_url = dotenv_values(".env")["url_instancia_jira"]
jira_email =  dotenv_values(".env")["jira_email"]
jira_token = dotenv_values(".env")["jira_token"]

def run_with_additional_query(query):
    endpoint = "/rest/api/3/search"
    settings.llm_query = query
    encoded_query = urllib.parse.quote(query)

    URI = jira_base_url + endpoint + "?jql=" + encoded_query
    response = requests.get(URI, auth=HTTPBasicAuth(jira_email, jira_token))

    json = response.json()
    json_post = jira_json_processing(json, jira_base_url)
    # Lo que se devuelve irá directamente a OpenAI, hay que tener cuidado porque se puede pasar del límite de tokens muy rapido o enviar más de los que realmente interesa enviar.
    return json_post

class RunQueryArgsSchema(BaseModel):
    query: str

run_with_additional_query_tool = Tool.from_function(
    name = "run_jira_query",
    description = "Run an query in JQL syntax\nAlways use the following issue status names in Spanish and never in English: 'Open' should be 'Abierto', 'In Progress' should be 'En Progreso', 'Resolved' should be 'Resuelto', 'Approved' should be 'Aprobada', 'Delivered' should be 'Entregado', 'Reopened' should be 'Reabierto', 'Closed' should be 'Cerrado.",
    func = run_with_additional_query,
    args_schema = RunQueryArgsSchema
)