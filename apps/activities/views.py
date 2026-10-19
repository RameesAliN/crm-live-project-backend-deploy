from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from drf_spectacular.utils import extend_schema, OpenApiParameter

from .models import Note,Task
from .serializers import NoteSerializer,TaskSerializer


class NoteAccessMixin:
    permission_classes = [IsAuthenticated]
    serializer_class = NoteSerializer

    def get_queryset(self):
        queryset = Note.objects.select_related("lead", "company", "deal", "created_by" )

        lead_id = self.request.query_params.get("lead")
        company_id = self.request.query_params.get("company")
        deal_id = self.request.query_params.get("deal")

        if lead_id:
            queryset = queryset.filter(lead_id=lead_id)

        if company_id:
            queryset = queryset.filter(company_id=company_id)

        if deal_id:
            queryset = queryset.filter(deal_id=deal_id)

        return queryset.order_by("-created_at")


class NoteListCreateView(NoteAccessMixin,generics.ListCreateAPIView):
    #for parameter 
    @extend_schema(
        parameters=[
            OpenApiParameter(name="lead",type=int,location=OpenApiParameter.QUERY,required=False,),
            OpenApiParameter(name="company",type=int,location=OpenApiParameter.QUERY,required=False,),
            OpenApiParameter(name="deal",type=int,location=OpenApiParameter.QUERY,required=False,),])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class NoteDetailView(NoteAccessMixin,generics.RetrieveUpdateDestroyAPIView):
    pass




#task module
class TaskAccessMixin:
    permission_classes = [IsAuthenticated]
    serializer_class = TaskSerializer

    def get_queryset(self):
        queryset = Task.objects.select_related("lead","company","deal","assigned_to",)
        lead_id = self.request.query_params.get("lead")
        company_id = self.request.query_params.get("company")
        deal_id = self.request.query_params.get("deal")

        if lead_id:
            queryset = queryset.filter(lead_id=lead_id)

        if company_id:
            queryset = queryset.filter(company_id=company_id)

        if deal_id:
            queryset = queryset.filter(deal_id=deal_id)

        return queryset.order_by("-created_at")



class TaskListCreateView(TaskAccessMixin,generics.ListCreateAPIView):
    @extend_schema(
        parameters=[
            OpenApiParameter(name="lead",type=int,location=OpenApiParameter.QUERY,required=False,),
            OpenApiParameter(name="company",type=int,location=OpenApiParameter.QUERY,required=False,),
            OpenApiParameter(name="deal",type=int,location=OpenApiParameter.QUERY,required=False,),
        ])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class TaskDetailView(TaskAccessMixin,generics.RetrieveUpdateDestroyAPIView):
    pass
