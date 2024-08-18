#!/usr/bin/env python

from app.database import db
from random import randint
from config import STATS

for stat in STATS:
    db.execute("UPDATE stats SET value = ? WHERE name = ?;", randint(0, 1000), stat)
