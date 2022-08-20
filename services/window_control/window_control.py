import sys
import pyautogui


minimize_window_coordinates = {"x": 1836, "y": 47}
close_window_coordinates = {"x": 1836, "y": 45}


class ScreenControl:
    def __init__(self, speech_rec, speech_to_text) -> None:
        self.get_audio = speech_rec
        self.speech_to_text = speech_to_text

    def start_writing(self) -> None:
        '''
        description:
            this function will write the given text in the input field of the window

            if text == "stop writing":
                it stop writing 

            otherwise: it keep writing  

        Inputs:
            text = text you want to write

        Outputs: None
        '''
        text = ""
        while "stop writing" not in text:

            if text != "":
                text += " "
                pyautogui.write(message=text, interval=0.1)

            audio = self.get_audio(phrase_time_limit=7)
            text = self.speech_to_text(audio=audio)

    def press_enter() -> None:
        '''description : press enter'''
        pyautogui.keyDown("return")

    def minimize_window(self):

        x = minimize_window_coordinates["x"]
        y = minimize_window_coordinates["y"]
        pyautogui.moveTo(x, y)
        pyautogui.click()

    def close_window(self):
        x = close_window_coordinates["x"]
        y = close_window_coordinates["y"]
        pyautogui.click(x=x, y=y)


if __name__ == "__main__":
    sys.path.append('../../')
    from speech_recognition_engine.speech_recognition_engine import SpeechTextEngine
    sr = SpeechTextEngine()
    speech_rec = sr.get_audio
    speech_to_text = sr.audio_to_text

    sc = ScreenControl(speech_rec=speech_rec, speech_to_text=speech_to_text)
    sc.start_writing()
