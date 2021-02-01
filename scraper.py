from bs4 import BeautifulSoup
import requests
import re


class PageScrape:
    def __init__(self, url, list_type_input):
        """
        :param url: The url of webpage you want to scrape from
        :param list_type_input: int representing what type of list it is, as asked in input question
        """
        self.url = url
        self.soup = self._make_soup_()
        # First locate the title in the HTML
        list_title = self.soup.find('h1').get_text(strip=False, separator=" ")
        # Replace numbers in the title and strip whitespace
        self.title = re.sub('[0-9]{2,3} ', '', list_title).strip()
        self.list_types = {1: 'song', 2: 'artist', 3: 'album', 4: 'musician'}
        self.list_type = self.list_types[list_type_input]
        self.item_list = self._create_list_()

    def _make_soup_(self):
        """
        Function to request input URL, check for error and return parsed HTML
        :return:
        """
        response = requests.get(self.url)
        response.raise_for_status()
        content = response.text
        return BeautifulSoup(content, "html.parser", exclude_encodings=["iso-8859-7"])

    def _create_list_(self):
        print(f"\nScraping {self.title} List...\n")
        arr = self.soup.find_all(class_="list")
        item_list_text = ''
        for i in range(len(arr)):
            item_list_text += arr[i].get_text(strip=True)
        return [song.split('-') for song in re.split('[0-9]{1,3}[.]', item_list_text) if len(song) > 5]
