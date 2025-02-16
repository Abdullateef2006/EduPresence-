from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Attendance

User = get_user_model()

# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ['id', 'username', 'matric_number', 'password']
#         extra_kwargs = {'password': {'write_only': True}}

#     def create(self, validated_data):
#         user = User.objects.create_user(**validated_data)
#         return user
# face_app/serializers.py
from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()  # This will return your custom user model if AUTH_USER_MODEL is set

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'matric_number', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        # Create user using the create_user method to properly hash the password.
        return User.objects.create_user(**validated_data)



class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = '__all__'


class LoginSerializer(serializers.Serializer):
    matric_number = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        matric_number = data.get('matric_number')
        password = data.get('password')
        try:
            user = User.objects.get(matric_number=matric_number)
        except User.DoesNotExist:
            raise serializers.ValidationError("Invalid matric number or password")

        if not user.check_password(password):
            raise serializers.ValidationError("Invalid matric number or password")

        token = RefreshToken.for_user(user)
        return {
            'refresh': str(token),
            'access': str(token.access_token),
            'user': {
                'id': user.id,
                'username': user.username,
                'matric_number': user.matric_number,
            }
        }
