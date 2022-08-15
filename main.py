from math import remainder
from click import command
from speech_recognition_engine import SpeechTextEngine
import config
from services.notion import NotionClient
from datetime import datetime
import time
from services.github import MyGithub

notion_integration_token = config.NOTION_INTEGRATION_TOKEN
notion_database_id = config.NOTION_DATABASE_ID

sr = SpeechTextEngine()
notionClient = NotionClient(token=notion_integration_token,
                            database_id=notion_database_id)

github_token = config.GITHUB_AUTH_TOKEN
github_template_owner_name = config.GITHUB_TEMPLATE_OWNER_NAME
github_template_repo_name = config.GITHUB_TEMPLATE_REPO_NAME
github_my_name = config.GITHUB_MY_NAME
local_path     = config.LOCAL_CLONING_PATH

my_info = { "name" : github_my_name}

template_data = { "template_owner" : github_template_owner_name,
                        "template_name" : github_template_repo_name }

myGithub = MyGithub(token=github_token, my_info=my_info, template_datas=template_data,local_path=local_path) 

non_active = 0

def recheck(type,value):
     while True:
        sr.speak(f'your {type} is ' + value)
        sr.speak(" is that right?")
        command = sr.speech_recognition()
        command = nullcheck(command)
        if command == "yes":
            return value
        sr.speak("ok tell me once more sir!")
        value = sr.speech_recognition()
        value = nullcheck(value)

def nullcheck(value):
    while value == "":
        sr.speak("i didn't get it sir, please tell me once more")
        value = sr.speech_recognition()
    sr.speak("ok")
    return value  



def check_activity(command):
    global non_active
    print(f"inside {non_active}")
    if non_active > 5:
        sr.speak("i didn't get any query for a long sir?")
        non_active = 0
    if command == "":
        while command == "":
            command = sr.speech_recognition()
            non_active += 1
            if non_active > 5:
                sr.speak("i didn't get any query for a long sir?")
                non_active = 0
    return command
    

if __name__ == "__main__":

    while True:
        if sr.wakeup():
            sr.speak("listening sir....")
            time.sleep(0.5)
            while True:
                command = sr.speech_recognition()
                command = check_activity(command)
                print(non_active)
                if "deactivate" in command: # for deactivate service temporarly
                    non_active = 0
                    print("Deactivate!")
                    sr.speak("Deactivating")
                    break

                if "note" in command or "todo" in command: # for createing notes
                    non_active = 0
                    
                    # for getting project or repository name
                    sr.speak("for which project sir ?")
                    project_name = sr.speech_recognition()
                    project_name = nullcheck(value=project_name)
                    project_name = recheck(type="project name",value=project_name)

                     # for getting task or todo or note 
                    sr.speak("tell me the note sir?")                        
                    note = sr.speech_recognition()
                    note = nullcheck(value=note)
                    note = recheck(type="note",value=note)
                    

                    sr.speak(" should i store?")
                    command = sr.speech_recognition()
                    command = nullcheck(command)
                    if "no" in command:
                        sr.speak("Ok sir")
                        continue
                
                    time_now = datetime.now().astimezone().isoformat()
                    status = "Active"
                    res = notionClient.create_page(project_name=project_name,task=note,status=status,date=time_now)
                    
                    if res.status_code == 200:
                        print("created successfully....!!!")
                        sr.speak("new note created")
                    else:
                        print(f"error :-> status code = {res.status_code}")
                        sr.speak("can't store the note")


                if "create" in command and ( "repo" in command or "repository"):
                    non_active = 0
                    sr.speak("you want to create new repository in github?")
                    if "yes" in sr.speech_recognition():
                        sr.speak("ok sir, creating new repository")
                        sr.speak("what is the repository name?")
                        
                        repo_name = sr.speech_recognition()
                        repo_name = nullcheck(value=repo_name)
                        repo_name = recheck(type="repository name",value=repo_name)
                    

                        sr.speak("do you want to add any descriptions?")
                        if "yes" in sr.speech_recognition():
                            sr.speak("ok then what should be the descriptions?")
                            
                            desc = sr.speech_recognition()
                            desc = nullcheck(value=desc)
                            desc = recheck(type="description",value=desc)
                        
                        else:
                            sr.speak("ok")
                            desc = ""

                        sr.speak("should i create now?")
                        if "yes" in sr.speech_recognition():
                            repo_url = myGithub.create_repo_using_template(repo_name=repo_name,desc=desc)
                            
                            if repo_url == False:
                                print("failed")
                                sr.speak("can't create the repository due to some errors,  please check the configaration file")
                                break

                            print("created")
                            sr.speak("new repository created")
                            sr.speak("Do you want to create a local copy of this repository ?")
                            if "yes" in sr.speech_recognition():
                                sr.speak("cloning the repository...")
                                myGithub.clone_repository(repo_url)
                    else:
                        sr.speak("ok sir")

                        
                        


                if "exit" in command: # for exiting program
                    sr.speak("program terminating")
                    exit()

                non_active += 1
