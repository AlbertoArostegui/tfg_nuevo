import requests
from requests.auth import HTTPBasicAuth
from dotenv import dotenv_values
import urllib
import json

def get_keys_for_query(query_ground_truth):
    jira_email =  dotenv_values(".env")["jira_email"]
    jira_token = dotenv_values(".env")["jira_token"]
    jira_base_url = dotenv_values(".env")["url_instancia_jira"]

    endpoint = "/rest/api/3/search"
    encoded_query = urllib.parse.quote(query_ground_truth)

    URI = jira_base_url + endpoint + "?jql=" + encoded_query
    response = requests.get(URI, auth=HTTPBasicAuth(jira_email, jira_token))

    json_response = response.json()
    try:
        incidencias_obtenidas = [issue['key'] for issue in json_response['issues']]
    except:
        print("Error en la petición a Jira con: " + query_ground_truth + "\n" + str(json_response))
        incidencias_obtenidas = []

    return incidencias_obtenidas

get_keys_for_query('project in (projectMatch("projectStartDate > 2025-02-28"))')