-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

DROP DATABASE IF EXISTS tournament;

CREATE DATABASE tournament;

\c tournament;

CREATE TABLE players (
  id serial PRIMARY KEY,
  name text
);

CREATE TABLE matches (
  id serial PRIMARY KEY,
  p1 integer REFERENCES players(id),
  p2 integer REFERENCES players(id),
  winner integer REFERENCES players(id)
);

-- All player_ids from matches table, whether p1 or p2
CREATE VIEW all_player_matches AS
  SELECT p1 as player_id FROM matches UNION ALL SELECT p2 FROM matches;

-- id | matches_count
CREATE VIEW matches_per_player AS
 SELECT p.id, count(a.player_id) AS matches_count FROM players AS p LEFT JOIN all_player_matches AS a ON a.player_id = p.id GROUP BY p.id;

-- player_id | wins
CREATE VIEW wins_per_player AS
  SELECT p.id AS player_id, count(m.winner) AS wins FROM players AS p LEFT JOIN matches AS m ON m.winner = p.id GROUP BY p.id ORDER BY p.id;

-- Standings view with id | name | wins | matches
CREATE VIEW standings AS
  SELECT s.player_id AS id, p.name, s.wins, m.matches_count AS matches
    FROM wins_per_player AS s, players AS p, matches_per_player AS m
    WHERE p.id = s.player_id
    AND p.id = m.id
    ORDER BY s.wins DESC;
