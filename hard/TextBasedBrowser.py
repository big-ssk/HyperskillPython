import sys
import os
import requests
from bs4 import BeautifulSoup
from colorama import Fore


# write your code here

class Browser:

    def __init__(self, cache_dir):
        self.create_cache_dir(cache_dir)
        self.cache_dir = os.path.abspath(cache_dir)
        self.last_page = None
        self.history = []

    def create_cache_dir(self, cache_dir):
        try:
            os.mkdir(cache_dir)
        except FileExistsError:
            pass

    def show_page(self, url):
        url, cache_name = self.fix_url(url)
        try:
            with open(f'{self.cache_dir}/{cache_name}') as f:
                print(f.read())
        except FileNotFoundError:
            page = requests.get(url)
            parsed_page = BeautifulSoup(page.content, 'html.parser').get_text()
            print(Fore.BLUE + parsed_page)
            self.cache_page(parsed_page, cache_name)
            self.last_page = cache_name

    def fix_url(self, url):
        prefix = 'http://'
        if not url.startswith(prefix):
            cache_name = url.rsplit('.', 1)[0]
            url = prefix + url
        else:
            cache_name = url.lstrip(prefix).rsplit('.', 1)[0]
        return url, cache_name

    def is_cached(self, page):
        if os.path.exists(f'{self.cache_dir}/{page}'):
            return True
        return False

    def cache_page(self, page, cache_name):
        if not self.is_cached(page):
            with open(f'{self.cache_dir}/{cache_name}', 'w') as f:
                f.write(page)

    def is_valid_input(self, url):
        if self.is_cached(url) or '.' in url[-4]:
            return True
        return False

    def open_last_page(self):
        try:
            self.show_page(self.history.pop())
        except IndexError:
            pass

    def main(self):
        while True:
            choice = input()
            if choice == 'exit':
                exit()
            if choice == 'back':
                self.open_last_page()
            if self.is_valid_input(choice):
                self.history.append(self.last_page)
                self.show_page(choice)
            else:
                print('Invalid URL')


browser = Browser(sys.argv[1])
browser.main()
