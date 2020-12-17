"""yavs_python URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
import debug_toolbar
from django.conf import settings
from django.urls import include, path
from yavs.views import Home, UploadVideo, SignIn, SignUp, VideoPlayer, PostComment, SignOut, UserProfile, ViewInsights, About
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('__debug__/', include(debug_toolbar.urls)),
    path('', Home.as_view()),
    path('upload_video', UploadVideo.as_view()),
    path('sign_in', SignIn.as_view()),
    path('sign_up', SignUp.as_view()),
    path('video_player/<int:id>', VideoPlayer.as_view()),
    path('view_insights/<int:id>', ViewInsights.as_view()),
    path('comment', PostComment.as_view()),
    path('sign_out', SignOut.as_view()),
    path('user_profile/<str:user_requested>', UserProfile.as_view()),
    path('django-rq/', include('django_rq.urls')),
    path('about/', About.as_view()),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


# Adding debug_toolbar


if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        
    ] + urlpatterns
