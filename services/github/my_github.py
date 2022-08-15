import os
import json
from re import template
import sys
import requests

class MyGithub:
    def __init__(self, token  : str,my_info : dict, template_datas : dict = None) -> None:
        '''
        inputs :
            token -> github authentication token
            
            my_info -> { "name" : your github name}

            template_data -> { "template_owner" : template owner name,
                                "template_name" : template name }
        '''
        self.token = token
        self.template_data = template_datas
        self.myInfo = my_info


        self.headers = {
            "Accept" : "application/vnd.github+json",
            "Authorization" : "token " + self.token
        }

    def create_repo(self) -> str:
        pass

    def create_repo_using_template(self, repo_name, desc = "") -> str:
        '''
        input:
            repo_name -> repository name

            desc -> repository description
        
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

   


if __name__ == "__main__":
     # setting path to import config
    sys.path.append('../../')
    import config

    token          = config.GITHUB_AUTH_TOKEN
    my_github_name = config.GITHUB_MY_NAME
    template_owner = config.GITHUB_TEMPLATE_OWNER_NAME
    template_name  = config.GITHUB_TEMPLATE_REPO_NAME

    template_data = { "template_owner" : template_owner,
                      "template_name" : template_name }

    myInfo = { "name" : my_github_name }
    
    
    mygithub = MyGithub(token=token,my_info=myInfo,template_datas=template_data)

    repo_name = "test case 5"
    desc = "nothing"
    res = mygithub.create_repo_using_template(repo_name=repo_name, desc=desc)
    print(res)
    