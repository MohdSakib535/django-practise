from django.shortcuts import render
from base.serlizers import *
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from base.models import *
from drf_yasg.utils import swagger_auto_schema
import logging
from django.contrib.auth.models import Permission

logger = logging.getLogger(__name__)

# Create your views here.

class Data_view(APIView):
    def get(self,request,format=None):
        user_data=User.objects.all()
        serlizer_data=UserSerializer(user_data,many=True,context={'request': request})
        return Response({"Response":serlizer_data.data})
       


class snippet_view(APIView):
    # user_data=User.objects.all().exist()
    # if user_data:



    def get(self,request):
        # snipped_data=Snippet.objects.filter(user_data=request.user)
        snipped_data=Snippet.objects.all()
        ser=SnippetSerlizers(snipped_data,many=True)
        return Response({"Response":ser.data})

    @swagger_auto_schema(request_body=snippetser)
    def post(self,request):
        try:
            params=request.data
            usr_Data=User.objects.filter(id=params.get('user_data'))
            if not usr_Data:
                return Response({"MSG":"user data doesnot exist"})
            serlizers_data=snippetser(data=params)
            if serlizers_data.is_valid():

                serlizers_data.save()
                print('data save')
            else:
                print('---------------error')
            return Response({"mess":serlizers_data.data,"status":"Created"})
        except Exception as err:
            return Response({"response":err})


class snippet_details(APIView):
    def get(self,request,pk,format=None):
        try:
            s1=Snippet.objects.get(pk=pk)
        except Exception as err:
            from sentry_sdk import capture_message
            from sentry_sdk import a
            capture_message({"MSG":"error from sentry","error":err}, level="error")

            logger.warning(f"Error in Get request in Snippet details .....GET {err}")
            return Response({"error":err})
        ser1=SnippetSerlizers(s1)
        logger.info(f"Get request for a particular data ")
        return Response({"Response":ser1.data})


    def put(self,request,pk):
        s1=Snippet.objects.get(pk=pk)
        sre1=SnippetSerlizers(s1,request.data)
        if sre1.is_valid():
            sre1.save()
            return Response({"Reponse":sre1.data,"status":"Updated"})
        

class Resource_view(APIView):
    def get(self,request,format=None):
        user_data=Resource.objects.all()
        serlizer_data=ResourceSerializer(user_data,many=True,context={'request': request})
        return Response({"Response":serlizer_data.data})
    
    def post(self,request):
        r_data=ResourceSerializer(data=request.data)

        if r_data.is_valid():
            r_data.save()
            return Response({"response":r_data.data})
        

from django.http import HttpResponse

def fun1(request):
    movie,created = Movie.objects.get_or_create(
    title='Inception',
    description='A mind-bending thriller by Christopher Nolan.',
    release_date='2010-07-16',
    rating=9,
    us_gross=292576195,
    worldwide_gross=829895144,
    )
    # print('movie-----',movie)
    # print('created----',created)

        # Retrieve the title dynamically
    title = getattr(movie, 'title', 'No title available')
    # print('title---------',title)  # Output: Inception

    # Attempt to access a non-existing attribute with a default value
    director = getattr(movie, 'director', 'Director not specified')
    # print('director---------',director)  # Output: Director not specified

    # Dynamically set the description
    if created == False:

        #triggere once once

        # setattr(movie, 'description', 'A movie about dreams within dreams all.')
        # movie.save()

         # Check the updated description
        # print('description-data----',movie.description)  # Output: A movie about dreams within dreams.


        # Check if the Movie instance has a 'rating' attribute
        if hasattr(movie, 'rating'):
            print(f"Rating: {getattr(movie, 'rating')}")
        else:
            print("Rating attribute not found.")

        # Check if the Movie instance has a 'director' attribute
        if hasattr(movie, 'director'):
            print(f"Director: {getattr(movie, 'director')}")
        else:
            print("Director attribute not found.")  # Output: Director attribute not found.

    
    if created:
        return HttpResponse('created')

    return HttpResponse('get only')






from rest_framework.views import APIView
from rest_framework.response import Response
from base.renderer import CustomJSONRenderer

class MyAPIView(APIView):
    renderer_classes = [CustomJSONRenderer]

    def get(self, request):
        data = {"message": "Hello, world!"}
        return Response(data)




import csv
import uuid
import zipfile
import os
from django.http import HttpResponse
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Movie

def create_zip(zip_name, files):
    zip_file_name = f"{zip_name}{uuid.uuid4()}.zip"
    with zipfile.ZipFile(zip_file_name, 'w') as zipf:
        for file in files:
            zipf.write(file)
    return zip_file_name

def remove_file_local_directory(files):
    for file in files:
        if os.path.exists(file):
            os.remove(file)

class ExportMovieInfoView(generics.GenericAPIView):
    """API to export Movie data in CSV format inside a ZIP file."""

    # permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            files = []

            # Export Movie Data
            movie_csv_filename = f"movies_{uuid.uuid4()}.csv"
            with open(movie_csv_filename, "w", newline='') as csvfile:
                csvwriter = csv.writer(csvfile)
                csvwriter.writerow(["ID", "Title", "Description", "Release Date", "Rating", "US Gross", "Worldwide Gross", "Resource ID"])

                for movie in Movie.objects.all():
                    csvwriter.writerow([
                        movie.id, movie.title, movie.description, movie.release_date, 
                        movie.rating, movie.us_gross, movie.worldwide_gross, 
                        movie.movie_resource.id if movie.movie_resource else None
                    ])
            files.append(movie_csv_filename)

            # Create ZIP file
            zip_name = "movie_data_"
            zip_file_name = create_zip(zip_name, files)
            files.append(zip_file_name)

            # Return ZIP file as response
            response = HttpResponse(open(zip_file_name, "rb"), content_type='application/zip')
            response['Content-Disposition'] = f'attachment; filename={zip_file_name}'

            # Cleanup
            remove_file_local_directory(files)

            return response
        except Exception:
            return Response({"message": "Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



from simple_history.utils import update_change_reason

# GET & POST for Poll
class PollListCreateView(generics.ListCreateAPIView):
    queryset = Poll.objects.all()
    serializer_class = PollSerializer

    def perform_create(self, serializer):
        user = self.request.user if self.request.user.is_authenticated else None
        try:
            update_change_reason(self.request, "Created via API")
        except AttributeError as e:
            print(f"AttributeError: {e}")
            # Log the error or handle it as needed
        serializer.save(history_user=user)  # Associate history with the user


## ✅ GET single Poll & UPDATE (PUT/PATCH)
class PollRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Poll.objects.all()
    serializer_class = PollSerializer

    def perform_update(self, serializer):
        user = self.request.user if self.request.user.is_authenticated else None
        try:
            update_change_reason(self.request, "Updated via API")
        except AttributeError as e:
            print(f"AttributeError: {e}")
            # Log the error or handle it as needed
        serializer.save(history_user=user)



# 🚀 **Choice APIs**
## ✅ GET all & POST new Choice
class ChoiceListCreateView(generics.ListCreateAPIView):
    queryset = Choice.objects.all()
    serializer_class = ChoiceSerializer

    def perform_create(self, serializer):
        user = self.request.user if self.request.user.is_authenticated else None
        try:
            update_change_reason(self.request, "Created via API")
        except AttributeError as e:
            print(f"AttributeError: {e}")
            # Log the error or handle it as needed
        serializer.save(history_user=user)  # Associate history with the user





## ✅ GET single Choice & UPDATE (PUT/PATCH)
class ChoiceRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Choice.objects.all()
    serializer_class = ChoiceSerializer

    def perform_update(self, serializer):
        user = self.request.user if self.request.user.is_authenticated else None
        try:
            update_change_reason(self.request, "Updated via API")
        except AttributeError as e:
            print(f"AttributeError: {e}")
            # Log the error or handle it as needed
        serializer.save(history_user=user)


# 🚀 **History APIs**
## ✅ Fetch Poll History
class PollHistoryView(APIView):
    def get(self, request, pk):
        poll = Poll.objects.get(pk=pk)
        history = poll.history.all()
        data = [
            {
                "id": record.id,
                "question": record.question,
                "history_date": record.history_date,
                "history_user": record.history_user.username if record.history_user else None,
                "history_type": record.history_type
            }
            for record in history
        ]
        return Response(data)

## ✅ Fetch Choice History
class ChoiceHistoryView(APIView):
    def get(self, request, pk):
        choice = Choice.objects.get(pk=pk)
        history = choice.history.all()
        data = [
            {
                "id": record.id,
                "choice_text": record.choice_text,
                "votes": record.votes,
                "history_date": record.history_date,
                "history_user": record.history_user.username if record.history_user else None,
                "history_type": record.history_type
            }
            for record in history
        ]
        return Response(data)