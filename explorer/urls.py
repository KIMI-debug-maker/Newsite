from . import views
from django.urls import path

urlpatterns = [
    path("", views.entrance, name="entrance"),
    path("login/", views.login, name="login"),
    path("register/", views.register, name="register"),
    path("regist/", views.regist, name="regist"),
    path("forgotpassword/", views.forgot, name="forgot"),

    path("index/", views.index, name="index"),

    path("settings/", views.settings, name="user-edit"),

    path("chatting/", views.chat, name="chat"),
    path("chatterbot/", views.chatterbot, name="chatterbot"),

    path("timeline/", views.timeline, name="timeline"),
    path("analysis/", views.Analysis, name="ecommerce"),
    path("analysis/relation", views.json_data, name="relation"),

    path("perspective/", views.perspective, name="blog-detail"),

    path("inference/", views.inference, name="blog"),

    path("portfolio/", views.portfolio, name="myportfolio")

]

