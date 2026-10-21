
from rest_framework.serializers import Serializer, CharField
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import CallActivity
from drf_spectacular.utils import extend_schema # type: ignore
from .serializers import CallActivitySerializer 
from .services import initiate_call

class TestTwilioCallSerializer(Serializer): 
    to_number = CharField( required=True, help_text="Destination phone number in international format, e.g. +971501234567", )



class TestTwilioCallView(APIView): 
    @extend_schema(
             request=TestTwilioCallSerializer, 
             responses={201: dict}, 
             description="Initiate a one-sided outbound call using Twilio.", )


    def post(self, request): 
        to_number = request.data.get("to_number") 
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
    
