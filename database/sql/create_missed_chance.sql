CREATE TABLE missed_chance (
    matchId  bigint references match(matchId) on delete cascade,
    playerId bigint,
    eventTypeId bigint,
    matchMinute bigint,
    matchMinuteSecond bigint,
    matchPart bigint,
    eventIndex bigint
);
