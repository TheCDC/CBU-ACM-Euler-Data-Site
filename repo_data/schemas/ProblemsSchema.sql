DROP TABLE if EXISTS Problems;
CREATE TABLE Problems (
  id INTEGER PRIMARY KEY,
  problem_number INTEGER ,
  popularity integer NOT NULL,
  times_solved integer NOT NULL,
  who_solved integer NOT NULL
)