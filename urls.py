"""
URL configuration for language project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from language import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
urlpatterns = [
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("admin/", admin.site.urls),
    path("api/index/", views.index, name="index"),

    path("api/courses/", views.courses, name="courses"),
    path("api/courses/<int:id>", views.course, name="course"),
    path("api/session/<int:id>", views.session, name="session"),
    path("api/section/<int:id>", views.section, name="section"),
    path("api/register/", views.register, name="register"),


    

    
    path("api/questions/", views.questionView, name="questionView"),

    



    #path("api/blog/", views.blog, name="blog"),
    path("api/blog/<int:id>", views.blogDetails, name="blogDetails"),

    
    #path("api/workspace/", views.workspace, name="workspace"),

]
