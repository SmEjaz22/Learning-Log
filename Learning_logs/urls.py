""" We create this new file urls.py inside our app which
Defines URL patterns for Learning_logs  """
from django.urls import path
from . import views

app_name='Learning_logs'

# **app_name** is a predefined variable in Django that
# the framework uses specifically to recognize the namespace for
# URL patterns in an app. It must be spelled exactly as app_name,
# and any variations like app_names, appname, or appnames will not work.


urlpatterns = [ # a list of individual pages that can be requested from the learning_logs app.
    # Home page
    path('', views.index,name='indexx'),
    # 3 para: URL, Which fn(here index fn) to call in views, Name index for URL pattern for easy refer.
    path('topics',views.topics,name='topics'),
    
    #creating individual topics their own page.
    path('topics/<int:topic_id_from_url>/',views.topic, name='topic'),
    # The first part of the string tells Django to look for URLs that have the word
    # topics after the base URL(localhost for now). The second part of the string, /<int:topic_id>/, 
    # matches an integer between two forward slashes and assigns the integer value to an argument
    # called topic_id.
    
    # Page for adding a new topic.
    path('new_topic/', views.new_topic, name='new_topic'),
    
    # Page for adding a new entry.
    path('new_entry/<int:topic_id>/', views.new_entry, name='new_entry'),
    
    # Page for editing an entry.
    path('edit_entry/<int:entry_id>/', views.edit_entry, name='edit_entry'),
    
    path('Entry_versions/<int:entry_id>',views.entry_versions,name="entry_versions"),
    
    path('delete_topic/<int:topic_id_from_url>/', views.delete_topic, name='delete_topic'),
]
