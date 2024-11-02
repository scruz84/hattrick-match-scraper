# Hattrick match scraper

This is a sample project for extracting information about matches from the great football game
[Hattrick](https://www.hattrick.org/).

## How it works

When the scraper is launched connects to [Hattrick](https://www.hattrick.org/) for getting matches 
information. This information is stored on a relational database (sqlite3 or Postgresql)

Configuration is read from environment variables, and can be specified on a file named `.ht_scraper.env`.

Sample content:
```
# Connectivity
# DB_DRIVER=postgresql
DB_DRIVER=sqlite3
DB_HOST=localhost
DB_PORT=5432
DB_USER=user
DB_PASSWORD=password
DB_DATABASE=database

# Scraper configuration
AUTO=true
GET_INTERVAL=0.5
NUMBER_MATCHES=10
LANG_REPORT=es
START_MATCH=
UP=false
```

* `AUTO`: if the application takes as starting match the last value processed at database. In case it does not exist,
it takes a random match identifier (true as default)
* `GET_INTERVAL`: seconds between each new request to retrieve a new match (0.5 as default)
* `NUMBER_MATCHES`: total matches to retrieve (1000 as default)
* `LANG_REPORT`: language from the match reports (en by default)
* `START_MATCH`: initial match id used for starting the process. It can be seen here `https://www.hattrick.org/en/Club/Matches/Match.aspx?matchID=<matchId>`, where `matchId` is the value to take.
* `UP`: if the next match to get is the `matchId` + 1 identifier (true by default)

By default, the application stores the data on sqlite3 database named `ht_matches.db`. 
It starts with `AUTO` mode enabled, and it takes a random match identifier as start point in case no matches
are still processed.


Database will contain the following tables with the retrieved information:
* avg_analysis
* avg_analysis_player
* booking
* event
* injury
* match
* match_player
* missed_chance
* rating
* referee
* scorer
* substitution
