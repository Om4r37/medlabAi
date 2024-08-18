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

STATS = (
    "current_appointments",
    "total_results",
    "users_count",
    "male",
    "female",
    "married",
    "current_smokers",
    "former_smokers",
    "never_smokers",
    "heart_disease",
    "exng",
    "rural",
    "urban",
    "never_worked",
    "private_work",
    "self_employed",
    "gov_work",
    "children",
    "ages_0_15",
    "ages_16_30",
    "ages_31_45",
    "ages_46_60",
    "ages_61_75",
    "ages_76_",
)


# flask config
class Config:
    SESSION_PERMANENT = False
    SESSION_TYPE = "filesystem"
