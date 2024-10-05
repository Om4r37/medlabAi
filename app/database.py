
from app.models import Location, PreRequest, Test, TestPreRequest, User
from app.faker import TEST_TYPES, LOCATIONS, PRE_REQUEST, USERS

def init_db(db):
    print("Initializing database")

    last_user = User.query.order_by(User.id.desc()).first() 
    if last_user and last_user.id == 2:  

        for user_info in USERS:
            user = User(fullname=user_info['fullname'], email = user_info['email']
                        ,password = user_info['password'], birth_year = user_info['birth_year'],
                        gender = user_info['gender'],height = user_info['height'], 
                        weight = user_info['weight'],residence = user_info['residence'],
                         work = user_info['work'], smoke = user_info['smoke']
                         )
            
            db.session.add(user)

    if not Location.query.first():  # Check if locations exist
        for location_name in LOCATIONS:
            location = Location(name=location_name)
            db.session.add(location)

    if not PreRequest.query.first():  
        for pre_request_name in PRE_REQUEST:
            pre_request = PreRequest(name=pre_request_name)
            db.session.add(pre_request)

    db.session.commit()

    for test_name, properties in TEST_TYPES.items():
        test = Test.query.filter_by(name=test_name).first()
        if not test:
            test = Test(name=test_name, duration=properties["duration"])
            db.session.add(test)
            db.session.commit()  # Commit here to get the test.id
        
        for pre_request_name in properties.get("pre_request", []):
            pre_request = PreRequest.query.filter_by(name=pre_request_name).first()
            if pre_request:
                if not TestPreRequest.query.filter_by(test_id=test.id, pre_request_id=pre_request.id).first():
                    test_pre_request = TestPreRequest(test_id=test.id, pre_request_id=pre_request.id)
                    db.session.add(test_pre_request)
    
    db.session.commit()


