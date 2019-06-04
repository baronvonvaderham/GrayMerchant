import re

from django.core.exceptions import ValidationError


class ZipCodeValidator:
    """
    Creates a validator for zip code fields
    """
    US_POSTAL_CODE_REGEX = re.compile(r'^\d{5}(-?\d{4})?$')

    def __init__(self, zip_code):
        if not self.US_POSTAL_CODE_REGEX.match(zip_code):
            raise ValidationError("Entered value is not a valid US Zip Code")
