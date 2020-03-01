from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()

class ChoiceField(serializers.ChoiceField):

    def to_representation(self, obj):
        return self._choices[obj]

class UserCreateSerializer(serializers.ModelSerializer):
    role = ChoiceField(choices=User.ROLES)

    password = serializers.CharField(write_only=True, required=True, style={"input_type":   "password"})
    password2 = serializers.CharField(style={"input_type": "password"}, write_only=True, label="Confirm password")

    class Meta:
        model = User
        fields = ['email','username','name','password', 'role','password2']
        extra_kwargs = {"password":{"write_only": True}, "role":{"write_only": True}}

    def create(self, validated_data):

        name = validated_data["name"]
        role = validated_data["role"]
        username = validated_data["username"]
        email = validated_data["email"]
        password = validated_data["password"]
        password2 = validated_data["password2"]

        if (email and User.objects.filter(email=email).exclude(username=username).exists()):
            raise serializers.ValidationError({"email":"Email addresses must be unique!"})
        if password != password2:
            raise serializers.ValidationError({"password":"Passwords did not match"})

        user = User(username=username, email=email)
        user.name = name
        user.role = role
        user.set_password(password)
        user.save()

        return user
