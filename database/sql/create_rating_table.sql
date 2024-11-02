CREATE TABLE rating (
    matchId  bigint references match(matchId) on delete cascade,
    teamId bigint,
    averageMidfield bigint,
    averageRightDef bigint,
    averageMidDef bigint,
    averageLeftDef bigint,
    averageRightAtt bigint,
    averageMidAtt bigint,
    averageLeftAtt bigint,
    averageIndirectFreeKickDef bigint,
    averageIndirectFreeKickAtt bigint,
    averageDef bigint,
    averageAtt bigint,
    experience bigint,
    speechLevel bigint
);
