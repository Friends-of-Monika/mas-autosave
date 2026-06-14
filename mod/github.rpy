default persistent._fom_autosave_config_github = None

init -1000 python:
    if persistent._fom_autosave_config_github is None:
        persistent._fom_autosave_config_github = {
            "repo_name": "",
            "commit_fmt": "Automatic backup ([reason])"
        }

init -897 python in _fom_autosave_github:
    from store._fom_autosave_http import request, urlencode
    from store._fom_autosave_common import PersistentBackup
    from store._fom_autosave_persistent import get_persistent_path

    from store import persistent
    import store

    import base64
    import json
    import os

    def call_method(http_method, method_path, token=None, payload=None, query=None):
        github_api_url = "https://api.github.com{method_path}".format(method_path=method_path)
        if query is not None:
            github_api_url += "?" + urlencode(query)

        request_headers = {
            "User-Agent": "Monika After Story v{version}".format(version=renpy.config.version),
            "Accept": "application/json"
        }

        if payload is not None:
            request_headers["Content-Type"] = "application/vnd.github.v3+json"
            payload_json = json.dumps(payload)
        else:
            payload_json = None

        if token is not None:
            request_headers["Authorization"] = "Bearer {token}".format(token=token)

        status, body = request(http_method, github_api_url, request_headers, payload_json)
        return (status, json.loads(body))

    def commit_file(file_path, repo_path, repo_owner, repo_name, commit_message, token):
        github_api_url = "/repos/{owner}/{repo}/contents/{repo_path}".format(
            owner=repo_owner,
            repo=repo_name,
            repo_path=repo_path)

        try:
            status, file_meta = get_repo_file(repo_owner, repo_name, repo_path, token)
            if status != 200:
                raise ValueError("Unexpected status code {0} != 200".format(status))
            file_sha = file_meta["sha"]
        except Exception as e:
            file_sha = None

        with open(file_path, "rb") as f:
            file_data = base64.b64encode(f.read())

        body_params = {
            "content": file_data,
            "message": commit_message
        }

        if file_sha is not None:
            body_params["sha"] = file_sha

        return call_method("PUT", github_api_url, token, body_params)

    def get_repo_file(repo_owner, repo_name, repo_path, token, sha=None):
        github_api_url = "/repos/{owner}/{repo}/contents/{repo_path}".format(
            owner=repo_owner,
            repo=repo_name,
            repo_path=repo_path)

        query = {}
        if sha is not None:
            query["ref"] = sha

        return call_method("GET",
            github_api_url,
            token,
            query=query)

    def download_file(repo_owner, repo_name, repo_path, file_path, token, sha=None):
        status, file_meta = get_repo_file(repo_owner, repo_name, repo_path, token, sha)
        if status != 200:
            raise ValueError("Unexpected status code {0} != 200".format(status))
        with open(file_path, "wb") as f:
            f.write(base64.b64decode(file_meta["content"]))

    def list_commits(repo_owner, repo_name, repo_path, token):
        github_api_url = "/repos/{owner}/{repo}/commits".format(
            owner=repo_owner,
            repo=repo_name)
        return call_method("GET", github_api_url, token, query={
            "path": repo_path})

    def get_own_repos(token):
        return call_method("GET", "/user/repos", token)

    def get_self(token):
        return call_method("GET", "/user", token)


    class GithubBackup(PersistentBackup):
        def __init__(self, reason=None, commit_sha=None):
            super(GithubBackup, self).__init__()
            self.reason = reason
            self.commit = commit_sha

        def is_configured(self):
            token = store.mas_getAPIKey(store._fom_autosave_config.KEY_ID_GITHUB)
            commit_fmt = persistent._fom_autosave_config_github["commit_fmt"]
            repo_name=persistent._fom_autosave_config_github["repo_name"]
            return bool(token and commit_fmt and repo_name)

        def upload(self):
            token = store.mas_getAPIKey(store._fom_autosave_config.KEY_ID_GITHUB)
            commit_fmt = persistent._fom_autosave_config_github["commit_fmt"]
            commit_message = renpy.substitute(commit_fmt, {"reason": self.reason})

            per_path = get_persistent_path()
            renpy.save_persistent()

            status, commit = commit_file(
                file_path=per_path,
                repo_path="persistent",
                repo_owner=persistent._fom_autosave_config_github["repo_owner"],
                repo_name=persistent._fom_autosave_config_github["repo_name"],
                commit_message=commit_message,
                token=token
            )

        def download(self):
            token = store.mas_getAPIKey(store._fom_autosave_config.KEY_ID_GITHUB)
            repo_owner = persistent._fom_autosave_config_github["repo_owner"]
            repo_name = persistent._fom_autosave_config_github["repo_name"]
            repo_path = "persistent"

            per_path = get_persistent_path()
            download_file(repo_owner, repo_name, repo_path, per_path, token, self.commit)
