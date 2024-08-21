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

STATS = {
    "current_appointments": 73,
    "total_results": 147,
    "users_count": 991,
    "male": 430,
    "female": 561,
    "married": 532,
    "current_smokers": 121,
    "former_smokers": 39,
    "never_smokers": 831,
    "heart_disease": 141,
    "exng": 238,
    "rural": 194,
    "urban": 797,
    "never_worked": 89,
    "private_work": 537,
    "self_employed": 123,
    "gov_work": 212,
    "children": 30,
    "ages_0_15": 37,
    "ages_16_30": 89,
    "ages_31_45": 123,
    "ages_46_60": 212,
    "ages_61_75": 202,
    "ages_76_": 318,
}


# flask config
class Config:
    SESSION_PERMANENT = False
    SESSION_TYPE = "filesystem"
