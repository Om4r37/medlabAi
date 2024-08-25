#!/usr/bin/env python

from cs50 import SQL
from config import STATS

db = SQL("sqlite:///database.db")

for k, v in STATS.items():
    db.execute("UPDATE stats SET value = ? WHERE name = ?;", v, k)

with open("users.sql") as f:
    while line := f.readline():
        db.execute(line)

db._disconnect()
