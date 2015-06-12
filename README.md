# Tournament application

This is a Python module which uses the PostgreSQL database to keep track of players and matches in a game tournament. The [Swiss system](https://en.wikipedia.org/wiki/Swiss-system_tournament) is used for pairing up players in each round.

## Requirements

- PostgreSQL
- Python (with `psycopg2` database adapter)

## Components

**1. Database schema**
  Contained in the `tournament.sql` file, this defines that tables and views.

**2. Python code to manage the tournament**
  Contained in the `tournament.py` file, this contains functions for each step in the tournament management process.

## Setting up

Create and configre PostgreSQL database running `\i tournament.sql` in `psql`. This creates the database, and configures the tables.

## Testing

Run `python tournament_test.py` to run the test suite, and confirm all tests are passing. If you see "Success!  All tests pass!", then all the tests are passing!

