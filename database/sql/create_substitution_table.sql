CREATE TABLE substitution (
    matchId  bigint references match(matchId) on delete cascade,
    outPlayerId bigint,
    inPlayerId bigint,
    matchMinute bigint,
    matchMinuteSecond bigint,
    matchPart bigint,
    orderType bigint,
    eventIndex bigint,
    outPositionId bigint,
    inPositionId bigint,
    outBehaviour bigint,
    inBehaviour bigint,
    oldFormation TEXT,
    newFormation TEXT
);
