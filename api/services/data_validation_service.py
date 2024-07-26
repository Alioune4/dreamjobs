from api.data_access.models import EmploymentTypeEnum, CategoryEnum, ApplicationStatusEnum
from werkzeug.exceptions import BadRequest

def validate_enum(enum_class, value):
    """ Validate if the value exists in the provided enum class. """
    if value not in {enum.value for enum in enum_class}:
        raise BadRequest(description='Value not in enum class')


def get_enum_value_from_string(enum_class, value):
    return enum_class(value)


def validate_required_fields(data, required_fields):
    for field in required_fields:
        if field not in data:
            raise BadRequest(description=f'{field} is required.')


def validate_enum_fields(data, enum_fields):
    for field, enum_class in enum_fields.items():
        if field in data:
            validate_enum(enum_class, data[field])


def validate_field_types(data, field_types):
    for field, expected_type in field_types.items():
        if field in data and not isinstance(data[field], expected_type):
            raise BadRequest(description=f'Expected type {expected_type.__name__} for {field}')


def validate_job_post_data(data):
    """ Validate job post data. """
    required_fields = ['title', 'description', 'employment_type', 'category']
    enum_fields = {'employment_type': EmploymentTypeEnum, 'category': CategoryEnum}

    validate_required_fields(data, required_fields)
    validate_enum_fields(data, enum_fields)


def validate_job_post_update_data(data):
    """ Validate update data for job posts. """
    valid_fields = {'title': str, 'description': str, 'salary': int, 'location': str,
                    'employment_type': EmploymentTypeEnum, 'category': CategoryEnum}

    enum_fields = {field: enum_class for field, enum_class in valid_fields.items() if enum_class in {EmploymentTypeEnum, CategoryEnum}}
    non_enum_fields = {field: field_type for field, field_type in valid_fields.items() if field_type not in {EmploymentTypeEnum, CategoryEnum}}

    validate_enum_fields(data, enum_fields)
    validate_field_types(data, non_enum_fields)


def validate_application_data(data):
    """ Validate application data. """
    required_fields = ['job_post_id', 'resume']
    validate_required_fields(data, required_fields)


def validate_application_update_data(data):
    """ Validate update data for applications. """
    valid_fields = {'resume': str, 'cover_letter': str, 'status': ApplicationStatusEnum}

    enum_fields = {field: enum_class for field, enum_class in valid_fields.items() if enum_class == ApplicationStatusEnum}
    non_enum_fields = {field: field_type for field, field_type in valid_fields.items() if field_type != ApplicationStatusEnum}

    validate_enum_fields(data, enum_fields)
    validate_field_types(data, non_enum_fields)


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
