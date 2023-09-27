from django.urls import path
from .views import Signin, Signup, Logout

app_name = 'users'

urlpatterns = [
    path('signup/', Signup.as_view(), name='signup'),
    path('signin/', Signin.as_view(), name='signin'),
    path('logout/', Logout.as_view(), name='logout'),
]