from django.contrib.auth import authenticate
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile


class SignupStep1Serializer(serializers.ModelSerializer):
    employment_status = serializers.CharField(max_length=255, required=False)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Profile
        fields = ['username', 'email', 'password', 'first_name', 'last_name', 'employment_status', 'phone_number']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user_data = validated_data.pop('user', None)
        user = User.objects.create_user(**user_data)
        profile = Profile.objects.create(user=user, **validated_data)
        return user


class SignupStep2Serializer(serializers.ModelSerializer):
    work_id_card = serializers.ImageField(required=False)
    government_issued_id = serializers.ImageField(required=False)

    class Meta:
        model = Profile
        fields = ['work_email', 'work_id_card', 'government_issued_id', 'work_place', 'course_of_expertise']


class SignupStep3Serializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['gender', 'address', 'state_of_origin', 'local_government_area', 'highest_education_level',
                  'marital_status', 'title']


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if user:
                if not user.is_active:
                    raise serializers.ValidationError("User is inactive.")
                data['user'] = user
            else:
                raise serializers.ValidationError("Invalid login credentials.")
        else:
            raise serializers.ValidationError("Must include username and password.")
        return data
