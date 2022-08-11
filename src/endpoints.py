from fastapi import Request
from main import app
from src import rate_limiter
from datetime import datetime, timedelta


@app.get("/")
def hello_world():
    return {"message": "Hello"}

@app.get("/howold")
def calculate_age(request: Request, dob: int|str):
    """Calculates the age of a person by using the person's date of birth

    Parameters:
        dob: string
            Date of birth of the person. Date format: DD-MM-YYYY

    Returns:
        age: int
    """
    if rate_limiter(request.client.host, 3, timedelta(seconds=1)):
        return 429;
    else:
        if not dob or dob is None:
            return 422;
        else:
            try:
                # Get the datetime object for the timestamp
                date_of_birth = datetime(1970, 1, 1, 0, 0, 0) + timedelta(microseconds=dob)
            except Exception:
                return 422
            # Get the current date
            current_date = datetime.now();

            if(date_of_birth > current_date):
                return 400
                
            # Return 1 or 0 (i.e int value of bool) if the current date precedes the date of birth's month and year or not
            is_preceeding_dob = (current_date.month, current_date.day) < (date_of_birth.month, date_of_birth.day)

            # Calculate age
            age = current_date.year - date_of_birth.year - is_preceeding_dob

            return age
