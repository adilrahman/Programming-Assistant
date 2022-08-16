from googlesearch import search
import pyautogui
import webbrowser as wb
wb.register('chrome', None)


class WebsiteController:
    def __init__(self, visiting_website_list: dict) -> None:
        '''
        inputs:
            eg:-
              visiting_website_list = { "google" : "www.google.com" }

        outputs: None
        '''
        self.websites = visiting_website_list

    def open_website(self, name: str) -> None:
        '''
        inputs:
            name = website_name

        output:

            if website url `exist` then:
                 return None and open website in browser
            else:
                return False
        '''
        if name not in self.websites:
            return False

        url = self.websites[name]
        wb.open(url=url)

    @staticmethod
    def open_top_results(query: str, nums_results: int = 5) -> None:
        '''
        description:
            it will open `top` #nums_results `in web browser`

        inputs:
            query = your search query

            nums_results = how many results you want

        output:
            open the results in web browser\n
            return None
        '''

        solutions = search(query)
        for idx, sol in enumerate(solutions):
            if idx == nums_results:
                break
            wb.open(sol)


if __name__ == "__main__":
    web_contr = WebsiteController()
    web_contr.open_website("twitter")
    print("s")
