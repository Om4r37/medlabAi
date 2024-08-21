#!/usr/bin/env python

from cs50 import SQL
from random import randint
from config import STATS

db = SQL("sqlite:///database.db")

for k, v in STATS.items():
    db.execute("UPDATE stats SET value = ? WHERE name = ?;", v, k)

db._disconnect()
