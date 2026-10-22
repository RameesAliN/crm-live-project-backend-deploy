
from django.http import HttpResponse
from rest_framework.serializers import Serializer, CharField
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from .models import CallActivity
from twilio.twiml.voice_response import VoiceResponse  # type: ignore
from drf_spectacular.utils import extend_schema # type: ignore
from .serializers import CallActivitySerializer 
from .services import initiate_call,create_bridge_call


def twiml_voice_view(request): 
    response = VoiceResponse() 
    response.say( "Hello! This is a call from your CRM system." \
    " " "Thank you for your time. Goodbye.", voice="alice", language="en-US",
      ) 
    response.hangup() 
    return HttpResponse( str(response), content_type="text/xml", )

class TestTwilioCallSerializer(Serializer): 
    to_number = CharField( required=True, help_text="Destination phone number in international format, e.g. +971501234567", )

class BridgeCallSerializer(Serializer):
    agent_number = CharField(
        required=True,
        help_text="CRM agent phone number in international format, e.g. +971501234567",
    )

    customer_number = CharField(
        required=True,
        help_text="Customer phone number in international format, e.g. +971551234567",
    )



class MakeBridgeCallView(APIView):

    @extend_schema( request=BridgeCallSerializer, responses={201: dict}, description="Initiate a bridge call between a CRM agent and a customer.", )

    def post(self, request):

        serializer = BridgeCallSerializer(data=request.data) 
        serializer.is_valid(raise_exception=True) 
        agent_number = serializer.validated_data["agent_number"]
        customer_number = serializer.validated_data["customer_number"]
        if not agent_number or not customer_number:
            return Response(
                {
                    "error": "agent_number and customer_number are required"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:

            call = create_bridge_call(
                agent_number,
                customer_number,
            )

            return Response(
                {
                    "message": "Bridge call initiated successfully",
                    "call_sid": call["call_sid"],
                    "status": call["status"],
                    "agent_number": call["agent_number"],
                    "customer_number": call["customer_number"],
                },
                status=status.HTTP_201_CREATED,
            )

        except Exception as e:

            return Response(
                {
                    "error": str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class MakeCallView(APIView):
    @extend_schema( request=TestTwilioCallSerializer, responses={201: dict}, description="Initiate a one-way test call using Twilio.", )
    def post(self, request): 
        serializer = TestTwilioCallSerializer(data=request.data) 
        serializer.is_valid(raise_exception=True) 
        to_number = serializer.validated_data["to_number"]
        if not to_number: 
            return Response( 
                {"error": "to_number is required."},
                 status=status.HTTP_400_BAD_REQUEST,
                   ) 
        try: 
            call = initiate_call(to_number) 
            return Response( { "message": "Call initiated successfully.", **call, },
                             status=status.HTTP_201_CREATED,
                           ) 
        except Exception as exc:
            return Response( {"error": str(exc)}, 
                 status=status.HTTP_400_BAD_REQUEST, 
            )


class CallActivityListCreateView(generics.ListCreateAPIView):
    serializer_class = CallActivitySerializer

    def get_queryset(self):
        queryset = CallActivity.objects.select_related(
            "lead",
            "company",
            "deal",
            "ticket",
            "created_by",
        ).all()


        lead_id = self.request.query_params.get("lead")
        company_id = self.request.query_params.get("company")
        deal_id = self.request.query_params.get("deal")
        ticket_id = self.request.query_params.get("ticket")

        if lead_id:
            queryset = queryset.filter(lead_id=lead_id)

        if company_id:
            queryset = queryset.filter(company_id=company_id)

        if deal_id:
            queryset = queryset.filter(deal_id=deal_id)

        if ticket_id:
            queryset = queryset.filter(ticket_id=ticket_id)

        return queryset

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class CallActivityDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CallActivity.objects.select_related(
        "lead",
        "company",
        "deal",
        "ticket",
        "created_by",
    ).all()

    serializer_class = CallActivitySerializer
    
