from django.urls import path
from . import views

app_name = "tasks"

urlpatterns = [
    path("my-tasks/", views.my_tasks,name="my_tasks"),
    path("notifications/read-all/", views.mark_all_notifications_read, name="mark_all_notifications_read"),
    path("notifications/<int:pk>/read/", views.mark_notification_read, name="mark_notification_read"),
    path("task/<int:task_id>/", views.task_detail, name="task_detail"),
    path("task/<int:task_id>/submit/", views.submit_task, name="submit_task"),
]