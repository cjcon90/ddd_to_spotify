from scraper import PageScrape
from playlist import PlaylistMachine

URL_MUSIC_LISTS = 'https://digitaldreamdoor.com/pages/music0.html'
URL_BEST_SONGS = 'https://digitaldreamdoor.com/pages/best_songsddd.html'
input_url = input("Please paste the url of the DigitalDreamDoor page you want to create a playlist from:\n")
input_list_type = int(input("What type of 'best of' list is this? (Select by entering 1, 2, 3 or 4)\n"
                            "1) A 'best song' list\n"
                            "2) A 'best artist' list\n"
                            "3) A 'best album' list\n"
                            "4) A 'best musician' list\n"))

digital_dream_door = PageScrape(input_url, input_list_type)
spotify_machine = PlaylistMachine(digital_dream_door)