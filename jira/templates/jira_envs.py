import airspeed
import json

def gen_user_story(project_key,request,description,env):
    request["project_key"] = project_key
    request["description"] = description

    loader = airspeed.CachingFileLoader("./")
    text_template = loader.load_template("jira/templates/" + env + "_user_story.json")
    request_body = text_template.merge(request, loader=loader)
    return request_body.replace("\n","")

def gen_user_story_subtask(project_key,request,description,parent_id,env):
    request["project_key"] = project_key
    request["description"] = description
    request["parent_id"] = parent_id

    loader = airspeed.CachingFileLoader("./")
    text_template = loader.load_template("jira/templates/" + env + "_user_story_subtask.json")
    request_body = text_template.merge(request, loader=loader)
    return request_body.replace("\n","")