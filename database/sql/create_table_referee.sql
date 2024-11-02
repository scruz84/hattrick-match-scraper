CREATE TABLE referee (
    matchId  bigint references match(matchId) on delete cascade,
    playerId bigint,
    firstName TEXT,
    nickName TEXT,
    lastName TEXT,
    teamId bigint,
    teamName TEXT,
    gentleness bigint,
    aggressiveness bigint,
    honesty bigint,
    leagueId bigint,
    leagueName TEXT
);
