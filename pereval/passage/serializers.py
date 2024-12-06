from rest_framework import serializers
from rest_framework.templatetags.rest_framework import items

from .models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        Fields = '__all__'

class LevelsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Levels
        fields = '__all__'

class CoordinatesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coordinates
        fields = '__all__'

class PassagesSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    coordinates = CoordinatesSerializer()
    level = LevelsSerializer()
    add_time = serializers.DateTimeField(format='%d %m %Y %H:%M:%S', read_only=True)
    status = serializers.CharField(read_only=True)

    class Meta:
        model = Passages
        fields = '__all__'

    def create(self,validated_date):
        user_date = validated_date.pop('user')
        coordinates_data = validated_date.pop('coordinates')
        level_data = validated_date.pop('level')

        user = User.objects.create(**user_date)
        coordinates = Coordinates.objects.create(**coordinates_data)
        level = Levels.objects.create(**level_data)

        passage = Passages.objects.create(
            user = user,
            coordinates = coordinates,
            level = level,
            **validated_date
        )
        return  passage

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', None)
        coordinates_data = validated_data.pop('coordinates', None)
        level_data = validated_data.pop('level', None)

        if user_data:
            for attr, value in user_data,items():
                setattr(instance.user, attr, value)
            instance.user.save()

        if coordinates_data:
            for attr, value in coordinates_data,items():
                setattr(instance.coordinates, attr, value)
            instance.coordinates.save()

        if level_data:
            for attr, value in level_data.items():
                setattr(instance.level, attr, value)
            instance.level.save()

        for attr, value in validated_data,items():
            setattr(instance, attr, value)
        instance.save()

        return instance

class ImagesSerializer(serializers.ModelSerializer):
    passage = PassagesSerializer()

    class Meta:
        Model = Images
        fields = '__all__'

    def create(self, validered_date):
        passage_date = validered_date.pop('passage')
        passage = Passages.objects.create(**passage_date)
        image = Images.objects.create(passage=passage, **validered_date)
        return image

    def update(self, instance, validated_data):
        passage_data = validated_data.pop('passage', None)

        if passage_data:
            for attr, value in passage_data.items():
                setattr(instance.passage, attr, value)
            instance.passage.save()

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        return instance
