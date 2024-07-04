from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, Serializer
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from rest_framework_simplejwt.tokens import Token
from .models import CustomUser, CustomUserConfirmation, AUTH_STATUS, AUTH_TYPE, Note
from django.core.mail import send_mail
from shared_app.utility import send_sms, validate_email_or_phone
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.utils import timezone




class RegisterSerializer(ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'}, validators=[validate_password])
    username = serializers.CharField(required=True, validators=[UniqueValidator(queryset=CustomUser.objects.all())])

    def __init__(self, *args, **kwargs):
        super(RegisterSerializer, self).__init__(*args, **kwargs)
        self.fields['password2'] = serializers.CharField(write_only=True, required=False, style={'input_type': 'password'}, validators=[validate_password])
        self.fields['email_or_phone'] = serializers.CharField(required=False)
        
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'password', 'auth_type', 'email', 'phone_number']
        
        extra_kwargs = {
            'auth_type': {'required': False},
        }
        
        
    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        if CustomUser.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError("Username already exists")
        email_or_phone = data['email_or_phone']
        auth_type = validate_email_or_phone(data['email_or_phone'])
        if auth_type == AUTH_TYPE.email:
            data.update({'email': email_or_phone, 'auth_type': auth_type})
            if CustomUser.objects.filter(email=data['email_or_phone']).exists():
                raise serializers.ValidationError("Email already exist")
        elif auth_type == AUTH_TYPE.phone:
            data.update({'phone_number': email_or_phone, 'auth_type': auth_type})
            if CustomUser.objects.filter(phone_number=data['email_or_phone']).exists():
                raise serializers.ValidationError("Phone number already exist")
        else:
            raise serializers.ValidationError("Invalid email or phone number")
        print('2) validated data from validate: ', data)
        return data

        
    def create(self, validated_data):
        validated_data.pop('password2')
        validated_data.pop('email_or_phone')
        print('3) validated_data from create: ', validated_data)
        user = super(RegisterSerializer, self).create(validated_data)
        try:
            user.set_password(validated_data.get('password'))
        except:
            print('user password did not hashed!!!')
        if user.auth_type == AUTH_TYPE.email:
            code = user.create_verify_code(AUTH_TYPE.email)
            print('4) auth_type is email, code: ', code)
            send_mail(subject='We congratulate you on registration', message=f"Welcome to our site {user.username}, your code: {code}", from_email='atajanovkamronbek2003@gmail.com', recipient_list=[user.email,], fail_silently=False)
        else:
            code = user.create_verify_code(AUTH_TYPE.phone)
            send_sms(to_number=user.phone_number, body=f"Welcome to our site {user.username}, your code: {code}")
        user.save()
        
        return user




class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
        
class VerificationSerializer(serializers.Serializer):
    code = serializers.CharField()

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod 
    def get_token(cls, user):
        
        token = super().get_token(user)
        token['username'] = user.username
        token['auth_type'] = user.auth_type
        
        return token




class CustomUserSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    auth_type = serializers.CharField(read_only=True)
    date_joined = serializers.DateTimeField(read_only=True)
    created_time = serializers.DateTimeField(read_only=True)
    updated_time = serializers.DateTimeField(read_only=True)
    days_since_joined = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'full_name', 'days_since_joined', 'photo', 'first_name', 'last_name', 'email', 'phone_number', 'date_of_birth', 'gender', 'auth_type', 'province', 'bio', 'date_joined', 'created_time', 'updated_time']
    
    def get_days_since_joined(self, obj):
        return (timezone.now() - obj.date_joined).days




class NoteSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    created_time = serializers.DateTimeField(read_only=True)
    updated_time = serializers.DateTimeField(read_only=True)
    owner = CustomUserSerializer(read_only=True)
    
    class Meta:
        model = Note
        fields = ['id','owner', 'text', 'created_time', 'updated_time']

    def validate(self, data):
        if not data['text']:
            raise serializers.ValidationError("Text field cannot be empty.")
        return data
    
    def create(self, validated_data):
        owner = validated_data.get('owner')
        note = validated_data.get('text')
        created_note = Note.objects.create(owner=owner, text=note)
        created_note.save()
        return created_note
    
    def update(self, instance, validated_data):
        instance.text = validated_data.get('text', instance.text)
        instance.save()
        return instance
    
    

