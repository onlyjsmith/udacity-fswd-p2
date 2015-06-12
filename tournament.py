#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def delete(table):
    """Execute the given DELETE query

    This is a tiny bit DRYer than repeating in both function definitions
    """
    query = ('DELETE FROM %s;' % table)
    conn = connect()
    c = conn.cursor()
    c.execute(query)
    conn.commit()
    conn.close()
    return


def deleteMatches():
    """Remove all the match records from the database."""
    return delete('matches')


def deletePlayers():
    """Remove all the player records from the database."""
    return delete('players')


def countPlayers():
    """Returns the number of players currently registered."""
    query = "SELECT count(*) AS count FROM players;"

    conn = connect()
    c = conn.cursor()
    c.execute(query)
    rows = c.fetchone()
    c.close()
    conn.close()
    return rows[0]


def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Sanitizes input to prevent SQL injection.

    Args:
      name: the player's full name (need not be unique).
    """

    conn = connect()
    c = conn.cursor()
    c.execute("INSERT INTO players (name) VALUES(%s)", (name,))
    conn.commit()
    conn.close()
    return


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or
    a player tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    query = "SELECT * FROM standings;"

    conn = connect()
    c = conn.cursor()
    c.execute(query)
    rows = c.fetchall()
    c.close()
    conn.close()
    return rows


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Sanitizes input to prevent SQL injection.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    conn = connect()
    c = conn.cursor()
    c.execute("INSERT INTO matches (p1, p2, winner) "
              "VALUES(%s,%s,%s)", (winner, loser, winner))
    conn.commit()
    conn.close()
    return


def swissPairings():
    """Returns a list of pairs of players for the next round of a match.

    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.

    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    standings = playerStandings()
    output = []
    # Combine every two elements from the array of playerStandings,
    # and extract the required fields
    for i, k in zip(standings[0::2], standings[1::2]):
        output.append(tuple([i[0], i[1], k[0], k[1]]))
    return output
