from django.urls import path
from . import views

app_name="recommend_app"
urlpatterns = [
    path("",views.IndexView.as_view(),name="index"),
    path("about",views.about,name="about"),
    path("input",views.input,name="input"),
    path("input_women",views.input_women,name="input_women"),
    path("result",views.result,name="result"),
    path("result_women",views.result_women,name="result_women"),
]