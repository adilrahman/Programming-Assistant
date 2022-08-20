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


if __name__ == "__main__":
    wikipediaController = WikipediaController()
    while True:
        topic = input("topic : ")
        summery = wikipediaController.get_summery(topic=topic)
        print(summery)
