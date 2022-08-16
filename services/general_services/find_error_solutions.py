from googlesearch import search
import pyautogui
import webbrowser as wb
from .open_websites import WebsiteController


wb.register('chrome', None)


class ErrorSolutions:
    def __init__(self) -> None:
        pass

    def find(self, num_solutions: int = 5) -> None:
        '''
        description:
            it will open a prompt to enter the error message and `top` #num_solutions\n
            will `open in web browser`

        inputs:
            num_solutions = how many solutions you want 

        output:
            `open the solutions in web browser`\n
            return None
        '''
        error_msg = pyautogui.prompt(title="copy the error message here")

        WebsiteController.open_top_results(query=error_msg,
                                           nums_results=num_solutions)


if __name__ == "__main__":

    errSolutions = ErrorSolutions()
    errSolutions.find()
