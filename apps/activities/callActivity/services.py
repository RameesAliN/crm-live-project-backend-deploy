
from django.conf import settings
from twilio.rest import Client # type: ignore
from twilio.base.exceptions import TwilioRestException # type: ignore


def initiate_call(to_number):
    try:
        client = Client(
            settings.TWILIO_ACCOUNT_SID,
            settings.TWILIO_AUTH_TOKEN,
        )

        call = client.calls.create(
            to=to_number,
            from_=settings.TWILIO_PHONE_NUMBER,
            url="https://demo.twilio.com/docs/voice.xml",
           

        )

        return {
            "call_sid": call.sid,
            "status": call.status,
            "to": call.to,
            "from": settings.TWILIO_PHONE_NUMBER,
        }
    except TwilioRestException as exc:
        print("Twilio error code:", exc.code)
        print("Twilio error message:", exc.msg)
        print("HTTP status:", exc.status)
        raise



