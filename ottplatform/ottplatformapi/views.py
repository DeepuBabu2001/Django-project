from rest_framework.decorators import api_view , permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password
from rest_framework import status
from moviestore.models import AdminLogin,MovieStore,Plan
from .serializer import UserSerializer,MovieSerializer,PlanSerializer
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from django.shortcuts import get_object_or_404




@api_view(["POST"])
@permission_classes([AllowAny])
def Ott_Signup(request):
    serializer = UserSerializer(data=request.data)

    if serializer.is_valid():
        user_data = serializer.validated_data

        if AdminLogin.objects.filter(email=user_data['email']).exists():
            return Response({'errors': {'email': 'Email already exists'}}, status=status.HTTP_400_BAD_REQUEST)

        user = serializer.save()
        user.password = make_password(user_data['password'])
        user.save()
        return Response({'message': 'You have successfully signed up'}, status=status.HTTP_201_CREATED)

    return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)



@csrf_exempt
@api_view(["POST"])
@permission_classes([AllowAny])
def Login(request):
    username = request.data.get("email")
    password = request.data.get("password")
    
    if not username or not password:
        return Response({'error': 'Please provide both username and password'}, status=status.HTTP_400_BAD_REQUEST)
    
    user = authenticate(username=username, password=password)
    
    if not user:
        return Response({'error': 'Invalid Credentials'}, status=status.HTTP_404_NOT_FOUND)
    
    token, _ = Token.objects.get_or_create(user=user)
    
    return Response({'token': token.key}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes((AllowAny,))
def List_Movie(request):
    movies = MovieStore.objects.all()
    serializer = MovieSerializer(movies, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([AllowAny])
def movie_view(request, id):
    print("movie_view")
    print(id)
    movie = get_object_or_404(MovieStore, pk=id)
    serializer = MovieSerializer(movie)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes((AllowAny,))
def List_Plan(request):
    plans = Plan.objects.all()
    serializer = PlanSerializer(plans, many=True)
    return Response(serializer.data)


