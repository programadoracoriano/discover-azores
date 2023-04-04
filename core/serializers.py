from rest_framework import serializers
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from .models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False, read_only=True)
    class Meta:
        model = Profile
        fields = '__all__'


class ImageGallerySerializer(serializers.ModelSerializer):
    class Meta:
        model   = ImageGallery
        fields  = '__all__'

class IslandSerializer(serializers.ModelSerializer):
    gallery = ImageGallerySerializer(read_only=True, many=True)
    class Meta:
        model   = Island
        fields  = '__all__'


class CountySerializer(serializers.ModelSerializer):
    gallery = ImageGallerySerializer(read_only=True, many=True)
    island  = IslandSerializer(read_only=True, many=False)
    class Meta:
        model   = County
        fields  = '__all__'

class ParishSerializer(serializers.ModelSerializer):
    county  = CountySerializer(read_only=True, many=False)
    gallery = ImageGallerySerializer(read_only=True, many=True)
    class Meta:
        model   = Parish
        fields  = '__all__'

class PlaceCategorieSerializer(serializers.ModelSerializer):
    class Meta:
        model   = PlaceCategorie
        fields  = '__all__'

class PlaceSubCategorieSerializer(serializers.ModelSerializer):
    categorie = PlaceCategorieSerializer(read_only=True, many=False)
    class Meta:
        model   = PlaceSubCategorie
        fields  = '__all__'

class PlaceTagSerializer(serializers.ModelSerializer):
    class Meta:
        model   = PlaceTag
        fields  = '__all__'

class FoodSerializer(serializers.ModelSerializer):
    class Meta:
        model   = Food
        fields  = '__all__'


class PlaceSerializer(serializers.ModelSerializer):
    # Add a custom field to the serializer to get the user from the request
    user        = serializers.SerializerMethodField()

    # Add a related field to the serializer to create/update related data
    categorie   = PlaceSubCategorieSerializer(many=False)
    parish      = ParishSerializer(many=False)
    categorie   = PlaceSubCategorieSerializer(many=False)
    gallery     = ImageGallerySerializer(many=True)
    tag         = PlaceTagSerializer(many=True)
    food        = FoodSerializer(many=True)

    class Meta:
        model = Place
        fields = '__all__'

    def get_user(self, obj):
        # Get the request object from the context
        request = self.context.get('request')

        # Use the JSONWebTokenAuthentication class to authenticate the request
        user = JSONWebTokenAuthentication().authenticate(request)[0]

        return user

    def create(self, validated_data):
        # Get the authenticated user object from the custom field
        user = self.get_user(validated_data)

        # Get the related data from the validated data
        categorie_data = validated_data.pop('categorie')
        parish_data    = validated_data.pop('parish')
        gallery_data   = validated_data.pop('gallery')
        tag_data       = validated_data.pop('tag')
        food_data      = validated_data.pop('food')
        Place.objects.create(user=user, 
                            categorie=categorie_data,
                            parish=parish_data,
                            gallery=gallery_data,
                            tag=tag_data,
                            food=food_data,
                             **validated_data)

        # Create the related data objects
        
        .objects.create(mymodel=mymodel, **data)

        return Place

    def update(self, instance, validated_data):
        # Get the authenticated user object from the custom field
        user = self.get_user(validated_data)

        # Get the related data from the validated data
        categorie_data  = validated_data.pop('categorie')
        cat_instance    = PlaceSubCategorieSerializer(instance=instance.categorie, 
                                                     data=categorie_data)
        parish_data     = validated_data.pop('parish')
        parish_instance = ParishSerializer(instance=instance.parish, 
                                           data=parish_data)
        gallery_data    = validated_data.pop('gallery')
        gallery_instance= ImageGallerySerializer(instance=instance.gallery, 
                                                 data=gallery_data)
        tag_data        = validated_data.pop('tag')
        tag_instance    = PlaceTagSerializer(instance=instance.tag, data=tag_data)

        food_data       = validated_data.pop('food')
        food_instance   = FoodSerializer(instance=instance.food, data=food_data)

        # Update the main model object
        instance.categorie = validated_data.get('categorie', instance.name)
        instance.save()

        # Create or update the related data objects
        for data in related_data:
            related, created = RelatedModel.objects.update_or_create(
                id=data.get('id', None),
                defaults={'field1': data.get('field1'), 'field2': data.get('field2')}
            )
            related.mymodel = instance
            related.save()

        return instance
