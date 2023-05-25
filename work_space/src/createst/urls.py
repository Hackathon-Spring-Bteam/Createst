from django.urls import path
from .views import  LoginView, ShowQuizView, CreateTestView, SignupView, LogoutView, UserView, OtherView, ChangeUsernameView, ChangeEmailView, ChangePasswordView,TestListView
from . import views

urlpatterns = [
    path('', TestListView.as_view(), name='index'),
    path('create/', views.CreateTestView.as_view(), name='create'),
    path('test/<uuid:test_id>/', ShowQuizView.as_view(), name='test'),
    path('accounts/login/', LoginView.as_view(), name='login'),
    path('signup/', SignupView.as_view(), name='signup'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('user/', UserView.as_view(), name='user'),
    path('other/', OtherView.as_view(), name='other'),
    path('nameup/',ChangeUsernameView.as_view(),name='nameup'),
    path('emailup/',ChangeEmailView.as_view(),name='emailup'),
    path('passwordup/',ChangePasswordView.as_view(), name='passwordup'),
    
]