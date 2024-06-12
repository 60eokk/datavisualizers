### Steps in setting up Django
( Keep in mind that if python -m does not work, try python3 -m)

1. cd to the created folder for this project
2. $ python -m pip install Django (this will create the basic files)
3. If github is already connected, in which this case it is, continue to next step
4. $ python manage.py runserver: will create port in 127.0.0.1:8000/





### Creating a project (= is also called creating an app)
$ django-admin startproject mysite (change mysite to my namings)

If I created an app called "polls", files will be created automtically under polls folder
Next, inside polls/view.py
#####
from django.http import HttpResponse
def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")
######

and inside polls/urls.py
#####
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
]
#####

and modify mysite/urls.py to
#####
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("polls/", include("polls.urls")),
    path("admin/", admin.site.urls),
]
#####

The include() function allows referencing other URLconfs.
