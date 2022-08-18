from speech_recognition_engine import SpeechTextEngine

sr = SpeechTextEngine()


def recheck(type: str, value: str):
    '''
    description:
        it affirming the input text; is that a valid input or not ?

    inputs:
        type = "what type of input is this"; 

            eg:- if it's checking for the affirmation of 
                 project name then: type = "project name"

        value = text / the input from speech recoginition

    outputs:
        if text != empty then:
            return text
        else:
            repeatly asking for the text until get a "none empty text"
    '''

    while True:
        sr.speak(f'your {type} is ' + value)
        sr.speak(" is that right?")
        command = sr.speech_recognition()
        command = nullcheck(command)
        command = yes_or_no(command)
        if command == "yes":
            return value
        sr.speak(f"ok tell me the {type} once more sir!")
        value = sr.speech_recognition()
        value = nullcheck(value)


def nullcheck(value: str):
    '''
    description:
        it check if the text is empty or not

    inputs:
        value = text / the input from speech recoginition

    outputs:
        if text != empty then:
            return text
        else:
            repeatly asking for the text until get a "none empty text"

    '''
    while value == "":
        sr.speak("i didn't get it sir, please tell me once more")
        value = sr.speech_recognition()
    sr.speak("ok")
    return value


def yes_or_no(command: str):
    yes = ["yes", "yea", "i want", "do it", "yeah", "yee", "ya", "yaa" "z", "yep", "yeap"
           "that's right", "proceed", "ok", "ahaa", "go on", "i want", "yeh", "doit", "create"]
    no = ["nah", "no", "don't", "not", "na", "n", "don't", "never"]

    for word in no:
        if word in command:
            return "no"

    for word in yes:
        if word in command:
            return "yes"

    return "nan"
