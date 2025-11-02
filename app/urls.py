from django.urls import path
from app.views import signupview


urlpatterns = [
    path('signup/', signupview),

]   