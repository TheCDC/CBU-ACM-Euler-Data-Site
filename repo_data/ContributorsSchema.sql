DROP TABLE if EXISTS Contributors;
CREATE TABLE Contributors (
  id INTEGER PRIMARY KEY,
  username text NOT NULL ,
  rank integer NOT NULL ,
  problems_solved text NOT NULL
)