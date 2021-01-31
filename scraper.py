from bs4 import BeautifulSoup
import requests
import re


class PageScrape:
    def __init__(self, url, list_type_input):
        """
        :param url: The url of webpage you want to scrape from
        :param list_type: str representing what type of "best of" list it is
        select either 'artist' / 'musician' / 'album' / 'song'
        """
        self.url = url
        self.soup = self._make_soup_()
        self.title = re.sub('[0-9]{2,3}', '', self.soup.find(itemprop="headline").text).strip()
        self.list_type = {1: 'song', 2: 'artist', 3: 'musician', 4: 'album'}
        self.song_list = self._get_tracks_(self.list_type[list_type_input])

    def _make_soup_(self):
        response = requests.get(self.url)
        response.raise_for_status()
        content = response.text
        return BeautifulSoup(content, "html.parser", exclude_encodings=["iso-8859-7"])

    def _get_tracks_(self, list_type):
        if list_type == 'song':
            return self._scrape_song_list_()
        else:
            return None

    def _scrape_song_list_(self):
        print(f"\nScraping {self.title} List...\n")
        arr = self.soup.find_all(class_="list")
        song_list_text = ''
        for i in range(len(arr)):
            song_list_text += arr[i].get_text(strip=True)
        return [song.split('-') for song in re.split('[0-9]{1,3}[.]', song_list_text) if len(song) > 5]