from api.data_access.models import EmploymentTypeEnum, CategoryEnum, ApplicationStatusEnum
from werkzeug.exceptions import BadRequest
import enum as python_enum

def validate_enum(enum_class, value):
    """ Validate if the value exists in the provided enum class. """
    if value not in {enum.value for enum in enum_class}:
        raise BadRequest(description='Value not in enum class')


def get_enum_value_from_string(enum_class, value):
    return enum_class(value)


def validate_fields(data, required_fields=None, enum_fields=None, field_types=None):
    """ Validate required fields, enum fields, and non enum field types. """
    if required_fields:
        for field in required_fields:
            if field not in data:
                raise BadRequest(description=f'{field} is required.')

    if enum_fields:
        for field, enum_class in enum_fields.items():
            if field in data:
                validate_enum(enum_class, data[field])

    if field_types:
        for field, expected_type in field_types.items():
            if not issubclass(expected_type, python_enum.Enum) and  field in data and not isinstance(data[field], expected_type):
                raise BadRequest(description=f'Expected type {expected_type.__name__} for {field}')


def validate_job_post_data(data, is_update=False):
    """ Validate job post data for create or update. """
    if not is_update:
        required_fields = ['title', 'description', 'employment_type', 'category']
    else:
        required_fields = None  # No required fields for update

    enum_fields = {'employment_type': EmploymentTypeEnum, 'category': CategoryEnum}
    field_types = {
        'title': str, 'description': str, 'salary': int, 'location': str,
        'employment_type': EmploymentTypeEnum, 'category': CategoryEnum
    }

    validate_fields(data, required_fields,
                    enum_fields if not is_update else {k: v for k, v in enum_fields.items() if k in data}, field_types)


def validate_application_data(data, is_update=False):
    """ Validate application data for create or update. """
    if not is_update:
        required_fields = ['job_post_id', 'resume']
    else:
        required_fields = None  # No required fields for update

    enum_fields = {'status': ApplicationStatusEnum}
    field_types = {'resume': str, 'cover_letter': str}

    validate_fields(data, required_fields,
                    enum_fields if not is_update else {k: v for k, v in enum_fields.items() if k in data}, field_types)


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
