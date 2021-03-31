from datetime import datetime, timedelta

from django.contrib.auth import authenticate, get_user_model
from django.conf import settings

from rest_framework import serializers
from rest_framework_jwt.serializers import JSONWebTokenSerializer

from .phone_auth_service import create_code
from .jwt_helpers import create_token_from_dict

from profiles.serializers import ProfileSerializer
from profiles.models import Profile
from .models import AuthPhoneModel


User = get_user_model()

# Время жизни кода из СМС
SMS_CODE_EXPIRATION_DELTA = getattr(settings, "SMS_CODE_EXPIRATION_DELTA", timedelta(seconds=90))


class UserSerializer(serializers.ModelSerializer):
    """Handles serialization and deserialization of User objects."""
    password = serializers.CharField(max_length=128, min_length=8, write_only=True)
    profile = ProfileSerializer(write_only=True)
    bio = serializers.CharField(source='profile.bio', read_only=True)
    
    class Meta:
        model = User
        fields = (
            'email',
            'username',
            'password',
            'token',
            'profile',
            'bio',
        )

        read_only_fields = ('token',)
    
    def update(self, instance, validated_data):
        """Performs an update on a User."""
        password = validated_data.pop('password', None)
        profile_data = validated_data.pop('profile', {})
        
        for (key, value) in validated_data.items():
            setattr(instance, key, value)
        
        # сохраняем данные User
        if password is not None:
            instance.set_password(password)
        instance.save()

        # сохраняем данные Profile
        for (key, value) in profile_data.items():
            setattr(instance.profile, key, value)

        instance.profile.failed_attempt = 0
        instance.profile.save()
        
        return instance
    

class LoginSerializer(JSONWebTokenSerializer):
    username = serializers.CharField(max_length=255)
    email = serializers.CharField(max_length=255, required=False)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)
    phone = serializers.CharField(max_length=11, read_only=True)
    
    def __init__(self, *args, **kwargs):
        super(LoginSerializer, self).__init__(*args, **kwargs)
    
    def validate(self, attrs):
        credentials = {
            self.username_field: attrs.get(self.username_field),
            'password': attrs.get('password')
        }
        
        if all(credentials.values()):
            user = authenticate(**credentials)
            if user:
                if not user.is_active:
                    raise serializers.ValidationError('User account is disabled.')

                # сбрасываем счетчик провыльных попыток
                user.profile.failed_attempt = 0
                user.profile.save()
                
                return {
                    'email': user.email,
                    'username': user.username,
                    'token': user.token,
                    'phone': user.profile.phone,
                    'user': user,
                }
            else:
                raise serializers.ValidationError('Unable to log in with provided credentials.')
        else:
            msg = 'Must include "{username_field}" and "password".'
            msg = msg.format(username_field=self.username_field)
            raise serializers.ValidationError(msg)


class TokenAppBase(serializers.Serializer):
    token_app = serializers.SerializerMethodField(read_only=True)
    app_name = serializers.CharField(max_length=50, write_only=True, required=False)
    token = serializers.CharField(max_length=255, read_only=True)

    def get_token_app(self, data):
        return create_token_from_dict({
            "app": data.get("app_name", ""),
            "token": data["token"]
        }, 60)


class LoginSerializerFromAPI(TokenAppBase):
    password = serializers.CharField(max_length=128, write_only=True)
    phone = serializers.CharField(max_length=11)
    
    class Meta:
        fields = ('password', 'phone', 'token', 'app_name', 'token_app', )


class PhoneSerializerAPI(serializers.Serializer):
    phone = serializers.CharField(max_length=11)

    def validate(self, data):
        if not data.get("phone") or len(data["phone"]) != 11:
            raise serializers.ValidationError(
                'An phone is required to log in.'
            )
        
        if not data["phone"].isdigit() or len(data["phone"]) != 11:
            raise serializers.ValidationError(
                'An phone is not valid.'
            )
        
        return data
    
    class Meta:
        fields = ('phone', )


class PhoneSerializerConfirmAPI(TokenAppBase):
    phone = serializers.CharField(max_length=11)
    confirmCode = serializers.CharField(max_length=10)
    
    def validate(self, data):
        if not data.get("phone") or len(data["phone"]) != 11:
            raise serializers.ValidationError(
                'An phone is required to log in.'
            )
        
        if not data["phone"].isdigit() or len(data["phone"]) != 11:
            raise serializers.ValidationError(
                'An phone is not valid.'
            )
        
        if not data.get("confirmCode"):
            raise serializers.ValidationError(
                'An confirmCode is required to log in.'
            )
        
        return data
    
    class Meta:
        fields = ('phone', 'confirmCode', 'token', 'app_name', 'token_app',)


class PhoneSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(max_length=20, write_only=True)
    code = serializers.CharField(max_length=25, required=False)
    user = UserSerializer(required=False, write_only=True)

    class Meta:
        model = AuthPhoneModel
        fields = ('user', 'code', 'phone', )
        read_only_fields = ('user', 'phone', )

    def validate(self, data):
        phone = data.get('phone', None)
        
        if phone is None:
            raise serializers.ValidationError(
                'An phone is required to log in.'
            )

        try:
            profile = Profile.objects.get(phone=phone)
            
        except Profile.DoesNotExist:
            raise serializers.ValidationError(
                'A user with this phone was not found.'
            )

        if not profile.user.is_active:
            raise serializers.ValidationError(
                'This user has been deactivated.'
            )
        
        data["code"] = create_code()
            
        data["user"] = profile.user
        return data

    def create(self, validated_data):
        old_records = AuthPhoneModel.objects.filter(user__id=validated_data["user"].id)
        if len(old_records) > 0:
            old_records.delete()
        return AuthPhoneModel.objects.create(user=validated_data["user"], code=validated_data["code"])


class LoginFromCodeSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(max_length=20, write_only=True)
    code = serializers.CharField(max_length=25, write_only=True)
    user = UserSerializer(required=False, read_only=True)
    
    class Meta:
        model = AuthPhoneModel
        fields = ('user', 'code', 'phone',)
        read_only_fields = ('user', 'phone',)
    
    def validate(self, data):
        phone = data.get('phone', None)
        code = data.get('code', None)
        
        if phone is None:
            raise serializers.ValidationError(
                'An phone is required to log in.'
            )
        
        if code is None:
            raise serializers.ValidationError(
                'An code is required to log in.'
            )
        
        try:
            authPhone = AuthPhoneModel.objects.filter(user__profile__phone=phone, code=code).select_related("user").get()
        
        except AuthPhoneModel.DoesNotExist:
            raise serializers.ValidationError(
                'A user with this phone was not found.'
            )
        
        user = authPhone.user
        
        if not user.is_active:
            raise serializers.ValidationError(
                'This user has been deactivated.'
            )

        authPhone.delete()
        
        # проверяем актуален ли еще код из СМС
        if authPhone.created_at.replace(tzinfo=None) + SMS_CODE_EXPIRATION_DELTA < datetime.today():
            raise serializers.ValidationError('Code is outdated.')
        
        user.profile.failed_attempt = 0
        user.profile.save()
        
        data["user"] = user
        return data


class RecoveryPasswordSerializer(serializers.Serializer):
    birthDate = serializers.DateField(format="%d.%m.%Y", input_formats=["%d.%m.%Y", ], write_only=True)
    phone = serializers.CharField(max_length=11, write_only=True)

    def validate_phone(self, phone: str):
        if not phone or len(phone) != 11:
            raise serializers.ValidationError('Phone not Valid.')
        
        return phone
    
    class Meta:
        fields = (
            'birthDate',
            'phone',
        )