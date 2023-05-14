import requests
from requests.structures import CaseInsensitiveDict
import os
from typing import Any, Dict
from jira.templates.jira_envs import gen_user_story, gen_user_story_subtask
headers = CaseInsensitiveDict()
headers["Accept"] = "application/json"
headers["Content-Type"] = "application/json"
import json

def get_all_jira_envs():
    endpt_sufix: str = "_JIRA_ENDPOINT"
    variables: Dict[str, str] = {}
    for key, value in os.environ.items():
        if key.endswith(endpt_sufix):
            variables[key.replace(endpt_sufix,"")] = value
    return variables

def create_user_story(project_key, description, request: Dict[Any, Any]):
    jira_env = request['jira_env']
    endpoint = os.getenv(jira_env + "_JIRA_ENDPOINT") + "/rest/api/latest/issue"
    try:
        answer = description
        request_body = gen_user_story(project_key,request,answer,jira_env)
        global headers
        headers["Authorization"] = "Bearer " + os.getenv(jira_env + "_JIRA_TOKEN")

        response = requests.post(endpoint, data=request_body, headers=headers).json()
        resp = {
            "description" : answer,
            "id" : response["id"],
            "jira_ticket" : response['key'],
            "jira_ticket_url": response['self']
        }
        return resp
    except Exception as e:
        error = e.__str__()
        print("Error : " + error)

def create_sub_task(project_key, description, request: Dict[Any, Any],parent_id,task_type):
    prompt = request['summary']
    jira_env = request['jira_env']

    endpoint = os.getenv(jira_env + "_JIRA_ENDPOINT") + "/rest/api/latest/issue"
    try:

        if task_type == "dev":
            answer = description
            request["summary"] = " Main Dev Task : " + request['summary']

        if task_type == "test":
           answer = description
           request["summary"] = "Main Test Task : " + request['summary']
        request_body = gen_user_story_subtask(project_key, request, answer,parent_id,jira_env)
        request["summary"] = prompt

        global headers
        headers["Authorization"] = "Bearer " + os.getenv(jira_env + "_JIRA_TOKEN")
        response = requests.post(endpoint, data=request_body, headers=headers).json()
        resp = {
            "description": answer,
            "id" : response["id"],
            "jira_ticket": response['key'],
            "jira_ticket_url": response['self']
        }
        return resp
    except Exception as e:
        error = e.__str__()
        print("Error : " + error)

def create_ustory_template(env_key, data):
    f = open("./jira/templates/" + env_key + "_user_story.json", "w")
    f.write(data)
    f.close()
    return {"success": True}

def create_ustory_task_template(env_key, data):
    f = open("./jira/templates/" + env_key + "_user_story_subtask.json", "w")
    f.write(data)
    f.close()
    return {"success": True}

def set_env_pat(jira_key, jira_pat, jira_endpoint):
    os.environ[jira_key + "_JIRA_TOKEN"] = jira_pat
    os.environ[jira_key + "_JIRA_ENDPOINT"] = jira_endpoint
    return {"success": True}
