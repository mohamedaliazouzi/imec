from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from api.models import Attribute, UserAttribute, Group, UserAttribute


class AttributeSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=30)
    value = serializers.CharField(max_length=255)

    def validate(self, data):
        if not data.get('name') or not data.get('value'):
            raise serializers.ValidationError("Both name and value are required for attributes.")
        return data


class UserRegistrationSerializer(serializers.ModelSerializer):
    attributes = AttributeSerializer(many=True, write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'attributes']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        attributes_data = validated_data.pop('attributes', [])
        print("Attributes Data:", attributes_data)

        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        print(f"User created: {user.username}")

        for attr in attributes_data:
            name = attr.get('name')
            value = attr.get('value')

            print(f"Processing Attribute - Name: {name}, Value: {value}")

            if not name or not value:
                print("Validation failed: Both name and value are required.")  # Debugging print
                raise serializers.ValidationError("Both name and value are required for each attribute.")

            attribute, created = Attribute.objects.get_or_create(name=name)
            print(f"Attribute {'created' if created else 'found'}: {attribute.name}")  # Debugging print

            user_attribute = UserAttribute.objects.create(user=user, attribute=attribute, value=value)
            print(
                f"UserAttribute created for {user.username} - {user_attribute.attribute.name} with value: {user_attribute.value}")  # Debugging print

        return user


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        token['email'] = user.email
        return token


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    attributes = serializers.ListField(child=serializers.DictField(), write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'attributes']

    def create(self, validated_data):
        # Extract attributes data from validated_data
        attributes_data = validated_data.pop('attributes', [])
        print("Attributes Data:", attributes_data)  # Print the extracted attributes data

        # Create the user
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        print(f"User created: {user.username}")  # Confirm the user was created

        # Loop through each attribute and create UserAttribute
        for attr in attributes_data:
            name = attr.get('name')
            value = attr.get('value')

            # Print to verify the data for each attribute
            print(f"Processing Attribute - Name: {name}, Value: {value}")

            # Validate if both name and value are provided
            if not name or not value:
                print("Validation failed: Both name and value are required.")  # Debugging print
                raise serializers.ValidationError("Both name and value are required for each attribute.")

            # Create or retrieve the attribute
            attribute, created = Attribute.objects.get_or_create(name=name)
            print(f"Attribute {'created' if created else 'found'}: {attribute.name}")  # Debugging print

            # Create the UserAttribute object
            user_attribute = UserAttribute.objects.create(user=user, attribute=attribute, value=value)
            print(
                f"UserAttribute created for {user.username} - {user_attribute.attribute.name} with value: {user_attribute.value}")  # Debugging print

        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class AttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attribute
        fields = '__all__'


class GroupSerializer(serializers.ModelSerializer):
    attributes = AttributeSerializer(many=True)

    class Meta:
        model = Group
        fields = '__all__'



class UserAttributeSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    attribute = AttributeSerializer()

    class Meta:
        model = UserAttribute
        fields = '__all__'
