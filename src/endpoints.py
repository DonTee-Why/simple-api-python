from main import app
from src import *
from datetime import datetime


@app.get("/")
def read_root():
    return {"message": "Hello"}


@app.get("/howold")
def calculate_age(dob: str = None):
    """Calculates the age of a person by using the person's date of birth

    Parameters:
        dob: string
            Date of birth of the person. Date format: DD-MM-YYYY

    Returns:
        age: json
    """
    
    if dob is not None:
        try:
            # Parse date of birth parameter
            date_of_birth = datetime.strptime(dob, '%d-%m-%Y')
        except ValueError:
            raise ApiException(code=400, detail="The dob field is not a valid date format.")
        
        # Get current date
        current_date = datetime.now().date();

        # Return 1 (i.e int value of bool True) if the current date precedes the date of birth's month and year
        is_preceeding_dob = (current_date.month, current_date.day) < (date_of_birth.month, date_of_birth.day)
        # Calculate age
        age = current_date.year - date_of_birth.year - is_preceeding_dob

        return {"age": age}
    else:
        raise ApiException(code=422, detail="Unprocessable Entity")