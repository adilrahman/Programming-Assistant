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


if __name__ == "__main__":
    web_contr = WebsiteControl()
    web_contr.open_website("twitter")
    print("s")
