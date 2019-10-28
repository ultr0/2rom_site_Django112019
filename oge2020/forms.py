from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
#from oge2020.models import User

from oge2020 import models
 
class UserForm(forms.Form):
    name = forms.CharField(min_length=3)
    age = forms.IntegerField(min_value=1, max_value=100)
    
class TestAnswerForm(forms.Form):
    answ = forms.CharField(min_length=50)

class ReplyForm(forms.Form):
    answer = forms.IntegerField()

    
## ������ ���������    
class BootstrapClassForm:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
    
class StudentTestForm(BootstrapClassForm, forms.ModelForm):
    class Meta:
        #model = models.StudentTest
        exclude = (
            'created_time',
            'modified_time',
            'points',
            'checked'
        )
        
# class StudentAnswerForm(BootstrapClassForm, forms.ModelForm):
    # question = forms.ModelChoiceField(
        # queryset=models.StudentTestQuestion.objects.all(),
        # widget=forms.HiddenInput()
    # )
    # answers = forms.ModelMultipleChoiceField(queryset=models.Answer.objects.all(), required=False)

    # class Meta:
        # model = models.StudentAnswer
        # fields = ['question', 'answers', 'text']



# REGISTRATION
class MyForm(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text='Required')
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

# PROFILE
class profileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
 

# class BootstrapClassForm:
    # def __init__(self, *args, **kwargs):
        # super().__init__(*args, **kwargs)
        # for visible in self.visible_fields():
            # visible.field.widget.attrs['class'] = 'form-control'

# class SignUpForm(BootstrapClassForm, UserCreationForm):
    # first_name = forms.CharField(max_length=30, required=True, label='Name')
    # last_name = forms.CharField(max_length=30, required=True, label='LastName')
    # middle_name = forms.CharField(max_length=30, required=False, label='Middle Name')
    # is_staff = forms.BooleanField(initial=True, widget=forms.HiddenInput())

    # class Meta:
        # model = models.Student
        # fields = (
            # 'username',
            # 'first_name',
            # 'last_name',
            # 'middle_name',
            # 'password1',
            # 'password2',
            # 'is_staff'
        # )


# class StudentTestForm(BootstrapClassForm, forms.ModelForm):
    # class Meta:
        # model = models.StudentTest
        # exclude = (
            # 'created_time',
            # 'modified_time',
            # 'points',
            # 'checked'
        # )


# class StudentAnswerForm(BootstrapClassForm, forms.ModelForm):
    # question = forms.ModelChoiceField(
        # queryset=models.StudentTestQuestion.objects.all(),
        # widget=forms.HiddenInput()
    # )
    # answers = forms.ModelMultipleChoiceField(queryset=models.Answer.objects.all(), required=False)

    # class Meta:
        # model = models.StudentAnswer
        # fields = ['question', 'answers', 'text']