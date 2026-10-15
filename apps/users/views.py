from django.shortcuts import render

from rest_framework import generics, permissions
from .serializers import RegisterSerializer, UserSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

# class ProfileView(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request):
#         user = request.user

#         return Response({
#             "id": user.id,
#             "first_name": user.first_name,
#             "last_name": user.last_name,
#             "email": user.email,
#             "phone": user.phone,
#             "company_name": user.company_name,
#             "industry_type": user.industry_type,
#             "country": user.country,
#             "role": user.role,
#         })
class ProfileView(APIView): 
    permission_classes = [IsAuthenticated] 
    def get(self, request): 
        serializer = UserSerializer(request.user)
        return Response(serializer.data)