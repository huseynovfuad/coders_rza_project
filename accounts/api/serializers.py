from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils import timezone
from services.generator import Generator
from django.core.mail import send_mail
from django.conf import settings

User = get_user_model()



class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()

    class Meta:
        model = User
        fields = ("email", "password")
        extra_kwargs = {
            "password": {"write_only": True}
        }


    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        user = authenticate(email=email, password=password)

        if not user:
            raise serializers.ValidationError(
                {"error": "Email or password is wrong"}
            )

        if not user.is_active:
            raise serializers.ValidationError(
                {"error": "Your account is not active"}
            )

        return attrs


    def to_representation(self, instance):
        repr_ = super().to_representation(instance)
        user = User.objects.get(email=instance.get("email"))
        token = RefreshToken.for_user(user)
        repr_["tokens"] = {"refresh": str(token),"access": str(token.access_token)}
        return repr_



class RegisterSerializer(serializers.ModelSerializer):
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ("email", "fullname", "slug", "password", "password_confirm")
        extra_kwargs = {
            "password": {"write_only": True},
            "slug": {"read_only": True},
        }

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")
        password_confirm = attrs.get("password_confirm")

        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                {"error": "This username already exists"}
            )

        if len(password) < 6:
            raise serializers.ValidationError(
                {"error": "Minimum length is 6"}
            )

        if password != password_confirm:
            raise serializers.ValidationError(
                {"error": "Passwords dont match"}
            )

        return attrs


    def create(self, validated_data):
        password = validated_data.pop("password")
        validated_data.pop("password_confirm")
        user = User.objects.create(
            **validated_data, is_active=False,
            activation_code = Generator.create_code_for_activate(size=6, model_=User),
            activation_code_expires_at = timezone.now() + timezone.timedelta(minutes=10)
        )
        user.set_password(password)
        user.save()

        # send mail part
        send_mail(
            "Activation Code",
            f"Your activation code: {user.activation_code}",
            settings.EMAIL_HOST_USER,
            [user.email]
        )
        return user



class ActivationSerializer(serializers.ModelSerializer):
    activation_code = serializers.CharField(max_length=6, min_length=6)
    class Meta:
        model = User
        fields = ("email", "slug", "activation_code", )
        extra_kwargs = {
            "email": {"read_only": True},
            "slug": {"read_only": True},
            "activation_code": {"write_only": True},
        }


    def validate(self, attrs):
        print(attrs)
        activation_code = attrs.get("activation_code")
        user = self.context.get("user")
        print(activation_code, user.activation_code)
        now = timezone.now()

        if now > user.activation_code_expires_at:
            raise serializers.ValidationError(
                {"error": "Activation code expires"}
            )

        if str(activation_code) != str(user.activation_code):
            raise serializers.ValidationError(
                {"error": "Activation code is wrong"}
            )
        return attrs


    def create(self, validated_data):
        user = self.context.get("user")
        user.is_active = True
        user.activation_code = None
        user.activation_code_expires_at = None
        user.save()

        return user


    def to_representation(self, instance):
        repr_ = super().to_representation(instance)
        token = RefreshToken.for_user(instance)
        repr_["tokens"] = {"refresh": str(token), "access": str(token.access_token)}
        return repr_