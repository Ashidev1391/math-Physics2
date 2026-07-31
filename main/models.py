from django.db import models
from django.contrib.auth.models import User
import jdatetime


class Category(models.Model):
    name = models.CharField(max_length=20)
    en_name = models.CharField(max_length=25)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Book(models.Model):
    class StatusChoices(models.TextChoices):
        PENDING = 'pending', 'منتظر تأیید'
        APPROVED = 'approved', 'تأیید شده'
        REJECTED = 'rejected', 'رد شده'

    title = models.CharField(max_length=50, blank=False)
    description = models.TextField(blank=False)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, blank=False)
    pdf_file = models.FileField(upload_to='pdfs/', blank=False)
    # تصویر صفحه اول یا پیش نمایش جزوه
    preview_image = models.ImageField(upload_to='jpgs/', blank=True, null=True)
    status = models.CharField(
        max_length=10, choices=StatusChoices.choices, default=StatusChoices.PENDING)

    def __str__(self):
        return self.title


class profile(models.Model):
    ROLE_CHOICES = [
        ('teacher', 'معلم'),
        ('student', 'دانش‌آموز'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    def __str__(self):
        return self.user.username


class Classroom(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Grade(models.Model):
    grade = models.CharField(max_length=20)

    def __str__(self):
        return self.grade


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    classroom = models.ForeignKey(
        Classroom, on_delete=models.CASCADE, verbose_name="کلاس")
    grade = models.ForeignKey(
        Grade, on_delete=models.CASCADE, verbose_name='پایه', default=9)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Homework(models.Model):
    subject = models.CharField(max_length=50, verbose_name="عنوان")
    body = models.TextField(verbose_name="متن تکلیف")
    classroom = models.ForeignKey(
        Classroom,
        on_delete=models.CASCADE,
        verbose_name="کلاس"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="تاریخ ثبت"
    )
    deadline = models.DateField(
        verbose_name="مهلت تحویل"
    )

    def created_at_jalali(self):
        return jdatetime.datetime.fromgregorian(
            datetime=self.created_at
        ).strftime("%Y/%m/%d")

    def deadline_jalali(self):
        return jdatetime.date.fromgregorian(
            date=self.deadline
        ).strftime("%Y/%m/%d")

    def __str__(self):
        return self.subject


class Cat_book(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Score(models.Model):
    STATUS_CHOICES = [
        ("pending", "در انتظار تایید"),
        ("approved", "تایید شده"),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE)
    classroom = models.ForeignKey(
        Classroom, on_delete=models.CASCADE, blank=True)
    subject = models.ForeignKey(Cat_book, on_delete=models.CASCADE)
    score = models.FloatField()
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="pending")

    def __str__(self):
        return f"{self.student} - {self.subject}"

class Attendance(models.Model):
    STATUS = [
        ("present", "حاضر"),
        ("absent", "غایب"),
    ]

    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE
    )

    classroom = models.ForeignKey(
        Classroom,
        on_delete=models.CASCADE
    )

    date = models.DateField(auto_now_add=True)

    time = models.TimeField(auto_now_add=True)

    status = models.CharField(
        max_length=10,
        choices=STATUS
    )


    def date_jalali(self):
        return jdatetime.date.fromgregorian(
            date=self.date
        ).strftime("%Y/%m/%d")


    def __str__(self):
        return f"{self.student} - {self.date}"