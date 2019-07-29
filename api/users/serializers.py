from rest_framework import serializers
from gray_merchant.models import User, UserProfile, UserAddress


class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfile
        fields = ('dob', 'phone', 'photo')


class UserAddressSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserAddress
        fields = ('address_line_1', 'address_line_2', 'address_line_3', 'city', 'state', 'zip_code')


class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(required=True)
    address = UserAddressSerializer(required=False)

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'password', 'profile', 'address')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        profile_data = validated_data.pop('profile')
        address_data = validated_data.pop('address')
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        UserProfile.objects.create(user=user, **profile_data)
        UserAddress.objects.create(user=user, **address_data)

        return user

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile')
        address_data = validated_data.pop('address')
        profile = instance.profile
        address = instance.address

        instance.email = validated_data.get('email', instance.email)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.is_staff = validated_data.get('is_staff', instance.is_staff)
        instance.is_active = validated_data.get('is_active', instance.is_active)
        instance.save()

        profile.dob = profile_data.get('dob', profile.dob)
        profile.photo = profile_data.get('photo', profile.photo)
        profile.save()
        
        address.address_line_1 = address_data.get('address_line_1', address.address_line_1)
        address.address_line_2 = address_data.get('address_line_2', address.address_line_2)
        address.address_line_3 = address_data.get('address_line_3', address.address_line_3)
        address.city = address_data.get('city', address.city)
        address.state = address_data.get('state', address.state)
        address.zip_code = address_data.get('zip_code', address.zip_code)
        address.save()

        return instance
