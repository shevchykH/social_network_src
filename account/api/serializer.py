from django.contrib.auth.models import User
from django.db.models import Q
from rest_framework import serializers
from rest_framework_simplejwt.tokens import AccessToken
import clearbit
from pyhunter import PyHunter


from social_network.settings import CLEARBIT_KEY, HUNTERIO_KEY


class RegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    extra_data = serializers.JSONField(required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2', 'extra_data']
        extra_kwargs = {'password': {'write_only': True}}

    def get_extra_data(self, email):
        try:
            clearbit.key = CLEARBIT_KEY
            return clearbit.Enrichment.find(email=email, stream=True)
        except Exception:
            pass

    def create(self, validated_data):
        extra_data = None
        email = validated_data.get('email')
        if email:
            extra_data = self.get_extra_data(email)
        user_obj = User.objects.create_user(
            username=validated_data.get('username'),
            email=email,
            password=validated_data.get('password'),
        )
        user_obj.is_staff = True
        print("extra_data == ", extra_data)
        user_obj.profile.extra_data = extra_data
        user_obj.save()
        return user_obj

    def validate_email(self, email):
        hunter = PyHunter(HUNTERIO_KEY)
        try:
            payload = hunter.email_verifier(email)
        except Exception:
            return
        result = payload.get('result')
        if result == 'undeliverable':
            raise serializers.ValidationError('The email address is not valid.')

    def validate(self, data):
        password1 = data.get('password')
        password2 = data.pop('password2')
        email = data.get('email')
        if password1 != password2:
            raise serializers.ValidationError("Passwords do not match.")
        data['extra'] = self.get_extra_data(email)
        return data


class LoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=False, allow_blank=True)
    email = serializers.EmailField(required=False, allow_blank=True)
    token = serializers.CharField(allow_blank=True, read_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'token']
        extra_kwargs = {"password": {"write_only": True}}

    def validate(self, data):
        email = data.get('email')
        username = data.get('username')
        password = data.get('password')
        if not email and not username:
            raise serializers.ValidationError('A username or email is required.')
        user = User.objects.filter(
            Q(username=username) |
            Q(email=email)
        )
        if user.exists() and user.count() == 1:
            user_obj = user.first()
        else:
            raise serializers.ValidationError('The username/email is not valid.')
        if user_obj:
            if not user_obj.check_password(password):
                raise serializers.ValidationError('Incorrect credentials please try again.')
        data['token'] = self.get_token(user_obj)
        return data

    def get_token(self, obj):
        user = obj
        token = AccessToken.for_user(user)
        return token
