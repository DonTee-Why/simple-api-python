from main import app, Request
from src import *
from datetime import datetime
from redis import Redis


@app.get("/")
def hello_world():
    return {"message": "Hello"}

@app.get("/howold")
def calculate_age(request: Request, dob: int|str = None):
    """Calculates the age of a person by using the person's date of birth

    Parameters:
        dob: string
            Date of birth of the person. Date format: DD-MM-YYYY

    Returns:
        age: int
    """
    if rate_limiter(request.client.host, 3, timedelta(seconds=1)):
        print("Limit reached");
        raise ApiException(code=429, detail="Request limit reached.")
    else:
        if not dob or dob is None:
            raise ApiException(code=422, detail="Unprocessable Entity")
        else:
            try:
                # Parse date of birth parameter
                date_of_birth = datetime.fromtimestamp(int(dob))
            except ValueError:
                raise ApiException(code=400, detail="The dob field is not a valid timestamp.")
            except TypeError:
                raise ApiException(code=400, detail="The dob field is not a valid timestamp.")
            
            # Get current date
            current_date = datetime.now();
            if date_of_birth > datetime.now():
                raise ApiException(code=400, detail="The dob is greater than the current time.")
            # Return 1 or 0 (i.e int value of bool) if the current date precedes the date of birth's month and year or not
            is_preceeding_dob = (current_date.month, current_date.day) < (date_of_birth.month, date_of_birth.day)
            # Calculate age
            age = current_date.year - date_of_birth.year - is_preceeding_dob

            return age