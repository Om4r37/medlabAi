from cs50 import SQL
import os, sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import TEST_TYPES, LOCATIONS

db = SQL("sqlite:///database.db")


def init():
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


if __name__ == "__main__":
    init()
