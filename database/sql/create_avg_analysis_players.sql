CREATE TABLE avg_analysis_player (
    matchId  bigint references match (matchId) on delete cascade,
    home_player boolean,
    avg_player_playerId bigint,
    avg_player_stars NUMERIC,
    avg_player_positionId bigint,
    avg_player_behaviour bigint,
    avg_player_isCaptain TEXT,
    avg_player_isKicker TEXT,
    avg_player_stamina NUMERIC
);
