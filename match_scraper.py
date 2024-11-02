import logging
import os
import sys
from pathlib import Path

from dotenv import load_dotenv

from scraper.Scraper import Scrapper

logger = logging.getLogger(__name__)

def main():
    logging.basicConfig(filename='ht_scraper.log', level=logging.INFO)
    logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))

    #load configuration
    load_dotenv(dotenv_path=Path('./.ht_scraper.env'))

    scraper = Scrapper(lang=os.getenv('LANG_REPORT'), start_match_id=os.getenv('START_MATCH'),
                       interval=os.getenv('GET_INTERVAL'), number_matches=os.getenv('NUMBER_MATCHES'),
                       auto=os.getenv('AUTO'), up=os.getenv('UP'))
    scraper.start()

if __name__=="__main__":
    main()
