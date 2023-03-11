from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields =['id','username','name','email','password'] # we want to fetch this fields
        extra_kwarg = {
            'password':{'write_only' : True}  #For hiding password in response confirmation data
        }

    def create(self, validated_data): # for hashing the password
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password) # set_password is provided by Django
        instance.save()
        return instance