from django.urls import path
from .views import IndexView, LoginView, SignupView, LogoutView, UserView, OtherView,ChangeUsernameView,ChangeEmailView
from .views import IndexView, CreateTestView, ShowQuizView, LoginView, SignupView
from . import views

urlpatterns = [
    path('index/', IndexView.as_view(), name='index'),
    path('create/', views.CreateTestView.as_view(), name='create'),
    path('test/<uuid:test_id>/', ShowQuizView.as_view(), name='test'),
    path('login/', LoginView.as_view(), name='login'),
    path('signup/', SignupView.as_view(), name='signup'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('user/', UserView.as_view(), name='user'),
    path('other/', OtherView.as_view(), name='other'),
    path('nameup/',ChangeUsernameView.as_view(),name='nameup'),
    path('emailup/',ChangeEmailView.as_view(),name='emailup'),
]