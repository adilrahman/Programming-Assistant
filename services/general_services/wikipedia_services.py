from bs4 import BeautifulSoup
import requests
import wikipedia as wiki


class WikipediaController:
    def __init__(self) -> None:
        '''
        description:
            None

        Inputs:
            None

        Outputs:
            None
        '''
        pass

    def get_summery(self, topic: str):
        '''
        description:
            it return the summery of the given topic

        Inputs:
            topic = topic name

        Outputs:
            return summery of the topic if `successed the search` otherwise return false
        '''
        try:
            summery = wiki.summary(topic, sentences=2)
            return str(summery).lower()

        except Exception as e:
            print(f"Error => {str(e)}")
            return False

    def google_search_result(self, query: str):
        '''
        description:
            it return the summery of the given query from google top result

        Inputs:
            query = the searching query

        Outputs:
            return summery of the query if `successed the search` otherwise return false
        '''

        url = "https://www.google.com/search?q="

        headers = {
            'User-agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19582'
        }

        url = url + "+".join(query.split(" "))
        print(url)

        try:
            r = requests.get(url=url, timeout=30, headers=headers)
            r.raise_for_status()
            html = r.text
        except:
            print("Get HTML Failed!")
            return False

        if html:
            soup = BeautifulSoup(html, "html.parser")

        try:

            result = soup.find("div", class_='BNeawe').text
        except:
            print("Translation Failed!")
            return False

        return result


if __name__ == "__main__":
    wikipediaController = WikipediaController()
    while True:
        topic = input("topic : ")
        # summery = wikipediaController.get_summery(topic=topic)
        summery = wikipediaController.google_search_result(query=topic)
        print(summery)
