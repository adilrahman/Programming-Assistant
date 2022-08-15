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

my_info = { "name" : github_my_name}

template_data = { "template_owner" : github_template_owner_name,
                        "template_name" : github_template_repo_name }

myGithub = MyGithub(token=github_token, my_info=my_info, template_datas=template_data) 

if __name__ == "__main__":

    remainder = 5
    count = 0
    while True:
        count = 0
        if sr.wakeup():
            sr.speak("listening sir....")
            time.sleep(0.5)
            while True:
                if count == remainder:
                    sr.speak("you didn't said anything for a while sir")
                    time.sleep(0.5)

                command = sr.speech_recognition()
                if "deactivate" in command: # for deactivate service temporarly
                    print("Deactivate!")
                    sr.speak("Deactivating")
                    break

                if "note" in command or "todo" in command: # for createing notes
                    sr.speak("Tell me sir")
                    note = sr.speech_recognition()

                    if note == "":
                        sr.speak("you didn't said anything")
                        continue
                    else:
                        sr.speak('your todo is ' + note)
                        sr.speak(" should i store?")

                        command = sr.speech_recognition()
                        if "no" in command:
                            sr.speak("Ok sir")
                            continue

                    time_now = datetime.now().astimezone().isoformat()
                    status = "Active"

                    ## test project attributes
                    time_now = datetime.now().astimezone().isoformat()
                    status = "Active"
                    project_name = "Test1"
                    task = "nothing"

                    res = notionClient.create_page(project_name=project_name,task=task,status=status,date=time_now)
                    if res.status_code == 200:
                        print("created successfully....!!!")
                        sr.speak("new note created")
                    else:
                        print(f"error :-> status code = {res.status_code}")
                        sr.speak("can't store the note")


                if "create" in command and ( "repo" in command or "repository"):
                    sr.speak("you want to create new repository in github?")
                    if "yes" in sr.speech_recognition():
                        sr.speak("ok sir, creating new repository")
                        sr.speak("what is the repository name?")
                        
                        while True:
                            repo_name = sr.speech_recognition()
                            sr.speak("your repository name is,   " + repo_name)
                            sr.speak("is that right?")
                            print(repo_name)
                            if "yes" in sr.speech_recognition():
                                break

                        sr.speak("do you want to add any descriptions")
                        if "yes" in sr.speech_recognition():
                            sr.speak("ok then what should be the descriptions?")
                            desc = sr.speech_recognition()
                            print(desc)
                            sr.speak("so your description is   " + desc)
                        else:
                            sr.speak("ok")
                            desc = ""
                        sr.speak("should i create now?")
                        if "yes" in sr.speech_recognition():
                            myGithub.create_repo_using_template(repo_name=repo_name,desc=desc)
                            print("created")
                            sr.speak("new repository created")
                    else:
                        sr.speak("ok sir")

                        
                        


                if "exit" in command: # for exiting program
                    sr.speak("program terminating")
                    exit()
