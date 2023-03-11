from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework.serializers import ModelSerializer
from rest_framework.validators import UniqueValidator
from rest_framework import serializers


from .models import User

class RegisterUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=get_user_model().objects.all())]
    )

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])

    class Meta:
        model = get_user_model()
        fields = ('id','email', 'password', 'first_name', 'last_name','profile_image')
        extra_kwargs = {
            'password': {'write_only': True, 'min_length': 8},
            'first_name': {'required': True},
            'last_name': {'required': True}
        }

    def create(self, validated_data):
        user = self.Meta.model.objects.create(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
        )

        user.set_password(validated_data['password'])
        user.save()

        return user





class UserProfileUpdateSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        return get_user_model().objects.create_user(**validated_data)

    class Meta:
        model = get_user_model()
        fields = ('id','email', 'password', 'first_name', 'last_name',)
        read_only_fields = ('id', 'email',)
        extra_kwargs = {
            'password': {'write_only': True, 'min_length': 8, 'required': False},
            'first_name': {'required': True},
            'last_name': {'required': True},
        }





class UserSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        return get_user_model().objects.create_user(**validated_data)

    class Meta:
        model = get_user_model()
        fields = ('id','email', 'password', 'first_name', 'last_name','profile_image','is_active','is_admin','is_staff','is_superuser')
        extra_kwargs = {
            'password': {'write_only': True, 'min_length': 8},
        }





    def create(self, validated_data): # for hashing the password
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password) # set_password is provided by Django
        instance.save()
        return instance