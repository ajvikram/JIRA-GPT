#!/usr/bin/env python

import streamlit as st
from requests.structures import CaseInsensitiveDict
import json
from pathlib import Path
from PIL import Image
import base64
from jira_git import gen_git_code
from jira.jira_client import get_all_jira_envs, create_user_story, create_sub_task, create_ustory_template, create_ustory_task_template, set_env_pat
st.set_page_config(layout='wide')
from streamlit_option_menu import option_menu
from gpt import gen_response, simple_gen_response
import datetime;

headers = CaseInsensitiveDict()
headers["Accept"] = "application/json"
headers["Content-Type"] = "application/json"


def show_messages(text):
    messages_str = [
        f"{_['role']}: {_['content']}" for _ in st.session_state["messages"][1:]
    ]
    text.text_area("Messages", value=str("\n".join(messages_str)), height=400)


def img_to_bytes(img_path):
    img_bytes = Path(img_path).read_bytes()
    encoded_img = base64.b64encode(img_bytes).decode()
    return encoded_img


with st.sidebar:
    choose = option_menu("Jira GPT", ["Generate User Story", "Jira Env Setup", "GPT Play Ground","About","Contact"],
                         icons=['list-task', 'gear','kanban', 'book', 'person lines fill'],
                         menu_icon="cast", default_index=0,
                         styles={
                             "container": {"padding": "5!important", "background-color": "#262730"},
                             "icon": {"color": "#02ab21", "font-size": "25px"},
                             "nav-link": {"font-size": "16px", "text-align": "left", "margin": "0px",
                                          "--hover-color": "#56755c"},
                             "nav-link-selected": {"background-color": "#2f5335"},
                         }
                         )

logo = Image.open(r'./images/jira-gpt.png')
if choose == "About":
    col1, col2 = st.columns([0.8, 0.2])
    with col1:  # To display the header text using css style
        st.markdown(""" <style> .font {
            font-size:30px ; font-family: 'Cooper Black'; color: #02ab21;} 
            </style> """, unsafe_allow_html=True)
        st.markdown('<p class="font">About the Jira GPT </p>', unsafe_allow_html=True)

    with col2:  # To display brand logo

        st.image(logo, width=150)
    st.write("This application uses GPT4ALL-J to generate user stories for projects in JIRA, This will not just generate user story but also generate Main Dev Task with code and Main Test Task with test steps")
    st.write(
        "Test Cases GPT model is also the GPT4ALL-J Model")
    st.write(
        "Dev(Code Gen) Model can be Salesforce CodeGen GPT Model")


elif choose == "Jira Env Setup":
    col1, col2 = st.columns([0.8, 0.2])
    with col1:  # To display the header text using css style
        st.markdown(""" <style> .font {
                font-size:30px ; font-family: 'Cooper Black'; color: #02ab21;} 
                </style> """, unsafe_allow_html=True)
        st.markdown('<p class="font">Setup Jira Environment </p>', unsafe_allow_html=True)

        st.markdown(""" <style> .table {
                        font-size:20px ; font-family: 'Cooper Black'; color: #02ab21; width: 100%; table-layout: fixed}
                        </style> """, unsafe_allow_html=True)

        st.markdown('<table class=table><th>Jira Env</th><th>Jira Endpoint</th></table>', unsafe_allow_html=True)
        envs = get_all_jira_envs()
        st.markdown(""" <style> .table1 {
                                    font-size:15px ; border-collapse: collapse; color: white; width: 100%; table-layout: fixed}
                                    </style> """, unsafe_allow_html=True)
        for key, value in envs.items():
            st.markdown('<table class=table1><tr><td>' + key + '</td><td>' + value + '</td></tr></table>', unsafe_allow_html=True)

    with col2:  # To display brand logo
        st.image(logo, width=150)

    st.markdown('<p></p><p >Jira Env :</p>', unsafe_allow_html=True)
    with st.form(key='columns_in_form2',
                 clear_on_submit=True):
        jira_key = st.text_input(label='Please Enter Jira Env Identifier :')
        jira_endpoint = st.text_input(label='Please Enter Jira Endpoint :')
        jira_pat = st.text_input(label='Please Enter Jira PAT :')
        submitted = st.form_submit_button('Submit')
        if submitted:
            msg = set_env_pat(jira_key, jira_pat, jira_endpoint)
            st.success(msg, icon="✅")

    st.markdown('<p >Jira Env Templates :</p>', unsafe_allow_html=True)
    with st.form(key='columns_in_form3',
                 clear_on_submit=True):
        jira_key = st.text_input(label='Please Enter Jira Env Identifier :')
        user_story_template = st.text_area(label='Please Enter Jira User Story Template :')
        user_story_subtask_template = st.text_area(label='Please Enter Jira User Story Sub Task Template :')
        submitted = st.form_submit_button('Submit')
        if submitted:
            msg = create_ustory_template(jira_key, user_story_template)
            msg1 = create_ustory_task_template(jira_key, user_story_subtask_template)
            st.success(msg, icon="✅")


elif choose == "Generate User Story":
    col1, col2 = st.columns([0.8, 0.2])
    with col1:  # To display the header text using css style
        st.markdown(""" <style> .font {
                    font-size:30px ; font-family: 'Cooper Black'; color: #02ab21;} 
                    </style> """, unsafe_allow_html=True)
        st.markdown('<p class="font">Generate User Story </p>', unsafe_allow_html=True)

    with col2:  # To display brand logo
        st.image(logo, width=150)

    if "messages" not in st.session_state:
        st.session_state["us_story"] = '0000'

    envs = get_all_jira_envs()
    with st.form(key='columns_in_form300',
                 clear_on_submit=False):
        col1, col2 = st.columns([0.5, 0.5])
        with col1:
            summary = st.text_input(label='Please Enter Summary to generate Jira User Story :')
            jira_project_key = st.text_input(label='Please Enter Jira Project Key :')
        with col2:
            jira_env = st.selectbox('Select Jira Env :', envs.keys())
            code_lan = st.selectbox('Select Code Language :', ['Java','C','C++','Python'])
        jira_params = st.text_area('Enter Jira Params as Json :')
        submitted = st.form_submit_button('Submit')

        if submitted:
            with st.spinner("Generating User Story..."):
                description = gen_response('Generate User Story for ' + summary)
                if jira_env is None or jira_env == '' :
                    st.success("Generated Successfully ", icon="✅")
                    st.text_area('User Story Description', value=description)
                else :
                    jira_params_dict = json.loads(jira_params)
                    story = {
                            "summary": summary,
                            "issue_type": "Story",
                            "assignee": jira_params_dict["assignee"],
                            "jira_env": jira_env,
                            "code_lan": code_lan
                    }
                    description = description.replace('\\', '\\\\').replace('"', "'").replace('\t','').replace('\n',"\\n")
                    res = create_user_story(jira_project_key, description, story)
                    us_id = res['id']
                    st.success(res['jira_ticket'] + ": " + res['jira_ticket_url'], icon="✅")
                    st.text_area('User Story Description', value=res['description'])

                col11, col12 = st.columns([0.5, 0.5])
                with col11:
                    with st.spinner("Generating User Story Dev Task..."):
                        dev_description = gen_response('Write ' + code_lan + ' code for ' + summary)
                        ts = datetime.datetime.now().timestamp()
                        jira_ticket = 'GenCode_' + str(ts)
                        if jira_env is None or jira_env == '':
                            st.success("Generated Successfully ", icon="✅")
                            st.text_area('User Story Dev Task Description', value=dev_description)
                        else :
                            dev_description1 = dev_description.replace('\\', '\\\\').replace('"', "'").replace('\t','').replace('\n',"\\n")
                            res = create_sub_task(jira_project_key, dev_description1, story,us_id,'dev')
                            st.success(res['jira_ticket'] + ": " + res['jira_ticket_url'], icon="✅")
                            st.text_area('User Story Dev Task Description', value=res['description'])
                            jira_ticket = res['jira_ticket']

                        gen_git_code(code_lan, dev_description, jira_ticket)
                with col12 :
                    with st.spinner("Generating User Story Test Task..."):
                        test_description = gen_response('Generate Testing Steps for ' + summary)
                        if jira_env is None or jira_env == '':
                            st.success("Generated Successfully ", icon="✅")
                            st.text_area('User Story Test Task Description', value=test_description)
                        else:
                            test_description = test_description.replace('\\', '\\\\').replace('"', "'").replace('\t','').replace('\n',"\\n")
                            res = create_sub_task(jira_project_key, test_description, story, us_id, 'test')
                            st.success(res['jira_ticket'] + ": " + res['jira_ticket_url'], icon="✅")
                            st.text_area('User Story Test Task Description', value=res['description'])

elif choose == "GPT Play Ground":
    col1, col2 = st.columns([0.8, 0.2])
    with col1:  # To display the header text using css style
        st.markdown(""" <style> .font {
                    font-size:30px ; font-family: 'Cooper Black'; color: #02ab21;} 
                    </style> """, unsafe_allow_html=True)
        st.markdown('<p class="font">Try GPT Chat </p>', unsafe_allow_html=True)

    with col2:
        st.image(logo, width=150)

    BASE_PROMPT = [{"role": "AI", "content": "You are a helpful assistant."}]

    if "messages" not in st.session_state:
        st.session_state["messages"] = BASE_PROMPT

    st.markdown(""" <style> .font {
                        font-size:30px ; font-family: 'Cooper Black'; color: #02ab21;} 
                        </style> """, unsafe_allow_html=True)
    st.markdown('<p class="font">GPT4 Play Ground :</p>', unsafe_allow_html=True)

    text = st.empty()
    show_messages(text)

    prompt = st.text_input("Prompt:", value="Enter your message here...")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Send"):
            with st.spinner("Generating response..."):
                st.session_state["messages"] += [{"role": "You", "content": prompt}]
                message_response = simple_gen_response(st.session_state["messages"][-1]["content"])
                st.session_state["messages"] += [
                    {"role": "AI", "content": message_response}
                ]
                show_messages(text)
    with col2:
        if st.button("Clear"):
            st.session_state["messages"] = BASE_PROMPT
            show_messages(text)


elif choose == "Contact":
    col1, col2 = st.columns([0.8, 0.2])
    with col1:
        st.markdown(""" <style> .font {
                font-size:30px ; font-family: 'Cooper Black'; color: #02ab21;} 
                </style> """, unsafe_allow_html=True)
        st.markdown('<p class="font">Contact </p>', unsafe_allow_html=True)

    with col2:  # To display brand logo
        st.image(logo, width=150)
    st.write("Ajay S")

