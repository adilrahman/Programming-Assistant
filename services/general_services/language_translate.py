from bs4 import BeautifulSoup
import requests


class LanguageTranslate:
    def __init__(self, lang_from: str, lang_to: str) -> None:
        '''
        description:
            it help translate from one language to another language
        Inputs :
            lang_from = "from which language"

            lang_to = "to which language"

            `language code should be in short form `
        Outputs: None
        '''
        self._from = lang_from
        self._to = lang_to
        self.base_url = "https://translate.google.com/m?hl={}&sl={}&ie=UTF-8&q={}"

    def __getHtmlText(self, url: str):
        '''
        description:
            it make a get request to get the response ( scrap google translator page )
        Inputs:
            url = google translator api for get request

        Outputs:
            translator page html contents
        '''
        try:
            r = requests.get(url=url, timeout=30)
            r.raise_for_status()
            return r.text
        except:
            print("Get HTML Failed!")
            return 0

    def translate(self, text, reverse=False):
        '''
        description:
            translate the given text to the `lang_to`
        Inputs:
            text = text you want to traslate 

        Outputs:
            return translated text `if` no error `else` return `False`
        '''

        if reverse:
            url = self.base_url.format(self._from, self._to, text)
        else:
            url = self.base_url.format(self._to, self._from, text)

        html = self.__getHtmlText(url)
        if html:
            soup = BeautifulSoup(html, "html.parser")

        try:
            result = soup.find_all(
                "div", {"class": "result-container"})[0].text
        except:
            print("Translation Failed!")
            return False

        print("translated :-> " + str(result))
        return result


if __name__ == "__main__":
    languageTranslator = LanguageTranslate(lang_from="en", lang_to="ml")
    while True:
        text = input("enter text : ")
        languageTranslator.translate(text=text)
