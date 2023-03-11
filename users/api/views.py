from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated

from .serializers import RegisterSerializer


# Create your views here.
class RegisterView(APIView):
    
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        
        instance = {}

        if serializer.is_valid():
            account = serializer.save()

            instance['Response:'] = "User created Successfully!"
            instance['Username'] = account.username

            try:
                token = Token.objects.get(user=account)
                instance['token'] = token.key
            except:
                token = Token.objects.create(user=account)
                instance['token'] = token.key
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(instance, status=status.HTTP_201_CREATED)

class LogoutView(APIView):
    permission_classes = [AllowAny]


    def post(self, request):
        try:
            request.user.auth_token.delete()
            return Response({"success": ("Successfully logged out.")}, status=status.HTTP_200_OK)

        except (AttributeError):
            return Response({"error": "Something went wrong."})