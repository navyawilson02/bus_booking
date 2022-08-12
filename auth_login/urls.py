from django.urls import path

from .views import signin, log_out, signup, Google_login, signup_succ


urlpatterns = [
    path('login/', signin),
    path('signup_succ/', signup_succ),
    path('logout/', log_out),
    path('signup/', signup),
    path('google-login/', Google_login),

]