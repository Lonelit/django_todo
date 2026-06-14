from django.urls import path
from .views import (about, register_view, login_view,
                    todo_list_view, logout_view, todo_create_view,
                    todo_detail_view, todo_edit_view, todo_delete_view)


urlpatterns = [
    path('register/', register_view, name="register"),
    path('login/', login_view, name="login"),
    path('logout/', logout_view, name="logout"),

    path('todo/', todo_list_view, name="todo_list"),
    path('new/', todo_create_view, name="todo_create"),
    path('todo/<int:pk>/', todo_detail_view, name="todo_detail"),
    path('todo/<int:pk>/edit', todo_edit_view, name="todo_edit"),
    path('todo/<int:pk>/delete', todo_delete_view, name="todo_delete"),

    path('about/', about, name="about"),

]
