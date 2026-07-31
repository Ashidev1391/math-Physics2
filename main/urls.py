from django.urls import path
from . import views

app_name = 'main'
urlpatterns = [
    path('', views.home, name='home'),
    path('physics', views.physics, name="physics"),
    path('math', views.math_calc, name="math"),
    path('show_book', views.appear_book, name="show_book"),
    path('help', views.help, name="help"),
    path('dashboard', views.dashboard, name="dashboard"),
    path('stu_list', views.stu_list, name="stu_list"),
    path('homework', views.homework, name="homework"),
    path('add_grade', views.add_grade, name="add_grade"),
    path("student-dashboard/", views.student_dashboard, name="student_dashboard"),
    path("add-homework/",views.add_homework,name="add_homework"),
    path("book/<int:id>/", views.book_detail, name="book_detail"),
    path("student/<int:id>/", views.student_detail, name="student_detail"),
    path("attendance/<int:classroom_id>/",
         views.attendance_page, name="attendance"),
]
