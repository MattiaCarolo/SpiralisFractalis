from django.urls import path

from evalfract.views import ImageView

urlpatterns = [
    path("Images", ImageView.as_view()),
]