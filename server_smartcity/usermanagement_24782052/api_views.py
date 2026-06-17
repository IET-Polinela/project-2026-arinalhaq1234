from rest_framework import generics, permissions
from .models import CustomUser
from .serializers import RegisterSerializer
from drf_spectacular.utils import extend_schema

@extend_schema(exclude=True)
class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]