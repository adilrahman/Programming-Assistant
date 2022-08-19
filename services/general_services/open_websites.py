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
        self.google_search = "www.google.com/search?gx&q="

    def open_website(self, name: str) -> None:
        '''
        description:
            it open the website in webbrowser;
            if the given name is in the visiting_website_list the it go to that url
            `otherwise` it do a google search and go to the top result 
        inputs:
            name = website_name

        output:

            if website url `exist` then:
                 return None and open website in browser
            else:
                return False
        '''
        if name not in self.websites:
            self.open_top_results(query=name, nums_results=1)
            return

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

    @staticmethod
    def search_prompt():
        '''
        description:
            it will open `top` #nums_results `in web browser`

        inputs:
           open a prompt to enter the queries

        output:
            open the results in web browser\n
            return None
        '''
        query = pyautogui.prompt(title="Enter the query?")

        if query == None or len(query) == 0:
            return False

        nums_results = pyautogui.prompt(
            title="how many results you want?")

        if len(nums_results) == 0:
            return False

        nums_results = int(nums_results)

        solutions = search(query)
        for idx, sol in enumerate(solutions):
            if idx == nums_results:
                break
            wb.open(sol)

    def search_query(self, query: str):
        pass


if __name__ == "__main__":
    visiting_website_list = {"twitter": "www.twitter.com"}
    web_contr = WebsiteController(visiting_website_list=visiting_website_list)
    while True:
        x = input("website : ")
        web_contr.open_website(name=x)
    # WebsiteController.search_prompt()
