import json
import os
import random
import re
from services.general_services.language_translate import LanguageTranslate
from speech_recognition_engine import SpeechTextEngine
import config
from services.notion import NotionClient
from datetime import datetime
import time
from services.github import MyGithub
from services.general_services import WebsiteController, ErrorSolutions, TakeScreenShot
from utils import nullcheck, recheck, yes_or_no
from nlp.intent_classification.naive_bayes import NaiveByasModel
from services.window_control import ScreenControl
import pyautogui
from speech_text_client import speechTextClient
from services.general_services.wikipedia_services import WikipediaController

notion_integration_token = config.NOTION_INTEGRATION_TOKEN
notion_database_id = config.NOTION_DATABASE_ID


languageTranslator = LanguageTranslate(lang_from="en", lang_to="ml")

# sr = SpeechTextEngine(translator=languageTranslator,
#                       speaking_lang="ml", listen_lang="ml-IN")

sr = speechTextClient

notionClient = NotionClient(token=notion_integration_token,
                            database_id=notion_database_id)

github_token = config.GITHUB_AUTH_TOKEN
github_template_owner_name = config.GITHUB_TEMPLATE_OWNER_NAME
github_template_repo_name = config.GITHUB_TEMPLATE_REPO_NAME
github_my_name = config.GITHUB_MY_NAME
local_path = config.LOCAL_CLONING_PATH
visiting_website_list = config.VISITING_WEBSITE_LIST
screenshot_locations = config.SCREENSHOTS_PATH


my_info = {"name": github_my_name}

template_data = {"template_owner": github_template_owner_name,
                 "template_name": github_template_repo_name}

myGithub = MyGithub(token=github_token, my_info=my_info,
                    template_datas=template_data, local_path=local_path)

websiteController = WebsiteController(
    visiting_website_list=visiting_website_list)

errorSolutions = ErrorSolutions()

screenshot = TakeScreenShot(path=screenshot_locations)

non_active = 0

intent_classifier = NaiveByasModel()

screenControl = ScreenControl(
    speech_rec=sr.get_audio, speech_to_text=sr.audio_to_text)

wikipediaController = WikipediaController()


# loading intent json for making random responses
intent_json_file_loc = "nlp/intent_classification/intents.json"
with open(intent_json_file_loc, "r") as file:
    intents = json.load(file)

intents_response = {}

for intent in intents["intents"]:
    intents_response[intent["tag"]] = intent["response"]


def check_activity(command):
    global non_active
    if non_active > 10:
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


def random_response(intent: str) -> None:
    '''
    description:
        it choose responses from intent file randomly
        for specific intents

    Inputs:
        intent = "the intent"
    Ouputs:
        speak response
    '''
    if intent == "not a command":
        return

    res = intents_response[intent]
    res = random.choice(res)
    sr.speak(res)


if __name__ == "__main__":

    while True:
        if sr.wakeup():  # repeat until hear wake up command
            sr.speak("listening sir....")
            time.sleep(0.5)
            while True:  # commanding mode on
                command = sr.speech_recognition()
                # command = check_activity(command)
                intent = intent_classifier.find_intent(command=command)
                random_response(intent=intent)

                print("intent -> " + intent)
                if intent == "deactivate":  # for deactivate service temporarly
                    non_active = 0
                    print("Deactivate!")
                    break

                if intent == "take note":  # for createing notes
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
                if intent == "find solutions":

                    sr.speak("Enter the error message in the prompt")
                    errorSolutions.find()
                    sr.speak("finding solutions....")

                # opening websites
                if intent == "open websites":
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

                if intent == "create repository":
                    non_active = 0
                    sr.speak("you want to create new repository in github?")
                    command = yes_or_no(nullcheck(sr.speech_recognition()))
                    if "yes" == command:

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

                if intent == "web search prompt":
                    WebsiteController.search_prompt()

                if intent == "clone repository":
                    while True:
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

                if intent == "take screenshot":
                    img_loc = screenshot.capture()

                    if img_loc == False:
                        sr.speak("i couldn't take the image sir")
                        continue

                    sr.speak("screenshot taken")
                    sr.speak("you wanna see the image?")
                    command = sr.speech_recognition()
                    command = nullcheck(command)
                    if yes_or_no(command=command) == "yes":
                        screenshot.open_image(img_loc=img_loc)
                    else:
                        sr.speak("ok")

                if intent == "start writing":
                    screenControl.start_writing()
                    sr.speak("ok. writing off")
                    sr.speak("should i submit this")
                    command = sr.speech_recognition()
                    command = yes_or_no(nullcheck(value=command))
                    if "yes" == command:
                        screenControl.press_enter()
                    sr.speak("ok")

                if intent == "music":
                    command = command + "in youtube"
                    websiteController.open_top_results(
                        query=command, nums_results=1)
                    #os.system("spotify &")

                if intent == "text translation":

                    patterns = [
                        "the meaning of",
                        "is mean by"]

                    find_pattern = False

                    for pattern in patterns:
                        if re.search(pattern=pattern, string=command) != None:
                            find_pattern = True
                            break

                    if find_pattern:
                        text = command.split(pattern)[-1]
                    else:
                        sr.speak("ok tell me the text")
                        text = sr.speech_recognition()
                        text = nullcheck(text)

                    translated_text = languageTranslator.translate(
                        text=text)
                    sr.speak(translated_text, lang="ml")
                    pyautogui.alert(text=translated_text)

                if intent == "wikipeadia":

                    summery = wikipediaController.google_search_result(
                        query=command)

                    sr.speak(summery)
                    pyautogui.alert(summery)
                    continue

                    patterns = [
                        "what is ",
                        "tell me about ",
                        "who is "]

                    find_pattern = False

                    for pattern in patterns:
                        if re.search(pattern=pattern, string=command) != None:
                            find_pattern = True
                            break

                    if find_pattern:
                        text = command.split(pattern)[-1]

                    else:
                        sr.speak("ok tell me the topic")
                        text = sr.speech_recognition()
                        text = nullcheck(text)

                    summery = wikipediaController.get_summery(topic=text)
                    if summery == False:
                        summery = wikipediaController.google_search_result(
                            query=command)

                    sr.speak(summery)
                    pyautogui.alert(summery)

                if intent == "exit":  # for exiting program
                    exit()

                if "friday" in command and non_active > 0:
                    non_active = 0
                    sr.speak("yes tell me sir")

                non_active += 1
