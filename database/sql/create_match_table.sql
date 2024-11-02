CREATE TABLE match (
   matchId bigint primary key,
   sourceSystem text,
   matchType bigint,
   matchSpeed bigint,
   leagueId bigint,
   leagueName text,
   lluId bigint,
   lluName text,
   cupId bigint,
   cupName text,
   cupLevel bigint,
   cupLevelIndex bigint,
   tournamentId bigint,
   tournamentTypeId bigint,
   specialTournamentTypeId bigint,
   tournamentName text NULL,
   federationId bigint,
   federationName text NULL,
   homeTeamId bigint,
   awayTeamId bigint,
   homeTeamIdDB bigint,
   awayTeamIdDB bigint,
   homeIsBot boolean,
   awayIsBot boolean,
   homeMotherTeamId bigint,
   awayMotherTeamId bigint,
   homeTeamName text,
   awayTeamName text,
   homeShortTeamName text,
   awayShortTeamName text,
   homeGoals bigint,
   awayGoals bigint,
   homeStatement text,
   awayStatement text,
   isWalkover boolean,
   homeNrOfChances_left bigint,
   homeNrOfChances_middle bigint,
   homeNrOfChances_right bigint,
   homeNrOfChances_other bigint,
   homeNrOfChances_specialEvents bigint,
   homeNrOfChances_leftGoals bigint,
   homeNrOfChances_middleGoals bigint,
   homeNrOfChances_rightGoals bigint,
   homeNrOfChances_otherGoals bigint,
   homeNrOfChances_specialEventsGoals bigint,
   awayNrOfChances_left bigint,
   awayNrOfChances_middle bigint,
   awayNrOfChances_right bigint,
   awayNrOfChances_other bigint,
   awayNrOfChances_specialEvents bigint,
   awayNrOfChances_leftGoals bigint,
   awayNrOfChances_middleGoals bigint,
   awayNrOfChances_rightGoals bigint,
   awayNrOfChances_otherGoals bigint,
   awayNrOfChances_specialEventsGoals bigint,
   matchDate text,
   matchRound bigint,
   matchRoundsLeft bigint,
   season bigint,
   arenaTeamId bigint,
   arenaId bigint,
   arenaName text,
   arenaCapacity bigint,
   seatsStanding bigint,
   seatsPlain bigint,
   seatsPlus bigint,
   seatsBoxed bigint,
   isFinished boolean,
   weather bigint,
   homeTacticType bigint,
   awayTacticType bigint,
   homeTacticSkill bigint,
   awayTacticSkill bigint,
   homeCoachModifier bigint,
   awayCoachModifier bigint,
   homeLogoUrl text,
   awayLogoUrl text NULL,
   homeShirtUrl text,
   awayShirtUrl text,
   homeKitId bigint,
   awayKitId bigint,
   homeGoalKeeperKitId bigint,
   awayGoalKeeperKitId bigint,
   isMatchOrderSet boolean,
   expectedResult text NULL,
   soldSeatsStanding bigint,
   soldSeatsPlain bigint,
   soldSeatsPlus bigint,
   soldSeatsBoxed bigint,
   possessionFirstHalf bigint,
   possessionSecondHalf bigint,
   matchSecond bigint,
   halftimeBreak bigint,
   overtimeBreak bigint,
   addedMinutes bigint,
   nextEventInSeconds bigint,
   isArchive boolean,
   chatChannelId text NULL,
   chatTitle text NULL,
   pimp text NULL,
   aggregatedScore text NULL,
   shouldHideSquadAndStatus boolean,
   eggHunt text NULL,
   memorialEvent text
);