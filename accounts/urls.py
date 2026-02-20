from django.urls import path
from . import views

app_name = 'accounts'


urlpatterns = [
    path("users/register/", views.UserCreateView.as_view(), name="user_create"),
    path("users/", views.UserListView.as_view(), name="user_list"),
    path("users/user_detail/<int:pk>/", views.UserDetailView.as_view(), name="user_detail"),
    path("users/user_update/<int:pk>/", views.UserUpdateView.as_view(), name="user_update"),
    path("users/user_delete/<int:pk>/", views.UserDeleteView.as_view(), name="user_delete"),
    
    
    path("students/", views.StudentListView.as_view(), name="student_list"),
    path("students/create/", views.StudentCreateView.as_view(), name="student_create"),
    path("students/create/class/<int:pk>/", views.StudentClassView.as_view(), name="student_class"),
    path("students/student_detail/<int:pk>/", views.StudentDetailView.as_view(), name="student_detail"),
    path("students/student_update_user/<int:pk>/", views.StudentAccountUpdateView.as_view(), name="student_update_user"),
    path("students/student_update_class/<int:pk>/", views.StudentClassUpdateView.as_view(), name="student_update_class"),
    path("students/student_delete/<int:pk>/", views.StudentDeleteView.as_view(), name="student_delete"),
    path("students/student_add_result/", views.StudentAddResultView.as_view(), name="student_add_result"),
    path("students/student_add_attendance/", views.StudentAddAttendanceView.as_view(), name="student_add_attendance"),
    path("students/student_result_list/", views.StudentResultListView.as_view(), name="student_result_list"),
]
