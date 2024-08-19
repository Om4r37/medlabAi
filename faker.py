#!/usr/bin/env python

from app.database import db
from random import randint
from config import STATS

for stat in STATS:
    db.execute("UPDATE stats SET value = ? WHERE name = ?;", randint(0, 800), stat)

db.execute("UPDATE stats SET value = 990 WHERE name = 'users_count';")
