OPENING_TIME = "09:00"
CLOSING_TIME = "22:00"
LOCATIONS = ("main lab", "secondary lab")
TEST_TYPES = {"diabetes": 10, "stroke": 20, "heart attack": 30, "heart failure": 30}


# flask config
class Config:
    SESSION_PERMANENT = False
    SESSION_TYPE = "filesystem"
