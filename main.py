import os

from bs4 import BeautifulSoup
from dotenv import load_dotenv
import requests
from trello import TrelloClient

URL = 'https://libraryofjuggling.com/TricksByDifficulty.html'

# Get this information from
load_dotenv()
TRELLO_CLIENT = TrelloClient(api_key=os.environ['API_KEY'],
                             api_secret=os.environ['API_SECRET'],
                             token=os.environ['TOKEN'])

if __name__ == '__main__':
    html = requests.get(URL).content
    soup = BeautifulSoup(html, features='html.parser')

    # Setup Trello board
    juggling_board = TRELLO_CLIENT.add_board(board_name='Juggling')
    juggling_board.add_list('Mastered', pos=3)
    juggling_board.add_list('Learning', pos=2)
    trick_list = juggling_board.add_list('Tricks', pos=1)

    for level, unordered_list in enumerate(soup.find_all('ul', 'MainText'), 2):
        print(f"Level {level}")
        trello_label = juggling_board.add_label(f"Level {level}", color=None)

        tricks = unordered_list.find_all('a')
        for trick in tricks:
            url = 'https://libraryofjuggling.com/' + trick.attrs['href']
            trick_name = trick.text
            trick_list.add_card(name=trick_name,
                                desc=url,
                                labels=[trello_label])
            print(f"Added {trick_name} to Trello.")
