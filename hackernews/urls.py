
from django.contrib import admin
from django.urls import path, include

from apps.core.views import signup
from apps.stories.views import frontpage, submit, latest, vote, detail, search
from django.contrib.auth import views

urlpatterns = [
    path('',frontpage,name='frontpage'),
    path('search/',search,name='search'),
    path('latest/',latest,name='latest'),
    path('s/<int:story_id>/',detail, name="detail"),
    path('s/<int:story_id>/vote/',vote, name="vote"),
    path('u/',include('apps.userprofile.urls')),
    path('submit/',submit, name="submit"),

    path('signup/',signup, name="signup"),
    path('logout/',views.LogoutView.as_view(), name="logout"),
    path('login/',views.LoginView.as_view(template_name='core/login.html'), name="login"),
    
    
    
    path('admin/', admin.site.urls),
]
