#!/usr/bin/env python
from cs50 import SQL
from random import randint
from config import STATS

db = SQL("sqlite:///database.db")

for stat in STATS:
    db.execute("UPDATE stats SET value = ? WHERE name = ?;", randint(0, 800), stat)

db.execute("UPDATE stats SET value = 990 WHERE name = 'users_count';")
db._disconnect()
