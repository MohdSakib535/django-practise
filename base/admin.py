from django.contrib import admin
from base.models import Snippet,Student,Resource,Movie,Poll,Choice
from django.contrib.auth.models import User
from simple_history.admin import SimpleHistoryAdmin




class PollAdmin(SimpleHistoryAdmin):
    list_display = ('question', 'pub_date')
    history_list_display = ['question']

class ChoiceAdmin(SimpleHistoryAdmin):
    list_display = ('choice_text', 'votes', 'poll')


# Register your models here.
# admin.site.register(User)
admin.site.register(Snippet)
admin.site.register(Student)
admin.site.register(Resource)
admin.site.register(Movie,SimpleHistoryAdmin)
admin.site.register(Poll,PollAdmin)
admin.site.register(Choice,ChoiceAdmin)