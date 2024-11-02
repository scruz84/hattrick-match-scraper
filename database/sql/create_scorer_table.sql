CREATE TABLE scorer (
    matchId bigint references match(matchId) on delete cascade,
    playerId bigint,
    matchMinute bigint,
    matchMinuteSecond bigint,
    matchPart bigint,
    homeGoals bigint,
    awayGoals bigint,
    eventIndex bigint
);

--INSERT INTO mytable (playerId,matchMinute,matchMinuteSecond,matchPart,homeGoals,awayGoals,eventIndex)
--VALUES
 --   (218304429,44,34,1,1,0,11);
