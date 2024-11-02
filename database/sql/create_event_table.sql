CREATE TABLE "event" (
    matchId bigint references match(matchId) on delete cascade,
    eventIndex bigint,
    eventType bigint,
    eventVariation bigint,
    matchMinute bigint,
    matchMinuteSecond bigint,
    matchPart bigint,
    eventText text,
    eventTextLive text NULL,
    subjectTeamId bigint,
    subjectPlayerId bigint,
    objectPlayerId bigint,
    originalEventIndex bigint,
    offsetSecond bigint
);

--INSERT INTO "mytable" ("eventIndex","eventType","eventVariation","matchMinute","matchMinuteSecond","matchPart","eventText","eventTextLive","subjectTeamId","subjectPlayerId","objectPlayerId","originalEventIndex","offsetSecond")
--VALUES
--    (0,31,5,0,0,0,'Los oscuros nubarrones pusieron a temblar a los 12000 espectadores presentes en [arena=1666435]fc kjærbæk Arena[/arena], aunque finalmente la lluvia no se presentó. [referee=404755174]张 (Zhang)  昌 (Chang)[/referee] fue el árbitro designado, junto a los asistentes [referee=467466951]Anderson Tezza[/referee] y [referee=428928518]Tobiasz Korczak[/referee].',NULL,12000,1666435,12000,0,0);
