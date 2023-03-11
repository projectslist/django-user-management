from django.shortcuts import render

from rest_framework.views import APIView

from .serializers import UserSerializer,UserProfileUpdateSerializer

from rest_framework.response import Response

from .models import User

from rest_framework.exceptions import AuthenticationFailed

from rest_framework_simplejwt.tokens import RefreshToken

from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser

#Updating user details
from rest_framework.decorators import permission_classes, authentication_classes
from datetime import datetime
import base64
from django.core.files.base import ContentFile
from rest_framework import status
from django.contrib.auth.hashers import make_password
import os
from django.core.files.storage import default_storage


#for prediction
from joblib import load # pip install joblib
from sklearn.datasets import load_iris # pip install scikit-learn


# Create your views here.
# APIView has get and post function

class RegisterView(APIView):

    def post(self, request): # this is for user registration
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True) # Validating data and raising an exception
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)



class LoginView(APIView):
    def post(self,request):
        email = request.data['email']
        password = request.data['password']

        user = User.objects.filter(email=email).first() # Finding unique user

        if user is None:
            raise AuthenticationFailed('User not found')

        if not user.check_password(password): # check_password is provided by Django
            raise AuthenticationFailed('Incorrect password')

        refresh_token = RefreshToken.for_user(user)
        access_token = str(refresh_token.access_token)
        fresh_token = str(refresh_token)




        response = Response()


        response.data = {
            'access_token': access_token,
            'refresh_token': fresh_token,
            'email': user.email
        }

        return response


class UserView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer


    def get(self, request, format=None):
        user_profile = request.user
        serializer = self.serializer_class(user_profile)
        return Response({'user': serializer.data})


class ProfileUpdateView(APIView):

    permission_classes = [IsAuthenticated, IsAdminUser]

    def patch(self, request, email):
        user = User.objects.get(email=email)

        serializer = UserProfileUpdateSerializer(user, data=request.data, partial=True)

        if serializer.is_valid():

            image_b64 = request.data.get('profile_image')

            if len(request.data.get('profile_image', '')) > 200:

                format, *imgstr_parts = image_b64.split(';base64,')
                imgstr = ';base64,'.join(imgstr_parts)
                padding = len(imgstr) % 4
                if padding > 0:
                    imgstr += "=" * (4 - padding)
                ext = format.split('/')[-1] if len(format.split('/')) > 1 else ''
                now = datetime.now()
                current_time = now.strftime("%Y%m%d%H%M%S")
                data = ContentFile(base64.b64decode(imgstr), name='temp-' + current_time + '.' + ext)
                serializer.validated_data['profile_image'] = data

                # Delete old profile image if it exists
                if user.profile_image:
                    if os.path.isfile(user.profile_image.path):
                        default_storage.delete(user.profile_image.path)
            else:
                # Keep existing profile image if not uploaded
                if user.profile_image:
                    serializer.validated_data['profile_image'] = user.profile_image
                else:
                    serializer.validated_data.pop('profile_image', None)

            password = request.data.get('password')
            if password:
                serializer.validated_data['password'] = make_password(password)

            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, email):
        return self.patch(request, email)










class UsersListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)


class AddUser(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def post(self, request, format=None):
        print(request.data['is_active'])
        print(request.data['first_name'])

        image_b64 = request.data['profile_image']  # This is your base64 string image
        # print(image_b64)

        format, imgstr = image_b64.split(';base64,')
        ext = format.split('/')[-1]
        now = datetime.now()

        current_time = now.strftime("%Y%m%d%H%M%S")
        print(current_time)
        data = ContentFile(base64.b64decode(imgstr), name='temp-' + current_time + '.' + ext)

        user = User.objects.create_user(request.data['email'], request.data['password'])

        user.first_name = request.data['first_name']
        user.last_name = request.data['last_name']

        user.is_active = request.data['is_active']
        user.is_admin = request.data['is_admin']
        user.is_superuser = request.data['is_superuser']
        user.is_staff = request.data['is_staff']

        user.profile_image = data

        user.save()
        serializer = UserSerializer(user, many=False)
        return Response(serializer.data)


class DeleteUserView(APIView):
    # permission_classes = [IsAuthenticated, IsAdminUser]
    permission_classes = [IsAuthenticated]

    def delete(self, request, email):
        user = User.objects.get(email=email)
        user.delete()
        serializer = UserSerializer(user, many=False)
        # return Response(serializer.data)

        return Response(serializer.data, status=status.HTTP_200_OK)


class LogoutView(APIView):

    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': 'Logout success!'
        }
        return response



class Predictor(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):

        model = load('./savedModels/model_saved_working')

        sepal_length = request.data['sepal_length']
        sepal_width = request.data['sepal_width']
        petal_length = request.data['petal_length']
        petal_width = request.data['petal_width']

        y_pred = model.predict([[sepal_length, sepal_width, petal_length, petal_width]])

        if y_pred[0] == 0:
            y_pred = 'Setosa'
        elif y_pred[0] == 1:
            y_pred = 'Verscicolor'
        else:
            y_pred = 'Virginica'

        return Response({'result': y_pred})