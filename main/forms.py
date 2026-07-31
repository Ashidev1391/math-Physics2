from django import forms
from .models import Book, Score, Homework


class BookForms(forms.ModelForm):

    class Meta:
        model = Book
        fields = ['title', 'description',
                  'category', 'preview_image', 'pdf_file']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'preview_image': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'pdf_file': forms.FileInput(attrs={'class': 'form-control', 'accept': 'application/pdf'}),
        }
        labels = {'title': 'عنوان جزوه', 'description': 'توضیحات کوتاه', 'category': 'دسته‌بندی',
                  'preview_image': 'تصویر پیش‌نمایش جزوه', 'pdf_file': 'فایل PDF', }


class ScoreForms(forms.ModelForm):
    class Meta:
        model = Score
        fields = ['student', 'grade', 'classroom', 'subject', 'score']

        widgets = {
            'student': forms.Select(attrs={'class': 'form-select'}),
            'grade': forms.Select(attrs={'class': 'form-select'}),
            'classroom': forms.Select(attrs={'class': 'form-select'}),
            'subject': forms.Select(attrs={'class': 'form-select'}),
            'score': forms.NumberInput(attrs={'class': 'form-control'}),
        }

        labels = {
            'student': 'دانش‌آموز',
            'grade': 'پایه',
            'classroom': 'کلاس',
            'subject': 'درس',
            'score': 'نمره',
        }

class AttendanceForm(forms.Form):
    status = forms.ChoiceField(
        choices=[
            ("present", "حاضر"),
            ("absent", "غایب")
        ],
        widget=forms.RadioSelect
    )

class HomeworkForm(forms.ModelForm):

    class Meta:
        model = Homework
        fields = ["subject","body","classroom","deadline",]
        labels = {"subject": "عنوان تکلیف","body": "متن تکلیف","classroom": "کلاس","deadline": "مهلت تحویل",}
        widgets = {
            "subject": forms.TextInput(attrs={"class": "form-control","placeholder": "مثلاً تمرین فصل دوم فیزیک"}),
            "body": forms.Textarea(attrs={"class": "form-control","rows": 5,"placeholder": "توضیحات تکلیف..."}),
            "classroom": forms.Select(attrs={"class": "form-select"}),
            "deadline": forms.DateInput(attrs={"class": "form-control","type": "date"}),
        }