from django.contrib.auth import login
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User
from .models import Profile
from .serializers import SignupStep1Serializer, SignupStep2Serializer, SignupStep3Serializer, LoginSerializer


class SignupStep1View(APIView):
    def post(self, request):
        serializer = SignupStep1Serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            request.session['user_id'] = user.id
            return Response({"message": "Step 1 completed."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SignupStep2View(APIView):
    def post(self, request):
        user_id = request.session.get('user_id')
        if not user_id:
            return Response({"error": "Session expired or invalid."}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.get(id=user_id)
        serializer = SignupStep2Serializer(data=request.data)
        if serializer.is_valid():
            profile_data = serializer.validated_data
            profile_data['user'] = user  # Attach the user instance to profile data
            profile, created = Profile.objects.get_or_create(user=user, defaults=profile_data)
            if not created:
                profile.phone_number = profile_data.get('phone_number', profile.phone_number)
                profile.address = profile_data.get('address', profile.address)
                profile.work_email = profile_data.get('work_email', profile.work_email)
                if 'work_id_card' in request.FILES:
                    profile.work_id_card = request.FILES['work_id_card']
                if 'government_issued_id' in request.FILES:
                    profile.government_issued_id = request.FILES['government_issued_id']
                profile.save()
            return Response({"message": "Step 2 completed."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SignupStep3View(APIView):
    def post(self, request):
        user_id = request.session.get('user_id')
        if not user_id:
            return Response({"error": "Session expired or invalid."}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.get(id=user_id)
        serializer = SignupStep3Serializer(data=request.data)
        if serializer.is_valid():
            profile_data = serializer.validated_data
            profile_data['user'] = user  # Attach the user instance to profile data
            profile, created = Profile.objects.get_or_create(user=user, defaults=profile_data)
            if not created:
                profile.gender = profile_data.get('gender', profile.gender)
                profile.address = profile_data.get('address', profile.address)
                profile.state_of_origin = profile_data.get('state_of_origin', profile.state_of_origin)
                profile.local_government_area = profile_data.get('local_government_area', profile.local_government_area)
                profile.highest_education_level = profile_data.get('highest_education_level',
                                                                   profile.highest_education_level)
                profile.marital_status = profile_data.get('marital_status', profile.marital_status)
                profile.title = profile_data.get('title', profile.title)
                profile.is_verified = True
                profile.save()
            return Response({"message": "Signup completed.", "user": user.username}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            login(request, user)
            return Response({"message": "Login successful"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
