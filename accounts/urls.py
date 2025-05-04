from django.urls import path

from .views import signin, signup, logout_user, delete_account

urlpatterns = [
    path('signin/', signin, name='signin'),
    path('signup/', signup, name='signup'),
    path('logout/', logout_user, name='logout_user'),
    path('delete-account/', delete_account, name='delete_account'),

]