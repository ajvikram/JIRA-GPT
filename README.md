# JIRA-GPT
###JIRA Automation Using GPT

#####Generate Jira User stories and test cases based on Summary one-liner - Based on Open Source GPT4ALL-J(can be use for commercial purpose), no OpenAI API needed.

#####Generate Code snippets in programing languages such as – Java, Python, C/C++, Java Script etc.
#### This is just a integration trial to see if GPT can help
* Head start for any iteration cycle
* Save DevOps team member times
* Provide valuable information for requirement, design, coding and testing
 

![Alt text](./images/JIRA_GPT.png?raw=true "JIRA GPT")

Local use : -
Download GPT4ALL-J model in model directory(from here - https://gpt4all.io/models/ggml-gpt4all-j-v1.3-groovy.bin
)

Can be integrate with any JIRA instance with PAT token.
```export git_dir_name=<GIT_PROJECT_NAME>
export GIT_USERNAME=<GIT_USERNAME>
export GIT_PASSWORD=<GIT_PAT>
export git_remote_url=https://${GIT_USERNAME}:${GIT_PASSWORD}@github.com/<Your_GIT_NAME>/${git_dir_name}.git

streamlit run main.py --server.port=8090 --server.address=0.0.0.0
```