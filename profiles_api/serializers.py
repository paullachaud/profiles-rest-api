from rest_framework import serializers
from rest_framework.relations import StringRelatedField

from profiles_api import models

class HelloSerializer(serializers.Serializer):
    """Serializes a name field for testing our APIView. Handles validation fields"""
    name = serializers.CharField(max_length = 10)


class HabitInstanceSerializer(serializers.ModelSerializer):
    """ Handles serialization of Habit Instance"""
    class Meta:
        model = models.HabitInstance
        fields = ['status']

class HabitSerializer(serializers.ModelSerializer):
    # habit_instance = HabitInstanceSerializer(many = True)
    """ Handles serialization of Habits"""
    class Meta:
        model = models.Habit
        fields = ['name', 'user', 'frequency']
    
    def create(self, validated_data):
        habit = models.Habit.objects.create(      
            name = validated_data['name'],
            user = validated_data['user'],
            frequency = validated_data['frequency']
        )

        # habit.instances = models.HabitInstance.objects.get()

        return habit

class UserProfileSerializer(serializers.ModelSerializer):
    """"""
    habits = StringRelatedField(many=True)
    class Meta:
        model = models.UserProfile
        fields = ('id', 'email', 'name', 'habits','password')
        extra_kwargs = {
            'password': {
                'write_only': True,
                'style' : {'input_type': 'password'}
            }
        }

    def create(self, validated_data):
        user = models.UserProfile.objects.create_user(
            email = validated_data['email'],
            name = validated_data['name'],
            password = validated_data['password']

        )
        return user

    def update(self, instance, validated_data):
        """Handle updating user account"""
        if 'password' in validated_data:
            password = validated_data.pop('password')
            instance.set_password(password)

        return super().update(instance, validated_data)





