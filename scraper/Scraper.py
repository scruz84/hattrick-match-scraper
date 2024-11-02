import json
import logging
import re
import sys
import time
from random import randrange

import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

from database.DataAccess import DataAccess

logger = logging.getLogger(__name__)

MATCHES_URL = 'https://www.hattrick.org/${lang}/Club/Matches/Match.aspx?matchID=${matchId}'


def extract_match_data(content: str) -> str:
    match = re.search(r"window\.HT\.ngMatch\.data\s*=\s*(\{.*}).*", content, re.MULTILINE)
    if match is not None and len(match.groups()) > 0:
        return match.group(1)
    return ""


class Scrapper:
    lang: str
    interval: float
    start_match_id: int
    number_matches: int
    up: bool
    auto: bool
    data_access: DataAccess

    def __init__(self, lang, interval, start_match_id, number_matches, auto, up):
        super().__init__()
        self.lang = 'en' if lang=='' or lang is None else lang
        self.interval = 0.5 if interval=='' or interval is None else float(interval)
        self.start_match_id = None if start_match_id=='' or start_match_id is None else int(start_match_id)
        self.number_matches = 1000 if number_matches=='' or number_matches is None else int(number_matches)
        self.up = True if up=='' or up is None else bool(up)
        self.auto = False if auto=='false' else True
        self.data_access = DataAccess()

    def start(self):
        ua = UserAgent(fallback="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36")
        header = {'User-Agent': str(ua.chrome)}

        if self.auto:
            self.start_match_id = self.data_access.get_auto_start_match(self.up)
            if self.start_match_id is None:
                self.start_match_id = randrange(1, 738392291)
        else:
            if self.start_match_id is None:
                logger.error("Parameter START_MATCH not specified with AUTO mode disabled")
                sys.exit(1)

        if self.up:
            match_range = range(self.start_match_id, self.start_match_id+self.number_matches, 1)
        else:
            match_range = range(self.start_match_id, self.start_match_id-self.number_matches, -1)

        logger.info("Starting the scraper\n\tAuto=%s\n\tAscendant order=%s\n\tInitial match=%d\n\tTotal matches=%d"
                    "\n\tLanguage:%s\n\tDatabase=%s",
                    self.auto, self.up, self.start_match_id, self.number_matches, self.lang, self.data_access.driver)

        for match_id in match_range:
            try:
                #get the json with data of the match
                logger.info("Requesting match %d", match_id)
                match_data = self.get_match_data(header, match_id)
                self.data_access.insert_match(match_data)
                #waits the interval for continuing
                time.sleep(self.interval)
            except Exception as err:
                logger.error("Error processing match %d: %s", match_id, err)


    def get_match_data(self, header, match_id):
        ht_url = (MATCHES_URL.replace("${lang}", self.lang)
                  .replace("${matchId}", str(match_id)))
        html_content = requests.get(ht_url, headers=header).text
        soup = BeautifulSoup(html_content, 'html.parser')
        script_tags = soup.find_all("script")
        for s in script_tags:
            match_data = extract_match_data(s.getText())
            if match_data != "":
                return json.loads(match_data)
        return None
