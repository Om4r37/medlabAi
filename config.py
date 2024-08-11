OPENING_TIME = "09:00"
CLOSING_TIME = "22:00"
LOCATIONS = ("main lab", "secondary lab")
TEST_TYPES = {
    "diabetes": {
        "duration": 10,
        "prerequisites": ("pregnancies", "height", "weight", "birth_year"),
    },
    "stroke": {
        "duration": 20,
        "prerequisites": (
            "height",
            "weight",
            "birth_year",
            "heart_disease",
            "married",
            "work",
            "residence",
            "smoke",
        ),
    },
    "heart attack": {"duration": 30, "prerequisites": ("birth_year", "gender", "exng")},
    "heart failure": {
        "duration": 30,
        "prerequisites": ("birth_year", "gender", "smoke"),
    },
}


# flask config
class Config:
    SESSION_PERMANENT = False
    SESSION_TYPE = "filesystem"
