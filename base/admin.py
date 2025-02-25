from django.contrib import admin
from base.models import Snippet,Student,Resource,Movie
from django.contrib.auth.models import User

# Register your models here.
# admin.site.register(User)
admin.site.register(Snippet)
admin.site.register(Student)
admin.site.register(Resource)
admin.site.register(Movie)