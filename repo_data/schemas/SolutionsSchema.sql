DROP TABLE if EXISTS Solutions;
CREATE TABLE Solutions (
  id INTEGER PRIMARY KEY,
  problem_number INTEGER NOT NULL,
  username text NOT NULL,
  FOREIGN KEY (problem_number) REFERENCES Problems(problem_number),
  FOREIGN KEY (username) REFERENCES Contributors(username)
)