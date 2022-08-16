
from speech_recognition_engine import SpeechTextEngine
import config
from services.notion import NotionClient
from datetime import datetime
import time
from services.github import MyGithub
from services.general_services import WebsiteController, ErrorSolutions
from utils import nullcheck, recheck, yes_or_no

notion_integration_token = config.NOTION_INTEGRATION_TOKEN
notion_database_id = config.NOTION_DATABASE_ID

sr = SpeechTextEngine()
notionClient = NotionClient(token=notion_integration_token,
                            database_id=notion_database_id)

github_token = config.GITHUB_AUTH_TOKEN
github_template_owner_name = config.GITHUB_TEMPLATE_OWNER_NAME
github_template_repo_name = config.GITHUB_TEMPLATE_REPO_NAME
github_my_name = config.GITHUB_MY_NAME
local_path = config.LOCAL_CLONING_PATH
visiting_website_list = config.VISITING_WEBSITE_LIST


my_info = {"name": github_my_name}

template_data = {"template_owner": github_template_owner_name,
                 "template_name": github_template_repo_name}

myGithub = MyGithub(token=github_token, my_info=my_info,
                    template_datas=template_data, local_path=local_path)

websiteController = WebsiteController(
    visiting_website_list=visiting_website_list)

errorSolutions = ErrorSolutions()

non_active = 0


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
                if "do you" in command:
                    sr.speak("No I don't want")
                print(non_active)
                if "deactivate" in command:  # for deactivate service temporarly
                    non_active = 0
                    print("Deactivate!")
                    sr.speak("Deactivating")
                    break

                if "note" in command or "todo" in command:  # for createing notes
                    non_active = 0

                    # for getting project or repository name
                    sr.speak("for which project sir ?")
                    project_name = sr.speech_recognition()
                    project_name = nullcheck(value=project_name)
                    project_name = recheck(
                        type="project name", value=project_name)

                    # for getting task or todo or note
                    sr.speak("tell me the note sir?")
                    note = sr.speech_recognition()
                    note = nullcheck(value=note)
                    note = recheck(type="note", value=note)

                    sr.speak(" should i store?")
                    command = sr.speech_recognition()
                    command = yes_or_no(nullcheck(sr.speech_recognition()))

                    if "no" == command:
                        sr.speak("Ok sir")
                        continue

                    time_now = datetime.now().astimezone().isoformat()
                    status = "Active"
                    res = notionClient.create_page(
                        project_name=project_name, task=note, status=status, date=time_now)

                    if res.status_code == 200:
                        print("created successfully....!!!")
                        sr.speak("new note created")
                    else:
                        print(f"error :-> status code = {res.status_code}")
                        sr.speak("can't store the note")

                # finding solutions for error
                if ("find" in command or "solution" in command or "solutions" in command) and ("error" in command):
                    sr.speak("ok")
                    sr.speak("Enter the error message in the prompt")
                    errorSolutions.find()
                    sr.speak("finding solutions....")

                # opening websites
                if "open" in command:
                    non_active = 0
                    name = command.split("open ")

                    if name == "" or len(name) == 1:
                        sr.speak(
                            "i didn't get the website name please tell me once more")
                        name = sr.speech_recognition()
                        name = nullcheck(value=name)
                        name = recheck(type="website", value=name)
                    else:
                        name = name[-1]

                    sr.speak("opening " + name)
                    websiteController.open_website(name=name)

                if "create" in command and ("repo" in command or "repository"):
                    non_active = 0
                    sr.speak("you want to create new repository in github?")
                    command = yes_or_no(nullcheck(sr.speech_recognition()))
                    if "yes" == command:
                        sr.speak("ok sir, creating new repository")
                        sr.speak("what is the repository name?")

                        repo_name = sr.speech_recognition()
                        repo_name = nullcheck(value=repo_name)
                        repo_name = recheck(
                            type="repository name", value=repo_name)

                        sr.speak("do you want to add any descriptions?")
                        command = yes_or_no(nullcheck(sr.speech_recognition()))
                        if "yes" == command:
                            sr.speak(
                                "ok then what should be the descriptions?")

                            desc = sr.speech_recognition()
                            desc = nullcheck(value=desc)
                            desc = recheck(type="description", value=desc)

                        else:
                            sr.speak("ok")
                            desc = ""

                        sr.speak("should i create now?")
                        command = yes_or_no(nullcheck(sr.speech_recognition()))
                        if "yes" == command:
                            repo_url = myGithub.create_repo_using_template(
                                repo_name=repo_name, desc=desc)

                            if repo_url == False:
                                print("failed")
                                sr.speak(
                                    "can't create the repository due to some errors,  please check the configaration file")
                                break

                            print("created")
                            sr.speak("new repository created")
                            sr.speak(
                                "Do you want to create a local copy of this repository ?")

                            command = yes_or_no(
                                nullcheck(sr.speech_recognition()))

                            if "yes" == command:
                                sr.speak("cloning the repository...")
                                myGithub.clone_repository(repo_url)
                    else:
                        sr.speak("ok sir")

                if "prompt" in command or "prom" in command:
                    sr.speak("opening search prompt..")
                    WebsiteController.search_prompt()

                if "clone this" in command:
                    while True:
                        sr.speak("ok")
                        sr.speak("cloning the repository....")
                        status = myGithub.clone_this_repository()
                        if status == False:
                            sr.speak("cloning failed")
                            sr.speak("make sure the repository link")
                            sr.speak("do you wanna try again!")
                            command = yes_or_no(
                                nullcheck(sr.speech_recognition()))
                            if command == "yes":
                                continue
                            else:
                                break
                        else:
                            break

                if "firday" in command and non_active > 0:
                    sr.speak("yes tell sir")

                if "exit" in command:  # for exiting program
                    sr.speak("program terminating")
                    exit()

                non_active += 1
