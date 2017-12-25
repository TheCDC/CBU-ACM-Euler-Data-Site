CREATE TABLE
IF NOT EXISTS Contributors(
  username integer PRIMARY KEY,
  rank integer NOT NULL ,
  number_solved integer NOT NULL ,
)

CREATE TABLE
if NOT EXISTS Problems(
  problem_number INTEGER PRIMARY KEY,
  popularity integer NOT NULL,
  times_solved integer NOT NULL,
)