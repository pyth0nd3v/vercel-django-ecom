from rest_framework import serializers
from django.contrib.auth.models import User


class RegisterSerializer(serializers.ModelSerializer):

    password2 = serializers.CharField(write_only=True, required=True)
    class Meta:
        model = User
        fields = '__all__'
 
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
            {"password": "Password fields didn't match."})

        if User.objects.filter(email=attrs['email']).exists():
                raise serializers.ValidationError({ "Email:" "Email already exist!" })

        return attrs
        
    def create(self, validated_data):
        user = User.objects.create(
            username = validated_data['username'], 
            first_name=validated_data['first_name'],
            last_name = validated_data['last_name'], 
            email = validated_data['email'] )
            
        user.set_password(validated_data['password'])
        user.save()
        return user