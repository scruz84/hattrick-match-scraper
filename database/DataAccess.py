import logging
import os
import sqlite3
import psycopg

logger = logging.getLogger(__name__)

class DataAccess:
    driver: str
    host: str
    port: str
    user: str
    password: str
    database: str

    def __init__(self):
        super().__init__()
        driver = os.getenv('DB_DRIVER')
        if driver == 'postgresql':
            self.host = os.getenv('DB_HOST')
            self.port = os.getenv('DB_PORT')
            self.user = os.getenv('DB_USER')
            self.password = os.getenv('DB_PASSWORD')
            self.database = os.getenv('DB_DATABASE')
        else:
            driver = 'sqlite3'

        self.driver = driver
        self._init()

    def _init(self):
        self.execute_sql_file("database/sql/create_match_table.sql")
        self.execute_sql_file("database/sql/create_player_table.sql")
        self.execute_sql_file("database/sql/create_avg_analysis_players.sql")
        self.execute_sql_file("database/sql/create_avg_analysis_sectors.sql")
        self.execute_sql_file("database/sql/create_booking_table.sql")
        self.execute_sql_file("database/sql/create_event_table.sql")
        self.execute_sql_file("database/sql/create_injuries_table.sql")
        self.execute_sql_file("database/sql/create_missed_chance.sql")
        self.execute_sql_file("database/sql/create_rating_table.sql")
        self.execute_sql_file("database/sql/create_scorer_table.sql")
        self.execute_sql_file("database/sql/create_substitution_table.sql")
        self.execute_sql_file("database/sql/create_table_referee.sql")


    def get_connection(self):
        if "sqlite3" == self.driver:
            return sqlite3.connect("ht_matches.db")
        else:
            conn = psycopg.connect("host="+self.host+" port="+self.port+" dbname="+self.database+" user="+self.user+" password="+self.password)
            conn.autocommit = True
            return conn


    def execute_sql_file(self, file):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            with open(file, "r") as f:
                try:
                    cursor.execute(f.read())
                except Exception as err:
                    logger.info(err)
            cursor.close()

    def insert_match(self, match_data : dict):
        self.remove_match(match_data["matchId"])
        with self.get_connection() as conn:
            cursor = conn.cursor()

            if match_data["isFinished"]:
                #Match table
                self.insert_match_data(cursor, match_data)
                self.insert_players_data(cursor, match_data)
                self.insert_events_data(cursor, match_data)
                self.insert_bookings_data(cursor, match_data)
                self.insert_scorers_data(cursor, match_data)
                self.insert_missed_chances_data(cursor, match_data)
                self.insert_injuries_data(cursor, match_data)
                self.insert_substitutions_data(cursor, match_data)
                self.insert_ratings_data(cursor, match_data)
                self.insert_avg_sectors_data(cursor, match_data)
                self.insert_avg_players_data(cursor, True, match_data)
                self.insert_avg_players_data(cursor, False, match_data)
                self.insert_referees_data(cursor, match_data)
            else:
                logger.info("match %d not played", match_data["matchId"])

            cursor.close()

    def remove_match(self, match_id: int):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(self.check_param_style(sql='DELETE FROM match where matchId = %s'), (match_id,))



    def insert_match_data(self, cursor, match_data):
        cursor.execute(self.check_param_style(sql=
            'insert into match (matchId, sourceSystem, matchType, matchSpeed, leagueId, leagueName, lluId, lluName, cupId, '
            'cupName, cupLevel, cupLevelIndex, tournamentId, tournamentTypeId, specialTournamentTypeId, '
            'tournamentName, federationId, federationName, homeTeamId, awayTeamId, homeTeamIdDB, '
            'awayTeamIdDB, homeIsBot, awayIsBot, homeMotherTeamId, awayMotherTeamId, homeTeamName, '
            'awayTeamName, homeShortTeamName, awayShortTeamName, homeGoals, awayGoals, homeStatement, '
            'awayStatement, isWalkover, homeNrOfChances_left, homeNrOfChances_middle, homeNrOfChances_right, '
            'homeNrOfChances_other, homeNrOfChances_specialEvents, homeNrOfChances_leftGoals, '
            'homeNrOfChances_middleGoals, homeNrOfChances_rightGoals, homeNrOfChances_otherGoals, '
            'homeNrOfChances_specialEventsGoals, awayNrOfChances_left, awayNrOfChances_middle, '
            'awayNrOfChances_right, awayNrOfChances_other, awayNrOfChances_specialEvents, '
            'awayNrOfChances_leftGoals, awayNrOfChances_middleGoals, awayNrOfChances_rightGoals, '
            'awayNrOfChances_otherGoals, awayNrOfChances_specialEventsGoals, matchDate, matchRound, '
            'matchRoundsLeft, season, arenaTeamId, arenaId, arenaName, arenaCapacity, seatsStanding, '
            'seatsPlain, seatsPlus, seatsBoxed, isFinished, weather, homeTacticType, awayTacticType, '
            'homeTacticSkill, awayTacticSkill, homeCoachModifier, awayCoachModifier, homeLogoUrl, '
            'awayLogoUrl, homeShirtUrl, awayShirtUrl, homeKitId, awayKitId, homeGoalKeeperKitId, '
            'awayGoalKeeperKitId, isMatchOrderSet, expectedResult, soldSeatsStanding, soldSeatsPlain, '
            'soldSeatsPlus, soldSeatsBoxed, possessionFirstHalf, possessionSecondHalf, matchSecond, '
            'halftimeBreak, overtimeBreak, addedMinutes, nextEventInSeconds, isArchive, chatChannelId, '
            'chatTitle, pimp, aggregatedScore, shouldHideSquadAndStatus, eggHunt, memorialEvent) '
            'values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,'
            '%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,'
            ' %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, '
            '%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'),
            (match_data['matchId'], match_data['sourceSystem'], match_data['matchType'],
             match_data['matchSpeed'], match_data['leagueId'], match_data['leagueName'], match_data['lluId'],
             match_data['lluName'], match_data['cupId'],
             match_data['cupName'], match_data['cupLevel'], match_data['cupLevelIndex'], match_data['tournamentId'],
             match_data['tournamentTypeId'], match_data['specialTournamentTypeId'],
             match_data['tournamentName'], match_data['federationId'], match_data['federationName'],
             match_data['homeTeamId'],
             match_data['awayTeamId'], match_data['homeTeamIdDB'],
             match_data['awayTeamIdDB'], match_data['homeIsBot'], match_data['awayIsBot'],
             match_data['homeMotherTeamId'],
             match_data['awayMotherTeamId'], match_data['homeTeamName'],
             match_data['awayTeamName'], match_data['homeShortTeamName'], match_data['awayShortTeamName'],
             match_data['homeGoals'],
             match_data['awayGoals'], match_data['homeStatement'],
             match_data['awayStatement'], match_data['isWalkover'],
             match_data['homeNrOfChances']['left'],
             match_data['homeNrOfChances']['middle'],
             match_data['homeNrOfChances']['right'],
             match_data['homeNrOfChances']['other'],
             match_data['homeNrOfChances']['specialEvents'],
             match_data['homeNrOfChances']['leftGoals'],
             match_data['homeNrOfChances']['middleGoals'],
             match_data['homeNrOfChances']['rightGoals'],
             match_data['homeNrOfChances']['otherGoals'],
             match_data['homeNrOfChances']['specialEventsGoals'],
             match_data['awayNrOfChances']['left'],
             match_data['awayNrOfChances']['middle'],
             match_data['awayNrOfChances']['right'],
             match_data['awayNrOfChances']['other'],
             match_data['awayNrOfChances']['specialEvents'],
             match_data['awayNrOfChances']['leftGoals'],
             match_data['awayNrOfChances']['middleGoals'],
             match_data['awayNrOfChances']['rightGoals'],
             match_data['awayNrOfChances']['otherGoals'],
             match_data['awayNrOfChances']['specialEventsGoals'],
             match_data['matchDate'], match_data['matchRound'],
             match_data['matchRoundsLeft'], match_data['season'], match_data['arenaTeamId'], match_data['arenaId'],
             match_data['arenaName'], match_data['arenaCapacity'], match_data['seatsStanding'],
             match_data['seatsPlain'], match_data['seatsPlus'], match_data['seatsBoxed'], match_data['isFinished'],
             match_data['weather'], match_data['homeTacticType'], match_data['awayTacticType'],
             match_data['homeTacticSkill'], match_data['awayTacticSkill'], match_data['homeCoachModifier'],
             match_data['awayCoachModifier'], match_data['homeLogoUrl'],
             match_data['awayLogoUrl'], match_data['homeShirtUrl'], match_data['awayShirtUrl'], match_data['homeKitId'],
             match_data['awayKitId'], match_data['homeGoalKeeperKitId'],
             match_data['awayGoalKeeperKitId'], match_data['isMatchOrderSet'], match_data['expectedResult'],
             match_data['soldSeatsStanding'], match_data['soldSeatsPlain'],
             match_data['soldSeatsPlus'], match_data['soldSeatsBoxed'], match_data['possessionFirstHalf'],
             match_data['possessionSecondHalf'], match_data['matchSecond'],
             match_data['halftimeBreak'], match_data['overtimeBreak'], match_data['addedMinutes'],
             match_data['nextEventInSeconds'], match_data['isArchive'], match_data['chatChannelId'],
             match_data['chatTitle'], match_data['pimp'], match_data['aggregatedScore'],
             match_data['shouldHideSquadAndStatus'], match_data['eggHunt'], match_data['memorialEvent'],),
        )

    def insert_players_data(self, cursor, match_data):
        try:
            players_data = match_data['players']
            for player in players_data:
                cursor.execute(self.check_param_style(sql='insert into match_player (matchId, playerId, sourcePlayerId, teamId, firstName, nickName, '
                               'lastName, playerNumber, specialty, health) '
                               'values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'),
                               (match_data['matchId'], player['playerId'], player['sourcePlayerId'],
                                player['teamId'], player['firstName'], player['nickName'],
                                player['lastName'], player['playerNumber'], player['specialty'],
                                player['health'],),)
        except Exception as err:
            logger.error(err)


    def insert_events_data(self, cursor, match_data):
        try:
            events_data = match_data['events']
            for event in events_data:
                cursor.execute(self.check_param_style(sql='insert into event (matchId, eventIndex, eventType, eventVariation, matchMinute, '
                               'matchMinuteSecond, matchPart, eventText, eventTextLive, subjectTeamId, subjectPlayerId, '
                               'objectPlayerId, originalEventIndex, offsetSecond) '
                               'values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'),
                               (match_data['matchId'], event['eventIndex'], event['eventType'],
                                event['eventVariation'], event['matchMinute'], event['matchMinuteSecond'],
                                event['matchPart'], event['eventText'], event['eventTextLive'],
                                event['subjectTeamId'], event['subjectPlayerId'],
                                event['objectPlayerId'], event['originalEventIndex'],event['offsetSecond'],),)
        except Exception as err:
            logger.error(err)


    def insert_bookings_data(self, cursor, match_data):
        try:
            bookings_data = match_data['bookings']
            for booking in bookings_data:
                cursor.execute(self.check_param_style(sql='insert into booking (matchId, playerId, matchMinute, matchMinuteSecond, matchPart, '
                               'cardValue, eventIndex)  '
                               'values (%s, %s, %s, %s, %s, %s, %s)'),
                               (match_data['matchId'], booking['playerId'], booking['matchMinute'],
                                booking['matchMinuteSecond'], booking['matchPart'],
                                booking['cardValue'], booking['eventIndex'],),)
        except Exception as err:
            logger.error(err)


    def insert_scorers_data(self, cursor, match_data):
        try:
            scorers_data = match_data['scorers']
            for scorer in scorers_data:
                cursor.execute(self.check_param_style(sql='insert into scorer (matchId, playerId, matchMinute, matchMinuteSecond, matchPart, homeGoals, '
                               'awayGoals, eventIndex) '
                               'values (%s, %s, %s, %s, %s, %s, %s, %s)'),
                               (match_data['matchId'], scorer['playerId'], scorer['matchMinute'],
                                scorer['matchMinuteSecond'], scorer['matchPart'],
                                scorer['homeGoals'], scorer['awayGoals'],
                                scorer['eventIndex'],),)
        except Exception as err:
            logger.error(err)


    def insert_missed_chances_data(self, cursor, match_data):
        try:
            missed_chances_data = match_data['missedChances']
            for chance in missed_chances_data:
                cursor.execute(self.check_param_style(sql='insert into missed_chance (matchId, playerId, eventTypeId, matchMinute, matchMinuteSecond, '
                               'matchPart, eventIndex)'
                               'values (%s,%s,%s,%s,%s,%s,%s)'),
                               (match_data['matchId'], chance['playerId'], chance['eventTypeId'],
                                chance['matchMinute'], chance['matchMinuteSecond'],
                                chance['matchPart'], chance['eventIndex'],),)
        except Exception as err:
            logger.error(err)


    def insert_injuries_data(self, cursor, match_data):
        try:
            injuries_data = match_data['injuries']
            for injury in injuries_data:
                cursor.execute(self.check_param_style(sql='insert into injury (matchId, playerId, matchMinute, matchMinuteSecond, matchPart, '
                               'injuryValue, eventIndex) '
                               'values (%s, %s, %s, %s, %s, %s, %s)'),
                               (match_data['matchId'], injury['playerId'],
                                injury['matchMinute'], injury['matchMinuteSecond'],
                                injury['matchPart'], injury['injuryValue'],
                                injury['eventIndex'],),)
        except Exception as err:
            logger.error(err)


    def insert_substitutions_data(self, cursor, match_data):
        try:
            substitutions_data = match_data['substitutions']
            for substitution in substitutions_data:
                cursor.execute(self.check_param_style(sql='insert into substitution (matchId, outPlayerId, inPlayerId, matchMinute, '
                               'matchMinuteSecond, matchPart, orderType,eventIndex, outPositionId, inPositionId, '
                               'outBehaviour, inBehaviour, oldFormation, newFormation)'
                               'values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'),
                               (match_data['matchId'], substitution['outPlayerId'],substitution['inPlayerId'],
                                substitution['matchMinute'], substitution['matchMinuteSecond'],
                                substitution['matchPart'], substitution['orderType'],
                                substitution['eventIndex'], substitution['outPositionId'],
                                substitution['inPositionId'], substitution['outBehaviour'],
                                substitution['inBehaviour'], substitution['oldFormation'],
                                substitution['newFormation'],),)
        except Exception as err:
            logger.error(err)


    def insert_ratings_data(self, cursor, match_data):
        try:
            ratings_data = match_data['ratings']
            for rating in ratings_data:
                cursor.execute(self.check_param_style(sql='insert into rating (matchId, teamId, averageMidfield, averageRightDef, averageMidDef, '
                               'averageLeftDef, averageRightAtt, averageMidAtt, averageLeftAtt, averageIndirectFreeKickDef, '
                               'averageIndirectFreeKickAtt, averageDef, averageAtt, experience, speechLevel)'
                               'values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'),
                               (match_data['matchId'], rating['teamId'], rating['averageMidfield'],
                                rating['averageRightDef'], rating['averageMidDef'], rating['averageLeftDef'],
                                rating['averageRightAtt'], rating['averageMidAtt'],
                                rating['averageLeftAtt'], rating['averageIndirectFreeKickDef'],
                                rating['averageIndirectFreeKickAtt'], rating['averageDef'],
                                rating['averageAtt'], rating['experience'], rating['speechLevel'],),)
        except Exception as err:
            logger.error(err)


    def insert_avg_sectors_data(self, cursor, match_data):
        try:
            avg_sectors_data = match_data['analysis']['avg']['sectors']
            for avg_sector in avg_sectors_data:
                cursor.execute(self.check_param_style(sql='insert into avg_analysis (matchId, avg_sectors_sectorId, avg_sectors_homeRating, avg_sectors_awayRating, '
                               'avg_sectors_homeProbability, avg_sectors_awayProbability) '
                               'values(%s, %s, %s, %s, %s, %s)'),
                               (match_data['matchId'], avg_sector['sectorId'], avg_sector['homeRating'], avg_sector['awayRating'],
                                avg_sector['homeProbability'], avg_sector['awayProbability'],),)
        except Exception as err:
            logger.error(err)


    def insert_avg_players_data(self, cursor, home, match_data):
        try:
            if home is True:
                avg_players_data = match_data['analysis']['avg']['homePlayers']
            else:
                avg_players_data = match_data['analysis']['avg']['awayPlayers']

            for avg_player in avg_players_data:
                cursor.execute(self.check_param_style(sql='insert into avg_analysis_player (matchId, home_player, avg_player_playerId, '
                               'avg_player_stars, avg_player_positionId, avg_player_behaviour, avg_player_isCaptain, '
                               'avg_player_isKicker, avg_player_stamina) '
                               'values (%s, %s, %s, %s, %s, %s, %s, %s, %s)'),
                               (match_data['matchId'], home, avg_player['playerId'],
                                avg_player['stars'], avg_player['positionId'], avg_player['behaviour'],
                                avg_player['isCaptain'], avg_player['isKicker'],
                                avg_player['stamina'],),)
        except Exception as err:
            logger.error(err)



    def insert_referees_data(self, cursor, match_data):
        try:
            referees_data = match_data['referees']
            for referee in referees_data:
                cursor.execute(self.check_param_style(sql='insert into referee (matchId, playerId, firstName, nickName, lastName, teamId, teamName, '
                               'gentleness, aggressiveness, honesty, leagueId, leagueName) '
                               'values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'),
                               (match_data['matchId'], referee['playerId'],
                                referee['firstName'],
                                referee['nickName'],
                                referee['lastName'],
                                referee['teamId'],
                                referee['teamName'],
                                referee['gentleness'],
                                referee['aggressiveness'],
                                referee['honesty'],
                                referee['leagueId'],
                                referee['leagueName'],),)
        except Exception as err:
            logger.error(err)


    def check_param_style(self, sql:str) -> str:
        if self.driver == 'sqlite3':
            return sql.replace("%s", "?")
        return sql


    def get_auto_start_match(self, max:bool):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            if max:
                match_id = cursor.execute("SELECT max(matchId) FROM match").fetchone()[0]
            else:
                match_id = cursor.execute("SELECT min(matchId) FROM match").fetchone()[0]
            cursor.close()
            return match_id

