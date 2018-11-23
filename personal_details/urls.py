from django.urls import path

urlpatterns = [
    path('', view.index, name = 'index'),
]
