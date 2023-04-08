from core.models import *
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
class TokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['username'] = user.username
        token['email'] = user.email

        return token

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    token = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'token', 'id')

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

    def get_token(self, obj):
        refresh = RefreshToken.for_user(obj)
        return str(refresh.access_token)

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
    user        = UserSerializer()

    # Add a related field to the serializer to create/update related data
    categorie   = PlaceSubCategorieSerializer()
    parish      = ParishSerializer()
    categorie   = PlaceSubCategorieSerializer(many=False)
    gallery     = ImageGallerySerializer(many=True)
    tag         = PlaceTagSerializer(many=True)
    food        = FoodSerializer(many=True)

    class Meta:
        model = Place
        fields = '__all__'
