from django.contrib.auth.models import User
from rest_framework import serializers
from base.models import *

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





class PollSerializer(serializers.ModelSerializer):
    class Meta:
        model = Poll
        fields = '__all__'

    def create(self, validated_data):
        # Remove 'history_user' from validated_data if it exists
        history_user = validated_data.pop('history_user', None)

        # Create the Poll instance
        poll = Poll.objects.create(**validated_data)

        # If history_user is provided, set it after creation
        if history_user is not None:
            poll.history.first().history_user = history_user
            poll.history.first().save()

        return poll
    
    # def update(self, instance, validated_data):
    #     # Remove 'history_user' from validated_data if it exists
    #     history_user = validated_data.pop('history_user', None)

    #     # Update the Poll instance
    #     poll = super().update(instance, validated_data)

    #     # If history_user is provided, set it after update
    #     if history_user is not None:
    #         poll.history.first().history_user = history_user
    #         poll.history.first().save()

    #     return poll
    

class ChoiceSerializer(serializers.ModelSerializer):
    # poll=PollSerializer(read_only=True)
    # poll = serializers.CharField(source='poll.question', read_only=True)
    poll = serializers.PrimaryKeyRelatedField(queryset=Poll.objects.all(), write_only=True)
    poll_question = serializers.SerializerMethodField()

    class Meta:
        model = Choice
        fields = '__all__'

    def create(self, validated_data):
        # Remove 'history_user' from validated_data if it exists
        history_user = validated_data.pop('history_user', None)

        # Create the Choice instance
        choice = Choice.objects.create(**validated_data)

        # If history_user is provided, set it after creation
        if history_user is not None:
            choice.history.first().history_user = history_user
            choice.history.first().save()

        return choice
    
    def get_poll_question(self, obj):
        return obj.poll.question  # Return poll question in GET response

    # def update(self, instance, validated_data):
    #     # Remove 'history_user' from validated_data if it exists
    #     history_user = validated_data.pop('history_user', None)

    #     # Update the Choice instance
    #     choice = super().update(instance, validated_data)

    #     # If history_user is provided, set it after update
    #     if history_user is not None:
    #         choice.history.first().history_user = history_user
    #         choice.history.first().save()

    #     return choice