import os
import json
import sys
import time
import requests
import pyautogui
import pyperclip
import re
import pyclip


class MyGithub:
    def __init__(self, token: str, my_info: dict, local_path: str, template_datas: dict = None, ) -> None:
        '''
        inputs :
            token = github authentication token

            my_info = { "name" : your github name}

            local_path = "local folder path where the cloning repository should store"

            template_data -> { "template_owner" : template owner name,
                                "template_name" : template name }
        '''
        self.token = token
        self.template_data = template_datas
        self.myInfo = my_info
        self.local_dir_path = local_path

        self.headers = {
            "Accept": "application/vnd.github+json",
            "Authorization": "token " + self.token
        }

    def create_repo(self) -> str:
        '''
        description:
            to create a repository without any templates
        '''
        pass

    def create_repo_using_template(self, repo_name, desc="") -> str:
        '''
        input:
            repo_name = repository name

            desc = repository description

        output:
             created -> return "repository url"

             not created -> return false
        '''

        # template details
        template_owner = self.template_data["template_owner"]
        template_repo = self.template_data["template_name"]

        url = f"https://api.github.com/repos/{template_owner}/{template_repo}/generate"

        data = {
            "owner": self.myInfo["name"],
            "name": repo_name,
            "description": desc,
            "include_all_branches": False,
            "private": False
        }

        data = json.dumps(data)  # convert dicts -> json

        # send post request
        res = requests.post(url=url, data=data, headers=self.headers)

        # 201 -> successfully created
        if res.status_code != 201:
            return False

        # parsing the repository clone link
        res = res.json()
        repo_link = res["html_url"]

        return repo_link

    def clone_repository(self, url: str) -> bool:
        '''
        inputs:
            url = "github repository url"

        output:
            true (created) / false (not created) 
        '''

        # change the dir to the specified location
        os.chdir(self.local_dir_path)
        os.system(f"git clone {url}")  # cloning repository

        # parsing the repository name from the url
        dir_name = url.split("/")[-1]
        dir_name = dir_name.replace(".git", "")

        # open the cloned repository (nautilus -> file manager)
        os.system(f"nautilus {dir_name} &")

        return True

    def clone_this_repository(self):
        '''
        description:
            first copy the github repository link and call this function.
            it will get the copied link from clipboard and clone the repository into the local path

        Input: None

        Output: `True if cloned` successfully `else False`
        '''

        time.sleep(0.2)
        repo_url = pyclip.paste().decode("utf-8")  # it past from clipboard
        print(repo_url)

        if re.search(pattern=".git", string=repo_url) != None:
            self.clone_repository(url=repo_url)
            return True

        return False


if __name__ == "__main__":
    # setting path to import config
    sys.path.append('../../')
    x = int(input("option : "))
    import config
    token = config.GITHUB_AUTH_TOKEN
    my_github_name = config.GITHUB_MY_NAME
    template_owner = config.GITHUB_TEMPLATE_OWNER_NAME
    template_name = config.GITHUB_TEMPLATE_REPO_NAME
    local_path = config.LOCAL_CLONING_PATH

    template_data = {"template_owner": template_owner,
                     "template_name": template_name}

    myInfo = {"name": my_github_name}

    mygithub = MyGithub(token=token, my_info=myInfo,
                        template_datas=template_data, local_path=local_path)

    if x == 1:  # create repo using template

        repo_name = "test case 5"
        desc = "nothing"
        res = mygithub.create_repo_using_template(
            repo_name=repo_name, desc=desc)
        print(res)

    if x == 2:  # copy local copy of repo
        mygithub.clone_repository(
            url="https://github.com/adilrahman/template-repo.git")

    if x == 3:
        time.sleep(5)
        mygithub.clone_this_repository()
