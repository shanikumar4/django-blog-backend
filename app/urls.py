from django.urls import path
from app.views import signupview, loginview, logoutview, createblog,readblog, updateblog, deleteblog, userdetails, trash, restore, deletetrash


urlpatterns = [
    path('signup/', signupview),
    path('login/', loginview),
    path('details/', userdetails),
    path('logout/', logoutview),
    path('addblog/', createblog),
    path('readblog/', readblog),
    path('update/', updateblog),
    path('delete/', deleteblog),
    path('trash/', trash),
    path('restore/', restore),
    path('deletetrash/', deletetrash ),
]   