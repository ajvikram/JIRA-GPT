export git_dir_name=<GIT_PROJECT_NAME>
export GIT_USERNAME=<GIT_USERNAME>
export GIT_PASSWORD=<GIT_PAT>
export git_remote_url=https://${GIT_USERNAME}:${GIT_PASSWORD}@github.com/<Your_GIT_Name>/${git_dir_name}.git

streamlit run main.py --server.port=8090 --server.address=0.0.0.0

