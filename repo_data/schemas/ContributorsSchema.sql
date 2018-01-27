DROP TABLE if EXISTS Contributors;
CREATE TABLE Contributors (
  username text NOT NULL PRIMARY KEY ,
  rank integer NOT NULL ,
  number_solved integer NOT NULL
)