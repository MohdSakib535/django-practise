from django.contrib.auth.models import User
from rest_framework import serializers
from base.models import Snippet,Resource,Movie

class Userserlizer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields='__all__'


class Userserlizer_forone(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=('username',)


class snippetser(serializers.ModelSerializer):
    def create(self, validated_data):
        print("---",validated_data)
        """
        Create and return a new `Snippet` instance, given the validated data.

        """
        # dtaa=self.perform_create(validated_data)
      

        return Snippet.objects.create(**validated_data)
    
    class Meta:
        model=Snippet
        # fields="__all__"
        fields=('id','title','code','linenos','language','style','user_data')
        




class SnippetSerlizers(serializers.ModelSerializer):
    # user_data=Userserlizer_forone()

    def create(self, validated_data):
        print("---",validated_data)
        """
        Create and return a new `Snippet` instance, given the validated data.

        """
        # dtaa=self.perform_create(validated_data)

        return Snippet.objects.create(**validated_data)
    
     
    # def perform_create(self,se3):
    #     print('-------',se3)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Snippet` instance, given the validated data.
        """
        instance.title = validated_data.get('title',instance.title).upper()
        instance.code = validated_data.get('code', instance.code).upper()
        instance.linenos = validated_data.get('linenos', instance.linenos)
        instance.language = validated_data.get('language', instance.language)
        instance.style = validated_data.get('style', instance.style)
        instance.save()
        return instance



    class Meta:
        model=Snippet
        fields='__all__'
        # fields=('id','code','title','user_data')

    


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'




class ResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resource
        fields = '__all__'



    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['likes'] = instance.liked_by.count()

        return representation
    

    def to_internal_value(self, data):
        resource_data = data['resource']

        return super().to_internal_value(resource_data)



class MovieSerializer(serializers.ModelSerializer):
    movie_resource = ResourceSerializer()

    class Meta:
        model = Movie
        fields = ['id', 'title', 'description', 'release_date', 'rating', 'us_gross', 'worldwide_gross', 'movie_resource']