FROM python:3.13-slim

WORKDIR /htscraper

COPY requirements.txt /htscraper
COPY . /htscraper

RUN pip install --no-cache-dir -r requirements.txt

CMD [ "python", "match_scraper.py" ]
