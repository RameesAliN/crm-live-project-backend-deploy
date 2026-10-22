
from django.conf import settings
from twilio.rest import Client # type: ignore
from twilio.base.exceptions import TwilioRestException # type: ignore

from twilio.twiml.voice_response import VoiceResponse, Dial # pyright: ignore[reportMissingImports]




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








def create_bridge_call(agent_number, customer_number):
    try:
        client = Client(
            settings.TWILIO_ACCOUNT_SID,
            settings.TWILIO_AUTH_TOKEN,
        )

        response = VoiceResponse()
        dial = Dial(caller_id=settings.TWILIO_PHONE_NUMBER)
        dial.number(customer_number)
        response.append(dial)

        
        call = client.calls.create(
            to=agent_number,
            from_=settings.TWILIO_PHONE_NUMBER,
            twiml=str(response),
        )

        return {
            "call_sid": call.sid,
            "status": call.status,
            "agent_number": agent_number,
            "customer_number": customer_number,
        }

    except TwilioRestException as exc:
        print("Twilio error code:", exc.code)
        print("Twilio error message:", exc.msg)
        print("HTTP status:", exc.status)
        raise


