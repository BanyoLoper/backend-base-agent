from django.contrib.auth import authenticate, login
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from .serializers import UserSerializer


@method_decorator(csrf_exempt, name='dispatch')
class RegisterView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            login(request, user) # Iniciamos sesión tras registro
            return Response({"message": "Usuario y Agente creados"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@method_decorator(csrf_exempt, name='dispatch')
class LoginView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(request, username=email, password=password)
        if user:
            login(request, user)
            return Response({"message": "Login exitoso"})
        return Response({"error": "Credenciales inválidas"}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['GET'])
def check_auth(request):
    print(f"DEBUG Check Auth: Usuario={request.user}, Autenticado={request.user.is_authenticated}")
    if request.user.is_authenticated:
        return Response({
            "isLoggedIn": True,
            "user": UserSerializer(request.user).data
        })
    return Response({"isLoggedIn": False}, status=200)
