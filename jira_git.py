import git
import os

git_dir_name = os.getenv('git_dir_name')
git_remote_url = os.getenv('git_remote_url')

project_dir = os.path.dirname(os.path.abspath(__file__))
os.environ['GIT_ASKPASS'] = os.path.join(project_dir, 'askpass.py')

if not os.path.isdir('./git_repo/' + git_dir_name):
    git.Git('./git_repo/').clone(git_remote_url)

repo = git.Repo('./git_repo/' + git_dir_name)

def gen_git_code(user_code_input, dev_description, jira_ticket):
    ft = ".py"
    if "java" in user_code_input.lower():
        ft = ".java"

    new_branch = 'feature/' + jira_ticket
    current = repo.create_head(new_branch,'main')
    current.checkout()

    f = open("./git_repo/"+ git_dir_name + "/code" + ft, "a")
    f.write(dev_description)
    f.close()

    repo.index.add([os.path.dirname(os.path.abspath(__file__))+ "/git_repo/"+ git_dir_name + "/code" + ft])

    repo.index.commit('[' + jira_ticket + '] Auto Code change')
    repo.git.push('--set-upstream', repo.remote().name, new_branch)
