CREATE TABLE avg_analysis (
    matchId  bigint references match(matchId) on delete cascade,
    avg_sectors_sectorId bigint,
    avg_sectors_homeRating bigint,
    avg_sectors_awayRating bigint,
    avg_sectors_homeProbability bigint,
    avg_sectors_awayProbability bigint
);
