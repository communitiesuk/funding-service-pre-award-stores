from flask_wtf import FlaskForm


class DataError(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message


class DataValidationError(DataError):
    def __init__(self, message, schema_field_name=None):
        super(DataValidationError, self).__init__(message)
        self.schema_field_name = schema_field_name


def attach_validation_error_to_form(form: FlaskForm, error: DataValidationError):
    if error.schema_field_name is not None:
        getattr(form, error.schema_field_name).errors.append(error.message)
    else:
        form.form_errors.append(error.message)
