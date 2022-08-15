import os
import json
from re import template
import sys
import requests

class MyGithub:
    def __init__(self, token  : str,my_info : dict, local_path : str ,template_datas : dict = None, ) -> None:
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
            "Accept" : "application/vnd.github+json",
            "Authorization" : "token " + self.token
        }

    def create_repo(self) -> str:
        pass

    def create_repo_using_template(self, repo_name, desc = "") -> str:
        '''
        input:
            repo_name = repository name

            desc = repository description
        
        output:
             true (created) / false (not created) 
        '''
        
        # template details
        template_owner = self.template_data["template_owner"]
        template_repo = self.template_data["template_name"]

        url = f"https://api.github.com/repos/{template_owner}/{template_repo}/generate"
        
        data = {
            "owner": self.myInfo["name"],
            "name": repo_name,
            "description": desc,
            "include_all_branches" : False,
            "private": False
        }

        data = json.dumps(data) # convert dicts -> json

        res = requests.post(url=url, data=data, headers=self.headers) #send post request

        # 201 -> successfully created 
        if res.status_code != 201:
            return False

        # parsing to create local copy of the created repo
        res = res.json()
        print(res["html_url"])
        
        return True


    def clone_repository(self, url : str) -> bool:
        '''
        inputs:
            url = "github repository url"

           
        
        output:
            true (created) / false (not created) 
        '''

        os.chdir(self.local_dir_path) # change the dir to the specified location
        os.system(f"git clone {url}") # cloning repository 

        # parsing the repository name from the url
        dir_name = url.split("/")[-1]
        dir_name = dir_name.replace(".git","")
        
        # open the cloned repository (nautilus -> file manager)
        os.system(f"nautilus {dir_name} &")

        return True



   


if __name__ == "__main__":
     # setting path to import config
    sys.path.append('../../')
    x = int(input("option : "))
    import config
    token          = config.GITHUB_AUTH_TOKEN
    my_github_name = config.GITHUB_MY_NAME
    template_owner = config.GITHUB_TEMPLATE_OWNER_NAME
    template_name  = config.GITHUB_TEMPLATE_REPO_NAME
    local_path     = config.LOCAL_CLONING_PATH

    template_data = { "template_owner" : template_owner,
                        "template_name" : template_name }

    myInfo = { "name" : my_github_name }
        
        
    mygithub = MyGithub(token=token,my_info=myInfo,template_datas=template_data,local_path=local_path)


    if x == 1: # create repo using template
       
        repo_name = "test case 5"
        desc = "nothing"
        res = mygithub.create_repo_using_template(repo_name=repo_name, desc=desc)
        print(res)

    if x == 2: # copy local copy of repo
        mygithub.clone_repository(url = "https://github.com/adilrahman/template-repo.git")

        