from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Student
from .serializers import StudentSerializer,LoginSerializer
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
# Create your views here.
class StudentApi(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        queryset=Student.objects.all()
        serializer=StudentSerializer(queryset,many=True)
        return Response({
            "status":True,
            "data":serializer.data
        })
    
class LoginApi(APIView):
    def post(self,request):
        data=request.data
        serializer=LoginSerializer(data=data)
        if not serializer.is_valid():
            return Response({
            "status":False,
            "data":serializer.errors
        })
        username=serializer.data['username']
        password=serializer.data['password']
        user_obj=authenticate(username=username,password=password)
        if user_obj:
            #This line is used to either get an existing token or create a new one for a user.
            #What Token.objects.get_or_create() does:
            #It tries to find a token for the given user.# If it exists, it returns that token.If it doesn't exist, it creates a new token for the user and returns it.
            # <Token: 05532483dbccff8de289ed59cee67786d3be8d34>
            #so token.key returns 05532483dbccff8de289ed59cee67786d3be8d34
            token,created=Token.objects.get_or_create(user=user_obj)
            return Response({
                "status":True,
                "token":token.key
            })
        
        return Response({
            "status":False,
            "data":{},
            "message":"Invalid credentails"
        })
        


