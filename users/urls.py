from django.urls import path
from .views import RegisterView,LoginView,UserView,LogoutView,ProfileUpdateView,UsersListView,DeleteUserView,AddUser,Predictor

urlpatterns = [
    path('register', RegisterView.as_view(), name='register'),
    path('login', LoginView.as_view(), name='login'),
    path('user/', UserView.as_view(), name='user-detail'),
    path('profile-update/<str:email>', ProfileUpdateView.as_view(), name='profile_update'),
    path('delete-user/<str:email>', DeleteUserView.as_view(), name='delete_user'),
    path('users-list', UsersListView.as_view(), name='users_list'),
    path('add-user/', AddUser.as_view(), name='add_user'),
    path('predictor/', Predictor.as_view(), name='predictor'),

    path('logout', LogoutView.as_view(), name='logout'),
]


