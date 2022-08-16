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
        if command == "yes":
            return value
        sr.speak("ok tell me once more sir!")
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
