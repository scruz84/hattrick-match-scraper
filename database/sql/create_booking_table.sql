CREATE TABLE booking (
   matchId bigint references match(matchId) on delete cascade,
   playerId bigint,
   matchMinute bigint,
   matchMinuteSecond bigint,
   matchPart bigint,
   cardValue bigint,
   eventIndex bigint
);

--INSERT INTO mytable (playerId,matchMinute,matchMinuteSecond,matchPart,cardValue,eventIndex)
--VALUES
 --   (123857705,73,39,2,1,21);
