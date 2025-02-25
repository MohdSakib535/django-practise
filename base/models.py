from django.db import models
from django.contrib.auth.models import User
from pygments.lexers import get_all_lexers
from pygments.styles import get_all_styles
from django.utils.translation import gettext_lazy as _

# Create your models here.

LEXERS = [item for item in get_all_lexers() if item[1]]
LANGUAGE_CHOICES = sorted([(item[1][0], item[0]) for item in LEXERS])
STYLE_CHOICES = sorted([(item, item) for item in get_all_styles()])


class Snippet(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, blank=True, default='')
    code = models.TextField()
    linenos = models.BooleanField(default=False)
    language = models.CharField(choices=LANGUAGE_CHOICES, default='python', max_length=100)
    style = models.CharField(choices=STYLE_CHOICES, default='friendly', max_length=100)
    user_data=models.ForeignKey(User,on_delete=models.CASCADE,related_name='%(app_label)s_%(class)s_user_Data')

    class Meta:
        ordering = ['created']


class Student(models.Model):
    class YearInSchool(models.TextChoices):
        FRESHMAN = "FR", _("Freshman")
        SOPHOMORE = "SO", _("Sophomore")
        JUNIOR = "JR", _("Junior")
        SENIOR = "SR", _("Senior")
        GRADUATE = "GR", _("Graduate")

    year_in_school = models.CharField(
        max_length=2,
        choices=YearInSchool,
        default=YearInSchool.FRESHMAN,
    )

    def is_upperclass(self):
        return self.year_in_school in {
            self.YearInSchool.JUNIOR,
            self.YearInSchool.SENIOR,
        }
    


class Resource(models.Model):
    title = models.CharField(max_length=256)
    content = models.TextField()
    liked_by = models.ManyToManyField(to=User)
    snippet_data=models.ForeignKey(Snippet,on_delete=models.CASCADE,related_name='%(app_label)s_%(class)s_snippet_data')

    # class Meta:
    #     permissions=[
    #         ("view_resource", "Can view resource"),
    #         ("special_permission", "Can perform special action"),
    #     ]
    

    def __str__(self):
        return f'{self.title}'
    
from django.utils.functional import cached_property

class Movie(models.Model):
    title = models.CharField(max_length=128)
    description = models.TextField(max_length=2048)
    release_date = models.DateField()
    rating = models.PositiveSmallIntegerField()
    us_gross = models.IntegerField(default=0)
    worldwide_gross = models.IntegerField(default=0)
    movie_resource=models.ForeignKey(Resource,on_delete=models.CASCADE,related_name='%(app_label)s_%(class)s_movie_resource',null=True,blank=True)




    def __str__(self):
        return f'{self.title}'
    
    @cached_property
    def movie_title_with_description(self):
        return f"{self.title} and {self.description}"


    @property
    def new_description(self):
        return f"{self.title} and {self.description}"



    