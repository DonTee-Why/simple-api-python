from time import time
from main import app, Request
from src import *
from datetime import datetime, timedelta
from time import time
from redis import Redis


@app.get("/")
def hello_world():
    return {"message": "Hello"}

@app.get("/howold")
def calculate_age(request: Request, dob: timedelta):
    """Calculates the age of a person by using the person's date of birth

    Parameters:
        dob: timestamp
            Date of birth of the person. Date format: DD-MM-YYYY

    Returns:
        age: int
    """
    if rate_limiter(request.client.host, 3, timedelta(seconds=1)):
        return 429;
    else:
        if not dob or dob is None:
            return 422
            # raise ApiException(code=422, detail="Unprocessable Entity")
        else:
            # print("Date of birth: ", dob)
            # Parse date of birth parameter
            date_of_birth = check_timestamp(dob)
            
            # Get current date
            current_date = datetime.now();
            if date_of_birth > datetime.now():
                return 400
                # raise ApiException(code=400, detail="The dob is greater than the current time.")

            # Return 1 or 0 (i.e int value of bool) if the current date precedes the date of birth's month and year or not
            is_preceeding_dob = (current_date.month, current_date.day) < (date_of_birth.month, date_of_birth.day)

            # Calculate age
            age = current_date.year - date_of_birth.year - is_preceeding_dob

            return age

def check_timestamp(dob: timedelta):
    try:
        # Check if the timestamp is in seconds or milliseconds and returns the apprpriate timestamp
        new_dob = datetime(1970, 1, 1, 0, 0, 0) + dob/1000
        return new_dob
    except Exception:
        # print("Invalid Input")
        # print("The dob field is not a valid timestamp.", dob)
        # raise ApiException(code=400, detail="The dob field is not a valid timestamp.")
        return 400