from datetime import datetime, date

from django.core.exceptions import ValidationError
from django.utils.timezone import now, make_aware
from django.conf import settings


def validate_date_range(start_date, end_date):
    # Ensure dates are provided
    if not start_date or not end_date:
        raise ValidationError("Both start date and end date must be provided.")

    # Convert naive datetime objects to aware ones
    if not start_date.tzinfo:
        start_date = make_aware(start_date)
    if not end_date.tzinfo:
        end_date = make_aware(end_date)

    # Check if the inputs are of the correct type
    if not isinstance(start_date, (datetime, date)) or not isinstance(end_date, (datetime, date)):
        raise ValidationError("Invalid date format. Start date and end date must be datetime objects.")

    # Ensure end date is not in the future
    if end_date > now():
        raise ValidationError("End date cannot be in the future.")

    # Ensure start date is not after end date
    if start_date > end_date:
        raise ValidationError("Start date cannot be after the end date.")

    # Ensure end date is not before the default start date
    if end_date < make_aware(settings.START_DATE):
        raise ValidationError(f"End date cannot be before the configured start date: {settings.START_DATE}.")
