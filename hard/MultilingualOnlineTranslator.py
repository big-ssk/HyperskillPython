import sys
import requests
from bs4 import BeautifulSoup


class Translation:

    def __init__(self, word_to_translate, source_language, target_language, limit):
        self.word_to_translate = word_to_translate
        self.source_language = source_language
        self.target_language = target_language
        self.limit = limit
        self.data = None
        self.words = None
        self.examples = None
        self.get_data()
        self.parse_data()

    def get_data(self):
        headers = {'user-agent': 'Mozilla/5.0'}
        language_pair = f'{self.source_language.lower()}-{self.target_language.lower()}'
        url = f"https://context.reverso.net/translation/{language_pair}/{self.word_to_translate}"
        response = requests.get(url, headers=headers)
        try:
            self.data = response.content
        except requests.exceptions.ConnectionError:
            print("Something wrong with your internet connection")
            exit()

    def parse_data(self):
        parser = 'html.parser'
        soup = BeautifulSoup(self.data, parser)
        try:
            self.words = '\n'.join(soup.find(id='translations-content').text.split()[:self.limit])
            examples = [x.text.strip() for x in soup.find_all(class_=['src ltr', 'trg ltr'])]
            examples = list(zip(examples[::2], examples[1::2]))[:self.limit]
            self.examples = '\n'.join(['\n'.join(x) for x in examples])
        except AttributeError:
            print(f"Sorry, unable to find {self.word_to_translate}")
            exit()

    def __str__(self):
        return f'\n{self.target_language} Translations:\n{self.words}' \
               f'\n\n{self.target_language} Examples:\n{self.examples}'


class OnlineTranslator:
    LANGUAGES = ['Arabic', 'German', 'English', 'Spanish', 'French', 'Hebrew', 'Japanese',
                 'Dutch', 'Polish', 'Portuguese', 'Romanian', 'Russian', 'Turkish', 'all']

    def __init__(self, source_language, target_language, word_to_translate):
        self.languages = {lang.lower(): lang for lang in OnlineTranslator.LANGUAGES}
        self.results = []
        try:
            self.source_language = self.languages[source_language]
            self.target_language = self.languages[target_language]
        except KeyError:
            print(f"Sorry, the program doesn't support {target_language}")
            exit()
        self.word_to_translate = word_to_translate

    def get_results(self, word_to_translate, source_language, target_language, limit):
        self.results.append(Translation(word_to_translate, source_language, target_language, limit))

    def save_results(self, word_to_translate):
        with open(word_to_translate + '.txt', 'w') as file:
            for result in self.results:
                file.write(str(result))

    def show_results(self, word_to_translate):
        with open(word_to_translate + '.txt') as file:
            print('\n' + file.read().strip())

    def set_up(self):
        if self.target_language != 'all':
            limit = 5
            self.get_results(self.word_to_translate, self.source_language, self.target_language, limit)
        else:
            for language in self.languages:
                self.target_language = self.languages[language]
                if not self.target_language == self.source_language:
                    limit = 1
                    self.get_results(self.word_to_translate, self.source_language, self.target_language, limit)
        self.save_results(self.word_to_translate)
        self.show_results(self.word_to_translate)


if __name__ == '__main__':
    source, target, word = sys.argv[1:]
    translator = OnlineTranslator(source, target, word)
    translator.set_up()
