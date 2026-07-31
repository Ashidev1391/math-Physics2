from django.contrib import admin
from . import models

# نمایش مدل در ادمین
admin.site.register(models.Category)
admin.site.register(models.Book)
admin.site.register(models.profile)
admin.site.register(models.Classroom)
admin.site.register(models.Student)
admin.site.register(models.Homework)
admin.site.register(models.Cat_book)
admin.site.register(models.Score)
admin.site.register(models.Grade)
admin.site.register(models.Attendance)
