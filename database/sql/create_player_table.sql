--INSERT INTO mytable (playerId,sourcePlayerId,teamId,firstName,nickName,lastName,playerNumber,specialty,health,avatar)
--VALUES
--(123857689,123857689,1669795,'Dean','','Thackaberry',100,0,-1,'[{url:backgrounds/bg_blue.png,x:9,y:10},{url://res.hattrick.org/kits/1/1/1/2/body5.png,x:9,y:10},{url:faces/f4c.png,x:9,y:10},{url:eyes/e24a.png,x:23,y:16},{url:mouths/m13c.png,x:28,y:57},{url:noses/n15.png,x:20,y:25},{url:hair/f4h8e.png,x:9,y:10}]');

CREATE TABLE match_player (
   matchId  bigint references match(matchId) on delete cascade,
   playerId bigint,
   sourcePlayerId bigint,
   teamId bigint,
   firstName text,
   nickName text,
   lastName text,
   playerNumber bigint,
   specialty bigint,
   health bigint);
