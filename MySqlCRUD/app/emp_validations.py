from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from .models import *

def validate_employee_data(data):
    name = data.get('name')
    age = data.get('age')
    email = data.get('email')
    salary = data.get('salary')
    dept_name = data.get('dept_name')

    errors = {}

    # Validate name
    if not name:
        errors['name'] = 'Name is required.'

    # Validate age
    if not age:
        errors['age'] = 'Age is required.'
    elif not age.isdigit():
        errors['age'] = 'Age must be a valid number.'

    # Validate email
    if not email:
        errors['email'] = 'Email is required.'
    else:
        try:
            validate_email(email)
        except ValidationError:
            errors['email'] = 'Invalid email format.'

    # Validate salary
    if not salary:
        errors['salary'] = 'Salary is required.'
    elif not salary.isdigit():
        errors['salary'] = 'Salary must be a valid number.'

    # Validate department
    if not dept_name:
        errors['Department'] = 'Department is required.'
    elif not Department.objects.filter(name__iexact=dept_name).exists():
        errors['dept_name'] = 'Department does not exist.'

    return errors
