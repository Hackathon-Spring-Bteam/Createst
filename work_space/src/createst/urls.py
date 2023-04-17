from django.urls import path
from .views import IndexView, LoginView, SignupView, LogoutView, UserView, OtherView

urlpatterns = [
    path('index/', IndexView.as_view(), name='index'),
    path('login/', LoginView.as_view(), name='login'),
    path('signup/', SignupView.as_view(), name='signup'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('user/', UserView.as_view(), name='user'),
    path('other/', OtherView.as_view(), name='other'),
]