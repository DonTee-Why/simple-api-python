from main import app, Request
from src import *
from datetime import datetime
from redis import Redis

r = Redis(host='127.0.0.1', port=6379, db=0)

@app.get("/")
def read_root():
    return {"message": "Hello"}

@app.get("/howold")
def calculate_age(request: Request, dob: str = None):
    """Calculates the age of a person by using the person's date of birth

    Parameters:
        dob: string
            Date of birth of the person. Date format: DD-MM-YYYY

    Returns:
        age: json
    """
    if rate_limiter(r, request.client.host, 3, timedelta(seconds=1)):
        raise ApiException(code=429, detail="Request limit reached.")

    if not dob or dob is None:
        raise ApiException(code=422, detail="Unprocessable Entity")
    else:
        try:
            # Parse date of birth parameter
            date_of_birth = datetime.strptime(dob, '%d-%m-%Y')
        except ValueError:
            raise ApiException(code=400, detail="The dob field is not a valid date format.")
        
        # Get current date
        current_date = datetime.now().date();

        # Return 1 or 0 (i.e int value of bool) if the current date precedes the date of birth's month and year or not
        is_preceeding_dob = (current_date.month, current_date.day) < (date_of_birth.month, date_of_birth.day)
        # Calculate age
        age = current_date.year - date_of_birth.year - is_preceeding_dob

        return {age}