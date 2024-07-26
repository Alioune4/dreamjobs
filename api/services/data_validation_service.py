from api.data_access.models import EmploymentTypeEnum, CategoryEnum, ApplicationStatusEnum


def validate_enum(enum_class, value):
    """ Validate if the value exists in the provided enum class. """
    for enum_value in enum_class:
        if enum_value.value == value:
            return True
    return False


def get_enum_value_from_string(enum_class, value):
    for enum_value in enum_class:
        if enum_value.value == value:
            return enum_value
    return None


def validate_job_post_data(data):
    """ Validate job post data. """
    required_fields = ['title', 'description', 'employment_type', 'category']

    errors = {}

    # Check for missing required fields
    for field in required_fields:
        if field not in data:
            errors[field] = 'This field is required.'

    # Validate employment_type
    if 'employment_type' in data:
        if not validate_enum(EmploymentTypeEnum, data['employment_type']):
            errors['employment_type'] = 'Invalid employment type.'

    # Validate category
    if 'category' in data:
        if not validate_enum(CategoryEnum, data['category']):
            errors['category'] = 'Invalid category.'

    return errors

def validate_job_post_update_data(data):
    """ Validate update data for job posts. """
    valid_fields = {'title': str, 'description': str, 'salary': int, 'location': str,
                    'employment_type': EmploymentTypeEnum, 'category': CategoryEnum}

    errors = {}

    for field, expected_type in valid_fields.items():
        if field in data:
            if expected_type in {EmploymentTypeEnum, CategoryEnum}:
                if not validate_enum(expected_type, data[field]):
                    errors[field] = f'Invalid {field}.'
            elif not isinstance(data[field], expected_type):
                errors[field] = f'{field} must be of type {expected_type.__name__}.'

    return errors



def validate_application_data(data):
    """ Validate application data. """
    required_fields = ['job_post_id', 'resume']

    errors = {}

    # Check for missing required fields
    for field in required_fields:
        if field not in data:
            errors[field] = 'This field is required.'

    return errors


def validate_application_update_data(data):
    """ Validate update data for applications. """
    valid_fields = {'resume': str, 'cover_letter': str, 'status': ApplicationStatusEnum}

    errors = {}

    for field, expected_type in valid_fields.items():
        if field in data:
            if expected_type == ApplicationStatusEnum:
                if not validate_enum(expected_type, data[field]):
                    errors[field] = f'Invalid {field}.'
            elif not isinstance(data[field], expected_type):
                errors[field] = f'{field} must be of type {expected_type.__name__}.'

    return errors


def update_job_post(job_post, data):
    """ Update a job post with the provided data. """
    valid_fields = {'title': str, 'description': str, 'salary': int, 'location': str,
                    'employment_type': EmploymentTypeEnum, 'category': CategoryEnum}

    for field, expected_type in valid_fields.items():
        if field in data:
            if expected_type in {EmploymentTypeEnum, CategoryEnum}:
                setattr(job_post, field, get_enum_value_from_string(expected_type, data[field]))
            else:
                setattr(job_post, field, data[field])

    return job_post
