from cs50 import SQL
import os, sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import TEST_TYPES, LOCATIONS


def init():
    os.system("touch database.db")
    db = SQL("sqlite:///database.db")
    with open("schema.sql", "r") as file:
        for query in file.read().split(";")[:-1]:
            db.execute(query)

    for location in LOCATIONS:
        db.execute("INSERT INTO locations (name) VALUES (?);", location)

    for test, properties in TEST_TYPES.items():
        db.execute(
            "INSERT INTO tests (name, duration) VALUES (?, ?);",
            test,
            properties["duration"],
        )
        for prerequisite in properties["prerequisites"]:
            db.execute(
                "INSERT INTO prerequisites (test_id, name) VALUES (?, ?);",
                db.execute("SELECT id FROM tests WHERE name = ?;", test)[0]["id"],
                prerequisite,
            )


try:
    db = SQL("sqlite:///database.db")
except:
    init()
    db = SQL("sqlite:///database.db")
