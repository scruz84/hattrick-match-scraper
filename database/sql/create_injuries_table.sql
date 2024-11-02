CREATE TABLE injury (
    matchId  bigint references match(matchId) on delete cascade,
    playerId bigint,
    matchMinute bigint,
    matchMinuteSecond bigint,
    matchPart bigint,
    injuryValue bigint,
    eventIndex bigint
);
