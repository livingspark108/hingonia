from django.db import transaction
from django.contrib.auth.models import User

from rest_framework import serializers

from app.models import *
from settings.models import *
from django_countries.serializers import CountryFieldMixin
from django_countries.serializer_fields import CountryField

class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(required=True)
    password = serializers.CharField(required=True)


class UserAllDataSerializer(serializers.ModelSerializer):
    """
        User All Data Serializer
    """
    user_shipping = serializers.SerializerMethodField()
    image = serializers.ImageField(required=False)
    token = serializers.ReadOnlyField(source='auth_token.key')

    class Meta:
        model = User
        fields = (
        'id', 'first_name', 'last_name', 'email', 'password', 'phone_no', 'address_1', 'address_2',
        'city', 'country', 'state', 'zip_code', 'image', 'role', 'token','credit_points','seva_points','gifted','followers', 'user_shipping')

    def get_user_shipping(self, instance):
        shipping = instance.user_shipping.all()
        return UserShippingListSerializer(shipping, many=True).data


class UserShippingSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserShipping
        fields = ('id','shipping_email', 'shipping_first_name', 'shipping_last_name', 'shipping_address_1',
                  'shipping_address_2', 'shipping_zip_code', 'shipping_phone_no', 'shipping_country', 'shipping_state',
                  'shipping_city', 'user')


class UserSerializer(serializers.ModelSerializer):
    """
    User Serializer
    """
    image = serializers.ImageField (required = False)
    token = serializers.ReadOnlyField(source='auth_token.key')
    class Meta:
        model = User
        fields = ('id','first_name','last_name', 'email', 'password','phone_no','address_1','address_2','city','country','state','zip_code','image','role', 'refer_code', 'token')

    @transaction.atomic
    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        user.username = validated_data['email']
        user.set_password(validated_data['password'])
        user.save()
        return user

    @transaction.atomic
    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.set_password(validated_data.get('password', instance.password))
        instance.save()
        return instance


class UpdateUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('first_name','last_name','username', 'email','address_1','address_2','city','country','state','phone_no','zip_code','role','image')
        extra_kwargs = {'first_name': {'required': False},
                        'username': {'required': False},
                        'email': {'required': False},
                        }


class UsergforgateSerializer(serializers.ModelSerializer):
    """
    User Forgot Password Serializer
    """

    class Meta:
        model = User
        fields = ('email')


class UserListSerializer(serializers.ModelSerializer):
    """
    User List Serializer
    """

    class Meta:
        model = User
        fields = ('id','first_name','last_name','username', 'email','address_1','address_2','city','country','state','phone_no',
                  'role','zip_code','role','image')


class UserShippingListSerializer(serializers.ModelSerializer):
    """
    User Shipping List Serializer
    """

    class Meta:
        model = UserShipping
        fields = ['id','shipping_email', 'shipping_first_name', 'shipping_last_name', 'shipping_address_1',
                  'shipping_address_2', 'shipping_zip_code', 'shipping_phone_no', 'shipping_country', 'shipping_state',
                  'shipping_city', 'user']


class UpdateShippingSerializer(serializers.ModelSerializer):
    """
    User Shipping Update Serializer
    """
    id = serializers.CharField()

    class Meta:
        model = UserShipping
        fields = ['id','shipping_email', 'shipping_first_name', 'shipping_last_name', 'shipping_address_1',
                  'shipping_address_2', 'shipping_zip_code', 'shipping_phone_no', 'shipping_country', 'shipping_state',
                  'shipping_city', 'user']


class UpdateUserAddressSerializer(serializers.ModelSerializer):
    """
    User Shipping Update Serializer
    """
    id = serializers.CharField()

    class Meta:
        model = User
        fields = ['address_1','address_2','city','country','state','phone_no','zip_code','id']


class IDSerializer(serializers.Serializer):
    id = serializers.CharField()


class IDUserShippingSerializer(serializers.ModelSerializer):
    id = serializers.CharField()

    class Meta:
        model = UserShipping
        fields = ['id']


class SlugSerializer(serializers.Serializer):
    slug = serializers.CharField()


class ChangePasswordSerializer(serializers.Serializer):

    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)


class StateSerializer(serializers.ModelSerializer):

    class Meta:
        model = StateList
        fields = ('id','name','country_code')
