import re
from django.conf import settings
from decouple import config


def validate_phone(phone_number):
        pattern_uz = "^+998([- ])?(90|91|93|94|95|98|99|33|97|71)([- ])?(\d{3})([- ])?(\d{2})([- ])?(\d{2})$"
        pattern = "^\\+?\\d{1,4}?[-.\\s]?\\(?\\d{1,3}?\\)?[-.\\s]?\\d{1,4}[-.\\s]?\\d{1,4}[-.\\s]?\\d{1,9}$"
        return bool(re.match(pattern, phone_number))
    
def validate_email(email):
        pattern = r"^[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?$"
        return bool(re.match(pattern, email))


def validate_email_or_phone(input):
    if validate_email(input):
        return 'email'
    elif validate_phone(input):
        return 'phone'
    else:
        return None
    



# Twilio
from twilio.rest import Client


account_sid = settings.TWILIO_ACCOUNT_SID
auth_token = settings.TWILIO_AUTH_TOKEN
account_sid_conf = config('TWILIO_ACCOUNT_SID')
auth_token_conf = config('TWILIO_AUTH_TOKEN')


def send_sms(to_number, body):
    
    # Initialize Twilio client
    client = Client(account_sid, auth_token)

    # Send SMS
    message = client.messages.create(
        body=body,
        from_='+12513062962',
        to=to_number
    )

    return message.sid












