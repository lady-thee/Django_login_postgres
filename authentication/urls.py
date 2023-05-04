from django.urls import path 
from .views import loadLoginPage, loadSignUpPage, loadTokenPage, loadSuccessPage

urlpatterns = [
    path('', loadLoginPage, name='login'),
    path('signup/', loadSignUpPage, name='signup'),
    path('token/', loadTokenPage, name='token'),
    path('success/', loadSuccessPage, name='success')
]